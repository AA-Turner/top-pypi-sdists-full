//! Port of `software.amazon.kinesis.coordinator.LeaderDecider` (interface).
//!
//! Concrete implementations land in later waves:
//! - `DeterministicShuffleShardSyncLeaderDecider` (2.x-style) — wave 10c.
//! - `DynamoDBLockBasedLeaderDecider` / `MigrationAdaptiveLeaderDecider`
//!   (in `leader`) — wave 10c.

/// Metric operation name for the leader decider. Java
/// `LeaderDecider.METRIC_OPERATION_LEADER_DECIDER`.
pub const METRIC_OPERATION_LEADER_DECIDER: &str = "LeaderDecider";

/// Metric operation name for the `isLeader` check. Java
/// `LeaderDecider.METRIC_OPERATION_LEADER_DECIDER_IS_LEADER`.
pub const METRIC_OPERATION_LEADER_DECIDER_IS_LEADER: &str = "LeaderDecider:IsLeader";

/// SPI for pluggable leader-election strategies used to gate periodic-shard-sync
/// execution to a subset of workers. Java `LeaderDecider`.
///
/// Java's boxed `Boolean isLeader(...)` (nullable only to allow test mocks to
/// return null; production never does) is ported as a plain `bool`.
#[cfg_attr(test, mockall::automock)]
pub trait LeaderDecider: Send + Sync {
    /// Java `isLeader(String workerId)` — whether `worker_id` may execute
    /// shard-sync.
    fn is_leader(&self, worker_id: &str) -> bool;

    /// Java `shutdown()` — shut down any clients/thread-pools.
    fn shutdown(&self);

    /// Java default `initialize()` — no-op.
    fn initialize(&self) {}

    /// Java default `releaseLeadershipIfHeld()` — no-op.
    fn release_leadership_if_held(&self) {}

    /// Stable name used as the metric key by
    /// [`MigrationAdaptiveLeaderDecider`](crate::leader::MigrationAdaptiveLeaderDecider),
    /// replacing Java's `getClass().getSimpleName()` (Rust has no portable
    /// runtime type-name). Concrete impls override this.
    fn metric_name(&self) -> &'static str {
        "LeaderDecider"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn metric_constants_verbatim() {
        assert_eq!(METRIC_OPERATION_LEADER_DECIDER, "LeaderDecider");
        assert_eq!(
            METRIC_OPERATION_LEADER_DECIDER_IS_LEADER,
            "LeaderDecider:IsLeader"
        );
    }

    #[test]
    fn default_methods_are_no_ops() {
        struct Decider;
        impl LeaderDecider for Decider {
            fn is_leader(&self, worker_id: &str) -> bool {
                worker_id == "leader"
            }
            fn shutdown(&self) {}
        }
        let d = Decider;
        d.initialize();
        d.release_leadership_if_held();
        assert!(d.is_leader("leader"));
        assert!(!d.is_leader("other"));
        d.shutdown();
    }
}
