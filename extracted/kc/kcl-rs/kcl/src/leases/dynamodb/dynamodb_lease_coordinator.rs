//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBLeaseCoordinator`.
//!
//! Top-level per-worker orchestrator implementing [`LeaseCoordinator`]: owns and
//! schedules the [`DynamoDBLeaseTaker`], [`DynamoDBLeaseRenewer`], and
//! [`DynamoDBLeaseDiscoverer`] components, and exposes the combined view of
//! currently-held leases/assignments.
//!
//! # Background loops (spawned tokio tasks)
//!
//! Java uses a 3-thread `ScheduledExecutorService` running three periodic jobs:
//!
//! | Job          | Java scheduling         | Cadence                                  |
//! |--------------|-------------------------|------------------------------------------|
//! | Taker        | `scheduleWithFixedDelay` | `(leaseDuration + epsilon) * 2` ms       |
//! | LeaseDiscovery | `scheduleAtFixedRate`  | `leaseAssignmentInterval / 2 - epsilon` ms |
//! | Renewer      | `scheduleAtFixedRate`   | `leaseDuration / 3 - epsilon` ms         |
//!
//! Each Rust loop is a spawned task driven by [`tokio::time::interval`] (fixed
//! rate: `MissedTickBehavior::Delay` approximates fixed-delay for the taker),
//! cancellable via a level-triggered [`CancellationToken`] (a `Notify` can lose
//! a signal sent while a loop is mid-tick); `stop` cancels the token and awaits
//! the [`JoinHandle`]s, bounded by [`STOP_WAIT_TIME_MILLIS`], aborting only the
//! stragglers (Java `awaitTermination` then `shutdownNow`). Like Java's
//! runnables — which catch `Throwable` — each loop iteration is wrapped in
//! `catch_unwind`, so a panic is logged and the loop keeps running rather than
//! silently killing lease renewal. The injectable period lets tests drive
//! cadence deterministically with `tokio(start_paused = true)`.
//!
//! Both the Taker and LeaseDiscovery loops check the lease-assignment mode at
//! execution time under the `shutdown` lock and no-op unless it matches their
//! active mode — supporting live KCLv2.x⇄KCLv3.x migration while both loops stay
//! registered. The `running` flag (an `AtomicBool` under the `shutdown` lock)
//! gates whether taken/discovered leases actually get added to the renewer.
//!
//! # Deviations
//!
//! - `initial_lease_table_read_capacity` / `initial_lease_table_write_capacity`
//!   (Java's deprecated fluent capacity setters that mutate + return the concrete
//!   type) live on this struct — they were dropped from the trait (see the
//!   [`LeaseCoordinator`] docs). They are constructor fields validated `>= 1`.
//! - `LeaseGracefulShutdownHandler` (lifecycle wave 7) is not yet ported; the
//!   graceful-shutdown callback wired into the renewer is a no-op placeholder and
//!   `stopLeaseTaker`'s handler-stop is a `// TODO(port)`.
//! - The taker/discoverer mode gates mirror Java's runnables: the taker loop
//!   executes only in `DefaultLeaseCountBasedAssignment` mode and the discovery
//!   loop only in `WorkerUtilizationAwareAssignment` mode, re-checked every tick
//!   (Java `TakerRunnable`/`LeaseDiscoveryRunnable`). An uninitialized provider
//!   maps to Java's `IllegalStateException` from `getLeaseAssignmentMode()`,
//!   which the runnable's catch block logs — the tick is skipped, the loop
//!   survives.

use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};

use async_trait::async_trait;
use futures::FutureExt;
use tokio::task::JoinHandle;
use tokio_util::sync::CancellationToken;
use uuid::Uuid;

use crate::common::get_renewer_taker_interval_millis;
use crate::coordinator::{
    LeaseAssignmentMode, MigrationAdaptiveLeaseAssignmentModeProvider, StreamIdCacheManager,
};
use crate::leases::exceptions::LeasingError;
use crate::leases::lease_management_config::{
    GracefulLeaseHandoffConfig, WorkerUtilizationAwareAssignmentConfig,
};
use crate::leases::{
    Lease, LeaseCoordinator, LeaseDiscoverer, LeaseRefresher, LeaseRenewer, LeaseStatsRecorder,
    LeaseTaker, ShardInfo,
};
use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};

use super::dynamodb_lease_discoverer::DynamoDBLeaseDiscoverer;
use super::dynamodb_lease_renewer::{DynamoDBLeaseRenewer, GracefulShutdownCallback};
use super::dynamodb_lease_taker::DynamoDBLeaseTaker;

/// Time to wait for in-flight background tasks to finish on `stop`.
pub const STOP_WAIT_TIME_MILLIS: u64 = 2000;

/// DynamoDB implementation of [`LeaseCoordinator`].
pub struct DynamoDBLeaseCoordinator {
    lease_renewer: Arc<dyn LeaseRenewer>,
    lease_taker: Arc<dyn LeaseTaker>,
    lease_discoverer: Arc<dyn LeaseDiscoverer>,
    renewer_interval_millis: i64,
    taker_interval_millis: i64,
    lease_discoverer_interval_millis: i64,
    lease_refresher: Arc<dyn LeaseRefresher>,
    lease_stats_recorder: Arc<LeaseStatsRecorder>,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    worker_identifier: String,
    #[allow(dead_code)]
    initial_lease_table_read_capacity: i64,
    #[allow(dead_code)]
    initial_lease_table_write_capacity: i64,
    #[allow(dead_code)]
    worker_utilization_aware_assignment_config: WorkerUtilizationAwareAssignmentConfig,

