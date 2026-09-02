use crate::emulator::TerminalEmulator;
use crate::terminal_input_handler::TerminalInputHandler;

#[test]
fn test_new_handler() {
    let handler = TerminalInputHandler::new(24, 80);
    assert_eq!(handler.size(), (24, 80));
    assert_eq!(handler.scrollback_size(), 1000);
    assert!(!handler.has_selection());
}

#[test]
fn test_new_with_scrollback() {
    let handler = TerminalInputHandler::new_with_scrollback(24, 80, 5000);
    assert_eq!(handler.scrollback_size(), 5000);
}

#[test]
fn test_clipboard_paste() {
    let mut handler = TerminalInputHandler::new(24, 80);
    let text = "SELECT * FROM users";
    let bytes = handler.handle_clipboard_paste(text);
    assert_eq!(bytes, text.as_bytes());
    assert_eq!(handler.clipboard_data(), text);
}

#[test]
fn test_resize() {
    let mut handler = TerminalInputHandler::new(24, 80);
    let mut terminal = TerminalEmulator::new(24, 80);

    handler.handle_resize(30, 100, &mut terminal).unwrap();
    assert_eq!(handler.size(), (30, 100));
    assert_eq!(terminal.size(), (30, 100));
}

#[test]
fn test_clear_selection() {
    let mut handler = TerminalInputHandler::new(24, 80);
    // Selection would be set by handle_mouse_event in real usage
    handler.clear_selection();
    assert!(!handler.has_selection());
}

#[test]
fn test_clipboard_instructions_empty() {
    let handler = TerminalInputHandler::new(24, 80);
    let terminal = TerminalEmulator::new(24, 80);
    let instrs = handler.get_clipboard_instructions(&terminal, 1);
    assert!(instrs.is_empty()); // No selection
}
