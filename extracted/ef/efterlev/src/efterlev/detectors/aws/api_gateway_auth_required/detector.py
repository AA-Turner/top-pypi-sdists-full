"""KSI-CNA-EIS + KSI-CNA-DFP: API Gateway route-level auth detector.

Reads Terraform source for `aws_api_gateway_method` (REST API v1) and
`aws_apigatewayv2_route` (HTTP/WebSocket API v2) resources and emits
one Evidence record per route describing whether the route declares
any non-`NONE` authorization mode.

Per DECISIONS 2026-05-10 "Tier 2 #3 design: VPC isolation, route auth,
WAF attachment": this is detector gamma of the Tier 2 #3 batch. The
fundamental design call: the detector emits per-route posture and lets
the Gap Agent reason about intentionality. Public-by-design routes
(health checks, public webhooks) are sometimes legitimate; the
detector does not try to distinguish them via heuristics, annotations,
or exemption lists.

This is the library's first detector evidencing KSI-CNA-EIS and
KSI-CNA-DFP. Auth on routes IS the intended-state enforcement and the
privilege boundary at the API edge — no other existing detector
covers either KSI.

Three states per route:
- `auth_required` -- field is any of AWS_IAM, CUSTOM (Lambda
  authorizer), COGNITO_USER_POOLS, or JWT (v2 only).
- `auth_none` -- field is `NONE` explicit OR field omitted (defaults
  to NONE in both v1 and v2). The gap.
- `unverifiable` -- field uses Terraform interpolation; resolved auth
  mode cannot be inferred from IaC alone. Reviewer flag, not a gap.

Coverage classified `partial`: a non-NONE authorization mode doesn't
prove the authorizer is correctly configured at runtime (e.g., a
Cognito user pool with permissive group rules), or that the
authorizer Lambda actually rejects bad tokens.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_INTERPOLATION_MARKERS = ("${", "{{")
_AUTH_REQUIRED_MODES = frozenset({"AWS_IAM", "CUSTOM", "COGNITO_USER_POOLS", "JWT"})
_AUTH_NONE_MODES = frozenset({"NONE", ""})


@detector(
    id="aws.api_gateway_auth_required",
    ksis=["KSI-CNA-EIS", "KSI-CNA-DFP"],
    controls=["AC-3", "AC-6"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit auth-mode Evidence per API Gateway route.

    Evidences (KSI):     KSI-CNA-EIS (Enforcing Intended State),
                         KSI-CNA-DFP (Defining Functionality and
                         Privileges) -- IaC-layer per-route auth-mode.
    Evidences (800-53):  AC-3 (Access Enforcement),
                         AC-6 (Least Privilege).
    Does NOT prove:      authorizer is correctly configured at runtime
                         (e.g., a Cognito user pool with permissive
                         group rules); the authorizer Lambda rejects
                         bad tokens; the public-by-design route case
                         (health endpoint) is not a gap. Per the
                         DECISIONS entry, the Gap Agent reasons about
                         intentionality from broader prompt context.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type == "aws_api_gateway_method":
            out.append(_emit_v1_evidence(r, now))
        elif r.type == "aws_apigatewayv2_route":
            out.append(_emit_v2_evidence(r, now))

    return out


def _emit_v1_evidence(r: TerraformResource, now: datetime) -> Evidence:
    """REST v1 routes use the `authorization` field (required by
    provider; no documented default, but practical experience treats
    omission as NONE)."""
    raw = _as_str(r.body.get("authorization"))
    return _build_evidence(
        r,
        raw,
        pattern="rest_api_v1_method_auth",
        route_label=_route_label_v1(r),
        now=now,
    )


def _emit_v2_evidence(r: TerraformResource, now: datetime) -> Evidence:
    """HTTP v2 routes use the `authorization_type` field. Defaults to
    NONE when omitted (provider docs; verified at apply time)."""
    raw = _as_str(r.body.get("authorization_type"))
    return _build_evidence(
        r,
        raw,
        pattern="http_api_v2_route_auth",
        route_label=_route_label_v2(r),
        now=now,
    )


def _build_evidence(
    r: TerraformResource,
    raw: str | None,
    *,
    pattern: str,
    route_label: str,
    now: datetime,
) -> Evidence:
    if raw is not None and _is_interpolated(raw):
        return Evidence.create(
            detector_id="aws.api_gateway_auth_required",
            ksis_evidenced=["KSI-CNA-EIS", "KSI-CNA-DFP"],
            controls_evidenced=["AC-3", "AC-6"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "route_label": route_label,
                "auth_state": "unverifiable",
                "pattern": pattern,
                "auth_mode": raw,
                "detail": (
                    f"auth field='{raw}' uses Terraform interpolation; "
                    "resolved auth mode cannot be inferred from IaC alone"
                ),
            },
            timestamp=now,
        )

    effective = (raw or "NONE").upper()

    if effective in _AUTH_REQUIRED_MODES:
        return Evidence.create(
            detector_id="aws.api_gateway_auth_required",
            ksis_evidenced=["KSI-CNA-EIS", "KSI-CNA-DFP"],
            controls_evidenced=["AC-3", "AC-6"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "route_label": route_label,
                "auth_state": "auth_required",
                "pattern": pattern,
                "auth_mode": effective,
                "detail": f"route={route_label}; authorization={effective}",
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.api_gateway_auth_required",
        ksis_evidenced=["KSI-CNA-EIS", "KSI-CNA-DFP"],
        controls_evidenced=["AC-3", "AC-6"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "route_label": route_label,
            "auth_state": "auth_none",
            "pattern": pattern,
            "auth_mode": effective,
            "gap": (
                f"{r.type} '{route_label}' has authorization="
                f"{effective!r}"
                + (
                    " (provider default when the field is omitted)"
                    if raw is None or raw == ""
                    else ""
                )
                + "; the route is publicly invokable. Compliance "
                "reviewers consistently ask about route-level auth on "
                "API edges. If this route is intentionally public "
                "(health endpoint, public webhook), the reviewer should "
                "annotate the gap as accepted."
            ),
        },
        timestamp=now,
    )


def _route_label_v1(r: TerraformResource) -> str:
    """REST v1 method label: HTTP_METHOD on the named resource. Falls
    back to the Terraform resource name when http_method is missing."""
    method = _as_str(r.body.get("http_method"))
    if method:
        return f"{method} {r.name}"
    return r.name


def _route_label_v2(r: TerraformResource) -> str:
    """HTTP v2 route label: route_key (e.g., `GET /users`). Falls back
    to the Terraform resource name when route_key is missing."""
    route_key = _as_str(r.body.get("route_key"))
    if route_key:
        return route_key
    return r.name


def _as_str(value: Any) -> str | None:
    """python-hcl2 occasionally returns strings wrapped in single-element lists."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    return value if isinstance(value, str) else None


def _is_interpolated(s: Any) -> bool:
    """True if `s` contains a Terraform interpolation marker."""
    if not isinstance(s, str):
        return False
    return any(marker in s for marker in _INTERPOLATION_MARKERS)
