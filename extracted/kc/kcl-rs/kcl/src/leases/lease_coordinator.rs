//! Port of `software.amazon.kinesis.leases.LeaseCoordinator`.
//!
//! Top-level per-worker facade coordinating lease taking, renewal, updates, and
//! current-assignment state; owns/starts the background
//! [`LeaseTaker`](crate::leases::LeaseTaker) +
//! [`LeaseRenewer`](crate::leases::LeaseRenewer) tasks for one worker.
//!
//! # Async vs sync split
//!
//! - **I/O** (DynamoDB / background-task control) → `async`: `initialize`,
//!   `start`, `run_lease_taker`, `run_lease_renewer`, `update_lease`, `stop`.
//! - **In-memory accessors** → sync: `is_running`, `worker_identifier`,
//!   `lease_refresher`, `get_assignments`, `get_currently_held_lease`,
//!   `stop_lease_taker`, `drop_lease`, `get_current_assignments`, `all_leases`,
//!   `lease_stats_recorder`, `get_consumer_id`.
//!
//! # Deviations
//!
//! - **`initialLeaseTableWriteCapacity` / `initialLeaseTableReadCapacity` are
//!   dropped from the trait.** In Java these return the concrete
//!   `DynamoDBLeaseCoordinator` (a builder-style API — an acknowledged
//!   abstraction leak: the trait naming its own concrete implementor). They only
//!   make sense on the concrete DynamoDB-backed struct, so they belong on
//!   `DynamoDBLeaseCoordinator` (6c/6d), not on this trait. Every other
//!   `DynamoDBLeaseCoordinator` reference in the Java signatures (e.g. the
//!   `getConsumerId` javadoc) is purely descriptive and needs no type.
//! - `leaseRefresher()` returns `Arc<dyn LeaseRefresher>` (Java returns the
//!   `LeaseRefresher` interface instance).
//! - `leaseStatsRecorder()` returns `Arc<LeaseStatsRecorder>` (the recorder is
//!   not `Clone` — it owns a `Mutex` — so it is shared via `Arc`).
//! - `getCurrentlyHeldLease` / `allLeases` nullable/empty semantics preserved
//!   (`Option` / default empty `Vec`).
//! - Checked exceptions → [`LeasingError`]; the `start`-only Java
//!   `IllegalStateException` is folded into [`LeasingError`] as well.

use std::sync::Arc;

use async_trait::async_trait;
use uuid::Uuid;

use crate::coordinator::MigrationAdaptiveLeaseAssignmentModeProvider;
use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, LeaseRefresher, LeaseStatsRecorder, ShardInfo};

/// Per-worker lease coordination facade.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait LeaseCoordinator: Send + Sync {
    /// Initialize the coordinator (create the lease table if needed).
    async fn initialize(&self) -> Result<(), LeasingError>;

    /// Start the background lease-holder and lease-taker tasks.
    ///
    /// `lease_assignment_mode_provider` decides whether to start components for
    /// both V2 and V3 functionality or only V3.
    async fn start(
        &self,
        lease_assignment_mode_provider: Arc<MigrationAdaptiveLeaseAssignmentModeProvider>,
    ) -> Result<(), LeasingError>;

    /// Run a single iteration of the lease taker (used by integration tests).
    async fn run_lease_taker(&self) -> Result<(), LeasingError>;

    /// Run a single iteration of the lease renewer (used by integration tests).
    async fn run_lease_renewer(&self) -> Result<(), LeasingError>;

    /// Whether this coordinator is running.
    fn is_running(&self) -> bool;

    /// This worker's identifier.
    fn worker_identifier(&self) -> String;

    /// The [`LeaseRefresher`] backing this coordinator.
    fn lease_refresher(&self) -> Arc<dyn LeaseRefresher>;

    /// Currently-held leases (Java `getAssignments`).
    fn get_assignments(&self) -> Vec<Lease>;

    /// A deep copy of the currently-held [`Lease`] for `lease_key`, or `None` if
    /// we don't hold it.
    fn get_currently_held_lease(&self, lease_key: &str) -> Option<Lease>;

    /// Update application-specific lease values in DynamoDB.
    ///
    /// `concurrency_token` is obtained from `Lease::concurrency_token` for a
    /// currently-held lease; `operation` labels the update for metrics;
    /// `single_stream_shard_id` is used for metrics in single-stream mode
    /// (multi-stream mode reads the shard id from the lease). Returns `true` if
    /// the update succeeded.
    async fn update_lease(
        &self,
        lease: &Lease,
        concurrency_token: Uuid,
        operation: &str,
        single_stream_shard_id: &str,
    ) -> Result<bool, LeasingError>;

    /// Request cancellation of the lease taker.
    fn stop_lease_taker(&self);

    /// Request that renewals for the given lease stop.
    fn drop_lease(&self, lease: &Lease);

    /// Stop background tasks, waiting a bounded time for them to complete before
    /// forcing shutdown.
    async fn stop(&self);

    /// Current shard/lease assignments (Java `getCurrentAssignments`).
    fn get_current_assignments(&self) -> Vec<ShardInfo>;

    /// All leases for the application in the lease table (enables external
    /// horizontal-scaling logic). Java default returns an empty list.
    fn all_leases(&self) -> Vec<Lease> {
        Vec::new()
    }

    /// The [`LeaseStatsRecorder`] for this coordinator.
    fn lease_stats_recorder(&self) -> Arc<LeaseStatsRecorder>;

    /// The consumer id of the lease table (for the DynamoDB impl, the hash of the
    /// lease-table ARN).
    fn get_consumer_id(&self) -> String;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn mock_lease_coordinator_basic() {
        let mut mock = MockLeaseCoordinator::new();
        mock.expect_is_running().returning(|| false);
        mock.expect_worker_identifier()
            .returning(|| "worker-1".to_string());
        mock.expect_get_assignments().returning(Vec::new);
        mock.expect_get_currently_held_lease().returning(|_| None);
        mock.expect_initialize().returning(|| Ok(()));

        assert!(!mock.is_running());
        assert_eq!(mock.worker_identifier(), "worker-1");
        assert!(mock.get_assignments().is_empty());
        assert!(mock.get_currently_held_lease("k").is_none());
        mock.initialize().await.unwrap();
    }
}
