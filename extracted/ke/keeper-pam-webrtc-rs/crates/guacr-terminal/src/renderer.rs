use crate::config::ColorScheme;
use crate::Result;
use fontdue::{Font, FontSettings};
use guacr_protocol::{format_cfill, format_instruction, format_rect, format_transfer};
use image::{Rgb, RgbImage};

// Primary font: JetBrains Mono (SIL Open Font License 1.1)
// Purpose-built for code/terminal: distinct l/1/I, 0/O, better hinting at small sizes.
// ~267KB vs ~580KB for Noto Sans Mono.
const FONT_DATA_PRIMARY: &[u8] = include_bytes!("../fonts/JetBrainsMono-Regular.ttf");

// Fallback font: DejaVu Sans Mono (Bitstream Vera license - permissive)
// Broader Unicode coverage including mathematical/technical symbols and box drawing.
// This matches guacd's behavior which requires dejavu-sans-mono-fonts.
const FONT_DATA_FALLBACK: &[u8] = include_bytes!("../fonts/DejaVuSansMono.ttf");

/// Terminal renderer - converts terminal screen to JPEG images or Guacamole instructions
///
/// Uses fontdue for actual text rendering with font fallback support.
/// Primary font is JetBrains Mono; falls back to DejaVu Sans Mono for missing glyphs.
/// Character cell dimensions and font size are calculated dynamically based on screen size.
/// JPEG encoding is used for fast rendering with minimal visual loss.
pub struct TerminalRenderer {
    char_width: u32,
    char_height: u32,
    font_size: f32,
    /// Primary font (JetBrains Mono)
    font_primary: Font,
    /// Fallback font (DejaVu Sans Mono) for broader Unicode coverage
    font_fallback: Font,
    /// Color scheme for terminal rendering
    color_scheme: ColorScheme,
}

impl TerminalRenderer {
    /// Create a new renderer with default dimensions
    ///
    /// Uses 19x38 pixel cells with 28pt font (legacy defaults for backward compatibility)
    pub fn new() -> Result<Self> {
        Self::new_with_dimensions(19, 38, 28.0)
    }

    /// Create a new renderer with specific character cell dimensions
    ///
    /// This allows dynamic sizing based on screen resolution and terminal dimensions.
    ///
    /// # Arguments
    ///
    /// * `char_width` - Width of each character cell in pixels
    /// * `char_height` - Height of each character cell in pixels
    /// * `font_size` - Font size in points (typically 70-75% of char_height for good fit)
    ///
    /// # Example
    ///
    /// ```
    /// use guacr_terminal::TerminalRenderer;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// // For 1920x1080 screen with 80x24 terminal:
    /// let char_width = 1920 / 80;  // = 24px
    /// let char_height = 1080 / 24; // = 45px
    /// let font_size = char_height as f32 * 0.70; // = 31.5pt
    /// let renderer = TerminalRenderer::new_with_dimensions(char_width, char_height, font_size)?;
    /// # Ok(())
    /// # }
    /// ```
    pub fn new_with_dimensions(char_width: u32, char_height: u32, font_size: f32) -> Result<Self> {
        Self::new_with_dimensions_and_scheme(
            char_width,
            char_height,
            font_size,
            ColorScheme::default(),
        )
    }

    /// Create a new renderer with specific dimensions and color scheme
    ///
    /// # Arguments
    ///
    /// * `char_width` - Width of each character cell in pixels
    /// * `char_height` - Height of each character cell in pixels
    /// * `font_size` - Font size in points (typically 70-75% of char_height for good fit)
    /// * `color_scheme` - Color scheme for terminal rendering
    pub fn new_with_dimensions_and_scheme(
        char_width: u32,
        char_height: u32,
        font_size: f32,
        color_scheme: ColorScheme,
    ) -> Result<Self> {
        // FontSettings::default() uses scale=40.0 which pre-hints at a common terminal
        // size for sharper glyphs. Fontdue always applies TrueType hinting.
        let font_primary =
            Font::from_bytes(FONT_DATA_PRIMARY, FontSettings::default()).map_err(|e| {
                crate::TerminalError::FontError(format!(
                    "Failed to load primary font (JetBrains Mono): {}",
                    e
                ))
            })?;

        let font_fallback =
            Font::from_bytes(FONT_DATA_FALLBACK, FontSettings::default()).map_err(|e| {
                crate::TerminalError::FontError(format!(
                    "Failed to load fallback font (DejaVu Sans Mono): {}",
                    e
                ))
            })?;

        Ok(Self {
            char_width,
            char_height,
            font_size,
            font_primary,
            font_fallback,
            color_scheme,
        })
    }

    /// Check if a character has a renderable glyph in the given font
    ///
    /// Returns true if the font can render this character (has non-zero width glyph)
    fn has_glyph(font: &Font, c: char, font_size: f32) -> bool {
        let (metrics, _) = font.rasterize(c, font_size);
        metrics.width > 0
    }

    /// Get the best font for rendering a character
    ///
    /// Tries primary font first, falls back to DejaVu Sans Mono for missing glyphs.
    /// This matches guacd's behavior which uses Pango with system font fallback.
    fn get_font_for_char(&self, c: char) -> &Font {
        if Self::has_glyph(&self.font_primary, c, self.font_size) {
            &self.font_primary
        } else if Self::has_glyph(&self.font_fallback, c, self.font_size) {
            &self.font_fallback
        } else {
            // Neither font has the glyph - return primary (will show placeholder)
            &self.font_primary
        }
    }

