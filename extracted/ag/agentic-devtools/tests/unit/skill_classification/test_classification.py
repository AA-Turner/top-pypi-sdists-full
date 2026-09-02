"""Tests for the Classification frozen dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.skill_classification import Classification


class TestClassificationInstantiation:
    """FR-005: Classification dataclass instantiation and defaults."""

    def test_default_universal(self) -> None:
        cls = Classification()
        assert cls.requires_issue_adapter is None
        assert cls.requires_code_hosting is None
        assert cls.always is False

    def test_explicit_values(self) -> None:
        cls = Classification(
            requires_issue_adapter="jira",
            requires_code_hosting="azure_devops",
            always=True,
        )
        assert cls.requires_issue_adapter == "jira"
        assert cls.requires_code_hosting == "azure_devops"
        assert cls.always is True

    def test_partial_values(self) -> None:
        cls = Classification(requires_issue_adapter="github")
        assert cls.requires_issue_adapter == "github"
        assert cls.requires_code_hosting is None
        assert cls.always is False


class TestClassificationFrozen:
    """FR-005: Classification is immutable (frozen dataclass)."""

    def test_cannot_set_requires_issue_adapter(self) -> None:
        cls = Classification()
        with pytest.raises(AttributeError):
            cls.requires_issue_adapter = "jira"  # type: ignore[misc]

    def test_cannot_set_requires_code_hosting(self) -> None:
        cls = Classification()
        with pytest.raises(AttributeError):
            cls.requires_code_hosting = "github"  # type: ignore[misc]

    def test_cannot_set_always(self) -> None:
        cls = Classification()
        with pytest.raises(AttributeError):
            cls.always = True  # type: ignore[misc]
