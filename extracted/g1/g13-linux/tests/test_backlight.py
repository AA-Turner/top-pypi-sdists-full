"""Tests for the backlight module."""

from unittest.mock import Mock

import pytest

from g13_linux.hardware.backlight import G13Backlight


class TestG13BacklightInit:
    """Test G13Backlight initialization."""

    def test_init_no_device(self):
        backlight = G13Backlight()
        assert backlight.device is None
        assert backlight._current_color == (255, 255, 255)
        assert backlight._current_brightness == 100

    def test_init_with_device(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)
        assert backlight.device == mock_device

    def test_report_constants(self):
        assert G13Backlight.REPORT_ID == 0x07
        assert G13Backlight.REPORT_SIZE == 5


class TestSetColor:
    """Test set_color method."""

    def test_set_color_valid(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)

        backlight.set_color(255, 128, 0)

        assert backlight._current_color == (255, 128, 0)
        mock_device.send_feature_report.assert_called_once_with(bytes([0x07, 255, 128, 0, 0x00]))

    def test_set_color_black(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)

        backlight.set_color(0, 0, 0)

        assert backlight._current_color == (0, 0, 0)

    def test_set_color_white(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)

        backlight.set_color(255, 255, 255)

        assert backlight._current_color == (255, 255, 255)

    def test_set_color_no_device(self, capsys):
        backlight = G13Backlight()

        backlight.set_color(255, 0, 0)

        assert backlight._current_color == (255, 0, 0)
        captured = capsys.readouterr()
        assert "No device" in captured.out

    def test_set_color_device_error(self, capsys):
        mock_device = Mock()
        mock_device.send_feature_report.side_effect = OSError("Device error")
        backlight = G13Backlight(mock_device)

        backlight.set_color(255, 0, 0)

        assert backlight._current_color == (255, 0, 0)
        captured = capsys.readouterr()
        assert "Failed to set color" in captured.out

    def test_set_color_invalid_r_high(self):
        backlight = G13Backlight()
        with pytest.raises(ValueError, match="0-255"):
            backlight.set_color(256, 0, 0)

    def test_set_color_invalid_g_negative(self):
        backlight = G13Backlight()
        with pytest.raises(ValueError, match="0-255"):
            backlight.set_color(0, -1, 0)

    def test_set_color_invalid_b_high(self):
        backlight = G13Backlight()
        with pytest.raises(ValueError, match="0-255"):
            backlight.set_color(0, 0, 300)


class TestSetColorHex:
    """Test set_color_hex method."""

    def test_set_color_hex_with_hash(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)

        backlight.set_color_hex("#FF8000")

        assert backlight._current_color == (255, 128, 0)

    def test_set_color_hex_without_hash(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)

        backlight.set_color_hex("00FF00")

        assert backlight._current_color == (0, 255, 0)

    def test_set_color_hex_lowercase(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)

        backlight.set_color_hex("aabbcc")

        assert backlight._current_color == (170, 187, 204)

    def test_set_color_hex_invalid_length(self):
        backlight = G13Backlight()
        with pytest.raises(ValueError, match="RRGGBB"):
            backlight.set_color_hex("#FFF")

    def test_set_color_hex_invalid_chars(self):
        backlight = G13Backlight()
        with pytest.raises(ValueError, match="Invalid hex"):
            backlight.set_color_hex("#GGGGGG")


class TestSetBrightness:
    """Test set_brightness method."""

    def test_set_brightness_full(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)
        backlight._current_color = (255, 255, 255)

        backlight.set_brightness(100)

        assert backlight._current_brightness == 100

    def test_set_brightness_half(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)
        backlight._current_color = (200, 100, 50)

        backlight.set_brightness(50)

        assert backlight._current_brightness == 50
        # Check that scaled color was sent
        call_args = mock_device.send_feature_report.call_args[0][0]
        assert call_args[1] == 100  # 200 * 0.5
        assert call_args[2] == 50  # 100 * 0.5
        assert call_args[3] == 25  # 50 * 0.5

    def test_set_brightness_zero(self):
        mock_device = Mock()
        backlight = G13Backlight(mock_device)
        backlight._current_color = (255, 255, 255)

        backlight.set_brightness(0)

        assert backlight._current_brightness == 0
        call_args = mock_device.send_feature_report.call_args[0][0]
        assert call_args[1] == 0
        assert call_args[2] == 0
        assert call_args[3] == 0

    def test_set_brightness_invalid_high(self):
        backlight = G13Backlight()
        with pytest.raises(ValueError, match="0-100"):
            backlight.set_brightness(101)

    def test_set_brightness_invalid_negative(self):
        backlight = G13Backlight()
        with pytest.raises(ValueError, match="0-100"):
            backlight.set_brightness(-1)


class TestApplyColor:
    """Test _apply_color method."""

    def test_apply_color_no_device(self):
        backlight = G13Backlight()
        backlight._current_color = (255, 0, 0)
        backlight._current_brightness = 50

        # Should not raise
        backlight._apply_color()

    def test_apply_color_device_error(self, capsys):
        mock_device = Mock()
        mock_device.send_feature_report.side_effect = OSError("error")
        backlight = G13Backlight(mock_device)
        backlight._current_color = (255, 0, 0)

        backlight._apply_color()

        captured = capsys.readouterr()
        assert "Failed to apply color" in captured.out


class TestGetters:
    """Test getter methods."""

    def test_get_color(self):
        backlight = G13Backlight()
        backlight._current_color = (100, 150, 200)

        result = backlight.get_color()

        assert result == (100, 150, 200)

    def test_get_brightness(self):
        backlight = G13Backlight()
        backlight._current_brightness = 75

        result = backlight.get_brightness()

        assert result == 75
