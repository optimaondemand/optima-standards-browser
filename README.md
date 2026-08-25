# Standards Browser

A teacher tool for Optima Academy Online. Pick a subject and a grade, and see how
Texas, Florida, Mississippi and Puerto Rico each state their standards — side by
side, with every standard linking back to the authority that published it.

**Live:** https://optimaondemand.github.io/optima-standards-browser/

## What it does

- **Subject + grade → every jurisdiction at once.** Toggle jurisdictions on and off.
- **Search within the results** by word or by code (`ELA.9.C.1.2`, `110.22(b)(3)`).
- **Take the bundle away** — copy to clipboard, or download CSV, Markdown or JSON.
- **Download the authority's own PDF** for any course, straight from this repo.
- **Florida clarifications** and **Mississippi objectives** are there, collapsed
  under each standard.
- Flags are shown rather than hidden: archived standards, "Major/Supporting"
  course relation, and source anomalies.

One page, no dependencies, no build step, no login. It loads a single ~1 MB
(gzipped) data file once and does everything else in the browser.

## Provenance

Standards text is reproduced **verbatim** from each authority's published
document. Nothing is paraphrased or summarised. Where a published document
contradicts itself, the record is shown **exactly as printed** and flagged, never
quietly corrected — a corrected standard is indistinguishable from an invented one.

| Jurisdiction | Source | Text |
|---|---|---|
| Texas | TEKS, 19 Texas Administrative Code (statute) | Full |
| Florida | FDOE course standards via CPALMS (government work) | Full |
| Mississippi | MDE College- and Career-Readiness Standards (government work) | Full |
| Puerto Rico | PRDE Content Standards, English Program 2022 | **Codes and structure only** |

**Puerto Rico:** PRDE asserts copyright over its wording, so this tool shows PR's
codes, hierarchy, strands and text-type variants but not PRDE's text. Each record
links out to PRDE's own document instead. That is deliberate, not a gap in the data.

### Source PDFs

`sources/` holds the authority's own published PDF for every Texas, Florida and
Mississippi course — 166 files, about 43 MB — and each course in the tool has a
**PDF** link that downloads it. Two reasons to keep local copies rather than
linking out only:

1. Teachers want the document itself, not just the extracted text.
2. An authority's site being down must not break the tool. `mdek12.org` was
   returning 502 across its entire domain the day this shipped, which is exactly
   the failure a local copy absorbs.

Every course also keeps a **publisher** link to the authority's own page, so the
canonical version is always one click away. No Puerto Rico PDF is stored here.

Also worth knowing when comparing: PR's English Program is a **second-language**
English curriculum, not the analogue of mainland ELA. It appears under
*ESL / Second-Language English*, alongside Texas Chapter 128 — not under English
Language Arts.

## Where the data comes from

`standards-data.json` is generated from the private
[`optima-standards`](https://github.com/optimaondemand/optima-standards)
repository, which holds the extractors, the source documents, and the full
provenance record. To refresh after a standards update:

```bash
# in the optima-standards repo
python build/<xx>_extract.py       # whichever jurisdiction changed
python build/build_index.py
python build/build_widget_data.py  # writes dist/standards-data.json
cp dist/standards-data.json ../optima-standards-browser/
```

The generator enforces the rights split: if a Puerto Rico record ever arrives
carrying text, it refuses to write the public file rather than publishing it.

## Embedding in Canvas

Canvas strips `<script>` from page bodies, so the tool has to be an iframe.
Paste this into a Canvas page's HTML editor:

```html
<p style="margin:0 0 8px;font:600 14px/1.4 'Segoe UI',sans-serif;color:#0d2b45">
  Standards Browser
</p>
<iframe src="https://optimaondemand.github.io/optima-standards-browser/"
        title="Standards Browser" width="100%" height="900"
        style="border:1px solid #dde4ea;border-radius:8px" loading="lazy"></iframe>
<p style="font:13px 'Segoe UI',sans-serif">
  <a href="https://optimaondemand.github.io/optima-standards-browser/" target="_blank"
     rel="noopener">Open in a new tab</a> if the frame does not load.
</p>
```

Teachers reaching it through Canvas are already signed in, so there is no separate
login. Note that the Pages URL itself is publicly reachable — the iframe removes a
second sign-in, it does not restrict access. That is fine here: everything
published is public-records material.

## The project-ideas bank

`planner.html` has a **Project ideas** tab holding shapes abstracted from work
that actually ran in the Canvas courses. Each form is a shape to fill, not a
thing to copy: it names what the student makes, the thinking move it requires,
when to reach for it, a set of slots the teacher fills, and the real instruments
it was abstracted from. Fill the slots and a form can be pulled into the plan,
where it joins the document, the Copilot prompt and the time calculator.

Four shelves:

| Shelf | What is in it |
|---|---|
| Project and assessment forms | 56 transferable shapes, with 226 slots between them |
| Routines | 36 recurring instruments, as fill-and-go templates |
| Raw material | 940 remaining instruments: names and provenance only |
| Write your own | An empty form with the same slots |

Nothing is filtered by subject or grade, deliberately. The bank sorts by kind and
shows subject as provenance, because a science teacher meeting the English
disagreement-letter form is where an idea comes from.

### Refreshing it

The bank is a snapshot. It refreshes when you run the two scripts and push:

```
python harvest-canvas.py      # reads Canvas, writes harvest.json
python build-bank.py          # writes ideas-bank.json
python probe-ideas.py         # 32 checks against a real browser
git add ideas-bank.json && git commit -m "refresh the ideas bank" && git push
```

`harvest-canvas.py` reads the Canvas token from
`OneDrive - OptimaEd\Academic Design & Curriculum\Access tokens.txt` and never
prints it. **`harvest.json` is gitignored on purpose**: it holds the full raw
descriptions, quiz content included, and this repo is public.

### What the build refuses to publish

`build-bank.py` fails rather than shipping a bank that breaks a rule:

- **A form with no provenance.** If a form's `from_` patterns match nothing in
  the harvest, that form was invented rather than abstracted, and the build
  stops. This has caught three bad provenance claims so far.
- **Quiz descriptions.** Never published, so no question banks or answer keys
  reach a public page.
- **"Facilitator".** Corrected to "teacher" on the way in, and the build fails if
  it survives. Note this is a correction to a *derived view* — the live courses
  still say it in 90 places, which is a separate job.
- **Weekday names in prose.** A weekday cannot be deleted without changing the
  sentence, so the whole description is withheld and the item is named in the
  run's output. Deployed instrument titles are exempt, which is why
  "Week 1 Friday Check-up" survives as a name.

Coverage is reported honestly: 142 of 169 project instruments currently sit under
a form, and the 27 that do not are printed by name at the end of every build
rather than hidden.

### Changing the source, or cloning the tool

The bank is a data file, not code, so:

- **Edit it** — `ideas-bank.json` is plain JSON. Change it and push.
- **Try a change without deploying** — the tab has a *load your own bank file*
  control that reads a local `.json` over the published one.
- **Harvest different courses** — the course query is at the top of
  `harvest-canvas.py`; the shelf thresholds (`PROJECT_PTS`, `ROUTINE_MIN`) are
  beside it.
- **Author more forms** — add entries to `forms.py` or `forms_b.py` and rebuild.
  The provenance gate will tell you if a new form does not correspond to anything
  real.
- **Clone the whole thing** — copy `planner.html` and `ideas-bank.json` to a new
  repo and change the `BASE` constant at the top of the page's script. There is
  no build step and no dependencies.