    /// `running` + task handles, guarded like Java's `shutdownLock`.
    inner: Mutex<CoordinatorInner>,
    running: Arc<AtomicBool>,
    consumer_id: Mutex<String>,
}

#[derive(Default)]
struct CoordinatorInner {
    shutdown: Option<CancellationToken>,
    taker_handle: Option<JoinHandle<()>>,
    discovery_handle: Option<JoinHandle<()>>,
    renewer_handle: Option<JoinHandle<()>>,
    /// Whether the taker loop was started (Java `takerFuture != null`).
    taker_started: bool,
}

impl DynamoDBLeaseCoordinator {
    /// Java constructor. Builds the taker, renewer, and discoverer and computes
    /// the three loop intervals.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if either capacity is `< 1`.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        lease_refresher: Arc<dyn LeaseRefresher>,
        worker_identifier: impl Into<String>,
        lease_duration_millis: i64,
        enable_priority_lease_assignment: bool,
        epsilon_millis: i64,
        max_leases_for_worker: i32,
        max_leases_to_steal_at_one_time: i32,
        _max_lease_renewer_thread_count: i32,
        initial_lease_table_read_capacity: i64,
        initial_lease_table_write_capacity: i64,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        worker_utilization_aware_assignment_config: WorkerUtilizationAwareAssignmentConfig,
        _graceful_lease_handoff_config: GracefulLeaseHandoffConfig,
        lease_assignment_interval_millis: i64,
        stream_id_cache_manager: Option<StreamIdCacheManager>,
        lease_table_scan_total_segments: i32,
    ) -> Self {
        let worker_identifier = worker_identifier.into();

        let renewer_interval_millis =
            get_renewer_taker_interval_millis(lease_duration_millis, epsilon_millis);
        let taker_interval_millis = (lease_duration_millis + epsilon_millis) * 2;
        // Runs twice per assignment interval to find new leases before expiry.
        let lease_discoverer_interval_millis =
            (lease_assignment_interval_millis / 2) - epsilon_millis;

        let lease_stats_recorder = Arc::new(LeaseStatsRecorder::new(
            renewer_interval_millis,
            Arc::new(now_millis),
        ));

        let lease_taker: Arc<dyn LeaseTaker> = Arc::new(
            DynamoDBLeaseTaker::new_with_cache_manager(
                lease_refresher.clone(),
                worker_identifier.clone(),
                lease_duration_millis,
                metrics_factory.clone(),
                stream_id_cache_manager,
            )
            .with_max_leases_for_worker(max_leases_for_worker)
            .with_max_leases_to_steal_at_one_time(max_leases_to_steal_at_one_time)
            .with_enable_priority_lease_assignment(enable_priority_lease_assignment),
        );

        // TODO(port) — lifecycle wave (7): LeaseGracefulShutdownHandler. Until it
        // is ported, the graceful-shutdown callback is a no-op placeholder.
        let graceful_shutdown_callback: GracefulShutdownCallback = Arc::new(|_lease| {});

        let lease_renewer: Arc<dyn LeaseRenewer> = Arc::new(DynamoDBLeaseRenewer::new(
            lease_refresher.clone(),
            worker_identifier.clone(),
            lease_duration_millis,
            metrics_factory.clone(),
            lease_stats_recorder.clone(),
            graceful_shutdown_callback,
            lease_table_scan_total_segments,
        ));

        let lease_discoverer: Arc<dyn LeaseDiscoverer> = Arc::new(DynamoDBLeaseDiscoverer::new(
            lease_refresher.clone(),
            lease_renewer.clone(),
            metrics_factory.clone(),
            worker_identifier.clone(),
        ));

        if initial_lease_table_read_capacity <= 0 {
            panic!("readCapacity should be >= 1");
        }
        if initial_lease_table_write_capacity <= 0 {
            panic!("writeCapacity should be >= 1");
        }

        Self {
            lease_renewer,
            lease_taker,
            lease_discoverer,
            renewer_interval_millis,
            taker_interval_millis,
            lease_discoverer_interval_millis,
            lease_refresher,
            lease_stats_recorder,
            metrics_factory,
            worker_identifier,
            initial_lease_table_read_capacity,
            initial_lease_table_write_capacity,
            worker_utilization_aware_assignment_config,
            inner: Mutex::new(CoordinatorInner::default()),
            running: Arc::new(AtomicBool::new(false)),
            consumer_id: Mutex::new(String::new()),
        }
    }

    /// Java deprecated fluent `initialLeaseTableReadCapacity(long)` setter.
    ///
    /// # Panics
    /// Panics if `< 1`.
    pub fn set_initial_lease_table_read_capacity(mut self, read_capacity: i64) -> Self {
        if read_capacity <= 0 {
            panic!("readCapacity should be >= 1");
        }
        self.initial_lease_table_read_capacity = read_capacity;
        self
    }

    /// Java deprecated fluent `initialLeaseTableWriteCapacity(long)` setter.
    ///
    /// # Panics
    /// Panics if `< 1`.
    pub fn set_initial_lease_table_write_capacity(mut self, write_capacity: i64) -> Self {
        if write_capacity <= 0 {
            panic!("writeCapacity should be >= 1");
        }
        self.initial_lease_table_write_capacity = write_capacity;
        self
    }

    /// Whether the taker loop was started (test seam mirroring Java's
    /// `takerFuture != null` reflection check).
    pub fn is_taker_started(&self) -> bool {
        self.inner.lock().unwrap().taker_started
    }

    /// Java `convertLeaseToAssignment` — build a [`ShardInfo`] from a lease,
    /// branching on multi-stream vs single-stream.
    pub fn convert_lease_to_assignment(lease: &Lease) -> ShardInfo {
        let concurrency_token = lease.concurrency_token().map(|t| t.to_string());
        if lease.is_multi_stream() {
            ShardInfo::new(
                lease.shard_id().unwrap_or("").to_string(),
                concurrency_token,
                lease.parent_shard_ids(),
                lease.checkpoint().cloned(),
                Some(lease.stream_identifier().unwrap_or("").to_string()),
            )
        } else {
            ShardInfo::single_stream(
                lease.lease_key().unwrap_or("").to_string(),
                concurrency_token,
                lease.parent_shard_ids(),
                lease.checkpoint().cloned(),
            )
        }
    }

    /// A shared handle to the `running` flag (Java's `volatile running`), so the
    /// background taker loop can gate lease additions under the shutdown lock.
    fn running_flag(&self) -> Arc<AtomicBool> {
        self.running.clone()
    }

    /// Should the taker loop be scheduled given the mode provider? Java's
    /// `dynamicModeChangeSupportNeeded() || mode == DEFAULT_LEASE_COUNT_BASED`.
    /// If the mode isn't initialized yet, default to the dual-mode path (taker
    /// started).
    fn should_start_taker(provider: &MigrationAdaptiveLeaseAssignmentModeProvider) -> bool {
        provider.dynamic_mode_change_support_needed()
            || matches!(
                provider.get_lease_assignment_mode(),
                Ok(LeaseAssignmentMode::DefaultLeaseCountBasedAssignment) | Err(_)
            )
    }
}

