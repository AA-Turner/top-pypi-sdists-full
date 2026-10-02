//! Port of
//! `software.amazon.kinesis.coordinator.migration.MigrationReadyMonitor`.

use std::collections::HashSet;
use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Mutex};

use async_trait::async_trait;

use crate::coordinator::leader_decider::LeaderDecider;
use crate::coordinator::migration::monitor_scheduler::{MonitorScheduler, ScheduledHandle};
use crate::leases::exceptions::LeasingError;
use crate::leases::lease_refresher::LeaseRefresher;
use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};
use crate::worker::metricstats::worker_metric_stats::WorkerMetricStats;

use aws_sdk_cloudwatch::types::StandardUnit;

/// Read surface over `WorkerMetricStatsDAO.getAllWorkerMetricStats()` needed by
/// this monitor. Java uses the concrete `WorkerMetricStatsDAO`; modeled as a
/// trait so the monitor can be unit-tested against a mock.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait WorkerMetricStatsSource: Send + Sync {
    /// Java `WorkerMetricStatsDAO.getAllWorkerMetricStats()`.
    async fn get_all_worker_metric_stats(&self) -> Result<Vec<WorkerMetricStats>, LeasingError>;
}

/// Injectable millisecond clock (Java `Callable<Long> timeProvider`), falling
/// back to wall-clock on error is unnecessary in Rust (infallible closure).
pub type TimeProvider = Arc<dyn Fn() -> i64 + Send + Sync>;

/// Callback invoked when readiness is stable (Java `Runnable callback`). Must be
/// idempotent (fired every tick after stabilization). Async so the leader's
/// `onMigrationReady` DDB write runs inline within the monitor tick (as in Java,
/// where `callback.run()` executes synchronously on the monitor thread).
pub type ReadyCallback = Arc<dyn Fn() -> Pin<Box<dyn Future<Output = ()> + Send>> + Send + Sync>;

const MONITOR_INTERVAL_MILLIS: u64 = 60_000;
const DDB_LOAD_RETRY_ATTEMPT: i32 = 1;

/// Leader-only polling monitor determining fleet-wide 3.x readiness (GSI
/// active and all lease owners emitting fresh WorkerMetricStats), with a
/// stabilizer requiring the condition to hold continuously before firing the
/// callback.
pub struct MigrationReadyMonitor {
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    time_provider: TimeProvider,
    leader_decider: Arc<dyn LeaderDecider>,
    current_worker_id: String,
    worker_metric_stats_dao: Arc<dyn WorkerMetricStatsSource>,
    worker_metric_stats_expiry_seconds: i64,
    lease_refresher: Arc<dyn LeaseRefresher>,
    scheduler: Arc<dyn MonitorScheduler>,
    inner: Mutex<Inner>,
}

struct Inner {
    handle: Option<ScheduledHandle>,
    cancelled: bool,
    gsi_status_ready: bool,
    worker_metrics_ready: bool,
    last_known_unique_lease_owners: HashSet<String>,
    last_known_workers_with_active_worker_metrics: HashSet<String>,
    stabilizer: MonitorTriggerStabilizer,
}

