mod async_service;
mod coalesce;
// The self-consumer and its metrics pipeline run only on the Linux scaling-group
// pods (they need the dataplane Redis). Their deps (chalk-queue / chalk_metrics →
// rdkafka's cyrus-sasl, chalk-protos' protoc) don't build on Windows and need
// extra native tooling on macOS, so they're Linux-only — keeping the gRPC
// server/client portable to every platform.
#[cfg(target_os = "linux")]
mod fnq_client;
#[cfg(target_os = "linux")]
mod metrics;
mod python_bridge;
#[cfg(target_os = "linux")]
mod self_consumer;
mod server;
mod service;

use std::sync::{Arc, Condvar, Mutex};
use std::time::{Duration, SystemTime, UNIX_EPOCH};

use pyo3::prelude::*;
use tracing_subscriber::EnvFilter;

use crate::coalesce::CoalescingQueue;
use crate::python_bridge::PythonHandler;

/// Shared opt-in readiness and request-admission state. The Python handle
/// changes this synchronized state directly; the gRPC health reporter watches
/// it, and each RPC consults the same state before dispatch.
pub(crate) struct ServingState {
    current: Mutex<ServingSnapshot>,
    changes: tokio::sync::watch::Sender<bool>,
    drained: Condvar,
    require_target: bool,
}

struct ServingSnapshot {
    serving: bool,
    deadline: Option<tokio::time::Instant>,
    lease_expires_at: Option<f64>,
    target: Option<String>,
    active: usize,
    failed: bool,
}

const MAX_SERVING_LEASE: Duration = Duration::from_secs(300);

impl ServingState {
    fn new(initially_serving: bool, require_target: bool) -> Arc<Self> {
        let (changes, _) = tokio::sync::watch::channel(initially_serving);
        Arc::new(Self {
            current: Mutex::new(ServingSnapshot {
                serving: initially_serving,
                deadline: None,
                lease_expires_at: None,
                target: None,
                active: 0,
                failed: false,
            }),
            changes,
            drained: Condvar::new(),
            require_target,
        })
    }

    pub(crate) fn is_serving(&self) -> bool {
        let mut current = self
            .current
            .lock()
            .unwrap_or_else(|error| error.into_inner());
        if current.serving
            && current
                .deadline
                .is_some_and(|deadline| deadline <= tokio::time::Instant::now())
        {
            current.serving = false;
            current.deadline = None;
            drop(current);
            self.changes.send_replace(false);
            return false;
        }
        current.serving
    }

    fn set_serving(
        &self,
        serving: bool,
        lease_expires_at: Option<f64>,
        target: Option<String>,
    ) -> PyResult<()> {
        if serving {
            if self.require_target && target.as_ref().is_none_or(|value| !valid_target(value)) {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "managed serving requires a lowercase SHA256 target fingerprint",
                ));
            }

