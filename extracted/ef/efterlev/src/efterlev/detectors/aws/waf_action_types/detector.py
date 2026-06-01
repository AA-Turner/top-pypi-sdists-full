"""KSI-CNA-RVP: AWS WAFv2 Web ACL action-types detector.

Reads Terraform source for `aws_wafv2_web_acl` resources and emits one
Evidence record per Web ACL classifying the rules' action posture.
Each rule has either a custom `action { block | allow | captcha |
count {} }` or a managed-group `override_action { none | count {} }`.
A `count` action means "log this rule's matches but do not block
them" -- observability without enforcement. The canonical gap: a
managed-group rule with `override_action { count {} }` looks like
protection in the Web ACL listing but blocks nothing.

Per DECISIONS 2026-05-10 "Tier 3 #3 design: aws.waf_* family v1 --
action types + IP-set blocking": this is detector beta of the
Tier 3 #3 batch. Per-Web-ACL emission. Three states (per Decision #3,
the third state is informational, not a gap):
- `enforcing` -- every declared rule has an enforcing action (block /
  allow / captcha / override_action.none). Vacuously true on the
  empty rule set: a Web ACL with zero rules emits enforcing with
  zeros (the rules-absent gap is already covered by waf_rule_count).
- `observing_only` -- at least one rule is declared AND every rule
  is a count-action. The "WAF that observes but does not enforce"
  gap.
- `mixed` -- both enforcing and count rules present. NOT a gap by
  itself; a legitimate ramp-up tactic for new rule deployments.
  Information for the Gap Agent to reason about.

Rules without either `action` or `override_action` block are treated
as enforcing per Decision #6 -- the AWS-side default for a missing
`override_action` on a managed-group rule is `none`, which is
enforcing.

Coverage classified `partial`: presence of enforcing actions doesn't
prove the action choices are appropriate per rule (a `block` action
on an over-broad managed group might cause false positives a
`captcha` action would avoid). Future detectors can drill into
action-type appropriateness per managed-group.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_ENFORCING_CUSTOM_ACTIONS: frozenset[str] = frozenset({"block", "allow", "captcha"})
_OBSERVING_CUSTOM_ACTIONS: frozenset[str] = frozenset({"count"})
_ENFORCING_OVERRIDE_ACTIONS: frozenset[str] = frozenset({"none"})
_OBSERVING_OVERRIDE_ACTIONS: frozenset[str] = frozenset({"count"})


@detector(
    id="aws.waf_action_types",
    ksis=["KSI-CNA-RVP"],
    controls=["SI-3", "SC-5"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit action-types Evidence per aws_wafv2_web_acl.

    Evidences (KSI):     KSI-CNA-RVP (Reviewing Protections) -- IaC-
                         layer per-Web-ACL action-type posture. 6th
                         detector evidencing KSI-CNA-RVP after
                         Tier 3 #1.
    Evidences (800-53):  SI-3 (Malicious Code Protection at L7),
                         SC-5 (Denial of Service Protection).
    Does NOT prove:      action choices are appropriate per rule
                         (block vs captcha vs allow); the count
                         action is intentional ramp-up vs forgotten
                         dry-run mode; rule priorities affect whether
                         a high-priority allow short-circuits a
                         low-priority block.
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
    enforcing_rule_names, observing_rule_names = _classify_rules(r.body.get("rule"))
    enforcing_count = len(enforcing_rule_names)
    observing_count = len(observing_rule_names)

    if observing_count == 0:
        rule_state = "enforcing"
    elif enforcing_count == 0:
        rule_state = "observing_only"
    else:
        rule_state = "mixed"

    content: dict[str, Any] = {
        "resource_type": r.type,
        "resource_name": r.name,
        "web_acl_name": web_acl_name,
        "rule_state": rule_state,
        "pattern": "wafv2_web_acl_action_types",
        "rule_count": enforcing_count + observing_count,
        "enforcing_rule_count": enforcing_count,
        "observing_rule_count": observing_count,
        "enforcing_rule_names": enforcing_rule_names,
        "observing_rule_names": observing_rule_names,
    }

    if rule_state == "observing_only":
        content["gap"] = (
            f"aws_wafv2_web_acl '{web_acl_name}' has {observing_count} "
            f"rule(s), all of which use count actions (custom rule "
            f"action.count or managed-group override_action.count). "
            f"Count actions log matches without blocking traffic -- "
            f"observability without enforcement. The Web ACL appears "
            f"protected in the AWS console but actually blocks nothing. "
            f"Verify whether this is intentional ramp-up or a forgotten "
            f"dry-run."
        )
    else:
        content["detail"] = (
            f"web_acl_name={web_acl_name}; "
            f"enforcing_count={enforcing_count}; "
            f"observing_count={observing_count}"
        )
        if rule_state == "mixed":
            content["detail"] += f"; observing_rules={', '.join(observing_rule_names)}"

    return Evidence.create(
        detector_id="aws.waf_action_types",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SI-3", "SC-5"],
        source_ref=r.source_ref,
        content=content,
        timestamp=now,
    )


def _classify_rules(rule_value: Any) -> tuple[list[str], list[str]]:
    """Walk every rule block and return (enforcing_names, observing_names).

    Each rule classifies as enforcing or observing based on its action
    or override_action keys (per Decision #6 of the DECISIONS entry,
    rules without either default to enforcing).
    """
    enforcing: list[str] = []
    observing: list[str] = []
    for index, rule in enumerate(_as_block_list(rule_value)):
        rule_name = _as_str(rule.get("name")) or f"rule_{index}"
        if _rule_is_observing(rule):
            observing.append(rule_name)
        else:
            enforcing.append(rule_name)
    return enforcing, observing


def _rule_is_observing(rule: dict[str, Any]) -> bool:
    """A rule is observing if its action.count or override_action.count
    is set. Custom rule actions (action.block / .allow / .captcha) and
    managed-group override_action.none are enforcing. Missing both
    blocks defaults to enforcing per Decision #6.
    """
    for action_block in _as_block_list(rule.get("action")):
        for key in action_block:
            if key in _OBSERVING_CUSTOM_ACTIONS:
                return True
            if key in _ENFORCING_CUSTOM_ACTIONS:
                return False

    for override_block in _as_block_list(rule.get("override_action")):
        for key in override_block:
            if key in _OBSERVING_OVERRIDE_ACTIONS:
                return True
            if key in _ENFORCING_OVERRIDE_ACTIONS:
                return False

    return False  # neither action nor override_action -> default enforcing


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
