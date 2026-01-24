// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! PyO3 wrappers for the goodness-of-fit functions of the Pareto distribution from the `powerlaw` crate.
//! This file provides thin wrappers that call the functionality from the `powerlaw` crate.

use powerlaw::dist::pareto::gof as rust_gof;
use powerlaw::dist::pareto::gof::ParetoFit;
use pyo3::prelude::*;

/// A Python-compatible wrapper for the `Fitment` struct.
/// It holds the results of a goodness-of-fit test.
#[pyclass(name = "ParetoFit")]
pub struct PyParetoFit {
    #[pyo3(get)]
    pub x_min: f64,
    #[pyo3(get)]
    pub alpha: f64,
    #[pyo3(get, name = "D")]
    pub d: f64,
    #[pyo3(get)]
    pub len_tail: usize,
}

#[pymethods]
impl PyParetoFit {
    #[new]
    fn new(x_min: f64, alpha: f64, d: f64, len_tail: usize) -> Self {
        PyParetoFit {
            x_min,
            alpha,
            d,
            len_tail,
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "ParetoFit(x_min={}, alpha={}, D={}, len_tail={})",
            self.x_min, self.alpha, self.d, self.len_tail
        )
    }
}

/// Converts a Rust `Fitment` struct to a Python `PyFitment` object.
impl From<ParetoFit> for PyParetoFit {
    fn from(fit: ParetoFit) -> Self {
        PyParetoFit {
            x_min: fit.x_min,
            alpha: fit.alpha,
            d: fit.d,
            len_tail: fit.len_tail,
        }
    }
}

/// Python wrapper for the `gof` (goodness-of-fit) function.
#[pyfunction]
fn gof(data: Vec<f64>, x_mins: Vec<f64>, alphas: Vec<f64>) -> PyResult<PyParetoFit> {
    let result = rust_gof::gof(&data, &x_mins, &alphas);
    Ok(result.into())
}

/// Creates the 'gof' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "gof")?;
    m.add_function(wrap_pyfunction!(gof, &m)?)?;
    m.add_class::<PyParetoFit>()?;
    Ok(m)
}
