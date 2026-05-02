"""Tests for RGB color utilities."""

import sys
from pathlib import Path

import pytest

# Add src to path without importing through __init__.py
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from g13_linux.led.colors import NAMED_COLORS, RGB, blend, brighten, dim, hsv_to_rgb


class TestRGBCreation:
    """Tests for RGB class creation and clamping."""

    def test_basic_creation(self):
        """RGB accepts valid values."""
        color = RGB(100, 150, 200)
        assert color.r == 100
        assert color.g == 150
        assert color.b == 200

    def test_clamps_negative_values(self):
        """RGB clamps negative values to 0."""
        color = RGB(-10, -50, -100)
        assert color.r == 0
        assert color.g == 0
        assert color.b == 0

    def test_clamps_values_above_255(self):
        """RGB clamps values above 255."""
        color = RGB(300, 500, 1000)
        assert color.r == 255
        assert color.g == 255
        assert color.b == 255

    def test_boundary_values(self):
        """RGB handles boundary values correctly."""
        color = RGB(0, 255, 128)
        assert color.r == 0
        assert color.g == 255
        assert color.b == 128


class TestRGBFromHex:
    """Tests for RGB.from_hex class method."""

    def test_from_hex_with_hash(self):
        """from_hex parses #RRGGBB format."""
        color = RGB.from_hex("#FF8000")
        assert color.r == 255
        assert color.g == 128
        assert color.b == 0

    def test_from_hex_without_hash(self):
        """from_hex parses RRGGBB format."""
        color = RGB.from_hex("00FF80")
        assert color.r == 0
        assert color.g == 255
        assert color.b == 128

    def test_from_hex_lowercase(self):
        """from_hex handles lowercase hex."""
        color = RGB.from_hex("#abcdef")
        assert color.r == 171
        assert color.g == 205
        assert color.b == 239

    def test_from_hex_black(self):
        """from_hex parses black correctly."""
        color = RGB.from_hex("#000000")
        assert color == RGB(0, 0, 0)

    def test_from_hex_white(self):
        """from_hex parses white correctly."""
        color = RGB.from_hex("#FFFFFF")
        assert color == RGB(255, 255, 255)

    def test_from_hex_invalid_length(self):
        """from_hex raises ValueError for invalid length."""
        with pytest.raises(ValueError, match="must be 6 characters"):
            RGB.from_hex("#FFF")

    def test_from_hex_invalid_characters(self):
        """from_hex raises ValueError for invalid characters."""
        with pytest.raises(ValueError, match="Invalid hex color"):
            RGB.from_hex("#GGGGGG")


class TestRGBFromName:
    """Tests for RGB.from_name class method."""

    def test_from_name_red(self):
        """from_name returns correct RGB for 'red'."""
        color = RGB.from_name("red")
        assert color == RGB(255, 0, 0)

    def test_from_name_case_insensitive(self):
        """from_name is case-insensitive."""
        assert RGB.from_name("RED") == RGB.from_name("red")
        assert RGB.from_name("Blue") == RGB.from_name("blue")
        assert RGB.from_name("GREEN") == RGB.from_name("green")

    def test_from_name_all_named_colors(self):
        """from_name works for all named colors."""
        for name in NAMED_COLORS:
            color = RGB.from_name(name)
            assert isinstance(color, RGB)

    def test_from_name_invalid(self):
        """from_name raises ValueError for unknown color."""
        with pytest.raises(ValueError, match="Unknown color"):
            RGB.from_name("notacolor")


class TestRGBConversions:
    """Tests for RGB conversion methods."""

    def test_to_hex(self):
        """to_hex returns #RRGGBB format."""
        color = RGB(255, 128, 0)
        assert color.to_hex() == "#FF8000"

    def test_to_hex_with_leading_zeros(self):
        """to_hex includes leading zeros."""
        color = RGB(0, 15, 1)
        assert color.to_hex() == "#000F01"

    def test_to_tuple(self):
        """to_tuple returns (r, g, b) tuple."""
        color = RGB(100, 150, 200)
        assert color.to_tuple() == (100, 150, 200)

    def test_iter_unpacking(self):
        """RGB supports unpacking via __iter__."""
        color = RGB(10, 20, 30)
        r, g, b = color
        assert r == 10
        assert g == 20
        assert b == 30


