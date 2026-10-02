//! Port of `software.amazon.kinesis.coordinator.assignment.MigrationAwareLAMDataManager`.
//!
//! The sole [`LamDataManager`] implementation: reads leases + worker metrics
//! from the lease table (via [`EntityDAO`]) and optionally the legacy table
//! (during migration), validates/filters/merges, deletes stale entries
//! asynchronously, and computes + publishes a `TableMigrationSummary`.
//!
//! # Concurrency (Java executor -> tokio)
//!
//! Java runs the (large) lease-table scan async on an executor while a
//! synchronous legacy-table read runs on the caller thread, then `join()`s. The
//! Rust port runs both concurrently via `tokio::join!`. The fire-and-forget
//! stale-metric deletion (`CompletableFuture.runAsync`, not joined) becomes a
//! detached `tokio::spawn` (best-effort; may be abandoned on shutdown, as in Java).
//!
//! # DAO abstractions
//!
//! The Java test mocks `WorkerMetricStatsDAO` + both delegates. To keep that
//! mockability, the manager depends on the [`WorkerMetricsDao`] +
//! [`WorkerMetricsDelegate`] traits (impl'd for the concrete DAO/delegate) — the
//! `EntityDAO` is already a trait.

use std::collections::{HashMap, HashSet};
use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;

use super::lam_data_manager::LamDataManager;
use super::lam_data_snapshot::LamDataSnapshot;
use crate::coordinator::migration::table_migration_status::TableMigrationStatus;
use crate::coordinator::migration::table_migration_status_provider::TableMigrationStatusProvider;
use crate::coordinator::migration::TableMigrationSummary;
use crate::leases::exceptions::LeasingError;
use crate::leases::lease_management_config::WorkerUtilizationAwareAssignmentConfig;
use crate::leases::{EntityDAO, EntityType, Lease};
use crate::metrics::metrics_level::MetricsLevel;
use crate::metrics::{metrics_util, MetricsScope};
use crate::worker::metricstats::worker_metric_stats::WorkerSupportInfo;
use crate::worker::metricstats::WorkerMetricStats;

/// Java default `DEFAULT_NO_OF_SKIP_STAT_FOR_DEAD_WORKER_THRESHOLD`.
pub const DEFAULT_NO_OF_SKIP_STAT_FOR_DEAD_WORKER_THRESHOLD: i64 = 2;
const DDB_LOAD_RETRY_ATTEMPT: u32 = 1;

/// A per-table worker-metrics delegate (Java `WorkerMetricStatsDAODelegate`) —
/// the subset the LAM data manager uses: read-all + delete.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait WorkerMetricsDelegate: Send + Sync {
    /// Java `getAllWorkerMetricStats()`.
    async fn get_all_worker_metric_stats(&self) -> Result<Vec<WorkerMetricStats>, LeasingError>;
    /// Java `deleteMetrics(wm)`.
    async fn delete_metrics(
        &self,
        worker_metrics: &WorkerMetricStats,
    ) -> Result<bool, LeasingError>;
}

/// The worker-metrics DAO (Java `WorkerMetricStatsDAO`), exposing its two
/// per-table delegates for manual routing of deletes.
#[cfg_attr(test, mockall::automock)]
pub trait WorkerMetricsDao: Send + Sync {
    /// Java `getLeaseTableDaoDelegate()`.
    fn lease_table_delegate(&self) -> Arc<dyn WorkerMetricsDelegate>;
    /// Java `getLegacyTableDaoDelegate()` — `None` when no legacy table is configured.
    fn legacy_table_delegate(&self) -> Option<Arc<dyn WorkerMetricsDelegate>>;
}

/// Consumer of the computed migration summary (Java `Consumer<TableMigrationSummary>`).
pub type MigrationSummaryConsumer = Arc<dyn Fn(TableMigrationSummary) + Send + Sync>;

/// Migration-aware [`LamDataManager`].
pub struct MigrationAwareLamDataManager {
    entity_dao: Arc<dyn EntityDAO>,
    worker_metrics_dao: Arc<dyn WorkerMetricsDao>,
    table_migration_status_provider: Arc<dyn TableMigrationStatusProvider>,
    migration_summary_consumer: MigrationSummaryConsumer,
    stale_worker_metrics_cleanup_duration: Duration,
    worker_metrics_expiry_duration: Duration,
    support_code_expiry_threshold: Duration,
}

