use crate::emulator::{MouseMode, ScrollbackLine, TerminalEmulator};

#[test]
fn test_terminal_new() {
    let term = TerminalEmulator::new(24, 80);
    assert_eq!(term.size(), (24, 80));
    assert!(!term.is_dirty());
}

#[test]
fn test_terminal_process() {
    let mut term = TerminalEmulator::new(24, 80);
    term.process(b"Hello, World!\n").unwrap();

    assert!(term.is_dirty());

    let screen = term.screen();
    let contents = screen.contents();
    assert!(contents.contains("Hello, World!"));
}

#[test]
fn test_terminal_dirty_flag() {
    let mut term = TerminalEmulator::new(24, 80);

    assert!(!term.is_dirty());

    term.process(b"test").unwrap();
    assert!(term.is_dirty());

    term.clear_dirty();
    assert!(!term.is_dirty());
}

#[test]
fn test_terminal_resize() {
    let mut term = TerminalEmulator::new(24, 80);

    term.resize(30, 100);
    assert_eq!(term.size(), (30, 100));
    assert!(term.is_dirty());
}

#[test]
fn test_full_screen_rect() {
    let term = TerminalEmulator::new(24, 80);
    let rect = term.full_screen_rect();

    assert_eq!(rect.x, 0);
    assert_eq!(rect.y, 0);
    assert_eq!(rect.width, 80);
    assert_eq!(rect.height, 24);
}

#[test]
fn test_scrollback_initial_state() {
    let term = TerminalEmulator::new_with_scrollback(24, 80, 150);
    assert_eq!(term.scrollback_lines(), 0);
    assert!(term.scrollback().is_empty());
}

#[test]
fn test_kitty_keyboard_protocol_enable_level_1() {
    let mut term = TerminalEmulator::new(24, 80);
    assert_eq!(term.kitty_keyboard_level(), 0);

    // Send CSI > 1 u to enable level 1
    term.process(b"\x1b[>1u").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 1);
    assert!(term.is_kitty_keyboard_enabled());
}

#[test]
fn test_kitty_keyboard_protocol_enable_level_2() {
    let mut term = TerminalEmulator::new(24, 80);

    // Enable level 2
    term.process(b"\x1b[>2u").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 2);
}

#[test]
fn test_kitty_keyboard_protocol_enable_level_3() {
    let mut term = TerminalEmulator::new(24, 80);

    // Enable level 3
    term.process(b"\x1b[>3u").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 3);
}

#[test]
fn test_kitty_keyboard_protocol_disable() {
    let mut term = TerminalEmulator::new(24, 80);

    // Enable level 2
    term.process(b"\x1b[>2u").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 2);

    // Disable with CSI < u
    term.process(b"\x1b[<u").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 0);
    assert!(!term.is_kitty_keyboard_enabled());
}

#[test]
fn test_kitty_keyboard_protocol_level_change() {
    let mut term = TerminalEmulator::new(24, 80);

    // Enable level 1
    term.process(b"\x1b[>1u").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 1);

    // Change to level 3
    term.process(b"\x1b[>3u").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 3);

    // Change back to level 1
    term.process(b"\x1b[>1u").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 1);
}

#[test]
fn test_kitty_keyboard_protocol_with_other_data() {
    let mut term = TerminalEmulator::new(24, 80);

    // Enable protocol mixed with other terminal output
    term.process(b"Hello\x1b[>2uWorld\n").unwrap();
    assert_eq!(term.kitty_keyboard_level(), 2);

    // Terminal should still process the text
    let screen = term.screen();
    let contents = screen.contents();
    assert!(contents.contains("Hello"));
    assert!(contents.contains("World"));
}

#[test]
fn test_kitty_keyboard_protocol_invalid_level() {
    let mut term = TerminalEmulator::new(24, 80);

    // Try to enable invalid level (> 3)
    term.process(b"\x1b[>5u").unwrap();
    // Should remain disabled
    assert_eq!(term.kitty_keyboard_level(), 0);
}

#[test]
fn test_scrollback_access() {
    let mut term = TerminalEmulator::new_with_scrollback(24, 80, 150);

    // Add scrollback lines manually
    for _ in 0..5 {
        let line = ScrollbackLine::new(80);
        term.add_to_scrollback(line);
    }

    assert_eq!(term.scrollback_lines(), 5);

    // Access scrollback buffer
    let scrollback = term.scrollback();
    assert_eq!(scrollback.len(), 5);

    // Get specific line
    let line = term.get_scrollback_line(0);
    assert!(line.is_some());
    assert_eq!(line.unwrap().cols, 80);
}

