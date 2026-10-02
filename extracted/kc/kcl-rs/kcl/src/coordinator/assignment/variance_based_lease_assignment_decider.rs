//! Port of `software.amazon.kinesis.coordinator.assignment.VarianceBasedLeaseAssignmentDecider`.
//!
//! Default/advanced strategy: balances leases to minimize cross-fleet variance
//! in one or more named `WorkerMetricStats` dimensions (e.g. CPU%) rather than
//! raw lease count, using each metric's fleet-average as a pivot and a max-heap
//! of workers ranked by capacity-remaining-to-reach-average.
//!
//! # PriorityQueue-with-live-comparator port
//!
//! Java's `PriorityQueue` re-invokes the comparator against **current** object
//! state on every structural op, and the algorithm relies on a strict
//! poll-mutate-reinsert discipline (never mutate a resident element). Rust's
//! [`BinaryHeap`](std::collections::BinaryHeap) is identical in that respect, so
//! we store `(ordering_key, WorkerMetricStats)` and **recompute the key on every
//! (re)insertion** — reproducing Java's re-evaluation-at-insertion exactly. The
//! fleet-average map is fixed after `initialize`, so keys are stable per state.
//!
//! # Randomness
//!
//! `getLeasesCombiningToThroughput` shuffles the donor's leases with the default
//! unseeded RNG (`rand::rng()`) — genuine run-to-run nondeterminism in
//! *which* leases move (the aggregate throughput is bounded either way). Tests
//! assert aggregate counts/throughput, not exact lease identities.

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, VecDeque};

use rand::seq::SliceRandom;

use super::in_memory_storage_view::StorageView;
use super::lease_assignment_decider::LeaseAssignmentDecider;
use crate::leases::Lease;
use crate::worker::metricstats::WorkerMetricStats;

/// Heap entry ordered as a **max-heap** by `computePercentageToReachAverage`
/// (workers furthest below target popped first). Key computed at insertion.
struct HeapEntry {
    key: f64,
    worker: WorkerMetricStats,
}

impl PartialEq for HeapEntry {
    fn eq(&self, other: &Self) -> bool {
        self.key == other.key
    }
}
impl Eq for HeapEntry {}
impl PartialOrd for HeapEntry {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}
impl Ord for HeapEntry {
    fn cmp(&self, other: &Self) -> Ordering {
        // Max-heap by key; total order over f64 (NaN sorts as equal-lowest).
        self.key.partial_cmp(&other.key).unwrap_or(Ordering::Equal)
    }
}

/// Variance-based [`LeaseAssignmentDecider`].
pub struct VarianceBasedLeaseAssignmentDecider<'a> {
    in_memory_storage_view: &'a dyn StorageView,
    dampening_percentage_value: i32,
    re_balance_threshold: i32,
    allow_throughput_overshoot: bool,
    worker_metrics_to_fleet_level_average: HashMap<String, f64>,
    assignable_workers: BinaryHeap<HeapEntry>,
    target_lease_per_worker: i32,
}

impl<'a> VarianceBasedLeaseAssignmentDecider<'a> {
    /// Java constructor `(InMemoryStorageView, dampeningPercentageValue,
    /// reBalanceThreshold, allowThroughputOvershoot)`.
    pub fn new(
        in_memory_storage_view: &'a dyn StorageView,
        dampening_percentage_value: i32,
        re_balance_threshold: i32,
        allow_throughput_overshoot: bool,
    ) -> Self {
        let mut decider = Self {
            in_memory_storage_view,
            dampening_percentage_value,
            re_balance_threshold,
            allow_throughput_overshoot,
            worker_metrics_to_fleet_level_average: HashMap::new(),
            assignable_workers: BinaryHeap::new(),
            target_lease_per_worker: 1,
        };
        decider.initialize();
        // Build the (max-heap) queue of assignable workers.
        let available = decider.get_available_workers_for_assignment(
            decider.in_memory_storage_view.active_worker_metrics(),
        );
        for w in available {
            decider.push_worker(w);
        }
        decider
    }

