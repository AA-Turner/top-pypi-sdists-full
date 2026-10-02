//! Port of `LeaseAssignmentManager.InMemoryStorageView`.
//!
//! Per-tick mutable snapshot shared with whichever
//! [`LeaseAssignmentDecider`](super::LeaseAssignmentDecider) runs for that tick.
//! Both deciders mutate it via `perform_lease_assignment` and query it heavily.
//!
//! # Design
//!
//! Java's non-static inner class implicitly captures the outer LAM's
//! `nanoTimeProvider`/`config`/`maxLeasesForWorker`/`lamDataManager`. In Rust it
//! is a standalone struct owning those, exposed through the [`StorageView`]
//! trait so the deciders can be unit-tested against a `mockall` mock (the Java
//! `LeaseCountBasedLeaseAssignmentDeciderTest` mocks `InMemoryStorageView`).

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};

use crate::coordinator::assignment::lam_data_manager::LamDataManager;
use crate::leases::lease_management_config::WorkerUtilizationAwareAssignmentConfig;
use crate::leases::Lease;
use crate::metrics::MetricsScope;
use crate::worker::metricstats::WorkerMetricStats;

/// Injectable nanosecond time source (Java `Supplier<Long> nanoTimeProvider`).
pub type NanoTimeProvider = Arc<dyn Fn() -> i64 + Send + Sync>;

/// The single metric-stat name literal used for default-metric workers (Java
/// `"T"`). Load-bearing contract with `WorkerMetricStats`' EMA/operating-range.
pub const DEFAULT_WORKER_METRIC_NAME: &str = "T";

/// The queries + mutation the lease-assignment deciders perform against the
/// per-tick in-memory view. Java `LeaseAssignmentManager.InMemoryStorageView`
/// `@Getter` accessors + `performLeaseAssignment` + admission predicates.
#[cfg_attr(test, mockall::automock)]
pub trait StorageView {
    /// Worker id -> set of leases assigned to it (Java `getWorkerToLeasesMap`).
    fn worker_to_leases_map(&self) -> HashMap<String, HashSet<Lease>>;
    /// Worker id -> total assigned throughput (Java `getWorkerToTotalAssignedThroughputMap`).
    fn worker_to_total_assigned_throughput_map(&self) -> HashMap<String, f64>;
    /// All leases (Java `getLeaseList`).
    fn lease_list(&self) -> Vec<Lease>;
    /// Active worker metrics eligible for assignment (Java `getActiveWorkerMetrics`).
    fn active_worker_metrics(&self) -> Vec<WorkerMetricStats>;
    /// Active worker ids (Java `getActiveWorkerIdSet`).
    fn active_worker_id_set(&self) -> HashSet<String>;
    /// Wall time in nanos when the lease-table scan completed (Java `getLeaseTableScanTime`).
    fn lease_table_scan_time(&self) -> i64;
    /// Average throughput for all workers (Java `getTargetAverageThroughput`).
    fn target_average_throughput(&self) -> f64;
    /// Java `performLeaseAssignment(lease, newOwner)`: move ownership in the
    /// in-memory maps + record the new assignment.
    fn perform_lease_assignment(&self, lease: &Lease, new_owner: &str);
    /// Java `isWorkerTotalThroughputLessThanMaxThroughput(workerId)`.
    fn is_worker_total_throughput_less_than_max_throughput(&self, worker_id: &str) -> bool;
    /// Java `isWorkerAssignedLeasesLessThanMaxLeases(workerId)`.
    fn is_worker_assigned_leases_less_than_max_leases(&self, worker_id: &str) -> bool;
    /// Java `getTotalAssignedThroughput(workerId)`.
    fn total_assigned_throughput(&self, worker_id: &str) -> f64;
}

/// Mutable per-tick state (Java inner-class fields), interior-mutable so the
/// deciders can query + mutate through a shared `&dyn StorageView` while the LAM
/// future stays `Send` (guarded by a `std::sync::Mutex`, never held across `.await`).
#[derive(Default)]
struct Inner {
    /// Java `workerToLeasesMap`: worker id -> set of assigned leases.
    worker_to_leases_map: HashMap<String, HashSet<Lease>>,
    /// Java `workerToTotalAssignedThroughputMap`.
    worker_to_total_assigned_throughput_map: HashMap<String, f64>,
    /// Java `leaseToNewAssignedWorkerMap`: this tick's new assignments (keyed by
    /// lease key -> new owner) + the lease value (for the persist phase).
    lease_to_new_assigned_worker: HashMap<String, (Lease, String)>,
    /// Java `leaseList`.
    lease_list: Vec<Lease>,
    /// Java `activeWorkerMetrics`.
    active_worker_metrics: Vec<WorkerMetricStats>,
    /// Java `activeWorkerIdSet`.
    active_worker_id_set: HashSet<String>,
    /// Java `leaseTableScanTime`.
    lease_table_scan_time: i64,
    /// Java `targetAverageThroughput`.
    target_average_throughput: f64,
}

