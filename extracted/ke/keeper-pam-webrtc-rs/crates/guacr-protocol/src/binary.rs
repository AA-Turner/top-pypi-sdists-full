// Binary protocol encoder (zero-copy)

use bytes::{BufMut, Bytes, BytesMut};

/// Binary protocol opcodes (matching BINARY_PROTOCOL_SPEC.md)
#[repr(u8)]
#[derive(Debug, Clone, Copy)]
pub enum Opcode {
    // Client -> Server
    Key = 0x01,
    Mouse = 0x02,
    ClipboardSet = 0x03,
    Size = 0x04,
    Disconnect = 0x05,

    // Server -> Client
    Image = 0x10,
    ImageDelta = 0x11,
    Audio = 0x12,
    ClipboardGet = 0x13,
    Cursor = 0x14,

    // Bidirectional
    Ping = 0xF0,
    Pong = 0xF1,
    Error = 0xFF,
}

/// Image format values for encode_image / encode_cursor payloads
#[repr(u8)]
#[derive(Debug, Clone, Copy)]
pub enum ImageFormat {
    RawRgba = 0,
    Png = 1,
    Jpeg = 2,
}

/// Binary protocol flags
pub const FLAG_COMPRESSED: u8 = 0x01; // Payload is zstd compressed
pub const FLAG_ENCRYPTED: u8 = 0x02; // Payload is encrypted (if not using TLS)

/// Protocol overhead constants
pub const FRAME_PROTOCOL_OVERHEAD: usize = 17; // CONN(4) + TS(8) + LEN(4) + TERM(1)
pub const BINARY_PROTOCOL_OVERHEAD: usize = 8; // Opcode(1) + Flags(1) + Reserved(2) + PayloadLen(4)
pub const TOTAL_PROTOCOL_OVERHEAD: usize = FRAME_PROTOCOL_OVERHEAD + BINARY_PROTOCOL_OVERHEAD;

/// Maximum payload size for the multi-channel H.264 sender.
/// WebRTC max: 64KB. Overhead: 25 bytes. 60KB leaves ~1KB headroom.
pub const MAX_SAFE_PAYLOAD_SIZE: usize = 60 * 1024;

/// Binary protocol message header (8 bytes, little-endian payload_len)
#[derive(Debug)]
struct MessageHeader {
    opcode: Opcode,
    flags: u8,
    reserved: u16,
    length: u32,
}

impl MessageHeader {
    fn to_bytes(&self) -> [u8; 8] {
        let mut bytes = [0u8; 8];
        bytes[0] = self.opcode as u8;
        bytes[1] = self.flags;
        bytes[2..4].copy_from_slice(&self.reserved.to_le_bytes());
        bytes[4..8].copy_from_slice(&self.length.to_le_bytes());
        bytes
    }
}

/// Binary protocol encoder (zero-copy)
pub struct BinaryEncoder {
    scratch: BytesMut,
}

impl BinaryEncoder {
    pub fn new() -> Self {
        Self {
            scratch: BytesMut::with_capacity(64 * 1024),
        }
    }

