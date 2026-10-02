//! Port of `software.amazon.kinesis.coordinator.assignment.LAMDataSnapshot`.
//!
//! Immutable snapshot returned by [`LAMDataManager::load_data`](super::LamDataManager::load_data):
//! merged leases, lease deserialization failures, and merged (possibly
//! duplicate) worker-metric stats.
//!
//! Java `@Value @Builder`. The `workerMetricStats` list may contain duplicate
//! entries per workerId (one per source table during migration) — dedup is the
//! caller's responsibility.

use crate::leases::Lease;
use crate::worker::metricstats::WorkerMetricStats;

/// Immutable DTO returned by `LAMDataManager.loadData()`.
#[derive(Debug, Default, bon::Builder)]
pub struct LamDataSnapshot {
    /// All leases from the lease table.
    #[builder(default)]
    pub leases: Vec<Lease>,
    /// Lease keys that failed deserialization during the scan.
    #[builder(default)]
    pub lease_deserialization_failures: Vec<String>,
    /// All worker-metric stats, merged from all sources (may contain duplicates
    /// per workerId).
    #[builder(default)]
    pub worker_metric_stats: Vec<WorkerMetricStats>,
}

impl LamDataSnapshot {
    /// Java `getLeases()`.
    pub fn leases(&self) -> &[Lease] {
        &self.leases
    }
    /// Java `getLeaseDeserializationFailures()`.
    pub fn lease_deserialization_failures(&self) -> &[String] {
        &self.lease_deserialization_failures
    }
    /// Java `getWorkerMetricStats()`.
    pub fn worker_metric_stats(&self) -> &[WorkerMetricStats] {
        &self.worker_metric_stats
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::Lease;

    fn lease(key: &str, owner: &str) -> Lease {
        let mut l = Lease::default();
        l.set_lease_key(key);
        l.set_lease_owner(Some(owner.to_string()));
        l.set_lease_counter(1);
        l
    }

    fn wm(worker_id: &str) -> WorkerMetricStats {
        WorkerMetricStats::legacy_builder()
            .worker_id(worker_id)
            .last_update_time(chrono::Utc::now().timestamp())
            .build()
    }

    #[test]
    fn builder_with_all_fields() {
        let snapshot = LamDataSnapshot::builder()
            .leases(vec![lease("l1", "w1"), lease("l2", "w2")])
            .worker_metric_stats(vec![wm("w1"), wm("w2")])
            .lease_deserialization_failures(vec!["badKey1".into(), "badKey2".into()])
            .build();
        assert_eq!(snapshot.leases().len(), 2);
        assert_eq!(snapshot.worker_metric_stats().len(), 2);
        assert_eq!(snapshot.lease_deserialization_failures().len(), 2);
        assert_eq!(snapshot.leases()[0].lease_key(), Some("l1"));
        assert_eq!(snapshot.worker_metric_stats()[0].worker_id(), Some("w1"));
        assert_eq!(snapshot.lease_deserialization_failures()[0], "badKey1");
    }

    #[test]
    fn builder_empty_lists() {
        let snapshot = LamDataSnapshot::builder().build();
        assert!(snapshot.leases().is_empty());
        assert!(snapshot.worker_metric_stats().is_empty());
        assert!(snapshot.lease_deserialization_failures().is_empty());
    }

    #[test]
    fn builder_duplicate_worker_metrics_both_retained() {
        let snapshot = LamDataSnapshot::builder()
            .worker_metric_stats(vec![wm("worker1"), wm("worker1")])
            .build();
        assert_eq!(snapshot.worker_metric_stats().len(), 2);
        assert_eq!(
            snapshot.worker_metric_stats()[0].worker_id(),
            Some("worker1")
        );
        assert_eq!(
            snapshot.worker_metric_stats()[1].worker_id(),
            Some("worker1")
        );
    }

    #[test]
    fn builder_single_lease_snapshot_accessible() {
        let snapshot = LamDataSnapshot::builder()
            .leases(vec![lease("singleLease", "owner1")])
            .build();
        assert_eq!(snapshot.leases().len(), 1);
        assert_eq!(snapshot.leases()[0].lease_key(), Some("singleLease"));
        assert_eq!(snapshot.leases()[0].lease_owner(), Some("owner1"));
    }

    #[test]
    fn builder_only_deserialization_failures() {
        let snapshot = LamDataSnapshot::builder()
            .lease_deserialization_failures(vec!["key1".into(), "key2".into(), "key3".into()])
            .build();
        assert_eq!(snapshot.leases().len(), 0);
        assert_eq!(snapshot.worker_metric_stats().len(), 0);
        assert_eq!(snapshot.lease_deserialization_failures().len(), 3);
    }
}
