// Helper functions for recording: opcode extraction, drawing instruction detection,
// timestamp injection.

use std::time::{SystemTime, UNIX_EPOCH};

/// Extract the opcode from a Guacamole protocol instruction string.
/// Format: "LENGTH.OPCODE,LENGTH.ARG1,...;"
pub fn extract_opcode(instr: &str) -> &str {
    if let Some(dot) = instr.find('.') {
        let after_dot = &instr[dot + 1..];
        let end = after_dot
            .find(',')
            .or_else(|| after_dot.find(';'))
            .unwrap_or(after_dot.len());
        &after_dot[..end]
    } else {
        ""
    }
}

/// Check whether an instruction is a drawing/output instruction that should
/// be excluded when `recording_exclude_output` is set.
/// Sync and layer-0 size are always kept for timing and dimensions.
pub fn is_drawing_instruction(instr: &str) -> bool {
    // Guacamole opcodes are always lowercase per spec, but normalize defensively
    // so the filter cannot be bypassed by sending "IMG" instead of "img".
    let opcode_lower = extract_opcode(instr).to_ascii_lowercase();
    matches!(
        opcode_lower.as_str(),
        "img"
            | "blob"
            | "end"
            | "copy"
            | "transfer"
            | "rect"
            | "cfill"
            | "cstroke"
            | "cursor"
            | "shade"
            | "dispose"
            | "move"
            | "audio"
            | "video"
            | "png"
            | "arc"
            | "line"
            | "close"
            | "clip"
            | "push"
            | "pop"
            | "body"
    )
}

/// Whether an instruction is a binary opcode frame rather than a text Guacamole
/// instruction.
///
/// A text instruction always opens with its length prefix, so byte 0 is an ASCII digit.
/// A binary frame opens with its opcode (`[opcode][flags][reserved u16][len u32]`), and
/// no opcode falls in `0x30..=0x39`, so the first byte separates the two exactly.
pub fn is_binary_frame(instruction: &[u8]) -> bool {
    instruction
        .first()
        .is_some_and(|byte| !byte.is_ascii_digit())
}

/// Whether a binary opcode frame carries session content, and so must be dropped when
/// `recording_exclude_output` is set.
///
/// This is the binary counterpart of [`is_drawing_instruction`], and the terminal family
/// needs it: running the text classifier over a lossy UTF-8 view of a binary frame finds
/// no length prefix and therefore never matches, which left the setting a silent no-op
/// for SSH, telnet, database and mainframe sessions.
pub fn is_binary_output_frame(frame: &[u8]) -> bool {
    use guacr_protocol::Opcode;

    // Spelled through the enum so a renamed or renumbered opcode is a compile error
    // here rather than a filter that quietly stops matching.
    const OUTPUT_OPCODES: [u8; 5] = [
        Opcode::Image as u8,
        Opcode::ImageDelta as u8,
        Opcode::Audio as u8,
        Opcode::Cursor as u8,
        Opcode::TerminalData as u8,
    ];

    frame
        .first()
        .is_some_and(|opcode| OUTPUT_OPCODES.contains(opcode))
}

/// Inject a Guacamole-protocol-encoded timestamp argument into an instruction.
/// Replaces the trailing ";" with ",LEN.TIMESTAMP;".
pub fn inject_timestamp(instr: &str) -> String {
    let ts = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_millis()
        .to_string();
    let len = ts.len();
    if let Some(stripped) = instr.strip_suffix(';') {
        format!("{},{}.{};", stripped, len, ts)
    } else {
        // Malformed instruction -- append anyway
        format!("{},{}.{};", instr, len, ts)
    }
}
