//! Integration test — port of `DynamoDBLeaseCoordinatorIntegrationTest.java`.
//!
//! Exercises the coordinator's taker/renewer wiring and the checkpoint update
//! path (optimistic concurrency on the lease `concurrencyToken`) against real
//! DynamoDB. `#[ignore]` — run with `cargo test -p kcl -- --ignored`
//! (optionally `AWS_ENDPOINT_URL=...` to redirect to LocalStack).
//!
//! Like Java (one per-class table, `@Before deleteAll()`, sequential
//! Surefire execution), all tests here share **one fixed-name lease table +
//! `LeaseOwnerToLeaseKeyIndex` GSI**, created on first-ever use and reused
//! across runs — DynamoDB throttles concurrent GSI creation account-wide, so
//! per-test tables made parallel fixtures miss the 900s ACTIVE-wait. A
//! process-global lock serializes the fixtures (the Rust stand-in for
//! Surefire's sequential execution), and each setup/teardown `delete_all`s.
//! The table is deliberately left behind (Java-style; prefixed `kclrs-it-`
//! for sweeping). Caveat, same as Java: two *processes* running this file
//! against the same account at the same time would interfere.

mod common;

use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;

use uuid::Uuid;

use kcl::coordinator::{LeaseAssignmentMode, MigrationAdaptiveLeaseAssignmentModeProvider};
use kcl::leases::dynamodb::DynamoDBLeaseCoordinator;
use kcl::leases::lease_management_config::{
    GracefulLeaseHandoffConfig, WorkerUtilizationAwareAssignmentConfig,
};
use kcl::leases::{Lease, LeaseCoordinator, LeaseRefresher};
use kcl::metrics::NullMetricsFactory;
use kcl::retrieval::kpl::ExtendedSequenceNumber;

use common::{build_pay_per_request_refresher, dynamodb_client, harness_lease};

const LEASE_DURATION_MILLIS: i64 = 5000;
const EPSILON_MILLIS: i64 = 25;
const MAX_LEASES_FOR_WORKER: i32 = i32::MAX;
const MAX_LEASES_TO_STEAL_AT_ONE_TIME: i32 = 1;
const MAX_LEASE_RENEWER_THREAD_COUNT: i32 = 20;
const INITIAL_READ_CAPACITY: i64 = 10;
const INITIAL_WRITE_CAPACITY: i64 = 10;
const OPERATION: &str = "TestOperation";

/// A prepared coordinator + shared refresher for one test, holding the
/// shared-table lock for the test's duration.
struct CoordinatorFixture {
    coordinator: Arc<DynamoDBLeaseCoordinator>,
    refresher: Arc<dyn LeaseRefresher>,
    worker_id: String,
    /// Held for the fixture's lifetime: serializes the tests onto the shared
    /// table (Java gets this from Surefire's sequential execution).
    _table_guard: tokio::sync::MutexGuard<'static, ()>,
}

/// The Java-style fixed per-class table name, shared by every test in this
/// file and reused across runs (created once; `delete_all` keeps it clean).
const SHARED_TABLE_NAME: &str = "kclrs-it-coordinator-shared";

/// Serializes fixtures onto [`SHARED_TABLE_NAME`]. `tokio::sync::Mutex` is
/// runtime-agnostic, so locking it from each `#[tokio::test]`'s own runtime is
/// sound.
static SHARED_TABLE_LOCK: tokio::sync::Mutex<()> = tokio::sync::Mutex::const_new(());

