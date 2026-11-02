"""Tests for platform argument normalization."""

import pytest

from agentic_devtools.skill_injector_planning import _normalize_platform_arg


def test_none_is_unresolved() -> None:
    assert _normalize_platform_arg(None, "issue_adapter", frozenset({"jira"})) is None


def test_empty_and_whitespace_values_are_unresolved() -> None:
    valid = frozenset({"jira"})

    assert _normalize_platform_arg("", "issue_adapter", valid) is None
    assert _normalize_platform_arg("  ", "issue_adapter", valid) is None


def test_unknown_value_warns_and_is_unresolved() -> None:
    with pytest.warns(RuntimeWarning, match="unknown issue_adapter value"):
        assert _normalize_platform_arg("other", "issue_adapter", frozenset({"jira"})) is None


def test_valid_value_is_stripped() -> None:
    assert _normalize_platform_arg(" jira ", "issue_adapter", frozenset({"jira"})) == "jira"
