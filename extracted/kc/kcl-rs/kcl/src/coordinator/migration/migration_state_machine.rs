//! Port of `software.amazon.kinesis.coordinator.migration.MigrationStateMachine`
//! (interface) and `MigrationStateMachineImpl`.

use std::sync::{Arc, Mutex, Weak};

use async_trait::async_trait;

use crate::coordinator::coordinator_config::ClientVersionConfig;
use crate::coordinator::coordinator_state_dao::CoordinatorStateAccess;
use crate::coordinator::migration::client_version::ClientVersion;
use crate::coordinator::migration::client_version_change_monitor::RandomDouble;
use crate::coordinator::migration::dynamic_migration_components_initializer::DynamicMigrationComponentsInitializer;
use crate::coordinator::migration::migration_client_version_state::{
    MigrationClientVersion2xState, MigrationClientVersion3xState,
    MigrationClientVersion3xWithRollbackState, MigrationClientVersionInitState,
    MigrationClientVersionState, MigrationClientVersionUpgradeFrom2xState, StateContext,
};
use crate::coordinator::migration::migration_client_version_state_initializer::MigrationClientVersionStateInitializer;
use crate::coordinator::migration::migration_ready_monitor::TimeProvider;
use crate::coordinator::migration::migration_state::MigrationState;
use crate::coordinator::migration::monitor_scheduler::MonitorScheduler;
use crate::leases::exceptions::LeasingError;
use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};

use aws_sdk_cloudwatch::types::StandardUnit;

/// Java `MigrationStateMachineImpl.FAULT_METRIC`.
pub const FAULT_METRIC: &str = "Fault";
/// Java `MigrationStateMachineImpl.METRICS_OPERATION`.
pub const METRICS_OPERATION: &str = "Migration";

/// Java `MigrationStateMachine` interface.
#[async_trait]
pub trait MigrationStateMachine: Send + Sync {
    /// Java `initialize()`.
    async fn initialize(&self) -> Result<(), LeasingError>;
    /// Java `shutdown()`.
    async fn shutdown(&self);
    /// Java `terminate()`.
    async fn terminate(&self);
    /// Java `transitionTo(next, state)`.
    async fn transition_to(
        &self,
        next: ClientVersion,
        state: MigrationState,
    ) -> Result<(), LeasingError>;
    /// Java `getCurrentClientVersion()`.
    fn get_current_client_version(&self) -> ClientVersion;
}

struct Inner {
    current_state: Option<Arc<dyn MigrationClientVersionState>>,
    terminated: bool,
    starting_client_version: Option<ClientVersion>,
}

/// Concrete thread-safe implementation of [`MigrationStateMachine`]. Java
/// `MigrationStateMachineImpl`.
pub struct MigrationStateMachineImpl {
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    time_provider: TimeProvider,
    coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
    scheduler: Arc<dyn MonitorScheduler>,
    client_version_config: ClientVersionConfig,
    random: RandomDouble,
    initializer: Arc<dyn DynamicMigrationComponentsInitializer>,
    worker_id: String,
    flip_to_3x_stabilizer_time_in_seconds: i64,
    inner: Mutex<Inner>,
    /// Weak self, set at construction so states can call back for transitions.
    self_weak: Mutex<Weak<MigrationStateMachineImpl>>,
}

