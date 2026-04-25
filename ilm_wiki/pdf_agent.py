from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - optional dependency fallback
    PdfReader = None  # type: ignore[assignment]

from .domains import DOMAINS

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
ALLOY_RE = re.compile(
    r"\b(?:Al|Cu|Ni|Fe|Pb|Sn|In|Bi|Si|Ge|GaAs|InSb|CdTe|Ti|Mg|Zn|Ag|Au)"
    r"(?:[-\s]?(?:Al|Cu|Ni|Fe|Pb|Sn|In|Bi|Si|Ge|Ti|Mg|Zn|Ag|Au))*"
    r"(?:[-\s]?\d+(?:\.\d+)?\s?(?:wt%|at%|%))?\b"
)
PLATFORM_TERMS = (
    "ISS",
    "TEXUS",
    "FOTON",
    "Space Shuttle",
    "Shuttle",
    "TEMPUS",
    "EML",
    "DECLIC",
    "MEPHISTO",
    "sounding rocket",
    "drop tower",
    "parabolic flight",
)


@dataclass
class PdfExtraction:
    path: str
    text_chars: int
    doi_candidates: list[str]
    alloy_candidates: list[str]
    platform_candidates: list[str]
    domain_matches: list[str]
    reference_snippet: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "text_chars": self.text_chars,
            "doi_candidates": self.doi_candidates,
            "alloy_candidates": self.alloy_candidates,
            "platform_candidates": self.platform_candidates,
            "domain_matches": self.domain_matches,
            "reference_snippet": self.reference_snippet,
        }


class PdfAgent:
    """Extracts citation and domain-routing hints from local PDF files."""

    def process_directory(self, pdf_dir: Path) -> list[PdfExtraction]:
        if not pdf_dir.exists():
            return []
        return [self.process_pdf(path) for path in sorted(pdf_dir.glob("*.pdf"))]

    def process_pdf(self, path: Path) -> PdfExtraction:
        text = self._read_pdf_text(path)
        doi_candidates = sorted(set(match.group(0).rstrip(".") for match in DOI_RE.finditer(text)))
        alloy_candidates = sorted(set(match.group(0).strip() for match in ALLOY_RE.finditer(text)))[:40]
        platform_candidates = [term for term in PLATFORM_TERMS if term.lower() in text.lower()]
        domain_matches = self._match_domains(text)
        reference_snippet = self._reference_snippet(text)
        return PdfExtraction(
            path=str(path),
            text_chars=len(text),
            doi_candidates=doi_candidates,
            alloy_candidates=alloy_candidates,
            platform_candidates=platform_candidates,
            domain_matches=domain_matches,
            reference_snippet=reference_snippet,
        )

    def _read_pdf_text(self, path: Path) -> str:
        if PdfReader is not None:
            try:
                reader = PdfReader(str(path))
                return "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception:
                pass

        try:
            result = subprocess.run(
                ["pdftotext", str(path), "-"],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.stdout if result.returncode == 0 else ""
        except Exception:
            return ""

    def _match_domains(self, text: str) -> list[str]:
        lowered = text.lower()
        matches: list[str] = []
        for domain_id, spec in DOMAINS.items():
            score = 0
            for query in spec.queries:
                terms = [term for term in re.split(r"\W+", query.lower()) if len(term) > 4]
                score += sum(1 for term in terms if term in lowered)
            if score >= 3:
                matches.append(domain_id)
        return matches

    def _reference_snippet(self, text: str) -> str | None:
        lowered = text.lower()
        for marker in ("references", "bibliography"):
            idx = lowered.rfind(marker)
            if idx >= 0:
                snippet = re.sub(r"\s+", " ", text[idx : idx + 2500]).strip()
                return snippet or None
        return None

