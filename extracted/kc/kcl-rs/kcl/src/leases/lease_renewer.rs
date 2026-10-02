//! Port of `software.amazon.kinesis.leases.LeaseRenewer`.
//!
//! Strategy used by [`LeaseCoordinator`](crate::leases::LeaseCoordinator) to
//! periodically renew (heartbeat) all currently-held leases and to apply
//! application-specific updates against the held set. Each coordinator (one per
//! worker) uses exactly one `LeaseRenewer`.
//!
//! # Async vs sync split
//!
//! - `initialize`, `renew_leases`, `update_lease` are **I/O** (DynamoDB) →
//!   `async`.
//! - `get_currently_held_leases`, `get_currently_held_lease`,
//!   `add_leases_to_renew`, `clear_currently_held_leases`, `drop_lease` operate
//!   on the in-memory held-lease set → **sync**.
//!
//! # Concurrency-token guard on `update_lease`
//!
//! `update_lease` fails if the `concurrency_token` doesn't match the internal
//! authoritative copy (i.e. we lost and re-acquired the lease since the caller
//! obtained its reference). The `concurrency_token` is intentionally excluded
//! from [`Lease`] value-equality yet is the **critical** update-safety guard —
//! value equality must not be conflated with this identity/ownership-epoch check.

use std::collections::HashMap;

use async_trait::async_trait;
use uuid::Uuid;

use crate::leases::exceptions::LeasingError;
use crate::leases::Lease;

/// Renews leases held by one worker's [`LeaseCoordinator`](crate::leases::LeaseCoordinator).
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait LeaseRenewer: Send + Sync {
    /// Bootstrap the initial set of held leases from the
    /// [`LeaseRefresher`](crate::leases::LeaseRefresher) (e.g. on process
    /// restart, pick up leases we own).
    async fn initialize(&self) -> Result<(), LeasingError>;

    /// Attempt to renew all currently-held leases (Java `renewLeases`).
    async fn renew_leases(&self) -> Result<(), LeasingError>;

    /// Currently-held leases (lease key → deep-copied [`Lease`]; a lease is held
    /// if we renewed it on the last `renew_leases()` run). The returned copies'
    /// counters will not tick.
    fn get_currently_held_leases(&self) -> HashMap<String, Lease>;

    /// A deep copy of a currently-held lease for `lease_key`, or `None` if not
    /// held.
    fn get_currently_held_lease(&self, lease_key: &str) -> Option<Lease>;

    /// Add leases to the held set. Each must already have
    /// `last_counter_increment_nanos` set to the last time its counter was
    /// incremented.
    fn add_leases_to_renew(&self, new_leases: Vec<Lease>);

    /// Clear the held-lease set.
    fn clear_currently_held_leases(&self);

    /// Stop maintaining (renewing) the given lease.
    fn drop_lease(&self, lease: &Lease);

    /// Update application-specific fields in a currently-held lease. Fails if we
    /// don't hold the lease, or if `concurrency_token` doesn't match the internal
    /// authoritative copy. Returns `true` if the update succeeded.
    async fn update_lease(
        &self,
        lease: &Lease,
        concurrency_token: Uuid,
        operation: &str,
        single_stream_shard_id: &str,
    ) -> Result<bool, LeasingError>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn mock_renewer_sync_and_async_methods() {
        let mut mock = MockLeaseRenewer::new();
        mock.expect_initialize().returning(|| Ok(()));
        mock.expect_get_currently_held_leases()
            .returning(HashMap::new);
        mock.expect_get_currently_held_lease().returning(|_| None);

        mock.initialize().await.unwrap();
        assert!(mock.get_currently_held_leases().is_empty());
        assert!(mock.get_currently_held_lease("k").is_none());
    }
}
