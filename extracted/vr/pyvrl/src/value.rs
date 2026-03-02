use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyFloat, PyAny};
use pyo3::exceptions::{PyTypeError, PyValueError};
use std::collections::BTreeMap;
use vrl::value::Value;

use vrl::prelude::*;

#[pyclass]
pub struct VrlValue {
    pub inner: Value,
}

impl VrlValue {
    pub fn new(value: Value) -> Self {
        VrlValue { inner: value }
    }

    pub fn into_py_object(self, py: Python) -> PyResult<PyObject> {
        match self.inner {
            Value::Array(arr) => {
                let list = PyList::new(py, &[] as &[PyObject]);
                for val in arr {
                    let py_val = VrlValue { inner: val };
                    list.append(py_val.into_py_object(py)?)?;
                }
                Ok(list.into_py(py))
            },
            Value::Bytes(b) => {
                Ok(String::from_utf8_lossy(&b).into_py(py))
            },
            Value::Boolean(b) => Ok(b.into_py(py)),
            Value::Float(f) => {
                let float: &PyFloat = PyFloat::new(py, f.into_inner());
                Ok(float.into_py(py))
            },
            Value::Integer(i) => Ok(i.into_py(py)),
            Value::Null => Ok(py.None()),
            Value::Object(map) => {
                let dict = PyDict::new(py);
                for (k, v) in map {
                    let py_vrl_value = VrlValue { inner: v };
                    dict.set_item(&*k, py_vrl_value.into_py_object(py)?)?;
                }
                Ok(dict.into_py(py))
            },
            Value::Timestamp(ts) => Ok(ts.into_py(py)),
            _ => Ok(py.None()),
        }
    }
}

impl<'source> FromPyObject<'source> for VrlValue {

    fn extract(ob: &'source PyAny) -> PyResult<Self> {

        let val: Value = match ob.get_type().name()? {
            "bool" => Value::Boolean(ob.extract::<bool>()?),
            "bytes" => Value::Bytes(ob.extract::<Vec<u8>>()?.into()),
            "dict" => {
                let dict = ob.downcast::<PyDict>()?;
                let mut map = BTreeMap::new();
                for (k, v) in dict {
                    let key: String = k.extract()?;
                    let value: VrlValue = v.extract()?;
                    map.insert(key.into(), value.inner);
                }
                Value::Object(map)
            },
            "float" => Value::Float(NotNan::new(ob.extract::<f64>()?)
                                            .map_err(|_|
                                                PyErr::new::<PyValueError, _>(
                                                    "Provided float value is NaN"))?),
            "int" => Value::Integer(ob.extract::<i64>()?),
            "list" => {
                let list = ob.downcast::<PyList>()?;
                let mut vec = Vec::new();
                for item in list {
                    let value: VrlValue = item.extract()?;
                    vec.push(value.inner);
                }
                Value::Array(vec)
            },
            "NoneType" => Value::Null,
            "str" => Value::Bytes(ob.extract::<String>()?.into()),
            _ => return Err(PyTypeError::new_err("Unsupported type"))
        };

        Ok(VrlValue::new(val))
    }
}
