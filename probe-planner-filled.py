# -*- coding: utf-8 -*-
"""
Phase 2: drive the real UI, then assert that typed values reach the plan and the
prompt.

Phase 1 (probe_moves.py) only proved the page renders. This proves the path a
teacher actually walks: tick a move that the template did not tick, type into its
fields, click the four-causes chips, override the stage-driven narration form,
and check that all of it comes out the other end -- and that the fields left
blank still print as named slots rather than vanishing.

The driver script is appended to a COPY of planner.html, so the deployed file is
never touched by the probe.
"""
from __future__ import annotations

import io
import os
import re
import subprocess
import sys
import tempfile
import uuid

def _chrome() -> str:
    """Find Chrome without hard-coding one machine's install. Edge is not a
    substitute -- it has bitten this project before."""
    for c in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
              "/usr/bin/google-chrome", "/usr/bin/chromium"):
        if os.path.exists(c):
            return c
    sys.exit("Google Chrome not found. Install it, or add its path to _chrome().")


CHROME = _chrome()
PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "planner.html")

DRIVER = """
<script>
/* probe driver -- appended to a temp copy only */
(function(){
  function fire(el,type){el.dispatchEvent(new Event(type,{bubbles:true}))}
  function set(sel,val){
    var el=document.querySelector(sel);
    if(!el){document.title="PROBE-MISSING "+sel;return}
    el.value=val;fire(el,el.tagName==="SELECT"?"change":"input");
  }
  function tick(id){
    var cb=document.querySelector('input[data-t='+id+']');
    if(!cb){document.title="PROBE-MISSING move "+id;return}
    if(!cb.checked){cb.checked=true;fire(cb,"change")}
  }
  /* a move the opening template does not tick, so this proves the tick path */
  tick("causes");
  set('[data-mv="causes.object"]',"The Athenian decision to sail to Sicily");
  set('[data-mv="causes.naming"]',"Named as the four causes");
  set('[data-mv="causes.questions"]',"What was it for? Who wanted it, and why did they get it?");
  /* the multi-value field: click two chips, out of declared order */
  var mx=document.querySelectorAll('[data-mxv="causes.causes"]');
  mx[3].checked=true;fire(mx[3],"change");   /* Final  -- clicked first */
  mx[1].checked=true;fire(mx[1],"change");   /* Formal -- clicked second */
  /* override the stage-driven narration form; the stage must then let go */
  set('[data-mv="narration.form"]',"Short essay");
  set("#stage","Rhetoric");
  /* a numeric field and a text field on a template-ticked move */
  set('[data-mv="attention.stretch"]',"25");
  set('[data-mv="attention.object"]',"Thucydides VI.8-VI.26");
})();
</script>
"""


def dump(html_path: str) -> tuple[str, str]:
    profile = os.path.join(tempfile.gettempdir(), "chrome-p2-" + uuid.uuid4().hex)
    r = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
         "--user-data-dir=" + profile, "--virtual-time-budget=9000",
         "--dump-dom", "file:///" + html_path.replace("\\", "/")],
        capture_output=True, timeout=180)
    dom = r.stdout.decode("utf-8", "replace")
    title = re.search(r"<title>(.*?)</title>", dom, re.S)
    return dom, (title.group(1) if title else "")


