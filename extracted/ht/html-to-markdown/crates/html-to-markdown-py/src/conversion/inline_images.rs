//! Inline image extraction conversion functions.
//!
//! This module provides conversion functions that extract inline images from HTML
//! alongside the markdown conversion.

use pyo3::prelude::*;
#[cfg(feature = "visitor")]
use std::cell::RefCell;
#[cfg(feature = "visitor")]
use std::rc::Rc;

use crate::handles::ConversionOptionsHandle;
use crate::helpers::{run_with_guard_and_profile, to_py_err};
use crate::options::ConversionOptions;
use crate::types::{InlineImageConfig, inline_image_to_py, warning_to_py};
#[cfg(feature = "visitor")]
use crate::visitor;
use html_to_markdown_bindings_common::{parse_conversion_options, parse_inline_image_config};
use html_to_markdown_rs::DEFAULT_INLINE_IMAGE_LIMIT;
#[cfg(feature = "visitor")]
use html_to_markdown_rs::visitor::HtmlVisitor;

/// Result type for inline image extraction functions.
pub type PyInlineExtraction = PyResult<(String, Vec<Py<PyAny>>, Vec<Py<PyAny>>)>;

/// Convert HTML to Markdown with inline image extraction.
///
/// Extracts embedded images (data URIs and inline SVG) during conversion.
///
/// Args:
///     html: HTML string to convert
///     options: Optional conversion configuration
///     image_config: Optional image extraction configuration
///     visitor: Optional visitor for custom conversion logic (requires visitor feature)
///
/// Returns:
///     Tuple of (markdown: str, images: List[dict], warnings: List[dict])
///
/// Raises:
///     ValueError: Invalid HTML or configuration
///
/// Example:
///     ```ignore
///     from html_to_markdown import convert_with_inline_images, InlineImageConfig
///
///     html = '<img src="data:image/png;base64,..." alt="Logo">'
///     config = InlineImageConfig(max_decoded_size_bytes=1024*1024)
///     markdown, images, warnings = convert_with_inline_images(html, image_config=config)
///
///     print(f"Found {len(images)} images")
///     for img in images:
///         print(f"Format: {img['format']}, Size: {len(img['data'])} bytes")
///     ```
#[cfg(feature = "visitor")]
#[pyfunction]
#[pyo3(signature = (html, options=None, image_config=None, visitor=None))]
pub fn convert_with_inline_images<'py>(
    py: Python<'py>,
    html: &str,
    options: Option<ConversionOptions>,
    image_config: Option<InlineImageConfig>,
    visitor: Option<Py<PyAny>>,
) -> PyInlineExtraction {
    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());
    let cfg = image_config.unwrap_or_else(|| InlineImageConfig::new(DEFAULT_INLINE_IMAGE_LIMIT, None, true, false));
    let rust_cfg = cfg.to_rust();

    let extraction = if let Some(visitor_py) = visitor {
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
                html_to_markdown_rs::convert_with_inline_images(
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
                html_to_markdown_rs::convert_with_inline_images(&html, rust_options.clone(), rust_cfg.clone(), None)
            })
        })
        .map_err(to_py_err)?
    };

    let images = extraction
        .inline_images
        .into_iter()
        .map(|image| inline_image_to_py(py, image))
        .collect::<PyResult<Vec<_>>>()?;

    let warnings = extraction
        .warnings
        .into_iter()
        .map(|warning| warning_to_py(py, warning))
        .collect::<PyResult<Vec<_>>>()?;

    Ok((extraction.markdown, images, warnings))
}

#[cfg(not(feature = "visitor"))]
#[pyfunction]
#[pyo3(signature = (html, options=None, image_config=None, visitor=None))]
pub fn convert_with_inline_images<'py>(
    py: Python<'py>,
    html: &str,
    options: Option<ConversionOptions>,
    image_config: Option<InlineImageConfig>,
    visitor: Option<Py<PyAny>>,
) -> PyInlineExtraction {
    if visitor.is_some() {
        return Err(PyErr::new::<pyo3::exceptions::PyNotImplementedError, _>(
            "Visitor support requires the 'visitor' feature to be enabled",
        ));
    }
    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());
    let cfg = image_config.unwrap_or_else(|| InlineImageConfig::new(DEFAULT_INLINE_IMAGE_LIMIT, None, true, false));
    let rust_cfg = cfg.to_rust();
    let extraction = py
        .detach(move || {
            run_with_guard_and_profile(|| {
                html_to_markdown_rs::convert_with_inline_images(&html, rust_options.clone(), rust_cfg.clone(), None)
            })
        })
        .map_err(to_py_err)?;

    let images = extraction
        .inline_images
        .into_iter()
        .map(|image| inline_image_to_py(py, image))
        .collect::<PyResult<Vec<_>>>()?;

    let warnings = extraction
        .warnings
        .into_iter()
        .map(|warning| warning_to_py(py, warning))
        .collect::<PyResult<Vec<_>>>()?;

    Ok((extraction.markdown, images, warnings))
}

#[pyfunction]
#[pyo3(signature = (html, options_json=None, image_config_json=None))]
pub fn convert_with_inline_images_json<'py>(
    py: Python<'py>,
    html: &str,
    options_json: Option<&str>,
    image_config_json: Option<&str>,
) -> PyInlineExtraction {
    let html = html.to_owned();
    let rust_options = parse_conversion_options(options_json).map_err(to_py_err)?;
    let rust_config = parse_inline_image_config(image_config_json).map_err(to_py_err)?;
    let extraction = py
        .detach(move || {
            run_with_guard_and_profile(|| {
                html_to_markdown_rs::convert_with_inline_images(&html, rust_options.clone(), rust_config.clone(), None)
            })
        })
        .map_err(to_py_err)?;

    let images = extraction
        .inline_images
        .into_iter()
        .map(|image| inline_image_to_py(py, image))
        .collect::<PyResult<Vec<_>>>()?;

    let warnings = extraction
        .warnings
        .into_iter()
        .map(|warning| warning_to_py(py, warning))
        .collect::<PyResult<Vec<_>>>()?;

    Ok((extraction.markdown, images, warnings))
}

/// Convert HTML to Markdown with inline images using a pre-parsed options handle.
#[pyfunction]
#[pyo3(signature = (html, handle, image_config=None))]
pub fn convert_with_inline_images_handle<'py>(
    py: Python<'py>,
    html: &str,
    handle: &ConversionOptionsHandle,
    image_config: Option<InlineImageConfig>,
) -> PyInlineExtraction {
    let html = html.to_owned();
    let rust_options = Some(handle.inner.clone());
    let cfg = image_config.unwrap_or_else(|| InlineImageConfig::new(DEFAULT_INLINE_IMAGE_LIMIT, None, true, false));
    let rust_cfg = cfg.to_rust();
    let extraction = py
        .detach(move || {
            run_with_guard_and_profile(|| {
                html_to_markdown_rs::convert_with_inline_images(&html, rust_options.clone(), rust_cfg.clone(), None)
            })
        })
        .map_err(to_py_err)?;

    let images = extraction
        .inline_images
        .into_iter()
        .map(|image| inline_image_to_py(py, image))
        .collect::<PyResult<Vec<_>>>()?;

    let warnings = extraction
        .warnings
        .into_iter()
        .map(|warning| warning_to_py(py, warning))
        .collect::<PyResult<Vec<_>>>()?;

    Ok((extraction.markdown, images, warnings))
}
