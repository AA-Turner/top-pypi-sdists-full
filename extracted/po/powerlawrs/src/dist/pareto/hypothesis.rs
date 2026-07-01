// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! PyO3 wrappers for the hypothesis testing functions of the Pareto distribution from the `powerlaw` crate.
//! This file provides thin wrappers that call the functionality from the `powerlaw` crate.

use powerlaw::dist::pareto::hypothesis as rust_hypothesis;
use powerlaw::dist::pareto::hypothesis::H0;
use pyo3::prelude::*;

/// A Python-compatible wrapper for the `H0` (null hypothesis) struct.
/// It holds the results of a hypothesis test.
#[pyclass(name = "H0")]
struct PyH0 {
    #[pyo3(get)]
    gt: usize,
    #[pyo3(get)]
    total: usize,
    #[pyo3(get)]
    pval: f64,
}

#[pymethods]
impl PyH0 {
    #[new]
    fn new(gt: usize, total: usize, pval: f64) -> Self {
        PyH0 { gt, total, pval }
    }

    fn __repr__(&self) -> String {
        format!(
            "H0(p_value={}, gt={}, total_sims={})",
            self.pval, self.gt, self.total
        )
    }
}

/// Converts a Rust `H0` struct to a Python `PyH0` object.
impl From<H0> for PyH0 {
    fn from(h0: H0) -> Self {
        PyH0 {
            gt: h0.gt,
            total: h0.total,
            pval: h0.pval,
        }
    }
}

/// Python wrapper for the `hypothesis_test` function.
#[pyfunction]
fn hypothesis_test(
    data: Vec<f64>,
    prec: f64,
    alpha: f64,
    x_min: f64,
    best_d: f64,
) -> PyResult<PyH0> {
    let result = rust_hypothesis::hypothesis_test(&data, prec, alpha, x_min, best_d);
    Ok(result.into())
}

/// Creates the 'hypothesis' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "hypothesis")?;
    m.add_function(wrap_pyfunction!(hypothesis_test, &m)?)?;
    m.add_class::<PyH0>()?;
    Ok(m)
}
