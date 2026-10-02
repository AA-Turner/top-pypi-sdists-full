//! Integration tests — port of the Java
//! `coordinator/assignment/LeaseCountBasedLeaseAssignmentDeciderIntegrationTest.java`.
//!
//! Despite its name, the Java integration test extends `LeaseIntegrationTest`
//! and exercises the **lease-count-based assignment** path exactly as it runs in
//! the DynamoDB leasing pipeline: through the real [`DynamoDBLeaseTaker`] against
//! a real DynamoDB lease table (create + `PutItem`), driving the same
//! `TestHarnessBuilder.takeMutateAssert` / `stealMutateAssert` assertions the
//! `DynamoDBLeaseTakerIntegrationTest` uses. In KCL v2 the taker *is* the
//! lease-count-based decider on the DDB path, so this faithfully ports the five
//! `@Test` methods (basic / non-greedy / steal / no-steal-off-by-one /
//! very-old-priority) — validating the real conditional-write assignment
//! semantics the in-memory decider unit tests cannot.
//!
//! Every test is `#[ignore]` (see the module doc in `common/mod.rs`). Run with:
//! `cargo test -p kcl -- --ignored` (optionally `AWS_ENDPOINT_URL=...` to
//! redirect to LocalStack).

mod common;

use std::collections::HashMap;
use std::sync::Arc;

use aws_sdk_dynamodb::types::BillingMode;

use kcl::leases::dynamodb::DynamoDBLeaseTaker;
use kcl::leases::{Lease, LeaseRefresher, LeaseTaker};
use kcl::metrics::NullMetricsFactory;

use common::{dynamodb_client, harness_lease, unique_table_name, LeaseTableGuard, VirtualClock};

/// Java `LEASE_DURATION_MILLIS = 1000L`.
const LEASE_DURATION_MILLIS: i64 = 1000;

// ---------------------------------------------------------------------------
// Test-local TestHarnessBuilder (the subset used by these five tests).
//
// Mirrors the Java `dynamodb/TestHarnessBuilder`: builds leases via the harness
// `createLease`, persists them with `createLeaseIfNotExists`, tracks a virtual
// clock, and provides `takeMutateAssert` (by count / by ids) + `stealMutateAssert`.
// (A fuller copy lives in `leases_dynamodb_it.rs`; each `*_it.rs` file is a
// separate test binary and cannot share private helpers, so the needed subset is
// duplicated here.)
// ---------------------------------------------------------------------------

struct TestHarnessBuilder {
    refresher: Arc<dyn LeaseRefresher>,
    leases: HashMap<String, Lease>,
    clock: VirtualClock,
}

impl TestHarnessBuilder {
    fn new(refresher: Arc<dyn LeaseRefresher>) -> Self {
        Self {
            refresher,
            leases: HashMap::new(),
            clock: VirtualClock::new(),
        }
    }

    /// `withLease(shardId, owner)`.
    fn with_lease(&mut self, shard_id: &str, owner: Option<&str>) -> &mut Self {
        self.leases
            .insert(shard_id.to_string(), harness_lease(shard_id, owner));
        self
    }

    /// `build()` — persist leases; set lastCounterIncrementNanos for owned ones,
    /// snapshotting the virtual time (so ownership age is stable).
    async fn build(&mut self) {
        for lease in self.leases.values_mut() {
            self.refresher
                .create_lease_if_not_exists(lease)
                .await
                .expect("create_lease_if_not_exists failed");
            if lease.lease_owner().is_some() {
                lease.set_last_counter_increment_nanos(Some(self.clock.now_nanos()));
            }
        }
    }

    /// `takeMutateAssert(taker, numToTake)`.
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
                .get(&key)
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
    ) {
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
    /// ownerSwitchesSinceCheckpoint when the owner changed, set the new owner,
    /// then assert the mutated original equals `actual`, storing it back.
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
}

