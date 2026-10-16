// Tests for the terminal mouse event orchestrator.
//
// These cover the two permission gates specifically. Before terminal_mouse moved
// out of guacr-handlers the gates read a HandlerSecuritySettings directly and had
// no test at all; now that the caller resolves them into MousePermissions, the
// wiring is a public API boundary worth pinning.

use crate::{
    handle_mouse_event, ModifierState, MouseEvent, MousePermissions, MouseSelection,
    TerminalEmulator,
};

const COLS: u16 = 80;
const ROWS: u16 = 24;
const CHAR_W: u32 = 9;
const CHAR_H: u32 = 18;

fn permissions(buttons_blocked: bool, copy_allowed: bool) -> MousePermissions {
    MousePermissions {
        buttons_blocked,
        copy_allowed,
    }
}

/// Terminal with X11 mouse reporting turned on (DECSET 1000).
fn terminal_with_mouse_mode() -> TerminalEmulator {
    let mut terminal = TerminalEmulator::new(ROWS, COLS);
    terminal.process(b"\x1b[?1000h").expect("enable mouse mode");
    assert!(
        terminal.is_mouse_enabled(),
        "DECSET 1000 should enable mouse reporting"
    );
    terminal
}

/// Terminal holding a word to select, with mouse reporting off so the left
/// button drives text selection instead of X11 sequences.
fn terminal_with_text() -> TerminalEmulator {
    let mut terminal = TerminalEmulator::new(ROWS, COLS);
    terminal.process(b"hello world").expect("write text");
    assert!(
        !terminal.is_mouse_enabled(),
        "selection path requires mouse reporting off"
    );
    terminal
}

fn click(button_mask: u32, col: u32, row: u32) -> MouseEvent {
    MouseEvent {
        x_px: col * CHAR_W,
        y_px: row * CHAR_H,
        button_mask,
    }
}

fn handle(
    event: MouseEvent,
    selection: &mut MouseSelection,
    terminal: &TerminalEmulator,
    perms: &MousePermissions,
) -> crate::MouseEventOutput {
    handle_mouse_event(
        event,
        selection,
        terminal,
        perms,
        CHAR_W,
        CHAR_H,
        ROWS,
        COLS,
        &ModifierState::default(),
    )
}

#[test]
fn buttons_blocked_suppresses_x11_sequence() {
    let terminal = terminal_with_mouse_mode();
    let mut selection = MouseSelection::new();

    let out = handle(
        click(1, 5, 3),
        &mut selection,
        &terminal,
        &permissions(true, true),
    );

    assert!(
        out.server_bytes.is_empty(),
        "blocked button must not reach the server, got {:?}",
        out.server_bytes
    );
    assert!(
        out.to_client.is_empty(),
        "blocked button sends nothing back"
    );
    assert!(out.new_clipboard.is_none());
}

#[test]
fn buttons_allowed_emits_x11_sequence() {
    let terminal = terminal_with_mouse_mode();
    let mut selection = MouseSelection::new();

    let out = handle(
        click(1, 5, 3),
        &mut selection,
        &terminal,
        &permissions(false, true),
    );

    assert!(
        !out.server_bytes.is_empty(),
        "allowed button in terminal mouse mode must produce an X11 sequence"
    );
}

/// Drag across "hello" and return the output of the button-release event, which
/// is the one that completes the selection.
fn drag_and_release(perms: &MousePermissions) -> crate::MouseEventOutput {
    let terminal = terminal_with_text();
    let mut selection = MouseSelection::new();

    let _ = handle(click(1, 0, 0), &mut selection, &terminal, perms);
    let _ = handle(click(1, 5, 0), &mut selection, &terminal, perms);
    handle(click(0, 5, 0), &mut selection, &terminal, perms)
}

#[test]
fn copy_allowed_returns_selected_text() {
    let out = drag_and_release(&permissions(false, true));

    let clipboard = out
        .new_clipboard
        .expect("completed selection with copy allowed must yield clipboard text");
    assert!(
        clipboard.contains("hello"),
        "expected the dragged word, got {clipboard:?}"
    );
    assert!(
        out.to_client.iter().any(|i| i.contains("clipboard")),
        "clipboard instructions must be sent to the client"
    );
}

#[test]
fn copy_denied_drops_selected_text() {
    let out = drag_and_release(&permissions(false, false));

    assert!(
        out.new_clipboard.is_none(),
        "copy disabled must not populate the clipboard, got {:?}",
        out.new_clipboard
    );
    assert!(
        !out.to_client.iter().any(|i| i.contains("clipboard")),
        "copy disabled must not emit clipboard instructions, got {:?}",
        out.to_client
    );
}
