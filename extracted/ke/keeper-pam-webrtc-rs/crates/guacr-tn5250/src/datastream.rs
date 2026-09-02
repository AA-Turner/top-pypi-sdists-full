//! 5250 Data Stream Parser
//!
//! Parses IBM 5250 data stream records as used by the AS/400 (iSeries) platform.
//! The 5250 data stream is a block-mode protocol where the host sends complete
//! screen updates and the client responds with modified field data.
//!
//! ## Record Format
//!
//! Every 5250 record has a header:
//! - 2 bytes: Record length (big-endian, includes header)
//! - 1 byte: Record type (0x04 = data flowing to display, 0x00 = response)
//! - 1 byte: Reserved (flags)
//! - 1 byte: Operation code
//!
//! ## Reference
//!
//! IBM 5494 Remote Control Unit - Functions Reference (SA21-9247)
//! IBM 5250 Information Display System - Functions Reference (SA21-9247)

use crate::ebcdic;
use crate::ebcdic::CodePage;
use log::{debug, trace, warn};

/// Default EBCDIC code page for 5250 (AS/400 uses CP 037).
pub(crate) const DEFAULT_CODE_PAGE: CodePage = CodePage::Cp037;

/// Minimum valid record length: 2 (length) + 1 (type) + 1 (reserved) + 1 (opcode).
pub(crate) const MIN_RECORD_LEN: usize = 5;

// ---------------------------------------------------------------------------
// Error types
// ---------------------------------------------------------------------------

/// Errors that can occur while parsing 5250 data stream records.
#[derive(Debug, thiserror::Error)]
pub enum Tn5250Error {
    #[error("record too short: need at least {MIN_RECORD_LEN} bytes, got {0}")]
    RecordTooShort(usize),

    #[error("record length field ({field_len}) exceeds available data ({available})")]
    RecordLengthMismatch { field_len: usize, available: usize },

    #[error("unknown operation code: 0x{0:02X}")]
    UnknownOpCode(u8),

    #[error("truncated order 0x{order:02X} at offset {offset}: need {need} bytes, have {have}")]
    TruncatedOrder {
        order: u8,
        offset: usize,
        need: usize,
        have: usize,
    },

    #[error("invalid SBA address: row={row}, col={col}")]
    InvalidAddress { row: u8, col: u8 },

    #[error("unexpected end of data at offset {0}")]
    UnexpectedEnd(usize),
}

// ---------------------------------------------------------------------------
// Operation codes
// ---------------------------------------------------------------------------

/// 5250 operation codes sent in the record header.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpCode {
    /// Write to Display -- primary command for screen output.
    WriteToDisplay,
    /// Clear the entire display and reset fields.
    ClearUnit,
    /// Clear the Format Table (removes field definitions).
    ClearFormatTable,
    /// Write to Display (alternate encoding, same semantics as WriteToDisplay).
    WriteToDisplayAlt,
}

impl OpCode {
    /// Parse an operation code byte into the enum.
    pub fn from_byte(b: u8) -> Result<Self, Tn5250Error> {
        match b {
            0x01 | 0x11 => {
                if b == 0x11 {
                    Ok(OpCode::WriteToDisplayAlt)
                } else {
                    Ok(OpCode::WriteToDisplay)
                }
            }
            0x02 => Ok(OpCode::ClearUnit),
            0x04 => Ok(OpCode::ClearFormatTable),
            other => Err(Tn5250Error::UnknownOpCode(other)),
        }
    }
}

// ---------------------------------------------------------------------------
// Field Control Word
// ---------------------------------------------------------------------------

/// Field shift type -- controls what kind of data can be entered.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FieldShift {
    /// Any character is accepted (default).
    Alpha,
    /// Only alphabetic characters (A-Z, a-z, space, period, comma, hyphen, plus).
    AlphaOnly,
    /// Numeric with special characters.
    Numeric,
    /// Digits only (0-9).
    NumericOnly,
    /// Signed numeric (digits plus leading sign).
    SignedNumeric,
    /// Katakana / DBCS support.
    Katakana,
}

