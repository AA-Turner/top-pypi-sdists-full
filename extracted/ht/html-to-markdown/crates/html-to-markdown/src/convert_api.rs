//! Main HTML to Markdown conversion APIs.
//!
//! This module provides the primary public functions for converting HTML to Markdown,
//! including support for metadata extraction, inline image collection, and custom visitors.

use std::borrow::Cow;

use crate::error::Result;
use crate::options::{ConversionOptions, WhitespaceMode};
use crate::text;
use crate::validation::{Utf16Encoding, detect_utf16_encoding, validate_input};
use crate::{ConversionError, ConversionOptionsUpdate};

#[cfg(feature = "visitor")]
use crate::visitor;
#[cfg(feature = "async-visitor")]
use crate::visitor_helpers;
#[cfg(feature = "metadata")]
use crate::{ExtendedMetadata, MetadataConfig};
#[cfg(feature = "inline-images")]
use crate::{HtmlExtraction, InlineImageConfig};

/// Convert HTML to Markdown.
///
/// # Arguments
///
/// * `html` - The HTML string to convert
/// * `options` - Optional conversion options (defaults to `ConversionOptions::default()`)
///
/// # Example
///
/// ```
/// use html_to_markdown_rs::{convert, ConversionOptions};
///
/// let html = "<h1>Hello World</h1>";
/// let markdown = convert(html, None).unwrap();
/// assert!(markdown.contains("Hello World"));
/// ```
/// # Errors
///
/// Returns an error if HTML parsing fails or if the input contains invalid UTF-8.
pub fn convert(html: &str, options: Option<ConversionOptions>) -> Result<String> {
    let options = options.unwrap_or_default();

    let normalized_html = normalize_input(html)?;

    if !options.wrap {
        if let Some(markdown) = fast_text_only(normalized_html.as_ref(), &options) {
            return Ok(markdown);
        }
    }

    let markdown = crate::converter::convert_html(normalized_html.as_ref(), &options)?;

    if options.wrap {
        Ok(crate::wrapper::wrap_markdown(&markdown, &options))
    } else {
        Ok(markdown)
    }
}

/// Convert HTML to Markdown while collecting inline image assets (requires the `inline-images` feature).
///
/// Extracts inline image data URIs and inline `<svg>` elements alongside Markdown conversion.
///
/// # Arguments
///
/// * `html` - The HTML string to convert
/// * `options` - Optional conversion options (defaults to `ConversionOptions::default()`)
/// * `image_cfg` - Configuration controlling inline image extraction
/// * `visitor` - Optional visitor for customizing conversion behavior. Only used if `visitor` feature is enabled.
/// # Errors
///
/// Returns an error if HTML parsing fails or if the input contains invalid UTF-8.
#[cfg(feature = "inline-images")]
pub fn convert_with_inline_images(
    html: &str,
    options: Option<ConversionOptions>,
    image_cfg: InlineImageConfig,
    #[cfg(feature = "visitor")] visitor: Option<visitor::VisitorHandle>,
    #[cfg(not(feature = "visitor"))] _visitor: Option<()>,
) -> Result<HtmlExtraction> {
    use std::cell::RefCell;
    use std::rc::Rc;

    let options = options.unwrap_or_default();

    let normalized_html = normalize_input(html)?;

    let collector = Rc::new(RefCell::new(crate::inline_images::InlineImageCollector::new(
        image_cfg,
    )?));

    #[cfg(feature = "visitor")]
    let markdown = crate::converter::convert_html_impl(
        normalized_html.as_ref(),
        &options,
        Some(Rc::clone(&collector)),
        None,
        visitor,
    )?;
    #[cfg(not(feature = "visitor"))]
    let markdown = crate::converter::convert_html_impl(
        normalized_html.as_ref(),
        &options,
        Some(Rc::clone(&collector)),
        None,
        None,
    )?;

    let markdown = if options.wrap {
        crate::wrapper::wrap_markdown(&markdown, &options)
    } else {
        markdown
    };

    let collector = Rc::try_unwrap(collector)
        .map_err(|_| ConversionError::Other("failed to recover inline image state".to_string()))?
        .into_inner();
    let (inline_images, warnings) = collector.finish();

    Ok(HtmlExtraction {
        markdown,
        inline_images,
        warnings,
    })
}

