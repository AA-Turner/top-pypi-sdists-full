//! Port of `software.amazon.kinesis.worker.metricstats`.
//!
//! The [`WorkerMetricStats`] DDB data model, the in-process
//! [`WorkerMetricStatsManager`] sampler, the [`WorkerMetricStatsReporter`], and
//! the migration-routing [`WorkerMetricStatsDAO`] (+ its per-table delegate).

pub mod ddb_serde;
pub mod delegate;
pub mod migration_stub;
pub mod worker_metric_stats;
pub mod worker_metric_stats_dao;
pub mod worker_metric_stats_manager;
pub mod worker_metric_stats_reporter;
pub mod worker_metrics_table_config;

pub use migration_stub::{TableMigrationStatus, TableMigrationStatusProvider};
pub use worker_metric_stats::{
    support_code, Features, PartitionKeyVariant, WorkerMetricStats, WorkerSupportInfo,
};
pub use worker_metric_stats_dao::WorkerMetricStatsDAO;
pub use worker_metric_stats_manager::WorkerMetricStatsManager;
pub use worker_metric_stats_reporter::WorkerMetricStatsReporter;
pub use worker_metrics_table_config::WorkerMetricsTableConfig;
