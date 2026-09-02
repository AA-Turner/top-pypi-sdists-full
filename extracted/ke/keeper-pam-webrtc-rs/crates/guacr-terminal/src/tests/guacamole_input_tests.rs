use crate::guacamole_input::{
    extract_selection_text_ratatui, parse_clipboard_blob, parse_key_instruction,
    parse_mouse_instruction,
};

#[test]
fn test_parse_key_instruction() {
    let event = parse_key_instruction("3.key,2.99,1.1;").unwrap();
    assert_eq!(event.keysym, 99); // 'c'
    assert!(event.pressed);

    let event = parse_key_instruction("3.key,2.99,1.0;").unwrap();
    assert_eq!(event.keysym, 99);
    assert!(!event.pressed);

    // Test Right Ctrl -> Left Ctrl fix
    let event = parse_key_instruction("3.key,5.65508,1.1;").unwrap();
    assert_eq!(event.keysym, 65507); // Fixed to Left Ctrl
}

#[test]
fn test_parse_mouse_instruction() {
    let event = parse_mouse_instruction("5.mouse,3.915,3.328,1.0;").unwrap();
    assert_eq!(event.x_px, 915);
    assert_eq!(event.y_px, 328);
    assert_eq!(event.button_mask, 0);

    let event = parse_mouse_instruction("5.mouse,3.100,2.50,1.1;").unwrap();
    assert_eq!(event.x_px, 100);
    assert_eq!(event.y_px, 50);
    assert_eq!(event.button_mask, 1); // Left button
}

#[test]
fn test_parse_clipboard_blob() {
    // "Rust handler level" in base64
    let text = parse_clipboard_blob("4.blob,1.0,24.UnVzdCBoYW5kbGVyIGxldmVs;").unwrap();
    assert_eq!(text, "Rust handler level");

    // Empty clipboard should return None
    let result = parse_clipboard_blob("4.blob,1.0,0.;");
    assert!(result.is_none());
}

// == extract_selection_text_ratatui tests ================================

fn make_buffer_with_text(cols: u16, rows: u16, row: u16, text: &str) -> ratatui::buffer::Buffer {
    let mut buf = ratatui::buffer::Buffer::empty(ratatui::layout::Rect::new(0, 0, cols, rows));
    for (i, ch) in text.chars().enumerate() {
        let idx = row as usize * cols as usize + i;
        if idx < buf.content.len() {
            let mut ch_buf = [0u8; 4];
            buf.content[idx].set_symbol(ch.encode_utf8(&mut ch_buf));
        }
    }
    buf
}

#[test]
fn test_extract_single_line() {
    let buf = make_buffer_with_text(80, 24, 0, "Hello");
    let text = extract_selection_text_ratatui(&buf, (0, 0), (0, 4), 80);
    assert_eq!(text, "Hello");
}

#[test]
fn test_extract_single_line_partial() {
    let buf = make_buffer_with_text(80, 24, 0, "Hello World");
    // Select only "Hello"
    let text = extract_selection_text_ratatui(&buf, (0, 0), (0, 4), 80);
    assert_eq!(text, "Hello");
}

#[test]
fn test_extract_normalises_reversed_coords() {
    // Passing end before start should produce the same result as the correct order.
    let buf = make_buffer_with_text(80, 24, 0, "Hello");
    let forward = extract_selection_text_ratatui(&buf, (0, 0), (0, 4), 80);
    let reversed = extract_selection_text_ratatui(&buf, (0, 4), (0, 0), 80);
    assert_eq!(forward, reversed);
}

#[test]
fn test_extract_multiline_trims_trailing_whitespace() {
    // Row 0: "AB    " (with trailing spaces), Row 1: "CD"
    let mut buf = ratatui::buffer::Buffer::empty(ratatui::layout::Rect::new(0, 0, 10, 5));
    buf.content[0].set_symbol("A");
    buf.content[1].set_symbol("B");
    // cols 2..9 are spaces (default)
    buf.content[10].set_symbol("C");
    buf.content[11].set_symbol("D");

    // Select from row 0 col 0 to row 1 col 1
    let text = extract_selection_text_ratatui(&buf, (0, 0), (1, 1), 10);
    // First line trailing spaces should be trimmed, then newline, then "CD"
    assert_eq!(text, "AB\nCD");
}

#[test]
fn test_extract_empty_selection_within_row() {
    let buf = make_buffer_with_text(80, 24, 0, "Hello");
    // start == end: single character
    let text = extract_selection_text_ratatui(&buf, (0, 2), (0, 2), 80);
    assert_eq!(text, "l");
}

#[test]
fn test_extract_out_of_bounds_is_safe() {
    let buf = ratatui::buffer::Buffer::empty(ratatui::layout::Rect::new(0, 0, 10, 5));
    // Row/col beyond buffer -- should not panic, returns empty or spaces
    let text = extract_selection_text_ratatui(&buf, (4, 0), (4, 9), 10);
    // All spaces trimmed gives empty (for multirow it would trim, single row doesn't trim)
    assert_eq!(text.trim(), "");
}
