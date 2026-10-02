//! Port of
//! `software.amazon.kinesis.coordinator.migration.ClientVersionChangeMonitor`.

use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Mutex};

use crate::coordinator::coordinator_state_dao::CoordinatorStateAccess;
use crate::coordinator::migration::client_version::ClientVersion;
use crate::coordinator::migration::migration_state::{MigrationState, MIGRATION_HASH_KEY};
use crate::coordinator::migration::monitor_scheduler::{MonitorScheduler, ScheduledHandle};
use crate::leases::exceptions::LeasingError;
use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};

use aws_sdk_cloudwatch::types::StandardUnit;

/// Java `ClientVersionChangeMonitor.ClientVersionChangeCallback` — invoked once
/// when a `clientVersion != expectedVersion` is observed. May fail with
/// `InvalidState`/`Dependency` (does NOT auto-cancel the monitor).
pub type ClientVersionChangeCallback = Arc<
    dyn Fn(MigrationState) -> Pin<Box<dyn Future<Output = Result<(), LeasingError>> + Send>>
        + Send
        + Sync,
>;

const MONITOR_INTERVAL_MILLIS: u64 = 60_000;
const JITTER_FACTOR: f64 = 0.5;

/// Injectable RNG (`random.nextDouble()`), matching Java `Random`.
pub type RandomDouble = Arc<dyn Fn() -> f64 + Send + Sync>;

struct MonitorState {
    /// `Some` while scheduled (Java non-null `scheduledFuture`). Also acts as
    /// the "cancelled" sentinel: `run()` no-ops when `None`.
    handle: Option<ScheduledHandle>,
    /// Set once cancelled/self-cancelled to mirror Java nulling
    /// `scheduledFuture` inside `run()` (so `run()` becomes a no-op).
    cancelled: bool,
}

/// Generic polling monitor that reads `MigrationState.clientVersion` from DDB
/// and invokes a callback exactly once when it observes a value different from
/// `expected_version`, then self-cancels. Java `ClientVersionChangeMonitor`.
pub struct ClientVersionChangeMonitor {
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
    scheduler: Arc<dyn MonitorScheduler>,
    callback: ClientVersionChangeCallback,
    expected_version: ClientVersion,
    random: RandomDouble,
    state: Mutex<MonitorState>,
}

impl ClientVersionChangeMonitor {
    /// Java constructor.
    pub fn new(
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
        scheduler: Arc<dyn MonitorScheduler>,
        callback: ClientVersionChangeCallback,
        expected_version: ClientVersion,
        random: RandomDouble,
    ) -> Self {
        Self {
            metrics_factory,
            coordinator_state_dao,
            scheduler,
            callback,
            expected_version,
            random,
            state: Mutex::new(MonitorState {
                handle: None,
                cancelled: false,
            }),
        }
    }

    /// Java `startMonitor()`: idempotent scheduling with initial jitter.
    pub fn start_monitor(self: &Arc<Self>) {
        let mut st = self.state.lock().expect("poisoned");
        if st.handle.is_some() {
            return;
        }
        let jitter = ((self.random)() * MONITOR_INTERVAL_MILLIS as f64 * JITTER_FACTOR) as u64;
        let initial_delay = MONITOR_INTERVAL_MILLIS + jitter;
        tracing::info!(
            expected = ?self.expected_version,
            period = MONITOR_INTERVAL_MILLIS,
            initial_delay,
            "Monitoring for MigrationState client version change"
        );
        let this = self.clone();
        let task = Arc::new(move || {
            let this = this.clone();
            Box::pin(async move {
                this.run().await;
            }) as Pin<Box<dyn Future<Output = ()> + Send>>
        });
        let handle =
            self.scheduler
                .schedule_with_fixed_delay(task, initial_delay, MONITOR_INTERVAL_MILLIS);
        st.handle = Some(handle);
    }

    /// Java `cancel()`. **Must not be called from within the callback's lock**
    /// (see the state impls which spawn cancel on a separate task).
    pub fn cancel(&self) {
        let mut st = self.state.lock().expect("poisoned");
        if let Some(h) = st.handle.take() {
            tracing::info!(expected = ?self.expected_version, "Cancelling ClientVersionChangeMonitor");
            h.cancel();
        }
        st.cancelled = true;
    }

