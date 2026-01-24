//! Metadata extraction conversion functions.
//!
//! This module provides conversion functions that extract metadata from HTML
//! alongside the markdown conversion.

use pyo3::prelude::*;
#[cfg(feature = "visitor")]
use std::cell::RefCell;
#[cfg(feature = "visitor")]
use std::rc::Rc;

use crate::handles::ConversionOptionsHandle;
use crate::helpers::{run_with_guard_and_profile, to_py_err};
use crate::options::ConversionOptions;
use crate::types::{MetadataConfig, extended_metadata_to_py};
#[cfg(feature = "visitor")]
use crate::visitor;
use html_to_markdown_bindings_common::{parse_conversion_options, parse_metadata_config};
use html_to_markdown_rs::metadata::DEFAULT_MAX_STRUCTURED_DATA_SIZE;
#[cfg(feature = "visitor")]
use html_to_markdown_rs::visitor::HtmlVisitor;

/// Convert HTML to Markdown with comprehensive metadata extraction.
///
/// Performs HTML-to-Markdown conversion while simultaneously extracting structured metadata
/// including document properties, headers, links, images, and structured data in a single pass.
/// Ideal for content analysis, SEO workflows, and document indexing.
///
/// Args:
///     html (str): HTML string to convert. Line endings are normalized (CRLF -> LF).
///     options (ConversionOptions, optional): Conversion configuration controlling output format.
///         Defaults to standard conversion options if None. Controls:
///         - heading_style: "atx", "atx_closed", or "underlined"
///         - list_indent_type: "spaces" or "tabs"
///         - wrap: Enable text wrapping at specified width
///         - And many other formatting options
///     metadata_config (MetadataConfig, optional): Configuration for metadata extraction.
///         Defaults to extracting all metadata types if None. Configure with:
///         - extract_headers: bool - Extract h1-h6 heading elements
///         - extract_links: bool - Extract hyperlinks with type classification
///         - extract_images: bool - Extract image elements
///         - extract_structured_data: bool - Extract JSON-LD/Microdata/RDFa
///         - max_structured_data_size: int - Size limit for structured data (bytes)
///
/// Returns:
///     tuple[str, dict]: A tuple of (markdown_string, metadata_dict) where:
///
///     markdown_string: str
///         The converted Markdown output
///
///     metadata_dict: dict with keys:
///         - document: dict containing:
///             - title: str | None - Document title from <title> tag
///             - description: str | None - From <meta name="description">
///             - keywords: list[str] - Keywords from <meta name="keywords">
///             - author: str | None - Author from <meta name="author">
///             - language: str | None - Language from lang attribute
///             - text_direction: str | None - Text direction ("ltr", "rtl", "auto")
///             - canonical_url: str | None - Canonical URL from <link rel="canonical">
///             - base_href: str | None - Base URL from <base href="">
///             - open_graph: dict[str, str] - Open Graph properties (og:*)
///             - twitter_card: dict[str, str] - Twitter Card properties (twitter:*)
///             - meta_tags: dict[str, str] - Other meta tags
///
///         - headers: list[dict] containing:
///             - level: int - Header level (1-6)
///             - text: str - Header text content
///             - id: str | None - HTML id attribute
///             - depth: int - Nesting depth in document tree
///             - html_offset: int - Byte offset in original HTML
///
///         - links: list[dict] containing:
///             - href: str - Link URL
///             - text: str - Link text content
///             - title: str | None - Link title attribute
///             - link_type: str - Type: "anchor", "internal", "external", "email", "phone", "other"
///             - rel: list[str] - Rel attribute values
///             - attributes: dict[str, str] - Additional HTML attributes
///
///         - images: list[dict] containing:
///             - src: str - Image source (URL or data URI)
///             - alt: str | None - Alt text for accessibility
///             - title: str | None - Title attribute
///             - dimensions: tuple[int, int] | None - (width, height) if available
///             - image_type: str - Type: "data_uri", "external", "relative", "inline_svg"
///             - attributes: dict[str, str] - Additional HTML attributes
///
///         - structured_data: list[dict] containing:
///             - data_type: str - Type: "json_ld", "microdata", or "rdfa"
///             - raw_json: str - Raw JSON string content
///             - schema_type: str | None - Schema type (e.g., "Article", "Event")
///
/// Raises:
///     ValueError: If HTML parsing fails or configuration is invalid
///     RuntimeError: If a panic occurs during conversion
///
/// Examples:
///
///     Basic usage - extract all metadata:
///
///     ```ignore
///     from html_to_markdown import convert_with_metadata, MetadataConfig
///
///     html = '''
///     <html lang="en">
///         <head>
///             <title>My Blog Post</title>
///             <meta name="description" content="A great article">
///         </head>
///         <body>
///             <h1 id="intro">Introduction</h1>
///             <p>Read more at <a href="https://example.com">our site</a></p>
///             <img src="photo.jpg" alt="Beautiful landscape">
///         </body>
///     </html>
///     '''
///
///     markdown, metadata = convert_with_metadata(html)
///
///     print(f"Title: {metadata['document']['title']}")
///     # Output: Title: My Blog Post
///
///     print(f"Language: {metadata['document']['language']}")
///     # Output: Language: en
///
///     print(f"Headers found: {len(metadata['headers'])}")
///     # Output: Headers found: 1
///
///     for header in metadata['headers']:
///         print(f"  - {header['text']} (level {header['level']})")
///     # Output:   - Introduction (level 1)
///
///     print(f"External links: {len([l for l in metadata['links'] if l['link_type'] == 'external'])}")
///     # Output: External links: 1
///
///     for img in metadata['images']:
///         print(f"Image: {img['alt']} ({img['src']})")
///     # Output: Image: Beautiful landscape (photo.jpg)
///     ```
///
///     Selective metadata extraction - headers and links only:
///
///     ```ignore
///     from html_to_markdown import convert_with_metadata, MetadataConfig
///
///     config = MetadataConfig(
///         extract_headers=True,
///         extract_links=True,
///         extract_images=False,  # Skip image extraction
///         extract_structured_data=False  # Skip structured data
///     )
///
///     markdown, metadata = convert_with_metadata(html, metadata_config=config)
///
///     assert len(metadata['images']) == 0  # Images not extracted
///     assert len(metadata['headers']) > 0  # Headers extracted
///     ```
///
///     With custom conversion options:
///
///     ```ignore
///     from html_to_markdown import convert_with_metadata, ConversionOptions, MetadataConfig
///
///     options = ConversionOptions(
///         heading_style="atx",  # Use # H1, ## H2 style
///         wrap=True,
///         wrap_width=80
///     )
///
///     config = MetadataConfig(extract_headers=True)
///
///     markdown, metadata = convert_with_metadata(html, options=options, metadata_config=config)
///     # Markdown uses ATX-style headings and is wrapped at 80 chars
///     ```
///
/// See Also:
///     - convert: Simple HTML to Markdown conversion without metadata
///     - convert_with_inline_images: Extract inline images alongside conversion
///     - ConversionOptions: Conversion configuration class
///     - MetadataConfig: Metadata extraction configuration class
#[cfg(feature = "visitor")]
#[pyfunction]
#[pyo3(signature = (html, options=None, metadata_config=None, visitor=None))]
pub fn convert_with_metadata<'py>(
    py: Python<'py>,
    html: &str,
    options: Option<ConversionOptions>,
    metadata_config: Option<MetadataConfig>,
    visitor: Option<Py<PyAny>>,
) -> PyResult<(String, Py<PyAny>)> {
    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());
    let cfg = metadata_config
        .unwrap_or_else(|| MetadataConfig::new(true, true, true, true, true, DEFAULT_MAX_STRUCTURED_DATA_SIZE));
    let rust_cfg = cfg.to_rust();

    let result = if let Some(visitor_py) = visitor {
        let bridge = visitor::PyVisitorBridge::new(visitor_py);
        let visitor_handle = std::sync::Arc::new(std::sync::Mutex::new(bridge));
        py.detach(move || {
            run_with_guard_and_profile(|| {
                let rc_visitor: Rc<RefCell<dyn HtmlVisitor>> = {
                    Python::attach(|py| {
                        let guard = visitor_handle.lock().unwrap();
                        let bridge_copy = visitor::PyVisitorBridge::new(guard.visitor.clone_ref(py));
                        Rc::new(RefCell::new(bridge_copy)) as Rc<RefCell<dyn HtmlVisitor>>
                    })
                };
                html_to_markdown_rs::convert_with_metadata(
                    &html,
                    rust_options.clone(),
                    rust_cfg.clone(),
                    Some(rc_visitor),
                )
            })
        })
        .map_err(to_py_err)?
    } else {
        py.detach(move || {
            run_with_guard_and_profile(|| {
                html_to_markdown_rs::convert_with_metadata(&html, rust_options.clone(), rust_cfg.clone(), None)
            })
        })
        .map_err(to_py_err)?
    };

    let (markdown, metadata) = result;
    let metadata_dict = extended_metadata_to_py(py, metadata)?;
    Ok((markdown, metadata_dict))
}

