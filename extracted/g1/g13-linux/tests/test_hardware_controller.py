"""Tests for HardwareController."""

from unittest.mock import MagicMock, patch

from g13_linux.gui.models.hardware_controller import HardwareController


class TestHardwareControllerInit:
    """Tests for HardwareController initialization."""

    def test_init(self):
        """Test initialization."""
        controller = HardwareController()

        assert controller.lcd is None
        assert controller.backlight is None
        assert controller._initialized is False

    def test_is_initialized_false(self):
        """Test is_initialized is False initially."""
        controller = HardwareController()
        assert controller.is_initialized is False


class TestHardwareControllerInitialize:
    """Tests for initialize method."""

    def test_initialize_creates_lcd(self):
        """Test initialize creates LCD instance."""
        controller = HardwareController()
        mock_handle = MagicMock()

        with patch("g13_linux.gui.models.hardware_controller.G13LCD") as mock_lcd_class:
            controller.initialize(mock_handle)

            mock_lcd_class.assert_called_once_with(mock_handle)
            assert controller.lcd is not None

    def test_initialize_creates_backlight(self):
        """Test initialize creates Backlight instance."""
        controller = HardwareController()
        mock_handle = MagicMock()

        with patch("g13_linux.gui.models.hardware_controller.G13Backlight") as mock_bl_class:
            controller.initialize(mock_handle)

            mock_bl_class.assert_called_once_with(mock_handle)
            assert controller.backlight is not None

    def test_initialize_sets_flag(self):
        """Test initialize sets _initialized flag."""
        controller = HardwareController()
        mock_handle = MagicMock()

        with patch("g13_linux.gui.models.hardware_controller.G13LCD"):
            with patch("g13_linux.gui.models.hardware_controller.G13Backlight"):
                controller.initialize(mock_handle)

        assert controller.is_initialized is True


class TestHardwareControllerLCD:
    """Tests for LCD methods."""

    def test_set_lcd_text_when_not_initialized(self, capsys):
        """Test set_lcd_text when LCD not initialized."""
        controller = HardwareController()

        controller.set_lcd_text("Hello")

        captured = capsys.readouterr()
        assert "LCD not initialized" in captured.out
        assert "Hello" in captured.out

    def test_set_lcd_text_when_initialized(self):
        """Test set_lcd_text calls LCD methods."""
        controller = HardwareController()
        mock_lcd = MagicMock()
        controller.lcd = mock_lcd

        controller.set_lcd_text("Test")

        mock_lcd.clear.assert_called_once()
        mock_lcd.write_text.assert_called_once_with("Test")

    def test_clear_lcd_when_not_initialized(self):
        """Test clear_lcd when LCD not initialized is safe."""
        controller = HardwareController()

        # Should not raise
        controller.clear_lcd()

    def test_clear_lcd_when_initialized(self):
        """Test clear_lcd calls LCD clear."""
        controller = HardwareController()
        mock_lcd = MagicMock()
        controller.lcd = mock_lcd

        controller.clear_lcd()

        mock_lcd.clear.assert_called_once()


class TestHardwareControllerBacklight:
    """Tests for backlight methods."""

    def test_set_backlight_color_when_not_initialized(self, capsys):
        """Test set_backlight_color when backlight not initialized."""
        controller = HardwareController()

        controller.set_backlight_color("#FF0000")

        captured = capsys.readouterr()
        assert "Backlight not initialized" in captured.out
        assert "#FF0000" in captured.out

    def test_set_backlight_color_when_initialized(self):
        """Test set_backlight_color calls backlight method."""
        controller = HardwareController()
        mock_backlight = MagicMock()
        controller.backlight = mock_backlight

        controller.set_backlight_color("#00FF00")

        mock_backlight.set_color_hex.assert_called_once_with("#00FF00")

    def test_set_backlight_brightness_when_not_initialized(self, capsys):
        """Test set_backlight_brightness when backlight not initialized."""
        controller = HardwareController()

        controller.set_backlight_brightness(50)

        captured = capsys.readouterr()
        assert "Backlight not initialized" in captured.out
        assert "50%" in captured.out

    def test_set_backlight_brightness_when_initialized(self):
        """Test set_backlight_brightness calls backlight method."""
        controller = HardwareController()
        mock_backlight = MagicMock()
        controller.backlight = mock_backlight

        controller.set_backlight_brightness(75)

        mock_backlight.set_brightness.assert_called_once_with(75)

    def test_get_backlight_color_when_not_initialized(self):
        """Test get_backlight_color returns None when not initialized."""
        controller = HardwareController()

        result = controller.get_backlight_color()

        assert result is None

    def test_get_backlight_color_when_initialized(self):
        """Test get_backlight_color returns color tuple."""
        controller = HardwareController()
        mock_backlight = MagicMock()
        mock_backlight.get_color.return_value = (255, 128, 64)
        controller.backlight = mock_backlight

        result = controller.get_backlight_color()

        assert result == (255, 128, 64)

    def test_get_backlight_brightness_when_not_initialized(self):
        """Test get_backlight_brightness returns None when not initialized."""
        controller = HardwareController()

        result = controller.get_backlight_brightness()

        assert result is None

    def test_get_backlight_brightness_when_initialized(self):
        """Test get_backlight_brightness returns brightness value."""
        controller = HardwareController()
        mock_backlight = MagicMock()
        mock_backlight.get_brightness.return_value = 80
        controller.backlight = mock_backlight

        result = controller.get_backlight_brightness()

        assert result == 80