#[async_trait]
impl LeaseCoordinator for DynamoDBLeaseCoordinator {
    async fn initialize(&self) -> Result<(), LeasingError> {
        let new_table_created = self
            .lease_refresher
            .create_lease_table_if_not_exists()
            .await?;
        if new_table_created {
            tracing::info!(
                "Created new lease table for coordinator with pay per request billing mode."
            );
        }
        let seconds_between_polls = 10;
        let timeout_seconds = 600;
        let is_table_active = self
            .lease_refresher
            .wait_until_lease_table_exists(seconds_between_polls, timeout_seconds)
            .await?;
        if !is_table_active {
            return Err(LeasingError::dependency("Creating table timeout"));
        }
        *self.consumer_id.lock().unwrap() =
            self.lease_refresher.get_lease_table_identifier().await?;
        Ok(())
    }

    async fn start(
        &self,
        lease_assignment_mode_provider: Arc<MigrationAdaptiveLeaseAssignmentModeProvider>,
    ) -> Result<(), LeasingError> {
        self.lease_renewer.initialize().await?;

        let shutdown = CancellationToken::new();
        let start_taker = Self::should_start_taker(&lease_assignment_mode_provider);

        let mut inner = self.inner.lock().unwrap();

        // --- Taker loop (fixed-delay cadence) ---
        if start_taker {
            let taker = self.lease_taker.clone();
            let renewer = self.lease_renewer.clone();
            let metrics_factory = self.metrics_factory.clone();
            let worker_identifier = self.worker_identifier.clone();
            let running = self.running_flag();
            let period = std::time::Duration::from_millis(self.taker_interval_millis.max(1) as u64);
            let sd = shutdown.clone();
            let provider = lease_assignment_mode_provider.clone();
            let handle = tokio::spawn(async move {
                let mut interval = tokio::time::interval(period);
                interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
                loop {
                    tokio::select! {
                        biased;
                        _ = sd.cancelled() => break,
                        _ = interval.tick() => {
                            // Java TakerRunnable: LeaseTaker is run in
                            // DEFAULT_LEASE_COUNT_BASED_ASSIGNMENT mode only.
                            match provider.get_lease_assignment_mode() {
                                Ok(LeaseAssignmentMode::DefaultLeaseCountBasedAssignment) => {}
                                Ok(_) => continue,
                                Err(e) => {
                                    // Java: IllegalStateException from an uninitialized
                                    // provider is caught by the runnable and logged.
                                    tracing::error!(
                                        "Throwable encountered in lease taking thread: {}", e
                                    );
                                    continue;
                                }
                            }
                            // Java TakerRunnable catches LeasingException AND Throwable.
                            let run = std::panic::AssertUnwindSafe(run_lease_taker_once(
                                &*taker,
                                &*renewer,
                                metrics_factory.as_ref(),
                                &worker_identifier,
                                &running,
                            ))
                            .catch_unwind()
                            .await;
                            match run {
                                Ok(Ok(())) => {}
                                Ok(Err(e)) => tracing::error!(
                                    "LeasingException encountered in lease taking thread: {}", e
                                ),
                                Err(panic) => tracing::error!(
                                    "Throwable encountered in lease taking thread: {}",
                                    panic_message(panic.as_ref())
                                ),
                            }
                        }
                    }
                }
            });
            inner.taker_handle = Some(handle);
            inner.taker_started = true;
        }

        // --- LeaseDiscovery loop (fixed-rate cadence) ---
        {
            let discoverer = self.lease_discoverer.clone();
            let renewer = self.lease_renewer.clone();
            let running = self.running_flag();
            let period = std::time::Duration::from_millis(
                self.lease_discoverer_interval_millis.max(1) as u64,
            );
            let sd = shutdown.clone();
            let provider = lease_assignment_mode_provider.clone();
            let handle = tokio::spawn(async move {
                let mut interval = tokio::time::interval(period);
                loop {
                    tokio::select! {
                        biased;
                        _ = sd.cancelled() => break,
                        _ = interval.tick() => {
                            // Java LeaseDiscoveryRunnable: LeaseDiscoverer is run in
                            // WORKER_UTILIZATION_AWARE_ASSIGNMENT mode only (the
                            // GSI it queries is only created by the KCLv3 migration
                            // machinery), and only while `running`.
                            match provider.get_lease_assignment_mode() {
                                Ok(LeaseAssignmentMode::WorkerUtilizationAwareAssignment) => {}
                                Ok(_) => continue,
                                Err(e) => {
                                    tracing::error!("Failed to execute lease discovery: {}", e);
                                    continue;
                                }
                            }
                            if !running.load(Ordering::SeqCst) {
                                continue;
                            }
                            // Java LeaseDiscoveryRunnable catches Exception; a panic maps
                            // from Java unchecked exceptions, so it must not kill the loop.
                            let run = std::panic::AssertUnwindSafe(discoverer.discover_new_leases())
                                .catch_unwind()
                                .await;
                            match run {
                                Ok(Ok(new_leases)) => renewer.add_leases_to_renew(new_leases),
                                Ok(Err(e)) => tracing::error!("Failed to execute lease discovery: {}", e),
                                Err(panic) => tracing::error!(
                                    "Failed to execute lease discovery: {}",
                                    panic_message(panic.as_ref())
                                ),
                            }
                        }
                    }
                }
            });
            inner.discovery_handle = Some(handle);
        }

        // --- Renewer loop (fixed-rate cadence) ---
        {
            let renewer = self.lease_renewer.clone();
            let period =
                std::time::Duration::from_millis(self.renewer_interval_millis.max(1) as u64);
            let sd = shutdown.clone();
            let handle = tokio::spawn(async move {
                let mut interval = tokio::time::interval(period);
                loop {
                    tokio::select! {
                        biased;
                        _ = sd.cancelled() => break,
                        _ = interval.tick() => {
                            // Java RenewerRunnable catches LeasingException AND Throwable.
                            let run = std::panic::AssertUnwindSafe(renewer.renew_leases())
                                .catch_unwind()
                                .await;
                            match run {
                                Ok(Ok(())) => {}
                                Ok(Err(e)) => tracing::error!(
                                    "LeasingException encountered in lease renewing thread: {}", e
                                ),
                                Err(panic) => tracing::error!(
                                    "Throwable encountered in lease renewing thread: {}",
                                    panic_message(panic.as_ref())
                                ),
                            }
                        }
                    }
                }
            });
            inner.renewer_handle = Some(handle);
        }

        inner.shutdown = Some(shutdown);
        drop(inner);

        // TODO(port) — lifecycle wave (7): leaseGracefulShutdownHandler.start().
        self.running.store(true, Ordering::SeqCst);
        Ok(())
    }

