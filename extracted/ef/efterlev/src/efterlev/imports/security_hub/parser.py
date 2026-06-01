"""ASFF (AWS Security Finding Format) JSON parser.

ASFF is the canonical Security Hub findings shape. Spec:
https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html

This parser handles only the fields M1 Stage 1 needs:
- `Id` — finding ARN, used for deterministic content addressing
- `GeneratorId` — control identifier (ASFF generator-id → KSI mapping key)
- `Compliance.Status` — PASSED / FAILED / WARNING / NOT_AVAILABLE
- `Severity.Label` — INFORMATIONAL / LOW / MEDIUM / HIGH / CRITICAL
- `Title` + `Description` — human-readable, carried into Evidence.content
- `Resources[]` — affected AWS resource ARNs
- `FirstObservedAt` / `UpdatedAt` — timestamps

Fields the parser does NOT consume at v0.1.113 (deferred):
- `Workflow.Status` (NEW / NOTIFIED / SUPPRESSED / RESOLVED) — relevant
  for filtering but adds policy decisions; ship raw at v0.1.113.
- `Note` (analyst annotations) — relevant for evidence-richness;
  defer until customer pull surfaces a need.

Added in v0.1.163 / #368 for VDR (RFC-0012) integration:
- `Vulnerabilities[]` (CVE shape) — Inspector-style findings carry
  one or more CVE IDs per finding. Parsed and surfaced through
  `cve_ids` so the VDR generator can populate the RFC-0012
  `cve_ids` field on the resulting entry. Each entry in
  `Vulnerabilities[]` has an `Id` field (the CVE id) per the
  ASFF spec; we collect all of them.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

AsffComplianceStatus = Literal["PASSED", "FAILED", "WARNING", "NOT_AVAILABLE"]
"""ASFF Compliance.Status field values per the AWS spec."""

AsffSeverityLabel = Literal["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
"""ASFF Severity.Label field values per the AWS spec."""


class AsffResource(BaseModel):
    """One affected resource per ASFF spec Resources[]."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    Type: str
    Id: str  # ARN
    Region: str | None = None


class AsffFinding(BaseModel):
    """One parsed ASFF finding. Strict on required fields, lenient otherwise."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    # Required by ASFF spec.
    Id: str  # ARN; canonical finding identifier
    ProductArn: str
    GeneratorId: str
    Title: str
    Description: str
    Resources: list[AsffResource] = Field(default_factory=list)

    # Required by ASFF spec but we tolerate missing for malformed inputs;
    # downstream mapping handles missing-field cases.
    Compliance: dict[str, Any] = Field(default_factory=dict)
    Severity: dict[str, Any] = Field(default_factory=dict)

    # Timestamps (ISO-8601 strings per ASFF spec).
    FirstObservedAt: str | None = None
    UpdatedAt: str | None = None

    # v0.1.163 / #368: Inspector-style CVE entries. Each item per the
    # ASFF spec is `{"Id": "CVE-YYYY-NNNN", ...}` plus optional
    # severity / cvss / references. We only need `Id` for VDR threading.
    # Empty list (default) for non-vulnerability findings (compliance
    # control failures, configuration drift, etc.).
    Vulnerabilities: list[dict[str, Any]] = Field(default_factory=list)

    @property
    def cve_ids(self) -> list[str]:
        """Extract CVE IDs from the `Vulnerabilities[]` array (v0.1.163).

        Empty list when the finding isn't a CVE-shaped one (the majority
        of compliance-control findings have no Vulnerabilities block).
        Order preserved from the source ASFF; deduped.
        """
        seen: set[str] = set()
        result: list[str] = []
        for vuln in self.Vulnerabilities:
            vid = vuln.get("Id") if isinstance(vuln, dict) else None
            if isinstance(vid, str) and vid not in seen:
                seen.add(vid)
                result.append(vid)
        return result

    @property
    def compliance_status(self) -> AsffComplianceStatus | None:
        """Return Compliance.Status if it's a known enum value, else None."""
        status = self.Compliance.get("Status")
        if status in ("PASSED", "FAILED", "WARNING", "NOT_AVAILABLE"):
            return status  # type: ignore[return-value]
        return None

    @property
    def severity_label(self) -> AsffSeverityLabel | None:
        """Return Severity.Label if it's a known enum value, else None."""
        label = self.Severity.get("Label")
        if label in ("INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"):
            return label  # type: ignore[return-value]
        return None


class AsffParseError(ValueError):
    """Raised when an ASFF document is structurally invalid."""


def parse_asff_document(path: Path) -> list[AsffFinding]:
    """Parse an ASFF JSON file into a list of AsffFinding records.

    Accepts both shapes the ASFF spec allows:
    - Top-level `{"Findings": [...]}` (the `aws securityhub get-findings` shape)
    - A bare array `[...]` of finding objects (the export-via-EventBridge shape)

    Findings that fail Pydantic validation (missing required fields like
    Id or GeneratorId) are skipped silently — ASFF in the wild can have
    soft schema drift, and we don't want one malformed finding to abort
    the entire ingest.
    """
    if not path.is_file():
        raise FileNotFoundError(f"ASFF input not found: {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise AsffParseError(f"ASFF input is not valid JSON: {e}") from e

    if isinstance(raw, dict) and "Findings" in raw:
        findings_raw = raw["Findings"]
    elif isinstance(raw, list):
        findings_raw = raw
    else:
        raise AsffParseError(
            f"ASFF input must be either a dict with `Findings` key or a "
            f"top-level array; got {type(raw).__name__}"
        )

    if not isinstance(findings_raw, list):
        raise AsffParseError(f"`Findings` must be a list; got {type(findings_raw).__name__}")

    out: list[AsffFinding] = []
    for entry in findings_raw:
        if not isinstance(entry, dict):
            continue
        try:
            out.append(AsffFinding.model_validate(entry))
        except ValidationError:
            continue
    return out
