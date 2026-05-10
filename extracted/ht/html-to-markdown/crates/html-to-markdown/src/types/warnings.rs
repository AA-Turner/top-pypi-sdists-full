//! Processing warning types for non-fatal issues during conversion.

#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};

/// A non-fatal warning generated during HTML processing.
#[derive(Debug, Clone)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub struct ProcessingWarning {
    /// Human-readable warning message.
    pub message: String,
    /// The category of warning.
    pub kind: WarningKind,
}

/// Categories of processing warnings.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "serde", serde(rename_all = "snake_case"))]
pub enum WarningKind {
    /// An image could not be extracted (e.g. invalid data URI, unsupported format).
    ImageExtractionFailed,
    /// The input encoding was not recognized; fell back to UTF-8.
    EncodingFallback,
    /// The input was truncated due to size limits.
    TruncatedInput,
    /// The HTML was malformed but processing continued with best effort.
    MalformedHtml,
    /// Sanitization was applied to remove potentially unsafe content.
    SanitizationApplied,
    /// DOM traversal was truncated because max_depth was exceeded.
    DepthLimitExceeded,
}