/// Field Control Word (FCW) -- a 2-byte value defining field behaviour.
///
/// Layout of the first byte:
///   bit 7 (MSB): bypass (protected / output-only field)
///   bit 6: duplication / field exit required
///   bit 5: modified data tag
///   bits 4-2: field shift (000=alpha, 001=alpha-only, 010=numeric,
///             011=numeric-only, 100=katakana, 111=signed-numeric)
///   bit 1: auto-enter after field is filled
///   bit 0: field exit required
///
/// Layout of the second byte:
///   bit 7: mandatory fill
///   bit 6: right-adjust with zero fill
///   bit 5: right-adjust with blank fill
///   bit 4: mandatory entry
///   bits 3-0: reserved / cursor progression
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FieldControlWord {
    /// Field is protected (bypass / output-only).
    pub bypass: bool,
    /// Modified Data Tag -- set when the field has been modified.
    pub modified: bool,
    /// Type of data the field accepts.
    pub shift: FieldShift,
    /// Field must be completely filled before the operator can leave it.
    pub mandatory_fill: bool,
    /// Right-adjust with zero fill on field exit.
    pub right_adjust_zero: bool,
    /// Right-adjust with blank fill on field exit.
    pub right_adjust_blank: bool,
    /// Mandatory entry -- field cannot be skipped.
    pub mandatory_entry: bool,
    /// Auto-enter when the field is completely filled.
    pub auto_enter: bool,
    /// Field exit required (Tab/Enter must be pressed to leave).
    pub field_exit_required: bool,
    /// Duplication allowed.
    pub duplication: bool,
    /// Raw first byte for callers that need the original bits.
    pub raw0: u8,
    /// Raw second byte.
    pub raw1: u8,
}

impl FieldControlWord {
    /// Decode a Field Control Word from its two raw bytes.
    pub fn from_bytes(b0: u8, b1: u8) -> Self {
        let bypass = (b0 & 0x80) != 0;
        let duplication = (b0 & 0x40) != 0;
        let modified = (b0 & 0x20) != 0;
        let shift_bits = (b0 >> 2) & 0x07;
        let auto_enter = (b0 & 0x02) != 0;
        let field_exit_required = (b0 & 0x01) != 0;

        let shift = match shift_bits {
            0b000 => FieldShift::Alpha,
            0b001 => FieldShift::AlphaOnly,
            0b010 => FieldShift::Numeric,
            0b011 => FieldShift::NumericOnly,
            0b100 => FieldShift::Katakana,
            0b111 => FieldShift::SignedNumeric,
            _ => {
                warn!(
                    "Unknown field shift bits 0b{:03b} in FCW byte 0x{:02X}, defaulting to Alpha",
                    shift_bits, b0
                );
                FieldShift::Alpha
            }
        };

        let mandatory_fill = (b1 & 0x80) != 0;
        let right_adjust_zero = (b1 & 0x40) != 0;
        let right_adjust_blank = (b1 & 0x20) != 0;
        let mandatory_entry = (b1 & 0x10) != 0;

        FieldControlWord {
            bypass,
            modified,
            shift,
            mandatory_fill,
            right_adjust_zero,
            right_adjust_blank,
            mandatory_entry,
            auto_enter,
            field_exit_required,
            duplication,
            raw0: b0,
            raw1: b1,
        }
    }

    /// Encode the FCW back into its two-byte representation.
    pub fn to_bytes(&self) -> [u8; 2] {
        // Reconstruct from the raw bytes stored at parse time; callers who
        // construct a FieldControlWord manually should set raw0/raw1.
        [self.raw0, self.raw1]
    }
}

// ---------------------------------------------------------------------------
// Extended attribute
// ---------------------------------------------------------------------------

/// Extended attribute set via the WEA (Write Extended Attribute) order.
///
/// The 5250 protocol supports a small set of extended attributes that
/// modify character appearance.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ExtendedAttribute {
    /// Attribute type byte.
    pub attr_type: u8,
    /// Attribute value byte.
    pub attr_value: u8,
}

// ---------------------------------------------------------------------------
// Start of Header data
// ---------------------------------------------------------------------------

/// Data carried by the SOH (Start of Header) order.
///
/// SOH defines screen-level formatting parameters. The length byte following
/// the 0x01 order code indicates how many additional bytes are in the SOH.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SohData {
    /// Length of the SOH data (not including the order byte and length byte).
    pub length: u8,
    /// Raw SOH payload bytes (interpretation is application-specific).
    pub data: Vec<u8>,
}

