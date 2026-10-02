//! Behavioral tests for [`FanOutRecordsPublisher`], ported from
//! `FanOutRecordsPublisherTest` (the deterministic subset).
//!
//! The RxJava-scheduler / executor-threading tests
//! (`testIfAllEventsReceivedWhenNoTasksRejectedByExecutor`,
//! `testIfStreamOfEvents...WithBackpressureAdheringServicePublisher*`,
//! `testNoDeadlock*`) are **not** ported: they exercise Java's `Flowable` +
//! `Schedulers.computation()` + mocked-`ExecutorService` machinery with no Rust
//! analog. Their load-bearing behaviors (in-order delivery under backpressure,
//! resubscribe-on-complete, shard-end onComplete, mid-stream onError, burst-limit
//! overflow) are covered here by driving the state machine deterministically via
//! an injected [`TestSubscriber`].

use std::sync::{Arc, Mutex};

use tokio::sync::mpsc;

use super::*;
use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended, StreamIdentifier};
use crate::retrieval::records_delivery_ack::SimpleRecordsDeliveryAck;
use aws_sdk_kinesis::types::{ChildShard, Record, SubscribeToShardEvent};
use aws_smithy_types::Blob;

const SHARD_ID: &str = "Shard-001";

/// A test [`ShardSubscriber`] that records subscribe/request/cancel calls and
/// exposes the per-flow event sender so the test can inject [`FlowEvent`]s.
struct TestSubscriber {
    inner: Mutex<TestSubInner>,
    request_count: Arc<Mutex<usize>>,
}

struct TestSubInner {
    // The event sender the publisher task listens on (captured on subscribe).
    events: Option<mpsc::UnboundedSender<FlowEvent>>,
    last_flow_id: Option<u64>,
    cancelled: Vec<u64>,
    /// One record per `subscribe` call: (sequence_number, is_first_connection).
    subscribe_calls: Vec<(ExtendedSequenceNumber, bool)>,
}

impl TestSubscriber {
    fn new() -> Arc<Self> {
        Arc::new(Self {
            inner: Mutex::new(TestSubInner {
                events: None,
                last_flow_id: None,
                cancelled: Vec::new(),
                subscribe_calls: Vec::new(),
            }),
            request_count: Arc::new(Mutex::new(0)),
        })
    }

    fn events(&self) -> mpsc::UnboundedSender<FlowEvent> {
        self.inner
            .lock()
            .unwrap()
            .events
            .clone()
            .expect("subscribed")
    }

    fn flow_id(&self) -> u64 {
        self.inner.lock().unwrap().last_flow_id.expect("subscribed")
    }

    fn request_count(&self) -> usize {
        *self.request_count.lock().unwrap()
    }

    fn cancelled(&self) -> Vec<u64> {
        self.inner.lock().unwrap().cancelled.clone()
    }

    fn subscribe_calls(&self) -> Vec<(ExtendedSequenceNumber, bool)> {
        self.inner.lock().unwrap().subscribe_calls.clone()
    }
}

#[async_trait::async_trait]
impl ShardSubscriber for TestSubscriber {
    async fn subscribe(
        &self,
        flow_id: u64,
        sequence_number: ExtendedSequenceNumber,
        is_first_connection: bool,
        _initial_position: InitialPositionInStreamExtended,
        events: mpsc::UnboundedSender<FlowEvent>,
    ) {
        let mut inner = self.inner.lock().unwrap();
        inner.events = Some(events);
        inner.last_flow_id = Some(flow_id);
        inner
            .subscribe_calls
            .push((sequence_number, is_first_connection));
    }

    fn request_next(&self, _flow_id: u64) {
        *self.request_count.lock().unwrap() += 1;
    }

    fn cancel(&self, flow_id: u64) {
        self.inner.lock().unwrap().cancelled.push(flow_id);
    }
}

fn make_record(seq: &str) -> Record {
    Record::builder()
        .sequence_number(seq)
        .partition_key("A")
        .data(Blob::new(b"data".to_vec()))
        .build()
        .unwrap()
}

fn event_with_records(seqs: &[&str], continuation: Option<&str>) -> SubscribeToShardEvent {
    let mut b = SubscribeToShardEvent::builder().millis_behind_latest(100);
    for s in seqs {
        b = b.records(make_record(s));
    }
    if let Some(c) = continuation {
        b = b.continuation_sequence_number(c);
    }
    b.build().unwrap()
}

