// X11 keysym to terminal input byte conversion

/// Modifier key state tracker
///
/// Tracks which modifier keys are currently pressed (Control, Shift, Alt, Meta/Command)
#[derive(Debug, Default, Clone)]
pub struct ModifierState {
    pub control: bool,
    pub shift: bool,
    pub alt: bool,
    pub meta: bool, // Command key on Mac, Windows key on PC
}

impl ModifierState {
    pub fn new() -> Self {
        Self::default()
    }

    /// Update modifier state based on keysym
    ///
    /// Returns true if this was a modifier key that was handled
    pub fn update_modifier(&mut self, keysym: u32, pressed: bool) -> bool {
        match keysym {
            // Control keys
            0xFFE3 | 0xFFE4 => {
                self.control = pressed;
                true
            }
            // Shift keys
            0xFFE1 | 0xFFE2 => {
                self.shift = pressed;
                true
            }
            // Alt keys
            0xFFE9 | 0xFFEA => {
                self.alt = pressed;
                true
            }
            // Meta/Command keys (0xFFE7 = left meta, 0xFFE8 = right meta)
            0xFFE7 | 0xFFE8 => {
                self.meta = pressed;
                true
            }
            _ => false,
        }
    }
}

/// Convert X11 keysym to terminal input bytes
///
/// Guacamole protocol uses X11 keysyms for keyboard input.
/// This function converts them to the appropriate bytes to send to a terminal.
///
/// Uses default backspace code (127 = DEL).
///
/// # Arguments
///
/// * `keysym` - X11 keysym value
/// * `pressed` - Whether the key is pressed (true) or released (false)
/// * `modifiers` - Optional modifier state for control character handling
pub fn x11_keysym_to_bytes(
    keysym: u32,
    pressed: bool,
    modifiers: Option<&ModifierState>,
) -> Vec<u8> {
    x11_keysym_to_bytes_with_backspace(keysym, pressed, modifiers, 127)
}

/// Convert X11 keysym to terminal input bytes with configurable backspace
///
/// Like `x11_keysym_to_bytes` but allows specifying the backspace code.
///
/// # Arguments
///
/// * `keysym` - X11 keysym value
/// * `pressed` - Whether the key is pressed (true) or released (false)
/// * `modifiers` - Optional modifier state for control character handling
/// * `backspace_code` - Code to send for backspace key (127 = DEL, 8 = BS)
pub fn x11_keysym_to_bytes_with_backspace(
    keysym: u32,
    pressed: bool,
    modifiers: Option<&ModifierState>,
    backspace_code: u8,
) -> Vec<u8> {
    x11_keysym_to_bytes_with_modes(keysym, pressed, modifiers, backspace_code, false)
}