impl CoordinatorFixture {
    /// Ports the Java `@Before setup`: ensure the shared table + GSI exist
    /// (no-op after the first-ever run), delete-all leftover leases, construct
    /// the coordinator, and `start` it with a
    /// WORKER_UTILIZATION_AWARE_ASSIGNMENT mode provider (dynamic mode change
    /// unsupported).
    async fn setup(_label: &str) -> Self {
        let table_guard = SHARED_TABLE_LOCK.lock().await;
        let client = dynamodb_client().await;
        let table_name = SHARED_TABLE_NAME.to_string();
        let worker_id = Uuid::new_v4().to_string();
        let refresher = build_pay_per_request_refresher(client.clone(), table_name.clone());

        refresher
            .create_lease_table_if_not_exists_with_capacity(
                INITIAL_READ_CAPACITY,
                INITIAL_WRITE_CAPACITY,
            )
            .await
            .expect("create_lease_table_if_not_exists");
        refresher
            .wait_until_lease_table_exists(10, 600)
            .await
            .expect("wait_until_lease_table_exists");
        refresher
            .create_lease_owner_to_lease_key_index_if_not_exists()
            .await
            .expect("create GSI");
        // Java ignores this boolean; here a non-ACTIVE index would surface
        // minutes later as a cryptic discovery-count assertion (the discoverer
        // queries the GSI), so fail fast instead. With the shared reused table
        // this only ever waits on the first-ever run's single GSI creation.
        let index_active = refresher
            .wait_until_lease_owner_to_lease_key_index_exists(10, 900)
            .await;
        assert!(
            index_active,
            "LeaseOwnerToLeaseKeyIndex on {table_name} did not become ACTIVE within 900s"
        );

        refresher.delete_all().await.expect("delete_all");

        let coordinator = Arc::new(DynamoDBLeaseCoordinator::new(
            refresher.clone(),
            worker_id.clone(),
            LEASE_DURATION_MILLIS,
            /* enable_priority_lease_assignment = */ true,
            EPSILON_MILLIS,
            MAX_LEASES_FOR_WORKER,
            MAX_LEASES_TO_STEAL_AT_ONE_TIME,
            MAX_LEASE_RENEWER_THREAD_COUNT,
            INITIAL_READ_CAPACITY,
            INITIAL_WRITE_CAPACITY,
            Arc::new(NullMetricsFactory::new()),
            WorkerUtilizationAwareAssignmentConfig::default(),
            GracefulLeaseHandoffConfig::default(),
            2 * LEASE_DURATION_MILLIS,
            None,
            0,
        ));

        // Mode provider: WORKER_UTILIZATION_AWARE_ASSIGNMENT, dynamic change off.
        let mode_provider = Arc::new(MigrationAdaptiveLeaseAssignmentModeProvider::new());
        mode_provider.initialize(false, LeaseAssignmentMode::WorkerUtilizationAwareAssignment);

        coordinator
            .start(mode_provider)
            .await
            .expect("coordinator start");

        Self {
            coordinator,
            refresher,
            worker_id,
            _table_guard: table_guard,
        }
    }

    /// Stop the coordinator and clear the shared table for the next test. The
    /// table itself is deliberately kept (Java-style fixed per-class table).
    async fn teardown(self) {
        self.coordinator.stop().await;
        let _ = self.refresher.delete_all().await;
    }
}

/// Build lease(s) directly via the refresher (the Java coordinator test's inline
/// `TestHarnessBuilder`: checkpoint="checkpoint", counter=0, parents={parentShardId}).
async fn build_leases(
    refresher: &Arc<dyn LeaseRefresher>,
    specs: &[(&str, Option<&str>)],
) -> HashMap<String, Lease> {
    let mut out = HashMap::new();
    for (shard_id, owner) in specs {
        let mut lease = harness_lease(shard_id, *owner);
        refresher
            .create_lease_if_not_exists(&lease)
            .await
            .expect("create_lease_if_not_exists");
        if lease.lease_owner().is_some() {
            lease.set_last_counter_increment_nanos(Some(now_nanos()));
        }
        out.insert(shard_id.to_string(), lease);
    }
    out
}

fn now_nanos() -> i64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_nanos() as i64)
        .unwrap_or(0)
}

