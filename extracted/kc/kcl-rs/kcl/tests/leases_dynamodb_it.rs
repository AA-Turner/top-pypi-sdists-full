//! Integration tests for the DynamoDB leasing layer — ports of the Java
//! `leases/dynamodb/*IntegrationTest.java` files that run against real AWS.
//!
//! These validate the real conditional-write (optimistic-concurrency) semantics
//! that the unit-test mocks cannot: create-if-not-exists, take/renew/evict
//! counter transitions, conditional-write failures (stale counter / owner /
//! concurrency token), graceful handoff, non-greedy + steal lease selection,
//! billing-mode PayPerRequest table creation, and list/scan/paging.
//!
//! Every test is `#[ignore]` (see the module doc in `common/mod.rs`). Run with:
//! `cargo test -p kcl -- --ignored` (optionally `AWS_ENDPOINT_URL=...` to
//! redirect to LocalStack).

mod common;

use std::collections::HashMap;
use std::collections::HashSet;
use std::sync::Arc;
use std::time::Duration;

use aws_sdk_dynamodb::types::BillingMode;

use kcl::common::HashKeyRangeForLease;
use kcl::leases::dynamodb::{DynamoDBLeaseRenewer, DynamoDBLeaseTaker};
use kcl::leases::{
    Lease, LeaseRefresher, LeaseRenewer, LeaseStatsRecorder, LeaseTaker, UpdateField,
};
use kcl::metrics::NullMetricsFactory;
use kcl::retrieval::kpl::ExtendedSequenceNumber;

use common::{
    build_pay_per_request_refresher, dynamodb_client, harness_lease, unique_table_name,
    LeaseTableGuard, VirtualClock,
};

const IGNORE_MSG: &str =
    "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack";

// ===========================================================================
// Test-side TestHarnessBuilder (ports `TestHarnessBuilder` from the Java tests)
// ===========================================================================
//
// Mirrors the Java `dynamodb/TestHarnessBuilder`: builds leases via the harness
// `createLease`, writes them with `createLeaseIfNotExists`, tracks a virtual
// clock, and provides the `takeMutateAssert` / `stealMutateAssert` /
// `addLeasesToRenew` / `renewMutateAssert` / `renewAllLeases` assertion helpers.

struct TestHarnessBuilder {
    refresher: Arc<dyn LeaseRefresher>,
    leases: HashMap<String, Lease>,
    original_leases: HashMap<String, Lease>,
    clock: VirtualClock,
}

impl TestHarnessBuilder {
    fn new(refresher: Arc<dyn LeaseRefresher>) -> Self {
        Self {
            refresher,
            leases: HashMap::new(),
            original_leases: HashMap::new(),
            clock: VirtualClock::new(),
        }
    }

    /// `withLease(shardId)` — default owner "leaseOwner".
    fn with_lease_default_owner(&mut self, shard_id: &str) -> &mut Self {
        self.with_lease(shard_id, Some("leaseOwner"))
    }

    /// `withLease(shardId, owner)`.
    fn with_lease(&mut self, shard_id: &str, owner: Option<&str>) -> &mut Self {
        self.leases
            .insert(shard_id.to_string(), harness_lease(shard_id, owner));
        self.original_leases
            .insert(shard_id.to_string(), harness_lease(shard_id, owner));
        self
    }

    /// `build()` — write leases; for owned leases set lastCounterIncrementNanos;
    /// then snapshot the current (virtual) time. Returns the built leases map.
    async fn build(&mut self) -> HashMap<String, Lease> {
        for lease in self.leases.values_mut() {
            self.refresher
                .create_lease_if_not_exists(lease)
                .await
                .expect("create_lease_if_not_exists failed");
            if lease.lease_owner().is_some() {
                lease.set_last_counter_increment_nanos(Some(self.clock.now_nanos()));
            }
        }
        self.leases.clone()
    }

    /// `passTime(millis)`.
    fn pass_time(&self, millis: i64) {
        self.clock.pass_time_millis(millis);
    }

    /// `takeMutateAssert(taker, numToTake)` — assert exactly `num` taken, and
    /// each taken lease matches the original after the take mutation.
    async fn take_mutate_assert_count(&mut self, taker: &DynamoDBLeaseTaker, num_to_take: usize) {
        let result = taker.take_leases().await.expect("take_leases failed");
        assert_eq!(
            num_to_take,
            result.len(),
            "unexpected number of leases taken"
        );
        let worker = taker.get_worker_identifier();
        for actual in result.values() {
            let key = actual.lease_key().unwrap().to_string();
            let original = self
                .leases
                .get_mut(&key)
                .unwrap_or_else(|| panic!("no original lease for {key}"))
                .clone();
            Self::mutate_assert(&worker, original, actual, &mut self.leases);
        }
    }

