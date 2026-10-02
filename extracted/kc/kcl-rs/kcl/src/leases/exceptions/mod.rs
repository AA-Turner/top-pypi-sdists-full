//! Port of `software.amazon.kinesis.leases.exceptions`.
//!
//! The Java `LeasingException` hierarchy (`DependencyException`,
//! `InvalidStateException`, `ProvisionedThroughputException`) is flattened into
//! a single [`LeasingError`] enum. `CustomerApplicationException` is a separate
//! [`CustomerApplicationError`] type (kept distinct so callers can tell a
//! customer bug from an infra failure). The package also (oddly) contains the
//! [`LeasePendingDeletion`] value type — a plain DTO, not an exception — and the
//! deprecated `ShardSyncer` shim (a doc-only stub for now; see `shard_syncer`).

pub mod customer_application_error;
pub mod lease_pending_deletion;
pub mod leasing_error;
pub mod shard_syncer;

pub use customer_application_error::CustomerApplicationError;
pub use lease_pending_deletion::LeasePendingDeletion;
pub use leasing_error::LeasingError;
