import numpy as np
import pytest

from lume.variables.bool import BoolVariable


class TestBoolVariable:
    """Test BoolVariable creation and validation."""

    def test_default_value_validated(self):
        var = BoolVariable(name="test", default_value=True)
        assert var.default_value is True

    def test_validate_bool_types(self):
        var = BoolVariable(name="test")
        var.validate_value(True)
        var.validate_value(False)
        var.validate_value(np.bool_(True))

    def test_reject_non_bool_types(self):
        var = BoolVariable(name="test")
        for invalid in [1, 0, "true", None, [True]]:
            with pytest.raises(TypeError, match="Expected value to be of type"):
                var.validate_value(invalid)