impl MigrationStateMachineImpl {
    /// Java constructor. Returns an `Arc` so the state objects can hold a weak
    /// back-reference for their monitor callbacks.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        time_provider: TimeProvider,
        coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
        scheduler: Arc<dyn MonitorScheduler>,
        client_version_config: ClientVersionConfig,
        random: RandomDouble,
        initializer: Arc<dyn DynamicMigrationComponentsInitializer>,
        worker_id: impl Into<String>,
        flip_to_3x_stabilizer_time_in_seconds: i64,
    ) -> Arc<Self> {
        let arc = Arc::new(Self {
            metrics_factory,
            time_provider,
            coordinator_state_dao,
            scheduler,
            client_version_config,
            random,
            initializer,
            worker_id: worker_id.into(),
            flip_to_3x_stabilizer_time_in_seconds,
            inner: Mutex::new(Inner {
                current_state: None,
                terminated: false,
                starting_client_version: None,
            }),
            self_weak: Mutex::new(Weak::new()),
        });
        *arc.self_weak.lock().expect("poisoned") = Arc::downgrade(&arc);
        arc
    }

    fn state_context(&self) -> StateContext {
        StateContext {
            state_machine: self.self_weak.lock().expect("poisoned").clone(),
            time_provider: self.time_provider.clone(),
            coordinator_state_dao: self.coordinator_state_dao.clone(),
            scheduler: self.scheduler.clone(),
            initializer: self.initializer.clone(),
            random: self.random.clone(),
            worker_id: self.worker_id.clone(),
            flip_to_3x_stabilizer_time_in_seconds: self.flip_to_3x_stabilizer_time_in_seconds,
        }
    }

    fn create_migration_client_version_state(
        &self,
        client_version: ClientVersion,
        migration_state: MigrationState,
    ) -> Arc<dyn MigrationClientVersionState> {
        let ctx = self.state_context();
        match client_version {
            ClientVersion::ClientVersionInit => Arc::new(MigrationClientVersionInitState::new(
                self.initializer.clone(),
            )),
            ClientVersion::ClientVersion2x => {
                MigrationClientVersion2xState::new(ctx, migration_state)
            }
            ClientVersion::ClientVersionUpgradeFrom2x => {
                MigrationClientVersionUpgradeFrom2xState::new(ctx, migration_state)
            }
            ClientVersion::ClientVersion3xWithRollback => {
                MigrationClientVersion3xWithRollbackState::new(ctx, migration_state)
            }
            ClientVersion::ClientVersion3x => {
                MigrationClientVersion3xState::new(ctx, migration_state)
            }
        }
    }

    /// Public async `initialize` (as free method so the trait impl can defer to
    /// it). Determines + enters the starting state.
    pub async fn initialize(&self) -> Result<(), LeasingError> {
        {
            let inner = self.inner.lock().expect("poisoned");
            if inner.starting_client_version.is_some() {
                tracing::info!("MigrationStateMachine already initialized");
                return Ok(());
            }
        }
        tracing::info!("Initializing MigrationStateMachine");
        let initializer = MigrationClientVersionStateInitializer::new(
            self.coordinator_state_dao.clone(),
            self.client_version_config,
            self.random.clone(),
            self.worker_id.clone(),
        );
        let (starting_client_version, starting_migration_state) =
            initializer.get_initial_state().await?;

        let starting_state = self.create_migration_client_version_state(
            starting_client_version,
            starting_migration_state,
        );
        // enter() may throw DependencyException; Scheduler retries the whole init.
        starting_state
            .enter(ClientVersion::ClientVersionInit)
            .await?;
        {
            let mut inner = self.inner.lock().expect("poisoned");
            inner.current_state = Some(starting_state);
            inner.starting_client_version = Some(starting_client_version);
        }
        tracing::info!(
            ?starting_client_version,
            "MigrationStateMachine initial clientVersion"
        );

        if starting_client_version == ClientVersion::ClientVersion3x {
            self.terminate().await;
        }
        Ok(())
    }

    /// Java synchronized `terminate()`. Idempotent.
    pub async fn terminate(&self) {
        // Take the current state under the lock, run leave() outside the lock.
        let state = {
            let mut inner = self.inner.lock().expect("poisoned");
            if inner.terminated || inner.current_state.is_none() {
                return;
            }
            tracing::info!("State machine is about to terminate");
            let s = inner.current_state.take();
            inner.terminated = true;
            s
        };
        if let Some(s) = state {
            s.leave().await;
        }
        tracing::info!("State machine reached a terminal state");
    }

    /// Java synchronized `transitionTo(next, state)`.
    pub async fn transition_to(
        &self,
        next_client_version: ClientVersion,
        migration_state: MigrationState,
    ) -> Result<(), LeasingError> {
        // Snapshot current state + terminated under lock.
        let current = {
            let inner = self.inner.lock().expect("poisoned");
            if inner.terminated {
                return Err(LeasingError::invalid_state(format!(
                    "Cannot transition to {} after state machine is terminated",
                    next_client_version.name()
                )));
            }
            inner.current_state.clone()
        };
        let current_version = current
            .as_ref()
            .map(|s| s.client_version())
            .unwrap_or(ClientVersion::ClientVersionInit);

        let next_state =
            self.create_migration_client_version_state(next_client_version, migration_state);
        tracing::info!(from = ?current_version, to = ?next_client_version, "Attempting to transition");
        if let Some(cur) = current {
            cur.leave().await;
        }
        self.enter(next_state, current_version).await
    }

    /// Java private `enter(next)` with retry. Leaving INIT rethrows immediately;
    /// otherwise retries forever with a flat 1s backoff (Fault metric per fail).
    async fn enter(
        &self,
        next_state: Arc<dyn MigrationClientVersionState>,
        current_version: ClientVersion,
    ) -> Result<(), LeasingError> {
        loop {
            match next_state.enter(current_version).await {
                Ok(()) => {
                    let terminal = {
                        let mut inner = self.inner.lock().expect("poisoned");
                        inner.current_state = Some(next_state.clone());
                        next_state.client_version() == ClientVersion::ClientVersion3x
                    };
                    tracing::info!(to = ?next_state.client_version(), "Successfully transitioned");
                    if terminal {
                        self.terminate().await;
                    }
                    return Ok(());
                }
                Err(e) => {
                    if current_version == ClientVersion::ClientVersionInit {
                        return Err(e);
                    }
                    tracing::info!(?e, "Transition failed, retrying after 1 second");
                    let mut scope = metrics_util::create_metrics_with_operation(
                        self.metrics_factory.as_ref(),
                        METRICS_OPERATION,
                    );
                    scope.add_data_with_level(
                        FAULT_METRIC,
                        1.0,
                        StandardUnit::Count,
                        MetricsLevel::Summary,
                    );
                    metrics_util::end_scope(scope.as_mut());
                    tokio::time::sleep(std::time::Duration::from_millis(1000)).await;
                }
            }
        }
    }

    /// Java `shutdown()`: terminate + shut down the (tokio-backed) scheduler.
    pub async fn shutdown(&self) {
        self.terminate().await;
        // The tokio scheduler tasks are per-monitor and cancelled by state
        // leave(); there is no shared pool to await here.
        tracing::info!("Shutdown successfully");
    }

    /// Java `getCurrentClientVersion()`.
    pub fn get_current_client_version(&self) -> ClientVersion {
        // The Java-parity panic must not fire while `inner` is held: panicking
        // with the guard alive would poison the lock, so a `catch_unwind` in
        // the calling loop would wedge every subsequent reader. Compute under
        // the lock, drop the guard, then panic.
        let version = {
            let inner = self.inner.lock().expect("poisoned");
            if let Some(s) = &inner.current_state {
                Some(s.client_version())
            } else if inner.terminated {
                Some(ClientVersion::ClientVersion3x)
            } else {
                None
            }
        };
        match version {
            Some(v) => v,
            None => panic!(
                "No current state when state machine is either not initialized or already terminated"
            ),
        }
    }
}