impl MigrationReadyMonitor {
    /// Java constructor.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        time_provider: TimeProvider,
        leader_decider: Arc<dyn LeaderDecider>,
        current_worker_id: impl Into<String>,
        worker_metric_stats_dao: Arc<dyn WorkerMetricStatsSource>,
        worker_metrics_expiry_seconds: i64,
        lease_refresher: Arc<dyn LeaseRefresher>,
        scheduler: Arc<dyn MonitorScheduler>,
        callback: ReadyCallback,
        callback_stabilization_in_seconds: i64,
    ) -> Self {
        let current_worker_id = current_worker_id.into();
        let stabilizer = MonitorTriggerStabilizer::new(
            time_provider.clone(),
            callback_stabilization_in_seconds,
            callback,
            current_worker_id.clone(),
        );
        Self {
            metrics_factory,
            time_provider,
            leader_decider,
            current_worker_id,
            worker_metric_stats_dao,
            worker_metric_stats_expiry_seconds: worker_metrics_expiry_seconds,
            lease_refresher,
            scheduler,
            inner: Mutex::new(Inner {
                handle: None,
                cancelled: false,
                gsi_status_ready: false,
                worker_metrics_ready: false,
                last_known_unique_lease_owners: HashSet::new(),
                last_known_workers_with_active_worker_metrics: HashSet::new(),
                stabilizer,
            }),
        }
    }

    /// Java `startMonitor()`: idempotent (period == initial delay, no jitter).
    pub fn start_monitor(self: &Arc<Self>) {
        let mut inner = self.inner.lock().expect("poisoned");
        if inner.handle.is_some() {
            return;
        }
        tracing::info!("Starting migration ready monitor");
        let this = self.clone();
        let task = Arc::new(move || {
            let this = this.clone();
            Box::pin(async move {
                this.run().await;
            }) as Pin<Box<dyn Future<Output = ()> + Send>>
        });
        let handle = self.scheduler.schedule_with_fixed_delay(
            task,
            MONITOR_INTERVAL_MILLIS,
            MONITOR_INTERVAL_MILLIS,
        );
        inner.handle = Some(handle);
    }

    /// Java `cancel()` (interrupt=true).
    pub fn cancel(&self) {
        let mut inner = self.inner.lock().expect("poisoned");
        if let Some(h) = inner.handle.take() {
            tracing::info!("Cancelled migration ready monitor");
            h.cancel();
        }
        inner.cancelled = true;
    }

    /// Java `run()`. Not-leader → reset stabilizer + clear caches. Leader →
    /// `triggerStabilizer.call(isReadyForUpgradeTo3x())`. All errors swallowed.
    pub async fn run(&self) {
        // Not the leader?
        if !self.leader_decider.is_leader(&self.current_worker_id) {
            let mut inner = self.inner.lock().expect("poisoned");
            inner.stabilizer.reset();
            inner.last_known_unique_lease_owners.clear();
            inner.last_known_workers_with_active_worker_metrics.clear();
            return;
        }

        let ready = match self.is_ready_for_upgrade_to_3x().await {
            Ok(r) => r,
            Err(e) => {
                tracing::warn!(?e, "MigrationReadyMonitor failed, will retry");
                return;
            }
        };
        // Decide whether to fire under the lock; await the callback outside it.
        let callback = {
            let mut inner = self.inner.lock().expect("poisoned");
            inner.stabilizer.call(ready)
        };
        if let Some(cb) = callback {
            cb().await;
        }
    }

    async fn is_ready_for_upgrade_to_3x(&self) -> Result<bool, LeasingError> {
        let mut scope = metrics_util::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            crate::coordinator::migration::migration_state_machine::METRICS_OPERATION,
        );
        // If GSI is not ready, skip the worker-metrics reads (short circuit).
        let local_gsi_ready = self
            .lease_refresher
            .is_lease_owner_to_lease_key_index_active()
            .await?;
        {
            let mut inner = self.inner.lock().expect("poisoned");
            if local_gsi_ready != inner.gsi_status_ready {
                inner.gsi_status_ready = local_gsi_ready;
                tracing::info!(gsi_ready = local_gsi_ready, "Gsi ready status changed");
            }
        }
        let result = if local_gsi_ready {
            self.are_lease_owners_emitting_worker_metrics().await?
        } else {
            false
        };
        let inner = self.inner.lock().expect("poisoned");
        scope.add_data_with_level(
            "GsiReadyStatus",
            if inner.gsi_status_ready { 1.0 } else { 0.0 },
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "WorkerMetricsReadyStatus",
            if inner.worker_metrics_ready { 1.0 } else { 0.0 },
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        drop(inner);
        metrics_util::end_scope(scope.as_mut());
        Ok(result)
    }

    async fn are_lease_owners_emitting_worker_metrics(&self) -> Result<bool, LeasingError> {
        // Java runs the two loads concurrently on the common pool then joins.
        let lease_list = self.load_leases_with_retry().await?;
        let worker_metrics = self.load_worker_metrics_with_retry().await?;

        let lease_owners: HashSet<String> = lease_list
            .iter()
            .filter_map(|l| l.lease_owner().map(|s| s.to_string()))
            .collect();

        let now_in_seconds = (self.time_provider)() / 1000;
        let workers_with_active_metrics: HashSet<String> = worker_metrics
            .iter()
            .filter(|m| self.is_worker_metric_stats_active(m, now_in_seconds))
            .filter_map(|m| m.worker_id().map(|s| s.to_string()))
            .collect();

        // Not filtering expired leases from lease_owners (deliberate, see Java).
        let local_worker_metrics_ready = lease_owners.is_subset(&workers_with_active_metrics);

        let mut inner = self.inner.lock().expect("poisoned");
        if local_worker_metrics_ready != inner.worker_metrics_ready {
            inner.worker_metrics_ready = local_worker_metrics_ready;
            tracing::info!(
                ready = local_worker_metrics_ready,
                "WorkerMetricStats status changed"
            );
        }
        inner.last_known_unique_lease_owners = lease_owners;
        inner.last_known_workers_with_active_worker_metrics = workers_with_active_metrics;
        Ok(inner.worker_metrics_ready)
    }

    fn is_worker_metric_stats_active(
        &self,
        metric_stats: &WorkerMetricStats,
        now_in_seconds: i64,
    ) -> bool {
        let last = metric_stats.last_update_time().unwrap_or(0);
        (last + self.worker_metric_stats_expiry_seconds) > now_in_seconds
    }

    async fn load_leases_with_retry(&self) -> Result<Vec<crate::leases::Lease>, LeasingError> {
        let mut attempt = 0;
        loop {
            match self.lease_refresher.list_leases().await {
                Ok(v) => return Ok(v),
                Err(e) => {
                    if attempt < DDB_LOAD_RETRY_ATTEMPT {
                        tracing::warn!(?e, "Failed to load leases, retrying");
                        attempt += 1;
                    } else {
                        return Err(e);
                    }
                }
            }
        }
    }

    async fn load_worker_metrics_with_retry(&self) -> Result<Vec<WorkerMetricStats>, LeasingError> {
        let mut attempt = 0;
        loop {
            match self
                .worker_metric_stats_dao
                .get_all_worker_metric_stats()
                .await
            {
                Ok(v) => return Ok(v),
                Err(e) => {
                    if attempt < DDB_LOAD_RETRY_ATTEMPT {
                        tracing::warn!(?e, "Failed to load worker metrics, retrying");
                        attempt += 1;
                    } else {
                        return Err(e);
                    }
                }
            }
        }
    }
}

