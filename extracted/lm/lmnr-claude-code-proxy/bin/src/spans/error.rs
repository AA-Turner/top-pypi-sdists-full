use std::fmt;

#[derive(Debug)]
pub enum SpanError {
    MessageStartEventNotFound,
    InvalidTraceIdLength { expected: usize, got: usize },
    InvalidSpanIdLength { expected: usize, got: usize },
    InvalidHexStringLength { length: usize },
    HexParseError { byte_str: String, error: String },
    AttributeConversionError { value: String },
    InvalidBytesLength { expected: usize, got: usize },
}

impl fmt::Display for SpanError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SpanError::MessageStartEventNotFound => {
                write!(f, "MessageStart event not found in stream")
            }
            SpanError::InvalidTraceIdLength { expected, got } => {
                write!(
                    f,
                    "Invalid trace_id length: expected {} hex chars, got {}",
                    expected, got
                )
            }
            SpanError::InvalidSpanIdLength { expected, got } => {
                write!(
                    f,
                    "Invalid span_id length: expected at least {} hex chars, got {}",
                    expected, got
                )
            }
            SpanError::InvalidHexStringLength { length } => {
                write!(f, "Invalid hex string length: {}", length)
            }
            SpanError::HexParseError { byte_str, error } => {
                write!(f, "Failed to parse hex byte '{}': {}", byte_str, error)
            }
            SpanError::AttributeConversionError { value } => {
                write!(f, "Failed to convert JSON value to AnyValue: {}", value)
            }
            SpanError::InvalidBytesLength { expected, got } => {
                write!(
                    f,
                    "Invalid bytes length: expected {}, got {}",
                    expected, got
                )
            }
        }
    }
}

impl std::error::Error for SpanError {}
