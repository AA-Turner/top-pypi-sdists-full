// Tests for `LeaseGracefulShutdownHandler` (included from the handler module).
//
// Port of `LeaseGracefulShutdownHandlerTest`. Java mocks the `ShardConsumer`
// (Mockito) to verify `gracefulShutdown(null)` was called and to control
// `isShutdown()`. In the Rust port `ShardConsumer` is a real (unmockable) type,
// so we build a real consumer and observe its `shutdown_reason()` (set by
// `graceful_shutdown`). The `ScheduledExecutorService` `Runnable` capture is
// replaced by calling `monitor_graceful_shutdown_leases()` directly (the test
// seam). `getCurrentlyHeldLease` / `assignLease` are mocked on the coordinator /
// refresher.

use super::*;
use crate::checkpoint::in_memory_checkpointer::InMemoryCheckpointer;
use crate::checkpoint::ShardRecordProcessorCheckpointer;
use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended, StreamIdentifier};
use crate::leases::{
    HierarchicalShardSyncer, Lease, LeaseCleanupManager, MockLeaseCoordinator, MockLeaseRefresher,
    ShardInfo,
};
use crate::lifecycle::test_support::RecordingRecordsPublisher;
use crate::lifecycle::{
    KinesisConsumerTaskFactory, NoOpTaskExecutionListener, ShardConsumer, ShardConsumerArgument,
    ShutdownReason,
};
use crate::metrics::NullMetricsFactory;
use crate::processor::{Checkpointer, MockShardRecordProcessor, ShardRecordProcessor};
use crate::retrieval::AggregatorUtil;
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex as StdMutex};
use std::time::Duration;
use uuid::Uuid;

const WORKER_ID: &str = "workerId";
const SHUTDOWN_TIMEOUT: i64 = 5000;

fn create_lease(shard_id: &str, lease_owner: &str) -> Lease {
    let mut l = Lease::default();
    l.set_lease_key(shard_id.to_string());
    l.set_lease_owner(Some(lease_owner.to_string()));
    l
}

/// Build a real, minimal `ShardConsumer` for the given shard id.
async fn build_consumer(shard_id: &str) -> Arc<ShardConsumer> {
    let info = ShardInfo::single_stream(shard_id, Some("".to_string()), Vec::<String>::new(), None);

    let store: Arc<dyn Checkpointer + Send + Sync> = Arc::new(InMemoryCheckpointer::new());
    let checkpointer = ShardRecordProcessorCheckpointer::new(info.clone(), store.clone());

    let mut coord = MockLeaseCoordinator::new();
    coord
        .expect_lease_stats_recorder()
        .returning(|| Arc::new(crate::leases::LeaseStatsRecorder::new(60_000, Arc::new(|| 0i64) as crate::leases::lease_stats_recorder::TimeProvider)));
    coord.expect_get_currently_held_lease().returning(|_| None);
    coord.expect_worker_identifier().returning(|| WORKER_ID.to_string());
    coord.expect_drop_lease().returning(|_| {});
    let coord: Arc<dyn crate::leases::LeaseCoordinator + Send + Sync> = Arc::new(coord);

    let processor: Arc<StdMutex<Box<dyn ShardRecordProcessor + Send>>> =
        Arc::new(StdMutex::new(Box::new(MockShardRecordProcessor::new())));

    let mut detector = crate::leases::shard_detector::MockShardDetector::new();
    detector.expect_shard().returning(|_| Ok(None));
    let detector: Arc<dyn crate::leases::ShardDetector> = Arc::new(detector);

    let mut cleanup_coord = MockLeaseCoordinator::new();
    cleanup_coord.expect_get_currently_held_lease().returning(|_| None);
    let cleanup = Arc::new(LeaseCleanupManager::new(
        Arc::new(cleanup_coord),
        Arc::new(NullMetricsFactory),
        false,
        60_000,
        60_000,
        60_000,
    ));

    let argument = ShardConsumerArgument::new(
        info.clone(),
        StreamIdentifier::single_stream_instance("TestStream"),
        coord,
        Arc::new(RecordingRecordsPublisher::new()),
        processor,
        store,
        checkpointer,
        1000,
        500,
        true,
        50,
        10,
        true,
        1000,
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::TrimHorizon),
        true,
        false,
        detector,
        Arc::new(AggregatorUtil),
        Arc::new(HierarchicalShardSyncer::new()),
        Arc::new(NullMetricsFactory),
        cleanup,
    );

    ShardConsumer::new(
        Arc::new(RecordingRecordsPublisher::new()),
        info,
        None,
        argument,
        None,
        1,
        Arc::new(NoOpTaskExecutionListener),
        0,
        Arc::new(KinesisConsumerTaskFactory),
    )
    .await
}

