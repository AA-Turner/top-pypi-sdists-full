"""Tests for PLACEHOLDER_ALIASES constant."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.template_placeholders import PLACEHOLDER_ALIASES


class TestPlaceholderAliases:
    """Tests for the placeholder alias mapping."""

    def test_is_mapping(self) -> None:
        """Aliases map placeholder names to canonical property names."""
        assert isinstance(PLACEHOLDER_ALIASES, dict)

    def test_values_are_strings(self) -> None:
        """Every alias resolves to a string canonical name."""
        assert all(isinstance(v, str) for v in PLACEHOLDER_ALIASES.values())
