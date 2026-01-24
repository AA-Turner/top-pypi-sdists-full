// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! PyO3 wrappers for the Lognormal distribution from the `powerlaw` crate.
//! This file provides thin wrappers that call the functionality from the `powerlaw` crate.
pub mod estimation;

use crate::dist::pareto::gof::PyParetoFit;
use powerlaw::dist::{lognormal::Lognormal, Distribution};
use pyo3::prelude::*;

/// A Python-compatible wrapper for the `Lognormal` struct from the `powerlaw` crate.
///
/// The Lognormal distribution is a continuous probability distribution of a random variable
/// whose logarithm is normally distributed.
///
/// Args:
///     mu (float): The mean of the underlying normal distribution.
///     sigma (float): The standard deviation of the underlying normal distribution. Must be > 0.
///     x_min (float, optional): The minimum value of the distribution (truncation point). Defaults to 0.0.
///
/// Example:
/// --------
/// .. code-block:: python
///
///    import powerlawrs
///    dist = powerlawrs.dist.lognormal.Lognormal(mu=0.0, sigma=1.0, x_min=1.0)
///    pdf_val = dist.pdf(2.0)
#[pyclass(name = "Lognormal")]
struct PyLognormal {
    inner: Lognormal,
}

#[pymethods]
impl PyLognormal {
    /// Creates a new Lognormal distribution instance.
    ///
    /// Args:
    ///     mu (float): The mean of the underlying normal distribution.
    ///     sigma (float): The standard deviation of the underlying normal distribution. Must be > 0.
    ///     x_min (float, optional): The minimum value of the distribution (truncation point). Defaults to 0.0.
    #[new]
    #[pyo3(signature = (mu, sigma, x_min=0.0))]
    fn new(mu: f64, sigma: f64, x_min: f64) -> PyResult<Self> {
        if sigma <= 0.0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "sigma must be positive.",
            ));
        }
        // This creates an instance of the original Lognormal struct from the `powerlaw` crate.
        Ok(PyLognormal {
            inner: Lognormal { mu, sigma, x_min },
        })
    }

    /// Creates a new Lognormal distribution by fitting it to data using the results of a Pareto fit.
    ///
    /// This method uses the Newton-Raphson method to find the maximum likelihood estimates
    /// for mu and sigma, accounting for the truncation at x_min.
    ///
    /// Args:
    ///     data (list[float]): The dataset to fit.
    ///     fitment (ParetoFit): The result of a previous Pareto fit (used for x_min).
    ///
    /// Returns:
    ///     Lognormal: A new Lognormal instance with fitted parameters.
    #[staticmethod]
    #[pyo3(text_signature = "(data, fitment)")]
    fn from_fitment(data: Vec<f64>, fitment: &PyParetoFit) -> PyResult<Self> {
        let (mu, sigma) = powerlaw::dist::lognormal::estimation::lognormal_mle_truncated_par(
            &data,
            fitment.x_min,
        );
        Ok(PyLognormal {
            inner: Lognormal {
                mu,
                sigma,
                x_min: fitment.x_min,
            },
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

    #[getter]
    fn mu(&self) -> f64 {
        self.inner.mu
    }

    #[getter]
    fn sigma(&self) -> f64 {
        self.inner.sigma
    }

    #[getter]
    fn x_min(&self) -> f64 {
        self.inner.x_min
    }
}

/// Creates the 'lognormal' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "lognormal")?;
    m.add_class::<PyLognormal>()?;
    m.add_submodule(&estimation::create_module(py)?)?;
    Ok(m)
}
