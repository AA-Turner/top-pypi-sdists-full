// guacr-protocol: Guacamole protocol instruction formatting and Telnet constants
//
// Provides utilities for formatting Guacamole protocol instructions
// according to the official Apache Guacamole protocol specification.

pub(crate) mod advanced;
pub(crate) mod binary;
pub(crate) mod drawing;
pub(crate) mod layers;
pub(crate) mod parser;
pub mod streaming;
pub(crate) mod streams;
pub mod telnet;
pub(crate) mod text_optimized;

pub use advanced::{
    // Instructions
    format_ack,
    format_error,
    format_nest,
    format_pipe,
    format_transfer,
    // Status codes
    STATUS_CLIENT_BAD_REQUEST,
    STATUS_CLIENT_BAD_TYPE,
    STATUS_CLIENT_FORBIDDEN,
    STATUS_CLIENT_OVERRUN,
    STATUS_CLIENT_TIMEOUT,
    STATUS_CLIENT_TOO_MANY,
    STATUS_CLIENT_UNAUTHORIZED,
    STATUS_RESOURCE_CLOSED,
    STATUS_RESOURCE_CONFLICT,
    STATUS_SERVER_ERROR,
    STATUS_UPSTREAM_ERROR,
    STATUS_UPSTREAM_NOT_FOUND,
    STATUS_UPSTREAM_TIMEOUT,
    STATUS_UPSTREAM_UNAVAILABLE,
};
pub use binary::{
    BinaryEncoder, ImageFormat, Opcode, BINARY_PROTOCOL_OVERHEAD, FLAG_COMPRESSED, FLAG_ENCRYPTED,
    FRAME_PROTOCOL_OVERHEAD, MAX_SAFE_PAYLOAD_SIZE, TOTAL_PROTOCOL_OVERHEAD,
};
pub use drawing::*;
pub use layers::*;
pub use parser::{GuacamoleParser, Instruction, ParseError};
pub use streaming::{
    GuacdInstruction, GuacdParser, GuacdParserError, OpcodeAction, OwnedInstruction, PeekError,
    PeekedInstruction, SpecialOpcode, StreamingParser, StreamingParserError, ARG_SEP,
    DISCONNECT_OPCODE, ELEM_SEP, ERROR_OPCODE, INST_TERM, SIZE_OPCODE,
};
pub use streams::{
    format_audio, format_bell_audio, format_blob, format_chunked_blobs, format_clipboard,
    format_clipboard_text, format_end, format_video, parse_clipboard_blob,
};
pub use text_optimized::TextProtocolEncoder;

/// Format a Guacamole protocol instruction
///
/// Helper function to format instructions with proper length prefixes
pub fn format_instruction(opcode: &str, args: &[&str]) -> String {
    let mut result = String::new();

    // Opcode with length prefix (character count, not byte count per Guacamole spec)
    result.push_str(&opcode.chars().count().to_string());
    result.push('.');
    result.push_str(opcode);

    // Arguments with length prefixes (character count, not byte count per Guacamole spec)
    for arg in args {
        result.push(',');
        result.push_str(&arg.chars().count().to_string());
        result.push('.');
        result.push_str(arg);
    }

    result.push(';');
    result
}

#[cfg(test)]
mod tests;
