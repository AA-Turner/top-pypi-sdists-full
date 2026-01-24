//! Shared helper utilities for Python bindings.

use html_to_markdown_rs::ConversionError;
use html_to_markdown_rs::safety::guard_panic;
use pyo3::prelude::*;
use std::panic::UnwindSafe;

use crate::profiling;

/// Convert ConversionError to PyErr using helper functions from common crate.
pub fn to_py_err(err: ConversionError) -> PyErr {
    use html_to_markdown_bindings_common::error::{error_message, is_panic_error};

    if is_panic_error(&err) {
        pyo3::exceptions::PyRuntimeError::new_err(error_message(&err))
    } else {
        pyo3::exceptions::PyValueError::new_err(error_message(&err))
    }
}

/// Run a function with panic guard and optional profiling.
pub fn run_with_guard_and_profile<F, T>(f: F) -> html_to_markdown_rs::Result<T>
where
    F: FnMut() -> html_to_markdown_rs::Result<T> + UnwindSafe,
{
    guard_panic(|| profiling::maybe_profile(f))
}
