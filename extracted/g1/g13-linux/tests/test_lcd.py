"""Tests for G13 LCD module."""

from unittest.mock import MagicMock, patch

import pytest

from g13_linux.hardware.lcd import FONT_5X7, G13LCD


class TestFont5x7:
    """Tests for the 5x7 font table."""

    def test_space_character(self):
        """Test space character is all zeros."""
        assert FONT_5X7[32] == [0x00, 0x00, 0x00, 0x00, 0x00]

    def test_exclamation_mark(self):
        """Test exclamation mark character."""
        assert FONT_5X7[33] == [0x00, 0x00, 0x5F, 0x00, 0x00]

    def test_letter_a_uppercase(self):
        """Test uppercase A."""
        assert 65 in FONT_5X7  # 'A'
        assert len(FONT_5X7[65]) == 5

    def test_letter_a_lowercase(self):
        """Test lowercase a."""
        assert 97 in FONT_5X7  # 'a'
        assert len(FONT_5X7[97]) == 5

    def test_digits(self):
        """Test all digits are present."""
        for digit in range(48, 58):  # '0' to '9'
            assert digit in FONT_5X7
            assert len(FONT_5X7[digit]) == 5

    def test_all_characters_have_5_columns(self):
        """Test all characters have 5 bytes."""
        for code, glyph in FONT_5X7.items():
            assert len(glyph) == 5, f"Character {code} ({chr(code)}) has {len(glyph)} columns"

    def test_printable_ascii_range(self):
        """Test characters 32-126 are covered."""
        for code in range(32, 127):
            assert code in FONT_5X7, f"Character {code} ({chr(code)}) missing from font"


class TestG13LCDConstants:
    """Tests for G13LCD constants."""

    def test_width(self):
        assert G13LCD.WIDTH == 160

    def test_height(self):
        assert G13LCD.HEIGHT == 43

    def test_buffer_rows(self):
        assert G13LCD.BUFFER_ROWS == 48

    def test_bytes_per_column(self):
        assert G13LCD.BYTES_PER_COLUMN == 6

    def test_framebuffer_size(self):
        assert G13LCD.FRAMEBUFFER_SIZE == 960
        assert G13LCD.FRAMEBUFFER_SIZE == G13LCD.WIDTH * G13LCD.BYTES_PER_COLUMN

    def test_header_size(self):
        assert G13LCD.HEADER_SIZE == 32

    def test_command_byte(self):
        assert G13LCD.COMMAND_BYTE == 0x03


class TestG13LCDInit:
    """Tests for G13LCD initialization."""

    def test_init_without_device(self):
        lcd = G13LCD()
        assert lcd.device is None
        assert len(lcd._framebuffer) == G13LCD.FRAMEBUFFER_SIZE
        assert all(b == 0 for b in lcd._framebuffer)

    def test_init_with_device(self):
        mock_device = MagicMock()
        lcd = G13LCD(mock_device)
        assert lcd.device is mock_device

    def test_framebuffer_initially_clear(self):
        lcd = G13LCD()
        assert lcd._framebuffer == bytearray(G13LCD.FRAMEBUFFER_SIZE)


class TestG13LCDClear:
    """Tests for clear method."""

    def test_clear_resets_framebuffer(self):
        lcd = G13LCD()
        lcd._framebuffer[0] = 0xFF
        lcd._framebuffer[100] = 0xAA

        with patch.object(lcd, "_send_framebuffer"):
            lcd.clear()

        assert all(b == 0 for b in lcd._framebuffer)

    def test_clear_sends_framebuffer(self):
        mock_device = MagicMock()
        lcd = G13LCD(mock_device)

        with patch.object(lcd, "_send_framebuffer") as mock_send:
            lcd.clear()
            mock_send.assert_called_once()


class TestG13LCDFill:
    """Tests for fill method."""

    def test_fill_sets_all_pixels(self):
        lcd = G13LCD()

        with patch.object(lcd, "_send_framebuffer"):
            lcd.fill()

        assert all(b == 0xFF for b in lcd._framebuffer)

    def test_fill_sends_framebuffer(self):
        mock_device = MagicMock()
        lcd = G13LCD(mock_device)

        with patch.object(lcd, "_send_framebuffer") as mock_send:
            lcd.fill()
            mock_send.assert_called_once()


