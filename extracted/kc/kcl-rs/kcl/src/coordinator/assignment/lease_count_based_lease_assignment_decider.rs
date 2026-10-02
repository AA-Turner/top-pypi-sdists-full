//! Port of `software.amazon.kinesis.coordinator.assignment.LeaseCountBasedLeaseAssignmentDecider`.
//!
//! Balances purely by lease **count** per worker (ignoring throughput /
//! WorkerMetricStats). Used when the config selects `LEASE_COUNT_BASED`.

use std::collections::{HashMap, HashSet};

use super::in_memory_storage_view::{NanoTimeProvider, StorageView};
use super::lease_assignment_decider::LeaseAssignmentDecider;
use crate::leases::Lease;

/// Lease-count-based [`LeaseAssignmentDecider`].
pub struct LeaseCountBasedLeaseAssignmentDecider<'a> {
    in_memory_storage_view: &'a dyn StorageView,
    max_leases_for_worker: i32,
    nano_time_provider: NanoTimeProvider,
}

impl<'a> LeaseCountBasedLeaseAssignmentDecider<'a> {
    /// Java constructor `(InMemoryStorageView, int maxLeasesForWorker, Supplier<Long> nanoTimeProvider)`.
    pub fn new(
        in_memory_storage_view: &'a dyn StorageView,
        max_leases_for_worker: i32,
        nano_time_provider: NanoTimeProvider,
    ) -> Self {
        Self {
            in_memory_storage_view,
            max_leases_for_worker,
            nano_time_provider,
        }
    }

    /// Java `calculateTargetLeaseCount()`: `1` if `workers >= leases`, else
    /// `ceil(leases/workers)` capped at `maxLeasesForWorker`.
    fn calculate_target_lease_count(&self) -> i32 {
        let total_leases = self.in_memory_storage_view.lease_list().len() as i32;
        let total_workers = self.in_memory_storage_view.active_worker_id_set().len() as i32;
        if total_workers >= total_leases {
            1
        } else {
            let mut target = total_leases / total_workers
                + if total_leases % total_workers == 0 {
                    0
                } else {
                    1
                };
            if target > self.max_leases_for_worker {
                let lease_spillover = (target - self.max_leases_for_worker).max(0);
                tracing::warn!(
                    "Target is {} leases and maxLeasesForWorker is {}. Resetting target to {}, lease spillover is {}. \
                     Note that some shards may not be processed if no other workers are able to pick them up.",
                    target,
                    self.max_leases_for_worker,
                    self.max_leases_for_worker,
                    lease_spillover
                );
                target = self.max_leases_for_worker;
            }
            target
        }
    }

    /// Java `getActiveWorkerLeaseCounts()`: per-active-worker current lease count
    /// (all active workers represented, even those with 0 leases).
    fn get_active_worker_lease_counts(&self) -> HashMap<String, i32> {
        let mut estimated_counts: HashMap<String, i32> = HashMap::new();
        let active_workers = self.in_memory_storage_view.active_worker_id_set();
        for (worker_id, leases) in self.in_memory_storage_view.worker_to_leases_map() {
            if active_workers.contains(&worker_id) {
                estimated_counts.insert(worker_id, leases.len() as i32);
            }
        }
        for worker_id in active_workers {
            estimated_counts.entry(worker_id).or_insert(0);
        }
        estimated_counts
    }

    /// Java `computeAvailableLeases()`: per-worker leases not blocked on a
    /// pending checkpoint (safe to transfer).
    fn compute_available_leases(&self) -> HashMap<String, Vec<Lease>> {
        let mut available_leases: HashMap<String, Vec<Lease>> = HashMap::new();
        let current_time_millis = nanos_to_millis((self.nano_time_provider)());
        for (worker_id, leases) in self.in_memory_storage_view.worker_to_leases_map() {
            let worker_available: Vec<Lease> = leases
                .into_iter()
                .filter(|lease| !lease.blocked_on_pending_checkpoint(current_time_millis))
                .collect();
            if !worker_available.is_empty() {
                available_leases.insert(worker_id, worker_available);
            }
        }
        available_leases
    }

    fn assign_lease(&self, lease: &Lease, worker_id: &str) {
        self.in_memory_storage_view
            .perform_lease_assignment(lease, worker_id);
    }
}