            let expires_at = lease_expires_at.ok_or_else(|| {
                pyo3::exceptions::PyValueError::new_err(
                    "lease_expires_at is required when enabling serving",
                )
            })?;
            if !expires_at.is_finite() {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "lease_expires_at must be a finite Unix timestamp",
                ));
            }
            let mut current = self
                .current
                .lock()
                .unwrap_or_else(|error| error.into_inner());
            if current.failed {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(
                    "managed execution failed; restart the replica",
                ));
            }
            if current.target != target && current.active != 0 {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(
                    "cannot change target before native calls drain",
                ));
            }
            if current.lease_expires_at == Some(expires_at) {
                if current
                    .deadline
                    .is_some_and(|deadline| deadline > tokio::time::Instant::now())
                {
                    // Repeated delivery of the same absolute lease cannot
                    // move its monotonic deadline forward. This also allows
                    // close/apply/open to reuse the still-valid lease.
                    current.target = target;
                    current.serving = true;
                    drop(current);
                    self.changes.send_replace(true);
                    return Ok(());
                }
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "lease_expires_at has already expired",
                ));
            }
            if current
                .lease_expires_at
                .is_some_and(|previous| expires_at < previous)
            {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "lease_expires_at moved backwards",
                ));
            }
            let now = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .map_err(|error| pyo3::exceptions::PyRuntimeError::new_err(error.to_string()))?
                .as_secs_f64();
            let remaining = expires_at - now;
            if remaining <= 0.0 || remaining > MAX_SERVING_LEASE.as_secs_f64() {
                return Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "lease_expires_at must be in the next {} seconds",
                    MAX_SERVING_LEASE.as_secs()
                )));
            }
            let deadline = tokio::time::Instant::now() + Duration::from_secs_f64(remaining);
            current.serving = true;
            current.target = target;
            current.deadline = Some(deadline);
            current.lease_expires_at = Some(expires_at);
            drop(current);
            self.changes.send_replace(true);
            return Ok(());
        } else {
            let mut current = self
                .current
                .lock()
                .unwrap_or_else(|error| error.into_inner());
            current.serving = false;
            drop(current);
            self.changes.send_replace(false);
        }
        Ok(())
    }

    pub(crate) fn check(&self, required: Option<&str>) -> Result<(), AdmissionRejection> {
        let current = self
            .current
            .lock()
            .unwrap_or_else(|error| error.into_inner());
        self.check_locked(&current, required)
    }

    fn check_locked(
        &self,
        current: &ServingSnapshot,
        required: Option<&str>,
    ) -> Result<(), AdmissionRejection> {
        if !current.serving
            || current.failed
            || current
                .deadline
                .is_some_and(|deadline| deadline <= tokio::time::Instant::now())
        {
            return Err(AdmissionRejection::NotReady);
        }
        if self.require_target && (required.is_none() || required != current.target.as_deref()) {
            return Err(AdmissionRejection::WrongTarget);
        }
        Ok(())
    }

    pub(crate) fn admit(
        self: &Arc<Self>,
        required: Option<&str>,
    ) -> Result<ServingPermit, AdmissionRejection> {
        let mut current = self
            .current
            .lock()
            .unwrap_or_else(|error| error.into_inner());
        // Checking the lease/target and counting the work under one lock prevents
        // a pause/drain from racing a handler that was accepted on the old target.
        self.check_locked(&current, required)?;
        current.active = current
            .active
            .checked_add(1)
            .ok_or(AdmissionRejection::Capacity)?;
        Ok(ServingPermit {
            state: Arc::clone(self),
            completed: false,
            started: false,
        })
    }

    fn wait_drained(&self, timeout: Duration) -> Result<bool, &'static str> {
        let started = std::time::Instant::now();
        let mut current = self
            .current
            .lock()
            .unwrap_or_else(|error| error.into_inner());
        loop {
            if current.serving {
                return Err("close native admission before waiting for drain");
            }
            if current.failed {
                return Err("managed execution failed; restart the replica");
            }
            if current.active == 0 {
                return Ok(true);
            }
            let Some(remaining) = timeout.checked_sub(started.elapsed()) else {
                return Ok(false);
            };
            let (next, _) = self
                .drained
                .wait_timeout(current, remaining)
                .unwrap_or_else(|error| error.into_inner());
            current = next;
        }
    }

    pub(crate) fn deadline(&self) -> Option<tokio::time::Instant> {
        self.current
            .lock()
            .unwrap_or_else(|error| error.into_inner())
            .deadline
    }

    pub(crate) fn subscribe(&self) -> tokio::sync::watch::Receiver<bool> {
        self.changes.subscribe()
    }
}

#[derive(Debug)]
pub(crate) enum AdmissionRejection {
    NotReady,
    WrongTarget,
    Capacity,
}

impl From<AdmissionRejection> for tonic::Status {
    fn from(value: AdmissionRejection) -> Self {
        match value {
            AdmissionRejection::NotReady => Self::unavailable("model is not ready"),
            AdmissionRejection::WrongTarget => {
                Self::unavailable("required model weight target is not applied")
            }
            AdmissionRejection::Capacity => Self::resource_exhausted("too many native calls"),
        }
    }
}

pub(crate) const REQUIRED_TARGET_HEADER: &str = "x-chalk-model-weight-target";

fn valid_target(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
}

pub(crate) struct ServingPermit {
    state: Arc<ServingState>,
    completed: bool,
    started: bool,
}

impl ServingPermit {
    pub(crate) fn start(&mut self) {
        self.started = true;
    }
    pub(crate) fn complete(&mut self) {
        self.completed = true;
    }
}

impl Drop for ServingPermit {
    fn drop(&mut self) {
        let mut current = self
            .state
            .current
            .lock()
            .unwrap_or_else(|error| error.into_inner());
        current.active -= 1;
        // A dropped transport future cannot prove GPU work completed. The permit
        // lives inside the blocking Python task; an execution error poisons managed
        // admission so the supervisor restarts instead of applying into uncertainty.
        if self.started && !self.completed && self.state.require_target {
            current.failed = true;
            current.serving = false;
            self.state.changes.send_replace(false);
        }
        self.state.drained.notify_all();
    }
}

/// A thread-safe handle for model serving integrations to control gRPC
/// readiness and admission from Python.
#[pyclass(name = "ServingHandle")]
struct PyServingHandle {
    state: Arc<ServingState>,
}

#[pymethods]
impl PyServingHandle {
    #[new]
    #[pyo3(signature = (require_target=false))]
    fn new(require_target: bool) -> Self {
        Self {
            state: ServingState::new(false, require_target),
        }
    }

