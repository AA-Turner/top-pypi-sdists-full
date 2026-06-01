"""`ingest_prowler` primitive — Prowler native JSON → Evidence records.

Mirrors `ingest_security_hub` and `ingest_config`: parse → look up
CheckID in the mapping table → emit Evidence record. Same skip
semantics:
- Unmapped CheckIDs: reported in skipped_unmapped_check_ids, no
  fabrication.
- MANUAL status: skipped (Prowler's MANUAL means "this check requires
  human inspection"; not actionable as evidence).
- PASS, FAIL: both flow through; Gap Agent reasons over them.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from efterlev.imports.prowler.mapping import ProwlerMapping, load_prowler_mapping
from efterlev.imports.prowler.parser import parse_prowler_document
from efterlev.models import Evidence, SourceRef
from efterlev.primitives.base import primitive


class IngestProwlerInput(BaseModel):
    """Input to `ingest_prowler`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    prowler_path: Path
    mapping_override: ProwlerMapping | None = None  # Test seam.


class IngestProwlerOutput(BaseModel):
    """Output: emitted Evidence list + skip metadata."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    evidence: list[Evidence]
    findings_total: int
    findings_emitted: int
    skipped_unmapped_check_ids: list[str] = Field(default_factory=list)
    skipped_manual_status: int = 0


@primitive(capability="evidence", side_effects=False, version="0.1.0", deterministic=True)
def ingest_prowler(input: IngestProwlerInput) -> IngestProwlerOutput:
    """Parse Prowler native JSON, map to KSIs, emit Evidence records."""
    findings = parse_prowler_document(input.prowler_path)
    mapping = input.mapping_override or load_prowler_mapping()

    evidence_list: list[Evidence] = []
    skipped_unmapped: list[str] = []
    skipped_manual = 0
    now = datetime.now(UTC)

    for idx, finding in enumerate(findings):
        if finding.Status == "MANUAL":
            skipped_manual += 1
            continue

        entry = mapping.lookup(finding.CheckID)
        if entry is None:
            if finding.CheckID not in skipped_unmapped:
                skipped_unmapped.append(finding.CheckID)
            continue

        source_ref = SourceRef(
            file=input.prowler_path,
            line_start=idx + 1,
        )

        evidence_list.append(
            Evidence.create(
                detector_id=f"aws.import.prowler.{entry.check_id}",
                ksis_evidenced=list(entry.ksis),
                controls_evidenced=list(entry.controls),
                source_ref=source_ref,
                content={
                    "import_source": "aws.prowler.native",
                    "prowler_check_id": finding.CheckID,
                    "prowler_status": finding.Status,
                    "prowler_severity": finding.Severity,
                    "prowler_check_title": finding.CheckTitle,
                    "prowler_status_extended": finding.StatusExtended,
                    "prowler_service_name": finding.ServiceName,
                    "prowler_resource_type": finding.ResourceType,
                    "prowler_resource_arn": finding.ResourceArn,
                    "prowler_resource_id": finding.ResourceId,
                    "prowler_account_id": finding.AccountId,
                    "prowler_region": finding.Region,
                    "prowler_assessment_start_time": finding.AssessmentStartTime,
                    # v0.1.163 / #368: Prowler is configuration-check based,
                    # not vulnerability-scan based — it doesn't emit CVE
                    # references. Empty list is intentional; cross-import
                    # shape consistency with Security Hub for the VDR
                    # generator's CVE-harvest path.
                    "cve_ids": [],
                    "evidence_strength": entry.evidence_strength,
                    "mapping_title": entry.title,
                },
                timestamp=now,
            )
        )

    return IngestProwlerOutput(
        evidence=evidence_list,
        findings_total=len(findings),
        findings_emitted=len(evidence_list),
        skipped_unmapped_check_ids=skipped_unmapped,
        skipped_manual_status=skipped_manual,
    )
