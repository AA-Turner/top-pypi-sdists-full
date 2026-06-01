"""KSI-SVC-PRR: at-rest encryption coverage detector.

Cross-cutting encryption-at-rest detector for data stores NOT covered
by the existing per-service detectors. Covers: DynamoDB, EFS,
ElastiCache (cluster + replication group), Aurora (rds_cluster),
Neptune, DocumentDB.

Per DECISIONS 2026-05-07 "Tier 1 #4 design": this is detector #4 of 6.
KSI-SVC-PRR classified `partial` — the detector covers the
configured-state half; the procedural review cadence ("persistently
review the state of information resources after making changes") is
manifest territory.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

# Per-resource encryption-flag spec:
#   resource_type → (flag_attr, cmk_attr_or_None)
# `flag_attr` is the boolean field that signals at-rest encryption is on.
# `cmk_attr_or_None` is the customer-managed-key reference attribute, if
# present (most resources allow either AWS-managed or customer-managed
# KMS keys; the CMK reference is informational, not a positive/negative
# gate).
_RESOURCE_SPECS: dict[str, tuple[str, str | None]] = {
    "aws_dynamodb_table": ("__nested_dynamodb__", "kms_key_arn"),
    "aws_efs_file_system": ("encrypted", "kms_key_id"),
    "aws_elasticache_cluster": ("at_rest_encryption_enabled", None),
    "aws_elasticache_replication_group": ("at_rest_encryption_enabled", None),
    "aws_rds_cluster": ("storage_encrypted", "kms_key_id"),
    "aws_neptune_cluster": ("storage_encrypted", "kms_key_arn"),
    "aws_docdb_cluster": ("storage_encrypted", "kms_key_id"),
}


@detector(
    id="aws.svc_at_rest_encryption_coverage",
    ksis=["KSI-SVC-PRR"],
    controls=["SC-4"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit at-rest-encryption Evidence per data-store resource.

    Evidences (KSI):     KSI-SVC-PRR — configured encryption-at-rest
                         on data stores prevents residual data
                         exposure on shared underlying storage.
    Evidences (800-53):  SC-4 (Information in Shared System Resources).
    Does NOT prove:      key management (rotation, BYOK), in-transit
                         encryption, runtime enforcement on already-
                         deployed objects, or the procedural review
                         cadence (manifest territory).
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.kind != "resource":
            continue
        spec = _RESOURCE_SPECS.get(r.type)
        if spec is None:
            continue
        out.append(_emit_evidence(r, now, spec[0], spec[1]))

    return out


def _emit_evidence(
    r: TerraformResource,
    now: datetime,
    flag_attr: str,
    cmk_attr: str | None,
) -> Evidence:
    body = r.body
    if flag_attr == "__nested_dynamodb__":
        encrypted, cmk_value = _dynamodb_encryption_state(body)
    else:
        encrypted = _is_truthy(body.get(flag_attr))
        cmk_value = _coerce_str(body.get(cmk_attr)) if cmk_attr else None

    if encrypted:
        content: dict[str, Any] = {
            "resource_type": r.type,
            "resource_name": r.name,
            "encryption_state": "configured",
            "pattern": "at_rest_encryption",
        }
        if cmk_value:
            content["detail"] = "cmk=true"
    else:
        content = {
            "resource_type": r.type,
            "resource_name": r.name,
            "encryption_state": "absent",
            "pattern": "at_rest_encryption",
            "gap": _gap_message(r.type, flag_attr),
        }

    return Evidence.create(
        detector_id="aws.svc_at_rest_encryption_coverage",
        ksis_evidenced=["KSI-SVC-PRR"],
        controls_evidenced=["SC-4"],
        source_ref=r.source_ref,
        content=content,
        timestamp=now,
    )


def _dynamodb_encryption_state(body: dict[str, Any]) -> tuple[bool, str | None]:
    """DynamoDB encryption is in a nested `server_side_encryption` block.

    Note: DynamoDB defaults to AWS-owned KMS keys with encryption ON
    when the block is omitted. We honor that default — `absent` block
    counts as configured (with cmk_value=None). An explicit
    `enabled = false` is the only negative case.
    """
    sse = body.get("server_side_encryption")
    if isinstance(sse, list) and len(sse) == 1:
        sse = sse[0]
    if sse is None:
        # AWS default: encryption on with AWS-owned key. Treat as configured.
        return True, None
    if not isinstance(sse, dict):
        return True, None
    enabled = sse.get("enabled")
    if enabled is None:
        return True, _coerce_str(sse.get("kms_key_arn"))
    return _is_truthy(enabled), _coerce_str(sse.get("kms_key_arn"))


def _is_truthy(v: Any) -> bool:
    if v is True:
        return True
    if isinstance(v, str):
        return v.lower() in ("true", "1")
    return False


def _coerce_str(v: Any) -> str | None:
    if isinstance(v, str) and v.strip():
        return v
    return None


def _gap_message(resource_type: str, flag_attr: str) -> str:
    if flag_attr == "__nested_dynamodb__":
        return (
            f"{resource_type} declared with `server_side_encryption.enabled = false` "
            f"(AWS default is on; explicit-false is the negative path)"
        )
    return f"{resource_type} declared without `{flag_attr} = true`"