    /// Get the current color scheme
    pub fn color_scheme(&self) -> &ColorScheme {
        &self.color_scheme
    }

    /// Set the color scheme
    pub fn set_color_scheme(&mut self, scheme: ColorScheme) {
        self.color_scheme = scheme;
    }

    /// Render terminal screen to JPEG
    ///
    /// Renders at exact pixel dimensions, padding if necessary to match browser's layer size
    /// Uses default quality of 85
    pub fn render_screen(&self, screen: &vt100::Screen, rows: u16, cols: u16) -> Result<Vec<u8>> {
        self.render_screen_with_quality(screen, rows, cols, 85)
    }

    /// Render terminal screen with adaptive quality (for bandwidth optimization)
    ///
    /// Same as render_screen but allows specifying JPEG quality (10-100)
    pub fn render_screen_with_quality(
        &self,
        screen: &vt100::Screen,
        rows: u16,
        cols: u16,
        quality: u8,
    ) -> Result<Vec<u8>> {
        self.render_screen_with_size_and_quality(
            screen,
            rows,
            cols,
            cols as u32 * self.char_width,
            rows as u32 * self.char_height,
            quality,
        )
    }

    /// Render terminal screen blended with scrollback history.
    ///
    /// When `scroll_view` contains `Some(sb_idx)` for a row, that row is drawn from
    /// `scrollback[sb_idx]`. When it is `None`, the corresponding live-screen row is used.
    ///
    /// `scroll_view` must have exactly `rows as usize` entries (as returned by
    /// `TerminalEmulator::scroll_view_indices()`).
    pub fn render_screen_with_scrollback(
        &self,
        screen: &vt100::Screen,
        rows: u16,
        cols: u16,
        scrollback: &std::collections::VecDeque<crate::ScrollbackLine>,
        scroll_view: &[Option<usize>],
        quality: u8,
    ) -> crate::Result<Vec<u8>> {
        let width_px = cols as u32 * self.char_width;
        let height_px = rows as u32 * self.char_height;

        if width_px == 0 || height_px == 0 || rows == 0 || cols == 0 {
            return Err(crate::TerminalError::RenderError(format!(
                "Invalid render dimensions: {}x{} px ({}x{} chars)",
                width_px, height_px, cols, rows
            )));
        }

        let mut img = RgbImage::new(width_px, height_px);
        for pixel in img.pixels_mut() {
            *pixel = Rgb([0, 0, 0]);
        }

        // How many leading rows come from scrollback vs live screen
        let sb_rows = scroll_view.iter().filter(|e| e.is_some()).count();

        for (visible_row, sb_idx_opt) in scroll_view.iter().enumerate() {
            let y_px = visible_row as u32 * self.char_height;

            match sb_idx_opt {
                Some(sb_idx) => {
                    // Render from scrollback buffer
                    if let Some(line) = scrollback.get(*sb_idx) {
                        for col in 0..cols {
                            let x_px = col as u32 * self.char_width;
                            if let Some(cell) = line.cells.get(col as usize) {
                                self.render_cell(&mut img, cell, x_px, y_px, false)?;
                            }
                        }
                    }
                }
                None => {
                    // Render from live screen; this visible row maps to live_row
                    let live_row = (visible_row - sb_rows) as u16;
                    for col in 0..cols {
                        let x_px = col as u32 * self.char_width;
                        if let Some(cell) = screen.cell(live_row, col) {
                            // Show cursor only in live portion, at its actual position
                            let has_cursor = screen.cursor_position() == (live_row, col);
                            self.render_cell(&mut img, cell, x_px, y_px, has_cursor)?;
                        }
                    }
                }
            }
        }

        let mut jpeg_data = Vec::new();
        let mut encoder =
            image::codecs::jpeg::JpegEncoder::new_with_quality(&mut jpeg_data, quality);
        encoder.encode_image(&img)?;
        Ok(jpeg_data)
    }

    /// Render only a specific region of the terminal (dirty region optimization)
    ///
    /// This is the guacd optimization - only render changed portions of the screen
    /// Uses default quality of 85
    pub fn render_region(
        &self,
        screen: &vt100::Screen,
        min_row: u16,
        max_row: u16,
        min_col: u16,
        max_col: u16,
    ) -> Result<(Vec<u8>, u32, u32, u32, u32)> {
        self.render_region_with_quality(screen, min_row, max_row, min_col, max_col, 85)
    }

