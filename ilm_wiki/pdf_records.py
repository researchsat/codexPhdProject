from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .domains import DOMAINS
from .pdf_agent import DOI_RE, PdfAgent


DOMAIN_RULES: dict[str, tuple[str, ...]] = {
    "D1": (
        "directional solidification experiments",
        "materials science laboratory",
        "space materials science",
        "solidification and crystal growth",
        "iss-eml",
        "electromagnetic levitation",
        "containerless",
        "space station",
        "sj-10",
    ),
    "D2": (
        "macrosegregation",
        "interdendritic",
        "natural convection",
        "gravity effects",
        "gravity effect",
        "fluid flow",
        "momentum",
        "convection",
        "diffusive and convective",
    ),
    "D3": (
        "dendritic",
        "dendrite",
        "cellular",
        "columnar-to-equiaxed",
        "columnar to equiaxed",
        "cet",
        "dendritic-array",
        "al-cu solidification",
        "al-7",
        "isothermal dendritic",
        "x-ray radiographic",
    ),
    "D4": (
        "eutectic",
        "peritectic",
        "monotectic",
        "immiscible",
        "lamellar",
        "lamellar-to-rod",
        "al-bi",
        "aluminum-bismuth",
        "zr50v50",
        "spiral eutectic",
        "tris-npg",
    ),
    "D5": (
        "undercooling",
        "undercooled",
        "nucleation",
        "metastable",
        "phase-selection",
        "phase selection",
        "surface flow patterns",
        "refractory alloy droplets",
    ),
    "D6": (
        "thermophysical",
        "property measurements",
        "thermal conductivity",
        "viscosity",
        "surface tension",
        "plane front",
        "bridgman apparatus",
        "heat flow",
        "ti-6al-4v",
        "co-cr-mo",
    ),
    "D7": (
        "detached",
        "de-wetting",
        "dewetted",
        "semiconductor",
        "single-crystal",
        "single crystal",
        "crystal growth",
        "bridgman growth",
        "gainsb",
        "gaas",
        "insb",
    ),
    "D8": (
        "porosity",
        "pore",
        "bubble",
        "shrinkage",
        "wrinkled shrinkage",
        "gas cavity",
        "pinholes",
        "surface cavity",
    ),
    "D9": (
        "mechanical properties",
        "micromechanical",
        "hardness",
        "tensile",
        "yield strength",
        "fracture",
        "processing-structure-property",
        "properties and solidification",
    ),
}

ALLOY_PATTERNS = (
    (re.compile(r"Al[-–]\s*([0-9.]+)\s*wt\.?%?\s*Cu", re.I), "Al-Cu"),
    (re.compile(r"Al[-–]\s*([0-9.]+)\s*wt\.?%?\s*Si", re.I), "Al-Si"),
    (re.compile(r"Al[-–]\s*Bi[-–]\s*Sn|aluminum[-–]bismuth[-–]tin", re.I), "Al-Bi-Sn"),
    (re.compile(r"Al[-–]\s*Bi", re.I), "Al-Bi"),
    (re.compile(r"Al[-–]\s*Pb", re.I), "Al-Pb"),
    (re.compile(r"Al[-–]\s*In", re.I), "Al-In"),
    (re.compile(r"Al[-–]\s*Ni", re.I), "Al-Ni"),
    (re.compile(r"Ti[-–]6Al[-–]4V|Ti64", re.I), "Ti-6Al-4V"),
    (re.compile(r"Co[-–]Cr[-–]Mo", re.I), "Co-Cr-Mo"),
    (re.compile(r"Zr50V50|Zr[-–]V", re.I), "Zr-V"),
    (re.compile(r"GaInSb|GaInSb", re.I), "GaInSb"),
    (re.compile(r"succinonitrile|SCN", re.I), "Succinonitrile model alloy"),
)

