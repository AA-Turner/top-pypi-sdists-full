//! Port of the `coordinator.migration`-facing surface of
//! `software.amazon.kinesis.coordinator.DynamicMigrationComponentsInitializer`.
//!
//! # Deviation: cross-module type ported as a trait
//!
//! The Java `DynamicMigrationComponentsInitializer` is a large concrete class in
//! the (out-of-subsystem) `coordinator` package that wires the LAM, leader
//! deciders, worker-metrics reporter, GSI creation, etc. — all of which belong
//! to later waves (assignment/leader 10c, Scheduler 10d). The migration
//! client-version states only depend on a small **read + lifecycle-hook**
//! surface, so this wave ports that surface as a trait
//! (`#[automock]`, matching the Java tests which mock the concrete class). The
//! full concrete initializer lands in wave 10c/10d.

use std::sync::Arc;

use async_trait::async_trait;

use crate::coordinator::leader_decider::LeaderDecider;
use crate::coordinator::migration::client_version::ClientVersion;
use crate::coordinator::migration::migration_ready_monitor::WorkerMetricStatsSource;
use crate::leases::exceptions::LeasingError;
use crate::leases::lease_refresher::LeaseRefresher;
use crate::metrics::MetricsFactory;

/// The subset of Java `DynamicMigrationComponentsInitializer` consumed by the
/// migration client-version states + monitors.
///
/// `initialize_client_version_for_phase1` / `_for_2x` are Java `void` (never
/// throw); the other three `throws DependencyException` and so return
/// `Result<(), LeasingError>`. All are `async` since the concrete impl performs
/// DDB I/O (GSI creation, worker-metrics DAO init) — the states already run
/// inside async contexts.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait DynamicMigrationComponentsInitializer: Send + Sync {
    /// Java `metricsFactory()`.
    fn metrics_factory(&self) -> Arc<dyn MetricsFactory + Send + Sync>;
    /// Java `leaderDecider()`.
    fn leader_decider(&self) -> Arc<dyn LeaderDecider>;
    /// Java `workerIdentifier()`.
    fn worker_identifier(&self) -> String;
    /// Java `workerMetricsDAO()`.
    fn worker_metrics_dao(&self) -> Arc<dyn WorkerMetricStatsSource>;
    /// Java `workerMetricsExpirySeconds()`.
    fn worker_metrics_expiry_seconds(&self) -> i64;
    /// Java `leaseRefresher()`.
    fn lease_refresher(&self) -> Arc<dyn LeaseRefresher>;

    /// Java `initializeClientVersionForPhase1()`.
    async fn initialize_client_version_for_phase1(&self);
    /// Java `initializeClientVersionFor2x(fromClientVersion)`.
    async fn initialize_client_version_for_2x(&self, from_client_version: ClientVersion);
    /// Java `initializeClientVersionForUpgradeFrom2x(fromClientVersion)`.
    async fn initialize_client_version_for_upgrade_from_2x(
        &self,
        from_client_version: ClientVersion,
    ) -> Result<(), LeasingError>;
    /// Java `initializeClientVersionFor3xWithRollback(fromClientVersion)`.
    async fn initialize_client_version_for_3x_with_rollback(
        &self,
        from_client_version: ClientVersion,
    ) -> Result<(), LeasingError>;
    /// Java `initializeClientVersionFor3x(fromClientVersion)`.
    async fn initialize_client_version_for_3x(
        &self,
        from_client_version: ClientVersion,
    ) -> Result<(), LeasingError>;
}
