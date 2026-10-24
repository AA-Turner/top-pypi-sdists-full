use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use chalk_remote_call_proto::chalk::common::v1::{ChalkError, ChalkException};
use chalk_remote_call_proto::chalk::runtime::v1::CallFunctionResponse;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyList};
use tokio::sync::{mpsc, Notify};
use tonic::Status;

/// Holds references to the Python handler and bridge function.
pub struct PythonHandler {
    /// The user's handler callable.
    handler: Py<PyAny>,
    /// Python bridge function — either `process_batches` (non-batched) or
    /// `process_batches_coalesced` (batched). The two bridges have different
    /// handler-shape contracts but accept structurally similar arg tuples.
    process_fn: Py<PyAny>,
    /// Optional column names from CHALK_INPUT_ARGS.
    arg_names: Option<Vec<String>>,
}

/// One caller's input: request bytes + function name + gRPC metadata + peer address.
/// Used identically in both the single-request and coalesced paths; the
/// coalesced path just has N of them.
pub struct CallerInput {
    pub ipc_bytes: Vec<u8>,
    pub function_name: String,
    pub metadata: HashMap<String, String>,
    pub peer: String,
}

impl PythonHandler {
    pub fn new(handler: Py<PyAny>, process_fn: Py<PyAny>, arg_names: Option<Vec<String>>) -> Self {
        Self {
            handler,
            process_fn,
            arg_names,
        }
    }