/// Convert X11 keysym to Kitty keyboard protocol sequence
///
/// Generates CSI u sequences according to the Kitty keyboard protocol specification.
/// Falls back to legacy sequences if kitty_level is 0.
///
/// # Kitty Protocol Levels
///
/// - Level 0: Disabled (uses legacy sequences)
/// - Level 1: Disambiguate escape codes (Ctrl+I vs Tab, Ctrl+M vs Enter)
/// - Level 2: Report event types (press=1, repeat=2, release=3)
/// - Level 3: Report alternate keys (base key + shifted key)
///
/// # Format
///
/// `CSI <unicode> ; <modifiers> : <event> u`
///
/// Where:
/// - unicode: Unicode codepoint of the key (decimal)
/// - modifiers: Bitmask (1=Shift, 2=Alt, 4=Ctrl, 8=Meta)
/// - event: 1=press, 2=repeat, 3=release (level 2+)
///
/// # Arguments
///
/// * `keysym` - X11 keysym value
/// * `pressed` - Whether the key is pressed (true) or released (false)
/// * `modifiers` - Optional modifier state for control character handling
/// * `backspace_code` - Code to send for backspace key (127 = DEL, 8 = BS)
/// * `application_cursor` - Whether terminal is in application cursor mode (for legacy fallback)
/// * `kitty_level` - Kitty keyboard protocol level (0 = disabled, 1-3 = enabled)
pub fn x11_keysym_to_kitty_sequence(
    keysym: u32,
    pressed: bool,
    modifiers: Option<&ModifierState>,
    backspace_code: u8,
    application_cursor: bool,
    kitty_level: u8,
) -> Vec<u8> {
    // Level 0 = disabled, use legacy sequences
    if kitty_level == 0 {
        return x11_keysym_to_bytes_with_modes(
            keysym,
            pressed,
            modifiers,
            backspace_code,
            application_cursor,
        );
    }

    // Convert keysym to Unicode codepoint
    let unicode = match keysym {
        // ASCII printable range
        0x0020..=0x007E => keysym,

        // Special keys - use their ASCII control codes or Unicode values
        0xFF0D => 13,                    // Enter (CR)
        0xFF08 => backspace_code as u32, // Backspace (DEL or BS)
        0xFF09 => 9,                     // Tab
        0xFF1B => 27,                    // Escape

        // Arrow keys - use special Unicode values (Kitty spec uses shifted values)
        0xFF51 => 57443, // Left
        0xFF52 => 57444, // Up
        0xFF53 => 57445, // Right
        0xFF54 => 57446, // Down

        // Navigation keys
        0xFF50 => 57423, // Home
        0xFF57 => 57424, // End
        0xFF55 => 57425, // Page Up
        0xFF56 => 57426, // Page Down
        0xFF63 => 57427, // Insert
        0xFFFF => 127,   // Delete

        // Function keys F1-F12 (use Kitty spec values)
        0xFFBE => 57376, // F1
        0xFFBF => 57377, // F2
        0xFFC0 => 57378, // F3
        0xFFC1 => 57379, // F4
        0xFFC2 => 57380, // F5
        0xFFC3 => 57381, // F6
        0xFFC4 => 57382, // F7
        0xFFC5 => 57383, // F8
        0xFFC6 => 57384, // F9
        0xFFC7 => 57385, // F10
        0xFFC8 => 57386, // F11
        0xFFC9 => 57387, // F12

        // Unsupported key - fall back to legacy
        _ => {
            return x11_keysym_to_bytes_with_modes(
                keysym,
                pressed,
                modifiers,
                backspace_code,
                application_cursor,
            )
        }
    };

    // Build modifier bitmask
    let mut mod_mask = 0u8;
    if let Some(mods) = modifiers {
        if mods.shift {
            mod_mask |= 1;
        }
        if mods.alt {
            mod_mask |= 2;
        }
        if mods.control {
            mod_mask |= 4;
        }
        if mods.meta {
            mod_mask |= 8;
        }
    }

    // Generate CSI u sequence: ESC [ <unicode> ; <modifiers> : <event> u
    let mut seq = vec![0x1B, b'[']; // ESC [

    // Unicode codepoint
    seq.extend_from_slice(unicode.to_string().as_bytes());

    // Add modifiers if present or if level >= 2 (need event type)
    if mod_mask > 0 || kitty_level >= 2 {
        seq.push(b';');
        seq.extend_from_slice(mod_mask.to_string().as_bytes());
    }

    // Level 2+: Add event type (1=press, 2=repeat, 3=release)
    if kitty_level >= 2 {
        seq.push(b':');
        seq.push(if pressed { b'1' } else { b'3' });
    }

    seq.push(b'u');
    seq
}