/// Reproduces `DynamoDBCheckpointer.setCheckpoint(leaseKey, checkpoint, token)`:
/// fetch the currently-held lease, commit the checkpoint (clearing pending +
/// resetting the owner-switch counter), then conditionally update. Returns false
/// if the lease is not currently held or the CAS on the token fails.
async fn set_checkpoint(
    coordinator: &Arc<DynamoDBLeaseCoordinator>,
    lease_key: &str,
    checkpoint: &ExtendedSequenceNumber,
    concurrency_token: Uuid,
) -> bool {
    let Some(mut lease) = coordinator.get_currently_held_lease(lease_key) else {
        return false;
    };
    lease.set_checkpoint(checkpoint.clone());
    lease.set_pending_checkpoint(None);
    lease.set_pending_checkpoint_state(None);
    lease.set_owner_switches_since_checkpoint(0);
    coordinator
        .update_lease(&lease, concurrency_token, OPERATION, lease_key)
        .await
        .expect("update_lease")
}

/// Reproduces `DynamoDBCheckpointer.prepareCheckpoint(...)`: set only the pending
/// checkpoint + pending state, leave the committed checkpoint + owner-switch
/// counter untouched, then conditionally update.
async fn prepare_checkpoint(
    coordinator: &Arc<DynamoDBLeaseCoordinator>,
    lease_key: &str,
    pending_checkpoint: &ExtendedSequenceNumber,
    concurrency_token: Uuid,
    pending_checkpoint_state: &[u8],
) -> bool {
    let Some(mut lease) = coordinator.get_currently_held_lease(lease_key) else {
        return false;
    };
    lease.set_pending_checkpoint(Some(pending_checkpoint.clone()));
    lease.set_pending_checkpoint_state(Some(pending_checkpoint_state.to_vec()));
    coordinator
        .update_lease(&lease, concurrency_token, OPERATION, lease_key)
        .await
        .expect("update_lease")
}

/// testUpdateCheckpoint — full initial→pending→new checkpoint sequence with
/// read-back assertions after each step.
#[tokio::test(flavor = "multi_thread")]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_update_checkpoint() {
    common::init_test_tracing();
    let fixture = CoordinatorFixture::setup("coord-update-ckpt").await;
    let lease_key = "shd-1";
    build_leases(&fixture.refresher, &[(lease_key, None)]).await;

    fixture
        .coordinator
        .run_lease_taker()
        .await
        .expect("run_lease_taker");
    fixture
        .coordinator
        .run_lease_renewer()
        .await
        .expect("run_lease_renewer");

    let mut lease = fixture
        .coordinator
        .get_currently_held_lease(lease_key)
        .expect("should hold lease after take+renew");

    let initial_checkpoint = ExtendedSequenceNumber::from_sequence_number("initialCheckpoint");
    let pending_checkpoint = ExtendedSequenceNumber::from_sequence_number("pendingCheckpoint");
    let new_checkpoint = ExtendedSequenceNumber::from_sequence_number("newCheckpoint");
    let checkpoint_state = b"checkpointState".to_vec();
    let token = lease.concurrency_token().expect("token");

    // --- initial checkpoint ---
    assert!(set_checkpoint(&fixture.coordinator, lease_key, &initial_checkpoint, token).await);
    let from_ddb = fixture
        .refresher
        .get_lease(lease_key)
        .await
        .unwrap()
        .unwrap();
    lease.set_lease_counter(lease.lease_counter() + 1);
    lease.set_checkpoint(initial_checkpoint.clone());
    lease.set_lease_owner(Some(fixture.coordinator.worker_identifier()));
    assert_eq!(lease, from_ddb);

    // --- pending checkpoint ---
    assert!(
        prepare_checkpoint(
            &fixture.coordinator,
            lease_key,
            &pending_checkpoint,
            token,
            &checkpoint_state
        )
        .await
    );
    let from_ddb = fixture
        .refresher
        .get_lease(lease_key)
        .await
        .unwrap()
        .unwrap();
    lease.set_lease_counter(lease.lease_counter() + 1);
    lease.set_checkpoint(initial_checkpoint.clone());
    lease.set_pending_checkpoint(Some(pending_checkpoint.clone()));
    lease.set_pending_checkpoint_state(Some(checkpoint_state.clone()));
    assert_eq!(lease, from_ddb);

    // --- new checkpoint (clears pending) ---
    assert!(set_checkpoint(&fixture.coordinator, lease_key, &new_checkpoint, token).await);
    let from_ddb = fixture
        .refresher
        .get_lease(lease_key)
        .await
        .unwrap()
        .unwrap();
    lease.set_lease_counter(lease.lease_counter() + 1);
    lease.set_checkpoint(new_checkpoint);
    lease.set_pending_checkpoint(None);
    lease.set_pending_checkpoint_state(None);
    assert_eq!(lease, from_ddb);

    fixture.teardown().await;
}