    /// Render region with adaptive quality (for bandwidth optimization)
    ///
    /// Same as render_region but allows specifying JPEG quality (10-100)
    pub fn render_region_with_quality(
        &self,
        screen: &vt100::Screen,
        min_row: u16,
        max_row: u16,
        min_col: u16,
        max_col: u16,
        quality: u8,
    ) -> Result<(Vec<u8>, u32, u32, u32, u32)> {
        let width = (max_col - min_col + 1) as u32;
        let height = (max_row - min_row + 1) as u32;
        let width_px = width * self.char_width;
        let height_px = height * self.char_height;

        let mut img = RgbImage::new(width_px, height_px);

        // Background (black)
        for pixel in img.pixels_mut() {
            *pixel = Rgb([0, 0, 0]);
        }

        // Render each cell in the region
        for row in min_row..=max_row {
            for col in min_col..=max_col {
                let x = (col - min_col) as u32;
                let y = (row - min_row) as u32;
                let x_px = x * self.char_width;
                let y_px = y * self.char_height;

                if let Some(cell) = screen.cell(row, col) {
                    let has_cursor = screen.cursor_position() == (row, col);
                    self.render_cell(&mut img, cell, x_px, y_px, has_cursor)?;
                }
            }
        }

        // JPEG encoding with specified quality (10-100)
        // Higher quality = better text clarity but larger file size
        // Lower quality = smaller bandwidth usage for slow connections
        let mut jpeg_data = Vec::new();
        let mut encoder =
            image::codecs::jpeg::JpegEncoder::new_with_quality(&mut jpeg_data, quality);
        encoder.encode_image(&img)?;

        // Return JPEG + position info (x, y in pixels)
        let x_px = min_col as u32 * self.char_width;
        let y_px = min_row as u32 * self.char_height;
        Ok((jpeg_data, x_px, y_px, width_px, height_px))
    }

    /// Render terminal screen to JPEG with exact pixel dimensions
    ///
    /// This version allows specifying exact output dimensions, useful for
    /// matching browser layer size exactly. Uses default quality of 85.
    pub fn render_screen_with_size(
        &self,
        screen: &vt100::Screen,
        rows: u16,
        cols: u16,
        width_px: u32,
        height_px: u32,
    ) -> Result<Vec<u8>> {
        self.render_screen_with_size_and_quality(screen, rows, cols, width_px, height_px, 85)
    }

    /// Render terminal screen with exact dimensions and adaptive quality
    ///
    /// Allows full control over output dimensions and JPEG quality (10-100)
    pub fn render_screen_with_size_and_quality(
        &self,
        screen: &vt100::Screen,
        rows: u16,
        cols: u16,
        width_px: u32,
        height_px: u32,
        quality: u8,
    ) -> Result<Vec<u8>> {
        // CRITICAL: Prevent rendering zero-size images (causes black screen)
        if width_px == 0 || height_px == 0 || rows == 0 || cols == 0 {
            return Err(crate::TerminalError::RenderError(format!(
                "Invalid render dimensions: {}x{} px ({}x{} chars)",
                width_px, height_px, cols, rows
            )));
        }

        let mut img = RgbImage::new(width_px, height_px);

        // Background (black)
        for pixel in img.pixels_mut() {
            *pixel = Rgb([0, 0, 0]);
        }

        // Render each cell
        for row in 0..rows {
            for col in 0..cols {
                let x_px = col as u32 * self.char_width;
                let y_px = row as u32 * self.char_height;

                // Skip if outside image bounds
                if x_px >= width_px || y_px >= height_px {
                    continue;
                }

                if let Some(cell) = screen.cell(row, col) {
                    let has_cursor = screen.cursor_position() == (row, col);
                    self.render_cell(&mut img, cell, x_px, y_px, has_cursor)?;
                }
            }
        }

        // JPEG encoding with specified quality (10-100)
        // Higher quality = better text clarity but larger file size
        // Lower quality = smaller bandwidth usage for slow connections
        let mut jpeg_data = Vec::new();
        let mut encoder =
            image::codecs::jpeg::JpegEncoder::new_with_quality(&mut jpeg_data, quality);
        encoder.encode_image(&img)?;

        Ok(jpeg_data)
    }

    fn render_cell(
        &self,
        img: &mut RgbImage,
        cell: &vt100::Cell,
        x: u32,
        y: u32,
        has_cursor: bool,
    ) -> Result<()> {
        let bg = self.vt100_color_to_rgb(cell.bgcolor(), false);
        let fg = self.vt100_color_to_rgb(cell.fgcolor(), true);
        self.render_glyph_at(img, &cell.contents(), fg, bg, x, y)?;
        if has_cursor {
            self.draw_cursor(img, x, y)?;
        }
        Ok(())
    }