class TestBlend:
    """Tests for blend function."""

    def test_blend_factor_zero(self):
        """blend with factor 0 returns first color."""
        color1 = RGB(255, 0, 0)
        color2 = RGB(0, 255, 0)
        result = blend(color1, color2, 0.0)
        assert result == RGB(255, 0, 0)

    def test_blend_factor_one(self):
        """blend with factor 1 returns second color."""
        color1 = RGB(255, 0, 0)
        color2 = RGB(0, 255, 0)
        result = blend(color1, color2, 1.0)
        assert result == RGB(0, 255, 0)

    def test_blend_factor_half(self):
        """blend with factor 0.5 returns average."""
        color1 = RGB(0, 0, 0)
        color2 = RGB(100, 200, 100)
        result = blend(color1, color2, 0.5)
        assert result == RGB(50, 100, 50)

    def test_blend_clamps_factor(self):
        """blend clamps factor to 0-1 range."""
        color1 = RGB(100, 100, 100)
        color2 = RGB(200, 200, 200)
        assert blend(color1, color2, -1.0) == blend(color1, color2, 0.0)
        assert blend(color1, color2, 2.0) == blend(color1, color2, 1.0)


class TestBrightenAndDim:
    """Tests for brighten and dim functions."""

    def test_brighten_zero(self):
        """brighten with factor 0 returns original color."""
        color = RGB(100, 100, 100)
        result = brighten(color, 0.0)
        assert result == RGB(100, 100, 100)

    def test_brighten_one(self):
        """brighten with factor 1 returns white."""
        color = RGB(100, 100, 100)
        result = brighten(color, 1.0)
        assert result == RGB(255, 255, 255)

    def test_dim_zero(self):
        """dim with factor 0 returns original color."""
        color = RGB(100, 100, 100)
        result = dim(color, 0.0)
        assert result == RGB(100, 100, 100)

    def test_dim_one(self):
        """dim with factor 1 returns black."""
        color = RGB(100, 100, 100)
        result = dim(color, 1.0)
        assert result == RGB(0, 0, 0)


class TestHSVToRGB:
    """Tests for hsv_to_rgb function."""

    def test_red_hue(self):
        """HSV (0, 1, 1) is red."""
        result = hsv_to_rgb(0.0, 1.0, 1.0)
        assert result == RGB(255, 0, 0)

    def test_green_hue(self):
        """HSV (0.33, 1, 1) is approximately green."""
        result = hsv_to_rgb(1 / 3, 1.0, 1.0)
        assert result == RGB(0, 255, 0)

    def test_blue_hue(self):
        """HSV (0.67, 1, 1) is approximately blue."""
        result = hsv_to_rgb(2 / 3, 1.0, 1.0)
        assert result == RGB(0, 0, 255)

    def test_white(self):
        """HSV with saturation 0 is grayscale."""
        result = hsv_to_rgb(0.0, 0.0, 1.0)
        assert result == RGB(255, 255, 255)

    def test_black(self):
        """HSV with value 0 is black."""
        result = hsv_to_rgb(0.0, 1.0, 0.0)
        assert result == RGB(0, 0, 0)

    def test_gray(self):
        """HSV with saturation 0 and mid value is gray."""
        result = hsv_to_rgb(0.0, 0.0, 0.5)
        assert result == RGB(127, 127, 127)

    def test_hue_wraps(self):
        """HSV hue wraps around at 1.0."""
        result1 = hsv_to_rgb(0.0, 1.0, 1.0)
        result2 = hsv_to_rgb(1.0, 1.0, 1.0)
        assert result1 == result2
