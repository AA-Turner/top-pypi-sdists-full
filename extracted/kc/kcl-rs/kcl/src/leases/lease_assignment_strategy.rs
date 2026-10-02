//! Port of `software.amazon.kinesis.leases.LeaseAssignmentStrategy`.
//!
//! Config-only enum selecting the lease-assignment algorithm used across the
//! worker fleet. The actual assignment algorithms live in the coordinator
//! subsystem; this selector belongs to the leases config surface
//! (`LeaseManagementConfig.leaseAssignmentStrategy`).
//!
//! Ported as a plain sync enum (no behavior). It is `Copy` + `Eq` for easy use
//! in config comparisons.

/// Selects the algorithm used to assign leases across the worker fleet.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum LeaseAssignmentStrategy {
    /// KCL v3 default: worker-utilization-aware assignment (considers CPU,
    /// memory, and throughput metrics; variance-based load balancing,
    /// dampening, gradual rebalancing, throughput-aware assignment).
    WorkerUtilizationAware,

    /// Simple lease-count balancing: distribute leases evenly across workers by
    /// count, ignoring worker-utilization metrics.
    LeaseCountBased,
}