class TestG13LCDSetPixel:
    """Tests for set_pixel method."""

    def test_set_pixel_top_left(self):
        lcd = G13LCD()
        lcd.set_pixel(0, 0, True)
        assert lcd._framebuffer[0] & 0x01

    def test_set_pixel_first_row_end(self):
        lcd = G13LCD()
        lcd.set_pixel(159, 0, True)
        assert lcd._framebuffer[159] & 0x01

    def test_set_pixel_row_7(self):
        lcd = G13LCD()
        lcd.set_pixel(0, 7, True)
        assert lcd._framebuffer[0] & 0x80

    def test_set_pixel_row_8(self):
        lcd = G13LCD()
        lcd.set_pixel(0, 8, True)
        assert lcd._framebuffer[160] & 0x01

    def test_set_pixel_middle(self):
        lcd = G13LCD()
        lcd.set_pixel(80, 21, True)
        assert lcd._framebuffer[400] & (1 << 5)

    def test_set_pixel_last_visible_row(self):
        lcd = G13LCD()
        lcd.set_pixel(0, 42, True)
        assert lcd._framebuffer[800] & (1 << 2)

    def test_clear_pixel(self):
        lcd = G13LCD()
        lcd._framebuffer[0] = 0xFF
        lcd.set_pixel(0, 0, False)
        assert lcd._framebuffer[0] == 0xFE

    def test_set_pixel_out_of_bounds_x(self):
        lcd = G13LCD()
        lcd.set_pixel(160, 0, True)
        lcd.set_pixel(-1, 0, True)
        assert all(b == 0 for b in lcd._framebuffer)

    def test_set_pixel_out_of_bounds_y(self):
        lcd = G13LCD()
        lcd.set_pixel(0, 43, True)
        lcd.set_pixel(0, -1, True)
        assert all(b == 0 for b in lcd._framebuffer)

    def test_row_block_layout(self):
        lcd = G13LCD()
        for row_block in range(6):
            y = row_block * 8
            if y >= G13LCD.HEIGHT:
                continue
            lcd.set_pixel(0, y, True)
            expected_byte = row_block * 160
            assert lcd._framebuffer[expected_byte] & 0x01


class TestG13LCDWriteText:
    """Tests for write_text method."""

    def test_write_single_char(self):
        lcd = G13LCD()
        with patch.object(lcd, "_send_framebuffer"):
            lcd.write_text("A", 0, 0)
        assert lcd._framebuffer[0] != 0 or lcd._framebuffer[1] != 0

    def test_write_text_position(self):
        lcd = G13LCD()
        with patch.object(lcd, "_send_framebuffer"):
            lcd.write_text("X", 10, 0)
        for x in range(10):
            assert lcd._framebuffer[x] == 0

    def test_write_text_unknown_char(self):
        lcd = G13LCD()
        with patch.object(lcd, "_send_framebuffer"):
            lcd.write_text("\x80", 0, 0)
        assert any(b != 0 for b in lcd._framebuffer[:6])

    def test_write_text_send_false(self):
        lcd = G13LCD()
        with patch.object(lcd, "_send_framebuffer") as mock_send:
            lcd.write_text("A", 0, 0, send=False)
            mock_send.assert_not_called()

    def test_write_text_clips_at_edge(self):
        lcd = G13LCD()
        with patch.object(lcd, "_send_framebuffer"):
            lcd.write_text("A" * 50, 0, 0)
        assert len(lcd._framebuffer) == G13LCD.FRAMEBUFFER_SIZE


class TestG13LCDWriteTextCentered:
    """Tests for write_text_centered method."""

    def test_center_short_text(self):
        lcd = G13LCD()
        with patch.object(lcd, "_send_framebuffer"):
            lcd.write_text_centered("Hi", y=0)
        for x in range(74):
            assert lcd._framebuffer[x] == 0

    def test_center_uses_default_y(self):
        lcd = G13LCD()
        with patch.object(lcd, "write_text") as mock_write:
            lcd.write_text_centered("Test")
            assert mock_write.call_args[0][2] == 18


