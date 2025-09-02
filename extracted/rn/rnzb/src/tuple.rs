use pyo3::prelude::*;
use pyo3::types::PyTuple;

// Wrapper around a Vec<T> to implement Python tuple.
pub struct Tuple<T>(pub Vec<T>);

impl<'py, T: IntoPyObject<'py>> IntoPyObject<'py> for Tuple<T> {
    type Target = PyTuple;
    type Output = Bound<'py, Self::Target>;
    type Error = std::convert::Infallible;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        Ok(PyTuple::new(py, self.0).unwrap())
    }
}

impl<T> From<Vec<T>> for Tuple<T> {
    fn from(v: Vec<T>) -> Self {
        Self(v)
    }
}

impl<T> From<Tuple<T>> for Vec<T> {
    fn from(v: Tuple<T>) -> Self {
        v.0
    }
}
