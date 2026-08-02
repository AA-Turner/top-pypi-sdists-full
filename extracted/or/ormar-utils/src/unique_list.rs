use pyo3::prelude::*;
use pyo3::types::PyList;
use std::collections::HashSet;

/// A list that prevents duplicates using hash-based O(1) lookups.
#[pyclass]
pub struct UniqueList {
    items: Vec<PyObject>,
    seen: HashSet<u64>,
}

#[pymethods]
impl UniqueList {
    #[new]
    #[pyo3(signature = (initial=None))]
    fn new(py: Python<'_>, initial: Option<&Bound<'_, PyList>>) -> PyResult<Self> {
        let mut list = UniqueList {
            items: Vec::new(),
            seen: HashSet::new(),
        };
        if let Some(init) = initial {
            for item in init.iter() {
                list.append(py, item.unbind())?;
            }
        }
        Ok(list)
    }

    fn append(&mut self, py: Python<'_>, item: PyObject) -> PyResult<()> {
        let hash = item.bind(py).hash()? as u64;
        if self.seen.insert(hash) {
            self.items.push(item);
        }
        Ok(())
    }

    fn to_list(&self, py: Python<'_>) -> PyResult<PyObject> {
        let list = PyList::new(py, self.items.iter().map(|x| x.bind(py)))?;
        Ok(list.unbind().into())
    }

    fn __len__(&self) -> usize {
        self.items.len()
    }

    fn __getitem__(&self, py: Python<'_>, idx: isize) -> PyResult<PyObject> {
        let len = self.items.len() as isize;
        let actual_idx = if idx < 0 { len + idx } else { idx };
        if actual_idx < 0 || actual_idx >= len {
            return Err(pyo3::exceptions::PyIndexError::new_err(
                "list index out of range",
            ));
        }
        Ok(self.items[actual_idx as usize].clone_ref(py))
    }

    fn __contains__(&self, _py: Python<'_>, item: &Bound<'_, PyAny>) -> PyResult<bool> {
        let hash = item.hash()? as u64;
        Ok(self.seen.contains(&hash))
    }

    fn __iter__(&self, py: Python<'_>) -> PyResult<PyObject> {
        let list = self.to_list(py)?;
        list.bind(py).call_method0("__iter__").map(|x| x.unbind())
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        let list = self.to_list(py)?;
        let repr = list.bind(py).repr()?;
        Ok(format!("UniqueList({})", repr))
    }

    fn __bool__(&self) -> bool {
        !self.items.is_empty()
    }
}
