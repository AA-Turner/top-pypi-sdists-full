use pyo3::prelude::*;

pub mod linreg;

/// Root level function (if you want any)
#[pyfunction]
pub fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

// Register functions that should be at the root level
pub fn register_root_functions(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}




// use pyo3::prelude::*;

// // Declare submodules (uncomment when you create them)
// // pub mod linreg;
// // pub mod mixed_effects;

// /// Formats the sum of two numbers as string.
// #[pyfunction]
// pub fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
//     Ok((a + b).to_string())
// }

// // This function registers all functions from the models module and its submodules
// pub fn register_models(m: &Bound<'_, PyModule>) -> PyResult<()> {
//     // Register functions from this module
//     m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    
//     // Register submodules (uncomment when you create them)
//     // linreg::register_linreg(m)?;
//     // mixed_effects::register_mixed_effects(m)?;
    
//     Ok(())
// }