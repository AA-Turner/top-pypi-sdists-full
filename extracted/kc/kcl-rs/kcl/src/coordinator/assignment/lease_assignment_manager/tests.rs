//! Tests for `LeaseAssignmentManager`.
//!
//! The Java `LeaseAssignmentManagerTest` `performAssignment_*` /
//! `loadInMemoryStorageView_*` cases are DynamoDBEmbedded integration tests
//! (skipped: WAVE-PLAN TEST-PARITY GAPS). Ported here: the two scheduling tests
//! (`testLeaseAssignmentSchedulingWithDefaultInterval` /
//! `testLeaseAssignmentWithDifferentIntervals`) adapted to the tokio
//! interval loop, plus not-leader + leader-loop behavior with mocked deps.

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

use super::*;
use crate::coordinator::assignment::lam_data_manager::MockLamDataManager;
use crate::coordinator::assignment::lam_data_snapshot::LamDataSnapshot;
use crate::coordinator::leader_decider::MockLeaderDecider;
use crate::leases::MockLeaseRefresher;
use crate::metrics::NullMetricsFactory;

fn nano_provider() -> NanoTimeProvider {
    Arc::new(|| 1_000_000_000)
}

fn config() -> WorkerUtilizationAwareAssignmentConfig {
    WorkerUtilizationAwareAssignmentConfig::default()
}

fn graceful() -> GracefulLeaseHandoffConfig {
    GracefulLeaseHandoffConfig::default()
        .set_graceful_lease_handoff_timeout_millis(30_000)
        .set_graceful_lease_handoff_enabled(false)
}

fn make_manager(
    leader_decider: Arc<dyn LeaderDecider>,
    lam_data_manager: Arc<dyn LamDataManager>,
    interval_millis: i64,
) -> LeaseAssignmentManager {
    let refresher: Arc<dyn LeaseRefresher> = Arc::new(MockLeaseRefresher::new());
    LeaseAssignmentManager::new(
        refresher,
        leader_decider,
        config(),
        "workerId",
        1000,
        Arc::new(NullMetricsFactory::new()),
        nano_provider(),
        i32::MAX,
        graceful(),
        LeaseAssignmentStrategy::WorkerUtilizationAware,
        interval_millis,
        None,
        lam_data_manager,
    )
}

#[test]
fn scheduling_interval_default_and_custom() {
    // Java testLeaseAssignmentSchedulingWithDefaultInterval / WithDifferentIntervals
    // verify the interval passed to scheduleWithFixedDelay. Here it's a stored,
    // observable field.
    for interval in [2000i64, 500, 1000, 2000] {
        let mut ld = MockLeaderDecider::new();
        ld.expect_is_leader().returning(|_| true);
        let m = make_manager(Arc::new(ld), Arc::new(MockLamDataManager::new()), interval);
        assert_eq!(m.lease_assignment_interval_millis(), interval);
    }
}

#[tokio::test]
async fn not_leader_does_not_load_data() {
    let mut ld = MockLeaderDecider::new();
    ld.expect_is_leader().returning(|_| false);
    // LAM data manager must NOT be loaded when not leader.
    let mut lam = MockLamDataManager::new();
    lam.expect_load_data().never();
    let m = make_manager(Arc::new(ld), Arc::new(lam), 1000);
    m.run_once().await;
}

#[tokio::test]
async fn leader_loads_data_once_per_tick() {
    let mut ld = MockLeaderDecider::new();
    ld.expect_is_leader().returning(|_| true);
    let mut lam = MockLamDataManager::new();
    lam.expect_load_data()
        .times(1)
        .returning(|_| Ok(LamDataSnapshot::builder().build()));
    let m = make_manager(Arc::new(ld), Arc::new(lam), 1000);
    m.run_once().await;
}