PLATFORM_RULES = (
    ("ISS", ("iss", "international space station")),
    ("China Space Station", ("china space station", "css")),
    ("Tiangong", ("tiangong",)),
    ("SJ-10", ("sj-10",)),
    ("Space Shuttle", ("space shuttle", "shuttle")),
    ("MASER sounding rocket", ("maser", "sounding rocket")),
    ("TEXUS sounding rocket", ("texus",)),
    ("Drop tube / drop shaft", ("drop tube", "drop shaft")),
    ("Ground-based microgravity analogue", ("static magnetic field", "earth experiments", "on earth")),
)

FACILITY_RULES = (
    ("ISS-EML", ("iss-eml", "electromagnetic levitation")),
    ("DECLIC-DSI", ("declic-dsi", "declic")),
    ("Materials Science Laboratory", ("materials science laboratory", "msl")),
    ("MEPHISTO", ("mephisto",)),
    ("TEMPUS", ("tempus",)),
    ("Transparent Alloys", ("transparent alloys",)),
    ("XRMON-GF", ("xrmon-gf",)),
    ("Bridgman apparatus", ("bridgman",)),
)


class PdfRecordBuilder:
    def __init__(self) -> None:
        self.pdf_agent = PdfAgent()

    def build_directory(self, pdf_dir: Path) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for path in sorted(pdf_dir.glob("*.pdf")):
            records.extend(self.build_pdf(path))
        return records

    def build_pdf(self, path: Path) -> list[dict[str, Any]]:
        text = self.pdf_agent._read_pdf_text(path)
        front = text[:20000]
        title = self._clean_filename(path)
        doi = self._front_doi(front)
        domains = self._classify(path, front)
        alloy = self._infer_alloy(path.name + "\n" + front[:6000])
        platform = self._infer_from_rules(path.name + "\n" + front[:6000], PLATFORM_RULES)
        facility = self._infer_from_rules(path.name + "\n" + front[:6000], FACILITY_RULES)
        reference = self._reference(title, doi, path)
        variables = self._variables(front)
        records = []
        for domain in domains:
            spec = DOMAINS[domain]
            records.append(
                {
                    "domain": domain,
                    "citation": {
                        "title": title,
                        "authors": [],
                        "year": self._year(front) or self._year(path.name),
                        "journal": None,
                        "doi": doi,
                        "reference": reference,
                        "source_type": "peer_reviewed" if doi else "pdf_extraction",
                        "url": f"local:{path.as_posix()}",
                    },
                    "alloy": alloy,
                    "composition": self._composition(path.name + "\n" + front),
                    "platform": platform,
                    "facility": facility,
                    "mission": self._mission(front),
                    "variables": variables,
                    "review_summary": self._summary(title, domain, alloy, platform, facility),
                    "key_findings": self._key_findings(title, domain, alloy, platform),
                    "theory_alignment": self._theory_alignment(domain),
                    "extraction_status": "quantitative_partial" if variables else "qualitative",
                    "evidence_level": self._evidence_level(title, domain),
                    "benchmark_match_type": self._benchmark_type(title, front),
                    "gap_flags": self._gap_flags(domain, doi, variables),
                    "flemings_alignment": list(spec.flemings_alignment),
                    "notes": f"Generated from local PDF: {path.as_posix()}; text_chars={len(text)}",
                }
            )
        return records

    def _clean_filename(self, path: Path) -> str:
        stem = path.stem
        if "_" in stem:
            parts = stem.split("_")
            if len(parts[-1]) <= 16 and re.fullmatch(r"[A-Za-z0-9 .-]+", parts[-1]):
                stem = "_".join(parts[:-1])
        title = stem.replace("+", " ").replace("_", " ")
        title = re.sub(r"\s+", " ", title).strip()
        return title

    def _front_doi(self, front: str) -> str | None:
        for match in DOI_RE.finditer(front[:12000]):
            doi = match.group(0).rstrip(".,);]")
            if "10.1016/0025-5416(84" in doi or doi.endswith("("):
                continue
            return doi
        return None

    def _classify(self, path: Path, front: str) -> list[str]:
        haystack = f"{path.stem}\n{front[:12000]}".lower()
        scores: dict[str, int] = {}
        for domain, terms in DOMAIN_RULES.items():
            score = 0
            for term in terms:
                if term in haystack:
                    score += 4 if term in path.stem.lower() else 1
            if score:
                scores[domain] = score
        if not scores:
            return ["D1"]
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        top_score = ranked[0][1]
        domains = [domain for domain, score in ranked if score >= max(2, top_score - 3)]
        return domains[:3]

    def _infer_alloy(self, text: str) -> str | None:
        hits = []
        for pattern, alloy in ALLOY_PATTERNS:
            if pattern.search(text):
                hits.append(alloy)
        return "; ".join(dict.fromkeys(hits)) if hits else None

    def _composition(self, text: str) -> str | None:
        comps = sorted(set(re.findall(r"\b[A-Z][a-z]?\s*[-–]\s*[0-9.]+\s*(?:wt\.?%|at\.?%)\s*[A-Z][a-z]?\b", text)))
        if comps:
            return "; ".join(comps[:6])
        comps = sorted(set(re.findall(r"\b(?:Al|Cu|Ni|Fe|Ti|Zr|V|Si|Ge|Ga|In|Sb|Bi|Sn|Pb|Co|Cr|Mo)[0-9]+(?:\.[0-9]+)?(?:[A-Z][a-z]?[0-9]+(?:\.[0-9]+)?)+\b", text)))
        return "; ".join(comps[:6]) if comps else None

    def _infer_from_rules(self, text: str, rules: tuple[tuple[str, tuple[str, ...]], ...]) -> str | None:
        lower = text.lower()
        for label, terms in rules:
            if any(term in lower for term in terms):
                return label
        return None

    def _mission(self, text: str) -> str | None:
        for term in ("CETSOL", "MICAST", "XRMON", "MASER-12", "MASER-14", "SJ-10", "IDGE"):
            if term.lower() in text.lower():
                return term
        return None

    def _year(self, text: str) -> int | None:
        years = [int(item) for item in re.findall(r"\b(19[7-9][0-9]|20[0-2][0-9])\b", text)]
        return min(years) if years else None

    def _reference(self, title: str, doi: str | None, path: Path) -> str:
        if doi:
            return f"{title}. https://doi.org/{doi}"
        return f"{title}. Local PDF extraction from {path.as_posix()}."

    def _variables(self, text: str) -> dict[str, Any]:
        variables: dict[str, Any] = {}
        cooling = self._range(text, r"([0-9]+(?:\.[0-9]+)?)\s*(?:K\s*s(?:−|-)?1|K/s|K\s+per\s+s)", 1, 10000000)
        if cooling:
            variables["cooling_rate_range_K_per_s"] = cooling
        undercooling = self._range_near(text, "undercool", r"([0-9]+(?:\.[0-9]+)?)\s*K", 0.001, 1000)
        if undercooling:
            variables["undercooling_range_K"] = undercooling
        gradient = self._range(text, r"([0-9]+(?:\.[0-9]+)?)\s*(?:K\s*cm(?:−|-)?1|K/cm)", 0.001, 10000)
        if gradient:
            variables["G_range_K_per_cm"] = gradient
        velocity = self._range(text, r"([0-9]+(?:\.[0-9]+)?)\s*(?:µm\s*s(?:−|-)?1|um/s|µm/s)", 0.001, 1000000)
        if velocity:
            variables["V_range_um_per_s"] = velocity
        gap = self._range_near(text, "gap", r"([0-9]+(?:\.[0-9]+)?)\s*(?:µm|um)", 0.001, 10000)
        if gap:
            variables["gap_width_range_um"] = gap
        return variables

    def _range(self, text: str, pattern: str, min_allowed: float, max_allowed: float) -> dict[str, float] | None:
        values = [float(match) for match in re.findall(pattern, text[:40000])]
        values = [value for value in values if min_allowed <= value <= max_allowed]
        if not values:
            return None
        return {"min": min(values), "max": max(values), "count": len(values)}

    def _range_near(self, text: str, term: str, pattern: str, min_allowed: float, max_allowed: float) -> dict[str, float] | None:
        values: list[float] = []
        lower = text.lower()
        for match in re.finditer(term, lower[:40000]):
            window = text[max(0, match.start() - 500) : match.end() + 500]
            values.extend(float(item) for item in re.findall(pattern, window))
        values = [value for value in values if min_allowed <= value <= max_allowed]
        if not values:
            return None
        return {"min": min(values), "max": max(values), "count": len(values)}

    def _summary(self, title: str, domain: str, alloy: str | None, platform: str | None, facility: str | None) -> str:
        subject = alloy or "the studied material system"
        place = ", ".join(item for item in (platform, facility) if item)
        suffix = f" using {place}" if place else ""
        return f"This local PDF contributes to {DOMAINS[domain].title} by documenting {subject}{suffix}. The record is generated from PDF text and should be upgraded after manual extraction of tables and figures."

    def _key_findings(self, title: str, domain: str, alloy: str | None, platform: str | None) -> list[str]:
        subject = alloy or "the material system"
        if domain == "D2":
            return [f"The paper is relevant to gravity-sensitive transport, convection, or macrosegregation in {subject}."]
        if domain == "D3":
            return [f"The paper is relevant to dendritic/cellular morphology or CET behavior in {subject}."]
        if domain == "D4":
            return [f"The paper is relevant to eutectic, peritectic, monotectic, or immiscible solidification in {subject}."]
        if domain == "D5":
            return [f"The paper is relevant to undercooling, nucleation, metastable phase selection, or interface kinetics in {subject}."]
        if domain == "D6":
            return [f"The paper is relevant to thermophysical properties, heat flow, plane-front stability, or Bridgman thermal modeling."]
        if domain == "D7":
            return [f"The paper is relevant to detached Bridgman growth, semiconductor crystals, or crystal-quality metrics."]
        if domain == "D8":
            return [f"The paper is relevant to shrinkage, pore, bubble, or defect formation under reduced gravity."]
        if domain == "D9":
            return [f"The paper may support processing-structure-property linkage or mechanical-property gap analysis."]
        return [f"The paper helps map alloy systems, platforms, and processing routes for {subject}."]

    def _theory_alignment(self, domain: str) -> str:
        return f"PDF-derived alignment: {', '.join(DOMAINS[domain].flemings_alignment)}."

    def _evidence_level(self, title: str, domain: str) -> str:
        lower = title.lower()
        if "review" in lower or "overview" in lower or "progress" in lower:
            return "review"
        if "model" in lower or "simulation" in lower or "computational" in lower:
            return "model"
        if "benchmark" in lower:
            return "benchmark"
        return "experiment"

    def _benchmark_type(self, title: str, front: str) -> str:
        lower = f"{title} {front[:3000]}".lower()
        if "microgravity and earth" in lower or "space and earth" in lower or "comparison of microgravity and earth" in lower:
            return "intra_study"
        return "none"

    def _gap_flags(self, domain: str, doi: str | None, variables: dict[str, Any]) -> list[str]:
        flags = ["pdf_generated_record", "requires_manual_table_extraction"]
        if not doi:
            flags.append("doi_not_found_in_pdf_front_matter")
        if not variables:
            flags.append("no_numeric_variables_auto_extracted")
        if domain == "D9":
            flags.append("mechanical_property_data_needs_manual_confirmation")
        return flags


def write_records(pdf_dir: Path, output: Path) -> int:
    records = PdfRecordBuilder().build_directory(pdf_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(records)
