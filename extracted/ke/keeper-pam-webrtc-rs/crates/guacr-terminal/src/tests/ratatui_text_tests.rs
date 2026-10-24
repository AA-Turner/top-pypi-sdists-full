use crate::ratatui_text::{buffer_to_ansi, AnsiRenderer};
use ratatui::{
    buffer::{Buffer, CellWidth},
    layout::Rect,
    style::{Color, Modifier, Style},
};

fn terminal_color(color: Color) -> vt100::Color {
    match color {
        Color::Reset => vt100::Color::Default,
        Color::Black => vt100::Color::Idx(0),
        Color::Red => vt100::Color::Idx(1),
        Color::Green => vt100::Color::Idx(2),
        Color::Yellow => vt100::Color::Idx(3),
        Color::Blue => vt100::Color::Idx(4),
        Color::Magenta => vt100::Color::Idx(5),
        Color::Cyan => vt100::Color::Idx(6),
        Color::White | Color::Gray => vt100::Color::Idx(7),
        Color::DarkGray => vt100::Color::Idx(8),
        Color::LightRed => vt100::Color::Idx(9),
        Color::LightGreen => vt100::Color::Idx(10),
        Color::LightYellow => vt100::Color::Idx(11),
        Color::LightBlue => vt100::Color::Idx(12),
        Color::LightMagenta => vt100::Color::Idx(13),
        Color::LightCyan => vt100::Color::Idx(14),
        Color::Indexed(n) => vt100::Color::Idx(n),
        Color::Rgb(r, g, b) => vt100::Color::Rgb(r, g, b),
    }
}

fn assert_buffer_screen(buffer: &Buffer, screen: &vt100::Screen) {
    let area = buffer.area;
    for row in 0..area.height {
        let mut col = 0;
        while col < area.width {
            let expected = &buffer[(area.x + col, area.y + row)];
            let actual = screen.cell(row, col).unwrap();
            let width = expected.cell_width().max(1);
            let symbol = if width > area.width - col {
                " "
            } else {
                expected.symbol()
            };
            assert_eq!(
                actual.contents().trim_end(),
                symbol.trim_end(),
                "cell ({col}, {row})"
            );
            assert_eq!(
                actual.fgcolor(),
                terminal_color(expected.fg),
                "foreground ({col}, {row})"
            );
            assert_eq!(
                actual.bgcolor(),
                terminal_color(expected.bg),
                "background ({col}, {row})"
            );
            assert_eq!(actual.bold(), expected.modifier.contains(Modifier::BOLD));
            assert_eq!(
                actual.italic(),
                expected.modifier.contains(Modifier::ITALIC)
            );
            assert_eq!(
                actual.underline(),
                expected.modifier.contains(Modifier::UNDERLINED)
            );
            assert_eq!(
                actual.inverse(),
                expected.modifier.contains(Modifier::REVERSED)
            );
            if width > 1 && width <= area.width - col {
                assert!(actual.is_wide());
                let trailing = screen.cell(row, col + 1).unwrap();
                assert!(trailing.is_wide_continuation());
            }
            col += width.min(area.width - col);
        }
    }
}

fn replay_frame(renderer: &mut AnsiRenderer, parser: &mut vt100::Parser, buffer: &Buffer) {
    parser.process(renderer.render(buffer));
    assert_buffer_screen(buffer, parser.screen());
    let mut fresh = vt100::Parser::new(buffer.area.height, buffer.area.width, 16);
    fresh.process(&buffer_to_ansi(buffer));
    assert_buffer_screen(buffer, fresh.screen());
    assert_eq!(parser.screen().contents(), fresh.screen().contents());
    parser.set_scrollback(16);
    assert_eq!(parser.screen().scrollback(), 0, "redraw must not scroll");
}

