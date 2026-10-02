//! Port of the concrete
//! `software.amazon.kinesis.coordinator.DynamicMigrationComponentsInitializer`.
//!
//! This is the concrete implementation of the
//! [`DynamicMigrationComponentsInitializer`](crate::coordinator::migration::DynamicMigrationComponentsInitializer)
//! trait (the trait itself lives in the `migration` submodule so the
//! client-version states can mock it). This struct wires the LAM, leader
//! deciders, worker-metrics reporter, GSI creation, etc. and drives the 3-phase
//! v2.x -> v3.x upgrade transitions.
//!
//! # Deviations from Java
//!
//! - **Thread pools -> tokio tasks.** Java holds two `ScheduledExecutorService`s
//!   (`lamThreadPool`, `workerMetricsThreadPool`). In this all-async port:
//!   - The LAM runs its own periodic loop as a spawned tokio task (managed inside
//!     [`LeaseAssignmentManager`]); there is no thread pool to pass into
//!     `lamCreator`, so the `lam_creator` closure drops the executor arg (Java
//!     `BiFunction<ScheduledExecutorService, LeaderDecider, LeaseAssignmentManager>`
//!     -> `Fn(Arc<dyn LeaderDecider>) -> LeaseAssignmentManager`).
//!   - The worker-metrics reporter is a spawned tokio interval task; its
//!     `ScheduledFuture` becomes a [`tokio::task::JoinHandle`] that
//!     `stop_worker_metrics_reporter` **aborts** (Java `future.cancel(false)`).
//!   - `shutdownThreadPool(...)` has no analog (no owned pools) and is modeled as
//!     a no-op — the per-component tokio tasks are stopped by
//!     `leaseAssignmentManager.stop()` / aborting the reporter handle. The 60s
//!     `SCHEDULER_SHUTDOWN_TIMEOUT_SECONDS` await is therefore not needed.
//!
//! - **`LeaderDecider` is NOT shut down in `shutdown()`** (comment preserved from
//!   Java: the scheduler still accesses it during its own final shutdown).
//!
//! - **`synchronized` -> `tokio::sync::Mutex<State>`.** Java guards every public
//!   init method with the intrinsic monitor. The mutable state
//!   (`leaseAssignmentManager`, `workerMetricsReporterFuture`,
//!   `currentAssignmentMode`, `dualMode`, `initialized`, plus the concrete
//!   adaptive decider handle needed for the live delegate-swap) sits behind one
//!   `tokio::sync::Mutex<State>`. The `leaderDecider()` getter is **sync** on the
//!   trait, so the current decider is additionally mirrored into a
//!   `std::sync::Mutex<Option<Arc<dyn LeaderDecider>>>` readable without `.await`.
//!
//! - **Leader-decider factories -> boxed closures.** Java's `Supplier<...>`
//!   fields become `Box<dyn Fn() -> Arc<...> + Send + Sync>`. The
//!   `adaptiveLeaderDeciderCreator` returns the concrete
//!   `Arc<MigrationAdaptiveLeaderDecider>` (so the initializer can call
//!   `update_leader_decider` on it for the live flip/rollback swap); the
//!   deterministic / ddb-lock creators return `Arc<dyn LeaderDecider>`.

use std::sync::{Arc, Mutex as StdMutex};

use async_trait::async_trait;
use tokio::sync::Mutex as AsyncMutex;
use tokio::task::JoinHandle;

use crate::coordinator::assignment::lam_data_manager::LamDataManager;
use crate::coordinator::assignment::lease_assignment_manager::LeaseAssignmentManager;
use crate::coordinator::leader_decider::LeaderDecider;
use crate::coordinator::migration::client_version::ClientVersion;
use crate::coordinator::migration::migration_ready_monitor::WorkerMetricStatsSource;
use crate::coordinator::migration::DynamicMigrationComponentsInitializer;
use crate::coordinator::migration_adaptive_lease_assignment_mode_provider::{
    LeaseAssignmentMode, MigrationAdaptiveLeaseAssignmentModeProvider,
};
use crate::leader::MigrationAdaptiveLeaderDecider;
use crate::leases::exceptions::LeasingError;
use crate::leases::lease_management_config::WorkerUtilizationAwareAssignmentConfig;
use crate::leases::lease_refresher::LeaseRefresher;
use crate::metrics::MetricsFactory;
use crate::utils::panic_util;
use crate::worker::metricstats::worker_metric_stats_dao::WorkerMetricStatsDAO;
use crate::worker::metricstats::worker_metric_stats_manager::WorkerMetricStatsManager;
use crate::worker::metricstats::worker_metric_stats_reporter::WorkerMetricStatsReporter;

/// Java `DEFAULT_NO_OF_SKIP_STAT_FOR_DEAD_WORKER_THRESHOLD`
/// (`MigrationAwareLAMDataManager`), used to derive `workerMetricsExpirySeconds`.
use crate::coordinator::assignment::migration_aware_lam_data_manager::DEFAULT_NO_OF_SKIP_STAT_FOR_DEAD_WORKER_THRESHOLD;

/// Factory for the `MigrationAdaptiveLeaderDecider` (Java
/// `Supplier<MigrationAdaptiveLeaderDecider>`).
pub type AdaptiveLeaderDeciderCreator =
    Box<dyn Fn() -> Arc<MigrationAdaptiveLeaderDecider> + Send + Sync>;

