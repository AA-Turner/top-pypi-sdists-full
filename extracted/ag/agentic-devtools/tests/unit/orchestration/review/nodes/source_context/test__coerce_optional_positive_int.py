"""Tests for _coerce_optional_positive_int helper."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.source_context import _coerce_optional_positive_int


class TestCoerceOptionalPositiveInt:
    """Tests for _coerce_optional_positive_int."""

    def test_positive_int_accepted(self) -> None:
        """Positive integers are returned as-is."""
        assert _coerce_optional_positive_int(7) == 7
        assert _coerce_optional_positive_int("7") == 7

    def test_zero_normalized_to_none(self) -> None:
        """Zero is normalized to None."""
        assert _coerce_optional_positive_int(0) is None

    def test_negative_normalized_to_none(self) -> None:
        """Negative values are normalized to None."""
        assert _coerce_optional_positive_int(-1) is None

    def test_none_returns_none(self) -> None:
        """None input returns None."""
        assert _coerce_optional_positive_int(None) is None

    def test_non_numeric_returns_none(self) -> None:
        """Non-numeric strings return None."""
        assert _coerce_optional_positive_int("abc") is None