fn shard_end_event(seqs: &[&str]) -> SubscribeToShardEvent {
    // continuationSequenceNumber = "" (Rust SDK's non-nullable analog of Java's
    // null) + non-empty childShards => shard end.
    let mut b = SubscribeToShardEvent::builder()
        .continuation_sequence_number("")
        .millis_behind_latest(0);
    for s in seqs {
        b = b.records(make_record(s));
    }
    let left = ChildShard::builder()
        .shard_id("Shard-002")
        .parent_shards(SHARD_ID)
        .build()
        .unwrap();
    b.child_shards(left).build().unwrap()
}

fn latest_position() -> InitialPositionInStreamExtended {
    InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest)
}

fn build_publisher(sub: Arc<TestSubscriber>) -> Arc<FanOutRecordsPublisher> {
    Arc::new(FanOutRecordsPublisher::with_subscriber(
        sub,
        SHARD_ID.to_string(),
    ))
}

fn stream_id() -> StreamIdentifier {
    StreamIdentifier::single_stream_instance("test-stream")
}

/// Drive the subscribe→start handshake and return the flow id.
async fn start_and_subscribe(
    publisher: &Arc<FanOutRecordsPublisher>,
    sub: &Arc<TestSubscriber>,
    start_seq: ExtendedSequenceNumber,
) -> RecordsPublisherSubscription {
    let subscription = publisher.subscribe();
    publisher.start(start_seq, latest_position()).await.unwrap();
    // Give the task a moment to process subscribe + start + subscribe_to_shard.
    for _ in 0..20 {
        tokio::task::yield_now().await;
        if sub.inner.lock().unwrap().events.is_some() {
            break;
        }
    }
    subscription
}

/// Like [`start_and_subscribe`] but issues `start(seq)` **before** `subscribe`,
/// so the initial `subscribeToShard` uses the given start sequence number (Java
/// `testContinuesAfterSequence` calls `start` then `subscribe`).
async fn start_then_subscribe(
    publisher: &Arc<FanOutRecordsPublisher>,
    sub: &Arc<TestSubscriber>,
    start_seq: ExtendedSequenceNumber,
) -> RecordsPublisherSubscription {
    publisher.start(start_seq, latest_position()).await.unwrap();
    let subscription = publisher.subscribe();
    for _ in 0..20 {
        tokio::task::yield_now().await;
        if sub.inner.lock().unwrap().events.is_some() {
            break;
        }
    }
    subscription
}

