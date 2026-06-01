"""Fixture-driven + synthetic-resource tests for `github.branch_protection`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape. Adds in-process synthetic-resource
tests for multi-resource mix + non-github-resource filter + name-only-rule.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.github.branch_protection.detector import detect
from efterlev.models import SourceRef, TerraformResource
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "github"
    / "branch_protection"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_branch_protection_with_all_blocks_emits_protections_present() -> None:
    """Branch protection rule with required reviews + status checks +
    enforce_admins emits protections_present with all three flags True."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "branch_protection_enforced.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "github.branch_protection"
    assert ev.ksis_evidenced == ["KSI-PIY-RSD"]
    assert ev.controls_evidenced == ["SA-15", "CM-2"]
    assert ev.content["resource_type"] == "github_branch_protection"
    assert ev.content["resource_name"] == "main"
    assert ev.content["protected_branch_pattern"] == "main"
    assert ev.content["pattern"] == "github_branch_protection"
    assert ev.content["rule_state"] == "protections_present"
    assert ev.content["has_required_status_checks"] is True
    assert ev.content["has_required_pull_request_reviews"] is True
    assert ev.content["enforce_admins"] is True
    assert ev.content["required_review_count"] == 2
    assert ev.content["required_status_check_count"] == 3
    assert "protected_branch=main" in ev.content["detail"]
    assert "gap" not in ev.content


# --- should_not_match (negative-evidence emission) ----------------------------


def test_branch_protection_empty_emits_protections_absent() -> None:
    """Branch protection rule with no enforcement blocks: emit gap with
    description that explicitly notes the 'rule declared but enforces
    nothing' shape."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "branch_protection_empty.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "weak"
    assert ev.content["protected_branch_pattern"] == "release/*"
    assert ev.content["rule_state"] == "protections_absent"
    assert ev.content["has_required_status_checks"] is False
    assert ev.content["has_required_pull_request_reviews"] is False
    assert ev.content["enforce_admins"] is False
    assert ev.content["required_review_count"] == 0
    assert ev.content["required_status_check_count"] == 0
    assert "no enforcement" in ev.content["gap"]
    assert "no actual merge-time gate" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_only_enforce_admins_true_still_emits_protections_present() -> None:
    """A rule with ONLY enforce_admins=true (no review/status_check
    blocks) is still protections_present -- enforce_admins enforces
    the rule against admins, which is meaningful."""
    rule = TerraformResource(
        type="github_branch_protection",
        name="admins_only",
        kind="resource",
        body={"pattern": "main", "enforce_admins": True},
        source_ref=SourceRef(file="admins.tf", line_start=1, line_end=5),
    )
    results = detect([rule])
    assert len(results) == 1
    assert results[0].content["rule_state"] == "protections_present"
    assert results[0].content["enforce_admins"] is True
    assert results[0].content["has_required_status_checks"] is False
    assert results[0].content["has_required_pull_request_reviews"] is False


def test_pattern_falls_back_when_omitted() -> None:
    """If `pattern` is omitted (Terraform would reject; defensive
    branch), the detector reports a placeholder."""
    rule = TerraformResource(
        type="github_branch_protection",
        name="no_pattern",
        kind="resource",
        body={"required_pull_request_reviews": {"required_approving_review_count": 1}},
        source_ref=SourceRef(file="nopattern.tf", line_start=1, line_end=4),
    )
    results = detect([rule])
    assert len(results) == 1
    assert results[0].content["protected_branch_pattern"] == "(no pattern declared)"
    assert results[0].content["rule_state"] == "protections_present"
    assert results[0].content["required_review_count"] == 1


def test_non_branch_protection_resources_emit_no_evidence() -> None:
    """Detector ignores resource types other than github_branch_protection
    (e.g., github_repository, github_team)."""
    other = TerraformResource(
        type="github_repository",
        name="this",
        kind="resource",
        body={"name": "my-repo", "visibility": "private"},
        source_ref=SourceRef(file="other.tf", line_start=1, line_end=5),
    )
    assert detect([other]) == []


def test_mixed_branch_protection_rules_each_emits_correct_evidence() -> None:
    """Multiple github_branch_protection resources with mixed enforcement
    postures: each gets its own evidence record."""
    enforced = TerraformResource(
        type="github_branch_protection",
        name="main",
        kind="resource",
        body={
            "pattern": "main",
            "required_pull_request_reviews": [{"required_approving_review_count": 2}],
            "required_status_checks": [{"strict": True, "contexts": ["build", "test"]}],
            "enforce_admins": True,
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=15),
    )
    weak = TerraformResource(
        type="github_branch_protection",
        name="staging",
        kind="resource",
        body={"pattern": "staging"},
        source_ref=SourceRef(file="main.tf", line_start=17, line_end=20),
    )
    review_only = TerraformResource(
        type="github_branch_protection",
        name="develop",
        kind="resource",
        body={
            "pattern": "develop",
            "required_pull_request_reviews": [{"required_approving_review_count": 1}],
        },
        source_ref=SourceRef(file="main.tf", line_start=22, line_end=27),
    )
    results = detect([enforced, weak, review_only])
    assert len(results) == 3
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["main"].content["rule_state"] == "protections_present"
    assert by_name["main"].content["required_review_count"] == 2
    assert by_name["main"].content["required_status_check_count"] == 2
    assert by_name["staging"].content["rule_state"] == "protections_absent"
    assert by_name["develop"].content["rule_state"] == "protections_present"
    assert by_name["develop"].content["has_required_status_checks"] is False
    assert by_name["develop"].content["has_required_pull_request_reviews"] is True


def test_max_review_count_across_multiple_review_blocks() -> None:
    """python-hcl2 represents repeated blocks as a list: detector takes
    max review count across all blocks."""
    rule = TerraformResource(
        type="github_branch_protection",
        name="multi_review",
        kind="resource",
        body={
            "pattern": "main",
            "required_pull_request_reviews": [
                {"required_approving_review_count": 1},
                {"required_approving_review_count": 3},
            ],
        },
        source_ref=SourceRef(file="multi.tf", line_start=1, line_end=10),
    )
    results = detect([rule])
    assert len(results) == 1
    assert results[0].content["required_review_count"] == 3
