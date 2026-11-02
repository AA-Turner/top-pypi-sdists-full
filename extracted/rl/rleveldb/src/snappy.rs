use std::fmt;

const FRAME_MAGIC: [u8; 6] = [0x73, 0x4E, 0x61, 0x50, 0x70, 0x59];

#[derive(Debug)]
pub enum SnappyError {
    InvalidMagic,
    InvalidFrame(String),
    CrcMismatch { offset: usize },
    DecompressionError(String),
    IoError(String),
}

impl fmt::Display for SnappyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SnappyError::InvalidMagic => write!(f, "Invalid snappy framed magic"),
            SnappyError::InvalidFrame(msg) => write!(f, "Invalid frame: {}", msg),
            SnappyError::CrcMismatch { offset } => write!(f, "CRC mismatch at offset {}", offset),
            SnappyError::DecompressionError(msg) => write!(f, "Decompression error: {}", msg),
            SnappyError::IoError(msg) => write!(f, "IO error: {}", msg),
        }
    }
}

impl std::error::Error for SnappyError {}

/// Decompresses raw snappy-compressed data.
pub fn decompress(data: &[u8]) -> Result<Vec<u8>, SnappyError> {
    let mut decoder = snap::raw::Decoder::new();
    decoder
        .decompress_vec(data)
        .map_err(|e| SnappyError::DecompressionError(e.to_string()))
}

/// Computes CRC32C with the appropriate finalization for standard or mozilla mode.
///
/// Standard CRC32C finalizes with XOR 0xFFFFFFFF (what the `crc32c` crate produces).
/// Mozilla mode uses XOR 0x0, so we undo the standard finalization by XORing again.
fn compute_crc(data: &[u8], mozilla_mode: bool) -> u32 {
    let crc = crc32c::crc32c(data);
    if mozilla_mode {
        crc ^ 0xFFFFFFFF
    } else {
        crc
    }
}

/// Checks a masked CRC32C value against the computed CRC of the given data.
fn check_masked_crc(stored_crc: u32, data: &[u8], mozilla_mode: bool) -> bool {
    let crc = compute_crc(data, mozilla_mode);
    let masked = crc.rotate_right(15).wrapping_add(0xA282EAD8);
    masked == stored_crc
}

/// Reads a 4-byte frame header and returns `(frame_type, frame_length)`.
/// Returns `None` if there is no more data.
fn read_frame_header(data: &[u8], offset: usize) -> Result<Option<(u8, usize)>, SnappyError> {
    if offset >= data.len() {
        return Ok(None);
    }
    if offset + 4 > data.len() {
        return Err(SnappyError::InvalidFrame(
            "Could not read entire frame header".into(),
        ));
    }
    let frame_type = data[offset];
    let length =
        data[offset + 1] as usize | (data[offset + 2] as usize) << 8 | (data[offset + 3] as usize) << 16;
    Ok(Some((frame_type, length)))
}