    /// Encode an IMAGE (0x10) message — terminal protocols only (SSH, Telnet, TN3270, TN5250, database).
    /// Payload: x(2) + y(2) + width(2) + height(2) + format(1) + compression(1) + padding(2) + data
    pub fn encode_image(
        &mut self,
        x: u16,
        y: u16,
        width: u16,
        height: u16,
        format: u8,
        data: Bytes,
    ) -> Bytes {
        self.scratch.clear();
        let payload_len = 12 + data.len();
        let header = MessageHeader {
            opcode: Opcode::Image,
            flags: 0,
            reserved: 0,
            length: payload_len as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_u16_le(x);
        self.scratch.put_u16_le(y);
        self.scratch.put_u16_le(width);
        self.scratch.put_u16_le(height);
        self.scratch.put_u8(format);
        self.scratch.put_u8(0); // compression: none
        self.scratch.put_u16_le(0); // padding
        self.scratch.extend_from_slice(&data);
        self.scratch.clone().freeze()
    }

    /// Encode an IMAGE_DELTA (0x11) dirty-rectangle update — terminal protocols only.
    /// Same payload layout as IMAGE.
    pub fn encode_image_delta(
        &mut self,
        x: u16,
        y: u16,
        width: u16,
        height: u16,
        format: u8,
        data: Bytes,
    ) -> Bytes {
        self.scratch.clear();
        let payload_len = 12 + data.len();
        let header = MessageHeader {
            opcode: Opcode::ImageDelta,
            flags: 0,
            reserved: 0,
            length: payload_len as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_u16_le(x);
        self.scratch.put_u16_le(y);
        self.scratch.put_u16_le(width);
        self.scratch.put_u16_le(height);
        self.scratch.put_u8(format);
        self.scratch.put_u8(0); // compression: none
        self.scratch.put_u16_le(0); // padding
        self.scratch.extend_from_slice(&data);
        self.scratch.clone().freeze()
    }

    /// Encode a SIZE (0x04) message.
    /// Payload: width(2) + height(2) + padding(4)
    pub fn encode_size(&mut self, width: u16, height: u16) -> Bytes {
        self.scratch.clear();
        let header = MessageHeader {
            opcode: Opcode::Size,
            flags: 0,
            reserved: 0,
            length: 8,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_u16_le(width);
        self.scratch.put_u16_le(height);
        self.scratch.put_u32_le(0); // padding
        self.scratch.clone().freeze()
    }

    /// Encode a CURSOR (0x14) message.
    /// Payload: hotspot_x(2) + hotspot_y(2) + width(2) + height(2) + format(1) + compression(1) + padding(2) + data
    pub fn encode_cursor(
        &mut self,
        hotspot_x: u16,
        hotspot_y: u16,
        width: u16,
        height: u16,
        data: Bytes,
    ) -> Bytes {
        self.scratch.clear();
        let payload_len = 12 + data.len();
        let header = MessageHeader {
            opcode: Opcode::Cursor,
            flags: 0,
            reserved: 0,
            length: payload_len as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_u16_le(hotspot_x);
        self.scratch.put_u16_le(hotspot_y);
        self.scratch.put_u16_le(width);
        self.scratch.put_u16_le(height);
        self.scratch.put_u8(ImageFormat::RawRgba as u8);
        self.scratch.put_u8(0); // compression: none
        self.scratch.put_u16_le(0); // padding
        self.scratch.extend_from_slice(&data);
        self.scratch.clone().freeze()
    }

    /// Encode an AUDIO (0x12) message.
    /// Payload: format(1) + sample_rate(2) + channels(1) + data_len(4) + data
    pub fn encode_audio(
        &mut self,
        format: u8,
        sample_rate: u16,
        channels: u8,
        data: Bytes,
    ) -> Bytes {
        self.scratch.clear();
        let payload_len = 8 + data.len();
        let header = MessageHeader {
            opcode: Opcode::Audio,
            flags: 0,
            reserved: 0,
            length: payload_len as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_u8(format);
        self.scratch.put_u16_le(sample_rate);
        self.scratch.put_u8(channels);
        self.scratch.put_u32_le(data.len() as u32);
        self.scratch.extend_from_slice(&data);
        self.scratch.clone().freeze()
    }

    /// Encode a PING (0xF0) message — zero payload.
    pub fn encode_ping(&mut self) -> Bytes {
        self.scratch.clear();
        let header = MessageHeader {
            opcode: Opcode::Ping,
            flags: 0,
            reserved: 0,
            length: 0,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.clone().freeze()
    }

    /// Encode a PONG (0xF1) message — zero payload.
    pub fn encode_pong(&mut self) -> Bytes {
        self.scratch.clear();
        let header = MessageHeader {
            opcode: Opcode::Pong,
            flags: 0,
            reserved: 0,
            length: 0,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.clone().freeze()
    }
}

impl Default for BinaryEncoder {
    fn default() -> Self {
        Self::new()
    }
}
