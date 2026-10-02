//! Port of `LeaseCountBasedLeaseAssignmentDeciderTest`.
//!
//! Java mocks `InMemoryStorageView` (Mockito); here we use the `mockall`-
//! generated [`MockStorageView`] and build real [`Lease`] values (the decider
//! only touches accessors real leases support). `performLeaseAssignment` is
//! recorded/mutates a shared map via the mock, mirroring Java's `doAnswer`.

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};

use super::*;
use crate::coordinator::assignment::in_memory_storage_view::MockStorageView;

const MAX_LEASES_FOR_WORKER: i32 = 10;
const CURRENT_TIME_NANOS: i64 = 10_000 * 1_000_000; // 10000ms in nanos

fn nano_provider() -> NanoTimeProvider {
    Arc::new(|| CURRENT_TIME_NANOS)
}

fn create_lease(lease_key: &str, owner: Option<&str>, last_counter_increment: i64) -> Lease {
    let mut l = Lease::default();
    l.set_lease_key(lease_key);
    l.set_lease_owner(owner.map(|s| s.to_string()));
    l.set_last_counter_increment_nanos(Some(last_counter_increment));
    l
}

/// worker1/checkpointOwner handoff lease: shutdown requested + blocked.
fn create_lease_with_handoff(
    lease_key: &str,
    lease_owner: &str,
    checkpoint_owner: &str,
    lcin: i64,
) -> Lease {
    let mut l = Lease::default();
    l.set_lease_key(lease_key);
    l.set_lease_owner(Some(lease_owner.to_string()));
    l.set_checkpoint_owner(Some(checkpoint_owner.to_string()));
    l.set_last_counter_increment_nanos(Some(lcin));
    // future deadline -> blocked_on_pending_checkpoint == true
    l.set_checkpoint_owner_timeout_timestamp_millis(Some(i64::MAX));
    l
}

// Records perform_lease_assignment calls and mutates a shared worker->leases map.
#[derive(Default, Clone)]
struct Recorder {
    calls: Arc<Mutex<Vec<(String, String)>>>, // (lease_key, worker_id)
}

impl Recorder {
    fn assign_count(&self) -> usize {
        self.calls.lock().unwrap().len()
    }
    fn assigned_to(&self, worker: &str) -> usize {
        self.calls
            .lock()
            .unwrap()
            .iter()
            .filter(|(_, w)| w == worker)
            .count()
    }
    fn assigned_any_to(&self, worker: &str) -> bool {
        self.assigned_to(worker) > 0
    }
    fn assigned_lease(&self, lease_key: &str) -> bool {
        self.calls
            .lock()
            .unwrap()
            .iter()
            .any(|(k, _)| k == lease_key)
    }
}

fn mock_with(
    worker_to_leases: HashMap<String, HashSet<Lease>>,
    active_workers: HashSet<String>,
    lease_list: Vec<Lease>,
    recorder: Recorder,
) -> MockStorageView {
    let mut m = MockStorageView::new();
    let shared = Arc::new(Mutex::new(worker_to_leases));

    let shared_get = shared.clone();
    m.expect_worker_to_leases_map()
        .returning(move || shared_get.lock().unwrap().clone());
    m.expect_active_worker_id_set()
        .returning(move || active_workers.clone());
    m.expect_lease_list().returning(move || lease_list.clone());

    let shared_assign = shared.clone();
    m.expect_perform_lease_assignment()
        .returning(move |lease, worker_id| {
            recorder.calls.lock().unwrap().push((
                lease.lease_key().unwrap_or_default().to_string(),
                worker_id.to_string(),
            ));
            // Simulate the real map mutation: add to new owner's set.
            shared_assign
                .lock()
                .unwrap()
                .entry(worker_id.to_string())
                .or_default()
                .insert(lease.clone());
        });
    m
}

#[test]
fn assign_expired_empty_list_no_assignments() {
    let recorder = Recorder::default();
    let m = mock_with(HashMap::new(), HashSet::new(), vec![], recorder.clone());
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    let mut empty: Vec<Lease> = vec![];
    decider.assign_expired_or_unassigned_leases(&mut empty);
    assert_eq!(recorder.assign_count(), 0);
}

