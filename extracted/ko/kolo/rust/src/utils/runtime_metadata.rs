use hashbrown::HashMap;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use rmpv::Value as RmpvValue;

use super::super::config;

/// Collect environment information similar to the Python `environment` dict.
pub fn collect_environment(py: Python) -> Result<HashMap<String, String>, PyErr> {
    let sys = PyModule::import(py, "sys")?;
    let platform_mod = PyModule::import(py, "platform")?;

    let py_version = platform_mod
        .call_method0("python_version")?
        .extract::<String>()?;
    let py_version_full = sys.getattr(intern!(py, "version"))?.extract::<String>()?;
    let platform_info = platform_mod.call_method0("platform")?.extract::<String>()?;
    let system = platform_mod.call_method0("system")?.extract::<String>()?;
    let machine = platform_mod.call_method0("machine")?.extract::<String>()?;
    let processor = platform_mod
        .call_method0("processor")?
        .extract::<String>()?;

    let mut environment = HashMap::new();
    environment.insert("py_version".to_string(), py_version);
    environment.insert("py_version_full".to_string(), py_version_full);
    environment.insert("platform".to_string(), platform_info);
    environment.insert("system".to_string(), system);
    environment.insert("machine".to_string(), machine);
    environment.insert("processor".to_string(), processor);

    Ok(environment)
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
