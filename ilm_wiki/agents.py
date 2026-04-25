from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from .domains import DOMAINS, DomainSpec
from .pdf_agent import PdfAgent, PdfExtraction
from .schemas import Citation, DomainHandoff, LiteratureRecord, PipelineOutput


VARIABLE_GROUPS = {
    "A_Process Variables": ("G_K_per_m", "V_um_per_s", "G_over_V", "cooling_rate_K_per_s", "duration", "microgravity_duration"),
    "B_Material Variables": ("alloy_system", "composition", "segregation_coefficient_k"),
    "C_Microstructure Variables": (
        "lambda1_um",
        "lambda1_um_microgravity",
        "lambda2_um",
        "lambda2_um_microgravity",
        "grain_size_um",
        "dendrite_tip_radius_um",
        "porosity_fraction_pct",
        "pore_volume_fraction_pct",
        "mean_pore_diameter_um",
    ),
    "D_Thermophysical Variables": (
        "thermal_conductivity_W_mK",
        "viscosity_mPa_s",
        "density_kg_m3",
        "surface_tension_N_m",
        "specific_heat_J_kgK",
        "thermal_diffusivity_m2_s",
    ),
    "E_Mechanical Variables": ("UTS_MPa", "yield_strength_MPa", "elongation_pct", "hardness", "fatigue_limit_MPa"),
    "F_Dimensionless Numbers": ("Ra", "Ma", "Gr", "Sc", "Pe", "Pe_thermal", "Pe_solutal"),
}

KEY_GAP_VARIABLES = (
    "G_K_per_m",
    "V_um_per_s",
    "lambda1_um_microgravity",
    "lambda1_um_1g",
    "porosity_fraction_pct",
    "UTS_MPa",
    "yield_strength_MPa",
    "hardness",
    "thermal_conductivity_W_mK",
)


class FetchAgent:
    def __init__(self, spec: DomainSpec):
        self.spec = spec

    def build_handoff(self, records: list[LiteratureRecord]) -> DomainHandoff:
        domain_records = [record for record in records if record.domain == self.spec.id]
        unique_sources = {
            record.citation.doi or record.citation.reference
            for record in domain_records
            if "example_record_not_for_analysis" not in record.gap_flags
        }
        qa_flags: list[str] = []
        retry_required = False
        if len(unique_sources) < self.spec.min_sources:
            retry_required = True
            qa_flags.append(
                f"Only {len(unique_sources)} traceable non-example sources found; minimum is {self.spec.min_sources}."
            )
        for record in domain_records:
            missing = [field for field in self.spec.target_fields if field not in record.variables and getattr(record, field, None) is None]
            if missing:
                record.gap_flags.append(f"missing_target_fields:{','.join(missing)}")
        return DomainHandoff(
            domain=self.spec.id,
            title=self.spec.title,
            minimum_sources=self.spec.min_sources,
            records=domain_records,
            retry_required=retry_required,
            qa_flags=qa_flags,
        )


