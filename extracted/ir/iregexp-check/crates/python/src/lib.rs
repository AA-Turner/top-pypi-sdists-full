use iregexp::check;
use pyo3::prelude::*;

/// Return _True_ if regular expression _pattern_ is valid according I-Regexp.
#[pyfunction]
#[pyo3(name = "check")]
fn py_check(pattern: &str) -> bool {
    check(pattern)
}

#[pymodule]
fn iregexp_check(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_check, m)?)?;
    Ok(())
}