/// Factory for a concrete leader decider (Java `Supplier<...LeaderDecider>` for
/// the deterministic and DDB-lock-based variants).
pub type LeaderDeciderCreator = Box<dyn Fn() -> Arc<dyn LeaderDecider> + Send + Sync>;

/// Factory for the LAM (Java
/// `BiFunction<ScheduledExecutorService, LeaderDecider, LeaseAssignmentManager>`;
/// the executor arg is dropped since the LAM manages its own tokio task).
pub type LamCreator = Box<dyn Fn(Arc<dyn LeaderDecider>) -> LeaseAssignmentManager + Send + Sync>;

/// Mutable, `synchronized`-guarded state (Java instance fields mutated across the
/// init methods).
struct State {
    /// Java `leaseAssignmentManager`.
    lease_assignment_manager: Option<LeaseAssignmentManager>,
    /// Java `workerMetricsReporterFuture` (a `ScheduledFuture` -> tokio
    /// `JoinHandle` that is aborted on cancel).
    worker_metrics_reporter_future: Option<JoinHandle<()>>,
    /// Java `currentAssignmentMode`.
    current_assignment_mode: LeaseAssignmentMode,
    /// Java `dualMode`.
    dual_mode: bool,
    /// Java `initialized`.
    initialized: bool,
    /// The concrete adaptive decider (present iff `dualMode`), retained so the
    /// live delegate-swap can call `update_leader_decider`. Java keeps the
    /// adaptive decider as the `leaderDecider` field and does an
    /// `instanceof`/cast; Rust trait objects are not downcastable, so the
    /// concrete handle is stored separately.
    adaptive_leader_decider: Option<Arc<MigrationAdaptiveLeaderDecider>>,
}

/// Concrete `DynamicMigrationComponentsInitializer`. Java
/// `DynamicMigrationComponentsInitializer` (`final`, `@ThreadSafe`).
pub struct DefaultDynamicMigrationComponentsInitializer {
    // --- immutable collaborators (Java `@Getter` + constructor-set fields) ---
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    lease_refresher: Arc<dyn LeaseRefresher>,
    worker_metrics_dao: Arc<WorkerMetricStatsDAO>,
    worker_metrics_manager: Arc<WorkerMetricStatsManager>,
    worker_identifier: String,
    worker_utilization_aware_assignment_config: WorkerUtilizationAwareAssignmentConfig,
    worker_metrics_expiry_seconds: i64,
    lease_mode_change_consumer: Arc<MigrationAdaptiveLeaseAssignmentModeProvider>,
    lam_data_manager: Arc<dyn LamDataManager>,

    // --- factories (Java `Supplier`/`BiFunction` fields) ---
    lam_creator: LamCreator,
    adaptive_leader_decider_creator: AdaptiveLeaderDeciderCreator,
    deterministic_leader_decider_creator: LeaderDeciderCreator,
    ddb_lock_based_leader_decider_creator: LeaderDeciderCreator,

    // --- mutable state ---
    /// Java `leaderDecider` (`@Getter`). Mirrored here so the **sync** trait
    /// getter can read it without `.await`.
    leader_decider: StdMutex<Option<Arc<dyn LeaderDecider>>>,
    state: AsyncMutex<State>,
}

impl DefaultDynamicMigrationComponentsInitializer {
    /// Java package-visible `@Builder` constructor. `worker_metrics_expiry_seconds`
    /// is derived exactly as Java:
    /// `Duration.ofMillis(DEFAULT_NO_OF_SKIP_STAT_FOR_DEAD_WORKER_THRESHOLD *
    /// workerMetricsReporterFreqInMillis()).getSeconds()`.
    #[allow(clippy::too_many_arguments)]
    // Used by the (backfill-pending) DynamicMigrationComponentsInitializerTest and by
    // the migration-adaptive Scheduler wiring; allow until that test module is ported.
    #[allow(dead_code)]
    pub(crate) fn new(
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        lease_refresher: Arc<dyn LeaseRefresher>,
        worker_metrics_dao: Arc<WorkerMetricStatsDAO>,
        worker_metrics_manager: Arc<WorkerMetricStatsManager>,
        lam_creator: LamCreator,
        adaptive_leader_decider_creator: AdaptiveLeaderDeciderCreator,
        deterministic_leader_decider_creator: LeaderDeciderCreator,
        ddb_lock_based_leader_decider_creator: LeaderDeciderCreator,
        worker_identifier: impl Into<String>,
        worker_utilization_aware_assignment_config: WorkerUtilizationAwareAssignmentConfig,
        lease_assignment_mode_provider: Arc<MigrationAdaptiveLeaseAssignmentModeProvider>,
        lam_data_manager: Arc<dyn LamDataManager>,
    ) -> Self {
        // Duration.ofMillis(millis).getSeconds() == millis / 1000 (floor).
        let worker_metrics_expiry_seconds = (DEFAULT_NO_OF_SKIP_STAT_FOR_DEAD_WORKER_THRESHOLD
            * worker_utilization_aware_assignment_config.worker_metrics_reporter_freq_in_millis)
            / 1000;

        Self {
            metrics_factory,
            lease_refresher,
            worker_metrics_dao,
            worker_metrics_manager,
            worker_identifier: worker_identifier.into(),
            worker_utilization_aware_assignment_config,
            worker_metrics_expiry_seconds,
            lease_mode_change_consumer: lease_assignment_mode_provider,
            lam_data_manager,
            lam_creator,
            adaptive_leader_decider_creator,
            deterministic_leader_decider_creator,
            ddb_lock_based_leader_decider_creator,
            leader_decider: StdMutex::new(None),
            state: AsyncMutex::new(State {
                lease_assignment_manager: None,
                worker_metrics_reporter_future: None,
                current_assignment_mode: LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
                dual_mode: false,
                initialized: false,
                adaptive_leader_decider: None,
            }),
        }
    }

