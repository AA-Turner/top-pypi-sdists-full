"""KSI-MLA-LET: API Gateway access-logging configuration detector.

Reads Terraform source for `aws_api_gateway_stage` (REST API v1) and
`aws_apigatewayv2_stage` (HTTP/WebSocket API v2) resources and emits
one Evidence record per stage describing whether an
`access_log_settings` block is declared.

Per DECISIONS 2026-05-10 "Tier 2 #2 design: Lambda env-var KMS +
APIGW access logging": this is detector gamma of the Tier 2 #2 batch.
KSI-MLA-LET classified `partial` -- IaC-layer block-declaration
evidence; runtime log flow, destination-bucket retention, and access
control on the destination are out of scope.

Stage-shaped evidence (one record per stage, NOT per API). A single
API can have multiple stages with different logging postures (e.g.,
`prod` with logging enabled, `staging` without) so per-stage
granularity matters for compliance reasons.

Two states (binary -- no `unverifiable`):
- `configured` -- access_log_settings block is declared.
- `absent` -- block is absent. The Lambda-behind-APIGW request-path
  audit trail is blind unless the Lambda itself logs the request,
  which it usually doesn't.

The detector does NOT inspect destination_arn for validity at scan
time. destination_arn is almost always a Terraform reference like
`aws_cloudwatch_log_group.x.arn` -- treating interpolation as
unverifiable would make the detector emit unverifiable on every
real-world resource. Block-presence is the signal.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_STAGE_TYPES = {"aws_api_gateway_stage", "aws_apigatewayv2_stage"}


@detector(
    id="aws.api_gateway_access_logging",
    ksis=["KSI-MLA-LET"],
    controls=["AU-2", "AU-3"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit access-logging Evidence per API Gateway stage.

    Evidences (KSI):     KSI-MLA-LET (Logging Event Types) -- IaC-layer
                         per-stage access-log-settings declaration.
    Evidences (800-53):  AU-2 (Event Logging),
                         AU-3 (Content of Audit Records).
    Does NOT prove:      runtime log flow; destination-bucket /
                         log-group retention adheres to FedRAMP
                         requirements; access control on the
                         destination; the format string captures
                         all event types compliance frameworks ask
                         about (`$context.requestId` alone is
                         minimally useful; full request/response
                         capture requires more fields).
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type not in _STAGE_TYPES:
            continue
        out.append(_emit_stage_evidence(r, now))

    return out


def _emit_stage_evidence(r: TerraformResource, now: datetime) -> Evidence:
    stage_name = _as_str(r.body.get("stage_name")) or r.name
    pattern = (
        "rest_api_v1_stage_access_logs"
        if r.type == "aws_api_gateway_stage"
        else "http_api_v2_stage_access_logs"
    )

    log_settings = _normalize_block(r.body.get("access_log_settings"))
    if log_settings is not None:
        destination_arn = _as_str(log_settings.get("destination_arn"))
        log_format = _as_str(log_settings.get("format"))
        content: dict[str, Any] = {
            "resource_type": r.type,
            "resource_name": r.name,
            "stage_name": stage_name,
            "logging_state": "configured",
            "pattern": pattern,
            "detail": f"stage_name={stage_name}; access_log_settings declared",
        }
        if destination_arn:
            content["destination_arn"] = destination_arn
        if log_format:
            content["format_present"] = True
        return Evidence.create(
            detector_id="aws.api_gateway_access_logging",
            ksis_evidenced=["KSI-MLA-LET"],
            controls_evidenced=["AU-2", "AU-3"],
            source_ref=r.source_ref,
            content=content,
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.api_gateway_access_logging",
        ksis_evidenced=["KSI-MLA-LET"],
        controls_evidenced=["AU-2", "AU-3"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "stage_name": stage_name,
            "logging_state": "absent",
            "pattern": pattern,
            "gap": (
                f"{r.type} '{stage_name}' has no access_log_settings block; "
                f"the request-path audit trail at this stage is blind unless "
                f"the backend (typically Lambda) logs request metadata itself"
            ),
        },
        timestamp=now,
    )


def _normalize_block(value: Any) -> dict[str, Any] | None:
    """python-hcl2 represents nested HCL blocks as a single dict OR a
    list-of-dicts (for repeatable blocks). access_log_settings is
    MaxItems=1 in both v1 and v2 schemas; unwrap a one-element list
    and otherwise expect a dict. Returns None when absent or malformed.
    """
    if isinstance(value, dict):
        return value
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict):
        return value[0]
    return None


def _as_str(value: Any) -> str | None:
    """python-hcl2 occasionally returns strings wrapped in single-element lists."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    return value if isinstance(value, str) else None