/// Convert X11 keysym to terminal input bytes with full mode support
///
/// Supports application cursor mode (DECCKM) for proper vim/less/tmux operation.
///
/// # Arguments
///
/// * `keysym` - X11 keysym value
/// * `pressed` - Whether the key is pressed (true) or released (false)
/// * `modifiers` - Optional modifier state for control character handling
/// * `backspace_code` - Code to send for backspace key (127 = DEL, 8 = BS)
/// * `application_cursor` - Whether terminal is in application cursor mode
pub fn x11_keysym_to_bytes_with_modes(
    keysym: u32,
    pressed: bool,
    modifiers: Option<&ModifierState>,
    backspace_code: u8,
    application_cursor: bool,
) -> Vec<u8> {
    // Only handle key press events
    if !pressed {
        return Vec::new();
    }

    // Handle control character combinations
    if let Some(mods) = modifiers {
        if mods.control {
            // Control + character combinations
            // X11 keysyms: uppercase A-Z = 0x0041-0x005A, lowercase a-z = 0x0061-0x007A
            // Browser sends LOWERCASE keysyms when typing Ctrl+C (keysym 99 = 'c')
            match keysym {
                // Control + A-Z (uppercase): convert to 0x01-0x1A
                0x0041..=0x005A => {
                    // A-Z: subtract 0x40 to get control character
                    // Ctrl+A (0x41) -> 0x01, Ctrl+C (0x43) -> 0x03, etc.
                    return vec![(keysym - 0x40) as u8];
                }
                // Control + a-z (lowercase): convert to 0x01-0x1A
                // This is the common case - browsers send lowercase when Ctrl is held
                0x0061..=0x007A => {
                    // a-z: subtract 0x60 to get control character
                    // Ctrl+a (0x61) -> 0x01, Ctrl+c (0x63) -> 0x03, etc.
                    return vec![(keysym - 0x60) as u8];
                }
                // Control + [ (0x5B) -> ESC (0x1B)
                0x005B => return vec![0x1B],
                // Control + \ (0x5C) -> FS (0x1C)
                0x005C => return vec![0x1C],
                // Control + ] (0x5D) -> GS (0x1D)
                0x005D => return vec![0x1D],
                // Control + ^ (0x5E) -> RS (0x1E)
                0x005E => return vec![0x1E],
                // Control + _ (0x5F) -> US (0x1F)
                0x005F => return vec![0x1F],
                // Control + @ (0x40) -> NUL (0x00)
                0x0040 => return vec![0x00],
                // Control + Space (0x20) -> NUL (0x00) - some terminals use this
                0x0020 if mods.control => return vec![0x00],
                _ => {}
            }
        }
    }

    match keysym {
        // Pre-computed control characters (0x01-0x1F).
        // Guacamole.Keyboard derives the keysym from the keypress charCode rather than the
        // keydown keysym for unreliable keys (any printable key held with a modifier).
        // For Ctrl+R the keypress charCode is 18 (DC2), so keysym 18 arrives here instead of
        // 0x0072 ('r'). Pass it through directly — it is already the correct terminal byte.
        0x01..=0x1F => vec![keysym as u8],

        // Return/Enter
        0xFF0D => vec![b'\r'],

        // Backspace - use configurable code (127 = DEL, 8 = BS)
        0xFF08 => vec![backspace_code],

        // Tab
        0xFF09 => vec![b'\t'],

        // Escape
        0xFF1B => vec![0x1B],

        // Arrow keys - check application cursor mode (DECCKM)
        // Normal mode: ESC[A/B/C/D
        // Application mode: ESCOA/OB/OC/OD (used by vim, less, tmux)
        0xFF51 => {
            // Left
            if application_cursor {
                vec![0x1B, b'O', b'D']
            } else {
                vec![0x1B, b'[', b'D']
            }
        }
        0xFF52 => {
            // Up
            if application_cursor {
                vec![0x1B, b'O', b'A']
            } else {
                vec![0x1B, b'[', b'A']
            }
        }
        0xFF53 => {
            // Right
            if application_cursor {
                vec![0x1B, b'O', b'C']
            } else {
                vec![0x1B, b'[', b'C']
            }
        }
        0xFF54 => {
            // Down
            if application_cursor {
                vec![0x1B, b'O', b'B']
            } else {
                vec![0x1B, b'[', b'B']
            }
        }

        // Home/End
        0xFF50 => vec![0x1B, b'[', b'H'], // Home
        0xFF57 => vec![0x1B, b'[', b'F'], // End

        // Page Up/Down
        0xFF55 => vec![0x1B, b'[', b'5', b'~'], // Page Up
        0xFF56 => vec![0x1B, b'[', b'6', b'~'], // Page Down

        // Insert/Delete
        0xFF63 => vec![0x1B, b'[', b'2', b'~'], // Insert
        0xFFFF => vec![0x1B, b'[', b'3', b'~'], // Delete

        // Function keys F1-F12
        0xFFBE => vec![0x1B, b'O', b'P'],             // F1
        0xFFBF => vec![0x1B, b'O', b'Q'],             // F2
        0xFFC0 => vec![0x1B, b'O', b'R'],             // F3
        0xFFC1 => vec![0x1B, b'O', b'S'],             // F4
        0xFFC2 => vec![0x1B, b'[', b'1', b'5', b'~'], // F5
        0xFFC3 => vec![0x1B, b'[', b'1', b'7', b'~'], // F6
        0xFFC4 => vec![0x1B, b'[', b'1', b'8', b'~'], // F7
        0xFFC5 => vec![0x1B, b'[', b'1', b'9', b'~'], // F8
        0xFFC6 => vec![0x1B, b'[', b'2', b'0', b'~'], // F9
        0xFFC7 => vec![0x1B, b'[', b'2', b'1', b'~'], // F10
        0xFFC8 => vec![0x1B, b'[', b'2', b'3', b'~'], // F11
        0xFFC9 => vec![0x1B, b'[', b'2', b'4', b'~'], // F12

        // ASCII printable characters (0x0020 - 0x007E) - must come after special keys
        0x0020..=0x007E => vec![keysym as u8],

        // Unsupported key
        _ => Vec::new(),
    }
}

