"""AWS Config rule-name → KSI mapping table loader.

Mirrors `efterlev.imports.security_hub.mapping` — same shape, different
key (`config_rule_name` vs `generator_id`).
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

EvidenceStrength = Literal["high", "medium", "low"]


class ConfigMappingEntry(BaseModel):
    """One Config-rule → KSI mapping entry."""

    model_config = ConfigDict(frozen=True)

    config_rule_name: str
    title: str
    ksis: list[str]
    controls: list[str]
    evidence_strength: EvidenceStrength = "medium"


class ConfigMapping(BaseModel):
    """The full mapping table loaded from mapping.yaml."""

    model_config = ConfigDict(frozen=True)

    mappings: list[ConfigMappingEntry] = Field(default_factory=list)

    def lookup(self, config_rule_name: str) -> ConfigMappingEntry | None:
        for entry in self.mappings:
            if entry.config_rule_name == config_rule_name:
                return entry
        return None


def load_config_mapping(path: Path | None = None) -> ConfigMapping:
    """Load the vendored Config mapping table."""
    if path is None:
        path = Path(__file__).parent / "mapping.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Config mapping file must be a dict; got {type(raw).__name__}")
    return ConfigMapping.model_validate(raw)
