# -*- coding: utf-8 -*-
"""
Probe persistence: the autosave and the plan code.

Two things neither existing probe can reach:

  autosave   needs TWO page loads sharing one browser profile AND one origin.
             So a single local server stays up across both Chrome runs -- a new
             port would be a new origin and localStorage would not carry over.
             file:// cannot be used: Chrome treats it as an opaque origin and
             localStorage there is unreliable, which is why saveNow() is wrapped
             in try/catch in the first place.

  plan code  encode -> mutate everything -> paste the original back -> assert the
             original returned. Re-applying a state onto itself would pass even
             if applyState did nothing, so the mutation step is the test.

The standards round-trip is the part most likely to break, because the bundle is
fetched asynchronously and the fetch clears `picked`. It is asserted explicitly.
"""
from __future__ import annotations

import http.server
import io
import os
import re
import socketserver
import subprocess
import sys
import tempfile
import threading
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))


def _chrome() -> str:
    for c in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
              "/usr/bin/google-chrome", "/usr/bin/chromium"):
        if os.path.exists(c):
            return c
    sys.exit("Google Chrome not found.")


CHROME = _chrome()

# --- load 1: build a distinctive plan, then report the code ----------------
FILL = r"""
<script>
(function(){
  var LOG=[];
  window.onerror=function(m){LOG.push("JSERROR: "+m)};
  function fire(el,t){el.dispatchEvent(new Event(t,{bubbles:true}))}
  function click(el){if(el)el.dispatchEvent(new MouseEvent("click",{bubbles:true}))}
  function set(s,v){var el=document.querySelector(s);
    if(!el){LOG.push("MISSING "+s);return}
    el.value=v;fire(el,el.tagName==="SELECT"?"change":"input")}
  function tick(id){var cb=document.querySelector('input[data-t='+id+']');
    if(!cb){LOG.push("MISSING move "+id);return}
    if(!cb.checked){cb.checked=true;fire(cb,"change")}}

  set("#title","SENTINEL Sicilian Expedition");
  set("#stage","Rhetoric");
  set("#len","SENTINEL 3 weeks");
  set("#roster","41");
  tick("causes"); tick("iconic");
  set('[data-mv="causes.object"]',"SENTINEL the decision to sail");
  set('[data-mv="iconic.experiment"]',"SENTINEL Eratosthenes and the shadows");
  set('[data-mv="narration.form"]',"Short essay");

  // a standard, which is the async part of restore
  var tries=0,iv=setInterval(function(){
    tries++;
    var cbs=document.querySelectorAll('#stdList input[type=checkbox]');
    if(!cbs.length&&tries<80)return;
    clearInterval(iv);
    if(cbs.length){cbs[0].checked=true;fire(cbs[0],"change");
      LOG.push("stdcode="+cbs[0].dataset.code)}
    else LOG.push("NO STANDARDS LOADED");

    // module scope, a renamed track and a filled cell
    set("#scope","module");
    set("#quarter","SENTINEL Q3");
    setTimeout(function(){
      var cell=document.querySelector('#weekGrid [data-cell]');
      if(cell){cell.value="SENTINEL week one";fire(cell,"input")}
      else LOG.push("MISSING week cell");
      // regenerate + expose the code
      click(document.querySelector("#copyCode"));
      setTimeout(function(){
        var box=document.querySelector("#stateCode");
        document.body.setAttribute("data-code",box?box.value:"");
        document.body.setAttribute("data-log",LOG.join(" | "));
      },250);
    },250);
  },100);
})();
</script>
"""

