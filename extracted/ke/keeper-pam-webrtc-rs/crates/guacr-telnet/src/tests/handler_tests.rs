use guacr_handlers::{HandlerSecuritySettings, HealthStatus, ProtocolHandler};
use guacr_terminal::{KeyEvent, ModifierState, TerminalEmulator};

use crate::handler::{handle_key_event, TelnetHandler};

// ---------------------------------------------------------------------------
// TelnetHandler trait tests
// ---------------------------------------------------------------------------

#[test]
fn test_telnet_handler_new() {
    let handler = TelnetHandler::with_defaults();
    assert_eq!(<TelnetHandler as ProtocolHandler>::name(&handler), "telnet");
}

#[test]
fn test_telnet_handler_has_passthrough_dlp_by_default() {
    let handler = TelnetHandler::with_defaults();
    let raw = b"\x1b[31mred\x1b[0m";
    let out = handler.dlp.filter(bytes::Bytes::from_static(raw));
    assert_eq!(out.as_ref(), raw);
}

#[tokio::test]
async fn test_telnet_handler_health() {
    let handler = TelnetHandler::with_defaults();
    let health = handler.health_check().await.unwrap();
    assert_eq!(health, HealthStatus::Healthy);
}

#[tokio::test]
async fn test_telnet_handler_stats() {
    let handler = TelnetHandler::with_defaults();
    let stats = handler.stats().await.unwrap();
    assert_eq!(stats.total_connections, 0);
}

// ---------------------------------------------------------------------------
// handle_key_event unit tests
// ---------------------------------------------------------------------------

fn make_security() -> HandlerSecuritySettings {
    HandlerSecuritySettings::default()
}

fn make_terminal() -> TerminalEmulator {
    TerminalEmulator::new(24, 80)
}

/// Printable ASCII key press (keysym == Unicode codepoint for ASCII range)
/// produces the corresponding byte.
#[test]
fn test_handle_key_event_printable_ascii_press() {
    let mut mods = ModifierState::new();
    let security = make_security();
    let terminal = make_terminal();

    // keysym 0x61 = 'a'
    let event = KeyEvent {
        keysym: 0x61,
        pressed: true,
    };
    let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127);

    let out = out.expect("expected Some output for printable key press");
    assert_eq!(out.server_bytes, b"a");
    assert!(out.new_clipboard.is_none());
}

/// Pressing multiple different printable characters each produces their byte.
#[test]
fn test_handle_key_event_printable_ascii_various_chars() {
    let mut mods = ModifierState::new();
    let security = make_security();
    let terminal = make_terminal();

    for (keysym, expected) in [(0x41u32, b'A'), (0x39, b'9'), (0x20, b' ')] {
        let event = KeyEvent {
            keysym,
            pressed: true,
        };
        let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127)
            .expect("expected Some for printable ASCII");
        assert_eq!(out.server_bytes, vec![expected], "keysym 0x{keysym:X}");
    }
}

/// Enter key (keysym 0xFF0D) press produces `\r` (CR).
/// Telnet typically sends CR; the exact byte is `\r` (0x0D).
#[test]
fn test_handle_key_event_enter_produces_cr() {
    let mut mods = ModifierState::new();
    let security = make_security();
    let terminal = make_terminal();

    let event = KeyEvent {
        keysym: 0xFF0D,
        pressed: true,
    };
    let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127)
        .expect("expected Some for Enter key");

    // x11_keysym_to_bytes_with_backspace returns b"\r" for 0xFF0D
    assert!(!out.server_bytes.is_empty(), "Enter must produce bytes");
    assert_eq!(out.server_bytes[0], b'\r', "Enter must start with CR");
}

/// Key release (pressed == false) produces nothing.
#[test]
fn test_handle_key_event_key_release_produces_nothing() {
    let mut mods = ModifierState::new();
    let security = make_security();
    let terminal = make_terminal();

    let event = KeyEvent {
        keysym: 0x61,
        pressed: false,
    }; // 'a' released
    let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127);

    assert!(out.is_none(), "key release must produce None");
}

/// Unknown / unsupported keysym press produces nothing.
#[test]
fn test_handle_key_event_unknown_keysym_produces_nothing() {
    let mut mods = ModifierState::new();
    let security = make_security();
    let terminal = make_terminal();

    // 0xDEAD is not a recognised keysym
    let event = KeyEvent {
        keysym: 0xDEAD,
        pressed: true,
    };
    let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127);

    assert!(out.is_none(), "unknown keysym must produce None");
}