/// A controllable coordinator for the handler: assign_lease counting, held-lease
/// toggling, worker id.
struct HandlerMocks {
    assign_calls: Arc<AtomicUsize>,
    held: Arc<AtomicBool>,
}

fn build_handler(
    time: Arc<StdMutex<i64>>,
    lease: Lease,
    consumer_map: ShardConsumerMap,
) -> (Arc<LeaseGracefulShutdownHandler>, HandlerMocks) {
    let assign_calls = Arc::new(AtomicUsize::new(0));
    let held = Arc::new(AtomicBool::new(true));

    let mut refresher = MockLeaseRefresher::new();
    {
        let ac = assign_calls.clone();
        refresher.expect_assign_lease().returning(move |_, _| {
            ac.fetch_add(1, Ordering::SeqCst);
            Ok(true)
        });
    }
    let refresher: Arc<dyn crate::leases::LeaseRefresher> = Arc::new(refresher);

    let mut coord = MockLeaseCoordinator::new();
    {
        let r = refresher.clone();
        coord.expect_lease_refresher().returning(move || r.clone());
    }
    coord.expect_worker_identifier().returning(|| WORKER_ID.to_string());
    {
        let lease = lease.clone();
        let held = held.clone();
        coord.expect_get_currently_held_lease().returning(move |_| {
            if held.load(Ordering::SeqCst) {
                Some(lease.clone())
            } else {
                None
            }
        });
    }
    let coord: Arc<dyn crate::leases::LeaseCoordinator + Send + Sync> = Arc::new(coord);

    let time_provider: TimeProvider = {
        let t = time.clone();
        Arc::new(move || *t.lock().unwrap())
    };

    // Use a very long check interval so the background poller task does not
    // auto-fire `monitor_graceful_shutdown_leases()` and race the explicit calls
    // the tests drive (tokio intervals fire once immediately at t=0 — harmless
    // here since `time` starts at 0 and no timeout is reached — but a 2000ms
    // periodic tick under CPU contention could double-count an assignment). This
    // only makes the poller dormant; it does not change any assertion. (Ported
    // from `SHUTDOWN_CHECK_INTERVAL_MILLIS`.)
    let handler = LeaseGracefulShutdownHandler::new(
        SHUTDOWN_TIMEOUT,
        consumer_map,
        coord,
        time_provider,
        Duration::from_secs(3600),
    );
    (handler, HandlerMocks { assign_calls, held })
}

#[tokio::test(flavor = "multi_thread")]
async fn subsequent_starts_and_stops_are_idempotent() {
    let time = Arc::new(StdMutex::new(0));
    let lease = create_lease("shardId-0", "leaseOwner");
    let map: ShardConsumerMap = Arc::new(StdMutex::new(HashMap::new()));
    let (handler, _mocks) = build_handler(time, lease, map);

    handler.start();
    assert!(handler.is_running());
    handler.start(); // no-op
    assert!(handler.is_running());
    handler.stop();
    assert!(!handler.is_running());
    handler.stop(); // no-op
    assert!(!handler.is_running());
}

#[tokio::test(flavor = "multi_thread")]
async fn enqueue_calls_graceful_shutdown_once() {
    let time = Arc::new(StdMutex::new(0));
    let mut lease = create_lease("shardId-0", "leaseOwner");
    lease.set_checkpoint_owner(Some(WORKER_ID.to_string()));
    lease.set_concurrency_token(Uuid::new_v4());

    let consumer = build_consumer("shardId-0").await;
    let shard_info = DynamoDBLeaseCoordinator::convert_lease_to_assignment(&lease);
    let map: ShardConsumerMap = Arc::new(StdMutex::new(HashMap::new()));
    map.lock().unwrap().insert(shard_info, consumer.clone());

    let (handler, _mocks) = build_handler(time, lease.clone(), map);
    handler.start();

    handler.enqueue_shutdown(Some(&lease)).await;
    // graceful shutdown recorded REQUESTED.
    assert_eq!(consumer.shutdown_reason().await, Some(ShutdownReason::Requested));
    assert_eq!(handler.pending_shutdown_count(), 1);

    // Enqueuing the same lease again is a no-op (still one tracker).
    handler.enqueue_shutdown(Some(&lease)).await;
    assert_eq!(handler.pending_shutdown_count(), 1);
}

