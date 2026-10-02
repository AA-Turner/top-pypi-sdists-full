//! Behavioral tests for the DDB-lock leader decider + the reimplemented lock.
//!
//! The Java `DynamoDBLockBasedLeaderDeciderTest` uses DynamoDBEmbedded (a real
//! in-process DB) for true CAS semantics — not portable to `aws-smithy-mocks`
//! (see WAVE-PLAN TEST-PARITY GAPS). These tests instead exercise the
//! reimplemented lock algorithm + the decider's control flow with a mocked DDB
//! client (`aws-smithy-mocks`) and a mocked `TableMigrationStateMachine`,
//! covering: acquire, renew, steal-after-lease, release, isLeader transitions,
//! the shutdown short-circuit, the false-result debounce, the always-called
//! `handleLeaderLockResult`, and the Dependency-exception force-release path.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use aws_sdk_dynamodb::operation::delete_item::{DeleteItemError, DeleteItemOutput};
use aws_sdk_dynamodb::operation::get_item::GetItemOutput;
use aws_sdk_dynamodb::operation::put_item::{PutItemError, PutItemOutput};
use aws_sdk_dynamodb::types::error::ConditionalCheckFailedException;
use aws_sdk_dynamodb::types::AttributeValue;
use aws_sdk_dynamodb::Client;
use aws_smithy_mocks::{mock, mock_client, MockResponse, RuleMode};

use super::*;
use crate::coordinator::coordinator_config::CoordinatorConfig;
use crate::coordinator::migration::table_migration_state_machine::MockTableMigrationStateMachine;
use crate::coordinator::migration::{DefaultTableMigrationStatusProvider, TableMigrationStatus};
use crate::leader::ddb_lock::{DdbLockClient, LEASE_DURATION, OWNER_NAME, RECORD_VERSION_NUMBER};
use crate::metrics::NullMetricsFactory;

const PK: &str = "leaseKey";
const KEY: &str = "Leader";
const TABLE: &str = "leaseTable";

fn lock_item(owner: &str, rvn: &str, lease_ms: i64) -> HashMap<String, AttributeValue> {
    let mut m = HashMap::new();
    m.insert(PK.to_string(), AttributeValue::S(KEY.to_string()));
    m.insert(OWNER_NAME.to_string(), AttributeValue::S(owner.to_string()));
    m.insert(
        RECORD_VERSION_NUMBER.to_string(),
        AttributeValue::S(rvn.to_string()),
    );
    m.insert(
        LEASE_DURATION.to_string(),
        AttributeValue::S(lease_ms.to_string()),
    );
    m
}

fn cond_failed_put() -> PutItemError {
    PutItemError::ConditionalCheckFailedException(
        ConditionalCheckFailedException::builder().build(),
    )
}

// -------- DdbLockClient direct tests --------

#[tokio::test]
async fn acquire_absent_lock_succeeds() {
    // getLock -> empty; putItem (claim) -> ok.
    let get = mock!(Client::get_item).then_output(|| GetItemOutput::builder().build());
    let put = mock!(Client::put_item).then_output(|| PutItemOutput::builder().build());
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::Sequential, &[&get, &put]);

    let lock = DdbLockClient::new(client, TABLE, PK, "worker1", 100);
    let acquired = lock.try_acquire_lock(KEY, &HashMap::new()).await.unwrap();
    assert!(acquired, "should acquire an absent lock");
}

#[tokio::test]
async fn acquire_absent_lock_race_returns_false() {
    // getLock -> empty; putItem (claim) -> ConditionalCheckFailed (someone won the race).
    let get = mock!(Client::get_item).then_output(|| GetItemOutput::builder().build());
    let put = mock!(Client::put_item).then_error(cond_failed_put);
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::Sequential, &[&get, &put]);

    let lock = DdbLockClient::new(client, TABLE, PK, "worker1", 100);
    let acquired = lock.try_acquire_lock(KEY, &HashMap::new()).await.unwrap();
    assert!(!acquired, "losing the race should not acquire");
}

#[tokio::test]
async fn renew_own_lock_succeeds() {
    // getLock -> lock owned by us; putItem (renew with fresh RVN) -> ok.
    let item = lock_item("worker1", "rvn-1", 100);
    let get = mock!(Client::get_item).then_output(move || {
        GetItemOutput::builder()
            .set_item(Some(item.clone()))
            .build()
    });
    let put = mock!(Client::put_item).then_output(|| PutItemOutput::builder().build());
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::Sequential, &[&get, &put]);

    let lock = DdbLockClient::new(client, TABLE, PK, "worker1", 100);
    let acquired = lock.try_acquire_lock(KEY, &HashMap::new()).await.unwrap();
    assert!(acquired, "owner should renew its own lock");
}

