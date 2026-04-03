//! 3270 Data Stream parser.
//!
//! Parses binary data streams from the IBM 3270 host as documented in the
//! IBM 3270 Data Stream Programmer's Reference (GA23-0059). The data stream
//! consists of a write command, a Write Control Character (WCC), followed by
//! a sequence of orders and character data.
//!
//! This module handles both standard (non-SNA) and SNA command codes.

use thiserror::Error;

/// Errors that can occur while parsing a 3270 data stream.
#[derive(Debug, Error)]
pub enum Tn3270Error {
    #[error("data stream is empty")]
    EmptyDataStream,

    #[error("unknown write command: 0x{0:02X}")]
    UnknownWriteCommand(u8),

    #[error("unexpected end of data at offset {0}: expected {1} more bytes")]
    UnexpectedEnd(usize, usize),

    #[error("invalid buffer address encoding at offset {0}")]
    InvalidBufferAddress(usize),

    #[error("unknown order code 0x{0:02X} at offset {1}")]
    UnknownOrder(u8, usize),

    #[error("SFE pair count is zero at offset {0}")]
    InvalidSfeCount(usize),
}

// -- Write commands (first byte of data stream) --

/// 3270 write command types.
///
/// These appear as the first byte of a host-to-terminal data stream.
/// Both standard (non-SNA) and SNA variants are supported.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WriteCommand {
    /// Write (W) - write data to the current screen without erasing.
    /// Standard: 0x01, SNA: 0xF1
    Write,
    /// Erase/Write (EW) - erase the screen then write data.
    /// Standard: 0x05, SNA: 0xF5
    EraseWrite,
    /// Erase/Write Alternate (EWA) - erase and switch to alternate screen size.
    /// Standard: 0x0D, SNA: 0x7E
    EraseWriteAlternate,
    /// Write Structured Field (WSF) - structured field data follows.
    /// Standard: 0x11, SNA: 0xF3
    WriteStructuredField,
}

/// Standard (non-SNA) write command bytes.
pub(crate) const CMD_WRITE: u8 = 0x01;
pub(crate) const CMD_ERASE_WRITE: u8 = 0x05;
const CMD_ERASE_WRITE_ALTERNATE: u8 = 0x0D;
pub(crate) const CMD_WRITE_STRUCTURED_FIELD: u8 = 0x11;

/// SNA write command bytes.
const CMD_WRITE_SNA: u8 = 0xF1;
pub(crate) const CMD_ERASE_WRITE_SNA: u8 = 0xF5;
const CMD_ERASE_WRITE_ALTERNATE_SNA: u8 = 0x7E;
const CMD_WRITE_STRUCTURED_FIELD_SNA: u8 = 0xF3;

impl WriteCommand {
    /// Parse a write command byte (handles both standard and SNA encodings).
    pub fn from_byte(byte: u8) -> Result<Self, Tn3270Error> {
        match byte {
            CMD_WRITE | CMD_WRITE_SNA => Ok(WriteCommand::Write),
            CMD_ERASE_WRITE | CMD_ERASE_WRITE_SNA => Ok(WriteCommand::EraseWrite),
            CMD_ERASE_WRITE_ALTERNATE | CMD_ERASE_WRITE_ALTERNATE_SNA => {
                Ok(WriteCommand::EraseWriteAlternate)
            }
            CMD_WRITE_STRUCTURED_FIELD | CMD_WRITE_STRUCTURED_FIELD_SNA => {
                Ok(WriteCommand::WriteStructuredField)
            }
            _ => Err(Tn3270Error::UnknownWriteCommand(byte)),
        }
    }
}

// -- Write Control Character (WCC) --

/// Write Control Character - the second byte after a write command.
///
/// Controls terminal behavior after data is written. Bit assignments follow
/// GA23-0059 Section 4.3.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Wcc {
    /// Bit 1: Reset Modified Data Tags in all fields.
    pub reset_mdt: bool,
    /// Bit 2: Restore the keyboard (unlock it).
    pub restore_keyboard: bool,
    /// Bit 6: Sound the terminal alarm.
    pub alarm: bool,
}

