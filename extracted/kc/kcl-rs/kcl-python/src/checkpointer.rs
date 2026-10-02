//! The `Checkpointer` `#[pyclass]` and the `CheckpointError` exception.
//!
//! Wraps `Arc<dyn RecordProcessorCheckpointer + Send + Sync>` and exposes the
//! single `checkpoint(sequence_number=None, sub_sequence_number=None)` method,
//! mirroring `amazon_kclpy.kcl.Checkpointer.checkpoint`. Errors from the sync
//! Rust checkpointer ([`KinesisClientLibError`]) are mapped to a Python
//! `CheckpointError` whose `value` is the Java-style exception name (e.g.
//! `"ShutdownException"`, `"ThrottlingException"`, `"InvalidStateException"`),
//! so existing `amazon_kclpy`-style retry logic (`if e.value == 'ShutdownException'`)
//! keeps working.

use std::sync::Arc;
use std::sync::Mutex;

use pyo3::create_exception;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;

use kcl::exceptions::KinesisClientLibError;
use kcl::processor::{
    PreparedCheckpointer as KclPreparedCheckpointer, RecordProcessorCheckpointer,
};

create_exception!(
    kcl_rs,
    CheckpointError,
    PyException,
    "Raised when a checkpoint operation fails.\n\n\
     The exception's `value` attribute (and `str(e)`) is the Java-style error\n\
     name, e.g. `ShutdownException`, `ThrottlingException`,\n\
     `InvalidStateException`, `KinesisClientLibDependencyException`. Mirrors\n\
     `amazon_kclpy.kcl.CheckpointError` (whose `__init__` stores it on `.value`)."
);

/// Map a Rust [`KinesisClientLibError`] to a Python `CheckpointError`.
///
/// The exception's message (`str(e)`) is the Java-style exception name, and the
/// same name is also set as a `value` attribute on the instance: in
/// `amazon_kclpy`, `CheckpointError.__init__(self, value)` stores its argument
/// on `self.value`, and ported retry logic compares
/// `e.value == 'ShutdownException'`. A `create_exception!` class has no such
/// attribute by itself, so it is set explicitly at raise time.
pub fn checkpoint_error(err: &KinesisClientLibError) -> PyErr {
    let name = match err {
        KinesisClientLibError::InvalidState { .. } => "InvalidStateException",
        KinesisClientLibError::Shutdown { .. } => "ShutdownException",
        KinesisClientLibError::Throttling { .. } => "ThrottlingException",
        KinesisClientLibError::Dependency { .. } => "KinesisClientLibDependencyException",
        KinesisClientLibError::BlockedOnParentShard { .. } => "BlockedOnParentShardException",
        KinesisClientLibError::Io { .. } => "KinesisClientLibIOException",
    };
    Python::attach(|py| {
        let exc = CheckpointError::new_err(name);
        if let Err(set_err) = exc.value(py).setattr("value", name) {
            // Extraordinarily unlikely; keep the original error either way.
            set_err.print(py);
        }
        exc
    })
}

/// A checkpointer handed to Python `process_records` / `shard_ended` /
/// `shutdown_requested` callbacks.
///
/// Mirrors `amazon_kclpy.kcl.Checkpointer`. Holds the Rust checkpointer as an
/// `Arc<dyn RecordProcessorCheckpointer + Send + Sync>`; each `checkpoint(...)`
/// call runs the *synchronous* Rust checkpoint under the current GIL (the caller
/// is already on a `spawn_blocking` worker thread, so this does not block the
/// tokio runtime).
#[pyclass(module = "kcl_rs", name = "Checkpointer", frozen)]
pub struct Checkpointer {
    inner: Arc<dyn RecordProcessorCheckpointer + Send + Sync>,
}

