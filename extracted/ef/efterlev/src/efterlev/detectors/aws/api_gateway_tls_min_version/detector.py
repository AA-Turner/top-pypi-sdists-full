"""KSI-SVC-SNT: API Gateway custom-domain TLS minimum-version detector.

Reads Terraform source for `aws_api_gateway_domain_name` (REST API v1)
and `aws_apigatewayv2_domain_name` (HTTP/WebSocket API v2) resources
and emits one Evidence record per custom domain describing whether the
configured `security_policy` enforces a TLS-1.2-or-higher floor.

Per DECISIONS 2026-05-09 "Tier 2 #1 design: Lambda + API Gateway
detector batch v0": this is detector gamma of the v0 batch. KSI-SVC-SNT
classified `partial` — IaC-layer policy-floor evidence.

AWS provider semantics (as of 2026):
- REST API v1 (`aws_api_gateway_domain_name`): `security_policy`
  is a top-level attribute. Valid values: `TLS_1_0`, `TLS_1_2`.
  Default when omitted is `TLS_1_0` — the legacy gap.
- HTTP/WebSocket API v2 (`aws_apigatewayv2_domain_name`): the
  `security_policy` is nested inside the required
  `domain_name_configuration` block. Only `TLS_1_2` is supported by
  the AWS service; older policies are not selectable. Absence of
  the field within an existing `domain_name_configuration` block
  resolves to `TLS_1_2`.

Coverage is reported as `partial` in mapping.yaml: the IaC layer
proves the configured floor, not the runtime cipher negotiation
outcome or the underlying CloudFront/edge infrastructure's
adherence to it.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_INTERPOLATION_MARKERS = ("${", "{{")

# REST API v1 default security_policy when the attribute is absent.
# Documented on AWS docs page "API Gateway custom domain names".
_V1_DEFAULT_POLICY = "TLS_1_0"

_ACCEPTED_POLICIES = {"TLS_1_2", "TLS_1_3"}


@detector(
    id="aws.api_gateway_tls_min_version",
    ksis=["KSI-SVC-SNT"],
    controls=["SC-8", "SC-13", "SC-23"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit TLS-min-version Evidence per API Gateway custom domain.

    Evidences (KSI):     KSI-SVC-SNT (Securing Network Traffic) — partial.
                         IaC-layer custom-domain TLS-policy floor.
    Evidences (800-53):  SC-8 (Transmission Confidentiality and Integrity),
                         SC-13 (Cryptographic Protection),
                         SC-23 (Session Authenticity).
    Does NOT prove:      runtime cipher negotiation outcomes; the underlying
                         CloudFront / edge infrastructure honors the
                         configured policy; certificate rotation; SNI / ALPN
                         configuration; backend integration TLS posture
                         (Gateway → Lambda / VPC link).
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type == "aws_api_gateway_domain_name":
            out.append(_emit_v1_evidence(r, now))
        elif r.type == "aws_apigatewayv2_domain_name":
            ev = _emit_v2_evidence(r, now)
            if ev is not None:
                out.append(ev)

    return out


def _emit_v1_evidence(r: TerraformResource, now: datetime) -> Evidence:
    """REST API v1: security_policy is a top-level attribute. Absence
    resolves to TLS_1_0 per the AWS provider default — emit `absent`
    in that case so the gap surfaces explicitly."""
    raw_policy = _as_str(r.body.get("security_policy"))

    if raw_policy is not None and _is_interpolated(raw_policy):
        return Evidence.create(
            detector_id="aws.api_gateway_tls_min_version",
            ksis_evidenced=["KSI-SVC-SNT"],
            controls_evidenced=["SC-8", "SC-13", "SC-23"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "tls_min_state": "unverifiable",
                "pattern": "rest_api_v1_custom_domain",
                "security_policy": raw_policy,
                "detail": (
                    f"security_policy='{raw_policy}' uses Terraform "
                    f"interpolation; resolved policy cannot be inferred "
                    f"from IaC alone"
                ),
            },
            timestamp=now,
        )

    effective_policy = raw_policy if raw_policy else _V1_DEFAULT_POLICY

    if effective_policy in _ACCEPTED_POLICIES:
        content: dict[str, Any] = {
            "resource_type": r.type,
            "resource_name": r.name,
            "tls_min_state": "configured",
            "pattern": "rest_api_v1_custom_domain",
            "security_policy": effective_policy,
            "detail": f"security_policy={effective_policy}",
        }
    else:
        content = {
            "resource_type": r.type,
            "resource_name": r.name,
            "tls_min_state": "absent",
            "pattern": "rest_api_v1_custom_domain",
            "security_policy": effective_policy,
            "gap": (
                f"aws_api_gateway_domain_name '{r.name}' uses "
                f"security_policy={effective_policy!r}"
                + (
                    " (provider default when the attribute is omitted)"
                    if raw_policy is None
                    else ""
                )
                + "; traffic terminating at this custom domain is permitted "
                "to negotiate down to TLS 1.0, below FedRAMP's TLS 1.2+ floor"
            ),
        }

    return Evidence.create(
        detector_id="aws.api_gateway_tls_min_version",
        ksis_evidenced=["KSI-SVC-SNT"],
        controls_evidenced=["SC-8", "SC-13", "SC-23"],
        source_ref=r.source_ref,
        content=content,
        timestamp=now,
    )


def _emit_v2_evidence(r: TerraformResource, now: datetime) -> Evidence | None:
    """HTTP/WebSocket API v2: security_policy is nested inside the
    `domain_name_configuration` block. The AWS service only supports
    `TLS_1_2` for v2, so absence within a present block resolves to
    `TLS_1_2`. A missing block entirely is a malformed resource —
    emit nothing rather than guess.
    """
    config_block = r.body.get("domain_name_configuration")
    config_dict = _normalize_block(config_block)
    if config_dict is None:
        return None

    raw_policy = _as_str(config_dict.get("security_policy"))

    if raw_policy is not None and _is_interpolated(raw_policy):
        return Evidence.create(
            detector_id="aws.api_gateway_tls_min_version",
            ksis_evidenced=["KSI-SVC-SNT"],
            controls_evidenced=["SC-8", "SC-13", "SC-23"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "tls_min_state": "unverifiable",
                "pattern": "http_api_v2_custom_domain",
                "security_policy": raw_policy,
                "detail": (
                    f"domain_name_configuration.security_policy='{raw_policy}' "
                    f"uses Terraform interpolation; resolved policy cannot be "
                    f"inferred from IaC alone"
                ),
            },
            timestamp=now,
        )

    # AWS v2 only supports TLS_1_2; absence resolves to TLS_1_2.
    effective_policy = raw_policy if raw_policy else "TLS_1_2"

    if effective_policy in _ACCEPTED_POLICIES:
        content: dict[str, Any] = {
            "resource_type": r.type,
            "resource_name": r.name,
            "tls_min_state": "configured",
            "pattern": "http_api_v2_custom_domain",
            "security_policy": effective_policy,
            "detail": f"security_policy={effective_policy}"
            + (" (v2 service default)" if raw_policy is None else ""),
        }
    else:
        content = {
            "resource_type": r.type,
            "resource_name": r.name,
            "tls_min_state": "absent",
            "pattern": "http_api_v2_custom_domain",
            "security_policy": effective_policy,
            "gap": (
                f"aws_apigatewayv2_domain_name '{r.name}' declares "
                f"security_policy={effective_policy!r}, below the "
                f"FedRAMP TLS 1.2+ floor"
            ),
        }

    return Evidence.create(
        detector_id="aws.api_gateway_tls_min_version",
        ksis_evidenced=["KSI-SVC-SNT"],
        controls_evidenced=["SC-8", "SC-13", "SC-23"],
        source_ref=r.source_ref,
        content=content,
        timestamp=now,
    )


def _normalize_block(value: Any) -> dict[str, Any] | None:
    """python-hcl2 represents nested HCL blocks as either a single dict
    OR a list-of-dicts (for repeatable blocks). `domain_name_configuration`
    is `MaxItems=1`, so unwrap a one-element list and otherwise expect
    a dict. Returns None when the block is absent or malformed.
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
    `{{...}}`). Used to detect non-literal values whose resolved form
    can't be matched at scan time.
    """
    if not isinstance(s, str):
        return False
    return any(marker in s for marker in _INTERPOLATION_MARKERS)