#[async_trait]
impl MigrationStateMachine for MigrationStateMachineImpl {
    async fn initialize(&self) -> Result<(), LeasingError> {
        MigrationStateMachineImpl::initialize(self).await
    }
    async fn shutdown(&self) {
        MigrationStateMachineImpl::shutdown(self).await
    }
    async fn terminate(&self) {
        MigrationStateMachineImpl::terminate(self).await
    }
    async fn transition_to(
        &self,
        next: ClientVersion,
        state: MigrationState,
    ) -> Result<(), LeasingError> {
        MigrationStateMachineImpl::transition_to(self, next, state).await
    }
    fn get_current_client_version(&self) -> ClientVersion {
        MigrationStateMachineImpl::get_current_client_version(self)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;
    use std::sync::atomic::{AtomicBool, Ordering};

    use aws_sdk_dynamodb::types::ExpectedAttributeValue;

    use crate::coordinator::coordinator_state::CoordinatorState;
    use crate::coordinator::coordinator_state_dao::CoordinatorStateAccess;
    use crate::coordinator::leader_decider::MockLeaderDecider;
    use crate::coordinator::migration::dynamic_migration_components_initializer::MockDynamicMigrationComponentsInitializer;
    use crate::coordinator::migration::migration_ready_monitor::MockWorkerMetricStatsSource;
    use crate::coordinator::migration::monitor_scheduler::RecordingScheduler;
    use crate::leases::lease_refresher::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;

    const WORKER_ID: &str = "MigrationStateMachineTestWorker";

    /// In-memory fake CoordinatorStateAccess backed by a shared MigrationState
    /// cell — lets the orchestration tests observe DDB writes deterministically.
    struct FakeDao {
        state: Mutex<Option<MigrationState>>,
    }
    impl FakeDao {
        fn new() -> Arc<Self> {
            Arc::new(Self {
                state: Mutex::new(None),
            })
        }
    }
    #[async_trait]
    impl CoordinatorStateAccess for FakeDao {
        async fn get_coordinator_state(
            &self,
            _key: &str,
        ) -> Result<Option<CoordinatorState>, LeasingError> {
            Ok(self
                .state
                .lock()
                .unwrap()
                .clone()
                .map(CoordinatorState::MigrationState))
        }
        async fn list_coordinator_state_by_entity_type(
            &self,
            _t: crate::leases::CoordinatorStateType,
        ) -> Result<Vec<CoordinatorState>, LeasingError> {
            Ok(Vec::new())
        }
        async fn create_coordinator_state_if_not_exists(
            &self,
            state: &CoordinatorState,
        ) -> Result<bool, LeasingError> {
            if let CoordinatorState::MigrationState(m) = state {
                *self.state.lock().unwrap() = Some(m.clone());
            }
            Ok(true)
        }
        async fn update_coordinator_state_with_expectation(
            &self,
            state: &CoordinatorState,
            _e: HashMap<String, ExpectedAttributeValue>,
        ) -> Result<bool, LeasingError> {
            if let CoordinatorState::MigrationState(m) = state {
                *self.state.lock().unwrap() = Some(m.clone());
            }
            Ok(true)
        }
        async fn delete_coordinator_state(&self, _key: &str) -> Result<bool, LeasingError> {
            *self.state.lock().unwrap() = None;
            Ok(true)
        }
    }

    fn ready_data_leases() -> Vec<crate::leases::Lease> {
        (0..10)
            .map(|i| {
                crate::leases::Lease::new(
                    Some(format!("shard-{i}")),
                    Some(format!("MigrationReadyMonitorTestWorker{i}")),
                    0,
                    None,
                    None,
                    None,
                    None,
                    0,
                    Default::default(),
                    Default::default(),
                    None,
                    None,
                )
            })
            .collect()
    }

    fn ready_data_metrics(
    ) -> Vec<crate::worker::metricstats::worker_metric_stats::WorkerMetricStats> {
        (0..10)
            .map(|i| {
                crate::worker::metricstats::worker_metric_stats::WorkerMetricStats::legacy_builder()
                    .worker_id(format!("MigrationReadyMonitorTestWorker{i}"))
                    .last_update_time(10000)
                    .build()
            })
            .collect()
    }

    /// Build a mock initializer whose accessors return the given collaborators.
    // Test builder that wires the many collaborators the state machine needs;
    // a params struct would only add ceremony to a test helper.
    #[allow(clippy::too_many_arguments)]
    fn mock_initializer(
        leader: Arc<dyn crate::coordinator::leader_decider::LeaderDecider>,
        refresher: Arc<dyn crate::leases::lease_refresher::LeaseRefresher>,
        wms: Arc<
            dyn crate::coordinator::migration::migration_ready_monitor::WorkerMetricStatsSource,
        >,
        upgrade_called: Arc<AtomicBool>,
        flip_called: Arc<AtomicBool>,
        rollback_called: Arc<AtomicBool>,
        rollforward_called: Arc<AtomicBool>,
        upgrade3x_called: Arc<AtomicBool>,
    ) -> Arc<MockDynamicMigrationComponentsInitializer> {
        let mut init = MockDynamicMigrationComponentsInitializer::new();
        init.expect_metrics_factory()
            .returning(|| Arc::new(NullMetricsFactory::new()));
        init.expect_leader_decider()
            .returning(move || leader.clone());
        init.expect_worker_identifier()
            .returning(|| WORKER_ID.to_string());
        init.expect_worker_metrics_dao()
            .returning(move || wms.clone());
        init.expect_worker_metrics_expiry_seconds().returning(|| 1);
        init.expect_lease_refresher()
            .returning(move || refresher.clone());
        init.expect_initialize_client_version_for_phase1()
            .returning(|| ());
        init.expect_initialize_client_version_for_2x()
            .returning(move |_| {
                rollback_called.store(true, Ordering::SeqCst);
            });
        init.expect_initialize_client_version_for_upgrade_from_2x()
            .returning(move |_| {
                upgrade_called.store(true, Ordering::SeqCst);
                Ok(())
            });
        init.expect_initialize_client_version_for_3x_with_rollback()
            .returning(move |_| {
                flip_called.store(true, Ordering::SeqCst);
                Ok(())
            });
        init.expect_initialize_client_version_for_3x()
            .returning(move |from| {
                if from == ClientVersion::ClientVersion3xWithRollback {
                    upgrade3x_called.store(true, Ordering::SeqCst);
                }
                let _ = &rollforward_called;
                Ok(())
            });
        Arc::new(init)
    }

    fn random_zero() -> RandomDouble {
        Arc::new(|| 0.0)
    }

    fn build_sm(
        config: ClientVersionConfig,
        dao: Arc<FakeDao>,
        initializer: Arc<MockDynamicMigrationComponentsInitializer>,
        scheduler: Arc<RecordingScheduler>,
    ) -> Arc<MigrationStateMachineImpl> {
        MigrationStateMachineImpl::new(
            Arc::new(NullMetricsFactory::new()),
            Arc::new(|| 10000),
            dao,
            scheduler,
            config,
            random_zero(),
            initializer,
            WORKER_ID,
            0,
        )
    }

    fn leader_mock() -> Arc<MockLeaderDecider> {
        let mut d = MockLeaderDecider::new();
        d.expect_is_leader().returning(|_| true);
        Arc::new(d)
    }

    fn refresher_ready() -> Arc<MockLeaseRefresher> {
        let mut r = MockLeaseRefresher::new();
        r.expect_is_lease_owner_to_lease_key_index_active()
            .returning(|| Ok(true));
        r.expect_list_leases().returning(|| Ok(ready_data_leases()));
        Arc::new(r)
    }

    fn wms_ready() -> Arc<MockWorkerMetricStatsSource> {
        let mut w = MockWorkerMetricStatsSource::new();
        w.expect_get_all_worker_metric_stats()
            .returning(|| Ok(ready_data_metrics()));
        Arc::new(w)
    }

    #[tokio::test]
    async fn state_machine_initialization_upgrade_from_2x() {
        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
        );
        let sm = build_sm(
            ClientVersionConfig::CompatibleWith2x,
            dao.clone(),
            init,
            scheduler,
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersionUpgradeFrom2x
        );
        // DDB state was created (INIT -> UPGRADE_FROM_2X).
        assert!(dao.state.lock().unwrap().is_some());
    }

