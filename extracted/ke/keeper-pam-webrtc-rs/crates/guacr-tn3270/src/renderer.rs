// TN3270 screen renderer
//
// Converts a ScreenBuffer directly to a ratatui::buffer::Buffer (no ANSI
// round-trip) and renders to JPEG via TerminalRenderer::render_ratatui_buffer.

use crate::datastream::Color3270;
use crate::screen::{Highlight3270, ScreenBuffer};
use guacr_terminal::TerminalError;
use ratatui::{
    buffer::Buffer,
    layout::Rect,
    style::{Color, Modifier, Style},
};

fn color3270(color: Color3270, is_fg: bool) -> Color {
    match color {
        Color3270::Default => {
            if is_fg {
                Color::Green
            } else {
                Color::Black
            }
        }
        Color3270::Blue => Color::Blue,
        Color3270::Red => Color::Red,
        Color3270::Pink => Color::Magenta,
        Color3270::Green => Color::Green,
        Color3270::Turquoise => Color::Cyan,
        Color3270::Yellow => Color::Yellow,
        Color3270::White => Color::White,
    }
}

fn highlight_modifier(h: Highlight3270) -> Modifier {
    match h {
        Highlight3270::Normal => Modifier::empty(),
        Highlight3270::Blink => Modifier::SLOW_BLINK,
        Highlight3270::ReverseVideo => Modifier::REVERSED,
        Highlight3270::Underscore => Modifier::UNDERLINED,
        Highlight3270::Intensified => Modifier::BOLD,
    }
}

/// Build a ratatui buffer from a 3270 screen buffer.
///
/// Exposed for testing: callers can inspect individual cell symbols and styles
/// without decoding JPEG output.
pub fn screen_to_buffer(screen: &ScreenBuffer) -> Buffer {
    let cols = screen.cols();
    let rows = screen.rows();
    let mut buffer = Buffer::empty(Rect::new(0, 0, cols, rows));

    for row in 0..rows {
        for col in 0..cols {
            let Some(cell) = screen.get_cell(row, col) else {
                continue;
            };
            // Field attribute bytes display as blank; leave default space.
            if cell.attribute.field_attribute.is_some() {
                continue;
            }
            let ch = cell.character;
            if ch == '\0' {
                continue; // null = blank, default space already set
            }
            let idx = row as usize * cols as usize + col as usize;
            let rc = &mut buffer.content[idx];
            let mut ch_buf = [0u8; 4];
            rc.set_symbol(ch.encode_utf8(&mut ch_buf));
            rc.set_style(
                Style::default()
                    .fg(color3270(cell.attribute.foreground, true))
                    .bg(color3270(cell.attribute.background, false))
                    .add_modifier(highlight_modifier(cell.attribute.highlight)),
            );
        }
    }

    buffer
}

/// Render a 3270 screen buffer to a JPEG using a pre-created renderer.
///
/// Callers that render multiple frames should create the renderer once and reuse it.
pub fn render_with_renderer(
    screen: &ScreenBuffer,
    renderer: &guacr_terminal::TerminalRenderer,
    quality: u8,
) -> Result<Vec<u8>, TerminalError> {
    let buffer = screen_to_buffer(screen);
    renderer.render_ratatui_buffer(&buffer, quality)
}

/// Render a 3270 screen buffer to a JPEG using fontdue.
///
/// Character cell size is the same 9x18 used by all other handlers.
/// For repeated rendering (e.g. in a render loop), prefer creating a
/// `TerminalRenderer` once and calling `render_with_renderer` instead.
pub fn render_to_jpeg(
    screen: &ScreenBuffer,
    char_width: u32,
    char_height: u32,
    quality: u8,
) -> Result<Vec<u8>, TerminalError> {
    use guacr_terminal::TerminalRenderer;

    let buffer = screen_to_buffer(screen);
    let font_size = char_height as f32 * 0.70;
    let renderer = TerminalRenderer::new_with_dimensions(char_width, char_height, font_size)?;
    renderer.render_ratatui_buffer(&buffer, quality)
}
