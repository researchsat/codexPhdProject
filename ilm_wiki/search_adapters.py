from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class SearchResult:
    title: str
    authors: list[str]
    year: int | None
    doi: str | None
    reference: str
    url: str | None
    source: str


class CrossrefAdapter:
    """Small optional search adapter for DOI discovery.

    This adapter is intentionally metadata-only. Full quantitative extraction
    should come from PDFs or human-verified manual records.
    """

    endpoint = "https://api.crossref.org/works"

    def search(self, query: str, rows: int = 5) -> list[SearchResult]:
        url = f"{self.endpoint}?{urlencode({'query': query, 'rows': rows})}"
        request = Request(url, headers={"User-Agent": "ilm-wiki/0.1 (mailto:unknown@example.com)"})
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        items = payload.get("message", {}).get("items", [])
        results: list[SearchResult] = []
        for item in items:
            title = (item.get("title") or [None])[0]
            if not title:
                continue
            authors = [
                f"{author.get('family', '')}, {author.get('given', '')}".strip(", ")
                for author in item.get("author", [])
                if author.get("family") or author.get("given")
            ]
            year = None
            date_parts = item.get("published-print", item.get("published-online", {})).get("date-parts", [])
            if date_parts and date_parts[0]:
                year = date_parts[0][0]
            doi = item.get("DOI")
            journal = (item.get("container-title") or [""])[0]
            reference = f"{'; '.join(authors) if authors else 'Unknown'} ({year or 'n.d.'}). {title}. {journal}."
            results.append(
                SearchResult(
                    title=title,
                    authors=authors,
                    year=year,
                    doi=doi,
                    reference=reference,
                    url=item.get("URL"),
                    source="crossref",
                )
            )
        return results