#[tokio::test(flavor = "multi_thread")]
async fn enqueue_second_independent_lease_shuts_down_its_own_consumer() {
    // Port of the second-lease/independent-tracker sub-case of
    // `testIgnoreDuplicatEnqueues`: adding a *second* lease (a different shard id,
    // its own consumer) enqueues independently and initiates graceful shutdown on
    // that consumer. (The duplicate-enqueue-is-idempotent sub-case is covered by
    // `enqueue_calls_graceful_shutdown_once`.)
    let time = Arc::new(StdMutex::new(0));

    let mut lease1 = create_lease("shardId-0", "leaseOwner");
    lease1.set_checkpoint_owner(Some(WORKER_ID.to_string()));
    lease1.set_concurrency_token(Uuid::new_v4());

    let consumer1 = build_consumer("shardId-0").await;
    let shard_info1 = DynamoDBLeaseCoordinator::convert_lease_to_assignment(&lease1);
    let map: ShardConsumerMap = Arc::new(StdMutex::new(HashMap::new()));
    map.lock().unwrap().insert(shard_info1, consumer1.clone());

    // A second, independent lease with its own consumer registered in the map.
    let mut lease2 = create_lease("shardId-2", "leaseOwner");
    lease2.set_checkpoint_owner(Some(WORKER_ID.to_string()));
    lease2.set_concurrency_token(Uuid::new_v4());
    let consumer2 = build_consumer("shardId-2").await;
    let shard_info2 = DynamoDBLeaseCoordinator::convert_lease_to_assignment(&lease2);
    map.lock().unwrap().insert(shard_info2, consumer2.clone());

    let (handler, _mocks) = build_handler(time, lease1.clone(), map);
    handler.start();

    handler.enqueue_shutdown(Some(&lease1)).await;
    assert_eq!(consumer1.shutdown_reason().await, Some(ShutdownReason::Requested));
    assert_eq!(handler.pending_shutdown_count(), 1);

    // Enqueuing the second lease initiates graceful shutdown on *its* consumer and
    // tracks it independently (two pending trackers now).
    handler.enqueue_shutdown(Some(&lease2)).await;
    assert_eq!(consumer2.shutdown_reason().await, Some(ShutdownReason::Requested));
    assert_eq!(handler.pending_shutdown_count(), 2);
}

#[tokio::test(flavor = "multi_thread")]
async fn not_enqueued_because_no_shard_consumer_found() {
    // Port of `testNotEnqueueBecauseNoShardConsumerFound`: a shutdown-requested
    // lease whose consumer is NOT in the map is not enqueued and never triggers a
    // lease assignment. The stale-tracker cleanup path is taken and no tracker is
    // recorded.
    let time = Arc::new(StdMutex::new(0));
    let mut lease = create_lease("shardId-0", "leaseOwner");
    lease.set_checkpoint_owner(Some(WORKER_ID.to_string()));
    lease.set_concurrency_token(Uuid::new_v4());

    // Empty consumer map -> no consumer for this lease's shard info.
    let map: ShardConsumerMap = Arc::new(StdMutex::new(HashMap::new()));
    let (handler, mocks) = build_handler(time, lease.clone(), map);
    handler.start();

    handler.enqueue_shutdown(Some(&lease)).await;
    assert_eq!(handler.pending_shutdown_count(), 0);
    assert_eq!(mocks.assign_calls.load(Ordering::SeqCst), 0);
}

#[tokio::test(flavor = "multi_thread")]
async fn ignore_non_pending_shutdown_lease() {
    let time = Arc::new(StdMutex::new(0));
    // A lease with no checkpoint owner is NOT shutdownRequested.
    let lease = create_lease("shardId-0", "leaseOwner");
    let map: ShardConsumerMap = Arc::new(StdMutex::new(HashMap::new()));
    let (handler, mocks) = build_handler(time, lease.clone(), map);
    handler.start();

    handler.enqueue_shutdown(Some(&lease)).await;
    assert_eq!(handler.pending_shutdown_count(), 0);
    assert_eq!(mocks.assign_calls.load(Ordering::SeqCst), 0);
}