    async fn run_lease_taker(&self) -> Result<(), LeasingError> {
        run_lease_taker_once(
            &*self.lease_taker,
            &*self.lease_renewer,
            self.metrics_factory.as_ref(),
            &self.worker_identifier,
            &self.running,
        )
        .await
    }

    async fn run_lease_renewer(&self) -> Result<(), LeasingError> {
        self.lease_renewer.renew_leases().await
    }

    fn is_running(&self) -> bool {
        self.running.load(Ordering::SeqCst)
    }

    fn worker_identifier(&self) -> String {
        self.lease_taker.get_worker_identifier()
    }

    fn lease_refresher(&self) -> Arc<dyn LeaseRefresher> {
        self.lease_refresher.clone()
    }

    fn get_assignments(&self) -> Vec<Lease> {
        self.lease_renewer
            .get_currently_held_leases()
            .into_values()
            .collect()
    }

    fn get_currently_held_lease(&self, lease_key: &str) -> Option<Lease> {
        self.lease_renewer.get_currently_held_lease(lease_key)
    }

    async fn update_lease(
        &self,
        lease: &Lease,
        concurrency_token: Uuid,
        operation: &str,
        single_stream_shard_id: &str,
    ) -> Result<bool, LeasingError> {
        self.lease_renewer
            .update_lease(lease, concurrency_token, operation, single_stream_shard_id)
            .await
    }

    fn stop_lease_taker(&self) {
        // Called during worker graceful shutdown: cancel the discoverer + taker
        // loops without touching the renewer.
        // TODO(port) — lifecycle wave (7): leaseGracefulShutdownHandler.stop().
        let mut inner = self.inner.lock().unwrap();
        if let Some(h) = inner.discovery_handle.take() {
            h.abort();
        }
        if let Some(h) = inner.taker_handle.take() {
            h.abort();
        }
    }

    fn drop_lease(&self, lease: &Lease) {
        // Guarded by the shutdown lock like Java.
        let _guard = self.inner.lock().unwrap();
        self.lease_renewer.drop_lease(lease);
    }

