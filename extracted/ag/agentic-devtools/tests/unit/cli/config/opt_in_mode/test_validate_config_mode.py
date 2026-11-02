"""Tests for validate_config_mode()."""

from agentic_devtools.cli.config.opt_in_mode import validate_config_mode


class TestValidateConfigMode:
    """Tests for validate_config_mode function."""

    def test_auto_is_valid(self) -> None:
        """'auto' returns None (valid)."""
        assert validate_config_mode("auto") is None

    def test_manual_is_valid(self) -> None:
        """'manual' returns None (valid)."""
        assert validate_config_mode("manual") is None

    def test_invalid_value_returns_error(self) -> None:
        """Invalid value returns error message."""
        result = validate_config_mode("invalid")
        assert result is not None
        assert "Invalid config_mode" in result
        assert "'invalid'" in result
        assert "'auto'" in result
        assert "'manual'" in result

    def test_empty_string_is_invalid(self) -> None:
        """Empty string is invalid."""
        result = validate_config_mode("")
        assert result is not None
        assert "Invalid config_mode" in result

    def test_uppercase_is_invalid(self) -> None:
        """Uppercase variants are invalid (case-sensitive)."""
        assert validate_config_mode("Auto") is not None
        assert validate_config_mode("MANUAL") is not None