impl std::fmt::Display for MigrationReadyMonitor {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        // Legacy cosmetic name (Java toString says "UpgradeReadyMonitor").
        let inner = self.inner.lock().expect("poisoned");
        write!(
            f,
            "UpgradeReadyMonitor[G={},W={}]",
            inner.gsi_status_ready, inner.worker_metrics_ready
        )
    }
}

/// Java nested `MonitorTriggerStabilizer` — debounce/hysteresis before invoking
/// the callback. Once stabilized, invokes the callback on EVERY subsequent tick
/// (not self-cancelling; the callback must be idempotent).
struct MonitorTriggerStabilizer {
    time_provider: TimeProvider,
    stabilization_duration_in_seconds: i64,
    callback: ReadyCallback,
    #[allow(dead_code)]
    current_worker_id: String,
    last_toggle_time_in_millis: i64,
    current_trigger_status: bool,
}

impl MonitorTriggerStabilizer {
    fn new(
        time_provider: TimeProvider,
        stabilization_duration_in_seconds: i64,
        callback: ReadyCallback,
        current_worker_id: String,
    ) -> Self {
        Self {
            time_provider,
            stabilization_duration_in_seconds,
            callback,
            current_worker_id,
            last_toggle_time_in_millis: 0,
            current_trigger_status: false,
        }
    }

    /// Returns the callback to invoke iff the trigger has been stable long
    /// enough (invoked by the caller outside the lock). Java calls
    /// `callback.run()` inline; we hand it back to keep the lock non-async.
    fn call(&mut self, is_monitor_triggered: bool) -> Option<ReadyCallback> {
        let now = (self.time_provider)();
        if self.current_trigger_status != is_monitor_triggered {
            tracing::info!(
                triggered = is_monitor_triggered,
                "Trigger status has changed"
            );
            self.current_trigger_status = is_monitor_triggered;
            self.last_toggle_time_in_millis = now;
        }
        if self.current_trigger_status {
            let delta_seconds = (now - self.last_toggle_time_in_millis) / 1000;
            if delta_seconds >= self.stabilization_duration_in_seconds {
                tracing::info!(
                    delta_seconds,
                    "Trigger consistently true, invoking callback"
                );
                return Some(self.callback.clone());
            }
            tracing::info!(
                delta_seconds,
                threshold = self.stabilization_duration_in_seconds,
                "Trigger true, waiting for stabilization"
            );
        }
        None
    }

    fn reset(&mut self) {
        self.current_trigger_status = false;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};

    use crate::coordinator::leader_decider::MockLeaderDecider;
    use crate::coordinator::migration::monitor_scheduler::RecordingScheduler;
    use crate::leases::lease::Lease;
    use crate::leases::lease_refresher::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;

    const WORKER_ID: &str = "MigrationReadyMonitorTestWorker0";
    const WORKER_METRICS_EXPIRY_SECONDS: i64 = 60;
    const EXPIRED_WORKER_STATS_LAST_UPDATE_TIME: i64 = 10;
    const ACTIVE_WORKER_STATS_LAST_UPDATE_TIME: i64 = 10000;
    const NUM_WORKERS: usize = 10;

    #[derive(Clone)]
    struct TestData {
        lease_list: Vec<Lease>,
        worker_metrics: Vec<WorkerMetricStats>,
    }