// Port of FanOutRecordsPublisherTest.testSimple: three batches delivered in order,
// one credit at a time.
#[tokio::test]
async fn simple_delivers_batches_in_order() {
    let _ = stream_id();
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;

    let flow_id = sub.flow_id();
    let events = sub.events();
    // The flow started (SDK began delivering) → publisher requests 1 once demand set.
    subscription.request(1);
    // Let the request(n) reach the task and set availableQueueSpace.
    tokio::task::yield_now().await;
    let _ = events.send(FlowEvent::Started { flow_id });

    let mut received = Vec::new();
    for i in 0..3 {
        let seq = format!("seq-{i}");
        let _ = events.send(FlowEvent::Records {
            flow_id,
            event: Box::new(event_with_records(&[&seq], Some("continuation"))),
        });
        let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
            .await
            .expect("timed out")
            .expect("channel closed")
            .expect("no retrieval error");
        let got = batch.process_records_input().records().unwrap()[0]
            .sequence_number()
            .unwrap()
            .to_string();
        received.push(got);
        // Ack + request the next (drives the credit + queue drain).
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                batch.batch_unique_identifier(),
            )))
            .await;
        subscription.request(1);
    }
    assert_eq!(received, vec!["seq-0", "seq-1", "seq-2"]);
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.testResourceNotFoundForShard: RNFE → synthetic
// shard-end batch (isAtShardEnd, empty records) then completion (no onError).
#[tokio::test]
async fn resource_not_found_synthesizes_shard_end() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();
    let events = sub.events();
    subscription.request(1);
    tokio::task::yield_now().await;

    let _ = events.send(FlowEvent::Error {
        flow_id,
        error: FlowError::ResourceNotFound("shard gone".to_string()),
    });
    let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .expect("channel closed")
        .expect("no retrieval error");
    assert!(batch.process_records_input().is_at_shard_end());
    assert!(batch.process_records_input().records().unwrap().is_empty());
    // After the synthetic batch, the subscriber is completed (channel closes).
    assert!(subscription.recv().await.is_none());
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.testReadTimeoutExceptionForShard: a read
// timeout terminates the subscriber via error. With the subscriber↔publisher
// error-path seam, the error is now DELIVERED (Java `onError`) as an
// `Err(RetrievalError)` on the channel, then the channel closes.
#[tokio::test]
async fn read_timeout_propagates_error() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();
    let events = sub.events();
    subscription.request(1);
    tokio::task::yield_now().await;

    let _ = events.send(FlowEvent::Error {
        flow_id,
        error: FlowError::ReadTimeout("ReadTimeoutException".to_string()),
    });
    // The error is delivered on the channel (onError), no batch.
    let delivery = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .expect("channel closed before error");
    let err = delivery.expect_err("expected a retrieval error, not a batch");
    assert!(err.is_retryable());
    assert!(err.message().contains("ReadTimeout"));
    // Then the channel closes (sink dropped after the error).
    assert!(subscription.recv().await.is_none());
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.testInvalidEvent: an event missing the
// continuation sequence number (and no child shards) is invalid → error, no batch.
#[tokio::test]
async fn invalid_event_fails_publisher() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();
    let events = sub.events();
    subscription.request(1);
    tokio::task::yield_now().await;

    // First a valid batch, delivered + acked.
    let _ = events.send(FlowEvent::Records {
        flow_id,
        event: Box::new(event_with_records(&["seq-1"], Some("continuation"))),
    });
    let first = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap()
        .expect("no retrieval error");
    publisher
        .notify(Box::new(SimpleRecordsDeliveryAck::new(
            first.batch_unique_identifier(),
        )))
        .await;
    subscription.request(1);
    tokio::task::yield_now().await;

    // Invalid event: empty continuation (Java null) AND empty child shards →
    // both-absent, which is invalid.
    let invalid = SubscribeToShardEvent::builder()
        .continuation_sequence_number("")
        .records(make_record("seq-2"))
        .millis_behind_latest(0)
        .build()
        .unwrap();
    let _ = events.send(FlowEvent::Records {
        flow_id,
        event: Box::new(invalid),
    });
    // Publisher fails: the error is delivered (onError), then the channel closes.
    let delivery = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .expect("channel closed before error");
    assert!(delivery.is_err(), "expected a retrieval error, not a batch");
    assert!(subscription.recv().await.is_none());
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest shard-end + onComplete: a shard-end event
// (null continuation + child shards) advances currentSequenceNumber to SHARD_END;
// a subsequent flow complete then completes the subscriber (no resubscribe).
#[tokio::test]
async fn shard_end_then_complete_completes_subscriber() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();
    let events = sub.events();
    subscription.request(1);
    tokio::task::yield_now().await;

    let _ = events.send(FlowEvent::Records {
        flow_id,
        event: Box::new(shard_end_event(&["seq-final"])),
    });
    let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap()
        .expect("no retrieval error");
    assert!(batch.process_records_input().is_at_shard_end());
    // Ack advances currentSequenceNumber to SHARD_END.
    publisher
        .notify(Box::new(SimpleRecordsDeliveryAck::new(
            batch.batch_unique_identifier(),
        )))
        .await;
    tokio::task::yield_now().await;
    // Flow completes → since currentSequenceNumber == SHARD_END, subscriber completes.
    let _ = events.send(FlowEvent::Complete { flow_id });
    assert!(subscription.recv().await.is_none());
    publisher.shutdown().await;
}

// Single-subscriber enforcement: a second subscribe rejects the new subscriber
// — Java MultipleSubscriberException path: onError to BOTH the current and the
// attempted subscriber (not a silent completion), so the consumer records a
// retrieval failure and restarts on its next health check.
#[tokio::test]
async fn second_subscribe_errors_both_subscribers() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut first = start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();

    let mut second = publisher.subscribe();

    for (name, subscription) in [("first", &mut first), ("second", &mut second)] {
        let delivery = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
            .await
            .expect("timed out")
            .unwrap_or_else(|| panic!("{name} subscriber completed silently, expected onError"));
        match delivery {
            Err(e) => assert!(
                e.message().contains("MultipleSubscriberException"),
                "unexpected error for {name}: {e}"
            ),
            Ok(_) => panic!("{name} subscriber received a batch, expected onError"),
        }
        // The channel then completes.
        assert!(subscription.recv().await.is_none());
    }
    // The existing flow was terminated (Java terminateExistingFlow).
    assert!(sub.cancelled().contains(&flow_id));
    publisher.shutdown().await;
}

