# Standards Browser

A teacher tool for Optima Academy Online. Pick a subject and a grade, and see how
Texas, Florida, Mississippi and Puerto Rico each state their standards — side by
side, with every standard linking back to the authority that published it.

**Live:** https://optimaondemand.github.io/optima-standards-browser/

## What it does

- **Subject + grade → every jurisdiction at once.** Toggle jurisdictions on and off.
- **Search within the results** by word or by code (`ELA.9.C.1.2`, `110.22(b)(3)`).
- **Take the bundle away** — copy to clipboard, or download CSV, Markdown or JSON.
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
