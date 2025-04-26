use pyo3::prelude::*;
use pyo3::types::PyDict;
use hashbrown::HashMap;
use rmpv::Value as RmpvValue;

const CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE: [&str; 3] = ["filters", "processors", "test_generation"];

pub struct Config {
    inner: HashMap<String, PyObject>,
}

impl Config {
    pub fn new(config: &Bound<'_, PyDict>) -> PyResult<Self> {
        let mut inner = HashMap::new();
        for (key, value) in config.iter() {
            let key: String = key.extract()?;
            let value: PyObject = value.extract()?;
            inner.insert(key, value);
        }
        Ok(Self { inner })
    }

    pub fn get_or<'py, T: FromPyObject<'py>>(&self, py: Python<'py>, key: &str, default: T) -> PyResult<T> {
        match self.inner.get(key) {
            Some(value) => value.extract(py),
            None => Ok(default),
        }
    }

    pub fn to_dict(&self, py: Python) -> PyResult<HashMap<String, RmpvValue>> {
        let mut result = HashMap::with_capacity(self.inner.len());
        for (key, value) in &self.inner {
            if CONFIG_KEYS_TO_OMIT_FROM_SAVED_TRACE.contains(&key.as_str()) {
                continue;
            }

            if let Ok(s) = value.extract::<String>(py) {
                result.insert(key.clone(), RmpvValue::String(s.into()));
            }
            else if let Ok(b) = value.extract::<bool>(py) {
                result.insert(key.clone(), RmpvValue::Boolean(b));
            }
            else if let Ok(n) = value.extract::<i64>(py) {
                result.insert(key.clone(), RmpvValue::Integer(n.into()));
            }
            else if let Ok(n) = value.extract::<f64>(py) {
                result.insert(key.clone(), RmpvValue::F64(n));
            } else {
                println!("unsupported config type: {:?}", key);
            }
            // Handle other types as needed
        }
        Ok(result)
    }
}
