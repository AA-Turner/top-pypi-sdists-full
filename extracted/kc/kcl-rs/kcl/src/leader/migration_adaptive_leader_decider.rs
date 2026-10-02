//! Port of `software.amazon.kinesis.leader.MigrationAdaptiveLeaderDecider`.
//!
//! A decorator [`LeaderDecider`] holding a swappable reference to the current
//! concrete decider, so KCL can hot-swap leader-election strategy at runtime
//! (e.g. `DeterministicShuffleShardSyncLeaderDecider` ->
//! `DynamoDBLockBasedLeaderDecider` during coordinator-state table migration).
//!
//! Java's single intrinsic monitor (`synchronized` on every public method) is
//! reproduced with **one** [`std::sync::Mutex`] guarding the whole
//! read+swap+shutdown critical section (coarse, matching Java: `shutdown()`
//! cannot interleave with a concurrent `isLeader()`).
//!
//! # Deviation
//! Java throws `IllegalStateException("LeaderDecider uninitialized")` from
//! `isLeader`/`releaseLeadershipIfHeld` when uninitialized. Per the porting
//! convention (unchecked Java exception -> `panic!` with the same message), and
//! because the trait's `is_leader` returns a plain `bool`, this port
//! **panics** with the exact Java message.

use std::sync::{Arc, Mutex};

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::coordinator::leader_decider::{LeaderDecider, METRIC_OPERATION_LEADER_DECIDER};
use crate::metrics::metrics_level::MetricsLevel;
use crate::metrics::{metrics_util, MetricsFactory};

/// Java message thrown when the decider is used before `updateLeaderDecider`.
pub const UNINITIALIZED_MESSAGE: &str = "LeaderDecider uninitialized";

/// Decorator `LeaderDecider` that delegates to a swappable current decider.
pub struct MigrationAdaptiveLeaderDecider {
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    current_leader_decider: Mutex<Option<Arc<dyn LeaderDecider>>>,
}

impl MigrationAdaptiveLeaderDecider {
    /// Java `MigrationAdaptiveLeaderDecider(MetricsFactory)`.
    pub fn new(metrics_factory: Arc<dyn MetricsFactory + Send + Sync>) -> Self {
        Self {
            metrics_factory,
            current_leader_decider: Mutex::new(None),
        }
    }

    /// Java `synchronized void updateLeaderDecider(LeaderDecider)`.
    ///
    /// If a current decider exists, `shutdown()`s it before swapping (all under
    /// the lock, so `isLeader` is blocked during swap+shutdown+initialize).
    /// Then sets the new decider and unconditionally `initialize()`s it.
    pub fn update_leader_decider(&self, leader_decider: Arc<dyn LeaderDecider>) {
        let mut guard = self
            .current_leader_decider
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        if let Some(current) = guard.as_ref() {
            current.shutdown();
            tracing::info!(
                "Updating leader decider dynamically from {} to {}",
                current.metric_name(),
                leader_decider.metric_name()
            );
        } else {
            tracing::info!(
                "Initializing dynamic leader decider with {}",
                leader_decider.metric_name()
            );
        }
        leader_decider.initialize();
        *guard = Some(leader_decider);
    }

    fn publish_selected_leader_decider_metrics(&self, decider: &dyn LeaderDecider) {
        let mut scope = metrics_util::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            METRIC_OPERATION_LEADER_DECIDER,
        );
        // Java: scope.addData(String.format(decider.getClass().getSimpleName()), 1D, COUNT, DETAILED)
        scope.add_data_with_level(
            decider.metric_name(),
            1.0,
            StandardUnit::Count,
            MetricsLevel::Detailed,
        );
        metrics_util::end_scope(scope.as_mut());
    }
}

impl LeaderDecider for MigrationAdaptiveLeaderDecider {
    fn is_leader(&self, worker_id: &str) -> bool {
        let guard = self
            .current_leader_decider
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        let decider = guard
            .as_ref()
            .unwrap_or_else(|| panic!("{}", UNINITIALIZED_MESSAGE));
        self.publish_selected_leader_decider_metrics(decider.as_ref());
        decider.is_leader(worker_id)
    }

    fn shutdown(&self) {
        let mut guard = self
            .current_leader_decider
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        if let Some(current) = guard.take() {
            tracing::info!("Shutting down current {}", current.metric_name());
            current.shutdown();
        } else {
            tracing::info!("LeaderDecider has already been shutdown");
        }
    }

    fn release_leadership_if_held(&self) {
        let guard = self
            .current_leader_decider
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        let decider = guard
            .as_ref()
            .unwrap_or_else(|| panic!("{}", UNINITIALIZED_MESSAGE));
        decider.release_leadership_if_held();
    }