#[tokio::test]
async fn foreign_lock_not_stolen_before_lease_elapses() {
    // Two getLock calls (each try_acquire re-reads); RVN unchanged but not enough time passed.
    let item = lock_item("otherWorker", "rvn-1", 100);
    let get1 = mock!(Client::get_item)
        .match_requests(|_| true)
        .sequence()
        .output(move || {
            GetItemOutput::builder()
                .set_item(Some(item.clone()))
                .build()
        })
        .repeatedly()
        .build();
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &[&get1]);

    // Clock fixed: no time elapses between calls.
    let base = Instant::now();
    let clock: LockClock = Arc::new(move || base);
    let lock = DdbLockClient::new(client, TABLE, PK, "worker1", 100).with_clock(clock);

    // First call: observe the foreign RVN, do not acquire.
    assert!(!lock.try_acquire_lock(KEY, &HashMap::new()).await.unwrap());
    // Second call at same instant: still not stealable.
    assert!(!lock.try_acquire_lock(KEY, &HashMap::new()).await.unwrap());
}

#[tokio::test]
async fn foreign_lock_stolen_after_lease_elapses() {
    // getLock repeatedly returns the same foreign RVN; putItem (steal) -> ok.
    let item = lock_item("otherWorker", "rvn-1", 100);
    let get = mock!(Client::get_item)
        .match_requests(|_| true)
        .sequence()
        .output(move || {
            GetItemOutput::builder()
                .set_item(Some(item.clone()))
                .build()
        })
        .repeatedly()
        .build();
    let put = mock!(Client::put_item).then_output(|| PutItemOutput::builder().build());
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &[&get, &put]);

    // Test-controlled clock: held at t0 for the first try_acquire (both internal
    // reads see t0), then advanced by 200ms (> 100ms lease) for the second.
    let base = Instant::now();
    let offset_ms = Arc::new(Mutex::new(0u64));
    let clock: LockClock = {
        let offset_ms = offset_ms.clone();
        Arc::new(move || base + Duration::from_millis(*offset_ms.lock().unwrap()))
    };
    let lock = DdbLockClient::new(client, TABLE, PK, "worker1", 100).with_clock(clock);

    // First call records observation at t0, does not steal.
    assert!(!lock.try_acquire_lock(KEY, &HashMap::new()).await.unwrap());
    // Advance past the lease, then the second call steals (RVN unchanged).
    *offset_ms.lock().unwrap() = 200;
    assert!(lock.try_acquire_lock(KEY, &HashMap::new()).await.unwrap());
}

#[tokio::test]
async fn release_owned_lock_deletes() {
    let item = lock_item("worker1", "rvn-1", 100);
    let get = mock!(Client::get_item).then_output(move || {
        GetItemOutput::builder()
            .set_item(Some(item.clone()))
            .build()
    });
    let del = mock!(Client::delete_item).then_output(|| DeleteItemOutput::builder().build());
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::Sequential, &[&get, &del]);

    // is not expired: fixed clock.
    let base = Instant::now();
    let clock: LockClock = Arc::new(move || base);
    let lock = DdbLockClient::new(client, TABLE, PK, "worker1", 100).with_clock(clock);

    let item = lock.get_lock(KEY).await.unwrap().unwrap();
    lock.release_lock(KEY, &item).await.unwrap();
}

// -------- Decider control-flow tests --------

fn make_dao(client: Client) -> Arc<CoordinatorStateDao> {
    let cfg = CoordinatorConfig::new("TestApp");
    let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
    // Route lock to the lease table (COMPLETE) & mark DAO initialized-for-writes.
    provider.initialize(false, TableMigrationStatus::Complete);
    let dao = CoordinatorStateDao::new(
        client,
        cfg.coordinator_state_table_config(),
        TABLE,
        provider,
    );
    let _ = dao.initialize();
    Arc::new(dao)
}

fn factory() -> Arc<dyn MetricsFactory + Send + Sync> {
    Arc::new(NullMetricsFactory::new())
}