    /// Enable or disable health reporting and new RPC admission.
    #[pyo3(signature = (serving, lease_expires_at=None, target_fingerprint=None))]
    fn set_serving(
        &self,
        serving: bool,
        lease_expires_at: Option<f64>,
        target_fingerprint: Option<String>,
    ) -> PyResult<()> {
        self.state
            .set_serving(serving, lease_expires_at, target_fingerprint)
    }

    /// Wait for the actual Python executions after closing admission; release the GIL.
    fn wait_drained(&self, py: Python<'_>, timeout_seconds: f64) -> PyResult<bool> {
        if !timeout_seconds.is_finite() || !(0.0..=300.0).contains(&timeout_seconds) {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "timeout_seconds must be between 0 and 300",
            ));
        }
        py.detach(|| {
            self.state
                .wait_drained(Duration::from_secs_f64(timeout_seconds))
        })
        .map_err(pyo3::exceptions::PyRuntimeError::new_err)
    }

    #[getter]
    fn requires_target(&self) -> bool {
        self.state.require_target
    }

    #[getter]
    fn is_serving(&self) -> bool {
        self.state.is_serving()
    }
}

/// Start the tonic gRPC server.
///
/// This function blocks until the server shuts down (via SIGINT/SIGTERM).
/// The GIL is released while the server runs; it is re-acquired per handler call.
///
/// When `max_batching_size > 0`, the server coalesces up to `max_batching_size`
/// concurrent calls (or waits up to `max_buffer_duration_ms`, whichever comes
/// first) into a single handler invocation. The handler must accept
/// `(events: list[dict], contexts: list[dict]) -> list[result]` in that mode.
#[pyfunction]
#[pyo3(signature = (handler, process_fn, host, port, workers, arg_names=None, max_batching_size=0, max_buffer_duration_ms=0, serving_handle=None, require_weight_fence=false))]
#[allow(clippy::too_many_arguments)]
fn start_server(
    py: Python<'_>,
    handler: Py<PyAny>,
    process_fn: Py<PyAny>,
    host: String,
    port: u16,
    workers: usize,
    arg_names: Option<Vec<String>>,
    max_batching_size: usize,
    max_buffer_duration_ms: u64,
    serving_handle: Option<Py<PyServingHandle>>,
    require_weight_fence: bool,
) -> PyResult<()> {
    // Kubernetes consumes stdout/stderr as a machine-readable log stream. Keep
    // event fields flattened so collectors can read `level`, `target`,
    // `message`, and fields such as `error` without parsing terminal output.
    let _ = tracing_subscriber::fmt()
        .json()
        .flatten_event(true)
        .with_env_filter(
            EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .try_init();

    let serving_state = serving_handle.map(|handle| handle.borrow(py).state.clone());
    if require_weight_fence
        && !serving_state
            .as_ref()
            .is_some_and(|state| state.require_target)
    {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "require_weight_fence needs a target-fenced ServingHandle",
        ));
    }
    #[cfg(target_os = "linux")]
    if serving_state
        .as_ref()
        .is_some_and(|state| state.require_target)
    {
        if let Some(config) = self_consumer::SelfConsumerConfig::from_env() {
            if config.consumer_endpoint.is_none() {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "managed model queue execution requires the DP Fnq consumer endpoint",
                ));
            }
        }
    }
    let python_handler = Arc::new(PythonHandler::new(
        handler,
        process_fn,
        arg_names,
        serving_state.clone(),
    ));

    // Release the GIL while the Rust server runs
    py.detach(|| {
        let rt = tokio::runtime::Builder::new_multi_thread()
            .worker_threads(workers)
            .enable_all()
            .build()
            .map_err(|e| {
                pyo3::exceptions::PyRuntimeError::new_err(format!(
                    "Failed to create tokio runtime: {e}"
                ))
            })?;

        rt.block_on(async {
            // Linux-only: the self-consumer + its metrics pipeline depend on
            // chalk-queue / chalk_metrics, since these don't compile on macos
            // and windows. Built inside the runtime since it needs to `.await`.
            #[cfg(target_os = "linux")]
            let metrics = crate::metrics::init().await;

            let coalescing_queue = if max_batching_size > 0 {
                Some(CoalescingQueue::new(
                    Arc::clone(&python_handler),
                    max_batching_size,
                    max_buffer_duration_ms,
                    #[cfg(target_os = "linux")]
                    metrics.clone(),
                ))
            } else {
                None
            };

            let server = server::run_server(
                host,
                port,
                python_handler,
                coalescing_queue,
                serving_state,
                #[cfg(target_os = "linux")]
                metrics.clone(),
            );

            #[cfg(target_os = "linux")]
            {
                crate::metrics::run_with_metrics(metrics, server).await
            }
            #[cfg(not(target_os = "linux"))]
            {
                server.await
            }
        })
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Server error: {e}")))
    })
}

/// Native extension module for chalk-remote-call.
#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(start_server, m)?)?;
    m.add_class::<PyServingHandle>()?;
    Ok(())
}
