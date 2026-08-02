use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyTuple};

/// Convert a dict or list into a hashable tuple for use as dictionary key.
#[pyfunction]
pub fn hash_item(py: Python<'_>, item: &Bound<'_, PyAny>) -> PyResult<PyObject> {
    hash_item_inner(py, item)
}

fn hash_item_inner(py: Python<'_>, item: &Bound<'_, PyAny>) -> PyResult<PyObject> {
    if let Ok(dict) = item.downcast::<PyDict>() {
        let mut items: Vec<(PyObject, PyObject)> = Vec::with_capacity(dict.len());
        for (key, value) in dict.iter() {
            items.push((key.unbind(), value.unbind()));
        }

        // Sort by key using Python's comparison
        items.sort_by(|a, b| {
            let a_key = a.0.bind(py);
            let b_key = b.0.bind(py);
            a_key
                .lt(b_key)
                .and_then(|lt| {
                    if lt {
                        Ok(std::cmp::Ordering::Less)
                    } else {
                        a_key.gt(b_key).map(|gt| {
                            if gt {
                                std::cmp::Ordering::Greater
                            } else {
                                std::cmp::Ordering::Equal
                            }
                        })
                    }
                })
                .unwrap_or(std::cmp::Ordering::Equal)
        });

        let mut result: Vec<PyObject> = Vec::with_capacity(items.len());
        for (key, value) in &items {
            let val_bound = value.bind(py);
            let processed_value =
                if val_bound.is_instance_of::<PyDict>() || val_bound.is_instance_of::<PyList>() {
                    hash_item_inner(py, val_bound)?
                } else {
                    value.clone_ref(py)
                };
            let pair = PyTuple::new(py, &[key.clone_ref(py), processed_value])?;
            result.push(pair.unbind().into());
        }
        let tuple = PyTuple::new(py, &result)?;
        Ok(tuple.unbind().into())
    } else if let Ok(list) = item.downcast::<PyList>() {
        let mut result: Vec<PyObject> = Vec::with_capacity(list.len());
        for (idx, value) in list.iter().enumerate() {
            let processed_value =
                if value.is_instance_of::<PyDict>() || value.is_instance_of::<PyList>() {
                    hash_item_inner(py, &value)?
                } else {
                    value.unbind()
                };
            let idx_obj: PyObject = idx.into_pyobject(py)?.into_any().unbind();
            let pair = PyTuple::new(py, &[idx_obj, processed_value])?;
            result.push(pair.unbind().into());
        }
        let tuple = PyTuple::new(py, &result)?;
        Ok(tuple.unbind().into())
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "hash_item expects a dict or list",
        ))
    }
}