#[test]
fn incremental_replay_preserves_edits_deletion_unicode_and_styles() {
    let mut renderer = AnsiRenderer::default();
    let mut parser = vt100::Parser::new(4, 12, 16);
    let mut buffer = Buffer::empty(Rect::new(0, 0, 12, 4));
    buffer.set_string(0, 0, "mysql> select", Style::default());
    buffer.set_string(0, 1, "a界e\u{301} Z", Style::default());
    buffer.set_string(11, 3, "!", Style::default());
    replay_frame(&mut renderer, &mut parser, &buffer);
    assert!(
        renderer.render(&buffer).is_empty(),
        "unchanged screen must emit no output"
    );

    buffer.set_string(7, 0, "delete", Style::default());
    replay_frame(&mut renderer, &mut parser, &buffer);
    buffer.set_string(7, 0, "     ", Style::default());
    replay_frame(&mut renderer, &mut parser, &buffer);

    let colored = Style::default()
        .fg(Color::Rgb(17, 103, 211))
        .bg(Color::Indexed(42))
        .add_modifier(
            Modifier::BOLD | Modifier::ITALIC | Modifier::UNDERLINED | Modifier::REVERSED,
        );
    buffer.set_string(1, 1, "界", colored);
    replay_frame(&mut renderer, &mut parser, &buffer);
    buffer.set_string(1, 1, "x ", Style::reset());
    replay_frame(&mut renderer, &mut parser, &buffer);

    // A new wide glyph overlaps the old lead cell, vacating its trailing cell.
    buffer.set_string(1, 2, "界", colored);
    replay_frame(&mut renderer, &mut parser, &buffer);
    buffer.set_string(0, 2, "界  ", Style::reset());
    replay_frame(&mut renderer, &mut parser, &buffer);
    buffer.set_string(0, 2, "    ", Style::reset());
    buffer.set_string(3, 1, "e\u{308}", Style::reset().fg(Color::LightRed));
    buffer.set_string(11, 3, "?", colored);
    replay_frame(&mut renderer, &mut parser, &buffer);
    assert!(renderer.render(&buffer).is_empty());
}

#[test]
fn full_and_incremental_replay_preserve_geometry_changes_and_buffer_origins() {
    let mut renderer = AnsiRenderer::default();
    let mut parser = vt100::Parser::new(3, 9, 16);
    let mut buffer = Buffer::empty(Rect::new(4, 7, 9, 3));
    buffer.set_string(4, 7, "界e\u{301} tail", Style::default().bg(Color::Blue));
    buffer.set_string(12, 9, "Z", Style::default());
    replay_frame(&mut renderer, &mut parser, &buffer);
    for (cols, rows) in [(5, 2), (13, 5), (13, 2), (1, 1)] {
        parser.set_size(rows, cols);
        buffer = Buffer::empty(Rect::new(0, 0, cols, rows));
        buffer.set_string(0, 0, "new", Style::default().fg(Color::Green));
        buffer.set_string(cols - 1, rows - 1, "!", Style::default().bg(Color::Red));
        replay_frame(&mut renderer, &mut parser, &buffer);
        assert!(renderer.render(&buffer).is_empty());
    }
}

#[test]
fn wide_glyph_at_right_edge_never_wraps_or_erases_the_last_cell() {
    let mut renderer = AnsiRenderer::default();
    let mut parser = vt100::Parser::new(2, 5, 16);
    let mut buffer = Buffer::empty(Rect::new(0, 0, 5, 2));
    buffer.set_string(3, 1, "界", Style::default().bg(Color::Yellow));
    replay_frame(&mut renderer, &mut parser, &buffer);
    buffer.set_string(3, 1, " !", Style::reset());
    replay_frame(&mut renderer, &mut parser, &buffer);
    // Even a directly supplied, clipped wide cell cannot scroll the emulator.
    buffer[(4, 1)].set_symbol("界");
    replay_frame(&mut renderer, &mut parser, &buffer);
}

#[test]
fn shifted_wide_runs_and_style_only_updates_replay_without_stale_cells() {
    let mut renderer = AnsiRenderer::default();
    let mut parser = vt100::Parser::new(2, 14, 16);
    for (text, color) in [
        (" 界界界界", Color::Blue),
        ("界界界界 ", Color::Red),
        ("界界界界 ", Color::Rgb(80, 160, 240)),
        (" a界b界c ", Color::Indexed(152)),
        (" a b c d ", Color::Reset),
        ("", Color::Reset),
    ] {
        let mut buffer = Buffer::empty(Rect::new(0, 0, 14, 2));
        buffer.set_string(
            0,
            0,
            text,
            Style::default()
                .bg(color)
                .add_modifier(Modifier::UNDERLINED),
        );
        buffer.set_string(13, 1, "X", Style::default().fg(color));
        replay_frame(&mut renderer, &mut parser, &buffer);
    }
}