/// Convert HTML to Markdown with comprehensive metadata extraction (requires the `metadata` feature).
///
/// Performs HTML-to-Markdown conversion while simultaneously extracting structured metadata in a
/// single pass for maximum efficiency. Ideal for content analysis, SEO optimization, and document
/// indexing workflows.
///
/// # Arguments
///
/// * `html` - The HTML string to convert. Will normalize line endings (CRLF → LF).
/// * `options` - Optional conversion configuration. Defaults to `ConversionOptions::default()` if `None`.
///   Controls heading style, list indentation, escape behavior, wrapping, and other output formatting.
/// * `metadata_cfg` - Configuration for metadata extraction granularity. Use `MetadataConfig::default()`
///   to extract all metadata types, or customize with selective extraction flags.
/// * `visitor` - Optional visitor for customizing conversion behavior. Only used if `visitor` feature is enabled.
///
/// # Returns
///
/// On success, returns a tuple of:
/// - `String`: The converted Markdown output
/// - `ExtendedMetadata`: Comprehensive metadata containing:
///   - `document`: Title, description, author, language, Open Graph, Twitter Card, and other meta tags
///   - `headers`: All heading elements (h1-h6) with hierarchy and IDs
///   - `links`: Hyperlinks classified as anchor, internal, external, email, or phone
///   - `images`: Image elements with source, dimensions, and alt text
///   - `structured_data`: JSON-LD, Microdata, and `RDFa` blocks
///
/// # Errors
///
/// Returns `ConversionError` if:
/// - HTML parsing fails
/// - Invalid UTF-8 sequences encountered
/// - Internal panic during conversion (wrapped in `ConversionError::Panic`)
/// - Configuration size limits exceeded
///
/// # Performance Notes
///
/// - Single-pass collection: metadata extraction has minimal overhead
/// - Zero cost when metadata feature is disabled
/// - Pre-allocated buffers: typically handles 50+ headers, 100+ links, 20+ images efficiently
/// - Structured data size-limited to prevent memory exhaustion (configurable)
///
/// # Example: Basic Usage
///
/// ```ignore
/// use html_to_markdown_rs::{convert_with_metadata, MetadataConfig};
///
/// let html = r#"
///   <html lang="en">
///     <head><title>My Article</title></head>
///     <body>
///       <h1 id="intro">Introduction</h1>
///       <p>Welcome to <a href="https://example.com">our site</a></p>
///     </body>
///   </html>
/// "#;
///
/// let (markdown, metadata) = convert_with_metadata(html, None, MetadataConfig::default(), None)?;
///
/// assert_eq!(metadata.document.title, Some("My Article".to_string()));
/// assert_eq!(metadata.document.language, Some("en".to_string()));
/// assert_eq!(metadata.headers[0].text, "Introduction");
/// assert_eq!(metadata.headers[0].id, Some("intro".to_string()));
/// assert_eq!(metadata.links.len(), 1);
/// # Ok::<(), html_to_markdown_rs::ConversionError>(())
/// ```
///
/// # Example: Selective Metadata Extraction
///
/// ```ignore
/// use html_to_markdown_rs::{convert_with_metadata, MetadataConfig};
///
/// let html = "<html><body><h1>Title</h1><a href='#anchor'>Link</a></body></html>";
///
/// // Extract only headers and document metadata, skip links/images
/// let config = MetadataConfig {
///     extract_headers: true,
///     extract_links: false,
///     extract_images: false,
///     extract_structured_data: false,
///     max_structured_data_size: 0,
/// };
///
/// let (markdown, metadata) = convert_with_metadata(html, None, config, None)?;
/// assert!(metadata.headers.len() > 0);
/// assert!(metadata.links.is_empty());  // Not extracted
/// # Ok::<(), html_to_markdown_rs::ConversionError>(())
/// ```
///
/// # Example: With Conversion Options and Metadata Config
///
/// ```ignore
/// use html_to_markdown_rs::{convert_with_metadata, ConversionOptions, MetadataConfig, HeadingStyle};
///
/// let html = "<html><head><title>Blog Post</title></head><body><h1>Hello</h1></body></html>";
///
/// let options = ConversionOptions {
///     heading_style: HeadingStyle::Atx,
///     wrap: true,
///     wrap_width: 80,
///     ..Default::default()
/// };
///
/// let metadata_cfg = MetadataConfig::default();
///
/// let (markdown, metadata) = convert_with_metadata(html, Some(options), metadata_cfg, None)?;
/// // Markdown will use ATX-style headings (# H1, ## H2, etc.)
/// // Wrapped at 80 characters
/// // All metadata extracted
/// # Ok::<(), html_to_markdown_rs::ConversionError>(())
/// ```
///
/// # See Also
///
/// - [`convert`] - Simple HTML to Markdown conversion without metadata
/// - [`convert_with_inline_images`] - Conversion with inline image extraction
/// - [`MetadataConfig`] - Configuration for metadata extraction
/// - [`ExtendedMetadata`] - Metadata structure documentation
/// - [`metadata`] module - Detailed type documentation for metadata components
#[cfg(feature = "metadata")]
pub fn convert_with_metadata(
    html: &str,
    options: Option<ConversionOptions>,
    metadata_cfg: MetadataConfig,
    #[cfg(feature = "visitor")] visitor: Option<visitor::VisitorHandle>,
    #[cfg(not(feature = "visitor"))] _visitor: Option<()>,
) -> Result<(String, ExtendedMetadata)> {
    use std::cell::RefCell;
    use std::rc::Rc;

    let options = options.unwrap_or_default();
    let normalized_html = normalize_input(html)?;
    if !metadata_cfg.any_enabled() {
        #[cfg(feature = "visitor")]
        let markdown = crate::converter::convert_html_impl(normalized_html.as_ref(), &options, None, None, visitor)?;
        #[cfg(not(feature = "visitor"))]
        let markdown = crate::converter::convert_html_impl(normalized_html.as_ref(), &options, None, None, None)?;
        let markdown = if options.wrap {
            crate::wrapper::wrap_markdown(&markdown, &options)
        } else {
            markdown
        };
        return Ok((markdown, ExtendedMetadata::default()));
    }

    let metadata_collector = Rc::new(RefCell::new(crate::metadata::MetadataCollector::new(metadata_cfg)));

    #[cfg(feature = "visitor")]
    let markdown = crate::converter::convert_html_impl(
        normalized_html.as_ref(),
        &options,
        None,
        Some(Rc::clone(&metadata_collector)),
        visitor,
    )?;
    #[cfg(not(feature = "visitor"))]
    let markdown = crate::converter::convert_html_impl(
        normalized_html.as_ref(),
        &options,
        None,
        Some(Rc::clone(&metadata_collector)),
        None,
    )?;

    let markdown = if options.wrap {
        crate::wrapper::wrap_markdown(&markdown, &options)
    } else {
        markdown
    };

    let metadata_collector = Rc::try_unwrap(metadata_collector)
        .map_err(|_| ConversionError::Other("failed to recover metadata state".to_string()))?
        .into_inner();
    let metadata = metadata_collector.finish();

    Ok((markdown, metadata))
}

