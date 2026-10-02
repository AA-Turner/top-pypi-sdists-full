//! The `Record` `#[pyclass]` exposed to Python `process_records` callbacks.
//!
//! Mirrors `amazon_kclpy.messages.Record`: `sequence_number`,
//! `sub_sequence_number`, `approximate_arrival_timestamp`, `partition_key`,
//! `data` (raw `bytes`), plus the `binary_data` alias.

use chrono::{DateTime, Utc};
use pyo3::prelude::*;
use pyo3::types::PyBytes;

use kcl::retrieval::KinesisClientRecord;

/// A single Kinesis data record delivered to a `process_records` callback.
///
/// Mirrors `amazon_kclpy.messages.Record`. Unlike the multilang-daemon variant
/// (which delivered base64 text over stdout), `data` here is already the raw
/// decoded `bytes` — so `data` and `binary_data` are the same `bytes` object.
#[pyclass(module = "kcl_rs", name = "Record", frozen)]
pub struct Record {
    sequence_number: Option<String>,
    sub_sequence_number: i64,
    approximate_arrival_timestamp: Option<DateTime<Utc>>,
    partition_key: Option<String>,
    data: Vec<u8>,
}

impl Record {
    /// Build a `Record` pyclass from the Rust [`KinesisClientRecord`].
    pub fn from_kinesis_client_record(record: &KinesisClientRecord) -> Self {
        Self {
            sequence_number: record.sequence_number().map(str::to_owned),
            sub_sequence_number: record.sub_sequence_number(),
            approximate_arrival_timestamp: record.approximate_arrival_timestamp(),
            partition_key: record.partition_key().map(str::to_owned),
            data: record
                .data()
                .map(|b| b.as_ref().to_vec())
                .unwrap_or_default(),
        }
    }
}

#[pymethods]
impl Record {
    /// The sequence number of this record.
    #[getter]
    fn sequence_number(&self) -> Option<String> {
        self.sequence_number.clone()
    }

    /// The sub-sequence number (0 unless this is a de-aggregated KPL record).
    #[getter]
    fn sub_sequence_number(&self) -> i64 {
        self.sub_sequence_number
    }

    /// The approximate server-side arrival timestamp (a `datetime`), or `None`.
    #[getter]
    fn approximate_arrival_timestamp(&self) -> Option<DateTime<Utc>> {
        self.approximate_arrival_timestamp
    }

    /// The approximate arrival time in milliseconds since the Unix epoch, or
    /// `None`. Mirrors `amazon_kclpy.messages.Record.timestamp_millis`.
    #[getter]
    fn timestamp_millis(&self) -> Option<i64> {
        self.approximate_arrival_timestamp
            .map(|ts| ts.timestamp_millis())
    }

    /// The partition key of this record.
    #[getter]
    fn partition_key(&self) -> Option<String> {
        self.partition_key.clone()
    }

    /// The raw record payload as `bytes`.
    #[getter]
    fn data<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        PyBytes::new(py, &self.data)
    }

    /// Alias for [`data`](Self::data) — the raw decoded payload as `bytes`.
    /// Mirrors `amazon_kclpy.messages.Record.binary_data` (already decoded here).
    #[getter]
    fn binary_data<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        PyBytes::new(py, &self.data)
    }

    fn __repr__(&self) -> String {
        format!(
            "Record(sequence_number={:?}, sub_sequence_number={}, partition_key={:?}, data_len={})",
            self.sequence_number,
            self.sub_sequence_number,
            self.partition_key,
            self.data.len()
        )
    }
}
