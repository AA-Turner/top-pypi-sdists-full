// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! Module and its submodules containing various helper functions primarily around generating synthetic datasets.

use powerlaw::util;
use pyo3::prelude::*;

/// Returns ``n`` quantity of evenly spaced numbers over a specified interval. Motivated by numpy's `linspace <https://numpy.org/doc/stable/reference/generated/numpy.linspace.html>`_.
///
/// Example
/// -------
/// .. code-block:: python
///
///    import powerlawrs
///
///    numbers = powerlawrs.util.linspace(0.0, 1.0, 5)
///    # numbers is [0.0, 0.25, 0.5, 0.75, 1.0]
#[pyfunction]
pub fn linspace(start: f64, end: f64, n: usize) -> PyResult<Vec<f64>> {
    let set = util::linspace(start, end, n);
    Ok(set)
}

/// Computes the error function of `x`, often denoted as `erf(x)`.
///
/// The error function is a special function of sigmoid shape that occurs in probability,
/// statistics, and partial differential equations. It is defined as:
///
/// .. math::
///    \\mathrm{erf}(x) = \\frac{2}{\\sqrt{\\pi}} \\int_0^x e^{-t^2}\\,dt
///
/// Example
/// -------
/// .. code-block:: python
///
///    import powerlawrs
///
///    result = powerlawrs.util.erf(0.0)
///    # result is 0.0
///    result = powerlawrs.util.erf(1.0)
///    # result is approx 0.8427
#[pyfunction]
pub fn erf(x: f64) -> f64 {
    util::erf(x)
}

/// Creates the 'util' Python submodule
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "util")?;
    m.add_function(wrap_pyfunction!(linspace, &m)?)?;
    m.add_function(wrap_pyfunction!(erf, &m)?)?;

    Ok(m)
}

/// Module for handling simulation related tasks such as identifying recommended parameters and generating synthetic datasets.
pub mod sim {
    use powerlaw::util::sim;
    use pyo3::prelude::*;
    use pyo3::types::PyDict; // Import PyDict

    /// Calculates the number of simulations, number of samples per sim, the size of the tail given a predetermined x_min, and calculate the probability of the tail event.
    /// The methodology is based on what is proposed in Section 4.1 of Clauset, Aaron, et al. ‘Power-Law Distributions in Empirical Data’.
    /// SIAM Review, vol. 51, no. 4, Society for Industrial & Applied Mathematics (SIAM), Nov. 2009, pp. 661–703, [doi:10.48550/ARXIV.0706.1062](https://doi.org/10.48550/arXiv.0706.1062).
    /// Where the number of simulations required for the desired level of precision in the estimate is: 1/4 * prec^(-2). Ex. 1/4 * 0.01^(-2) = 2500 sims gives accuracy within 0.01
    #[pyfunction]
    fn calculate_sim_params(
        py: Python<'_>,
        prec: f64,
        data: Vec<f64>,
        x_min: f64,
    ) -> PyResult<Py<PyAny>> {
        let params = sim::calculate_sim_params(&prec, &data, &x_min);
        let dict = PyDict::new(py);

        dict.set_item("num_sims_m", params.num_sims_m)?;
        dict.set_item("sim_len_n", params.sim_len_n)?;
        dict.set_item("n_tail", params.n_tail)?;
        dict.set_item("p_tail", params.p_tail)?;

        Ok(dict.into())
    }

    #[pyclass]
    #[derive(Clone)]
    struct PySimParams {
        #[pyo3(get, set)]
        pub num_sims_m: usize,
        #[pyo3(get, set)]
        pub sim_len_n: usize,
        #[pyo3(get, set)]
        pub n_tail: usize,
        #[pyo3(get, set)]
        pub p_tail: f64,
    }

    #[pymethods]
    impl PySimParams {
        #[new]
        fn new(num_sims_m: usize, sim_len_n: usize, n_tail: usize, p_tail: f64) -> Self {
            Self {
                num_sims_m,
                sim_len_n,
                n_tail,
                p_tail,
            }
        }
    }

    // Implement conversion from python class to the powerlaw struct
    impl From<&PySimParams> for sim::SimParams {
        fn from(params: &PySimParams) -> Self {
            sim::SimParams {
                num_sims_m: params.num_sims_m,
                sim_len_n: params.sim_len_n,
                n_tail: params.n_tail,
                p_tail: params.p_tail,
            }
        }
    }

    /// Generates multiple synthetic datasets using a hybrid model based on the input data and a proposed Pareto Type I fit. This process is fully parallelized,
    /// with M simulations running concurrently on separate threads.
    ///
    /// Each simulated dataset (of size 'n') is constructed by mixing two sampling mechanisms:
    /// 1. Sampling from the 'lower' part of the original data (where x < x_min).
    /// 2. Sampling from a Pareto Type I distribution (defined by x_min and alpha).
    ///
    /// The probability of selecting the Pareto tail is controlled by 'p_tail'.
    ///
    ///This approach is commonly used in bootstrapping or simulation studies for extreme value analysis.
    #[pyfunction]
    fn generate_synthetic_datasets(
        data: Vec<f64>,
        x_min: f64,
        sim_params: &PySimParams, // Accepts an instance of your pyclass
        alpha: f64,
    ) -> PyResult<Vec<Vec<f64>>> {
        // Convert from local class (&PySimParams) into the external struct (sim::SimParams). #TODO this may have major performance
        // implications vs being called directly from powerlaw::dist::pareto::gof
        let powerlaw_params = sim::SimParams::from(sim_params);

        let result = sim::generate_synthetic_datasets(&data, alpha, x_min, powerlaw_params);

        Ok(result)
    }

    /// Creates the 'sim' Python submodule
    pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
        let m = PyModule::new(py, "sim")?;
        m.add_function(wrap_pyfunction!(calculate_sim_params, &m)?)?;
        m.add_function(wrap_pyfunction!(generate_synthetic_datasets, &m)?)?;
        m.add_class::<PySimParams>()?;

        Ok(m)
    }
}