// restartFrom continuation: restart_from a fanout batch sets the resume point.
#[tokio::test]
async fn restart_from_sets_continuation() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();
    let events = sub.events();
    subscription.request(1);
    tokio::task::yield_now().await;
    let _ = events.send(FlowEvent::Records {
        flow_id,
        event: Box::new(event_with_records(&["seq-1"], Some("cont-3"))),
    });
    let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap()
        .expect("no retrieval error");
    // restart_from accepts the concrete fanout batch (downcast succeeds).
    publisher.restart_from(Arc::clone(&batch)).await;
    // The old flow was cancelled on restart.
    tokio::task::yield_now().await;
    assert!(sub.cancelled().contains(&flow_id));
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.largeRequestTest: subscriber requests 3
// up front, three batches arrive with a continuation sequence number and are all
// delivered in order.
#[tokio::test]
async fn large_request_delivers_all_batches_in_order() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();
    let events = sub.events();

    // request(3) up front (Java subscription.request(3)).
    subscription.request(3);
    tokio::task::yield_now().await;
    let _ = events.send(FlowEvent::Started { flow_id });

    let mut received = Vec::new();
    for i in 1..=3 {
        let seq = format!("seq-{i}");
        let _ = events.send(FlowEvent::Records {
            flow_id,
            event: Box::new(event_with_records(
                &[&seq],
                Some("continuationSequenceNumber"),
            )),
        });
        let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
            .await
            .expect("timed out")
            .expect("channel closed")
            .expect("no retrieval error");
        received.push(
            batch.process_records_input().records().unwrap()[0]
                .sequence_number()
                .unwrap()
                .to_string(),
        );
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                batch.batch_unique_identifier(),
            )))
            .await;
        // Emulate the subscriber's onNext request(1).
        subscription.request(1);
    }
    assert_eq!(received, vec!["seq-1", "seq-2", "seq-3"]);
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.testContinuesAfterSequence: a start at
// sequence "0" delivers a batch with continuation "3"; on flow complete the
// publisher resubscribes at "3" (the continuation advanced) and delivers more.
#[tokio::test]
async fn continues_after_sequence() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription = start_then_subscribe(
        &publisher,
        &sub,
        ExtendedSequenceNumber::from_sequence_number("0"),
    )
    .await;
    let flow_id = sub.flow_id();
    let events = sub.events();

    // First subscribe was at "0", first connection.
    let calls = sub.subscribe_calls();
    assert_eq!(calls.len(), 1);
    assert_eq!(
        calls[0].0,
        ExtendedSequenceNumber::from_sequence_number("0")
    );
    assert!(calls[0].1, "first connection");

    subscription.request(1);
    tokio::task::yield_now().await;
    let _ = events.send(FlowEvent::Started { flow_id });

    // First batch with continuation "3".
    let _ = events.send(FlowEvent::Records {
        flow_id,
        event: Box::new(event_with_records(&["seq-1"], Some("3"))),
    });
    let batch1 = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap()
        .expect("no retrieval error");
    publisher
        .notify(Box::new(SimpleRecordsDeliveryAck::new(
            batch1.batch_unique_identifier(),
        )))
        .await;
    subscription.request(1);
    tokio::task::yield_now().await;

    // Flow completes -> resubscribe at "3" (currentSequenceNumber advanced, not shard end).
    let _ = events.send(FlowEvent::Complete { flow_id });
    // Wait for the resubscribe (a second subscribe call).
    for _ in 0..40 {
        tokio::task::yield_now().await;
        if sub.subscribe_calls().len() >= 2 {
            break;
        }
    }
    let calls = sub.subscribe_calls();
    assert_eq!(calls.len(), 2, "resubscribed after complete");
    assert_eq!(
        calls[1].0,
        ExtendedSequenceNumber::from_sequence_number("3")
    );
    assert!(
        !calls[1].1,
        "resubscribe is not a first connection (AFTER_SEQUENCE_NUMBER)"
    );

    // Second flow delivers another batch.
    let flow_id2 = sub.flow_id();
    let events2 = sub.events();
    let _ = events2.send(FlowEvent::Started { flow_id: flow_id2 });
    let _ = events2.send(FlowEvent::Records {
        flow_id: flow_id2,
        event: Box::new(event_with_records(&["seq-2"], Some("6"))),
    });
    let batch2 = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap()
        .expect("no retrieval error");
    assert_eq!(
        batch2.process_records_input().records().unwrap()[0]
            .sequence_number()
            .unwrap(),
        "seq-2"
    );
    publisher.shutdown().await;
}