    fn set_leader_decider(&self, decider: Arc<dyn LeaderDecider>) {
        *self
            .leader_decider
            .lock()
            .unwrap_or_else(|e| e.into_inner()) = Some(decider);
    }

    /// Shared startup logic for all init methods (Java `initializeStartupComponents`).
    ///
    /// `leader_decider_supplier` selects the initial concrete decider; in dual
    /// mode it is wrapped in a `MigrationAdaptiveLeaderDecider`, otherwise used
    /// directly. Must be called with `state` already locked.
    async fn initialize_startup_components(
        &self,
        state: &mut State,
        dual_mode: bool,
        assignment_mode: LeaseAssignmentMode,
        leader_decider_supplier: &LeaderDeciderCreator,
        create_lam_and_start_metrics: bool,
    ) {
        state.dual_mode = dual_mode;
        state.current_assignment_mode = assignment_mode;

        if create_lam_and_start_metrics {
            tracing::info!("Start collection of WorkerMetricStats");
            self.worker_metrics_manager.start_manager();
        }

        tracing::info!(
            "Initializing dualMode {} assignmentMode {:?}",
            dual_mode,
            assignment_mode
        );

        let leader_decider: Arc<dyn LeaderDecider> = if dual_mode {
            let initial_leader_decider = leader_decider_supplier();
            let adaptive_leader_decider = (self.adaptive_leader_decider_creator)();
            tracing::info!(
                "Initializing MigrationAdaptiveLeaderDecider with {}",
                initial_leader_decider.metric_name()
            );
            adaptive_leader_decider.update_leader_decider(initial_leader_decider);
            state.adaptive_leader_decider = Some(Arc::clone(&adaptive_leader_decider));
            adaptive_leader_decider as Arc<dyn LeaderDecider>
        } else {
            leader_decider_supplier()
        };

        tracing::info!("Initializing {}", leader_decider.metric_name());
        // NOTE: MigrationAdaptiveLeaderDecider.update_leader_decider already
        // initialize()s its delegate; the outer initialize() is a no-op default
        // on the adaptive decider (matching Java where the adaptive decider's
        // initialize() is inherited no-op). For the non-dual path this
        // initializes the concrete decider.
        leader_decider.initialize();
        self.set_leader_decider(Arc::clone(&leader_decider));

        if create_lam_and_start_metrics {
            tracing::info!("Creating LAM");
            state.lease_assignment_manager = Some((self.lam_creator)(Arc::clone(&leader_decider)));
        }

        tracing::info!("Initializing MigrationAdaptiveLeaseAssignmentModeProvider");
        self.lease_mode_change_consumer
            .initialize(dual_mode, assignment_mode);
        state.initialized = true;
    }

    /// Java `createGsi(blockingWait)`.
    async fn create_gsi(&self, blocking_wait: bool) -> Result<(), LeasingError> {
        tracing::info!("Creating Lease table GSI if it does not exist");
        // KCLv3.0 always starts with GSI available.
        self.lease_refresher
            .create_lease_owner_to_lease_key_index_if_not_exists()
            .await?;

        if blocking_wait {
            tracing::info!("Waiting for Lease table GSI creation");
            let seconds_between_polls = 10;
            let timeout_seconds = 600;
            let is_index_active = self
                .lease_refresher
                .wait_until_lease_owner_to_lease_key_index_exists(
                    seconds_between_polls,
                    timeout_seconds,
                )
                .await;

            if !is_index_active {
                return Err(LeasingError::dependency(
                    "Creating LeaseOwnerToLeaseKeyIndex on Lease table timed out",
                ));
            }
        }
        Ok(())
    }