/// testGetAllAssignments — after runLeaseTaker, allLeases() returns all 5 leases.
#[tokio::test(flavor = "multi_thread")]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_get_all_assignments() {
    common::init_test_tracing();
    let fixture = CoordinatorFixture::setup("coord-getall").await;
    let specs: Vec<(&str, Option<&str>)> = vec![
        ("1", Some(fixture.worker_id.as_str())),
        ("2", Some(fixture.worker_id.as_str())),
        ("3", Some(fixture.worker_id.as_str())),
        ("4", Some(fixture.worker_id.as_str())),
        ("5", Some(fixture.worker_id.as_str())),
    ];
    let added = build_leases(&fixture.refresher, &specs).await;

    fixture
        .coordinator
        .run_lease_taker()
        .await
        .expect("run_lease_taker");

    let all = fixture.coordinator.all_leases();
    assert_eq!(added.len(), all.len());
    for lease in added.values() {
        assert!(
            all.iter().any(|l| l.lease_key() == lease.lease_key()),
            "missing lease {:?}",
            lease.lease_key()
        );
    }

    fixture.teardown().await;
}

/// testLeaseDiscoveryFutureRuns — after waiting a lease duration, the background
/// discovery loop has run and getAssignments() sees all leases.
#[tokio::test(flavor = "multi_thread")]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_lease_discovery_future_runs() {
    common::init_test_tracing();
    let fixture = CoordinatorFixture::setup("coord-discovery").await;
    let specs: Vec<(&str, Option<&str>)> = vec![
        ("1", Some(fixture.worker_id.as_str())),
        ("2", Some(fixture.worker_id.as_str())),
        ("3", Some(fixture.worker_id.as_str())),
        ("4", Some(fixture.worker_id.as_str())),
        ("5", Some(fixture.worker_id.as_str())),
    ];
    let added = build_leases(&fixture.refresher, &specs).await;

    // Ensure the discovery loop runs at least once.
    tokio::time::sleep(Duration::from_millis(LEASE_DURATION_MILLIS as u64)).await;

    assert_eq!(added.len(), fixture.coordinator.get_assignments().len());

    fixture.teardown().await;
}

/// stopLeaseTakerCancelsLeaseDiscoveryFuture — stopping the taker cancels the
/// discovery loop, so no leases are discovered.
///
/// Adaptation from Java's ordering (build leases → stop): the discovery loop's
/// first tick fires at start and the next after ~5s, so Java's order is a
/// latent race — under slow AWS (e.g. concurrent fixtures), a discovery tick
/// can land mid-`build_leases` and hand a lease to the renewer before `stop`.
/// Stopping FIRST tests the same intent (a cancelled discovery loop must not
/// discover the leases created afterwards) deterministically.
#[tokio::test(flavor = "multi_thread")]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn stop_lease_taker_cancels_lease_discovery_future() {
    common::init_test_tracing();
    let fixture = CoordinatorFixture::setup("coord-stopdiscovery").await;

    fixture.coordinator.stop_lease_taker();

    let specs: Vec<(&str, Option<&str>)> = vec![
        ("1", Some(fixture.worker_id.as_str())),
        ("2", Some(fixture.worker_id.as_str())),
        ("3", Some(fixture.worker_id.as_str())),
        ("4", Some(fixture.worker_id.as_str())),
        ("5", Some(fixture.worker_id.as_str())),
    ];
    build_leases(&fixture.refresher, &specs).await;

    tokio::time::sleep(Duration::from_millis(LEASE_DURATION_MILLIS as u64)).await;

    assert_eq!(0, fixture.coordinator.get_assignments().len());

    fixture.teardown().await;
}

