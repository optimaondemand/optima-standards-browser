# -*- coding: utf-8 -*-
"""
Probe the project-ideas tab.

The tab fetches ideas-bank.json from BASE, so a file:// probe cannot exercise the
real path. This serves the repo over localhost and loads a temp copy of the page
with BASE rewritten to a relative "" -- which means the actual fetch, the actual
JSON, and the actual rendering all run.

Then it drives the UI: opens the tab, switches shelves, searches, opens a card,
types into a form's slots, pulls the form into the plan, and checks that the plan
document and the Copilot prompt both carry it.
"""
from __future__ import annotations

import http.server
import io
import json
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

DRIVER = r"""
<script>
(function(){
  var LOG=[];
  window.onerror=function(m){LOG.push("JSERROR: "+m)};
  function fire(el,t){el.dispatchEvent(new Event(t,{bubbles:true}))}
  function click(el){el.dispatchEvent(new MouseEvent("click",{bubbles:true}))}
  function need(sel){var el=document.querySelector(sel);if(!el)LOG.push("MISSING "+sel);return el}

  // open the tab -- this is what triggers the fetch
  var tabBtn=need('.tabs button[data-p=ideas]');
  if(tabBtn)click(tabBtn);

  // the bank arrives asynchronously; poll, then drive
  var tries=0;
  var iv=setInterval(function(){
    tries++;
    var cards=document.querySelectorAll('#ideaList [data-card]');
    if(!cards.length && tries<60)return;
    clearInterval(iv);
    if(!cards.length){LOG.push("BANK NEVER RENDERED");finish();return}
    LOG.push("cards="+cards.length);

    // shelf switching
    var shelves=document.querySelectorAll('#shelf [data-sh]');
    LOG.push("shelves="+shelves.length);

    // search
    var find=need('#ideaFind');
    if(find){find.value="gallery";fire(find,"input");
      LOG.push("searched=" + document.querySelectorAll('#ideaList [data-card]').length);
      find.value="";fire(find,"input");}

    // open the vr-gallery card and fill two slots
    var card=document.querySelector('#ideaList [data-card="vr-gallery"]');
    if(!card){LOG.push("MISSING vr-gallery card");finish();return}
    click(card.querySelector('.hd'));
    LOG.push("opened="+card.dataset.open);
    var s1=card.querySelector('[data-idea="vr-gallery.stations"]');
    var s2=card.querySelector('[data-idea="vr-gallery.order"]');
    if(s1){s1.value="One station per stage of the water cycle";fire(s1,"input")}
    else LOG.push("MISSING stations slot");
    if(s2){s2.value="The sequence is the argument";fire(s2,"input")}
    else LOG.push("MISSING order slot");

    // pull it into the plan
    var use=card.querySelector('[data-use="vr-gallery"]');
    if(use){click(use);LOG.push("used")}else LOG.push("MISSING use button");

    // and the raw shelf, which is a table not cards
    var rawBtn=document.querySelector('#shelf [data-sh=raw]');
    if(rawBtn){click(rawBtn);
      LOG.push("rawrows="+document.querySelectorAll('#ideaList table.rawt tr').length)}

    // and the blank form
    var blankBtn=document.querySelector('#shelf [data-sh=blank]');
    if(blankBtn){click(blankBtn);
      LOG.push("blankcards="+document.querySelectorAll('#ideaList [data-card]').length)}

    finish();
  },100);

  function finish(){document.body.setAttribute("data-log",LOG.join(" | "))}
})();
</script>
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def translate_path(self, path):
        rel = path.split("?", 1)[0].split("#", 1)[0].lstrip("/")
        return os.path.join(HERE, rel.replace("/", os.sep))


def serve() -> tuple[socketserver.TCPServer, int]:
    httpd = socketserver.TCPServer(("127.0.0.1", 0), Quiet)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def main() -> int:
    bank_path = os.path.join(HERE, "ideas-bank.json")
    if not os.path.exists(bank_path):
        sys.exit("ideas-bank.json not found. Run build-bank.py first.")
    bank = json.load(io.open(bank_path, encoding="utf-8"))

    src = io.open(os.path.join(HERE, "planner.html"), encoding="utf-8").read()
    # BASE -> relative, so the fetch hits the local server rather than Pages
    base_re = re.compile(r'var BASE="[^"]*";')
    assert base_re.search(src), "could not find the BASE constant"
    page = base_re.sub('var BASE="";', src, count=1)
    cut = page.rindex("</body>")
    page = page[:cut] + DRIVER + page[cut:]

    tmp_name = "__probe_ideas_%s.html" % uuid.uuid4().hex[:8]
    tmp = os.path.join(HERE, tmp_name)
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(page)

    httpd, port = serve()
    try:
        profile = os.path.join(tempfile.gettempdir(), "chrome-ideas-" + uuid.uuid4().hex)
        r = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
             "--user-data-dir=" + profile, "--virtual-time-budget=15000",
             "--dump-dom", "http://127.0.0.1:%d/%s" % (port, tmp_name)],
            capture_output=True, timeout=240)
        dom = r.stdout.decode("utf-8", "replace")
    finally:
        httpd.shutdown()
        os.remove(tmp)

    checks: list[tuple[bool, str]] = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))

    m = re.search(r'data-log="([^"]*)"', dom)
    log = m.group(1) if m else ""
    ck(bool(m), "the driver ran to completion (log present)")
    ck("JSERROR" not in log, "no JavaScript error during the interaction: %s" % log)
    ck("MISSING" not in log, "every selector the driver needed exists: %s" % log)
    ck("BANK NEVER RENDERED" not in log, "the bank fetched and rendered")

    def num(key):
        mm = re.search(key + r"=(\d+)", log)
        return int(mm.group(1)) if mm else -1

    ck(num("cards") == len(bank["forms"]),
       "every form rendered a card: %d, expected %d" % (num("cards"), len(bank["forms"])))
    ck(num("shelves") == 4, "four shelves (got %d)" % num("shelves"))
    ck(0 < num("searched") < len(bank["forms"]),
       "search narrowed the list to %d of %d" % (num("searched"), len(bank["forms"])))
    ck("opened=true" in log, "clicking a card header opens it")
    ck("used" in log, "the use button fired")
    ck(num("rawrows") > 100, "the raw shelf rendered a table (%d rows)" % num("rawrows"))
    ck(num("blankcards") == 1, "the blank form shelf shows exactly one card")

    # ---- the plan document carries the chosen form ----------------------
    doc = re.search(r'<div class="doc" id="doc">(.*?)</div></div>', dom, re.S)
    d = doc.group(1) if doc else ""
    ck("<h3>Project form</h3>" in d, "the plan gained a Project form section")
    ck("Build a gallery" in d, "the chosen form is named in the plan")
    ck("One station per stage of the water cycle" in d,
       "a typed slot reached the plan document")
    ck("The sequence is the argument" in d, "the second typed slot reached the plan")
    ck("Still to name:" in d, "unfilled slots print as named slots in the plan")
    ck(re.search(r"This shape ran as .*? in .*?\.", d) is not None,
       "the plan states the provenance rather than presenting the form as novel")

    # ---- the prompt carries it too -------------------------------------
    pr = re.search(r'<pre class="prompt" id="prompt">(.*?)</pre>', dom, re.S)
    p = pr.group(1) if pr else ""
    ck("PROJECT FORM TO BUILD ON" in p, "the prompt names the project form")
    ck("One station per stage of the water cycle" in p, "the prompt carries the filled slots")
    ck("NOT YET SPECIFIED, propose each" in p, "the prompt states the open slots")
    ck("do not reproduce that one" in p,
       "the prompt tells the model to build a new instance, not copy the original")

    # ---- the calculator picked up the form's student time --------------
    ck("Build a gallery" in d and re.search(r"180 min", d) is not None,
       "the form's student time joined the calculator")

    # ---- nothing published that should not be ---------------------------
    published = json.dumps(bank, ensure_ascii=False)
    ck(all(not r["desc"] for r in bank["routines"] if r["quiz"]),
       "no quiz description is present in the bank")
    ck("answer key" not in published.lower(), "no answer keys in the bank")
    # Weekdays: prose only. "Week 1 Friday Check-up" is a deployed instrument
    # name and deployed titles are the documented exception. This check
    # previously passed only because it never looked for Friday.
    prose = " ".join(
        [r["desc"] for r in bank["routines"]]
        + [t for f in bank["forms"] + [bank["blank"]]
           for t in (f.get("makes", ""), f.get("move", ""), f.get("why", ""))]
        + [t for f in bank["forms"] + [bank["blank"]] for fl in f["fields"]
           for t in (fl.get("l", ""), fl.get("ph", ""))]).lower()
    for weekday in ("monday", "tuesday", "wednesday", "thursday", "friday",
                    "saturday", "sunday"):
        ck(weekday not in prose, "no weekday in bank prose: %s" % weekday)
    ck("facilitator" not in published.lower(), "no use of facilitator in the bank")

    bad = [msg for ok, msg in checks if not ok]
    print("%d checks, %d failed" % (len(checks), len(bad)))
    for msg in bad:
        print("  FAIL  " + msg)
    if not bad:
        print("driver log: " + log)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