    fn initialize(&mut self) {
        // workerMetricsToFleetLevelAverageMap: per metric name, arithmetic mean
        // of that stat's current value across ALL active workers that report it.
        let active = self.in_memory_storage_view.active_worker_metrics();
        let mut sums: HashMap<String, (f64, usize)> = HashMap::new();
        for wm in &active {
            if let Some(stats) = wm.metric_stats() {
                for name in stats.keys() {
                    let v = wm.get_metric_stat(name);
                    let e = sums.entry(name.clone()).or_insert((0.0, 0));
                    e.0 += v;
                    e.1 += 1;
                }
            }
        }
        self.worker_metrics_to_fleet_level_average = sums
            .into_iter()
            .map(|(k, (sum, cnt))| (k, if cnt > 0 { sum / cnt as f64 } else { 0.0 }))
            .collect();

        let total_workers = active.len().max(1);
        self.target_lease_per_worker =
            ((self.in_memory_storage_view.lease_list().len() / total_workers) as i32).max(1);
    }

    fn get_available_workers_for_assignment(
        &self,
        worker_metrics_list: Vec<WorkerMetricStats>,
    ) -> Vec<WorkerMetricStats> {
        worker_metrics_list
            .into_iter()
            .filter(|wm| {
                let id = wm.worker_id().unwrap_or_default();
                self.in_memory_storage_view
                    .is_worker_total_throughput_less_than_max_throughput(id)
                    && self
                        .in_memory_storage_view
                        .is_worker_assigned_leases_less_than_max_leases(id)
            })
            .collect()
    }

    fn push_worker(&mut self, worker: WorkerMetricStats) {
        let key =
            worker.compute_percentage_to_reach_average(&self.worker_metrics_to_fleet_level_average);
        self.assignable_workers.push(HeapEntry { key, worker });
    }

    fn poll_worker(&mut self) -> Option<WorkerMetricStats> {
        self.assignable_workers.pop().map(|e| e.worker)
    }

    /// Java `getWorkersToTakeLeasesFromIfRequired`.
    fn get_workers_to_take_leases_from_if_required(
        &self,
        current_worker_metrics: &[WorkerMetricStats],
        worker_metrics_name: &str,
        worker_metrics_value_avg: f64,
    ) -> Vec<WorkerMetricStats> {
        let mut worker_ids_above_average: Vec<WorkerMetricStats> = Vec::new();
        let upper_limit =
            worker_metrics_value_avg * (1.0 + self.re_balance_threshold as f64 / 100.0);
        let lower_limit =
            worker_metrics_value_avg * (1.0 - self.re_balance_threshold as f64 / 100.0);

        tracing::info!(
            "Range for re-balance upper threshold {} and lower threshold {}",
            upper_limit,
            lower_limit
        );

        let mut most_loaded_worker: Option<WorkerMetricStats> = None;
        let mut most_loaded_value = f64::NEG_INFINITY;
        let mut should_trigger_re_balance = false;

        for wm in current_worker_metrics {
            let current_value = wm.get_metric_stat(worker_metrics_name);
            let above_operating_range =
                wm.is_worker_metric_above_operating_range(worker_metrics_name);
            if current_value > upper_limit || current_value < lower_limit || above_operating_range {
                should_trigger_re_balance = true;
            }
            if current_value >= upper_limit || above_operating_range {
                worker_ids_above_average.push(wm.clone());
            }
            if most_loaded_worker.is_none() || most_loaded_value < current_value {
                most_loaded_worker = Some(wm.clone());
                most_loaded_value = current_value;
            }
        }

        if worker_ids_above_average.is_empty() {
            if let Some(w) = most_loaded_worker {
                worker_ids_above_average.push(w);
            }
        }

        if should_trigger_re_balance {
            worker_ids_above_average
        } else {
            Vec::new()
        }
    }