impl Wcc {
    /// Parse a WCC byte.
    ///
    /// Bit numbering follows IBM convention (bit 0 = MSB = 0x80).
    /// - Bit 1 (0x40): Reset MDT
    /// - Bit 2 (0x20): Restore keyboard (type-ahead)
    /// - Bit 6 (0x02): Sound alarm
    pub fn from_byte(byte: u8) -> Self {
        Wcc {
            reset_mdt: (byte & 0x40) != 0,
            restore_keyboard: (byte & 0x20) != 0,
            alarm: (byte & 0x02) != 0,
        }
    }

    /// Encode this WCC back to a byte.
    pub fn to_byte(&self) -> u8 {
        let mut b = 0u8;
        if self.reset_mdt {
            b |= 0x40;
        }
        if self.restore_keyboard {
            b |= 0x20;
        }
        if self.alarm {
            b |= 0x02;
        }
        b
    }
}

// -- Field attributes --

/// Field display intensity / visibility.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Intensity {
    /// Normal display intensity.
    Normal,
    /// Non-display (invisible) field.
    Invisible,
    /// High-intensity (bright) display.
    Intensified,
}

/// Field attribute byte, parsed from the SF (Start Field) order.
///
/// The attribute byte layout (GA23-0059 Section 4.4.4):
/// - Bits 0-1: Reserved
/// - Bit 2: Protected (1) / Unprotected (0)
/// - Bit 3: Numeric (1) / Alphanumeric (0)
/// - Bits 4-5: Intensity/visibility
///   - 00 = Normal, non-pen-detectable
///   - 01 = Normal, pen-detectable
///   - 10 = High intensity, pen-detectable
///   - 11 = Non-display
/// - Bit 6: Reserved
/// - Bit 7: Modified Data Tag (MDT)
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FieldAttribute {
    /// Whether the field is protected (read-only).
    pub protected: bool,
    /// Whether the field is numeric-only.
    pub numeric: bool,
    /// Display intensity/visibility.
    pub intensity: Intensity,
    /// Modified Data Tag - set when field has been modified.
    pub modified: bool,
}

impl FieldAttribute {
    /// Parse a field attribute byte.
    pub fn from_byte(byte: u8) -> Self {
        let protected = (byte & 0x20) != 0;
        let numeric = (byte & 0x10) != 0;

        let intensity_bits = (byte >> 2) & 0x03;
        let intensity = match intensity_bits {
            0b00 | 0b01 => Intensity::Normal,
            0b10 => Intensity::Intensified,
            0b11 => Intensity::Invisible,
            _ => unreachable!(),
        };

        let modified = (byte & 0x01) != 0;

        FieldAttribute {
            protected,
            numeric,
            intensity,
            modified,
        }
    }

    /// Encode this field attribute back to a byte.
    pub fn to_byte(&self) -> u8 {
        let mut b = 0u8;
        if self.protected {
            b |= 0x20;
        }
        if self.numeric {
            b |= 0x10;
        }
        match self.intensity {
            Intensity::Normal => {} // bits 4-5 = 00
            Intensity::Intensified => b |= 0x08,
            Intensity::Invisible => b |= 0x0C,
        }
        if self.modified {
            b |= 0x01;
        }
        b
    }

    /// Returns true if this field can accept user input.
    pub fn is_unprotected(&self) -> bool {
        !self.protected
    }

    /// Returns true if this field is a skip field (protected + numeric).
    pub fn is_skip(&self) -> bool {
        self.protected && self.numeric
    }
}

// -- Extended attributes --

/// Extended attribute types used by SFE (Start Field Extended) and SA (Set Attribute).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ExtendedAttribute {
    /// 3270 field attribute (type 0xC0).
    FieldAttribute(FieldAttribute),
    /// Extended highlighting (type 0x41).
    Highlighting(Highlighting),
    /// Foreground color (type 0x42).
    ForegroundColor(Color3270),
    /// Background color (type 0x45).
    BackgroundColor(Color3270),
    /// Character set (type 0x43).
    CharacterSet(u8),
    /// Unknown/unsupported attribute type.
    Unknown { attr_type: u8, value: u8 },
}

