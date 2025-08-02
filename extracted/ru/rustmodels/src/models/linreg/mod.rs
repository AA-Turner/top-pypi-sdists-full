use pyo3::prelude::*;

#[pyfunction]
pub fn linear_regression_fit(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

// Create the linreg submodule
pub fn create_linreg_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "linreg")?;
    m.add_function(wrap_pyfunction!(linear_regression_fit, &m)?)?;
    Ok(m)
}