/// Convert HTML to Markdown with a custom visitor callback.
///
/// This function allows you to provide a visitor implementation that can inspect,
/// modify, or replace the default conversion behavior for any HTML element type.
///
/// # Arguments
///
/// * `html` - The HTML input to convert
/// * `options` - Optional conversion options (uses defaults if None)
/// * `visitor` - Mutable reference to visitor implementation for customization
///
/// # Example
///
/// ```ignore
/// use html_to_markdown_rs::convert_with_visitor;
/// use html_to_markdown_rs::visitor::{HtmlVisitor, NodeContext, VisitResult};
///
/// #[derive(Debug)]
/// struct CustomVisitor;
///
/// impl HtmlVisitor for CustomVisitor {
///     fn visit_code_block(
///         &mut self,
///         _ctx: &NodeContext,
///         language: Option<&str>,
///         code: &str,
///     ) -> VisitResult {
///         VisitResult::Custom(format!("```{}\n{}\n```", language.unwrap_or(""), code))
///     }
/// }
///
/// let html = "<pre><code class=\"language-rust\">fn main() {}</code></pre>";
/// let mut visitor = CustomVisitor;
/// let markdown = convert_with_visitor(html, None, &mut visitor).unwrap();
/// ```
#[cfg(feature = "visitor")]
/// # Errors
///
/// Returns an error if HTML parsing fails or if the input contains invalid UTF-8.
pub fn convert_with_visitor(
    html: &str,
    options: Option<ConversionOptions>,
    visitor: Option<visitor::VisitorHandle>,
) -> Result<String> {
    let options = options.unwrap_or_default();

    let normalized_html = normalize_input(html)?;

    let markdown = crate::converter::convert_html_with_visitor(normalized_html.as_ref(), &options, visitor)?;

    if options.wrap {
        Ok(crate::wrapper::wrap_markdown(&markdown, &options))
    } else {
        Ok(markdown)
    }
}