impl<'a> LeaseAssignmentDecider for LeaseCountBasedLeaseAssignmentDecider<'a> {
    fn assign_expired_or_unassigned_leases(
        &mut self,
        expired_or_unassigned_leases: &mut Vec<Lease>,
    ) {
        if expired_or_unassigned_leases.is_empty()
            || self
                .in_memory_storage_view
                .active_worker_id_set()
                .is_empty()
        {
            return;
        }

        // Stable sort ascending by lastCounterIncrementNanos (oldest first).
        expired_or_unassigned_leases.sort_by_key(|a| a.last_counter_increment_nanos());

        let mut lease_count_per_active_worker = self.get_active_worker_lease_counts();
        let target = self.calculate_target_lease_count();

        tracing::info!(
            "Lease count balancing: {} total leases, {} workers, target {} leases per worker",
            self.in_memory_storage_view.lease_list().len(),
            self.in_memory_storage_view.active_worker_id_set().len(),
            target
        );

        // workerQueue = worker ids sorted ascending by current lease count.
        // Java derives it from HashMap.entrySet() sorted by value; ties are in
        // arbitrary map-iteration order. We match "sort by count" (ties: by id
        // for determinism within this port).
        let mut worker_queue: Vec<(String, i32)> = lease_count_per_active_worker
            .iter()
            .map(|(k, v)| (k.clone(), *v))
            .collect();
        worker_queue.sort_by(|a, b| a.1.cmp(&b.1).then_with(|| a.0.cmp(&b.0)));
        let worker_queue: Vec<String> = worker_queue.into_iter().map(|(k, _)| k).collect();

        let mut assigned_keys: HashSet<String> = HashSet::new();
        let mut worker_index = 0usize;

        for lease in expired_or_unassigned_leases.iter() {
            if worker_index >= worker_queue.len() {
                break;
            }
            let worker_to_assign = &worker_queue[worker_index];
            self.assign_lease(lease, worker_to_assign);
            if let Some(k) = lease.lease_key() {
                assigned_keys.insert(k.to_string());
            }
            let new_count = lease_count_per_active_worker
                .get(worker_to_assign)
                .copied()
                .unwrap_or(0)
                + 1;
            lease_count_per_active_worker.insert(worker_to_assign.clone(), new_count);
            if new_count >= target {
                worker_index += 1;
            }
        }

        // removeAll(assignedLeases): retain only the unassigned (by lease key).
        expired_or_unassigned_leases.retain(|lease| {
            !lease
                .lease_key()
                .map(|k| assigned_keys.contains(k))
                .unwrap_or(false)
        });
    }

    fn balance_worker_variance(&mut self) {
        if self
            .in_memory_storage_view
            .active_worker_id_set()
            .is_empty()
        {
            return;
        }
        let lease_count_per_active_worker = self.get_active_worker_lease_counts();
        let mut available_leases_by_worker = self.compute_available_leases();
        let target = self.calculate_target_lease_count();

        // sortedWorkers = (worker, count) sorted ascending by count. Java holds
        // live Map.Entry handles; we hold a Vec and mutate counts by index.
        let mut sorted_workers: Vec<(String, i32)> = lease_count_per_active_worker
            .iter()
            .map(|(k, v)| (k.clone(), *v))
            .collect();
        sorted_workers.sort_by(|a, b| a.1.cmp(&b.1).then_with(|| a.0.cmp(&b.0)));

        let mut left = 0isize;
        let mut right = sorted_workers.len() as isize - 1;

        while left < right {
            let underloaded_count = sorted_workers[left as usize].1;
            let overloaded_count = sorted_workers[right as usize].1;

            let needed = target - underloaded_count;
            let excess = overloaded_count - target;

            if needed <= 0 {
                left += 1;
                continue;
            }
            if excess <= 0 {
                right -= 1;
                continue;
            }

            let overloaded_key = sorted_workers[right as usize].0.clone();
            let underloaded_key = sorted_workers[left as usize].0.clone();

            let lease_to_steal = available_leases_by_worker
                .get_mut(&overloaded_key)
                .and_then(|v| {
                    if v.is_empty() {
                        None
                    } else {
                        Some(v.remove(0))
                    }
                });

            match lease_to_steal {
                Some(lease) => {
                    self.assign_lease(&lease, &underloaded_key);
                    sorted_workers[left as usize].1 += 1;
                    sorted_workers[right as usize].1 -= 1;
                }
                None => {
                    right -= 1;
                }
            }
        }
    }
}

fn nanos_to_millis(nanos: i64) -> i64 {
    nanos / 1_000_000
}

#[cfg(test)]
mod tests;