    /// `takeMutateAssert(taker, shardIds...)`.
    async fn take_mutate_assert_ids(
        &mut self,
        taker: &DynamoDBLeaseTaker,
        taken_shard_ids: &[&str],
    ) -> HashMap<String, Lease> {
        let result = taker.take_leases().await.expect("take_leases failed");
        assert_eq!(
            taken_shard_ids.len(),
            result.len(),
            "unexpected number of leases taken"
        );
        let worker = taker.get_worker_identifier();
        for shard_id in taken_shard_ids {
            let original = self
                .leases
                .get(*shard_id)
                .unwrap_or_else(|| panic!("no original lease for {shard_id}"))
                .clone();
            let actual = result
                .get(*shard_id)
                .unwrap_or_else(|| panic!("expected {shard_id} to be taken"));
            Self::mutate_assert(&worker, original, actual, &mut self.leases);
        }
        result
    }

    /// `stealMutateAssert(taker, numToTake)`.
    async fn steal_mutate_assert(
        &mut self,
        taker: &DynamoDBLeaseTaker,
        num_to_take: usize,
    ) -> HashMap<String, Lease> {
        let result = taker.take_leases().await.expect("take_leases failed");
        assert_eq!(
            num_to_take,
            result.len(),
            "unexpected number of leases stolen"
        );
        let worker = taker.get_worker_identifier();
        for actual in result.values() {
            let key = actual.lease_key().unwrap().to_string();
            let mut original = self
                .leases
                .get(&key)
                .unwrap_or_else(|| panic!("no original lease for {key}"))
                .clone();
            // Java: original.isMarkedForLeaseSteal(true).lastCounterIncrementNanos(actual...)
            original.set_marked_for_lease_steal(true);
            original.set_last_counter_increment_nanos(actual.last_counter_increment_nanos());
            Self::mutate_assert(&worker, original, actual, &mut self.leases);
        }
        result
    }

    /// The Java `mutateAssert`: bump the original's counter, bump
    /// ownerSwitchesSinceCheckpoint when the owner changed to a new worker, set
    /// the new owner, then assert the mutated original equals `actual`. Also
    /// stores the mutated original back so successive scans compound correctly.
    fn mutate_assert(
        new_worker: &str,
        mut original: Lease,
        actual: &Lease,
        leases: &mut HashMap<String, Lease>,
    ) {
        original.set_lease_counter(original.lease_counter() + 1);
        if let Some(owner) = original.lease_owner() {
            if owner != new_worker {
                original.set_owner_switches_since_checkpoint(
                    original.owner_switches_since_checkpoint() + 1,
                );
            }
        }
        original.set_lease_owner(Some(new_worker.to_string()));
        assert_eq!(
            original, *actual,
            "taken lease did not match expected mutation"
        );
        leases.insert(original.lease_key().unwrap().to_string(), original);
    }

    /// `addLeasesToRenew(renewer, shardIds...)`.
    fn add_leases_to_renew(&self, renewer: &DynamoDBLeaseRenewer, shard_ids: &[&str]) {
        let to_renew: Vec<Lease> = shard_ids
            .iter()
            .map(|id| {
                self.leases
                    .get(*id)
                    .unwrap_or_else(|| panic!("no lease for {id}"))
                    .clone()
            })
            .collect();
        renewer.add_leases_to_renew(to_renew);
    }

    /// `renewMutateAssert(renewer, shardIds...)`.
    async fn renew_mutate_assert(
        &mut self,
        renewer: &DynamoDBLeaseRenewer,
        renewed_shard_ids: &[&str],
    ) -> HashMap<String, Lease> {
        renewer.renew_leases().await.expect("renew_leases failed");
        let held = renewer.get_currently_held_leases();
        assert_eq!(
            renewed_shard_ids.len(),
            held.len(),
            "unexpected number of held leases after renewal"
        );
        for shard_id in renewed_shard_ids {
            let original = self
                .original_leases
                .get_mut(*shard_id)
                .unwrap_or_else(|| panic!("no original lease for {shard_id}"));
            original.set_lease_counter(original.lease_counter() + 1);
            let actual = held
                .get(*shard_id)
                .unwrap_or_else(|| panic!("expected {shard_id} to be held"));
            assert_eq!(*original, *actual, "renewed lease did not match expected");
        }
        held
    }

    /// `renewAllLeases()`.
    async fn renew_all_leases(&mut self) {
        for lease in self.leases.values_mut() {
            self.refresher
                .renew_lease(lease)
                .await
                .expect("renew_lease failed");
        }
    }
}

// ===========================================================================
// FILE 1: DynamoDBLeaseRefresherIntegrationTest
// ===========================================================================

/// testListNoRecords
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_list_no_records() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("list-no-records"),
        BillingMode::PayPerRequest,
    )
    .await;

    let leases = guard.refresher.list_leases().await.expect("list_leases");
    assert!(leases.is_empty());

    guard.teardown().await;
}

/// testListWithRecords — exercises Dynamo paging.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_list_with_records() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("list-with-records"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    for i in 0..10 {
        builder.with_lease_default_owner(&i.to_string());
    }
    let mut expected = builder.build().await;

    // list_leases pages internally; assert every built lease appears once.
    let actual = guard.refresher.list_leases().await.expect("list_leases");
    for lease in actual {
        let key = lease.lease_key().unwrap().to_string();
        let removed = expected.remove(&key);
        assert!(removed.is_some(), "unexpected lease {key}");
        assert_eq!(removed.unwrap(), lease);
    }
    assert!(expected.is_empty(), "not all leases were listed");

    guard.teardown().await;
}

/// testGetLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_get_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("get-lease"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let expected = builder.build().await.remove("1").unwrap();

    let actual = guard
        .refresher
        .get_lease(expected.lease_key().unwrap())
        .await
        .expect("get_lease")
        .expect("lease should exist");
    assert_eq!(expected, actual);

    guard.teardown().await;
}

/// testGetNull
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_get_null() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("get-null"),
        BillingMode::PayPerRequest,
    )
    .await;

    let actual = guard
        .refresher
        .get_lease("bogusShardId")
        .await
        .expect("get_lease");
    assert!(actual.is_none());

    guard.teardown().await;
}

/// testDeleteLeaseThenUpdateLeaseWithMetaInfo
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_delete_lease_then_update_lease_with_meta_info() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("del-then-meta"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let lease = builder.build().await.remove("1").unwrap();
    let lease_key = lease.lease_key().unwrap().to_string();

    guard
        .refresher
        .delete_lease(&lease)
        .await
        .expect("delete_lease");
    guard
        .refresher
        .update_lease_with_meta_info(&lease, UpdateField::HashKeyRange)
        .await
        .expect("update_lease_with_meta_info");
    let deleted = guard
        .refresher
        .get_lease(&lease_key)
        .await
        .expect("get_lease");
    assert!(deleted.is_none(), "delete should persist");

    guard.teardown().await;
}

/// testUpdateLeaseWithMetaInfo
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_update_lease_with_meta_info() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("meta"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let mut lease = builder.build().await.remove("1").unwrap();
    let lease_key = lease.lease_key().unwrap().to_string();

    let hkr = HashKeyRangeForLease::new(num_bigint::BigInt::from(1), num_bigint::BigInt::from(2));
    lease.set_hash_key_range(hkr);
    guard
        .refresher
        .update_lease_with_meta_info(&lease, UpdateField::HashKeyRange)
        .await
        .expect("update_lease_with_meta_info");
    let updated = guard
        .refresher
        .get_lease(&lease_key)
        .await
        .expect("get_lease")
        .expect("lease exists");
    assert_eq!(lease, updated);

    guard.teardown().await;
}

/// testRenewLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renew_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("renew"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let mut lease = builder.build().await.remove("1").unwrap();
    let original_counter = lease.lease_counter();

    assert!(guard
        .refresher
        .renew_lease(&mut lease)
        .await
        .expect("renew_lease"));
    assert_eq!(original_counter + 1, lease.lease_counter());

    let from_dynamo = guard
        .refresher
        .get_lease(lease.lease_key().unwrap())
        .await
        .expect("get_lease")
        .expect("lease exists");
    assert_eq!(lease, from_dynamo);

    guard.teardown().await;
}

/// testHoldUpdatedLease — renew with a stale copy fails (counter mismatch).
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_hold_updated_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("hold-updated"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let mut lease = builder.build().await.remove("1").unwrap();

    let mut lease_copy = guard
        .refresher
        .get_lease(lease.lease_key().unwrap())
        .await
        .expect("get_lease")
        .expect("lease exists");

    // lose lease
    guard
        .refresher
        .take_lease(&mut lease, "bar")
        .await
        .expect("take_lease");

    assert!(!guard
        .refresher
        .renew_lease(&mut lease_copy)
        .await
        .expect("renew_lease"));

    guard.teardown().await;
}

/// testTakeUnownedLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_take_unowned_lease() {
    common::init_test_tracing();
    take_lease_helper(false).await;
}

/// testTakeOwnedLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_take_owned_lease() {
    common::init_test_tracing();
    take_lease_helper(true).await;
}

async fn take_lease_helper(owned: bool) {
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name(if owned { "take-owned" } else { "take-unowned" }),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", if owned { Some("originalOwner") } else { None });
    let mut lease = builder.build().await.remove("1").unwrap();
    let original_counter = lease.lease_counter();

    let new_owner = "newOwner";
    assert!(guard
        .refresher
        .take_lease(&mut lease, new_owner)
        .await
        .expect("take_lease"));
    assert_eq!(original_counter + 1, lease.lease_counter());
    assert_eq!(
        if owned { 1 } else { 0 },
        lease.owner_switches_since_checkpoint()
    );
    assert_eq!(Some(new_owner), lease.lease_owner());

    let from_dynamo = guard
        .refresher
        .get_lease(lease.lease_key().unwrap())
        .await
        .expect("get_lease")
        .expect("lease exists");
    assert_eq!(lease, from_dynamo);

    guard.teardown().await;
}

/// testTakeUpdatedLease — take with a stale copy fails.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_take_updated_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("take-updated"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let mut lease = builder.build().await.remove("1").unwrap();

    let mut lease_copy = guard
        .refresher
        .get_lease(lease.lease_key().unwrap())
        .await
        .expect("get_lease")
        .expect("lease exists");

    let new_owner = "newOwner";
    guard
        .refresher
        .take_lease(&mut lease, new_owner)
        .await
        .expect("take_lease");

    assert!(!guard
        .refresher
        .take_lease(&mut lease_copy, new_owner)
        .await
        .expect("take_lease"));

    guard.teardown().await;
}