#[cfg(feature = "async-visitor")]
/// Convert HTML to Markdown with an async visitor callback.
///
/// This async function allows you to provide an async visitor implementation that can inspect,
/// modify, or replace the default conversion behavior for any HTML element type.
///
/// This function is useful for:
/// - Python async functions (with `async def` and `asyncio`)
/// - TypeScript/JavaScript async functions (with `Promise`-based callbacks)
/// - Elixir processes (with message-passing async operations)
///
/// For synchronous languages (Ruby, PHP, Go, Java, C#), use `convert_with_visitor` instead.
///
/// # Note
///
/// The async visitor trait (`AsyncHtmlVisitor`) and async dispatch helpers are designed to be
/// consumed by language bindings (`PyO3`, NAPI-RS, Magnus, etc.) which can bridge async/await
/// semantics from their host languages. The conversion pipeline wraps async visitor calls using
/// tokio's runtime to support both multi-threaded and current_thread runtimes (like NAPI's).
///
/// Binding implementations will be responsible for running async callbacks on appropriate
/// event loops (asyncio for Python, Promise chains for TypeScript, etc.).
///
/// # Arguments
///
/// * `html` - The HTML input to convert
/// * `options` - Optional conversion options (uses defaults if None)
/// * `visitor` - Optional async visitor implementing `AsyncHtmlVisitor` trait for customization
///
/// # Example (Rust-like async)
///
/// ```ignore
/// use html_to_markdown_rs::convert_with_async_visitor;
/// use html_to_markdown_rs::visitor::{AsyncHtmlVisitor, NodeContext, VisitResult};
/// use async_trait::async_trait;
/// use std::rc::Rc;
/// use std::cell::RefCell;
///
/// #[derive(Debug)]
/// struct CustomAsyncVisitor;
///
/// #[async_trait]
/// impl AsyncHtmlVisitor for CustomAsyncVisitor {
///     async fn visit_code_block(
///         &mut self,
///         _ctx: &NodeContext,
///         language: Option<&str>,
///         code: &str,
///     ) -> VisitResult {
///         // Can perform async operations here (e.g., syntax highlighting via service)
///         VisitResult::Custom(format!("```{}\n{}\n```", language.unwrap_or(""), code))
///     }
/// }
///
/// let html = "<pre><code class=\"language-rust\">fn main() {}</code></pre>";
/// let visitor = Some(Rc::new(RefCell::new(CustomAsyncVisitor) as _));
/// let markdown = convert_with_async_visitor(html, None, visitor).await.unwrap();
/// ```
#[allow(clippy::future_not_send)]
/// # Errors
///
/// Returns an error if HTML parsing fails or if the input contains invalid UTF-8.
pub async fn convert_with_async_visitor(
    html: &str,
    options: Option<ConversionOptions>,
    visitor: Option<visitor_helpers::AsyncVisitorHandle>,
) -> Result<String> {
    let options = options.unwrap_or_default();

    let normalized_html = normalize_input(html)?;

    // Use the async implementation that properly awaits visitor callbacks
    let markdown =
        crate::converter::convert_html_with_visitor_async(normalized_html.as_ref(), &options, visitor).await?;

    if options.wrap {
        Ok(crate::wrapper::wrap_markdown(&markdown, &options))
    } else {
        Ok(markdown)
    }
}

