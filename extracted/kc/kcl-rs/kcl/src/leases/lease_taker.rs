//! Port of `software.amazon.kinesis.leases.LeaseTaker`.
//!
//! Strategy used by [`LeaseCoordinator`](crate::leases::LeaseCoordinator) to
//! decide which unowned/expired/stealable leases to attempt to take each cycle.
//! Each coordinator (one per worker) uses exactly one `LeaseTaker`.
//!
//! # Async
//!
//! `take_leases` is an **I/O** method (scans + conditional-writes DynamoDB) →
//! `#[async_trait]` + `async`. `get_worker_identifier` and `all_leases`
//! (in-memory / cached) stay sync default/plain methods.
//!
//! # Core taking rules (contract preserved by any impl; algorithm lives in 6c)
//!
//! 1. If a lease's counter hasn't changed in long enough (expired), try to take
//!    it.
//! 2. For a never-before-seen lease, take it only if `owner == null` (if owned,
//!    the owner is probably holding it; we can't tell until we see it more than
//!    once).
//! 3. For load balancing, rules 1 and 2 may be violated for **at most one**
//!    lease per `take_leases()` call (to allow gradual rebalancing/stealing).

use std::collections::HashMap;

use async_trait::async_trait;

use crate::leases::exceptions::LeasingError;
use crate::leases::Lease;

/// Takes new leases (and leases other workers fail to renew) for one worker.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait LeaseTaker: Send + Sync {
    /// Compute the set of takeable leases and attempt to take them, returning a
    /// map of lease key → the [`Lease`] we just successfully took (Java
    /// `takeLeases`). See the taking rules in the module docs.
    async fn take_leases(&self) -> Result<HashMap<String, Lease>, LeasingError>;

    /// The worker identifier for this taker (Java `getWorkerIdentifier`).
    fn get_worker_identifier(&self) -> String;

    /// All leases in the table (from a read or an internal cache). Java default
    /// returns an empty list.
    fn all_leases(&self) -> Vec<Lease> {
        Vec::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn mock_take_leases_and_default_all_leases() {
        let mut mock = MockLeaseTaker::new();
        mock.expect_take_leases().returning(|| Ok(HashMap::new()));
        mock.expect_get_worker_identifier()
            .returning(|| "worker-1".to_string());
        assert!(mock.take_leases().await.unwrap().is_empty());
        assert_eq!(mock.get_worker_identifier(), "worker-1");
    }
}