#[tokio::test(flavor = "multi_thread")]
async fn assign_lease_called_when_timeout_reached() {
    let time = Arc::new(StdMutex::new(0));
    let mut lease = create_lease("shardId-0", "leaseOwner");
    lease.set_checkpoint_owner(Some(WORKER_ID.to_string()));
    lease.set_concurrency_token(Uuid::new_v4());

    let consumer = build_consumer("shardId-0").await;
    let shard_info = DynamoDBLeaseCoordinator::convert_lease_to_assignment(&lease);
    let map: ShardConsumerMap = Arc::new(StdMutex::new(HashMap::new()));
    map.lock().unwrap().insert(shard_info.clone(), consumer.clone());

    let (handler, mocks) = build_handler(time.clone(), lease.clone(), map);
    handler.start();
    handler.enqueue_shutdown(Some(&lease)).await;

    // Timeout << SHUTDOWN_TIMEOUT: no assign.
    handler.monitor_graceful_shutdown_leases().await;
    assert_eq!(mocks.assign_calls.load(Ordering::SeqCst), 0);

    // Timeout < SHUTDOWN_TIMEOUT: still no assign.
    *time.lock().unwrap() = SHUTDOWN_TIMEOUT - 1000;
    handler.monitor_graceful_shutdown_leases().await;
    assert_eq!(mocks.assign_calls.load(Ordering::SeqCst), 0);

    // Timeout > SHUTDOWN_TIMEOUT: assign is called, transfer marked so it does
    // not repeat on subsequent ticks.
    *time.lock().unwrap() = SHUTDOWN_TIMEOUT + 1000;
    handler.monitor_graceful_shutdown_leases().await;
    assert_eq!(mocks.assign_calls.load(Ordering::SeqCst), 1);
    assert!(handler.lease_transfer_called(&shard_info));

    // A subsequent tick does NOT re-attempt the transfer.
    handler.monitor_graceful_shutdown_leases().await;
    assert_eq!(mocks.assign_calls.load(Ordering::SeqCst), 1);
}

#[tokio::test(flavor = "multi_thread")]
async fn remove_tracker_when_lease_no_longer_held() {
    let time = Arc::new(StdMutex::new(0));
    let mut lease = create_lease("shardId-0", "leaseOwner");
    lease.set_checkpoint_owner(Some(WORKER_ID.to_string()));
    lease.set_concurrency_token(Uuid::new_v4());

    let consumer = build_consumer("shardId-0").await;
    let shard_info = DynamoDBLeaseCoordinator::convert_lease_to_assignment(&lease);
    let map: ShardConsumerMap = Arc::new(StdMutex::new(HashMap::new()));
    map.lock().unwrap().insert(shard_info, consumer.clone());

    // Time out the shutdown, but pretend we no longer hold the lease.
    *time.lock().unwrap() = SHUTDOWN_TIMEOUT + 1000;
    let (handler, mocks) = build_handler(time, lease.clone(), map);
    mocks.held.store(false, Ordering::SeqCst);
    handler.start();
    handler.enqueue_shutdown(Some(&lease)).await;

    handler.monitor_graceful_shutdown_leases().await;
    // Not owned anymore → no assign; tracker removed (success path).
    assert_eq!(mocks.assign_calls.load(Ordering::SeqCst), 0);
    assert_eq!(handler.pending_shutdown_count(), 0);
}

#[tokio::test(flavor = "multi_thread")]
async fn assign_not_called_if_checkpoint_owner_is_different_worker() {
    let time = Arc::new(StdMutex::new(0));
    let mut lease = create_lease("shardId-0", "leaseOwner");
    lease.set_checkpoint_owner(Some("random_owner".to_string()));
    lease.set_concurrency_token(Uuid::new_v4());

    let consumer = build_consumer("shardId-0").await;
    let shard_info = DynamoDBLeaseCoordinator::convert_lease_to_assignment(&lease);
    let map: ShardConsumerMap = Arc::new(StdMutex::new(HashMap::new()));
    map.lock().unwrap().insert(shard_info, consumer.clone());

    let (handler, mocks) = build_handler(time.clone(), lease.clone(), map);
    handler.start();
    handler.enqueue_shutdown(Some(&lease)).await;

    // Time out; but checkpoint owner mismatches WORKER_ID → attempt_lease_transfer
    // logs a warning and does NOT assign.
    *time.lock().unwrap() = SHUTDOWN_TIMEOUT + 1000;
    handler.monitor_graceful_shutdown_leases().await;
    assert_eq!(mocks.assign_calls.load(Ordering::SeqCst), 0);
}
