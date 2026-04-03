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
    let opcode = extract_opcode(instr);
    matches!(
        opcode,
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