    fn lease_owned_by(shard: &str, owner: &str) -> Lease {
        Lease::new(
            Some(shard.to_string()),
            Some(owner.to_string()),
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
    }

    fn active_metrics_for_all() -> Vec<WorkerMetricStats> {
        (0..NUM_WORKERS)
            .map(|i| {
                WorkerMetricStats::legacy_builder()
                    .worker_id(format!("MigrationReadyMonitorTestWorker{i}"))
                    .last_update_time(ACTIVE_WORKER_STATS_LAST_UPDATE_TIME)
                    .build()
            })
            .collect()
    }

    fn leases_all_workers() -> Vec<Lease> {
        // 100 leases owned by workers 0..9 deterministically (all 10 own some).
        (0..100)
            .map(|i| {
                lease_owned_by(
                    &format!("shardId-000000000{i}"),
                    &format!("MigrationReadyMonitorTestWorker{}", i % NUM_WORKERS),
                )
            })
            .collect()
    }

    fn worker_ready_condition_met() -> TestData {
        TestData {
            lease_list: leases_all_workers(),
            worker_metrics: active_metrics_for_all(),
        }
    }

    fn worker_ready_condition_met_few_shards() -> TestData {
        let base = worker_ready_condition_met();
        TestData {
            lease_list: base.lease_list[0..1].to_vec(),
            worker_metrics: base.worker_metrics,
        }
    }

    fn all_inactive_worker_stats() -> TestData {
        TestData {
            lease_list: leases_all_workers(),
            worker_metrics: (0..NUM_WORKERS)
                .map(|i| {
                    WorkerMetricStats::legacy_builder()
                        .worker_id(format!("MigrationReadyMonitorTestWorker{i}"))
                        .last_update_time(EXPIRED_WORKER_STATS_LAST_UPDATE_TIME)
                        .build()
                })
                .collect(),
        }
    }

    fn zero_worker_stats() -> TestData {
        TestData {
            lease_list: leases_all_workers(),
            worker_metrics: Vec::new(),
        }
    }

    fn partial_worker_stats() -> TestData {
        // Only 5 of 10 workers emit metrics -> not all lease owners covered.
        TestData {
            lease_list: leases_all_workers(),
            worker_metrics: (0..5)
                .map(|i| {
                    WorkerMetricStats::legacy_builder()
                        .worker_id(format!("MigrationReadyMonitorTestWorker{i}"))
                        .last_update_time(ACTIVE_WORKER_STATS_LAST_UPDATE_TIME)
                        .build()
                })
                .collect(),
        }
    }

    fn partial_inactive_worker_stats() -> TestData {
        // Half active, half inactive across the 10 workers.
        TestData {
            lease_list: leases_all_workers(),
            worker_metrics: (0..NUM_WORKERS)
                .map(|i| {
                    let t = if i % 2 == 0 {
                        EXPIRED_WORKER_STATS_LAST_UPDATE_TIME
                    } else {
                        ACTIVE_WORKER_STATS_LAST_UPDATE_TIME
                    };
                    WorkerMetricStats::legacy_builder()
                        .worker_id(format!("MigrationReadyMonitorTestWorker{i}"))
                        .last_update_time(t)
                        .build()
                })
                .collect(),
        }
    }

    fn expired_leases_and_inactive_worker_stats() -> TestData {
        // Add 5 leases for an extra "ExpiredLeaseWorker" not in the active set,
        // plus an inactive metric entry for it.
        let mut leases = leases_all_workers();
        for i in 0..5 {
            leases.push(lease_owned_by(
                &format!("shardId-100000000{i}"),
                "ExpiredLeaseWorker",
            ));
        }
        let mut metrics = active_metrics_for_all();
        metrics.push(
            WorkerMetricStats::legacy_builder()
                .worker_id("ExpiredLeaseWorker")
                .last_update_time(EXPIRED_WORKER_STATS_LAST_UPDATE_TIME)
                .build(),
        );
        TestData {
            lease_list: leases,
            worker_metrics: metrics,
        }
    }

    fn expired_leases_and_no_worker_stats() -> TestData {
        // Java WORKER_READY_CONDITION_NOT_MET_WITH_EXPIRED_LEASES_AND_NO_WORKER_STATS:
        // 5 extra leases owned by "ExpiredLeaseWorker" (which has NO metric entry),
        // over the active-for-all worker metrics.
        let mut leases = leases_all_workers();
        for i in 0..5 {
            leases.push(lease_owned_by(
                &format!("shardId-100000000{i}"),
                "ExpiredLeaseWorker",
            ));
        }
        TestData {
            lease_list: leases,
            worker_metrics: active_metrics_for_all(),
        }
    }

    const DUMMY_STREAM_NAME: &str = "DummyStreamName";
    const NUM_STREAMS: usize = 3;

    fn multi_stream_lease(stream: &str, shard: &str, owner: &str) -> Lease {
        let lease_key = format!("{stream}:{shard}");
        let base = lease_owned_by(&lease_key, owner);
        Lease::new_multi_stream(base, stream, shard)
    }

    fn multistream_met() -> TestData {
        // Java WORKER_READY_CONDITION_MET_MULTISTREAM_MODE_SANITY: 100 multi-stream
        // leases spread across NUM_STREAMS streams and NUM_WORKERS workers, over the
        // active-for-all worker metrics. Assigned deterministically (i % N) so every
        // worker owns at least one lease (Java uses random; determinism here).
        let leases: Vec<Lease> = (0..100)
            .map(|i| {
                let stream = format!("{DUMMY_STREAM_NAME}{}", i % NUM_STREAMS);
                let owner = format!("MigrationReadyMonitorTestWorker{}", i % NUM_WORKERS);
                multi_stream_lease(&stream, &format!("shardId-00000000{i}"), &owner)
            })
            .collect();
        TestData {
            lease_list: leases,
            worker_metrics: active_metrics_for_all(),
        }
    }

    fn multistream_not_met() -> TestData {
        // Java WORKER_READY_CONDITION_NOT_MET_MULTISTREAM_MODE_SANITY: the multistream
        // MET lease list, but only 5 workers' metrics (partial) -> not all owners
        // covered -> not ready.
        TestData {
            lease_list: multistream_met().lease_list,
            worker_metrics: (0..5)
                .map(|i| {
                    WorkerMetricStats::legacy_builder()
                        .worker_id(format!("MigrationReadyMonitorTestWorker{i}"))
                        .last_update_time(ACTIVE_WORKER_STATS_LAST_UPDATE_TIME)
                        .build()
                })
                .collect(),
        }
    }

    fn met_after_expired_leases_reassigned() -> TestData {
        // The ExpiredLeaseWorker leases get reassigned to active workers.
        let mut leases = leases_all_workers();
        for i in 0..5 {
            leases.push(lease_owned_by(
                &format!("shardId-100000000{i}"),
                &format!("MigrationReadyMonitorTestWorker{}", i % NUM_WORKERS),
            ));
        }
        TestData {
            lease_list: leases,
            worker_metrics: active_metrics_for_all(),
        }
    }

    /// Time provider that returns a fixed value.
    fn fixed_time(millis: i64) -> TimeProvider {
        Arc::new(move || millis)
    }

    /// Time provider returning queued values, repeating the last.
    fn queued_time(values: Vec<i64>) -> TimeProvider {
        let idx = Arc::new(AtomicUsize::new(0));
        Arc::new(move || {
            let i = idx.fetch_add(1, Ordering::SeqCst);
            let v = &values;
            *v.get(i).unwrap_or_else(|| v.last().unwrap())
        })
    }

    #[derive(Clone, Default)]
    struct CountingCallback {
        count: Arc<AtomicUsize>,
    }
    impl CountingCallback {
        fn callback(&self) -> ReadyCallback {
            let count = self.count.clone();
            Arc::new(move || {
                let count = count.clone();
                Box::pin(async move {
                    count.fetch_add(1, Ordering::SeqCst);
                }) as Pin<Box<dyn Future<Output = ()> + Send>>
            })
        }
        fn count(&self) -> usize {
            self.count.load(Ordering::SeqCst)
        }
        fn reset(&self) {
            self.count.store(0, Ordering::SeqCst);
        }
    }

    struct Fixture {
        leader: bool,
        gsi_ready: bool,
        data_seq: Vec<TestData>,
    }

    fn build_monitor(
        fixture: Fixture,
        time: TimeProvider,
        callback: ReadyCallback,
        stabilization_seconds: i64,
        leader_flag: Arc<std::sync::atomic::AtomicBool>,
        gsi_flag: Arc<std::sync::atomic::AtomicBool>,
    ) -> Arc<MigrationReadyMonitor> {
        let mut leader_decider = MockLeaderDecider::new();
        let lf = leader_flag.clone();
        leader_decider
            .expect_is_leader()
            .returning(move |_| lf.load(Ordering::SeqCst));
        leader_flag.store(fixture.leader, Ordering::SeqCst);

        let mut refresher = MockLeaseRefresher::new();
        let gf = gsi_flag.clone();
        refresher
            .expect_is_lease_owner_to_lease_key_index_active()
            .returning(move || Ok(gf.load(Ordering::SeqCst)));
        gsi_flag.store(fixture.gsi_ready, Ordering::SeqCst);
        let lease_seq: Vec<Vec<Lease>> = fixture
            .data_seq
            .iter()
            .map(|d| d.lease_list.clone())
            .collect();
        let lease_idx = Arc::new(AtomicUsize::new(0));
        refresher.expect_list_leases().returning(move || {
            let i = lease_idx.fetch_add(1, Ordering::SeqCst);
            Ok(lease_seq
                .get(i)
                .cloned()
                .unwrap_or_else(|| lease_seq.last().unwrap().clone()))
        });

        let mut wms = MockWorkerMetricStatsSource::new();
        let wm_seq: Vec<Vec<WorkerMetricStats>> = fixture
            .data_seq
            .iter()
            .map(|d| d.worker_metrics.clone())
            .collect();
        let wm_idx = Arc::new(AtomicUsize::new(0));
        wms.expect_get_all_worker_metric_stats().returning(move || {
            let i = wm_idx.fetch_add(1, Ordering::SeqCst);
            Ok(wm_seq
                .get(i)
                .cloned()
                .unwrap_or_else(|| wm_seq.last().unwrap().clone()))
        });

        Arc::new(MigrationReadyMonitor::new(
            Arc::new(NullMetricsFactory::new()),
            time,
            Arc::new(leader_decider),
            WORKER_ID,
            Arc::new(wms),
            WORKER_METRICS_EXPIRY_SECONDS,
            Arc::new(refresher),
            Arc::new(RecordingScheduler::new()),
            callback,
            stabilization_seconds,
        ))
    }

    #[tokio::test]
    async fn non_leader_does_not_perform_migration_checks() {
        for data in [
            worker_ready_condition_met(),
            worker_ready_condition_met_few_shards(),
            multistream_met(),
        ] {
            let cb = CountingCallback::default();
            let monitor = build_monitor(
                Fixture {
                    leader: false,
                    gsi_ready: true,
                    data_seq: vec![data],
                },
                fixed_time(1000),
                cb.callback(),
                0,
                Arc::new(std::sync::atomic::AtomicBool::new(false)),
                Arc::new(std::sync::atomic::AtomicBool::new(true)),
            );
            monitor.start_monitor();
            monitor.run().await;
            assert_eq!(cb.count(), 0);
        }
    }

    #[tokio::test]
    async fn leader_performs_migration_checks_and_fires_when_ready() {
        for data in [
            worker_ready_condition_met(),
            worker_ready_condition_met_few_shards(),
            multistream_met(),
        ] {
            let cb = CountingCallback::default();
            let monitor = build_monitor(
                Fixture {
                    leader: true,
                    gsi_ready: true,
                    data_seq: vec![data],
                },
                fixed_time(1000),
                cb.callback(),
                0,
                Arc::new(std::sync::atomic::AtomicBool::new(true)),
                Arc::new(std::sync::atomic::AtomicBool::new(true)),
            );
            monitor.start_monitor();
            monitor.run().await;
            assert_eq!(cb.count(), 1);
        }
    }

    #[tokio::test]
    async fn ready_condition_not_met_does_not_invoke_callback() {
        // (gsi_ready, data) — the full Java @CsvSource (10 rows).
        let cases: Vec<(bool, TestData)> = vec![
            (false, worker_ready_condition_met()),
            (false, worker_ready_condition_met_few_shards()),
            (false, multistream_met()),
            (true, zero_worker_stats()),
            (true, partial_worker_stats()),
            (true, all_inactive_worker_stats()),
            (true, partial_inactive_worker_stats()),
            (true, expired_leases_and_no_worker_stats()),
            (true, expired_leases_and_inactive_worker_stats()),
            (true, multistream_not_met()),
        ];
        for (gsi, data) in cases {
            let cb = CountingCallback::default();
            let monitor = build_monitor(
                Fixture {
                    leader: true,
                    gsi_ready: gsi,
                    data_seq: vec![data],
                },
                fixed_time(80 * 1000),
                cb.callback(),
                0,
                Arc::new(std::sync::atomic::AtomicBool::new(true)),
                Arc::new(std::sync::atomic::AtomicBool::new(gsi)),
            );
            monitor.start_monitor();
            monitor.run().await;
            assert_eq!(cb.count(), 0);
        }
    }

    #[tokio::test]
    async fn expired_lease_owner_then_reassigned_succeeds() {
        let cb = CountingCallback::default();
        let monitor = build_monitor(
            Fixture {
                leader: true,
                gsi_ready: true,
                data_seq: vec![
                    expired_leases_and_inactive_worker_stats(),
                    met_after_expired_leases_reassigned(),
                ],
            },
            fixed_time(80 * 1000),
            cb.callback(),
            0,
            Arc::new(std::sync::atomic::AtomicBool::new(true)),
            Arc::new(std::sync::atomic::AtomicBool::new(true)),
        );
        monitor.start_monitor();
        monitor.run().await;
        assert_eq!(cb.count(), 0);
        monitor.run().await;
        assert_eq!(cb.count(), 1);
    }

    #[tokio::test]
    async fn inactive_to_active_worker_metrics_causes_success() {
        let cb = CountingCallback::default();
        let monitor = build_monitor(
            Fixture {
                leader: true,
                gsi_ready: true,
                data_seq: vec![all_inactive_worker_stats(), worker_ready_condition_met()],
            },
            fixed_time(80 * 1000),
            cb.callback(),
            0,
            Arc::new(std::sync::atomic::AtomicBool::new(true)),
            Arc::new(std::sync::atomic::AtomicBool::new(true)),
        );
        monitor.start_monitor();
        monitor.run().await;
        assert_eq!(cb.count(), 0);
        monitor.run().await;
        assert_eq!(cb.count(), 1);
    }

    #[tokio::test]
    async fn worker_metrics_expiry_boundary_conditions() {
        // Each run reads timeProvider twice. Provide pairs at 0/59 (valid) and
        // 60/61 (expired), relative to ACTIVE_WORKER_STATS_LAST_UPDATE_TIME.
        let base = ACTIVE_WORKER_STATS_LAST_UPDATE_TIME * 1000;
        let time = queued_time(vec![
            base,
            base,
            base + 59_000,
            base + 59_000,
            base + 60_000,
            base + 60_000,
            base + 61_000,
        ]);
        let cb = CountingCallback::default();
        let monitor = build_monitor(
            Fixture {
                leader: true,
                gsi_ready: true,
                data_seq: vec![worker_ready_condition_met()],
            },
            time,
            cb.callback(),
            0,
            Arc::new(std::sync::atomic::AtomicBool::new(true)),
            Arc::new(std::sync::atomic::AtomicBool::new(true)),
        );
        monitor.start_monitor();

        // At 0s -> valid
        cb.reset();
        monitor.run().await;
        assert_eq!(cb.count(), 1);
        // At 59s -> valid
        cb.reset();
        monitor.run().await;
        assert_eq!(cb.count(), 1);
        // At 60s -> expired
        cb.reset();
        monitor.run().await;
        assert_eq!(cb.count(), 0);
        // At 61s -> expired
        cb.reset();
        monitor.run().await;
        assert_eq!(cb.count(), 0);
    }

    #[tokio::test]
    async fn trigger_stability_fires_only_after_stabilization() {
        let stability = 12i64;
        let cb = CountingCallback::default();
        let leader_flag = Arc::new(std::sync::atomic::AtomicBool::new(true));
        let gsi_flag = Arc::new(std::sync::atomic::AtomicBool::new(true));
        // A time provider we can advance manually.
        let clock = Arc::new(std::sync::Mutex::new(
            (ACTIVE_WORKER_STATS_LAST_UPDATE_TIME - 200) * 1000,
        ));
        let clock_c = clock.clone();
        let time: TimeProvider = Arc::new(move || *clock_c.lock().unwrap());
        let monitor = build_monitor(
            Fixture {
                leader: true,
                gsi_ready: true,
                data_seq: vec![worker_ready_condition_met()],
            },
            time,
            cb.callback(),
            stability,
            leader_flag,
            gsi_flag,
        );
        monitor.start_monitor();

        // Callback only fires after trigger has been true for `stability` seconds.
        for i in 0..=stability {
            assert_eq!(
                cb.count(),
                0,
                "should not fire before stabilization at i={i}"
            );
            *clock.lock().unwrap() = (ACTIVE_WORKER_STATS_LAST_UPDATE_TIME - 200 + i) * 1000;
            monitor.run().await;
        }
        assert_eq!(cb.count(), 1);
    }

    /// Full faithful port of Java `testTriggerStability` (@ValueSource
    /// longs={12,30,60,180}) with all four phases:
    ///   1. callback fires only after `stability` consecutive true seconds;
    ///   2. leader flips to non-leader mid-count -> timer restarts;
    ///   3. worker-stats expire -> stabilizer resets;
    ///   4. trigger toggles (true x5, false x3) -> full restart required.
    #[tokio::test(start_paused = true)]
    async fn trigger_stability_full() {
        for stability in [12i64, 30, 60, 180] {
            // Shared mutable collaborators.
            let leader = Arc::new(std::sync::atomic::AtomicBool::new(true));
            let gsi = Arc::new(std::sync::atomic::AtomicBool::new(true));
            let clock = Arc::new(std::sync::Mutex::new(0i64));
            let leases: Arc<std::sync::Mutex<Vec<Lease>>> = Arc::new(std::sync::Mutex::new(
                worker_ready_condition_met().lease_list,
            ));
            let metrics: Arc<std::sync::Mutex<Vec<WorkerMetricStats>>> = Arc::new(
                std::sync::Mutex::new(worker_ready_condition_met().worker_metrics),
            );

            let mut leader_decider = MockLeaderDecider::new();
            {
                let l = leader.clone();
                leader_decider
                    .expect_is_leader()
                    .returning(move |_| l.load(Ordering::SeqCst));
            }
            let mut refresher = MockLeaseRefresher::new();
            {
                let g = gsi.clone();
                refresher
                    .expect_is_lease_owner_to_lease_key_index_active()
                    .returning(move || Ok(g.load(Ordering::SeqCst)));
            }
            {
                let ls = leases.clone();
                refresher
                    .expect_list_leases()
                    .returning(move || Ok(ls.lock().unwrap().clone()));
            }
            let mut wms = MockWorkerMetricStatsSource::new();
            {
                let ms = metrics.clone();
                wms.expect_get_all_worker_metric_stats()
                    .returning(move || Ok(ms.lock().unwrap().clone()));
            }
            let cb = CountingCallback::default();
            let clock_c = clock.clone();
            let time: TimeProvider = Arc::new(move || *clock_c.lock().unwrap());
            let monitor = Arc::new(MigrationReadyMonitor::new(
                Arc::new(NullMetricsFactory::new()),
                time,
                Arc::new(leader_decider),
                WORKER_ID,
                Arc::new(wms),
                WORKER_METRICS_EXPIRY_SECONDS,
                Arc::new(refresher),
                Arc::new(RecordingScheduler::new()),
                cb.callback(),
                stability,
            ));
            monitor.start_monitor();

            let set_time = |secs: i64| *clock.lock().unwrap() = secs * 1000;

            // Phase 1: callback fires only after trigger true for `stability` seconds.
            let mut test_time = ACTIVE_WORKER_STATS_LAST_UPDATE_TIME - 200;
            for i in 0..=stability {
                assert_eq!(cb.count(), 0, "phase1 i={i} stability={stability}");
                set_time(test_time + i);
                monitor.run().await;
            }
            assert_eq!(cb.count(), 1, "phase1 fire stability={stability}");
            cb.reset();

            // Phase 2: if leader changes, the timer starts over.
            test_time = ACTIVE_WORKER_STATS_LAST_UPDATE_TIME - 600;
            for i in 0..(stability / 2) {
                assert_eq!(cb.count(), 0, "phase2a i={i} stability={stability}");
                test_time += 1;
                set_time(test_time);
                monitor.run().await;
                if i == stability / 3 {
                    // Lose leadership -> next runs reset the stabilizer.
                    leader.store(false, Ordering::SeqCst);
                }
            }
            assert_eq!(cb.count(), 0, "phase2 no-fire-yet stability={stability}");
            leader.store(true, Ordering::SeqCst);
            let mut j = stability / 2;
            while j <= 3 * stability / 2 {
                assert_eq!(cb.count(), 0, "phase2b j={j} stability={stability}");
                test_time += 1;
                set_time(test_time);
                monitor.run().await;
                j += 1;
            }
            assert_eq!(cb.count(), 1, "phase2 fire stability={stability}");
            cb.reset();

            // Phase 3: reset the flag by making worker stats expire (PARTIAL_INACTIVE).
            *metrics.lock().unwrap() = partial_inactive_worker_stats().worker_metrics;
            *leases.lock().unwrap() = partial_inactive_worker_stats().lease_list;
            test_time += 1;
            set_time(test_time);
            monitor.run().await;
            assert_eq!(cb.count(), 0, "phase3 stability={stability}");

            // Use active worker stats again for the rest.
            *metrics.lock().unwrap() = worker_ready_condition_met().worker_metrics;
            *leases.lock().unwrap() = worker_ready_condition_met().lease_list;

            // Phase 4: trigger toggles back and forth.
            // True 5 times in a row.
            for _ in 0..5 {
                assert_eq!(cb.count(), 0, "phase4-true stability={stability}");
                test_time += 1;
                set_time(test_time);
                monitor.run().await;
            }
            // Then false 3 times (GSI not ready).
            gsi.store(false, Ordering::SeqCst);
            for _ in 0..3 {
                assert_eq!(cb.count(), 0, "phase4-false stability={stability}");
                test_time += 1;
                set_time(test_time);
                monitor.run().await;
            }
            // Then true until stability + 8: callback should not fire until 8 more
            // invocations have passed (full restart of the stabilization window).
            gsi.store(true, Ordering::SeqCst);
            let mut i = 8;
            while i <= stability + 8 {
                assert_eq!(cb.count(), 0, "phase4-restart i={i} stability={stability}");
                test_time += 1;
                set_time(test_time);
                monitor.run().await;
                i += 1;
            }
            assert_eq!(cb.count(), 1, "phase4 fire stability={stability}");
        }
    }
}