# --- load 2: assert the autosave brought it all back -----------------------
ASSERT = r"""
<script>
(function(){
  var LOG=[];
  window.onerror=function(m){LOG.push("JSERROR: "+m)};
  var tries=0,iv=setInterval(function(){
    tries++;
    var t=document.querySelector("#title");
    var cbs=document.querySelectorAll('#stdList input[type=checkbox]:checked');
    var ready=t&&t.value.indexOf("SENTINEL")>=0&&cbs.length;
    if(!ready&&tries<80)return;
    clearInterval(iv);
    function v(s){var el=document.querySelector(s);return el?el.value:"(missing)"}
    LOG.push("title="+v("#title"));
    LOG.push("stage="+v("#stage"));
    LOG.push("len="+v("#len"));
    LOG.push("roster="+v("#roster"));
    LOG.push("scope="+v("#scope"));
    LOG.push("quarter="+v("#quarter"));
    LOG.push("causesobj="+v('[data-mv="causes.object"]'));
    LOG.push("iconic="+v('[data-mv="iconic.experiment"]'));
    LOG.push("nform="+v('[data-mv="narration.form"]'));
    var ticked=[];
    Array.prototype.forEach.call(
      document.querySelectorAll('input[type=checkbox][data-t]'),
      function(cb){if(cb.checked)ticked.push(cb.dataset.t)});
    LOG.push("ticks="+ticked.join(","));
    LOG.push("stdchecked="+document.querySelectorAll('#stdList input:checked').length);
    var cell=document.querySelector('#weekGrid [data-cell]');
    LOG.push("cell="+(cell?cell.value:"(no grid)"));
    document.body.setAttribute("data-log",LOG.join(" | "));
  },100);
})();
</script>
"""