    /// Java `startWorkerMetricsReporting()`. Schedules a
    /// [`WorkerMetricStatsReporter`] on a tokio interval (initial delay =
    /// `2 * inMemoryWorkerMetricsCaptureFrequencyMillis`, period =
    /// `workerMetricsReporterFreqInMillis`). Idempotent when already running.
    async fn start_worker_metrics_reporting(&self, state: &mut State) -> Result<(), LeasingError> {
        if state.worker_metrics_reporter_future.is_some() {
            tracing::info!("Worker metrics reporting is already running...");
            return Ok(());
        }
        tracing::info!("Initializing WorkerMetricStats");
        self.worker_metrics_dao.initialize().await?;
        tracing::info!("Starting worker metrics reporter");

        let reporter = Arc::new(WorkerMetricStatsReporter::new(
            Arc::clone(&self.metrics_factory),
            self.worker_identifier.clone(),
            Arc::clone(&self.worker_metrics_manager),
            Arc::clone(&self.worker_metrics_dao),
        ));
        let config = &self.worker_utilization_aware_assignment_config;
        // Start with a delay for workerStatsManager to capture some values.
        let initial_delay_millis =
            (config.in_memory_worker_metrics_capture_frequency_millis * 2).max(0) as u64;
        let period_millis = config.worker_metrics_reporter_freq_in_millis.max(0) as u64;

        let worker_identifier = self.worker_identifier.clone();
        let handle = tokio::spawn(async move {
            let period = std::time::Duration::from_millis(period_millis);
            tokio::time::sleep(std::time::Duration::from_millis(initial_delay_millis)).await;
            let mut interval = tokio::time::interval(if period.is_zero() {
                std::time::Duration::from_millis(1)
            } else {
                period
            });
            interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
            loop {
                interval.tick().await;
                // Java WorkerMetricStatsReporter.run catch(Exception): a
                // panicking report must not kill the reporter loop.
                if let Err(panic_msg) = panic_util::catch_tick(reporter.run()).await {
                    tracing::error!(
                        "Failed to update worker metric stats for worker : {}: {}",
                        worker_identifier,
                        panic_msg
                    );
                }
            }
        });
        state.worker_metrics_reporter_future = Some(handle);
        Ok(())
    }

    /// Java `stopWorkerMetricsReporter()`. Aborts the tokio task (Java
    /// `future.cancel(false)`).
    fn stop_worker_metrics_reporter(state: &mut State) {
        tracing::info!("Stopping worker metrics reporter");
        if let Some(handle) = state.worker_metrics_reporter_future.take() {
            handle.abort();
        }
    }

    /// Java `notifyLeaseAssignmentModeChange()`.
    fn notify_lease_assignment_mode_change(&self, state: &State) {
        if state.dual_mode {
            tracing::info!(
                "Notifying MigrationAdaptiveLeaseAssignmentModeProvider of {:?}",
                state.current_assignment_mode
            );
            if let Err(e) = self
                .lease_mode_change_consumer
                .update_lease_assignment_mode(state.current_assignment_mode)
            {
                tracing::warn!("LeaseAssignmentMode change consumer threw exception: {}", e);
            }
        } else {
            panic!("Unexpected assignment mode change");
        }
    }

    /// Java `shutdown()`.
    ///
    /// Not part of the trait (Java `shutdown()` is package-visible and called by
    /// the Scheduler, not the migration states). Provided as an inherent method.
    pub async fn shutdown(&self) {
        tracing::info!("Shutting down components");
        let mut state = self.state.lock().await;
        if state.initialized {
            tracing::info!("Stopping LAM, LeaderDecider, workerMetrics reporting and collection");
            if let Some(lam) = state.lease_assignment_manager.as_ref() {
                lam.stop().await;
            }
            self.lam_data_manager.shutdown().await;
            // leader decider is shut down later when scheduler is doing a final
            // shutdown since scheduler still accesses the leader decider while
            // shutting down.
            Self::stop_worker_metrics_reporter(&mut state);
            self.worker_metrics_manager.stop_manager();
            state.initialized = false;
        }
        // Deviation: no owned thread pools to shut down (the LAM + worker-metrics
        // reporter run as per-component tokio tasks stopped above).
    }
}

#[async_trait]
impl DynamicMigrationComponentsInitializer for DefaultDynamicMigrationComponentsInitializer {
    fn metrics_factory(&self) -> Arc<dyn MetricsFactory + Send + Sync> {
        Arc::clone(&self.metrics_factory)
    }

    fn leader_decider(&self) -> Arc<dyn LeaderDecider> {
        self.leader_decider
            .lock()
            .unwrap_or_else(|e| e.into_inner())
            .clone()
            .expect("leaderDecider accessed before initialization")
    }

    fn worker_identifier(&self) -> String {
        self.worker_identifier.clone()
    }

    fn worker_metrics_dao(&self) -> Arc<dyn WorkerMetricStatsSource> {
        Arc::clone(&self.worker_metrics_dao) as Arc<dyn WorkerMetricStatsSource>
    }

    fn worker_metrics_expiry_seconds(&self) -> i64 {
        self.worker_metrics_expiry_seconds
    }

    fn lease_refresher(&self) -> Arc<dyn LeaseRefresher> {
        Arc::clone(&self.lease_refresher)
    }

    /// Java `initializeClientVersionForPhase1()`.
    async fn initialize_client_version_for_phase1(&self) {
        let mut state = self.state.lock().await;
        if state.initialized {
            tracing::info!("Already initialized, nothing to do");
            return;
        }
        tracing::info!(
            "Initializing for Phase 1 (passive 2.x compatible mode) - no LAM, no WorkerMetrics, no GSI"
        );
        let supplier = &self.deterministic_leader_decider_creator;
        self.initialize_startup_components(
            &mut state,
            false,
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
            supplier,
            false,
        )
        .await;
    }

