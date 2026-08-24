#!/usr/bin/env python
"""
Catch the class of syntax error that kills a whole page silently.

Written after a patch put a literal newline inside a regex literal in
planner.html. That is a fatal parse error, so nothing in the script ran: no
listeners, no tabs, no dropdowns. Counting braces did not catch it, and reading
the code did not either, because the broken character is invisible.

This walks the script tracking whether it is inside a string, a template
literal, a regex literal, or a comment, and reports any string or regex literal
that spans a newline. It is not a full JavaScript parser -- it is the specific
check that would have caught the bug, run before every deploy.

    python check-js.py [file.html ...]      (defaults to every .html here)
"""
from __future__ import annotations

import glob
import re
import sys

NL = "\n"


def check(path: str) -> list[str]:
    src = open(path, encoding="utf-8", errors="replace").read()
    problems: list[str] = []

    for m in re.finditer(r"<script[^>]*>(.*?)</script>", src, re.S):
        js = m.group(1)
        base = src[:m.start(1)].count(NL)
        i, n = 0, len(js)
        # a regex literal may only follow one of these; otherwise "/" is division
        prev_significant = ""
        while i < n:
            c = js[i]
            nxt = js[i + 1] if i + 1 < n else ""

            if c == "/" and nxt == "/":
                i = js.find(NL, i)
                if i < 0:
                    break
                continue
            if c == "/" and nxt == "*":
                j = js.find("*/", i + 2)
                i = n if j < 0 else j + 2
                continue

            if c in "\"'":
                j, closed = i + 1, False
                while j < n:
                    if js[j] == "\\":
                        j += 2
                        continue
                    if js[j] == NL:
                        problems.append(
                            f"{path}:{base + js[:i].count(NL) + 1}: "
                            f"string literal opened with {c} runs past the end "
                            f"of its line")
                        break
                    if js[j] == c:
                        closed = True
                        break
                    j += 1
                if not closed and j >= n:
                    problems.append(f"{path}: unterminated string literal")
                i = j + 1
                prev_significant = c
                continue

            if c == "`":
                j = i + 1
                while j < n and js[j] != "`":
                    j += 2 if js[j] == "\\" else 1
                i = j + 1
                prev_significant = c
                continue

            if c == "/" and prev_significant in "(,=:[!&|?{};+-*%~^<>" or (
                    c == "/" and prev_significant == "" ):
                j, closed = i + 1, False
                while j < n:
                    if js[j] == "\\":
                        j += 2
                        continue
                    if js[j] == NL:
                        problems.append(
                            f"{path}:{base + js[:i].count(NL) + 1}: "
                            f"regex literal contains a real newline -- this is "
                            f"a fatal parse error and stops the whole script")
                        break
                    if js[j] == "[":
                        k = js.find("]", j)
                        j = j + 1 if k < 0 else k + 1
                        continue
                    if js[j] == "/":
                        closed = True
                        break
                    j += 1
                i = j + 1
                prev_significant = "/"
                continue

            if not c.isspace():
                prev_significant = c
            i += 1

        for a, b, name in (("{", "}", "braces"), ("(", ")", "parens"),
                           ("[", "]", "brackets")):
            if js.count(a) != js.count(b):
                problems.append(f"{path}: {name} unbalanced "
                                f"({js.count(a)} vs {js.count(b)})")
    return problems


def main() -> int:
    files = sys.argv[1:] or sorted(glob.glob("*.html"))
    if not files:
        print("no html files to check", file=sys.stderr)
        return 1
    bad: list[str] = []
    for f in files:
        p = check(f)
        print(f"  {'FAIL' if p else 'ok  '}  {f}")
        bad += p
    if bad:
        print()
        for b in bad:
            print("FAIL:", b)
        return 2
    print("\nPASS: no unterminated strings, no newline inside a regex literal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
