from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


@dataclass
class Citation:
    title: str | None = None
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    journal: str | None = None
    doi: str | None = None
    reference: str | None = None
    source_type: Literal["peer_reviewed", "technical_report", "conference", "manual", "pdf_extraction", "unknown"] = "unknown"
    url: str | None = None

    def __post_init__(self) -> None:
        if not self.doi and not self.reference:
            raise ValueError("citation must include doi or reference")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Citation":
        return cls(**data)


@dataclass
class LiteratureRecord:
    domain: str
    citation: Citation
    alloy: str | None = None
    composition: str | None = None
    platform: str | None = None
    facility: str | None = None
    mission: str | None = None
    variables: dict[str, Any] = field(default_factory=dict)
    benchmark_source: str | None = None
    benchmark_match_type: Literal["intra_study", "inter_study", "none"] = "none"
    gap_flags: list[str] = field(default_factory=list)
    flemings_alignment: list[str] = field(default_factory=list)
    notes: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LiteratureRecord":
        payload = dict(data)
        citation = payload.get("citation")
        if isinstance(citation, dict):
            payload["citation"] = Citation.from_dict(citation)
        if not isinstance(payload.get("citation"), Citation):
            raise ValueError("record must include a citation object")
        return cls(**payload)


@dataclass
class DomainHandoff:
    domain: str
    title: str
    minimum_sources: int
    records: list[LiteratureRecord] = field(default_factory=list)
    retry_required: bool = False
    qa_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PipelineOutput:
    domains: dict[str, DomainHandoff]
    linked_alloy_records: dict[str, dict[str, Any]]
    variable_groups: dict[str, list[dict[str, Any]]]
    benchmark_pairs: list[dict[str, Any]]
    gap_matrix: dict[str, dict[str, str]]
    qa_report: dict[str, Any]

