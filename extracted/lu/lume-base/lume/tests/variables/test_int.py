import warnings

import numpy as np
import pytest

from lume.variables.int import IntVariable


class TestIntVariable:
    """Test IntVariable creation and validation."""

    def test_value_range_validation(self):
        with pytest.raises(ValueError, match="Minimum value.*must be lower or equal"):
            IntVariable(name="test", value_range=(10, 5))

    def test_value_range_equal_bounds_allowed(self):
        var = IntVariable(name="test", value_range=(5, 5))
        assert var.value_range == (5, 5)

    def test_default_value_must_be_in_range(self):
        with pytest.raises(ValueError, match="out of valid range"):
            IntVariable(name="test", default_value=15, value_range=(0, 10))

    def test_validate_int_types(self):
        var = IntVariable(name="test")
        var.validate_value(5)
        var.validate_value(np.int32(5))
        var.validate_value(np.int64(5))

    def test_reject_non_int_types(self):
        var = IntVariable(name="test")
        for invalid in [5.0, "5", True, [5], None]:
            with pytest.raises(TypeError, match="Expected value to be of type"):
                var.validate_value(invalid)

    def test_range_validation_with_config(self):
        var = IntVariable(name="test", value_range=(0, 10))

        var.validate_value(5, config="error")
        var.validate_value(15, config="none")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            var.validate_value(15, config="warn")
            assert len(w) == 1
            assert "out of valid range" in str(w[0].message)

        with pytest.raises(ValueError, match="out of valid range"):
            var.validate_value(15, config="error")

    def test_range_validation_inclusive_bounds(self):
        var = IntVariable(name="test", value_range=(0, 10))
        var.validate_value(0, config="error")
        var.validate_value(10, config="error")
