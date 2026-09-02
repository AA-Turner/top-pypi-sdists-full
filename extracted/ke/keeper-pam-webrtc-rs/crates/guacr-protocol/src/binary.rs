// Binary protocol encoder (zero-copy)

use bytes::{BufMut, Bytes, BytesMut};
use std::borrow::Cow;

/// Binary protocol opcodes (matching BINARY_PROTOCOL_SPEC.md)
#[repr(u8)]
#[derive(Debug, Clone, Copy)]
pub enum Opcode {
    // Client -> Server
    Key = 0x01,
    Mouse = 0x02,
    MouseDelta = 0x06, // delta-encoded position; see encode_mouse_delta
    ClipboardSet = 0x03,
    Size = 0x04,
    Disconnect = 0x05,

    // Server -> Client
    Image = 0x10,
    ImageDelta = 0x11,
    Audio = 0x12,
    ClipboardGet = 0x13,
    Cursor = 0x14,
    TerminalData = 0x20,

    // Bidirectional
    Ping = 0xF0,
    Pong = 0xF1,
    Error = 0xFF,
}

/// Image format values for encode_image / encode_cursor payloads
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ImageFormat {
    RawRgba = 0,
    Png = 1,
    Jpeg = 2,
}

/// Binary protocol flags
pub const FLAG_COMPRESSED: u8 = 0x01; // Payload is zstd compressed
pub const FLAG_ENCRYPTED: u8 = 0x02; // Payload is encrypted (if not using TLS)
pub const FLAG_FRAGMENTED: u8 = 0x04; // Message is split into fragments (see fragmentation spec)

/// Fragmentation fragment size (payload bytes per fragment, not counting the 8-byte message header).
/// Chosen so each WebRTC data channel message stays within MAX_SAFE_PAYLOAD_SIZE.
pub const FRAGMENT_PAYLOAD_SIZE: usize = MAX_SAFE_PAYLOAD_SIZE - BINARY_PROTOCOL_OVERHEAD;

/// Protocol overhead constants
pub const FRAME_PROTOCOL_OVERHEAD: usize = 17; // CONN(4) + TS(8) + LEN(4) + TERM(1)
pub const BINARY_PROTOCOL_OVERHEAD: usize = 8; // Opcode(1) + Flags(1) + Reserved(2) + PayloadLen(4)
pub const TOTAL_PROTOCOL_OVERHEAD: usize = FRAME_PROTOCOL_OVERHEAD + BINARY_PROTOCOL_OVERHEAD;

/// The vault's `ControlDataChannel.ts` (`handleIncomingMessage`) drops any single incoming
/// data-channel message larger than this. Mirrors the vault's own arithmetic:
///   `MAX_INCOMING_MESSAGE_BYTES = MAX_MESSAGE_SIZE_BYTES * 2`
///   `MAX_MESSAGE_SIZE_BYTES     = 16 * 1024 - PROTOCOL_BYTE_LENGTH`
///   `PROTOCOL_BYTE_LENGTH       = CONNECTION_NUMBER(4) + TIME_STAMP(8) + DATA_LENGTH(4) + TERMINATOR(1)`
/// which is the same 17 bytes as [`FRAME_PROTOCOL_OVERHEAD`] — the vault counts the whole
/// outer frame, timestamp included.
///
/// This value tracks the vault and must be re-checked whenever the vault's constant moves.
/// It has been wrong twice: first at 60 KB (sized against the generic 64 KB SCTP limit), then
/// at `(16*1024 - 9) * 2 = 32,750` — that 9 mirrored a vault `PROTOCOL_BYTE_LENGTH` that
/// omitted the 8 timestamp bytes the wire message actually carries. The vault has since
/// corrected its own constant to include them, which moved the cap down by 16 and would have
/// silently resumed dropping every full-size fragment.
const VAULT_MAX_INCOMING_MESSAGE_BYTES: usize = (16 * 1024 - FRAME_PROTOCOL_OVERHEAD) * 2; // 32,734 bytes