    async fn stop(&self) {
        let (shutdown, taker_handle, discovery_handle, renewer_handle) = {
            let mut inner = self.inner.lock().unwrap();
            (
                inner.shutdown.take(),
                inner.taker_handle.take(),
                inner.discovery_handle.take(),
                inner.renewer_handle.take(),
            )
        };

        if let Some(sd) = &shutdown {
            // Level-triggered: a loop that is mid-tick observes the cancellation
            // on its next iteration, so the signal cannot be lost.
            sd.cancel();
        }

        // Java: `awaitTermination(STOP_WAIT_TIME_MILLIS)` then `shutdownNow()`
        // for whatever didn't finish in time.
        let mut handles: Vec<JoinHandle<()>> = [taker_handle, discovery_handle, renewer_handle]
            .into_iter()
            .flatten()
            .collect();
        if !handles.is_empty() {
            let graceful = tokio::time::timeout(
                std::time::Duration::from_millis(STOP_WAIT_TIME_MILLIS),
                futures::future::join_all(handles.iter_mut()),
            )
            .await
            .is_ok();
            if graceful {
                tracing::info!(
                    "Worker {} has successfully stopped lease-tracking threads",
                    self.worker_identifier
                );
            } else {
                for h in &handles {
                    h.abort();
                }
                tracing::info!(
                    "Worker {} stopped lease-tracking threads {} ms after stop",
                    self.worker_identifier,
                    STOP_WAIT_TIME_MILLIS
                );
            }
        }

        // TODO(port) — lifecycle wave (7): leaseGracefulShutdownHandler.stop().
        let _guard = self.inner.lock().unwrap();
        self.lease_renewer.clear_currently_held_leases();
        self.running.store(false, Ordering::SeqCst);
    }

    fn get_current_assignments(&self) -> Vec<ShardInfo> {
        self.get_assignments()
            .iter()
            .map(Self::convert_lease_to_assignment)
            .collect()
    }

    fn all_leases(&self) -> Vec<Lease> {
        self.lease_taker.all_leases()
    }

    fn lease_stats_recorder(&self) -> Arc<LeaseStatsRecorder> {
        self.lease_stats_recorder.clone()
    }

    fn get_consumer_id(&self) -> String {
        self.consumer_id.lock().unwrap().clone()
    }
}

/// Java `runLeaseTaker()`: take leases, then (only if still running) add them to
/// the renewer. Free function so both the trait method and the background loop
/// share it.
async fn run_lease_taker_once(
    taker: &dyn LeaseTaker,
    renewer: &dyn LeaseRenewer,
    metrics_factory: &(dyn MetricsFactory + Send + Sync),
    worker_identifier: &str,
    running: &AtomicBool,
) -> Result<(), LeasingError> {
    let mut scope = metrics_util::create_metrics_with_operation(metrics_factory, "TakeLeases");
    metrics_util::add_worker_identifier(scope.as_mut(), worker_identifier);
    let start_time = now_millis();
    let mut success = false;

    let result = async {
        let taken_leases = taker.take_leases().await?;
        // Only add taken leases to the renewer if the coordinator is still
        // running (Java's `synchronized(shutdownLock) { if (running) ... }`).
        if running.load(Ordering::SeqCst) {
            renewer.add_leases_to_renew(taken_leases.into_values().collect());
        }
        Ok::<(), LeasingError>(())
    }
    .await;

    if result.is_ok() {
        success = true;
    }
    metrics_util::add_success_and_latency(
        scope.as_mut(),
        success,
        start_time,
        MetricsLevel::Summary,
    );
    metrics_util::end_scope(scope.as_mut());

    result
}

use crate::utils::panic_util::panic_message;

