# -*- coding: utf-8 -*-
"""
Build ideas-bank.json from the harvested Canvas corpus plus the authored forms.

Run order:
    python harvest-canvas.py      # reads Canvas, writes harvest.json
    python build-bank.py          # writes ideas-bank.json

The bank has four shelves:

  forms     -- transferable project/assessment shapes, each with fields a teacher
               fills and provenance naming the real instruments behind it
  routines  -- the recurring instruments, as fill-and-go templates
  raw       -- every remaining instrument as raw material: name, course, points,
               kind. No description, no abstraction.
  blank     -- an empty form, so inventing something new gets the same slots

Two rules this script enforces, loudly:

  1. A form whose `from_` patterns match NOTHING in the harvest is a form that was
     invented rather than abstracted. That is a build failure, not a warning.
  2. Quiz descriptions never enter the bank. The bank publishes to a public site
     and question banks and answer keys stay out of it.
"""
from __future__ import annotations

import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from forms import FORMS            # noqa: E402
from forms_b import FORMS_B        # noqa: E402

ALL_FORMS = FORMS + FORMS_B

HARVEST = os.path.join(HERE, "harvest.json")
OUT = os.path.join(HERE, "ideas-bank.json")

# Course name -> (subject, grade band). Derived from the course titles Canvas
# reports; unmatched courses keep their raw title and an empty band rather than
# being guessed at.
SUBJECT_PATTERNS = [
    (r"Language Arts|English", "English Language Arts"),
    (r"Visual Art|Digital Art|Art History", "Visual Art"),
    (r"Music", "Music"),
    (r"Chemistry|Integrated Science|Biology|Physics", "Science"),
    (r"Sociology|College Counseling|Career Research|Critical Thinking",
     "Social Studies and Life Skills"),
    (r"Math|Calculus|Precalculus", "Mathematics"),
    (r"Latin|Spanish|French", "World Languages"),
]
GRADE_PATTERNS = [
    (r"\b3rd Grade\b|Music 1\b", "3"), (r"\b4th Grade\b|Music 2\b", "4"),
    (r"\b5th Grade\b|Music 3\b", "5"), (r"\b6th Grade\b", "6"),
    (r"\b7th Grade\b", "7"), (r"\b8th Grade\b", "8"),
    (r"\b9th Grade\b|English 1\b", "9"), (r"\b10th Grade\b|English 2\b", "10"),
    (r"\b11th Grade\b|English 3\b|ENGLISH III", "11"),
    (r"\b12th Grade\b|English 4\b", "12"),
    (r"^M/J |Music Theory|Critical Thinking and Study", "6-8"),
]


def subject_of(course: str) -> str:
    for pat, name in SUBJECT_PATTERNS:
        if re.search(pat, course, re.I):
            return name
    return "Other"


def grade_of(course: str) -> str:
    for pat, g in GRADE_PATTERNS:
        if re.search(pat, course, re.I):
            return g
    if re.search(r"\bHS |Honors|Sociology|Career|College", course, re.I):
        return "9-12"
    return ""


WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday")

# Counters so the run reports what it touched instead of silently changing text.
SCRUBBED: list[tuple[str, str]] = []
WITHHELD: list[tuple[str, str, str]] = []


def house_text(item: dict, text: str) -> str:
    """Bring a harvested description into line with the house rules, or withhold
    it. The bank publishes to a public page and must not spread an error it found.
    """
    if not text:
        return ""
    out = text
    if "facilitator" in out.lower():
        SCRUBBED.append((item["name"], item["course"]))
        out = (out.replace("Facilitators", "Teachers").replace("facilitators", "teachers")
                  .replace("Facilitator", "Teacher").replace("facilitator", "teacher"))
    low = out.lower()
    for d in WEEKDAYS:
        if d in low:
            # a weekday cannot be removed without changing the sentence, so the
            # whole description is withheld and the item is named in the report
            WITHHELD.append((item["name"], item["course"], d))
            return ""
    return out


def is_quiz(item: dict) -> bool:
    t = item.get("types") or []
    return "online_quiz" in t or bool(re.search(r"\bquiz\b|\bexam\b", item["name"], re.I))