/// Extended highlighting modes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Highlighting {
    /// Default (no highlighting).
    Default,
    /// Blinking.
    Blink,
    /// Reverse video.
    ReverseVideo,
    /// Underscore.
    Underscore,
    /// Intensified (same as field attribute intensified).
    Intensified,
}

impl Highlighting {
    pub(crate) fn from_byte(byte: u8) -> Self {
        match byte {
            0x00 | 0xF0 => Highlighting::Default,
            0xF1 => Highlighting::Blink,
            0xF2 => Highlighting::ReverseVideo,
            0xF4 => Highlighting::Underscore,
            0xF8 => Highlighting::Intensified,
            _ => Highlighting::Default,
        }
    }
}

/// 3270 color values used in extended color attributes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Color3270 {
    Default,
    Blue,
    Red,
    Pink,
    Green,
    Turquoise,
    Yellow,
    White,
}

impl Color3270 {
    pub(crate) fn from_byte(byte: u8) -> Self {
        match byte {
            0x00 | 0xF0 => Color3270::Default,
            0xF1 => Color3270::Blue,
            0xF2 => Color3270::Red,
            0xF3 => Color3270::Pink,
            0xF4 => Color3270::Green,
            0xF5 => Color3270::Turquoise,
            0xF6 => Color3270::Yellow,
            0xF7 => Color3270::White,
            _ => Color3270::Default,
        }
    }

    /// Convert to a byte value for encoding.
    pub fn to_byte(&self) -> u8 {
        match self {
            Color3270::Default => 0x00,
            Color3270::Blue => 0xF1,
            Color3270::Red => 0xF2,
            Color3270::Pink => 0xF3,
            Color3270::Green => 0xF4,
            Color3270::Turquoise => 0xF5,
            Color3270::Yellow => 0xF6,
            Color3270::White => 0xF7,
        }
    }
}

impl ExtendedAttribute {
    /// Parse an extended attribute type-value pair.
    pub(crate) fn from_pair(attr_type: u8, value: u8) -> Self {
        match attr_type {
            0xC0 => ExtendedAttribute::FieldAttribute(FieldAttribute::from_byte(value)),
            0x41 => ExtendedAttribute::Highlighting(Highlighting::from_byte(value)),
            0x42 => ExtendedAttribute::ForegroundColor(Color3270::from_byte(value)),
            0x45 => ExtendedAttribute::BackgroundColor(Color3270::from_byte(value)),
            0x43 => ExtendedAttribute::CharacterSet(value),
            _ => ExtendedAttribute::Unknown { attr_type, value },
        }
    }
}

// -- Orders --

/// 3270 data stream order codes.
pub(crate) const ORDER_SBA: u8 = 0x11; // Set Buffer Address
pub(crate) const ORDER_SF: u8 = 0x1D; // Start Field
pub(crate) const ORDER_SFE: u8 = 0x29; // Start Field Extended
pub(crate) const ORDER_SA: u8 = 0x28; // Set Attribute
pub(crate) const ORDER_IC: u8 = 0x13; // Insert Cursor
pub(crate) const ORDER_PT: u8 = 0x05; // Program Tab
pub(crate) const ORDER_RA: u8 = 0x3C; // Repeat to Address
pub(crate) const ORDER_EUA: u8 = 0x12; // Erase Unprotected to Address
const ORDER_MF: u8 = 0x2C; // Modify Field

/// 3270 data stream orders.
///
/// Orders are interspersed with character data in the data stream and control
/// positioning, field attributes, and other display properties.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Order {
    /// Set Buffer Address - moves the current buffer position.
    /// The u16 is the linear buffer address (row * cols + col).
    Sba(u16),
    /// Start Field - begins a new field with the given attribute.
    Sf(FieldAttribute),
    /// Start Field Extended - begins a field with extended attributes.
    Sfe(Vec<ExtendedAttribute>),
    /// Set Attribute - changes a display attribute without starting a field.
    Sa(ExtendedAttribute),
    /// Insert Cursor - sets the cursor position to the current buffer address.
    Ic,
    /// Program Tab - advance to the next unprotected field.
    Pt,
    /// Repeat to Address - fill from current position to the target address
    /// with the given EBCDIC character byte.
    Ra(u16, u8),
    /// Erase Unprotected to Address - clear unprotected fields from current
    /// position to the target address.
    Eua(u16),
    /// Modify Field - modify attributes of an existing field.
    Mf(Vec<ExtendedAttribute>),
}