    /// Run the handler on a blocking thread, building the per-call emitter via
    /// `make_emitter`. Shared by `call_streaming` (emits onto an mpsc channel
    /// feeding the gRPC response stream) and `call_into_buffer` (writes straight
    /// into a shared buffer). The only difference between the two paths is which
    /// emitter object `process_batches` is handed.
    async fn call_with_emitter<F>(
        self: &Arc<Self>,
        ipc_bytes: Vec<u8>,
        function_name: String,
        metadata: HashMap<String, String>,
        peer: String,
        make_emitter: F,
    ) -> Result<(), PythonError>
    where
        F: FnOnce(Python<'_>) -> PyResult<Py<PyAny>> + Send + 'static,
    {
        // GIL acquisition can block, so only clone the Rust owner on the runtime worker.
        let owner = Arc::clone(self);
        tokio::task::spawn_blocking(move || {
            Python::attach(|py| -> Result<(), PythonError> {
                let handler = owner.handler.clone_ref(py);
                let process_fn = &owner.process_fn;
                let arg_names = &owner.arg_names;
                let py_bytes = PyBytes::new(py, &ipc_bytes).into_any().unbind();
                let py_ctx = build_context(py, &function_name, &metadata, &peer)?
                    .into_any()
                    .unbind();
                let py_arg_names = build_arg_names(py, arg_names.as_deref())?;
                let emitter = make_emitter(py).map_err(|e| into_python_error(py, e))?;

                process_fn
                    .call1(py, (py_bytes, handler, py_arg_names, py_ctx, emitter))
                    .map_err(|e| into_python_error(py, e))?;
                Ok(())
            })
        })
        .await
        .map_err(|e| PythonError::new(format!("Task join error: {e}")))?
    }

    /// Non-batched streaming dispatch. Calls `process_batches(..., emit)` so
    /// generator results are sent to the gRPC stream as each yield is encoded.
    pub async fn call_streaming(
        self: &Arc<Self>,
        ipc_bytes: Vec<u8>,
        function_name: String,
        metadata: HashMap<String, String>,
        peer: String,
        response_tx: mpsc::Sender<Result<CallFunctionResponse, Status>>,
    ) -> Result<(), PythonError> {
        self.call_with_emitter(ipc_bytes, function_name, metadata, peer, move |py| {
            Ok(Py::new(py, ChunkEmitter { response_tx })?.into_any())
        })
        .await
    }

    /// Non-batched dispatch for the async (enqueue/poll) path: each emitted
    /// chunk is appended directly to `buffer`. There is no channel and nothing
    /// to drain — the caller marks the call terminal from this function's return
    /// value, so completion never depends on emitter teardown timing (which is
    /// what caused a Python 3.10 hang in the channel-drain version).
    pub async fn call_into_buffer(
        self: &Arc<Self>,
        ipc_bytes: Vec<u8>,
        function_name: String,
        metadata: HashMap<String, String>,
        peer: String,
        buffer: Arc<Mutex<ChunkBuffer>>,
    ) -> Result<(), PythonError> {
        self.call_with_emitter(ipc_bytes, function_name, metadata, peer, move |py| {
            Ok(Py::new(py, BufferEmitter { buffer })?.into_any())
        })
        .await
    }

    /// Coalesced: N callers merged into one invocation. Dispatches to
    /// `process_batches_coalesced`. Returns one IPC-encoded response per
    /// caller, in input order.
    pub async fn call_coalesced(
        self: &Arc<Self>,
        callers: Vec<CallerInput>,
    ) -> Result<Vec<Vec<u8>>, PythonError> {
        // GIL acquisition can block, so only clone the Rust owner on the runtime worker.
        let owner = Arc::clone(self);
        tokio::task::spawn_blocking(move || {
            Python::attach(|py| -> Result<Vec<Vec<u8>>, PythonError> {
                let handler = &owner.handler;
                let process_fn = &owner.process_fn;
                let arg_names = &owner.arg_names;
                let py_inputs = PyList::empty(py);
                let py_contexts = PyList::empty(py);
                for c in &callers {
                    py_inputs
                        .append(PyBytes::new(py, &c.ipc_bytes))
                        .map_err(|e| into_python_error(py, e))?;
                    py_contexts
                        .append(build_context(py, &c.function_name, &c.metadata, &c.peer)?)
                        .map_err(|e| into_python_error(py, e))?;
                }
                let py_arg_names = build_arg_names(py, arg_names.as_deref())?;
                invoke_process_fn(
                    py,
                    process_fn,
                    handler,
                    py_inputs.into_any().unbind(),
                    py_arg_names,
                    py_contexts.into_any().unbind(),
                )
            })
        })
        .await
        .map_err(|e| PythonError::new(format!("Task join error: {e}")))?
    }
}

// ---- Shared helpers -------------------------------------------------------

#[pyclass]
struct ChunkEmitter {
    response_tx: mpsc::Sender<Result<CallFunctionResponse, Status>>,
}

#[pymethods]
impl ChunkEmitter {
    fn __call__(&self, py: Python<'_>, chunk: &Bound<'_, PyBytes>) -> PyResult<()> {
        // Copy the bytes out of Python memory before releasing the GIL.
        let msg = CallFunctionResponse {
            feather_stream: chunk.as_bytes().to_vec().into(),
        };
        // Release the GIL while parked in blocking_send so a backpressured
        // client can't stall every other request's Python execution. Collapse
        // the (large) SendError to `()` inside the closure so it isn't carried
        // across the detach boundary.
        py.detach(|| self.response_tx.blocking_send(Ok(msg)).map_err(|_| ()))
            .map_err(|()| pyo3::exceptions::PyRuntimeError::new_err("client disconnected"))?;
        Ok(())
    }
}

/// Shared sink for one async call's emitted chunks. The enqueue/poll path hands
/// a clone to the handler's emitter (chunks are appended straight in) and reads
/// it back on poll. Chunks are only appended, so a chunk's index is its stable
/// poll cursor position. The notify is signaled whenever a chunk is appended, so
/// the flush loop can wait on new data instead of polling on a tick.
/// Clone is cheap: Arc<Notify> and Vec both clone cheaply, so cloning this struct
/// just increments Arc reference counts and copies the vector metadata.
#[derive(Clone)]
pub struct ChunkBuffer {
    chunks: Vec<CallFunctionResponse>,
    notify: Arc<Notify>,
}

impl ChunkBuffer {
    pub fn new() -> Self {
        Self {
            chunks: Vec::new(),
            notify: Arc::new(Notify::new()),
        }
    }

    pub fn into_shared(self) -> Arc<Mutex<Self>> {
        Arc::new(Mutex::new(self))
    }

    pub fn len(&self) -> usize {
        self.chunks.len()
    }

    pub fn chunks(&self) -> &[CallFunctionResponse] {
        &self.chunks
    }

    pub fn push(&mut self, chunk: CallFunctionResponse) {
        self.chunks.push(chunk);
        self.notify.notify_one();
    }

