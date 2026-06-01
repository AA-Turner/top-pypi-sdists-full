use crate::safe_gil::SafeGil;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::pyclass;
use pyo3::pymethods;
use pyo3::types::PyBytes;
use pyo3::types::PyModule;
use pyo3::types::PyType;
use pyo3_stub_gen::derive::*;

use statsig_rust::interned_values::InternedStore;
use statsig_rust::log_e;
use statsig_rust::StatsigRuntime;

const TAG: &str = stringify!(InternStorePy);

#[gen_stub_pyclass]
#[pyclass(name = "InternedStore", module = "statsig_python_core")]
#[derive(Default)]
pub struct InternedStorePy;

#[gen_stub_pymethods]
#[pymethods]
impl InternedStorePy {
    #[classmethod]
    pub fn preload(_cls: &Bound<'_, PyType>, data: &Bound<'_, PyBytes>) -> PyResult<()> {
        let bytes: &[u8] = data.as_bytes();

        if let Err(e) = InternedStore::preload(bytes) {
            log_e!(TAG, "Failed to preload interned store: {}", e);
            return Err(PyRuntimeError::new_err(e.to_string()));
        }

        Ok(())
    }

    #[classmethod]
    pub fn preload_multi(_cls: &Bound<'_, PyType>, data: Vec<Bound<'_, PyBytes>>) -> PyResult<()> {
        let bytes: Vec<&[u8]> = data.iter().map(|data| data.as_bytes()).collect();

        if let Err(e) = InternedStore::preload_multi(&bytes) {
            log_e!(TAG, "Failed to preload interned store: {}", e);
            return Err(PyRuntimeError::new_err(e.to_string()));
        }

        Ok(())
    }

    #[classmethod]
    #[pyo3(signature = (sdk_key, specs_url=None))]
    pub fn fetch_and_write_mmap(
        _cls: &Bound<'_, PyType>,
        sdk_key: &str,
        specs_url: Option<String>,
        py: Python,
    ) -> PyResult<Py<PyAny>> {
        let (completion_event, event_clone) = get_completion_event(py)?;
        let sdk_key = sdk_key.to_string();
        let runtime = StatsigRuntime::get_runtime();
        let runtime_guard = runtime.clone();
        let spawn_result = runtime.spawn(TAG, move |_| async move {
            let _runtime_guard = runtime_guard;

            let result = match specs_url {
                Some(specs_url) => {
                    InternedStore::fetch_and_write_mmap_with_specs_url(&sdk_key, &specs_url).await
                }
                None => InternedStore::fetch_and_write_mmap(&sdk_key).await,
            };

            if let Err(e) = result {
                log_e!(TAG, "Failed to fetch and write mmap data: {}", e);
            }

            SafeGil::run(|py| {
                let py = match py {
                    Some(py) => py,
                    None => return,
                };

                call_completion_event(&event_clone, py);
            });
        });

        if let Err(e) = spawn_result {
            log_e!(TAG, "Failed to spawn mmap fetch task: {e}");
            call_completion_event(&completion_event, py);
        }

        Ok(completion_event)
    }

    #[classmethod]
    pub fn preload_mmap(_cls: &Bound<'_, PyType>, sdk_key: &str) -> PyResult<()> {
        if let Err(e) = InternedStore::preload_mmap(sdk_key) {
            log_e!(TAG, "Failed to load mmap data: {}", e);
            return Err(PyRuntimeError::new_err(e.to_string()));
        }

        Ok(())
    }
}

fn get_completion_event(py: Python) -> PyResult<(Py<PyAny>, Py<PyAny>)> {
    let threading = PyModule::import(py, "threading")?;
    let event = threading.call_method0("Event")?;
    let event_clone: Py<PyAny> = event.clone().unbind();

    Ok((event.unbind(), event_clone))
}

fn call_completion_event(event: &Py<PyAny>, py: Python) {
    if let Err(e) = event.as_ref().call_method0(py, "set") {
        log_e!(TAG, "Failed to set mmap completion event: {}", e);
    }
}
