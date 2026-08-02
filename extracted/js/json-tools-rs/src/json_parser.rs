use serde::Serialize;
use serde_json::Value;

#[cfg(target_pointer_width = "64")]
pub use sonic_rs::Error as JsonError;

#[cfg(target_pointer_width = "32")]
pub use simd_json::Error as JsonError;

/// Parse JSON string to serde_json::Value
#[cfg(target_pointer_width = "64")]
#[inline]
pub fn from_str(s: &str) -> Result<Value, JsonError> {
    sonic_rs::from_str(s)
}

/// Parse JSON string to serde_json::Value
/// Note: simd-json requires mutable input, so we need to clone
#[cfg(target_pointer_width = "32")]
#[inline]
pub fn from_str(s: &str) -> Result<Value, JsonError> {
    let mut bytes = s.as_bytes().to_vec();
    simd_json::serde::from_slice(&mut bytes)
}

/// Serialize any serializable type to JSON string
#[cfg(target_pointer_width = "64")]
#[inline]
pub fn to_string<T: Serialize>(value: &T) -> Result<String, JsonError> {
    sonic_rs::to_string(value)
}

/// Serialize any serializable type to JSON string
#[cfg(target_pointer_width = "32")]
#[inline]
pub fn to_string<T: Serialize>(value: &T) -> Result<String, JsonError> {
    simd_json::serde::to_string(value)
}

/// Parse JSON using sonic-rs (30-50% faster than simd-json)
///
/// sonic-rs benefits:
/// - More aggressive SIMD optimizations (AVX2/SSE4.2)
/// - No padding requirement (simpler API, less overhead)
/// - Better handling of UTF-8 validation
/// - Optimized for modern x86-64 CPUs
#[inline]
pub(crate) fn parse_json(json: &str) -> Result<Value, crate::error::JsonToolsError> {
    // Use json_parser module (sonic-rs on 64-bit, simd-json on 32-bit)
    from_str(json).map_err(crate::error::JsonToolsError::json_parse_error)
}
