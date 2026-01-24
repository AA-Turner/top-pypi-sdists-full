#![allow(
    clippy::too_many_lines,
    clippy::option_if_let_else,
    clippy::match_wildcard_for_single_variants,
    clippy::needless_pass_by_value,
    clippy::struct_excessive_bools,
    clippy::fn_params_excessive_bools,
    clippy::branches_sharing_code,
    clippy::match_same_arms,
    clippy::missing_errors_doc,
    clippy::items_after_statements,
    clippy::doc_markdown,
    clippy::cast_sign_loss,
    clippy::default_trait_access,
    clippy::unused_self,
    clippy::cast_precision_loss,
    clippy::collapsible_if,
    clippy::too_many_arguments,
    clippy::collapsible_else_if,
    clippy::extra_unused_lifetimes,
    clippy::unnecessary_lazy_evaluations,
    clippy::must_use_candidate,
    clippy::trivially_copy_pass_by_ref,
    clippy::explicit_iter_loop,
    clippy::missing_const_for_fn,
    clippy::manual_assert,
    clippy::return_self_not_must_use,
    clippy::collapsible_match,
    clippy::cast_possible_truncation,
    clippy::map_unwrap_or,
    clippy::manual_let_else,
    clippy::used_underscore_binding,
    clippy::assigning_clones,
    clippy::uninlined_format_args
)]
#![allow(dead_code)]

//! High-performance HTML to Markdown converter.
//!
//! Built with html5ever for fast, memory-efficient HTML parsing.
//!
//! ## Optional inline image extraction
//!
//! Enable the `inline-images` Cargo feature to collect embedded data URI images and inline SVG
//! assets alongside the produced Markdown.

// ============================================================================
// Module Declarations
// ============================================================================

pub mod converter;
pub mod error;
pub mod hocr;
#[cfg(feature = "inline-images")]
mod inline_images;
#[cfg(feature = "metadata")]
pub mod metadata;
pub mod options;
pub mod safety;
pub mod text;
#[cfg(feature = "visitor")]
pub mod visitor;
#[cfg(feature = "visitor")]
pub mod visitor_helpers;
pub mod wrapper;

// Internal modules (not part of public API)
mod convert_api;
mod exports;
pub mod prelude;
mod validation;

// ============================================================================
// Public Re-exports (from exports module)
// ============================================================================

pub use exports::*;

// ============================================================================
// Main Public API Functions
// ============================================================================

pub use convert_api::convert;

#[cfg(any(feature = "serde", feature = "metadata"))]
pub use convert_api::{conversion_options_from_json, conversion_options_update_from_json};

#[cfg(feature = "metadata")]
pub use convert_api::metadata_config_from_json;

#[cfg(feature = "inline-images")]
pub use convert_api::{convert_with_inline_images, inline_image_config_from_json};

#[cfg(feature = "metadata")]
pub use convert_api::convert_with_metadata;

#[cfg(feature = "visitor")]
pub use convert_api::convert_with_visitor;

#[cfg(feature = "async-visitor")]
pub use convert_api::convert_with_async_visitor;

// Tests
// ============================================================================

#[cfg(all(test, feature = "metadata"))]
mod tests {
    use super::*;

    #[test]
    fn test_convert_with_metadata_full_workflow() {
        let html = "<html lang=\"en\" dir=\"ltr\"><head><title>Test Article</title></head><body><h1 id=\"main-title\">Main Title</h1><p>This is a paragraph with a <a href=\"https://example.com\">link</a>.</p><h2>Subsection</h2><p>Another paragraph with <a href=\"#main-title\">internal link</a>.</p><img src=\"https://example.com/image.jpg\" alt=\"Test image\" title=\"Image title\"></body></html>";

        let config = MetadataConfig {
            extract_document: true,
            extract_headers: true,
            extract_links: true,
            extract_images: true,
            extract_structured_data: true,
            max_structured_data_size: metadata::DEFAULT_MAX_STRUCTURED_DATA_SIZE,
        };

        let (markdown, metadata) = convert_with_metadata(html, None, config, None).expect("conversion should succeed");

        assert!(!markdown.is_empty());
        assert!(markdown.contains("Main Title"));
        assert!(markdown.contains("Subsection"));

        assert_eq!(metadata.document.language, Some("en".to_string()));

        assert_eq!(metadata.headers.len(), 2);
        assert_eq!(metadata.headers[0].level, 1);
        assert_eq!(metadata.headers[0].text, "Main Title");
        assert_eq!(metadata.headers[0].id, Some("main-title".to_string()));
        assert_eq!(metadata.headers[1].level, 2);
        assert_eq!(metadata.headers[1].text, "Subsection");

        assert!(metadata.links.len() >= 2);
        let external_link = metadata.links.iter().find(|l| l.link_type == LinkType::External);
        assert!(external_link.is_some());
        let anchor_link = metadata.links.iter().find(|l| l.link_type == LinkType::Anchor);
        assert!(anchor_link.is_some());

        assert_eq!(metadata.images.len(), 1);
        assert_eq!(metadata.images[0].alt, Some("Test image".to_string()));
        assert_eq!(metadata.images[0].title, Some("Image title".to_string()));
        assert_eq!(metadata.images[0].image_type, ImageType::External);
    }

