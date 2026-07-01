// Copyright (c) 2025 Adam Ulichny
//
// This source code is licensed under the MIT OR Apache-2.0 license
// that can be found in the LICENSE-MIT or LICENSE-APACHE files
// at the root of this source tree.

use pyo3::prelude::*;

pub mod dist;
pub mod stats;
pub mod util;

/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name = "_powerlawrs")]
fn _powerlawrs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Create the stats submodule
    let stats_module = PyModule::new(m.py(), "stats")?;
    stats_module.add_submodule(&stats::descriptive::create_module(m.py())?)?;
    stats_module.add_submodule(&stats::random::create_module(m.py())?)?;
    stats_module.add_submodule(&stats::ks::create_module(m.py())?)?;
    stats_module.add_submodule(&stats::compare::create_module(m.py())?)?;
    m.add_submodule(&stats_module)?;

    // Create the util submodule
    let util_module = util::create_module(m.py())?;
    util_module.add_submodule(&util::sim::create_module(m.py())?)?;
    m.add_submodule(&util_module)?;

    // Add the dist submodule
    m.add_submodule(&dist::create_module(m.py())?)?;

    Ok(())
}