impl MigrationAwareLamDataManager {
    /// Java constructor `(EntityDAO, WorkerMetricStatsDAO, TableMigrationStatusProvider,
    /// Consumer<TableMigrationSummary>, WorkerUtilizationAwareAssignmentConfig, ExecutorService)`.
    /// The executor is not needed (tokio); the summary consumer is a closure.
    pub fn new(
        entity_dao: Arc<dyn EntityDAO>,
        worker_metrics_dao: Arc<dyn WorkerMetricsDao>,
        table_migration_status_provider: Arc<dyn TableMigrationStatusProvider>,
        migration_summary_consumer: MigrationSummaryConsumer,
        config: &WorkerUtilizationAwareAssignmentConfig,
    ) -> Self {
        let freq = config.worker_metrics_reporter_freq_in_millis;
        Self {
            entity_dao,
            worker_metrics_dao,
            table_migration_status_provider,
            migration_summary_consumer,
            worker_metrics_expiry_duration: Duration::from_millis(
                (DEFAULT_NO_OF_SKIP_STAT_FOR_DEAD_WORKER_THRESHOLD * freq) as u64,
            ),
            support_code_expiry_threshold: Duration::from_millis((freq * 3) as u64),
            stale_worker_metrics_cleanup_duration: config
                .stale_worker_metrics_entry_cleanup_duration,
        }
    }

    fn wm_expiry_chrono(&self) -> chrono::Duration {
        chrono::Duration::from_std(self.worker_metrics_expiry_duration)
            .unwrap_or_else(|_| chrono::Duration::zero())
    }

    fn should_scan_legacy_table(&self, status: TableMigrationStatus) -> bool {
        status != TableMigrationStatus::Complete
            && self.worker_metrics_dao.legacy_table_delegate().is_some()
    }

    async fn load_with_retry<F, Fut, T>(mut load: F) -> Result<T, LeasingError>
    where
        F: FnMut() -> Fut,
        Fut: std::future::Future<Output = Result<T, LeasingError>>,
    {
        let mut attempt = 0u32;
        loop {
            match load().await {
                Ok(v) => return Ok(v),
                Err(e) => {
                    if attempt < DDB_LOAD_RETRY_ATTEMPT {
                        tracing::warn!("Failed to load, retrying (attempt {}): {e}", attempt + 1);
                        attempt += 1;
                    } else {
                        return Err(e);
                    }
                }
            }
        }
    }

    fn extract_leases(entities: Vec<Box<dyn crate::leases::Entity>>) -> Vec<Lease> {
        let mut leases = Vec::new();
        for entity in entities {
            if entity.get_entity_type() == EntityType::Lease {
                if let Ok(lease) = entity.into_any().downcast::<Lease>() {
                    leases.push(*lease);
                }
            }
        }
        leases
    }

    fn extract_worker_metrics(
        entities: Vec<Box<dyn crate::leases::Entity>>,
    ) -> Vec<WorkerMetricStats> {
        let mut metrics = Vec::new();
        for entity in entities {
            if entity.get_entity_type() == EntityType::WorkerMetricStats {
                if let Ok(wm) = entity.into_any().downcast::<WorkerMetricStats>() {
                    metrics.push(*wm);
                }
            }
        }
        metrics
    }

    /// Java `deleteStaleWorkerMetricsAsync` — fire-and-forget (detached task).
    fn delete_stale_worker_metrics_async(
        &self,
        lease_table_metrics: &[WorkerMetricStats],
        legacy_table_metrics: &[WorkerMetricStats],
    ) {
        let threshold = chrono::Duration::from_std(self.stale_worker_metrics_cleanup_duration)
            .unwrap_or_else(|_| chrono::Duration::zero());

        let stale_lease: Vec<WorkerMetricStats> = lease_table_metrics
            .iter()
            .filter(|wm| wm.is_stale(threshold))
            .cloned()
            .collect();
        let stale_legacy: Vec<WorkerMetricStats> = legacy_table_metrics
            .iter()
            .filter(|wm| wm.is_stale(threshold))
            .cloned()
            .collect();

        if stale_lease.is_empty() && stale_legacy.is_empty() {
            return;
        }
        tracing::info!(
            "Deleting stale worker metrics: {} from lease table, {} from legacy table",
            stale_lease.len(),
            stale_legacy.len()
        );

        let lease_delegate = self.worker_metrics_dao.lease_table_delegate();
        let legacy_delegate = self.worker_metrics_dao.legacy_table_delegate();
        tokio::spawn(async move {
            for wm in stale_lease {
                if let Err(e) = lease_delegate.delete_metrics(&wm).await {
                    tracing::warn!(
                        "Failed to delete stale worker metric {:?} from lease table: {e}",
                        wm.worker_id()
                    );
                }
            }
            if let Some(legacy) = legacy_delegate {
                for wm in stale_legacy {
                    if let Err(e) = legacy.delete_metrics(&wm).await {
                        tracing::warn!(
                            "Failed to delete stale worker metric {:?} from legacy table: {e}",
                            wm.worker_id()
                        );
                    }
                }
            }
        });
    }

