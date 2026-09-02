"""Tests for BASE_REQUIRED_PROPERTIES constant."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.template_placeholders import (
    BASE_REQUIRED_PROPERTIES,
)


class TestBaseRequiredProperties:
    """Tests for the base required property set."""

    def test_contains_title_and_description(self) -> None:
        """The base required set includes title and description."""
        assert BASE_REQUIRED_PROPERTIES == frozenset({"title", "description"})

    def test_is_frozenset(self) -> None:
        """The base required set is an immutable frozenset."""
        assert isinstance(BASE_REQUIRED_PROPERTIES, frozenset)
