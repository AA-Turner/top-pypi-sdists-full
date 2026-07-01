// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! PyO3 wrappers for the estimation functions of the Pareto distribution from the `powerlaw` crate.
//! This file provides thin wrappers that call the functionality from the `powerlaw` crate.

use powerlaw::dist::pareto::estimation as rust_estimation;
use pyo3::prelude::*;

/// Python wrapper for the `find_alphas_fast` function.
#[pyfunction]
fn find_alphas_fast(mut data: Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>)> {
    let result = rust_estimation::find_alphas_fast(&mut data);
    Ok(result)
}

/// Python wrapper for the `find_alphas_exhaustive` function.
#[pyfunction]
fn find_alphas_exhaustive(mut data: Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>)> {
    let result = rust_estimation::find_alphas_exhaustive(&mut data);
    Ok(result)
}

/// Python wrapper for the `param_est` function.
#[pyfunction]
fn param_est(data: Vec<f64>, m: usize) -> PyResult<(f64, f64)> {
    let result = rust_estimation::param_est(&data, m);
    Ok(result)
}

/// Creates the 'estimation' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "estimation")?;
    m.add_function(wrap_pyfunction!(find_alphas_fast, &m)?)?;
    m.add_function(wrap_pyfunction!(find_alphas_exhaustive, &m)?)?;
    m.add_function(wrap_pyfunction!(param_est, &m)?)?;
    Ok(m)
}