/// Convert mouse event to X11 mouse escape sequence for terminal mouse support
///
/// Terminal applications (vim, tmux) use X11 mouse escape sequences:
/// `ESC [ M <button> <x> <y>`
///
/// Where:
/// - button: encodes button (0-2) + action (32 for drag, 35 for release)
/// - x, y: character cell coordinates (1-based, +32 to make printable)
///
/// # Arguments
///
/// * `x_px` - X coordinate in pixels
/// * `y_px` - Y coordinate in pixels
/// * `button_mask` - Button mask: 0=move, 1=left, 2=middle, 4=right, 32=drag
/// * `char_width` - Width of character cell in pixels
/// * `char_height` - Height of character cell in pixels
///
/// # Returns
///
/// X11 mouse escape sequence bytes, or empty Vec if invalid
pub fn mouse_event_to_x11_sequence(
    x_px: u32,
    y_px: u32,
    button_mask: u8,
    char_width: u32,
    char_height: u32,
) -> Vec<u8> {
    // Convert pixel coordinates to character cell coordinates (0-based)
    let col = (x_px / char_width.max(1)) as u8;
    let row = (y_px / char_height.max(1)) as u8;

    // X11 mouse protocol uses 1-based coordinates + 32 to make them printable ASCII
    let x_char = col.saturating_add(33); // +1 for 1-based, +32 for printable
    let y_char = row.saturating_add(33);

    // Determine button and action
    // Button mask: 0=move, 1=left, 2=middle, 4=right, 32=drag
    let is_drag = (button_mask & 32) != 0;
    let button = button_mask & 0x07; // Extract button (0-7)

    // Encode button: 0=left, 1=middle, 2=right
    // Action: 0=press, 3=release, 32=drag
    // First map button: 1->0 (left), 2->1 (middle), 4->2 (right)
    let mapped_button = match button {
        1 => 0, // Left
        2 => 1, // Middle
        4 => 2, // Right
        0 => {
            // Move (no button pressed)
            if is_drag {
                return Vec::new(); // Can't drag without a button
            }
            return vec![0x1B, b'[', b'M', 35, x_char, y_char]; // Move/release
        }
        _ => return Vec::new(), // Unknown button
    };

    let button_code = if is_drag {
        // Drag: mapped_button + 32
        mapped_button + 32
    } else {
        // Button press
        mapped_button
    };

    // X11 mouse escape sequence: ESC [ M <button> <x> <y>
    let seq = vec![0x1B, b'[', b'M', button_code, x_char, y_char];

    seq
}
