use indexmap::IndexMap;
use pyo3::prelude::*;
use pyo3::types::PyList;

/// Groups items by PK hash, preserving insertion order.
/// Returns list of index groups.
#[pyfunction]
pub fn group_by_pk(py: Python<'_>, pks: Vec<PyObject>) -> PyResult<PyObject> {
    let mut groups: IndexMap<u64, Vec<usize>> = IndexMap::new();

    for (idx, pk) in pks.iter().enumerate() {
        let hash = pk.bind(py).hash()? as u64;
        groups.entry(hash).or_default().push(idx);
    }

    let result = PyList::empty(py);
    for (_hash, indices) in &groups {
        let py_indices = PyList::new(py, indices)?;
        result.append(&py_indices)?;
    }

    Ok(result.unbind().into())
}
