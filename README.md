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

To process the local `ReferencePapers/` archive into schema-valid literature records:

```bash
python3 -m ilm_wiki.cli process-pdfs --pdf-dir ReferencePapers --output output/reference_pdf_extractions.json
python3 -m ilm_wiki.cli build-records-from-pdfs --pdf-dir ReferencePapers --output data/manual_records/reference_papers_generated.json
python3 -m ilm_wiki.cli run --pdf-dir data/pdfs --manual-dir data/manual_records --output-dir output
```

Use the bundled document Python if your system Python does not have `pypdf`.

## Manual Records

Use `data/manual_records/example_record.json` as a starting point. Manual records are useful for curated extraction from paywalled papers or human-verified table data.

The runtime record model is mirrored by `config/literature_record.schema.json`. Validate local records with:

```bash
ilm-wiki validate-records --manual-dir data/manual_records
```

The seeded corpus in `data/manual_records/seed_literature.json` gives the first traceable literature-review layer across D1-D9. It intentionally marks many entries as `qualitative` or `quantitative_partial` until paper tables and figures are manually extracted.

For collection work, use:

- `docs/literature_collection_guide.md` for the domain-by-domain collection protocol.
- `templates/literature_extraction_template.csv` for spreadsheet-style extraction before conversion to JSON.

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

- “LLM wiki Karpathy” is implemented as a plain, dense Markdown wiki style: simple headings, compact tables, source-backed claims, and explicit gaps.
- Live literature search adapters are kept behind an optional interface so the pipeline remains reproducible when network access or database credentials are unavailable.
