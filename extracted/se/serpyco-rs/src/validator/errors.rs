use pyo3::types::PyType;
use pyo3::{PyErr, PyResult, Python};

use crate::errors::ErrorItem;
use crate::errors::SchemaValidationError;
use crate::validator::context::PathChunk;
use crate::validator::InstancePath;

pub fn raise_error<T: Into<String>>(error: T, instance_path: &InstancePath) -> PyResult<()> {
    Python::with_gil(|py| {
        let errors: Vec<ErrorItem> = vec![into_err_item(error, instance_path)];

        let pyerror_type = PyType::new::<SchemaValidationError>(py);
        Err(PyErr::from_type(
            pyerror_type,
            ("Schema validation failed".to_string(), errors),
        ))
    })
}

fn into_err_item<T: Into<String>>(error: T, instance_path: &InstancePath) -> ErrorItem {
    let instance_path = into_path(instance_path);
    ErrorItem::new(error.into(), instance_path)
}

fn into_path(pointer: &InstancePath) -> String {
    let mut path = vec![];
    for chunk in pointer.to_vec() {
        match chunk {
            PathChunk::Property(property) => {
                path.push(property.to_string());
            }
            PathChunk::Index(index) => path.push(index.to_string()),
            PathChunk::PropertyValue(value) => path.push(value.to_string()),
        };
    }
    path.join("/")
}

pub fn map_py_err_to_schema_validation_error(
    py: Python<'_>,
    error: PyErr,
    instance_path: &InstancePath,
) -> PyErr {
    let error_message = format!("{}", &error);
    let instance_path = into_path(instance_path);
    let err = PyErr::new::<SchemaValidationError, _>((
        "Schema validation failed".to_string(),
        vec![ErrorItem::new(error_message, instance_path)],
    ));
    err.set_cause(py, Some(error));
    err
}
