//! Unit tests for the variance-based decider's core math.
//!
//! Java has no dedicated `VarianceBasedLeaseAssignmentDeciderTest` — its
//! behavior is covered by the DynamoDBEmbedded `LeaseAssignmentManagerTest`
//! cases (skipped: WAVE-PLAN TEST-PARITY GAPS). These focused tests validate
//! the variance assignment/rebalance math against a `MockStorageView`.

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};

use super::*;
use crate::coordinator::assignment::in_memory_storage_view::MockStorageView;

fn lease(key: &str, owner: Option<&str>, throughput: f64, lcin: i64) -> Lease {
    let mut l = Lease::default();
    l.set_lease_key(key);
    l.set_lease_owner(owner.map(|s| s.to_string()));
    l.set_throughput_kbps(throughput);
    l.set_last_counter_increment_nanos(Some(lcin));
    l
}

fn wm(worker_id: &str, cpu: f64) -> WorkerMetricStats {
    let mut ms = HashMap::new();
    ms.insert("C".to_string(), vec![cpu, cpu]);
    let mut op = HashMap::new();
    op.insert("C".to_string(), vec![100i64]);
    WorkerMetricStats::legacy_builder()
        .worker_id(worker_id)
        .last_update_time(chrono::Utc::now().timestamp())
        .metric_stats(ms)
        .operating_range(op)
        .ema_alpha(0.5)
        .build()
}

#[derive(Default, Clone)]
struct Recorder {
    calls: Arc<Mutex<Vec<(String, String)>>>,
}
impl Recorder {
    fn assigned_to(&self, worker: &str) -> usize {
        self.calls
            .lock()
            .unwrap()
            .iter()
            .filter(|(_, w)| w == worker)
            .count()
    }
}

fn mock_view(
    worker_to_leases: HashMap<String, HashSet<Lease>>,
    worker_throughput: HashMap<String, f64>,
    active_metrics: Vec<WorkerMetricStats>,
    lease_list: Vec<Lease>,
    target_avg: f64,
    max_throughput: f64,
    recorder: Recorder,
) -> MockStorageView {
    let mut m = MockStorageView::new();
    let shared = Arc::new(Mutex::new(worker_to_leases));
    let shared_tp = Arc::new(Mutex::new(worker_throughput));

    let g = shared.clone();
    m.expect_worker_to_leases_map()
        .returning(move || g.lock().unwrap().clone());
    let active2 = active_metrics.clone();
    m.expect_active_worker_metrics()
        .returning(move || active2.clone());
    let active_ids: HashSet<String> = active_metrics
        .iter()
        .filter_map(|w| w.worker_id().map(|s| s.to_string()))
        .collect();
    m.expect_active_worker_id_set()
        .returning(move || active_ids.clone());
    m.expect_lease_list().returning(move || lease_list.clone());
    m.expect_target_average_throughput()
        .returning(move || target_avg);

    let tp = shared_tp.clone();
    m.expect_total_assigned_throughput()
        .returning(move |w| tp.lock().unwrap().get(w).copied().unwrap_or(0.0));
    let tp2 = shared_tp.clone();
    m.expect_worker_to_total_assigned_throughput_map()
        .returning(move || tp2.lock().unwrap().clone());
    let tp3 = shared_tp.clone();
    m.expect_is_worker_total_throughput_less_than_max_throughput()
        .returning(move |w| tp3.lock().unwrap().get(w).copied().unwrap_or(0.0) <= max_throughput);
    let g2 = shared.clone();
    m.expect_is_worker_assigned_leases_less_than_max_leases()
        .returning(move |w| {
            g2.lock()
                .unwrap()
                .get(w)
                .map(|s| s.len() < 1_000_000)
                .unwrap_or(true)
        });

    let rec = recorder;
    let g3 = shared.clone();
    let tp4 = shared_tp.clone();
    m.expect_perform_lease_assignment()
        .returning(move |lease, worker_id| {
            rec.calls.lock().unwrap().push((
                lease.lease_key().unwrap_or_default().to_string(),
                worker_id.to_string(),
            ));
            let old = lease
                .actual_owner()
                .map(|s| s.to_string())
                .unwrap_or_default();
            let mut map = g3.lock().unwrap();
            if let Some(s) = map.get_mut(&old) {
                s.remove(lease);
            }
            map.entry(worker_id.to_string())
                .or_default()
                .insert(lease.clone());
            let t = lease.throughput_kbps().unwrap_or(0.0);
            let mut tp = tp4.lock().unwrap();
            *tp.entry(worker_id.to_string()).or_insert(0.0) += t;
            *tp.entry(old).or_insert(0.0) -= t;
        });
    m
}