#[tokio::test]
async fn is_leader_acquires_and_invokes_handle_leader_lock_result_true() {
    let get = mock!(Client::get_item).then_output(|| GetItemOutput::builder().build());
    let put = mock!(Client::put_item).then_output(|| PutItemOutput::builder().build());
    let client = mock_client!(
        aws_sdk_dynamodb,
        RuleMode::MatchAny,
        &[
            &mock!(Client::get_item)
                .match_requests(|_| true)
                .sequence()
                .output(|| GetItemOutput::builder().build())
                .repeatedly()
                .build(),
            &mock!(Client::put_item)
                .match_requests(|_| true)
                .sequence()
                .output(|| PutItemOutput::builder().build())
                .repeatedly()
                .build(),
        ]
    );
    let _ = (get, put);

    let dao = make_dao(client);
    let mut sm = MockTableMigrationStateMachine::new();
    sm.expect_handle_leader_lock_result()
        .withf(|is_leader| *is_leader)
        .times(1)
        .returning(|_| Ok(()));

    let decider =
        DynamoDBLockBasedLeaderDecider::create(dao, "worker1", 100, 10, factory(), Arc::new(sm));
    assert!(
        decider.is_leader_async("worker1").await,
        "should acquire and be leader"
    );
}

#[tokio::test]
async fn is_leader_present_valid_owned_by_us_true() {
    let item = lock_item("worker1", "rvn-1", 100_000);
    let get = mock!(Client::get_item)
        .match_requests(|_| true)
        .sequence()
        .output(move || {
            GetItemOutput::builder()
                .set_item(Some(item.clone()))
                .build()
        })
        .repeatedly()
        .build();
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &[&get]);

    let dao = make_dao(client);
    let mut sm = MockTableMigrationStateMachine::new();
    sm.expect_handle_leader_lock_result()
        .withf(|is_leader| *is_leader)
        .returning(|_| Ok(()));

    // Large lease so the lock isn't considered expired between lookup and check.
    let decider =
        DynamoDBLockBasedLeaderDecider::create(dao, "worker1", 10, 10, factory(), Arc::new(sm));
    assert!(decider.is_leader_async("worker1").await);
}

#[tokio::test]
async fn is_leader_present_valid_owned_by_other_false() {
    let item = lock_item("otherWorker", "rvn-1", 100_000);
    let get = mock!(Client::get_item)
        .match_requests(|_| true)
        .sequence()
        .output(move || {
            GetItemOutput::builder()
                .set_item(Some(item.clone()))
                .build()
        })
        .repeatedly()
        .build();
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &[&get]);

    let dao = make_dao(client);
    let mut sm = MockTableMigrationStateMachine::new();
    sm.expect_handle_leader_lock_result()
        .withf(|is_leader| !*is_leader)
        .times(1)
        .returning(|_| Ok(()));

    let decider =
        DynamoDBLockBasedLeaderDecider::create(dao, "worker1", 10, 10, factory(), Arc::new(sm));
    assert!(!decider.is_leader_async("worker1").await);
}

#[tokio::test]
async fn is_leader_shutdown_short_circuits_false() {
    let get = mock!(Client::get_item)
        .match_requests(|_| true)
        .sequence()
        .output(|| GetItemOutput::builder().build())
        .repeatedly()
        .build();
    let del = mock!(Client::delete_item)
        .match_requests(|_| true)
        .sequence()
        .output(|| DeleteItemOutput::builder().build())
        .repeatedly()
        .build();
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &[&get, &del]);

    let dao = make_dao(client);
    let sm = MockTableMigrationStateMachine::new(); // never called after shutdown

    let decider =
        DynamoDBLockBasedLeaderDecider::create(dao, "worker1", 100, 10, factory(), Arc::new(sm));
    decider.shutdown_async().await;
    assert!(
        !decider.is_leader_async("worker1").await,
        "should return false after shutdown"
    );
}

