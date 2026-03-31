//! Error mapping patterns for language bindings.
//!
//! Provides a trait for mapping `ConversionError` from the core library
//! to language-specific error types.

use html_to_markdown_rs::ConversionError;

/// Helper function to categorize conversion errors.
///
/// Returns `true` if the error is a panic/runtime error that should
/// be treated differently from validation errors.
#[must_use]
pub fn is_panic_error(err: &ConversionError) -> bool {
    matches!(err, ConversionError::Panic(_))
}

/// Extract error message from `ConversionError`.
#[must_use]
pub fn error_message(err: &ConversionError) -> String {
    match err {
        ConversionError::Panic(msg) => format!("html-to-markdown panic during conversion: {msg}"),
        other => other.to_string(),
    }
}