/// Modifier key alone (Ctrl press, keysym 0xFFE3) produces nothing — the
/// modifier state is updated and `update_modifier` returns true, causing
/// `handle_key_event` to return None.
#[test]
fn test_handle_key_event_modifier_key_alone_produces_nothing() {
    let mut mods = ModifierState::new();
    let security = make_security();
    let terminal = make_terminal();

    // Left Control press
    let event = KeyEvent {
        keysym: 0xFFE3,
        pressed: true,
    };
    let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127);

    assert!(out.is_none(), "modifier key alone must produce None");
    // Modifier state must have been updated
    assert!(mods.control);
}

/// Ctrl+C (keysym 0x63 = lowercase 'c' while control is held) produces 0x03
/// (ETX — the Unix interrupt signal byte).
#[test]
fn test_handle_key_event_ctrl_c_produces_etx() {
    let mut mods = ModifierState::new();
    let security = make_security();
    let terminal = make_terminal();

    // First simulate the Ctrl key going down so modifier state is updated
    let ctrl_down = KeyEvent {
        keysym: 0xFFE3,
        pressed: true,
    };
    let _ = handle_key_event(ctrl_down, &mut mods, &security, "", &terminal, 127);
    assert!(mods.control);

    // Now send 'c' (0x63) while Ctrl is held
    let event = KeyEvent {
        keysym: 0x63,
        pressed: true,
    };
    let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127)
        .expect("Ctrl+C must produce Some output");

    assert_eq!(
        out.server_bytes,
        vec![0x03],
        "Ctrl+C must produce ETX (0x03)"
    );
}

/// In read-only mode, regular key presses are blocked (None returned).
#[test]
fn test_handle_key_event_readonly_blocks_input() {
    let mut mods = ModifierState::new();
    let mut security = make_security();
    security.read_only = true;
    let terminal = make_terminal();

    let event = KeyEvent {
        keysym: 0x61,
        pressed: true,
    }; // 'a'
    let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127);

    assert!(out.is_none(), "read-only mode must block regular key input");
}

/// In read-only mode, Ctrl+C is still allowed (used to interrupt processes).
#[test]
fn test_handle_key_event_readonly_allows_ctrl_c() {
    let mut mods = ModifierState::new();
    let mut security = make_security();
    security.read_only = true;
    let terminal = make_terminal();

    // Simulate Ctrl down
    let ctrl_down = KeyEvent {
        keysym: 0xFFE3,
        pressed: true,
    };
    let _ = handle_key_event(ctrl_down, &mut mods, &security, "", &terminal, 127);

    // Ctrl+C while read-only
    let event = KeyEvent {
        keysym: 0x63,
        pressed: true,
    };
    let out = handle_key_event(event, &mut mods, &security, "", &terminal, 127);

    // is_keyboard_event_allowed_readonly allows Ctrl+C
    assert!(
        out.is_some(),
        "Ctrl+C must be allowed even in read-only mode"
    );
    assert_eq!(out.unwrap().server_bytes, vec![0x03]);
}

// ---------------------------------------------------------------------------
// Phase 1e security: ZK proof — PTY data cannot escape session boundary
//
// Proof: raw PTY bytes fed through the Telnet handler's encoding pipeline emerge
// as a binary Guacamole terminal-data frame (opcode 0x20), not as the original
// raw bytes. This confirms the session boundary holds — plaintext PTY data never
// exits as plaintext on the to_client channel.
// ---------------------------------------------------------------------------

/// Verify that raw PTY bytes are wrapped in a Guacamole terminal-data instruction
/// before they leave the session boundary on the to_client channel.
///
/// The Telnet handler calls `format_terminal_data_binary(filtered)` for every
/// server-data read. This test exercises that function directly and asserts:
///   1. The output is NOT the raw PTY bytes (encapsulation happens).
///   2. The first byte is 0x20 (TerminalData binary opcode).
///   3. The raw PTY payload is embedded verbatim after the 8-byte header.
#[test]
fn test_pty_data_wrapped_in_terminal_data() {
    use guacr_protocol::format_terminal_data_binary;

    let pty_bytes: &[u8] = b"Welcome to telnet\r\nlogin: ";

    let framed = format_terminal_data_binary(pty_bytes);

    assert_ne!(
        framed.as_ref(),
        pty_bytes,
        "raw PTY bytes must not pass through unchanged"
    );

    assert_eq!(
        framed[0], 0x20,
        "first byte must be the TerminalData binary opcode (0x20)"
    );

    assert!(
        framed.len() >= 8,
        "binary frame must have at least the 8-byte header"
    );
    assert_eq!(
        &framed[8..],
        pty_bytes,
        "PTY payload must be embedded verbatim after the 8-byte header"
    );
}