    fn get_leases_to_take(&self, worker_id: &str, throughput_to_take: f64) -> VecDeque<Lease> {
        let map = self.in_memory_storage_view.worker_to_leases_map();
        let existing_leases = map.get(worker_id);
        let existing_leases = match existing_leases {
            None => return VecDeque::new(),
            Some(s) if s.is_empty() => return VecDeque::new(),
            Some(s) => s,
        };

        if self
            .in_memory_storage_view
            .total_assigned_throughput(worker_id)
            == 0.0
        {
            // Zero throughput but 1+ leases: take exactly 1 lease.
            let first = existing_leases.iter().next().cloned();
            let mut q = VecDeque::new();
            if let Some(l) = first {
                q.push_back(l);
            }
            return q;
        }

        self.get_leases_combining_to_throughput(worker_id, throughput_to_take)
    }

    fn get_leases_combining_to_throughput(
        &self,
        worker_id: &str,
        throughput_to_get: f64,
    ) -> VecDeque<Lease> {
        let map = self.in_memory_storage_view.worker_to_leases_map();
        let mut assigned_leases: Vec<Lease> = match map.get(worker_id) {
            None => return VecDeque::new(),
            Some(s) => s.iter().cloned().collect(),
        };
        if assigned_leases.is_empty() {
            return VecDeque::new();
        }
        assigned_leases.shuffle(&mut rand::rng());

        let mut response: VecDeque<Lease> = VecDeque::new();
        let mut remaining = throughput_to_get;
        for lease in &assigned_leases {
            let tp = lease.throughput_kbps().unwrap_or(0.0);
            // Stop BEFORE overshooting.
            if remaining - tp <= 0.0 {
                continue;
            }
            remaining -= tp;
            response.push_back(lease.clone());
        }

        if self.allow_throughput_overshoot && response.is_empty() {
            if let Some(min) = assigned_leases
                .iter()
                .min_by(|a, b| {
                    a.throughput_kbps()
                        .unwrap_or(0.0)
                        .partial_cmp(&b.throughput_kbps().unwrap_or(0.0))
                        .unwrap_or(Ordering::Equal)
                })
                .cloned()
            {
                response.push_back(min);
            }
        }
        response
    }

    /// Java `assignLease(lease, workerMetrics, isExpiredLease)`.
    fn assign_lease(
        &mut self,
        lease: &Lease,
        worker_metrics: WorkerMetricStats,
        is_expired_lease: bool,
    ) {
        let is_pending_checkpoint_expired = is_expired_lease && lease.shutdown_requested();

        if !is_pending_checkpoint_expired
            && lease.actual_owner().is_some()
            && lease.actual_owner() == worker_metrics.worker_id()
        {
            // Same owner: no assignment; requeue the (unmutated) worker.
            self.push_worker(worker_metrics);
            return;
        }

        if is_pending_checkpoint_expired {
            tracing::info!(
                "Assigning expired pending checkpoint lease {} (checkpointOwner={:?}) to worker {:?}",
                lease.lease_key().unwrap_or_default(),
                lease.checkpoint_owner(),
                worker_metrics.worker_id()
            );
        } else {
            tracing::info!(
                "Assigning lease : {} to worker : {:?}",
                lease.lease_key().unwrap_or_default(),
                worker_metrics.worker_id()
            );
        }

        worker_metrics.extrapolate_metric_stat_values_for_added_throughput(
            &self.worker_metrics_to_fleet_level_average,
            self.in_memory_storage_view.target_average_throughput(),
            lease.throughput_kbps().unwrap_or(0.0),
            self.target_lease_per_worker as f64,
        );
        let worker_id = worker_metrics.worker_id().unwrap_or_default().to_string();
        self.in_memory_storage_view
            .perform_lease_assignment(lease, &worker_id);
        if self
            .in_memory_storage_view
            .is_worker_total_throughput_less_than_max_throughput(&worker_id)
            && self
                .in_memory_storage_view
                .is_worker_assigned_leases_less_than_max_leases(&worker_id)
        {
            self.push_worker(worker_metrics);
        }
    }
}