    /// Java `initializeClientVersionFor2x(fromClientVersion)`.
    async fn initialize_client_version_for_2x(&self, from_client_version: ClientVersion) {
        tracing::info!(
            "Initializing KCL components for rollback to 2x from {:?}",
            from_client_version
        );
        let mut state = self.state.lock().await;

        if from_client_version == ClientVersion::ClientVersionInit {
            let supplier = &self.deterministic_leader_decider_creator;
            self.initialize_startup_components(
                &mut state,
                true,
                LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
                supplier,
                true,
            )
            .await;
        } else {
            // dynamic rollback
            Self::stop_worker_metrics_reporter(&mut state);
            // Migration Tool will delete the lease table LeaseOwner GSI and
            // WorkerMetricStats table.
        }

        if from_client_version == ClientVersion::ClientVersion3xWithRollback {
            // we are rolling back after flip
            state.current_assignment_mode = LeaseAssignmentMode::DefaultLeaseCountBasedAssignment;
            self.notify_lease_assignment_mode_change(&state);
            tracing::info!("Stopping LAM");
            if let Some(lam) = state.lease_assignment_manager.as_ref() {
                lam.stop().await;
            }
            let leader_decider = (self.deterministic_leader_decider_creator)();
            match state.adaptive_leader_decider.as_ref() {
                Some(adaptive) => {
                    tracing::info!("Updating LeaderDecider to {}", leader_decider.metric_name());
                    adaptive.update_leader_decider(leader_decider);
                }
                None => panic!("Unexpected leader decider"),
            }
        }
    }

    /// Java `initializeClientVersionForUpgradeFrom2x(fromClientVersion)`.
    async fn initialize_client_version_for_upgrade_from_2x(
        &self,
        from_client_version: ClientVersion,
    ) -> Result<(), LeasingError> {
        tracing::info!(
            "Initializing KCL components for upgrade from 2x from {:?}",
            from_client_version
        );
        let mut state = self.state.lock().await;

        if from_client_version == ClientVersion::ClientVersionInit {
            let supplier = &self.deterministic_leader_decider_creator;
            self.initialize_startup_components(
                &mut state,
                true,
                LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
                supplier,
                true,
            )
            .await;
        }

        self.create_gsi(false).await?;
        self.start_worker_metrics_reporting(&mut state).await?;
        // LAM is not started until the dynamic flip to 3xWithRollback.
        Ok(())
    }

    /// Java `initializeClientVersionFor3xWithRollback(fromClientVersion)`.
    async fn initialize_client_version_for_3x_with_rollback(
        &self,
        from_client_version: ClientVersion,
    ) -> Result<(), LeasingError> {
        tracing::info!(
            "Initializing KCL components for 3x with rollback from {:?}",
            from_client_version
        );
        let mut state = self.state.lock().await;

        if from_client_version == ClientVersion::ClientVersionInit {
            let supplier = &self.ddb_lock_based_leader_decider_creator;
            self.initialize_startup_components(
                &mut state,
                true,
                LeaseAssignmentMode::WorkerUtilizationAwareAssignment,
                supplier,
                true,
            )
            .await;
            self.start_worker_metrics_reporting(&mut state).await?;
        } else if from_client_version == ClientVersion::ClientVersionUpgradeFrom2x {
            // dynamic flip
            state.current_assignment_mode = LeaseAssignmentMode::WorkerUtilizationAwareAssignment;
            self.notify_lease_assignment_mode_change(&state);
            let leader_decider = (self.ddb_lock_based_leader_decider_creator)();
            tracing::info!("Updating LeaderDecider to {}", leader_decider.metric_name());
            // Java casts `this.leaderDecider` to MigrationAdaptiveLeaderDecider
            // (unguarded); a non-adaptive decider would ClassCastException ->
            // panic here.
            let adaptive = state
                .adaptive_leader_decider
                .as_ref()
                .expect("Unexpected leader decider");
            adaptive.update_leader_decider(leader_decider);
        } else {
            self.start_worker_metrics_reporting(&mut state).await?;
        }

        tracing::info!("Starting LAM");
        if let Some(lam) = state.lease_assignment_manager.as_ref() {
            lam.start().await;
        }
        Ok(())
    }