/// Build the `DynamoDBLeaseTaker` for worker "foo" driven by the harness clock
/// (Java `new DynamoDBLeaseTaker(leaseRefresher, "foo", LEASE_DURATION_MILLIS,
/// NullMetricsFactory)`).
fn build_taker(refresher: Arc<dyn LeaseRefresher>, clock: &VirtualClock) -> DynamoDBLeaseTaker {
    DynamoDBLeaseTaker::new(
        refresher,
        "foo",
        LEASE_DURATION_MILLIS,
        Arc::new(NullMetricsFactory::new()),
    )
    .with_time_provider(clock.provider())
}

// ===========================================================================
// The five @Test methods.
// ===========================================================================

/// Test 1: `testBasicLeaseAssignment` — 3 unassigned leases → all taken.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_basic_lease_assignment() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("assign-basic"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(guard.refresher.clone(), &builder.clock);
    builder
        .with_lease("1", None)
        .with_lease("2", None)
        .with_lease("3", None);
    builder.build().await;

    builder
        .take_mutate_assert_ids(&taker, &["1", "2", "3"])
        .await;

    guard.teardown().await;
}

/// Test 2: `testNonGreedyAssignment` — 3 unassigned + 1 owned across 2 workers;
/// with the very-old short-circuit disabled, take exactly 2.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_non_greedy_assignment() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("assign-nongreedy"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    // Very high multiplier avoids the very-old-lease priority short-circuit
    // (Java: taker.withVeryOldLeaseDurationNanosMultiplier(5000000)).
    let taker = build_taker(guard.refresher.clone(), &builder.clock)
        .with_very_old_lease_duration_nanos_multiplier(5_000_000);
    for i in 0..3 {
        builder.with_lease(&i.to_string(), None);
    }
    builder.with_lease("4", Some("bar"));
    builder.build().await;

    builder.take_mutate_assert_count(&taker, 2).await;

    guard.teardown().await;
}

/// Test 3: `testSteal` — foo (0 leases) steals 1 from baz (5 leases); never bar's.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_steal() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("assign-steal"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(guard.refresher.clone(), &builder.clock);
    builder.with_lease("1", Some("bar"));
    for i in 2..=6 {
        builder.with_lease(&i.to_string(), Some("baz"));
    }
    builder.build().await;

    let taken = builder.steal_mutate_assert(&taker, 1).await;
    let stolen = taken.keys().next().unwrap();
    assert_ne!("1", stolen, "should steal one of baz's leases, not bar's");

    guard.teardown().await;
}

/// Test 4: `testNoStealWhenOffByOne` — all leases new+owned; short by 1 → no take.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_no_steal_when_off_by_one() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("assign-offbyone"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(guard.refresher.clone(), &builder.clock);
    builder
        .with_lease("1", Some("bar"))
        .with_lease("2", Some("bar"))
        .with_lease("3", Some("baz"))
        .with_lease("4", Some("baz"))
        .with_lease("5", Some("foo"));
    builder.build().await;

    builder.take_mutate_assert_count(&taker, 0).await;

    guard.teardown().await;
}

/// Test 5: `testVeryOldLeasePriority` — 3 very-old unassigned leases → all taken
/// regardless of the balanced target.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_very_old_lease_priority() {
    common::init_test_tracing();
    let client = dynamodb_client().await;
    let guard = LeaseTableGuard::setup(
        client.clone(),
        unique_table_name("assign-veryold"),
        BillingMode::PayPerRequest,
    )
    .await;

    let mut builder = TestHarnessBuilder::new(guard.refresher.clone());
    let taker = build_taker(guard.refresher.clone(), &builder.clock);
    for i in 0..3 {
        builder.with_lease(&i.to_string(), None);
    }
    builder.with_lease("4", Some("bar"));
    builder.build().await;

    builder.take_mutate_assert_count(&taker, 3).await;

    guard.teardown().await;
}