// ---------------------------------------------------------------------------
// Orders
// ---------------------------------------------------------------------------

/// An order within a Write to Display data stream.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Order {
    /// Start of Header -- screen-level formatting.
    Soh(SohData),

    /// Repeat to Address -- fill from the current position to (row, col) with
    /// the given EBCDIC character byte.
    Ra(u16, u16, u8),

    /// Erase to Address -- blank from the current position to (row, col).
    Ea(u16, u16),

    /// Transparent Data -- raw bytes that should be placed as-is.
    Td(Vec<u8>),

    /// Set Buffer Address -- move the output cursor to (row, col).
    Sba(u16, u16),

    /// Write Extended Attribute.
    Wea(ExtendedAttribute),

    /// Start Field -- defines an input field at the current position.
    Sf(FieldControlWord),

    /// Insert Cursor -- place the visible cursor at the current position.
    Ic,
}

// ---------------------------------------------------------------------------
// Data stream items
// ---------------------------------------------------------------------------

/// A single item in the parsed 5250 data stream: either an order or a
/// character to write to the screen.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DataStreamItem5250 {
    /// A structured order (SBA, SF, RA, etc.).
    Order(Order),
    /// A displayable character (EBCDIC byte value).
    Character(u8),
}

// ---------------------------------------------------------------------------
// Parsed record
// ---------------------------------------------------------------------------

/// A fully parsed 5250 record.
#[derive(Debug, Clone)]
pub struct Record5250 {
    /// Raw record type byte from the header.
    pub record_type: u8,
    /// Parsed operation code.
    pub opcode: OpCode,
    /// The ordered sequence of items (orders and characters) in this record.
    pub orders: Vec<DataStreamItem5250>,
}

// ---------------------------------------------------------------------------
// Address decoding
// ---------------------------------------------------------------------------

/// Decode a 5250 buffer address from the (row, col) byte pair.
///
/// 5250 addresses are 1-based in the wire format. This function returns
/// 0-based (row, col).
///
/// # Errors
///
/// Returns `Tn5250Error::InvalidAddress` if either byte is zero (which is
/// invalid in the 1-based addressing scheme).
pub fn decode_address(row: u8, col: u8) -> Result<(u16, u16), Tn5250Error> {
    if row == 0 || col == 0 {
        return Err(Tn5250Error::InvalidAddress { row, col });
    }
    Ok(((row as u16) - 1, (col as u16) - 1))
}

/// Encode a 0-based (row, col) into the 1-based wire format.
pub fn encode_address(row: u16, col: u16) -> (u8, u8) {
    ((row + 1) as u8, (col + 1) as u8)
}

// ---------------------------------------------------------------------------
// Record parser
// ---------------------------------------------------------------------------

/// Parse a single 5250 record from the given byte slice.
///
/// `data` should start at the first byte of the record (the high byte of the
/// length field). The parser will consume up to the number of bytes indicated
/// by the length field.
///
/// # Errors
///
/// Returns a `Tn5250Error` if the data is malformed.
pub fn parse_5250_record(data: &[u8]) -> Result<Record5250, Tn5250Error> {
    if data.len() < MIN_RECORD_LEN {
        return Err(Tn5250Error::RecordTooShort(data.len()));
    }

    let record_len = ((data[0] as usize) << 8) | (data[1] as usize);
    if record_len > data.len() {
        return Err(Tn5250Error::RecordLengthMismatch {
            field_len: record_len,
            available: data.len(),
        });
    }

    let record_type = data[2];
    let _reserved = data[3];
    let opcode_byte = data[4];
    let opcode = OpCode::from_byte(opcode_byte)?;

    debug!(
        "5250 record: len={}, type=0x{:02X}, opcode={:?}",
        record_len, record_type, opcode
    );

    // For ClearUnit and ClearFormatTable, there is no payload beyond the header.
    let orders = match opcode {
        OpCode::ClearUnit | OpCode::ClearFormatTable => Vec::new(),
        OpCode::WriteToDisplay | OpCode::WriteToDisplayAlt => {
            // Payload starts after the 5-byte header.
            let payload = if record_len > MIN_RECORD_LEN {
                &data[MIN_RECORD_LEN..record_len]
            } else {
                &[]
            };
            parse_wtd_payload(payload)?
        }
    };

    Ok(Record5250 {
        record_type,
        opcode,
        orders,
    })
}