#[cfg(not(feature = "visitor"))]
#[pyfunction]
#[pyo3(signature = (html, options=None, metadata_config=None, visitor=None))]
pub fn convert_with_metadata<'py>(
    py: Python<'py>,
    html: &str,
    options: Option<ConversionOptions>,
    metadata_config: Option<MetadataConfig>,
    visitor: Option<Py<PyAny>>,
) -> PyResult<(String, Py<PyAny>)> {
    if visitor.is_some() {
        return Err(PyErr::new::<pyo3::exceptions::PyNotImplementedError, _>(
            "Visitor support requires the 'visitor' feature to be enabled",
        ));
    }
    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());
    let cfg = metadata_config
        .unwrap_or_else(|| MetadataConfig::new(true, true, true, true, true, DEFAULT_MAX_STRUCTURED_DATA_SIZE));
    let rust_cfg = cfg.to_rust();
    let result = py
        .detach(move || {
            run_with_guard_and_profile(|| {
                html_to_markdown_rs::convert_with_metadata(&html, rust_options.clone(), rust_cfg.clone(), None)
            })
        })
        .map_err(to_py_err)?;

    let (markdown, metadata) = result;
    let metadata_dict = extended_metadata_to_py(py, metadata)?;
    Ok((markdown, metadata_dict))
}