    /// Render a character cell to the image buffer.
    ///
    /// Shared by render_cell (vt100) and render_ratatui_cell (ratatui).
    /// Callers extract the symbol and colors from their respective cell types,
    /// then delegate here for the background fill + glyph rendering.
    fn render_glyph_at(
        &self,
        img: &mut RgbImage,
        symbol: &str,
        fg: Rgb<u8>,
        bg: Rgb<u8>,
        x: u32,
        y: u32,
    ) -> Result<()> {
        // Fill cell background
        for py in y..(y + self.char_height).min(img.height()) {
            for px in x..(x + self.char_width).min(img.width()) {
                img.put_pixel(px, py, bg);
            }
        }

        if let Some(c) = symbol.chars().next() {
            if c != ' ' && c != '\0' {
                // Box drawing characters (U+2500–U+257F): render manually for crispness
                if Self::is_box_drawing_char(c) {
                    self.render_box_drawing_char(img, c, x, y, fg)?;
                    return Ok(());
                }

                // Block elements (U+2580–U+259F): often missing from fonts, render as rectangles
                if let Some(block_region) = Self::get_block_character_region(c) {
                    let (x_start, y_start, x_end, y_end) = block_region;
                    let x0 = x + (self.char_width as f32 * x_start) as u32;
                    let y0 = y + (self.char_height as f32 * y_start) as u32;
                    let x1 = x + (self.char_width as f32 * x_end) as u32;
                    let y1 = y + (self.char_height as f32 * y_end) as u32;
                    for py in y0..y1.min(img.height()) {
                        for px in x0..x1.min(img.width()) {
                            img.put_pixel(px, py, fg);
                        }
                    }
                    return Ok(());
                }

                let font = self.get_font_for_char(c);
                let (metrics, bitmap) = font.rasterize(c, self.font_size);

                // Missing glyph: render a small placeholder rectangle
                if bitmap.is_empty() && metrics.width == 0 {
                    let margin_x = self.char_width / 4;
                    let margin_y = self.char_height / 4;
                    for py in (y + margin_y)..(y + self.char_height - margin_y).min(img.height()) {
                        for px in (x + margin_x)..(x + self.char_width - margin_x).min(img.width())
                        {
                            img.put_pixel(px, py, fg);
                        }
                    }
                    return Ok(());
                }

                // Baseline at 75% of cell height (standard terminal practice)
                const BASELINE_RATIO: f32 = 0.75;
                let glyph_x =
                    x + ((self.char_width as i32 - metrics.width as i32) / 2).max(0) as u32;
                // Fixed integer baseline; glyph top = baseline - (ymin + height).
                // metrics.ymin is the signed pixel offset of the bitmap bottom from the
                // baseline (negative = below). metrics.height is the integer bitmap height.
                // This is the correct integer form of the fontdue placement formula and
                // produces consistent per-character alignment regardless of descenders.
                let baseline_y = (y + (self.char_height as f32 * BASELINE_RATIO) as u32) as i32;
                let glyph_y =
                    (baseline_y - metrics.ymin - metrics.height as i32).max(y as i32) as u32;

                for (i, &alpha) in bitmap.iter().enumerate() {
                    if alpha > 0 {
                        let dx = (i % metrics.width) as u32;
                        let dy = (i / metrics.width) as u32;
                        let px = glyph_x + dx;
                        let py = glyph_y + dy;
                        if px < img.width() && py < img.height() {
                            let alpha_f = alpha as f32 / 255.0;
                            let current = img.get_pixel(px, py);
                            let blended = Rgb([
                                ((fg.0[0] as f32 * alpha_f)
                                    + (current.0[0] as f32 * (1.0 - alpha_f)))
                                    as u8,
                                ((fg.0[1] as f32 * alpha_f)
                                    + (current.0[1] as f32 * (1.0 - alpha_f)))
                                    as u8,
                                ((fg.0[2] as f32 * alpha_f)
                                    + (current.0[2] as f32 * (1.0 - alpha_f)))
                                    as u8,
                            ]);
                            img.put_pixel(px, py, blended);
                        }
                    }
                }
            }
        }
        Ok(())
    }

    fn draw_cursor(&self, img: &mut RgbImage, x: u32, y: u32) -> Result<()> {
        // Draw cursor as underline (bottom 3 pixels of cell)
        let cursor_color = Rgb([255, 255, 255]);
        let cursor_height = 3;

        for dy in 0..cursor_height {
            for dx in 0..self.char_width {
                let px = x + dx;
                let py = y + self.char_height - dy - 1;
                if px < img.width() && py < img.height() {
                    img.put_pixel(px, py, cursor_color);
                }
            }
        }

        Ok(())
    }

    /// Check if character is a box drawing character (U+2500-U+257F)
    fn is_box_drawing_char(c: char) -> bool {
        matches!(c, '\u{2500}'..='\u{257F}')
    }