    /// Java `initializeClientVersionFor3x(fromClientVersion)`.
    async fn initialize_client_version_for_3x(
        &self,
        from_client_version: ClientVersion,
    ) -> Result<(), LeasingError> {
        tracing::info!(
            "Initializing KCL components for 3x from {:?}",
            from_client_version
        );
        let mut state = self.state.lock().await;

        if from_client_version == ClientVersion::ClientVersionInit {
            let supplier = &self.ddb_lock_based_leader_decider_creator;
            self.initialize_startup_components(
                &mut state,
                false,
                LeaseAssignmentMode::WorkerUtilizationAwareAssignment,
                supplier,
                true,
            )
            .await;

            // gsi may already exist and be active for migrated application.
            self.create_gsi(true).await?;
            self.start_worker_metrics_reporting(&mut state).await?;
            tracing::info!("Starting LAM");
            if let Some(lam) = state.lease_assignment_manager.as_ref() {
                lam.start().await;
            }
        }
        // nothing to do when transitioning from CLIENT_VERSION_3X_WITH_ROLLBACK.
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    //! Port of the mock-portable subset of `DynamicMigrationComponentsInitializerTest`.
    //!
    //! # What is ported vs skipped
    //!
    //! The Java test relies almost entirely on Mockito `verify(mock).method()`
    //! over concrete collaborators (`LeaseAssignmentManager`, `WorkerMetricStatsDAO`,
    //! `WorkerMetricStatsManager`) that are **concrete structs (no trait) in the
    //! Rust port** and therefore cannot be spied on for call-verification. What IS
    //! observable in the Rust design — and thus faithfully asserted here — is:
    //!
    //! * **which leader-decider creator ran** (the `Supplier`s are `Box<dyn Fn>`
    //!   closures we supply, so we count invocations — the analog of
    //!   `verify(mockXCreator).get()` / `verify(..., never())`),
    //! * **the resulting `leader_decider()`** and its `metric_name()`,
    //! * **the `dualMode` + assignmentMode** pushed to the
    //!   `MigrationAdaptiveLeaseAssignmentModeProvider` (observable via
    //!   `dynamic_mode_change_support_needed()` / `get_lease_assignment_mode()` —
    //!   the analog of `verify(mockConsumer).initialize(dual, mode)`),
    //! * **the GSI-creation success/failure outcome** (via a `MockLeaseRefresher`).
    //!
    //! Skipped (documented, not portable to a call-verification test):
    //! `testShutdown`, `testComponentsInitialization_After*/Rollback_*`,
    //! `testWorkerMetricsReporting` — all depend on `verify(mockLam).start()/stop()`,
    //! `verify(mockWorkerMetricsDAO).updateMetrics(..)`, `mockFuture.cancel(..)`
    //! and similar spies over the concrete non-trait collaborators / the
    //! executor-`ScheduledFuture` lifecycle that has no Rust analog.

    use super::*;
    use crate::coordinator::assignment::lam_data_manager::MockLamDataManager;
    use crate::coordinator::assignment::lam_data_snapshot::LamDataSnapshot;
    use crate::coordinator::assignment::lease_assignment_manager::LeaseAssignmentManager;
    use crate::coordinator::leader_decider::MockLeaderDecider;
    use crate::coordinator::migration::table_migration_status::TableMigrationStatus;
    use crate::coordinator::migration::table_migration_status_provider::MockTableMigrationStatusProvider;
    use crate::leases::lease_assignment_strategy::LeaseAssignmentStrategy;
    use crate::leases::lease_management_config::{
        GracefulLeaseHandoffConfig, WorkerUtilizationAwareAssignmentConfig,
    };
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;
    use crate::worker::metricstats::worker_metric_stats_manager::WorkerMetricStatsManager;
    use aws_smithy_mocks::{mock, mock_client, RuleMode};
    use std::sync::atomic::{AtomicUsize, Ordering as AtomicOrdering};

    const WORKER_ID: &str = "TEST_WORKER_ID";
    const APP: &str = "TEST_APPLICATION";

    /// Counters for the leader-decider `Supplier.get()` invocations (Java's
    /// `verify(mockXCreator).get()` / `never()`).
    #[derive(Default)]
    struct CreatorCounts {
        deterministic: Arc<AtomicUsize>,
        ddb_lock: Arc<AtomicUsize>,
        adaptive: Arc<AtomicUsize>,
    }

    /// A leader decider with a fixed, distinguishable `metric_name`.
    fn named_decider(name: &'static str) -> MockLeaderDecider {
        let mut d = MockLeaderDecider::new();
        d.expect_metric_name().returning(move || name);
        d.expect_initialize().returning(|| ());
        d.expect_is_leader().returning(|_| true);
        d.expect_shutdown().returning(|| ());
        d
    }

    fn worker_config() -> WorkerUtilizationAwareAssignmentConfig {
        WorkerUtilizationAwareAssignmentConfig {
            worker_metrics_table_config: Some(
                crate::common::DdbTableConfig::with_application_name_and_suffix(
                    APP,
                    "WorkerMetricStats",
                ),
            ),
            ..WorkerUtilizationAwareAssignmentConfig::default()
        }
    }

    /// A permissive DDB mock: describe_table/create_table/update_time_to_live all
    /// succeed. Used for the DAO's `initialize()` in the metrics-reporting paths.
    fn permissive_ddb() -> aws_sdk_dynamodb::Client {
        use aws_sdk_dynamodb::operation::create_table::CreateTableOutput;
        use aws_sdk_dynamodb::operation::describe_table::DescribeTableOutput;
        use aws_sdk_dynamodb::operation::update_time_to_live::UpdateTimeToLiveOutput;
        let describe = mock!(aws_sdk_dynamodb::Client::describe_table)
            .then_output(|| DescribeTableOutput::builder().build());
        let create = mock!(aws_sdk_dynamodb::Client::create_table)
            .then_output(|| CreateTableOutput::builder().build());
        let ttl = mock!(aws_sdk_dynamodb::Client::update_time_to_live)
            .then_output(|| UpdateTimeToLiveOutput::builder().build());
        mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&describe, &create, &ttl]
        )
    }

    fn worker_metrics_dao() -> Arc<WorkerMetricStatsDAO> {
        let mut provider = MockTableMigrationStatusProvider::new();
        provider
            .expect_get_table_migration_status()
            .returning(|| TableMigrationStatus::Complete);
        Arc::new(WorkerMetricStatsDAO::new(
            permissive_ddb(),
            &crate::worker::metricstats::worker_metrics_table_config::WorkerMetricsTableConfig::new(
                Some(APP),
            ),
            "LeaseTable",
            30_000,
            Arc::new(provider),
        ))
    }

    fn worker_metrics_manager() -> Arc<WorkerMetricStatsManager> {
        WorkerMetricStatsManager::new(10, Vec::new(), Arc::new(NullMetricsFactory), 1_000)
    }

    /// A `MockLamDataManager` that tolerates any number of `load_data` calls.
    ///
    /// Several paths under test end in `lam.start()`, which spawns the real
    /// assignment loop; its first `interval` tick fires immediately, and the
    /// stub deciders report leadership, so the loop may race the test body to
    /// `load_data`. Without a `.returning(..)` that call panics on a tokio
    /// worker while holding the expectation mutex, and the poisoned mutex then
    /// fails the test from the mock's `Drop`. Java never sees this because its
    /// test injects a Mockito-mocked LAM whose `start()` is a no-op.
    fn permissive_lam_data_manager() -> MockLamDataManager {
        let mut lam_dm = MockLamDataManager::new();
        lam_dm
            .expect_load_data()
            .returning(|_| Ok(LamDataSnapshot::builder().build()));
        lam_dm
    }

    /// Build an initializer with instrumented creator closures + a caller-supplied
    /// `LeaseRefresher` (so GSI-creation outcomes can be controlled).
    fn build_initializer(
        lease_refresher: Arc<dyn LeaseRefresher>,
    ) -> (DefaultDynamicMigrationComponentsInitializer, CreatorCounts) {
        let counts = CreatorCounts::default();
        let (det_c, ddb_c, adp_c) = (
            Arc::clone(&counts.deterministic),
            Arc::clone(&counts.ddb_lock),
            Arc::clone(&counts.adaptive),
        );

        let deterministic_creator: LeaderDeciderCreator = Box::new(move || {
            det_c.fetch_add(1, AtomicOrdering::SeqCst);
            Arc::new(named_decider("DETERMINISTIC")) as Arc<dyn LeaderDecider>
        });
        let ddb_lock_creator: LeaderDeciderCreator = Box::new(move || {
            ddb_c.fetch_add(1, AtomicOrdering::SeqCst);
            Arc::new(named_decider("DDB_LOCK")) as Arc<dyn LeaderDecider>
        });
        let metrics_factory: Arc<dyn MetricsFactory + Send + Sync> = Arc::new(NullMetricsFactory);
        let adaptive_mf = Arc::clone(&metrics_factory);
        let adaptive_creator: AdaptiveLeaderDeciderCreator = Box::new(move || {
            adp_c.fetch_add(1, AtomicOrdering::SeqCst);
            Arc::new(MigrationAdaptiveLeaderDecider::new(Arc::clone(
                &adaptive_mf,
            )))
        });

        // LAM built by the creator closure from mocked deps. Some paths under
        // test DO start it (both `with_rollback` inits and the GSI-active 3x
        // init), so its data manager must tolerate background `load_data` calls.
        let lam_refresher = Arc::clone(&lease_refresher);
        let lam_creator: LamCreator = Box::new(move |leader_decider: Arc<dyn LeaderDecider>| {
            LeaseAssignmentManager::new(
                Arc::clone(&lam_refresher),
                leader_decider,
                WorkerUtilizationAwareAssignmentConfig::default(),
                WORKER_ID,
                1000,
                Arc::new(NullMetricsFactory),
                Arc::new(|| 1_000_000_000),
                i32::MAX,
                GracefulLeaseHandoffConfig::default(),
                LeaseAssignmentStrategy::WorkerUtilizationAware,
                2000,
                None,
                Arc::new(permissive_lam_data_manager()),
            )
        });

        let initializer = DefaultDynamicMigrationComponentsInitializer::new(
            metrics_factory,
            lease_refresher,
            worker_metrics_dao(),
            worker_metrics_manager(),
            lam_creator,
            adaptive_creator,
            deterministic_creator,
            ddb_lock_creator,
            WORKER_ID,
            worker_config(),
            Arc::new(MigrationAdaptiveLeaseAssignmentModeProvider::new()),
            Arc::new(permissive_lam_data_manager()),
        );
        (initializer, counts)
    }

    fn refresher_ok_gsi(active: bool) -> Arc<dyn LeaseRefresher> {
        let mut r = MockLeaseRefresher::new();
        r.expect_create_lease_owner_to_lease_key_index_if_not_exists()
            .returning(|| Ok(None));
        r.expect_wait_until_lease_owner_to_lease_key_index_exists()
            .returning(move |_, _| active);
        Arc::new(r)
    }

    fn provider_of(init: &DefaultDynamicMigrationComponentsInitializer) -> LeaseAssignmentMode {
        init.lease_mode_change_consumer
            .get_lease_assignment_mode()
            .unwrap()
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_client_version_for_phase1() {
        // Java `testInitializeClientVersionForPhase1`.
        let (init, counts) = build_initializer(refresher_ok_gsi(true));
        init.initialize_client_version_for_phase1().await;

        // Deterministic decider created; no DDB-lock, no adaptive.
        assert_eq!(counts.deterministic.load(AtomicOrdering::SeqCst), 1);
        assert_eq!(counts.ddb_lock.load(AtomicOrdering::SeqCst), 0);
        assert_eq!(counts.adaptive.load(AtomicOrdering::SeqCst), 0);
        // Consumer initialized non-dual, DEFAULT_LEASE_COUNT_BASED_ASSIGNMENT.
        assert!(!init
            .lease_mode_change_consumer
            .dynamic_mode_change_support_needed());
        assert_eq!(
            provider_of(&init),
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment
        );
        // Leader decider is the deterministic one.
        assert_eq!(init.leader_decider().metric_name(), "DETERMINISTIC");
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_client_version_for_phase1_idempotent() {
        // Java `testInitializeClientVersionForPhase1_idempotent`.
        let (init, counts) = build_initializer(refresher_ok_gsi(true));
        init.initialize_client_version_for_phase1().await;
        init.initialize_client_version_for_phase1().await;
        // Only initialized once.
        assert_eq!(counts.deterministic.load(AtomicOrdering::SeqCst), 1);
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_client_version_for_2x() {
        // Java `testInitialize_ClientVersion_2X`: dual mode, DEFAULT assignment,
        // deterministic + adaptive deciders created, no DDB-lock, no GSI/metrics.
        let (init, counts) = build_initializer(refresher_ok_gsi(true));
        init.initialize_client_version_for_2x(ClientVersion::ClientVersionInit)
            .await;

        assert_eq!(counts.deterministic.load(AtomicOrdering::SeqCst), 1);
        assert_eq!(counts.adaptive.load(AtomicOrdering::SeqCst), 1);
        assert_eq!(counts.ddb_lock.load(AtomicOrdering::SeqCst), 0);
        assert!(init
            .lease_mode_change_consumer
            .dynamic_mode_change_support_needed());
        assert_eq!(
            provider_of(&init),
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment
        );
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_client_version_for_3x() {
        // Java `testInitialize_ClientVersion3_X`: non-dual, WORKER_UTILIZATION_AWARE,
        // DDB-lock decider created (no adaptive, no deterministic), GSI created +
        // waited-for (active).
        let (init, counts) = build_initializer(refresher_ok_gsi(true));
        init.initialize_client_version_for_3x(ClientVersion::ClientVersionInit)
            .await
            .expect("3x init should succeed when GSI becomes active");

        assert_eq!(counts.ddb_lock.load(AtomicOrdering::SeqCst), 1);
        assert_eq!(counts.adaptive.load(AtomicOrdering::SeqCst), 0);
        assert_eq!(counts.deterministic.load(AtomicOrdering::SeqCst), 0);
        assert!(!init
            .lease_mode_change_consumer
            .dynamic_mode_change_support_needed());
        assert_eq!(
            provider_of(&init),
            LeaseAssignmentMode::WorkerUtilizationAwareAssignment
        );
        assert_eq!(init.leader_decider().metric_name(), "DDB_LOCK");
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_client_version_for_3x_with_rollback() {
        // Java `testInitialize_ClientVersion_3_xWithRollback`: dual mode,
        // WORKER_UTILIZATION_AWARE, both DDB-lock + adaptive created (no
        // deterministic), GSI NOT waited-for (so no failure even if inactive).
        let (init, counts) = build_initializer(refresher_ok_gsi(true));
        init.initialize_client_version_for_3x_with_rollback(ClientVersion::ClientVersionInit)
            .await
            .expect("3xWithRollback init should succeed");

        assert_eq!(counts.ddb_lock.load(AtomicOrdering::SeqCst), 1);
        assert_eq!(counts.adaptive.load(AtomicOrdering::SeqCst), 1);
        assert_eq!(counts.deterministic.load(AtomicOrdering::SeqCst), 0);
        assert!(init
            .lease_mode_change_consumer
            .dynamic_mode_change_support_needed());
        assert_eq!(
            provider_of(&init),
            LeaseAssignmentMode::WorkerUtilizationAwareAssignment
        );
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_client_version_for_upgrade_from_2x() {
        // Java `testInitialize_ClientVersion_UpgradeFrom2X`: dual mode, DEFAULT
        // assignment, deterministic + adaptive created (no DDB-lock), GSI created
        // without waiting.
        let (init, counts) = build_initializer(refresher_ok_gsi(false));
        init.initialize_client_version_for_upgrade_from_2x(ClientVersion::ClientVersionInit)
            .await
            .expect("upgradeFrom2x should not wait on GSI, so it succeeds");

        assert_eq!(counts.deterministic.load(AtomicOrdering::SeqCst), 1);
        assert_eq!(counts.adaptive.load(AtomicOrdering::SeqCst), 1);
        assert_eq!(counts.ddb_lock.load(AtomicOrdering::SeqCst), 0);
        assert!(init
            .lease_mode_change_consumer
            .dynamic_mode_change_support_needed());
        assert_eq!(
            provider_of(&init),
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment
        );
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialization_fails_when_gsi_is_not_active_in_3x() {
        // Java `initializationFails_WhenGsiIsNotActiveIn3_X`.
        let (init, _counts) = build_initializer(refresher_ok_gsi(false));
        let err = init
            .initialize_client_version_for_3x(ClientVersion::ClientVersionInit)
            .await
            .unwrap_err();
        assert!(matches!(err, LeasingError::Dependency { .. }));
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialization_does_not_fail_when_gsi_is_not_active_in_3x_with_rollback() {
        // Java `initializationDoesNotFail_WhenGsiIsNotActiveIn3_XWithRollback`:
        // the rollback path does NOT block on GSI activation, so an inactive GSI
        // is not an error.
        let (init, _counts) = build_initializer(refresher_ok_gsi(false));
        init.initialize_client_version_for_3x_with_rollback(ClientVersion::ClientVersionInit)
            .await
            .expect("3xWithRollback must not fail when GSI is inactive");
    }
}