/// Decompresses Snappy framed format data.
///
/// The framed format starts with a magic header (`0xFF` frame containing `sNaPpY`),
/// followed by frames each with a 4-byte header `[frame_type, length_lo, length_mid, length_hi]`.
pub fn decompress_framed(data: &[u8], mozilla_mode: bool) -> Result<Vec<u8>, SnappyError> {
    if data.len() < 10 {
        return Err(SnappyError::InvalidMagic);
    }

    // Read the stream identifier frame
    let (header_type, header_len) = read_frame_header(data, 0)?
        .ok_or(SnappyError::InvalidMagic)?;

    if header_type != 0xFF || header_len != FRAME_MAGIC.len() {
        return Err(SnappyError::InvalidMagic);
    }

    let magic_start = 4;
    let magic_end = magic_start + header_len;
    if magic_end > data.len() {
        return Err(SnappyError::InvalidMagic);
    }
    if data[magic_start..magic_end] != FRAME_MAGIC {
        return Err(SnappyError::InvalidMagic);
    }

    let mut offset = magic_end;
    let mut output = Vec::new();

    while offset < data.len() {
        let frame_offset = offset;
        let (frame_type, frame_length) = read_frame_header(data, offset)?
            .ok_or_else(|| SnappyError::InvalidFrame("Unexpected end of data".into()))?;
        offset += 4;

        if offset + frame_length > data.len() {
            return Err(SnappyError::InvalidFrame(format!(
                "Could not read all data; wanted: {}; got: {}",
                frame_length,
                data.len() - offset
            )));
        }

        let frame_data = &data[offset..offset + frame_length];
        offset += frame_length;

        match frame_type {
            0x00 => {
                // Compressed data frame
                if frame_data.len() < 4 {
                    return Err(SnappyError::InvalidFrame(
                        "Compressed frame too short for CRC".into(),
                    ));
                }
                let stored_crc = u32::from_le_bytes([
                    frame_data[0],
                    frame_data[1],
                    frame_data[2],
                    frame_data[3],
                ]);
                let decompressed = decompress(&frame_data[4..])?;
                if !check_masked_crc(stored_crc, &decompressed, mozilla_mode) {
                    return Err(SnappyError::CrcMismatch {
                        offset: frame_offset,
                    });
                }
                output.extend_from_slice(&decompressed);
            }
            0x01 => {
                // Uncompressed data frame
                if frame_data.len() < 4 {
                    return Err(SnappyError::InvalidFrame(
                        "Uncompressed frame too short for CRC".into(),
                    ));
                }
                let stored_crc = u32::from_le_bytes([
                    frame_data[0],
                    frame_data[1],
                    frame_data[2],
                    frame_data[3],
                ]);
                let payload = &frame_data[4..];
                if !check_masked_crc(stored_crc, payload, mozilla_mode) {
                    return Err(SnappyError::CrcMismatch {
                        offset: frame_offset,
                    });
                }
                output.extend_from_slice(payload);
            }
            0xFE => {
                // Padding — skip
            }
            0x02..=0x7F => {
                return Err(SnappyError::InvalidFrame(
                    "Reserved unskippable data".into(),
                ));
            }
            0x80..=0xFD => {
                // Reserved skippable — skip
            }
            0xFF => {
                // Stream identifier (additional magic headers are allowed)
            }
        }
    }

    Ok(output)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_decompress_empty_snap() {
        // Snappy-compressed empty input: varint 0 (uncompressed length = 0)
        let compressed = snap::raw::Encoder::new()
            .compress_vec(b"")
            .unwrap();
        let result = decompress(&compressed).unwrap();
        assert!(result.is_empty());
    }

    #[test]
    fn test_decompress_hello() {
        let original = b"hello world";
        let compressed = snap::raw::Encoder::new()
            .compress_vec(original)
            .unwrap();
        let result = decompress(&compressed).unwrap();
        assert_eq!(result, original);
    }

    #[test]
    fn test_crc_masking() {
        let data = b"hello";
        let crc = compute_crc(data, false);
        let masked = crc.rotate_right(15).wrapping_add(0xA282EAD8);
        assert!(check_masked_crc(masked, data, false));
        assert!(!check_masked_crc(masked.wrapping_add(1), data, false));
    }

    #[test]
    fn test_crc_mozilla_mode() {
        let data = b"test data";
        let crc_std = compute_crc(data, false);
        let crc_moz = compute_crc(data, true);
        // Mozilla mode undoes the 0xFFFFFFFF XOR
        assert_eq!(crc_moz, crc_std ^ 0xFFFFFFFF);
    }

    #[test]
    fn test_framed_invalid_magic() {
        let result = decompress_framed(b"not snappy", false);
        assert!(matches!(result, Err(SnappyError::InvalidMagic)));
    }

    #[test]
    fn test_framed_empty_stream() {
        // Stream identifier frame only, no data frames
        let mut data = Vec::new();
        // Frame header: type=0xFF, length=6
        data.push(0xFF);
        data.push(0x06);
        data.push(0x00);
        data.push(0x00);
        data.extend_from_slice(&FRAME_MAGIC);
        let result = decompress_framed(&data, false).unwrap();
        assert!(result.is_empty());
    }

    #[test]
    fn test_framed_uncompressed_frame() {
        let payload = b"hello world";
        let crc = compute_crc(payload, false);
        let masked = crc.rotate_right(15).wrapping_add(0xA282EAD8);

        let mut data = Vec::new();
        // Stream identifier frame
        data.push(0xFF);
        data.push(0x06);
        data.push(0x00);
        data.push(0x00);
        data.extend_from_slice(&FRAME_MAGIC);

        // Uncompressed data frame (type 0x01)
        let frame_len = 4 + payload.len();
        data.push(0x01);
        data.push(frame_len as u8);
        data.push((frame_len >> 8) as u8);
        data.push((frame_len >> 16) as u8);
        data.extend_from_slice(&masked.to_le_bytes());
        data.extend_from_slice(payload);

        let result = decompress_framed(&data, false).unwrap();
        assert_eq!(result, payload);
    }

    #[test]
    fn test_framed_compressed_frame() {
        let payload = b"the quick brown fox jumps over the lazy dog";
        let compressed = snap::raw::Encoder::new()
            .compress_vec(payload)
            .unwrap();
        let crc = compute_crc(payload, false);
        let masked = crc.rotate_right(15).wrapping_add(0xA282EAD8);

        let mut data = Vec::new();
        // Stream identifier frame
        data.push(0xFF);
        data.push(0x06);
        data.push(0x00);
        data.push(0x00);
        data.extend_from_slice(&FRAME_MAGIC);

        // Compressed data frame (type 0x00)
        let frame_len = 4 + compressed.len();
        data.push(0x00);
        data.push(frame_len as u8);
        data.push((frame_len >> 8) as u8);
        data.push((frame_len >> 16) as u8);
        data.extend_from_slice(&masked.to_le_bytes());
        data.extend_from_slice(&compressed);

        let result = decompress_framed(&data, false).unwrap();
        assert_eq!(result, payload);
    }

    #[test]
    fn test_framed_crc_mismatch() {
        let payload = b"test";
        let bad_crc: u32 = 0xDEADBEEF;

        let mut data = Vec::new();
        data.push(0xFF);
        data.push(0x06);
        data.push(0x00);
        data.push(0x00);
        data.extend_from_slice(&FRAME_MAGIC);

        let frame_len = 4 + payload.len();
        data.push(0x01);
        data.push(frame_len as u8);
        data.push((frame_len >> 8) as u8);
        data.push((frame_len >> 16) as u8);
        data.extend_from_slice(&bad_crc.to_le_bytes());
        data.extend_from_slice(payload);

        let result = decompress_framed(&data, false);
        assert!(matches!(result, Err(SnappyError::CrcMismatch { .. })));
    }

    #[test]
    fn test_framed_reserved_unskippable() {
        let mut data = Vec::new();
        data.push(0xFF);
        data.push(0x06);
        data.push(0x00);
        data.push(0x00);
        data.extend_from_slice(&FRAME_MAGIC);

        // Reserved unskippable frame (type 0x02)
        data.push(0x02);
        data.push(0x00);
        data.push(0x00);
        data.push(0x00);

        let result = decompress_framed(&data, false);
        assert!(matches!(result, Err(SnappyError::InvalidFrame(_))));
    }

    #[test]
    fn test_framed_padding_skipped() {
        let payload = b"data";
        let crc = compute_crc(payload, false);
        let masked = crc.rotate_right(15).wrapping_add(0xA282EAD8);

        let mut data = Vec::new();
        data.push(0xFF);
        data.push(0x06);
        data.push(0x00);
        data.push(0x00);
        data.extend_from_slice(&FRAME_MAGIC);

        // Padding frame (type 0xFE) with 2 bytes of padding content
        data.push(0xFE);
        data.push(0x02);
        data.push(0x00);
        data.push(0x00);
        data.push(0x00);
        data.push(0x00);

        // Uncompressed data frame
        let frame_len = 4 + payload.len();
        data.push(0x01);
        data.push(frame_len as u8);
        data.push((frame_len >> 8) as u8);
        data.push((frame_len >> 16) as u8);
        data.extend_from_slice(&masked.to_le_bytes());
        data.extend_from_slice(payload);

        let result = decompress_framed(&data, false).unwrap();
        assert_eq!(result, payload);
    }
}