#[test]
fn assign_expired_single_worker_assigns_all() {
    let l1 = create_lease("lease1", None, 100);
    let l2 = create_lease("lease2", None, 200);
    let mut w2l = HashMap::new();
    w2l.insert("worker1".to_string(), HashSet::new());
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string()]),
        vec![l1.clone(), l2.clone()],
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    let mut leases = vec![l1, l2];
    decider.assign_expired_or_unassigned_leases(&mut leases);
    assert!(recorder
        .calls
        .lock()
        .unwrap()
        .contains(&("lease1".to_string(), "worker1".to_string())));
    assert!(recorder
        .calls
        .lock()
        .unwrap()
        .contains(&("lease2".to_string(), "worker1".to_string())));
    assert!(leases.is_empty());
}

#[test]
fn assign_expired_multiple_workers_distributes() {
    let l1 = create_lease("lease1", None, 100);
    let l2 = create_lease("lease2", None, 200);
    let l3 = create_lease("lease3", None, 300);
    let mut w2l = HashMap::new();
    w2l.insert("worker1".to_string(), HashSet::new());
    w2l.insert("worker2".to_string(), HashSet::new());
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string(), "worker2".to_string()]),
        vec![l1.clone(), l2.clone(), l3.clone()],
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    let mut leases = vec![l1, l2, l3];
    decider.assign_expired_or_unassigned_leases(&mut leases);
    assert_eq!(recorder.assign_count(), 3);
    assert!(leases.is_empty());
}

#[test]
fn balance_even_distribution_no_rebalancing() {
    let l1 = create_lease("lease1", Some("worker1"), 100);
    let l2 = create_lease("lease2", Some("worker2"), 200);
    let mut w2l = HashMap::new();
    w2l.insert("worker1".to_string(), HashSet::from([l1.clone()]));
    w2l.insert("worker2".to_string(), HashSet::from([l2.clone()]));
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string(), "worker2".to_string()]),
        vec![l1, l2],
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    decider.balance_worker_variance();
    assert_eq!(recorder.assign_count(), 0);
}

#[test]
fn balance_unbalanced_rebalances() {
    let l1 = create_lease("lease1", Some("worker1"), 100);
    let l2 = create_lease("lease2", Some("worker1"), 200);
    let mut w2l = HashMap::new();
    w2l.insert(
        "worker1".to_string(),
        HashSet::from([l1.clone(), l2.clone()]),
    );
    w2l.insert("worker2".to_string(), HashSet::new());
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string(), "worker2".to_string()]),
        vec![l1, l2],
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    decider.balance_worker_variance();
    assert!(
        recorder.assigned_any_to("worker2"),
        "one lease should move to worker2"
    );
}

#[test]
fn balance_avoids_stealing_handoff_leases() {
    let normal = create_lease("lease1", Some("worker1"), 100);
    let handoff = create_lease_with_handoff("lease2", "worker2", "worker1", 200);
    let mut w2l = HashMap::new();
    w2l.insert(
        "worker1".to_string(),
        HashSet::from([normal.clone(), handoff.clone()]),
    );
    w2l.insert("worker2".to_string(), HashSet::new());
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string(), "worker2".to_string()]),
        vec![normal, handoff],
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    decider.balance_worker_variance();
    assert!(
        !recorder.assigned_lease("lease2"),
        "handoff lease must not be stolen"
    );
}

#[test]
fn balance_expired_handoff_lease_treated_as_available() {
    let normal = create_lease("lease1", Some("worker1"), 100);
    // expired handoff: shutdown requested + deadline passed -> blocked == false.
    let mut expired = Lease::default();
    expired.set_lease_key("lease2");
    expired.set_lease_owner(Some("worker1".to_string()));
    expired.set_checkpoint_owner(Some("worker1".to_string()));
    expired.set_last_counter_increment_nanos(Some(200));
    expired.set_checkpoint_owner_timeout_timestamp_millis(Some(0)); // past deadline

    let mut w2l = HashMap::new();
    w2l.insert(
        "worker1".to_string(),
        HashSet::from([normal.clone(), expired.clone()]),
    );
    w2l.insert("worker2".to_string(), HashSet::new());
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string(), "worker2".to_string()]),
        vec![normal, expired],
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    decider.balance_worker_variance();
    assert!(
        recorder.assigned_any_to("worker2"),
        "expired handoff lease can be stolen"
    );
}

