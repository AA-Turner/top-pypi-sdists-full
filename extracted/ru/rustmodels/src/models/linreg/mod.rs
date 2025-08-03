use pyo3::prelude::*;

// ---------- Import submodules ----------

use super::utils::formula_utils;

// ---------- Linreg module functions ----------

// REMEMBER: If possible, use GPU for speed

/// Function that fits and returns a linear regression.
///
/// Args:
/// - `formula` (string): Formula for the regression taking place. This will use the R formula syntax, and will use a 'formula' object.
/// - `df` (polars DataFrame): A DataFrame containing the data to fit the model. It will be used in conjunction with the formula.
///
/// Returns:
/// - A 'linreg' object.
#[pyfunction]
pub fn fit_linear_regression(formula: &str, _df: PyObject) -> PyResult<String> {
    // Steps:
    // 1. Parse the formula to identify dependent and independent variables.  - Use _parse_formula
    println!("{:#?}", formula_utils::parse_formula(formula)?);
    // 2. Extract the relevant columns from the DataFrame and create the model matrices.                - Use _get_data_columns
    // 3. Perform the linear regression using matrix operations.                                        - Use _linear_regression
    // 4. Return the results as a 'linreg' object.                                                      - Use _create_linreg_result_object
    Ok("hey!".to_string())
}

/// Internal function to create the linreg submodule. Should be run in src/lib.rs.
pub fn _create_linreg_module(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "linreg")?;
    m.add_function(wrap_pyfunction!(fit_linear_regression, &m)?)?;
    Ok(m)
}

// ---------- Linreg module struct ----------

// struct linreg {

// }


