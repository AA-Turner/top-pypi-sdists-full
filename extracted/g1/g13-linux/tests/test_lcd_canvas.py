"""Tests for LCD Canvas drawing primitives."""

from g13_linux.lcd.canvas import Canvas


class TestCanvasBasics:
    """Test basic canvas operations."""

    def test_canvas_init_default_size(self):
        """Canvas initializes with default 160x43 dimensions."""
        canvas = Canvas()
        assert canvas.width == 160
        assert canvas.height == 43
        assert len(canvas._buffer) == Canvas.FRAMEBUFFER_SIZE

    def test_canvas_init_custom_size(self):
        """Canvas can be initialized with custom dimensions."""
        canvas = Canvas(width=100, height=30)
        assert canvas.width == 100
        assert canvas.height == 30

    def test_clear(self):
        """Clear sets all pixels to off."""
        canvas = Canvas()
        canvas.fill()
        canvas.clear()
        assert all(b == 0 for b in canvas._buffer)

    def test_fill(self):
        """Fill sets all pixels to on."""
        canvas = Canvas()
        canvas.fill()
        assert all(b == 0xFF for b in canvas._buffer)


class TestPixelOperations:
    """Test pixel-level operations."""

    def test_set_pixel_on(self):
        """Setting a pixel on works."""
        canvas = Canvas()
        canvas.set_pixel(10, 5, True)
        assert canvas.get_pixel(10, 5) is True

    def test_set_pixel_off(self):
        """Setting a pixel off works."""
        canvas = Canvas()
        canvas.fill()
        canvas.set_pixel(10, 5, False)
        assert canvas.get_pixel(10, 5) is False

    def test_get_pixel_default_off(self):
        """Pixels are off by default."""
        canvas = Canvas()
        assert canvas.get_pixel(0, 0) is False
        assert canvas.get_pixel(80, 21) is False

    def test_set_pixel_out_of_bounds_ignored(self):
        """Out-of-bounds pixel operations are silently ignored."""
        canvas = Canvas()
        # Should not raise
        canvas.set_pixel(-1, 0, True)
        canvas.set_pixel(0, -1, True)
        canvas.set_pixel(160, 0, True)
        canvas.set_pixel(0, 43, True)

    def test_get_pixel_out_of_bounds_returns_false(self):
        """Out-of-bounds get_pixel returns False."""
        canvas = Canvas()
        assert canvas.get_pixel(-1, 0) is False
        assert canvas.get_pixel(0, -1) is False
        assert canvas.get_pixel(160, 0) is False
        assert canvas.get_pixel(0, 43) is False

    def test_pixel_bit_packing(self):
        """Verify correct bit packing for pixel storage."""
        canvas = Canvas()
        # Set pixels in same column, different rows
        canvas.set_pixel(0, 0, True)
        canvas.set_pixel(0, 7, True)
        # Both should be in byte 0
        assert canvas._buffer[0] == 0b10000001  # bits 0 and 7

    def test_pixel_row_block_packing(self):
        """Verify row-block byte layout."""
        canvas = Canvas()
        # Pixel at y=8 should be in the next row of bytes
        canvas.set_pixel(0, 8, True)
        # Row 1 starts at byte 160 (WIDTH)
        assert canvas._buffer[160] == 0b00000001


class TestLineDrawing:
    """Test line drawing operations."""

    def test_draw_hline(self):
        """Horizontal line draws correctly."""
        canvas = Canvas()
        canvas.draw_hline(10, 5, 20)
        for x in range(10, 30):
            assert canvas.get_pixel(x, 5) is True
        # Check adjacent pixels are off
        assert canvas.get_pixel(9, 5) is False
        assert canvas.get_pixel(30, 5) is False

    def test_draw_vline(self):
        """Vertical line draws correctly."""
        canvas = Canvas()
        canvas.draw_vline(5, 10, 15)
        for y in range(10, 25):
            assert canvas.get_pixel(5, y) is True
        # Check adjacent pixels are off
        assert canvas.get_pixel(5, 9) is False
        assert canvas.get_pixel(5, 25) is False

    def test_draw_line_horizontal(self):
        """Bresenham line draws horizontal correctly."""
        canvas = Canvas()
        canvas.draw_line(0, 0, 10, 0)
        for x in range(11):
            assert canvas.get_pixel(x, 0) is True

    def test_draw_line_vertical(self):
        """Bresenham line draws vertical correctly."""
        canvas = Canvas()
        canvas.draw_line(0, 0, 0, 10)
        for y in range(11):
            assert canvas.get_pixel(0, y) is True

    def test_draw_line_diagonal(self):
        """Bresenham line draws diagonal correctly."""
        canvas = Canvas()
        canvas.draw_line(0, 0, 10, 10)
        # Diagonal should hit both endpoints
        assert canvas.get_pixel(0, 0) is True
        assert canvas.get_pixel(10, 10) is True

    def test_draw_line_reverse_direction(self):
        """Bresenham works with reversed direction."""
        canvas = Canvas()
        canvas.draw_line(10, 10, 0, 0)
        assert canvas.get_pixel(0, 0) is True
        assert canvas.get_pixel(10, 10) is True