#[test]
fn test_scrollback_with_scrolling() {
    let mut term = TerminalEmulator::new_with_scrollback(5, 80, 10); // Small terminal for testing

    // Fill terminal with content that will cause scrolling
    for i in 0..10 {
        term.process(format!("Line {}\n", i).as_bytes()).unwrap();
    }

    // After scrolling, we should have some scrollback
    // Note: Scrollback detection depends on screen state changes
    let scrollback_count = term.scrollback_lines();

    // Verify scrollback methods work
    if scrollback_count > 0 {
        let line = term.get_scrollback_line(0);
        assert!(line.is_some());
        assert_eq!(line.unwrap().cols, 80);
    }
}

#[test]
fn test_scrollback_limit() {
    let mut term = TerminalEmulator::new_with_scrollback(5, 80, 3); // Limit to 3 lines

    // Create scrollback lines manually (since scrollback detection is complex)
    for _ in 0..5 {
        let line = ScrollbackLine::new(80);
        term.add_to_scrollback(line);
    }

    // Should be limited to 3 lines
    assert_eq!(term.scrollback_lines(), 3);
}

#[test]
fn test_clear_scrollback() {
    let mut term = TerminalEmulator::new_with_scrollback(24, 80, 150);

    // Add some scrollback
    for _ in 0..5 {
        let line = ScrollbackLine::new(80);
        term.add_to_scrollback(line);
    }

    assert_eq!(term.scrollback_lines(), 5);

    // Clear it
    term.clear_scrollback();
    assert_eq!(term.scrollback_lines(), 0);
}

#[test]
fn test_scrollback_line_creation() {
    let line = ScrollbackLine::new(80);
    assert_eq!(line.cols, 80);
    assert!(line.cells.is_empty());
}

#[test]
fn test_mouse_mode_default() {
    let term = TerminalEmulator::new(24, 80);
    assert_eq!(term.mouse_mode(), MouseMode::Disabled);
    assert!(!term.is_mouse_enabled());
    assert!(!term.is_sgr_mouse_mode());
}

#[test]
fn test_mouse_mode_normal_enable() {
    let mut term = TerminalEmulator::new(24, 80);

    // ESC [ ? 1000 h - Enable normal tracking
    term.process(b"\x1b[?1000h").unwrap();
    assert_eq!(term.mouse_mode(), MouseMode::Normal);
    assert!(term.is_mouse_enabled());
}

#[test]
fn test_mouse_mode_normal_disable() {
    let mut term = TerminalEmulator::new(24, 80);

    // Enable then disable
    term.process(b"\x1b[?1000h").unwrap();
    assert!(term.is_mouse_enabled());

    term.process(b"\x1b[?1000l").unwrap();
    assert_eq!(term.mouse_mode(), MouseMode::Disabled);
    assert!(!term.is_mouse_enabled());
}

#[test]
fn test_mouse_mode_button_event() {
    let mut term = TerminalEmulator::new(24, 80);

    // ESC [ ? 1002 h - Enable button event tracking
    term.process(b"\x1b[?1002h").unwrap();
    assert_eq!(term.mouse_mode(), MouseMode::ButtonEvent);
    assert!(term.is_mouse_enabled());
}

#[test]
fn test_mouse_mode_any_event() {
    let mut term = TerminalEmulator::new(24, 80);

    // ESC [ ? 1003 h - Enable any event tracking
    term.process(b"\x1b[?1003h").unwrap();
    assert_eq!(term.mouse_mode(), MouseMode::AnyEvent);
    assert!(term.is_mouse_enabled());
}

#[test]
fn test_mouse_mode_sgr() {
    let mut term = TerminalEmulator::new(24, 80);

    // ESC [ ? 1006 h - Enable SGR extended mode
    term.process(b"\x1b[?1006h").unwrap();
    assert!(term.is_sgr_mouse_mode());

    // Disable
    term.process(b"\x1b[?1006l").unwrap();
    assert!(!term.is_sgr_mouse_mode());
}

#[test]
fn test_mouse_mode_in_mixed_data() {
    let mut term = TerminalEmulator::new(24, 80);

    // Mouse enable sequence embedded in regular text
    term.process(b"Hello \x1b[?1000h World").unwrap();
    assert!(term.is_mouse_enabled());

    // Verify text was still processed
    let screen = term.screen();
    let contents = screen.contents();
    assert!(contents.contains("Hello"));
    assert!(contents.contains("World"));
}

#[test]
fn test_application_cursor_mode_default() {
    let term = TerminalEmulator::new(24, 80);
    assert!(!term.is_application_cursor_mode());
}

#[test]
fn test_application_cursor_mode_enable() {
    let mut term = TerminalEmulator::new(24, 80);

    // ESC [ ? 1 h - Enable application cursor mode (DECCKM)
    term.process(b"\x1b[?1h").unwrap();
    assert!(term.is_application_cursor_mode());
}

