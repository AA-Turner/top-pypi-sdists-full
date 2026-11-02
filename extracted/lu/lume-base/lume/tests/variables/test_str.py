import warnings

import pytest

from lume.variables.str import StrVariable


class TestStrVariable:
    """Test StrVariable creation and validation."""

    def test_length_bounds_negative_rejected(self):
        with pytest.raises(ValueError):
            StrVariable(name="test", min_length=-1)
        with pytest.raises(ValueError):
            StrVariable(name="test", max_length=-1)

    def test_min_greater_than_max_rejected(self):
        with pytest.raises(ValueError, match="min_length.*max_length"):
            StrVariable(name="test", min_length=5, max_length=3)

    def test_default_value_must_satisfy_constraints(self):
        with pytest.raises(ValueError):
            StrVariable(name="test", default_value="hi", min_length=5)
        with pytest.raises(ValueError):
            StrVariable(name="test", default_value="hello world", max_length=5)
        with pytest.raises(ValueError):
            StrVariable(name="test", default_value="abc", regex=r"\d+")

    def test_validate_str_type(self):
        var = StrVariable(name="test")
        var.validate_value("hello")

    def test_reject_non_str_types(self):
        var = StrVariable(name="test")
        for invalid in [5, 5.0, True, None, ["hello"]]:
            with pytest.raises(TypeError, match="Expected value to be of type"):
                var.validate_value(invalid)

    def test_length_validation_with_config(self):
        var = StrVariable(name="test", min_length=3, max_length=6)

        var.validate_value("hello", config="error")
        var.validate_value("hi", config="none")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            var.validate_value("hi", config="warn")
            assert len(w) == 1
            assert "min_length" in str(w[0].message)

        with pytest.raises(ValueError, match="min_length"):
            var.validate_value("hi", config="error")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            var.validate_value("toolongstring", config="warn")
            assert len(w) == 1
            assert "max_length" in str(w[0].message)

        with pytest.raises(ValueError, match="max_length"):
            var.validate_value("toolongstring", config="error")

    def test_length_validation_inclusive_bounds(self):
        var = StrVariable(name="test", min_length=3, max_length=5)
        var.validate_value("abc", config="error")
        var.validate_value("abcde", config="error")

    def test_regex_validation_with_config(self):
        var = StrVariable(name="test", regex=r"\d{3}-\d{4}")

        var.validate_value("123-4567", config="error")
        var.validate_value("bad", config="none")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            var.validate_value("bad", config="warn")
            assert len(w) == 1
            assert "pattern" in str(w[0].message)

        with pytest.raises(ValueError, match="pattern"):
            var.validate_value("bad", config="error")

    def test_regex_requires_full_match(self):
        var = StrVariable(name="test", regex=r"\d+")
        var.validate_value("123", config="error")
        with pytest.raises(ValueError):
            var.validate_value("123abc", config="error")
