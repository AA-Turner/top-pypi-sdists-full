//! The Rust<->Python bridge for the record-processing SPI.
//!
//! * [`PyRecordProcessor`] wraps a Python `RecordProcessor` object and implements
//!   the *synchronous* Rust [`ShardRecordProcessor`] trait. Each callback
//!   acquires the GIL (`Python::with_gil`), builds the matching input pyclass,
//!   invokes the Python method, and — mirroring `amazon_kclpy`'s
//!   `KCLProcess._perform_action` — logs and *swallows* any Python exception so
//!   one bad callback cannot crash the worker.
//! * [`PyRecordProcessorFactory`] wraps a Python factory (a callable, or an
//!   object with a `shard_record_processor()` method) and implements the Rust
//!   [`ShardRecordProcessorFactory`] trait, producing a fresh `PyRecordProcessor`
//!   per shard.
//!
//! GIL model: these are the *only* places the KCL touches Python. The core
//! lifecycle invokes the sync `ShardRecordProcessor` trait via `spawn_blocking`
//! (off the tokio worker threads), so acquiring the GIL here never blocks the
//! runtime's async workers.

use std::sync::Arc;

use pyo3::prelude::*;
use pyo3::types::PyList;

use kcl::lifecycle::events::{
    InitializationInput, LeaseLostInput as RustLeaseLostInput, ProcessRecordsInput,
    ShardEndedInput, ShutdownRequestedInput,
};
use kcl::processor::{
    RecordProcessorCheckpointer, ShardRecordProcessor, ShardRecordProcessorFactory,
};

use crate::checkpointer::Checkpointer;
use crate::inputs;
use crate::record::Record;

/// Log a Python exception to stderr and swallow it, mirroring
/// `amazon_kclpy.kcl.KCLProcess._perform_action` (which catches client
/// exceptions so one bad callback doesn't crash the worker).
fn log_and_swallow(py: Python<'_>, context: &str, err: PyErr) {
    // Print the traceback to stderr (the interpreter's `sys.stderr`) if possible.
    err.print(py);
    eprintln!("kcl_rs: caught exception from RecordProcessor.{context}: {err}");
}

/// Wraps a Python `RecordProcessor` object and implements the sync Rust
/// [`ShardRecordProcessor`] trait. `Py<PyAny>` is `Send + Sync`, so this struct
/// is `Send` as the trait object requires.
pub struct PyRecordProcessor {
    /// The Python `RecordProcessor` instance.
    py_processor: Py<PyAny>,
}

impl PyRecordProcessor {
    /// Wrap an already-constructed Python `RecordProcessor` object.
    pub fn new(py_processor: Py<PyAny>) -> Self {
        Self { py_processor }
    }

    /// Invoke `self.py_processor.<method>(input)`, swallowing any exception.
    fn call_method1(&self, py: Python<'_>, method: &str, input: Py<PyAny>) {
        let obj = self.py_processor.bind(py);
        match obj.call_method1(method, (input,)) {
            Ok(_) => {}
            Err(err) => log_and_swallow(py, method, err),
        }
    }
}

impl ShardRecordProcessor for PyRecordProcessor {
    fn initialize(&mut self, initialization_input: InitializationInput) {
        Python::attach(|py| {
            let (seq, sub) = match initialization_input.extended_sequence_number() {
                Some(esn) => (
                    Some(esn.sequence_number().to_string()),
                    Some(esn.sub_sequence_number()),
                ),
                None => (None, None),
            };
            let input = inputs::InitializeInput::new(
                initialization_input.shard_id().map(str::to_owned),
                seq,
                sub,
            );
            match Py::new(py, input) {
                Ok(obj) => self.call_method1(py, "initialize", obj.into_any()),
                Err(err) => log_and_swallow(py, "initialize", err),
            }
        });
    }

    fn process_records(&mut self, process_records_input: ProcessRecordsInput) {
        Python::attach(|py| {
            // Build the list of Record pyclasses.
            let py_records: Vec<Py<Record>> = match process_records_input.records() {
                Some(records) => {
                    let mut v = Vec::with_capacity(records.len());
                    for r in records {
                        match Py::new(py, Record::from_kinesis_client_record(r)) {
                            Ok(obj) => v.push(obj),
                            Err(err) => {
                                log_and_swallow(py, "process_records", err);
                                return;
                            }
                        }
                    }
                    v
                }
                None => Vec::new(),
            };
            let list = match PyList::new(py, py_records) {
                Ok(l) => l.unbind(),
                Err(err) => {
                    log_and_swallow(py, "process_records", err);
                    return;
                }
            };

            // Attach the checkpointer (if any). If the batch carries no
            // checkpointer (shouldn't happen for process_records), we still
            // build one only when present.
            let checkpointer = match process_records_input.checkpointer() {
                Some(cp) => cp.clone(),
                None => {
                    // No checkpointer supplied: skip the callback gracefully.
                    eprintln!("kcl_rs: process_records called without a checkpointer; skipping");
                    return;
                }
            };
            let py_cp = match Py::new(py, Checkpointer::new(checkpointer)) {
                Ok(c) => c,
                Err(err) => {
                    log_and_swallow(py, "process_records", err);
                    return;
                }
            };

            let input = inputs::ProcessRecordsInput::new(
                list,
                process_records_input.millis_behind_latest(),
                py_cp,
            );
            match Py::new(py, input) {
                Ok(obj) => self.call_method1(py, "process_records", obj.into_any()),
                Err(err) => log_and_swallow(py, "process_records", err),
            }
        });
    }