/// Set demand + mark the flow started, returning (flow_id, events). Shared setup
/// for the buffering-mechanism tests.
async fn buffering_setup(
    sub: &Arc<TestSubscriber>,
    subscription: &mut RecordsPublisherSubscription,
) -> (u64, mpsc::UnboundedSender<FlowEvent>) {
    let flow_id = sub.flow_id();
    let events = sub.events();
    subscription.request(1);
    tokio::task::yield_now().await;
    let _ = events.send(FlowEvent::Started { flow_id });
    tokio::task::yield_now().await;
    (flow_id, events)
}

// Port of FanOutRecordsPublisherTest.testIfBufferingRecordsWithinCapacityPublishesOneEvent:
// buffering up to the queue capacity without acking delivers exactly one event
// (the head); the rest stay queued behind it.
#[tokio::test]
async fn buffering_within_capacity_publishes_one_event() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let (flow_id, events) = buffering_setup(&sub, &mut subscription).await;

    // 10 events (== capacity, no overflow). No ack, so only the head is delivered.
    for i in 1..=10 {
        let _ = events.send(FlowEvent::Records {
            flow_id,
            event: Box::new(event_with_records(&[&format!("s{i}")], Some("cont"))),
        });
    }
    // Exactly one batch is delivered (the head); the other 9 are queued.
    let first = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap()
        .expect("no error");
    let _ = first;
    // No further delivery arrives without an ack.
    let more =
        tokio::time::timeout(std::time::Duration::from_millis(200), subscription.recv()).await;
    assert!(more.is_err(), "no further delivery without an ack");
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.testIfBufferingRecordsOverCapacityPublishesOneEventAndThrows:
// buffering beyond the queue capacity delivers one event then surfaces a
// "Queue full" failure (Java IllegalStateException, routed here to onError).
#[tokio::test]
async fn buffering_over_capacity_publishes_one_and_throws() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let (flow_id, events) = buffering_setup(&sub, &mut subscription).await;

    // 12 events (> capacity of 11) with no ack -> head delivered, then queue full.
    for i in 1..=12 {
        let _ = events.send(FlowEvent::Records {
            flow_id,
            event: Box::new(event_with_records(&[&format!("s{i}")], Some("cont"))),
        });
    }
    // The head batch is delivered first.
    let first = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap();
    assert!(first.is_ok(), "first is a batch");
    // Then the queue-full error is delivered (onError).
    let err = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .expect("channel closed before error")
        .expect_err("expected a Queue full error");
    assert!(
        err.message().contains("Queue full"),
        "got: {}",
        err.message()
    );
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.testIfPublisherAlwaysPublishesWhenQueueIsEmpty:
// acking each event immediately (draining the queue) lets every one of many
// events be delivered.
#[tokio::test]
async fn always_publishes_when_queue_is_empty() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let (flow_id, events) = buffering_setup(&sub, &mut subscription).await;

    let total = 137;
    let mut delivered = 0;
    for i in 1..=total {
        let _ = events.send(FlowEvent::Records {
            flow_id,
            event: Box::new(event_with_records(&[&format!("s{i}")], Some("cont"))),
        });
        let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no error");
        delivered += 1;
        // Ack immediately (Java evictAckedEventAndScheduleNextEvent) so the queue
        // is empty for the next event.
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                batch.batch_unique_identifier(),
            )))
            .await;
        subscription.request(1);
    }
    assert_eq!(delivered, total);
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.testIfPublisherIgnoresStaleEventsAndContinuesWithNextFlow:
// interleaving a stale ack (different flow) is ignored; all events still delivered.
#[tokio::test]
async fn ignores_stale_acks_and_continues() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let (flow_id, events) = buffering_setup(&sub, &mut subscription).await;

    let total = 100;
    let mut delivered = 0;
    for i in 1..=total {
        let _ = events.send(FlowEvent::Records {
            flow_id,
            event: Box::new(event_with_records(&[&format!("s{i}")], Some("cont"))),
        });
        let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no error");
        delivered += 1;
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                batch.batch_unique_identifier(),
            )))
            .await;
        // Periodically inject a stale ack (unknown flow) — must be ignored.
        if delivered % 10 == 0 {
            publisher
                .notify(Box::new(SimpleRecordsDeliveryAck::new(
                    BatchUniqueIdentifier::new("some_uuid_str", "some_old_flow"),
                )))
                .await;
        }
        subscription.request(1);
    }
    assert_eq!(delivered, total);
    publisher.shutdown().await;
}

