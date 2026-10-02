//! Port of `software.amazon.kinesis.coordinator.assignment.LeaseAssignmentManager`.
//!
//! Top-level orchestrator for a single node's lease-assignment loop: runs only
//! when leader, loads data, computes expired/unassigned leases, delegates to a
//! [`LeaseAssignmentDecider`] for expired-lease assignment + periodic variance
//! balancing, then writes new assignments back to DynamoDB.
//!
//! # Concurrency (Java executors -> tokio)
//!
//! Java uses a caller-supplied `ScheduledExecutorService`
//! (`scheduleWithFixedDelay(performAssignment, 0, leaseAssignmentIntervalMillis)`)
//! plus a static JVM-wide fixed thread pool to parallelize the final per-lease
//! DDB writes. The Rust port:
//! - runs the periodic loop as a **spawned tokio task** driven by
//!   `tokio::time::interval(lease_assignment_interval)` (fixed-delay-ish via
//!   `MissedTickBehavior::Delay`), cancelled via a `tokio::sync::Notify` +
//!   awaited `JoinHandle` on `stop`; the injectable interval lets tests drive
//!   cadence with `#[tokio::test(start_paused)]`;
//! - fans the per-lease writes out with `futures::future::join_all` (a
//!   per-instance fan-out, not a static process-wide pool — a deliberate
//!   deviation, more idiomatic and normally there is one LAM per process).
//!
//! # Failure handling
//!
//! Java's `catch(Throwable)` distinguishes interrupt/cancellation (restore flag,
//! not a failure) from real failures (increments a continuous-failure counter;
//! releases leadership after `failureThreshold` — 1 for `Error`, else 3). In
//! tokio, cancellation is the `Notify` (loop exit), so any `perform_assignment`
//! error — or a contained panic — is a real failure feeding the same
//! counter/leadership-release logic.

use std::collections::HashMap;
use std::sync::Arc;

use aws_sdk_cloudwatch::types::StandardUnit;
use tokio::sync::{Mutex as AsyncMutex, Notify};
use tokio::task::JoinHandle;

use super::in_memory_storage_view::{InMemoryStorageView, NanoTimeProvider, StorageView};
use super::lam_data_manager::LamDataManager;
use super::lease_assignment_decider::LeaseAssignmentDecider;
use super::lease_count_based_lease_assignment_decider::LeaseCountBasedLeaseAssignmentDecider;
use super::variance_based_lease_assignment_decider::VarianceBasedLeaseAssignmentDecider;
use crate::coordinator::leader_decider::LeaderDecider;
use crate::coordinator::stream_info::StreamIdCacheManager;
use crate::leases::lease_management_config::{
    GracefulLeaseHandoffConfig, WorkerUtilizationAwareAssignmentConfig,
};
use crate::leases::{Lease, LeaseAssignmentStrategy, LeaseRefresher};
use crate::metrics::metrics_level::MetricsLevel;
use crate::metrics::{metrics_util, MetricsFactory, MetricsScope};
use crate::utils::panic_util;

const DEFAULT_FAILURE_COUNT_TO_SWITCH_LEADER: i32 = 3;
const FORCE_LEADER_RELEASE_METRIC_NAME: &str = "ForceLeaderRelease";
const METRICS_LEASE_ASSIGNMENT_MANAGER: &str = "LeaseAssignmentManager";

/// Cross-tick mutable state (Java instance fields mutated in `performAssignment`).
#[derive(Default)]
struct RunState {
    took_over_leadership_in_this_run: bool,
    prev_run_leases_state: HashMap<String, Lease>,
    no_of_continuous_failed_attempts: i32,
    lam_run_counter: i32,
}

/// Immutable dependencies shared with the background task.
struct Deps {
    lease_refresher: Arc<dyn LeaseRefresher>,
    leader_decider: Arc<dyn LeaderDecider>,
    config: WorkerUtilizationAwareAssignmentConfig,
    current_worker_id: String,
    lease_duration_millis: i64,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    nano_time_provider: NanoTimeProvider,
    max_leases_for_worker: i32,
    graceful_lease_handoff_config: GracefulLeaseHandoffConfig,
    lease_assignment_strategy: LeaseAssignmentStrategy,
    stream_id_cache_manager: Option<Arc<StreamIdCacheManager>>,
    lam_data_manager: Arc<dyn LamDataManager>,
}

/// The periodic leader-run lease-balancing manager. Java `LeaseAssignmentManager`.
pub struct LeaseAssignmentManager {
    deps: Arc<Deps>,
    lease_assignment_interval_millis: i64,
    /// Guards the background task handle (Java `synchronized` start/stop).
    task: AsyncMutex<Option<TaskHandles>>,
}

