use pyo3::prelude::*;
use pyo3::types::{PyEllipsis, PyList, PyMapping, PySequence, PyTuple};

pub fn ellipsis() -> Py<PyEllipsis> {
    Python::attach(|py| PyEllipsis::get(py).to_owned().unbind())
}

#[derive(FromPyObject)]
pub enum KeyValPairs<'py> {
    Mapping(Bound<'py, PyMapping>),
    List(Bound<'py, PyList>),
    Tuple(Bound<'py, PyTuple>),
    Sequence(Bound<'py, PySequence>),
}
impl<'py> KeyValPairs<'py> {
    pub fn for_each<F, K, V>(self, mut f: F) -> PyResult<()>
    where
        F: FnMut((K, V)) -> PyResult<()>,
        for<'a> K: FromPyObject<'a, 'py>,
        for<'a> V: FromPyObject<'a, 'py>,
    {
        match self {
            KeyValPairs::Mapping(v) => v.items()?.iter().try_for_each(|v| f(v.extract::<(K, V)>()?)),
            KeyValPairs::List(v) => v.try_iter()?.try_for_each(|v| f(v?.extract::<(K, V)>()?)),
            KeyValPairs::Tuple(v) => v.iter().try_for_each(|v| f(v.extract::<(K, V)>()?)),
            KeyValPairs::Sequence(v) => v.try_iter()?.try_for_each(|v| f(v?.extract::<(K, V)>()?)),
        }
    }

    pub fn into_vec<K, V>(self) -> PyResult<Vec<(K, V)>>
    where
        for<'a> K: FromPyObject<'a, 'py>,
        for<'a> V: FromPyObject<'a, 'py>,
    {
        let mut res = Vec::with_capacity(self.len()?);
        self.for_each(|(key, value)| {
            res.push((key, value));
            Ok(())
        })?;
        Ok(res)
    }

    pub fn len(&self) -> PyResult<usize> {
        match self {
            KeyValPairs::Mapping(v) => v.len(),
            KeyValPairs::List(v) => Ok(v.len()),
            KeyValPairs::Tuple(v) => Ok(v.len()),
            KeyValPairs::Sequence(v) => v.len(),
        }
    }
}
