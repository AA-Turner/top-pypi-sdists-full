"""`ingest_security_hub` primitive — ASFF JSON → Evidence records.

Orchestrates: parse ASFF → look up each finding's GeneratorId in the
mapping table → emit Evidence records into the active provenance store.

Findings whose GeneratorId isn't in the mapping table are skipped + reported
in the output (no fabrication, same posture as `generate_poam_oscal`'s
`skipped_unknown_ksi`).

Honest scope at v0.1.113:
- Compliance.Status PASSED, FAILED, WARNING all flow through (let Gap
  Agent reason). NOT_AVAILABLE is skipped (no signal).
- Out-of-IaC findings carry `boundary_state="boundary_undeclared"`
  unconditionally — boundary scoping doesn't apply to runtime findings
  the way it does to IaC source files.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from efterlev.imports.security_hub.mapping import AsffMapping, load_asff_mapping
from efterlev.imports.security_hub.parser import parse_asff_document
from efterlev.models import Evidence, SourceRef
from efterlev.primitives.base import primitive


class IngestSecurityHubInput(BaseModel):
    """Input to `ingest_security_hub`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    asff_path: Path
    mapping_override: AsffMapping | None = None  # Test seam; production omits.


class IngestSecurityHubOutput(BaseModel):
    """Output: emitted Evidence list + skip metadata."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    evidence: list[Evidence]
    findings_total: int
    findings_emitted: int
    skipped_unmapped_generator_ids: list[str] = Field(default_factory=list)
    skipped_status_not_available: int = 0


@primitive(capability="evidence", side_effects=False, version="0.1.0", deterministic=True)
def ingest_security_hub(input: IngestSecurityHubInput) -> IngestSecurityHubOutput:
    """Parse ASFF, map to KSIs, emit Evidence records.

    Returns the Evidence list; caller writes to the provenance store
    (separating the deterministic transform from the I/O side effect
    matches the rest of the primitives layer).
    """
    findings = parse_asff_document(input.asff_path)
    mapping = input.mapping_override or load_asff_mapping()

    evidence_list: list[Evidence] = []
    skipped_unmapped: list[str] = []
    skipped_no_signal = 0
    now = datetime.now(UTC)

    for idx, finding in enumerate(findings):
        if finding.compliance_status == "NOT_AVAILABLE":
            skipped_no_signal += 1
            continue

        entry = mapping.lookup(finding.GeneratorId)
        if entry is None:
            if finding.GeneratorId not in skipped_unmapped:
                skipped_unmapped.append(finding.GeneratorId)
            continue

        # SourceRef points at the input ASFF file; line_start = the index
        # of the finding within the input list (1-based, for human reading).
        # Hash-stable across re-imports of the same file.
        source_ref = SourceRef(
            file=input.asff_path,
            line_start=idx + 1,
        )

        evidence_list.append(
            Evidence.create(
                detector_id=f"aws.import.security_hub.{entry.generator_id}",
                ksis_evidenced=list(entry.ksis),
                controls_evidenced=list(entry.controls),
                source_ref=source_ref,
                content={
                    "import_source": "aws.security_hub.asff",
                    "asff_finding_id": finding.Id,
                    "asff_generator_id": finding.GeneratorId,
                    "asff_compliance_status": finding.compliance_status,
                    "asff_severity_label": finding.severity_label,
                    "asff_title": finding.Title,
                    "asff_description": finding.Description,
                    "asff_resources": [
                        {"type": r.Type, "id": r.Id, "region": r.Region} for r in finding.Resources
                    ],
                    "asff_first_observed_at": finding.FirstObservedAt,
                    "asff_updated_at": finding.UpdatedAt,
                    # v0.1.163 / #368: CVE IDs from ASFF Vulnerabilities[]
                    # for the VDR generator. Empty list for non-vuln
                    # findings (compliance-control failures, etc.).
                    "cve_ids": finding.cve_ids,
                    "evidence_strength": entry.evidence_strength,
                    "mapping_title": entry.title,
                },
                timestamp=now,
            )
        )

    return IngestSecurityHubOutput(
        evidence=evidence_list,
        findings_total=len(findings),
        findings_emitted=len(evidence_list),
        skipped_unmapped_generator_ids=skipped_unmapped,
        skipped_status_not_available=skipped_no_signal,
    )