/// testEvictUnownedLease — the Java method exists but carries **no `@Test`
/// annotation** and asserts the stale KCLv2 semantics (`assertFalse`). Since
/// the v3 graceful-handoff rework, `evictLease` conditions on "owner fields
/// match" via `getDynamoLeaseOwnerExpectation`, and for an unowned lease
/// (owner `null` → `exists(false)` expectation) that condition trivially
/// holds — the evict succeeds and returns **true** (presumably why AWS
/// un-annotated the test instead of updating it). This port pins the actual
/// v3 behavior.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_evict_unowned_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("evict-unowned"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", None);
    let mut lease = builder.build().await.remove("1").unwrap();
    let original_counter = lease.lease_counter();

    assert!(guard
        .refresher
        .evict_lease(&mut lease)
        .await
        .expect("evict_lease"));
    assert_eq!(lease.lease_owner(), None);
    assert_eq!(lease.lease_counter(), original_counter + 1);

    guard.teardown().await;
}

/// testEvictOwnedLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_evict_owned_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("evict-owned"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let mut lease = builder.build().await.remove("1").unwrap();
    let original_counter = lease.lease_counter();

    assert!(guard
        .refresher
        .evict_lease(&mut lease)
        .await
        .expect("evict_lease"));
    assert_eq!(None, lease.lease_owner());
    assert_eq!(original_counter + 1, lease.lease_counter());

    let from_dynamo = guard
        .refresher
        .get_lease(lease.lease_key().unwrap())
        .await
        .expect("get_lease")
        .expect("lease exists");
    assert_eq!(lease, from_dynamo);

    guard.teardown().await;
}

/// testEvictChangedLease — evict is conditional on OWNER (not counter).
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_evict_changed_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("evict-changed"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let mut lease = builder.build().await.remove("1").unwrap();

    // Change owner only — optimistic lock (on owner) should fail.
    lease.set_lease_owner(Some("otherOwner".to_string()));
    assert!(!guard
        .refresher
        .evict_lease(&mut lease)
        .await
        .expect("evict_lease"));

    guard.teardown().await;
}

/// testDeleteLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_delete_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("delete"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let lease = builder.build().await.remove("1").unwrap();

    guard
        .refresher
        .delete_lease(&lease)
        .await
        .expect("delete_lease");

    let new_lease = guard
        .refresher
        .get_lease(lease.lease_key().unwrap())
        .await
        .expect("get_lease");
    assert!(new_lease.is_none());

    guard.teardown().await;
}

/// testUpdateLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_update_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("update"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease_default_owner("1");
    let lease = builder.build().await.remove("1").unwrap();
    let mut updated_lease = lease.copy();
    updated_lease.set_child_shard_ids(["updatedChildShardId".to_string()]);

    guard
        .refresher
        .update_lease(&mut updated_lease)
        .await
        .expect("update_lease");
    let new_lease = guard
        .refresher
        .get_lease(lease.lease_key().unwrap())
        .await
        .expect("get_lease")
        .expect("lease exists");
    let expected: HashSet<String> = ["updatedChildShardId".to_string()].into_iter().collect();
    assert_eq!(expected, new_lease.child_shard_ids());

    guard.teardown().await;
}

/// testDeleteNonexistentLease — delete of a never-written lease succeeds.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_delete_nonexistent_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("delete-nonexistent"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut lease = Lease::default();
    lease.set_lease_key("1");
    guard
        .refresher
        .delete_lease(&lease)
        .await
        .expect("delete of nonexistent lease should succeed");

    guard.teardown().await;
}

/// testWaitUntilLeaseTableExists — create then wait returns true.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_wait_until_lease_table_exists() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let table_name = unique_table_name("table-eventually-exists");
    let refresher = build_pay_per_request_refresher(client.clone(), table_name.clone());

    refresher
        .create_lease_table_if_not_exists()
        .await
        .expect("create_lease_table_if_not_exists");
    let exists = refresher
        .wait_until_lease_table_exists(1, 60)
        .await
        .expect("wait_until_lease_table_exists");
    assert!(exists);

    common::delete_table_best_effort(&client, &table_name).await;
}

/// testWaitUntilLeaseTableExistsTimeout — waiting on a nonexistent table returns
/// false without ever creating it.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_wait_until_lease_table_exists_timeout() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let table_name = unique_table_name("nonexistent");
    let refresher = build_pay_per_request_refresher(client.clone(), table_name);

    // Poll every 1s for a 1s budget: the table is never created, so this must
    // return false quickly (Java asserted exactly one sleep; here we assert the
    // observable result: it reports the table does not exist).
    let exists = refresher
        .wait_until_lease_table_exists(1, 1)
        .await
        .expect("wait_until_lease_table_exists");
    assert!(!exists);
    // Nothing was created — no teardown needed.
}

