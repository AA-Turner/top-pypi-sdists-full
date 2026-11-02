"""Tests for SpecKit Cloud Agent base-branch derivation."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.cloud_agent_guard import derive_speckit_base_branch


@pytest.mark.parametrize(
    ("phase", "hierarchy_level", "issue_number", "expected"),
    [
        (1, "feature", 7, "main"),
        (2, "feature", 7, "speckit/7/phase-1-specify"),
        (3, "feature", 7, "speckit/7/phase-2-clarify"),
        (3, "epic", 7, "speckit/7/phase-2-clarify"),
        (3, "task", 7, "main"),
    ],
)
def test_derives_expected_base_branch(phase: int, hierarchy_level: str, issue_number: int, expected: str) -> None:
    assert derive_speckit_base_branch(phase, hierarchy_level, issue_number) == expected


def test_rejects_invalid_phase() -> None:
    with pytest.raises(ValueError, match="phase"):
        derive_speckit_base_branch(4, "feature", 7)


def test_rejects_invalid_issue_number() -> None:
    with pytest.raises(ValueError, match="issue_number"):
        derive_speckit_base_branch(1, "feature", 0)


def test_rejects_invalid_hierarchy_level() -> None:
    with pytest.raises(ValueError, match="hierarchy_level"):
        derive_speckit_base_branch(3, "invalid", 7)
