"""ASFF generator-id → KSI mapping table loader.

The mapping itself lives in `mapping.yaml` next to this module so it
reads + reviews like data, not code. Loader vendors the YAML at
package-data inclusion time; refresh the file when expanding the
Security Hub standards coverage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

EvidenceStrength = Literal["high", "medium", "low"]


class AsffMappingEntry(BaseModel):
    """One generator-id → KSI mapping entry."""

    model_config = ConfigDict(frozen=True)

    generator_id: str
    title: str
    ksis: list[str]
    controls: list[str]
    evidence_strength: EvidenceStrength = "medium"


class AsffMapping(BaseModel):
    """The full mapping table loaded from mapping.yaml."""

    model_config = ConfigDict(frozen=True)

    mappings: list[AsffMappingEntry] = Field(default_factory=list)

    def lookup(self, generator_id: str) -> AsffMappingEntry | None:
        """Return the mapping for `generator_id`, or None if unmapped."""
        for entry in self.mappings:
            if entry.generator_id == generator_id:
                return entry
        return None


def load_asff_mapping(path: Path | None = None) -> AsffMapping:
    """Load the vendored ASFF mapping table.

    `path` override is for testing; production callers omit it and
    load the package-data YAML next to this module.
    """
    if path is None:
        path = Path(__file__).parent / "mapping.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"ASFF mapping file must be a dict; got {type(raw).__name__}")
    return AsffMapping.model_validate(raw)
