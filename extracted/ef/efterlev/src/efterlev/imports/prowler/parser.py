"""Prowler native JSON parser.

Prowler's `prowler aws -M json` produces a top-level array of finding
objects; older versions / certain wrappers may emit `{"findings": [...]}`.
This parser accepts both shapes.

Spec reference (Prowler v4+ output schema):
https://docs.prowler.com/projects/prowler-open-source/en/latest/tutorials/reporting/

The fields we consume at v0.1.123 (intentionally minimal):
- `CheckID` — canonical check identifier (mapping table key)
- `Status` — PASS / FAIL / MANUAL
- `CheckTitle` + `Description` — human-readable
- `ServiceName` + `ResourceType` — categorization
- `ResourceArn` (or `ResourceId`) — affected resource
- `Severity` — informational / low / medium / high / critical
- `AccountId`, `Region`, `Provider` — context
- `StatusExtended` — finding-specific narrative
- `AssessmentStartTime` — timestamp

Fields we ignore at v0.1.123 (deferred):
- `Remediation` (rich object) — useful but not evidence-bearing for KSI mapping
- `Compliance` (per-framework labels) — Prowler emits its own framework
  mappings; we use the CheckID → KSI mapping table instead
- `RelatedUrl`, `Categories`, `Risk`, `Notes` — informational, not load-bearing
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

ProwlerStatus = Literal["PASS", "FAIL", "MANUAL"]
"""Prowler's 3-state Status field per the v4+ schema."""

ProwlerSeverity = Literal["informational", "low", "medium", "high", "critical"]


class ProwlerFinding(BaseModel):
    """One parsed Prowler finding. Strict on required fields, lenient otherwise."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    # Required by Prowler schema.
    CheckID: str
    Status: ProwlerStatus
    CheckTitle: str
    ServiceName: str
    Provider: str = "aws"

    # Recommended but tolerated as missing.
    AccountId: str | None = None
    Region: str | None = None
    Description: str = ""
    StatusExtended: str = ""
    ResourceType: str = ""
    ResourceArn: str = ""
    ResourceId: str = ""
    Severity: str = "medium"  # Pydantic-wide; not Literal-validated for forward-compat
    AssessmentStartTime: str | None = None
    ResourceTags: dict[str, str] | list = Field(default_factory=dict)


class ProwlerParseError(ValueError):
    """Raised when a Prowler document is structurally invalid."""


def parse_prowler_document(path: Path) -> list[ProwlerFinding]:
    """Parse a Prowler native JSON file.

    Accepts both shapes:
    - Top-level array `[...]` (the `prowler aws -M json` default)
    - `{"findings": [...]}` (some wrappers use this)

    Soft schema drift handling: findings that fail Pydantic validation
    are skipped silently — Prowler's schema has changed across major
    versions and we don't want one malformed finding to abort the
    entire ingest.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Prowler input not found: {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ProwlerParseError(f"Prowler input is not valid JSON: {e}") from e

    if isinstance(raw, dict) and "findings" in raw:
        findings_raw = raw["findings"]
    elif isinstance(raw, list):
        findings_raw = raw
    else:
        raise ProwlerParseError(
            f"Prowler input must be either a dict with `findings` key or "
            f"a top-level array; got {type(raw).__name__}"
        )

    if not isinstance(findings_raw, list):
        raise ProwlerParseError(f"`findings` must be a list; got {type(findings_raw).__name__}")

    out: list[ProwlerFinding] = []
    for entry in findings_raw:
        if not isinstance(entry, dict):
            continue
        try:
            out.append(ProwlerFinding.model_validate(entry))
        except ValidationError:
            continue
    return out