    fn metric_name(&self) -> &'static str {
        "MigrationAdaptiveLeaderDecider"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::coordinator::leader_decider::MockLeaderDecider;
    use crate::metrics::NullMetricsFactory;

    const TEST_RANDOM_WORKER_ID: &str = "IAmRandomWorkerId";

    fn factory() -> Arc<dyn MetricsFactory + Send + Sync> {
        Arc::new(NullMetricsFactory::new())
    }

    // A LeaderDecider mock whose metric_name is fixed (automock would otherwise
    // require an expectation for every metric_name() call).
    fn decider_returning(is_leader: bool, name: &'static str) -> MockLeaderDecider {
        let mut m = MockLeaderDecider::new();
        m.expect_metric_name().return_const(name);
        m.expect_initialize().return_const(());
        m.expect_is_leader().returning(move |_| is_leader);
        m
    }

    #[test]
    fn is_leader_kcl3x_true() {
        let d = decider_returning(true, "Kcl3x");
        let mad = MigrationAdaptiveLeaderDecider::new(factory());
        mad.update_leader_decider(Arc::new(d));
        assert!(mad.is_leader(TEST_RANDOM_WORKER_ID));
    }

    #[test]
    fn is_leader_kcl2x_true() {
        let d = decider_returning(true, "Kcl2x");
        let mad = MigrationAdaptiveLeaderDecider::new(factory());
        mad.update_leader_decider(Arc::new(d));
        assert!(mad.is_leader(TEST_RANDOM_WORKER_ID));
    }

    #[test]
    fn transition_from_kcl2x_to_kcl3x_switches_and_shuts_down_old() {
        // 2x decider: returns false, must be initialized once + shutdown once on swap.
        let mut kcl2x = MockLeaderDecider::new();
        kcl2x.expect_metric_name().return_const("Kcl2x");
        kcl2x.expect_initialize().times(1).return_const(());
        kcl2x.expect_is_leader().times(2).returning(|_| false);
        kcl2x.expect_shutdown().times(1).return_const(());

        // 3x decider: returns true, initialized once (on swap), never shutdown.
        let mut kcl3x = MockLeaderDecider::new();
        kcl3x.expect_metric_name().return_const("Kcl3x");
        kcl3x.expect_initialize().times(1).return_const(());
        kcl3x.expect_is_leader().times(2).returning(|_| true);

        let mad = MigrationAdaptiveLeaderDecider::new(factory());
        mad.update_leader_decider(Arc::new(kcl2x));

        assert!(!mad.is_leader(TEST_RANDOM_WORKER_ID));
        assert!(!mad.is_leader(TEST_RANDOM_WORKER_ID));

        mad.update_leader_decider(Arc::new(kcl3x));

        assert!(mad.is_leader(TEST_RANDOM_WORKER_ID));
        assert!(mad.is_leader(TEST_RANDOM_WORKER_ID));
    }

    #[test]
    fn release_leadership_delegates() {
        let mut d = MockLeaderDecider::new();
        d.expect_metric_name().return_const("Kcl3x");
        d.expect_initialize().return_const(());
        d.expect_release_leadership_if_held()
            .times(1)
            .return_const(());
        let mad = MigrationAdaptiveLeaderDecider::new(factory());
        mad.update_leader_decider(Arc::new(d));
        mad.release_leadership_if_held();
    }

    #[test]
    #[should_panic(expected = "LeaderDecider uninitialized")]
    fn release_leadership_uninitialized_panics() {
        let mad = MigrationAdaptiveLeaderDecider::new(factory());
        mad.release_leadership_if_held();
    }

    #[test]
    fn release_leadership_after_transition_delegates_to_new() {
        let mut kcl2x = MockLeaderDecider::new();
        kcl2x.expect_metric_name().return_const("Kcl2x");
        kcl2x.expect_initialize().return_const(());
        kcl2x.expect_shutdown().return_const(());
        // never release
        kcl2x.expect_release_leadership_if_held().times(0);

        let mut kcl3x = MockLeaderDecider::new();
        kcl3x.expect_metric_name().return_const("Kcl3x");
        kcl3x.expect_initialize().return_const(());
        kcl3x
            .expect_release_leadership_if_held()
            .times(1)
            .return_const(());

        let mad = MigrationAdaptiveLeaderDecider::new(factory());
        mad.update_leader_decider(Arc::new(kcl2x));
        mad.update_leader_decider(Arc::new(kcl3x));
        mad.release_leadership_if_held();
    }
}