    fn publish_migration_summary(
        &self,
        leases: &[Lease],
        lease_table_metrics: &[WorkerMetricStats],
        legacy_table_metrics: &[WorkerMetricStats],
    ) {
        let wm_expiry = self.wm_expiry_chrono();

        let unexpired_lease_owners: HashSet<String> = leases
            .iter()
            .filter(|l| !l.is_expired_or_unassigned())
            .filter_map(|l| l.lease_owner().map(|s| s.to_string()))
            .collect();

        let all_lease_owners: HashSet<String> = leases
            .iter()
            .filter_map(|l| l.lease_owner().map(|s| s.to_string()))
            .collect();

        let active_in_lease_table: HashSet<String> = lease_table_metrics
            .iter()
            .filter(|wm| !wm.is_expired(wm_expiry))
            .filter_map(|wm| wm.worker_id().map(|s| s.to_string()))
            .collect();

        let active_in_legacy_table: HashSet<String> = legacy_table_metrics
            .iter()
            .filter(|wm| !wm.is_expired(wm_expiry))
            .filter_map(|wm| wm.worker_id().map(|s| s.to_string()))
            .collect();

        let mut all_active: HashSet<String> = active_in_lease_table.clone();
        all_active.extend(active_in_legacy_table.iter().cloned());

        let lease_owners_with_active_metrics = all_lease_owners
            .iter()
            .filter(|o| all_active.contains(*o))
            .count() as i32;

        let min_support_code = self.compute_min_support_code(
            &unexpired_lease_owners,
            lease_table_metrics,
            legacy_table_metrics,
        );

        let summary = TableMigrationSummary::builder()
            .total_active_workers_with_metrics(all_active.len() as i32)
            .active_workers_with_metrics_in_lease_table(active_in_lease_table.len() as i32)
            .active_workers_with_metrics_in_legacy_table(active_in_legacy_table.len() as i32)
            .workers_with_unexpired_leases(unexpired_lease_owners.len() as i32)
            .total_workers_with_leases(all_lease_owners.len() as i32)
            .lease_owners_with_active_metrics(lease_owners_with_active_metrics)
            .min_support_code(min_support_code)
            .build();

        tracing::info!("Table migration summary: {:?}", summary);
        (self.migration_summary_consumer)(summary);
    }

    /// Java `computeMinSupportCode`: -1 if no lease owners, 0 if any lease owner
    /// blocks (missing entry / null code / expired heartbeat), else the min code.
    fn compute_min_support_code(
        &self,
        lease_owner_worker_ids: &HashSet<String>,
        lease_table_metrics: &[WorkerMetricStats],
        legacy_table_metrics: &[WorkerMetricStats],
    ) -> i32 {
        if lease_owner_worker_ids.is_empty() {
            return -1;
        }

        // Build workerId -> WorkerSupportInfo (freshest heartbeat wins).
        let mut support_info: HashMap<String, WorkerSupportInfo> = HashMap::new();
        for wm in lease_table_metrics
            .iter()
            .chain(legacy_table_metrics.iter())
        {
            let worker_id = wm.worker_id().unwrap_or_default().to_string();
            let candidate = WorkerSupportInfo {
                support_code: wm.support_code(),
                support_code_update_epoch_seconds: wm.support_code_update_epoch_seconds(),
            };
            match support_info.get(&worker_id) {
                None => {
                    support_info.insert(worker_id, candidate);
                }
                Some(existing) => {
                    let keep_incoming = match (
                        existing.support_code_update_epoch_seconds,
                        candidate.support_code_update_epoch_seconds,
                    ) {
                        (None, _) => true,
                        (_, None) => false,
                        (Some(e), Some(i)) => i > e,
                    };
                    if keep_incoming {
                        support_info.insert(worker_id, candidate);
                    }
                }
            }
        }

        let mut min_support = i32::MAX;
        for lease_owner in lease_owner_worker_ids {
            let info = match support_info.get(lease_owner) {
                None => {
                    tracing::info!("computeMinSupportCode: lease owner '{}' has no worker metrics entry, min=0.", lease_owner);
                    return 0;
                }
                Some(i) => i,
            };
            let support_code = match info.support_code {
                None => {
                    tracing::info!(
                        "computeMinSupportCode: lease owner '{}' has no support code, min=0.",
                        lease_owner
                    );
                    return 0;
                }
                Some(c) => c,
            };
            if !info.is_support_code_expired(self.support_code_expiry_chrono()) {
                min_support = min_support.min(support_code);
            } else {
                tracing::info!(
                    "computeMinSupportCode: lease owner '{}' has expired support code heartbeat, min=0.",
                    lease_owner
                );
                return 0;
            }
        }

        let result = if min_support == i32::MAX {
            -1
        } else {
            min_support
        };
        tracing::info!(
            "computeMinSupportCode: result={} (leaseOwners={})",
            result,
            lease_owner_worker_ids.len()
        );
        result
    }

