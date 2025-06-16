// src/concurrency.rs

use std::sync::{Arc, RwLock};
use pyo3::prelude::*;
use numpy::{PyReadonlyArray1, PyReadonlyArray2};
use crate::index::AnnIndex;
use crate::metrics::Distance;

/// Python‐visible thread‐safe ANN index.
#[pyclass]
pub struct ThreadSafeAnnIndex {
    inner: Arc<RwLock<AnnIndex>>,
}

#[pymethods]
impl ThreadSafeAnnIndex {
    #[new]
    pub fn new(dim: usize, metric: Distance) -> PyResult<Self> {
        let idx = AnnIndex::new(dim, metric)?;
        Ok(ThreadSafeAnnIndex { inner: Arc::new(RwLock::new(idx)) })
    }

    pub fn add(&self, py: Python, data: PyReadonlyArray2<f32>, ids: PyReadonlyArray1<i64>)
        -> PyResult<()>
    {
        // Acquire write lock then call under GIL
        let mut guard = self.inner.write().unwrap();
        guard.add(py, data, ids)
    }

    pub fn remove(&self, _py: Python, ids: Vec<i64>) -> PyResult<()> {
        let mut guard = self.inner.write().unwrap();
        guard.remove(ids)
    }

    pub fn search(&self, py: Python, query: PyReadonlyArray1<f32>, k: usize)
        -> PyResult<(PyObject, PyObject)>
    {
        let guard = self.inner.read().unwrap();
        guard.search(py, query, k)
    }

    pub fn search_batch(&self, py: Python, data: PyReadonlyArray2<f32>, k: usize)
        -> PyResult<(PyObject, PyObject)>
    {
        let guard = self.inner.read().unwrap();
        guard.search_batch(py, data, k)
    }

    pub fn save(&self, _py: Python, path: &str) -> PyResult<()> {
        let guard = self.inner.read().unwrap();
        guard.save(path)
    }

    #[staticmethod]
    pub fn load(_py: Python, path: &str) -> PyResult<Self> {
        let idx = AnnIndex::load(path)?;
        Ok(ThreadSafeAnnIndex { inner: Arc::new(RwLock::new(idx)) })
    }
}
