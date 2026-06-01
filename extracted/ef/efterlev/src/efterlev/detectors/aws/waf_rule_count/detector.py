"""KSI-CNA-RVP: AWS WAFv2 Web ACL rule-count detector.

Reads Terraform source for `aws_wafv2_web_acl` resources and emits one
Evidence record per Web ACL describing whether at least one `rule`
block is declared. A Web ACL with `default_action { allow {} }` and
zero rules passes the existing `aws.api_gateway_waf_attached` check
but provides no L7 protection — that's the gap this detector closes.

Per DECISIONS 2026-05-10 "Tier 3 #1 design: aws.waf_* detector family
v0": this is detector β of the Tier 3 #1 batch. Per-Web-ACL emission
(NOT per-rule) — per-rule would explode evidence-record count without
adding signal the Gap Agent needs.

Two states per Web ACL (binary, no `unverifiable` per the DECISIONS
entry's third design choice):
- `rules_present` — count of `rule` blocks ≥ 1.
- `rules_absent` — count of `rule` blocks == 0. The canonical
  "WAF attached but does nothing" gap.

Coverage classified `partial`: presence of rule blocks doesn't prove
the rules' actions are appropriate (a `count` action provides
observability without enforcement). Future detectors in the
`aws.waf_*` family will drill into action types and rule-group
selection.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.waf_rule_count",
    ksis=["KSI-CNA-RVP"],
    controls=["SI-3", "SC-5"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit rule-count Evidence per aws_wafv2_web_acl.

    Evidences (KSI):     KSI-CNA-RVP (Reviewing Protections) -- IaC-
                         layer per-Web-ACL rule presence. Joins
                         aws.cna_dos_protection and
                         aws.api_gateway_waf_attached on this KSI.
    Evidences (800-53):  SI-3 (Malicious Code Protection at L7),
                         SC-5 (Denial of Service Protection).
    Does NOT prove:      the rules' actions are appropriate (a `count`
                         action is observability without enforcement);
                         the rules cover the OWASP Top 10 or any
                         specific threat model; rule priorities are
                         set correctly. Those dimensions are the
                         future aws.waf_* family's territory.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type != "aws_wafv2_web_acl":
            continue
        out.append(_emit_web_acl_evidence(r, now))

    return out


def _emit_web_acl_evidence(r: TerraformResource, now: datetime) -> Evidence:
    web_acl_name = _as_str(r.body.get("name")) or r.name
    rule_count = _count_rule_blocks(r.body.get("rule"))

    if rule_count >= 1:
        return Evidence.create(
            detector_id="aws.waf_rule_count",
            ksis_evidenced=["KSI-CNA-RVP"],
            controls_evidenced=["SI-3", "SC-5"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "web_acl_name": web_acl_name,
                "rule_state": "rules_present",
                "pattern": "wafv2_web_acl_rule_count",
                "rule_count": rule_count,
                "detail": f"web_acl_name={web_acl_name}; rule_count={rule_count}",
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.waf_rule_count",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SI-3", "SC-5"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "web_acl_name": web_acl_name,
            "rule_state": "rules_absent",
            "pattern": "wafv2_web_acl_rule_count",
            "rule_count": 0,
            "gap": (
                f"aws_wafv2_web_acl '{web_acl_name}' declares zero rule "
                f"blocks. With the default_action set to allow (or even "
                f"block), zero rules means the Web ACL provides no L7 "
                f"protection beyond the default action. The Web ACL "
                f"may pass aws.api_gateway_waf_attached (it is attached) "
                f"but provides no actual rule-driven protection."
            ),
        },
        timestamp=now,
    )


def _count_rule_blocks(value: Any) -> int:
    """python-hcl2 represents repeated HCL blocks as either a single
    dict (one block) OR a list of dicts (multiple blocks). Returns
    the count; 0 if absent.
    """
    if isinstance(value, dict):
        return 1
    if isinstance(value, list):
        return sum(1 for item in value if isinstance(item, dict))
    return 0


def _as_str(value: Any) -> str | None:
    """python-hcl2 occasionally returns strings wrapped in single-element lists."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    return value if isinstance(value, str) else None
