use crate::cursor::{format_cursor_instruction, CursorState, CursorType};

#[test]
fn test_cursor_type_from_css() {
    assert_eq!(CursorType::from_css("pointer"), CursorType::Pointer);
    assert_eq!(CursorType::from_css("text"), CursorType::Text);
    assert_eq!(CursorType::from_css("wait"), CursorType::Wait);
    assert_eq!(CursorType::from_css("default"), CursorType::Default);
    assert_eq!(CursorType::from_css("auto"), CursorType::Default);
    assert_eq!(CursorType::from_css("url(cursor.png)"), CursorType::Custom);
    assert_eq!(CursorType::from_css("unknown"), CursorType::Default);
}

#[test]
fn test_cursor_state() {
    let mut state = CursorState::new();

    let result = state.update("pointer", 1);
    assert_eq!(result, Some(CursorType::Pointer));

    let result = state.update("pointer", 2);
    assert_eq!(result, None);

    let result = state.update("text", 3);
    assert_eq!(result, Some(CursorType::Text));

    let result = state.update("wait", 1);
    assert_eq!(result, None);
}

#[test]
fn test_format_cursor_instruction() {
    let instr = format_cursor_instruction(0, 0, 0, 0, 0, 16, 16);
    assert!(instr.starts_with("6.cursor,"));
    assert!(instr.contains("16"));
}
