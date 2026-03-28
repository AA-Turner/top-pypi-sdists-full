#![allow(clippy::cast_precision_loss, clippy::cast_sign_loss, clippy::unused_self)]
//! hOCR 1.2 document processing.
//!
//! **Deprecated since 2.30.0**: hOCR support will be removed in v3.
//!
//! Complete hOCR 1.2 specification support for extracting structured content from OCR documents.
//!
//! ## Features
//!
//! - **Full Element Support**: All 40+ hOCR 1.2 element types
//! - **Complete Property Parsing**: All 20+ hOCR properties (bbox, baseline, fonts, etc.)
//! - **Document Structure**: Logical hierarchy (paragraphs, sections, chapters)
//! - **Spatial Table Reconstruction**: Automatic table detection from bbox coordinates
//! - **Metadata Extraction**: OCR system info, capabilities, languages
//!
//! ## Modules
//!
//! - [`types`]: Core hOCR element and property types
//! - [`parser`]: Property parsing from title attributes
//! - [`extractor`]: DOM to hOCR element tree extraction
//! - [`converter`]: hOCR to Markdown conversion
//! - [`spatial`]: Spatial table reconstruction from bounding boxes

#[allow(deprecated)]
pub mod converter;
#[allow(deprecated)]
pub mod extractor;
#[allow(deprecated)]
pub mod parser;
#[allow(deprecated)]
pub mod spatial;
#[allow(deprecated)]
pub mod types;

#[deprecated(since = "2.30.0", note = "hOCR support will be removed in v3.")]
pub use converter::{convert_to_markdown, convert_to_markdown_with_options};
#[deprecated(since = "2.30.0", note = "hOCR support will be removed in v3.")]
pub use extractor::extract_hocr_document;
#[deprecated(since = "2.30.0", note = "hOCR support will be removed in v3.")]
pub use spatial::{HocrWord, extract_hocr_words, reconstruct_table, table_to_markdown};
#[deprecated(since = "2.30.0", note = "hOCR support will be removed in v3.")]
pub use types::{BBox, Baseline, HocrElement, HocrElementType, HocrMetadata, HocrProperties};