impl Checkpointer {
    /// Wrap a Rust checkpointer for exposure to Python.
    pub fn new(inner: Arc<dyn RecordProcessorCheckpointer + Send + Sync>) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Checkpointer {
    /// Checkpoint the record processor's progress.
    ///
    /// * no args → checkpoint at the last delivered record (Rust `checkpoint()`),
    /// * `sequence_number` only → `checkpoint_sequence(seq)`,
    /// * `sequence_number` + `sub_sequence_number` → `checkpoint_sequence_sub(seq, sub)`.
    ///
    /// Raises `CheckpointError` on failure (the `value` is the Java-style
    /// exception name). Mirrors `amazon_kclpy.kcl.Checkpointer.checkpoint`.
    #[pyo3(signature = (sequence_number=None, sub_sequence_number=None))]
    fn checkpoint(
        &self,
        py: Python<'_>,
        sequence_number: Option<String>,
        sub_sequence_number: Option<i64>,
    ) -> PyResult<()> {
        // Release the GIL while the synchronous Rust checkpoint runs (it may
        // touch DynamoDB via the sync->async bridge). Nothing here re-enters
        // Python, so this is safe and keeps the interpreter responsive.
        let result = py.detach(|| match (sequence_number, sub_sequence_number) {
            (None, _) => self.inner.checkpoint(),
            (Some(seq), None) => self.inner.checkpoint_sequence(&seq),
            (Some(seq), Some(sub)) => self.inner.checkpoint_sequence_sub(&seq, sub),
        });
        result.map_err(|e| checkpoint_error(&e))
    }

    /// Prepare a two-phase (pending) checkpoint and return a
    /// [`PreparedCheckpointer`] whose `checkpoint()` commits it.
    ///
    /// * no args → prepare at the last delivered record (Rust `prepare_checkpoint()`),
    /// * `sequence_number` only → `prepare_checkpoint_sequence(seq)`,
    /// * `sequence_number` + `sub_sequence_number` → `prepare_checkpoint_sequence_sub(seq, sub)`.
    ///
    /// Preparing durably records the pending checkpoint; the returned object's
    /// `checkpoint()` commits it (enabling idempotent side effects across
    /// failover). Raises `CheckpointError` on failure (the `value` is the
    /// Java-style exception name).
    #[pyo3(signature = (sequence_number=None, sub_sequence_number=None))]
    fn prepare_checkpoint(
        &self,
        py: Python<'_>,
        sequence_number: Option<String>,
        sub_sequence_number: Option<i64>,
    ) -> PyResult<PreparedCheckpointer> {
        // Release the GIL while the synchronous Rust prepare runs (it may touch
        // DynamoDB via the sync->async bridge). Nothing here re-enters Python.
        let prepared = py.detach(|| match (sequence_number, sub_sequence_number) {
            (None, _) => self.inner.prepare_checkpoint(),
            (Some(seq), None) => self.inner.prepare_checkpoint_sequence(&seq),
            (Some(seq), Some(sub)) => self.inner.prepare_checkpoint_sequence_sub(&seq, sub),
        });
        prepared
            .map(PreparedCheckpointer::new)
            .map_err(|e| checkpoint_error(&e))
    }

    fn __repr__(&self) -> &'static str {
        "Checkpointer(...)"
    }
}

/// A two-phase "pending" checkpoint returned by
/// [`Checkpointer::prepare_checkpoint`].
///
/// Mirrors the `IPreparedCheckpointer` concept from the Java KCL. Holds the Rust
/// [`kcl::processor::PreparedCheckpointer`] as a `Box<dyn ... + Send + Sync>`;
/// calling [`checkpoint`](Self::checkpoint) commits the pending checkpoint.
///
/// The box is behind a `Mutex` so the pyclass is `Sync` (required by a non-
/// `unsendable`, `frozen` `#[pyclass]`); the Rust `checkpoint()` takes `&self`,
/// so `checkpoint()` may be called more than once (the second commit is subject
/// to the same monotonicity validation as any checkpoint).
#[pyclass(module = "kcl_rs", name = "PreparedCheckpointer", frozen)]
pub struct PreparedCheckpointer {
    inner: Mutex<Box<dyn KclPreparedCheckpointer + Send + Sync>>,
}

impl PreparedCheckpointer {
    /// Wrap a Rust prepared checkpointer for exposure to Python.
    pub fn new(inner: Box<dyn KclPreparedCheckpointer + Send + Sync>) -> Self {
        Self {
            inner: Mutex::new(inner),
        }
    }
}

#[pymethods]
impl PreparedCheckpointer {
    /// Commit the pending checkpoint.
    ///
    /// Raises `CheckpointError` on failure (the `value` is the Java-style
    /// exception name), mirroring `Checkpointer.checkpoint`.
    fn checkpoint(&self, py: Python<'_>) -> PyResult<()> {
        // Release the GIL while the synchronous Rust commit runs. Nothing here
        // re-enters Python, so this is safe.
        let result = py.detach(|| self.inner.lock().unwrap().checkpoint());
        result.map_err(|e| checkpoint_error(&e))
    }

    /// The sequence number of the pending checkpoint (`sequence_number`,
    /// `sub_sequence_number`).
    #[getter]
    fn pending_checkpoint(&self) -> (String, i64) {
        let esn = self.inner.lock().unwrap().pending_checkpoint();
        (esn.sequence_number().to_string(), esn.sub_sequence_number())
    }

    fn __repr__(&self) -> String {
        let (seq, sub) = self.pending_checkpoint();
        format!("PreparedCheckpointer(sequence_number={seq:?}, sub_sequence_number={sub})")
    }
}