// -- Buffer addressing --

/// Decode a 2-byte 3270 buffer address.
///
/// The 3270 uses two encoding schemes depending on screen size:
///
/// 12-bit encoding (for screens <= 4096 positions):
///   If bits 0-1 of byte 1 are not both 1, the address is encoded as:
///   byte1 bits 0-5 = high 6 bits, byte2 bits 0-5 = low 6 bits.
///   Each byte uses a 6-bit encoding where the actual address bits are
///   in positions 0-5, and the top 2 bits are set/clear per a lookup pattern.
///
/// 14-bit encoding (for larger screens):
///   If bits 6-7 of byte 1 are both set (0b11xxxxxx), the address is:
///   byte1 bits 0-5 = high 6 bits, byte2 = low 8 bits = full 14-bit address.
///
/// In practice: if (b1 & 0xC0) == 0x00, it is the 14-bit form.
/// Otherwise it is the 12-bit 6+6 form.
pub fn decode_buffer_address(b1: u8, b2: u8) -> u16 {
    if (b1 & 0xC0) == 0x00 {
        // 14-bit addressing: top 6 bits from b1, full 8 bits from b2
        ((b1 as u16 & 0x3F) << 8) | (b2 as u16)
    } else {
        // 12-bit addressing: 6 bits from each byte
        ((b1 as u16 & 0x3F) << 6) | (b2 as u16 & 0x3F)
    }
}

/// Encode a buffer address into two bytes using 12-bit encoding.
///
/// Uses the standard 6+6 bit encoding suitable for screens up to 4096
/// positions (which covers 24x80=1920 and 32x80=2560 and 43x80=3440).
///
/// Each 6-bit value is encoded with specific high bits per the 3270 address
/// translation table.
pub fn encode_buffer_address(addr: u16) -> (u8, u8) {
    let high = ((addr >> 6) & 0x3F) as u8;
    let low = (addr & 0x3F) as u8;
    (encode_address_byte(high), encode_address_byte(low))
}

/// Encode a single 6-bit value into a 3270 address byte.
///
/// The encoding table maps 6-bit values (0-63) to specific byte patterns
/// as defined in GA23-0059. The top two bits follow a specific pattern:
/// 0x00-0x0F -> 0x40+val, 0x10-0x1F -> val-0x10+0x50, etc.
///
/// The standard pattern is:
///   0-63 maps to the well-known 3270 address bytes.
fn encode_address_byte(val: u8) -> u8 {
    const ADDRESS_TABLE: [u8; 64] = [
        0x40, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, // 0-7
        0xC8, 0xC9, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, // 8-15
        0x50, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, // 16-23
        0xD8, 0xD9, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, // 24-31
        0x60, 0x61, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, // 32-39
        0xE8, 0xE9, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, // 40-47
        0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, // 48-55
        0xF8, 0xF9, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F, // 56-63
    ];
    ADDRESS_TABLE[val as usize & 0x3F]
}

/// Encode a buffer address into two bytes using 14-bit encoding.
///
/// Used for screens larger than 4096 positions. The first byte has its
/// top two bits cleared (0b00xxxxxx), and the second byte contains the
/// low 8 bits of the address.
pub fn encode_buffer_address_14bit(addr: u16) -> (u8, u8) {
    let high = ((addr >> 8) & 0x3F) as u8;
    let low = (addr & 0xFF) as u8;
    (high, low)
}

// -- Data stream items --

/// A single item in a parsed 3270 data stream (either an order or character data).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DataStreamItem {
    /// A 3270 order (SBA, SF, IC, etc.)
    Order(Order),
    /// An EBCDIC character byte to be placed at the current buffer position.
    Character(u8),
}

/// A fully parsed 3270 data stream from the host.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DataStream {
    /// The write command type.
    pub command: WriteCommand,
    /// The Write Control Character.
    pub wcc: Wcc,
    /// The sequence of orders and character data.
    pub orders: Vec<DataStreamItem>,
}

