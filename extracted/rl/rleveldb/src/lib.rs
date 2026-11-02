#![allow(dead_code)]

mod snappy;
mod varint;
mod types;
mod ldb_file;
mod log_file;
mod manifest;
mod db;

use pyo3::prelude::*;
use pyo3::types::PyBytes;
use std::path::Path;

#[pyclass(eq, eq_int)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum KeyState {
    Deleted = 0,
    Live = 1,
    Unknown = 2,
}

impl From<types::KeyState> for KeyState {
    fn from(ks: types::KeyState) -> Self {
        match ks {
            types::KeyState::Deleted => KeyState::Deleted,
            types::KeyState::Live => KeyState::Live,
            types::KeyState::Unknown => KeyState::Unknown,
        }
    }
}

#[pyclass(eq, eq_int)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FileType {
    Ldb = 1,
    Log = 2,
}

impl From<types::FileType> for FileType {
    fn from(ft: types::FileType) -> Self {
        match ft {
            types::FileType::Ldb => FileType::Ldb,
            types::FileType::Log => FileType::Log,
        }
    }
}

#[pyclass]
pub struct Record {
    inner: types::Record,
}

#[pymethods]
impl Record {
    #[getter]
    fn key<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        PyBytes::new(py, &self.inner.key)
    }

    #[getter]
    fn value<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        PyBytes::new(py, &self.inner.value)
    }

    #[getter]
    fn seq(&self) -> u64 {
        self.inner.seq
    }

    #[getter]
    fn state(&self) -> KeyState {
        self.inner.state.into()
    }

    #[getter]
    fn file_type(&self) -> FileType {
        self.inner.file_type.into()
    }

    #[getter]
    fn origin_file(&self) -> String {
        self.inner.origin_file.to_string_lossy().to_string()
    }

    #[getter]
    fn offset(&self) -> u64 {
        self.inner.offset
    }

    #[getter]
    fn was_compressed(&self) -> bool {
        self.inner.was_compressed
    }

    #[getter]
    fn user_key<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        PyBytes::new(py, self.inner.user_key())
    }

    fn __repr__(&self) -> String {
        format!(
            "Record(key=<{} bytes>, value=<{} bytes>, seq={}, state={:?}, file_type={:?})",
            self.inner.key.len(),
            self.inner.value.len(),
            self.inner.seq,
            self.inner.state,
            self.inner.file_type,
        )
    }
}

#[pyclass]
pub struct RawLevelDb {
    inner: Option<db::RawLevelDb>,
}

#[pymethods]
impl RawLevelDb {
    #[new]
    fn new(in_dir: &str) -> PyResult<Self> {
        let db = db::RawLevelDb::open(Path::new(in_dir))
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
        Ok(Self { inner: Some(db) })
    }

    #[pyo3(signature = (*, reverse = false))]
    fn iterate_records_raw(&self, reverse: bool) -> PyResult<Vec<Record>> {
        let db = self.inner.as_ref()
            .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err("Database is closed"))?;
        Ok(db.iterate_records_raw(reverse)
            .into_iter()
            .map(|r| Record { inner: r })
            .collect())
    }

    #[getter]
    fn in_dir_path(&self) -> PyResult<String> {
        let db = self.inner.as_ref()
            .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err("Database is closed"))?;
        Ok(db.in_dir_path().to_string_lossy().to_string())
    }

    fn close(&mut self) {
        self.inner = None;
    }

    fn __enter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __exit__(
        &mut self,
        _exc_type: Option<&Bound<'_, pyo3::types::PyAny>>,
        _exc_val: Option<&Bound<'_, pyo3::types::PyAny>>,
        _exc_tb: Option<&Bound<'_, pyo3::types::PyAny>>,
    ) -> bool {
        self.inner = None;
        false
    }
}

#[pymodule]
fn _rleveldb(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<KeyState>()?;
    m.add_class::<FileType>()?;
    m.add_class::<Record>()?;
    m.add_class::<RawLevelDb>()?;
    Ok(())
}