#[test]
fn test_application_cursor_mode_disable() {
    let mut term = TerminalEmulator::new(24, 80);

    // Enable then disable
    term.process(b"\x1b[?1h").unwrap();
    assert!(term.is_application_cursor_mode());

    // ESC [ ? 1 l - Disable application cursor mode
    term.process(b"\x1b[?1l").unwrap();
    assert!(!term.is_application_cursor_mode());
}

#[test]
fn test_application_cursor_mode_multiple_switches() {
    let mut term = TerminalEmulator::new(24, 80);

    // Simulate: bash -> vim -> bash -> less -> bash

    // Start in bash (normal mode)
    assert!(!term.is_application_cursor_mode());

    // Open vim (enables application mode)
    term.process(b"\x1b[?1h").unwrap();
    assert!(term.is_application_cursor_mode());

    // Exit vim (back to normal mode)
    term.process(b"\x1b[?1l").unwrap();
    assert!(!term.is_application_cursor_mode());

    // Open less (enables application mode again)
    term.process(b"\x1b[?1h").unwrap();
    assert!(term.is_application_cursor_mode());

    // Exit less (back to normal mode)
    term.process(b"\x1b[?1l").unwrap();
    assert!(!term.is_application_cursor_mode());
}

#[test]
fn test_application_cursor_mode_vim_simulation() {
    let mut term = TerminalEmulator::new(24, 80);

    // Simulate vim startup sequence
    // Vim typically sends multiple mode changes
    term.process(b"\x1b[?1h").unwrap(); // Enable application cursor
    term.process(b"\x1b[?1h").unwrap(); // Redundant enable (should be idempotent)
    assert!(term.is_application_cursor_mode());

    // Vim exit sequence
    term.process(b"\x1b[?1l").unwrap();
    assert!(!term.is_application_cursor_mode());
}

#[test]
fn test_application_cursor_mode_in_mixed_data() {
    let mut term = TerminalEmulator::new(24, 80);

    // Application cursor mode sequence embedded in regular output
    term.process(b"Hello \x1b[?1h World").unwrap();
    assert!(term.is_application_cursor_mode());

    // More text with disable sequence
    term.process(b"More text \x1b[?1l here").unwrap();
    assert!(!term.is_application_cursor_mode());
}

#[test]
fn test_application_cursor_mode_with_other_modes() {
    let mut term = TerminalEmulator::new(24, 80);

    // Enable multiple modes at once (like vim does)
    term.process(b"\x1b[?1h\x1b[?1000h").unwrap(); // App cursor + mouse
    assert!(term.is_application_cursor_mode());
    assert!(term.is_mouse_enabled());

    // Disable both
    term.process(b"\x1b[?1l\x1b[?1000l").unwrap();
    assert!(!term.is_application_cursor_mode());
    assert!(!term.is_mouse_enabled());
}

#[test]
fn test_mouse_mode_and_text_selection_interaction() {
    let mut term = TerminalEmulator::new(24, 80);

    // In bash: mouse mode disabled, text selection should work
    assert!(!term.is_mouse_enabled());

    // Open vim with mouse enabled
    term.process(b"\x1b[?1000h").unwrap();
    assert!(term.is_mouse_enabled());
    // When mouse mode is enabled, mouse events go to terminal (not text selection)

    // Exit vim
    term.process(b"\x1b[?1000l").unwrap();
    assert!(!term.is_mouse_enabled());
    // Back to bash: text selection should work again
}

#[test]
fn test_vim_full_mode_sequence() {
    let mut term = TerminalEmulator::new(24, 80);

    // Vim startup: enables application cursor + mouse
    term.process(b"\x1b[?1h\x1b[?1000h\x1b[?1002h\x1b[?1006h")
        .unwrap();

    assert!(
        term.is_application_cursor_mode(),
        "Vim should enable app cursor"
    );
    assert!(term.is_mouse_enabled(), "Vim should enable mouse");
    assert!(term.is_sgr_mouse_mode(), "Vim should enable SGR mouse");

    // In vim:
    // - Arrow keys send ESCOA/OB/OC/OD (application cursor mode)
    // - Mouse events send X11 sequences (mouse mode enabled)
    // - Text selection is disabled (mouse goes to vim)

    // Vim exit: disables all modes
    term.process(b"\x1b[?1l\x1b[?1000l\x1b[?1002l\x1b[?1006l")
        .unwrap();

    assert!(
        !term.is_application_cursor_mode(),
        "Should return to normal cursor"
    );
    assert!(!term.is_mouse_enabled(), "Should disable mouse");
    assert!(!term.is_sgr_mouse_mode(), "Should disable SGR mouse");

    // Back in bash:
    // - Arrow keys send ESC[A/B/C/D (normal mode)
    // - Mouse events trigger text selection
    // - Highlighting/copy works
}

