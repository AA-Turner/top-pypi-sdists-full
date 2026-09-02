use crate::{Result, TerminalError, TerminalRenderer};
use ratatui::{backend::TestBackend, buffer::Buffer, layout::Rect, Terminal};

/// Ratatui-based renderer that uses TestBackend as a layout engine
/// and fontdue for pixel rendering to JPEG.
///
/// TestBackend is used intentionally: we want ratatui's layout/widget engine
/// to produce a structured cell buffer, which we then render to pixels using
/// the existing fontdue pipeline (TerminalRenderer).
pub struct RatatuiRenderer {
    pub terminal: Terminal<TestBackend>,
    pub font_renderer: TerminalRenderer,
    /// Buffer snapshot from the previous render, used for dirty row detection.
    prev_buffer: Option<Buffer>,
}

impl RatatuiRenderer {
    pub fn new(cols: u16, rows: u16, char_width: u32, char_height: u32) -> Result<Self> {
        let backend = TestBackend::new(cols, rows);
        let terminal =
            Terminal::new(backend).map_err(|e| TerminalError::RenderError(e.to_string()))?;
        let font_size = char_height as f32 * 0.70;
        let font_renderer =
            TerminalRenderer::new_with_dimensions(char_width, char_height, font_size)?;
        Ok(Self {
            terminal,
            font_renderer,
            prev_buffer: None,
        })
    }

    pub fn resize(&mut self, cols: u16, rows: u16) -> Result<()> {
        self.prev_buffer = None; // invalidate on resize — next render is always full
        self.terminal.backend_mut().resize(cols, rows);
        self.terminal
            .resize(Rect::new(0, 0, cols, rows))
            .map_err(|e| TerminalError::RenderError(e.to_string()))
    }

    /// Full-screen render. Updates the prev_buffer snapshot.
    pub fn render_to_jpeg(&mut self, quality: u8) -> Result<Vec<u8>> {
        let buffer = self.terminal.backend().buffer();
        let jpeg = self.font_renderer.render_ratatui_buffer(buffer, quality)?;
        // Reuse existing Vec allocation when dimensions match; only reallocate on first
        // render or after resize. Vec::clone_from copies in-place without reallocating.
        if let Some(prev) = &mut self.prev_buffer {
            if prev.area == buffer.area {
                prev.content.clone_from(&buffer.content);
                return Ok(jpeg);
            }
        }
        self.prev_buffer = Some(buffer.clone());
        Ok(jpeg)
    }

    /// Find the bounding row range that changed since the last render.
    ///
    /// Returns `(min_dirty_row, max_dirty_row)`. If no previous snapshot exists
    /// (first render, or after a resize) returns the full row range so the caller
    /// always does a full-screen render.
    pub fn find_dirty_rows(&self) -> (u16, u16) {
        let cur = self.terminal.backend().buffer();
        let total_rows = cur.area.height.saturating_sub(1);

        let Some(prev) = &self.prev_buffer else {
            return (0, total_rows);
        };

        // Different dimensions → full screen
        if prev.area != cur.area {
            return (0, total_rows);
        }

        let width = cur.area.width as usize;
        let height = cur.area.height as usize;
        let mut min_row = height;
        let mut max_row = 0usize;

        for row in 0..height {
            let base = row * width;
            for col in 0..width {
                let idx = base + col;
                if prev.content[idx] != cur.content[idx] {
                    if row < min_row {
                        min_row = row;
                    }
                    if row > max_row {
                        max_row = row;
                    }
                    break; // one dirty cell in this row is enough
                }
            }
        }

        if min_row > max_row {
            // Nothing changed — return an empty sentinel (min > max means "no dirty rows")
            return (1, 0);
        }

        (min_row as u16, max_row as u16)
    }

    /// Render only `min_row..=max_row` to JPEG. Updates prev_buffer.
    ///
    /// Returns `(jpeg_bytes, y_px_offset)`.
    pub fn render_region_to_jpeg(
        &mut self,
        min_row: u16,
        max_row: u16,
        quality: u8,
    ) -> Result<(Vec<u8>, u32)> {
        let buffer = self.terminal.backend().buffer();
        let result = self
            .font_renderer
            .render_ratatui_region(buffer, min_row, max_row, quality)?;
        if let Some(prev) = &mut self.prev_buffer {
            if prev.area == buffer.area {
                prev.content.clone_from(&buffer.content);
                return Ok(result);
            }
        }
        self.prev_buffer = Some(buffer.clone());
        Ok(result)
    }
}
