//! Port of `software.amazon.kinesis.coordinator.assignment` — coordinator
//! sub-wave 10c.
//!
//! The periodic leader-run lease-balancing subsystem: the [`LeaseAssignmentManager`]
//! orchestrator, its per-tick [`in_memory_storage_view::InMemoryStorageView`],
//! the two pluggable [`LeaseAssignmentDecider`] strategies (lease-count vs
//! worker-utilization/throughput variance), and the migration-aware
//! [`LamDataManager`] that loads + validates the lease/worker-metric data.

pub mod in_memory_storage_view;
pub mod lam_data_manager;
pub mod lam_data_snapshot;
pub mod lease_assignment_decider;
pub mod lease_assignment_manager;
pub mod lease_count_based_lease_assignment_decider;
pub mod migration_aware_lam_data_manager;
pub mod variance_based_lease_assignment_decider;

pub use in_memory_storage_view::{InMemoryStorageView, NanoTimeProvider, StorageView};
pub use lam_data_manager::LamDataManager;
pub use lam_data_snapshot::LamDataSnapshot;
pub use lease_assignment_decider::LeaseAssignmentDecider;
pub use lease_assignment_manager::LeaseAssignmentManager;
pub use lease_count_based_lease_assignment_decider::LeaseCountBasedLeaseAssignmentDecider;
pub use migration_aware_lam_data_manager::MigrationAwareLamDataManager;
pub use variance_based_lease_assignment_decider::VarianceBasedLeaseAssignmentDecider;

#[cfg(test)]
pub use in_memory_storage_view::MockStorageView;
#[cfg(test)]
pub use lam_data_manager::MockLamDataManager;