// -- AID (Attention Identifier) bytes --

/// Attention Identifier (AID) codes sent from the terminal to the host.
///
/// These identify which key the user pressed to submit data.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Aid {
    /// No AID (initial state).
    None,
    /// Enter key.
    Enter,
    /// PF1-PF24 keys.
    Pf(u8),
    /// PA1-PA3 keys (program attention, do not transmit modified fields).
    Pa(u8),
    /// Clear key.
    Clear,
    /// Short-read structured field.
    StructuredField,
}

impl Aid {
    /// The AID byte value for Enter.
    pub const ENTER: u8 = 0x7D;
    /// The AID byte value for Clear.
    pub const CLEAR: u8 = 0x6D;
    /// The AID byte value for PA1.
    pub const PA1: u8 = 0x6C;
    /// The AID byte value for PA2.
    pub const PA2: u8 = 0x6E;
    /// The AID byte value for PA3.
    pub const PA3: u8 = 0x6B;

    /// PF key AID bytes (PF1 through PF24).
    const PF_AIDS: [u8; 24] = [
        0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0x7A, 0x7B, 0x7C, // PF1-12
        0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0x4A, 0x4B, 0x4C, // PF13-24
    ];

    /// Convert an AID enum to its byte value.
    pub fn to_byte(&self) -> u8 {
        match self {
            Aid::None => 0x60,
            Aid::Enter => Self::ENTER,
            Aid::Clear => Self::CLEAR,
            Aid::Pa(1) => Self::PA1,
            Aid::Pa(2) => Self::PA2,
            Aid::Pa(3) => Self::PA3,
            Aid::Pa(_) => Self::PA1, // fallback
            Aid::Pf(n) if *n >= 1 && *n <= 24 => Self::PF_AIDS[(*n - 1) as usize],
            Aid::Pf(_) => Self::PF_AIDS[0], // fallback
            Aid::StructuredField => 0x88,
        }
    }

    /// Parse an AID byte into an Aid enum.
    pub fn from_byte(byte: u8) -> Self {
        match byte {
            0x7D => Aid::Enter,
            0x6D => Aid::Clear,
            0x6C => Aid::Pa(1),
            0x6E => Aid::Pa(2),
            0x6B => Aid::Pa(3),
            0x60 => Aid::None,
            0x88 => Aid::StructuredField,
            _ => {
                // Check PF keys
                for (i, &aid_byte) in Self::PF_AIDS.iter().enumerate() {
                    if byte == aid_byte {
                        return Aid::Pf((i + 1) as u8);
                    }
                }
                Aid::None
            }
        }
    }
}

// -- Parser --

/// Returns true if the given byte is a 3270 order code.
fn is_order(byte: u8) -> bool {
    matches!(
        byte,
        ORDER_SBA
            | ORDER_SF
            | ORDER_SFE
            | ORDER_SA
            | ORDER_IC
            | ORDER_PT
            | ORDER_RA
            | ORDER_EUA
            | ORDER_MF
    )
}