#[tokio::test]
async fn is_leader_false_result_debounced_within_heartbeat_window() {
    // Foreign lock present & valid -> false. Then within heartbeat window,
    // a second call must be cached (no extra DDB / handleLeaderLockResult).
    let item = lock_item("otherWorker", "rvn-1", 100_000);
    let get = mock!(Client::get_item)
        .match_requests(|_| true)
        .sequence()
        .output(move || {
            GetItemOutput::builder()
                .set_item(Some(item.clone()))
                .build()
        })
        .repeatedly()
        .build();
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &[&get]);

    let dao = make_dao(client);
    let mut sm = MockTableMigrationStateMachine::new();
    // Only ONE call — the second is debounced.
    sm.expect_handle_leader_lock_result()
        .times(1)
        .returning(|_| Ok(()));

    // Frozen clock so the debounce window never elapses.
    let clock: Arc<dyn Fn() -> i64 + Send + Sync> = Arc::new(|| 1_000);
    let lock_clock: LockClock = Arc::new(Instant::now);
    let decider =
        DynamoDBLockBasedLeaderDecider::create(dao, "worker1", 100, 10, factory(), Arc::new(sm))
            .with_clocks(clock, lock_clock);

    assert!(!decider.is_leader_async("worker1").await);
    // Second call within window -> cached false, no DDB, no SM call.
    assert!(!decider.is_leader_async("worker1").await);
}

#[tokio::test]
async fn is_leader_handle_leader_lock_result_dependency_forces_false_and_releases() {
    // Acquire succeeds -> response true; handleLeaderLockResult throws Dependency
    // -> release + return false.
    let get = mock!(Client::get_item)
        .match_requests(|_| true)
        .sequence()
        .output(|| GetItemOutput::builder().build())
        .repeatedly()
        .build();
    let put = mock!(Client::put_item)
        .match_requests(|_| true)
        .sequence()
        .output(|| PutItemOutput::builder().build())
        .repeatedly()
        .build();
    let del = mock!(Client::delete_item)
        .match_requests(|_| true)
        .sequence()
        .output(|| DeleteItemOutput::builder().build())
        .repeatedly()
        .build();
    let client = mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &[&get, &put, &del]);

    let dao = make_dao(client);
    let mut sm = MockTableMigrationStateMachine::new();
    sm.expect_handle_leader_lock_result().returning(|_| {
        Err(
            crate::coordinator::migration::TableMigrationError::Dependency(
                crate::leases::exceptions::LeasingError::dependency("boom"),
            ),
        )
    });

    let decider =
        DynamoDBLockBasedLeaderDecider::create(dao, "worker1", 100, 10, factory(), Arc::new(sm));
    assert!(
        !decider.is_leader_async("worker1").await,
        "Dependency from handleLeaderLockResult forces false"
    );
}

// -------- Shared in-memory lock table (DynamoDBEmbedded stand-in) --------

/// A single-item, thread-safe in-memory lock table shared by several
/// `DdbLockClient`s, reproducing the DynamoDB conditional-write CAS semantics
/// the decider relies on. The Java test uses a real `DynamoDBEmbedded` table so
/// multiple workers' lock clients operate against the *same* lock row; this
/// store gives the same shared-state behavior without a real DB.
#[derive(Clone, Default)]
struct SharedLockTable {
    /// The single lock row (keyed by the `Leader` hash key), or `None` if absent.
    item: Arc<Mutex<Option<HashMap<String, AttributeValue>>>>,
}

impl SharedLockTable {
    fn s(item: &HashMap<String, AttributeValue>, attr: &str) -> Option<String> {
        item.get(attr).and_then(|v| v.as_s().ok()).cloned()
    }

