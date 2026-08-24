# -*- coding: utf-8 -*-
"""
Render planner.html in real Chrome and assert on the resulting DOM.

check-js.py catches the invisible fatal parse error. It does not catch a
reference to a function that does not exist, which kills the script just as
dead. This runs the page and looks at what actually came out.

Assertions are deliberately anchored on MARKUP (data-mv keys, data-tick, option
values) rather than on prose, because prose moves and markup does not.
"""
from __future__ import annotations

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

MOVES = ["attention", "aloud", "narration", "common", "copywork", "dictation",
         "copia", "imitation", "progym", "memory", "review", "disputed",
         "socratic", "causes", "apprentice", "worked", "shared"]

GROUPS = ["Reading and attention", "Language and craft", "Memory",
          "Reasoning and argument", "How the teacher works"]

NEW_TPL = ["Worked example, then practice", "Investigation or lab",
           "Review and recitation", "Progymnasmata exercise"]

# every field key the schema declares, so a typo in one move's fields is caught
FIELDS = {
    "attention": ["object", "stretch", "removed"],
    "aloud": ["reader", "passage", "minutes", "then"],
    "narration": ["passage", "form", "length", "shows"],
    "common": ["enters", "cadence", "checked", "format"],
    "copywork": ["passage", "minutes", "hand"],
    "dictation": ["passage", "prep", "phrasing", "correction"],
    "copia": ["source", "dimension", "count", "label"],
    "imitation": ["model", "what", "rung", "feedback"],
    "progym": ["exercise", "models", "produces", "shape"],
    "memory": ["piece", "story", "review", "occasion"],
    "review": ["what", "cadence", "minutes", "who"],
    "disputed": ["question", "objections", "contra", "produces"],
    "socratic": ["text", "questions", "turn", "refocus"],
    "causes": ["object", "causes", "naming", "questions"],
    "apprentice": ["demonstrates", "alongside", "release", "own"],
    "worked": ["example", "watching", "practice", "check"],
    "shared": ["format", "what", "occasion"],
}


def dump_dom() -> str:
    profile = os.path.join(tempfile.gettempdir(), "chrome-probe-" + uuid.uuid4().hex)
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
           "--user-data-dir=" + profile, "--virtual-time-budget=9000",
           "--dump-dom", "file:///" + PAGE.replace("\\", "/")]
    out = subprocess.run(cmd, capture_output=True, timeout=180)
    return out.stdout.decode("utf-8", "replace")


def main() -> int:
    dom = dump_dom()
    if len(dom) < 5000:
        print("FAIL: Chrome returned %d bytes -- the page did not render" % len(dom))
        return 1

    checks: list[tuple[bool, str]] = []

    def ck(cond: bool, msg: str) -> None:
        checks.append((bool(cond), msg))

    # --- the script ran at all -------------------------------------------
    tools = re.search(r'<div id="tools">(.*?)\n  <h2>Assets', dom, re.S)
    ck(tools is not None, "the moves panel rendered")
    panel = tools.group(1) if tools else ""
    ck(panel.count('class="tool"') == 17, "17 move boxes in the panel (got %d)"
       % panel.count('class="tool"'))

    # --- every move present, grouped -------------------------------------
    for m in MOVES:
        ck('data-id="%s"' % m in panel, "move box present: %s" % m)
    for g in GROUPS:
        ck('class="grp">%s<' % g in panel, "group heading present: %s" % g)

    # --- every declared field rendered an input --------------------------
    for m, keys in FIELDS.items():
        for k in keys:
            key = "%s.%s" % (m, k)
            ck(('data-mv="%s"' % key) in panel or ('data-mxv="%s"' % key) in panel,
               "field input present: %s" % key)

    # --- the multi-select field really is checkboxes ----------------------
    ck(panel.count('data-mxv="causes.causes"') == 4,
       "four-causes field rendered 4 checkboxes (got %d)"
       % panel.count('data-mxv="causes.causes"'))

    # --- templates --------------------------------------------------------
    sel = re.search(r'<select id="template">(.*?)</select>', dom, re.S)
    ck(sel is not None, "the template menu rendered")
    opts = sel.group(1) if sel else ""
    ck(opts.count("<option") == 11, "11 lesson templates (7 old + 4 new); got %d"
       % opts.count("<option"))
    for t in NEW_TPL:
        ck(t in opts, "new template present: %s" % t)

    # --- the default template's ticks revealed their fields ---------------
    ck('data-tick="true"' in panel,
       "the opening template ticked moves and revealed their fields")
    ticked = re.findall(r'data-tick="true" data-id="([a-z]+)"', panel)
    ck(set(ticked) == {"attention", "narration"},
       "the default reading template ticked exactly attention+narration (got %s)"
       % sorted(ticked))

    # --- the stage default reached the narration form ---------------------
    # Setting a select's .value in JS emits no `selected` attribute, so the DOM
    # dump cannot see it. Assert on the plan document, which reflects MV, and on
    # the option list, which is markup.
    nf = re.search(r'data-mv="narration\.form">(.*?)</select>', panel, re.S)
    ck(nf is not None, "the narration form field is a select")
    for want in ("Oral", "Written paragraph", "Short essay"):
        ck(nf is not None and (">%s<" % want) in nf.group(1),
           "narration form offers the %s option" % want)

    # --- the plan document rendered the moves with slots ------------------
    doc = re.search(r'<div class="doc" id="doc">(.*?)</div></div>', dom, re.S)
    ck(doc is not None, "the plan document rendered")
    d = doc.group(1) if doc else ""
    ck("Moves in use" in d, "plan carries a Moves in use section")
    ck("Still to name:" in d, "unfilled fields print as a named slot, not silence")
    ck("<h4>Narration</h4>" in d, "the narration move has its own block in the plan")
    # Grammar is the opening stage, so the narration form must arrive as Oral --
    # this is the assertion that actually proves syncNarrationForm ran.
    ck(re.search(r"<th>Form</th><td>Oral</td>", d) is not None,
       "the trivium stage filled the narration form (Grammar -> Oral)")
    ck(re.search(r"Still to name:</strong> What is narrated; Length expected", d) is not None,
       "the narration slot names its own unfilled fields, in field order")

    # --- the prompt carries the fields and the gaps -----------------------
    pr = re.search(r'<pre class="prompt" id="prompt">(.*?)</pre>', dom, re.S)
    ck(pr is not None, "the prompt rendered")
    p = pr.group(1) if pr else ""
    ck("PEDAGOGICAL MOVES TO USE" in p, "prompt names the moves section")
    ck("NOT YET SPECIFIED" in p, "prompt states the gaps explicitly")
    ck("CLASSICAL TOOLS TO USE" not in p, "the old prompt heading is gone")

    # --- house rules the generators must not lose -------------------------
    body = dom
    ck("facilitator" not in body.lower().replace("never facilitator", ""),
       "no stray use of facilitator")
    for weekday in ("monday", "tuesday", "wednesday", "thursday", "friday"):
        ck(weekday not in body.lower(), "no weekday names: %s" % weekday)

    bad = [m for ok, m in checks if not ok]
    print("%d checks, %d failed" % (len(checks), len(bad)))
    for m in bad:
        print("  FAIL  " + m)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
