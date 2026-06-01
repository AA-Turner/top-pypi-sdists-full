"""Fixture-driven tests for `aws.waf_rule_count`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 3 #1 design", this is detector β of the
Tier 3 #1 batch. Locks the binary `rules_present` / `rules_absent`
emission and the per-Web-ACL aggregation pattern.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.waf_rule_count.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "waf_rule_count"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_web_acl_with_rules_emits_rules_present() -> None:
    """Web ACL with at least one `rule` block."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "web_acl_with_rules.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.waf_rule_count"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert ev.controls_evidenced == ["SI-3", "SC-5"]
    assert ev.content["resource_type"] == "aws_wafv2_web_acl"
    assert ev.content["resource_name"] == "protected"
    assert ev.content["web_acl_name"] == "api-waf"
    assert ev.content["rule_state"] == "rules_present"
    assert ev.content["pattern"] == "wafv2_web_acl_rule_count"
    assert ev.content["rule_count"] == 1


# --- should_not_match (negative-evidence emission) ----------------------------


def test_web_acl_zero_rules_emits_rules_absent() -> None:
    """Web ACL with zero rule blocks: emit gap with description that
    explicitly notes the 'WAF attached but does nothing' shape."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "web_acl_zero_rules.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "bare"
    assert ev.content["web_acl_name"] == "bare-waf"
    assert ev.content["rule_state"] == "rules_absent"
    assert ev.content["rule_count"] == 0
    assert "zero rule blocks" in ev.content["gap"]
    assert "no L7 protection" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_web_acl_with_multiple_rules_counts_correctly() -> None:
    """Multiple `rule` blocks: count reflects all of them. python-hcl2
    represents repeated blocks as a list."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="multi_rule",
        kind="resource",
        body={
            "name": "multi-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [
                {"name": "r1", "priority": 1, "statement": {}},
                {"name": "r2", "priority": 2, "statement": {}},
                {"name": "r3", "priority": 3, "statement": {}},
            ],
        },
        source_ref=SourceRef(file="multi.tf", line_start=1, line_end=20),
    )
    results = detect([web_acl])
    assert len(results) == 1
    assert results[0].content["rule_state"] == "rules_present"
    assert results[0].content["rule_count"] == 3


def test_web_acl_name_falls_back_to_resource_name() -> None:
    """`name` attribute omitted (rare; provider rejects at apply):
    detector falls back to the Terraform resource name."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="fallback_named",
        kind="resource",
        body={
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [{"name": "r1", "priority": 1}],
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
        body={"name": "custom-group"},
        source_ref=SourceRef(file="other.tf", line_start=1, line_end=5),
    )
    assert detect([other]) == []


def test_mixed_web_acls_each_emits_correct_evidence() -> None:
    """Multiple Web ACLs with mixed rule counts: each gets its own
    evidence record."""
    from efterlev.models import SourceRef, TerraformResource

    protected = TerraformResource(
        type="aws_wafv2_web_acl",
        name="protected",
        kind="resource",
        body={
            "name": "protected-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [{"name": "r1", "priority": 1}, {"name": "r2", "priority": 2}],
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
    assert by_name["protected"].content["rule_state"] == "rules_present"
    assert by_name["protected"].content["rule_count"] == 2
    assert by_name["bare"].content["rule_state"] == "rules_absent"
    assert by_name["bare"].content["rule_count"] == 0
