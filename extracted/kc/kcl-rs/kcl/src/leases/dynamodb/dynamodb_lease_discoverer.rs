//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBLeaseDiscoverer`.
//!
//! Implements [`LeaseDiscoverer`]: finds leases newly assigned to this worker
//! (via the `LeaseOwnerToLeaseKeyIndex` GSI) that the [`LeaseRenewer`] doesn't
//! yet track, fetches/validates them, and returns them for enrollment.
//!
//! # Concurrency
//!
//! Java fans out per-lease `getLease` calls on an `ExecutorService` via
//! `CompletableFuture.supplyAsync(...).join()`. The Rust port uses
//! [`futures::future::join_all`] over per-lease async tasks, preserving the
//! key property that **each per-lease fetch failure is isolated** (caught and
//! turned into `None`) so one bad lease doesn't fail the whole discovery pass.
//!
//! # Validation (`fetch_lease`)
//!
//! Returns `None` when: the lease doesn't exist; its owner != this worker (GSI
//! is eventually consistent → `OwnerMismatch`); or `checkpoint_owner` is set
//! (mid graceful-handoff — not ready for the renewer). Otherwise stamps
//! `last_counter_increment_nanos` = "now" and returns it.

use std::sync::Arc;

use async_trait::async_trait;

use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, LeaseDiscoverer, LeaseRefresher, LeaseRenewer};
use crate::metrics::MetricsFactory;

/// DynamoDB implementation of [`LeaseDiscoverer`].
pub struct DynamoDBLeaseDiscoverer {
    lease_refresher: Arc<dyn LeaseRefresher>,
    lease_renewer: Arc<dyn LeaseRenewer>,
    #[allow(dead_code)]
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    worker_identifier: String,
}

impl DynamoDBLeaseDiscoverer {
    /// Construct a discoverer (Java `@RequiredArgsConstructor`). The Java
    /// `ExecutorService` is dropped — parallelism is achieved with `join_all`.
    pub fn new(
        lease_refresher: Arc<dyn LeaseRefresher>,
        lease_renewer: Arc<dyn LeaseRenewer>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        worker_identifier: impl Into<String>,
    ) -> Self {
        Self {
            lease_refresher,
            lease_renewer,
            metrics_factory,
            worker_identifier: worker_identifier.into(),
        }
    }

    /// Java `fetchLease(leaseKey)` — per-lease validation, exceptions swallowed.
    async fn fetch_lease(&self, lease_key: &str) -> Option<Lease> {
        match self.lease_refresher.get_lease(lease_key).await {
            Ok(None) => None,
            Ok(Some(mut lease)) => {
                // GSI is eventually consistent: verify ownership.
                if lease.lease_owner() != Some(self.worker_identifier.as_str()) {
                    return None; // OwnerMismatch
                }
                // Mid graceful-handoff: not ready for the renewer yet.
                if lease.checkpoint_owner().is_some() {
                    return None;
                }
                // Mark "just discovered" so it isn't immediately treated as expired.
                lease.set_last_counter_increment_nanos(Some(now_nanos()));
                Some(lease)
            }
            Err(_e) => {
                // GetLease:Error — swallow so one bad lease doesn't fail the pass.
                None
            }
        }
    }
}

fn now_nanos() -> i64 {
    // Java System.nanoTime(): the process-wide monotonic clock. The stamp set
    // here is compared against the renewer's clock readings, so it must share
    // that epoch.
    crate::utils::monotonic_clock::monotonic_nanos()
}

#[async_trait]
impl LeaseDiscoverer for DynamoDBLeaseDiscoverer {
    async fn discover_new_leases(&self) -> Result<Vec<Lease>, LeasingError> {
        let current_held_lease_keys = self.lease_renewer.get_currently_held_leases();
        let lease_keys = self
            .lease_refresher
            .list_lease_keys_for_worker(&self.worker_identifier)
            .await?;

        let new_lease_keys: Vec<String> = lease_keys
            .into_iter()
            .filter(|k| !current_held_lease_keys.contains_key(k))
            .collect();

        // Fan out per-lease fetches; each failure is isolated to None.
        let futures = new_lease_keys
            .iter()
            .map(|k| self.fetch_lease(k))
            .collect::<Vec<_>>();
        let results = futures::future::join_all(futures).await;
        let new_leases: Vec<Lease> = results.into_iter().flatten().collect();
        Ok(new_leases)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::lease_renewer::MockLeaseRenewer;
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::kpl::ExtendedSequenceNumber;
    use std::collections::HashMap;

    const WORKER: &str = "TestWorkerIdentifier";

    fn lease_owned_by(key: &str, owner: &str) -> Lease {
        let mut lease = Lease::default();
        lease.set_lease_key(key);
        lease.set_lease_owner(Some(owner.to_string()));
        lease.set_lease_counter(13);
        lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number("123"));
        lease
    }

