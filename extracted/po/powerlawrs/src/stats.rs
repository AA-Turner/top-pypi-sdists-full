// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! Module to aid in statistical inference. Contains functions for basic descriptive statistics, non parametric methods for comparing distributions etc.

/// A collection of descriptive statistics, mean, variance etc.
pub mod descriptive {
    use powerlaw::stats;
    use pyo3::prelude::*;

    /// Calculates the arithmetic mean of a vector.
    ///
    /// Example
    /// -------
    /// .. code-block:: python
    ///
    ///    import powerlawrs
    ///
    ///    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    ///    mu = powerlawrs.stats.descriptive.mean(data)
    ///    # mu is 3.0
    #[pyfunction]
    fn mean(data: Vec<f64>) -> PyResult<f64> {
        let mu = stats::descriptive::mean(&data);
        Ok(mu)
    }

    /// Calculates the variance of a vector where ``ddof`` = degrees of freedom. If ``ddof=1``, the sample variance is returned otherwise the population variance is returned.
    ///
    /// Example
    /// -------
    /// .. code-block:: python
    ///
    ///    import powerlawrs
    ///
    ///    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    ///    # Population variance (ddof=0)
    ///    sigma_sq_pop = powerlawrs.stats.descriptive.variance(data, 0)
    ///    # sigma_sq_pop is 2.0
    ///
    ///    # Sample variance (ddof=1)
    ///    sigma_sq_samp = powerlawrs.stats.descriptive.variance(data, 1)
    ///    # sigma_sq_samp is 2.5
    #[pyfunction]
    fn variance(data: Vec<f64>, ddof: u8) -> PyResult<f64> {
        let sigma2 = stats::descriptive::variance(&data, ddof);
        Ok(sigma2)
    }

    /// Creates the 'mean' submodule
    pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
        // Create a new Python submodule
        let m = PyModule::new(py, "descriptive")?;

        // Add the wrapped function to the submodule
        m.add_function(wrap_pyfunction!(mean, &m)?)?;
        m.add_function(wrap_pyfunction!(variance, &m)?)?;

        Ok(m)
    }
}

/// Functions in support of randomization.
pub mod random {
    use powerlaw::stats;
    use pyo3::prelude::*;

    /// Sample ``n`` elements with probability U(0,1) with replacement.
    ///
    /// Example
    /// -------
    /// .. code-block:: python
    ///
    ///    import powerlawrs
    ///
    ///    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    ///    # Get 10 random samples from data with replacement
    ///    samples = powerlawrs.stats.random.random_choice(data, 10)
    ///    # len(samples) will be 10
    #[pyfunction]
    fn random_choice(data: Vec<f64>, size: usize) -> PyResult<Vec<f64>> {
        let samp = stats::random::random_choice(&data, size);
        Ok(samp)
    }

    /// Generate ``n`` random variates from U(0,1).
    #[pyfunction]
    fn random_uniform(n: usize) -> PyResult<Vec<f64>> {
        let u = stats::random::random_uniform(n);
        Ok(u)
    }

    /// Creates the 'mean' submodule
    pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
        // Create a new Python submodule
        let m = PyModule::new(py, "random")?;

        // Add the wrapped function to the submodule
        m.add_function(wrap_pyfunction!(random_choice, &m)?)?;
        m.add_function(wrap_pyfunction!(random_uniform, &m)?)?;

        Ok(m)
    }
}

/// Supporting functions for Kolmogorov–Smirnov testing for similarity between empirical and reference cumulative distribution functions.
/// Given this function is called iteratively over the data during the goodness of fit portion in [crate::dist::pareto::gof()], it requires the observed data to be sorted.
/// Thank you @Google Gemini for helping with handling Rust generics to Python.
pub mod ks {
    use pyo3::exceptions::{PyTypeError, PyValueError};
    use pyo3::prelude::*;

    /// The D+ statistic measures the largest amount by which the ECDF is above the theoretical CDF.
    fn compute_dplus(cdfvals: &[f64], n: usize) -> f64 {
        (1..=n)
            .map(|i| i as f64 / n as f64 - cdfvals[i - 1])
            .fold(f64::MIN, f64::max)
    }

    /// The D- statistic measures the largest amount by which the ECDF is below the theoretical CDF.
    fn compute_dminus(cdfvals: &[f64], n: usize) -> f64 {
        /*
        Computes D- as used in the Kolmogorov-Smirnov test.
        ...
        */
        (0..n)
            .map(|i| cdfvals[i] - i as f64 / n as f64)
            .fold(f64::MIN, f64::max)
    }