#[test]
fn assign_expired_goes_to_lowest_utilization_worker() {
    // worker1 hot (cpu 90), worker2 cold (cpu 10). Unassigned lease -> worker2.
    let w1 = wm("worker1", 90.0);
    let w2 = wm("worker2", 10.0);
    let l = lease("lease1", None, 5.0, 0);

    let mut w2l = HashMap::new();
    w2l.insert("worker1".to_string(), HashSet::new());
    w2l.insert("worker2".to_string(), HashSet::new());
    let mut tp = HashMap::new();
    tp.insert("worker1".to_string(), 0.0);
    tp.insert("worker2".to_string(), 0.0);

    let recorder = Recorder::default();
    let m = mock_view(
        w2l,
        tp,
        vec![w1, w2],
        vec![l.clone()],
        50.0,
        f64::MAX,
        recorder.clone(),
    );
    let mut decider = VarianceBasedLeaseAssignmentDecider::new(&m, 60, 20, true);
    let mut leases = vec![l];
    decider.assign_expired_or_unassigned_leases(&mut leases);
    assert!(leases.is_empty(), "lease should be assigned");
    assert_eq!(
        recorder.assigned_to("worker2"),
        1,
        "lease goes to the cold worker"
    );
    assert_eq!(recorder.assigned_to("worker1"), 0);
}

#[test]
fn assign_expired_no_workers_leaves_leases_unassigned() {
    let l = lease("lease1", None, 5.0, 0);
    let recorder = Recorder::default();
    let m = mock_view(
        HashMap::new(),
        HashMap::new(),
        vec![], // no active workers -> empty heap
        vec![l.clone()],
        0.0,
        f64::MAX,
        recorder.clone(),
    );
    let mut decider = VarianceBasedLeaseAssignmentDecider::new(&m, 60, 20, true);
    let mut leases = vec![l];
    decider.assign_expired_or_unassigned_leases(&mut leases);
    assert_eq!(leases.len(), 1, "no worker -> lease stays unassigned");
}

#[test]
fn balance_rebalances_from_outlier_worker() {
    // worker1 hot (cpu 90, holds all the throughput), worker2 cold (cpu 10, empty).
    // Fleet avg cpu = 50; worker1 is above the upper re-balance limit (60) so it
    // donates. Leases are fine-grained (40 kbps each) relative to the per-worker
    // target throughput (200/2 = 100) so that worker2 can absorb one lease
    // without its extrapolated cpu crossing the fleet average — otherwise the
    // faithful `willAnyMetricStatsGoAboveAverage...` guard (KCL) would refuse
    // every candidate and no lease would move.
    let w1 = wm("worker1", 90.0);
    let w2 = wm("worker2", 10.0);
    let leases: Vec<Lease> = (0..5)
        .map(|i| lease(&format!("lease{i}"), Some("worker1"), 40.0, 100 + i as i64))
        .collect();

    let mut w2l = HashMap::new();
    w2l.insert(
        "worker1".to_string(),
        leases.iter().cloned().collect::<HashSet<_>>(),
    );
    w2l.insert("worker2".to_string(), HashSet::new());
    let mut tp = HashMap::new();
    tp.insert("worker1".to_string(), 200.0); // 5 x 40 kbps
    tp.insert("worker2".to_string(), 0.0);

    let recorder = Recorder::default();
    let m = mock_view(
        w2l,
        tp,
        vec![w1, w2],
        leases.clone(),
        100.0, // target avg throughput (200 total / 2 workers)
        f64::MAX,
        recorder.clone(),
    );
    let mut decider = VarianceBasedLeaseAssignmentDecider::new(&m, 60, 20, true);
    decider.balance_worker_variance();
    assert!(
        recorder.assigned_to("worker2") >= 1,
        "at least one lease rebalanced to the cold worker"
    );
}