    /// Render box drawing character manually for consistency
    /// Box drawing characters (U+2500-U+257F) are lines, corners, and intersections
    fn render_box_drawing_char(
        &self,
        img: &mut RgbImage,
        c: char,
        x: u32,
        y: u32,
        color: Rgb<u8>,
    ) -> Result<()> {
        // Line thickness (1-2 pixels for crisp rendering)
        let thick = 1;

        // Calculate midpoints and edges
        let mid_x = x + self.char_width / 2;
        let mid_y = y + self.char_height / 2;
        let left = x;
        let right = x + self.char_width;
        let top = y;
        let bottom = y + self.char_height;

        // Helper to draw horizontal line
        let draw_h_line = |img: &mut RgbImage, y: u32, x1: u32, x2: u32| {
            for py in y.saturating_sub(thick / 2)..=(y + thick / 2).min(img.height() - 1) {
                for px in x1..x2.min(img.width()) {
                    img.put_pixel(px, py, color);
                }
            }
        };

        // Helper to draw vertical line
        let draw_v_line = |img: &mut RgbImage, x: u32, y1: u32, y2: u32| {
            for px in x.saturating_sub(thick / 2)..=(x + thick / 2).min(img.width() - 1) {
                for py in y1..y2.min(img.height()) {
                    img.put_pixel(px, py, color);
                }
            }
        };

        match c {
            // Horizontal lines
            '\u{2500}' | '\u{2501}' => draw_h_line(img, mid_y, left, right), // ─ ━
            // Vertical lines
            '\u{2502}' | '\u{2503}' => draw_v_line(img, mid_x, top, bottom), // │ ┃

            // Corners
            '\u{250C}' | '\u{250D}' | '\u{250E}' | '\u{250F}' => {
                // ┌ ┍ ┎ ┏
                draw_h_line(img, mid_y, mid_x, right);
                draw_v_line(img, mid_x, mid_y, bottom);
            }
            '\u{2510}' | '\u{2511}' | '\u{2512}' | '\u{2513}' => {
                // ┐ ┑ ┒ ┓
                draw_h_line(img, mid_y, left, mid_x);
                draw_v_line(img, mid_x, mid_y, bottom);
            }
            '\u{2514}' | '\u{2515}' | '\u{2516}' | '\u{2517}' => {
                // └ ┕ ┖ ┗
                draw_h_line(img, mid_y, mid_x, right);
                draw_v_line(img, mid_x, top, mid_y);
            }
            '\u{2518}' | '\u{2519}' | '\u{251A}' | '\u{251B}' => {
                // ┘ ┙ ┚ ┛
                draw_h_line(img, mid_y, left, mid_x);
                draw_v_line(img, mid_x, top, mid_y);
            }

            // T-junctions
            '\u{251C}' | '\u{251D}' | '\u{251E}' | '\u{251F}' | '\u{2520}' | '\u{2521}'
            | '\u{2522}' | '\u{2523}' => {
                // ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣
                draw_h_line(img, mid_y, mid_x, right);
                draw_v_line(img, mid_x, top, bottom);
            }
            '\u{2524}' | '\u{2525}' | '\u{2526}' | '\u{2527}' | '\u{2528}' | '\u{2529}'
            | '\u{252A}' | '\u{252B}' => {
                // ┤ ┥ ┦ ┧ ┨ ┩ ┪ ┫
                draw_h_line(img, mid_y, left, mid_x);
                draw_v_line(img, mid_x, top, bottom);
            }
            '\u{252C}' | '\u{252D}' | '\u{252E}' | '\u{252F}' | '\u{2530}' | '\u{2531}'
            | '\u{2532}' | '\u{2533}' => {
                // ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳
                draw_h_line(img, mid_y, left, right);
                draw_v_line(img, mid_x, mid_y, bottom);
            }
            '\u{2534}' | '\u{2535}' | '\u{2536}' | '\u{2537}' | '\u{2538}' | '\u{2539}'
            | '\u{253A}' | '\u{253B}' => {
                // ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻
                draw_h_line(img, mid_y, left, right);
                draw_v_line(img, mid_x, top, mid_y);
            }

            // Cross
            '\u{253C}' | '\u{253D}' | '\u{253E}' | '\u{253F}' | '\u{2540}' | '\u{2541}'
            | '\u{2542}' | '\u{2543}' | '\u{2544}' | '\u{2545}' | '\u{2546}' | '\u{2547}'
            | '\u{2548}' | '\u{2549}' | '\u{254A}' | '\u{254B}' => {
                // ┼ and variants
                draw_h_line(img, mid_y, left, right);
                draw_v_line(img, mid_x, top, bottom);
            }

            // For other box drawing chars, fall back to font rendering
            _ => {
                // Try font rendering for less common box drawing chars
                let font = self.get_font_for_char(c);
                let (metrics, bitmap) = font.rasterize(c, self.font_size);
                if !bitmap.is_empty() {
                    // Render using font — same baseline logic as the main render path
                    const BASELINE_RATIO: f32 = 0.75;
                    let glyph_x =
                        x + ((self.char_width as i32 - metrics.width as i32) / 2).max(0) as u32;
                    let baseline_y = (y + (self.char_height as f32 * BASELINE_RATIO) as u32) as i32;
                    let glyph_top =
                        (baseline_y - metrics.ymin - metrics.height as i32).max(y as i32) as u32;

                    for (i, &alpha) in bitmap.iter().enumerate() {
                        if alpha > 0 {
                            let gx = i % metrics.width;
                            let gy = i / metrics.width;
                            let px = glyph_x + gx as u32;
                            let py = glyph_top + gy as u32;

                            if px < img.width() && py < img.height() {
                                let alpha_f = alpha as f32 / 255.0;
                                let current = img.get_pixel(px, py);
                                let blended = Rgb([
                                    ((color.0[0] as f32 * alpha_f)
                                        + (current.0[0] as f32 * (1.0 - alpha_f)))
                                        as u8,
                                    ((color.0[1] as f32 * alpha_f)
                                        + (current.0[1] as f32 * (1.0 - alpha_f)))
                                        as u8,
                                    ((color.0[2] as f32 * alpha_f)
                                        + (current.0[2] as f32 * (1.0 - alpha_f)))
                                        as u8,
                                ]);
                                img.put_pixel(px, py, blended);
                            }
                        }
                    }
                }
            }
        }

        Ok(())
    }