    /// 1 sample KS test based on a known cdf.
    ///
    /// Args:
    ///     sorted_x (list[float]): A list of data points, pre-sorted in ascending order.
    ///     cdf_func (callable): A Python function (or lambda) that takes a single float
    ///         (x) and returns its cumulative probability F(x) as a float.
    ///
    /// Returns:
    ///     tuple[float, float, float]: A tuple containing (D+, D-, D).
    ///
    /// Raises:
    ///     ValueError: If the list is empty.
    ///     TypeError: If the cdf_func does not return a float.
    ///     (Any exception): Any exception raised by the cdf_func will be propagated.
    #[pyfunction]
    fn ks_1sam_sorted(
        py: Python<'_>,
        sorted_x: Vec<f64>,
        cdf_func: Py<PyAny>,
    ) -> PyResult<(f64, f64, f64)> {
        let n = sorted_x.len();
        if n == 0 {
            // Return a Python-style error, not a (0,0,0) tuple
            return Err(PyValueError::new_err(
                "Input list 'sorted_x' cannot be empty.",
            ));
        }

        // This is the logic from your original function, but now
        // it can properly handle Python errors.
        let mut cdfvals: Vec<f64> = Vec::with_capacity(n);

        for &x in sorted_x.iter() {
            // 1. Create Python arguments (a 1-element tuple)
            let args = (x,);

            // 2. Call the user's Python function
            // The '?' will propagate any exception (e.g., ValueError, ZeroDivisionError)
            let cdf_val_py = cdf_func.call1(py, args)?;

            // 3. Extract the Python float result back to a Rust f64
            // The '?' will propagate a TypeError if the user returned None, a string, etc.
            let cdf_val: f64 = cdf_val_py
                .extract(py)
                .map_err(|_| PyTypeError::new_err("cdf_func must return a float"))?;

            cdfvals.push(cdf_val);
        }

        // The rest of the logic is the same
        let dplus = compute_dplus(&cdfvals, n);
        let dminus = compute_dminus(&cdfvals, n);
        let d = dplus.max(dminus);

        Ok((dplus, dminus, d))
    }

    /// Creates the 'ks' Python submodule
    pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
        // This module will be named 'ks' in Python
        let m = PyModule::new(py, "ks")?;

        // Add the wrapper function to the module
        m.add_function(wrap_pyfunction!(ks_1sam_sorted, &m)?)?;

        Ok(m)
    }
}

pub mod compare {
    use powerlaw::stats;
    use pyo3::prelude::*;

    /// Performs Vuong's likelihood ratio test to compare two non-nested distributions.
    ///
    /// This test determines if one distribution provides a significantly better fit
    /// to the data than another.
    ///
    /// Args:
    ///     dist1 (list[float]): The first distribution's data points (e.g., log-likelihoods).
    ///     dist2 (list[float]): The second distribution's data points (e.g., log-likelihoods).
    ///
    /// Returns:
    ///     tuple[float, float]: A tuple containing the Z-score and the p-value.
    ///     A positive Z-score indicates that the first distribution is a better fit,
    ///     while a negative Z-score indicates the second is better. The p-value
    ///     indicates the statistical significance of the result.
    ///
    /// Example
    /// -------
    /// .. code-block:: python
    ///
    ///    import powerlawrs
    ///    import numpy as np
    ///
    ///    # Assume dist1_ll and dist2_ll are arrays of log-likelihoods
    ///    # for two different models on the same data.
    ///    dist1_ll = np.random.normal(loc=0.5, scale=1.0, size=100).tolist()
    ///    dist2_ll = np.random.normal(loc=0.2, scale=1.0, size=100).tolist()
    ///
    ///    z, p_value = powerlawrs.stats.compare.vuongs_test(dist1_ll, dist2_ll)
    ///    print(f"Z-score: {z}, P-value: {p_value}")
    ///    # If z > 0 and p_value < 0.05, then dist1 is a significantly better fit.
    #[pyfunction]
    pub fn vuongs_test(dist1: Vec<f64>, dist2: Vec<f64>) -> (f64, f64) {
        let (z, p_value) = stats::compare::vuongs_test(&dist1, &dist2);
        (z, p_value)
    }

    /// create the "compare" sub module
    pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
        let m = PyModule::new(py, "compare")?;
        m.add_function(wrap_pyfunction!(vuongs_test, &m)?)?;
        Ok(m)
    }
}
