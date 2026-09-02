"""Tests for coerce_token_count helper."""

from agentic_devtools.orchestration.observability_pricing import coerce_token_count


class TestCoerceTokenCount:
    """Tests for coerce_token_count function."""

    def test_none_returns_none(self) -> None:
        assert coerce_token_count(None) is None

    def test_int_returned_unchanged(self) -> None:
        assert coerce_token_count(1000) == 1000

    def test_zero_int_returned(self) -> None:
        assert coerce_token_count(0) == 0

    def test_float_coerced_to_int(self) -> None:
        assert coerce_token_count(1000.7) == 1000

    def test_numeric_string_coerced(self) -> None:
        assert coerce_token_count("500") == 500

    def test_float_string_coerced(self) -> None:
        assert coerce_token_count("250.9") == 250

    def test_bool_true_returns_none(self) -> None:
        """True is a bool (subclass of int) and must not be treated as 1."""
        assert coerce_token_count(True) is None

    def test_bool_false_returns_none(self) -> None:
        """False is a bool (subclass of int) and must not be treated as 0."""
        assert coerce_token_count(False) is None

    def test_non_numeric_string_returns_none(self) -> None:
        assert coerce_token_count("not-a-number") is None

    def test_empty_string_returns_none(self) -> None:
        assert coerce_token_count("") is None

    def test_list_returns_none(self) -> None:
        assert coerce_token_count([1, 2, 3]) is None

    def test_dict_returns_none(self) -> None:
        assert coerce_token_count({"tokens": 100}) is None

    def test_negative_int_returns_none(self) -> None:
        """Negative token counts are not valid and must return None."""
        assert coerce_token_count(-1) is None

    def test_negative_float_returns_none(self) -> None:
        """Negative float token counts are not valid and must return None."""
        assert coerce_token_count(-0.5) is None

    def test_negative_string_returns_none(self) -> None:
        """Negative numeric string token counts must return None."""
        assert coerce_token_count("-100") is None

    def test_infinity_returns_none(self) -> None:
        """float('inf') triggers OverflowError in int() and must return None."""
        assert coerce_token_count(float("inf")) is None

    def test_negative_infinity_returns_none(self) -> None:
        """float('-inf') triggers OverflowError in int() and must return None."""
        assert coerce_token_count(float("-inf")) is None

    def test_infinity_string_returns_none(self) -> None:
        """'inf' string coerces to float('inf'), which overflows to int."""
        assert coerce_token_count("inf") is None