    fn support_code_expiry_chrono(&self) -> chrono::Duration {
        chrono::Duration::from_std(self.support_code_expiry_threshold)
            .unwrap_or_else(|_| chrono::Duration::zero())
    }
}

#[async_trait]
impl LamDataManager for MigrationAwareLamDataManager {
    async fn load_data(
        &self,
        metrics_scope: &mut (dyn MetricsScope + Send),
    ) -> Result<LamDataSnapshot, LeasingError> {
        let status = self
            .table_migration_status_provider
            .get_table_migration_status();

        // Step 1+2+3: run the lease scan concurrently with the (optional) legacy scan.
        let entity_dao = self.entity_dao.clone();
        let lease_scan_fut = Self::load_with_retry(|| {
            let dao = entity_dao.clone();
            async move {
                dao.scan_entities(&[EntityType::Lease, EntityType::WorkerMetricStats])
                    .await
            }
        });

        let legacy_metrics: Vec<WorkerMetricStats> = if self.should_scan_legacy_table(status) {
            let legacy = self
                .worker_metrics_dao
                .legacy_table_delegate()
                .expect("legacy delegate present (checked by should_scan_legacy_table)");
            Self::load_with_retry(|| {
                let legacy = legacy.clone();
                async move { legacy.get_all_worker_metric_stats().await }
            })
            .await?
        } else {
            Vec::new()
        };

        let mut scan_results = lease_scan_fut.await?;
        let lease_scan = scan_results
            .remove(&EntityType::Lease)
            .unwrap_or_default_scan();
        let metrics_scan = scan_results
            .remove(&EntityType::WorkerMetricStats)
            .unwrap_or_default_scan();

        let leases = Self::extract_leases(lease_scan.entities);
        let lease_table_metrics = Self::extract_worker_metrics(metrics_scan.entities);
        let lease_deserialization_failures = lease_scan.deserialization_failures;

        // Step 4: deserialization-failure metric.
        if !lease_deserialization_failures.is_empty() {
            tracing::warn!(
                "Leases that failed deserialization: {:?}",
                lease_deserialization_failures
            );
            metrics_util::add_count(
                metrics_scope,
                "LeaseDeserializationFailureCount",
                lease_deserialization_failures.len() as i64,
                MetricsLevel::Summary,
            );
        }

        // Step 5: migration summary (raw, time-filtered — before invalid filter).
        self.publish_migration_summary(&leases, &lease_table_metrics, &legacy_metrics);

        // Step 6: merge + validity filter (+ NumWorkersWithInvalidEntry metric).
        let mut all_raw: Vec<WorkerMetricStats> = lease_table_metrics.clone();
        all_raw.extend(legacy_metrics.iter().cloned());

        let invalid_worker_ids: Vec<String> = all_raw
            .iter()
            .filter(|wm| !wm.is_valid_worker_metric())
            .filter_map(|wm| wm.worker_id().map(|s| s.to_string()))
            .collect();
        if !invalid_worker_ids.is_empty() {
            tracing::warn!(
                "List of workerIds with invalid entries: {:?}",
                invalid_worker_ids
            );
            metrics_util::add_count(
                metrics_scope,
                "NumWorkersWithInvalidEntry",
                invalid_worker_ids.len() as i64,
                MetricsLevel::Summary,
            );
        }

        // Step 7: fire-and-forget stale deletion.
        self.delete_stale_worker_metrics_async(&lease_table_metrics, &legacy_metrics);

        // Step 8: return valid, non-expired metrics.
        let wm_expiry = self.wm_expiry_chrono();
        let active_worker_metrics: Vec<WorkerMetricStats> = all_raw
            .into_iter()
            .filter(|wm| wm.is_valid_worker_metric())
            .filter(|wm| !wm.is_expired(wm_expiry))
            .collect();

        tracing::info!(
            "LAMDataManager loaded {} leases, {} active worker metrics (migration status: {:?})",
            leases.len(),
            active_worker_metrics.len(),
            status
        );

        Ok(LamDataSnapshot::builder()
            .leases(leases)
            .lease_deserialization_failures(lease_deserialization_failures)
            .worker_metric_stats(active_worker_metrics)
            .build())
    }

    async fn shutdown(&self) {
        tracing::info!("MigrationAwareLAMDataManager shut down.");
    }
}

// Small helper: Option<EntityScanList> -> default empty on None.
trait ScanListExt {
    fn unwrap_or_default_scan(self) -> crate::leases::EntityScanList;
}
impl ScanListExt for Option<crate::leases::EntityScanList> {
    fn unwrap_or_default_scan(self) -> crate::leases::EntityScanList {
        self.unwrap_or_else(|| crate::leases::EntityScanList::builder().build())
    }
}

#[cfg(test)]
mod tests;