    /// Java `run()`: read DDB, if the version differs, invoke the callback then
    /// self-cancel. All exceptions from the callback or the DDB read are caught,
    /// logged, and swallowed (monitor keeps polling).
    pub async fn run(&self) {
        // Java `run()` is synchronized and no-ops if scheduledFuture == null.
        {
            let st = self.state.lock().expect("poisoned");
            if st.cancelled {
                tracing::debug!("Monitor has been cancelled, not running");
                return;
            }
        }
        self.emit_metrics();
        let result = self
            .coordinator_state_dao
            .get_coordinator_state(MIGRATION_HASH_KEY)
            .await;
        let migration_state = match result {
            Ok(Some(cs)) => cs.as_migration_state().cloned(),
            Ok(None) => None,
            Err(e) => {
                tracing::warn!(?e, expected = ?self.expected_version, "Exception monitoring client version change, will retry");
                return;
            }
        };
        if let Some(state) = migration_state {
            if state.client_version() != self.expected_version {
                tracing::info!(
                    ?state,
                    "MigrationState client version changed, invoking callback"
                );
                match (self.callback)(state).await {
                    Ok(()) => {
                        tracing::info!("Callback successful, monitor cancelling itself");
                        // self-cancel: stop further monitoring
                        let mut st = self.state.lock().expect("poisoned");
                        if let Some(h) = st.handle.take() {
                            h.cancel();
                        }
                        st.cancelled = true;
                    }
                    Err(e) => {
                        // Java swallows the exception; monitor keeps polling.
                        tracing::warn!(?e, expected = ?self.expected_version, "Callback failed, will retry");
                    }
                }
            }
        }
    }

    /// Whether the monitor has self-cancelled or been cancelled (test aid).
    pub fn is_cancelled(&self) -> bool {
        self.state.lock().expect("poisoned").cancelled
    }

    fn emit_metrics(&self) {
        let mut scope = metrics_util::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            crate::coordinator::migration::migration_state_machine::METRICS_OPERATION,
        );
        match self.expected_version {
            ClientVersion::ClientVersion3xWithRollback => {
                scope.add_data_with_level(
                    "CurrentState:3xWorker",
                    1.0,
                    StandardUnit::Count,
                    MetricsLevel::Summary,
                );
            }
            ClientVersion::ClientVersion2x | ClientVersion::ClientVersionUpgradeFrom2x => {
                scope.add_data_with_level(
                    "CurrentState:2xCompatibleWorker",
                    1.0,
                    StandardUnit::Count,
                    MetricsLevel::Summary,
                );
            }
            other => {
                metrics_util::end_scope(scope.as_mut());
                panic!("Unexpected version {}", other.name());
            }
        }
        metrics_util::end_scope(scope.as_mut());
    }
}