impl<'a> LeaseAssignmentDecider for VarianceBasedLeaseAssignmentDecider<'a> {
    fn assign_expired_or_unassigned_leases(
        &mut self,
        expired_or_unassigned_leases: &mut Vec<Lease>,
    ) {
        // Sort ascending by lastCounterIncrementNanos (unassigned=0 first).
        expired_or_unassigned_leases.sort_by_key(|a| a.last_counter_increment_nanos());

        let mut assigned_keys: std::collections::HashSet<String> = std::collections::HashSet::new();
        // Iterate over an owned snapshot; assign_lease borrows &mut self.
        let leases: Vec<Lease> = expired_or_unassigned_leases.clone();
        for lease in &leases {
            match self.poll_worker() {
                Some(worker) => {
                    self.assign_lease(lease, worker, true);
                    if let Some(k) = lease.lease_key() {
                        assigned_keys.insert(k.to_string());
                    }
                }
                None => {
                    tracing::info!(
                        "No worker available to assign lease {}",
                        lease.lease_key().unwrap_or_default()
                    );
                    break;
                }
            }
        }
        expired_or_unassigned_leases.retain(|lease| {
            !lease
                .lease_key()
                .map(|k| assigned_keys.contains(k))
                .unwrap_or(false)
        });
    }

    fn balance_worker_variance(&mut self) {
        let active_worker_metrics = self.in_memory_storage_view.active_worker_metrics();

        let mut worker_id_to_throughput_to_take: HashMap<String, f64> = HashMap::new();
        let mut max_throughput_take = -1.0f64;

        // Iterate metric names deterministically for reproducibility.
        let mut metric_names: Vec<String> = self
            .worker_metrics_to_fleet_level_average
            .keys()
            .cloned()
            .collect();
        metric_names.sort();

        for worker_metrics_name in &metric_names {
            let fleet_average = self.worker_metrics_to_fleet_level_average[worker_metrics_name];
            let current_worker_metrics: Vec<WorkerMetricStats> = active_worker_metrics
                .iter()
                .filter(|wm| wm.contains_metric_stat(worker_metrics_name))
                .cloned()
                .collect();

            let workers_to_take_from = self.get_workers_to_take_leases_from_if_required(
                &current_worker_metrics,
                worker_metrics_name,
                fleet_average,
            );

            let mut current_map: HashMap<String, f64> = HashMap::new();
            let mut total_for_metric = 0.0;
            for worker in &workers_to_take_from {
                let worker_value = worker.get_metric_stat(worker_metrics_name);
                let load_percentage_to_take = (worker_value - fleet_average) / worker_value;
                let dampened =
                    load_percentage_to_take * (self.dampening_percentage_value as f64 / 100.0);
                let worker_id = worker.worker_id().unwrap_or_default();
                let throughput_to_take = self
                    .in_memory_storage_view
                    .total_assigned_throughput(worker_id)
                    * dampened;
                tracing::info!(
                    "For worker : {} taking throughput : {} after dampening based on WorkerMetricStats : {}",
                    worker_id,
                    throughput_to_take,
                    worker_metrics_name
                );
                total_for_metric += throughput_to_take;
                current_map.insert(worker_id.to_string(), throughput_to_take);
            }

            if max_throughput_take < total_for_metric {
                worker_id_to_throughput_to_take = current_map;
                max_throughput_take = total_for_metric;
            }
        }

        // Sort donors descending by throughput-to-take.
        let mut sorted_donors: Vec<(String, f64)> =
            worker_id_to_throughput_to_take.into_iter().collect();
        sorted_donors.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(Ordering::Equal));

        for (worker_id, throughput_to_take) in sorted_donors {
            let leases_to_take = self.get_leases_to_take(&worker_id, throughput_to_take);
            for lease in leases_to_take {
                match self.poll_worker() {
                    Some(worker_to_assign) => {
                        if worker_to_assign
                            .will_any_metric_stats_go_above_average_utilization_or_operating_range(
                                &self.worker_metrics_to_fleet_level_average,
                                self.in_memory_storage_view.target_average_throughput(),
                                lease.throughput_kbps().unwrap_or(0.0),
                                self.target_lease_per_worker as f64,
                            )
                        {
                            tracing::info!("No worker to assign anymore in this iteration due to hitting average values");
                            // Java: break the whole taken-lease loop for this donor
                            // (worker is dropped from the queue, not requeued).
                            break;
                        }
                        self.assign_lease(&lease, worker_to_assign, false);
                    }
                    None => break,
                }
            }
        }
    }
}

#[cfg(test)]
mod tests;
