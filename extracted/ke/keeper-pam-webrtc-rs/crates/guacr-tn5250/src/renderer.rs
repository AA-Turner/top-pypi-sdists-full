// TN5250 screen renderer
//
// Converts a ScreenBuffer5250 directly to a ratatui::buffer::Buffer and
// renders to JPEG via TerminalRenderer::render_ratatui_buffer.

use crate::screen::{Color5250, ScreenBuffer5250};
use guacr_terminal::TerminalError;
use ratatui::{
    buffer::Buffer,
    layout::Rect,
    style::{Color, Modifier, Style},
};

fn color5250(color: Color5250) -> Color {
    match color {
        Color5250::Black => Color::Black,
        Color5250::Green => Color::Green,
        Color5250::White => Color::White,
        Color5250::Red => Color::Red,
        Color5250::Blue => Color::Blue,
        Color5250::Turquoise => Color::Cyan,
        Color5250::Yellow => Color::Yellow,
        Color5250::Pink => Color::Magenta,
    }
}

/// Build a ratatui buffer from a 5250 screen buffer.
///
/// Exposed for testing: callers can inspect individual cell symbols and styles
/// without decoding JPEG output.
pub fn screen_to_buffer(screen: &ScreenBuffer5250) -> Buffer {
    let cols = screen.cols();
    let rows = screen.rows();
    let mut buffer = Buffer::empty(Rect::new(0, 0, cols, rows));

    for row in 0..rows {
        for col in 0..cols {
            let Some(cell) = screen.get_cell(row, col) else {
                continue;
            };
            if cell.field_start {
                continue;
            }
            let ch = cell.character;
            if ch == '\0' || ch == ' ' {
                if cell.foreground != Color5250::Green || cell.background != Color5250::Black {
                    let idx = row as usize * cols as usize + col as usize;
                    buffer.content[idx].set_style(
                        Style::default()
                            .fg(color5250(cell.foreground))
                            .bg(color5250(cell.background)),
                    );
                }
                continue;
            }
            let idx = row as usize * cols as usize + col as usize;
            let rc = &mut buffer.content[idx];
            let mut ch_buf = [0u8; 4];
            rc.set_symbol(ch.encode_utf8(&mut ch_buf));
            let mut modifier = Modifier::empty();
            if cell.underline {
                modifier |= Modifier::UNDERLINED;
            }
            rc.set_style(
                Style::default()
                    .fg(color5250(cell.foreground))
                    .bg(color5250(cell.background))
                    .add_modifier(modifier),
            );
        }
    }

    buffer
}

/// Render a 5250 screen buffer to a JPEG using fontdue.
pub fn render_to_jpeg(
    screen: &ScreenBuffer5250,
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