// ===========================================================================
// FILE 5: DynamoDBLeaseTakerIntegrationTest
// ===========================================================================
//
// LEASE_DURATION_MILLIS = 1000. The taker uses the harness's VirtualClock via
// with_time_provider so passTime() drives lease-age math deterministically.

const TAKER_LEASE_DURATION_MILLIS: i64 = 1000;

fn build_taker(
    refresher: Arc<dyn LeaseRefresher>,
    worker: &str,
    lease_duration_millis: i64,
    clock: &VirtualClock,
) -> DynamoDBLeaseTaker {
    DynamoDBLeaseTaker::new(
        refresher,
        worker,
        lease_duration_millis,
        Arc::new(NullMetricsFactory::new()),
    )
    .with_time_provider(clock.provider())
}

/// testSimpleLeaseTake
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_simple_lease_take() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-simple"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    builder.with_lease("1", None);
    builder.build().await;

    builder.take_mutate_assert_ids(&taker, &["1"]).await;

    guard.teardown().await;
}

/// testNotTakeUpdatedLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_not_take_updated_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-not-updated"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    builder.with_lease("1", Some("bar"));
    builder.build().await;

    builder.take_mutate_assert_count(&taker, 0).await; // learn state
    builder.renew_all_leases().await; // renew leases
    builder.pass_time(TAKER_LEASE_DURATION_MILLIS + 1);

    builder.take_mutate_assert_count(&taker, 0).await; // second scan

    guard.teardown().await;
}

/// testTakeOwnLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_take_own_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-own"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    builder.with_lease("1", Some(&taker.get_worker_identifier()));
    builder.build().await;

    builder.take_mutate_assert_count(&taker, 0).await; // learn state
    builder.pass_time(TAKER_LEASE_DURATION_MILLIS + 1);
    builder.take_mutate_assert_ids(&taker, &["1"]).await; // take own (expired) lease

    guard.teardown().await;
}

/// testNotTakeNewOwnedLease
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_not_take_new_owned_lease() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-new-owned"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    builder.with_lease("1", Some("bar"));
    builder.build().await;

    builder.take_mutate_assert_count(&taker, 0).await; // new + owned → no take
    builder.pass_time(TAKER_LEASE_DURATION_MILLIS + 1);
    builder.take_mutate_assert_ids(&taker, &["1"]).await; // old → take

    guard.teardown().await;
}

/// testNonGreedyTake — 3 free + 1 owned across 2 workers; take exactly 2.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_non_greedy_take() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-nongreedy"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    // very high multiplier avoids the very-old-lease priority short-circuit
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    )
    .with_very_old_lease_duration_nanos_multiplier(5_000_000);
    for i in 0..3 {
        builder.with_lease(&i.to_string(), None);
    }
    builder.with_lease("4", Some("bar"));
    builder.build().await;

    builder.take_mutate_assert_count(&taker, 2).await;

    guard.teardown().await;
}

/// testVeryOldLeaseTaker — all 3 free leases are "very old" → take all 3.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_very_old_lease_taker() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-veryold"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    for i in 0..3 {
        builder.with_lease(&i.to_string(), None);
    }
    builder.with_lease("4", Some("bar"));
    builder.build().await;

    builder.take_mutate_assert_count(&taker, 3).await;

    guard.teardown().await;
}

/// testGetAllLeases — allLeases() is empty until takeLeases() populates the cache.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_get_all_leases() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-getall"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    builder.with_lease("1", Some("bar"));
    builder.with_lease("2", Some("bar"));
    builder.with_lease("3", Some("baz"));
    builder.with_lease("4", Some("baz"));
    builder.with_lease("5", Some("foo"));
    let added = builder.build().await;

    assert_eq!(0, taker.all_leases().len());
    taker.take_leases().await.expect("take_leases");
    let all = taker.all_leases();
    assert_eq!(added.len(), all.len());

    guard.teardown().await;
}

/// testSlowGetAllLeases — leaseDurationMillis = 0.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_slow_get_all_leases() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-slow-getall"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(guard.refresher.clone(), "foo", 0, &builder.clock);
    builder.with_lease("1", Some("bar"));
    builder.with_lease("2", Some("bar"));
    builder.with_lease("5", Some("foo"));
    let added = builder.build().await;

    assert_eq!(0, taker.all_leases().len());
    taker.take_leases().await.expect("take_leases");
    let all = taker.all_leases();
    assert_eq!(added.len(), all.len());

    guard.teardown().await;
}

/// testNoStealWhenOffByOne
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_no_steal_when_off_by_one() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-offbyone"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    builder.with_lease("1", Some("bar"));
    builder.with_lease("2", Some("bar"));
    builder.with_lease("3", Some("baz"));
    builder.with_lease("4", Some("baz"));
    builder.with_lease("5", Some("foo"));
    builder.build().await;

    // Nothing: all leases new+owned and we won't steal when short by 1.
    builder.take_mutate_assert_count(&taker, 0).await;

    guard.teardown().await;
}