class OrchestratorAgent:
    def __init__(self, pdf_dir: Path, manual_dir: Path, output_dir: Path):
        self.pdf_dir = pdf_dir
        self.manual_dir = manual_dir
        self.output_dir = output_dir

    def run(self) -> PipelineOutput:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        manual_records = self._load_manual_records(self.manual_dir)
        pdf_extractions = PdfAgent().process_directory(self.pdf_dir)
        pdf_records = self._records_from_pdf_extractions(pdf_extractions)
        records = manual_records + pdf_records
        handoffs = {
            domain_id: FetchAgent(spec).build_handoff(records)
            for domain_id, spec in DOMAINS.items()
        }
        analysis = AnalysisAgent(handoffs).run()
        pipeline_output = PipelineOutput(domains=handoffs, **analysis)
        ReportAgent(pipeline_output, self.output_dir).write_all()
        self._write_json("raw_domain_handoff.json", {key: value.to_dict() for key, value in handoffs.items()})
        self._write_json("pdf_extractions.json", [extraction.to_dict() for extraction in pdf_extractions])
        self._write_json("qa_report.json", pipeline_output.qa_report)
        return pipeline_output

    def _load_manual_records(self, manual_dir: Path) -> list[LiteratureRecord]:
        if not manual_dir.exists():
            return []
        records: list[LiteratureRecord] = []
        for path in sorted(manual_dir.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            items = data if isinstance(data, list) else [data]
            for item in items:
                try:
                    record = LiteratureRecord.from_dict(item)
                    if "example_record_not_for_analysis" not in record.gap_flags:
                        records.append(record)
                except ValueError as exc:
                    raise ValueError(f"Invalid manual record in {path}: {exc}") from exc
        return records

    def _records_from_pdf_extractions(self, extractions: list[PdfExtraction]) -> list[LiteratureRecord]:
        records: list[LiteratureRecord] = []
        for extraction in extractions:
            reference = extraction.reference_snippet or f"Local PDF extraction: {Path(extraction.path).name}"
            doi = extraction.doi_candidates[0] if extraction.doi_candidates else None
            citation = Citation(
                title=Path(extraction.path).stem,
                doi=doi,
                reference=reference,
                source_type="pdf_extraction",
            )
            domains = extraction.domain_matches or ["D1"]
            for domain in domains:
                spec = DOMAINS[domain]
                records.append(
                    LiteratureRecord(
                        domain=domain,
                        citation=citation,
                        alloy=extraction.alloy_candidates[0] if extraction.alloy_candidates else None,
                        platform=extraction.platform_candidates[0] if extraction.platform_candidates else None,
                        variables={},
                        gap_flags=["pdf_requires_human_quantitative_extraction"],
                        flemings_alignment=list(spec.flemings_alignment),
                        notes=f"PDF text chars: {extraction.text_chars}; DOI candidates: {', '.join(extraction.doi_candidates[:5]) or 'none'}",
                    )
                )
        return records

    def _write_json(self, filename: str, payload: Any) -> None:
        (self.output_dir / filename).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


class AnalysisAgent:
    def __init__(self, handoffs: dict[str, DomainHandoff]):
        self.handoffs = handoffs
        self.records = [record for handoff in handoffs.values() for record in handoff.records]

    def run(self) -> dict[str, Any]:
        return {
            "linked_alloy_records": self._linked_alloy_records(),
            "variable_groups": self._variable_groups(),
            "benchmark_pairs": self._benchmark_pairs(),
            "gap_matrix": self._gap_matrix(),
            "qa_report": self._qa_report(),
        }

    def _linked_alloy_records(self) -> dict[str, dict[str, Any]]:
        linked: dict[str, dict[str, Any]] = {}
        for record in self.records:
            alloy = record.alloy or "Unknown alloy"
            slot = linked.setdefault(alloy, {"domains": set(), "platforms": set(), "process": {}, "microstructure": {}, "properties": {}, "citations": set()})
            slot["domains"].add(record.domain)
            if record.platform:
                slot["platforms"].add(record.platform)
            citation_key = record.citation.doi or record.citation.reference
            slot["citations"].add(citation_key)
            for key, value in record.variables.items():
                if value is None:
                    continue
                if key in VARIABLE_GROUPS["A_Process Variables"]:
                    slot["process"][key] = value
                elif key in VARIABLE_GROUPS["C_Microstructure Variables"]:
                    slot["microstructure"][key] = value
                elif key in VARIABLE_GROUPS["E_Mechanical Variables"]:
                    slot["properties"][key] = value
        return {
            alloy: {
                **data,
                "domains": sorted(data["domains"]),
                "platforms": sorted(data["platforms"]),
                "citations": sorted(data["citations"]),
                "single_paper_flag": len(data["citations"]) == 1,
            }
            for alloy, data in linked.items()
        }

    def _variable_groups(self) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for group, keys in VARIABLE_GROUPS.items():
            rows = []
            for key in keys:
                values: list[float] = []
                domains: set[str] = set()
                platforms: set[str] = set()
                for record in self.records:
                    value = record.variables.get(key)
                    if isinstance(value, int | float) and not isinstance(value, bool):
                        values.append(float(value))
                        domains.add(record.domain)
                        if record.platform:
                            platforms.add(record.platform)
                if values:
                    rows.append(
                        {
                            "variable": key,
                            "count": len(values),
                            "min": min(values),
                            "max": max(values),
                            "mean": statistics.mean(values),
                            "std": statistics.pstdev(values) if len(values) > 1 else 0.0,
                            "domains": sorted(domains),
                            "platforms": sorted(platforms),
                        }
                    )
            grouped[group] = rows
        return grouped

    def _benchmark_pairs(self) -> list[dict[str, Any]]:
        pairs: list[dict[str, Any]] = []
        for record in self.records:
            for key, ug_value in record.variables.items():
                if not key.endswith("_microgravity"):
                    continue
                base = key.removesuffix("_microgravity")
                one_g_key = f"{base}_1g"
                one_g_value = record.variables.get(one_g_key)
                if one_g_value is None:
                    continue
                pct = None
                if isinstance(ug_value, int | float) and isinstance(one_g_value, int | float) and one_g_value:
                    pct = ((ug_value - one_g_value) / one_g_value) * 100.0
                pairs.append(
                    {
                        "domain": record.domain,
                        "variable": base,
                        "alloy": record.alloy,
                        "value_1g": one_g_value,
                        "value_microgravity": ug_value,
                        "percent_difference": pct,
                        "platform": record.platform,
                        "reference": record.citation.doi or record.citation.reference,
                        "benchmark_match_type": record.benchmark_match_type,
                    }
                )
        return pairs

    def _gap_matrix(self) -> dict[str, dict[str, str]]:
        alloys = sorted({record.alloy or "Unknown alloy" for record in self.records})
        matrix: dict[str, dict[str, str]] = {}
        for alloy in alloys:
            alloy_records = [record for record in self.records if (record.alloy or "Unknown alloy") == alloy]
            matrix[alloy] = {}
            for variable in KEY_GAP_VARIABLES:
                has_ug = any(self._has_variable(record, variable, "microgravity") for record in alloy_records)
                has_1g = any(self._has_variable(record, variable, "1g") for record in alloy_records)
                if has_ug and has_1g:
                    mark = "✓"
                elif has_ug:
                    mark = "µg only"
                elif has_1g:
                    mark = "1g only"
                else:
                    mark = "✗"
                matrix[alloy][variable] = mark
        return matrix

    def _has_variable(self, record: LiteratureRecord, variable: str, condition: str) -> bool:
        if condition == "microgravity":
            return record.variables.get(variable) is not None or record.variables.get(f"{variable}_microgravity") is not None
        return record.variables.get(f"{variable}_1g") is not None

    def _qa_report(self) -> dict[str, Any]:
        domain_qa = {domain: handoff.qa_flags for domain, handoff in self.handoffs.items()}
        retry_domains = [domain for domain, handoff in self.handoffs.items() if handoff.retry_required]
        records_missing_benchmark = [
            record.citation.doi or record.citation.reference
            for record in self.records
            if record.benchmark_match_type == "none"
        ]
        return {
            "domain_qa": domain_qa,
            "retry_domains": retry_domains,
            "records_total": len(self.records),
            "records_missing_benchmark_count": len(records_missing_benchmark),
            "status": "human_review_required" if retry_domains else "complete",
        }


class ReportAgent:
    def __init__(self, output: PipelineOutput, output_dir: Path):
        self.output = output
        self.output_dir = output_dir

    def write_all(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "microgravity_solidification_wiki.md").write_text(self._wiki(), encoding="utf-8")
        (self.output_dir / "1g_vs_microgravity_benchmark_table.md").write_text(self._benchmarks(), encoding="utf-8")
        (self.output_dir / "variable_groups_consolidated.md").write_text(self._variable_groups(), encoding="utf-8")
        (self.output_dir / "gap_matrix.md").write_text(self._gap_matrix(), encoding="utf-8")

    def _wiki(self) -> str:
        lines = ["# Microgravity Metal Alloy Solidification - Literature Wiki", "", "## Table of Contents"]
        for domain_id, handoff in self.output.domains.items():
            lines.append(f"- [{domain_id}. {handoff.title}](#{domain_id.lower()}-{self._anchor(handoff.title)})")
        lines.extend(["- [10. Cross-Domain Variable Groups](#10-cross-domain-variable-groups)", "- [11. Literature Gap Analysis](#11-literature-gap-analysis)", ""])
        for domain_id, handoff in self.output.domains.items():
            lines.extend(self._domain_section(domain_id, handoff))
        lines.extend(["## 10. Cross-Domain Variable Groups", ""])
        lines.append("The analysis agent groups extracted values into process, material, microstructure, thermophysical, mechanical, and dimensionless-number categories. Empty rows indicate that no validated quantitative value has been ingested yet.")
        for group, rows in self.output.variable_groups.items():
            lines.extend([f"### {group}", ""])
            lines.extend(self._table(rows, ["variable", "count", "min", "max", "mean", "std", "domains", "platforms"]))
        lines.extend(["## 11. Literature Gap Analysis", ""])
        lines.append(f"Pipeline status: `{self.output.qa_report['status']}`. Domains requiring expanded search or human curation: {', '.join(self.output.qa_report['retry_domains']) or 'none'}.")
        lines.append("")
        return "\n".join(lines)

    def _domain_section(self, domain_id: str, handoff: DomainHandoff) -> list[str]:
        lines = [f"## {domain_id}. {handoff.title}", ""]
        lines.append(f"Flemings alignment: {', '.join(DOMAINS[domain_id].flemings_alignment)}.")
        lines.append("")
        lines.append("Key findings are limited to the traceable records currently ingested. The system flags this section for retry when the source count is below the configured threshold.")
        lines.append("")
        if handoff.qa_flags:
            lines.append("QA flags: " + "; ".join(handoff.qa_flags))
            lines.append("")
        rows = []
        for record in handoff.records:
            rows.append(
                {
                    "alloy": record.alloy,
                    "platform": record.platform,
                    "facility": record.facility,
                    "variables": self._compact_variables(record.variables),
                    "citation": record.citation.doi or record.citation.reference,
                    "gaps": "; ".join(record.gap_flags),
                }
            )
        lines.extend(self._table(rows, ["alloy", "platform", "facility", "variables", "citation", "gaps"]))
        lines.extend(["### Citations", ""])
        citations = sorted({record.citation.reference or record.citation.doi or "Unknown" for record in handoff.records})
        if citations:
            lines.extend(f"- {citation}" for citation in citations)
        else:
            lines.append("- No validated sources ingested yet.")
        lines.append("")
        return lines

    def _benchmarks(self) -> str:
        lines = ["# 1g vs Microgravity Benchmark Table", ""]
        rows = self.output.benchmark_pairs
        if not rows:
            lines.append("No benchmark pairs with both 1g and microgravity values have been ingested yet.")
            lines.append("")
            return "\n".join(lines)
        by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            by_domain[row["domain"]].append(row)
        for domain, domain_rows in sorted(by_domain.items()):
            lines.extend([f"## {domain}. {DOMAINS[domain].title}", ""])
            lines.extend(self._table(sorted(domain_rows, key=lambda item: str(item.get("alloy"))), ["variable", "alloy", "value_1g", "value_microgravity", "percent_difference", "platform", "reference", "benchmark_match_type"]))
        return "\n".join(lines)

    def _variable_groups(self) -> str:
        lines = ["# Consolidated Variable Groups", ""]
        for group, rows in self.output.variable_groups.items():
            lines.extend([f"## {group}", ""])
            lines.extend(self._table(rows, ["variable", "count", "min", "max", "mean", "std", "domains", "platforms"]))
        return "\n".join(lines)

    def _gap_matrix(self) -> str:
        lines = ["# Gap Matrix", ""]
        headers = ["Alloy System", *KEY_GAP_VARIABLES]
        rows = [{"Alloy System": alloy, **values} for alloy, values in self.output.gap_matrix.items()]
        lines.extend(self._table(rows, headers))
        lines.extend(["## Narrative Gap Analysis", ""])
        lines.append("Cells marked `✓` have both 1g and microgravity values. `µg only` and `1g only` identify incomplete benchmarks. `✗` marks variables absent from the ingested corpus.")
        lines.append("")
        lines.append("Priority recommendation: curate verified quantitative records for every retry domain, then rerun the pipeline so benchmark pairing and variable statistics become meaningful.")
        lines.append("")
        return "\n".join(lines)

    def _table(self, rows: list[dict[str, Any]], headers: list[str]) -> list[str]:
        if not rows:
            return ["No validated rows yet.", ""]
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for row in rows:
            lines.append("| " + " | ".join(self._cell(row.get(header)) for header in headers) + " |")
        lines.append("")
        return lines

    def _cell(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, float):
            if math.isfinite(value):
                return f"{value:.4g}"
            return ""
        if isinstance(value, list):
            return ", ".join(str(item) for item in value)
        return str(value).replace("\n", " ").replace("|", "\\|")

    def _compact_variables(self, variables: dict[str, Any]) -> str:
        populated = {key: value for key, value in variables.items() if value is not None}
        if not populated:
            return ""
        return "; ".join(f"{key}={value}" for key, value in populated.items())

    def _anchor(self, text: str) -> str:
        return text.lower().replace("&", "").replace(",", "").replace("/", "").replace(" ", "-")