    // Only the Linux self-consumer waits on this notify (the streaming flush
    // loop); on macOS/Windows that module is gated out, leaving this unused.
    #[cfg_attr(not(target_os = "linux"), allow(dead_code))]
    pub fn notify_handle(&self) -> Arc<Notify> {
        self.notify.clone()
    }
}

/// Emitter for the async path: appends each chunk directly into the shared
/// per-call buffer. Unlike [`ChunkEmitter`] there is no channel, so there is no
/// backpressure (the buffer-and-poll model wants the handler to run to
/// completion) and no teardown ordering to coordinate.
#[pyclass]
struct BufferEmitter {
    buffer: Arc<Mutex<ChunkBuffer>>,
}

#[pymethods]
impl BufferEmitter {
    fn __call__(&self, py: Python<'_>, chunk: &Bound<'_, PyBytes>) -> PyResult<()> {
        // Copy the bytes out of Python memory before releasing the GIL.
        let msg = CallFunctionResponse {
            feather_stream: chunk.as_bytes().to_vec().into(),
        };
        // Release the GIL while holding the short-lived per-call buffer lock, so
        // a concurrent poll on the same call can't stall handler execution.
        py.detach(|| {
            if let Ok(mut buf) = self.buffer.lock() {
                buf.push(msg);
            }
        });
        Ok(())
    }
}

/// Build a `{"function_name": str, "peer": str, "metadata": dict}` context dict for one caller.
fn build_context<'py>(
    py: Python<'py>,
    function_name: &str,
    metadata: &HashMap<String, String>,
    peer: &str,
) -> Result<Bound<'py, PyDict>, PythonError> {
    let meta_dict = PyDict::new(py);
    for (k, v) in metadata {
        meta_dict
            .set_item(k, v)
            .map_err(|e| into_python_error(py, e))?;
    }
    let ctx = PyDict::new(py);
    ctx.set_item("function_name", function_name)
        .map_err(|e| into_python_error(py, e))?;
    ctx.set_item("peer", peer)
        .map_err(|e| into_python_error(py, e))?;
    ctx.set_item("metadata", meta_dict)
        .map_err(|e| into_python_error(py, e))?;
    Ok(ctx)
}

/// Build the `arg_names: list[str] | None` Python argument.
fn build_arg_names(py: Python<'_>, arg_names: Option<&[String]>) -> Result<Py<PyAny>, PythonError> {
    match arg_names {
        Some(names) => {
            let list = PyList::new(py, names).map_err(|e| into_python_error(py, e))?;
            Ok(list.into_any().unbind())
        }
        None => Ok(py.None()),
    }
}

/// Call the bound Python bridge function with the standard 4-tuple and
/// extract its `list[bytes]` response.
///
/// The bridge contract (identical for both `process_batches` and
/// `process_batches_coalesced`) is:
///   process_fn(input, handler, arg_names, context) -> list[bytes]
/// where `input` is `bytes` or `list[bytes]` and `context` is `dict` or
/// `list[dict]` respectively.
fn invoke_process_fn(
    py: Python<'_>,
    process_fn: &Py<PyAny>,
    handler: &Py<PyAny>,
    input: Py<PyAny>,
    arg_names: Py<PyAny>,
    context: Py<PyAny>,
) -> Result<Vec<Vec<u8>>, PythonError> {
    let result = process_fn
        .call1(py, (input, handler, arg_names, context))
        .map_err(|e| into_python_error(py, e))?;

    let result_list: &Bound<'_, PyList> = result
        .bind(py)
        .cast::<PyList>()
        .map_err(|e| PythonError::new(format!("bridge must return a list, got: {e}")))?;

    let mut out = Vec::with_capacity(result_list.len());
    for item in result_list.iter() {
        let bytes_ref: &Bound<'_, PyBytes> = item.cast::<PyBytes>().map_err(|e| {
            PythonError::new(format!("bridge must return list[bytes], got item: {e}"))
        })?;
        out.push(bytes_ref.as_bytes().to_vec());
    }
    Ok(out)
}

/// Error type for Python handler invocations.
#[derive(Debug)]
pub struct PythonError {
    details: String,
    wire_message: String,
}

impl PythonError {
    fn new(message: String) -> Self {
        Self {
            details: message.clone(),
            wire_message: message,
        }
    }

    pub fn details(&self) -> &str {
        &self.details
    }