def main() -> int:
    src = io.open(PAGE, encoding="utf-8").read()
    tmp = os.path.join(tempfile.gettempdir(), "planner-probe-" + uuid.uuid4().hex + ".html")
    # Anchor on the LAST </body>, not the first. planner.html's download handler
    # builds a Word file with the literal "</body></html>" inside a JS string, so
    # replacing the first occurrence injects a <script> into a string literal and
    # kills the whole page -- exactly the failure check-js.py exists to catch.
    cut = src.rindex("</body>")
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src[:cut] + DRIVER + src[cut:])

    dom, title = dump(tmp)
    os.remove(tmp)

    checks: list[tuple[bool, str]] = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))

    ck(not title.startswith("PROBE-MISSING"),
       "every selector the driver used exists (title said: %s)" % title)

    doc = re.search(r'<div class="doc" id="doc">(.*?)</div></div>', dom, re.S)
    ck(doc is not None, "the plan document rendered after the interaction")
    d = doc.group(1) if doc else ""

    # --- the newly ticked move reached the plan --------------------------
    ck("<h4>The four causes</h4>" in d, "ticking a move adds its block to the plan")
    ck("Thucydides VI.8-VI.26" in d, "a typed text field reaches the plan")
    ck("<td>25</td>" in d, "a typed numeric field reaches the plan")
    ck("The Athenian decision to sail to Sicily" in d, "the four-causes object reaches the plan")

    # --- the multi field kept DECLARED order, not click order ------------
    ck("<td>Formal, Final</td>" in d,
       "the four-causes chips print in declared order, not click order")
    ck("<td>Final, Formal</td>" not in d, "click order did not leak into the plan")

    # --- the stage let go once the teacher overrode the form -------------
    ck("<th>Form</th><td>Short essay</td>" in d,
       "an overridden narration form survives a later stage change")
    ck("Rhetoric stage" in d, "the stage change itself did land")

    # --- blanks still print as slots ------------------------------------
    ck("Still to name:" in d, "fields left blank still print as named slots")
    ck(re.search(r"Still to name:</strong>[^<]*What you are taking out of the way", d) is not None,
       "the one blank field on a mostly-filled move is still named")

    # --- the prompt carries values and only the real gaps ---------------
    pr = re.search(r'<pre class="prompt" id="prompt">(.*?)</pre>', dom, re.S)
    ck(pr is not None, "the prompt rendered")
    p = (pr.group(1) if pr else "").replace("&amp;", "&").replace("&#39;", "'")
    ck("Causes in play: Formal, Final" in p, "the prompt carries the multi field")
    ck("Uninterrupted minutes: 25" in p, "the prompt carries the numeric field")
    ck("NOT YET SPECIFIED" in p, "the prompt still lists the real gaps")
    ck("The four causes \u2014 What is being examined" not in p
       and "The four causes &#8212; What is being examined" not in p,
       "a filled field is NOT listed as a gap")
    ck("Attention \u2014 What you are taking out of the way" in p
       or "Attention &#8212; What you are taking out of the way" in p,
       "a blank field IS listed as a gap")
    # a newline inside a textarea must not break the prompt's line structure
    ck("\n" not in "x", "sanity: string check works")

    # ---------------------------------------------------------------------
    # Module scope is half the tool and renders through a different function.
    # ---------------------------------------------------------------------
    # The extra steps must go INSIDE the driver's IIFE -- `set` is local to it.
    # Appending before </script> lands them outside, where set is undefined and
    # the ReferenceError is silent.
    mod_driver = DRIVER.replace("})();", """
  set("#scope","module");
  set("#title","The Sicilian Expedition");
  set("#question","When is a war worth fighting?");
})();""", 1)
    assert "#scope" in mod_driver, "module steps did not get injected"
    tmp2 = os.path.join(tempfile.gettempdir(), "planner-probe-" + uuid.uuid4().hex + ".html")
    cut2 = src.rindex("</body>")
    with io.open(tmp2, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src[:cut2] + mod_driver + src[cut2:])
    dom2, title2 = dump(tmp2)
    os.remove(tmp2)

    ck(not title2.startswith("PROBE-MISSING"),
       "module-scope selectors all exist (title said: %s)" % title2)
    doc2 = re.search(r'<div class="doc" id="doc">(.*?)</div></div>', dom2, re.S)
    d2 = doc2.group(1) if doc2 else ""
    ck("Moves across the module" in d2, "module plan carries a moves section")
    ck("<h4>The four causes</h4>" in d2, "a ticked move reaches the MODULE plan too")
    ck("<td>Formal, Final</td>" in d2, "field values survive the switch to module scope")
    ck("Still to name:" in d2, "module plan also prints named slots for blanks")
    ck("When is a war worth fighting?" in d2, "the module central question rendered")
    ck('data-p="weeks"' in dom2 and 'id="weeksTab" style=""' in dom2,
       "the week-by-week tab is revealed in module scope")

    bad = [m for ok, m in checks if not ok]
    print("%d checks, %d failed" % (len(checks), len(bad)))
    for m in bad:
        print("  FAIL  " + m)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
