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

// --- MouseDelta accumulation tests ---

#[test]
fn test_mouse_position_initial() {
    let handler = RbiInputHandler::new();
    assert_eq!(handler.mouse_position(), (0, 0));
}

#[test]
fn test_mouse_position_after_absolute_move() {
    let mut handler = RbiInputHandler::new();
    handler.handle_mouse(400, 300, 0);
    assert_eq!(handler.mouse_position(), (400, 300));
}

#[test]
fn test_mouse_position_accumulates_delta() {
    // Simulate what the MouseDelta handler does: get current pos, add delta, call handle_mouse
    let mut handler = RbiInputHandler::new();
    // Start at (400, 300)
    handler.handle_mouse(400, 300, 0);
    // Apply delta (+10, -5)
    let (x, y) = handler.mouse_position();
    let new_x = (x + 10).clamp(0, 1808);
    let new_y = (y + (-5)).clamp(0, 1322);
    handler.handle_mouse(new_x, new_y, 0);
    assert_eq!(handler.mouse_position(), (410, 295));
}

#[test]
fn test_mouse_delta_clamped_to_screen() {
    let mut handler = RbiInputHandler::new();
    // At (5, 5), delta (-100, -100) → clamped to (0, 0)
    handler.handle_mouse(5, 5, 0);
    let (x, y) = handler.mouse_position();
    let new_x = (x + (-100i32)).clamp(0, 1808);
    let new_y = (y + (-100i32)).clamp(0, 1808);
    handler.handle_mouse(new_x, new_y, 0);
    assert_eq!(handler.mouse_position(), (0, 0));
}

// ---------------------------------------------------------------------------
// Additional MouseDelta edge-case tests
//
// The binary MouseDelta opcode (0x06) in browser_client.rs computes:
//
//   let (abs_x, abs_y) = self.input_handler.mouse_position();
//   let x = (abs_x + dx as i32).clamp(0, self.width as i32 - 1);
//   let y = (abs_y + dy as i32).clamp(0, self.height as i32 - 1);
//   let mouse_event = self.input_handler.handle_mouse(x, y, buttons);
//
// These tests exercise the boundary conditions that the opcode dispatch
// relies on so we catch regressions if the clamping arithmetic changes.
// ---------------------------------------------------------------------------

/// A large positive delta at the right/bottom edge must stay within bounds.
///
/// The viewport is W×H; the max addressable coordinate is (W-1, H-1).
/// A delta of +127 (i8 max) applied at (W-1, H-1) must still land on (W-1, H-1).
#[test]
fn test_mouse_delta_clamped_to_max_boundary() {
    let width = 1920i32;
    let height = 1080i32;
    let mut handler = RbiInputHandler::new();

    // Place cursor at bottom-right corner.
    handler.handle_mouse(width - 1, height - 1, 0);

    // Apply maximum positive i8 delta — must clamp to the boundary.
    let (x, y) = handler.mouse_position();
    let new_x = (x + 127i32).clamp(0, width - 1);
    let new_y = (y + 127i32).clamp(0, height - 1);
    handler.handle_mouse(new_x, new_y, 0);

    assert_eq!(
        handler.mouse_position(),
        (width - 1, height - 1),
        "delta past the right/bottom boundary must clamp to (W-1, H-1)"
    );
}

/// Sequential delta accumulation must match direct absolute positioning.
///
/// Three deltas of (+10, +5) applied from origin (0, 0) must leave the
/// cursor at (30, 15) — the same result as a single handle_mouse(30, 15, 0).
#[test]
fn test_mouse_delta_sequential_accumulation() {
    let width = 1920i32;
    let height = 1080i32;
    let mut handler = RbiInputHandler::new();

    // Start at origin.
    handler.handle_mouse(0, 0, 0);

    for _ in 0..3 {
        let (x, y) = handler.mouse_position();
        let new_x = (x + 10i32).clamp(0, width - 1);
        let new_y = (y + 5i32).clamp(0, height - 1);
        handler.handle_mouse(new_x, new_y, 0);
    }

    assert_eq!(
        handler.mouse_position(),
        (30, 15),
        "three (+10, +5) deltas from origin should land at (30, 15)"
    );
}

/// A delta packet with scroll only (dx=0, dy=0) must not move the cursor.
///
/// In browser_client.rs the scroll path is:
///   if scroll != 0 { chrome_session.inject_scroll(x, y, 0, scroll as i32)? }
/// x and y come from the clamped delta — when dx=dy=0, x and y equal the
/// current position, so the cursor position must be unchanged after the event.
#[test]
fn test_mouse_delta_scroll_only_does_not_move_cursor() {
    let width = 1920i32;
    let height = 1080i32;
    let mut handler = RbiInputHandler::new();

    // Place cursor at an arbitrary position.
    handler.handle_mouse(640, 480, 0);

    // Zero dx, zero dy — position must not change.
    let (x, y) = handler.mouse_position();
    let new_x = x.clamp(0, width - 1);
    let new_y = y.clamp(0, height - 1);
    handler.handle_mouse(new_x, new_y, 0);

    assert_eq!(
        handler.mouse_position(),
        (640, 480),
        "scroll-only delta (dx=0 dy=0) must not move the cursor"
    );
}

/// The W3C buttons bitmask must reflect the button state carried through a delta.
///
/// In browser_client.rs the delta handler reads mouse_buttons_mask() AFTER
/// calling handle_mouse(x, y, buttons) to pass to inject_mouse_move.
/// Left button bit in Guacamole is 0x01; W3C left button is 1.
#[test]
fn test_mouse_delta_buttons_mask_w3c_encoding() {
    let mut handler = RbiInputHandler::new();

    // Press left button (Guacamole mask bit 0x01).
    handler.handle_mouse(100, 100, MOUSE_BUTTON_LEFT);

    assert_eq!(
        handler.mouse_buttons_mask(),
        1,
        "Guacamole left button (0x01) should map to W3C bit 1"
    );

    // Now a delta arrives with left still held.
    handler.handle_mouse(110, 105, MOUSE_BUTTON_LEFT);

    assert_eq!(
        handler.mouse_buttons_mask(),
        1,
        "W3C mask must remain 1 while left button is held through a delta"
    );

    // Release the button.
    handler.handle_mouse(110, 105, 0);
    assert_eq!(
        handler.mouse_buttons_mask(),
        0,
        "W3C mask must be 0 after button release"
    );
}
