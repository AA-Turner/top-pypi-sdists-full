use base64::engine::general_purpose::STANDARD as BASE64_STANDARD;
use base64::Engine;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyString};

/// Encode bytes to string representation.
/// If represent_as_string is true, uses base64 encoding.
/// Otherwise, decodes bytes as UTF-8.
#[pyfunction]
#[pyo3(signature = (value, represent_as_string=false))]
pub fn encode_bytes(
    py: Python<'_>,
    value: &Bound<'_, PyAny>,
    represent_as_string: bool,
) -> PyResult<PyObject> {
    if value.is_instance_of::<PyString>() {
        return Ok(value.clone().unbind());
    }

    let bytes_val: &[u8] = value.downcast::<PyBytes>()?.as_bytes();

    if represent_as_string {
        let encoded = BASE64_STANDARD.encode(bytes_val);
        Ok(PyString::new(py, &encoded).into())
    } else {
        let s = std::str::from_utf8(bytes_val)
            .map_err(|e| pyo3::exceptions::PyUnicodeDecodeError::new_err(e.to_string()))?;
        Ok(PyString::new(py, s).into())
    }
}

/// Decode string to bytes.
/// If represent_as_string is true, uses base64 decoding.
/// Otherwise, encodes string as UTF-8 bytes.
#[pyfunction]
#[pyo3(signature = (value, represent_as_string=false))]
pub fn decode_bytes(
    py: Python<'_>,
    value: &Bound<'_, PyAny>,
    represent_as_string: bool,
) -> PyResult<PyObject> {
    if value.is_instance_of::<PyBytes>() {
        return Ok(value.clone().unbind());
    }

    let s: &str = value.extract()?;

    if represent_as_string {
        let decoded = BASE64_STANDARD
            .decode(s)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
        Ok(PyBytes::new(py, &decoded).into())
    } else {
        Ok(PyBytes::new(py, s.as_bytes()).into())
    }
}

/// Encode a value to JSON string.
/// Handles datetime objects by calling .isoformat() first.
#[pyfunction]
pub fn encode_json(py: Python<'_>, value: &Bound<'_, PyAny>) -> PyResult<PyObject> {
    let datetime_mod = py.import("datetime")?;
    let date_type = datetime_mod.getattr("date")?;
    let datetime_type = datetime_mod.getattr("datetime")?;
    let time_type = datetime_mod.getattr("time")?;

    let mut val = value.clone().unbind();

    // Convert datetime types to isoformat string
    if value.is_instance(&datetime_type)?
        || value.is_instance(&date_type)?
        || value.is_instance(&time_type)?
    {
        val = value.call_method0("isoformat")?.unbind();
    }

    let val_bound = val.bind(py);

    // If already a string, try to re-dump it (load then dump for normalization)
    if val_bound.is_instance_of::<PyString>() {
        let s: String = val_bound.extract()?;
        // Try to parse as JSON and re-serialize for normalization
        match serde_json::from_str::<serde_json::Value>(&s) {
            Ok(parsed) => {
                let result = serde_json::to_string(&parsed)
                    .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
                return Ok(PyString::new(py, &result).into());
            }
            Err(_) => {
                // Not valid JSON, return as-is
                return Ok(val_bound.clone().unbind());
            }
        }
    }

    // For other types, use Python's json.dumps
    let json_mod = py.import("orjson").or_else(|_| py.import("json"))?;

    // Check if using orjson (which is always compact) or standard json
    let is_orjson = json_mod.getattr("__name__")?.extract::<String>()? == "orjson";

    let dumped = if is_orjson {
        // orjson is always compact, no need for separators parameter
        json_mod.call_method1("dumps", (val_bound,))?
    } else {
        // Standard json: use separators to match orjson's compact format
        let kwargs = PyDict::new(py);
        kwargs.set_item("separators", (",", ":"))?;
        json_mod.call_method("dumps", (val_bound,), Some(&kwargs))?
    };

    // orjson returns bytes, json returns str
    if dumped.is_instance_of::<PyBytes>() {
        let bytes_val: &[u8] = dumped.downcast::<PyBytes>()?.as_bytes();
        let s = std::str::from_utf8(bytes_val)
            .map_err(|e| pyo3::exceptions::PyUnicodeDecodeError::new_err(e.to_string()))?;
        Ok(PyString::new(py, s).into())
    } else {
        Ok(dumped.unbind())
    }
}