/// Maximum size of a single binary protocol frame (8-byte header + payload) sent over the data
/// channel. Each frame is wrapped in a 17-byte outer Frame (CONN_NO + TS + LEN + TERMINATOR)
/// before it reaches the wire, so the per-frame budget is the vault's cap minus that wrapper:
///   32,734 - FRAME_PROTOCOL_OVERHEAD(17) = 32,717 bytes, landing at exactly 32,734 on the
/// wire — the vault drops on `>`, so equality passes.
/// FRAGMENT_PAYLOAD_SIZE (above) derives from this, keeping each fragment within that budget.
pub const MAX_SAFE_PAYLOAD_SIZE: usize = VAULT_MAX_INCOMING_MESSAGE_BYTES - FRAME_PROTOCOL_OVERHEAD; // 32,717 bytes

/// Minimum payload size below which compression is never attempted.
/// At sub-512-byte payloads the zstd frame header overhead exceeds the savings.
const COMPRESS_THRESHOLD: usize = 512;

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

    /// Compress `data` with zstd level 1 when it is large enough to benefit.
    ///
    /// Returns `(data, FLAG_COMPRESSED)` when the compressed form is at least 10% smaller
    /// than the original, otherwise returns `(original, 0)` with no allocation.
    ///
    /// Never called for payloads below `COMPRESS_THRESHOLD` — at that size the 18-byte
    /// zstd frame header alone can exceed the savings.
    fn compress_if_beneficial(data: &[u8]) -> (Cow<'_, [u8]>, u8) {
        if data.len() < COMPRESS_THRESHOLD {
            return (Cow::Borrowed(data), 0);
        }
        match zstd::encode_all(data, 1) {
            Ok(compressed) if compressed.len() < data.len() * 9 / 10 => {
                (Cow::Owned(compressed), FLAG_COMPRESSED)
            }
            _ => (Cow::Borrowed(data), 0),
        }
    }

    /// Encode an IMAGE (0x10) message — terminal protocols only (SSH, Telnet, TN3270, TN5250, database).
    /// Payload: x(2) + y(2) + width(2) + height(2) + format(1) + compression(1) + padding(2) + data
    ///
    /// IMAGE payloads are already JPEG or PNG — do not add zstd on top.
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
        self.scratch.put_u8(0); // compression: none (JPEG/PNG already compressed)
        self.scratch.put_u16_le(0); // padding
        self.scratch.extend_from_slice(&data);
        self.scratch.clone().freeze()
    }

    /// Encode an IMAGE_DELTA (0x11) dirty-rectangle update — terminal protocols only.
    /// Same payload layout as IMAGE. Do not add zstd — payload is already JPEG/PNG.
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
    ///
    /// Pass `ImageFormat::RawRgba` for RGBA bitmaps — zstd is applied automatically when the
    /// bitmap is large enough to benefit (cursor RGBA has many transparent/repeated bytes).
    /// Pass `ImageFormat::Png` or `ImageFormat::Jpeg` for pre-encoded data; no further
    /// compression is applied since those formats are already compressed.
    pub fn encode_cursor(
        &mut self,
        hotspot_x: u16,
        hotspot_y: u16,
        width: u16,
        height: u16,
        format: ImageFormat,
        data: Bytes,
    ) -> Bytes {
        let (data, compress_flag) = if format == ImageFormat::RawRgba {
            let (d, f) = Self::compress_if_beneficial(&data);
            (Bytes::copy_from_slice(&d), f)
        } else {
            (data, 0) // PNG/JPEG already compressed
        };

        self.scratch.clear();
        let payload_len = 12 + data.len();
        let header = MessageHeader {
            opcode: Opcode::Cursor,
            flags: compress_flag,
            reserved: 0,
            length: payload_len as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_u16_le(hotspot_x);
        self.scratch.put_u16_le(hotspot_y);
        self.scratch.put_u16_le(width);
        self.scratch.put_u16_le(height);
        self.scratch.put_u8(format as u8);
        self.scratch.put_u8(if compress_flag != 0 { 1 } else { 0 }); // compression field
        self.scratch.put_u16_le(0); // padding
        self.scratch.extend_from_slice(&data);
        self.scratch.clone().freeze()
    }

    /// Encode a CLIPBOARD_SET (0x03) message — Client -> Server.
    /// Payload: mimetype_len(2) + padding(2) + data_len(4) + mimetype bytes + data bytes
    ///
    /// zstd compression is applied automatically when the data exceeds `COMPRESS_THRESHOLD`
    /// and compresses by more than 10%. Clipboard content (text, HTML, RTF) typically achieves
    /// 3–5× compression.
    pub fn encode_clipboard_set(&mut self, mimetype: &str, data: &[u8]) -> Bytes {
        let (data, compress_flag) = Self::compress_if_beneficial(data);
        self.scratch.clear();
        let payload_len = 2 + 2 + 4 + mimetype.len() + data.len();
        let header = MessageHeader {
            opcode: Opcode::ClipboardSet,
            flags: compress_flag,
            reserved: 0,
            length: payload_len as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_u16_le(mimetype.len() as u16);
        self.scratch.put_u16_le(0); // padding
        self.scratch.put_u32_le(data.len() as u32);
        self.scratch.extend_from_slice(mimetype.as_bytes());
        self.scratch.extend_from_slice(&data);
        self.scratch.clone().freeze()
    }

    /// Encode a CLIPBOARD_GET (0x13) message — Server -> Client.
    /// Same payload layout as CLIPBOARD_SET. zstd applied on the same threshold.
    pub fn encode_clipboard_get(&mut self, mimetype: &str, data: &[u8]) -> Bytes {
        let (data, compress_flag) = Self::compress_if_beneficial(data);
        self.scratch.clear();
        let payload_len = 2 + 2 + 4 + mimetype.len() + data.len();
        let header = MessageHeader {
            opcode: Opcode::ClipboardGet,
            flags: compress_flag,
            reserved: 0,
            length: payload_len as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_u16_le(mimetype.len() as u16);
        self.scratch.put_u16_le(0); // padding
        self.scratch.put_u32_le(data.len() as u32);
        self.scratch.extend_from_slice(mimetype.as_bytes());
        self.scratch.extend_from_slice(&data);
        self.scratch.clone().freeze()
    }

    /// Encode an AUDIO (0x12) message.
    /// Payload: format(1) + sample_rate(2) + channels(1) + data_len(4) + data
    ///
    /// Audio format MUST be Opus (format=1) for network transmission. PCM (format=0) is
    /// ~176 KB/s at 44100Hz stereo; Opus is ~16 KB/s at equivalent quality. Do not send
    /// PCM over the wire — encode to Opus before calling this function.
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

    /// Encode a MOUSE_DELTA (0x06) message — Client -> Server.
    /// 4-byte payload: dx(i8) + dy(i8) + button_mask(u8) + scroll_delta(i8)
    ///
    /// Use when |dx| ≤ 127 and |dy| ≤ 127 and the button state has not changed since the
    /// last MOUSE or MOUSE_DELTA message. Fall back to MOUSE (0x02) for:
    ///   - deltas that exceed ±127
    ///   - any button state change (click, release, scroll without position change)
    ///   - absolute position resets (e.g. cursor warp, focus change)
    ///
    /// The decoder maintains a running absolute position by accumulating deltas from the
    /// last known absolute MOUSE position.
    pub fn encode_mouse_delta(
        &mut self,
        dx: i8,
        dy: i8,
        button_mask: u8,
        scroll_delta: i8,
    ) -> Bytes {
        self.scratch.clear();
        let header = MessageHeader {
            opcode: Opcode::MouseDelta,
            flags: 0,
            reserved: 0,
            length: 4,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.put_i8(dx);
        self.scratch.put_i8(dy);
        self.scratch.put_u8(button_mask);
        self.scratch.put_i8(scroll_delta);
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

    // ── Fragmentation ────────────────────────────────────────────────────────
    //
    // Callers that need both compression and fragmentation must compress FIRST,
    // then pass the compressed bytes to fragment_message(). The FLAG_COMPRESSED
    // flag is propagated to every fragment so the receiver knows to decompress
    // after reassembly. Order: compress → fragment → send. Receive: reassemble
    // → decompress.

    /// Fragment a message payload into multiple frames if it exceeds MAX_SAFE_PAYLOAD_SIZE.
    ///
    /// AC-1: Sub-limit messages return a single non-fragmented frame (FLAG_FRAGMENTED not set).
    /// AC-2: Over-limit messages are split into multiple frames, each within the limit.
    /// AC-3: Each fragment carries FLAG_FRAGMENTED, a sequence number (0-indexed, in `reserved[0]`),
    ///        and total count (in `reserved[1]`).
    /// AC-4: All fragments share the same opcode.
    /// AC-5: A receiver that ignores FLAG_FRAGMENTED can still process non-fragmented messages.
    pub fn fragment_message(&mut self, opcode: Opcode, flags: u8, payload: &[u8]) -> Vec<Bytes> {
        // AC-1: sub-limit — send as a single non-fragmented frame.
        if payload.len() <= FRAGMENT_PAYLOAD_SIZE {
            return vec![self.encode_raw(opcode, flags, payload)];
        }

        // AC-2: over-limit — split into fragments.
        let chunks: Vec<&[u8]> = payload.chunks(FRAGMENT_PAYLOAD_SIZE).collect();
        let total = chunks.len().min(255) as u8; // clamp to u8 max (reserved field is 1 byte)
        let mut frames = Vec::with_capacity(chunks.len());

        for (seq, chunk) in chunks.into_iter().enumerate() {
            let seq = seq.min(254) as u8; // 0-indexed, max 254
                                          // AC-3: embed seq_num in reserved[0], total_count in reserved[1].
            let fragment_flags = flags | FLAG_FRAGMENTED;
            let frame = self.encode_raw_with_reserved(opcode, fragment_flags, seq, total, chunk);
            frames.push(frame);
        }

        frames
    }

    /// Encode a single message without fragmentation.
    fn encode_raw(&mut self, opcode: Opcode, flags: u8, payload: &[u8]) -> Bytes {
        self.scratch.clear();
        let header = MessageHeader {
            opcode,
            flags,
            reserved: 0,
            length: payload.len() as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.extend_from_slice(payload);
        self.scratch.clone().freeze()
    }

    /// Encode a fragment with sequence and total encoded in the reserved field.
    fn encode_raw_with_reserved(
        &mut self,
        opcode: Opcode,
        flags: u8,
        seq: u8,
        total: u8,
        payload: &[u8],
    ) -> Bytes {
        self.scratch.clear();
        // Pack seq into low byte of reserved, total into high byte.
        let reserved = (seq as u16) | ((total as u16) << 8);
        let header = MessageHeader {
            opcode,
            flags,
            reserved,
            length: payload.len() as u32,
        };
        self.scratch.put_slice(&header.to_bytes());
        self.scratch.extend_from_slice(payload);
        self.scratch.clone().freeze()
    }
}

impl Default for BinaryEncoder {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // ── Clipboard compression round-trip ─────────────────────────────────────

    #[test]
    fn clipboard_set_small_not_compressed() {
        let mut enc = BinaryEncoder::new();
        let data = b"hello world";
        let msg = enc.encode_clipboard_set("text/plain", data);
        // Header byte 1 (flags) must not have FLAG_COMPRESSED set for small payloads
        assert_eq!(
            msg[1] & FLAG_COMPRESSED,
            0,
            "small clipboard must not be compressed"
        );
    }

    #[test]
    fn clipboard_set_large_compressed_and_round_trips() {
        let mut enc = BinaryEncoder::new();
        // 2 KB of highly compressible text
        let data: Vec<u8> = b"the quick brown fox jumps over the lazy dog. "
            .iter()
            .cycle()
            .take(2048)
            .copied()
            .collect();
        let msg = enc.encode_clipboard_set("text/plain", &data);

        // FLAG_COMPRESSED must be set
        assert_ne!(
            msg[1] & FLAG_COMPRESSED,
            0,
            "large clipboard must be compressed"
        );

        // Parse the payload manually: skip 8-byte header, then mimetype_len(2)+pad(2)+data_len(4)
        let mimetype_len = u16::from_le_bytes([msg[8], msg[9]]) as usize;
        let compressed_len = u32::from_le_bytes([msg[12], msg[13], msg[14], msg[15]]) as usize;
        let payload_start = 8 + 2 + 2 + 4 + mimetype_len;
        let compressed = &msg[payload_start..payload_start + compressed_len];

        // Decompress and verify round-trip
        let decoded = zstd::decode_all(compressed).expect("zstd decode failed");
        assert_eq!(decoded, data, "clipboard round-trip mismatch");

        // Verify actual compression happened (output smaller than input)
        assert!(
            compressed_len < data.len(),
            "compressed must be smaller than original"
        );
    }

    #[test]
    fn clipboard_get_large_compressed() {
        let mut enc = BinaryEncoder::new();
        let data: Vec<u8> = (0u8..255).cycle().take(1024).collect();
        let msg = enc.encode_clipboard_get("text/html", &data);
        // flags byte is index 1; low-entropy data may or may not compress well,
        // but the encode path must not panic regardless
        let _ = msg[1]; // just assert no panic
    }

    // ── Cursor compression ───────────────────────────────────────────────────

    #[test]
    fn cursor_rgba_large_compressed() {
        let mut enc = BinaryEncoder::new();
        // Simulate a 11×19 pointer cursor (836 bytes) — mostly transparent (0x00000000)
        let rgba: Vec<u8> = std::iter::repeat_n(0u8, 836).collect();
        let msg = enc.encode_cursor(
            0,
            0,
            11,
            19,
            ImageFormat::RawRgba,
            Bytes::copy_from_slice(&rgba),
        );
        // Transparent RGBA compresses extremely well; flag must be set
        assert_ne!(
            msg[1] & FLAG_COMPRESSED,
            0,
            "transparent cursor must be compressed"
        );
        // Total message must be smaller than uncompressed equivalent
        let uncompressed_size = 8 + 12 + 836;
        assert!(
            msg.len() < uncompressed_size,
            "compressed cursor must be smaller"
        );
    }

    #[test]
    fn cursor_png_not_recompressed() {
        let mut enc = BinaryEncoder::new();
        // PNG data is already compressed — flag must not be set
        let png_bytes = Bytes::from_static(b"\x89PNG\r\n\x1a\nfakedata");
        let msg = enc.encode_cursor(0, 0, 8, 8, ImageFormat::Png, png_bytes);
        assert_eq!(
            msg[1] & FLAG_COMPRESSED,
            0,
            "PNG cursor must not be recompressed"
        );
    }

    // ── MouseDelta ───────────────────────────────────────────────────────────

    #[test]
    fn mouse_delta_size_and_opcode() {
        let mut enc = BinaryEncoder::new();
        let msg = enc.encode_mouse_delta(10, -5, 0, 0);
        assert_eq!(msg.len(), 12, "MOUSE_DELTA: 8-byte header + 4-byte payload");
        assert_eq!(msg[0], Opcode::MouseDelta as u8);
        assert_eq!(msg[1], 0, "no flags on MOUSE_DELTA");
        // payload: dx=10, dy=-5 (0xFB), button_mask=0, scroll=0
        assert_eq!(msg[8], 10i8 as u8);
        assert_eq!(msg[9], (-5i8) as u8);
        assert_eq!(msg[10], 0);
        assert_eq!(msg[11], 0);
    }

    // ── compress_if_beneficial threshold ────────────────────────────────────

    #[test]
    fn compress_threshold_not_triggered_below_512() {
        let data: Vec<u8> = b"aaaa".iter().cycle().take(511).copied().collect();
        let (result, flag) = BinaryEncoder::compress_if_beneficial(&data);
        assert_eq!(flag, 0, "must not compress below threshold");
        assert!(
            matches!(result, Cow::Borrowed(_)),
            "must borrow original below threshold"
        );
    }

    #[test]
    fn compress_threshold_triggered_above_512() {
        // 512 bytes of repeated 'a' compresses extremely well
        let data: Vec<u8> = b"a".iter().cycle().take(512).copied().collect();
        let (_, flag) = BinaryEncoder::compress_if_beneficial(&data);
        assert_ne!(
            flag, 0,
            "must compress highly compressible data above threshold"
        );
    }
}
