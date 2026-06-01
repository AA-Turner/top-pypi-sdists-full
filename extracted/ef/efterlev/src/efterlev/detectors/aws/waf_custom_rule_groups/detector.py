"""KSI-CNA-RVP: AWS WAFv2 Web ACL custom-rule-groups detector.

Reads Terraform source for both `aws_wafv2_web_acl` AND
`aws_wafv2_rule_group` resources. For each Web ACL, walks rules
looking for `statement.rule_group_reference_statement.arn`
references; emits per Web ACL whether any references exist. Custom
rule groups are the customer-curated complement to managed groups
-- in mature WAF deployments customers ship workload-specific rule
sets that managed groups don't cover (application-specific
malicious-pattern rules, per-tenant access controls, etc.).

The `defined_rule_groups` inventory in the evidence content lists
the `aws_wafv2_rule_group` resource names found in the same
plan/repo, regardless of whether the Web ACL references them.
This lets the Gap Agent flag the "defined but unreferenced"
anti-pattern from the absent state.

Per DECISIONS 2026-05-10 "Tier 3 #5 design: aws.waf_custom_rule_groups
(closes the WAF family at 7/7)": this is detector beta of the
Tier 3 #5 batch -- the FINAL detector closing the WAF family v0/v1
arc that started in v0.1.46. Per-Web-ACL emission. Two states
(binary, no `unverifiable`):
- `custom_rule_groups_present` -- at least one rule has a
  `rule_group_reference_statement`. Detail field lists the
  referenced ARN strings (typically Terraform interpolations).
- `custom_rule_groups_absent` -- zero references across all rules.
  Gap message includes `defined_rule_groups` so the Gap Agent can
  flag the "defined but unreferenced" anti-pattern explicitly.

Per Decision #3: no cross-resource VALIDATION at the detector
layer -- the literal ARN strings (Terraform interpolations) are
emitted as-is. The Gap Agent reasons about whether references
resolve and whether unreferenced groups are intentional.

Coverage classified `partial`: presence of a rule group reference
doesn't prove the rule group's rules are appropriate to the
workload (an empty rule group provides no protection; a stale
legacy rule group provides only token coverage).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.waf_custom_rule_groups",
    ksis=["KSI-CNA-RVP"],
    controls=["SI-3", "SC-7"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit custom-rule-groups Evidence per aws_wafv2_web_acl.

    Cross-resource detector: walks both aws_wafv2_web_acl AND
    aws_wafv2_rule_group resources. The defined_rule_groups
    inventory lets the Gap Agent flag the "defined but unreferenced"
    anti-pattern from the absent state.

    Evidences (KSI):     KSI-CNA-RVP (Reviewing Protections) -- IaC-
                         layer per-Web-ACL custom-rule-group
                         reference presence. 9th detector evidencing
                         KSI-CNA-RVP after Tier 3 #4. Final WAF v0/v1
                         dimension.
    Evidences (800-53):  SI-3 (Malicious Code Protection at L7 --
                         custom groups are the customer-curated
                         complement to managed groups), SC-7
                         (Boundary Protection -- custom groups can
                         encode workload-specific perimeter rules).
    Does NOT prove:      the referenced rule group's rules are
                         appropriate (empty / stale / mis-scoped
                         groups provide only token coverage); the
                         rule_group_reference_statement.arn resolves
                         to an extant aws_wafv2_rule_group (Gap Agent
                         handles cross-reference resolution per
                         DECISIONS Decision #3).
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    defined_rule_groups = sorted(r.name for r in resources if r.type == "aws_wafv2_rule_group")

    for r in resources:
        if r.type != "aws_wafv2_web_acl":
            continue
        out.append(_emit_web_acl_evidence(r, now, defined_rule_groups))

    return out


def _emit_web_acl_evidence(
    r: TerraformResource, now: datetime, defined_rule_groups: list[str]
) -> Evidence:
    web_acl_name = _as_str(r.body.get("name")) or r.name
    referenced_arns = _collect_rule_group_arns(r.body.get("rule"))

    if referenced_arns:
        joined = ", ".join(referenced_arns)
        return Evidence.create(
            detector_id="aws.waf_custom_rule_groups",
            ksis_evidenced=["KSI-CNA-RVP"],
            controls_evidenced=["SI-3", "SC-7"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "web_acl_name": web_acl_name,
                "rule_state": "custom_rule_groups_present",
                "pattern": "wafv2_web_acl_custom_rule_groups",
                "referenced_arn_count": len(referenced_arns),
                "referenced_arns": referenced_arns,
                "defined_rule_groups": defined_rule_groups,
                "detail": (
                    f"web_acl_name={web_acl_name}; "
                    f"referenced_arn_count={len(referenced_arns)}; "
                    f"referenced_arns={joined}"
                ),
            },
            timestamp=now,
        )

    inventory_note = (
        f"; defined_rule_groups_in_scope={', '.join(defined_rule_groups)}"
        if defined_rule_groups
        else "; no aws_wafv2_rule_group resources in scope"
    )
    return Evidence.create(
        detector_id="aws.waf_custom_rule_groups",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SI-3", "SC-7"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "web_acl_name": web_acl_name,
            "rule_state": "custom_rule_groups_absent",
            "pattern": "wafv2_web_acl_custom_rule_groups",
            "referenced_arn_count": 0,
            "referenced_arns": [],
            "defined_rule_groups": defined_rule_groups,
            "gap": (
                f"aws_wafv2_web_acl '{web_acl_name}' references zero "
                f"customer-defined rule groups via "
                f"rule_group_reference_statement. Custom rule groups "
                f"are the customer-curated complement to AWS-managed "
                f"groups -- in mature deployments they encode "
                f"workload-specific malicious-pattern rules, per-tenant "
                f"access controls, and other domain-specific signatures "
                f"managed groups do not cover{inventory_note}."
            ),
        },
        timestamp=now,
    )


def _collect_rule_group_arns(rule_value: Any) -> list[str]:
    """Walk every rule block and collect the deduplicated set of
    `arn` strings from rule_group_reference_statement blocks. Per
    DECISIONS Decision #3, no validation that the ARN resolves to
    an extant aws_wafv2_rule_group resource -- emit literal strings.
    """
    rules = _as_block_list(rule_value)
    seen: list[str] = []
    seen_set: set[str] = set()
    for rule in rules:
        statement = rule.get("statement")
        if statement is None:
            continue
        for stmt in _as_block_list(statement):
            for ref in _as_block_list(stmt.get("rule_group_reference_statement")):
                arn = _as_str(ref.get("arn"))
                if arn and arn not in seen_set:
                    seen.append(arn)
                    seen_set.add(arn)
    return seen


def _as_block_list(value: Any) -> list[dict[str, Any]]:
    """Normalize python-hcl2's "single dict OR list of dicts" block
    representation into a list of dicts."""
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def _as_str(value: Any) -> str | None:
    """python-hcl2 occasionally returns strings wrapped in single-element lists."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    return value if isinstance(value, str) else None
