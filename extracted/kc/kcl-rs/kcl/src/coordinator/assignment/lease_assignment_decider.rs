//! Port of `software.amazon.kinesis.coordinator.assignment.LeaseAssignmentDecider`.
//!
//! Strategy interface for the two pluggable lease-balancing algorithms used by
//! [`LeaseAssignmentManager`](super::LeaseAssignmentManager).

use crate::leases::Lease;

/// The pluggable lease-balancing strategy. Java `LeaseAssignmentDecider`.
pub trait LeaseAssignmentDecider {
    /// Java `assignExpiredOrUnassignedLeases(List<Lease>)`.
    ///
    /// **Mutate-in-place contract preserved:** implementations *remove* the
    /// leases they successfully assigned from the passed `Vec`, leaving only the
    /// unassigned leases visible to the caller (LAM inspects `is_empty()`
    /// afterward for the `LeaseSpillover` metric).
    fn assign_expired_or_unassigned_leases(
        &mut self,
        expired_or_unassigned_leases: &mut Vec<Lease>,
    );

    /// Java `balanceWorkerVariance()`: rebalance leases between workers.
    fn balance_worker_variance(&mut self);
}
