use crate::keysym::{
    mouse_event_to_x11_sequence, x11_keysym_to_bytes, x11_keysym_to_bytes_with_modes,
    x11_keysym_to_kitty_sequence, ModifierState,
};

#[test]
fn test_ascii_characters() {
    assert_eq!(x11_keysym_to_bytes(0x0041, true, None), vec![b'A']);
    assert_eq!(x11_keysym_to_bytes(0x0061, true, None), vec![b'a']);
    assert_eq!(x11_keysym_to_bytes(0x0030, true, None), vec![b'0']);
    assert_eq!(x11_keysym_to_bytes(0x0020, true, None), vec![b' ']);
}

#[test]
fn test_special_keys() {
    assert_eq!(x11_keysym_to_bytes(0xFF0D, true, None), vec![b'\r']); // Enter
    assert_eq!(x11_keysym_to_bytes(0xFF08, true, None), vec![0x7F]); // Backspace
    assert_eq!(x11_keysym_to_bytes(0xFF09, true, None), vec![b'\t']); // Tab
    assert_eq!(x11_keysym_to_bytes(0xFF1B, true, None), vec![0x1B]); // Escape
}

#[test]
fn test_arrow_keys() {
    // Normal mode (default)
    assert_eq!(
        x11_keysym_to_bytes(0xFF51, true, None),
        vec![0x1B, b'[', b'D']
    ); // Left
    assert_eq!(
        x11_keysym_to_bytes(0xFF52, true, None),
        vec![0x1B, b'[', b'A']
    ); // Up
    assert_eq!(
        x11_keysym_to_bytes(0xFF53, true, None),
        vec![0x1B, b'[', b'C']
    ); // Right
    assert_eq!(
        x11_keysym_to_bytes(0xFF54, true, None),
        vec![0x1B, b'[', b'B']
    ); // Down
}

#[test]
fn test_arrow_keys_application_cursor_mode() {
    // Application cursor mode (used by vim, less, tmux)
    assert_eq!(
        x11_keysym_to_bytes_with_modes(0xFF51, true, None, 127, true),
        vec![0x1B, b'O', b'D']
    ); // Left
    assert_eq!(
        x11_keysym_to_bytes_with_modes(0xFF52, true, None, 127, true),
        vec![0x1B, b'O', b'A']
    ); // Up
    assert_eq!(
        x11_keysym_to_bytes_with_modes(0xFF53, true, None, 127, true),
        vec![0x1B, b'O', b'C']
    ); // Right
    assert_eq!(
        x11_keysym_to_bytes_with_modes(0xFF54, true, None, 127, true),
        vec![0x1B, b'O', b'B']
    ); // Down

    // Normal mode (application_cursor = false) - MUST still work for bash!
    assert_eq!(
        x11_keysym_to_bytes_with_modes(0xFF51, true, None, 127, false),
        vec![0x1B, b'[', b'D']
    ); // Left
    assert_eq!(
        x11_keysym_to_bytes_with_modes(0xFF52, true, None, 127, false),
        vec![0x1B, b'[', b'A']
    ); // Up
    assert_eq!(
        x11_keysym_to_bytes_with_modes(0xFF53, true, None, 127, false),
        vec![0x1B, b'[', b'C']
    ); // Right
    assert_eq!(
        x11_keysym_to_bytes_with_modes(0xFF54, true, None, 127, false),
        vec![0x1B, b'[', b'B']
    ); // Down
}

#[test]
fn test_mode_switching_scenario() {
    // Simulate the exact scenario: bash -> vim -> bash

    // 1. In bash (normal mode = false), arrows should work
    let bash_up = x11_keysym_to_bytes_with_modes(0xFF52, true, None, 127, false);
    assert_eq!(
        bash_up,
        vec![0x1B, b'[', b'A'],
        "Bash: Up arrow should be ESC[A"
    );

    // 2. Open vim (application mode = true), arrows should work differently
    let vim_up = x11_keysym_to_bytes_with_modes(0xFF52, true, None, 127, true);
    assert_eq!(
        vim_up,
        vec![0x1B, b'O', b'A'],
        "Vim: Up arrow should be ESCOA"
    );

    // 3. Exit vim (back to normal mode = false), arrows should work again
    let bash_up_again = x11_keysym_to_bytes_with_modes(0xFF52, true, None, 127, false);
    assert_eq!(
        bash_up_again,
        vec![0x1B, b'[', b'A'],
        "Bash again: Up arrow should be ESC[A"
    );

    // Verify they're different sequences
    assert_ne!(
        bash_up, vim_up,
        "Bash and vim should send different sequences"
    );
    assert_eq!(bash_up, bash_up_again, "Bash should be consistent");
}

