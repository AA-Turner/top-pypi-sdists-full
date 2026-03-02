//! File-based extraction operations.
//!
//! This module handles extraction from filesystem paths, including:
//! - MIME type detection and validation
//! - Legacy format conversion (DOC, PPT)
//! - File validation and reading
//! - Extraction pipeline orchestration

#[cfg(any(feature = "otel", not(feature = "office")))]
use crate::KreuzbergError;
use crate::Result;
use crate::core::config::ExtractionConfig;
use crate::core::mime::{LEGACY_POWERPOINT_MIME_TYPE, LEGACY_WORD_MIME_TYPE};
use crate::types::ExtractionResult;
use std::path::Path;

use super::helpers::get_extractor;

/// Sanitize a file path to return only the filename.
///
/// This function extracts the filename from a path to avoid recording
/// potentially sensitive full file paths in telemetry data.
///
/// # Arguments
///
/// * `path` - The path to sanitize
///
/// # Returns
///
/// The filename as a string, or "unknown" if extraction fails
///
/// # Security
///
/// This prevents PII (personally identifiable information) from appearing in
/// traces by only recording filenames instead of full paths.
///
/// # Example
///
/// ```rust,ignore
/// let path = Path::new("/home/user/documents/secret.pdf");
/// assert_eq!(sanitize_path(path), "secret.pdf");
/// ```
#[cfg(feature = "otel")]
pub(super) fn sanitize_path(path: &Path) -> String {
    path.file_name()
        .and_then(|n| n.to_str())
        .unwrap_or("unknown")
        .to_string()
}

/// Record error information in the current OpenTelemetry span.
///
/// This function records error details in the current span when the `otel` feature is enabled.
/// It marks the span with `otel.status_code=ERROR` and adds error type and message fields.
///
/// # Arguments
///
/// * `error` - The error to record in the span
///
/// # Example
///
/// ```rust,ignore
/// let result = extract_file("doc.pdf", None, &config).await;
/// #[cfg(feature = "otel")]
/// if let Err(ref e) = result {
///     record_error(e);
/// }
/// result
/// ```
#[cfg(feature = "otel")]
pub(in crate::core::extractor) fn record_error(error: &KreuzbergError) {
    let span = tracing::Span::current();
    span.record("otel.status_code", "ERROR");
    span.record("error.type", format!("{:?}", error));
    span.record("error.message", error.to_string());
}

/// Extract content from a file.
///
/// This is the main entry point for file-based extraction. It performs the following steps:
/// 1. Check cache for existing result (if caching enabled)
/// 2. Detect or validate MIME type
/// 3. Select appropriate extractor from registry
/// 4. Extract content
/// 5. Run post-processing pipeline
/// 6. Store result in cache (if caching enabled)
///
/// # Arguments
///
/// * `path` - Path to the file to extract
/// * `mime_type` - Optional MIME type override. If None, will be auto-detected
/// * `config` - Extraction configuration
///
/// # Returns
///
/// An `ExtractionResult` containing the extracted content and metadata.
///
/// # Errors
///
/// Returns `KreuzbergError::Io` if the file doesn't exist (NotFound) or for other file I/O errors.
/// Returns `KreuzbergError::UnsupportedFormat` if MIME type is not supported.
///
/// # Example
///
/// ```rust,no_run
/// use kreuzberg::core::extractor::extract_file;
/// use kreuzberg::core::config::ExtractionConfig;
///
/// # async fn example() -> kreuzberg::Result<()> {
/// let config = ExtractionConfig::default();
/// let result = extract_file("document.pdf", None, &config).await?;
/// println!("Content: {}", result.content);
/// # Ok(())
/// # }
/// ```
#[cfg_attr(feature = "otel", tracing::instrument(
    skip(config, path),
    fields(
        extraction.filename = tracing::field::Empty,
    )
))]
pub async fn extract_file(
    path: impl AsRef<Path>,
    mime_type: Option<&str>,
    config: &ExtractionConfig,
) -> Result<ExtractionResult> {
    use crate::core::{io, mime};

    let path = path.as_ref();

    #[cfg(feature = "otel")]
    {
        let span = tracing::Span::current();
        span.record("extraction.filename", sanitize_path(path));
    }

    let result = async {
        io::validate_file_exists(path)?;

        let detected_mime = mime::detect_or_validate(Some(path), mime_type)?;

        // Native DOC/PPT extractors are registered in the plugin registry.
        // When the office feature is disabled, these MIME types are unsupported.
        #[cfg(not(feature = "office"))]
        match detected_mime.as_str() {
            LEGACY_WORD_MIME_TYPE => {
                return Err(KreuzbergError::UnsupportedFormat(
                    "Legacy Word extraction requires the `office` feature".to_string(),
                ));
            }
            LEGACY_POWERPOINT_MIME_TYPE => {
                return Err(KreuzbergError::UnsupportedFormat(
                    "Legacy PowerPoint extraction requires the `office` feature".to_string(),
                ));
            }
            _ => {}
        }

        // Suppress unused import warnings when office feature is enabled
        #[cfg(feature = "office")]
        {
            let _ = LEGACY_WORD_MIME_TYPE;
            let _ = LEGACY_POWERPOINT_MIME_TYPE;
        }

        extract_file_with_extractor(path, &detected_mime, config).await
    }
    .await;

    #[cfg(feature = "otel")]
    if let Err(ref e) = result {
        record_error(e);
    }

    result
}

pub(in crate::core::extractor) async fn extract_file_with_extractor(
    path: &Path,
    mime_type: &str,
    config: &ExtractionConfig,
) -> Result<ExtractionResult> {
    crate::extractors::ensure_initialized()?;

    let extractor = get_extractor(mime_type)?;
    let mut result = extractor.extract_file(path, mime_type, config).await?;
    result = crate::core::pipeline::run_pipeline(result, config).await?;
    Ok(result)
}

pub(in crate::core::extractor) async fn extract_bytes_with_extractor(
    content: &[u8],
    mime_type: &str,
    config: &ExtractionConfig,
) -> Result<ExtractionResult> {
    crate::extractors::ensure_initialized()?;

    let extractor = get_extractor(mime_type)?;
    let mut result = extractor.extract_bytes(content, mime_type, config).await?;
    result = crate::core::pipeline::run_pipeline(result, config).await?;
    Ok(result)
}