/// Concrete per-tick in-memory storage view (Java `InMemoryStorageView`).
pub struct InMemoryStorageView {
    config: WorkerUtilizationAwareAssignmentConfig,
    max_leases_for_worker: i32,
    nano_time_provider: NanoTimeProvider,
    inner: Mutex<Inner>,
}

impl InMemoryStorageView {
    /// Create a fresh per-tick view (Java `new InMemoryStorageView()`, capturing
    /// the outer LAM's config/maxLeasesForWorker/nanoTimeProvider).
    pub fn new(
        config: WorkerUtilizationAwareAssignmentConfig,
        max_leases_for_worker: i32,
        nano_time_provider: NanoTimeProvider,
    ) -> Self {
        Self {
            config,
            max_leases_for_worker,
            nano_time_provider,
            inner: Mutex::new(Inner::default()),
        }
    }

    fn lock(&self) -> std::sync::MutexGuard<'_, Inner> {
        self.inner.lock().unwrap_or_else(|e| e.into_inner())
    }

    /// This tick's new assignments as `(lease, new_owner)` pairs (for the persist
    /// phase). Java `getLeaseToNewAssignedWorkerMap`.
    pub fn lease_to_new_assigned_worker(&self) -> Vec<(Lease, String)> {
        self.lock()
            .lease_to_new_assigned_worker
            .values()
            .cloned()
            .collect()
    }

    /// Number of new assignments recorded so far this tick.
    pub fn new_assignment_count(&self) -> usize {
        self.lock().lease_to_new_assigned_worker.len()
    }

    /// Java `loadInMemoryStorageView(MetricsScope)`. Loads leases + worker
    /// metrics via the [`LamDataManager`], builds the in-memory maps, seeds
    /// default-worker metric stats, and returns the count of workers with
    /// failing metrics (so LAM can emit `NumWorkersWithFailingWorkerMetric`).
    pub async fn load_in_memory_storage_view(
        &self,
        lam_data_manager: &(dyn LamDataManager + Send + Sync),
        scope: &mut (dyn MetricsScope + Send),
    ) -> Result<usize, crate::leases::exceptions::LeasingError> {
        let snapshot = lam_data_manager.load_data(scope).await?;

        let lease_list = snapshot.leases;
        let scan_time = (self.nano_time_provider)();

        let worker_metrics_from_snapshot = snapshot.worker_metric_stats;
        let count_of_workers_with_failing_metric = worker_metrics_from_snapshot
            .iter()
            .filter(|wm| wm.is_any_worker_metric_failing())
            .count();

        let mut active_worker_metrics: Vec<WorkerMetricStats> = worker_metrics_from_snapshot
            .into_iter()
            .filter(|wm| !wm.is_any_worker_metric_failing())
            .collect();

        // averageLeaseThroughput over leases that have a throughput value.
        let (sum, cnt) = lease_list
            .iter()
            .filter_map(|l| l.throughput_kbps())
            .fold((0.0, 0usize), |(s, c), v| (s + v, c + 1));
        let average_lease_throughput = if cnt > 0 { sum / cnt as f64 } else { 0.0 };

        let target_average_throughput = average_lease_throughput * lease_list.len() as f64
            / (active_worker_metrics.len().max(1)) as f64;

        // Build the worker->leases + throughput maps; assign the fleet-average
        // throughput to leases with no value.
        let mut lease_list = lease_list;
        let mut worker_to_leases_map: HashMap<String, HashSet<Lease>> = HashMap::new();
        let mut worker_to_total_assigned_throughput_map: HashMap<String, f64> = HashMap::new();
        for lease in lease_list.iter_mut() {
            if lease.throughput_kbps().is_none() {
                lease.set_throughput_kbps(average_lease_throughput);
            }
            let owner = lease.actual_owner().map(|s| s.to_string());
            let tp = lease.throughput_kbps().unwrap_or(0.0);
            // Java uses `computeIfAbsent(lease.actualOwner(), ...)` — a null owner
            // key becomes a real map entry in Java's HashMap. We model the null
            // owner as an empty-string bucket to preserve that grouping.
            let key = owner.unwrap_or_default();
            worker_to_leases_map
                .entry(key.clone())
                .or_default()
                .insert(lease.clone());
            *worker_to_total_assigned_throughput_map
                .entry(key)
                .or_insert(0.0) += tp;
        }

        // Active worker ids + default-worker metric seeding.
        let mut active_worker_id_set = HashSet::new();
        let ema_alpha = self.config.worker_metrics_ema_alpha;
        for wm in active_worker_metrics.iter_mut() {
            if let Some(id) = wm.worker_id() {
                active_worker_id_set.insert(id.to_string());
            }
            wm.set_ema_alpha(ema_alpha);
            if wm.is_using_default_worker_metric() {
                let assigned = wm
                    .worker_id()
                    .and_then(|id| worker_to_total_assigned_throughput_map.get(id).copied())
                    .unwrap_or(0.0);
                let ratio = if target_average_throughput != 0.0 {
                    assigned / target_average_throughput
                } else {
                    // Java divides by targetAverageThroughput even when 0 → NaN/Inf;
                    // preserved by the plain division above when non-zero. Guard the
                    // 0/0 case to 0.0 to avoid NaN propagation in the ordering.
                    0.0
                };
                Self::set_default_worker_metrics(wm, ratio);
            }
        }

        let mut inner = self.lock();
        inner.lease_list = lease_list;
        inner.lease_table_scan_time = scan_time;
        inner.active_worker_metrics = active_worker_metrics;
        inner.active_worker_id_set = active_worker_id_set;
        inner.target_average_throughput = target_average_throughput;
        inner.worker_to_leases_map = worker_to_leases_map;
        inner.worker_to_total_assigned_throughput_map = worker_to_total_assigned_throughput_map;

        Ok(count_of_workers_with_failing_metric)
    }

    /// Java `setOperatingRangeAndWorkerMetricsDataForDefaultWorker`: seed the
    /// single `"T"` metric with operating-range ceiling 100 and a 2-element
    /// metric-stats list `[ratio*100, ratio*100]` (load-bearing EMA seed shape).
    fn set_default_worker_metrics(wm: &mut WorkerMetricStats, ratio: f64) {
        let mut op = HashMap::new();
        op.insert(DEFAULT_WORKER_METRIC_NAME.to_string(), vec![100i64]);
        wm.set_operating_range(op);
        let mut ms = HashMap::new();
        ms.insert(
            DEFAULT_WORKER_METRIC_NAME.to_string(),
            vec![ratio * 100.0, ratio * 100.0],
        );
        wm.set_metric_stats(ms);
    }

    fn update_worker_throughput(inner: &mut Inner, worker_id: &str, lease_throughput: f64) {
        let v = inner
            .worker_to_total_assigned_throughput_map
            .entry(worker_id.to_string())
            .or_insert(0.0);
        *v += lease_throughput;
    }
}

