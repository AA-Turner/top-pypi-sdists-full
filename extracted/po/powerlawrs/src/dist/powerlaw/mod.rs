// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! PyO3 wrappers for the generic Power-Law distribution functions from the `powerlaw` crate.
//! This file provides thin wrappers that call the functionality from the `powerlaw` crate.

pub mod estimation;

use powerlaw::dist::{powerlaw::Powerlaw, Distribution};
use pyo3::prelude::*;

/// A Python-compatible wrapper for the `Powerlaw` struct from the `powerlaw` crate.
///
/// Represents a generic Power-Law distribution where the probability density function (PDF) is:
/// f(x) = C * x^(-alpha)
///
/// This simplifies to a Pareto Type I distribution.
/// Note: The `alpha` parameter here is the power-law exponent. It is equal to `1 + alpha_pareto`,
/// where `alpha_pareto` is the shape parameter of the standard Pareto Type I distribution.
///
/// Args:
///     alpha (float): The scaling exponent of the distribution. Must be > 1.
///     x_min (float): The minimum value of the distribution. Must be > 0.
///
/// Example:
/// --------
/// .. code-block:: python
///
///    import powerlawrs
///    # Create a distribution with exponent 2.5 (equivalent to Pareto alpha 1.5)
///    dist = powerlawrs.dist.powerlaw.Powerlaw(alpha=2.5, x_min=1.0)
///    pdf_val = dist.pdf(2.0)
#[pyclass(name = "Powerlaw")]
struct PyPowerlaw {
    inner: Powerlaw,
}

#[pymethods]
impl PyPowerlaw {
    /// Creates a new Powerlaw distribution instance.
    ///
    /// Args:
    ///     alpha (float): The scaling exponent of the distribution. Must be > 1.
    ///     x_min (float): The minimum value of the distribution. Must be > 0.
    #[new]
    fn new(alpha: f64, x_min: f64) -> PyResult<Self> {
        if alpha <= 1.0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "alpha must be greater than 1 for the generic Power-Law distribution.",
            ));
        }
        if x_min <= 0.0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "x_min must be positive.",
            ));
        }
        // This creates an instance of the original Powerlaw struct from the `powerlaw` crate.
        Ok(PyPowerlaw {
            inner: Powerlaw { alpha, x_min },
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

    /// Calculates the log-likelihood of the data given the distribution.  Note: The log likelihoods are not summed.
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

    #[getter]
    fn alpha(&self) -> f64 {
        self.inner.alpha
    }

    #[getter]
    fn x_min(&self) -> f64 {
        self.inner.x_min
    }
}

/// Python wrapper that calls the `alpha_hat` function from the `powerlaw` crate.
///
/// Calculates the maximum likelihood estimate (MLE) for the `alpha` parameter
/// of a generic Power-Law distribution. This returns the power-law exponent (f(x) ~ x^-alpha).
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

/// Creates the 'powerlaw' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "powerlaw")?;
    m.add_function(wrap_pyfunction!(alpha_hat, &m)?)?;
    m.add_class::<PyPowerlaw>()?;
    Ok(m)
}