    fn lease_lost(&mut self, _lease_lost_input: RustLeaseLostInput) {
        Python::attach(|py| match Py::new(py, inputs::LeaseLostInput {}) {
            Ok(obj) => self.call_method1(py, "lease_lost", obj.into_any()),
            Err(err) => log_and_swallow(py, "lease_lost", err),
        });
    }

    fn shard_ended(&mut self, shard_ended_input: ShardEndedInput) {
        Python::attach(|py| {
            let cp: Arc<dyn RecordProcessorCheckpointer + Send + Sync> =
                shard_ended_input.checkpointer().clone();
            let py_cp = match Py::new(py, Checkpointer::new(cp)) {
                Ok(c) => c,
                Err(err) => {
                    log_and_swallow(py, "shard_ended", err);
                    return;
                }
            };
            match Py::new(py, inputs::ShardEndedInput::new(py_cp)) {
                Ok(obj) => self.call_method1(py, "shard_ended", obj.into_any()),
                Err(err) => log_and_swallow(py, "shard_ended", err),
            }
        });
    }

    fn shutdown_requested(&mut self, shutdown_requested_input: ShutdownRequestedInput) {
        Python::attach(|py| {
            let cp: Arc<dyn RecordProcessorCheckpointer + Send + Sync> =
                shutdown_requested_input.checkpointer().clone();
            let py_cp = match Py::new(py, Checkpointer::new(cp)) {
                Ok(c) => c,
                Err(err) => {
                    log_and_swallow(py, "shutdown_requested", err);
                    return;
                }
            };
            match Py::new(py, inputs::ShutdownRequestedInput::new(py_cp)) {
                Ok(obj) => self.call_method1(py, "shutdown_requested", obj.into_any()),
                Err(err) => log_and_swallow(py, "shutdown_requested", err),
            }
        });
    }
}

/// Wraps a Python factory and implements the Rust
/// [`ShardRecordProcessorFactory`] trait.
///
/// The Python factory may be:
/// * a **callable** (e.g. a class or a lambda) — invoked as `factory()`, or
/// * an **object with a `shard_record_processor()` method** — invoked as
///   `factory.shard_record_processor()`.
///
/// Either way it must return a fresh Python `RecordProcessor` object per call.
pub struct PyRecordProcessorFactory {
    py_factory: Py<PyAny>,
}

impl PyRecordProcessorFactory {
    /// Wrap a Python factory object.
    pub fn new(py_factory: Py<PyAny>) -> Self {
        Self { py_factory }
    }

    /// Create a new Python `RecordProcessor` by invoking the factory. Panics
    /// (with a descriptive message) if the factory raises — this is a
    /// programming error at wiring time, not a per-record client error, so it
    /// should surface loudly rather than be swallowed. The panic unwinds the
    /// scheduler run-loop task; `Scheduler.run()` / `Scheduler.shutdown()` on
    /// the Python side observe the crashed task and raise `RuntimeError`.
    fn make_processor(&self) -> Py<PyAny> {
        Python::attach(|py| {
            let factory = self.py_factory.bind(py);
            // Prefer an explicit `shard_record_processor()` method; fall back to
            // calling the factory directly (a class or callable).
            let result = if factory.hasattr("shard_record_processor").unwrap_or(false) {
                factory.call_method0("shard_record_processor")
            } else {
                factory.call((), None)
            };
            match result {
                Ok(obj) => obj.unbind(),
                Err(err) => {
                    err.print(py);
                    panic!(
                        "kcl_rs: RecordProcessor factory raised an exception \
                         (traceback above); the shard consumer aborts and the \
                         scheduler run loop crashes — surfaced by run()/shutdown() \
                         as RuntimeError: {err}"
                    );
                }
            }
        })
    }
}

impl ShardRecordProcessorFactory for PyRecordProcessorFactory {
    fn shard_record_processor(&self) -> Box<dyn ShardRecordProcessor + Send + Sync> {
        Box::new(PyRecordProcessor::new(self.make_processor()))
    }
}

// `PyRecordProcessor` must be `Send + Sync` to satisfy the factory return type.
// `Py<PyAny>` is `Send + Sync`, so this holds. (Enforced at the trait boundary.)
// The `#[allow]` keeps a compile-time assertion cheap and explicit.
#[allow(dead_code)]
fn _assert_send_sync() {
    fn is_send_sync<T: Send + Sync>() {}
    is_send_sync::<PyRecordProcessor>();
    is_send_sync::<PyRecordProcessorFactory>();
}