    /// Build a mock DDB `Client` backed by this shared table. Every client built
    /// this way shares the same underlying row, so two deciders race for the same
    /// lock exactly like the Java `DynamoDBEmbedded` workers do.
    fn client(&self) -> Client {
        let get_store = self.item.clone();
        let get = mock!(Client::get_item).then_compute_response(move |_req| {
            let store = get_store.lock().unwrap_or_else(|e| e.into_inner());
            let mut out = GetItemOutput::builder();
            if let Some(item) = store.as_ref() {
                out = out.set_item(Some(item.clone()));
            }
            MockResponse::Output(out.build())
        });

        let put_store = self.item.clone();
        let put = mock!(Client::put_item).then_compute_response(move |req| {
            let mut store = put_store.lock().unwrap_or_else(|e| e.into_inner());
            let cond = req.condition_expression();
            let new_item = req.item().cloned().unwrap_or_default();
            let ok = match cond {
                // Claim an absent lock: succeeds only when the row is absent.
                Some(c) if c.contains("attribute_not_exists") => store.is_none(),
                // Steal/renew: succeeds only when the current RVN matches :expected.
                Some(c) if c.contains("#rvn") => {
                    let expected = req
                        .expression_attribute_values()
                        .and_then(|m| m.get(":expected"))
                        .and_then(|v| v.as_s().ok())
                        .cloned();
                    store
                        .as_ref()
                        .and_then(|it| Self::s(it, RECORD_VERSION_NUMBER))
                        == expected
                }
                // Unconditional put (not exercised by the lock client) — accept.
                _ => true,
            };
            if ok {
                *store = Some(new_item);
                MockResponse::Output(PutItemOutput::builder().build())
            } else {
                MockResponse::Error(cond_failed_put())
            }
        });

        let del_store = self.item.clone();
        let del = mock!(Client::delete_item).then_compute_response(move |req| {
            let mut store = del_store.lock().unwrap_or_else(|e| e.into_inner());
            // Guarded by `#owner = :owner AND #rvn = :rvn`.
            let want_owner = req
                .expression_attribute_values()
                .and_then(|m| m.get(":owner"))
                .and_then(|v| v.as_s().ok())
                .cloned();
            let want_rvn = req
                .expression_attribute_values()
                .and_then(|m| m.get(":rvn"))
                .and_then(|v| v.as_s().ok())
                .cloned();
            let matches = store.as_ref().is_some_and(|it| {
                Self::s(it, OWNER_NAME) == want_owner
                    && Self::s(it, RECORD_VERSION_NUMBER) == want_rvn
            });
            if matches {
                *store = None;
                MockResponse::Output(DeleteItemOutput::builder().build())
            } else {
                MockResponse::Error(DeleteItemError::ConditionalCheckFailedException(
                    ConditionalCheckFailedException::builder().build(),
                ))
            }
        });

        mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &[&get, &put, &del])
    }
}

/// Port of `isLeader_doesNotReleaseExistingLockWithMatchingVersionHash`.
///
/// Java uses `DynamoDBEmbedded` with 10 workers sharing a lock table; here a
/// [`SharedLockTable`] gives two deciders (worker1, worker2) the same shared
/// lock row. Once worker1 holds the lock, worker2 checking leadership must NOT
/// release worker1's lock (the normal not-leader path never releases another
/// worker's lock — only the exception path does), and worker1 stays leader.
///
/// `start_paused` freezes time so the lock never expires mid-test and the
/// heartbeat debounce window never elapses (deterministic, non-flaky).
#[tokio::test(start_paused = true)]
async fn is_leader_does_not_release_existing_lock_with_matching_version_hash() {
    let table = SharedLockTable::default();

    // Two deciders sharing the same lock table (each with its own DAO, as in Java).
    // Frozen clocks: the lock clock never advances (no expiry) and the debounce
    // millis-clock is fixed so worker2's false result is recomputed each call.
    let frozen_lock: LockClock = {
        let base = Instant::now();
        Arc::new(move || base)
    };
    let frozen_millis: Arc<dyn Fn() -> i64 + Send + Sync> = Arc::new(|| 1_000);

    let sm1 = MockTableMigrationStateMachine::new();
    let mut sm1 = sm1;
    sm1.expect_handle_leader_lock_result().returning(|_| Ok(()));
    let decider1 = DynamoDBLockBasedLeaderDecider::create(
        make_dao(table.client()),
        "worker1",
        100,
        10,
        factory(),
        Arc::new(sm1),
    )
    .with_clocks(frozen_millis.clone(), frozen_lock.clone());

    let mut sm2 = MockTableMigrationStateMachine::new();
    sm2.expect_handle_leader_lock_result().returning(|_| Ok(()));
    let decider2 = DynamoDBLockBasedLeaderDecider::create(
        make_dao(table.client()),
        "worker2",
        100,
        10,
        factory(),
        Arc::new(sm2),
    )
    .with_clocks(frozen_millis, frozen_lock);

    // worker1 acquires the lock first.
    assert!(
        decider1.is_leader_async("worker1").await,
        "worker1 should acquire the lock"
    );

    // worker2 checks leadership: it sees worker1's valid lock, is not leader, and
    // must NOT release worker1's lock.
    assert!(
        !decider2.is_leader_async("worker2").await,
        "worker2 must not become leader"
    );

    // The lock row still exists and is still owned by worker1.
    {
        let item = table.item.lock().unwrap();
        let item = item.as_ref().expect("worker1's lock must still be present");
        assert_eq!(
            SharedLockTable::s(item, OWNER_NAME).as_deref(),
            Some("worker1")
        );
    }

    // worker1 remains leader (its lock was never released by worker2).
    assert!(
        decider1.is_leader_async("worker1").await,
        "worker1 should still be leader"
    );
}