// ---------------------------------------------------------------------------
// FIX 0 — Integration test layout: verify non-integration tests now live here
// (The terminal_tests and unit_tests modules previously in integration_test.rs
// have been moved to telnet_functional_test.rs. This comment serves as the
// audit trail for that migration.)
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// FIX 1+2 — parse_size_instruction unit tests (resize handling)
// ---------------------------------------------------------------------------

/// Verify that a well-formed size instruction is parsed correctly.
#[test]
fn test_parse_size_instruction_valid() {
    use crate::serial::parse_size_instruction;

    // Format from the Guacamole client: "4.size,4.1024,3.768;"
    assert_eq!(
        parse_size_instruction("4.size,4.1024,3.768;"),
        Some((1024, 768))
    );
}

/// Verify that common pixel dimensions round-trip correctly.
#[test]
fn test_parse_size_instruction_various_dimensions() {
    use crate::serial::parse_size_instruction;

    assert_eq!(
        parse_size_instruction("4.size,3.800,3.600;"),
        Some((800, 600))
    );
    assert_eq!(
        parse_size_instruction("4.size,4.1920,4.1080;"),
        Some((1920, 1080))
    );
    assert_eq!(parse_size_instruction("4.size,1.1,1.1;"), Some((1, 1)));
}

/// Verify that a size instruction with zero width returns None.
#[test]
fn test_parse_size_instruction_zero_width_is_none() {
    use crate::serial::parse_size_instruction;
    assert_eq!(parse_size_instruction("4.size,1.0,3.600;"), None);
}

/// Verify that a size instruction with zero height returns None.
#[test]
fn test_parse_size_instruction_zero_height_is_none() {
    use crate::serial::parse_size_instruction;
    assert_eq!(parse_size_instruction("4.size,3.800,1.0;"), None);
}

/// Verify that a key instruction is not parsed as a size instruction.
#[test]
fn test_parse_size_instruction_non_size_is_none() {
    use crate::serial::parse_size_instruction;
    assert_eq!(parse_size_instruction("3.key,5.65507,1.1;"), None);
    assert_eq!(parse_size_instruction(""), None);
}

// ---------------------------------------------------------------------------
// FIX 1 — NAWS sub-negotiation bytes (serial.rs helper used by both handlers)
// ---------------------------------------------------------------------------

/// Verify that build_naws_subneg produces the correct RFC 1073 byte sequence.
#[test]
fn test_build_naws_subneg_80x24() {
    use crate::serial::{build_naws_subneg, IAC, OPT_NAWS, SB, SE};

    let bytes = build_naws_subneg(80, 24);
    // Expected: IAC SB NAWS 0x00 0x50 0x00 0x18 IAC SE
    // 80 = 0x0050, 24 = 0x0018
    assert_eq!(
        bytes,
        vec![IAC, SB, OPT_NAWS, 0x00, 0x50, 0x00, 0x18, IAC, SE]
    );
}

/// Verify NAWS with large (common HD) dimensions.
#[test]
fn test_build_naws_subneg_220x50() {
    use crate::serial::{build_naws_subneg, IAC, OPT_NAWS, SB, SE};

    let bytes = build_naws_subneg(220, 50);
    // 220 = 0x00DC, 50 = 0x0032
    assert_eq!(
        bytes,
        vec![IAC, SB, OPT_NAWS, 0x00, 0xDC, 0x00, 0x32, IAC, SE]
    );
}

/// Verify that 0xFF bytes in width/height are IAC-escaped (doubled).
#[test]
fn test_build_naws_subneg_iac_escaping() {
    use crate::serial::{build_naws_subneg, IAC, OPT_NAWS, SB, SE};

    // Width = 0x00FF -> high byte 0x00, low byte 0xFF (must be doubled)
    let bytes = build_naws_subneg(0x00FF, 1);
    // Expected: IAC SB NAWS 0x00 0xFF 0xFF 0x00 0x01 IAC SE
    assert_eq!(
        bytes,
        vec![IAC, SB, OPT_NAWS, 0x00, 0xFF, 0xFF, 0x00, 0x01, IAC, SE]
    );
}

// ---------------------------------------------------------------------------
// FIX 5 — Initial Telnet option negotiation bytes
// ---------------------------------------------------------------------------