    pub fn chalk_error(&self) -> ChalkError {
        let exception = serde_json::from_str::<serde_json::Value>(&self.wire_message)
            .ok()
            .and_then(|payload| {
                let exception = payload.get("exception")?;
                Some(ChalkException {
                    kind: exception.get("kind")?.as_str()?.to_string(),
                    message: exception.get("message")?.as_str()?.to_string(),
                    stacktrace: exception.get("stacktrace")?.as_str()?.to_string(),
                    internal_stacktrace: exception
                        .get("internal_stacktrace")?
                        .as_str()?
                        .to_string(),
                })
            });
        ChalkError {
            message: self.wire_message.clone(),
            exception,
            ..Default::default()
        }
    }
}

impl std::fmt::Display for PythonError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.wire_message)
    }
}

fn into_python_error(py: Python<'_>, err: PyErr) -> PythonError {
    let summary = err.to_string();
    let details = format_python_traceback(py, &err).unwrap_or_else(|_| summary.clone());
    let wire_message = py
        .import("chalk_remote_call.errors")
        .and_then(|module| module.call_method1("serialize_exception", (err.value(py),)))
        .and_then(|value| value.extract::<String>())
        .unwrap_or_else(|_| details.clone());
    PythonError {
        details,
        wire_message,
    }
}

fn format_python_traceback(py: Python<'_>, err: &PyErr) -> PyResult<String> {
    let traceback = py.import("traceback")?;
    let formatted = traceback.call_method1(
        "format_exception",
        (err.get_type(py), err.value(py), err.traceback(py)),
    )?;
    let lines: Vec<String> = formatted.extract()?;
    Ok(lines.concat().trim_end().to_string())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::future::{poll_fn, Future};
    use std::task::Poll;
    use std::time::Duration;

    #[derive(Clone, Copy)]
    enum Dispatch {
        Streaming,
        Buffered,
        Coalesced,
    }

    // Polling a dispatch must yield even while another thread owns the GIL:
    // otherwise Python contention blocks the worker that also serves health RPCs.
    fn dispatch_yields_while_gil_is_held(dispatch: Dispatch) {
        Python::initialize();
        let (yielded, worker) = Python::attach(|py| {
            let handler = Arc::new(PythonHandler::new(
                py.None(),
                py.eval(pyo3::ffi::c_str!("lambda *args: []"), None, None)
                    .unwrap()
                    .unbind(),
                None,
            ));
            let (polled_tx, polled_rx) = std::sync::mpsc::channel();
            let worker = std::thread::spawn(move || {
                let runtime = tokio::runtime::Builder::new_current_thread()
                    .build()
                    .unwrap();
                runtime.block_on(async move {
                    let call = async {
                        match dispatch {
                            Dispatch::Streaming => {
                                let (tx, _rx) = mpsc::channel(1);
                                handler
                                    .call_streaming(
                                        Vec::new(),
                                        String::new(),
                                        HashMap::new(),
                                        String::new(),
                                        tx,
                                    )
                                    .await
                            }
                            Dispatch::Buffered => {
                                handler
                                    .call_into_buffer(
                                        Vec::new(),
                                        String::new(),
                                        HashMap::new(),
                                        String::new(),
                                        ChunkBuffer::new().into_shared(),
                                    )
                                    .await
                            }
                            Dispatch::Coalesced => {
                                handler.call_coalesced(Vec::new()).await.map(|_| ())
                            }
                        }
                    };
                    tokio::pin!(call);
                    poll_fn(|cx| {
                        assert!(call.as_mut().poll(cx).is_pending());
                        let _ = polled_tx.send(());
                        Poll::Ready(())
                    })
                    .await;
                    call.await.unwrap();
                });
            });
            // No Python bytecode runs here, so CPython cannot periodically release
            // the GIL and accidentally let a blocking attach pass the test.
            let yielded = polled_rx.recv_timeout(Duration::from_secs(5)).is_ok();
            (yielded, worker)
        });
        // Release the GIL before joining so even a regressed implementation exits.
        worker.join().unwrap();
        assert!(
            yielded,
            "dispatch blocked its Tokio worker acquiring the GIL"
        );
    }

    #[test]
    fn streaming_dispatch_yields_under_gil_contention() {
        dispatch_yields_while_gil_is_held(Dispatch::Streaming);
    }

    #[test]
    fn buffered_dispatch_yields_under_gil_contention() {
        dispatch_yields_while_gil_is_held(Dispatch::Buffered);
    }

    #[test]
    fn coalesced_dispatch_yields_under_gil_contention() {
        dispatch_yields_while_gil_is_held(Dispatch::Coalesced);
    }
}