/// testSteal — foo (0 leases) steals 1 from baz (5 leases).
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_steal() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-steal"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    builder.with_lease("1", Some("bar"));
    for i in 2..=6 {
        builder.with_lease(&i.to_string(), Some("baz"));
    }
    builder.build().await;

    let taken = builder.steal_mutate_assert(&taker, 1).await;
    let stolen: &String = taken.keys().next().unwrap();
    assert_ne!("1", stolen, "should steal one of baz's leases, not bar's");

    guard.teardown().await;
}

/// testNoStealWhenExpiredLeases — take the free lease "1" instead of stealing.
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_no_steal_when_expired_leases() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("taker-nosteal-expired"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(
        guard.refresher.clone(),
        "foo",
        TAKER_LEASE_DURATION_MILLIS,
        &builder.clock,
    );
    builder.with_lease("1", None);
    for i in 2..=4 {
        builder.with_lease(&i.to_string(), Some("bar"));
    }
    builder.build().await;

    builder.take_mutate_assert_ids(&taker, &["1"]).await;

    guard.teardown().await;
}

// ===========================================================================
// FILE 3 & 4: DynamoDBLeaseRenewer[BillingModePayPerRequest]IntegrationTest
// ===========================================================================
//
// Both Java files are identical except the billing mode of the lease table.
// Ported once as parametrized helpers, invoked from two thin test wrappers per
// case (Provisioned = the base test's default table; PayPerRequest = the
// billing-mode variant). LEASE_DURATION_MILLIS = 2000.

const RENEWER_LEASE_DURATION_MILLIS: i64 = 2000;
const TEST_METRIC: &str = "TestOperation";

fn build_renewer(
    refresher: Arc<dyn LeaseRefresher>,
    worker: &str,
    lease_duration_millis: i64,
) -> DynamoDBLeaseRenewer {
    DynamoDBLeaseRenewer::new(
        refresher,
        worker,
        lease_duration_millis,
        Arc::new(NullMetricsFactory::new()),
        Arc::new(LeaseStatsRecorder::new(30_000, Arc::new(|| 0))),
        Arc::new(|_lease| {}),
        1,
    )
}

async fn renewer_guard(
    billing_mode: BillingMode,
    label: &str,
) -> (LeaseTableGuard, aws_sdk_dynamodb::Client) {
    let client = dynamodb_client().await;
    let guard =
        LeaseTableGuard::setup(client.clone(), unique_table_name(label), billing_mode).await;
    (guard, client)
}

// --- testSimpleRenew ---
async fn renewer_simple_renew(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.build().await;

    builder.add_leases_to_renew(&renewer, &["1"]);
    builder.renew_mutate_assert(&renewer, &["1"]).await;

    guard.teardown().await;
}

// --- testLeaseLoss ---
async fn renewer_lease_loss(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.with_lease("2", Some("foo"));
    builder.build().await;

    builder.add_leases_to_renew(&renewer, &["1", "2"]);
    let mut renewed = builder.renew_mutate_assert(&renewer, &["1", "2"]).await;
    let mut lease2 = renewed.remove("2").unwrap();

    // lose lease 2
    guard
        .refresher
        .take_lease(&mut lease2, "bar")
        .await
        .expect("take_lease");

    builder.renew_mutate_assert(&renewer, &["1"]).await;

    guard.teardown().await;
}

// --- testClear ---
async fn renewer_clear(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.build().await;
    builder.add_leases_to_renew(&renewer, &["1"]);
    builder.renew_mutate_assert(&renewer, &["1"]).await;

    renewer.clear_currently_held_leases();
    builder.renew_mutate_assert(&renewer, &[]).await;

    guard.teardown().await;
}

// --- testGetCurrentlyHeldLease ---
async fn renewer_get_currently_held_lease(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.build().await;
    builder.add_leases_to_renew(&renewer, &["1"]);
    builder.renew_mutate_assert(&renewer, &["1"]).await;

    // this should be a copy that doesn't get updated
    let lease = renewer.get_currently_held_lease("1").expect("held");
    assert_eq!(1, lease.lease_counter());

    // one more renewal; the old copy must not change
    builder.renew_mutate_assert(&renewer, &["1"]).await;
    assert_eq!(1, lease.lease_counter());

    guard.teardown().await;
}

// --- testGetCurrentlyHeldLeases ---
async fn renewer_get_currently_held_leases(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.with_lease("2", Some("foo"));
    builder.build().await;
    builder.add_leases_to_renew(&renewer, &["1", "2"]);
    let mut renewed = builder.renew_mutate_assert(&renewer, &["1", "2"]).await;
    let mut lease2 = renewed.remove("2").unwrap();

    // This should be a snapshot that doesn't get updated.
    let held = renewer.get_currently_held_leases();
    assert_eq!(2, held.len());
    assert_eq!(1, held.get("1").unwrap().lease_counter());
    assert_eq!(1, held.get("2").unwrap().lease_counter());

    // lose lease 2
    guard
        .refresher
        .take_lease(&mut lease2, "bar")
        .await
        .expect("take_lease");

    // Another renewal — the earlier snapshot must not change.
    builder.renew_mutate_assert(&renewer, &["1"]).await;
    assert_eq!(2, held.len());
    assert_eq!(1, held.get("1").unwrap().lease_counter());
    assert_eq!(1, held.get("2").unwrap().lease_counter());

    guard.teardown().await;
}

