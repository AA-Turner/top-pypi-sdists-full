//! Port of `software.amazon.kinesis.worker.metricstats.WorkerMetricStatsDAO`.
//!
//! Routes read/write/delete to the legacy or lease table based on the
//! table-migration state machine (the [`TableMigrationStatusProvider`] stub —
//! coordinator wave). Read routing uses the **live** status; write/delete
//! routing uses the status **cached at `initialize()`** — the deliberate
//! migration-safety asymmetry (preserved exactly).

use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};

use aws_sdk_dynamodb::Client;

use super::delegate::WorkerMetricStatsDAODelegate;
use super::migration_stub::{TableMigrationStatus, TableMigrationStatusProvider};
use super::worker_metric_stats::WorkerMetricStats;
use super::worker_metrics_table_config::WorkerMetricsTableConfig;
use crate::leases::exceptions::LeasingError;

/// Routes [`WorkerMetricStats`] operations to the correct DDB table.
pub struct WorkerMetricStatsDAO {
    lease_table_dao_delegate: WorkerMetricStatsDAODelegate,
    legacy_table_dao_delegate: WorkerMetricStatsDAODelegate,
    table_migration_status_provider: Arc<dyn TableMigrationStatusProvider>,
    cached_status: Mutex<Option<TableMigrationStatus>>,
    initialized: AtomicBool,
}

impl WorkerMetricStatsDAO {
    /// Construct the DAO (Java constructor).
    pub fn new(
        dynamo_db_client: Client,
        worker_metrics_table_config: &WorkerMetricsTableConfig,
        lease_table_name: impl Into<String>,
        worker_metrics_reporter_frequency_millis: i64,
        table_migration_status_provider: Arc<dyn TableMigrationStatusProvider>,
    ) -> Self {
        let lease_table_name = lease_table_name.into();
        let legacy_table_name = worker_metrics_table_config
            .table_name()
            .unwrap_or("WorkerMetricStats")
            .to_string();
        Self {
            lease_table_dao_delegate: WorkerMetricStatsDAODelegate::new_lease_table(
                dynamo_db_client.clone(),
                lease_table_name,
                worker_metrics_reporter_frequency_millis,
            ),
            legacy_table_dao_delegate: WorkerMetricStatsDAODelegate::new_legacy(
                dynamo_db_client,
                legacy_table_name,
                worker_metrics_reporter_frequency_millis,
            ),
            table_migration_status_provider,
            cached_status: Mutex::new(None),
            initialized: AtomicBool::new(false),
        }
    }

    /// The legacy-table delegate accessor (Java `getLegacyTableDaoDelegate`).
    pub fn legacy_table_dao_delegate(&self) -> &WorkerMetricStatsDAODelegate {
        &self.legacy_table_dao_delegate
    }

    /// The lease-table delegate accessor (Java `getLeaseTableDaoDelegate`).
    pub fn lease_table_dao_delegate(&self) -> &WorkerMetricStatsDAODelegate {
        &self.lease_table_dao_delegate
    }

    /// Initialize both delegates and cache the current migration status for
    /// write routing (Java `initialize`). UNKNOWN at init => fail fast.
    pub async fn initialize(&self) -> Result<(), LeasingError> {
        if self.initialized.load(Ordering::SeqCst) {
            tracing::info!("WorkerMetricStatsDAO already initialized");
            return Ok(());
        }
        self.legacy_table_dao_delegate.initialize().await?;
        self.lease_table_dao_delegate.initialize().await?;

        let status = self
            .table_migration_status_provider
            .get_table_migration_status();
        if status == TableMigrationStatus::Unknown {
            return Err(LeasingError::dependency(
                "Cannot initialize WorkerMetricStatsDAO: TableMigrationStatusProvider is still UNKNOWN",
            ));
        }
        *self.cached_status.lock().unwrap() = Some(status);
        self.initialized.store(true, Ordering::SeqCst);
        tracing::info!(
            "WorkerMetricStatsDAO initialized. Legacy enabled: {}, cached migration status: {:?}",
            self.legacy_table_dao_delegate.is_enabled(),
            status
        );
        Ok(())
    }

    fn ensure_initialized(&self) -> Result<(), LeasingError> {
        if !self.initialized.load(Ordering::SeqCst) {
            return Err(LeasingError::invalid_state(
                "WorkerMetricStatsDAO is not initialized. Call initialize() first.",
            ));
        }
        Ok(())
    }

    fn is_table_migration_complete(&self) -> bool {
        self.table_migration_status_provider
            .get_table_migration_status()
            == TableMigrationStatus::Complete
    }

    fn write_delegate(&self) -> &WorkerMetricStatsDAODelegate {
        let status = self
            .cached_status
            .lock()
            .unwrap()
            .expect("cached status set after initialize");
        match status {
            TableMigrationStatus::Complete | TableMigrationStatus::Pending => {
                &self.lease_table_dao_delegate
            }
            TableMigrationStatus::Init | TableMigrationStatus::Deployed => {
                &self.legacy_table_dao_delegate
            }
            TableMigrationStatus::Unknown => {
                panic!("Cannot determine write delegate for status: {:?}", status)
            }
        }
    }