struct TaskHandles {
    handle: JoinHandle<()>,
    stop: Arc<Notify>,
}

impl LeaseAssignmentManager {
    /// Java constructor (`@RequiredArgsConstructor`, field-declaration order).
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        lease_refresher: Arc<dyn LeaseRefresher>,
        leader_decider: Arc<dyn LeaderDecider>,
        config: WorkerUtilizationAwareAssignmentConfig,
        current_worker_id: impl Into<String>,
        lease_duration_millis: i64,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        nano_time_provider: NanoTimeProvider,
        max_leases_for_worker: i32,
        graceful_lease_handoff_config: GracefulLeaseHandoffConfig,
        lease_assignment_strategy: LeaseAssignmentStrategy,
        lease_assignment_interval_millis: i64,
        stream_id_cache_manager: Option<Arc<StreamIdCacheManager>>,
        lam_data_manager: Arc<dyn LamDataManager>,
    ) -> Self {
        Self {
            deps: Arc::new(Deps {
                lease_refresher,
                leader_decider,
                config,
                current_worker_id: current_worker_id.into(),
                lease_duration_millis,
                metrics_factory,
                nano_time_provider,
                max_leases_for_worker,
                graceful_lease_handoff_config,
                lease_assignment_strategy,
                stream_id_cache_manager,
                lam_data_manager,
            }),
            lease_assignment_interval_millis,
            task: AsyncMutex::new(None),
        }
    }

    /// The scheduled interval (Java `scheduleWithFixedDelay(.., interval, ..)` arg).
    pub fn lease_assignment_interval_millis(&self) -> i64 {
        self.lease_assignment_interval_millis
    }

    /// Java `synchronized void start()`.
    pub async fn start(&self) {
        let mut guard = self.task.lock().await;
        if guard.is_some() {
            tracing::info!("LeaseAssignmentManager already running...");
            return;
        }
        let deps = self.deps.clone();
        let interval_millis = self.lease_assignment_interval_millis;
        let stop = Arc::new(Notify::new());
        let stop_task = stop.clone();
        tracing::info!(
            "Started LeaseAssignmentManager using {:?}",
            deps.lease_assignment_strategy
        );
        let handle = tokio::spawn(async move {
            let mut state = RunState::default();
            let mut ticker = tokio::time::interval(std::time::Duration::from_millis(
                interval_millis.max(1) as u64,
            ));
            ticker.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
            loop {
                tokio::select! {
                    _ = stop_task.notified() => break,
                    _ = ticker.tick() => {
                        Self::perform_assignment(&deps, &mut state).await;
                    }
                }
            }
        });
        *guard = Some(TaskHandles { handle, stop });
    }

    /// Java `synchronized void stop()`.
    pub async fn stop(&self) {
        let handles = self.task.lock().await.take();
        match handles {
            Some(h) => {
                h.stop.notify_waiters();
                if let Err(e) = h.handle.await {
                    if e.is_panic() {
                        let payload = e.into_panic();
                        tracing::error!(
                            "LeaseAssignmentManager assignment loop had panicked: {}",
                            panic_util::panic_message(payload.as_ref())
                        );
                    }
                }
                tracing::info!("Completed shutdown of LeaseAssignmentManager");
            }
            None => tracing::info!("LeaseAssignmentManager is not running..."),
        }
    }

    /// Whether the background loop is running (test seam).
    pub async fn is_running(&self) -> bool {
        self.task.lock().await.is_some()
    }

    fn create_metrics_scope(deps: &Deps, operation: &str) -> Box<dyn MetricsScope + Send> {
        metrics_util::create_metrics_with_operation(deps.metrics_factory.as_ref(), operation)
    }

    /// Java `performAssignment()` (one tick). Public for the `start_paused` tests
    /// and to drive a single cycle directly.
    pub async fn run_once(&self) {
        // Match `start()`'s fresh-restart reset.
        let mut state = RunState {
            took_over_leadership_in_this_run: false,
            ..RunState::default()
        };
        Self::perform_assignment(&self.deps, &mut state).await;
    }

    async fn perform_assignment(deps: &Deps, state: &mut RunState) {
        let mut scope = Self::create_metrics_scope(deps, METRICS_LEASE_ASSIGNMENT_MANAGER);
        let start_time = metrics_util::current_time_millis();
        let mut success = false;

        // Java performAssignment catch(Throwable): a panicking tick must not kill
        // the loop — it feeds the same failure counter / leadership-release path
        // as an Err. (Java lowers failureThreshold to 1 for `Error` vs 3 for
        // `Exception`; Rust panics model Java unchecked exceptions per the
        // porting convention, so the threshold stays 3.)
        let result =
            panic_util::catch_tick(Self::perform_assignment_inner(deps, state, scope.as_mut()))
                .await
                .unwrap_or_else(|panic_msg| Err(PerformOutcome::Failed(panic_msg)));
        match result {
            Ok(()) => {
                success = true;
                state.no_of_continuous_failed_attempts = 0;
            }
            Err(PerformOutcome::NotLeader) => {
                state.took_over_leadership_in_this_run = false;
                success = true;
            }
            Err(PerformOutcome::Failed(msg)) => {
                tracing::error!("LeaseAssignmentManager failed to perform lease assignment: {msg}");
                state.no_of_continuous_failed_attempts += 1;
                let failure_threshold = DEFAULT_FAILURE_COUNT_TO_SWITCH_LEADER;
                if state.no_of_continuous_failed_attempts >= failure_threshold {
                    tracing::error!(
                        "Failed to perform assignment {} times in a row, releasing leadership from worker : {}",
                        failure_threshold,
                        deps.current_worker_id
                    );
                    metrics_util::add_count(
                        scope.as_mut(),
                        FORCE_LEADER_RELEASE_METRIC_NAME,
                        1,
                        MetricsLevel::Summary,
                    );
                    deps.leader_decider.release_leadership_if_held();
                }
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

    async fn perform_assignment_inner(
        deps: &Deps,
        state: &mut RunState,
        scope: &mut (dyn MetricsScope + Send),
    ) -> Result<(), PerformOutcome> {
        if !deps.leader_decider.is_leader(&deps.current_worker_id) {
            tracing::info!(
                "Current worker {} is not a leader, ignore",
                deps.current_worker_id
            );
            return Err(PerformOutcome::NotLeader);
        }

        if !state.took_over_leadership_in_this_run {
            state.took_over_leadership_in_this_run = true;
            state.lam_run_counter = 0;
            // prepareAfterLeaderSwitch.
            state.prev_run_leases_state.clear();
            state.no_of_continuous_failed_attempts = 0;
        }
        tracing::info!(
            "Current worker {} is a leader, performing assignment",
            deps.current_worker_id
        );

        let view = InMemoryStorageView::new(
            deps.config.clone(),
            deps.max_leases_for_worker,
            deps.nano_time_provider.clone(),
        );

        let load_start = metrics_util::current_time_millis();
        let count_failing = view
            .load_in_memory_storage_view(deps.lam_data_manager.as_ref(), scope)
            .await
            .map_err(|e| PerformOutcome::Failed(format!("loadData failed: {e}")))?;
        metrics_util::add_latency(
            scope,
            Some("LeaseAndWorkerMetricsLoad"),
            load_start,
            MetricsLevel::Detailed,
        );

        if count_failing > 0 {
            scope.add_data_with_level(
                "NumWorkersWithFailingWorkerMetric",
                count_failing as f64,
                StandardUnit::Count,
                MetricsLevel::Summary,
            );
        }

        // Publish TotalLeases / NumWorkers.
        scope.add_data_with_level(
            "TotalLeases",
            view.lease_list().len() as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "NumWorkers",
            view.active_worker_metrics().len() as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );

        // Update lastCounterIncrementNanos + shutdown timeouts (mutates leases in
        // the view's lease list — recompute then write back the modified leases).
        let mut lease_list = view.lease_list();
        Self::update_leases_last_counter_and_shutdown_timeout(
            deps,
            state,
            &mut lease_list,
            view.lease_table_scan_time(),
        );

        // Compute expiredOrUnassigned (mark them).
        let lease_duration_nanos = deps.lease_duration_millis * 1_000_000;
        let scan_time = view.lease_table_scan_time();
        let mut expired_or_unassigned: Vec<Lease> = lease_list
            .iter()
            .filter(|l| l.is_expired(lease_duration_nanos, scan_time) || l.actual_owner().is_none())
            .cloned()
            .map(|mut l| {
                l.set_expired_or_unassigned(true);
                l
            })
            .collect();

        tracing::info!(
            "Total expiredOrUnassignedLeases count : {}",
            expired_or_unassigned.len()
        );
        scope.add_data_with_level(
            "ExpiredLeases",
            expired_or_unassigned.len() as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );

        let strategy = deps.lease_assignment_strategy;
        let expired_start = metrics_util::current_time_millis();
        let new_assignments_before_variance;
        {
            // Build the decider bound to the view (borrow), run assign + balance.
            let mut decider = Self::make_decider(deps, &view, strategy);
            decider.assign_expired_or_unassigned_leases(&mut expired_or_unassigned);
            metrics_util::add_latency(
                scope,
                Some("AssignExpiredOrUnassignedLeases"),
                expired_start,
                MetricsLevel::Detailed,
            );

            if !expired_or_unassigned.is_empty() {
                tracing::warn!("Not able to assign all expiredOrUnAssignedLeases");
                scope.add_data_with_level(
                    "LeaseSpillover",
                    expired_or_unassigned.len() as f64,
                    StandardUnit::Count,
                    MetricsLevel::Summary,
                );
            }

            if Self::should_run_variance_balancing(deps, state) {
                let balance_start = metrics_util::current_time_millis();
                new_assignments_before_variance = view.new_assignment_count();
                decider.balance_worker_variance();
                metrics_util::add_latency(
                    scope,
                    Some("BalanceWorkerVariance"),
                    balance_start,
                    MetricsLevel::Detailed,
                );
                scope.add_data_with_level(
                    "NumOfLeasesReassignment",
                    (view.new_assignment_count() - new_assignments_before_variance) as f64,
                    StandardUnit::Count,
                    MetricsLevel::Summary,
                );
            }
        }

        if view.new_assignment_count() == 0 {
            tracing::info!("No new lease assignment performed in this iteration");
        }

        Self::parallely_assign_leases(deps, &view, scope).await;
        Ok(())
    }

    fn make_decider<'a>(
        deps: &Deps,
        view: &'a dyn StorageView,
        strategy: LeaseAssignmentStrategy,
    ) -> Box<dyn LeaseAssignmentDecider + 'a> {
        match strategy {
            LeaseAssignmentStrategy::LeaseCountBased => {
                Box::new(LeaseCountBasedLeaseAssignmentDecider::new(
                    view,
                    deps.max_leases_for_worker,
                    deps.nano_time_provider.clone(),
                ))
            }
            LeaseAssignmentStrategy::WorkerUtilizationAware => {
                Box::new(VarianceBasedLeaseAssignmentDecider::new(
                    view,
                    deps.config.dampening_percentage,
                    deps.config.re_balance_threshold_percentage,
                    deps.config.allow_throughput_overshoot,
                ))
            }
        }
    }

    fn should_run_variance_balancing(deps: &Deps, state: &mut RunState) -> bool {
        let response = state.lam_run_counter == 0;
        let freq = deps.config.variance_balancing_frequency.max(1);
        state.lam_run_counter = (state.lam_run_counter + 1) % freq;
        response
    }

    /// Java `parallelyAssignLeases`.
    async fn parallely_assign_leases(
        deps: &Deps,
        view: &InMemoryStorageView,
        scope: &mut (dyn MetricsScope + Send),
    ) {
        let start_time = metrics_util::current_time_millis();
        let failed = Arc::new(std::sync::atomic::AtomicI32::new(0));
        let now_millis = Self::nano_time_millis(deps);

        let mut futures = Vec::new();
        for (lease, new_owner) in view.lease_to_new_assigned_worker() {
            if lease.blocked_on_pending_checkpoint(now_millis) {
                continue; // still heartbeating during graceful shutdown wait.
            }
            let failed = failed.clone();
            futures.push(async move {
                let graceful = deps
                    .graceful_lease_handoff_config
                    .is_graceful_lease_handoff_enabled()
                    && lease.is_eligible_for_graceful_shutdown();
                if graceful {
                    Self::handle_graceful_lease_handoff(deps, lease, &new_owner, &failed).await;
                } else {
                    Self::handle_regular_lease_assignment(deps, lease, &new_owner, &failed).await;
                }
            });
        }
        futures::future::join_all(futures).await;

        metrics_util::add_count(
            scope,
            "FailedAssignmentCount",
            failed.load(std::sync::atomic::Ordering::SeqCst) as i64,
            MetricsLevel::Detailed,
        );
        metrics_util::add_success_and_latency_with_dimension(
            scope,
            Some("ParallelyAssignLeases"),
            true,
            start_time,
            MetricsLevel::Detailed,
        );
    }

    async fn handle_graceful_lease_handoff(
        deps: &Deps,
        mut lease: Lease,
        new_owner: &str,
        failed: &std::sync::atomic::AtomicI32,
    ) {
        match deps
            .lease_refresher
            .initiate_graceful_lease_handoff(&mut lease, new_owner)
            .await
        {
            Ok(true) => {
                lease.set_checkpoint_owner_timeout_timestamp_millis(Some(
                    Self::checkpoint_owner_timeout_millis(deps),
                ));
                Self::resolve_stream_id(deps, &lease).await;
            }
            Ok(false) => {
                failed.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            }
            Err(e) => {
                tracing::warn!("initiateGracefulLeaseHandoff failed: {e}");
                failed.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            }
        }
    }

    async fn handle_regular_lease_assignment(
        deps: &Deps,
        mut lease: Lease,
        new_owner: &str,
        failed: &std::sync::atomic::AtomicI32,
    ) {
        match deps
            .lease_refresher
            .assign_lease(&mut lease, new_owner)
            .await
        {
            Ok(true) => {
                lease.set_last_counter_increment_nanos(Some((deps.nano_time_provider)()));
                Self::resolve_stream_id(deps, &lease).await;
            }
            Ok(false) => {
                failed.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            }
            Err(e) => {
                tracing::warn!("assignLease failed: {e}");
                failed.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            }
        }
    }

    async fn resolve_stream_id(deps: &Deps, lease: &Lease) {
        // Best-effort; only meaningful for multi-stream leases (Java passes a
        // null identifier for single-stream, a no-op).
        if !lease.is_multi_stream() {
            return;
        }
        let Some(cache) = deps.stream_id_cache_manager.as_ref() else {
            return;
        };
        let ser = crate::coordinator::stream_info::StreamInfo::multi_stream_lease_key_to_stream_identifier(
            lease.lease_key().unwrap_or_default(),
        );
        let stream_identifier = crate::common::StreamIdentifier::multi_stream_instance(&ser);
        if let Err(e) = cache.resolve_stream_id(&stream_identifier).await {
            tracing::warn!(
                "Failed to resolve stream id for lease key {:?}: {e}",
                lease.lease_key()
            );
        }
    }

    /// Java `updateLeasesLastCounterIncrementNanosAndLeaseShutdownTimeout`.
    fn update_leases_last_counter_and_shutdown_timeout(
        deps: &Deps,
        state: &mut RunState,
        lease_list: &mut [Lease],
        scan_time: i64,
    ) {
        for lease in lease_list.iter_mut() {
            let key = lease.lease_key().unwrap_or_default().to_string();
            let prev = state.prev_run_leases_state.get(&key);

            if lease.shutdown_requested() {
                let use_prev = matches!(
                    prev,
                    Some(p) if p.shutdown_requested() && Self::is_same_owners(lease, p)
                );
                if use_prev {
                    lease.set_checkpoint_owner_timeout_timestamp_millis(
                        prev.unwrap().checkpoint_owner_timeout_timestamp_millis(),
                    );
                } else {
                    lease.set_checkpoint_owner_timeout_timestamp_millis(Some(
                        Self::checkpoint_owner_timeout_millis(deps),
                    ));
                }
            }

            match prev {
                None => {
                    lease.set_last_counter_increment_nanos(Some(
                        if lease.actual_owner().is_none() {
                            0
                        } else {
                            scan_time
                        },
                    ));
                }
                Some(p) => {
                    let v = if lease.lease_counter() > p.lease_counter() {
                        scan_time
                    } else {
                        p.last_counter_increment_nanos().unwrap_or(0)
                    };
                    lease.set_last_counter_increment_nanos(Some(v));
                }
            }
        }

        state.prev_run_leases_state.clear();
        for lease in lease_list.iter() {
            state.prev_run_leases_state.insert(
                lease.lease_key().unwrap_or_default().to_string(),
                lease.clone(),
            );
        }
    }

    fn checkpoint_owner_timeout_millis(deps: &Deps) -> i64 {
        Self::nano_time_millis(deps)
            + deps
                .graceful_lease_handoff_config
                .graceful_lease_handoff_timeout_millis()
            + deps.lease_duration_millis
    }

    fn nano_time_millis(deps: &Deps) -> i64 {
        (deps.nano_time_provider)() / 1_000_000
    }

    fn is_same_owners(current: &Lease, previous: &Lease) -> bool {
        current.lease_owner() == previous.lease_owner()
            && current.checkpoint_owner() == previous.checkpoint_owner()
    }
}

/// Outcome of one `perform_assignment_inner` (drives the failure counter).
enum PerformOutcome {
    NotLeader,
    Failed(String),
}

#[cfg(test)]
mod tests;
