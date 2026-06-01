"""Fixture-driven tests for `aws.waf_rate_limiting`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 3 #1 design", this is detector delta of the
Tier 3 #1 batch. Locks the binary `rate_limiting_present` /
`rate_limiting_absent` emission and the per-Web-ACL aggregation pattern.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.waf_rate_limiting.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "waf_rate_limiting"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_web_acl_with_rate_limit_emits_rate_limiting_present() -> None:
    """Web ACL with one rate-based statement: emit one record listing
    the limit and aggregate-key type."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "web_acl_with_rate_limit.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.waf_rate_limiting"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert ev.controls_evidenced == ["SC-5", "SC-5(2)"]
    assert ev.content["resource_type"] == "aws_wafv2_web_acl"
    assert ev.content["resource_name"] == "protected"
    assert ev.content["web_acl_name"] == "api-waf"
    assert ev.content["rule_state"] == "rate_limiting_present"
    assert ev.content["pattern"] == "wafv2_web_acl_rate_limiting"
    assert ev.content["rate_limit_count"] == 1
    assert ev.content["rate_limits"] == [{"limit": 2000, "aggregate_key_type": "IP"}]
    assert "limit=2000" in ev.content["detail"]
    assert "key=IP" in ev.content["detail"]


# --- should_not_match (negative-evidence emission) ----------------------------


def test_web_acl_managed_only_emits_rate_limiting_absent() -> None:
    """Web ACL with managed groups but no rate-based statement: emit
    gap with description that explicitly recommends adding a
    rate_based_statement."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "web_acl_managed_only.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "managed_only"
    assert ev.content["web_acl_name"] == "managed-only-waf"
    assert ev.content["rule_state"] == "rate_limiting_absent"
    assert ev.content["rate_limit_count"] == 0
    assert ev.content["rate_limits"] == []
    assert "zero rate-based statements" in ev.content["gap"]
    assert "rate_based_statement" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_web_acl_with_no_rules_emits_rate_limiting_absent() -> None:
    """Web ACL with no rule blocks at all: emit absent (consistent with
    the corresponding state in the sibling waf_* detectors)."""
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
    assert results[0].content["rule_state"] == "rate_limiting_absent"
    assert results[0].content["rate_limit_count"] == 0


def test_multiple_rate_based_statements_all_listed() -> None:
    """Web ACL with two rate-based statements (e.g., one IP, one
    FORWARDED_IP): both limits and key types appear in the evidence."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="multi_rate",
        kind="resource",
        body={
            "name": "multi-rate-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [
                {
                    "name": "ip-rate",
                    "priority": 1,
                    "statement": {
                        "rate_based_statement": {
                            "limit": 2000,
                            "aggregate_key_type": "IP",
                        }
                    },
                },
                {
                    "name": "forwarded-ip-rate",
                    "priority": 2,
                    "statement": {
                        "rate_based_statement": {
                            "limit": 5000,
                            "aggregate_key_type": "FORWARDED_IP",
                        }
                    },
                },
            ],
        },
        source_ref=SourceRef(file="multi.tf", line_start=1, line_end=30),
    )
    results = detect([web_acl])
    assert len(results) == 1
    ev = results[0]
    assert ev.content["rule_state"] == "rate_limiting_present"
    assert ev.content["rate_limit_count"] == 2
    assert ev.content["rate_limits"] == [
        {"limit": 2000, "aggregate_key_type": "IP"},
        {"limit": 5000, "aggregate_key_type": "FORWARDED_IP"},
    ]


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
                    "name": "rate",
                    "statement": {
                        "rate_based_statement": {"limit": 100, "aggregate_key_type": "IP"}
                    },
                }
            ],
        },
        source_ref=SourceRef(file="other.tf", line_start=1, line_end=10),
    )
    assert detect([other]) == []


def test_mixed_web_acls_each_emits_correct_evidence() -> None:
    """Multiple Web ACLs with mixed rate-limiting posture: each gets
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
                "name": "rate",
                "priority": 1,
                "statement": {
                    "rate_based_statement": {
                        "limit": 1000,
                        "aggregate_key_type": "IP",
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
    assert by_name["protected"].content["rule_state"] == "rate_limiting_present"
    assert by_name["protected"].content["rate_limit_count"] == 1
    assert by_name["protected"].content["rate_limits"] == [
        {"limit": 1000, "aggregate_key_type": "IP"}
    ]
    assert by_name["bare"].content["rule_state"] == "rate_limiting_absent"
    assert by_name["bare"].content["rate_limit_count"] == 0


def test_aggregate_key_type_defaults_to_ip_when_omitted() -> None:
    """`aggregate_key_type` is technically required by AWS but if a
    user omits it (or python-hcl2 returns it as None), default to IP
    so we don't crash and so the Gap Agent gets a usable signal."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="default_key",
        kind="resource",
        body={
            "name": "default-key-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": {
                "name": "rate",
                "priority": 1,
                "statement": {
                    "rate_based_statement": {"limit": 500},
                },
            },
        },
        source_ref=SourceRef(file="default.tf", line_start=1, line_end=15),
    )
    results = detect([web_acl])
    assert len(results) == 1
    ev = results[0]
    assert ev.content["rate_limits"] == [{"limit": 500, "aggregate_key_type": "IP"}]
