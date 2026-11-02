"""Tests for ``_derive_speckit_base_branch``."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.commands import _derive_speckit_base_branch


@pytest.mark.parametrize(
    ("phase", "hierarchy_level", "issue_number", "expected"),
    [
        (1, "feature", 10, "main"),
        (1, "epic", 10, "main"),
        (1, "task", 10, "main"),
        (2, "feature", 10, "speckit/10/phase-1-specify"),
        (2, "epic", 10, "speckit/10/phase-1-specify"),
        (2, "task", 10, "speckit/10/phase-1-specify"),
        (3, "feature", 10, "speckit/10/phase-2-clarify"),
        (3, "epic", 10, "speckit/10/phase-2-clarify"),
        (3, "task", 10, "main"),
    ],
)
def test__derive_speckit_base_branch(phase: int, hierarchy_level: str, issue_number: int, expected: str) -> None:
    assert (
        _derive_speckit_base_branch(phase=phase, hierarchy_level=hierarchy_level, issue_number=issue_number) == expected
    )
