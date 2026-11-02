"""Tests for truncate_summary utility."""

import json

from agentic_devtools.orchestration.observability_truncation import truncate_summary


class TestTruncateSummary:
    """Tests for the truncate_summary function."""

    def test_none_input_returns_none(self) -> None:
        assert truncate_summary(None) is None

    def test_short_string_unchanged(self) -> None:
        result = truncate_summary("hello world")
        assert result == "hello world"

    def test_short_dict_unchanged(self) -> None:
        data = {"key": "value"}
        result = truncate_summary(data)
        assert result == data

    def test_long_string_truncated_with_suffix(self) -> None:
        data = "x" * 3000
        result = truncate_summary(data, max_chars=100)
        assert isinstance(result, str)
        assert "… [" in result
        assert "chars omitted]" in result
        assert len(result) <= 100

    def test_long_dict_truncated(self) -> None:
        data = {"key": "v" * 3000}
        result = truncate_summary(data, max_chars=100)
        assert isinstance(result, str)
        assert "… [" in result

    def test_deterministic_output(self) -> None:
        data = "a" * 5000
        result1 = truncate_summary(data, max_chars=200)
        result2 = truncate_summary(data, max_chars=200)
        assert result1 == result2

    def test_suffix_contains_correct_omitted_count(self) -> None:
        data = "x" * 3000
        result = truncate_summary(data, max_chars=2000)
        # suffix = "… [NNNN chars omitted]" (22 chars); cut_at = 2000 - 22 = 1978
        # actual chars omitted = 3000 - 1978 = 1022 (not 1000, which ignores suffix budget)
        assert "1022 chars omitted" in result

    def test_suffix_correct_at_digit_count_boundary(self) -> None:
        """Omitted count crossing a power-of-10 digit boundary converges correctly."""
        # initial_omitted = 1999 - 1000 = 999 (3 digits); after accounting for the
        # suffix budget, cut_at shifts and true omitted becomes 1021 (4 digits).
        data = "x" * 1999
        result = truncate_summary(data, max_chars=1000)
        assert len(result) == 1000
        # suffix for 1021 omitted = "… [1021 chars omitted]" (22 chars)
        # cut_at = 1000 - 22 = 978; omitted = 1999 - 978 = 1021
        assert "1021 chars omitted" in result

    def test_list_input_truncated(self) -> None:
        data = list(range(1000))
        result = truncate_summary(data, max_chars=50)
        assert isinstance(result, str)
        assert "… [" in result

    def test_custom_max_chars(self) -> None:
        data = "a" * 500
        result = truncate_summary(data, max_chars=100)
        assert len(result) <= 100

    def test_exact_boundary_not_truncated(self) -> None:
        data = "a" * 2000
        result = truncate_summary(data, max_chars=2000)
        assert result == data

    def test_one_over_boundary_truncated(self) -> None:
        data = "a" * 2001
        result = truncate_summary(data, max_chars=2000)
        assert "… [" in result

    def test_non_serializable_dict_uses_repr(self) -> None:
        """Dict that causes json.dumps TypeError falls back to repr."""

        class Unserializable:
            def __repr__(self) -> str:
                return "Unserializable()"

        # json.dumps with default=str won't raise TypeError for most objects,
        # but a dict with a key that can't be serialized as a JSON key will
        # We need to trigger the except (TypeError, ValueError) branch
        # Use a custom object that makes json.dumps fail
        from unittest.mock import patch

        data = {"key": "value"}
        with patch("json.dumps", side_effect=TypeError("not serializable")):
            result = truncate_summary(data, max_chars=5)
        assert isinstance(result, str)

    def test_non_serializable_dict_within_budget_returns_repr_string(self) -> None:
        """Fallback repr output stays JSON-safe even when truncation is unnecessary."""
        data = {(1, 2): "value"}
        result = truncate_summary(data, max_chars=100)
        assert isinstance(result, str)
        assert result == repr(data)
        assert json.loads(json.dumps({"summary": result})) == {"summary": repr(data)}

    def test_non_dict_non_list_non_str_uses_str(self) -> None:
        """Non-string, non-dict, non-list data always returns str() representation."""
        result = truncate_summary(42)
        assert result == "42"  # str() form returned, not original int

    def test_non_json_serializable_non_dict_list_returns_str(self) -> None:
        """A set (non-JSON-serializable) within budget returns str(), never original."""
        data: set[int] = {1, 2, 3}
        result = truncate_summary(data, max_chars=2000)
        assert isinstance(result, str)
        assert result == str(data)

    def test_non_dict_non_list_non_str_truncated(self) -> None:
        """Non-string, non-dict, non-list data that exceeds budget is truncated."""

        # A number that when str()'d is short won't trigger truncation
        # Use an object with a long repr
        class LongRepr:
            def __str__(self) -> str:
                return "x" * 5000

        result = truncate_summary(LongRepr(), max_chars=100)
        assert isinstance(result, str)
        assert "… [" in result

    def test_very_small_max_chars_cut_at_zero(self) -> None:
        """Very small budgets still respect max_chars and signal truncation."""
        data = "a" * 100
        result = truncate_summary(data, max_chars=5)
        assert isinstance(result, str)
        assert len(result) <= 5
        assert result.endswith("…")

    def test_single_character_budget_returns_ellipsis(self) -> None:
        result = truncate_summary("a" * 100, max_chars=1)
        assert result == "…"

    def test_non_positive_budget_returns_empty_string(self) -> None:
        result = truncate_summary("a" * 100, max_chars=0)
        assert result == ""