    /// Returns the fill region (x_start, y_start, x_end, y_end) as fractions of cell size
    /// for Unicode block drawing characters (U+2580-U+259F).
    /// Returns None if the character is not a block element.
    fn get_block_character_region(c: char) -> Option<(f32, f32, f32, f32)> {
        match c {
            // Block Elements (U+2580-U+259F)
            '\u{2580}' => Some((0.0, 0.0, 1.0, 0.5)), // ▀ Upper half block
            '\u{2581}' => Some((0.0, 0.875, 1.0, 1.0)), // ▁ Lower one eighth block
            '\u{2582}' => Some((0.0, 0.75, 1.0, 1.0)), // ▂ Lower one quarter block
            '\u{2583}' => Some((0.0, 0.625, 1.0, 1.0)), // ▃ Lower three eighths block
            '\u{2584}' => Some((0.0, 0.5, 1.0, 1.0)), // ▄ Lower half block
            '\u{2585}' => Some((0.0, 0.375, 1.0, 1.0)), // ▅ Lower five eighths block
            '\u{2586}' => Some((0.0, 0.25, 1.0, 1.0)), // ▆ Lower three quarters block
            '\u{2587}' => Some((0.0, 0.125, 1.0, 1.0)), // ▇ Lower seven eighths block
            '\u{2588}' => Some((0.0, 0.0, 1.0, 1.0)), // █ Full block
            '\u{2589}' => Some((0.0, 0.0, 0.875, 1.0)), // ▉ Left seven eighths block
            '\u{258A}' => Some((0.0, 0.0, 0.75, 1.0)), // ▊ Left three quarters block
            '\u{258B}' => Some((0.0, 0.0, 0.625, 1.0)), // ▋ Left five eighths block
            '\u{258C}' => Some((0.0, 0.0, 0.5, 1.0)), // ▌ Left half block
            '\u{258D}' => Some((0.0, 0.0, 0.375, 1.0)), // ▍ Left three eighths block
            '\u{258E}' => Some((0.0, 0.0, 0.25, 1.0)), // ▎ Left one quarter block
            '\u{258F}' => Some((0.0, 0.0, 0.125, 1.0)), // ▏ Left one eighth block
            '\u{2590}' => Some((0.5, 0.0, 1.0, 1.0)), // ▐ Right half block
            '\u{2591}' => Some((0.0, 0.0, 1.0, 1.0)), // ░ Light shade (render as full for now)
            '\u{2592}' => Some((0.0, 0.0, 1.0, 1.0)), // ▒ Medium shade (render as full for now)
            '\u{2593}' => Some((0.0, 0.0, 1.0, 1.0)), // ▓ Dark shade (render as full for now)
            '\u{2594}' => Some((0.0, 0.0, 1.0, 0.125)), // ▔ Upper one eighth block
            '\u{2595}' => Some((0.875, 0.0, 1.0, 1.0)), // ▕ Right one eighth block
            '\u{2596}' => Some((0.0, 0.5, 0.5, 1.0)), // ▖ Quadrant lower left
            '\u{2597}' => Some((0.5, 0.5, 1.0, 1.0)), // ▗ Quadrant lower right
            '\u{2598}' => Some((0.0, 0.0, 0.5, 0.5)), // ▘ Quadrant upper left
            '\u{2599}' => Some((0.0, 0.0, 1.0, 1.0)), // ▙ Quadrant upper left and lower left and lower right (complex)
            '\u{259A}' => Some((0.0, 0.0, 1.0, 1.0)), // ▚ Quadrant upper left and lower right (complex)
            '\u{259B}' => Some((0.0, 0.0, 1.0, 1.0)), // ▛ Quadrant upper left and upper right and lower left (complex)
            '\u{259C}' => Some((0.0, 0.0, 1.0, 1.0)), // ▜ Quadrant upper left and upper right and lower right (complex)
            '\u{259D}' => Some((0.5, 0.0, 1.0, 0.5)), // ▝ Quadrant upper right
            '\u{259E}' => Some((0.0, 0.0, 1.0, 1.0)), // ▞ Quadrant upper right and lower left (complex)
            '\u{259F}' => Some((0.0, 0.0, 1.0, 1.0)), // ▟ Quadrant upper right and lower left and lower right (complex)
            _ => None,
        }
    }

    pub(crate) fn vt100_color_to_rgb(&self, color: vt100::Color, is_foreground: bool) -> Rgb<u8> {
        match color {
            vt100::Color::Default => {
                // Use color scheme for default colors
                if is_foreground {
                    Rgb(self.color_scheme.foreground)
                } else {
                    Rgb(self.color_scheme.background)
                }
            }
            vt100::Color::Idx(n) => {
                // Standard 16-color palette
                // For index 0 (black) and 7 (white), use color scheme if they match
                // the default foreground/background to maintain theme consistency
                match n {
                    0 => Rgb([0, 0, 0]),        // Black
                    1 => Rgb([205, 0, 0]),      // Red
                    2 => Rgb([0, 205, 0]),      // Green
                    3 => Rgb([205, 205, 0]),    // Yellow
                    4 => Rgb([0, 0, 238]),      // Blue
                    5 => Rgb([205, 0, 205]),    // Magenta
                    6 => Rgb([0, 205, 205]),    // Cyan
                    7 => Rgb([229, 229, 229]),  // White
                    8 => Rgb([127, 127, 127]),  // Bright Black
                    9 => Rgb([255, 0, 0]),      // Bright Red
                    10 => Rgb([0, 255, 0]),     // Bright Green
                    11 => Rgb([255, 255, 0]),   // Bright Yellow
                    12 => Rgb([92, 92, 255]),   // Bright Blue
                    13 => Rgb([255, 0, 255]),   // Bright Magenta
                    14 => Rgb([0, 255, 255]),   // Bright Cyan
                    15 => Rgb([255, 255, 255]), // Bright White
                    _ => Rgb([0, 0, 0]),        // Fallback
                }
            }
            vt100::Color::Rgb(r, g, b) => Rgb([r, g, b]),
        }
    }