fn now_millis() -> i64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::kpl::ExtendedSequenceNumber;

    const WORKER_ID: &str = "testWorker";
    const LEASE_DURATION_MILLIS: i64 = 10000;
    const EPSILON_MILLIS: i64 = 25;
    const MAX_LEASES_FOR_WORKER: i32 = i32::MAX;
    const MAX_LEASES_TO_STEAL: i32 = 1;
    const MAX_LEASE_RENEWER_THREAD_COUNT: i32 = 20;
    const INITIAL_READ_CAPACITY: i64 = 10;
    const INITIAL_WRITE_CAPACITY: i64 = 10;

    fn coordinator(refresher: MockLeaseRefresher) -> DynamoDBLeaseCoordinator {
        DynamoDBLeaseCoordinator::new(
            Arc::new(refresher),
            WORKER_ID,
            LEASE_DURATION_MILLIS,
            true,
            EPSILON_MILLIS,
            MAX_LEASES_FOR_WORKER,
            MAX_LEASES_TO_STEAL,
            MAX_LEASE_RENEWER_THREAD_COUNT,
            INITIAL_READ_CAPACITY,
            INITIAL_WRITE_CAPACITY,
            Arc::new(NullMetricsFactory),
            WorkerUtilizationAwareAssignmentConfig::default(),
            GracefulLeaseHandoffConfig::default(),
            2 * LEASE_DURATION_MILLIS,
            None,
            0,
        )
    }

    fn refresher_with_empty_leases() -> MockLeaseRefresher {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_list_leases().returning(|| Ok(vec![]));
        refresher
            .expect_list_leases_parallely()
            .returning(|_seg| Ok((vec![], vec![])));
        refresher
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn worker_identifier_and_not_running_initially() {
        let c = coordinator(refresher_with_empty_leases());
        assert_eq!(c.worker_identifier(), WORKER_ID);
        assert!(!c.is_running());
        assert!(c.get_assignments().is_empty());
        assert!(c.get_current_assignments().is_empty());
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_creates_table_and_sets_consumer_id() {
        let mut refresher = refresher_with_empty_leases();
        refresher
            .expect_create_lease_table_if_not_exists()
            .returning(|| Ok(true));
        refresher
            .expect_wait_until_lease_table_exists()
            .returning(|_, _| Ok(true));
        refresher
            .expect_get_lease_table_identifier()
            .returning(|| Ok("consumer-id-123".to_string()));
        let c = coordinator(refresher);
        c.initialize().await.unwrap();
        assert_eq!(c.get_consumer_id(), "consumer-id-123");
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_table_timeout_errors() {
        let mut refresher = refresher_with_empty_leases();
        refresher
            .expect_create_lease_table_if_not_exists()
            .returning(|| Ok(false));
        refresher
            .expect_wait_until_lease_table_exists()
            .returning(|_, _| Ok(false));
        let c = coordinator(refresher);
        assert!(c.initialize().await.is_err());
    }

    #[tokio::test(start_paused = true)]
    async fn start_sets_running_and_taker_started_then_stop() {
        let c = coordinator(refresher_with_empty_leases());
        c.start(Arc::new(MigrationAdaptiveLeaseAssignmentModeProvider::new()))
            .await
            .unwrap();
        assert!(c.is_running());
        assert!(c.is_taker_started());
        c.stop().await;
        assert!(!c.is_running());
    }

    #[tokio::test(start_paused = true)]
    async fn background_loops_tick_deterministically_then_stop() {
        // Exercises the spawned taker/discovery/renewer loops on a paused clock
        // (current-thread runtime): each fires its immediate first tick plus at
        // least one interval tick after time advances. Dual mode + default
        // assignment: the taker executes, the discovery loop ticks but no-ops
        // (its per-tick mode gate — see `discovery_loop_*` tests).
        let c = Arc::new(coordinator(refresher_with_empty_leases()));
        c.start(mode_provider(
            true,
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
        ))
        .await
        .unwrap();
        // Advance well past all three intervals to let the loops run.
        tokio::time::sleep(std::time::Duration::from_secs(60)).await;
        assert!(c.is_running());
        c.stop().await;
        assert!(!c.is_running());
    }

    /// Java `LeaseDiscoveryRunnable`: the discoverer executes only in
    /// WORKER_UTILIZATION_AWARE_ASSIGNMENT mode. In that mode the loop queries
    /// the `LeaseOwnerToLeaseKeyIndex` GSI via the refresher; the discovery loop
    /// also calls the renewer's sync accessors, covering `run_sync` on a
    /// current-thread runtime.
    #[tokio::test(start_paused = true)]
    async fn discovery_loop_runs_in_worker_utilization_mode() {
        let mut refresher = refresher_with_empty_leases();
        let queried = Arc::new(AtomicBool::new(false));
        let queried_flag = queried.clone();
        refresher
            .expect_list_lease_keys_for_worker()
            .returning(move |_| {
                queried_flag.store(true, Ordering::SeqCst);
                Ok(vec![])
            });
        let c = Arc::new(coordinator(refresher));
        c.start(mode_provider(
            false,
            LeaseAssignmentMode::WorkerUtilizationAwareAssignment,
        ))
        .await
        .unwrap();
        tokio::time::sleep(std::time::Duration::from_secs(60)).await;
        assert!(
            queried.load(Ordering::SeqCst),
            "discoverer should query the lease-owner GSI in worker-utilization mode"
        );
        c.stop().await;
    }

    /// Java `LeaseDiscoveryRunnable` returns without discovering in
    /// DEFAULT_LEASE_COUNT_BASED_ASSIGNMENT mode — the GSI it queries is only
    /// created by the (un-wired) KCLv3 migration machinery, so an ungated loop
    /// would error every tick against a fresh lease table.
    #[tokio::test(start_paused = true)]
    async fn discovery_loop_noops_in_default_lease_count_mode() {
        let mut refresher = refresher_with_empty_leases();
        refresher.expect_list_lease_keys_for_worker().never();
        let c = Arc::new(coordinator(refresher));
        c.start(mode_provider(
            false,
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
        ))
        .await
        .unwrap();
        tokio::time::sleep(std::time::Duration::from_secs(60)).await;
        c.stop().await;
    }

    #[tokio::test(start_paused = true)]
    async fn taker_loop_survives_panicking_iteration() {
        let mut refresher = MockLeaseRefresher::new();
        // First taker tick panics (Java unchecked exception → the runnable's
        // `catch (Throwable)` logs it and the schedule keeps running).
        refresher
            .expect_list_leases()
            .times(1)
            .returning(|| panic!("injected panic in lease taking"));
        // Later ticks succeed, proving the loop survived the panic.
        let alive = Arc::new(AtomicBool::new(false));
        let alive_flag = alive.clone();
        refresher.expect_list_leases().returning(move || {
            alive_flag.store(true, Ordering::SeqCst);
            Ok(vec![])
        });
        refresher
            .expect_list_leases_parallely()
            .returning(|_seg| Ok((vec![], vec![])));
        let c = Arc::new(coordinator(refresher));
        c.start(mode_provider(
            false,
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
        ))
        .await
        .unwrap();
        // Taker interval is (leaseDuration + epsilon) * 2 ≈ 20s; cross several
        // ticks so the loop runs again after the panicking first tick.
        tokio::time::sleep(std::time::Duration::from_secs(60)).await;
        assert!(
            alive.load(Ordering::SeqCst),
            "taker loop died after a panicking iteration"
        );
        c.stop().await;
        assert!(!c.is_running());
    }

    #[tokio::test(start_paused = true)]
    async fn stop_is_not_lost_when_signalled_before_loops_park() {
        // `stop` immediately after `start` races the loops' first poll. The
        // level-triggered CancellationToken cannot lose that signal (a Notify
        // could, if a loop wasn't parked on `notified()` yet), so the graceful
        // join must complete without waiting out the STOP_WAIT window: the
        // 1 ms outer timeout only fires if stop() needs the clock to advance.
        let c = coordinator(refresher_with_empty_leases());
        c.start(Arc::new(MigrationAdaptiveLeaseAssignmentModeProvider::new()))
            .await
            .unwrap();
        tokio::time::timeout(std::time::Duration::from_millis(1), c.stop())
            .await
            .expect("stop() should join the loops without waiting out the stop window");
        assert!(!c.is_running());
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn run_lease_taker_adds_taken_leases_when_running() {
        let mut refresher = MockLeaseRefresher::new();
        // One unowned lease available to take.
        refresher.expect_list_leases().returning(|| {
            let mut lease = Lease::default();
            lease.set_lease_key("shard-1");
            lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
            lease.set_lease_counter(0);
            Ok(vec![lease])
        });
        refresher.expect_take_lease().returning(|lease, owner| {
            lease.set_lease_owner(Some(owner.to_string()));
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let c = coordinator(refresher);
        // Not started -> `running` is false, so taken leases are NOT added.
        c.run_lease_taker().await.unwrap();
        assert!(c.get_assignments().is_empty());
    }

    // --- Ported DynamoDBLeaseCoordinatorTest mode-combination scenarios ---
    //
    // Java asserts on the private `takerFuture` field via reflection; here
    // `is_taker_started()` is the equivalent seam. `start()` requires a mode
    // provider whose `dynamic_mode_change_support_needed` + `lease_assignment_mode`
    // are configured via `initialize(dynamic, mode)`.

    fn mode_provider(
        dynamic: bool,
        mode: LeaseAssignmentMode,
    ) -> Arc<MigrationAdaptiveLeaseAssignmentModeProvider> {
        let provider = MigrationAdaptiveLeaseAssignmentModeProvider::new();
        provider.initialize(dynamic, mode);
        Arc::new(provider)
    }

    /// Port of `DynamoDBLeaseCoordinatorTest.start_withDynamicModeChangeSupport_startsTakerThread`.
    #[tokio::test(start_paused = true)]
    async fn start_with_dynamic_mode_change_support_starts_taker_thread() {
        let c = coordinator(refresher_with_empty_leases());
        c.start(mode_provider(
            true,
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
        ))
        .await
        .unwrap();
        assert!(c.is_taker_started());
        c.stop().await;
    }

    /// Port of `DynamoDBLeaseCoordinatorTest.start_withPhase1DefaultLeaseCountMode_startsTakerThread`.
    #[tokio::test(start_paused = true)]
    async fn start_with_phase1_default_lease_count_mode_starts_taker_thread() {
        let c = coordinator(refresher_with_empty_leases());
        c.start(mode_provider(
            false,
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
        ))
        .await
        .unwrap();
        assert!(c.is_taker_started());
        c.stop().await;
    }

    /// Port of `DynamoDBLeaseCoordinatorTest.start_withWorkerUtilAwareAndNoDynamicSupport_doesNotStartTakerThread`.
    #[tokio::test(start_paused = true)]
    async fn start_with_worker_util_aware_and_no_dynamic_support_does_not_start_taker_thread() {
        let c = coordinator(refresher_with_empty_leases());
        c.start(mode_provider(
            false,
            LeaseAssignmentMode::WorkerUtilizationAwareAssignment,
        ))
        .await
        .unwrap();
        assert!(!c.is_taker_started());
        c.stop().await;
    }

    /// Port of `DynamoDBLeaseCoordinatorTest.start_withDynamicSupportAndWorkerUtilAwareMode_startsTakerThread`.
    #[tokio::test(start_paused = true)]
    async fn start_with_dynamic_support_and_worker_util_aware_mode_starts_taker_thread() {
        let c = coordinator(refresher_with_empty_leases());
        c.start(mode_provider(
            true,
            LeaseAssignmentMode::WorkerUtilizationAwareAssignment,
        ))
        .await
        .unwrap();
        assert!(c.is_taker_started());
        c.stop().await;
    }

    // --- Ported DynamoDBLeaseCoordinatorIntegrationTest scenarios ---
    //
    // Java runs these against a real DynamoDB. Here we drive the coordinator's
    // taker + discovery + renewer loops through a `MockLeaseRefresher`. The three
    // `testUpdateCheckpoint*` methods exercise `DynamoDBCheckpointer.setCheckpoint`
    // against real-DB optimistic-concurrency (CAS) sequences that cannot be
    // reproduced with response mocks; they are intentionally not ported.

    /// A `MockLeaseRefresher` that reports `owner_leases` owned by `WORKER_ID`
    /// (via both `list_leases` for the taker and the GSI-backed
    /// `list_lease_keys_for_worker` + `get_lease` for the discoverer).
    fn refresher_with_owned_leases(count: usize) -> MockLeaseRefresher {
        let leases: Vec<Lease> = (1..=count)
            .map(|i| {
                let mut lease = Lease::default();
                lease.set_lease_key(i.to_string());
                lease.set_lease_owner(Some(WORKER_ID.to_string()));
                lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
                lease.set_lease_counter(1);
                lease
            })
            .collect();

        let mut refresher = MockLeaseRefresher::new();
        let leases_for_list = leases.clone();
        refresher
            .expect_list_leases()
            .returning(move || Ok(leases_for_list.clone()));
        let leases_for_parallel = leases.clone();
        refresher
            .expect_list_leases_parallely()
            .returning(move |_seg| Ok((leases_for_parallel.clone(), vec![])));
        let keys: Vec<String> = leases
            .iter()
            .map(|l| l.lease_key().unwrap().to_string())
            .collect();
        refresher
            .expect_list_lease_keys_for_worker()
            .returning(move |_| Ok(keys.clone()));
        let leases_for_get = leases.clone();
        refresher.expect_get_lease().returning(move |key| {
            Ok(leases_for_get
                .iter()
                .find(|l| l.lease_key() == Some(key))
                .cloned())
        });
        refresher.expect_take_lease().returning(|lease, owner| {
            lease.set_lease_owner(Some(owner.to_string()));
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        refresher
    }

    fn worker_util_mode_provider() -> Arc<MigrationAdaptiveLeaseAssignmentModeProvider> {
        let provider = MigrationAdaptiveLeaseAssignmentModeProvider::new();
        provider.initialize(false, LeaseAssignmentMode::WorkerUtilizationAwareAssignment);
        Arc::new(provider)
    }

    /// Port of `DynamoDBLeaseCoordinatorIntegrationTest.testGetAllAssignments`.
    ///
    /// `runLeaseTaker()` populates the taker's cache; `allLeases()` returns all
    /// five leases.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_get_all_assignments() {
        let c = Arc::new(coordinator(refresher_with_owned_leases(5)));
        c.run_lease_taker().await.unwrap();

        let c2 = c.clone();
        let all = tokio::task::spawn_blocking(move || c2.all_leases())
            .await
            .unwrap();
        assert_eq!(all.len(), 5);
        let keys: std::collections::HashSet<String> = all
            .iter()
            .map(|l| l.lease_key().unwrap().to_string())
            .collect();
        assert_eq!(keys, (1..=5).map(|i| i.to_string()).collect());
    }

    /// Port of `DynamoDBLeaseCoordinatorIntegrationTest.testLeaseDiscoveryFutureRuns`.
    ///
    /// After the coordinator starts, the periodic discovery loop runs at least
    /// once and hands the discovered leases to the renewer, so `getAssignments()`
    /// (the currently-held leases) reports all five.
    #[tokio::test(start_paused = true)]
    async fn test_lease_discovery_future_runs() {
        let c = coordinator(refresher_with_owned_leases(5));
        c.start(worker_util_mode_provider()).await.unwrap();

        // Advance well past the discovery interval so the loop ticks.
        tokio::time::sleep(std::time::Duration::from_secs(60)).await;

        assert_eq!(c.get_assignments().len(), 5);
        c.stop().await;
    }

    // NOTE: `DynamoDBLeaseCoordinatorIntegrationTest.stopLeaseTakerCancelsLeaseDiscoveryFuture`
    // is NOT ported. It relies on Java's `ScheduledFuture.cancel()` being able to
    // stop the discovery future before its first execution. tokio's periodic
    // `interval` fires an immediate first tick and `JoinHandle::abort()` cannot
    // reliably preempt that first poll on a paused clock, so the "zero
    // assignments after stopping the taker" assertion is inherently racy and not
    // faithfully reproducible with the ported loop design.

    #[test]
    fn convert_lease_to_assignment_single_stream() {
        let mut lease = Lease::default();
        lease.set_lease_key("shard-1");
        lease.set_concurrency_token(Uuid::new_v4());
        lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
        let info = DynamoDBLeaseCoordinator::convert_lease_to_assignment(&lease);
        assert_eq!(info.shard_id(), "shard-1");
        assert!(info.stream_identifier_ser_opt().is_none());
    }

    #[test]
    fn convert_lease_to_assignment_multi_stream() {
        let mut lease = Lease::default();
        lease.set_lease_key("acc:stream:1:shard-1");
        lease.set_concurrency_token(Uuid::new_v4());
        lease.set_stream_identifier("acc:stream:1");
        lease.set_shard_id("shard-1");
        lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
        let info = DynamoDBLeaseCoordinator::convert_lease_to_assignment(&lease);
        assert_eq!(info.shard_id(), "shard-1");
        assert_eq!(info.stream_identifier_ser_opt(), Some("acc:stream:1"));
    }

    #[test]
    #[should_panic(expected = "readCapacity should be >= 1")]
    fn constructor_rejects_zero_read_capacity() {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_list_leases().returning(|| Ok(vec![]));
        DynamoDBLeaseCoordinator::new(
            Arc::new(refresher),
            WORKER_ID,
            LEASE_DURATION_MILLIS,
            true,
            EPSILON_MILLIS,
            MAX_LEASES_FOR_WORKER,
            MAX_LEASES_TO_STEAL,
            MAX_LEASE_RENEWER_THREAD_COUNT,
            0, // invalid
            INITIAL_WRITE_CAPACITY,
            Arc::new(NullMetricsFactory),
            WorkerUtilizationAwareAssignmentConfig::default(),
            GracefulLeaseHandoffConfig::default(),
            2 * LEASE_DURATION_MILLIS,
            None,
            0,
        );
    }
}
