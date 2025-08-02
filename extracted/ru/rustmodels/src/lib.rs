use pyo3::prelude::*;

// Import the submodules
mod models;

/// A Python module implemented in Rust.
#[pymodule]
fn rustmodels(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add the linreg submodule
    m.add_submodule(&models::linreg::create_linreg_module(m.py())?)?;
    
    // Add other functions to the root module if needed
    models::register_root_functions(m)?;
    
    Ok(())
}