class TestG13LCDWriteBitmap:
    """Tests for write_bitmap method."""

    def test_write_full_bitmap(self):
        lcd = G13LCD()
        bitmap = bytes([0xAA] * G13LCD.FRAMEBUFFER_SIZE)
        with patch.object(lcd, "_send_framebuffer"):
            lcd.write_bitmap(bitmap)
        assert bytes(lcd._framebuffer) == bitmap

    def test_write_partial_bitmap(self):
        lcd = G13LCD()
        bitmap = bytes([0xFF] * 100)
        with patch.object(lcd, "_send_framebuffer"):
            lcd.write_bitmap(bitmap)
        assert all(b == 0xFF for b in lcd._framebuffer[:100])
        assert all(b == 0 for b in lcd._framebuffer[100:])

    def test_write_bitmap_too_large(self):
        lcd = G13LCD()
        bitmap = bytes([0xFF] * (G13LCD.FRAMEBUFFER_SIZE + 1))
        with pytest.raises(ValueError, match="Bitmap too large"):
            lcd.write_bitmap(bitmap)


class TestG13LCDSendFramebuffer:
    """Tests for _send_framebuffer method."""

    def test_send_without_device(self, capsys):
        lcd = G13LCD()
        lcd._send_framebuffer()
        captured = capsys.readouterr()
        assert "No device connected" in captured.out

    def test_send_packet_format(self):
        mock_device = MagicMock()
        mock_device.write.return_value = 992
        lcd = G13LCD(mock_device)
        lcd._send_framebuffer()
        mock_device.write.assert_called_once()
        packet = mock_device.write.call_args[0][0]
        assert len(packet) == 992
        assert packet[0] == 0x03
        assert all(b == 0 for b in packet[1:32])

    def test_partial_write_warning(self, capsys):
        mock_device = MagicMock()
        mock_device.write.return_value = 500
        lcd = G13LCD(mock_device)
        lcd._send_framebuffer()
        captured = capsys.readouterr()
        assert "Partial write" in captured.out

    def test_send_handles_exception(self, capsys):
        mock_device = MagicMock()
        mock_device.write.side_effect = OSError("USB error")
        lcd = G13LCD(mock_device)
        lcd._send_framebuffer()
        captured = capsys.readouterr()
        assert "Failed to send framebuffer" in captured.out


class TestG13LCDSetBrightness:
    """Tests for set_brightness method."""

    def test_brightness_valid_range(self, capsys):
        lcd = G13LCD()
        lcd.set_brightness(0)
        lcd.set_brightness(50)
        lcd.set_brightness(100)
        captured = capsys.readouterr()
        assert "not supported" in captured.out

    def test_brightness_invalid_low(self):
        lcd = G13LCD()
        with pytest.raises(ValueError, match="Brightness must be 0-100"):
            lcd.set_brightness(-1)

    def test_brightness_invalid_high(self):
        lcd = G13LCD()
        with pytest.raises(ValueError, match="Brightness must be 0-100"):
            lcd.set_brightness(101)


class TestG13LCDInitLcd:
    """Tests for _init_lcd method."""

    def test_init_lcd_no_device(self):
        lcd = G13LCD()
        lcd._init_lcd()

    def test_init_lcd_calls_ctrl_transfer(self):
        mock_device = MagicMock()
        mock_device._dev = MagicMock()
        lcd = G13LCD(mock_device)
        lcd._init_lcd()
        mock_device._dev.ctrl_transfer.assert_called_once_with(0, 9, 1, 0, None, 1000)

    def test_init_lcd_handles_exception(self, capsys):
        mock_device = MagicMock()
        mock_device._dev = MagicMock()
        mock_device._dev.ctrl_transfer.side_effect = Exception("USB error")
        lcd = G13LCD(mock_device)
        lcd._init_lcd()
        captured = capsys.readouterr()
        assert "init_lcd failed" in captured.out


class TestG13LCDMissingCoverage:
    """Tests for edge cases to achieve 100% coverage."""

    def test_write_text_clips_rows_at_bottom(self):
        """Test write_text clips rows that exceed display height (line 193).

        When text is rendered near the bottom of the display (y=37+),
        some rows of the 7-row font would exceed HEIGHT=43 and must be skipped.
        """
        lcd = G13LCD()
        with patch.object(lcd, "_send_framebuffer"):
            # y=38 means rows 0-4 are at y=38-42 (visible)
            # but rows 5-6 would be at y=43-44 (off-screen, HEIGHT=43)
            lcd.write_text("A", 0, 38)

        # Text should render - some pixels in the visible area should be set
        # The character 'A' has data in multiple rows
        # At y=38, we can render rows 0-4 (y=38,39,40,41,42)
        # Rows 5-6 are skipped (y=43,44 >= HEIGHT)
        has_pixels = any(b != 0 for b in lcd._framebuffer)
        assert has_pixels, "Some pixels should be set for visible portion of text"
