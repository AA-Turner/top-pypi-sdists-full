"""Ground-truth schema + YAML loader for the eval harness.

Each fixture under `evals/fixtures/<id>/` carries a `GROUND_TRUTH.yaml`
that names the human-labeled expected outputs the harness measures
agent runs against.

The schema is intentionally narrow at Phase 1 (DECISIONS 2026-05-08
"v0.2 eval harness -- Phase 1 scope"):

  - `expected_classifications`: per-KSI expected status. Supports
    `<status>` OR `<status>|<status>` to express acceptable
    alternatives (resolves the sketch's open question on
    `evidence_layer_inapplicable`).
  - `expected_rationale_resources`: per-KSI substring match
    requirements for narrative quality (M3 metric).
  - `expected_manifest_quoting`: per-KSI required substrings from
    procedural manifest narratives (M4 metric).
  - `expected_poam`: POAM scope discipline (M5 metric).

Plus required metadata fields that lock the schema to a specific FRMR
catalog version and maintainer (changes there break the loader, so
silent label drift can't happen).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator

# Pinned to FRMR 0.9.43-beta. Updates require a fresh ground-truth
# audit (KSI ids may have moved; statuses may have been redefined).
# Mismatch = loader rejects the fixture; fail-closed at Phase 1.
SUPPORTED_FRMR_VERSIONS = {"0.9.43-beta"}

# The classifications the gap agent emits. Single source of truth so
# the loader can validate label values against the canonical set.
GapStatus = Literal[
    "implemented",
    "partial",
    "not_implemented",
    "evidence_layer_inapplicable",
    "not_applicable",
]


class POAMExpectations(BaseModel):
    """Per-fixture POAM scope expectations (drives metric M5).

    `excluded_count_min` / `excluded_count_max` bound how many items
    the POAM should mark `excluded_out_of_boundary`. `must_not_mention`
    is a list of substrings that MUST NOT appear in any POAM rationale
    (catches boundary leaks where OOB resource names slip into the
    in-boundary narrative).
    """

    excluded_count_min: int = Field(default=0, ge=0)
    excluded_count_max: int = Field(default=60, ge=0)
    must_not_mention: list[str] = Field(default_factory=list)

    @field_validator("excluded_count_max")
    @classmethod
    def _max_ge_min(cls, v: int, info: object) -> int:
        # Pydantic v2 passes a FieldValidationInfo; we read the already-
        # validated `excluded_count_min` from .data. The field-order
        # default for the model has _min before _max, so .data is
        # populated by the time _max validates.
        data = getattr(info, "data", {}) or {}
        if "excluded_count_min" in data and v < data["excluded_count_min"]:
            raise ValueError(
                f"excluded_count_max ({v}) must be >= excluded_count_min "
                f"({data['excluded_count_min']})"
            )
        return v


class GroundTruth(BaseModel):
    """Per-fixture ground-truth labels.

    `expected_classifications` keys are KSI ids (e.g. `KSI-SVC-VRI`).
    Values are either a single GapStatus or `<status1>|<status2>`
    when multiple verdicts are acceptable (e.g. a procedural-only KSI
    may legitimately classify as `evidence_layer_inapplicable` OR
    `not_applicable` depending on whether a manifest is present).
    """

    fixture_id: str
    description: str
    authored_by: str
    authored_at: str  # ISO date string; YAML parser reads as str
    revision: int = Field(ge=1)
    frmr_version: str

    expected_classifications: dict[str, str] = Field(default_factory=dict)
    expected_rationale_resources: dict[str, list[str]] = Field(default_factory=dict)
    expected_manifest_quoting: dict[str, list[str]] = Field(default_factory=dict)
    expected_poam: POAMExpectations = Field(default_factory=POAMExpectations)

    @field_validator("authored_at", mode="before")
    @classmethod
    def _coerce_date_to_isoformat(cls, v: object) -> object:
        # PyYAML returns datetime.date for unquoted ISO dates. Coerce
        # to the YYYY-MM-DD string form so authors can write either
        # `authored_at: 2026-05-08` (date) or `authored_at: "2026-05-08"`
        # (string) and both work.
        if isinstance(v, date):
            return v.isoformat()
        return v

    @field_validator("frmr_version")
    @classmethod
    def _frmr_version_supported(cls, v: str) -> str:
        if v not in SUPPORTED_FRMR_VERSIONS:
            raise ValueError(
                f"ground-truth FRMR version {v!r} not in supported set "
                f"{sorted(SUPPORTED_FRMR_VERSIONS)}. Phase 1 fails closed; "
                f"a migration tool ships in Phase 2."
            )
        return v

    @field_validator("expected_classifications")
    @classmethod
    def _classifications_valid(cls, v: dict[str, str]) -> dict[str, str]:
        valid_statuses = set(GapStatus.__args__)  # type: ignore[attr-defined]
        for ksi, value in v.items():
            for option in value.split("|"):
                option = option.strip()
                if option not in valid_statuses:
                    raise ValueError(
                        f"expected_classifications[{ksi!r}] = {value!r}: "
                        f"unrecognized status {option!r}. Valid values: "
                        f"{sorted(valid_statuses)}. Use `|` to express "
                        f"acceptable alternatives (e.g. 'partial|not_implemented')."
                    )
        return v

    def acceptable_statuses(self, ksi_id: str) -> set[str] | None:
        """Return the set of acceptable statuses for a KSI, or None if
        the fixture didn't label this KSI (loader skips unlabeled KSIs
        in metric calculations rather than penalizing).
        """
        raw = self.expected_classifications.get(ksi_id)
        if raw is None:
            return None
        return {opt.strip() for opt in raw.split("|")}


def load_ground_truth(path: Path) -> GroundTruth:
    """Load + validate a ground-truth YAML file.

    Raises:
      FileNotFoundError: path doesn't exist.
      ValueError: YAML parse error or schema validation failure
        (including unsupported FRMR version, invalid status values).
    """
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(
            f"{path}: expected a YAML mapping at the top level, got {type(raw).__name__}"
        )
    return GroundTruth.model_validate(raw)
