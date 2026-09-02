"""Tests for the ``Violation`` result dataclass."""

from __future__ import annotations

import dataclasses

import pytest

from agentic_devtools.cli.checks.customization_quality import Violation


class TestViolation:
    def test_stores_rule_path_and_message(self) -> None:
        """A violation keeps the rule id, the file it applies to, and the reason."""
        violation = Violation("Q9", ".agents/skills/demo/SKILL.md", "too much emphasis")

        assert violation.rule == "Q9"
        assert violation.path == ".agents/skills/demo/SKILL.md"
        assert violation.message == "too much emphasis"

    def test_is_frozen(self) -> None:
        """Violations are immutable so callers cannot rewrite a finding."""
        violation = Violation("Q1", "a.md", "missing description")

        with pytest.raises(dataclasses.FrozenInstanceError):
            violation.rule = "Q2"  # type: ignore[misc]
