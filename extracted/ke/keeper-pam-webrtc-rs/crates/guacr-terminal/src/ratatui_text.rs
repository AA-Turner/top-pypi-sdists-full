// Convert ratatui buffers to ANSI escape sequences for xterm.js rendering.
// Full redraws remain available to all ratatui-based protocol handlers.

use std::io::Write;

use ratatui::{
    backend::{Backend, TestBackend},
    buffer::{Buffer, Cell, CellWidth},
    style::{Color, Modifier},
};

/// Serialize a complete ratatui screen, including its foreground/background and modifiers.
/// Wide grapheme continuation cells are not printed, and rows are separated by CRLF.
/// Cursor addressing cancels pending right-margin wrapping without scrolling the screen.
pub fn buffer_to_ansi(buffer: &Buffer) -> Vec<u8> {
    let mut output = Vec::with_capacity(buffer.content.len().saturating_mul(4));
    write_full_screen(buffer, &mut output);
    output
}

/// Stateful cell-buffer serializer for database terminal-data output.
///
/// The first screen and any geometry change are full redraws. Later screens use ratatui's
/// buffer diff iterator, keeping both the previous cell allocation and output storage.
/// The returned bytes are valid until the next render; unchanged screens return an empty slice.
#[derive(Default)]
pub struct AnsiRenderer {
    previous: Option<Buffer>,
    output: Vec<u8>,
    backend_updates: Vec<(u16, u16)>,
}

impl AnsiRenderer {
    pub fn render(&mut self, buffer: &Buffer) -> &[u8] {
        self.output.clear();
        match &self.previous {
            Some(previous) if previous.area == buffer.area => {
                write_diff(previous, buffer, &mut self.output);
            }
            _ => write_full_screen(buffer, &mut self.output),
        }
        if self.output.is_empty() {
            return &self.output;
        }
        // Database widgets draw an inline cursor, not the emulator's hardware cursor.
        self.output.extend_from_slice(b"\x1b[?25l");
        // Commit only after serialization; clone_from reuses the existing cell allocation.
        if let Some(previous) = &mut self.previous {
            previous.area = buffer.area;
            previous.content.clone_from(&buffer.content);
        } else {
            self.previous = Some(buffer.clone());
        }
        &self.output
    }

    /// Keep the layout backend's cells authoritative for mouse selection and JPEG rendering.
    /// TestBackend applies only diff entries: it does not clear older cells hidden by a new
    /// wide glyph. Repair those cells from the completed frame without cloning a second buffer.
    pub fn synchronize_backend(&mut self, backend: &mut TestBackend) {
        let Some(previous) = &self.previous else {
            return;
        };
        self.backend_updates.clear();
        let actual = backend.buffer();
        for (index, (actual, expected)) in actual.content.iter().zip(&previous.content).enumerate()
        {
            if actual != expected {
                self.backend_updates.push(previous.pos_of(index));
            }
        }
        let updates = self
            .backend_updates
            .iter()
            .map(|&(x, y)| (x, y, &previous[(x, y)]));
        // TestBackend::draw is infallible and copies only these mismatched cells.
        backend.draw(updates).unwrap();
    }
}

fn write_full_screen(buffer: &Buffer, output: &mut Vec<u8>) {
    // Clear with default attributes before painting so resize removes stale rows/columns.
    output.extend_from_slice(b"\x1b[H\x1b[0m\x1b[2J");
    let mut style = AnsiStyle::default();
    let area = buffer.area;
    for row in 0..area.height {
        let mut col = 0;
        while col < area.width {
            let cell = &buffer[(area.x + col, area.y + row)];
            style.write_cell(cell, area.width - col, output);
            col += cell.cell_width().max(1).min(area.width - col);
        }
        if row + 1 < area.height {
            output.extend_from_slice(b"\r\n");
        }
    }
    // Do not erase at the right margin: ED would erase the bottom-right cell just painted.
    output.extend_from_slice(b"\x1b[0m\x1b[H");
}

