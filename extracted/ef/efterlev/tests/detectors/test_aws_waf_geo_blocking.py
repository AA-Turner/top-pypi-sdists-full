"""Fixture-driven tests for `aws.waf_geo_blocking`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 3 #4 design", this is detector beta of
the Tier 3 #4 batch. Locks the binary `geo_blocking_present` /
`geo_blocking_absent` emission, the per-Web-ACL aggregation pattern,
and the country-code deduplication / sorting.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.waf_geo_blocking.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "waf_geo_blocking"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_web_acl_with_geo_block_emits_present() -> None:
    """Web ACL with one rule blocking the canonical embargoed-country
    set: emit geo_blocking_present with the country codes sorted."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "web_acl_with_geo_block.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.waf_geo_blocking"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert ev.controls_evidenced == ["SC-7", "AC-3"]
    assert ev.content["resource_name"] == "fed_workload"
    assert ev.content["rule_state"] == "geo_blocking_present"
    assert ev.content["pattern"] == "wafv2_web_acl_geo_blocking"
    assert ev.content["country_code_count"] == 4
    # Sorted output
    assert ev.content["country_codes"] == ["CU", "IR", "KP", "SY"]


# --- should_not_match (negative-evidence emission) ----------------------------


def test_web_acl_no_geo_block_emits_absent_with_intent_hint() -> None:
    """Web ACL with managed groups but no geo-match: emit absent with
    a gap message that explicitly names the may-be-intentional case."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "web_acl_no_geo_block.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "global_workload"
    assert ev.content["rule_state"] == "geo_blocking_absent"
    assert ev.content["country_code_count"] == 0
    assert ev.content["country_codes"] == []
    assert "may be intentional" in ev.content["gap"]
    assert "embargoed countries" in ev.content["gap"]


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
    assert results[0].content["rule_state"] == "geo_blocking_absent"


def test_multiple_geo_rules_dedupe_and_sort() -> None:
    """Web ACL with two geo-match rules with overlapping country
    sets: country_codes is the deduplicated, sorted union."""
    from efterlev.models import SourceRef, TerraformResource

    web_acl = TerraformResource(
        type="aws_wafv2_web_acl",
        name="multi_geo",
        kind="resource",
        body={
            "name": "multi-geo-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": [
                {
                    "name": "block-embargoed",
                    "priority": 1,
                    "action": {"block": {}},
                    "statement": {"geo_match_statement": {"country_codes": ["KP", "IR", "CU"]}},
                },
                {
                    "name": "block-additional",
                    "priority": 2,
                    "action": {"block": {}},
                    "statement": {
                        "geo_match_statement": {
                            "country_codes": ["IR", "SY", "CU"]  # overlaps with first
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
    assert ev.content["rule_state"] == "geo_blocking_present"
    # Deduplicated: {KP, IR, CU, SY} = 4 unique codes; sorted alphabetically
    assert ev.content["country_codes"] == ["CU", "IR", "KP", "SY"]
    assert ev.content["country_code_count"] == 4


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
        type="aws_wafv2_rule_group",
        name="rg",
        kind="resource",
        body={
            "name": "rg",
            "rule": [{"statement": {"geo_match_statement": {"country_codes": ["KP"]}}}],
        },
        source_ref=SourceRef(file="rg.tf", line_start=1, line_end=10),
    )
    assert detect([other]) == []


def test_mixed_web_acls_each_emits_correct_evidence() -> None:
    """Multiple Web ACLs with mixed geo posture: each gets its
    own evidence record."""
    from efterlev.models import SourceRef, TerraformResource

    fed = TerraformResource(
        type="aws_wafv2_web_acl",
        name="fed",
        kind="resource",
        body={
            "name": "fed-waf",
            "scope": "REGIONAL",
            "default_action": {"allow": {}},
            "rule": {
                "name": "block-embargoed",
                "priority": 1,
                "action": {"block": {}},
                "statement": {"geo_match_statement": {"country_codes": ["KP", "IR"]}},
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
    results = detect([fed, bare])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["fed"].content["rule_state"] == "geo_blocking_present"
    assert by_name["fed"].content["country_codes"] == ["IR", "KP"]
    assert by_name["bare"].content["rule_state"] == "geo_blocking_absent"
