# -*- coding: utf-8 -*-
"""
Leg B, stage 1. Harvest the Canvas corpus into three shelves and cache it.

  projects  -- singular instruments at >=25 pts. The generative layer: these get
               read and abstracted into transferable FORMS.
  routines  -- names recurring 3+ times across the corpus. Genuinely template-
               shaped; these get read too, but abstract into fill-and-go items.
  raw       -- the remaining singular instruments. Metadata only, no reading and
               no abstraction, because a small practice task cannot honestly be
               turned into an idea. Kept as raw material, as asked.

Descriptions are fetched only for projects+routines, stripped to plain text and
truncated -- the task statement lives in the opening of a Canvas description, and
reading 4,000 characters of lesson HTML per item buys nothing.

Never prints the token.
"""
from __future__ import annotations

import collections
import html
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request

HOME = os.path.expanduser("~")
TOKENS = os.path.join(HOME, "OneDrive - OptimaEd",
                      "Academic Design & Curriculum", "Access tokens.txt")
HOST = "optimaoaoteam.instructure.com"
OUT = os.path.dirname(os.path.abspath(__file__))
DESC_CAP = 1400          # enough to see the form; not the whole lesson
PROJECT_PTS = 25
ROUTINE_MIN = 3


def cv_token() -> str:
    txt = io.open(TOKENS, encoding="utf-8", errors="replace").read()
    m = re.search(r"\b\d{4,5}~[A-Za-z0-9]{40,}", txt)
    if not m:
        sys.exit("No Canvas token in the tokens file.")
    return m.group(0)


TOK = cv_token()


def cv(path: str):
    url = "https://%s/api/v1%s" % (HOST, path)
    url += ("&" if "?" in url else "?") + "per_page=100"
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + TOK, "User-Agent": "optima-harvest"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError:
        return None


def plain(h: str) -> str:
    """Canvas descriptions are RCE HTML. Reduce to readable prose."""
    if not h:
        return ""
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
    s = re.sub(r"(?i)<(br|/p|/div|/li|/h[1-6]|/tr)\s*/?>", "\n", s)
    s = re.sub(r"(?i)<li[^>]*>", "\n- ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace(" ", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[–—]", " ", s)
    s = re.sub(r"\b(module|week|unit|lesson|quarter|studio|cycle|part|day|"
               r"activity|no\.?)\s*\d+[a-z]?\b", " ", s)
    s = re.sub(r"\b\d+(\.\d+)*\b", " ", s)
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^a-z ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------------------
print("enumerating courses...")
courses = cv("/courses?state[]=available&state[]=unpublished&state[]=completed") or []
print("  %d courses" % len(courses))

items = []
for c in courses:
    cid = c["id"]
    groups = {g["id"]: g["name"] for g in (cv("/courses/%d/assignment_groups" % cid) or [])}
    for a in (cv("/courses/%d/assignments" % cid) or []):
        items.append({
            "id": a["id"], "cid": cid, "course": c.get("name") or "?",
            "code": c.get("course_code") or "",
            "name": a["name"],
            "pts": a.get("points_possible") or 0,
            "group": groups.get(a.get("assignment_group_id"), ""),
            "types": a.get("submission_types") or [],
            "has_rubric": bool(a.get("rubric")),
            "desc_len": len(a.get("description") or ""),
            "desc": plain(a.get("description") or "")[:DESC_CAP],
        })
print("  %d instruments" % len(items))

counts = collections.Counter(norm(i["name"]) for i in items)
for i in items:
    n = norm(i["name"])
    if counts[n] >= ROUTINE_MIN and n:
        i["shelf"] = "routine"
    elif i["pts"] >= PROJECT_PTS:
        i["shelf"] = "project"
    else:
        i["shelf"] = "raw"

by = collections.Counter(i["shelf"] for i in items)
print("")
print("shelves: project=%d routine=%d raw=%d" % (by["project"], by["routine"], by["raw"]))

# routines collapse to one entry per pattern; keep the fullest description
routines: dict[str, dict] = {}
for i in items:
    if i["shelf"] != "routine":
        continue
    k = norm(i["name"])
    if k not in routines or len(i["desc"]) > len(routines[k]["desc"]):
        routines[k] = dict(i)
    routines[k].setdefault("uses", 0)
    routines[k]["uses"] = routines[k].get("uses", 0) + 1
for k, v in routines.items():
    v["uses"] = sum(1 for i in items if norm(i["name"]) == k)
    v["courses"] = sorted({i["course"] for i in items if norm(i["name"]) == k})
print("routine PATTERNS after collapsing: %d" % len(routines))

projects = [i for i in items if i["shelf"] == "project"]
thin = [p for p in projects if len(p["desc"]) < 200]
print("")
print("projects to abstract: %d" % len(projects))
print("  of those, THIN (<200 chars of description, cannot be honestly"
      " abstracted): %d" % len(thin))
print("  median description length: %d chars"
      % sorted(len(p["desc"]) for p in projects)[len(projects) // 2])
rt = list(routines.values())
print("routines to abstract: %d, thin: %d"
      % (len(rt), sum(1 for r in rt if len(r["desc"]) < 200)))

json.dump({"items": items, "routines": rt},
          io.open(os.path.join(OUT, "harvest.json"), "w", encoding="utf-8"),
          ensure_ascii=False)
print("")
print("cached -> harvest.json  (%.1f MB)"
      % (os.path.getsize(os.path.join(OUT, "harvest.json")) / 1e6))
print("")
print("THIN project titles (these stay out unless the source improves):")
for p in thin[:40]:
    print("  %-52s %s" % (p["name"][:52], p["course"][:28]))
