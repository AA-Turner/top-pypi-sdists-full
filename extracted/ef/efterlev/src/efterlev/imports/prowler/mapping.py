"""Prowler CheckID → KSI mapping table loader.

Mirrors `efterlev.imports.security_hub.mapping` and
`efterlev.imports.config.mapping` — same shape, different key
(`check_id`).
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

EvidenceStrength = Literal["high", "medium", "low"]


class ProwlerMappingEntry(BaseModel):
    """One Prowler CheckID → KSI mapping entry."""

    model_config = ConfigDict(frozen=True)

    check_id: str
    title: str
    ksis: list[str]
    controls: list[str]
    evidence_strength: EvidenceStrength = "medium"


class ProwlerMapping(BaseModel):
    """The full mapping table loaded from mapping.yaml."""

    model_config = ConfigDict(frozen=True)

    mappings: list[ProwlerMappingEntry] = Field(default_factory=list)

    def lookup(self, check_id: str) -> ProwlerMappingEntry | None:
        for entry in self.mappings:
            if entry.check_id == check_id:
                return entry
        return None


def load_prowler_mapping(path: Path | None = None) -> ProwlerMapping:
    """Load the vendored Prowler mapping table."""
    if path is None:
        path = Path(__file__).parent / "mapping.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Prowler mapping file must be a dict; got {type(raw).__name__}")
    return ProwlerMapping.model_validate(raw)
