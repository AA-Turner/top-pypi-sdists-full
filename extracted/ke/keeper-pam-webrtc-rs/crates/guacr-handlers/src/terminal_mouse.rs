use guacr_terminal::{
    format_clipboard_instructions, handle_mouse_selection, mouse_event_to_x11_sequence,
    ModifierState, MouseSelection, SelectionResult, TerminalEmulator,
};
use log::{debug, info, trace, warn};

use crate::{is_mouse_event_allowed_readonly, HandlerSecuritySettings};

/// Output from handling a single mouse event.
pub struct MouseEventOutput {
    /// Instructions to send to Guacamole client
    pub to_client: Vec<String>,
    /// Bytes to send to the server (X11 mouse sequences)
    pub server_bytes: Vec<u8>,
    /// New clipboard text (Some if selection completed and copy allowed)
    pub new_clipboard: Option<String>,
}

impl MouseEventOutput {
    pub fn empty() -> Self {
        Self {
            to_client: Vec::new(),
            server_bytes: Vec::new(),
            new_clipboard: None,
        }
    }
}

#[allow(clippy::too_many_arguments)]
pub fn handle_mouse_event(
    mouse_event: guacr_terminal::MouseEvent,
    mouse_selection: &mut MouseSelection,
    terminal: &TerminalEmulator,
    security: &HandlerSecuritySettings,
    char_width: u32,
    char_height: u32,
    current_rows: u16,
    current_cols: u16,
    modifier_state: &ModifierState,
) -> MouseEventOutput {
    debug!(
        "Mouse event - button={}, pos=({},{}), term_mouse={}",
        mouse_event.button_mask,
        mouse_event.x_px,
        mouse_event.y_px,
        terminal.is_mouse_enabled()
    );

    let mut out = MouseEventOutput::empty();

    // Security: Check read-only mode for mouse clicks
    if security.read_only && !is_mouse_event_allowed_readonly(mouse_event.button_mask) {
        trace!("Mouse click blocked (read-only mode)");
        return out;
    }

    // Handle mouse events intelligently:
    // 1. If terminal has mouse mode enabled (vim/tmux) - send X11 sequences
    // 2. Otherwise, left-click drag = text selection (copy to clipboard)
    // 3. Hover with no buttons = ignored (prevents garbage)

    if terminal.is_mouse_enabled() && mouse_event.button_mask != 0 {
        debug!("Terminal mouse mode enabled - sending X11 sequences (no selection)");
        let mouse_seq = mouse_event_to_x11_sequence(
            mouse_event.x_px,
            mouse_event.y_px,
            mouse_event.button_mask as u8,
            char_width,
            char_height,
        );
        if !mouse_seq.is_empty() {
            trace!(
                "Mouse X11 sequence (button={}) at ({}, {})",
                mouse_event.button_mask,
                mouse_event.x_px,
                mouse_event.y_px
            );
            out.server_bytes = mouse_seq;
        }
    } else {
        debug!("Terminal mouse mode disabled - handling text selection");
        match handle_mouse_selection(
            mouse_event,
            mouse_selection,
            terminal,
            char_width,
            char_height,
            current_cols,
            current_rows,
            modifier_state.shift,
        ) {
            SelectionResult::InProgress(overlay_instructions) => {
                for instr in overlay_instructions {
                    out.to_client.push(instr);
                }
            }
            SelectionResult::Complete {
                text: selected_text,
                clear_instructions,
            } => {
                info!(
                    "Selection complete - {} chars selected",
                    selected_text.len()
                );

                if !security.is_copy_allowed() {
                    warn!("Selection copy blocked (copy disabled)");
                    for instr in clear_instructions {
                        out.to_client.push(instr);
                    }
                    return out;
                }

                debug!("Copying {} chars to clipboard", selected_text.len());

                // CRITICAL: Update local clipboard immediately to avoid race condition
                // If user pastes immediately after selecting, they expect the selected text
                // Without this, there's a race where the clipboard blob from client arrives
                // after the user has already pressed Ctrl+Shift+V
                out.new_clipboard = Some(selected_text.clone());
                debug!(
                    "Local clipboard updated immediately with {} chars",
                    selected_text.len()
                );

                for instr in clear_instructions {
                    out.to_client.push(instr);
                }

                let clipboard_stream_id = 10;
                let clipboard_instructions =
                    format_clipboard_instructions(&selected_text, clipboard_stream_id);
                info!(
                    "Sending {} clipboard instructions for {} chars to UI",
                    clipboard_instructions.len(),
                    selected_text.len()
                );
                for instr in clipboard_instructions {
                    debug!("Sending clipboard instruction: {}", instr);
                    out.to_client.push(instr);
                }
                info!("Clipboard instructions sent successfully to UI");
            }
            SelectionResult::None => {
                // No selection action (hovering, etc.) - ignore
            }
        }
    }

    out
}
