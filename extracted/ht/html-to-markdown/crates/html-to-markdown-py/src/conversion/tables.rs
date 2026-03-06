//! Table extraction conversion functions.
//!
//! This module provides conversion functions that extract structured table data
//! from HTML alongside the markdown conversion.

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};

use crate::helpers::{run_with_guard_and_profile, to_py_err};
use crate::options::ConversionOptions;
#[cfg(feature = "metadata")]
use crate::types::{MetadataConfig, extended_metadata_to_py};

/// Convert HTML to Markdown with structured table extraction.
///
/// Performs HTML-to-Markdown conversion while simultaneously extracting structured
/// table data including cell contents, rendered markdown, and header row flags.
///
/// Args:
///     html (str): HTML string to convert.
///     options (ConversionOptions, optional): Conversion configuration.
///     metadata_config (MetadataConfig, optional): Metadata extraction configuration.
///         Only available when the metadata feature is enabled.
///
/// Returns:
///     dict: A dictionary with keys:
///         - content (str): The converted Markdown output
///         - metadata (dict | None): Extended metadata if metadata_config was provided
///         - tables (list[dict]): List of extracted tables, each with:
///             - cells (list[list[str]]): Row-major cell contents
///             - markdown (str): Rendered table in target format
///             - is_header_row (list[bool]): Per-row header flag
#[cfg(feature = "metadata")]
#[pyfunction]
#[pyo3(signature = (html, options=None, metadata_config=None))]
pub fn convert_with_tables<'py>(
    py: Python<'py>,
    html: &str,
    options: Option<ConversionOptions>,
    metadata_config: Option<MetadataConfig>,
) -> PyResult<Py<PyDict>> {
    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());
    let rust_metadata_cfg = metadata_config.map(|cfg| cfg.to_rust());

    let result = py
        .detach(move || {
            run_with_guard_and_profile(|| {
                html_to_markdown_rs::convert_with_tables(&html, rust_options.clone(), rust_metadata_cfg.clone())
            })
        })
        .map_err(to_py_err)?;

    let dict = PyDict::new(py);
    dict.set_item("content", &result.content)?;

    // Build tables list
    let tables_list = PyList::empty(py);
    for table in &result.tables {
        let table_dict = PyDict::new(py);
        let cells_list = PyList::empty(py);
        for row in &table.cells {
            let row_list = PyList::new(py, row)?;
            cells_list.append(row_list)?;
        }
        table_dict.set_item("cells", cells_list)?;
        table_dict.set_item("markdown", &table.markdown)?;
        let header_list = PyList::new(py, &table.is_header_row)?;
        table_dict.set_item("is_header_row", header_list)?;
        tables_list.append(table_dict)?;
    }
    dict.set_item("tables", tables_list)?;

    match result.metadata {
        Some(metadata) => {
            let metadata_py = extended_metadata_to_py(py, metadata)?;
            dict.set_item("metadata", metadata_py)?;
        }
        None => {
            dict.set_item("metadata", py.None())?;
        }
    }

    Ok(dict.into())
}

#[cfg(not(feature = "metadata"))]
#[pyfunction]
#[pyo3(signature = (html, options=None, metadata_config=None))]
pub fn convert_with_tables<'py>(
    py: Python<'py>,
    html: &str,
    options: Option<ConversionOptions>,
    metadata_config: Option<PyObject>,
) -> PyResult<Py<PyDict>> {
    let _ = metadata_config;
    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());

    let result = py
        .detach(move || {
            run_with_guard_and_profile(|| html_to_markdown_rs::convert_with_tables(&html, rust_options.clone(), None))
        })
        .map_err(to_py_err)?;

    let dict = PyDict::new(py);
    dict.set_item("content", &result.content)?;

    let tables_list = PyList::empty(py);
    for table in &result.tables {
        let table_dict = PyDict::new(py);
        let cells_list = PyList::empty(py);
        for row in &table.cells {
            let row_list = PyList::new(py, row)?;
            cells_list.append(row_list)?;
        }
        table_dict.set_item("cells", cells_list)?;
        table_dict.set_item("markdown", &table.markdown)?;
        let header_list = PyList::new(py, &table.is_header_row)?;
        table_dict.set_item("is_header_row", header_list)?;
        tables_list.append(table_dict)?;
    }
    dict.set_item("tables", tables_list)?;
    dict.set_item("metadata", py.None())?;

    Ok(dict.into())
}
