"""Fixture-driven tests for `aws.waf_managed_rule_groups`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 3 #1 design", this is detector gamma of the
Tier 3 #1 batch. Locks the binary `managed_groups_present` /
`managed_groups_absent` emission and the per-Web-ACL aggregation pattern.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.waf_managed_rule_groups.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "waf_managed_rule_groups"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_web_acl_with_managed_groups_emits_managed_groups_present() -> None:
    """Web ACL with two managed-group rules: emit one record listing both."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "web_acl_with_managed_groups.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.waf_managed_rule_groups"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert ev.controls_evidenced == ["SI-3", "RA-5(11)"]
    assert ev.content["resource_type"] == "aws_wafv2_web_acl"
    assert ev.content["resource_name"] == "protected"
    assert ev.content["web_acl_name"] == "api-waf"
    assert ev.content["rule_state"] == "managed_groups_present"
    assert ev.content["pattern"] == "wafv2_web_acl_managed_rule_groups"
    assert ev.content["managed_group_count"] == 2
    assert ev.content["managed_group_names"] == [
        "AWSManagedRulesCommonRuleSet",
        "AWSManagedRulesKnownBadInputsRuleSet",
    ]
    assert "AWSManagedRulesCommonRuleSet" in ev.content["detail"]


# --- should_not_match (negative-evidence emission) ----------------------------


def test_web_acl_custom_rules_only_emits_managed_groups_absent() -> None:
    """Web ACL with only hand-written rules: emit gap with description that
    explicitly recommends adding managed groups."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "web_acl_custom_rules_only.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "custom_only"
    assert ev.content["web_acl_name"] == "custom-waf"
    assert ev.content["rule_state"] == "managed_groups_absent"
    assert ev.content["managed_group_count"] == 0
    assert ev.content["managed_group_names"] == []
    assert "zero AWS- or vendor-managed rule groups" in ev.content["gap"]
    assert "AWSManagedRulesCommonRuleSet" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_web_acl_with_no_rules_emits_managed_groups_absent() -> None:
    """Web ACL with no rule blocks at all: emit absent (consistent with the
    'rules_absent' case from waf_rule_count -- both gaps coexist)."""
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
    assert results[0].content["rule_state"] == "managed_groups_absent"
    assert results[0].content["managed_group_count"] == 0


def test_mixed_rules_some_managed_some_custom_emits_present() -> None:
    """Web ACL with one managed-group rule + one custom rule: still
    `managed_groups_present` (count == 1, only the managed one is listed)."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="mixed",
        kind="resource",
        body={
            "name": "mixed-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [
                {
                    "name": "managed",
                    "priority": 1,
                    "statement": {
                        "managed_rule_group_statement": {
                            "name": "AWSManagedRulesCommonRuleSet",
                            "vendor_name": "AWS",
                        }
                    },
                },
                {
                    "name": "custom",
                    "priority": 2,
                    "statement": {"byte_match_statement": {"search_string": "x"}},
                },
            ],
        },
        source_ref=SourceRef(file="mixed.tf", line_start=1, line_end=30),
    )
    results = detect([web_acl])
    assert len(results) == 1
    ev = results[0]
    assert ev.content["rule_state"] == "managed_groups_present"
    assert ev.content["managed_group_count"] == 1
    assert ev.content["managed_group_names"] == ["AWSManagedRulesCommonRuleSet"]


def test_web_acl_name_falls_back_to_resource_name() -> None:
    """`name` attribute omitted: detector falls back to the Terraform
    resource name."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="fallback_named",
        kind="resource",
        body={
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
        },
        source_ref=SourceRef(file="fallback.tf", line_start=1, line_end=8),
    )
    results = detect([web_acl])
    assert len(results) == 1
    assert results[0].content["web_acl_name"] == "fallback_named"


def test_non_web_acl_resources_emit_no_evidence() -> None:
    """Detector ignores resource types other than aws_wafv2_web_acl."""
    from efterlev.models import SourceRef, TerraformResource

    other = TerraformResource(
        type="aws_wafv2_rule_group",  # not a web_acl
        name="custom_group",
        kind="resource",
        body={
            "name": "custom-group",
            "rule": [
                {
                    "name": "managed",
                    "statement": {
                        "managed_rule_group_statement": {"name": "AWSManagedRulesCommonRuleSet"}
                    },
                }
            ],
        },
        source_ref=SourceRef(file="other.tf", line_start=1, line_end=10),
    )
    assert detect([other]) == []


def test_mixed_web_acls_each_emits_correct_evidence() -> None:
    """Multiple Web ACLs with mixed managed-group posture: each gets
    its own evidence record."""
    from efterlev.models import SourceRef, TerraformResource

    protected = TerraformResource(
        type="aws_wafv2_web_acl",
        name="protected",
        kind="resource",
        body={
            "name": "protected-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": {
                "name": "common",
                "priority": 1,
                "statement": {
                    "managed_rule_group_statement": {
                        "name": "AWSManagedRulesCommonRuleSet",
                        "vendor_name": "AWS",
                    }
                },
            },
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=15),
    )
    bare = TerraformResource(
        type="aws_wafv2_web_acl",
        name="bare",
        kind="resource",
        body={"name": "bare-waf", "scope": "REGIONAL", "default_action": {"allow": {}}},
        source_ref=SourceRef(file="main.tf", line_start=17, line_end=24),
    )
    results = detect([protected, bare])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["protected"].content["rule_state"] == "managed_groups_present"
    assert by_name["protected"].content["managed_group_count"] == 1
    assert by_name["bare"].content["rule_state"] == "managed_groups_absent"
    assert by_name["bare"].content["managed_group_count"] == 0
