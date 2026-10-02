//! Port of `software.amazon.kinesis.worker`.
//!
//! The worker-metrics subsystem: pluggable resource metrics
//! ([`metric`]), compute-platform detection ([`platform`]), the persistent
//! per-worker metric stats + reporting ([`metricstats`]), and the default-metric
//! [`WorkerMetricsSelector`].

pub mod metric;
pub mod metricstats;
pub mod platform;
pub mod worker_metrics_selector;

pub use worker_metrics_selector::WorkerMetricsSelector;