#[test]
fn test_multiple_mode_switches_all_arrows() {
    // Test all arrow keys through multiple mode switches
    // Simulates: bash -> vim -> bash -> less -> bash

    let arrow_keys = [
        (0xFF51, "Left", b'D'),
        (0xFF52, "Up", b'A'),
        (0xFF53, "Right", b'C'),
        (0xFF54, "Down", b'B'),
    ];

    for (keysym, name, letter) in arrow_keys {
        // Bash (normal mode)
        let normal1 = x11_keysym_to_bytes_with_modes(keysym, true, None, 127, false);
        assert_eq!(
            normal1,
            vec![0x1B, b'[', letter],
            "{} in bash should be ESC[{}",
            name,
            letter as char
        );

        // Vim (application mode)
        let app1 = x11_keysym_to_bytes_with_modes(keysym, true, None, 127, true);
        assert_eq!(
            app1,
            vec![0x1B, b'O', letter],
            "{} in vim should be ESCO{}",
            name,
            letter as char
        );

        // Back to bash
        let normal2 = x11_keysym_to_bytes_with_modes(keysym, true, None, 127, false);
        assert_eq!(
            normal2,
            vec![0x1B, b'[', letter],
            "{} in bash again should be ESC[{}",
            name,
            letter as char
        );

        // Less (application mode)
        let app2 = x11_keysym_to_bytes_with_modes(keysym, true, None, 127, true);
        assert_eq!(
            app2,
            vec![0x1B, b'O', letter],
            "{} in less should be ESCO{}",
            name,
            letter as char
        );

        // Back to bash again
        let normal3 = x11_keysym_to_bytes_with_modes(keysym, true, None, 127, false);
        assert_eq!(
            normal3,
            vec![0x1B, b'[', letter],
            "{} in bash final should be ESC[{}",
            name,
            letter as char
        );

        // Verify consistency
        assert_eq!(
            normal1, normal2,
            "{} normal mode should be consistent",
            name
        );
        assert_eq!(
            normal2, normal3,
            "{} normal mode should be consistent",
            name
        );
        assert_eq!(app1, app2, "{} application mode should be consistent", name);
        assert_ne!(
            normal1, app1,
            "{} sequences should differ between modes",
            name
        );
    }
}

#[test]
fn test_rapid_mode_switching() {
    // Test rapid switching like opening/closing vim multiple times
    for i in 0..10 {
        let is_app_mode = i % 2 == 1; // Alternate between modes
        let up = x11_keysym_to_bytes_with_modes(0xFF52, true, None, 127, is_app_mode);

        if is_app_mode {
            assert_eq!(up, vec![0x1B, b'O', b'A'], "Iteration {}: App mode", i);
        } else {
            assert_eq!(up, vec![0x1B, b'[', b'A'], "Iteration {}: Normal mode", i);
        }
    }
}

#[test]
fn test_function_keys() {
    assert_eq!(
        x11_keysym_to_bytes(0xFFBE, true, None),
        vec![0x1B, b'O', b'P']
    ); // F1
    assert_eq!(
        x11_keysym_to_bytes(0xFFBF, true, None),
        vec![0x1B, b'O', b'Q']
    ); // F2
}

#[test]
fn test_key_release_ignored() {
    assert_eq!(x11_keysym_to_bytes(0x0041, false, None), Vec::<u8>::new()); // A released
}

#[test]
fn test_unsupported_key() {
    assert_eq!(
        x11_keysym_to_bytes(0xFFFF + 1, true, None),
        Vec::<u8>::new()
    );
}

#[test]
fn test_control_characters() {
    let mut mods = ModifierState::new();
    mods.control = true;

    // Ctrl+C (uppercase C is 0x43, should become 0x03)
    assert_eq!(x11_keysym_to_bytes(0x0043, true, Some(&mods)), vec![0x03]);

    // Ctrl+c (lowercase c is 0x63, should also become 0x03)
    // This is what browsers actually send!
    assert_eq!(x11_keysym_to_bytes(0x0063, true, Some(&mods)), vec![0x03]);

    // Ctrl+A (uppercase A is 0x41, should become 0x01)
    assert_eq!(x11_keysym_to_bytes(0x0041, true, Some(&mods)), vec![0x01]);

    // Ctrl+a (lowercase a is 0x61, should also become 0x01)
    assert_eq!(x11_keysym_to_bytes(0x0061, true, Some(&mods)), vec![0x01]);

    // Ctrl+Z (uppercase Z is 0x5A, should become 0x1A)
    assert_eq!(x11_keysym_to_bytes(0x005A, true, Some(&mods)), vec![0x1A]);

    // Ctrl+z (lowercase z is 0x7A, should also become 0x1A)
    assert_eq!(x11_keysym_to_bytes(0x007A, true, Some(&mods)), vec![0x1A]);

    // Ctrl+[ should become ESC (0x1B)
    assert_eq!(x11_keysym_to_bytes(0x005B, true, Some(&mods)), vec![0x1B]);

    // Ctrl+d (lowercase d is 0x64, should become 0x04 - EOF)
    assert_eq!(x11_keysym_to_bytes(0x0064, true, Some(&mods)), vec![0x04]);
}

