"""Tests for ``_coerce_decimal``."""

from decimal import Decimal

import pytest

from agentic_devtools.cli.config.project_config import _coerce_decimal


class TestCoerceDecimal:
    """Tests for strict Decimal coercion."""

    def test_int_is_accepted(self):
        assert _coerce_decimal(3, field_name="x") == Decimal("3")

    def test_float_is_accepted(self):
        assert _coerce_decimal(1.5, field_name="x") == Decimal("1.5")

    def test_str_is_accepted(self):
        assert _coerce_decimal("2.5", field_name="x") == Decimal("2.5")

    def test_finite_decimal_is_returned_unchanged(self):
        assert _coerce_decimal(Decimal("2.5"), field_name="x") == Decimal("2.5")

    def test_decimal_nan_is_rejected(self):
        with pytest.raises(ValueError, match="must be finite"):
            _coerce_decimal(Decimal("NaN"), field_name="x")

    def test_decimal_infinity_is_rejected(self):
        with pytest.raises(ValueError, match="must be finite"):
            _coerce_decimal(Decimal("Infinity"), field_name="x")

    def test_float_nan_is_rejected(self):
        with pytest.raises(ValueError, match="must be finite"):
            _coerce_decimal(float("nan"), field_name="x")

    def test_float_inf_is_rejected(self):
        with pytest.raises(ValueError, match="must be finite"):
            _coerce_decimal(float("inf"), field_name="x")

    def test_boolean_is_rejected(self):
        with pytest.raises(ValueError, match="not boolean"):
            _coerce_decimal(True, field_name="x")

    def test_non_numeric_type_is_rejected(self):
        with pytest.raises(ValueError, match="must be numeric"):
            _coerce_decimal(object(), field_name="x")
