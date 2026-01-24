#[cfg(feature = "inline-images")]
use html_to_markdown_rs::{DEFAULT_INLINE_IMAGE_LIMIT, InlineImageConfig as RustInlineImageConfig};
use pyo3::prelude::*;
#[cfg(feature = "inline-images")]
use pyo3::types::{PyBytes, PyDict};

/// Python wrapper for inline image extraction configuration
#[cfg(feature = "inline-images")]
#[pyclass]
#[derive(Clone)]
pub struct InlineImageConfig {
    #[pyo3(get, set)]
    pub max_decoded_size_bytes: u64,
    #[pyo3(get, set)]
    pub filename_prefix: Option<String>,
    #[pyo3(get, set)]
    pub capture_svg: bool,
    #[pyo3(get, set)]
    pub infer_dimensions: bool,
}

#[cfg(feature = "inline-images")]
#[pymethods]
impl InlineImageConfig {
    #[new]
    #[pyo3(signature = (
        max_decoded_size_bytes=DEFAULT_INLINE_IMAGE_LIMIT,
        filename_prefix=None,
        capture_svg=true,
        infer_dimensions=false
    ))]
    pub const fn new(
        max_decoded_size_bytes: u64,
        filename_prefix: Option<String>,
        capture_svg: bool,
        infer_dimensions: bool,
    ) -> Self {
        Self {
            max_decoded_size_bytes,
            filename_prefix,
            capture_svg,
            infer_dimensions,
        }
    }
}

#[cfg(feature = "inline-images")]
impl InlineImageConfig {
    pub fn to_rust(&self) -> RustInlineImageConfig {
        let mut cfg = RustInlineImageConfig::new(self.max_decoded_size_bytes);
        cfg.filename_prefix = self.filename_prefix.clone();
        cfg.capture_svg = self.capture_svg;
        cfg.infer_dimensions = self.infer_dimensions;
        cfg
    }
}

/// Convert InlineImage to Python dict
#[cfg(feature = "inline-images")]
pub fn inline_image_to_py<'py>(py: Python<'py>, image: html_to_markdown_rs::InlineImage) -> PyResult<Py<PyAny>> {
    let dict = PyDict::new(py);
    dict.set_item("data", PyBytes::new(py, &image.data))?;
    dict.set_item("format", image.format.to_string())?;

    match image.filename {
        Some(filename) => dict.set_item("filename", filename)?,
        None => dict.set_item("filename", py.None())?,
    }

    match image.description {
        Some(description) => dict.set_item("description", description)?,
        None => dict.set_item("description", py.None())?,
    }

    if let Some((width, height)) = image.dimensions {
        dict.set_item("dimensions", (width, height))?;
    } else {
        dict.set_item("dimensions", py.None())?;
    }

    dict.set_item("source", image.source.to_string())?;

    let attrs = PyDict::new(py);
    for (key, value) in image.attributes {
        attrs.set_item(key, value)?;
    }
    dict.set_item("attributes", attrs)?;

    Ok(dict.into())
}

/// Convert InlineImageWarning to Python dict
#[cfg(feature = "inline-images")]
pub fn warning_to_py<'py>(py: Python<'py>, warning: html_to_markdown_rs::InlineImageWarning) -> PyResult<Py<PyAny>> {
    let dict = PyDict::new(py);
    dict.set_item("index", warning.index)?;
    dict.set_item("message", warning.message)?;
    Ok(dict.into())
}