/// testUpdateCheckpointLeaseUpdated — an external renew bumps the counter, so
/// the checkpoint CAS (on the token) fails; only counter + owner change.
#[tokio::test(flavor = "multi_thread")]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_update_checkpoint_lease_updated() {
    common::init_test_tracing();
    let fixture = CoordinatorFixture::setup("coord-ckpt-updated").await;
    let lease_key = "shd-1";
    build_leases(&fixture.refresher, &[(lease_key, None)]).await;

    fixture
        .coordinator
        .run_lease_taker()
        .await
        .expect("run_lease_taker");
    fixture
        .coordinator
        .run_lease_renewer()
        .await
        .expect("run_lease_renewer");
    let mut lease = fixture
        .coordinator
        .get_currently_held_lease(lease_key)
        .expect("held");

    // externally renew (bumps counter) — simulates concurrent update
    let mut held = fixture
        .coordinator
        .get_currently_held_lease(lease_key)
        .expect("held");
    fixture
        .refresher
        .renew_lease(&mut held)
        .await
        .expect("renew_lease");

    let new_checkpoint = ExtendedSequenceNumber::from_sequence_number("newCheckpoint");
    let token = lease.concurrency_token().expect("token");
    assert!(!set_checkpoint(&fixture.coordinator, lease_key, &new_checkpoint, token).await);

    let from_ddb = fixture
        .refresher
        .get_lease(lease_key)
        .await
        .unwrap()
        .unwrap();
    lease.set_lease_counter(lease.lease_counter() + 1);
    // counter + owner changed, checkpoint did not.
    lease.set_lease_owner(Some(fixture.coordinator.worker_identifier()));
    assert_eq!(lease, from_ddb);

    fixture.teardown().await;
}

/// testUpdateCheckpointBadConcurrencyToken — a wrong token fails the CAS; only
/// the owner (set by taker/renewer) differs from the freshly-built lease.
#[tokio::test(flavor = "multi_thread")]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_update_checkpoint_bad_concurrency_token() {
    common::init_test_tracing();
    let fixture = CoordinatorFixture::setup("coord-ckpt-badtoken").await;
    let lease_key = "shd-1";
    build_leases(&fixture.refresher, &[(lease_key, None)]).await;

    fixture
        .coordinator
        .run_lease_taker()
        .await
        .expect("run_lease_taker");
    fixture
        .coordinator
        .run_lease_renewer()
        .await
        .expect("run_lease_renewer");
    let mut lease = fixture
        .coordinator
        .get_currently_held_lease(lease_key)
        .expect("held");

    let new_checkpoint = ExtendedSequenceNumber::from_sequence_number("newCheckpoint");
    assert!(
        !set_checkpoint(
            &fixture.coordinator,
            lease_key,
            &new_checkpoint,
            Uuid::new_v4()
        )
        .await
    );

    let from_ddb = fixture
        .refresher
        .get_lease(lease_key)
        .await
        .unwrap()
        .unwrap();
    // Owner should be the only thing that changed vs the freshly-built lease.
    lease.set_lease_owner(Some(fixture.coordinator.worker_identifier()));
    assert_eq!(lease, from_ddb);

    fixture.teardown().await;
}
