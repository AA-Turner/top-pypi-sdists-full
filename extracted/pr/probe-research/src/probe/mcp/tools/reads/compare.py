"""research_compare: two or more entities side by side, one list per requested dimension."""

from __future__ import annotations
from dataclasses import dataclass

from probe.mcp.tools.shaping.payload import to_dict


@dataclass(frozen=True, slots=True)
class ComparedEntity:
    """One compared ref and the record it resolved to."""

    ref: str
    entity_type: str
    entity: dict


@dataclass(frozen=True, slots=True)
class ComparePayload:
    """The entities in ref order, and per dimension one value per entity in that same order."""

    entities: list[ComparedEntity]
    comparison: dict[str, list]


class CompareMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def research_compare(
        self,
        refs: list[str],
        dimensions: list[str] | None = None,
    ) -> dict:
        if len(refs) < 2:
            raise ValueError("compare requires at least two refs")
        rows = []
        for ref in refs:
            kind, entity = self.source.get(ref)
            rows.append(ComparedEntity(ref=ref, entity_type=kind, entity=entity))
        requested = dimensions or ["config", "metadata", "summary", "status", "question"]
        comparison = {
            dimension: [row.entity.get(dimension) for row in rows] for dimension in requested
        }
        return self._envelope(to_dict(ComparePayload(entities=rows, comparison=comparison)))
