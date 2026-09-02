// Convert a ratatui buffer to ANSI escape sequences for xterm.js rendering.
//
// Used by all ratatui-based protocol handlers (database, TN3270, TN5250) to
// produce terminal-data instructions instead of JPEG pixel output.

use ratatui::{
    buffer::Buffer,
    style::{Color, Modifier},
};

/// Convert a ratatui `Buffer` to ANSI escape sequences.
///
/// Produces a byte sequence that xterm.js (or any VT100 terminal) can render
/// directly. Emits SGR color/style codes only when they change between cells,
/// keeping output compact. Rows are separated by `\r\n`.
///
/// Starts with `\x1b[H` (cursor home) so subsequent renders repaint in place
/// without a full clear. xterm.js handles the display state.
pub fn buffer_to_ansi(buffer: &Buffer) -> Vec<u8> {
    let area = buffer.area();
    let mut out = Vec::with_capacity((area.width as usize * area.height as usize) * 10);

    out.extend_from_slice(b"\x1b[H");

    let mut prev_fg = Color::Reset;
    let mut prev_bg = Color::Reset;
    let mut prev_modifier = Modifier::empty();

    for y in 0..area.height {
        for x in 0..area.width {
            let default_cell = ratatui::buffer::Cell::default();
            let cell = buffer.cell((x, y)).unwrap_or(&default_cell);

            if cell.fg != prev_fg || cell.bg != prev_bg || cell.modifier != prev_modifier {
                out.extend_from_slice(b"\x1b[0m");
                let fg = color_to_ansi(cell.fg, true);
                if !fg.is_empty() {
                    out.extend_from_slice(fg.as_bytes());
                }
                let bg = color_to_ansi(cell.bg, false);
                if !bg.is_empty() {
                    out.extend_from_slice(bg.as_bytes());
                }
                if cell.modifier.contains(Modifier::BOLD) {
                    out.extend_from_slice(b"\x1b[1m");
                }
                if cell.modifier.contains(Modifier::UNDERLINED) {
                    out.extend_from_slice(b"\x1b[4m");
                }
                if cell.modifier.contains(Modifier::DIM) {
                    out.extend_from_slice(b"\x1b[2m");
                }
                if cell.modifier.contains(Modifier::REVERSED) {
                    out.extend_from_slice(b"\x1b[7m");
                }
                if cell.modifier.contains(Modifier::SLOW_BLINK) {
                    out.extend_from_slice(b"\x1b[5m");
                }
                prev_fg = cell.fg;
                prev_bg = cell.bg;
                prev_modifier = cell.modifier;
            }

            out.extend_from_slice(cell.symbol().as_bytes());
        }
        if y < area.height - 1 {
            out.extend_from_slice(b"\r\n");
        }
    }
    out.extend_from_slice(b"\x1b[0m"); // reset styles
    out.extend_from_slice(b"\x1b[J"); // erase from cursor to end-of-screen (removes stale rows after resize)
    out
}

fn color_to_ansi(color: Color, fg: bool) -> String {
    let (basic, truecolor) = if fg { (30u8, 38u8) } else { (40u8, 48u8) };
    match color {
        Color::Reset => String::new(),
        Color::Black => format!("\x1b[{}m", basic),
        Color::Red => format!("\x1b[{}m", basic + 1),
        Color::Green => format!("\x1b[{}m", basic + 2),
        Color::Yellow => format!("\x1b[{}m", basic + 3),
        Color::Blue => format!("\x1b[{}m", basic + 4),
        Color::Magenta => format!("\x1b[{}m", basic + 5),
        Color::Cyan => format!("\x1b[{}m", basic + 6),
        Color::White => format!("\x1b[{}m", basic + 7),
        Color::Gray => format!("\x1b[{}m", basic + 7),
        Color::DarkGray => format!("\x1b[{}m", basic + 60),
        Color::LightRed => format!("\x1b[{}m", basic + 61),
        Color::LightGreen => format!("\x1b[{}m", basic + 62),
        Color::LightYellow => format!("\x1b[{}m", basic + 63),
        Color::LightBlue => format!("\x1b[{}m", basic + 64),
        Color::LightMagenta => format!("\x1b[{}m", basic + 65),
        Color::LightCyan => format!("\x1b[{}m", basic + 66),
        Color::Rgb(r, g, b) => format!("\x1b[{};2;{};{};{}m", truecolor, r, g, b),
        Color::Indexed(n) => format!("\x1b[{};5;{}m", truecolor, n),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ratatui::{backend::TestBackend, Terminal};

    #[test]
    fn test_starts_with_cursor_home() {
        let backend = TestBackend::new(5, 2);
        let mut term = Terminal::new(backend).unwrap();
        term.draw(|_| {}).unwrap();
        let ansi = buffer_to_ansi(term.backend().buffer());
        assert!(ansi.starts_with(b"\x1b[H"));
    }

    #[test]
    fn test_ends_with_erase() {
        // buffer_to_ansi ends with \x1b[0m (style reset) followed by \x1b[J
        // (erase from cursor to end of screen, clears stale rows after resize).
        let backend = TestBackend::new(5, 2);
        let mut term = Terminal::new(backend).unwrap();
        term.draw(|_| {}).unwrap();
        let ansi = buffer_to_ansi(term.backend().buffer());
        assert!(
            ansi.ends_with(b"\x1b[J"),
            "should end with erase-to-end sequence"
        );
        assert!(
            ansi.windows(4).any(|w| w == b"\x1b[0m"),
            "should contain style reset"
        );
    }

    #[test]
    fn test_row_separator_count() {
        let backend = TestBackend::new(5, 3);
        let mut term = Terminal::new(backend).unwrap();
        term.draw(|_| {}).unwrap();
        let ansi = buffer_to_ansi(term.backend().buffer());
        let separators = ansi.windows(2).filter(|w| *w == b"\r\n").count();
        // 3 rows → 2 separators
        assert_eq!(separators, 2);
    }

    #[test]
    fn test_color_reset_is_empty() {
        assert_eq!(color_to_ansi(Color::Reset, true), "");
        assert_eq!(color_to_ansi(Color::Reset, false), "");
    }

    #[test]
    fn test_basic_colors_fg() {
        assert_eq!(color_to_ansi(Color::Red, true), "\x1b[31m");
        assert_eq!(color_to_ansi(Color::Green, true), "\x1b[32m");
    }

    #[test]
    fn test_rgb_color() {
        assert_eq!(
            color_to_ansi(Color::Rgb(255, 128, 0), true),
            "\x1b[38;2;255;128;0m"
        );
        assert_eq!(
            color_to_ansi(Color::Rgb(255, 128, 0), false),
            "\x1b[48;2;255;128;0m"
        );
    }

    #[test]
    fn test_reversed_modifier_emitted() {
        use ratatui::{layout::Rect, style::Style, widgets::Paragraph};
        let backend = TestBackend::new(3, 1);
        let mut term = Terminal::new(backend).unwrap();
        term.draw(|f| {
            let p = Paragraph::new("X").style(Style::default().add_modifier(Modifier::REVERSED));
            f.render_widget(p, Rect::new(0, 0, 3, 1));
        })
        .unwrap();
        let ansi = buffer_to_ansi(term.backend().buffer());
        assert!(
            ansi.windows(4).any(|w| w == b"\x1b[7m"),
            "REVERSED modifier should emit \\x1b[7m"
        );
    }
}
