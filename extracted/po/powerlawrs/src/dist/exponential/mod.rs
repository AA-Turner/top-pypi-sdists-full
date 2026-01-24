// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! PyO3 wrappers for the Exponential distribution from the `powerlaw` crate.
//! This file provides thin wrappers that call the functionality from the `powerlaw` crate.

pub mod estimation;

use crate::dist::pareto::gof::PyParetoFit;
use powerlaw::dist::{exponential::Exponential, Distribution};
use pyo3::prelude::*;

/// A Python-compatible wrapper for the `Exponential` struct from the `powerlaw` crate.
///
/// Creates a new Exponential distribution instance.
///
/// Args:
///     lambda (float): The rate parameter of the distribution. Must be > 0.
///     x_min (float): The minimum value of the distribution (scale parameter). Must be > 0.
/// It does not contain any logic itself, but calls the underlying Rust implementation.
#[pyclass(name = "Exponential")]
struct PyExponential {
    inner: Exponential,
}

#[pymethods]
impl PyExponential {
    /// Creates a new Exponential distribution instance.
    ///
    /// Args:
    ///     lambda (float): The rate parameter of the distribution. Must be > 0.
    #[new]
    fn new(lambda: f64, x_min: f64) -> PyResult<Self> {
        if lambda <= 0.0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "lambda must be positive.",
            ));
        }
        // This creates an instance of the original Exponential struct from the `powerlaw` crate.
        Ok(PyExponential {
            inner: Exponential { lambda, x_min },
        })
    }

    /// Calls the underlying `pdf` method from the `powerlaw` crate.
    #[pyo3(text_signature = "($self, x)")]
    fn pdf(&self, x: f64) -> f64 {
        self.inner.pdf(x)
    }

    /// Calls the underlying `cdf` method from the `powerlaw` crate.
    #[pyo3(text_signature = "($self, x)")]
    fn cdf(&self, x: f64) -> f64 {
        self.inner.cdf(x)
    }

    /// Calls the underlying `ccdf` method from the `powerlaw` crate.
    #[pyo3(text_signature = "($self, x)")]
    fn ccdf(&self, x: f64) -> f64 {
        self.inner.ccdf(x)
    }

    /// Calls the underlying `rv` method from the `powerlaw` crate.
    ///
    /// Args:
    ///     u (float): A random number from a Uniform(0, 1) distribution.
    #[pyo3(text_signature = "($self, u)")]
    fn rv(&self, u: f64) -> f64 {
        self.inner.rv(u)
    }

    /// Calculates the log-likelihood of the data given the distribution. Note: The log likelihoods are not summed.
    #[pyo3(text_signature = "($self, x)")]
    fn loglikelihood(&self, x: Vec<f64>) -> Vec<f64> {
        self.inner.loglikelihood(&x)
    }

    /// Set the name of the distribution
    #[pyo3(text_signature = "($self)")]
    fn name(&self) -> &str {
        self.inner.name()
    }

    /// Fitted distribution parameters
    #[pyo3(text_signature = "($self)")]
    fn parameters(&self) -> Vec<(&'static str, f64)> {
        self.inner.parameters()
    }

    #[staticmethod]
    fn from_fitment(data: Vec<f64>, fitment: &PyParetoFit) -> PyResult<Self> {
        let lam: Result<f64, PyErr> = estimation::lambda_hat(data, fitment.x_min);

        Self::new(lam?, fitment.x_min)
    }

    #[getter]
    fn lambda(&self) -> f64 {
        self.inner.lambda
    }
}

/// Creates the 'exponential' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "exponential")?;
    m.add_class::<PyExponential>()?;
    m.add_submodule(&estimation::create_module(py)?)?;
    Ok(m)
}
