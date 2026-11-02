"""Tests for the immutable hierarchy resolution result."""

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import Resolution


def test_default_success_and_immutable_contract() -> None:
    result = Resolution("feature", "specs/42-feature", "", "", "task-without-parent")
    assert result.exit_code == 0
    assert result.hierarchy_level == "feature"
    assert result.spec_dir == "specs/42-feature"
    assert result.spec_context == result.parent_number == ""
    assert result.reason == "task-without-parent"
    with pytest.raises(FrozenInstanceError):
        setattr(result, "hierarchy_level", "task")


def test_explicit_failure_status() -> None:
    result = Resolution("blocked", "", "", "10", "parent-spec-missing", 3)
    assert result.exit_code == 3
    assert result.parent_number == "10"
