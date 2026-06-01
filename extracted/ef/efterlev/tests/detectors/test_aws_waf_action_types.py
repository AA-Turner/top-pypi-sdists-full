"""Fixture-driven tests for `aws.waf_action_types`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 3 #3 design", this is detector beta of
the Tier 3 #3 batch. Locks the three-state classification
(enforcing / observing_only / mixed) and the per-Web-ACL aggregation
pattern.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.waf_action_types.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "waf_action_types"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_web_acl_enforcing_emits_enforcing() -> None:
    """Web ACL with one action.block rule: emit enforcing."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "web_acl_enforcing.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.waf_action_types"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert ev.controls_evidenced == ["SI-3", "SC-5"]
    assert ev.content["resource_name"] == "enforcing_one"
    assert ev.content["rule_state"] == "enforcing"
    assert ev.content["rule_count"] == 1
    assert ev.content["enforcing_rule_count"] == 1
    assert ev.content["observing_rule_count"] == 0
    assert ev.content["enforcing_rule_names"] == ["block-bad-host"]


# --- should_not_match (negative-evidence emission) ----------------------------


def test_web_acl_observing_only_emits_gap() -> None:
    """Web ACL with one override_action.count managed-group rule:
    emit observing_only with a gap message."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "web_acl_observing_only.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "observing_only"
    assert ev.content["rule_state"] == "observing_only"
    assert ev.content["enforcing_rule_count"] == 0
    assert ev.content["observing_rule_count"] == 1
    assert ev.content["observing_rule_names"] == ["common-rules-in-count"]
    assert "all of which use count actions" in ev.content["gap"]
    assert "appears protected" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_web_acl_with_no_rules_emits_enforcing_vacuously() -> None:
    """Web ACL with no rule blocks: emit enforcing with 0/0 counts.
    Per Decision #3, this is vacuously enforcing -- the rules-absent
    gap is already flagged by aws.waf_rule_count."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="bare",
        kind="resource",
        body={"name": "bare-waf", "scope": "REGIONAL", "default_action": {"allow": {}}},
        source_ref=SourceRef(file="bare.tf", line_start=1, line_end=8),
    )
    results = detect([web_acl])
    assert len(results) == 1
    ev = results[0]
    assert ev.content["rule_state"] == "enforcing"
    assert ev.content["rule_count"] == 0
    assert ev.content["enforcing_rule_count"] == 0
    assert ev.content["observing_rule_count"] == 0


def test_mixed_action_types_emits_mixed_informational() -> None:
    """Web ACL with one enforcing rule + one count rule: emit mixed.
    Per Decision #3, mixed is informational, not a gap."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="mixed_acl",
        kind="resource",
        body={
            "name": "mixed-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [
                {
                    "name": "enforced-rule",
                    "priority": 1,
                    "action": {"block": {}},
                    "statement": {},
                },
                {
                    "name": "counted-rule",
                    "priority": 2,
                    "override_action": {"count": {}},
                    "statement": {
                        "managed_rule_group_statement": {"name": "AWSManagedRulesCommonRuleSet"}
                    },
                },
            ],
        },
        source_ref=SourceRef(file="mixed.tf", line_start=1, line_end=30),
    )
    results = detect([web_acl])
    assert len(results) == 1
    ev = results[0]
    assert ev.content["rule_state"] == "mixed"
    assert ev.content["enforcing_rule_count"] == 1
    assert ev.content["observing_rule_count"] == 1
    assert "gap" not in ev.content  # mixed is informational, no gap
    assert "counted-rule" in ev.content["detail"]


def test_rule_with_no_action_block_defaults_to_enforcing() -> None:
    """Per Decision #6: a rule with neither action nor override_action
    defaults to enforcing (AWS-side default for managed-group
    override_action is `none`).
    """
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="default_enforce",
        kind="resource",
        body={
            "name": "default-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": {
                "name": "no-action-spec",
                "priority": 1,
                "statement": {"managed_rule_group_statement": {"name": "X"}},
            },
        },
        source_ref=SourceRef(file="default.tf", line_start=1, line_end=15),
    )
    results = detect([web_acl])
    assert len(results) == 1
    ev = results[0]
    assert ev.content["rule_state"] == "enforcing"
    assert ev.content["enforcing_rule_count"] == 1
    assert ev.content["observing_rule_count"] == 0


def test_override_action_none_is_enforcing() -> None:
    """override_action.none is the AWS-side default for managed-group
    rules and means "use the managed group's default actions" --
    enforcing."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="override_none",
        kind="resource",
        body={
            "name": "override-none-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": {
                "name": "managed-enforcing",
                "priority": 1,
                "override_action": {"none": {}},
                "statement": {"managed_rule_group_statement": {"name": "X"}},
            },
        },
        source_ref=SourceRef(file="override.tf", line_start=1, line_end=15),
    )
    results = detect([web_acl])
    assert len(results) == 1
    assert results[0].content["rule_state"] == "enforcing"


def test_non_web_acl_resources_emit_no_evidence() -> None:
    """Detector ignores resource types other than aws_wafv2_web_acl."""
    from efterlev.models import SourceRef, TerraformResource

    other = TerraformResource(
        type="aws_wafv2_rule_group",
        name="rg",
        kind="resource",
        body={"name": "rg", "rule": [{"action": {"count": {}}}]},
        source_ref=SourceRef(file="other.tf", line_start=1, line_end=5),
    )
    assert detect([other]) == []


def test_mixed_web_acls_each_emits_correct_evidence() -> None:
    """Multiple Web ACLs with mixed action posture: each gets its
    own evidence record."""
    from efterlev.models import SourceRef, TerraformResource

    enforcing = TerraformResource(
        type="aws_wafv2_web_acl",
        name="enforcing",
        kind="resource",
        body={
            "name": "enforcing-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": {"name": "r", "action": {"block": {}}, "statement": {}},
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=15),
    )
    observing = TerraformResource(
        type="aws_wafv2_web_acl",
        name="observing",
        kind="resource",
        body={
            "name": "observing-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": {
                "name": "r",
                "override_action": {"count": {}},
                "statement": {"managed_rule_group_statement": {"name": "X"}},
            },
        },
        source_ref=SourceRef(file="main.tf", line_start=17, line_end=30),
    )
    results = detect([enforcing, observing])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["enforcing"].content["rule_state"] == "enforcing"
    assert by_name["observing"].content["rule_state"] == "observing_only"
