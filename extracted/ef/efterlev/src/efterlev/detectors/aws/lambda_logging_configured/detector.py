"""KSI-MLA-LET: Lambda CloudWatch Logs configuration detector.

Reads Terraform source for `aws_lambda_function` resources and emits one
Evidence record per function describing whether a corresponding
`aws_cloudwatch_log_group` is declared in the same plan/repo. The
canonical Lambda log-group name is `/aws/lambda/<function_name>`; the
detector matches on that convention.

Per DECISIONS 2026-05-09 "Tier 2 #1 design: Lambda + API Gateway
detector batch v0": this is detector β of the v0 batch. KSI-MLA-LET
classified `partial` — IaC-layer logging-presence vs runtime
log-flow proof.

Coverage is reported as `partial` in mapping.yaml: the IaC layer
covers whether the log group is declared (which gates retention +
encryption + KMS configuration); runtime log flow, log access
control, and retention adherence are out of scope. AWS Lambda
auto-creates log groups on first invoke when the execution role has
`logs:CreateLogGroup`, but auto-created groups have no retention
policy and no encryption — the detector flags missing declarations
because those properties cannot be set without an explicit resource.

Three positive/negative states per function:
- `configured` — `function_name` is a literal string AND a matching
  `aws_cloudwatch_log_group` exists.
- `absent` — `function_name` is a literal string AND no matching
  log group exists.
- `unverifiable` — `function_name` uses Terraform interpolation
  (`${var.foo}`, `aws_iam_role.bar.name`, etc.) so the resolved log
  group name cannot be inferred from IaC alone. Surfaces as a
  reviewer flag, not a gap.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_INTERPOLATION_MARKERS = ("${", "{{")


@detector(
    id="aws.lambda_logging_configured",
    ksis=["KSI-MLA-LET"],
    controls=["AU-2", "AU-12"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit logging-state Evidence for every aws_lambda_function.

    Evidences (KSI):     KSI-MLA-LET — IaC-declared CloudWatch log group
                         per Lambda function (gates retention + KMS
                         encryption configuration).
    Evidences (800-53):  AU-2 (Event Logging), AU-12 (Audit Record
                         Generation).
    Does NOT prove:      log retention is set per FedRAMP requirements,
                         log group is KMS-encrypted, logs are actually
                         flowing at runtime, log access control is
                         restrictive, log shipping to a SIEM exists.
                         An auto-created (non-IaC) log group provides
                         logs but cannot satisfy the procedural
                         requirements compliance frameworks ask for.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    declared_log_group_names = _collect_declared_log_group_names(resources)

    for r in resources:
        if r.type != "aws_lambda_function":
            continue
        ev = _emit_lambda_evidence(r, declared_log_group_names, now)
        if ev is not None:
            out.append(ev)

    return out


def _collect_declared_log_group_names(
    resources: list[TerraformResource],
) -> set[str]:
    """Return the set of `name` values from aws_cloudwatch_log_group
    resources whose name is a literal string. Interpolated names are
    skipped (they can't be matched without resolving Terraform vars).
    """
    out: set[str] = set()
    for r in resources:
        if r.type != "aws_cloudwatch_log_group":
            continue
        name = r.body.get("name")
        if isinstance(name, str) and not _is_interpolated(name):
            out.add(name)
    return out


def _emit_lambda_evidence(
    r: TerraformResource,
    declared_log_group_names: set[str],
    now: datetime,
) -> Evidence | None:
    function_name = r.body.get("function_name")

    if not isinstance(function_name, str) or not function_name.strip():
        # function_name is required by the AWS provider; if absent or
        # non-string, the IaC is malformed. Skip rather than emit
        # noisy evidence.
        return None

    if _is_interpolated(function_name):
        return Evidence.create(
            detector_id="aws.lambda_logging_configured",
            ksis_evidenced=["KSI-MLA-LET"],
            controls_evidenced=["AU-2", "AU-12"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "logging_state": "unverifiable",
                "pattern": "log_group_per_function",
                "detail": (
                    f"function_name='{function_name}' uses Terraform "
                    f"interpolation; resolved log group name cannot be "
                    f"inferred from IaC alone"
                ),
            },
            timestamp=now,
        )

    expected_log_group = f"/aws/lambda/{function_name}"
    if expected_log_group in declared_log_group_names:
        return Evidence.create(
            detector_id="aws.lambda_logging_configured",
            ksis_evidenced=["KSI-MLA-LET"],
            controls_evidenced=["AU-2", "AU-12"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "logging_state": "configured",
                "pattern": "log_group_per_function",
                "detail": f"function_name={function_name}; log_group={expected_log_group}",
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.lambda_logging_configured",
        ksis_evidenced=["KSI-MLA-LET"],
        controls_evidenced=["AU-2", "AU-12"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "logging_state": "absent",
            "pattern": "log_group_per_function",
            "gap": (
                f"aws_lambda_function '{function_name}' has no matching "
                f"aws_cloudwatch_log_group '{expected_log_group}'; auto-created "
                f"log groups have no retention or KMS-encryption configuration"
            ),
        },
        timestamp=now,
    )


def _is_interpolated(s: Any) -> bool:
    """True if `s` contains a Terraform interpolation marker (`${...}` or
    `{{...}}`). Used to detect non-literal values whose resolved form
    can't be matched at scan time.
    """
    if not isinstance(s, str):
        return False
    return any(marker in s for marker in _INTERPOLATION_MARKERS)
