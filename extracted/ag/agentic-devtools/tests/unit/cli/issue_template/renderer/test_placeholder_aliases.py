"""Tests for _PLACEHOLDER_ALIASES constant in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _PLACEHOLDER_ALIASES


class TestPlaceholderAliases:
    """Tests for the _PLACEHOLDER_ALIASES constant (FR-003, FR-004)."""

    def test_issue_id_alias_maps_to_id(self) -> None:
        """The alias 'issue_id' maps to canonical name 'id'."""
        assert _PLACEHOLDER_ALIASES["issue_id"] == "id"

    def test_only_one_alias_defined(self) -> None:
        """Only one alias pair is defined per spec."""
        assert len(_PLACEHOLDER_ALIASES) == 1

    def test_alias_mapping_is_dict(self) -> None:
        """The alias mapping is a plain dict."""
        assert isinstance(_PLACEHOLDER_ALIASES, dict)
