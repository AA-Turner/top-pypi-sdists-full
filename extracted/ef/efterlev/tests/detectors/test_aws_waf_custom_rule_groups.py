"""Fixture-driven tests for `aws.waf_custom_rule_groups`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 3 #5 design", this is detector beta of
the Tier 3 #5 batch -- the FINAL detector closing the WAF family v0/v1
arc. Locks the binary `custom_rule_groups_present` /
`custom_rule_groups_absent` emission, the cross-resource
`defined_rule_groups` inventory, and the per-Web-ACL aggregation
pattern.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.waf_custom_rule_groups.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "waf_custom_rule_groups"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_web_acl_with_custom_group_emits_present() -> None:
    """Web ACL with one rule_group_reference_statement: emit
    custom_rule_groups_present with the referenced ARN listed."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "web_acl_with_custom_group.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.waf_custom_rule_groups"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert ev.controls_evidenced == ["SI-3", "SC-7"]
    assert ev.content["resource_name"] == "protected"
    assert ev.content["rule_state"] == "custom_rule_groups_present"
    assert ev.content["referenced_arn_count"] == 1
    # The ARN comes through as a Terraform interpolation -- just check
    # the rule group's resource name is in the literal expression.
    assert any("api_specific_rules" in arn for arn in ev.content["referenced_arns"])
    # Inventory: the api_specific_rules group is defined in the same fixture.
    assert ev.content["defined_rule_groups"] == ["api_specific_rules"]


# --- should_not_match (the canonical "defined but unreferenced" anti-pattern) -


def test_web_acl_unreferenced_group_emits_absent_with_inventory() -> None:
    """The canonical 'defined but unreferenced' anti-pattern: an
    aws_wafv2_rule_group exists but no Web ACL references it. The
    absent state's gap message surfaces the inventory so the Gap
    Agent can flag this explicitly."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "web_acl_unreferenced_group.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "managed_only"
    assert ev.content["rule_state"] == "custom_rule_groups_absent"
    assert ev.content["referenced_arn_count"] == 0
    assert ev.content["referenced_arns"] == []
    # The defined_rule_groups inventory lists the orphaned group.
    assert ev.content["defined_rule_groups"] == ["orphaned_rules"]
    assert "orphaned_rules" in ev.content["gap"]
    assert "customer-curated complement" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_web_acl_with_no_rule_groups_and_no_inventory() -> None:
    """Web ACL with no rule_group references AND no rule_group
    resources defined in scope: emit absent with empty inventory.
    The gap message names the no-inventory case."""
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
    assert ev.content["rule_state"] == "custom_rule_groups_absent"
    assert ev.content["defined_rule_groups"] == []
    assert "no aws_wafv2_rule_group resources in scope" in ev.content["gap"]


def test_multiple_referenced_groups_dedup() -> None:
    """Web ACL with two rules referencing different rule groups +
    one rule that re-references the first group: referenced_arns
    is deduplicated, order-preserving."""
    from efterlev.models import SourceRef, TerraformResource

    rg_a = TerraformResource(
        type="aws_wafv2_rule_group",
        name="group_a",
        kind="resource",
        body={"name": "group-a"},
        source_ref=SourceRef(file="a.tf", line_start=1, line_end=5),
    )
    rg_b = TerraformResource(
        type="aws_wafv2_rule_group",
        name="group_b",
        kind="resource",
        body={"name": "group-b"},
        source_ref=SourceRef(file="b.tf", line_start=1, line_end=5),
    )
    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="multi_ref",
        kind="resource",
        body={
            "name": "multi-ref-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [
                {
                    "name": "apply-a",
                    "priority": 1,
                    "statement": {
                        "rule_group_reference_statement": {
                            "arn": "${aws_wafv2_rule_group.group_a.arn}"
                        }
                    },
                },
                {
                    "name": "apply-b",
                    "priority": 2,
                    "statement": {
                        "rule_group_reference_statement": {
                            "arn": "${aws_wafv2_rule_group.group_b.arn}"
                        }
                    },
                },
                {
                    "name": "apply-a-again",
                    "priority": 3,
                    "statement": {
                        "rule_group_reference_statement": {
                            "arn": "${aws_wafv2_rule_group.group_a.arn}"
                        }
                    },
                },
            ],
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=30),
    )
    results = detect([rg_a, rg_b, web_acl])
    assert len(results) == 1
    ev = results[0]
    assert ev.content["rule_state"] == "custom_rule_groups_present"
    assert ev.content["referenced_arn_count"] == 2  # deduplicated
    # Order-preserving (group_a appears first):
    assert "group_a" in ev.content["referenced_arns"][0]
    assert "group_b" in ev.content["referenced_arns"][1]
    # defined_rule_groups is sorted alphabetically.
    assert ev.content["defined_rule_groups"] == ["group_a", "group_b"]


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
    """Detector ignores resource types other than aws_wafv2_web_acl.
    The aws_wafv2_rule_group resource is walked for inventory but
    doesn't produce its own evidence record."""
    from efterlev.models import SourceRef, TerraformResource

    rg = TerraformResource(
        type="aws_wafv2_rule_group",
        name="some_group",
        kind="resource",
        body={"name": "some-group"},
        source_ref=SourceRef(file="rg.tf", line_start=1, line_end=5),
    )
    # Just an aws_wafv2_rule_group with no Web ACL -> no evidence.
    assert detect([rg]) == []


def test_mixed_web_acls_each_sees_same_inventory() -> None:
    """Multiple Web ACLs with mixed reference posture: each gets
    its own evidence record but the `defined_rule_groups` inventory
    is the same global set (helps the Gap Agent reason about the
    workload's rule-group landscape consistently across Web ACLs)."""
    from efterlev.models import SourceRef, TerraformResource

    rg = TerraformResource(
        type="aws_wafv2_rule_group",
        name="api_rules",
        kind="resource",
        body={"name": "api-rules"},
        source_ref=SourceRef(file="rg.tf", line_start=1, line_end=5),
    )
    referencing = TerraformResource(
        type="aws_wafv2_web_acl",
        name="referencing",
        kind="resource",
        body={
            "name": "referencing-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": {
                "name": "apply",
                "priority": 1,
                "statement": {
                    "rule_group_reference_statement": {
                        "arn": "${aws_wafv2_rule_group.api_rules.arn}"
                    }
                },
            },
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=15),
    )
    not_referencing = TerraformResource(
        type="aws_wafv2_web_acl",
        name="not_referencing",
        kind="resource",
        body={
            "name": "not-referencing-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
        },
        source_ref=SourceRef(file="main.tf", line_start=17, line_end=24),
    )
    results = detect([rg, referencing, not_referencing])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["referencing"].content["rule_state"] == "custom_rule_groups_present"
    assert by_name["not_referencing"].content["rule_state"] == "custom_rule_groups_absent"
    # Both see the same global inventory.
    assert by_name["referencing"].content["defined_rule_groups"] == ["api_rules"]
    assert by_name["not_referencing"].content["defined_rule_groups"] == ["api_rules"]