#[test]
fn test_modifier_tracking() {
    let mut mods = ModifierState::new();

    // Press left Control
    assert!(mods.update_modifier(0xFFE3, true));
    assert!(mods.control);
    assert!(!mods.shift);

    // Press right Shift
    assert!(mods.update_modifier(0xFFE2, true));
    assert!(mods.control);
    assert!(mods.shift);

    // Release Control
    assert!(mods.update_modifier(0xFFE3, false));
    assert!(!mods.control);
    assert!(mods.shift);

    // Non-modifier key should return false
    assert!(!mods.update_modifier(0x0041, true));
}

#[test]
fn test_mouse_event_left_click() {
    // Left click at character position (10, 5) with 19x38 pixel cells
    let seq = mouse_event_to_x11_sequence(190, 190, 1, 19, 38);

    // Should be: ESC [ M <button> <x> <y>
    // x = 10 + 33 = 43, y = 5 + 33 = 38, button = 0 (left)
    assert_eq!(seq.len(), 6);
    assert_eq!(seq[0], 0x1B); // ESC
    assert_eq!(seq[1], b'[');
    assert_eq!(seq[2], b'M');
    assert_eq!(seq[3], 0); // Left button press
    assert_eq!(seq[4], 43); // x = 10 + 33
    assert_eq!(seq[5], 38); // y = 5 + 33
}

#[test]
fn test_mouse_event_right_click() {
    // Right click at (0, 0) with 19x38 pixel cells
    let seq = mouse_event_to_x11_sequence(0, 0, 4, 19, 38);

    assert_eq!(seq.len(), 6);
    assert_eq!(seq[3], 2); // Right button (4 -> 2)
    assert_eq!(seq[4], 33); // x = 0 + 33
    assert_eq!(seq[5], 33); // y = 0 + 33
}

#[test]
fn test_mouse_event_drag() {
    // Drag with left button at (100, 200) with 19x38 pixel cells
    // Button mask: 1 (left) + 32 (drag) = 33
    let seq = mouse_event_to_x11_sequence(100, 200, 33, 19, 38);

    assert_eq!(seq.len(), 6);
    assert_eq!(seq[3], 32); // Drag: left button (0) + 32 = 32
}

#[test]
fn test_mouse_event_move() {
    // Mouse move (no button) at (50, 50)
    let seq = mouse_event_to_x11_sequence(50, 50, 0, 19, 38);

    assert_eq!(seq.len(), 6);
    assert_eq!(seq[3], 35); // Move/release
}

#[test]
fn test_mouse_event_middle_click() {
    // Middle click at (100, 100)
    let seq = mouse_event_to_x11_sequence(100, 100, 2, 19, 38);

    assert_eq!(seq.len(), 6);
    assert_eq!(seq[3], 1); // Middle button press
}

#[test]
fn test_mouse_event_coordinate_calculation() {
    // Test coordinate conversion
    // At pixel (0, 0) with 19x38 cells: col=0, row=0 -> x_char=33, y_char=33
    let seq = mouse_event_to_x11_sequence(0, 0, 1, 19, 38);
    assert_eq!(seq[4], 33); // x_char = 0 + 33
    assert_eq!(seq[5], 33); // y_char = 0 + 33

    // At pixel (190, 380) with 19x38 cells: col=10, row=10 -> x_char=43, y_char=43
    let seq2 = mouse_event_to_x11_sequence(190, 380, 1, 19, 38);
    assert_eq!(seq2[4], 43); // x_char = 10 + 33
    assert_eq!(seq2[5], 43); // y_char = 10 + 33
}

#[test]
fn test_modifier_state_default() {
    let mods = ModifierState::default();
    assert!(!mods.control);
    assert!(!mods.shift);
    assert!(!mods.alt);
}

