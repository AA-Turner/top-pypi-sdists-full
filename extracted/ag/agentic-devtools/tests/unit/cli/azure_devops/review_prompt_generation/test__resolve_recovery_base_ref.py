"""Tests for _resolve_recovery_base_ref."""

from agentic_devtools.cli.azure_devops.review_prompt_generation import _resolve_recovery_base_ref


def test_prefers_persisted_branch_diff_ref() -> None:
    assert _resolve_recovery_base_ref({}, "origin/release") == "origin/release"


def test_derives_origin_base_from_pr_details() -> None:
    assert _resolve_recovery_base_ref({"comparison": {"baseBranch": "release"}}, None) == "origin/release"
