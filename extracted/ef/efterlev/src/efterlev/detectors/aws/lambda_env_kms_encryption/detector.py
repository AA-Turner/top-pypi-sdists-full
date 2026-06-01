"""KSI-AFR-UCM: Lambda environment-variable KMS-encryption detector.

Reads Terraform source for `aws_lambda_function` resources whose
`environment.variables` block is non-empty and emits one Evidence
record per such function describing whether `kms_key_arn` is set
(customer-managed-key encryption-at-rest of env-var values).

Per DECISIONS 2026-05-10 "Tier 2 #2 design: Lambda env-var KMS +
APIGW access logging": this is detector beta of the Tier 2 #2 batch.
KSI-AFR-UCM classified `partial` — IaC-layer CMK-declaration
evidence; runtime key validity, FIPS posture of the key, and
rotation cadence are out of scope (the key-rotation cadence is
already evidenced by `aws.kms_key_rotation`).

Lambda env vars are encrypted at rest by AWS-managed keys by
default; this detector surfaces the explicit-CMK gap that compliance
audits typically ask about. A function with no env vars at all is
SKIPPED — there's nothing to protect, so emitting evidence would be
noise.

Three positive/negative states:
- `configured` — function has non-empty env vars AND `kms_key_arn`
  is a literal string.
- `absent` — function has non-empty env vars AND no `kms_key_arn`
  (default AWS-managed-key encryption — gap for explicit-CMK
  compliance posture).
- `unverifiable` — function has env vars AND `kms_key_arn` uses
  Terraform interpolation; resolved key cannot be inferred from IaC
  alone. Surfaces as a reviewer flag, not a gap.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_INTERPOLATION_MARKERS = ("${", "{{")


@detector(
    id="aws.lambda_env_kms_encryption",
    ksis=["KSI-AFR-UCM"],
    controls=["SC-28", "SC-28(1)"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit env-var-KMS Evidence per aws_lambda_function with env vars.

    Evidences (KSI):     KSI-AFR-UCM (Using Cryptographic Modules) —
                         IaC-layer customer-managed-key declaration on
                         Lambda env-var encryption.
    Evidences (800-53):  SC-28 (Protection of Information at Rest),
                         SC-28(1) (Cryptographic Protection).
    Does NOT prove:      key validity at runtime, FIPS-approval status
                         of the cryptographic module, key rotation
                         cadence (separately evidenced by
                         `aws.kms_key_rotation`), or that env-var
                         secrets shouldn't be in Secrets Manager
                         instead. Functions with no env vars at all
                         are skipped — no secrets to protect.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type != "aws_lambda_function":
            continue
        ev = _emit_lambda_evidence(r, now)
        if ev is not None:
            out.append(ev)

    return out


def _emit_lambda_evidence(r: TerraformResource, now: datetime) -> Evidence | None:
    if not _has_env_variables(r.body):
        # No env vars to protect — skip cleanly. Adding noisy
        # "function has no env vars" evidence would just dilute the
        # M3 signal on the KSIs the agent later classifies.
        return None

    raw_kms = _as_str(r.body.get("kms_key_arn"))
    function_name = _as_str(r.body.get("function_name")) or r.name

    if raw_kms is not None and _is_interpolated(raw_kms):
        return Evidence.create(
            detector_id="aws.lambda_env_kms_encryption",
            ksis_evidenced=["KSI-AFR-UCM"],
            controls_evidenced=["SC-28", "SC-28(1)"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "kms_state": "unverifiable",
                "pattern": "lambda_env_var_cmk",
                "function_name": function_name,
                "kms_key_arn": raw_kms,
                "detail": (
                    f"kms_key_arn='{raw_kms}' uses Terraform interpolation; "
                    f"resolved key cannot be inferred from IaC alone"
                ),
            },
            timestamp=now,
        )

    if raw_kms:
        return Evidence.create(
            detector_id="aws.lambda_env_kms_encryption",
            ksis_evidenced=["KSI-AFR-UCM"],
            controls_evidenced=["SC-28", "SC-28(1)"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "kms_state": "configured",
                "pattern": "lambda_env_var_cmk",
                "function_name": function_name,
                "kms_key_arn": raw_kms,
                "detail": f"function_name={function_name}; kms_key_arn declared",
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.lambda_env_kms_encryption",
        ksis_evidenced=["KSI-AFR-UCM"],
        controls_evidenced=["SC-28", "SC-28(1)"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "kms_state": "absent",
            "pattern": "lambda_env_var_cmk",
            "function_name": function_name,
            "gap": (
                f"aws_lambda_function '{function_name}' declares environment "
                f"variables but no kms_key_arn; env-var values are encrypted "
                f"with AWS-managed keys, not a customer-managed key. The "
                f"declared-CMK posture compliance frameworks ask about "
                f"requires an explicit kms_key_arn"
            ),
        },
        timestamp=now,
    )


def _has_env_variables(body: dict[str, Any]) -> bool:
    """True iff the function declares a non-empty `environment.variables` map.

    python-hcl2 represents the `environment` block as a list of dicts
    (it's repeatable in the schema even though MaxItems=1). Inside,
    `variables` is a map. An empty `variables = {}` declaration counts
    as "no env vars" for this detector — a function with empty env
    vars has no secrets to protect, so emitting evidence would be
    noise.
    """
    env = body.get("environment")
    env_dict = _normalize_block(env)
    if env_dict is None:
        return False
    variables = env_dict.get("variables")
    return isinstance(variables, dict) and len(variables) > 0


def _normalize_block(value: Any) -> dict[str, Any] | None:
    """python-hcl2 represents nested HCL blocks as a single dict OR a
    list-of-dicts (for repeatable blocks). Returns None when the block
    is absent or malformed.
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


def _is_interpolated(s: Any) -> bool:
    """True if `s` contains a Terraform interpolation marker (`${...}` or
    `{{...}}`).
    """
    if not isinstance(s, str):
        return False
    return any(marker in s for marker in _INTERPOLATION_MARKERS)
