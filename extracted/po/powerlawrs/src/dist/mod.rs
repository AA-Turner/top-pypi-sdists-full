// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

//! A submodule for wrapping the distribution-related functionalities from the `powerlaw` crate.

use pyo3::prelude::*;

pub mod exponential;
pub mod lognormal;
pub mod pareto;
pub mod powerlaw;

/// Creates the 'dist' Python submodule.
pub fn create_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "dist")?;
    m.add_submodule(&pareto::create_module(py)?)?;
    m.add_submodule(&powerlaw::create_module(py)?)?;
    m.add_submodule(&exponential::create_module(py)?)?;
    m.add_submodule(&lognormal::create_module(py)?)?;
    Ok(m)
}