fn write_diff(previous: &Buffer, buffer: &Buffer, output: &mut Vec<u8>) {
    let area = buffer.area;
    let mut style = AnsiStyle::default();
    let mut cursor = None;
    for (x, y, cell) in previous.diff_iter(buffer) {
        // Some diff iterator paths yield emoji continuation cells. Printing them would
        // overwrite the glyph's trailing half. Repairs below also cover later diff entries.
        if cursor.is_some_and(|(next_x, next_y)| y == next_y && x < next_x) {
            continue;
        }
        if output.is_empty() {
            output.extend_from_slice(b"\x1b[0m");
        }
        if cursor != Some((x, y)) {
            write_cursor(x - area.x, y - area.y, output);
        }
        let width = cell.cell_width().max(1).min(area.right() - x);
        style.write_cell(cell, area.right() - x, output);
        let mut end = x + width;
        cursor = Some((end, y));

        // A wide glyph can cover the *lead* of an older wide glyph. Buffer::diff handles
        // a narrow replacement at the same lead, but not a shifted overlap whose old
        // trailing cell is equal in both buffers. Repaint those exposed cells explicitly.
        let mut repair_end = end;
        for old_x in x..end {
            let old_width = previous[(old_x, y)].cell_width().max(1);
            repair_end = repair_end.max(old_x.saturating_add(old_width).min(area.right()));
        }
        while end < repair_end {
            let repair = &buffer[(end, y)];
            let repair_width = repair.cell_width().max(1).min(area.right() - end);
            for old_x in end..end + repair_width {
                let old_width = previous[(old_x, y)].cell_width().max(1);
                repair_end = repair_end.max(old_x.saturating_add(old_width).min(area.right()));
            }
            style.write_cell(repair, area.right() - end, output);
            end += repair_width;
            cursor = Some((end, y));
        }
    }
    if !output.is_empty() {
        output.extend_from_slice(b"\x1b[0m\x1b[H");
    }
}

fn write_cursor(col: u16, row: u16, output: &mut Vec<u8>) {
    // Vec<u8>'s Write implementation is infallible.
    write!(
        output,
        "\x1b[{};{}H",
        u32::from(row) + 1,
        u32::from(col) + 1
    )
    .unwrap();
}

#[derive(Default)]
struct AnsiStyle {
    foreground: Color,
    background: Color,
    modifiers: Modifier,
}

impl AnsiStyle {
    fn write_cell(&mut self, cell: &Cell, remaining: u16, output: &mut Vec<u8>) {
        if cell.fg != self.foreground
            || cell.bg != self.background
            || cell.modifier != self.modifiers
        {
            output.extend_from_slice(b"\x1b[0m");
            write_color(cell.fg, true, output);
            write_color(cell.bg, false, output);
            for (modifier, sgr) in [
                (Modifier::BOLD, b"\x1b[1m".as_slice()),
                (Modifier::DIM, b"\x1b[2m".as_slice()),
                (Modifier::ITALIC, b"\x1b[3m".as_slice()),
                (Modifier::UNDERLINED, b"\x1b[4m".as_slice()),
                (Modifier::SLOW_BLINK, b"\x1b[5m".as_slice()),
                (Modifier::RAPID_BLINK, b"\x1b[6m".as_slice()),
                (Modifier::REVERSED, b"\x1b[7m".as_slice()),
                (Modifier::HIDDEN, b"\x1b[8m".as_slice()),
                (Modifier::CROSSED_OUT, b"\x1b[9m".as_slice()),
            ] {
                if cell.modifier.contains(modifier) {
                    output.extend_from_slice(sgr);
                }
            }
            self.foreground = cell.fg;
            self.background = cell.bg;
            self.modifiers = cell.modifier;
        }
        if cell.cell_width() > remaining {
            // A clipped wide grapheme must never wrap into the next row.
            output.extend_from_slice(b" ");
        } else {
            output.extend_from_slice(cell.symbol().as_bytes());
        }
    }
}

fn write_color(color: Color, foreground: bool, output: &mut Vec<u8>) {
    let (basic, extended) = if foreground {
        (30u8, 38u8)
    } else {
        (40u8, 48u8)
    };
    let code = match color {
        Color::Reset => return,
        Color::Black => basic,
        Color::Red => basic + 1,
        Color::Green => basic + 2,
        Color::Yellow => basic + 3,
        Color::Blue => basic + 4,
        Color::Magenta => basic + 5,
        Color::Cyan => basic + 6,
        Color::White | Color::Gray => basic + 7,
        Color::DarkGray => basic + 60,
        Color::LightRed => basic + 61,
        Color::LightGreen => basic + 62,
        Color::LightYellow => basic + 63,
        Color::LightBlue => basic + 64,
        Color::LightMagenta => basic + 65,
        Color::LightCyan => basic + 66,
        Color::Rgb(r, g, b) => {
            write!(output, "\x1b[{extended};2;{r};{g};{b}m").unwrap();
            return;
        }
        Color::Indexed(n) => {
            write!(output, "\x1b[{extended};5;{n}m").unwrap();
            return;
        }
    };
    write!(output, "\x1b[{code}m").unwrap();
}
