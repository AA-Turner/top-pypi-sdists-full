"""Fixture-driven tests for `aws.waf_ip_set_blocking`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 3 #3 design", this is detector gamma of
the Tier 3 #3 batch. Locks the binary `ip_set_blocking_present` /
`ip_set_blocking_absent` emission and the per-Web-ACL aggregation
pattern.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.waf_ip_set_blocking.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "waf_ip_set_blocking"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_web_acl_with_ip_set_emits_present() -> None:
    """Web ACL with one rule referencing an aws_wafv2_ip_set: emit
    ip_set_blocking_present with the ARN string in detail."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "web_acl_with_ip_set.tf")
    # Two resources in the fixture file -- the aws_wafv2_ip_set is
    # ignored (not aws_wafv2_web_acl); only the Web ACL gets an
    # evidence record.
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.waf_ip_set_blocking"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert ev.controls_evidenced == ["SC-5", "AC-3"]
    assert ev.content["resource_name"] == "protected"
    assert ev.content["rule_state"] == "ip_set_blocking_present"
    assert ev.content["pattern"] == "wafv2_web_acl_ip_set_blocking"
    assert ev.content["ip_set_count"] == 1
    # python-hcl2 returns interpolations as the literal expression
    # string (with a `${...}` wrapper). Just check the IP-set name
    # substring is in there.
    assert any("bad_actors" in arn for arn in ev.content["ip_set_arns"])


# --- should_not_match (negative-evidence emission) ----------------------------


def test_web_acl_no_ip_set_emits_absent() -> None:
    """Web ACL with only a managed-group rule, no IP-set reference:
    emit ip_set_blocking_absent with a gap message."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "web_acl_no_ip_set.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "managed_only"
    assert ev.content["rule_state"] == "ip_set_blocking_absent"
    assert ev.content["ip_set_count"] == 0
    assert ev.content["ip_set_arns"] == []
    assert "zero IP-set blocklists" in ev.content["gap"]
    assert "ip_set_reference_statement" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_web_acl_with_no_rules_emits_absent() -> None:
    """Web ACL with no rule blocks: emit absent (consistent with the
    sibling waf_* detectors' negative path)."""
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
    assert results[0].content["rule_state"] == "ip_set_blocking_absent"


def test_multiple_ip_sets_all_listed() -> None:
    """Web ACL with two rules each referencing a different IP-set:
    both ARNs appear in the evidence."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="multi_ip",
        kind="resource",
        body={
            "name": "multi-ip-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [
                {
                    "name": "block-bad-actors",
                    "priority": 1,
                    "action": {"block": {}},
                    "statement": {
                        "ip_set_reference_statement": {"arn": "${aws_wafv2_ip_set.bad_actors.arn}"}
                    },
                },
                {
                    "name": "block-tor-exits",
                    "priority": 2,
                    "action": {"block": {}},
                    "statement": {
                        "ip_set_reference_statement": {"arn": "${aws_wafv2_ip_set.tor_exits.arn}"}
                    },
                },
            ],
        },
        source_ref=SourceRef(file="multi.tf", line_start=1, line_end=30),
    )
    results = detect([web_acl])
    assert len(results) == 1
    ev = results[0]
    assert ev.content["rule_state"] == "ip_set_blocking_present"
    assert ev.content["ip_set_count"] == 2
    assert "bad_actors" in ev.content["detail"]
    assert "tor_exits" in ev.content["detail"]


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
    """Detector ignores resource types other than aws_wafv2_web_acl
    (notably the aws_wafv2_ip_set resources themselves)."""
    from efterlev.models import SourceRef, TerraformResource

    ip_set = TerraformResource(
        type="aws_wafv2_ip_set",
        name="bad_actors",
        kind="resource",
        body={"name": "bad-actors", "addresses": ["1.2.3.4/32"]},
        source_ref=SourceRef(file="other.tf", line_start=1, line_end=5),
    )
    rule_group = TerraformResource(
        type="aws_wafv2_rule_group",
        name="custom",
        kind="resource",
        body={
            "name": "custom-rg",
            "rule": [
                {
                    "name": "r",
                    "statement": {
                        "ip_set_reference_statement": {"arn": "${aws_wafv2_ip_set.x.arn}"}
                    },
                }
            ],
        },
        source_ref=SourceRef(file="rg.tf", line_start=1, line_end=15),
    )
    assert detect([ip_set, rule_group]) == []


def test_mixed_web_acls_each_emits_correct_evidence() -> None:
    """Multiple Web ACLs with mixed IP-set posture: each gets its
    own evidence record."""
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
                "name": "block-ip",
                "priority": 1,
                "action": {"block": {}},
                "statement": {"ip_set_reference_statement": {"arn": "${aws_wafv2_ip_set.bad.arn}"}},
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
    assert by_name["protected"].content["rule_state"] == "ip_set_blocking_present"
    assert by_name["bare"].content["rule_state"] == "ip_set_blocking_absent"