// --- testUpdateLease ---
async fn renewer_update_lease(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.build().await;
    builder.add_leases_to_renew(&renewer, &["1"]);
    builder.renew_mutate_assert(&renewer, &["1"]).await;

    let mut expected = renewer.get_currently_held_lease("1").expect("held");
    expected.set_checkpoint(ExtendedSequenceNumber::from_sequence_number(
        "new checkpoint",
    ));
    let token = expected.concurrency_token().expect("token");
    assert!(renewer
        .update_lease(&expected, token, TEST_METRIC, expected.lease_key().unwrap())
        .await
        .expect("update_lease"));

    // counter + data changed immediately after the update
    let actual = renewer.get_currently_held_lease("1").expect("held");
    expected.set_lease_counter(expected.lease_counter() + 1);
    assert_eq!(expected, actual);

    // ...and after another round of renewal
    renewer.renew_leases().await.expect("renew_leases");
    let actual = renewer.get_currently_held_lease("1").expect("held");
    expected.set_lease_counter(expected.lease_counter() + 1);
    assert_eq!(expected, actual);

    guard.teardown().await;
}

// --- testUpdateLostLease ---
async fn renewer_update_lost_lease(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.build().await;
    builder.add_leases_to_renew(&renewer, &["1"]);
    builder.renew_mutate_assert(&renewer, &["1"]).await;

    let mut lease = renewer.get_currently_held_lease("1").expect("held");

    // cause loss without the renewer realizing (external renew bumps counter)
    guard
        .refresher
        .renew_lease(&mut lease)
        .await
        .expect("renew_lease");

    // renewer still thinks it holds the lease
    assert!(renewer.get_currently_held_lease("1").is_some());
    lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number(
        "new checkpoint",
    ));

    // update fails
    let token = lease.concurrency_token().expect("token");
    assert!(!renewer
        .update_lease(&lease, token, TEST_METRIC, lease.lease_key().unwrap())
        .await
        .expect("update_lease"));
    // renewer no longer thinks it holds the lease
    assert!(renewer.get_currently_held_lease("1").is_none());

    guard.teardown().await;
}

// --- testUpdateOldLease ---
async fn renewer_update_old_lease(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.build().await;
    builder.add_leases_to_renew(&renewer, &["1"]);
    builder.renew_mutate_assert(&renewer, &["1"]).await;

    let mut lease = renewer.get_currently_held_lease("1").expect("held");

    // cause loss such that the renewer knows the lease is gone
    guard
        .refresher
        .take_lease(&mut lease, "bar")
        .await
        .expect("take_lease");
    builder.renew_mutate_assert(&renewer, &[]).await;

    lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number(
        "new checkpoint",
    ));
    let token = lease.concurrency_token().expect("token");
    assert!(!renewer
        .update_lease(&lease, token, TEST_METRIC, lease.lease_key().unwrap())
        .await
        .expect("update_lease"));

    guard.teardown().await;
}

// --- testUpdateRegainedLease ---
async fn renewer_update_regained_lease(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.build().await;
    builder.add_leases_to_renew(&renewer, &["1"]);
    builder.renew_mutate_assert(&renewer, &["1"]).await;

    let mut lease = renewer.get_currently_held_lease("1").expect("held");

    // cause loss
    guard
        .refresher
        .take_lease(&mut lease, "bar")
        .await
        .expect("take_lease");
    builder.renew_mutate_assert(&renewer, &[]).await;

    // regain the lease (fresh concurrency token)
    builder.add_leases_to_renew(&renewer, &["1"]);

    lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number(
        "new checkpoint",
    ));
    let token = lease.concurrency_token().expect("token");
    // old copy's token is stale for the regained lease → update fails
    assert!(!renewer
        .update_lease(&lease, token, TEST_METRIC, lease.lease_key().unwrap())
        .await
        .expect("update_lease"));

    guard.teardown().await;
}

// --- testIgnoreNoRenewalTimestamp ---
async fn renewer_ignore_no_renewal_timestamp(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    let mut lease = builder.build().await.remove("1").unwrap();
    lease.set_last_counter_increment_nanos(None);

    renewer.add_leases_to_renew(vec![lease]);
    assert_eq!(0, renewer.get_currently_held_leases().len());

    guard.teardown().await;
}

// --- testLeaseTimeout ---
async fn renewer_lease_timeout(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let renewer = build_renewer(
        guard.refresher.clone(),
        "foo",
        RENEWER_LEASE_DURATION_MILLIS,
    );

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease("1", Some("foo"));
    builder.build().await;
    builder.add_leases_to_renew(&renewer, &["1"]);
    builder.renew_mutate_assert(&renewer, &["1"]).await;

    // wait for the lease to time out
    tokio::time::sleep(Duration::from_millis(RENEWER_LEASE_DURATION_MILLIS as u64)).await;

    assert_eq!(0, renewer.get_currently_held_leases().len());

    guard.teardown().await;
}