// Port of
// FanOutRecordsPublisherTest.testIfPublisherIgnoresStaleEventsAndContinuesWithNextFlowWhenDeliveryQueueIsNotEmpty:
// with a non-empty queue, a good ack followed by a stale ack still delivers all.
#[tokio::test]
async fn ignores_stale_acks_when_queue_not_empty() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let (flow_id, events) = buffering_setup(&sub, &mut subscription).await;

    let total = 10;
    let mut delivered = 0;
    for i in 1..=total {
        let _ = events.send(FlowEvent::Records {
            flow_id,
            event: Box::new(event_with_records(&[&format!("s{i}")], Some("cont"))),
        });
        let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no error");
        delivered += 1;
        // Good ack, then a stale ack (different flow) — the stale one is ignored.
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                batch.batch_unique_identifier(),
            )))
            .await;
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                BatchUniqueIdentifier::new("some_uuid_str", "some_old_flow"),
            )))
            .await;
        subscription.request(1);
    }
    assert_eq!(delivered, total);
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.testIfPublisherThrowsWhenMismatchAckforActiveFlowSeen:
// an ack whose flow identifier matches the active flow but whose batch id does
// not is a fatal mismatch (Java IllegalStateException, routed to onError here).
#[tokio::test]
async fn mismatch_ack_for_active_flow_fails() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let (flow_id, events) = buffering_setup(&sub, &mut subscription).await;

    // Deliver one batch (so a flow is active with a queued head).
    let _ = events.send(FlowEvent::Records {
        flow_id,
        event: Box::new(event_with_records(&["s1"], Some("cont"))),
    });
    let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap()
        .expect("no error");
    let _ = batch;
    // An ack with the SAME (active) flow identifier but a DIFFERENT batch id ->
    // fatal mismatch. The publisher fails (onError) rather than silently ignoring.
    publisher
        .notify(Box::new(SimpleRecordsDeliveryAck::new(
            BatchUniqueIdentifier::new("some_uuid_str", flow_id.to_string()),
        )))
        .await;
    let err = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .expect("channel closed before error")
        .expect_err("expected a mismatch failure");
    assert!(
        err.message().contains("Unexpected ack"),
        "got: {}",
        err.message()
    );
    publisher.shutdown().await;
}

// Port of FanOutRecordsPublisherTest.restartFromShardEndCallsSubscribeToShardAtLatest:
// restartFrom a SHARD_END batch, then subscribe, resubscribes from SHARD_END —
// the input from which the SDK-backed subscriber selects the LATEST iterator type.
#[tokio::test]
async fn restart_from_shard_end_subscribes_at_latest() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));

    // A SHARD_END fanout batch.
    let shard_end_batch: Arc<dyn crate::retrieval::records_retrieved::RecordsRetrieved> =
        Arc::new(FanoutRecordsRetrieved::new(
            ProcessRecordsInput::builder().build(),
            ExtendedSequenceNumber::shard_end(),
            "shard-001".to_string(),
        ));
    publisher.restart_from(shard_end_batch).await;

    // Subscribe drives subscribe_to_shard(SHARD_END).
    let _subscription = publisher.subscribe();
    for _ in 0..40 {
        tokio::task::yield_now().await;
        if !sub.subscribe_calls().is_empty() {
            break;
        }
    }
    let calls = sub.subscribe_calls();
    assert_eq!(calls.len(), 1);
    // The resubscribe is from SHARD_END as a first connection — the state from
    // which KinesisShardSubscriber selects ShardIteratorType::LATEST.
    assert_eq!(calls[0].0, ExtendedSequenceNumber::shard_end());
    assert!(calls[0].1, "first connection after restart");
    publisher.shutdown().await;
}

// The publisher requests upstream one at a time (credit-based backpressure).
#[tokio::test]
async fn credit_is_one_at_a_time() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let mut subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();
    let events = sub.events();

    // The event stream starts with no outstanding demand: no upstream request.
    let _ = events.send(FlowEvent::Started { flow_id });
    tokio::task::yield_now().await;
    assert_eq!(sub.request_count(), 0);

    // request(1) with availableQueueSpace previously <= 0 triggers exactly one
    // flow.request(1).
    subscription.request(1);
    for _ in 0..2000 {
        if sub.request_count() >= 1 {
            break;
        }
        tokio::task::yield_now().await;
    }
    assert_eq!(sub.request_count(), 1);

    // Deliver + ack one batch; with no remaining credit, no extra upstream request.
    let _ = events.send(FlowEvent::Records {
        flow_id,
        event: Box::new(event_with_records(&["s"], Some("c"))),
    });
    let batch = tokio::time::timeout(std::time::Duration::from_secs(2), subscription.recv())
        .await
        .expect("timed out")
        .unwrap()
        .expect("no retrieval error");
    publisher
        .notify(Box::new(SimpleRecordsDeliveryAck::new(
            batch.batch_unique_identifier(),
        )))
        .await;
    publisher.shutdown().await;
}

