use crate::input::{
    keysym_to_js_keycode, keysym_to_unicode, ChromeEventFlags, KeyboardShortcut, KeyboardState,
    MouseState, RbiInputHandler, KEYSYM_CTRL_LEFT, MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT,
};

#[test]
fn test_keysym_to_js_keycode() {
    assert_eq!(keysym_to_js_keycode('A' as u32), 'A' as u32);
    assert_eq!(keysym_to_js_keycode('a' as u32), 'A' as u32);
    assert_eq!(keysym_to_js_keycode(0xFF0D), 13);
    assert_eq!(keysym_to_js_keycode(0xFFBE), 112);
    assert_eq!(keysym_to_js_keycode('`' as u32), 192);
}

#[test]
fn test_keyboard_state() {
    let mut state = KeyboardState::new();

    state.set_pressed(KEYSYM_CTRL_LEFT, true);
    assert!(state.is_pressed(KEYSYM_CTRL_LEFT));
    assert_eq!(state.pressed_count(), 1);
    assert_eq!(
        state.get_modifiers() & ChromeEventFlags::CONTROL_DOWN,
        ChromeEventFlags::CONTROL_DOWN
    );

    state.set_pressed('A' as u32, true);
    assert_eq!(state.pressed_count(), 2);

    state.set_pressed(KEYSYM_CTRL_LEFT, false);
    assert!(!state.is_pressed(KEYSYM_CTRL_LEFT));
    assert_eq!(state.pressed_count(), 1);
}

#[test]
fn test_mouse_state() {
    let state = MouseState::new();

    let modifiers = state.get_mouse_modifiers(MOUSE_BUTTON_LEFT | MOUSE_BUTTON_RIGHT);
    assert_eq!(
        modifiers & ChromeEventFlags::LEFT_MOUSE_BUTTON,
        ChromeEventFlags::LEFT_MOUSE_BUTTON
    );
    assert_eq!(
        modifiers & ChromeEventFlags::RIGHT_MOUSE_BUTTON,
        ChromeEventFlags::RIGHT_MOUSE_BUTTON
    );
}

#[test]
fn test_input_handler_shortcut() {
    let mut handler = RbiInputHandler::new();

    handler.handle_keyboard(KEYSYM_CTRL_LEFT, true);
    handler.handle_keyboard('c' as u32, true);

    let shortcut = handler.check_shortcut('c' as u32, true);
    assert_eq!(shortcut, Some(KeyboardShortcut::Copy));

    handler.handle_keyboard('c' as u32, false);

    handler.handle_keyboard('v' as u32, true);

    let shortcut = handler.check_shortcut('v' as u32, true);
    assert_eq!(shortcut, Some(KeyboardShortcut::Paste));
}

#[test]
fn test_unicode_conversion() {
    assert_eq!(keysym_to_unicode(0xFF0D), Some('\r'));
    assert_eq!(keysym_to_unicode(0xFF09), Some('\t'));
    assert_eq!(keysym_to_unicode(0xFFB5), Some('5')); // Keypad 5
    assert_eq!(keysym_to_unicode('a' as u32), Some('a'));
}
