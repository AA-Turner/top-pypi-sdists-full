use async_trait::async_trait;
use pyo3::{FromPyObject, prelude::*, pyclass, pymethods, types::PyDict};
use pyo3_stub_gen::derive::*;
use statsig_rust::{
    EventLoggingAdapter, StatsigErr, StatsigRuntime, log_e, log_event_payload::LogEventRequest,
};
use std::sync::Arc;

use crate::pyo_utils::json_value_to_py_object;
use crate::safe_gil::SafeGil;

const TAG: &str = "EventLoggingAdapterBasePy";

#[gen_stub_pyclass]
#[pyclass(name = "LogEventRequest", module = "statsig_python_core")]
pub struct LogEventRequestPy {
    #[pyo3(get)]
    pub payload: Py<PyAny>,
    #[pyo3(get)]
    pub event_count: u64,
    #[pyo3(get)]
    pub retries: u32,
}

#[gen_stub_pymethods]
#[pymethods]
impl LogEventRequestPy {
    #[new]
    pub fn new(payload: Py<PyAny>, event_count: u64, retries: u32) -> Self {
        Self {
            payload,
            event_count,
            retries,
        }
    }
}

#[gen_stub_pyclass]
#[pyclass(
    name = "EventLoggingAdapterBase",
    module = "statsig_python_core",
    subclass
)]
#[derive(FromPyObject, Default)]
pub struct EventLoggingAdapterBasePy {
    log_events_fn: Option<Py<PyAny>>,
}

#[gen_stub_pymethods]
#[pymethods]
impl EventLoggingAdapterBasePy {
    #[new]
    pub fn new() -> Self {
        Self::default()
    }
}

#[async_trait]
impl EventLoggingAdapter for EventLoggingAdapterBasePy {
    async fn start(&self, _statsig_runtime: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
        Ok(())
    }

    async fn log_events(&self, request: LogEventRequest) -> Result<bool, StatsigErr> {
        SafeGil::run(|py| {
            let py = py.ok_or_else(|| {
                StatsigErr::LogEventError("Python interpreter has been shutdown".to_string())
            })?;

            let log_events_fn = self.log_events_fn.as_ref().ok_or_else(|| {
                StatsigErr::LogEventError("No 'log_events' function provided".to_string())
            })?;

            let py_request = self.make_py_request(py, request)?;
            let result = log_events_fn
                .as_ref()
                .call1(py, (py_request,))
                .map_err(|e| {
                    log_e!(
                        TAG,
                        "Failed to call EventLoggingAdapter.log_events: {:?}",
                        e
                    );
                    StatsigErr::LogEventError("Failed to call log_events".to_string())
                })?;

            result.extract::<bool>(py).map_err(|e| {
                log_e!(
                    TAG,
                    "Failed to extract EventLoggingAdapter.log_events result: {:?}",
                    e
                );
                StatsigErr::LogEventError("log_events must return bool".to_string())
            })
        })
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        Ok(())
    }

    fn should_schedule_background_flush(&self) -> bool {
        true
    }
}

impl EventLoggingAdapterBasePy {
    fn make_py_request(
        &self,
        py: Python<'_>,
        request: LogEventRequest,
    ) -> Result<Py<LogEventRequestPy>, StatsigErr> {
        let py_payload = PyDict::new(py);
        py_payload
            .set_item(
                "events",
                json_value_to_py_object(py, &request.payload.events).map_err(|e| {
                    log_e!(TAG, "Failed to convert log events payload: {:?}", e);
                    StatsigErr::LogEventError("Failed to convert log events payload".to_string())
                })?,
            )
            .map_err(|e| {
                log_e!(TAG, "Failed to set log events payload: {:?}", e);
                StatsigErr::LogEventError("Failed to set log events payload".to_string())
            })?;

        py_payload
            .set_item(
                "statsigMetadata",
                json_value_to_py_object(py, &request.payload.statsig_metadata).map_err(|e| {
                    log_e!(TAG, "Failed to convert log event metadata: {:?}", e);
                    StatsigErr::LogEventError("Failed to convert log event metadata".to_string())
                })?,
            )
            .map_err(|e| {
                log_e!(TAG, "Failed to set log event metadata: {:?}", e);
                StatsigErr::LogEventError("Failed to set log event metadata".to_string())
            })?;

        Py::new(
            py,
            LogEventRequestPy {
                payload: py_payload.unbind().into(),
                event_count: request.event_count,
                retries: request.retries,
            },
        )
        .map_err(|e| {
            log_e!(TAG, "Failed to create LogEventRequest: {:?}", e);
            StatsigErr::LogEventError("Failed to create LogEventRequest".to_string())
        })
    }
}
