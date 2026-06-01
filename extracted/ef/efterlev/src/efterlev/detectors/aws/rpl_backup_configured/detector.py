"""KSI-RPL-ARP: Aligning Recovery Plan detector.

Reads Terraform for the IaC-declared recovery-plan orchestration
primitives:

- `aws_backup_plan` — AWS Backup plans, with rule counting and
  cross-region copy_action detection.
- `aws_backup_vault` — backup destinations (CMK detail when set).
- `aws_backup_selection` — what's protected.
- `aws_db_instance_automated_backups_replication` — RDS automated-
  backup cross-region replication.

Per DECISIONS 2026-05-07 "Tier 1 #4 design": this is detector #5 of 6.
KSI-RPL-ARP classified `partial` — the detector covers the
configured-state half; the procedural review of objective alignment
is manifest territory.

Distinct from `aws.backup_retention_configured` (KSI-RPL-ABO + CP-9):
that detector covers RDS retention + S3 versioning. This one covers
the AWS Backup orchestration + cross-region replication surface.

No negative evidence emitted. Absence of AWS Backup isn't a gap per
se — many small workspaces use only RDS native backups.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.rpl_backup_configured",
    ksis=["KSI-RPL-ARP"],
    controls=["CP-7", "CP-10"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit recovery-plan Evidence per AWS Backup / cross-region resource.

    Evidences (KSI):     KSI-RPL-ARP — IaC-declared recovery-plan
                         orchestration primitives (AWS Backup plans,
                         vaults, selections; RDS cross-region
                         automated-backup replication).
    Evidences (800-53):  CP-7 (Alternate Processing Site),
                         CP-10 (System Recovery and Reconstitution).
    Does NOT prove:      alignment with stated RTO/RPO (manifest
                         territory); restore validation (separate
                         detector); vault-lock policies.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.kind != "resource":
            continue
        if r.type == "aws_backup_plan":
            out.append(_emit_backup_plan(r, now))
        elif r.type == "aws_backup_vault":
            out.append(_emit_backup_vault(r, now))
        elif r.type == "aws_backup_selection":
            out.append(_emit_backup_selection(r, now))
        elif r.type == "aws_db_instance_automated_backups_replication":
            out.append(_emit_rds_cross_region(r, now))

    return out


def _emit_backup_plan(r: TerraformResource, now: datetime) -> Evidence:
    rules = _normalize_blocks(r.body.get("rule"))
    rule_count = len(rules)
    copy_actions = sum(_count_copy_actions(rule) for rule in rules)
    return Evidence.create(
        detector_id="aws.rpl_backup_configured",
        ksis_evidenced=["KSI-RPL-ARP"],
        controls_evidenced=["CP-7", "CP-10"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "recovery_state": "configured",
            "pattern": "backup_plan",
            "detail": f"rules={rule_count} copy_actions={copy_actions}",
        },
        timestamp=now,
    )


def _emit_backup_vault(r: TerraformResource, now: datetime) -> Evidence:
    cmk = _coerce_str(r.body.get("kms_key_arn"))
    content: dict[str, Any] = {
        "resource_type": r.type,
        "resource_name": r.name,
        "recovery_state": "configured",
        "pattern": "backup_vault",
    }
    if cmk:
        content["detail"] = "cmk=true"
    return Evidence.create(
        detector_id="aws.rpl_backup_configured",
        ksis_evidenced=["KSI-RPL-ARP"],
        controls_evidenced=["CP-7", "CP-10"],
        source_ref=r.source_ref,
        content=content,
        timestamp=now,
    )


def _emit_backup_selection(r: TerraformResource, now: datetime) -> Evidence:
    return Evidence.create(
        detector_id="aws.rpl_backup_configured",
        ksis_evidenced=["KSI-RPL-ARP"],
        controls_evidenced=["CP-7", "CP-10"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "recovery_state": "configured",
            "pattern": "backup_selection",
        },
        timestamp=now,
    )


def _emit_rds_cross_region(r: TerraformResource, now: datetime) -> Evidence:
    source = _coerce_str(r.body.get("source_db_instance_arn")) or "<unresolved>"
    return Evidence.create(
        detector_id="aws.rpl_backup_configured",
        ksis_evidenced=["KSI-RPL-ARP"],
        controls_evidenced=["CP-7", "CP-10"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "recovery_state": "configured",
            "pattern": "rds_cross_region_replication",
            "detail": f"source={source}",
        },
        timestamp=now,
    )


def _normalize_blocks(v: Any) -> list[dict[str, Any]]:
    """python-hcl2 returns a single block as a dict OR a list of dicts.
    Normalize to a flat list."""
    if v is None:
        return []
    if isinstance(v, dict):
        return [v]
    if isinstance(v, list):
        return [b for b in v if isinstance(b, dict)]
    return []


def _count_copy_actions(rule: dict[str, Any]) -> int:
    """Count `copy_action` blocks within an `aws_backup_plan` rule.
    Each copy_action targets a destination_vault_arn; presence indicates
    cross-region (or cross-account) copy is configured."""
    return len(_normalize_blocks(rule.get("copy_action")))


def _coerce_str(v: Any) -> str | None:
    if isinstance(v, str) and v.strip():
        return v
    return None
