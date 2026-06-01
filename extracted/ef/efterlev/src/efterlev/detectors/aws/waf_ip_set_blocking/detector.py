"""KSI-CNA-RVP: AWS WAFv2 Web ACL IP-set blocking detector.

Reads Terraform source for `aws_wafv2_web_acl` resources and emits one
Evidence record per Web ACL describing whether at least one rule
references an IP-set blocklist via `statement.ip_set_reference_statement`.
IP-set references typically point at an `aws_wafv2_ip_set` resource by
ARN (Terraform interpolation: `aws_wafv2_ip_set.bad_actors.arn`),
giving the boundary an explicit network-layer access-enforcement
primitive distinct from the bulk OWASP coverage managed groups
provide.

Per DECISIONS 2026-05-10 "Tier 3 #3 design: aws.waf_* family v1 --
action types + IP-set blocking": this is detector gamma of the
Tier 3 #3 batch. Per-Web-ACL emission. Two states (binary, no
`unverifiable`):
- `ip_set_blocking_present` -- at least one rule has an
  `ip_set_reference_statement`. Detail field lists the referenced
  IP-set ARN strings (typically Terraform interpolations) so the
  Gap Agent can reason about which lists the boundary uses.
- `ip_set_blocking_absent` -- zero IP-set references across all
  rules. The Web ACL relies on managed groups + custom rules but
  has no explicit IP-set access enforcement.

Coverage classified `partial`: presence of an IP-set reference does
not prove the underlying IP-set is current, that the IP-set's scope
is appropriate (a stale or empty IP-set provides no protection),
or that the rule's action enforces (a rule with override_action.count
on an IP-set match logs without blocking -- aws.waf_action_types
covers that dimension).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.waf_ip_set_blocking",
    ksis=["KSI-CNA-RVP"],
    controls=["SC-5", "AC-3"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit IP-set-blocking Evidence per aws_wafv2_web_acl.

    Evidences (KSI):     KSI-CNA-RVP (Reviewing Protections) -- IaC-
                         layer per-Web-ACL IP-set-reference presence.
                         7th detector evidencing KSI-CNA-RVP (joining
                         the Tier 3 #1 batch + Tier 3 #3 PR beta
                         waf_action_types).
    Evidences (800-53):  SC-5 (Denial of Service Protection),
                         AC-3 (Access Enforcement) -- IP-set blocking
                         is access enforcement at the network layer.
                         First WAF detector to evidence AC-3 at the
                         IaC layer.
    Does NOT prove:      the IP-set is current, the IP-set's scope is
                         appropriate, or the rule's action enforces
                         (a rule with override_action.count on an
                         IP-set match logs without blocking --
                         aws.waf_action_types covers that dimension).
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
    ip_set_arns = _collect_ip_set_arns(r.body.get("rule"))

    if ip_set_arns:
        joined = ", ".join(ip_set_arns)
        return Evidence.create(
            detector_id="aws.waf_ip_set_blocking",
            ksis_evidenced=["KSI-CNA-RVP"],
            controls_evidenced=["SC-5", "AC-3"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "web_acl_name": web_acl_name,
                "rule_state": "ip_set_blocking_present",
                "pattern": "wafv2_web_acl_ip_set_blocking",
                "ip_set_count": len(ip_set_arns),
                "ip_set_arns": ip_set_arns,
                "detail": (
                    f"web_acl_name={web_acl_name}; "
                    f"ip_set_count={len(ip_set_arns)}; "
                    f"ip_set_arns={joined}"
                ),
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.waf_ip_set_blocking",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SC-5", "AC-3"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "web_acl_name": web_acl_name,
            "rule_state": "ip_set_blocking_absent",
            "pattern": "wafv2_web_acl_ip_set_blocking",
            "ip_set_count": 0,
            "ip_set_arns": [],
            "gap": (
                f"aws_wafv2_web_acl '{web_acl_name}' references zero "
                f"IP-set blocklists. Without ip_set_reference_statement "
                f"rules, the Web ACL has no explicit network-layer "
                f"access enforcement -- it relies entirely on managed "
                f"groups and custom rules. Consider adding an "
                f"aws_wafv2_ip_set resource (AWS-managed feeds, "
                f"customer threat-intel lists, or per-tenant allowlists) "
                f"and referencing it from a rule via "
                f"statement.ip_set_reference_statement."
            ),
        },
        timestamp=now,
    )


def _collect_ip_set_arns(rule_value: Any) -> list[str]:
    """Walk every rule block and collect the `arn` strings from
    ip_set_reference_statement blocks. python-hcl2 represents repeated
    HCL blocks as either a single dict or a list of dicts at every
    level. Interpolations (e.g. `aws_wafv2_ip_set.bad_actors.arn`)
    come back as the literal expression string -- per the DECISIONS
    Decision #1 carry-forward, we don't try to cross-reference; the
    Gap Agent resolves them.
    """
    rules = _as_block_list(rule_value)
    arns: list[str] = []
    for rule in rules:
        statement = rule.get("statement")
        if statement is None:
            continue
        for stmt in _as_block_list(statement):
            for ip_set_ref in _as_block_list(stmt.get("ip_set_reference_statement")):
                arn = _as_str(ip_set_ref.get("arn"))
                if arn:
                    arns.append(arn)
    return arns


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
