use pyo3::prelude::*;

#[pyfunction]
fn parse_code(code: &str) -> PyResult<()> {
    ruff_python_parser::parse_module(code)
        .map(|_| ())
        .map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
                "Failed to parse code: {}",
                e
            ))
        })
}

#[pyfunction]
fn is_valid_syntax(code: &str) -> bool {
    ruff_python_parser::parse_module(code).is_ok()
}

#[pyfunction]
#[pyo3(signature = (code, *, line_width = 80u16))]
fn format_string(code: &str, line_width: u16) -> PyResult<String> {
    ruff_python_formatter::format_module_source(
        code,
        ruff_python_formatter::PyFormatOptions::default().with_line_width(line_width.try_into()?),
    )
    .map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to format code: {}", e))
    })
    .map(|formatted| formatted.into_code())
}

#[pymodule(gil_used = false)]
fn ruff_format(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(format_string, m)?)?;
    m.add_function(wrap_pyfunction!(is_valid_syntax, m)?)?;
    m.add_function(wrap_pyfunction!(parse_code, m)?)?;
    Ok(())
}