/// Parse the payload of a Write to Display record into a sequence of
/// data-stream items.
fn parse_wtd_payload(data: &[u8]) -> Result<Vec<DataStreamItem5250>, Tn5250Error> {
    let mut items: Vec<DataStreamItem5250> = Vec::new();
    let mut pos = 0;

    while pos < data.len() {
        let byte = data[pos];

        match byte {
            // ---------------------------------------------------------------
            // 0x01 = SOH (Start of Header)
            // ---------------------------------------------------------------
            0x01 => {
                pos += 1;
                if pos >= data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x01,
                        offset: pos - 1,
                        need: 2,
                        have: 0,
                    });
                }
                let soh_len = data[pos] as usize;
                pos += 1;
                if pos + soh_len > data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x01,
                        offset: pos - 2,
                        need: soh_len,
                        have: data.len() - pos,
                    });
                }
                let soh_data = data[pos..pos + soh_len].to_vec();
                trace!("SOH: len={}, data={:02X?}", soh_len, &soh_data);
                items.push(DataStreamItem5250::Order(Order::Soh(SohData {
                    length: soh_len as u8,
                    data: soh_data,
                })));
                pos += soh_len;
            }

            // ---------------------------------------------------------------
            // 0x02 = RA (Repeat to Address)
            // Followed by: row (1 byte), col (1 byte), character (1 byte)
            // ---------------------------------------------------------------
            0x02 => {
                if pos + 3 >= data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x02,
                        offset: pos,
                        need: 4,
                        have: data.len() - pos,
                    });
                }
                let row_byte = data[pos + 1];
                let col_byte = data[pos + 2];
                let fill_char = data[pos + 3];
                let (row, col) = decode_address(row_byte, col_byte)?;
                trace!(
                    "RA: target=({},{}), fill=0x{:02X} ('{}')",
                    row,
                    col,
                    fill_char,
                    ebcdic::ebcdic_to_unicode(fill_char, DEFAULT_CODE_PAGE)
                );
                items.push(DataStreamItem5250::Order(Order::Ra(row, col, fill_char)));
                pos += 4;
            }

            // ---------------------------------------------------------------
            // 0x03 = EA (Erase to Address)
            // Followed by: row (1 byte), col (1 byte)
            // ---------------------------------------------------------------
            0x03 => {
                if pos + 2 >= data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x03,
                        offset: pos,
                        need: 3,
                        have: data.len() - pos,
                    });
                }
                let row_byte = data[pos + 1];
                let col_byte = data[pos + 2];
                let (row, col) = decode_address(row_byte, col_byte)?;
                trace!("EA: target=({},{})", row, col);
                items.push(DataStreamItem5250::Order(Order::Ea(row, col)));
                pos += 3;
            }

            // ---------------------------------------------------------------
            // 0x04 = TD (Transparent Data)
            // Followed by: 1 byte length, then that many raw bytes.
            // ---------------------------------------------------------------
            0x04 => {
                pos += 1;
                if pos >= data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x04,
                        offset: pos - 1,
                        need: 2,
                        have: 0,
                    });
                }
                let td_len = data[pos] as usize;
                pos += 1;
                if pos + td_len > data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x04,
                        offset: pos - 2,
                        need: td_len,
                        have: data.len() - pos,
                    });
                }
                let td_bytes = data[pos..pos + td_len].to_vec();
                trace!("TD: len={}, data={:02X?}", td_len, &td_bytes);
                items.push(DataStreamItem5250::Order(Order::Td(td_bytes)));
                pos += td_len;
            }

            // ---------------------------------------------------------------
            // 0x10 = SBA (Set Buffer Address)
            // Followed by: row (1 byte), col (1 byte)
            // ---------------------------------------------------------------
            0x10 => {
                if pos + 2 >= data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x10,
                        offset: pos,
                        need: 3,
                        have: data.len() - pos,
                    });
                }
                let row_byte = data[pos + 1];
                let col_byte = data[pos + 2];
                let (row, col) = decode_address(row_byte, col_byte)?;
                trace!("SBA: ({},{})", row, col);
                items.push(DataStreamItem5250::Order(Order::Sba(row, col)));
                pos += 3;
            }

            // ---------------------------------------------------------------
            // 0x11 = WEA (Write Extended Attribute)
            // Followed by: attribute type (1 byte), attribute value (1 byte)
            // ---------------------------------------------------------------
            0x11 => {
                if pos + 2 >= data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x11,
                        offset: pos,
                        need: 3,
                        have: data.len() - pos,
                    });
                }
                let attr_type = data[pos + 1];
                let attr_value = data[pos + 2];
                trace!("WEA: type=0x{:02X}, value=0x{:02X}", attr_type, attr_value);
                items.push(DataStreamItem5250::Order(Order::Wea(ExtendedAttribute {
                    attr_type,
                    attr_value,
                })));
                pos += 3;
            }

            // ---------------------------------------------------------------
            // 0x20 = SF (Start Field)
            // Followed by: 2-byte Field Control Word
            // ---------------------------------------------------------------
            0x20 => {
                if pos + 2 >= data.len() {
                    return Err(Tn5250Error::TruncatedOrder {
                        order: 0x20,
                        offset: pos,
                        need: 3,
                        have: data.len() - pos,
                    });
                }
                let fcw = FieldControlWord::from_bytes(data[pos + 1], data[pos + 2]);
                trace!(
                    "SF: bypass={}, shift={:?}, modified={}",
                    fcw.bypass,
                    fcw.shift,
                    fcw.modified
                );
                items.push(DataStreamItem5250::Order(Order::Sf(fcw)));
                pos += 3;
            }

            // ---------------------------------------------------------------
            // 0x29 = IC (Insert Cursor)
            // No operands.
            // ---------------------------------------------------------------
            0x29 => {
                trace!("IC");
                items.push(DataStreamItem5250::Order(Order::Ic));
                pos += 1;
            }

            // ---------------------------------------------------------------
            // Anything else is a displayable EBCDIC character.
            // ---------------------------------------------------------------
            _ => {
                items.push(DataStreamItem5250::Character(byte));
                pos += 1;
            }
        }
    }

    Ok(items)
}