#[test]
fn test_modifier_state_all_keys() {
    let mut mods = ModifierState::new();

    // Test all modifier keys
    assert!(mods.update_modifier(0xFFE3, true)); // Left Control
    assert!(mods.update_modifier(0xFFE4, true)); // Right Control (should still work)
    assert!(mods.update_modifier(0xFFE1, true)); // Left Shift
    assert!(mods.update_modifier(0xFFE2, true)); // Right Shift
    assert!(mods.update_modifier(0xFFE9, true)); // Left Alt
    assert!(mods.update_modifier(0xFFEA, true)); // Right Alt

    assert!(mods.control);
    assert!(mods.shift);
    assert!(mods.alt);

    // Release all
    mods.update_modifier(0xFFE3, false);
    mods.update_modifier(0xFFE1, false);
    mods.update_modifier(0xFFE9, false);

    assert!(!mods.control);
    assert!(!mods.shift);
    assert!(!mods.alt);
}

#[test]
fn test_modifier_state_combinations() {
    let mut mods = ModifierState::new();

    // Ctrl+Shift
    mods.update_modifier(0xFFE3, true);
    mods.update_modifier(0xFFE1, true);
    assert!(mods.control && mods.shift && !mods.alt);

    // Add Alt
    mods.update_modifier(0xFFE9, true);
    assert!(mods.control && mods.shift && mods.alt);

    // Release Shift
    mods.update_modifier(0xFFE1, false);
    assert!(mods.control && !mods.shift && mods.alt);
}

// Kitty keyboard protocol tests

#[test]
fn test_kitty_protocol_disabled() {
    // Level 0 should use legacy sequences
    let seq = x11_keysym_to_kitty_sequence(0xFF52, true, None, 127, false, 0);
    assert_eq!(seq, vec![0x1B, b'[', b'A']); // Legacy up arrow
}

