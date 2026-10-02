mod async_service;
mod coalesce;
// The self-consumer and its metrics pipeline run only on the Linux scaling-group
// pods (they need the dataplane Redis). Their deps (chalk-queue / chalk_metrics →
// rdkafka's cyrus-sasl, chalk-protos' protoc) don't build on Windows and need
// extra native tooling on macOS, so they're Linux-only — keeping the gRPC
// server/client portable to every platform.
#[cfg(target_os = "linux")]
mod metrics;
mod python_bridge;
#[cfg(target_os = "linux")]
mod self_consumer;
mod server;
mod service;

use std::sync::Arc;

use pyo3::prelude::*;
use tracing_subscriber::EnvFilter;

use crate::coalesce::CoalescingQueue;
use crate::python_bridge::PythonHandler;

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
#[pyo3(signature = (handler, process_fn, host, port, workers, arg_names=None, max_batching_size=0, max_buffer_duration_ms=0))]
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

    let python_handler = Arc::new(PythonHandler::new(handler, process_fn, arg_names));

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
            let pipeline = crate::metrics::init_pipeline().await;

            let coalescing_queue = if max_batching_size > 0 {
                Some(CoalescingQueue::new(
                    Arc::clone(&python_handler),
                    max_batching_size,
                    max_buffer_duration_ms,
                    #[cfg(target_os = "linux")]
                    pipeline.clone(),
                ))
            } else {
                None
            };

            server::run_server(
                host,
                port,
                python_handler,
                coalescing_queue,
                #[cfg(target_os = "linux")]
                pipeline,
            )
            .await
        })
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Server error: {e}")))
    })
}

/// Native extension module for chalk-remote-call.
#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(start_server, m)?)?;
    Ok(())
}
