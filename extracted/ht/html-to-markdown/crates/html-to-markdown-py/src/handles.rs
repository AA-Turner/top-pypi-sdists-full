use html_to_markdown_rs::ConversionOptions as RustConversionOptions;
use pyo3::prelude::*;

use crate::options::ConversionOptions;

/// Pre-parsed conversion options handle for efficient reuse.
///
/// ConversionOptionsHandle stores parsed Rust options internally,
/// allowing for efficient reuse across multiple conversions without
/// re-parsing options on each call.
#[pyclass(name = "ConversionOptionsHandle")]
#[derive(Clone)]
pub struct ConversionOptionsHandle {
    pub inner: RustConversionOptions,
}

impl ConversionOptionsHandle {
    /// Create a new handle from optional Python conversion options.
    pub fn new_with_options(options: Option<ConversionOptions>) -> Self {
        let inner = options.map(|opts| opts.to_rust()).unwrap_or_default();
        Self { inner }
    }

    /// Create a new handle from Rust conversion options directly.
    pub const fn new_with_rust(options: RustConversionOptions) -> Self {
        Self { inner: options }
    }
}

#[pymethods]
impl ConversionOptionsHandle {
    #[new]
    #[pyo3(signature = (options=None))]
    fn py_new(options: Option<ConversionOptions>) -> Self {
        Self::new_with_options(options)
    }
}