    /// Get all worker metric stats (Java `getAllWorkerMetricStats`). COMPLETE
    /// (live) => lease table only; else union of both.
    pub async fn get_all_worker_metric_stats(
        &self,
    ) -> Result<Vec<WorkerMetricStats>, LeasingError> {
        self.ensure_initialized()?;
        if self.is_table_migration_complete() {
            return self
                .lease_table_dao_delegate
                .get_all_worker_metric_stats()
                .await;
        }
        let mut combined = self
            .legacy_table_dao_delegate
            .get_all_worker_metric_stats()
            .await?;
        combined.extend(
            self.lease_table_dao_delegate
                .get_all_worker_metric_stats()
                .await?,
        );
        Ok(combined)
    }

    /// Upsert the worker metrics (Java `updateMetrics`).
    pub async fn update_metrics(
        &self,
        worker_metrics: &WorkerMetricStats,
    ) -> Result<(), LeasingError> {
        self.ensure_initialized()?;
        self.write_delegate().update_metrics(worker_metrics).await
    }

    /// Conditional delete (Java `deleteMetrics`).
    pub async fn delete_metrics(
        &self,
        worker_metrics: &WorkerMetricStats,
    ) -> Result<bool, LeasingError> {
        self.ensure_initialized()?;
        self.write_delegate().delete_metrics(worker_metrics).await
    }
}

#[async_trait::async_trait]
impl crate::coordinator::migration::migration_ready_monitor::WorkerMetricStatsSource
    for WorkerMetricStatsDAO
{
    async fn get_all_worker_metric_stats(&self) -> Result<Vec<WorkerMetricStats>, LeasingError> {
        WorkerMetricStatsDAO::get_all_worker_metric_stats(self).await
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::worker::metricstats::migration_stub::MockTableMigrationStatusProvider;

    fn dummy_client() -> Client {
        let config = aws_sdk_dynamodb::Config::builder()
            .behavior_version(aws_sdk_dynamodb::config::BehaviorVersion::latest())
            .region(aws_config::Region::new("us-east-1"))
            .build();
        Client::from_conf(config)
    }

    // Routing state-machine tests (write delegate selection) without hitting DDB:
    // the DAO's write_delegate() is a pure function of the cached status.
    fn dao_with_cached(status: TableMigrationStatus) -> WorkerMetricStatsDAO {
        let mut provider = MockTableMigrationStatusProvider::new();
        provider
            .expect_get_table_migration_status()
            .returning(move || status);
        let config = WorkerMetricsTableConfig::with_table_name("legacy");
        let dao =
            WorkerMetricStatsDAO::new(dummy_client(), &config, "lease", 10_000, Arc::new(provider));
        *dao.cached_status.lock().unwrap() = Some(status);
        dao.initialized.store(true, Ordering::SeqCst);
        dao
    }

    #[test]
    fn write_delegate_routes_complete_and_pending_to_lease_table() {
        let dao = dao_with_cached(TableMigrationStatus::Complete);
        assert_eq!(
            dao.write_delegate().table_name(),
            dao.lease_table_dao_delegate.table_name()
        );
        let dao = dao_with_cached(TableMigrationStatus::Pending);
        assert_eq!(
            dao.write_delegate().table_name(),
            dao.lease_table_dao_delegate.table_name()
        );
    }

    #[test]
    fn write_delegate_routes_init_and_deployed_to_legacy_table() {
        let dao = dao_with_cached(TableMigrationStatus::Init);
        assert_eq!(
            dao.write_delegate().table_name(),
            dao.legacy_table_dao_delegate.table_name()
        );
        let dao = dao_with_cached(TableMigrationStatus::Deployed);
        assert_eq!(
            dao.write_delegate().table_name(),
            dao.legacy_table_dao_delegate.table_name()
        );
    }

    #[tokio::test]
    async fn ensure_initialized_errors_before_init() {
        let mut provider = MockTableMigrationStatusProvider::new();
        provider
            .expect_get_table_migration_status()
            .returning(|| TableMigrationStatus::Complete);
        let config = WorkerMetricsTableConfig::with_table_name("legacy");
        let dao =
            WorkerMetricStatsDAO::new(dummy_client(), &config, "lease", 10_000, Arc::new(provider));
        let err = dao.get_all_worker_metric_stats().await.unwrap_err();
        assert!(matches!(err, LeasingError::InvalidState { .. }));
    }

    #[test]
    fn is_table_migration_complete_reads_live_status() {
        let dao = dao_with_cached(TableMigrationStatus::Complete);
        assert!(dao.is_table_migration_complete());
    }
}
