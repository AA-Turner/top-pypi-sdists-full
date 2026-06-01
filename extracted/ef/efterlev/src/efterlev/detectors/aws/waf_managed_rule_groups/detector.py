"""KSI-CNA-RVP: AWS WAFv2 Web ACL managed-rule-group detector.

Reads Terraform source for `aws_wafv2_web_acl` resources and emits one
Evidence record per Web ACL describing whether at least one rule
references an AWS- or vendor-managed rule group via
`statement.managed_rule_group_statement`. Managed rule groups
(AWSManagedRulesCommonRuleSet, AWSManagedRulesKnownBadInputsRuleSet,
etc.) provide bulk OWASP-Top-10 / known-bad-input coverage that hand-
written custom rules rarely match for breadth.

Per DECISIONS 2026-05-10 "Tier 3 #1 design: aws.waf_* detector family
v0": this is detector gamma of the Tier 3 #1 batch. Per-Web-ACL emission
(NOT per-rule) per the family's first design choice. Two states
(binary, no `unverifiable` per the third design choice):
- `managed_groups_present` — at least one rule has a
  `managed_rule_group_statement`. The detail field lists the group
  names so the Gap Agent can reason about which groups were chosen.
- `managed_groups_absent` — zero managed-rule-group references across
  all rules. The Web ACL may still have hand-written custom rules
  (the sibling `aws.waf_rule_count` covers presence) but lacks
  managed bulk coverage.

Coverage classified `partial`: presence of a managed rule group does
not prove the chosen group is appropriate, that the override action
is `none` (so rules actually fire), or that the group is current.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.waf_managed_rule_groups",
    ksis=["KSI-CNA-RVP"],
    controls=["SI-3", "RA-5(11)"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit managed-rule-group Evidence per aws_wafv2_web_acl.

    Evidences (KSI):     KSI-CNA-RVP (Reviewing Protections) -- IaC-
                         layer per-Web-ACL managed-rule-group presence.
                         Joins aws.waf_rule_count, aws.cna_dos_protection,
                         and aws.api_gateway_waf_attached on this KSI.
    Evidences (800-53):  SI-3 (Malicious Code Protection at L7),
                         RA-5(11) (Public Disclosure Program -- proxy
                         signal that AWS-managed rule sets, which track
                         CVE-class disclosures, are in use).
    Does NOT prove:      the chosen managed group is appropriate for
                         the workload; the override action is `none`
                         (so rules fire vs only count); the group is
                         the current version. Action-type and version-
                         pinning are future detectors' territory.
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
    group_names = _collect_managed_group_names(r.body.get("rule"))

    if group_names:
        joined = ", ".join(group_names)
        return Evidence.create(
            detector_id="aws.waf_managed_rule_groups",
            ksis_evidenced=["KSI-CNA-RVP"],
            controls_evidenced=["SI-3", "RA-5(11)"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "web_acl_name": web_acl_name,
                "rule_state": "managed_groups_present",
                "pattern": "wafv2_web_acl_managed_rule_groups",
                "managed_group_count": len(group_names),
                "managed_group_names": group_names,
                "detail": (
                    f"web_acl_name={web_acl_name}; "
                    f"managed_group_count={len(group_names)}; "
                    f"managed_groups={joined}"
                ),
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.waf_managed_rule_groups",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SI-3", "RA-5(11)"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "web_acl_name": web_acl_name,
            "rule_state": "managed_groups_absent",
            "pattern": "wafv2_web_acl_managed_rule_groups",
            "managed_group_count": 0,
            "managed_group_names": [],
            "gap": (
                f"aws_wafv2_web_acl '{web_acl_name}' references zero "
                f"AWS- or vendor-managed rule groups. Custom rules can "
                f"complement managed groups but rarely match their "
                f"breadth for OWASP Top 10 / known-bad-input coverage. "
                f"Consider adding at least AWSManagedRulesCommonRuleSet "
                f"and AWSManagedRulesKnownBadInputsRuleSet via a "
                f"managed_rule_group_statement block."
            ),
        },
        timestamp=now,
    )


def _collect_managed_group_names(rule_value: Any) -> list[str]:
    """Walk every rule block and collect managed_rule_group_statement
    names. python-hcl2 represents repeated HCL blocks as either a single
    dict or a list of dicts at every level (rule, statement,
    managed_rule_group_statement).
    """
    rules = _as_block_list(rule_value)
    names: list[str] = []
    for rule in rules:
        statement = rule.get("statement")
        if statement is None:
            continue
        for stmt in _as_block_list(statement):
            for group in _as_block_list(stmt.get("managed_rule_group_statement")):
                name = _as_str(group.get("name"))
                if name:
                    names.append(name)
    return names


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
