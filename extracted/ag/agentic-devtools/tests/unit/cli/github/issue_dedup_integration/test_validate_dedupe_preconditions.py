"""Tests for validate_dedupe_preconditions."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.github.issue_dedup_integration import validate_dedupe_preconditions


class TestValidateDedupePreConditions:
    """Tests for validate_dedupe_preconditions."""

    def test_returns_stripped_value_for_valid_input(self) -> None:
        """Valid non-blank input returns stripped string."""
        result = validate_dedupe_preconditions("  ssl_handshake_failure  ")
        assert result == "ssl_handshake_failure"

    def test_raises_value_error_for_none(self) -> None:
        """None input raises ValueError."""
        with pytest.raises(ValueError, match="issue.error_class is required"):
            validate_dedupe_preconditions(None)

    def test_raises_value_error_for_empty_string(self) -> None:
        """Empty string raises ValueError."""
        with pytest.raises(ValueError, match="must not be blank"):
            validate_dedupe_preconditions("")

    def test_raises_value_error_for_whitespace_only(self) -> None:
        """Whitespace-only string raises ValueError."""
        with pytest.raises(ValueError, match="must not be blank"):
            validate_dedupe_preconditions("   \t\n  ")

    def test_preserves_internal_whitespace(self) -> None:
        """Internal whitespace is preserved (only leading/trailing stripped)."""
        result = validate_dedupe_preconditions("  error class name  ")
        assert result == "error class name"

    def test_raises_value_error_for_integer(self) -> None:
        """Integer input raises ValueError instead of AttributeError."""
        with pytest.raises(ValueError, match="must be a string.*got 'int'"):
            validate_dedupe_preconditions(42)  # type: ignore[arg-type]

    def test_raises_value_error_for_list(self) -> None:
        """List input raises ValueError instead of AttributeError."""
        with pytest.raises(ValueError, match="must be a string.*got 'list'"):
            validate_dedupe_preconditions(["ssl_error"])  # type: ignore[arg-type]