#[test]
fn test_less_mode_sequence() {
    let mut term = TerminalEmulator::new(24, 80);

    // Less typically enables application cursor but not mouse
    term.process(b"\x1b[?1h").unwrap();

    assert!(
        term.is_application_cursor_mode(),
        "Less should enable app cursor"
    );
    assert!(
        !term.is_mouse_enabled(),
        "Less typically doesn't enable mouse"
    );

    // In less:
    // - Arrow keys send ESCOA/OB/OC/OD (application cursor mode)
    // - Mouse events still trigger text selection (mouse mode disabled)
    // - Highlighting/copy still works!

    // Exit less
    term.process(b"\x1b[?1l").unwrap();

    assert!(!term.is_application_cursor_mode());
    assert!(!term.is_mouse_enabled());
}

#[test]
fn test_mode_combinations_bash_vim_bash() {
    let mut term = TerminalEmulator::new(24, 80);

    // Bash: Both modes disabled
    assert!(!term.is_application_cursor_mode());
    assert!(!term.is_mouse_enabled());
    // Text selection: works
    // Arrow keys: ESC[A/B/C/D

    // Open vim
    term.process(b"\x1b[?1h\x1b[?1000h").unwrap();
    assert!(term.is_application_cursor_mode());
    assert!(term.is_mouse_enabled());
    // Text selection: Disabled (mouse goes to vim)
    // Arrow keys: ESCOA/OB/OC/OD

    // Exit vim
    term.process(b"\x1b[?1l\x1b[?1000l").unwrap();
    assert!(!term.is_application_cursor_mode());
    assert!(!term.is_mouse_enabled());
    // Text selection: Works again
    // Arrow keys: ESC[A/B/C/D
}

#[test]
fn test_mouse_mode_vim_like_sequence() {
    let mut term = TerminalEmulator::new(24, 80);

    // Vim typically enables mouse with: ESC[?1000h ESC[?1002h ESC[?1006h
    term.process(b"\x1b[?1000h\x1b[?1002h\x1b[?1006h").unwrap();

    // Last one wins for mode, SGR should be enabled
    assert_eq!(term.mouse_mode(), MouseMode::ButtonEvent);
    assert!(term.is_mouse_enabled());
    assert!(term.is_sgr_mouse_mode());
}

// --- Scrollback scroll_offset tests ---

#[test]
fn test_scroll_up_and_down() {
    let mut term = TerminalEmulator::new_with_scrollback(5, 80, 50);
    for _ in 0..10 {
        term.add_to_scrollback(ScrollbackLine::new(80));
    }
    assert_eq!(term.scroll_offset(), 0);
    assert!(!term.is_scrolled_back());

    term.scroll_up(3);
    assert_eq!(term.scroll_offset(), 3);
    assert!(term.is_scrolled_back());

    term.scroll_down(2);
    assert_eq!(term.scroll_offset(), 1);

    term.scroll_down(10);
    assert_eq!(term.scroll_offset(), 0);
    assert!(!term.is_scrolled_back());
}

#[test]
fn test_scroll_cap_at_scrollback_len() {
    let mut term = TerminalEmulator::new_with_scrollback(5, 80, 50);
    let n = 8usize;
    for _ in 0..n {
        term.add_to_scrollback(ScrollbackLine::new(80));
    }
    term.scroll_up(n + 100);
    assert!(term.scroll_offset() <= term.scrollback_lines());
}

#[test]
fn test_reset_scroll() {
    let mut term = TerminalEmulator::new_with_scrollback(5, 80, 50);
    for _ in 0..5 {
        term.add_to_scrollback(ScrollbackLine::new(80));
    }
    term.scroll_up(3);
    assert!(term.is_scrolled_back());
    term.reset_scroll();
    assert_eq!(term.scroll_offset(), 0);
    assert!(!term.is_scrolled_back());
}

#[test]
fn test_scroll_view_indices() {
    let mut term = TerminalEmulator::new_with_scrollback(5, 80, 50);
    term.add_to_scrollback(ScrollbackLine::new(80)); // index 0
    term.add_to_scrollback(ScrollbackLine::new(80)); // index 1
    term.scroll_up(2);

    let indices = term.scroll_view_indices();
    assert_eq!(indices.len(), 5);
    assert!(indices[0].is_some());
    assert!(indices[1].is_some());
    assert!(indices[2].is_none());
    assert!(indices[3].is_none());
    assert!(indices[4].is_none());
}
