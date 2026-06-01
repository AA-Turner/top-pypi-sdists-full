"""`ingest_config` primitive — AWS Config evaluations → Evidence records.

Mirrors `ingest_security_hub`: parse → look up rule-name in mapping
table → emit Evidence record. Same skip semantics:
- Unmapped rule names: reported in skipped_unmapped_config_rule_names,
  no fabrication.
- INSUFFICIENT_DATA evaluations: skipped (no signal).
- COMPLIANT, NON_COMPLIANT, NOT_APPLICABLE: all flow through; Gap
  Agent reasons over them.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from efterlev.imports.config.mapping import ConfigMapping, load_config_mapping
from efterlev.imports.config.parser import parse_config_document
from efterlev.models import Evidence, SourceRef
from efterlev.primitives.base import primitive


class IngestConfigInput(BaseModel):
    """Input to `ingest_config`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    config_path: Path
    mapping_override: ConfigMapping | None = None  # Test seam.


class IngestConfigOutput(BaseModel):
    """Output: emitted Evidence list + skip metadata."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    evidence: list[Evidence]
    evaluations_total: int
    evaluations_emitted: int
    skipped_unmapped_config_rule_names: list[str] = Field(default_factory=list)
    skipped_insufficient_data: int = 0


@primitive(capability="evidence", side_effects=False, version="0.1.0", deterministic=True)
def ingest_config(input: IngestConfigInput) -> IngestConfigOutput:
    """Parse AWS Config evaluations, map to KSIs, emit Evidence records."""
    evaluations = parse_config_document(input.config_path)
    mapping = input.mapping_override or load_config_mapping()

    evidence_list: list[Evidence] = []
    skipped_unmapped: list[str] = []
    skipped_no_signal = 0
    now = datetime.now(UTC)

    for idx, ev in enumerate(evaluations):
        if ev.ComplianceType == "INSUFFICIENT_DATA":
            skipped_no_signal += 1
            continue

        entry = mapping.lookup(ev.config_rule_name)
        if entry is None:
            if ev.config_rule_name not in skipped_unmapped:
                skipped_unmapped.append(ev.config_rule_name)
            continue

        source_ref = SourceRef(
            file=input.config_path,
            line_start=idx + 1,
        )

        evidence_list.append(
            Evidence.create(
                detector_id=f"aws.import.config.{entry.config_rule_name}",
                ksis_evidenced=list(entry.ksis),
                controls_evidenced=list(entry.controls),
                source_ref=source_ref,
                content={
                    "import_source": "aws.config.evaluations",
                    "config_rule_name": ev.config_rule_name,
                    "config_compliance_type": ev.ComplianceType,
                    "config_resource_type": ev.resource_type,
                    "config_resource_id": ev.resource_id,
                    "config_annotation": ev.Annotation,
                    "config_result_recorded_time": ev.ResultRecordedTime,
                    "evidence_strength": entry.evidence_strength,
                    "mapping_title": entry.title,
                },
                timestamp=now,
            )
        )

    return IngestConfigOutput(
        evidence=evidence_list,
        evaluations_total=len(evaluations),
        evaluations_emitted=len(evidence_list),
        skipped_unmapped_config_rule_names=skipped_unmapped,
        skipped_insufficient_data=skipped_no_signal,
    )
