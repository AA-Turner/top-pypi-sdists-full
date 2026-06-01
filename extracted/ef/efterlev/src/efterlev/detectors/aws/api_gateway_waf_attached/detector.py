"""KSI-CNA-RVP: API Gateway WAF-attachment detector.

Reads Terraform source for `aws_api_gateway_stage` (REST API v1) and
`aws_apigatewayv2_stage` (HTTP/WebSocket API v2) resources and emits
one Evidence record per stage describing whether an
`aws_wafv2_web_acl_association` resource references the stage by
Terraform name.

Per DECISIONS 2026-05-10 "Tier 2 #3 design: VPC isolation, route auth,
WAF attachment": this is detector delta of the Tier 2 #3 batch. Two
design calls govern this detector:

- Decision #2: ship as a single WAF-attachment detector NOW; defer the
  broader `aws.waf_*` family (rule coverage, rate limiting,
  geo-blocking, managed rule groups) to Tier 3. Customers without ANY
  Web ACL on a public APIGW are visibly exposed; partial coverage
  early beats waiting for complete coverage.
- Decision #3: NO `unverifiable` state. WAF attachment is detected via
  cross-resource search for `aws_wafv2_web_acl_association` whose
  `resource_arn` references the stage. The `resource_arn` is almost
  always a Terraform reference (`aws_apigatewayv2_stage.x.arn`);
  treating interpolation as `unverifiable` would force every
  real-world pairing into an unhelpful state. Detect by name-substring
  match.

Per the central design call (#1) shared with the rest of Tier 2 #3:
emit per-stage gap; let the Gap Agent reason about whether absence is
intentional (a private API not exposed publicly).

Two states per stage (binary):
- `waf_attached` -- a matching aws_wafv2_web_acl_association exists.
- `waf_absent` -- no matching association.

Coverage classified `partial`: an association doesn't prove the Web
ACL has any rules or that the rules are appropriate. Future
`aws.waf_*` family detectors will close those dimensions.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_STAGE_TYPES = {"aws_api_gateway_stage", "aws_apigatewayv2_stage"}


@detector(
    id="aws.api_gateway_waf_attached",
    ksis=["KSI-CNA-RVP"],
    controls=["SI-3", "SC-5"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit WAF-attachment Evidence per API Gateway stage.

    Evidences (KSI):     KSI-CNA-RVP (Reviewing Protections) -- IaC-
                         layer per-stage WAF-attachment posture.
                         Joins aws.cna_dos_protection on this KSI.
    Evidences (800-53):  SI-3 (Malicious Code Protection -- WAF is
                         the AWS-native equivalent at the L7
                         boundary), SC-5 (Denial of Service
                         Protection).
    Does NOT prove:      the Web ACL has any rules; the rules are
                         appropriate; rate limiting / geo-blocking
                         is configured; managed rule groups are
                         selected. Those dimensions are the future
                         `aws.waf_*` family's territory; this
                         detector is the early-warning signal that
                         a public APIGW has zero WAF protection.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    associations = [r for r in resources if r.type == "aws_wafv2_web_acl_association"]

    for r in resources:
        if r.type not in _STAGE_TYPES:
            continue
        out.append(_emit_stage_evidence(r, associations, now))

    return out


def _emit_stage_evidence(
    stage: TerraformResource,
    associations: list[TerraformResource],
    now: datetime,
) -> Evidence:
    stage_name = (
        _as_str(stage.body.get("stage_name")) or _as_str(stage.body.get("name")) or stage.name
    )
    pattern = (
        "rest_api_v1_stage_waf"
        if stage.type == "aws_api_gateway_stage"
        else "http_api_v2_stage_waf"
    )

    matched = _find_matching_association(stage, associations)
    if matched is not None:
        web_acl_arn = _as_str(matched.body.get("web_acl_arn"))
        content: dict[str, Any] = {
            "resource_type": stage.type,
            "resource_name": stage.name,
            "stage_name": stage_name,
            "waf_state": "waf_attached",
            "pattern": pattern,
            "association_resource_name": matched.name,
            "detail": (
                f"stage_name={stage_name}; aws_wafv2_web_acl_association "
                f"'{matched.name}' references this stage"
            ),
        }
        if web_acl_arn:
            content["web_acl_arn"] = web_acl_arn
        return Evidence.create(
            detector_id="aws.api_gateway_waf_attached",
            ksis_evidenced=["KSI-CNA-RVP"],
            controls_evidenced=["SI-3", "SC-5"],
            source_ref=stage.source_ref,
            content=content,
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.api_gateway_waf_attached",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SI-3", "SC-5"],
        source_ref=stage.source_ref,
        content={
            "resource_type": stage.type,
            "resource_name": stage.name,
            "stage_name": stage_name,
            "waf_state": "waf_absent",
            "pattern": pattern,
            "gap": (
                f"{stage.type} '{stage_name}' has no aws_wafv2_web_acl_association "
                f"referencing it; the stage receives no WAF protection at the L7 "
                f"boundary. If this stage is intentionally private (internal API "
                f"not exposed publicly), the reviewer should annotate the gap as "
                f"accepted."
            ),
        },
        timestamp=now,
    )


def _find_matching_association(
    stage: TerraformResource,
    associations: list[TerraformResource],
) -> TerraformResource | None:
    """Return the first aws_wafv2_web_acl_association whose
    `resource_arn` references this stage by Terraform name.

    The match is name-substring: `resource_arn` strings like
    `${aws_apigatewayv2_stage.prod.arn}` count as referencing the
    stage named `prod` of type `aws_apigatewayv2_stage`. We do NOT
    require the resolved ARN to literally match -- per DECISIONS
    Decision #3, treating interpolation as unverifiable would force
    every real-world pairing into an unhelpful state.
    """
    needle = f"{stage.type}.{stage.name}"
    for assoc in associations:
        resource_arn = _as_str(assoc.body.get("resource_arn"))
        if not resource_arn:
            continue
        if needle in resource_arn:
            return assoc
    return None


def _as_str(value: Any) -> str | None:
    """python-hcl2 occasionally returns strings wrapped in single-element lists."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    return value if isinstance(value, str) else None