/// Parse a complete 3270 data stream from raw bytes.
///
/// The input must contain at least the command byte and WCC byte.
/// For WriteStructuredField commands, the WCC is not present and the
/// remaining data is returned as raw character bytes.
pub fn parse_data_stream(data: &[u8]) -> Result<DataStream, Tn3270Error> {
    if data.is_empty() {
        return Err(Tn3270Error::EmptyDataStream);
    }

    let command = WriteCommand::from_byte(data[0])?;

    // WSF has no WCC - the rest is structured field data
    if command == WriteCommand::WriteStructuredField {
        let orders: Vec<DataStreamItem> = data[1..]
            .iter()
            .map(|&b| DataStreamItem::Character(b))
            .collect();
        return Ok(DataStream {
            command,
            wcc: Wcc {
                reset_mdt: false,
                restore_keyboard: false,
                alarm: false,
            },
            orders,
        });
    }

    if data.len() < 2 {
        return Err(Tn3270Error::UnexpectedEnd(1, 1));
    }

    let wcc = Wcc::from_byte(data[1]);
    let mut orders = Vec::new();
    let mut pos = 2;

    while pos < data.len() {
        let byte = data[pos];

        if is_order(byte) {
            match byte {
                ORDER_SBA => {
                    // SBA: 2-byte buffer address follows
                    if pos + 2 >= data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, 2));
                    }
                    let addr = decode_buffer_address(data[pos + 1], data[pos + 2]);
                    orders.push(DataStreamItem::Order(Order::Sba(addr)));
                    pos += 3;
                }
                ORDER_SF => {
                    // SF: 1-byte attribute follows
                    if pos + 1 >= data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, 1));
                    }
                    let attr = FieldAttribute::from_byte(data[pos + 1]);
                    orders.push(DataStreamItem::Order(Order::Sf(attr)));
                    pos += 2;
                }
                ORDER_SFE => {
                    // SFE: count byte, then count * (type, value) pairs
                    if pos + 1 >= data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, 1));
                    }
                    let count = data[pos + 1] as usize;
                    if count == 0 {
                        return Err(Tn3270Error::InvalidSfeCount(pos));
                    }
                    let pairs_len = count * 2;
                    if pos + 2 + pairs_len > data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, pairs_len + 2));
                    }
                    let mut attrs = Vec::with_capacity(count);
                    for i in 0..count {
                        let attr_type = data[pos + 2 + i * 2];
                        let attr_value = data[pos + 2 + i * 2 + 1];
                        attrs.push(ExtendedAttribute::from_pair(attr_type, attr_value));
                    }
                    orders.push(DataStreamItem::Order(Order::Sfe(attrs)));
                    pos += 2 + pairs_len;
                }
                ORDER_SA => {
                    // SA: 2 bytes (type, value)
                    if pos + 2 >= data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, 2));
                    }
                    let attr = ExtendedAttribute::from_pair(data[pos + 1], data[pos + 2]);
                    orders.push(DataStreamItem::Order(Order::Sa(attr)));
                    pos += 3;
                }
                ORDER_IC => {
                    // IC: no operands
                    orders.push(DataStreamItem::Order(Order::Ic));
                    pos += 1;
                }
                ORDER_PT => {
                    // PT: no operands
                    orders.push(DataStreamItem::Order(Order::Pt));
                    pos += 1;
                }
                ORDER_RA => {
                    // RA: 2-byte address + 1-byte character
                    if pos + 3 >= data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, 3));
                    }
                    let addr = decode_buffer_address(data[pos + 1], data[pos + 2]);
                    let ch = data[pos + 3];
                    orders.push(DataStreamItem::Order(Order::Ra(addr, ch)));
                    pos += 4;
                }
                ORDER_EUA => {
                    // EUA: 2-byte buffer address follows
                    if pos + 2 >= data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, 2));
                    }
                    let addr = decode_buffer_address(data[pos + 1], data[pos + 2]);
                    orders.push(DataStreamItem::Order(Order::Eua(addr)));
                    pos += 3;
                }
                ORDER_MF => {
                    // MF: count byte, then count * (type, value) pairs
                    if pos + 1 >= data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, 1));
                    }
                    let count = data[pos + 1] as usize;
                    if count == 0 {
                        return Err(Tn3270Error::InvalidSfeCount(pos));
                    }
                    let pairs_len = count * 2;
                    if pos + 2 + pairs_len > data.len() {
                        return Err(Tn3270Error::UnexpectedEnd(pos, pairs_len + 2));
                    }
                    let mut attrs = Vec::with_capacity(count);
                    for i in 0..count {
                        let attr_type = data[pos + 2 + i * 2];
                        let attr_value = data[pos + 2 + i * 2 + 1];
                        attrs.push(ExtendedAttribute::from_pair(attr_type, attr_value));
                    }
                    orders.push(DataStreamItem::Order(Order::Mf(attrs)));
                    pos += 2 + pairs_len;
                }
                _ => {
                    return Err(Tn3270Error::UnknownOrder(byte, pos));
                }
            }
        } else {
            // Character data - EBCDIC byte to be written at current position
            orders.push(DataStreamItem::Character(byte));
            pos += 1;
        }
    }

    Ok(DataStream {
        command,
        wcc,
        orders,
    })
}
