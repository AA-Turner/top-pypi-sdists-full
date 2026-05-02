use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict, PyModule};
use cfn_guard::{run_checks, ValidateInput};

/// Placeholder validate function; will be wired to Guard later.
#[pyfunction]
#[pyo3(signature = (template_content, rules=None, verbose=false))]
fn validate_with_guard(py: Python<'_>, template_content: &str, rules: Option<&str>, verbose: bool) -> PyResult<PyObject> {
    let result = PyDict::new_bound(py);
    result.set_item("tool", "guard")?;

    let rules_str = match rules {
        Some(r) if !r.trim().is_empty() => r,
        _ => {
            result.set_item("success", false)?;
            result.set_item("error", "rules is required and must be non-empty")?;
            return Ok(result.into_py(py));
        }
    };

    let data_in = ValidateInput { content: template_content, file_name: "DATA_STDIN" };
    let rules_in = ValidateInput { content: rules_str, file_name: "RULES_STDIN" };

    match run_checks(data_in, rules_in, verbose) {
        Ok(json_str) => {
            // Prefer structured JSON from guard; parse into Python object
            let json_loads = py.import_bound("json")?.getattr("loads")?;
            match json_loads.call1((json_str.as_str(),)) {
                Ok(py_obj) => {
                    result.set_item("success", true)?;
                    result.set_item("result", py_obj)?;
                }
                Err(_) => {
                    // If not JSON (e.g., verbose tree), return raw string
                    result.set_item("success", true)?;
                    result.set_item("result", json_str)?;
                }
            }
        }
        Err(e) => {
            result.set_item("success", false)?;
            result.set_item("error", format!("{}", e))?;
        }
    }

    Ok(result.into_py(py))
}

/// Python module definition
#[pymodule]
fn guardpycfn(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction_bound!(validate_with_guard, m)?)?;
    Ok(())
}

