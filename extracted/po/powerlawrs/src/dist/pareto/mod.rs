// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! PyO3 wrappers for the Pareto distribution functions from the `powerlaw` crate.

use crate::dist::pareto::gof::PyParetoFit;
use powerlaw::dist::pareto::Pareto;
use powerlaw::dist::Distribution;
use pyo3::prelude::*;

pub mod estimation;
pub mod gof;
pub mod hypothesis;

/// A Python-compatible wrapper for the `Pareto` struct from the `powerlaw` crate.
///
/// Creates a new Pareto Type I distribution instance.
///
/// Args:
///     alpha (float): The shape parameter of the distribution. Must be > 0.
///     x_min (float): The minimum value of the distribution (scale parameter). Must be > 0.
///
/// It does not contain any logic itself, but calls the underlying Rust implementation.
#[pyclass(name = "Pareto")]
struct PyPareto {
    inner: Pareto,
}

#[pymethods]
impl PyPareto {
    /// Creates a new Pareto Type I distribution instance.
    ///
    /// Args:
    ///     alpha (float): The shape parameter of the distribution. Must be > 0.
    ///     x_min (float): The minimum value of the distribution (scale parameter). Must be > 0.
    #[new]
    fn new(alpha: f64, x_min: f64) -> PyResult<Self> {
        if alpha <= 0.0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "alpha must be positive.",
            ));
        }
        if x_min <= 0.0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "x_min must be positive.",
            ));
        }
        // This creates an instance of the original Pareto struct from the `powerlaw` crate.
        Ok(PyPareto {
            inner: Pareto::new(alpha, x_min),
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

    /// Creates a `Pareto` distribution directly from a `Fitment` result.
    ///
    /// This allows for a clean conversion from the results of a goodness-of-fit test
    /// to a concrete distribution instance.
    #[staticmethod]
    fn from_fitment(fitment: &PyParetoFit) -> PyResult<Self> {
        let alpha = fitment.alpha;
        let x_min = fitment.x_min;
        Self::new(alpha, x_min)
    }

    #[getter]
    fn alpha(&self) -> f64 {
        self.inner.alpha
    }

    #[getter]
    fn x_min(&self) -> f64 {
        self.inner.x_min
    }
}

/// Creates the 'pareto' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "pareto")?;
    m.add_class::<PyPareto>()?;
    m.add_submodule(&estimation::create_module(py)?)?;
    m.add_submodule(&gof::create_module(py)?)?;
    m.add_submodule(&hypothesis::create_module(py)?)?;
    Ok(m)
}