/// Validate and normalize HTML input for conversion.
fn normalize_input(html: &str) -> Result<Cow<'_, str>> {
    let decoded = decode_utf16_if_needed(html);
    match decoded {
        Cow::Borrowed(borrowed) => {
            validate_input(borrowed)?;
            let sanitized = strip_nul_bytes(borrowed);
            match sanitized {
                Cow::Borrowed(b) => Ok(normalize_line_endings(b)),
                Cow::Owned(o) => Ok(Cow::Owned(normalize_line_endings(&o).into_owned())),
            }
        }
        Cow::Owned(mut owned) => {
            validate_input(&owned)?;
            if owned.contains('\0') {
                owned = owned.replace('\0', "");
            }
            if owned.contains('\r') {
                owned = owned.replace("\r\n", "\n").replace('\r', "\n");
            }
            Ok(Cow::Owned(owned))
        }
    }
}

/// Attempt to decode UTF-16 HTML that was provided as a lossy UTF-8 string.
///
/// Some callers read raw bytes and convert with `from_utf8_lossy`, which preserves
/// the NUL-byte pattern of UTF-16 input. When we detect that pattern, we can
/// recover the original HTML instead of rejecting it as binary data.
fn decode_utf16_if_needed(html: &str) -> Cow<'_, str> {
    let bytes = html.as_bytes();
    if !bytes.contains(&0) {
        return Cow::Borrowed(html);
    }

    let Some(encoding) = detect_utf16_encoding(bytes) else {
        return Cow::Borrowed(html);
    };

    let decoded = decode_utf16_bytes(bytes, encoding);
    if decoded.is_empty() {
        Cow::Borrowed(html)
    } else {
        Cow::Owned(decoded)
    }
}

fn decode_utf16_bytes(bytes: &[u8], encoding: Utf16Encoding) -> String {
    let (is_little_endian, skip_bom) = match encoding {
        Utf16Encoding::BomLe => (true, true),
        Utf16Encoding::BomBe => (false, true),
        Utf16Encoding::NoBomLe => (true, false),
        Utf16Encoding::NoBomBe => (false, false),
    };

    let mut units = Vec::with_capacity(bytes.len() / 2);
    for chunk in bytes.chunks_exact(2) {
        let unit = if is_little_endian {
            u16::from_le_bytes([chunk[0], chunk[1]])
        } else {
            u16::from_be_bytes([chunk[0], chunk[1]])
        };
        units.push(unit);
    }

    let mut decoded = String::from_utf16_lossy(&units);
    if skip_bom {
        decoded = decoded.trim_start_matches('\u{FEFF}').to_string();
    }
    decoded
}

/// Strip NUL bytes that can appear in malformed HTML inputs.
fn strip_nul_bytes(html: &str) -> Cow<'_, str> {
    if html.contains('\0') {
        Cow::Owned(html.replace('\0', ""))
    } else {
        Cow::Borrowed(html)
    }
}

/// Normalize line endings in HTML input.
///
/// Converts CRLF and CR line endings to LF for consistent processing.
fn normalize_line_endings(html: &str) -> Cow<'_, str> {
    if html.contains('\r') {
        Cow::Owned(html.replace("\r\n", "\n").replace('\r', "\n"))
    } else {
        Cow::Borrowed(html)
    }
}

