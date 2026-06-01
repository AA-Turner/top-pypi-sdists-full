"""Tests for ``smplkit.management.types`` (Color, EnvironmentClassification)."""

from __future__ import annotations

import pytest

from smplkit.management.types import Color


class TestColor:
    def test_six_digit_hex(self):
        c = Color("#ef4444")
        assert c.hex == "#ef4444"

    def test_three_digit_hex(self):
        c = Color("#fff")
        assert c.hex == "#fff"

    def test_eight_digit_hex_with_alpha(self):
        c = Color("#ef4444aa")
        assert c.hex == "#ef4444aa"

    def test_normalizes_to_lowercase(self):
        assert Color("#EF4444").hex == "#ef4444"

    def test_str_returns_hex(self):
        assert str(Color("#ef4444")) == "#ef4444"

    def test_equality(self):
        assert Color("#ef4444") == Color("#EF4444")  # case-insensitive
        assert Color("#ef4444") != Color("#ef4445")

    def test_hashable(self):
        # frozen dataclass is hashable
        assert {Color("#ef4444"), Color("#EF4444")} == {Color("#ef4444")}

    def test_non_string_raises_typeerror(self):
        with pytest.raises(TypeError, match="Color hex must be a string"):
            Color(0xEF4444)  # type: ignore[arg-type]

    def test_invalid_hex_raises_valueerror(self):
        with pytest.raises(ValueError, match="must be a CSS hex string"):
            Color("red")
        with pytest.raises(ValueError, match="must be a CSS hex string"):
            Color("#ef44")  # 5-char body
        with pytest.raises(ValueError, match="must be a CSS hex string"):
            Color("ef4444")  # missing #


class TestColorRgb:
    def test_basic(self):
        assert Color.rgb(239, 68, 68) == Color("#ef4444")

    def test_zero(self):
        assert Color.rgb(0, 0, 0) == Color("#000000")

    def test_max(self):
        assert Color.rgb(255, 255, 255) == Color("#ffffff")

    def test_non_int_raises_typeerror(self):
        with pytest.raises(TypeError, match="must be an integer"):
            Color.rgb(239.0, 68, 68)  # type: ignore[arg-type]

    def test_bool_rejected(self):
        with pytest.raises(TypeError, match="must be an integer"):
            Color.rgb(True, 0, 0)  # type: ignore[arg-type]

    def test_out_of_range_raises_valueerror(self):
        with pytest.raises(ValueError, match="must be in range 0–255"):
            Color.rgb(256, 0, 0)
        with pytest.raises(ValueError, match="must be in range 0–255"):
            Color.rgb(-1, 0, 0)