impl std::fmt::Display for ClientVersionChangeMonitor {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "ClientVersionChangeMonitor[{:?}]", self.expected_version)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};

    use crate::coordinator::coordinator_state::CoordinatorState;
    use crate::coordinator::coordinator_state_dao::MockCoordinatorStateAccess;
    use crate::coordinator::migration::monitor_scheduler::RecordingScheduler;
    use crate::metrics::NullMetricsFactory;

    fn migration_state(cv: ClientVersion) -> MigrationState {
        let mut s = MigrationState::new("DUMMY_WORKER");
        s.update(cv, "DUMMY_WORKER");
        s
    }

    /// A recording callback: counts invocations; optionally fails.
    #[derive(Clone, Default)]
    struct RecordingCallback {
        count: Arc<AtomicUsize>,
        fail: Arc<std::sync::atomic::AtomicBool>,
    }
    impl RecordingCallback {
        fn callback(&self) -> ClientVersionChangeCallback {
            let count = self.count.clone();
            let fail = self.fail.clone();
            Arc::new(move |_state: MigrationState| {
                let count = count.clone();
                let fail = fail.clone();
                Box::pin(async move {
                    count.fetch_add(1, Ordering::SeqCst);
                    if fail.load(Ordering::SeqCst) {
                        Err(LeasingError::invalid_state("test exception"))
                    } else {
                        Ok(())
                    }
                }) as _
            })
        }
        fn count(&self) -> usize {
            self.count.load(Ordering::SeqCst)
        }
    }

    fn random_zero() -> RandomDouble {
        Arc::new(|| 0.0)
    }

    async fn run_monitor_test(current: ClientVersion, changed: ClientVersion) {
        let cb = RecordingCallback::default();
        let mut dao = MockCoordinatorStateAccess::new();
        let calls = Arc::new(AtomicUsize::new(0));
        let calls_c = calls.clone();
        let initial = migration_state(current);
        let changed_state = migration_state(changed);
        dao.expect_get_coordinator_state().returning(move |_| {
            let n = calls_c.fetch_add(1, Ordering::SeqCst);
            let s = if n == 0 {
                initial.clone()
            } else {
                changed_state.clone()
            };
            Ok(Some(CoordinatorState::MigrationState(s)))
        });

        let scheduler = Arc::new(RecordingScheduler::new());
        let monitor = Arc::new(ClientVersionChangeMonitor::new(
            Arc::new(NullMetricsFactory::new()),
            Arc::new(dao),
            scheduler.clone(),
            cb.callback(),
            current,
            random_zero(),
        ));
        monitor.start_monitor();
        assert_eq!(scheduler.call_count(), 1);

        // First run: no change -> no callback.
        monitor.run().await;
        assert_eq!(cb.count(), 0);

        // Second run: changed -> callback once.
        monitor.run().await;
        assert_eq!(cb.count(), 1);
    }

    #[tokio::test]
    async fn test_monitor_2x_to_upgrade() {
        run_monitor_test(
            ClientVersion::ClientVersion2x,
            ClientVersion::ClientVersionUpgradeFrom2x,
        )
        .await;
    }

    #[tokio::test]
    async fn test_monitor_3x_with_rollback_to_2x() {
        run_monitor_test(
            ClientVersion::ClientVersion3xWithRollback,
            ClientVersion::ClientVersion2x,
        )
        .await;
    }

    #[tokio::test]
    async fn test_monitor_upgrade_to_3x_with_rollback() {
        run_monitor_test(
            ClientVersion::ClientVersionUpgradeFrom2x,
            ClientVersion::ClientVersion3xWithRollback,
        )
        .await;
    }

    #[tokio::test]
    async fn test_monitor_3x_with_rollback_to_3x() {
        run_monitor_test(
            ClientVersion::ClientVersion3xWithRollback,
            ClientVersion::ClientVersion3x,
        )
        .await;
    }

    #[tokio::test]
    async fn test_call_is_invoked_only_once_if_successful() {
        let cb = RecordingCallback::default();
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(move |_| {
            Ok(Some(CoordinatorState::MigrationState(migration_state(
                ClientVersion::ClientVersionUpgradeFrom2x,
            ))))
        });
        let scheduler = Arc::new(RecordingScheduler::new());
        let monitor = Arc::new(ClientVersionChangeMonitor::new(
            Arc::new(NullMetricsFactory::new()),
            Arc::new(dao),
            scheduler,
            cb.callback(),
            ClientVersion::ClientVersion2x,
            random_zero(),
        ));
        monitor.start_monitor();

        monitor.run().await;
        assert_eq!(cb.count(), 1);
        // After a successful callback, the monitor self-cancels and no-ops.
        monitor.run().await;
        assert_eq!(cb.count(), 1);
        assert!(monitor.is_cancelled());
    }

    #[tokio::test]
    async fn test_call_is_invoked_again_if_failed() {
        let cb = RecordingCallback {
            count: Arc::new(AtomicUsize::new(0)),
            fail: Arc::new(std::sync::atomic::AtomicBool::new(true)),
        };
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(move |_| {
            Ok(Some(CoordinatorState::MigrationState(migration_state(
                ClientVersion::ClientVersionUpgradeFrom2x,
            ))))
        });
        let scheduler = Arc::new(RecordingScheduler::new());
        let monitor = Arc::new(ClientVersionChangeMonitor::new(
            Arc::new(NullMetricsFactory::new()),
            Arc::new(dao),
            scheduler,
            cb.callback(),
            ClientVersion::ClientVersion2x,
            random_zero(),
        ));
        monitor.start_monitor();

        // Callback fails -> monitor does not self-cancel, keeps invoking.
        monitor.run().await;
        assert_eq!(cb.count(), 1);
        monitor.run().await;
        assert_eq!(cb.count(), 2);

        // Now callback succeeds -> self-cancels; subsequent runs no-op.
        cb.fail.store(false, Ordering::SeqCst);
        monitor.run().await;
        assert_eq!(cb.count(), 3);
        monitor.run().await;
        assert_eq!(cb.count(), 3);
    }
}
