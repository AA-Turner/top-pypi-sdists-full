"""Tests for normalize_missing_properties in speckit/phase0/observability.py (FR-001)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.observability import normalize_missing_properties


class TestNormalizeMissingProperties:
    """Tests for the normalize_missing_properties function."""

    def test_none_returns_empty_list(self) -> None:
        assert normalize_missing_properties(None) == []

    def test_empty_list_returns_empty_list(self) -> None:
        assert normalize_missing_properties([]) == []

    def test_sorts_ascending_utf8_order(self) -> None:
        assert normalize_missing_properties(["zeta", "alpha", "mu"]) == ["alpha", "mu", "zeta"]

    def test_deduplicates_values(self) -> None:
        assert normalize_missing_properties(["a", "b", "a"]) == ["a", "b"]

    def test_rejects_empty_property_name(self) -> None:
        with pytest.raises(ValueError, match="missingProperties"):
            normalize_missing_properties([""])

    def test_rejects_non_string_value(self) -> None:
        with pytest.raises(ValueError, match="missingProperties"):
            normalize_missing_properties(["ok", None])  # type: ignore[list-item]

    def test_sanitizes_control_characters_in_name(self) -> None:
        result = normalize_missing_properties(["prop\u0000name"])
        assert "\u0000" not in result[0]
        assert "\ufffd" in result[0]

    def test_redacts_secret_in_name(self) -> None:
        _FAKE = "".join(["fake", "secret", "val123"])
        result = normalize_missing_properties([f"token={_FAKE}"])
        assert _FAKE not in result[0]
        assert "[REDACTED]" in result[0]
