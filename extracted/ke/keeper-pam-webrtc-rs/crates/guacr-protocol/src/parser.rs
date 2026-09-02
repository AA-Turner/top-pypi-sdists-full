// Guacamole protocol parser (zero-copy)
//
// Complete-buffer front end over `StreamingParser`: use this when a whole
// instruction is already in hand (a data-channel message, a clipboard blob), and
// `StreamingParser` directly when reading a byte stream whose instruction
// boundaries are not yet known. Both share one implementation of the wire format
// so they cannot disagree about it.

use bytes::Bytes;
use std::str;

use crate::streaming::{PeekError, StreamingParser};

/// Parsed Guacamole instruction (zero-copy)
///
/// Uses string slices that reference the original Bytes buffer.
/// No allocations needed for parsing.
#[derive(Debug, Clone)]
pub struct Instruction<'a> {
    pub opcode: &'a str,
    pub args: Vec<&'a str>,
}

/// Guacamole protocol parser (zero-copy)
///
/// Parses Guacamole protocol instructions directly from Bytes without
/// allocating Strings. Uses string slices that reference the original buffer.
pub struct GuacamoleParser;

impl GuacamoleParser {
    /// Parse a single instruction from Bytes (zero-copy)
    ///
    /// Returns instruction with string slices referencing the original buffer.
    /// No allocations needed.
    ///
    /// # Format
    ///
    /// `<opcode_len>.<opcode>,<arg1_len>.<arg1>,<arg2_len>.<arg2>;`
    ///
    /// # Example
    ///
    /// ```
    /// use guacr_protocol::GuacamoleParser;
    /// use bytes::Bytes;
    ///
    /// let data = Bytes::from("3.key,5.65507,1.1;");
    /// let instr = GuacamoleParser::parse_instruction(&data).unwrap();
    /// assert_eq!(instr.opcode, "key");
    /// assert_eq!(instr.args, vec!["65507", "1"]);
    /// ```
    pub fn parse_instruction(data: &Bytes) -> Result<Instruction<'_>, ParseError> {
        // Convert to &str for parsing (zero-copy if Bytes is valid UTF-8)
        let text = str::from_utf8(data.as_ref()).map_err(|_| ParseError::InvalidUtf8)?;

        Self::parse_instruction_str(text)
    }

    /// Parse instruction from string slice (zero-copy)
    ///
    /// Works with any string slice. Trailing bytes after the first instruction's
    /// terminator are ignored; use [`Self::parse_instructions`] to read them all.
    pub fn parse_instruction_str(text: &str) -> Result<Instruction<'_>, ParseError> {
        let (instruction, _consumed) = Self::parse_one(text)?;
        Ok(instruction)
    }

    /// Parse one instruction, returning it plus the number of bytes consumed
    /// (including the trailing `;`).
    ///
    /// Delegates to [`StreamingParser::peek_instruction`], which is the single
    /// implementation of the wire format for the whole crate. Element boundaries
    /// come from each element's declared length — a count of CHARACTERS, not bytes
    /// — never from scanning for `;` or `,`, both of which are legal inside a
    /// value.
    fn parse_one(text: &str) -> Result<(Instruction<'_>, usize), ParseError> {
        let peeked = StreamingParser::peek_instruction(text.as_bytes()).map_err(map_peek_error)?;
        let total_length = peeked.total_length_in_buffer;
        Ok((
            Instruction {
                opcode: peeked.opcode,
                args: peeked.args.into_vec(),
            },
            total_length,
        ))
    }

    /// Parse every complete instruction in a buffer.
    ///
    /// Each instruction's extent comes from its declared element lengths, so a
    /// `;` inside a value does not end it. A trailing incomplete instruction is
    /// not an error — it is left unparsed for the caller to retry with more bytes.
    pub fn parse_instructions(data: &Bytes) -> Result<Vec<Instruction<'_>>, ParseError> {
        let text = str::from_utf8(data.as_ref()).map_err(|_| ParseError::InvalidUtf8)?;

        let mut instructions = Vec::new();
        let mut remaining = text;

        while !remaining.is_empty() {
            match Self::parse_one(remaining) {
                Ok((instr, consumed)) => {
                    instructions.push(instr);
                    remaining = &remaining[consumed..];
                }
                // A trailing partial instruction is not an error: callers stream
                // buffers in and re-parse once more bytes arrive.
                Err(ParseError::MissingTerminator) => break,
                Err(e) => return Err(e),
            }
        }

        Ok(instructions)
    }
}

/// Maps the streaming parser's error onto this module's coarser taxonomy.
///
/// `Incomplete` becomes `MissingTerminator`: for a complete-buffer caller, "the
/// declared element lengths and terminator have not all arrived" and "this buffer
/// is not a whole instruction" are the same condition. The streaming parser's
/// detailed messages are dropped here because `ParseError`'s variants carry no
/// payload — callers wanting the detail should use `StreamingParser` directly.
fn map_peek_error(err: PeekError) -> ParseError {
    match err {
        PeekError::Incomplete => ParseError::MissingTerminator,
        PeekError::Utf8Error(_) => ParseError::InvalidUtf8,
        PeekError::InvalidFormat(_) => ParseError::InvalidFormat,
    }
}

/// Parse error
#[derive(Debug, Clone, PartialEq)]
pub enum ParseError {
    InvalidUtf8,
    /// The buffer does not hold a complete instruction — either an element is
    /// shorter than its declared character count, or the terminator is absent.
    MissingTerminator,
    InvalidFormat,
    /// Retained for API compatibility. No longer produced: a non-numeric length
    /// field now surfaces as `InvalidFormat`, and a declared count that exceeds
    /// the available characters is truncation (`MissingTerminator`), not a length
    /// error — `;` and `,` are legal value characters, so a short value is never
    /// by itself evidence of corruption.
    InvalidLength,
}

impl std::fmt::Display for ParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ParseError::InvalidUtf8 => write!(f, "Invalid UTF-8"),
            ParseError::MissingTerminator => write!(f, "Missing semicolon terminator"),
            ParseError::InvalidFormat => write!(f, "Invalid instruction format"),
            ParseError::InvalidLength => write!(f, "Invalid length value"),
        }
    }
}

impl std::error::Error for ParseError {}
