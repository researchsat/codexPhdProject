from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agents import OrchestratorAgent
from .pdf_agent import PdfAgent


def main() -> None:
    parser = argparse.ArgumentParser(prog="ilm-wiki")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the full literature-review pipeline.")
    run_parser.add_argument("--pdf-dir", type=Path, default=Path("data/pdfs"))
    run_parser.add_argument("--manual-dir", type=Path, default=Path("data/manual_records"))
    run_parser.add_argument("--output-dir", type=Path, default=Path("output"))

    pdf_parser = subparsers.add_parser("process-pdfs", help="Extract DOI/reference/domain hints from local PDFs.")
    pdf_parser.add_argument("--pdf-dir", type=Path, default=Path("data/pdfs"))
    pdf_parser.add_argument("--output", type=Path, default=Path("output/pdf_extractions.json"))

    qa_parser = subparsers.add_parser("qa", help="Read the latest QA report.")
    qa_parser.add_argument("--output-dir", type=Path, default=Path("output"))

    args = parser.parse_args()
    if args.command == "run":
        output = OrchestratorAgent(args.pdf_dir, args.manual_dir, args.output_dir).run()
        print(json.dumps(output.qa_report, indent=2, ensure_ascii=False))
    elif args.command == "process-pdfs":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        extractions = PdfAgent().process_directory(args.pdf_dir)
        args.output.write_text(
            json.dumps([extraction.to_dict() for extraction in extractions], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Processed {len(extractions)} PDF file(s). Wrote {args.output}.")
    elif args.command == "qa":
        path = args.output_dir / "qa_report.json"
        if not path.exists():
            raise SystemExit(f"No QA report found at {path}. Run `ilm-wiki run` first.")
        print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