# --- single load: code survives being overwritten -------------------------
CODE_RT = r"""
<script>
(function(){
  var LOG=[];
  window.onerror=function(m){LOG.push("JSERROR: "+m)};
  function fire(el,t){el.dispatchEvent(new Event(t,{bubbles:true}))}
  function click(el){if(el)el.dispatchEvent(new MouseEvent("click",{bubbles:true}))}
  function set(s,v){var el=document.querySelector(s);
    if(!el){LOG.push("MISSING "+s);return}
    el.value=v;fire(el,el.tagName==="SELECT"?"change":"input")}

  // state A
  set("#title","STATE-A title");
  set("#stage","Logic");
  var cb=document.querySelector('input[data-t=copia]');
  if(cb){cb.checked=true;fire(cb,"change")}
  set('[data-mv="copia.count"]',"12");

  setTimeout(function(){
    click(document.querySelector("#copyCode"));
    var codeA=document.querySelector("#stateCode").value;
    LOG.push("codelen="+codeA.length);

    // now destroy it: different title, different stage, untick copia
    set("#title","STATE-B WRONG");
    set("#stage","Grammar");
    var c2=document.querySelector('input[data-t=copia]');
    if(c2&&c2.checked){c2.checked=false;fire(c2,"change")}
    set('[data-mv="copia.count"]',"999");
    LOG.push("mutated="+document.querySelector("#title").value);

    // paste A back
    click(document.querySelector("#openCode"));          // arm
    var box=document.querySelector("#stateCode");
    box.value=codeA;fire(box,"input");
    click(document.querySelector("#openCode"));          // open

    setTimeout(function(){
      LOG.push("title="+document.querySelector("#title").value);
      LOG.push("stage="+document.querySelector("#stage").value);
      var c3=document.querySelector('input[data-t=copia]');
      LOG.push("copia="+(c3?c3.checked:"?"));
      var n=document.querySelector('[data-mv="copia.count"]');
      LOG.push("count="+(n?n.value:"?"));
      document.body.setAttribute("data-log",LOG.join(" | "));
    },1200);
  },400);
})();
</script>
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def translate_path(self, path):
        rel = path.split("?", 1)[0].lstrip("/")
        return os.path.join(HERE, rel.replace("/", os.sep))


def write_page(driver: str, name: str) -> str:
    src = io.open(os.path.join(HERE, "planner.html"), encoding="utf-8").read()
    page = re.sub(r'var BASE="[^"]*";', 'var BASE="";', src, count=1)
    cut = page.rindex("</body>")
    page = page[:cut] + driver + page[cut:]
    p = os.path.join(HERE, name)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    return p


def run(url: str, profile: str) -> str:
    r = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
         "--user-data-dir=" + profile, "--virtual-time-budget=20000",
         "--dump-dom", url], capture_output=True, timeout=240)
    return r.stdout.decode("utf-8", "replace")


def attr(dom: str, name: str) -> str:
    m = re.search(r'%s="([^"]*)"' % name, dom)
    return m.group(1) if m else ""


def main() -> int:
    tag = uuid.uuid4().hex[:8]
    p1 = write_page(FILL, "__p_fill_%s.html" % tag)
    p2 = write_page(ASSERT, "__p_assert_%s.html" % tag)
    p3 = write_page(CODE_RT, "__p_code_%s.html" % tag)

    # ONE server for both loads: same port means same origin means localStorage
    # actually carries over.
    httpd = socketserver.TCPServer(("127.0.0.1", 0), Quiet)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    profile = os.path.join(tempfile.gettempdir(), "chrome-persist-" + tag)

    try:
        base = "http://127.0.0.1:%d/" % port
        dom1 = run(base + os.path.basename(p1), profile)
        dom2 = run(base + os.path.basename(p2), profile)
        dom3 = run(base + os.path.basename(p3), profile + "-rt")
    finally:
        httpd.shutdown()
        for p in (p1, p2, p3):
            try:
                os.remove(p)
            except OSError:
                pass

    checks: list[tuple[bool, str]] = []

    def ck(c, m):
        checks.append((bool(c), m))

    log1, log2, log3 = (attr(d, "data-log") for d in (dom1, dom2, dom3))
    code = attr(dom1, "data-code")

    # --- load 1 built the plan ------------------------------------------
    ck("JSERROR" not in log1, "load 1: no JS error (%s)" % log1[:180])
    ck("MISSING" not in log1, "load 1: every selector existed (%s)" % log1[:180])
    ck("NO STANDARDS LOADED" not in log1, "load 1: the standards list populated")
    ck(len(code) > 200, "load 1: a plan code was produced (%d chars)" % len(code))
    stdcode = re.search(r"stdcode=([^\s|]+)", log1)
    ck(stdcode is not None, "load 1: a standard was ticked")

    # --- load 2: autosave restored everything ---------------------------
    ck("JSERROR" not in log2, "load 2: no JS error (%s)" % log2[:180])

    def g(key, log=None):
        m = re.search(key + r"=([^|]*)", log if log else log2)
        return m.group(1).strip() if m else ""

    ck(g("title") == "SENTINEL Sicilian Expedition",
       "autosave restored the title (got %r)" % g("title"))
    ck(g("stage") == "Rhetoric", "autosave restored the trivium stage (got %r)" % g("stage"))
    ck(g("len") == "SENTINEL 3 weeks", "autosave restored the length")
    ck(g("roster") == "41", "autosave restored the roster")
    ck(g("scope") == "module", "autosave restored module scope")
    ck(g("quarter") == "SENTINEL Q3", "autosave restored a module-only field")
    ck(g("causesobj") == "SENTINEL the decision to sail",
       "autosave restored a move field (got %r)" % g("causesobj"))
    ck(g("iconic") == "SENTINEL Eratosthenes and the shadows",
       "autosave restored a second move's field")
    ck(g("nform") == "Short essay",
       "autosave restored an overridden narration form rather than the stage default")
    ticks = g("ticks").split(",") if g("ticks") else []
    ck("causes" in ticks and "iconic" in ticks,
       "autosave restored the ticked moves (got %s)" % ticks)
    ck(g("stdchecked") not in ("", "0"),
       "autosave re-ticked the standard AFTER the async bundle arrived (got %r)"
       % g("stdchecked"))
    ck(g("cell") == "SENTINEL week one",
       "autosave restored a week-grid cell (got %r)" % g("cell"))

    # --- load 3: the code survives the state being overwritten ----------
    ck("JSERROR" not in log3, "code round-trip: no JS error (%s)" % log3[:180])
    ck(g("mutated", log3) == "STATE-B WRONG",
       "the mutation step actually changed the state first")
    ck(g("title", log3) == "STATE-A title",
       "pasting a code restored the title over the mutation (got %r)" % g("title", log3))
    ck(g("stage", log3) == "Logic", "pasting a code restored the stage")
    ck(g("copia", log3) == "true", "pasting a code re-ticked an unticked move")
    ck(g("count", log3) == "12",
       "pasting a code restored a field the mutation had overwritten (got %r)"
       % g("count", log3))

    bad = [m for ok, m in checks if not ok]
    print("%d checks, %d failed" % (len(checks), len(bad)))
    for m in bad:
        print("  FAIL  " + m)
    if not bad:
        print("plan code: %d chars" % len(code))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