#[pyfunction]
#[pyo3(signature = (html, options_json=None, metadata_config_json=None))]
pub fn convert_with_metadata_json(
    py: Python<'_>,
    html: &str,
    options_json: Option<&str>,
    metadata_config_json: Option<&str>,
) -> PyResult<(String, Py<PyAny>)> {
    let html = html.to_owned();
    let rust_options = parse_conversion_options(options_json).map_err(to_py_err)?;
    let rust_cfg = parse_metadata_config(metadata_config_json).map_err(to_py_err)?;

    let result = py
        .detach(move || {
            run_with_guard_and_profile(|| {
                html_to_markdown_rs::convert_with_metadata(&html, rust_options.clone(), rust_cfg.clone(), None)
            })
        })
        .map_err(to_py_err)?;

    let (markdown, metadata) = result;
    let metadata_dict = extended_metadata_to_py(py, metadata)?;
    Ok((markdown, metadata_dict))
}

/// Convert HTML to Markdown with metadata using a pre-parsed options handle.
#[pyfunction]
#[pyo3(signature = (html, handle, metadata_config=None))]
pub fn convert_with_metadata_handle<'py>(
    py: Python<'py>,
    html: &str,
    handle: &ConversionOptionsHandle,
    metadata_config: Option<MetadataConfig>,
) -> PyResult<(String, Py<PyAny>)> {
    let html = html.to_owned();
    let rust_options = Some(handle.inner.clone());
    let cfg = metadata_config
        .unwrap_or_else(|| MetadataConfig::new(true, true, true, true, true, DEFAULT_MAX_STRUCTURED_DATA_SIZE));
    let rust_cfg = cfg.to_rust();
    let result = py
        .detach(move || {
            run_with_guard_and_profile(|| {
                html_to_markdown_rs::convert_with_metadata(&html, rust_options.clone(), rust_cfg.clone(), None)
            })
        })
        .map_err(to_py_err)?;

    let (markdown, metadata) = result;
    let metadata_dict = extended_metadata_to_py(py, metadata)?;
    Ok((markdown, metadata_dict))
}