// Java RecordFlow.request: demand arriving while the SubscribeToShard connection
// is still being established is dropped (`subscription != null` guard); the
// credit is issued once by RecordSubscription.onSubscribe when the stream comes
// up. Forwarding it on both paths would double the outstanding credit for a
// single request(1).
#[tokio::test]
async fn demand_before_flow_start_is_requested_once_on_start() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let subscription =
        start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow_id = sub.flow_id();
    let events = sub.events();

    // Demand while the flow is connecting: accumulates queue space only.
    subscription.request(1);
    for _ in 0..20 {
        tokio::task::yield_now().await;
    }
    assert_eq!(
        sub.request_count(),
        0,
        "demand must not be forwarded before the event stream starts"
    );

    // The stream starts: exactly one upstream request is issued.
    let _ = events.send(FlowEvent::Started { flow_id });
    for _ in 0..2000 {
        if sub.request_count() >= 1 {
            break;
        }
        tokio::task::yield_now().await;
    }
    assert_eq!(sub.request_count(), 1);
    publisher.shutdown().await;
}

// The consumer's restart path (ShardConsumerSubscriber::restart_if_request_timer_
// expired) cancels its subscription and immediately re-subscribes. Whichever
// order the publisher task observes the queued cancel and the Subscribe command
// in, the new subscription must be accepted and served by a fresh flow — not
// tripped up by single-subscriber enforcement (Java's synchronous
// Subscription.cancel() under lockObject makes this ordering implicit).
#[tokio::test]
async fn resubscribe_after_cancel_is_accepted() {
    let sub = TestSubscriber::new();
    let publisher = build_publisher(Arc::clone(&sub));
    let first = start_and_subscribe(&publisher, &sub, ExtendedSequenceNumber::latest()).await;
    let flow1 = sub.flow_id();

    // Cancel and immediately re-subscribe (no yield in between: the cancel may
    // still be queued on the old demand channel when Subscribe is processed).
    first.cancel();
    let mut second = publisher.subscribe();

    // A second flow is established for the new subscription.
    for _ in 0..2000 {
        if sub.subscribe_calls().len() >= 2 {
            break;
        }
        tokio::task::yield_now().await;
    }
    assert_eq!(
        sub.subscribe_calls().len(),
        2,
        "re-subscribe after cancel was not granted a new flow"
    );
    let flow2 = sub.flow_id();
    assert_ne!(flow2, flow1);

    // The new subscription is live end-to-end.
    let events = sub.events();
    second.request(1);
    tokio::task::yield_now().await;
    let _ = events.send(FlowEvent::Started { flow_id: flow2 });
    let _ = events.send(FlowEvent::Records {
        flow_id: flow2,
        event: Box::new(event_with_records(&["after-restart"], Some("cont"))),
    });
    let batch = tokio::time::timeout(std::time::Duration::from_secs(2), second.recv())
        .await
        .expect("timed out")
        .expect("second subscription must be live")
        .expect("no retrieval error");
    assert_eq!(
        batch.process_records_input().records().unwrap()[0]
            .sequence_number()
            .unwrap(),
        "after-restart"
    );
    publisher.shutdown().await;
}