#[test]
fn full_replay_preserves_the_ansi_color_palette() {
    let colors = [
        Color::Reset,
        Color::Black,
        Color::Red,
        Color::Green,
        Color::Yellow,
        Color::Blue,
        Color::Magenta,
        Color::Cyan,
        Color::White,
        Color::Gray,
        Color::DarkGray,
        Color::LightRed,
        Color::LightGreen,
        Color::LightYellow,
        Color::LightBlue,
        Color::LightMagenta,
        Color::LightCyan,
        Color::Indexed(241),
        Color::Rgb(31, 129, 242),
    ];
    let mut buffer = Buffer::empty(Rect::new(0, 0, colors.len() as u16, 2));
    for (col, color) in colors.into_iter().enumerate() {
        buffer.set_string(col as u16, 0, "X", Style::default().fg(color));
        buffer.set_string(col as u16, 1, " ", Style::default().bg(color));
    }
    let mut renderer = AnsiRenderer::default();
    let mut parser = vt100::Parser::new(2, colors.len() as u16, 16);
    replay_frame(&mut renderer, &mut parser, &buffer);
}

#[test]
fn full_redraw_replaces_stale_content_and_inherited_attributes() {
    let buffer = Buffer::with_lines(["plain", "last!"]);
    let mut parser = vt100::Parser::new(2, 5, 16);
    parser.process(b"\x1b[31m\x1b[44m\x1b[1;4mXXXXX\r\nYYYYY");
    parser.process(&buffer_to_ansi(&buffer));
    assert_buffer_screen(&buffer, parser.screen());
    parser.set_scrollback(16);
    assert_eq!(parser.screen().scrollback(), 0);
}

#[test]
fn completed_frames_remove_hidden_backend_cells_when_results_narrow_and_popup_clears() {
    use ratatui::{
        backend::TestBackend,
        widgets::{Clear, Paragraph},
        Terminal,
    };

    let mut terminal = Terminal::new(TestBackend::new(100, 12)).unwrap();
    let mut renderer = AnsiRenderer::default();
    let mut parser = vt100::Parser::new(12, 100, 16);
    for step in 0..4 {
        let completed = terminal
            .draw(|frame| {
                frame.render_widget(
                    Paragraph::new("n    next_n   unicode"),
                    Rect::new(33, 6, 45, 1),
                );
                match step {
                    0 => frame.render_widget(Paragraph::new("s"), Rect::new(65, 7, 1, 1)),
                    1 => frame.render_widget(Paragraph::new("界 café"), Rect::new(64, 7, 20, 1)),
                    _ => frame.render_widget(Paragraph::new("3"), Rect::new(33, 7, 1, 1)),
                }
                if step == 3 {
                    frame.render_widget(Clear, Rect::new(58, 2, 40, 9));
                    frame.render_widget(Paragraph::new("Export options"), Rect::new(59, 3, 30, 1));
                }
            })
            .unwrap();
        let expected = completed.buffer.clone();
        let output = renderer.render(completed.buffer);
        assert!(!output.is_empty());
        if step > 0 {
            assert!(output.len() < 100 * 12, "changes must remain incremental");
        }
        parser.process(output);
        renderer.synchronize_backend(terminal.backend_mut());
        assert_eq!(terminal.backend().buffer(), &expected);
        assert_buffer_screen(&expected, parser.screen());
        if step >= 2 {
            assert!(parser
                .screen()
                .cell(7, 65)
                .unwrap()
                .contents()
                .trim()
                .is_empty());
            assert_eq!(terminal.backend().buffer()[(65, 7)].symbol(), " ");
        }
        assert!(renderer.render(&expected).is_empty());
    }
}

#[test]
fn completed_frames_keep_unicode_continuations_current_for_mouse_and_jpeg_consumers() {
    use ratatui::{backend::TestBackend, widgets::Paragraph, Terminal};

    let mut terminal = Terminal::new(TestBackend::new(100, 12)).unwrap();
    let mut renderer = AnsiRenderer::default();
    for text in ["s stale result", "界 café 👩‍💻", "3", ""] {
        let completed = terminal
            .draw(|frame| {
                frame.render_widget(Paragraph::new(text), Rect::new(64, 7, 25, 1));
            })
            .unwrap();
        let expected = completed.buffer.clone();
        renderer.render(completed.buffer);
        renderer.synchronize_backend(terminal.backend_mut());
        assert_eq!(terminal.backend().buffer(), &expected);
    }
    assert_eq!(terminal.backend().buffer()[(65, 7)].symbol(), " ");
}
