use std::sync::Arc;
use std::time::Duration;

use pyo3::{
    prelude::*,
    types::{PyDict, PyDictMethods, PyTuple},
};
use pyo3_stub_gen::derive::*;
use statsig_rust::{
    ConfigUpdates, DynamicConfigEvaluationOptions, Statsig,
    statsig_types_raw::DynamicConfigRaw,
    user::{StatsigUserInternal, fast_statsig_user::FastStatsigUser},
};

use crate::raw_evaluation_compat_py::raw_dynamic_config_to_py_dict;

fn is_usable(raw: &DynamicConfigRaw<'_>, source: &str) -> bool {
    raw.value.is_some_and(|value| {
        value.get_json_archived_ref().is_some() || value.get_json_pointer_ref().is_some()
    }) && raw.details.reason.ends_with(":Recognized")
        && !matches!(
            source,
            "Error"
                | "Loading"
                | "Uninitialized"
                | "NoValues"
                | "CountryLookupNotLoaded"
                | "UAParserNotLoaded"
        )
}

pub(crate) fn typed_config_to_py_dict(
    py: Python<'_>,
    raw: &DynamicConfigRaw<'_>,
    source: &str,
    revisions: &[(String, Option<u32>, Option<String>)],
) -> PyResult<Py<PyDict>> {
    let usable = is_usable(raw, source);
    let result = raw_dynamic_config_to_py_dict(py, raw, None, None)?;
    let dict = result.bind(py);
    dict.set_item("__typed_usable", usable)?;
    dict.set_item(
        "__typed_revision",
        (
            dict.get_item("ruleID")?,
            dict.get_item("idType")?,
            raw.details.version,
            raw.value.map(|value| value.get_hash()),
            PyTuple::new(py, revisions.iter().cloned())?,
        ),
    )?;
    Ok(result)
}

#[gen_stub_pyclass]
#[pyclass(name = "_TypedConfigContext", module = "statsig_python_core")]
pub struct NativeTypedConfigContext {
    pub(crate) statsig: Arc<Statsig>,
    pub(crate) user: FastStatsigUser,
    pub(crate) name: String,
}

#[gen_stub_pymethods]
#[pymethods]
impl NativeTypedConfigContext {
    pub fn get_evaluation(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        let user = StatsigUserInternal::from_fast_user(&self.user, Some(&self.statsig));
        self.statsig.use_typed_config(
            &user,
            &self.name,
            DynamicConfigEvaluationOptions {
                disable_exposure_logging: true,
            },
            |raw, source, revisions| typed_config_to_py_dict(py, raw, source, revisions),
        )
    }
}

#[gen_stub_pyclass]
#[pyclass(name = "_ConfigUpdates", module = "statsig_python_core")]
pub struct NativeConfigUpdates {
    pub(crate) inner: Arc<ConfigUpdates>,
}

#[gen_stub_pymethods]
#[pymethods]
impl NativeConfigUpdates {
    #[pyo3(signature = (timeout_ms=1000))]
    pub fn wait(&self, py: Python<'_>, timeout_ms: u64) -> Option<bool> {
        py.detach(|| self.inner.wait(Duration::from_millis(timeout_ms)))
    }

    pub fn close(&self) {
        self.inner.close();
    }
}

#[cfg(test)]
mod tests;
