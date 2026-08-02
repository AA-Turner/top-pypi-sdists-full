use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Splits the list of '__'-separated strings and converts them to a nested dict.
#[pyfunction]
#[pyo3(signature = (list_to_trans, default=None))]
pub fn translate_list_to_dict(
    py: Python<'_>,
    list_to_trans: Vec<String>,
    default: Option<PyObject>,
) -> PyResult<PyObject> {
    let ellipsis = py.Ellipsis();
    let default_obj = default.unwrap_or_else(|| ellipsis.clone_ref(py));

    let is_ellipsis = default_obj.bind(py).is(&ellipsis);

    let new_dict = PyDict::new(py);

    for path in &list_to_trans {
        let parts: Vec<&str> = path.split("__").collect();
        let mut current_level = new_dict.clone();

        let def_val = if is_ellipsis {
            default_obj.clone_ref(py)
        } else {
            let copy_mod = py.import("copy")?;
            copy_mod.call_method1("deepcopy", (&default_obj,))?.unbind()
        };

        for (ind, part) in parts.iter().enumerate() {
            let is_last = ind == parts.len() - 1;

            let has_key = current_level.contains(*part)?;

            if has_key {
                let existing = current_level.get_item(*part)?.unwrap();
                if !is_last && existing.downcast::<PyDict>().is_err() {
                    let empty = PyDict::new(py);
                    current_level.set_item(*part, &empty)?;
                    current_level = empty;
                } else if is_last {
                    break;
                } else {
                    current_level = existing.downcast_into::<PyDict>()?;
                }
            } else if is_last {
                current_level.set_item(*part, &def_val)?;
                break;
            } else {
                let empty = PyDict::new(py);
                current_level.set_item(*part, &empty)?;
                current_level = empty;
            }
        }
    }

    Ok(new_dict.into())
}
