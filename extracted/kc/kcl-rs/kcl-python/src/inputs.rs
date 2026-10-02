//! The `*Input` `#[pyclass]`es passed into Python `RecordProcessor` callbacks.
//!
//! Mirrors `amazon_kclpy.messages`:
//! * [`InitializeInput`] — `shard_id`, `sequence_number`, `sub_sequence_number`
//! * [`ProcessRecordsInput`] — `records`, `millis_behind_latest`, `checkpointer`
//! * [`LeaseLostInput`] — (empty)
//! * [`ShardEndedInput`] — `checkpointer`
//! * [`ShutdownRequestedInput`] — `checkpointer`
//!
//! They are built from the Rust `kcl::lifecycle::events::*` inputs by
//! [`crate::processor::PyRecordProcessor`].

use pyo3::prelude::*;

use crate::checkpointer::Checkpointer;

/// Parameters to `RecordProcessorBase.initialize`.
///
/// Mirrors `amazon_kclpy.messages.InitializeInput`.
#[pyclass(module = "kcl_rs", name = "InitializeInput", frozen)]
pub struct InitializeInput {
    #[pyo3(get)]
    shard_id: Option<String>,
    #[pyo3(get)]
    sequence_number: Option<String>,
    #[pyo3(get)]
    sub_sequence_number: Option<i64>,
}

impl InitializeInput {
    pub fn new(
        shard_id: Option<String>,
        sequence_number: Option<String>,
        sub_sequence_number: Option<i64>,
    ) -> Self {
        Self {
            shard_id,
            sequence_number,
            sub_sequence_number,
        }
    }
}

#[pymethods]
impl InitializeInput {
    fn __repr__(&self) -> String {
        format!(
            "InitializeInput(shard_id={:?}, sequence_number={:?}, sub_sequence_number={:?})",
            self.shard_id, self.sequence_number, self.sub_sequence_number
        )
    }
}

/// Parameters to `RecordProcessorBase.process_records`.
///
/// Mirrors `amazon_kclpy.messages.ProcessRecordsInput`.
#[pyclass(module = "kcl_rs", name = "ProcessRecordsInput", frozen)]
pub struct ProcessRecordsInput {
    #[pyo3(get)]
    records: Py<pyo3::types::PyList>,
    #[pyo3(get)]
    millis_behind_latest: Option<i64>,
    #[pyo3(get)]
    checkpointer: Py<Checkpointer>,
}

impl ProcessRecordsInput {
    pub fn new(
        records: Py<pyo3::types::PyList>,
        millis_behind_latest: Option<i64>,
        checkpointer: Py<Checkpointer>,
    ) -> Self {
        Self {
            records,
            millis_behind_latest,
            checkpointer,
        }
    }
}

#[pymethods]
impl ProcessRecordsInput {
    fn __repr__(&self, py: Python<'_>) -> String {
        let n = self.records.bind(py).len();
        format!(
            "ProcessRecordsInput(records=[{} record(s)], millis_behind_latest={:?})",
            n, self.millis_behind_latest
        )
    }
}

/// Parameters to `RecordProcessorBase.lease_lost` (currently empty).
///
/// Mirrors `amazon_kclpy.messages.LeaseLostInput`.
#[pyclass(module = "kcl_rs", name = "LeaseLostInput", frozen)]
pub struct LeaseLostInput {}

#[pymethods]
impl LeaseLostInput {
    fn __repr__(&self) -> &'static str {
        "LeaseLostInput()"
    }
}

/// Parameters to `RecordProcessorBase.shard_ended`.
///
/// Mirrors `amazon_kclpy.messages.ShardEndedInput`.
#[pyclass(module = "kcl_rs", name = "ShardEndedInput", frozen)]
pub struct ShardEndedInput {
    #[pyo3(get)]
    checkpointer: Py<Checkpointer>,
}

impl ShardEndedInput {
    pub fn new(checkpointer: Py<Checkpointer>) -> Self {
        Self { checkpointer }
    }
}

#[pymethods]
impl ShardEndedInput {
    fn __repr__(&self) -> &'static str {
        "ShardEndedInput(...)"
    }
}

/// Parameters to `RecordProcessorBase.shutdown_requested`.
///
/// Mirrors `amazon_kclpy.messages.ShutdownRequestedInput`.
#[pyclass(module = "kcl_rs", name = "ShutdownRequestedInput", frozen)]
pub struct ShutdownRequestedInput {
    #[pyo3(get)]
    checkpointer: Py<Checkpointer>,
}

impl ShutdownRequestedInput {
    pub fn new(checkpointer: Py<Checkpointer>) -> Self {
        Self { checkpointer }
    }
}

#[pymethods]
impl ShutdownRequestedInput {
    fn __repr__(&self) -> &'static str {
        "ShutdownRequestedInput(...)"
    }
}
