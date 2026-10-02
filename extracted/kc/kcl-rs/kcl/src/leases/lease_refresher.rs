//! Port of `software.amazon.kinesis.leases.LeaseRefresher`.
//!
//! The primary CRUD + table-lifecycle abstraction over the lease persistence
//! store (DynamoDB); nearly every other lease class depends on it for
//! reading/writing lease records with optimistic-locking semantics.
//!
//! # Async
//!
//! This is an **I/O trait** (`#[async_trait]`): the Java impl blocks on
//! DynamoDB futures via `FutureUtils`; the Rust port stays async and does not
//! block. Every method is `async` and returns `Result<_, LeasingError>`.
//!
//! # Semantics to preserve (documented on each write method)
//!
//! Every write method has precise **conditional-update / mutate-caller's-object**
//! semantics that must be preserved 1:1 for correctness (optimistic locking
//! against `lease_counter` or `lease_owner`). In Rust, "mutates the passed-in
//! lease object" is expressed with `&mut Lease`.
//!
//! # Deviations
//!
//! - Checked exceptions
//!   (`DependencyException`/`InvalidStateException`/`ProvisionedThroughputException`)
//!   → `Result<_, LeasingError>`.
//! - Nullable returns (`getLease`, `getCheckpoint`) → `Option`.
//! - Java `default` methods that throw `UnsupportedOperationException` become
//!   default trait-method bodies returning [`LeasingError::dependency`] with the
//!   same message (opt-in extension points: `assign_lease`,
//!   `initiate_graceful_lease_handoff`, `update_lease_with_meta_info`,
//!   `list_leases_parallely`, `create_lease_owner_to_lease_key_index_if_not_exists`).
//!   The other `default` bodies (`list_lease_keys_for_worker`,
//!   `wait_until_lease_owner_to_lease_key_index_exists`, `get_lease_table_identifier`)
//!   preserve their non-throwing default behavior.
//! - The deprecated `createLeaseTableIfNotExists(Long, Long)` capacity overload
//!   → [`create_lease_table_if_not_exists_with_capacity`].
//! - `listLeasesParallely` returns Java `Map.Entry<List<Lease>, List<String>>`
//!   (leases + deserialization-failure keys) → a Rust `(Vec<Lease>, Vec<String>)`
//!   tuple. The `ExecutorService threadPool` parameter is dropped — parallelism
//!   in the async port is achieved with tokio tasks internally, so the
//!   thread-pool handle is not part of the trait surface; only the
//!   `parallelism_factor` is kept.
//!
//! [`create_lease_table_if_not_exists_with_capacity`]: LeaseRefresher::create_lease_table_if_not_exists_with_capacity

use async_trait::async_trait;

