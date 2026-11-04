use crate::safe_gil::SafeGil;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::pyclass;
use pyo3::pymethods;
use pyo3::types::PyBytes;
use pyo3::types::PyModule;
use pyo3::types::PyType;
use pyo3_stub_gen::derive::*;

use statsig_rust::interned_values::{
    InternedStore, MmapPreloadOptions, MmapPreloadReport as RustMmapPreloadReport,
    MmapReaderMemorySnapshot,
};
use statsig_rust::log_e;
use statsig_rust::{StatsigErr, StatsigRuntime};

const TAG: &str = stringify!(InternStorePy);

#[gen_stub_pyclass]
#[pyclass(name = "MmapReaderMemorySnapshot", module = "statsig_python_core")]
pub struct MmapReaderMemorySnapshotPy {
    #[pyo3(get)]
    pub format_version: u32,
    #[pyo3(get)]
    pub mapped_bytes: u64,
    #[pyo3(get)]
    pub resident_bytes: Option<u64>,
    #[pyo3(get)]
    pub proportional_set_bytes: Option<u64>,
    #[pyo3(get)]
    pub private_dirty_bytes: Option<u64>,
    #[pyo3(get)]
    pub deleted_mapped_bytes: Option<u64>,
    #[pyo3(get)]
    pub loaded_generation_count: u64,
    #[pyo3(get)]
    pub vma_segment_count: Option<u64>,
}

impl From<MmapReaderMemorySnapshot> for MmapReaderMemorySnapshotPy {
    fn from(snapshot: MmapReaderMemorySnapshot) -> Self {
        Self {
            format_version: snapshot.format_version,
            mapped_bytes: snapshot.mapped_bytes,
            resident_bytes: snapshot.resident_bytes,
            proportional_set_bytes: snapshot.proportional_set_bytes,
            private_dirty_bytes: snapshot.private_dirty_bytes,
            deleted_mapped_bytes: snapshot.deleted_mapped_bytes,
            loaded_generation_count: snapshot.loaded_generation_count,
            vma_segment_count: snapshot.vma_segment_count,
        }
    }
}

#[gen_stub_pyclass]
#[pyclass(name = "MmapPreloadReport", module = "statsig_python_core")]
pub struct MmapPreloadReportPy {
    #[pyo3(get)]
    pub loaded: usize,

    #[pyo3(get)]
    pub skipped_optional_indexes: Vec<usize>,
}

impl From<RustMmapPreloadReport> for MmapPreloadReportPy {
    fn from(report: RustMmapPreloadReport) -> Self {
        Self {
            loaded: report.loaded,
            skipped_optional_indexes: report
                .skipped_optional
                .into_iter()
                .map(|failure| failure.index)
                .collect(),
        }
    }
}

#[gen_stub_pyclass]
#[pyclass(name = "InternedStore", module = "statsig_python_core")]
#[derive(Default)]
pub struct InternedStorePy;

#[gen_stub_pymethods]
#[pymethods]
impl InternedStorePy {
    #[classmethod]
    pub fn preload(
        _cls: &Bound<'_, PyType>,
        #[gen_stub(override_type(
            type_repr = "typing.Union[builtins.bytes, typing.List[builtins.bytes]]"
        ))]
        data: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        let payloads = if let Ok(single) = data.cast::<PyBytes>() {
            vec![single.clone()]
        } else {
            data.extract::<Vec<Bound<'_, PyBytes>>>()?
        };
        let bytes: Vec<&[u8]> = payloads.iter().map(|data| data.as_bytes()).collect();
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
    pub fn mmap_reader_memory_snapshot(
        _cls: &Bound<'_, PyType>,
        py: Python<'_>,
    ) -> PyResult<Option<MmapReaderMemorySnapshotPy>> {
        py.detach(|| {
            InternedStore::mmap_reader_memory_snapshot().map_err(|error| error.to_string())
        })
        .map(|snapshot| snapshot.map(Into::into))
        .map_err(|error| {
            log_e!(TAG, "Failed to inspect mmap reader memory: {error}");
            PyRuntimeError::new_err(error)
        })
    }

    #[classmethod]
    #[pyo3(signature = (required=None, *, optional=None, precompute_returnable_stable_hashes=false))]
    pub fn preload_mmap(
        cls: &Bound<'_, PyType>,
        #[gen_stub(override_type(
            type_repr = "typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]"
        ))]
        required: Option<&Bound<'_, PyAny>>,
        #[gen_stub(override_type(
            type_repr = "typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]"
        ))]
        optional: Option<&Bound<'_, PyAny>>,
        precompute_returnable_stable_hashes: bool,
    ) -> PyResult<MmapPreloadReportPy> {
        let required_keys = extract_sdk_keys(required)?;
        let optional_keys = extract_sdk_keys(optional)?;
        let required = required_keys.iter().map(String::as_str).collect::<Vec<_>>();
        let optional = optional_keys.iter().map(String::as_str).collect::<Vec<_>>();

        let options = MmapPreloadOptions {
            precompute_returnable_stable_hashes,
        };
        match InternedStore::preload_mmap(&required, &optional, &options) {
            Ok(report) => Ok(report.into()),
            Err(error) => {
                log_e!(TAG, "Failed to load mmap data: {}", error);
                Err(to_python_error(cls.py(), &error))
            }
        }
    }
}

fn extract_sdk_keys(value: Option<&Bound<'_, PyAny>>) -> PyResult<Vec<String>> {
    match value {
        None => Ok(Vec::new()),
        Some(value) => match value.extract::<String>() {
            Ok(key) => Ok(vec![key]),
            Err(_) => value.extract::<Vec<String>>(),
        },
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

fn to_python_error(py: Python, error: &StatsigErr) -> PyErr {
    let message = error.to_string();
    let exception = PyRuntimeError::new_err(message.clone());
    let value = exception.value(py);
    let result = value
        .setattr("error_name", error.name())
        .and_then(|_| value.setattr("error_message", message));
    if let Err(e) = result {
        log_e!(TAG, "Failed to set interned store error details: {}", e);
    }
    exception
}