    #[test]
    fn test_convert_with_metadata_document_fields() {
        let html = "<html lang=\"en\"><head><title>Test Article</title><meta name=\"description\" content=\"Desc\"><meta name=\"author\" content=\"Author\"><meta property=\"og:title\" content=\"OG Title\"><meta property=\"og:description\" content=\"OG Desc\"></head><body><h1>Heading</h1></body></html>";

        let (_markdown, metadata) =
            convert_with_metadata(html, None, MetadataConfig::default(), None).expect("conversion should succeed");

        assert_eq!(
            metadata.document.title,
            Some("Test Article".to_string()),
            "document: {:?}",
            metadata.document
        );
        assert_eq!(metadata.document.description, Some("Desc".to_string()));
        assert_eq!(metadata.document.author, Some("Author".to_string()));
        assert_eq!(metadata.document.language, Some("en".to_string()));
        assert_eq!(metadata.document.open_graph.get("title"), Some(&"OG Title".to_string()));
        assert_eq!(
            metadata.document.open_graph.get("description"),
            Some(&"OG Desc".to_string())
        );
    }

    #[test]
    fn test_convert_with_metadata_empty_config() {
        let html = "<html lang=\"en\"><head><title>Test</title></head><body><h1>Title</h1><a href=\"#\">Link</a></body></html>";

        let config = MetadataConfig {
            extract_document: false,
            extract_headers: false,
            extract_links: false,
            extract_images: false,
            extract_structured_data: false,
            max_structured_data_size: 0,
        };

        let (_markdown, metadata) = convert_with_metadata(html, None, config, None).expect("conversion should succeed");

        assert!(metadata.headers.is_empty());
        assert!(metadata.links.is_empty());
        assert!(metadata.images.is_empty());
        assert_eq!(metadata.document.language, None);
    }

    #[test]
    fn test_convert_with_metadata_data_uri_image() {
        let html = "<html><body><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==\" alt=\"Pixel\"></body></html>";

        let config = MetadataConfig::default();

        let (_markdown, metadata) = convert_with_metadata(html, None, config, None).expect("conversion should succeed");

        assert_eq!(metadata.images.len(), 1);
        assert_eq!(metadata.images[0].image_type, ImageType::DataUri);
        assert_eq!(metadata.images[0].alt, Some("Pixel".to_string()));
    }

    #[test]
    fn test_convert_with_metadata_relative_paths() {
        let html = r#"<html><body><a href="/page">Internal</a><a href="../other">Relative</a></body></html>"#;

        let config = MetadataConfig::default();

        let (_markdown, metadata) = convert_with_metadata(html, None, config, None).expect("conversion should succeed");

        let internal_links: Vec<_> = metadata
            .links
            .iter()
            .filter(|l| l.link_type == LinkType::Internal)
            .collect();
        assert_eq!(internal_links.len(), 2);
    }
}

#[cfg(test)]
mod basic_tests {
    use super::*;

    #[test]
    fn test_binary_input_rejected() {
        let html = "PDF\0DATA";
        let result = convert(html, None);
        assert!(matches!(result, Err(ConversionError::InvalidInput(_))));
    }

    #[test]
    fn test_binary_magic_rejected() {
        let html = String::from_utf8_lossy(b"\x1F\x8B\x08\x00gzip").to_string();
        let result = convert(&html, None);
        assert!(matches!(result, Err(ConversionError::InvalidInput(_))));
    }

    #[test]
    fn test_utf16_hint_rejected() {
        let html = String::from_utf8_lossy(b"\xFF\xFE<\0h\0t\0m\0l\0>\0").to_string();
        let result = convert(&html, None);
        assert!(matches!(result, Err(ConversionError::InvalidInput(_))));
    }

    #[test]
    fn test_plain_text_allowed() {
        let result = convert("Just text", None).unwrap();
        assert!(result.contains("Just text"));
    }

    #[test]
    fn test_plain_text_escaped_when_enabled() {
        let options = ConversionOptions {
            escape_asterisks: true,
            escape_underscores: true,
            ..ConversionOptions::default()
        };
        let result = convert("Text *asterisks* _underscores_", Some(options)).unwrap();
        assert!(result.contains(r"\*asterisks\*"));
        assert!(result.contains(r"\_underscores\_"));
    }
}