    #[tokio::test]
    async fn state_machine_initialization_3x() {
        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
        );
        let sm = build_sm(
            ClientVersionConfig::ClientVersionConfig3x,
            dao,
            init,
            scheduler,
        );
        sm.initialize().await.unwrap();
        // 3X is terminal -> immediately terminated -> reports 3X.
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion3x
        );
    }

    // The Java-parity panic in `get_current_client_version` (before initialize)
    // must not poison `inner`: after a caught panic (as in a `catch_unwind`-
    // guarded background loop) the state machine must remain fully usable.
    #[tokio::test]
    async fn get_current_client_version_panic_does_not_poison_the_lock() {
        use std::panic::{catch_unwind, AssertUnwindSafe};

        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
        );
        let sm = build_sm(
            ClientVersionConfig::ClientVersionConfig3x,
            dao,
            init,
            scheduler,
        );

        // Not initialized and not terminated -> Java-parity panic.
        let err = catch_unwind(AssertUnwindSafe(|| sm.get_current_client_version())).unwrap_err();
        assert_eq!(
            err.downcast_ref::<&str>().copied(),
            Some("No current state when state machine is either not initialized or already terminated")
        );

        // Lock is not poisoned: the full lifecycle still works on the same
        // instance.
        sm.initialize().await.unwrap();
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion3x
        );
    }

    #[tokio::test]
    async fn state_machine_initialization_phase1_enters_init() {
        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let phase1_called = Arc::new(AtomicBool::new(false));
        let mut init = MockDynamicMigrationComponentsInitializer::new();
        let p1 = phase1_called.clone();
        init.expect_initialize_client_version_for_phase1()
            .returning(move || {
                p1.store(true, Ordering::SeqCst);
            });
        let sm = build_sm(
            ClientVersionConfig::CompatibleWith2xPhase1,
            dao.clone(),
            Arc::new(init),
            scheduler,
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersionInit
        );
        assert!(phase1_called.load(Ordering::SeqCst));
        // No DDB write for Phase 1 INIT.
        assert!(dao.state.lock().unwrap().is_none());
    }

    #[tokio::test]
    async fn state_machine_initialization_phase1_honors_existing_state() {
        let dao = FakeDao::new();
        {
            let mut s = MigrationState::new(WORKER_ID);
            s.update(ClientVersion::ClientVersion3xWithRollback, WORKER_ID);
            *dao.state.lock().unwrap() = Some(s);
        }
        let scheduler = Arc::new(RecordingScheduler::new());
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
        );
        let sm = build_sm(
            ClientVersionConfig::CompatibleWith2xPhase1,
            dao,
            init,
            scheduler,
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion3xWithRollback
        );
    }

    #[tokio::test]
    async fn migration_ready_flip() {
        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let flip_called = Arc::new(AtomicBool::new(false));
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            Arc::new(AtomicBool::new(false)),
            flip_called.clone(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
        );
        let sm = build_sm(
            ClientVersionConfig::CompatibleWith2x,
            dao.clone(),
            init,
            scheduler.clone(),
        );
        sm.initialize().await.unwrap();

        // Two monitors scheduled: ready monitor (period == interval, no jitter)
        // and version-change monitor (jittered initial delay). Identify by
        // initial_delay: ready monitor initial_delay == period.
        // UpgradeFrom2x::enter schedules the migration-ready monitor first, then
        // the version-change monitor (order-stable).
        let calls = scheduler.calls();
        assert_eq!(calls.len(), 2);
        let ready_task = calls[0].task.clone();
        let version_task = calls[1].task.clone();

        // Run the ready monitor: leader + ready -> updates DDB to 3X_WITH_ROLLBACK.
        ready_task().await;
        assert_eq!(
            dao.state.lock().unwrap().as_ref().unwrap().client_version(),
            ClientVersion::ClientVersion3xWithRollback
        );

        // Run the version-change monitor: reads 3X_WITH_ROLLBACK -> transition.
        version_task().await;
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion3xWithRollback
        );
        assert!(flip_called.load(Ordering::SeqCst));
    }

    #[tokio::test]
    async fn rollback_before_flip() {
        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let rollback_called = Arc::new(AtomicBool::new(false));
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            rollback_called.clone(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
        );
        let sm = build_sm(
            ClientVersionConfig::CompatibleWith2x,
            dao.clone(),
            init,
            scheduler.clone(),
        );
        sm.initialize().await.unwrap();

        // UpgradeFrom2x::enter schedules the migration-ready monitor first (calls[0])
        // then the version-change monitor (calls[1]). Identify by scheduling order,
        // NOT by initial_delay-vs-period: with zero jitter both equal the period.
        let calls = scheduler.calls();
        assert_eq!(calls.len(), 2);
        let version_task = calls[1].task.clone();

        // Simulate a rollback: DDB now says 2X.
        {
            let mut s = MigrationState::new(WORKER_ID);
            s.update(ClientVersion::ClientVersion2x, WORKER_ID);
            *dao.state.lock().unwrap() = Some(s);
        }
        version_task().await;
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion2x
        );
        assert!(rollback_called.load(Ordering::SeqCst));
    }

    /// Java `initiateAndTestFlip`: drives the ready + version-change monitors so
    /// the machine flips UPGRADE_FROM_2X -> 3X_WITH_ROLLBACK. Resets the scheduler
    /// first (Java `reset(mockMigrationStateMachineThreadPool)`) so that after the
    /// flip only the newly-scheduled monitor is recorded.
    async fn initiate_and_test_flip(
        sm: &Arc<MigrationStateMachineImpl>,
        dao: &Arc<FakeDao>,
        scheduler: &Arc<RecordingScheduler>,
        flip_called: &Arc<AtomicBool>,
    ) {
        // UpgradeFrom2x::enter scheduled the ready monitor (calls[0]) then the
        // version-change monitor (calls[1]).
        let calls = scheduler.calls();
        assert_eq!(calls.len(), 2);
        let ready_task = calls[0].task.clone();
        let version_task = calls[1].task.clone();

        scheduler.reset();

        // Ready monitor: leader + ready -> updates DDB to 3X_WITH_ROLLBACK.
        ready_task().await;
        assert_eq!(
            dao.state.lock().unwrap().as_ref().unwrap().client_version(),
            ClientVersion::ClientVersion3xWithRollback
        );

        // Version-change monitor: reads 3X_WITH_ROLLBACK -> transition.
        version_task().await;
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion3xWithRollback
        );
        assert!(flip_called.load(Ordering::SeqCst));
    }

    /// Java `testRollbackAfterFlip`: after a flip to 3X_WITH_ROLLBACK, the newly
    /// scheduled rollback monitor fires (DDB now says 2X) and transitions back.
    #[tokio::test]
    async fn rollback_after_flip() {
        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let flip_called = Arc::new(AtomicBool::new(false));
        let rollback_called = Arc::new(AtomicBool::new(false));
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            Arc::new(AtomicBool::new(false)),
            flip_called.clone(),
            rollback_called.clone(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
        );
        let sm = build_sm(
            ClientVersionConfig::CompatibleWith2x,
            dao.clone(),
            init,
            scheduler.clone(),
        );
        sm.initialize().await.unwrap();

        initiate_and_test_flip(&sm, &dao, &scheduler, &flip_called).await;

        // 3X_WITH_ROLLBACK::enter scheduled a new rollback monitor (calls[0] after reset).
        let calls = scheduler.calls();
        assert_eq!(calls.len(), 1);
        let rollback_task = calls[0].task.clone();

        // Simulate a rollback: DDB now says 2X.
        {
            let mut s = MigrationState::new(WORKER_ID);
            s.update(ClientVersion::ClientVersion2x, WORKER_ID);
            *dao.state.lock().unwrap() = Some(s);
        }
        rollback_task().await;
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion2x
        );
        // initializeClientVersionFor2x(3X_WITH_ROLLBACK) was invoked.
        assert!(rollback_called.load(Ordering::SeqCst));
    }

    /// Java `testRollForward`: flip -> rollback to 2X -> the 2X roll-forward
    /// monitor fires (DDB says UPGRADE_FROM_2X) and transitions forward again.
    #[tokio::test]
    async fn roll_forward() {
        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let flip_called = Arc::new(AtomicBool::new(false));
        let rollback_called = Arc::new(AtomicBool::new(false));
        let upgrade_called = Arc::new(AtomicBool::new(false));
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            upgrade_called.clone(),
            flip_called.clone(),
            rollback_called.clone(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
        );
        let sm = build_sm(
            ClientVersionConfig::CompatibleWith2x,
            dao.clone(),
            init,
            scheduler.clone(),
        );
        sm.initialize().await.unwrap();

        initiate_and_test_flip(&sm, &dao, &scheduler, &flip_called).await;

        // Rollback: run the new rollback monitor with DDB = 2X.
        let calls = scheduler.calls();
        assert_eq!(calls.len(), 1);
        let rollback_task = calls[0].task.clone();
        scheduler.reset();
        {
            let mut s = MigrationState::new(WORKER_ID);
            s.update(ClientVersion::ClientVersion2x, WORKER_ID);
            *dao.state.lock().unwrap() = Some(s);
        }
        rollback_task().await;
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion2x
        );
        assert!(rollback_called.load(Ordering::SeqCst));

        // 2X::enter scheduled a new roll-forward monitor (calls[0] after reset).
        let calls = scheduler.calls();
        assert_eq!(calls.len(), 1);
        let rollforward_task = calls[0].task.clone();

        // Roll forward: DDB now says UPGRADE_FROM_2X.
        {
            let mut s = MigrationState::new(WORKER_ID);
            s.update(ClientVersion::ClientVersionUpgradeFrom2x, WORKER_ID);
            *dao.state.lock().unwrap() = Some(s);
        }
        rollforward_task().await;
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersionUpgradeFrom2x
        );
        // initializeClientVersionForUpgradeFrom2x(2X) was invoked.
        assert!(upgrade_called.load(Ordering::SeqCst));
    }

    /// Java `successfulUpgradeAfterFlip`: after a flip to 3X_WITH_ROLLBACK, the
    /// rollback monitor sees DDB = 3X (customer switched) and transitions to the
    /// terminal 3X state (initializeClientVersionFor3x called).
    #[tokio::test]
    async fn successful_upgrade_after_flip() {
        let dao = FakeDao::new();
        let scheduler = Arc::new(RecordingScheduler::new());
        let flip_called = Arc::new(AtomicBool::new(false));
        let upgrade3x_called = Arc::new(AtomicBool::new(false));
        let init = mock_initializer(
            leader_mock(),
            refresher_ready(),
            wms_ready(),
            Arc::new(AtomicBool::new(false)),
            flip_called.clone(),
            Arc::new(AtomicBool::new(false)),
            Arc::new(AtomicBool::new(false)),
            upgrade3x_called.clone(),
        );
        let sm = build_sm(
            ClientVersionConfig::CompatibleWith2x,
            dao.clone(),
            init,
            scheduler.clone(),
        );
        sm.initialize().await.unwrap();

        initiate_and_test_flip(&sm, &dao, &scheduler, &flip_called).await;

        // 3X_WITH_ROLLBACK::enter scheduled a monitor (calls[0] after reset).
        let calls = scheduler.calls();
        assert_eq!(calls.len(), 1);
        let upgrade_task = calls[0].task.clone();

        // Customer switched to 3.x: DDB now says 3X.
        {
            let mut s = MigrationState::new(WORKER_ID);
            s.update(ClientVersion::ClientVersion3x, WORKER_ID);
            *dao.state.lock().unwrap() = Some(s);
        }
        upgrade_task().await;
        assert_eq!(
            sm.get_current_client_version(),
            ClientVersion::ClientVersion3x
        );
        // initializeClientVersionFor3x(3X_WITH_ROLLBACK) was invoked.
        assert!(upgrade3x_called.load(Ordering::SeqCst));
    }
}