def main() -> int:
    if not os.path.exists(HARVEST):
        sys.exit("harvest.json not found. Run harvest-canvas.py first.")
    h = json.load(io.open(HARVEST, encoding="utf-8"))
    items, routines = h["items"], h["routines"]

    # ---- forms: attach provenance, and fail if a form has none -------------
    problems: list[str] = []
    forms_out = []

    def key(s: str) -> str:
        """Match on words, not punctuation. Canvas titles use em dashes, curly
        apostrophes and colons interchangeably, and an em dash where a form
        expected a hyphen is not a missing provenance -- it is a missing
        normalisation."""
        return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

    for f in ALL_FORMS:
        hits = []
        for pat in f["from_"]:
            k = key(pat)
            for it in items:
                if k in key(it["name"]):
                    hits.append(it)
        # Provenance that lives in the description rather than the title. A
        # studio project named "Mosaic Painting" is an instance of artwork-plus-
        # statement and its own description says so; refusing to look there
        # would mean reporting a gap that is not there.
        for pat in f.get("from_desc", []):
            k = key(pat)
            for it in items:
                if it["shelf"] == "project" and k in key(it["desc"]):
                    hits.append(it)
        if not hits:
            problems.append("form %-26s matched NOTHING in the harvest: %s"
                            % (f["id"], f["from_"]))
            continue
        # dedupe provenance by (name, course), cap the list, keep the biggest first
        seen, prov = set(), []
        for it in sorted(hits, key=lambda x: -x["pts"]):
            k = (it["name"], it["course"])
            if k in seen:
                continue
            seen.add(k)
            prov.append({"name": it["name"], "course": it["course"],
                         "pts": it["pts"], "subject": subject_of(it["course"]),
                         "grade": grade_of(it["course"])})
        g = f.copy()
        g.pop("from_")
        g.pop("from_desc", None)
        g["seen_in"] = len(prov)
        # `covers` is the FULL set this form sits above; `provenance` is only the
        # display sample. Counting coverage off the sample made forms with more
        # than eight instances look narrower than they are. Stripped before the
        # bank is written -- it is a build-time measure, not page data.
        g["covers"] = [[q["name"], q["course"]] for q in prov]
        g["provenance"] = prov[:8]
        g["subjects"] = sorted({p["subject"] for p in prov})
        g["grades"] = sorted({p["grade"] for p in prov if p["grade"]})
        g["pts_seen"] = sorted({p["pts"] for p in prov})
        forms_out.append(g)

    if problems:
        print("BUILD FAILED - a form with no provenance is a form that was invented:")
        for p in problems:
            print("  " + p)
        return 1

    # ---- routines: fill-and-go templates ---------------------------------
    rout_out = []
    for r in routines:
        rout_out.append({
            "id": re.sub(r"[^a-z0-9]+", "-", r["name"].lower()).strip("-")[:48],
            "name": r["name"],
            "kind": "routine",
            "uses": r["uses"],
            "courses": r["courses"],
            "subjects": sorted({subject_of(c) for c in r["courses"]}),
            "grades": sorted({grade_of(c) for c in r["courses"] if grade_of(c)}),
            "pts": r["pts"],
            "tier": 1 if is_quiz(r) else (2 if r["pts"] <= 10 else 3),
            # a quiz's description is never published, and anything that
            # survives is brought into line with the house rules first
            "desc": "" if is_quiz(r) else house_text(r, r["desc"])[:700],
            "quiz": is_quiz(r),
        })
    rout_out.sort(key=lambda x: -x["uses"])

    # ---- raw shelf: metadata only ---------------------------------------
    raw_out = []
    for it in items:
        if it["shelf"] != "raw":
            continue
        raw_out.append({"name": it["name"], "course": it["course"],
                        "pts": it["pts"], "group": it["group"],
                        "subject": subject_of(it["course"]),
                        "grade": grade_of(it["course"]),
                        "kind": "quiz" if is_quiz(it) else (
                            "recording" if "media_recording" in it["types"] else
                            "discussion" if "discussion_topic" in it["types"] else
                            "assignment")})
    raw_out.sort(key=lambda x: (x["subject"], x["course"], -x["pts"]))

    # ---- the blank form -------------------------------------------------
    blank = {"id": "blank", "kind": "blank", "name": "Your own form",
             "makes": "", "move": "", "why":
             "Nothing here came from a book. If the shape you want is not in the "
             "bank, write it down with the same slots and it sits beside the rest.",
             "tier": 3, "student_min": 0,
             "fields": [
                 {"k": "makes", "l": "What the student makes", "t": "area", "ph": "one line"},
                 {"k": "move", "l": "The thinking move it requires", "t": "area", "ph": "one line"},
                 {"k": "why", "l": "When you would reach for it", "t": "area", "ph": ""},
                 {"k": "slot1", "l": "Slot 1", "t": "text", "ph": "what the teacher supplies"},
                 {"k": "slot2", "l": "Slot 2", "t": "text", "ph": ""},
                 {"k": "slot3", "l": "Slot 3", "t": "text", "ph": ""},
                 {"k": "slot4", "l": "Slot 4", "t": "text", "ph": ""}],
             "provenance": [], "seen_in": 0, "subjects": [], "grades": [],
             "pts_seen": []}

    bank = {
        "built_from": {"courses": len({i["cid"] for i in items}),
                       "instruments": len(items)},
        "forms": forms_out, "routines": rout_out, "raw": raw_out, "blank": blank,
    }
    # ---- coverage, measured before the build-time field is stripped ------
    covered = set()
    for f in forms_out:
        for n, c in f["covers"]:
            covered.add((n, c))
    proj = {(i["name"], i["course"]) for i in items if i["shelf"] == "project"}
    for g in forms_out:
        g.pop("covers", None)

    # ---- the guard, on exactly the object that will ship -----------------
    # Weekdays are checked in PROSE only. "Week 1 Friday Check-up" is a live
    # Canvas instrument name, and deployed titles are the documented exception
    # to the no-weekdays rule; a gate that fails on the exception is a gate that
    # gets switched off. `name`, `course` and `group` are what Canvas calls
    # things and are not ours to rewrite.
    prose_parts = [r["desc"] for r in bank["routines"]]
    for f in bank["forms"] + [bank["blank"]]:
        prose_parts += [f.get("makes", ""), f.get("move", ""), f.get("why", "")]
        for fl in f["fields"]:
            prose_parts += [fl.get("l", ""), fl.get("ph", "")]
            prose_parts += list(fl.get("opts", []))
    prose = " ".join(prose_parts).lower()
    published = json.dumps(bank, ensure_ascii=False).lower()

    violations = []
    if "facilitator" in published:
        violations.append("the word facilitator survived into the bank")
    for d in WEEKDAYS:
        if d in prose:
            violations.append("weekday name in bank PROSE: %s" % d)
    if violations:
        print("BUILD FAILED - house rules broken, nothing written:")
        for v in violations:
            print("  " + v)
        return 1

    # ---- write only once the gate has passed ----------------------------
    json.dump(bank, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False)

    print("ideas-bank.json written  (%.2f MB)" % (os.path.getsize(OUT) / 1e6))
    print("  forms    %3d   (%d fields, %d provenance rows)"
          % (len(forms_out), sum(len(f["fields"]) for f in forms_out),
             sum(len(f["provenance"]) for f in forms_out)))
    print("  routines %3d" % len(rout_out))
    print("  raw      %3d" % len(raw_out))
    print("  quiz descriptions withheld: %d routines, all raw rows"
          % sum(1 for r in rout_out if r["quiz"]))
    print("")
    print("forms by kind: %s"
          % dict(collections.Counter(f["kind"] for f in forms_out)))

    if SCRUBBED:
        print("")
        print("HOUSE RULE - facilitator corrected to teacher in %d description(s)"
              " on the way into the bank. The live courses still say it; that is a"
              " separate job." % len(SCRUBBED))
    if WITHHELD:
        print("HOUSE RULE - description withheld for a weekday name, which cannot"
              " be removed without changing the sentence: %d item(s)" % len(WITHHELD))
        for n, c, d in WITHHELD:
            print("    %-44s %-26s (%s)" % (n[:44], c[:26], d))

    print("")
    print("project instruments with a form above them: %d of %d (%.0f%%)"
          % (len(covered & proj), len(proj), 100.0 * len(covered & proj) / len(proj)))
    orphans = sorted(proj - covered)
    if orphans:
        print("")
        print("project instruments NOT covered by any form (%d) - these are the"
              " gaps, named rather than hidden:" % len(orphans))
        for n, c in orphans[:30]:
            print("  %-56s %s" % (n[:56], c[:30]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