// --- testInitialize ---
async fn renewer_initialize(billing_mode: BillingMode, label: &str) {
    let (guard, _client) = renewer_guard(billing_mode, label).await;
    let shard_id = "shd-0-0";
    let owner = "foo:8000";

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    builder.with_lease(shard_id, Some(owner));
    let leases = builder.build().await;

    let renewer = build_renewer(guard.refresher.clone(), owner, 30_000);
    renewer.initialize().await.expect("initialize");
    let held = renewer.get_currently_held_leases();
    assert_eq!(leases.len(), held.len());
    let held_keys: HashSet<String> = held.keys().cloned().collect();
    let expected_keys: HashSet<String> = leases.keys().cloned().collect();
    assert_eq!(expected_keys, held_keys);

    guard.teardown().await;
}

// ---- Provisioned-mode wrappers (File 3: DynamoDBLeaseRenewerIntegrationTest) ----
// (Java's base LeaseIntegrationTest table used PAY_PER_REQUEST in getLeaseRefresher,
//  so both files effectively used PayPerRequest; we run these against Provisioned
//  to additionally cover the provisioned-billing table path.)

#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_simple_renew() {
    common::init_test_tracing();
    renewer_simple_renew(BillingMode::Provisioned, "renewer-simple").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_lease_loss() {
    common::init_test_tracing();
    renewer_lease_loss(BillingMode::Provisioned, "renewer-loss").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_clear() {
    common::init_test_tracing();
    renewer_clear(BillingMode::Provisioned, "renewer-clear").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_get_currently_held_lease() {
    common::init_test_tracing();
    renewer_get_currently_held_lease(BillingMode::Provisioned, "renewer-getheld").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_get_currently_held_leases() {
    common::init_test_tracing();
    renewer_get_currently_held_leases(BillingMode::Provisioned, "renewer-getheld-s").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_update_lease() {
    common::init_test_tracing();
    renewer_update_lease(BillingMode::Provisioned, "renewer-update").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_update_lost_lease() {
    common::init_test_tracing();
    renewer_update_lost_lease(BillingMode::Provisioned, "renewer-update-lost").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_update_old_lease() {
    common::init_test_tracing();
    renewer_update_old_lease(BillingMode::Provisioned, "renewer-update-old").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_update_regained_lease() {
    common::init_test_tracing();
    renewer_update_regained_lease(BillingMode::Provisioned, "renewer-update-regained").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ignore_no_renewal_timestamp() {
    common::init_test_tracing();
    renewer_ignore_no_renewal_timestamp(BillingMode::Provisioned, "renewer-nots").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_lease_timeout() {
    common::init_test_tracing();
    renewer_lease_timeout(BillingMode::Provisioned, "renewer-timeout").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_initialize() {
    common::init_test_tracing();
    renewer_initialize(BillingMode::Provisioned, "renewer-init").await;
}

// ---- PayPerRequest-mode wrappers (File 4) ----

#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_simple_renew() {
    common::init_test_tracing();
    renewer_simple_renew(BillingMode::PayPerRequest, "renewer-ppr-simple").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_lease_loss() {
    common::init_test_tracing();
    renewer_lease_loss(BillingMode::PayPerRequest, "renewer-ppr-loss").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_clear() {
    common::init_test_tracing();
    renewer_clear(BillingMode::PayPerRequest, "renewer-ppr-clear").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_get_currently_held_lease() {
    common::init_test_tracing();
    renewer_get_currently_held_lease(BillingMode::PayPerRequest, "renewer-ppr-getheld").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_get_currently_held_leases() {
    common::init_test_tracing();
    renewer_get_currently_held_leases(BillingMode::PayPerRequest, "renewer-ppr-getheld-s").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_update_lease() {
    common::init_test_tracing();
    renewer_update_lease(BillingMode::PayPerRequest, "renewer-ppr-update").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_update_lost_lease() {
    common::init_test_tracing();
    renewer_update_lost_lease(BillingMode::PayPerRequest, "renewer-ppr-update-lost").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_update_old_lease() {
    common::init_test_tracing();
    renewer_update_old_lease(BillingMode::PayPerRequest, "renewer-ppr-update-old").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_update_regained_lease() {
    common::init_test_tracing();
    renewer_update_regained_lease(BillingMode::PayPerRequest, "renewer-ppr-update-regained").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_ignore_no_renewal_timestamp() {
    common::init_test_tracing();
    renewer_ignore_no_renewal_timestamp(BillingMode::PayPerRequest, "renewer-ppr-nots").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_lease_timeout() {
    common::init_test_tracing();
    renewer_lease_timeout(BillingMode::PayPerRequest, "renewer-ppr-timeout").await;
}
#[tokio::test]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_renewer_ppr_initialize() {
    common::init_test_tracing();
    renewer_initialize(BillingMode::PayPerRequest, "renewer-ppr-init").await;
}

// Silence unused-const warning for IGNORE_MSG (kept for documentation parity).
const _: &str = IGNORE_MSG;
