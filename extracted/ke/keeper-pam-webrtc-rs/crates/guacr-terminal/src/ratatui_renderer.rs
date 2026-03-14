use crate::{Result, TerminalError, TerminalRenderer};
use ratatui::{backend::TestBackend, layout::Rect, Terminal};

/// Ratatui-based renderer that uses TestBackend as a layout engine
/// and fontdue for pixel rendering to JPEG.
///
/// TestBackend is used intentionally: we want ratatui's layout/widget engine
/// to produce a structured cell buffer, which we then render to pixels using
/// the existing fontdue pipeline (TerminalRenderer).
pub struct RatatuiRenderer {
    pub terminal: Terminal<TestBackend>,
    pub font_renderer: TerminalRenderer,
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
        })
    }

    pub fn resize(&mut self, cols: u16, rows: u16) -> Result<()> {
        // Resize the backend first so that Terminal::draw()'s autoresize()
        // query returns the new size and doesn't revert our resize.
        self.terminal.backend_mut().resize(cols, rows);
        self.terminal
            .resize(Rect::new(0, 0, cols, rows))
            .map_err(|e| TerminalError::RenderError(e.to_string()))
    }

    pub fn render_to_jpeg(&self, quality: u8) -> Result<Vec<u8>> {
        let buffer = self.terminal.backend().buffer();
        self.font_renderer.render_ratatui_buffer(buffer, quality)
    }
}
