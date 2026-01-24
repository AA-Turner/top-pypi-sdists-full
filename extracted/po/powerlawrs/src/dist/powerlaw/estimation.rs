// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! PyO3 wrappers for the estimation functions of the Powerlaw distribution from the `powerlaw` crate.
//! This file provides thin wrappers that call the functionality from the `powerlaw` crate.

use powerlaw::dist::powerlaw::estimation as rust_estimation;
use pyo3::prelude::*;

/// Python wrapper for the `alpha_hat` function.
#[pyfunction]
fn alpha_hat(data: Vec<f64>, x_min: f64) -> PyResult<f64> {
    if x_min <= 0.0 {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "x_min must be positive.",
        ));
    }
    let result = powerlaw::dist::powerlaw::alpha_hat(&data, x_min);
    Ok(result)
}

/// Creates the 'estimation' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "estimation")?;
    m.add_function(wrap_pyfunction!(alpha_hat, &m)?)?;
    Ok(m)
}
