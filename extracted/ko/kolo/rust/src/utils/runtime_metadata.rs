use hashbrown::HashMap;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use rmpv::Value as RmpvValue;

use super::super::config;

/// The Python `environment` dict, from `kolo._platform_info` so that Rust traces
/// avoid the same Windows CPython 3.12 WMI crash.
pub fn collect_environment(py: Python) -> Result<HashMap<String, String>, PyErr> {
    PyModule::import(py, "kolo._platform_info")?
        .call_method0(intern!(py, "environment"))?
        .extract::<std::collections::HashMap<String, String>>()
        .map(|environment| environment.into_iter().collect())
}

pub fn collect_config(
    py: Python,
    config: &config::Config,
    use_monitoring: bool,
) -> Result<HashMap<String, RmpvValue>, PyErr> {
    let raw_config = config.to_dict(py)?;
    let mut filtered_config = HashMap::new();

    for (key, value) in raw_config {
        filtered_config.insert(key, value.into()); // Convert PyAny to RmpvValue
    }

    filtered_config.insert(
        "use_monitoring".to_string(),
        RmpvValue::Boolean(use_monitoring),
    );
    filtered_config.insert("use_rust".to_string(), RmpvValue::Boolean(true));

    Ok(filtered_config)
}
