use crate::input_handler::{keysym_to_scancode, RdpInputHandler};

#[test]
fn test_keysym_to_scancode_letters() {
    // Uppercase
    assert_eq!(keysym_to_scancode(0x0041).unwrap(), (0x1E, false)); // A
    assert_eq!(keysym_to_scancode(0x0051).unwrap(), (0x10, false)); // Q
    assert_eq!(keysym_to_scancode(0x005A).unwrap(), (0x2C, false)); // Z

    // Lowercase maps to same scancode
    assert_eq!(keysym_to_scancode(0x0061).unwrap(), (0x1E, false)); // a
    assert_eq!(keysym_to_scancode(0x0071).unwrap(), (0x10, false)); // q
    assert_eq!(keysym_to_scancode(0x007A).unwrap(), (0x2C, false)); // z
}

#[test]
fn test_keysym_to_scancode_digits() {
    assert_eq!(keysym_to_scancode(0x0030).unwrap(), (0x0B, false)); // 0
    assert_eq!(keysym_to_scancode(0x0031).unwrap(), (0x02, false)); // 1
    assert_eq!(keysym_to_scancode(0x0039).unwrap(), (0x0A, false)); // 9
}

#[test]
fn test_keysym_to_scancode_special() {
    assert_eq!(keysym_to_scancode(0x0020).unwrap(), (0x39, false)); // Space
    assert_eq!(keysym_to_scancode(0xFF0D).unwrap(), (0x1C, false)); // Enter
    assert_eq!(keysym_to_scancode(0xFF08).unwrap(), (0x0E, false)); // Backspace
    assert_eq!(keysym_to_scancode(0xFF09).unwrap(), (0x0F, false)); // Tab
    assert_eq!(keysym_to_scancode(0xFF1B).unwrap(), (0x01, false)); // Escape
}

#[test]
fn test_keysym_to_scancode_extended() {
    // Navigation keys are extended
    assert_eq!(keysym_to_scancode(0xFF51).unwrap(), (0x4B, true)); // Left
    assert_eq!(keysym_to_scancode(0xFF52).unwrap(), (0x48, true)); // Up
    assert_eq!(keysym_to_scancode(0xFF53).unwrap(), (0x4D, true)); // Right
    assert_eq!(keysym_to_scancode(0xFF54).unwrap(), (0x50, true)); // Down
    assert_eq!(keysym_to_scancode(0xFF50).unwrap(), (0x47, true)); // Home
    assert_eq!(keysym_to_scancode(0xFF57).unwrap(), (0x4F, true)); // End
    assert_eq!(keysym_to_scancode(0xFFFF).unwrap(), (0x53, true)); // Delete
    assert_eq!(keysym_to_scancode(0xFF63).unwrap(), (0x52, true)); // Insert

    // Right Ctrl/Alt are extended
    assert_eq!(keysym_to_scancode(0xFFE4).unwrap(), (0x1D, true)); // Right Ctrl
    assert_eq!(keysym_to_scancode(0xFFEA).unwrap(), (0x38, true)); // Right Alt
}

#[test]
fn test_keysym_to_scancode_function_keys() {
    assert_eq!(keysym_to_scancode(0xFFBE).unwrap(), (0x3B, false)); // F1
    assert_eq!(keysym_to_scancode(0xFFC7).unwrap(), (0x44, false)); // F10
    assert_eq!(keysym_to_scancode(0xFFC8).unwrap(), (0x57, false)); // F11
    assert_eq!(keysym_to_scancode(0xFFC9).unwrap(), (0x58, false)); // F12
}

#[test]
fn test_keysym_to_scancode_modifiers() {
    assert_eq!(keysym_to_scancode(0xFFE1).unwrap(), (0x2A, false)); // Left Shift
    assert_eq!(keysym_to_scancode(0xFFE2).unwrap(), (0x36, false)); // Right Shift
    assert_eq!(keysym_to_scancode(0xFFE3).unwrap(), (0x1D, false)); // Left Ctrl
    assert_eq!(keysym_to_scancode(0xFFE9).unwrap(), (0x38, false)); // Left Alt
    assert_eq!(keysym_to_scancode(0xFFE5).unwrap(), (0x3A, false)); // Caps Lock
}

#[test]
fn test_keysym_to_scancode_punctuation() {
    assert_eq!(keysym_to_scancode(0x002D).unwrap(), (0x0C, false)); // -
    assert_eq!(keysym_to_scancode(0x003D).unwrap(), (0x0D, false)); // =
    assert_eq!(keysym_to_scancode(0x005B).unwrap(), (0x1A, false)); // [
    assert_eq!(keysym_to_scancode(0x005D).unwrap(), (0x1B, false)); // ]
    assert_eq!(keysym_to_scancode(0x003B).unwrap(), (0x27, false)); // ;
    assert_eq!(keysym_to_scancode(0x0027).unwrap(), (0x28, false)); // '
    assert_eq!(keysym_to_scancode(0x002C).unwrap(), (0x33, false)); // ,
    assert_eq!(keysym_to_scancode(0x002E).unwrap(), (0x34, false)); // .
    assert_eq!(keysym_to_scancode(0x002F).unwrap(), (0x35, false)); // /
}

#[test]
fn test_unknown_keysym_returns_error() {
    assert!(keysym_to_scancode(0x9999).is_err());
}

#[test]
fn test_handle_keyboard_integration() {
    let handler = RdpInputHandler::new();
    // Typing lowercase 'a' should produce scancode 0x1E, not extended
    let event = handler.handle_keyboard(0x0061, true).unwrap();
    assert_eq!(event.scancode, 0x1E);
    assert!(event.pressed);
    assert!(!event.extended);
}

#[test]
fn test_mouse_handling() {
    let mut handler = RdpInputHandler::new();

    // Test left button click
    let event = handler.handle_mouse(0x01, 100, 200).unwrap();
    assert!(event.left_button);
    assert!(!event.right_button);
    assert_eq!(event.x, 100);
    assert_eq!(event.y, 200);
}