#[tokio::test(start_paused = true)]
async fn background_loop_ticks_at_interval_and_stops() {
    let ticks = Arc::new(AtomicUsize::new(0));
    let mut ld = MockLeaderDecider::new();
    ld.expect_is_leader().returning(|_| false); // not leader -> cheap tick

    let ticks2 = ticks.clone();
    let mut lam = MockLamDataManager::new();
    // Not leader -> load_data never called; count ticks via is_leader side channel.
    lam.expect_load_data()
        .returning(move |_| Ok(LamDataSnapshot::builder().build()));
    let _ = &ticks2;

    // Count ticks by wrapping the leader decider is_leader.
    let counting_ld = CountingLeaderDecider {
        inner: Arc::new(ld),
        count: ticks.clone(),
    };
    let m = make_manager(Arc::new(counting_ld), Arc::new(lam), 100);

    m.start().await;
    assert!(m.is_running().await);
    // Advance ~350ms -> ~3-4 ticks.
    tokio::time::sleep(std::time::Duration::from_millis(350)).await;
    m.stop().await;
    assert!(!m.is_running().await);
    let n = ticks.load(Ordering::SeqCst);
    assert!(
        n >= 3,
        "expected at least 3 ticks in 350ms at 100ms interval, got {n}"
    );
}

struct CountingLeaderDecider {
    inner: Arc<dyn LeaderDecider>,
    count: Arc<AtomicUsize>,
}
impl LeaderDecider for CountingLeaderDecider {
    fn is_leader(&self, worker_id: &str) -> bool {
        self.count.fetch_add(1, Ordering::SeqCst);
        self.inner.is_leader(worker_id)
    }
    fn shutdown(&self) {}
    fn release_leadership_if_held(&self) {
        self.inner.release_leadership_if_held();
    }
}

#[tokio::test(start_paused = true)]
async fn panicking_tick_does_not_kill_the_loop() {
    // Java performAssignment catch(Throwable): a panicking tick is contained,
    // the schedule keeps running, and stop() still completes cleanly.
    let ticks = Arc::new(AtomicUsize::new(0));
    let mut ld = MockLeaderDecider::new();
    ld.expect_is_leader().returning(|_| true);
    // Panics accrue on the failure counter, so leadership release fires too.
    ld.expect_release_leadership_if_held().returning(|| ());
    let counting_ld = CountingLeaderDecider {
        inner: Arc::new(ld),
        count: ticks.clone(),
    };

    let mut lam = MockLamDataManager::new();
    lam.expect_load_data()
        .returning(|_| panic!("load_data boom"));

    let m = make_manager(Arc::new(counting_ld), Arc::new(lam), 100);
    m.start().await;
    assert!(m.is_running().await);
    // Advance across several ticks; each one panics inside load_data.
    tokio::time::sleep(std::time::Duration::from_millis(350)).await;
    assert!(m.is_running().await);
    let n = ticks.load(Ordering::SeqCst);
    assert!(
        n >= 3,
        "expected the loop to survive panicking ticks (>= 3 ticks in 350ms at \
         100ms interval), got {n}"
    );
    m.stop().await;
    assert!(!m.is_running().await);
}

#[tokio::test(start_paused = true)]
async fn three_consecutive_panicking_ticks_release_leadership() {
    // Java: after DEFAULT_FAILURE_COUNT_TO_SWITCH_LEADER (3) consecutive
    // failures — panics included — the leader releases leadership.
    let mut ld = MockLeaderDecider::new();
    ld.expect_is_leader().returning(|_| true);
    ld.expect_release_leadership_if_held()
        .times(1..)
        .returning(|| ());

    let mut lam = MockLamDataManager::new();
    lam.expect_load_data()
        .returning(|_| panic!("load_data boom"));

    let m = make_manager(Arc::new(ld), Arc::new(lam), 100);
    m.start().await;
    // First tick fires immediately; 450ms covers >= 4 ticks, comfortably past
    // the 3-failure threshold.
    tokio::time::sleep(std::time::Duration::from_millis(450)).await;
    m.stop().await;
}
