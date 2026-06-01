use crate::operation::format_operation;
use crate::Operation;
use pyo3::{
    exceptions::{PyIndexError, PyTypeError},
    prelude::*,
    types::PySlice,
};
use taskchampion::Operations as TCOperations;

#[pyclass(from_py_object, sequence)]
#[derive(PartialEq, Eq, Clone, Debug, Default)]
/// A sequence of Operations.
///
/// This is a list-like type, and can be indexed, iterated over, and so on like any
/// other list-like type.
pub struct Operations(TCOperations);

#[pymethods]
impl Operations {
    #[new]
    pub fn new() -> Operations {
        Operations(TCOperations::new())
    }

    pub fn append(&mut self, op: Operation) {
        self.0.push(op.into());
    }

    pub fn __repr__(&self) -> String {
        let body: Vec<String> = self.0.iter().map(format_operation).collect();
        format!("Operations([{}])", body.join(", "))
    }

    pub fn __len__(&self) -> usize {
        self.0.len()
    }

    pub fn __getitem__(&self, py: Python<'_>, key: &Bound<'_, PyAny>) -> PyResult<Py<PyAny>> {
        let len = self.0.len() as isize;

        if let Ok(slice) = key.cast::<PySlice>() {
            let indices = slice.indices(len)?;
            let mut result = TCOperations::new();
            let mut i = indices.start;
            for _ in 0..indices.slicelength {
                result.push(self.0[i as usize].clone());
                i += indices.step;
            }
            Ok(Py::new(py, Operations(result))?.into_any())
        } else if let Ok(idx) = key.extract::<isize>() {
            let normalized = if idx < 0 { idx + len } else { idx };
            if normalized < 0 || normalized >= len {
                return Err(PyIndexError::new_err("operation index out of range"));
            }
            Ok(Py::new(py, Operation(self.0[normalized as usize].clone()))?.into_any())
        } else {
            Err(PyTypeError::new_err(
                "Operations indices must be integers or slices",
            ))
        }
    }
}

impl AsRef<TCOperations> for Operations {
    fn as_ref(&self) -> &TCOperations {
        &self.0
    }
}

impl AsMut<TCOperations> for Operations {
    fn as_mut(&mut self) -> &mut TCOperations {
        &mut self.0
    }
}

impl From<Operations> for TCOperations {
    fn from(val: Operations) -> Self {
        val.0
    }
}

impl From<TCOperations> for Operations {
    fn from(val: TCOperations) -> Self {
        Operations(val)
    }
}
