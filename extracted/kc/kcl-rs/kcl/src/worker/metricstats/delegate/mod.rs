//! Port of `software.amazon.kinesis.worker.metricstats.delegate`.
//!
//! The per-table DAO delegate. Java's abstract base + two subclasses are
//! collapsed into one delegate discriminated by
//! [`DelegateKind`](worker_metric_stats_dao_delegate::DelegateKind).

pub mod worker_metric_stats_dao_delegate;

pub use worker_metric_stats_dao_delegate::{DelegateKind, WorkerMetricStatsDAODelegate};
