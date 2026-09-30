"""math operands accept human-formatted numbers ("3,000").

Captured page text routinely carries thousands separators. `_as_number` was a
bare `float(value.strip())`, so a captured "3,000" raised ValueError and the
whole math step failed.

Port of V2 (CommonParser.safe_float).
"""
import pytest

from testmu_selenium._helpers.math import _as_number, _safe_float


class TestSafeFloat:
    @pytest.mark.parametrize("raw,expected", [
        ("3,000", 3000.0),
        ("1,234,567", 1234567.0),
        ("1,200.50", 1200.5),
        ("  2,500  ", 2500.0),   # surrounding whitespace still tolerated
        ("42", 42.0),            # no separator - unchanged
        ("3.14", 3.14),
        ("-1,500", -1500.0),
        ("0", 0.0),
    ])
    def test_parses_grouped_numbers(self, raw, expected):
        assert _safe_float(raw) == expected

    @pytest.mark.parametrize("raw", ["abc", "", "1,2,a", "$1,200.50", "12%"])
    def test_raises_on_genuinely_non_numeric(self, raw):
        # Parity note: the source fix strips commas only. Currency symbols and
        # percent signs are still non-numeric and must keep raising rather than
        # silently parsing to a wrong number.
        with pytest.raises(ValueError):
            _safe_float(raw)


class TestAsNumber:
    def test_grouped_string_no_longer_fails_the_step(self):
        assert _as_number("3,000") == 3000.0

    def test_plain_numeric_string_unchanged(self):
        assert _as_number("42") == 42.0

    def test_numbers_pass_through(self):
        assert _as_number(7) == 7.0
        assert _as_number(2.5) == 2.5

    def test_non_numeric_still_raises_the_operand_error(self):
        with pytest.raises(ValueError, match="Non-numeric operand encountered"):
            _as_number("not a number")

    def test_unsupported_type_still_raises(self):
        with pytest.raises(ValueError, match="Unsupported operand type"):
            _as_number({"a": 1})
