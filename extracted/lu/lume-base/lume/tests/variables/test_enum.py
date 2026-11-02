import warnings

import pytest

from lume.variables.enum import EnumVariable


class TestEnumVariable:
    """Test EnumVariable creation and validation."""

    def test_options_validation_empty(self):
        with pytest.raises(ValueError, match="options must not be empty"):
            EnumVariable(name="test", options=[])

    def test_options_validation_non_list(self):
        with pytest.raises(ValueError, match="options must be a list or tuple"):
            EnumVariable(name="test", options="invalid")

    def test_options_converted_to_list(self):
        var = EnumVariable(name="test", options=("a", "b", "c"))
        assert var.options == ["a", "b", "c"]
        assert isinstance(var.options, list)

    def test_default_value_must_be_in_options(self):
        with pytest.raises(ValueError, match="not one of the allowed options"):
            EnumVariable(name="test", options=["a", "b", "c"], default_value="d")

    def test_default_value_validated(self):
        var = EnumVariable(name="test", options=["a", "b", "c"], default_value="a")
        assert var.default_value == "a"

    def test_validate_string_options(self):
        var = EnumVariable(name="test", options=["red", "green", "blue"])
        var.validate_value("red", config="error")
        var.validate_value("green", config="error")
        var.validate_value("blue", config="error")

    def test_validate_numeric_options(self):
        var = EnumVariable(name="test", options=[1, 2, 3])
        var.validate_value(1, config="error")
        var.validate_value(2, config="error")
        var.validate_value(3, config="error")

    def test_validate_mixed_type_options(self):
        var = EnumVariable(name="test", options=[1, "a", 2.5, None])
        var.validate_value(1, config="error")
        var.validate_value("a", config="error")
        var.validate_value(2.5, config="error")
        var.validate_value(None, config="error")

    def test_reject_invalid_value(self):
        var = EnumVariable(name="test", options=["a", "b", "c"])
        with pytest.raises(ValueError, match="not one of the allowed options"):
            var.validate_value("d", config="error")

    def test_validation_with_config_warn(self):
        var = EnumVariable(name="test", options=["a", "b", "c"])
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            var.validate_value("d", config="warn")
            assert len(w) == 1
            assert "not one of the allowed options" in str(w[0].message)

    def test_validation_with_config_error(self):
        var = EnumVariable(name="test", options=["a", "b", "c"])
        with pytest.raises(ValueError, match="not one of the allowed options"):
            var.validate_value("d", config="error")

    def test_validation_uses_default_config(self):
        var = EnumVariable(
            name="test", options=["a", "b", "c"], default_validation_config="warn"
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            var.validate_value("d")
            assert len(w) == 1
