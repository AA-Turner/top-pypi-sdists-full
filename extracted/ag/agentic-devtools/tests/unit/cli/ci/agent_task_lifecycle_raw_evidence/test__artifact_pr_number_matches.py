"""Tests for valid pull-artifact number aliases."""

from agentic_devtools.cli.ci.agent_task_lifecycle_raw_evidence import _artifact_pr_number_matches


def test_compares_integer_and_digit_string_pull_numbers() -> None:
    assert _artifact_pr_number_matches(42, 42)
    assert not _artifact_pr_number_matches(43, 42)
    assert _artifact_pr_number_matches("42", 42)
    assert not _artifact_pr_number_matches("43", 42)


def test_ignores_invalid_or_non_numeric_pull_number_values() -> None:
    assert _artifact_pr_number_matches(True, 42)
    assert _artifact_pr_number_matches("invalid", 42)
    assert _artifact_pr_number_matches(None, 42)
    assert _artifact_pr_number_matches("²", 42)
