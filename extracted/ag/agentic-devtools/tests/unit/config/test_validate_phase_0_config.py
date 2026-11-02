"""Tests for agentic_devtools.config.validate_phase_0_config."""

import pytest

from agentic_devtools.config import validate_phase_0_config


class TestValidatePhase0Config:
    """Tests for the public validate_phase_0_config wrapper."""

    def test_returns_defaults_for_empty_dict(self) -> None:
        """Returns safe defaults when given empty dict."""
        result = validate_phase_0_config({})
        assert result["enabled"] is False
        assert result["sync_back_on_merge"] is False
        assert result["sync_back_fields"] == ["comment"]

    def test_preserves_valid_values(self) -> None:
        """Preserves explicitly set valid values."""
        result = validate_phase_0_config(
            {"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["comment", "label"]}
        )
        assert result["enabled"] is True
        assert result["sync_back_on_merge"] is True
        assert result["sync_back_fields"] == ["comment", "label"]

    def test_raises_on_invalid_fields_when_active(self) -> None:
        """Raises ValueError on invalid sync_back_fields when both gates active."""
        with pytest.raises(ValueError, match="Unknown sync_back_fields"):
            validate_phase_0_config({"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["invalid"]})

    def test_delegates_to_private_validate(self) -> None:
        """Public wrapper delegates to _validate_phase_0."""
        from agentic_devtools.config import _validate_phase_0

        raw: dict[str, object] = {"enabled": True, "sync_back_on_merge": False}
        assert validate_phase_0_config(raw) == _validate_phase_0(raw)

    def test_accepts_non_dict_values(self) -> None:
        """Accepts non-dict inputs and normalizes them via the private validator."""
        assert validate_phase_0_config(None) == {
            "enabled": False,
            "sync_back_on_merge": False,
            "sync_back_fields": ["comment"],
        }