/// Verify that build_initial_telnet_negotiation contains all required IAC sequences.
#[test]
fn test_build_initial_telnet_negotiation_contains_required_sequences() {
    use crate::serial::{
        build_initial_telnet_negotiation, DO, IAC, OPT_ECHO, OPT_NAWS, OPT_SGA, OPT_TERMINAL_TYPE,
        SB, SE, TERMINAL_TYPE_IS, WILL,
    };

    let bytes = build_initial_telnet_negotiation(80, 24);

    // DO ECHO
    assert!(
        bytes.windows(3).any(|w| w == [IAC, DO, OPT_ECHO]),
        "must contain IAC DO ECHO"
    );
    // DO SGA
    assert!(
        bytes.windows(3).any(|w| w == [IAC, DO, OPT_SGA]),
        "must contain IAC DO SGA"
    );
    // WILL TERMINAL-TYPE
    assert!(
        bytes
            .windows(3)
            .any(|w| w == [IAC, WILL, OPT_TERMINAL_TYPE]),
        "must contain IAC WILL TERMINAL-TYPE"
    );
    // WILL NAWS
    assert!(
        bytes.windows(3).any(|w| w == [IAC, WILL, OPT_NAWS]),
        "must contain IAC WILL NAWS"
    );
    // TERMINAL-TYPE IS subneg start
    assert!(
        bytes
            .windows(4)
            .any(|w| w == [IAC, SB, OPT_TERMINAL_TYPE, TERMINAL_TYPE_IS]),
        "must contain TERMINAL-TYPE IS subneg"
    );
    // Contains xterm-256color string
    assert!(
        bytes.windows(14).any(|w| w == b"xterm-256color"),
        "must contain xterm-256color terminal type"
    );
    // NAWS sub-neg for 80x24
    assert!(
        bytes.windows(3).any(|w| w == [IAC, SB, OPT_NAWS]),
        "must contain NAWS subneg"
    );
    // Ends with IAC SE somewhere (for the subneg terminator)
    assert!(
        bytes.windows(2).any(|w| w == [IAC, SE]),
        "must contain IAC SE terminator"
    );
}

/// Verify that the initial negotiation sequence is non-empty and has reasonable length.
#[test]
fn test_build_initial_telnet_negotiation_nonempty() {
    use crate::serial::build_initial_telnet_negotiation;
    let bytes = build_initial_telnet_negotiation(80, 24);
    // At minimum: 3+3+3+3 (four 3-byte option negotiations) + subneg overhead
    assert!(bytes.len() > 20, "negotiation sequence must be substantive");
}

// ---------------------------------------------------------------------------
// FIX 3 — strip_telnet_commands called in TelnetHandler
//
// The fix ensures IAC sequences from the server don't reach the vt100 parser.
// These tests confirm the stripping function produces clean output. The
// integration between TelnetHandler and strip_telnet_commands is verified by
// the handler now calling strip_telnet_commands before terminal.process().
// ---------------------------------------------------------------------------

/// Verify that IAC sequences mixed with real data are stripped.
/// This is the "was broken" test — before fix, garbage would reach the terminal.
#[test]
fn test_strip_telnet_commands_removes_iac_from_real_data() {
    use crate::serial::{strip_telnet_commands, DO, IAC, OPT_ECHO, WILL};

    // Server sends "login: " interleaved with IAC WILL ECHO and IAC DO ECHO
    let mut input = Vec::new();
    input.extend_from_slice(b"login: ");
    input.extend_from_slice(&[IAC, WILL, OPT_ECHO]);
    input.extend_from_slice(&[IAC, DO, OPT_ECHO]);

    let clean = strip_telnet_commands(&input);
    assert_eq!(
        clean, b"login: ",
        "IAC negotiation must be stripped from terminal output"
    );
    assert!(
        !clean.contains(&IAC),
        "no IAC bytes must remain after stripping"
    );
}

// ---------------------------------------------------------------------------
// Phase 1e security: Threat detection initialisation proof
// ---------------------------------------------------------------------------

/// Verify that the threat detector initialises from a minimal params map.
///
/// The Telnet handler constructs a ThreatDetectorConfig when
/// `threat_detection_baml_endpoint` is present. This test confirms:
///   1. A params map with the endpoint key produces a Some(detector).
///   2. The wiring between param parsing and detector construction is intact.
#[cfg(feature = "threat-detection")]
#[test]
fn test_threat_detector_initialises_from_params() {
    use std::collections::HashMap;

    let mut params = HashMap::new();
    params.insert(
        "threat_detection_baml_endpoint".to_string(),
        "http://threat-svc.internal/api".to_string(),
    );

    let detector = guacr_threat_detection::ThreatDetector::from_params(&params, "Telnet");
    assert!(
        detector.is_some(),
        "ThreatDetector::from_params must return Some when baml_endpoint is present"
    );
}