class TestRectangle:
    """Test rectangle drawing."""

    def test_draw_rect_outline(self):
        """Rectangle outline draws correctly."""
        canvas = Canvas()
        canvas.draw_rect(10, 10, 20, 10, filled=False)
        # Top edge
        assert canvas.get_pixel(10, 10) is True
        assert canvas.get_pixel(29, 10) is True
        # Bottom edge
        assert canvas.get_pixel(10, 19) is True
        assert canvas.get_pixel(29, 19) is True
        # Interior should be empty
        assert canvas.get_pixel(15, 15) is False

    def test_draw_rect_filled(self):
        """Filled rectangle draws correctly."""
        canvas = Canvas()
        canvas.draw_rect(10, 10, 5, 5, filled=True)
        for y in range(10, 15):
            for x in range(10, 15):
                assert canvas.get_pixel(x, y) is True
        # Outside should be empty
        assert canvas.get_pixel(9, 10) is False
        assert canvas.get_pixel(15, 10) is False


class TestProgressBar:
    """Test progress bar drawing."""

    def test_progress_bar_empty(self):
        """Empty progress bar shows just border."""
        canvas = Canvas()
        canvas.draw_progress_bar(10, 10, 50, 10, 0)
        # Border exists
        assert canvas.get_pixel(10, 10) is True
        # Interior empty (at 0%)
        assert canvas.get_pixel(15, 15) is False

    def test_progress_bar_full(self):
        """Full progress bar is completely filled."""
        canvas = Canvas()
        canvas.draw_progress_bar(10, 10, 50, 10, 100)
        # Interior should be filled
        assert canvas.get_pixel(15, 15) is True
        assert canvas.get_pixel(55, 15) is True

    def test_progress_bar_half(self):
        """Half-filled progress bar."""
        canvas = Canvas()
        canvas.draw_progress_bar(0, 0, 100, 10, 50)
        # Left half filled
        assert canvas.get_pixel(25, 5) is True
        # Right half empty
        assert canvas.get_pixel(75, 5) is False


class TestInvertRegion:
    """Test region inversion."""

    def test_invert_region(self):
        """Region inversion toggles pixels."""
        canvas = Canvas()
        canvas.set_pixel(5, 5, True)
        canvas.set_pixel(6, 5, False)
        canvas.invert_region(5, 5, 2, 1)
        assert canvas.get_pixel(5, 5) is False
        assert canvas.get_pixel(6, 5) is True


class TestBlit:
    """Test canvas blitting."""

    def test_blit_copies_pixels(self):
        """Blit copies source canvas pixels."""
        source = Canvas(width=10, height=10)
        source.set_pixel(0, 0, True)
        source.set_pixel(5, 5, True)

        dest = Canvas()
        dest.blit(source, 20, 20)

        assert dest.get_pixel(20, 20) is True
        assert dest.get_pixel(25, 25) is True
        assert dest.get_pixel(21, 21) is False


class TestSerialization:
    """Test buffer serialization."""

    def test_to_bytes(self):
        """to_bytes returns correct framebuffer."""
        canvas = Canvas()
        canvas.set_pixel(0, 0, True)
        data = canvas.to_bytes()
        assert isinstance(data, bytes)
        assert len(data) == Canvas.FRAMEBUFFER_SIZE
        assert data[0] == 0x01

    def test_from_bytes(self):
        """from_bytes loads framebuffer correctly."""
        canvas = Canvas()
        data = bytes([0x01] + [0] * (Canvas.FRAMEBUFFER_SIZE - 1))
        canvas.from_bytes(data)
        assert canvas.get_pixel(0, 0) is True
        assert canvas.get_pixel(1, 0) is False

    def test_from_bytes_truncates_long_data(self):
        """from_bytes handles oversized data."""
        canvas = Canvas()
        data = bytes([0xFF] * 2000)
        canvas.from_bytes(data)
        assert len(canvas._buffer) == Canvas.FRAMEBUFFER_SIZE

    def test_from_bytes_pads_short_data(self):
        """from_bytes handles undersized data."""
        canvas = Canvas()
        data = bytes([0xFF] * 100)
        canvas.from_bytes(data)
        assert len(canvas._buffer) == Canvas.FRAMEBUFFER_SIZE
        assert canvas._buffer[99] == 0xFF
        assert canvas._buffer[100] == 0x00
