"""Tests for _coerce_id."""

from agentic_devtools.cli.azure_devops.consolidated_scaffold import _coerce_id


class TestCoerceId:
    """Coercion of API-returned comment ids to positive ints."""

    def test_positive_int(self):
        assert _coerce_id(7) == 7

    def test_numeric_string(self):
        assert _coerce_id("12") == 12

    def test_none_is_zero(self):
        assert _coerce_id(None) == 0

    def test_non_numeric_is_zero(self):
        assert _coerce_id("abc") == 0

    def test_zero_and_negative_are_zero(self):
        assert _coerce_id(0) == 0
        assert _coerce_id(-3) == 0
