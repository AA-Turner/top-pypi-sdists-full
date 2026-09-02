"""Tests for normalize_property_entries in speckit/phase0/observability.py (FR-001)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.observability import normalize_property_entries


class TestNormalizePropertyEntries:
    """Tests for the normalize_property_entries function."""

    def test_none_returns_empty_list(self) -> None:
        assert normalize_property_entries(None) == []

    def test_empty_list_returns_empty_list(self) -> None:
        assert normalize_property_entries([]) == []

    def test_sorts_by_ascending_utf8_order(self) -> None:
        entries = [
            {"name": "zeta", "templateSection": "s1"},
            {"name": "alpha", "templateSection": "s2"},
        ]
        result = normalize_property_entries(entries)
        assert [entry["name"] for entry in result] == ["alpha", "zeta"]

    def test_deduplicates_keeping_first_occurrence(self) -> None:
        entries = [
            {"name": "dup", "templateSection": "first"},
            {"name": "dup", "templateSection": "second"},
        ]
        result = normalize_property_entries(entries)
        assert result == [{"name": "dup", "templateSection": "first"}]

    def test_supports_custom_name_key(self) -> None:
        entries = [{"name": "b", "reason": "y"}, {"name": "a", "reason": "x"}]
        result = normalize_property_entries(entries, name_key="name")
        assert [entry["name"] for entry in result] == ["a", "b"]

    def test_value_key_whitelists_to_two_keys_only(self) -> None:
        entries = [{"name": "p", "templateSection": "s1", "extra_key": "should-be-dropped"}]
        result = normalize_property_entries(entries, value_key="templateSection")
        assert result == [{"name": "p", "templateSection": "s1"}]
        assert "extra_key" not in result[0]

    def test_value_key_redacts_secret_in_value_field(self) -> None:
        _FAKE = "".join(["fake", "secret", "val123"])
        entries = [{"name": "header", "reason": f"secret={_FAKE}"}]
        result = normalize_property_entries(entries, value_key="reason")
        assert _FAKE not in result[0]["reason"]
        assert "[REDACTED]" in result[0]["reason"]

    def test_value_key_missing_value_field_raises(self) -> None:
        with pytest.raises(ValueError, match="templateSection"):
            normalize_property_entries([{"name": "p"}], value_key="templateSection")

    def test_value_key_rejects_empty_name(self) -> None:
        with pytest.raises(ValueError, match="name"):
            normalize_property_entries([{"name": "", "templateSection": "s1"}], value_key="templateSection")

    def test_value_key_rejects_non_string_value(self) -> None:
        with pytest.raises(ValueError, match="templateSection"):
            normalize_property_entries(
                [{"name": "p", "templateSection": None}],  # type: ignore[dict-item]
                value_key="templateSection",
            )

    def test_rejects_non_dict_entry(self) -> None:
        with pytest.raises(ValueError, match="dict"):
            normalize_property_entries(["not-a-dict"])  # type: ignore[list-item]

    def test_sanitizes_control_characters_in_name(self) -> None:
        entries = [{"name": "prop\u0000name", "templateSection": "s1"}]
        result = normalize_property_entries(entries)
        assert "\u0000" not in result[0]["name"]
        assert "\ufffd" in result[0]["name"]

    def test_redacts_secret_in_name(self) -> None:
        _FAKE = "".join(["fake", "secret", "val123"])
        entries = [{"name": f"token={_FAKE}", "templateSection": "s1"}]
        result = normalize_property_entries(entries)
        assert _FAKE not in result[0]["name"]
        assert "[REDACTED]" in result[0]["name"]
