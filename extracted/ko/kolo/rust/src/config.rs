use hashbrown::HashMap;
use pyo3::conversion::FromPyObjectOwned;
use pyo3::exceptions::{PyOverflowError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyFloat, PyInt};
use rmpv::Value as RmpvValue;

/// Default `max_value_mb`. Mirrors `DEFAULT_MAX_VALUE_MB` in
/// `python/src/kolo/config.py`.
pub const DEFAULT_MAX_VALUE_MB: usize = 64;

/// The per-value byte budget from `max_value_mb` (integer or float megabytes,
/// or `false` for no limit). Mirrors `config.resolve_max_value_bytes`.
pub fn resolve_max_value_bytes(config_dict: &Bound<'_, PyDict>) -> PyResult<Option<usize>> {
    let invalid = || PyValueError::new_err("max_value_mb must be a non-negative number or false");
    let Some(value) = config_dict.get_item("max_value_mb")? else {
        return Ok(Some(DEFAULT_MAX_VALUE_MB * 1024 * 1024));
    };
    if value.is_none() {
        return Ok(None);
    }
    // Python bools are ints, so check for one before extracting a number.
    if value.is_instance_of::<PyBool>() {
        return match value.extract::<bool>()? {
            false => Ok(None),
            true => Err(invalid()),
        };
    }
    // Only ints and floats, as in Python: `extract` alone would also take a
    // Decimal, a Fraction or anything with `__float__`.
    if !(value.is_instance_of::<PyInt>() || value.is_instance_of::<PyFloat>()) {
        return Err(invalid());
    }
    // `float(mb)`, as in Python, so a subclass's `__float__` counts the same;
    // only its OverflowError means an invalid budget.
    let mb: f64 = match value
        .py()
        .get_type::<PyFloat>()
        .call1((&value,))
        .and_then(|mb| mb.extract())
    {
        Ok(mb) => mb,
        Err(error) if error.is_instance_of::<PyOverflowError>(value.py()) => return Err(invalid()),
        Err(error) => return Err(error),
    };
    let bytes = mb * 1024.0 * 1024.0;
    // The same bound as `kolo.config.resolve_max_value_bytes`: at most
    // `sys.maxsize`, i.e. below isize::MAX + 1 (exactly representable).
    let limit = isize::MAX as f64 + 1.0;
    if !bytes.is_finite() || bytes < 0.0 || bytes >= limit {
        return Err(invalid());
    }
    Ok(Some(bytes as usize))
}

const CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE: [&str; 5] = ["filters", "processors", "auto_emit", "flush_subtree_mb", "trace_points"];

pub struct Config {
    inner: HashMap<String, Py<PyAny>>,
}

impl Config {
    pub fn new(config: &Bound<'_, PyDict>) -> PyResult<Self> {
        let mut inner = HashMap::new();
        for (key, value) in config.iter() {
            let key: String = key.extract()?;
            let value: Py<PyAny> = value.extract()?;
            inner.insert(key, value);
        }
        Ok(Self { inner })
    }

    pub fn get_or<'py, T: FromPyObjectOwned<'py>>(
        &self,
        py: Python<'py>,
        key: &str,
        default: T,
    ) -> PyResult<T> {
        match self.inner.get(key) {
            Some(value) => value.extract(py).map_err(Into::into),
            None => Ok(default),
        }
    }

    /// Build a PyDict containing the saved-trace config shape: every
    /// non-omitted key from the raw config dict, plus `use_monitoring=True`
    /// and `use_rust=True` to mirror what Python's `_build_trace_meta()`
    /// attaches on the Python monitor.
    pub fn to_py_dict<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        let dict = PyDict::new(py);
        for (key, value) in &self.inner {
            if CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE.contains(&key.as_str()) {
                continue;
            }
            dict.set_item(key, value.bind(py))?;
        }
        dict.set_item("use_monitoring", true)?;
        dict.set_item("use_rust", true)?;
        Ok(dict)
    }

    pub fn to_dict(&self, py: Python) -> PyResult<HashMap<String, RmpvValue>> {
        let mut result = HashMap::with_capacity(self.inner.len());
        for (key, value) in &self.inner {
            if CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE.contains(&key.as_str()) {
                continue;
            }

            if value.is_none(py) {
                result.insert(key.clone(), RmpvValue::Nil);
            } else if let Ok(s) = value.extract::<String>(py) {
                result.insert(key.clone(), RmpvValue::String(s.into()));
            } else if let Ok(b) = value.extract::<bool>(py) {
                result.insert(key.clone(), RmpvValue::Boolean(b));
            } else if let Ok(n) = value.extract::<i64>(py) {
                result.insert(key.clone(), RmpvValue::Integer(n.into()));
            } else if let Ok(n) = value.extract::<f64>(py) {
                result.insert(key.clone(), RmpvValue::F64(n));
            } else {
                println!("unsupported config type: {:?}", key);
            }
            // Handle other types as needed
        }
        Ok(result)
    }
}