    /// Generate Guacamole protocol instructions for drawing operations
    ///
    /// Note: This method uses drawing instructions instead of JPEG images.
    /// For this implementation, JPEG is preferred (5-10x faster than PNG).
    pub fn format_drawing_instructions(
        &self,
        screen: &vt100::Screen,
        rows: u16,
        cols: u16,
    ) -> Vec<String> {
        let mut instructions = Vec::new();

        // Clear screen
        instructions.push(format_rect(
            0,
            0,
            0,
            cols as u32 * self.char_width,
            rows as u32 * self.char_height,
        ));
        instructions.push(format_cfill(14, 0, 0, 0, 0, 255)); // Black background

        // Render each cell as colored rectangle (simplified)
        for row in 0..rows {
            for col in 0..cols {
                if let Some(cell) = screen.cell(row, col) {
                    let x = col as u32 * self.char_width;
                    let y = row as u32 * self.char_height;

                    let bg = self.vt100_color_to_rgb(cell.bgcolor(), false);

                    instructions.push(format_rect(0, x, y, self.char_width, self.char_height));
                    instructions.push(format_cfill(14, 0, bg.0[0], bg.0[1], bg.0[2], 255));
                }
            }
        }

        instructions
    }

    /// Format ready instruction
    pub fn format_ready_instruction(protocol: &str) -> String {
        format_instruction("ready", &[protocol])
    }

    /// Format size instruction
    pub fn format_size_instruction(layer: i32, width: u32, height: u32) -> String {
        format_instruction(
            "size",
            &[&layer.to_string(), &width.to_string(), &height.to_string()],
        )
    }

    /// Format sync instruction
    ///
    /// Format: `4.sync,{timestamp};`
    ///
    /// # Arguments
    /// - `timestamp_ms`: Timestamp in milliseconds
    pub fn format_sync_instruction(&self, timestamp_ms: u64) -> String {
        let timestamp_str = timestamp_ms.to_string();
        format_instruction("sync", &[&timestamp_str])
    }

    /// Format copy instruction (for scroll optimization)
    #[allow(clippy::too_many_arguments)]
    pub fn format_copy_instruction(
        src_row: u16,
        src_col: u16,
        width: u16,
        height: u16,
        dst_row: u16,
        dst_col: u16,
        char_width: u32,
        char_height: u32,
        layer: i32,
    ) -> String {
        // Copy instruction format: copy,<src_layer>,<src_x>,<src_y>,<width>,<height>,<dst_layer>,<dst_x>,<dst_y>;
        let src_x = src_col as u32 * char_width;
        let src_y = src_row as u32 * char_height;
        let width_px = width as u32 * char_width;
        let height_px = height as u32 * char_height;
        let dst_x = dst_col as u32 * char_width;
        let dst_y = dst_row as u32 * char_height;

        format_transfer(
            layer, src_x, src_y, width_px, height_px, 12, // SRC function
            layer, dst_x, dst_y,
        )
    }

    /// Format clear region instructions (for scroll optimization)
    pub fn format_clear_region_instructions(
        row: u16,
        col: u16,
        width: u16,
        height: u16,
        char_width: u32,
        char_height: u32,
    ) -> Vec<String> {
        let x = col as u32 * char_width;
        let y = row as u32 * char_height;
        let width_px = width as u32 * char_width;
        let height_px = height as u32 * char_height;

        vec![
            format_rect(0, x, y, width_px, height_px),
            format_cfill(14, 0, 0, 0, 0, 255), // Black background
        ]
    }

    /// Render a ratatui buffer to JPEG using fontdue
    ///
    /// Mirrors render_screen_with_size_and_quality() but reads from
    /// a ratatui::buffer::Buffer instead of a vt100::Screen.
    /// Render a row range of a ratatui buffer to JPEG.
    ///
    /// Returns `(jpeg_bytes, y_px_offset)` where `y_px_offset` is the pixel
    /// distance from the top of the screen to the start of the rendered region.
    /// Pass this as `y` in `format_img_instruction` for a partial update.
    pub fn render_ratatui_region(
        &self,
        buffer: &ratatui::buffer::Buffer,
        min_row: u16,
        max_row: u16,
        quality: u8,
    ) -> Result<(Vec<u8>, u32)> {
        let area = buffer.area;
        let region_rows = max_row - min_row + 1;
        let width_px = area.width as u32 * self.char_width;
        let height_px = region_rows as u32 * self.char_height;
        let y_px_offset = min_row as u32 * self.char_height;

        if width_px == 0 || height_px == 0 {
            return Err(crate::TerminalError::RenderError(format!(
                "Invalid region dimensions: {}x{} px (rows {}..={})",
                width_px, height_px, min_row, max_row
            )));
        }

        let mut img = RgbImage::new(width_px, height_px);
        for pixel in img.pixels_mut() {
            *pixel = Rgb([0, 0, 0]);
        }

        for row in min_row..=max_row {
            for col in 0..area.width {
                let idx = row as usize * area.width as usize + col as usize;
                if idx >= buffer.content.len() {
                    break;
                }
                let cell = &buffer.content[idx];
                let x_px = col as u32 * self.char_width;
                let y_px = (row - min_row) as u32 * self.char_height;
                self.render_ratatui_cell(&mut img, cell, x_px, y_px)?;
            }
        }

        let mut jpeg_data = Vec::new();
        let mut encoder =
            image::codecs::jpeg::JpegEncoder::new_with_quality(&mut jpeg_data, quality);
        encoder.encode_image(&img)?;
        Ok((jpeg_data, y_px_offset))
    }