#[test]
fn balance_max_leases_reached_stops() {
    let mut w2l = HashMap::new();
    let mut w1 = HashSet::new();
    let mut w2 = HashSet::new();
    let mut all = vec![];
    for i in 1..=12 {
        let a = create_lease(&format!("lease{i}"), Some("worker1"), i * 100);
        let b = create_lease(&format!("lease{}", i + 12), Some("worker2"), (i + 12) * 100);
        w1.insert(a.clone());
        w2.insert(b.clone());
        all.push(a);
        all.push(b);
    }
    w2l.insert("worker1".to_string(), w1);
    w2l.insert("worker2".to_string(), w2);
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string(), "worker2".to_string()]),
        all,
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    decider.balance_worker_variance();
    // Both workers at 12 (> target 12? target = ceil(24/2)=12, capped at 10 -> 10).
    // needed = 10 - 12 < 0 for both -> no moves.
    assert_eq!(recorder.assign_count(), 0);
}

#[test]
fn assign_expired_max_leases_reached_stops_assigning() {
    let mut unassigned = vec![];
    for i in 1..=15 {
        unassigned.push(create_lease(&format!("lease{i}"), None, i * 100));
    }
    let mut w2l = HashMap::new();
    w2l.insert("worker1".to_string(), HashSet::new());
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string()]),
        unassigned.clone(),
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    decider.assign_expired_or_unassigned_leases(&mut unassigned);
    assert_eq!(
        recorder.assigned_to("worker1"),
        MAX_LEASES_FOR_WORKER as usize
    );
    assert_eq!(unassigned.len(), 5);
}

#[test]
fn sequential_assignment_and_balancing_works_with_updated_worker_to_leases_map() {
    // 3 expired leases and 2 workers, worker1 already has 2 leases.
    let existing1 = create_lease("existing1", Some("worker1"), 40);
    let existing2 = create_lease("existing2", Some("worker1"), 50);
    let expired1 = create_lease("expired1", None, 100);
    let expired2 = create_lease("expired2", None, 200);
    let expired3 = create_lease("expired3", None, 300);

    let mut w2l = HashMap::new();
    w2l.insert(
        "worker1".to_string(),
        HashSet::from([existing1.clone(), existing2.clone()]),
    );
    w2l.insert("worker2".to_string(), HashSet::new());

    let recorder = Recorder::default();
    // `mock_with` simulates `performLeaseAssignment` mutating the shared
    // worker->leases map (Java's `doAnswer`), so `balance_worker_variance`
    // observes the updated counts.
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string(), "worker2".to_string()]),
        vec![
            existing1,
            existing2,
            expired1.clone(),
            expired2.clone(),
            expired3.clone(),
        ],
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());

    // Assign expired leases first.
    let mut expired = vec![expired1, expired2, expired3];
    decider.assign_expired_or_unassigned_leases(&mut expired);
    assert_eq!(recorder.assign_count(), 3);
    assert!(expired.is_empty());

    // Now balance variance using the updated worker->leases map.
    decider.balance_worker_variance();

    // No fewer than the 3 assignments already made.
    assert!(recorder.assign_count() >= 3);
}

#[test]
fn assign_expired_dead_worker_leases_go_to_active_workers() {
    let d1 = create_lease("dead1", Some("deadWorker"), 100);
    let d2 = create_lease("dead2", Some("deadWorker"), 200);
    let d3 = create_lease("dead3", Some("deadWorker"), 300);
    let mut w2l = HashMap::new();
    w2l.insert(
        "deadWorker".to_string(),
        HashSet::from([d1.clone(), d2.clone(), d3.clone()]),
    );
    w2l.insert("worker1".to_string(), HashSet::new());
    w2l.insert("worker2".to_string(), HashSet::new());
    let recorder = Recorder::default();
    let m = mock_with(
        w2l,
        HashSet::from(["worker1".to_string(), "worker2".to_string()]),
        vec![d1.clone(), d2.clone(), d3.clone()],
        recorder.clone(),
    );
    let mut decider =
        LeaseCountBasedLeaseAssignmentDecider::new(&m, MAX_LEASES_FOR_WORKER, nano_provider());
    let mut expired = vec![d1, d2, d3];
    decider.assign_expired_or_unassigned_leases(&mut expired);
    assert_eq!(recorder.assigned_to("deadWorker"), 0);
    assert_eq!(recorder.assign_count(), 3);
    assert!(expired.is_empty());
}