    fn discoverer(
        refresher: MockLeaseRefresher,
        renewer: MockLeaseRenewer,
    ) -> DynamoDBLeaseDiscoverer {
        DynamoDBLeaseDiscoverer::new(
            Arc::new(refresher),
            Arc::new(renewer),
            Arc::new(NullMetricsFactory::new()),
            WORKER,
        )
    }

    #[tokio::test]
    async fn happy_case_returns_only_untracked_leases() {
        let mut renewer = MockLeaseRenewer::new();
        renewer.expect_get_currently_held_leases().returning(|| {
            let mut m = HashMap::new();
            // lease-1 and lease-2 are already held.
            m.insert("lease-1".to_string(), lease_owned_by("lease-1", WORKER));
            m.insert("lease-2".to_string(), lease_owned_by("lease-2", WORKER));
            m
        });

        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_list_lease_keys_for_worker()
            .returning(|_| {
                Ok(vec![
                    "lease-1".to_string(),
                    "lease-2".to_string(),
                    "lease-3".to_string(),
                    "lease-4".to_string(),
                ])
            });
        refresher
            .expect_get_lease()
            .returning(|k| Ok(Some(lease_owned_by(k, WORKER))));

        let d = discoverer(refresher, renewer);
        let mut response = d.discover_new_leases().await.unwrap();
        response.sort_by(|a, b| a.lease_key().cmp(&b.lease_key()));
        let keys: Vec<&str> = response.iter().filter_map(|l| l.lease_key()).collect();
        assert_eq!(keys, vec!["lease-3", "lease-4"]);
    }

    #[tokio::test]
    async fn no_leases_in_renewer_returns_all() {
        let mut renewer = MockLeaseRenewer::new();
        renewer
            .expect_get_currently_held_leases()
            .returning(HashMap::new);
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_list_lease_keys_for_worker()
            .returning(|_| Ok(vec!["lease-3".to_string(), "lease-4".to_string()]));
        refresher
            .expect_get_lease()
            .returning(|k| Ok(Some(lease_owned_by(k, WORKER))));
        let d = discoverer(refresher, renewer);
        assert_eq!(d.discover_new_leases().await.unwrap().len(), 2);
    }

    #[tokio::test]
    async fn refresher_throws_returns_empty() {
        let mut renewer = MockLeaseRenewer::new();
        renewer
            .expect_get_currently_held_leases()
            .returning(HashMap::new);
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_list_lease_keys_for_worker()
            .returning(|_| Ok(vec!["lease-3".to_string()]));
        refresher
            .expect_get_lease()
            .returning(|_| Err(LeasingError::dependency("boom")));
        let d = discoverer(refresher, renewer);
        assert_eq!(d.discover_new_leases().await.unwrap().len(), 0);
    }

    #[tokio::test]
    async fn inconsistent_gsi_owner_mismatch_filtered() {
        let mut renewer = MockLeaseRenewer::new();
        renewer
            .expect_get_currently_held_leases()
            .returning(HashMap::new);
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_list_lease_keys_for_worker()
            .returning(|_| {
                Ok(vec![
                    "ownerMatchingKey".to_string(),
                    "ownerNotMatchingKey".to_string(),
                ])
            });
        refresher.expect_get_lease().returning(|k| {
            if k == "ownerMatchingKey" {
                Ok(Some(lease_owned_by(k, WORKER)))
            } else {
                Ok(Some(lease_owned_by(k, "RandomOwner")))
            }
        });
        let d = discoverer(refresher, renewer);
        assert_eq!(d.discover_new_leases().await.unwrap().len(), 1);
    }

    #[tokio::test]
    async fn ignore_pending_checkpoint_leases() {
        let mut renewer = MockLeaseRenewer::new();
        renewer
            .expect_get_currently_held_leases()
            .returning(HashMap::new);
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_list_lease_keys_for_worker()
            .returning(|_| {
                Ok(vec![
                    "lease-3".to_string(),
                    "lease-4".to_string(),
                    "pendingCheckpointLease".to_string(),
                ])
            });
        refresher.expect_get_lease().returning(|k| {
            let mut lease = lease_owned_by(k, WORKER);
            if k == "pendingCheckpointLease" {
                lease.set_checkpoint_owner(Some("other_worker".to_string()));
            }
            Ok(Some(lease))
        });
        let d = discoverer(refresher, renewer);
        assert_eq!(d.discover_new_leases().await.unwrap().len(), 2);
    }
}
