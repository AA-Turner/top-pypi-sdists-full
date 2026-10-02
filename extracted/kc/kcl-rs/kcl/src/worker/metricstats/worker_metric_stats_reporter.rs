//! Port of `software.amazon.kinesis.worker.metricstats.WorkerMetricStatsReporter`.
//!
//! Snapshots the manager's computed metrics + operating ranges into a
//! `WorkerMetricStats` record and writes it to DDB via the DAO, emitting
//! success/latency metrics.
//!
//! Java implements `Runnable.run()` (sync); the DAO write is async in this port,
//! so [`run`](WorkerMetricStatsReporter::run) is `async`. `run()` never
//! propagates errors (swallows on failure), matching the Java `Runnable`
//! contract.

use std::sync::Arc;

use super::worker_metric_stats::{support_code, WorkerMetricStats};
use super::worker_metric_stats_dao::WorkerMetricStatsDAO;
use super::worker_metric_stats_manager::WorkerMetricStatsManager;
use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};

/// Periodic reporter writing worker metric stats to DDB.
pub struct WorkerMetricStatsReporter {
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    worker_identifier: String,
    worker_metrics_manager: Arc<WorkerMetricStatsManager>,
    worker_metrics_dao: Arc<WorkerMetricStatsDAO>,
}

impl WorkerMetricStatsReporter {
    /// Construct the reporter (Java `@RequiredArgsConstructor`).
    pub fn new(
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        worker_identifier: impl Into<String>,
        worker_metrics_manager: Arc<WorkerMetricStatsManager>,
        worker_metrics_dao: Arc<WorkerMetricStatsDAO>,
    ) -> Self {
        Self {
            metrics_factory,
            worker_identifier: worker_identifier.into(),
            worker_metrics_manager,
            worker_metrics_dao,
        }
    }

    /// Snapshot + write the current metrics (Java `run`). Always builds a legacy
    /// record (the DAO's write delegate converts as needed). Two separate
    /// `now()` reads for lastUpdateTime + supportCodeUpdateEpochSeconds preserve
    /// Java's two `Instant.now()` calls.
    pub async fn run(&self) {
        let mut scope = metrics_util::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            "WorkerMetricStatsReporter",
        );
        metrics_util::add_worker_identifier(scope.as_mut(), &self.worker_identifier);
        let start_time = metrics_util::current_time_millis();
        let mut success = false;

        let worker_metrics = WorkerMetricStats::legacy_builder()
            .worker_id(self.worker_identifier.clone())
            .metric_stats(self.worker_metrics_manager.compute_metrics())
            .operating_range(self.worker_metrics_manager.get_operating_range())
            .last_update_time(chrono::Utc::now().timestamp())
            .support_code(support_code())
            .support_code_update_epoch_seconds(chrono::Utc::now().timestamp())
            .build();

        match self
            .worker_metrics_dao
            .update_metrics(&worker_metrics)
            .await
        {
            Ok(()) => success = true,
            Err(e) => {
                tracing::error!(
                    "Failed to update worker metric stats for worker : {}: {}",
                    self.worker_identifier,
                    e
                );
            }
        }

        metrics_util::add_success_and_latency(
            scope.as_mut(),
            success,
            start_time,
            MetricsLevel::Summary,
        );
        metrics_util::end_scope(scope.as_mut());
    }
}