impl StorageView for InMemoryStorageView {
    fn worker_to_leases_map(&self) -> HashMap<String, HashSet<Lease>> {
        self.lock().worker_to_leases_map.clone()
    }

    fn worker_to_total_assigned_throughput_map(&self) -> HashMap<String, f64> {
        self.lock().worker_to_total_assigned_throughput_map.clone()
    }

    fn lease_list(&self) -> Vec<Lease> {
        self.lock().lease_list.clone()
    }

    fn active_worker_metrics(&self) -> Vec<WorkerMetricStats> {
        self.lock().active_worker_metrics.clone()
    }

    fn active_worker_id_set(&self) -> HashSet<String> {
        self.lock().active_worker_id_set.clone()
    }

    fn lease_table_scan_time(&self) -> i64 {
        self.lock().lease_table_scan_time
    }

    fn target_average_throughput(&self) -> f64 {
        self.lock().target_average_throughput
    }

    fn perform_lease_assignment(&self, lease: &Lease, new_owner: &str) {
        let mut inner = self.lock();
        let existing_owner = lease
            .actual_owner()
            .map(|s| s.to_string())
            .unwrap_or_default();
        // Java: workerToLeasesMap.get(existingOwner).remove(lease)
        if let Some(set) = inner.worker_to_leases_map.get_mut(&existing_owner) {
            set.remove(lease);
        }
        // Java: computeIfAbsent(newOwner, ..).add(lease)
        inner
            .worker_to_leases_map
            .entry(new_owner.to_string())
            .or_default()
            .insert(lease.clone());
        let tp = lease.throughput_kbps().unwrap_or(0.0);
        Self::update_worker_throughput(&mut inner, new_owner, tp);
        Self::update_worker_throughput(&mut inner, &existing_owner, -tp);
        let key = lease.lease_key().unwrap_or_default().to_string();
        inner
            .lease_to_new_assigned_worker
            .insert(key, (lease.clone(), new_owner.to_string()));
    }

    fn is_worker_total_throughput_less_than_max_throughput(&self, worker_id: &str) -> bool {
        self.total_assigned_throughput(worker_id) <= self.config.max_throughput_per_host_kbps
    }

    fn is_worker_assigned_leases_less_than_max_leases(&self, worker_id: &str) -> bool {
        let inner = self.lock();
        match inner.worker_to_leases_map.get(worker_id) {
            None => true,
            Some(set) if set.is_empty() => true,
            Some(set) => (set.len() as i32) < self.max_leases_for_worker,
        }
    }

    fn total_assigned_throughput(&self, worker_id: &str) -> f64 {
        self.lock()
            .worker_to_total_assigned_throughput_map
            .get(worker_id)
            .copied()
            .unwrap_or(0.0)
    }
}
