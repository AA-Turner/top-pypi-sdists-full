//! Port of `software.amazon.kinesis.lifecycle.ShutdownReason`.

/// Reason the `ShardRecordProcessor` is being shut down.
///
/// Distinguishes a fail-over ([`LeaseLost`](ShutdownReason::LeaseLost)) from a
/// termination ([`ShardEnd`](ShutdownReason::ShardEnd), shard closed and all
/// records delivered) from a worker-requested graceful shutdown
/// ([`Requested`](ShutdownReason::Requested)). On a fail-over the application
/// should **not** checkpoint; on termination it **should** checkpoint.
///
/// Each reason carries a numeric `rank` used to arbitrate precedence between
/// competing shutdown triggers: `LEASE_LOST(3) > SHARD_END(2) > REQUESTED(1)`.
/// Each also carries a target [`ConsumerState`] via [`shutdown_state`](ShutdownReason::shutdown_state):
/// `LEASE_LOST`/`SHARD_END → SHUTTING_DOWN`, `REQUESTED → SHUTDOWN_REQUESTED`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ShutdownReason {
    /// Processing will move to a different record processor (fail over / load
    /// balancing). Applications SHOULD NOT checkpoint.
    LeaseLost,
    /// Terminate processing (resharding): the shard is closed and all records
    /// have been delivered. Applications SHOULD checkpoint.
    ShardEnd,
    /// The entire application is shutting down; the record processor is given a
    /// final chance to checkpoint.
    Requested,
}

impl ShutdownReason {
    /// The precedence rank (`LEASE_LOST=3 > SHARD_END=2 > REQUESTED=1`).
    fn rank(self) -> i32 {
        match self {
            ShutdownReason::LeaseLost => 3,
            ShutdownReason::ShardEnd => 2,
            ShutdownReason::Requested => 1,
        }
    }

    /// Whether the given `reason` can override this reason.
    ///
    /// Java `canTransitionTo(ShutdownReason)`: `true` iff `reason.rank >
    /// this.rank` — only a strictly higher rank can overwrite a previously
    /// recorded reason (equal rank cannot re-trigger). The Java `null` argument
    /// (`false`) has no Rust analogue (the argument is non-`Option`).
    pub fn can_transition_to(self, reason: ShutdownReason) -> bool {
        reason.rank() > self.rank()
    }

    /// The [`ConsumerState`] this reason drives the consumer toward. Port of the
    /// Java enum's `state` field: `LEASE_LOST`/`SHARD_END → SHUTTING_DOWN`,
    /// `REQUESTED → SHUTDOWN_REQUESTED` (the `ShutdownNotificationState`).
    pub fn shutdown_state(self) -> crate::lifecycle::ConsumerState {
        match self {
            ShutdownReason::LeaseLost | ShutdownReason::ShardEnd => {
                crate::lifecycle::ConsumerState::ShuttingDown
            }
            ShutdownReason::Requested => crate::lifecycle::ConsumerState::ShutdownNotification,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Port of ShutdownReasonTest.

    #[test]
    fn transition_zombie() {
        assert!(!ShutdownReason::LeaseLost.can_transition_to(ShutdownReason::ShardEnd));
        assert!(!ShutdownReason::LeaseLost.can_transition_to(ShutdownReason::Requested));
    }

    #[test]
    fn transition_terminate() {
        assert!(ShutdownReason::ShardEnd.can_transition_to(ShutdownReason::LeaseLost));
        assert!(!ShutdownReason::ShardEnd.can_transition_to(ShutdownReason::Requested));
    }

    #[test]
    fn transition_requested() {
        assert!(ShutdownReason::Requested.can_transition_to(ShutdownReason::LeaseLost));
        assert!(ShutdownReason::Requested.can_transition_to(ShutdownReason::ShardEnd));
    }
}
