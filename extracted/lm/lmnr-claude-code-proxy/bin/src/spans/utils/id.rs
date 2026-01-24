use rand::Rng;

use crate::spans::SpanError;

/// Parse trace_id from UUID format (e.g., "01234567-89ab-4def-0123-456789abcdef")
/// Returns a 16-byte array
pub fn parse_trace_id(uuid_str: &str) -> Result<Vec<u8>, SpanError> {
    // Remove hyphens from UUID
    let hex_str: String = uuid_str.chars().filter(|c| *c != '-').collect();

    // Trace ID should be exactly 32 hex characters (16 bytes)
    if hex_str.len() != 32 {
        return Err(SpanError::InvalidTraceIdLength {
            expected: 32,
            got: hex_str.len(),
        });
    }

    hex_string_to_bytes(&hex_str)
}

/// Parse span_id from UUID format (e.g., "00000000-0000-0000-8123-456789abcdef")
/// Returns an 8-byte array (last 8 bytes of the UUID)
pub fn parse_span_id(uuid_str: &str) -> Result<Vec<u8>, SpanError> {
    // Remove hyphens from UUID
    let hex_str: String = uuid_str.chars().filter(|c| *c != '-').collect();

    // Should be 32 hex characters total, we take the last 16 (8 bytes)
    if hex_str.len() < 16 {
        return Err(SpanError::InvalidSpanIdLength {
            expected: 16,
            got: hex_str.len(),
        });
    }

    // Take the last 16 hex characters (8 bytes) for span_id
    let span_hex = &hex_str[hex_str.len() - 16..];
    hex_string_to_bytes(span_hex)
}

/// Convert a hex string (without hyphens) to bytes
pub fn hex_string_to_bytes(hex_str: &str) -> Result<Vec<u8>, SpanError> {
    if hex_str.len() % 2 != 0 {
        return Err(SpanError::InvalidHexStringLength {
            length: hex_str.len(),
        });
    }

    let mut bytes = Vec::new();
    for i in (0..hex_str.len()).step_by(2) {
        let byte_str = &hex_str[i..i + 2];
        let byte = u8::from_str_radix(byte_str, 16).map_err(|e| SpanError::HexParseError {
            byte_str: byte_str.to_string(),
            error: e.to_string(),
        })?;
        bytes.push(byte);
    }

    Ok(bytes)
}

pub fn generate_span_id() -> Result<Vec<u8>, SpanError> {
    let mut rng = rand::rng();
    let span_id = format!("{:016x}", rng.random::<u64>());
    hex_string_to_bytes(&span_id)
}

pub fn bytes_to_uuid_like_string(bytes: &[u8]) -> Result<String, SpanError> {
    if bytes.len() != 8 {
        return Err(SpanError::InvalidBytesLength {
            expected: 8,
            got: bytes.len(),
        });
    }
    let span_id = format!(
        "{:016x}",
        u64::from_be_bytes(
            bytes
                .try_into()
                .map_err(|_| SpanError::InvalidBytesLength {
                    expected: 8,
                    got: bytes.len(),
                })?
        )
    );
    Ok(format!(
        "00000000-0000-0000-{}-{}",
        &span_id[0..4],
        &span_id[4..16]
    ))
}