#[test]
fn test_kitty_protocol_level_1_basic() {
    // Level 1: Basic key without modifiers
    // 'a' should be CSI 97 u
    let seq = x11_keysym_to_kitty_sequence(0x61, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[97u");
}

#[test]
fn test_kitty_protocol_level_1_ctrl() {
    // Level 1: Ctrl+C should be CSI 99 ; 4 u
    let mut mods = ModifierState::new();
    mods.control = true;
    let seq = x11_keysym_to_kitty_sequence(0x63, true, Some(&mods), 127, false, 1);
    assert_eq!(seq, b"\x1b[99;4u");
}

#[test]
fn test_kitty_protocol_level_1_shift() {
    // Level 1: Shift+A should be CSI 97 ; 1 u
    let mut mods = ModifierState::new();
    mods.shift = true;
    let seq = x11_keysym_to_kitty_sequence(0x61, true, Some(&mods), 127, false, 1);
    assert_eq!(seq, b"\x1b[97;1u");
}

#[test]
fn test_kitty_protocol_level_1_ctrl_shift() {
    // Level 1: Ctrl+Shift+C should be CSI 99 ; 5 u (4 + 1)
    let mut mods = ModifierState::new();
    mods.control = true;
    mods.shift = true;
    let seq = x11_keysym_to_kitty_sequence(0x63, true, Some(&mods), 127, false, 1);
    assert_eq!(seq, b"\x1b[99;5u");
}

#[test]
fn test_kitty_protocol_level_1_alt() {
    // Level 1: Alt+Enter should be CSI 13 ; 2 u
    let mut mods = ModifierState::new();
    mods.alt = true;
    let seq = x11_keysym_to_kitty_sequence(0xFF0D, true, Some(&mods), 127, false, 1);
    assert_eq!(seq, b"\x1b[13;2u");
}

#[test]
fn test_kitty_protocol_level_1_meta() {
    // Level 1: Meta+A should be CSI 97 ; 8 u
    let mut mods = ModifierState::new();
    mods.meta = true;
    let seq = x11_keysym_to_kitty_sequence(0x61, true, Some(&mods), 127, false, 1);
    assert_eq!(seq, b"\x1b[97;8u");
}

#[test]
fn test_kitty_protocol_level_1_all_modifiers() {
    // Level 1: Ctrl+Alt+Shift+Meta+A should be CSI 97 ; 15 u (1+2+4+8)
    let mut mods = ModifierState::new();
    mods.shift = true;
    mods.alt = true;
    mods.control = true;
    mods.meta = true;
    let seq = x11_keysym_to_kitty_sequence(0x61, true, Some(&mods), 127, false, 1);
    assert_eq!(seq, b"\x1b[97;15u");
}

#[test]
fn test_kitty_protocol_level_2_press() {
    // Level 2: Key press should include event type :1
    // Shift+A press should be CSI 97 ; 1 : 1 u
    let mut mods = ModifierState::new();
    mods.shift = true;
    let seq = x11_keysym_to_kitty_sequence(0x61, true, Some(&mods), 127, false, 2);
    assert_eq!(seq, b"\x1b[97;1:1u");
}

#[test]
fn test_kitty_protocol_level_2_release() {
    // Level 2: Key release should include event type :3
    // Shift+A release should be CSI 97 ; 1 : 3 u
    let mut mods = ModifierState::new();
    mods.shift = true;
    let seq = x11_keysym_to_kitty_sequence(0x61, false, Some(&mods), 127, false, 2);
    assert_eq!(seq, b"\x1b[97;1:3u");
}

#[test]
fn test_kitty_protocol_level_2_no_modifiers() {
    // Level 2: Even without modifiers, event type is included
    // 'a' press should be CSI 97 ; 0 : 1 u
    let seq = x11_keysym_to_kitty_sequence(0x61, true, None, 127, false, 2);
    assert_eq!(seq, b"\x1b[97;0:1u");
}

#[test]
fn test_kitty_protocol_special_keys() {
    // Test special keys with Kitty protocol
    // Enter
    let seq = x11_keysym_to_kitty_sequence(0xFF0D, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[13u");

    // Tab
    let seq = x11_keysym_to_kitty_sequence(0xFF09, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[9u");

    // Escape
    let seq = x11_keysym_to_kitty_sequence(0xFF1B, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[27u");
}

#[test]
fn test_kitty_protocol_arrow_keys() {
    // Arrow keys use special Unicode values in Kitty protocol
    // Up arrow
    let seq = x11_keysym_to_kitty_sequence(0xFF52, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[57444u");

    // Down arrow
    let seq = x11_keysym_to_kitty_sequence(0xFF54, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[57446u");

    // Left arrow
    let seq = x11_keysym_to_kitty_sequence(0xFF51, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[57443u");

    // Right arrow
    let seq = x11_keysym_to_kitty_sequence(0xFF53, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[57445u");
}

#[test]
fn test_kitty_protocol_function_keys() {
    // F1
    let seq = x11_keysym_to_kitty_sequence(0xFFBE, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[57376u");

    // F12
    let seq = x11_keysym_to_kitty_sequence(0xFFC9, true, None, 127, false, 1);
    assert_eq!(seq, b"\x1b[57387u");
}

#[test]
fn test_kitty_protocol_disambiguate_ctrl_i_tab() {
    // This is a key feature of Kitty protocol: disambiguate Ctrl+I from Tab
    let mut mods = ModifierState::new();
    mods.control = true;

    // Ctrl+I should be CSI 105 ; 4 u
    let ctrl_i = x11_keysym_to_kitty_sequence(0x69, true, Some(&mods), 127, false, 1);
    assert_eq!(ctrl_i, b"\x1b[105;4u");

    // Tab should be CSI 9 u
    let tab = x11_keysym_to_kitty_sequence(0xFF09, true, None, 127, false, 1);
    assert_eq!(tab, b"\x1b[9u");

    // They should be different
    assert_ne!(ctrl_i, tab);
}

#[test]
fn test_kitty_protocol_disambiguate_ctrl_m_enter() {
    // Another key feature: disambiguate Ctrl+M from Enter
    let mut mods = ModifierState::new();
    mods.control = true;

    // Ctrl+M should be CSI 109 ; 4 u
    let ctrl_m = x11_keysym_to_kitty_sequence(0x6D, true, Some(&mods), 127, false, 1);
    assert_eq!(ctrl_m, b"\x1b[109;4u");

    // Enter should be CSI 13 u
    let enter = x11_keysym_to_kitty_sequence(0xFF0D, true, None, 127, false, 1);
    assert_eq!(enter, b"\x1b[13u");

    // They should be different
    assert_ne!(ctrl_m, enter);
}

#[test]
fn test_kitty_protocol_backspace_configurable() {
    // Test that backspace code is respected
    // Backspace with DEL (127)
    let seq_del = x11_keysym_to_kitty_sequence(0xFF08, true, None, 127, false, 1);
    assert_eq!(seq_del, b"\x1b[127u");

    // Backspace with BS (8)
    let seq_bs = x11_keysym_to_kitty_sequence(0xFF08, true, None, 8, false, 1);
    assert_eq!(seq_bs, b"\x1b[8u");
}