// ---------------------------------------------------------------------------
// Response builder helpers
// ---------------------------------------------------------------------------

/// Build a 5250 response record containing the given payload bytes.
///
/// The response record has record_type = 0x00 and a dummy opcode of 0x00.
/// The caller is responsible for filling in proper AID/cursor fields.
pub fn build_response_record(payload: &[u8]) -> Vec<u8> {
    let total_len = MIN_RECORD_LEN + payload.len();
    let mut record = Vec::with_capacity(total_len);
    record.push((total_len >> 8) as u8);
    record.push((total_len & 0xFF) as u8);
    record.push(0x00); // record type: response
    record.push(0x00); // reserved
    record.push(0x00); // opcode placeholder
    record.extend_from_slice(payload);
    record
}

/// Build an AID (Attention Identifier) byte for common 5250 keys.
///
/// Returns `None` for keys that do not have a standard AID mapping.
pub fn aid_byte_for_key(key_name: &str) -> Option<u8> {
    match key_name {
        "Enter" => Some(0xF1),
        "F1" => Some(0x31),
        "F2" => Some(0x32),
        "F3" => Some(0x33),
        "F4" => Some(0x34),
        "F5" => Some(0x35),
        "F6" => Some(0x36),
        "F7" => Some(0x37),
        "F8" => Some(0x38),
        "F9" => Some(0x39),
        "F10" => Some(0x3A),
        "F11" => Some(0x3B),
        "F12" => Some(0x3C),
        "F13" => Some(0xB1),
        "F14" => Some(0xB2),
        "F15" => Some(0xB3),
        "F16" => Some(0xB4),
        "F17" => Some(0xB5),
        "F18" => Some(0xB6),
        "F19" => Some(0xB7),
        "F20" => Some(0xB8),
        "F21" => Some(0xB9),
        "F22" => Some(0xBA),
        "F23" => Some(0xBB),
        "F24" => Some(0xBC),
        "PageUp" | "RollDown" => Some(0xF4),
        "PageDown" | "RollUp" => Some(0xF5),
        "Help" => Some(0xF3),
        "Clear" => Some(0xBD),
        "Print" => Some(0xF6),
        "Attn" | "SysReq" => Some(0xF0),
        _ => None,
    }
}