    pub fn render_ratatui_buffer(
        &self,
        buffer: &ratatui::buffer::Buffer,
        quality: u8,
    ) -> Result<Vec<u8>> {
        let area = buffer.area;
        let width_px = area.width as u32 * self.char_width;
        let height_px = area.height as u32 * self.char_height;

        if width_px == 0 || height_px == 0 {
            return Err(crate::TerminalError::RenderError(format!(
                "Invalid render dimensions: {}x{} px ({}x{} chars)",
                width_px, height_px, area.width, area.height
            )));
        }

        let mut img = RgbImage::new(width_px, height_px);
        for pixel in img.pixels_mut() {
            *pixel = Rgb([0, 0, 0]);
        }

        for row in 0..area.height {
            for col in 0..area.width {
                let idx = row as usize * area.width as usize + col as usize;
                let cell = &buffer.content[idx];
                let x_px = col as u32 * self.char_width;
                let y_px = row as u32 * self.char_height;
                self.render_ratatui_cell(&mut img, cell, x_px, y_px)?;
            }
        }

        let mut jpeg_data = Vec::new();
        let mut encoder =
            image::codecs::jpeg::JpegEncoder::new_with_quality(&mut jpeg_data, quality);
        encoder.encode_image(&img)?;
        Ok(jpeg_data)
    }

    fn render_ratatui_cell(
        &self,
        img: &mut RgbImage,
        cell: &ratatui::buffer::Cell,
        x: u32,
        y: u32,
    ) -> Result<()> {
        let bg = self.ratatui_color_to_rgb(cell.bg, false);
        let fg = self.ratatui_color_to_rgb(cell.fg, true);
        self.render_glyph_at(img, cell.symbol(), fg, bg, x, y)
    }

    fn ratatui_color_to_rgb(&self, color: ratatui::style::Color, is_foreground: bool) -> Rgb<u8> {
        use ratatui::style::Color;
        match color {
            Color::Reset => {
                if is_foreground {
                    Rgb(self.color_scheme.foreground)
                } else {
                    Rgb(self.color_scheme.background)
                }
            }
            Color::Black => Rgb([0, 0, 0]),
            Color::Red => Rgb([205, 0, 0]),
            Color::Green => Rgb([0, 205, 0]),
            Color::Yellow => Rgb([205, 205, 0]),
            Color::Blue => Rgb([0, 0, 238]),
            Color::Magenta => Rgb([205, 0, 205]),
            Color::Cyan => Rgb([0, 205, 205]),
            Color::Gray => Rgb([229, 229, 229]),
            Color::DarkGray => Rgb([127, 127, 127]),
            Color::LightRed => Rgb([255, 0, 0]),
            Color::LightGreen => Rgb([0, 255, 0]),
            Color::LightYellow => Rgb([255, 255, 0]),
            Color::LightBlue => Rgb([92, 92, 255]),
            Color::LightMagenta => Rgb([255, 0, 255]),
            Color::LightCyan => Rgb([0, 255, 255]),
            Color::White => Rgb([255, 255, 255]),
            Color::Rgb(r, g, b) => Rgb([r, g, b]),
            Color::Indexed(i) => Self::xterm_256_color(i),
        }
    }

    fn xterm_256_color(index: u8) -> Rgb<u8> {
        match index {
            0 => Rgb([0, 0, 0]),
            1 => Rgb([205, 0, 0]),
            2 => Rgb([0, 205, 0]),
            3 => Rgb([205, 205, 0]),
            4 => Rgb([0, 0, 238]),
            5 => Rgb([205, 0, 205]),
            6 => Rgb([0, 205, 205]),
            7 => Rgb([229, 229, 229]),
            8 => Rgb([127, 127, 127]),
            9 => Rgb([255, 0, 0]),
            10 => Rgb([0, 255, 0]),
            11 => Rgb([255, 255, 0]),
            12 => Rgb([92, 92, 255]),
            13 => Rgb([255, 0, 255]),
            14 => Rgb([0, 255, 255]),
            15 => Rgb([255, 255, 255]),
            16..=231 => {
                let i = index - 16;
                let b = i % 6;
                let g = (i / 6) % 6;
                let r = i / 36;
                let scale = |v: u8| if v == 0 { 0 } else { 55 + v * 40 };
                Rgb([scale(r), scale(g), scale(b)])
            }
            232..=255 => {
                let v = 8 + (index - 232) * 10;
                Rgb([v, v, v])
            }
        }
    }
}