use crate::common::StreamIdentifier;
use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, UpdateField};
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Supports basic CRUD operations for leases.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait LeaseRefresher: Send + Sync {
    /// Deprecated capacity-specifying overload of
    /// [`create_lease_table_if_not_exists`](LeaseRefresher::create_lease_table_if_not_exists)
    /// (Java `createLeaseTableIfNotExists(Long, Long)`). Returns `true` if a new
    /// table was created.
    async fn create_lease_table_if_not_exists_with_capacity(
        &self,
        read_capacity: i64,
        write_capacity: i64,
    ) -> Result<bool, LeasingError>;

    /// Creates the lease table (PayPerRequest billing by default). Succeeds if
    /// the table already exists. Returns `true` if a new table was created.
    async fn create_lease_table_if_not_exists(&self) -> Result<bool, LeasingError>;

    /// Returns `true` if the lease table already exists.
    async fn lease_table_exists(&self) -> Result<bool, LeasingError>;

    /// Blocks (async) until the lease table exists by polling
    /// [`lease_table_exists`](LeaseRefresher::lease_table_exists). Returns `true`
    /// if the table exists, `false` if the timeout was reached.
    async fn wait_until_lease_table_exists(
        &self,
        seconds_between_polls: i64,
        timeout_seconds: i64,
    ) -> Result<bool, LeasingError>;

    /// Creates the `LeaseOwnerToLeaseKey` GSI if it doesn't exist and returns the
    /// index status (or `None`; Java default returns `null`).
    async fn create_lease_owner_to_lease_key_index_if_not_exists(
        &self,
    ) -> Result<Option<String>, LeasingError> {
        Ok(None)
    }

    /// Blocks (async) until the `LeaseOwnerToLeaseKey` GSI is ACTIVE or the
    /// timeout is reached (Java default returns `false`).
    async fn wait_until_lease_owner_to_lease_key_index_exists(
        &self,
        _seconds_between_polls: i64,
        _timeout_seconds: i64,
    ) -> bool {
        false
    }

    /// Returns `true` if the `LeaseOwner` GSI is ACTIVE.
    async fn is_lease_owner_to_lease_key_index_active(&self) -> Result<bool, LeasingError>;

    /// List all leases for a given stream.
    async fn list_leases_for_stream(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<Vec<Lease>, LeasingError>;

    /// List all lease keys owned by a given worker. Default impl filters
    /// [`list_leases`](LeaseRefresher::list_leases).
    async fn list_lease_keys_for_worker(
        &self,
        worker_identifier: &str,
    ) -> Result<Vec<String>, LeasingError> {
        let leases = self.list_leases().await?;
        Ok(leases
            .into_iter()
            .filter(|lease| lease.lease_owner() == Some(worker_identifier))
            .filter_map(|lease| lease.lease_key().map(str::to_string))
            .collect())
    }

    /// List all leases in the table.
    async fn list_leases(&self) -> Result<Vec<Lease>, LeasingError>;

    /// List all leases in parallel, returning `(leases, deserialization_failure_keys)`
    /// (Java `Map.Entry<List<Lease>, List<String>>`). If `parallelism_factor` is
    /// 0 it is computed from the table size. Default throws
    /// `UnsupportedOperationException`.
    async fn list_leases_parallely(
        &self,
        _parallelism_factor: i32,
    ) -> Result<(Vec<Lease>, Vec<String>), LeasingError> {
        Err(LeasingError::dependency(
            "listLeasesParallely is not implemented",
        ))
    }

    /// Create a new lease, conditional on a lease not already existing with this
    /// lease key. Returns `true` if created, `false` if it already exists.
    async fn create_lease_if_not_exists(&self, lease: &Lease) -> Result<bool, LeasingError>;

    /// Get the lease for `lease_key`, or `None` if it doesn't exist.
    async fn get_lease(&self, lease_key: &str) -> Result<Option<Lease>, LeasingError>;

    /// Renew a lease by incrementing its counter, conditional on the counter in
    /// DynamoDB matching the input's. **Mutates** the passed-in lease's counter
    /// after updating the record. Returns `true` if renewal succeeded.
    async fn renew_lease(&self, lease: &mut Lease) -> Result<bool, LeasingError>;

    /// Take a lease for `owner`: increment counter + set owner, conditional on
    /// the counter matching. **Mutates** the passed-in lease's counter + owner.
    /// Returns `true` if the lease was taken.
    async fn take_lease(&self, lease: &mut Lease, owner: &str) -> Result<bool, LeasingError>;

    /// Assign a lease to `new_owner`: increment counter + set owner, conditional
    /// on the **owner** in DynamoDB matching the input's owner. **Mutates** the
    /// passed-in lease's counter + owner. Default throws
    /// `UnsupportedOperationException`.
    async fn assign_lease(
        &self,
        _lease: &mut Lease,
        _new_owner: &str,
    ) -> Result<bool, LeasingError> {
        Err(LeasingError::dependency("assignLease is not implemented"))
    }

    /// Initiate a graceful handoff of `lease` to `new_owner`, giving the current
    /// owner time to finish before ownership transfers. Default throws
    /// `UnsupportedOperationException`.
    async fn initiate_graceful_lease_handoff(
        &self,
        _lease: &mut Lease,
        _new_owner: &str,
    ) -> Result<bool, LeasingError> {
        Err(LeasingError::dependency(
            "assignLeaseWithWait is not implemented",
        ))
    }

    /// Evict the current owner by setting owner to null, conditional on the owner
    /// matching. **Mutates** the passed-in lease's counter + owner. Returns
    /// `true` if eviction succeeded.
    async fn evict_lease(&self, lease: &mut Lease) -> Result<bool, LeasingError>;

    /// Delete the given lease. No-op if it doesn't exist in DynamoDB.
    async fn delete_lease(&self, lease: &Lease) -> Result<(), LeasingError>;

    /// Delete all leases (for tools/tests).
    async fn delete_all(&self) -> Result<(), LeasingError>;

    /// Update application-specific fields of `lease` (not library-managed fields),
    /// conditional on the counter matching; increments the counter. **Mutates**
    /// the passed-in lease's counter. Returns `true` if the update succeeded.
    async fn update_lease(&self, lease: &mut Lease) -> Result<bool, LeasingError>;

    /// Unconditionally update the given `update_field` of a lease (no
    /// optimistic-lock check). Default throws `UnsupportedOperationException`.
    async fn update_lease_with_meta_info(
        &self,
        _lease: &Lease,
        _update_field: UpdateField,
    ) -> Result<(), LeasingError> {
        Err(LeasingError::dependency(
            "updateLeaseWithNoExpectation is not implemented",
        ))
    }

    /// Returns `true` if there are no leases in the lease table.
    async fn is_lease_table_empty(&self) -> Result<bool, LeasingError>;

    /// Get the current checkpoint of the shard, or `None` if the shard record
    /// doesn't exist.
    async fn get_checkpoint(
        &self,
        lease_key: &str,
    ) -> Result<Option<ExtendedSequenceNumber>, LeasingError>;

    /// Get the lease-table identifier (Java default returns `""`).
    async fn get_lease_table_identifier(&self) -> Result<String, LeasingError> {
        Ok(String::new())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn mock_get_lease_returns_optional() {
        let mut mock = MockLeaseRefresher::new();
        mock.expect_get_lease()
            .withf(|k| k == "lease-1")
            .returning(|_| Ok(None));
        assert_eq!(mock.get_lease("lease-1").await.unwrap(), None);
    }

    #[tokio::test]
    async fn unsupported_defaults_return_dependency_error() {
        // A minimal impl that only supplies the required methods, exercising the
        // opt-in default extension points.
        struct Minimal;
        #[async_trait]
        impl LeaseRefresher for Minimal {
            async fn create_lease_table_if_not_exists_with_capacity(
                &self,
                _r: i64,
                _w: i64,
            ) -> Result<bool, LeasingError> {
                Ok(false)
            }
            async fn create_lease_table_if_not_exists(&self) -> Result<bool, LeasingError> {
                Ok(false)
            }
            async fn lease_table_exists(&self) -> Result<bool, LeasingError> {
                Ok(true)
            }
            async fn wait_until_lease_table_exists(
                &self,
                _p: i64,
                _t: i64,
            ) -> Result<bool, LeasingError> {
                Ok(true)
            }
            async fn is_lease_owner_to_lease_key_index_active(&self) -> Result<bool, LeasingError> {
                Ok(false)
            }
            async fn list_leases_for_stream(
                &self,
                _s: &StreamIdentifier,
            ) -> Result<Vec<Lease>, LeasingError> {
                Ok(Vec::new())
            }
            async fn list_leases(&self) -> Result<Vec<Lease>, LeasingError> {
                Ok(Vec::new())
            }
            async fn create_lease_if_not_exists(&self, _l: &Lease) -> Result<bool, LeasingError> {
                Ok(true)
            }
            async fn get_lease(&self, _k: &str) -> Result<Option<Lease>, LeasingError> {
                Ok(None)
            }
            async fn renew_lease(&self, _l: &mut Lease) -> Result<bool, LeasingError> {
                Ok(true)
            }
            async fn take_lease(&self, _l: &mut Lease, _o: &str) -> Result<bool, LeasingError> {
                Ok(true)
            }
            async fn evict_lease(&self, _l: &mut Lease) -> Result<bool, LeasingError> {
                Ok(true)
            }
            async fn delete_lease(&self, _l: &Lease) -> Result<(), LeasingError> {
                Ok(())
            }
            async fn delete_all(&self) -> Result<(), LeasingError> {
                Ok(())
            }
            async fn update_lease(&self, _l: &mut Lease) -> Result<bool, LeasingError> {
                Ok(true)
            }
            async fn is_lease_table_empty(&self) -> Result<bool, LeasingError> {
                Ok(true)
            }
            async fn get_checkpoint(
                &self,
                _k: &str,
            ) -> Result<Option<ExtendedSequenceNumber>, LeasingError> {
                Ok(None)
            }
        }

        let r = Minimal;
        // list_lease_keys_for_worker default impl filters list_leases() (empty here).
        assert!(r
            .list_lease_keys_for_worker("worker-1")
            .await
            .unwrap()
            .is_empty());
        assert!(r.assign_lease(&mut Lease::default(), "o").await.is_err());
        assert!(r.list_leases_parallely(0).await.is_err());
        assert!(
            !r.wait_until_lease_owner_to_lease_key_index_exists(1, 1)
                .await
        );
        assert_eq!(r.get_lease_table_identifier().await.unwrap(), "");
        assert_eq!(
            r.create_lease_owner_to_lease_key_index_if_not_exists()
                .await
                .unwrap(),
            None
        );
    }
}