/// Fast path for plain text (no HTML) conversion.
///
/// Skips HTML parsing if no angle brackets are present.
fn fast_text_only(html: &str, options: &ConversionOptions) -> Option<String> {
    if html.contains('<') {
        return None;
    }

    let mut decoded = text::decode_html_entities_cow(html);
    if options.strip_newlines && (decoded.contains('\n') || decoded.contains('\r')) {
        decoded = Cow::Owned(decoded.replace(&['\r', '\n'][..], " "));
    }
    let trimmed = decoded.trim_end_matches('\n');
    if trimmed.is_empty() {
        return Some(String::new());
    }

    let normalized = if options.whitespace_mode == WhitespaceMode::Normalized {
        text::normalize_whitespace_cow(trimmed)
    } else {
        Cow::Borrowed(trimmed)
    };

    let escaped =
        if options.escape_misc || options.escape_asterisks || options.escape_underscores || options.escape_ascii {
            text::escape(
                normalized.as_ref(),
                options.escape_misc,
                options.escape_asterisks,
                options.escape_underscores,
                options.escape_ascii,
            )
            .into_owned()
        } else {
            normalized.into_owned()
        };

    let mut output = String::with_capacity(escaped.len() + 1);
    output.push_str(&escaped);
    while output.ends_with(' ') || output.ends_with('\t') {
        output.pop();
    }
    output.push('\n');
    Some(output)
}

// ============================================================================
// JSON Configuration Parsing (requires serde feature)
// ============================================================================

#[cfg(any(feature = "serde", feature = "metadata"))]
fn parse_json<T: serde::de::DeserializeOwned>(json: &str) -> Result<T> {
    serde_json::from_str(json).map_err(|err| ConversionError::ConfigError(err.to_string()))
}

#[cfg(any(feature = "serde", feature = "metadata"))]
/// Parse JSON string into `ConversionOptions`.
///
/// Deserializes a JSON string into a full set of conversion options.
/// The JSON can be either a complete or partial options object.
///
/// # Arguments
///
/// * `json` - JSON string representing conversion options
///
/// # Returns
///
/// Fully populated `ConversionOptions` with defaults applied to any unspecified values
///
/// # Errors
///
/// Returns `ConversionError::ConfigError` if JSON parsing fails or contains invalid option values
pub fn conversion_options_from_json(json: &str) -> Result<ConversionOptions> {
    let update: ConversionOptionsUpdate = parse_json(json)?;
    Ok(ConversionOptions::from(update))
}

#[cfg(any(feature = "serde", feature = "metadata"))]
/// Parse JSON string into partial `ConversionOptions` update.
///
/// Deserializes a JSON string into a partial set of conversion options.
/// Only specified options are included; unspecified options are None.
///
/// # Arguments
///
/// * `json` - JSON string representing partial conversion options
///
/// # Returns
///
/// `ConversionOptionsUpdate` with only specified fields populated
///
/// # Errors
///
/// Returns `ConversionError::ConfigError` if JSON parsing fails or contains invalid option values
pub fn conversion_options_update_from_json(json: &str) -> Result<ConversionOptionsUpdate> {
    parse_json(json)
}

#[cfg(all(feature = "inline-images", any(feature = "serde", feature = "metadata")))]
/// Parse JSON string into `InlineImageConfig` (requires `inline-images` feature).
///
/// Deserializes a JSON string into inline image extraction configuration.
/// The JSON can be either a complete or partial configuration object.
///
/// # Arguments
///
/// * `json` - JSON string representing inline image configuration
///
/// # Returns
///
/// Fully populated `InlineImageConfig` with defaults applied to any unspecified values
///
/// # Errors
///
/// Returns `ConversionError::ConfigError` if JSON parsing fails or contains invalid configuration values
pub fn inline_image_config_from_json(json: &str) -> Result<InlineImageConfig> {
    let update: crate::InlineImageConfigUpdate = parse_json(json)?;
    Ok(InlineImageConfig::from_update(update))
}

#[cfg(all(feature = "metadata", any(feature = "serde", feature = "metadata")))]
/// Parse JSON string into `MetadataConfig` (requires `metadata` feature).
///
/// Deserializes a JSON string into metadata extraction configuration.
/// The JSON can be either a complete or partial configuration object.
///
/// # Arguments
///
/// * `json` - JSON string representing metadata extraction configuration
///
/// # Returns
///
/// Fully populated `MetadataConfig` with defaults applied to any unspecified values
///
/// # Errors
///
/// Returns `ConversionError::ConfigError` if JSON parsing fails or contains invalid configuration values
pub fn metadata_config_from_json(json: &str) -> Result<MetadataConfig> {
    let update: crate::MetadataConfigUpdate = parse_json(json)?;
    Ok(MetadataConfig::from(update))
}
