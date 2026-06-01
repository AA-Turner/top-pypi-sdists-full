use pyo3::prelude::*;
use taskchampion::Uuid;
use taskchampion::WorkingSet as TCWorkingSet;

#[pyclass]
pub struct WorkingSet(TCWorkingSet);

#[pyclass]
struct WorkingSetIter {
    ws: Py<WorkingSet>,
    idx: usize,
    largest: usize,
}

#[pymethods]
impl WorkingSetIter {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>) -> Option<(usize, String)> {
        let py = slf.py();
        while slf.idx <= slf.largest {
            let i = slf.idx;
            slf.idx += 1;
            let found = slf.ws.borrow(py).0.by_index(i).map(|u| (i, u.to_string()));
            if found.is_some() {
                return found;
            }
        }
        None
    }
}

#[pymethods]
impl WorkingSet {
    pub fn __len__(&self) -> usize {
        self.0.len()
    }

    pub fn __repr__(&self) -> String {
        format!(
            "WorkingSet(len={}, largest_index={})",
            self.0.len(),
            self.0.largest_index(),
        )
    }

    pub fn largest_index(&self) -> usize {
        self.0.largest_index()
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn by_index(&self, index: usize) -> Option<String> {
        self.0.by_index(index).map(|uuid| uuid.into())
    }

    pub fn by_uuid(&self, uuid: String) -> PyResult<Option<usize>> {
        let u = Uuid::parse_str(&uuid)
            .map_err(|_| pyo3::exceptions::PyValueError::new_err("Invalid UUID"))?;
        Ok(self.0.by_uuid(u))
    }

    fn __iter__(slf: Bound<'_, Self>) -> PyResult<Py<WorkingSetIter>> {
        let py = slf.py();
        let largest = slf.borrow().0.largest_index();
        let iter = WorkingSetIter {
            ws: slf.unbind(),
            idx: 0,
            largest,
        };
        Py::new(py, iter)
    }
}

impl AsRef<TCWorkingSet> for WorkingSet {
    fn as_ref(&self) -> &TCWorkingSet {
        &self.0
    }
}

impl From<TCWorkingSet> for WorkingSet {
    fn from(value: TCWorkingSet) -> Self {
        WorkingSet(value)
    }
}

impl From<WorkingSet> for TCWorkingSet {
    fn from(value: WorkingSet) -> Self {
        value.0
    }
}
