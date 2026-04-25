# Microgravity Metal Alloy Solidification Literature Review System

This repository contains a deployable agent pipeline for building a PhD-level Markdown wiki on metal alloy solidification in microgravity.

The implementation is intentionally citation-first: it does not invent literature data. It can ingest local PDF files, manual JSON records, and optional search-adapter results, then validates every extracted record for a DOI or reference string before report generation.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
ilm-wiki run --pdf-dir data/pdfs --manual-dir data/manual_records --output-dir output
```

Generated files:

- `output/microgravity_solidification_wiki.md`
- `output/1g_vs_microgravity_benchmark_table.md`
- `output/variable_groups_consolidated.md`
- `output/gap_matrix.md`
- `output/raw_domain_handoff.json`
- `output/qa_report.json`

## PDF Agent

Place PDFs in `data/pdfs/`, then run:

```bash
ilm-wiki process-pdfs --pdf-dir data/pdfs --output output/pdf_extractions.json
```

The PDF agent extracts text, DOI candidates, reference-section snippets, platform/facility hints, alloy mentions, and domain matches. Quantitative fields are only populated when they are explicitly present in structured manual records or extractor output.

For better PDF text extraction, install `pypdf` in your environment. If it is unavailable, the agent falls back to the `pdftotext` command when present.

## Manual Records

Use `data/manual_records/example_record.json` as a starting point. Manual records are useful for curated extraction from paywalled papers or human-verified table data.

## Deployment

Local CLI:

```bash
make install
make run
```

Docker:

```bash
docker build -t ilm-wiki .
docker run --rm -v "$PWD/data:/app/data" -v "$PWD/output:/app/output" ilm-wiki
```

## Notes

- “ILM wiki Karpathy” is implemented as a plain, dense Markdown wiki style: simple headings, compact tables, source-backed claims, and explicit gaps.
- Live literature search adapters are kept behind an optional interface so the pipeline remains reproducible when network access or database credentials are unavailable.