// White-box (deterministic) variant of the above: the Subscribe command must
// apply a cancel still queued on the old subscription's demand channel before
// enforcing single-subscriber — the restart path's cancel→re-subscribe is not
// serialized across the demand and command channels, so the task can see the
// Subscribe first.
#[tokio::test]
async fn subscribe_command_drains_queued_cancel_before_enforcing() {
    use std::collections::VecDeque;

    let sub = TestSubscriber::new();
    let (flow_event_tx, _flow_event_rx) = mpsc::unbounded_channel();
    let mut state = PublisherState {
        subscriber: None,
        current_flow_id: None,
        next_flow_id: 2,
        current_sequence_number: ExtendedSequenceNumber::latest(),
        initial_position: latest_position(),
        is_first_connection: true,
        flow_connected: true,
        available_queue_space: 0,
        records_delivery_queue: VecDeque::new(),
        subscriber_impl: Arc::clone(&sub) as Arc<dyn ShardSubscriber>,
        stream_and_shard_id: SHARD_ID.to_string(),
        last_successful_request_details: Arc::new(Mutex::new(
            crate::common::request_details::RequestDetails::empty(),
        )),
        flow_event_tx,
    };
    // A live first subscription (flow 1) whose cancel is queued but not yet
    // observed by the task.
    let (old_subscription, old_sink) = new_subscription();
    state.subscriber = Some(old_sink);
    state.current_flow_id = Some(1);
    old_subscription.cancel();

    let (mut new_subscription_handle, new_sink) = new_subscription();
    let (ack_tx, ack_rx) = tokio::sync::oneshot::channel();
    let done = handle_command(
        &mut state,
        Command::Subscribe {
            sink: new_sink,
            ack: ack_tx,
        },
    )
    .await;
    assert!(!done);
    assert_eq!(
        ack_rx.await.expect("ack dropped"),
        Ok(()),
        "queued cancel must vacate the old subscriber, not trip enforcement"
    );
    // The old flow was cancelled by the drained cancel; a new flow subscribed.
    assert!(sub.cancelled().contains(&1));
    assert_eq!(sub.subscribe_calls().len(), 1);
    assert_eq!(state.current_flow_id, Some(2));
    // The old subscription's channel is closed; the new one is live (not errored).
    let mut old_subscription = old_subscription;
    assert!(old_subscription.recv().await.is_none());
    assert!(
        tokio::time::timeout(
            std::time::Duration::from_millis(100),
            new_subscription_handle.recv()
        )
        .await
        .is_err(),
        "new subscription must be pending (live), not closed or errored"
    );
}

/// A [`ShardSubscriber`] whose `subscribe` always panics — used to prove
/// command-handling panic containment (2026-07-14 hardening item 5, same
/// hazard as `PrefetchRecordsPublisher`'s `handle_command_guarded`).
struct PanicOnSubscribe;
#[async_trait::async_trait]
impl ShardSubscriber for PanicOnSubscribe {
    async fn subscribe(
        &self,
        _flow_id: u64,
        _sequence_number: ExtendedSequenceNumber,
        _is_first_connection: bool,
        _initial_position: InitialPositionInStreamExtended,
        _events: mpsc::UnboundedSender<FlowEvent>,
    ) {
        panic!("injected subscribe panic (command-handling containment test)");
    }
    fn request_next(&self, _flow_id: u64) {}
    fn cancel(&self, _flow_id: u64) {}
}

// New (2026-07-14 hardening item 5): a panic while handling a command
// (`Command::Subscribe` awaiting `ShardSubscriber::subscribe`, made to panic)
// must be caught by `handle_command_guarded` — logged, not propagated, and
// NOT treated as a shutdown request — leaving `state` usable for the next
// command. Before this fix only `PrefetchRecordsPublisher` had this
// containment; `FanOutRecordsPublisher::run_task`'s command arm was bare.
#[tokio::test(flavor = "multi_thread")]
async fn panic_in_command_handling_is_contained_by_handle_command_guarded() {
    let (flow_event_tx, _flow_event_rx) = mpsc::unbounded_channel();
    let mut state = PublisherState {
        subscriber: None,
        current_flow_id: None,
        next_flow_id: 1,
        current_sequence_number: ExtendedSequenceNumber::latest(),
        initial_position: latest_position(),
        is_first_connection: true,
        flow_connected: false,
        available_queue_space: 0,
        records_delivery_queue: VecDeque::new(),
        subscriber_impl: Arc::new(PanicOnSubscribe) as Arc<dyn ShardSubscriber>,
        stream_and_shard_id: SHARD_ID.to_string(),
        last_successful_request_details: Arc::new(Mutex::new(
            crate::common::request_details::RequestDetails::empty(),
        )),
        flow_event_tx,
    };

    let (_subscription, sink) = new_subscription();
    let (ack_tx, _ack_rx) = tokio::sync::oneshot::channel();
    let done = handle_command_guarded(&mut state, Command::Subscribe { sink, ack: ack_tx }).await;
    assert!(
        !done,
        "a contained panic must not be treated as a shutdown request"
    );

    // State remains usable: a subsequent command (an ack against an empty
    // queue — a benign no-op/stale-ack path) still runs normally, proving the
    // caught panic didn't corrupt `state` or wedge command handling.
    let done = handle_command_guarded(
        &mut state,
        Command::Ack(BatchUniqueIdentifier::new("x", "y")),
    )
    .await;
    assert!(!done);
}
