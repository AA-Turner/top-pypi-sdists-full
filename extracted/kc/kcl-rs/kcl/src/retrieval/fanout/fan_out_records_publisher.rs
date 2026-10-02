//! Port of `software.amazon.kinesis.retrieval.fanout.FanOutRecordsPublisher`.
//!
//! The core enhanced-fan-out (EFO) [`RecordsPublisher`]: drives the Kinesis
//! `SubscribeToShard` event stream, buffers events in a small bounded delivery
//! queue with an ack protocol, applies 1-at-a-time credit-based backpressure,
//! resubscribes across connection lifetimes, and translates/propagates errors.
//!
//! # Actor-model translation (Java → Rust)
//!
//! Java guards *all* mutable state with a single reentrant intrinsic monitor
//! (`lockObject`) shared across SDK I/O callback threads, the downstream
//! subscriber's `request(n)`/`cancel()`, and `notify(ack)`. This port collapses
//! that into a **single spawned tokio task** ([`run_task`]) owning all state
//! ([`PublisherState`]); every call-path becomes a message, so no locking (and no
//! Java reentrancy hazard) is needed:
//!
//! * Downstream demand/cancel arrive via the retrieval-core sink
//!   (`sink.next_demand()`); acks/restart/shutdown/subscribe arrive as
//!   [`Command`]s.
//! * The SDK `SubscribeToShard` event stream is driven by a per-generation
//!   "flow" driver task ([`ShardSubscriber`]) that forwards [`FlowEvent`]s
//!   (`Started` / `Records` / `Complete` / `Error` / `ResponseReceived`) tagged
//!   with a monotonically-increasing `flow_id` — the Rust analog of Java's
//!   `RecordFlow`/`subscribeToShardId` stale-flow detection.
//!
//! Preserved behaviors: 1-credit-at-a-time `availableQueueSpace` flow control,
//! the bounded ack queue (cap [`MAX_EVENT_BURST_FROM_SERVICE`] = 11) with
//! deferred terminal events ordered behind buffered records, continuation-sequence
//! handling + SHARD_END resubscribe-vs-complete, single-subscriber enforcement
//! ([`MultipleSubscriberError`]), `ResourceNotFoundException` → synthetic
//! shard-end, read-timeout → retryable error, and stale-flow/stale-ack handling.

use std::collections::VecDeque;
use std::sync::{Arc, Mutex};
use std::time::Instant;

use async_trait::async_trait;
use tokio::sync::mpsc;

use crate::common::request_details::RequestDetails;
use crate::common::InitialPositionInStreamExtended;
use crate::common::StreamIdentifier;
use crate::exceptions::BoxError;
use crate::lifecycle::events::process_records_input::ProcessRecordsInput;
use crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier;
use crate::retrieval::data_retrieval_util::is_valid_result;
use crate::retrieval::fanout::fanout_records_retrieved::FanoutRecordsRetrieved;
use crate::retrieval::kinesis_client_record::KinesisClientRecord;
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::records_delivery_ack::RecordsDeliveryAck;
use crate::retrieval::records_publisher::{
    new_subscription, DemandSignal, RecordsPublisher, RecordsPublisherSink,
    RecordsPublisherSubscription,
};
use crate::retrieval::records_retrieved::RecordsRetrieved;
use crate::retrieval::RetrievalError;

use aws_sdk_kinesis::types::{ChildShard, SubscribeToShardEvent};

/// Max burst of 10 payload events + 1 terminal event from the service (Java
/// `MAX_EVENT_BURST_FROM_SERVICE`). The delivery queue is bounded to this.
pub const MAX_EVENT_BURST_FROM_SERVICE: usize = 10 + 1;

/// Signals that a second subscriber attempted to subscribe while one was active
/// (Java `MultipleSubscriberException`). A marker error, no message.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct MultipleSubscriberError;

impl std::fmt::Display for MultipleSubscriberError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "MultipleSubscriberException")
    }
}
impl std::error::Error for MultipleSubscriberError {}

/// A classified flow error (the Rust analog of Java's `throwableCategory`).
#[derive(Debug, Clone)]
pub enum FlowError {
    /// Netty/connection-pool acquire timeout (Java `ACQUIRE_TIMEOUT`).
    AcquireTimeout(String),
    /// Read timeout → translated to a retryable retrieval error (Java `READ_TIMEOUT`).
    ReadTimeout(String),
    /// The shard no longer exists → graceful synthetic shard-end (cause is
    /// `ResourceNotFoundException`).
    ResourceNotFound(String),
    /// Any other error (Java `OTHER`).
    Other(String),
}

impl FlowError {
    /// The human-readable message carried by this error category.
    pub fn message(&self) -> &str {
        match self {
            FlowError::AcquireTimeout(m)
            | FlowError::ReadTimeout(m)
            | FlowError::ResourceNotFound(m)
            | FlowError::Other(m) => m,
        }
    }
}

/// An event forwarded from a flow driver (SDK event-stream reader) to the task,
/// tagged with the generation id it belongs to (stale-flow detection).
#[derive(Debug)]
pub enum FlowEvent {
    /// The event stream has started (the SDK began delivering). Marks
    /// `isFirstConnection=false` and requests the first item if demand exists.
    Started { flow_id: u64 },
    /// A `SubscribeToShardEvent` batch arrived.
    Records {
        flow_id: u64,
        event: Box<SubscribeToShardEvent>,
    },
    /// A `responseReceived` diagnostic (request id).
    ResponseReceived { flow_id: u64, request_id: String },
    /// The flow completed (Java `RecordFlow.complete`).
    Complete { flow_id: u64 },
    /// The flow errored (Java `RecordFlow.exceptionOccurred`).
    Error { flow_id: u64, error: FlowError },
}

/// How to establish a `SubscribeToShard` connection for a given flow generation.
///
/// The production impl ([`KinesisShardSubscriber`]) drives the SDK event stream;
/// tests inject a fake that lets them feed [`FlowEvent`]s directly.
#[async_trait]
pub trait ShardSubscriber: Send + Sync {
    /// Begin a subscription for `flow_id`, forwarding [`FlowEvent`]s to `events`.
    ///
    /// `sequence_number` is the position to (re)subscribe from; `is_first_connection`
    /// and `is_shard_end` select the iterator type (Java `subscribeToShard`
    /// three-way branch). One `flow.request(1)` on this flow corresponds to a
    /// [`request_next`](Self::request_next) call.
    async fn subscribe(
        &self,
        flow_id: u64,
        sequence_number: ExtendedSequenceNumber,
        is_first_connection: bool,
        initial_position: InitialPositionInStreamExtended,
        events: mpsc::UnboundedSender<FlowEvent>,
    );

    /// Request one more event from the SDK subscription for `flow_id` (Java
    /// `flow.request(1)`).
    fn request_next(&self, flow_id: u64);

    /// Cancel the SDK subscription for `flow_id` (Java `flow.cancel()`).
    fn cancel(&self, flow_id: u64);
}

/// Commands sent to the single publisher task.
enum Command {
    /// Set the start position (Java `start`).
    Start {
        sequence_number: ExtendedSequenceNumber,
        initial_position: InitialPositionInStreamExtended,
    },
    /// A downstream subscribe attempt (single-subscriber enforced).
    Subscribe {
        sink: RecordsPublisherSink,
        ack: tokio::sync::oneshot::Sender<Result<(), MultipleSubscriberError>>,
    },
    /// A delivery ack (Java `notify`).
    Ack(BatchUniqueIdentifier),
    /// Restart from a batch's continuation sequence number (Java `restartFrom`).
    RestartFrom(ExtendedSequenceNumber),
    /// Shut down (Java `shutdown`).
    Shutdown(tokio::sync::oneshot::Sender<()>),
}

/// A queued delivery-queue element: a records batch or a deferred terminal event.
enum QueueEntry {
    Records {
        records: Arc<FanoutRecordsRetrieved>,
        flow_id: u64,
        #[allow(dead_code)]
        enqueue_time: Instant,
    },
    /// A deferred terminal action (Java `SubscriptionShutdownEvent`): run once it
    /// reaches the head of the queue.
    Shutdown {
        kind: ShutdownKind,
        #[allow(dead_code)]
        flow_id: u64,
    },
}

#[derive(Clone)]
enum ShutdownKind {
    Complete,
    Error(FlowError),
}

/// All mutable state owned by the single publisher task.
struct PublisherState {
    subscriber: Option<RecordsPublisherSink>,
    current_flow_id: Option<u64>,
    next_flow_id: u64,
    current_sequence_number: ExtendedSequenceNumber,
    initial_position: InitialPositionInStreamExtended,
    is_first_connection: bool,
    /// Whether the current flow's event stream has started delivering (Java's
    /// `RecordSubscription.subscription != null`: demand arriving while the
    /// connection is still being established must not be forwarded upstream —
    /// `flow_started` re-issues one request when the stream comes up).
    flow_connected: bool,
    available_queue_space: i64,
    records_delivery_queue: VecDeque<QueueEntry>,
    subscriber_impl: Arc<dyn ShardSubscriber>,
    stream_and_shard_id: String,
    last_successful_request_details: Arc<Mutex<RequestDetails>>,
    flow_event_tx: mpsc::UnboundedSender<FlowEvent>,
}

impl PublisherState {
    fn is_active_flow(&self, flow_id: u64) -> bool {
        self.current_flow_id == Some(flow_id)
    }

    fn should_shutdown_now(&self) -> bool {
        self.records_delivery_queue.is_empty()
    }

    /// Java `subscribeToShard`: pick the iterator type and start a new flow.
    async fn subscribe_to_shard(&mut self, sequence_number: ExtendedSequenceNumber) {
        // Clear any lingering queue entries (Java resetRecordsDeliveryStateOnSubscriptionOnInit).
        if !self.records_delivery_queue.is_empty() {
            tracing::warn!(
                "{}: Found non-empty queue while starting subscription; clearing.",
                self.stream_and_shard_id
            );
            self.records_delivery_queue.clear();
        }
        let flow_id = self.next_flow_id;
        self.next_flow_id += 1;
        self.current_flow_id = Some(flow_id);
        self.flow_connected = false;
        let is_first = self.is_first_connection;
        self.subscriber_impl
            .subscribe(
                flow_id,
                sequence_number,
                is_first,
                self.initial_position,
                self.flow_event_tx.clone(),
            )
            .await;
    }

    /// Java `bufferCurrentEventAndScheduleIfRequired`.
    async fn buffer_current_event(&mut self, records: Arc<FanoutRecordsRetrieved>, flow_id: u64) {
        if self.records_delivery_queue.len() >= MAX_EVENT_BURST_FROM_SERVICE {
            // Java `queue.add` throws IllegalStateException on overflow; we surface
            // it as an error to the subscriber via errorOccurred.
            tracing::warn!(
                "{}: Unable to enqueue payload: delivery queue full.",
                self.stream_and_shard_id
            );
            self.error_occurred(flow_id, FlowError::Other("Queue full".to_string()))
                .await;
            return;
        }
        let is_sole = self.records_delivery_queue.is_empty();
        self.records_delivery_queue.push_back(QueueEntry::Records {
            records: Arc::clone(&records),
            flow_id,
            enqueue_time: Instant::now(),
        });
        if is_sole {
            self.deliver(records).await;
        }
    }

    /// Deliver a batch to the subscriber (Java `subscriber.onNext`).
    async fn deliver(&mut self, records: Arc<FanoutRecordsRetrieved>) {
        if let Some(sink) = &self.subscriber {
            let arc: Arc<dyn RecordsRetrieved> = records;
            let _ = sink.deliver(arc).await;
        }
    }

    /// Deliver a retrieval error to the subscriber (Java `subscriber.onError(t)`).
    ///
    /// Subscriber↔publisher error-path seam: routes the classified [`FlowError`]
    /// to the consumer as a typed [`RetrievalError`] so
    /// `ShardConsumerSubscriber::note_retrieval_failure` fires (restart /
    /// health-check), instead of silently completing by dropping the sink.
    async fn deliver_error(&mut self, error: &FlowError) {
        if let Some(sink) = &self.subscriber {
            let retrieval_error = match error {
                // READ_TIMEOUT maps to a retryable error whose message contains
                // "ReadTimeout" (the subscriber's ReadTimeout grace-period match).
                FlowError::ReadTimeout(m) => RetrievalError::retryable(format!("ReadTimeout: {m}")),
                FlowError::AcquireTimeout(m) | FlowError::Other(m) => {
                    RetrievalError::other(m.clone())
                }
                // ResourceNotFound is delivered as a synthetic shard-end batch,
                // not an error (handled by the caller).
                FlowError::ResourceNotFound(m) => RetrievalError::other(m.clone()),
            };
            let _ = sink.deliver_error(retrieval_error).await;
        }
    }

    /// Java `evictAckedEventAndScheduleNextEvent` + `updateAvailableQueueSpaceAndRequestUpstream`.
    /// Returns the triggering flow id (for the upstream request) on a successful evict.
    async fn handle_ack(&mut self, ack_id: &BatchUniqueIdentifier) {
        let head_matches = matches!(
            self.records_delivery_queue.front(),
            Some(QueueEntry::Records { records, .. })
                if &records.batch_unique_identifier() == ack_id
        );
        if head_matches {
            // Pop the head + advance the sequence number.
            let (flow_id, continuation) = match self.records_delivery_queue.pop_front() {
                Some(QueueEntry::Records {
                    records, flow_id, ..
                }) => (flow_id, records.continuation_sequence_number().clone()),
                _ => unreachable!("checked head_matches"),
            };
            self.current_sequence_number = continuation;
            // Schedule the next queued entry (record onNext or deferred terminal).
            self.execute_head_action().await;
            // Update credit + request upstream.
            self.update_available_and_request(flow_id);
        } else {
            // Mismatch: fatal for the active flow, ignored for a stale flow.
            let flow_matches_active = self
                .current_flow_id
                .map(|active| {
                    // The ack's flow identifier is compared to the active flow's
                    // string id ("shard-<n>" analog); we store flow ids numerically,
                    // so compare the ack's flow identifier to the active flow id.
                    ack_id.flow_identifier() == active.to_string()
                })
                .unwrap_or(false);
            if flow_matches_active {
                // Java throws IllegalStateException here (bug detection). We route
                // it into errorOccurred on the active flow.
                let flow_id = self.current_flow_id.unwrap();
                tracing::error!(
                    "{}: Received unexpected ack for the active subscription {}. Failing.",
                    self.stream_and_shard_id,
                    flow_id
                );
                self.error_occurred(
                    flow_id,
                    FlowError::Other("Unexpected ack for the active subscription".into()),
                )
                .await;
            } else {
                tracing::info!(
                    "{}: Publisher received an ack for a stale subscription. Ignoring.",
                    self.stream_and_shard_id
                );
            }
        }
    }

    /// Run the action for the new head of the queue (Java `executeEventAction`).
    async fn execute_head_action(&mut self) {
        match self.records_delivery_queue.front() {
            Some(QueueEntry::Records { records, .. }) => {
                let records = Arc::clone(records);
                self.deliver(records).await;
            }
            Some(QueueEntry::Shutdown { kind, .. }) => {
                let kind = kind.clone();
                // Pop the shutdown entry and execute it.
                self.records_delivery_queue.pop_front();
                self.run_shutdown(kind).await;
            }
            None => {}
        }
    }

    /// Java `updateAvailableQueueSpaceAndRequestUpstream`.
    fn update_available_and_request(&mut self, flow_id: u64) {
        if self.available_queue_space <= 0 {
            return;
        }
        self.available_queue_space -= 1;
        if self.available_queue_space > 0 {
            self.subscriber_impl.request_next(flow_id);
        }
    }

    /// Java `recordsReceived`: validate + buffer.
    async fn records_received(&mut self, flow_id: u64, event: SubscribeToShardEvent) {
        if self.subscriber.is_none() {
            self.subscriber_impl.cancel(flow_id);
            if let Some(active) = self.current_flow_id {
                self.subscriber_impl.cancel(active);
            }
            return;
        }
        if !self.is_active_flow(flow_id) {
            // Records for an inactive flow: ignore.
            return;
        }

        // The Rust SDK models `continuationSequenceNumber` as a required `String`
        // (defaulting to "" when unset); Java's null → shard-end signal maps to an
        // empty string here.
        let continuation_raw = event.continuation_sequence_number();
        let continuation: Option<&str> = if continuation_raw.is_empty() {
            None
        } else {
            Some(continuation_raw)
        };
        let child_shards: Vec<ChildShard> = event.child_shards().to_vec();
        if !is_valid_result(continuation, &child_shards) {
            self.error_occurred(
                flow_id,
                FlowError::Other(format!(
                    "RecordBatchEvent for flow {flow_id} is invalid. continuationSequenceNumber: {continuation:?}, childShards: {child_shards:?}"
                )),
            )
            .await;
            return;
        }

        let records: Vec<KinesisClientRecord> = event
            .records()
            .iter()
            .map(KinesisClientRecord::from_record)
            .collect();
        let input = ProcessRecordsInput::builder()
            .cache_entry_time(chrono::Utc::now())
            .millis_behind_latest(event.millis_behind_latest())
            .is_at_shard_end(continuation.is_none())
            .records(records)
            .child_shards(child_shards)
            .build();
        let continuation_seq = match continuation {
            None => ExtendedSequenceNumber::shard_end(),
            Some(seq) => ExtendedSequenceNumber::from_sequence_number(seq),
        };
        let retrieved = Arc::new(FanoutRecordsRetrieved::new(
            input,
            continuation_seq,
            flow_id.to_string(),
        ));
        self.buffer_current_event(retrieved, flow_id).await;
    }

    /// Java `onComplete`: resubscribe unless SHARD_END, else complete subscriber.
    async fn on_complete(&mut self, flow_id: u64) {
        self.subscriber_impl.cancel(flow_id);
        if self.subscriber.is_none() {
            return;
        }
        if !self.is_active_flow(flow_id) {
            // Spurious onComplete from a stale flow: ignore.
            return;
        }
        if self.current_sequence_number.is_shard_end() {
            // Shard ended: complete the subscriber (drop the sink → onComplete).
            self.subscriber = None;
            self.current_flow_id = None;
        } else {
            let seq = self.current_sequence_number.clone();
            self.subscribe_to_shard(seq).await;
        }
    }

    /// Java `errorOccurred` + `handleFlowError`.
    async fn error_occurred(&mut self, flow_id: u64, error: FlowError) {
        if self.subscriber.is_none() {
            return;
        }
        if self.is_active_flow(flow_id) {
            self.subscriber_impl.cancel(flow_id);
            self.available_queue_space = 0;
            match &error {
                FlowError::ResourceNotFound(_) => {
                    // Synthesize a shard-end batch + complete (graceful).
                    let input = ProcessRecordsInput::builder()
                        .records(vec![])
                        .is_at_shard_end(true)
                        .child_shards(vec![])
                        .build();
                    let synth = Arc::new(FanoutRecordsRetrieved::new(
                        input,
                        ExtendedSequenceNumber::shard_end(),
                        flow_id.to_string(),
                    ));
                    self.deliver(synth).await;
                    // Complete: drop the sink.
                    self.subscriber = None;
                }
                FlowError::AcquireTimeout(_) => {
                    self.log_acquire_timeout_message();
                    // Propagate as onError (deliver the error, then drop the sink).
                    self.deliver_error(&error).await;
                    self.subscriber = None;
                }
                _ => {
                    // READ_TIMEOUT / OTHER → onError: deliver the typed error to
                    // the consumer (subscriber↔publisher error-path seam), then
                    // drop the sink.
                    self.deliver_error(&error).await;
                    self.subscriber = None;
                }
            }
            self.current_flow_id = None;
        } else {
            // Stale flow error: just cancel it.
            self.subscriber_impl.cancel(flow_id);
        }
    }

    fn log_acquire_timeout_message(&self) {
        tracing::error!(
            "An acquire timeout occurred which usually indicates that the KinesisAsyncClient supplied has a low maximum streams limit. Use KinesisClientUtil to set up the client."
        );
    }

    async fn run_shutdown(&mut self, kind: ShutdownKind) {
        let flow_id = self.current_flow_id.unwrap_or(0);
        match kind {
            ShutdownKind::Complete => self.on_complete(flow_id).await,
            ShutdownKind::Error(e) => self.error_occurred(flow_id, e).await,
        }
    }

    /// Java `RecordFlow.complete`: act now if the queue is empty, else defer.
    async fn flow_complete(&mut self, flow_id: u64) {
        if !self.is_active_flow(flow_id) {
            // Stale-flow complete: cancel + ignore (Java swallows via isActiveFlow).
            self.subscriber_impl.cancel(flow_id);
            return;
        }
        if self.should_shutdown_now() {
            self.on_complete(flow_id).await;
        } else {
            self.records_delivery_queue.push_back(QueueEntry::Shutdown {
                kind: ShutdownKind::Complete,
                flow_id,
            });
        }
    }

    /// Java `RecordFlow.exceptionOccurred`: act now if the queue is empty, else defer.
    async fn flow_error(&mut self, flow_id: u64, error: FlowError) {
        if self.should_shutdown_now() {
            self.error_occurred(flow_id, error).await;
        } else {
            self.records_delivery_queue.push_back(QueueEntry::Shutdown {
                kind: ShutdownKind::Error(error),
                flow_id,
            });
        }
    }

    /// Java `RecordSubscription.onSubscribe` request-1-if-demand + flip first-connection.
    fn flow_started(&mut self, flow_id: u64) {
        if !self.is_active_flow(flow_id) {
            return;
        }
        self.is_first_connection = false;
        self.flow_connected = true;
        if self.available_queue_space > 0 {
            self.subscriber_impl.request_next(flow_id);
        }
    }

    /// Apply one downstream demand/cancel signal (or `None` = subscription handle
    /// dropped). Java `RecordSubscription.request(n)` / `cancel()` under
    /// `lockObject`; shared by the run-loop's demand arm and
    /// [`drain_pending_demand`](Self::drain_pending_demand).
    fn apply_demand_signal(&mut self, signal: Option<DemandSignal>) {
        match signal {
            Some(DemandSignal::Request(n)) => {
                let was_nonpositive = self.available_queue_space <= 0;
                self.available_queue_space += n as i64;
                // Java RecordFlow.request drops a request made before the SDK
                // subscription exists (`subscription != null` guard); the credit
                // is re-issued by `flow_started` once the stream comes up.
                // Forwarding it here too would double the outstanding credit.
                if was_nonpositive && self.flow_connected {
                    if let Some(flow_id) = self.current_flow_id {
                        self.subscriber_impl.request_next(flow_id);
                    }
                }
            }
            Some(DemandSignal::Cancel) => {
                if let Some(flow_id) = self.current_flow_id.take() {
                    self.subscriber_impl.cancel(flow_id);
                }
                self.subscriber = None;
                self.available_queue_space = 0;
            }
            None => {
                // Subscription handle dropped.
                self.subscriber = None;
            }
        }
    }

    /// Apply any demand/cancel signals already queued on the current subscriber's
    /// demand channel, without blocking.
    ///
    /// The consumer's restart path cancels its old subscription and immediately
    /// re-subscribes; the cancel (or the dropped handle) may still be sitting in
    /// the old sink's demand channel when the `Subscribe` command arrives on the
    /// command channel. Java's synchronous `Subscription.cancel()` under
    /// `lockObject` makes that ordering implicit — here we drain first so a
    /// vacated subscriber is not mistaken for a live one.
    fn drain_pending_demand(&mut self) {
        use tokio::sync::mpsc::error::TryRecvError;
        loop {
            let signal = match self.subscriber.as_mut() {
                None => return,
                Some(sink) => match sink.try_next_demand() {
                    Ok(signal) => Some(signal),
                    Err(TryRecvError::Disconnected) => None,
                    Err(TryRecvError::Empty) => return,
                },
            };
            let dropped = signal.is_none();
            self.apply_demand_signal(signal);
            if dropped {
                return;
            }
        }
    }
}

/// The publisher handle (Java `FanOutRecordsPublisher`).
pub struct FanOutRecordsPublisher {
    inner: Mutex<HandleState>,
    last_successful_request_details: Arc<Mutex<RequestDetails>>,
    build: Mutex<Option<BuildParams>>,
}

struct HandleState {
    command_tx: Option<mpsc::UnboundedSender<Command>>,
    started: bool,
}

struct BuildParams {
    subscriber_impl: Arc<dyn ShardSubscriber>,
    stream_and_shard_id: String,
}

impl FanOutRecordsPublisher {
    /// Construct with the SDK-backed subscriber over the given client (Java 4-arg
    /// constructor).
    pub fn new(
        kinesis: aws_sdk_kinesis::Client,
        shard_id: impl Into<String>,
        consumer_arn: impl Into<String>,
        stream_identifier: StreamIdentifier,
    ) -> Self {
        let shard_id = shard_id.into();
        let stream_and_shard_id = shard_id.clone();
        Self::with_subscriber(
            Arc::new(KinesisShardSubscriber::new(
                kinesis,
                shard_id,
                consumer_arn.into(),
                stream_identifier,
            )),
            stream_and_shard_id,
        )
    }

    /// Construct with the SDK-backed subscriber, multi-stream logging prefix (Java
    /// 5-arg constructor).
    pub fn new_multi_stream(
        kinesis: aws_sdk_kinesis::Client,
        shard_id: impl Into<String>,
        consumer_arn: impl Into<String>,
        stream_identifier_ser: impl Into<String>,
        stream_identifier: StreamIdentifier,
    ) -> Self {
        let shard_id = shard_id.into();
        let stream_and_shard_id = format!("{}:{}", stream_identifier_ser.into(), shard_id);
        Self::with_subscriber(
            Arc::new(KinesisShardSubscriber::new(
                kinesis,
                shard_id,
                consumer_arn.into(),
                stream_identifier,
            )),
            stream_and_shard_id,
        )
    }

    /// Construct with an injected [`ShardSubscriber`] (test seam / production wiring).
    pub fn with_subscriber(
        subscriber_impl: Arc<dyn ShardSubscriber>,
        stream_and_shard_id: String,
    ) -> Self {
        Self {
            inner: Mutex::new(HandleState {
                command_tx: None,
                started: false,
            }),
            last_successful_request_details: Arc::new(Mutex::new(RequestDetails::empty())),
            build: Mutex::new(Some(BuildParams {
                subscriber_impl,
                stream_and_shard_id,
            })),
        }
    }

    fn ensure_task_started(&self) -> mpsc::UnboundedSender<Command> {
        let mut inner = self.inner.lock().unwrap();
        if let Some(tx) = &inner.command_tx {
            return tx.clone();
        }
        // Lazily start the task the first time it is needed (start/subscribe).
        let params = self.build.lock().unwrap().take().expect("task built once");
        let (command_tx, command_rx) = mpsc::unbounded_channel();
        let (flow_event_tx, flow_event_rx) = mpsc::unbounded_channel();
        let state = PublisherState {
            subscriber: None,
            current_flow_id: None,
            next_flow_id: 1,
            current_sequence_number: ExtendedSequenceNumber::latest(),
            initial_position: InitialPositionInStreamExtended::new_initial_position(
                crate::common::InitialPositionInStream::Latest,
            ),
            is_first_connection: true,
            flow_connected: false,
            available_queue_space: 0,
            records_delivery_queue: VecDeque::new(),
            subscriber_impl: params.subscriber_impl,
            stream_and_shard_id: params.stream_and_shard_id,
            last_successful_request_details: Arc::clone(&self.last_successful_request_details),
            flow_event_tx,
        };
        tokio::spawn(run_task(state, command_rx, flow_event_rx));
        inner.command_tx = Some(command_tx.clone());
        command_tx
    }
}

#[async_trait]
impl RecordsPublisher for FanOutRecordsPublisher {
    async fn start(
        &self,
        extended_sequence_number: ExtendedSequenceNumber,
        initial_position_in_stream_extended: InitialPositionInStreamExtended,
    ) -> Result<(), BoxError> {
        // Java: `start` is `void`, synchronous, and never throws (it just
        // records the starting position under `lockObject`) — no I/O happens
        // here, so this never fails. The `Result` exists only for the shared
        // `RecordsPublisher::start` trait signature (`PrefetchRecordsPublisher`
        // needs it to surface a failed `GetShardIterator`).
        let tx = self.ensure_task_started();
        self.inner.lock().unwrap().started = true;
        let _ = tx.send(Command::Start {
            sequence_number: extended_sequence_number,
            initial_position: initial_position_in_stream_extended,
        });
        Ok(())
    }

    async fn restart_from(&self, records_retrieved: Arc<dyn RecordsRetrieved>) {
        let continuation = records_retrieved
            .as_any()
            .and_then(|any| any.downcast_ref::<FanoutRecordsRetrieved>())
            .map(|f| f.continuation_sequence_number().clone())
            .unwrap_or_else(|| {
                panic!("Provided ProcessRecordsInput not created from the FanOutRecordsPublisher")
            });
        let tx = self.ensure_task_started();
        let _ = tx.send(Command::RestartFrom(continuation));
    }

    async fn shutdown(&self) {
        let rx = {
            let mut inner = self.inner.lock().unwrap();
            inner.started = false;
            inner.command_tx.as_ref().map(|tx| {
                let (done_tx, done_rx) = tokio::sync::oneshot::channel();
                let _ = tx.send(Command::Shutdown(done_tx));
                done_rx
            })
        };
        if let Some(rx) = rx {
            let _ = rx.await;
        }
    }

    fn last_successful_request_details(&self) -> RequestDetails {
        self.last_successful_request_details.lock().unwrap().clone()
    }

    async fn notify(&self, ack: Box<dyn RecordsDeliveryAck>) {
        let tx = self.ensure_task_started();
        let _ = tx.send(Command::Ack(ack.batch_unique_identifier().clone()));
    }

    fn subscribe(&self) -> RecordsPublisherSubscription {
        let (subscription, sink) = new_subscription();
        let tx = self.ensure_task_started();
        let (ack_tx, _ack_rx) = tokio::sync::oneshot::channel();
        let _ = tx.send(Command::Subscribe { sink, ack: ack_tx });
        subscription
    }
}

/// The single owning task.
async fn run_task(
    mut state: PublisherState,
    mut command_rx: mpsc::UnboundedReceiver<Command>,
    mut flow_event_rx: mpsc::UnboundedReceiver<FlowEvent>,
) {
    loop {
        tokio::select! {
            // Downstream demand/cancel from the sink.
            demand = async {
                match state.subscriber.as_mut() {
                    Some(sink) => sink.next_demand().await,
                    None => std::future::pending().await,
                }
            } => {
                state.apply_demand_signal(demand);
            }
            cmd = command_rx.recv() => {
                match cmd {
                    Some(cmd) => {
                        if handle_command_guarded(&mut state, cmd).await {
                            return;
                        }
                    }
                    None => return,
                }
            }
            ev = flow_event_rx.recv() => {
                if let Some(ev) = ev {
                    handle_flow_event(&mut state, ev).await;
                }
            }
        }
    }
}

/// Guard [`handle_command`] with the same per-tick `catch (Throwable)`
/// containment `run_task`'s fetch/event-driver step already gets (Java wraps
/// the *whole* daemon-loop body — see `PrefetchRecordsPublisher.java` /
/// `run_task` in the polling sibling). Without this a panic while handling a
/// command (e.g. `Subscribe`) would unwind out of `run_task` and silently kill
/// the publisher's owning task: every later `subscribe()`/`notify()`/demand
/// send would hit a dead channel, permanently wedging the consumer (health
/// checks would keep re-subscribing into a channel nothing is listening on).
/// A caught panic is logged and never treated as a shutdown request.
async fn handle_command_guarded(state: &mut PublisherState, cmd: Command) -> bool {
    match crate::utils::panic_util::catch_tick(handle_command(state, cmd)).await {
        Ok(shutdown) => shutdown,
        Err(panic) => {
            tracing::error!(
                "{}: Unexpected exception was thrown while handling a command. This could probably be an issue or a bug. Please search for the exception/error online to check what is going on. If the issue persists or is a recurring problem, feel free to open an issue on, https://github.com/awslabs/amazon-kinesis-client. {}",
                state.stream_and_shard_id,
                panic
            );
            false
        }
    }
}

async fn handle_command(state: &mut PublisherState, cmd: Command) -> bool {
    match cmd {
        Command::Start {
            sequence_number,
            initial_position,
        } => {
            state.current_sequence_number = sequence_number;
            state.initial_position = initial_position;
            state.is_first_connection = true;
        }
        Command::Subscribe { sink, ack } => {
            // A cancel (or dropped handle) from the previous subscription may
            // still be queued on its demand channel — apply it before deciding
            // whether a live subscriber actually exists.
            state.drain_pending_demand();
            if state.subscriber.is_some() {
                tracing::error!(
                    "{}: A subscribe occurred while there was an active subscriber. Sending error to current subscriber",
                    state.stream_and_shard_id
                );
                // Java: onError(MultipleSubscriberException) to BOTH the current
                // and the attempted subscriber, then terminate the flow. The
                // error (not a silent completion) lets ShardConsumerSubscriber
                // record a retrieval failure and restart on its next health
                // check.
                if let Some(existing) = state.subscriber.take() {
                    // The old consumer may have an undelivered batch occupying
                    // its capacity-1 channel; never block the task on it —
                    // dropping the sink still completes that consumer.
                    let _ = tokio::time::timeout(
                        std::time::Duration::ZERO,
                        existing.deliver_error(RetrievalError::other(
                            MultipleSubscriberError.to_string(),
                        )),
                    )
                    .await;
                }
                let _ = sink
                    .deliver_error(RetrievalError::other(MultipleSubscriberError.to_string()))
                    .await;
                if let Some(flow_id) = state.current_flow_id.take() {
                    state.subscriber_impl.cancel(flow_id);
                }
                let _ = ack.send(Err(MultipleSubscriberError));
                // The new sink is dropped here (never stored) → its channel closes.
                drop(sink);
            } else {
                if let Some(flow_id) = state.current_flow_id.take() {
                    state.subscriber_impl.cancel(flow_id);
                }
                state.subscriber = Some(sink);
                let seq = state.current_sequence_number.clone();
                state.subscribe_to_shard(seq).await;
                let _ = ack.send(Ok(()));
            }
        }
        Command::Ack(id) => {
            state.handle_ack(&id).await;
        }
        Command::RestartFrom(continuation) => {
            if let Some(flow_id) = state.current_flow_id.take() {
                state.subscriber_impl.cancel(flow_id);
            }
            state.current_sequence_number = continuation;
        }
        Command::Shutdown(done) => {
            if let Some(flow_id) = state.current_flow_id.take() {
                state.subscriber_impl.cancel(flow_id);
            }
            let _ = done.send(());
            return true;
        }
    }
    false
}

async fn handle_flow_event(state: &mut PublisherState, ev: FlowEvent) {
    match ev {
        FlowEvent::Started { flow_id } => {
            if flow_id != u64::MAX {
                state.flow_started(flow_id);
            }
        }
        FlowEvent::Records { flow_id, event } => {
            state.records_received(flow_id, *event).await;
        }
        FlowEvent::ResponseReceived {
            flow_id,
            request_id,
        } => {
            if state.is_active_flow(flow_id) || state.current_flow_id.is_none() {
                *state.last_successful_request_details.lock().unwrap() =
                    RequestDetails::new(request_id, chrono::Utc::now().to_rfc3339());
            }
        }
        FlowEvent::Complete { flow_id } => {
            state.flow_complete(flow_id).await;
        }
        FlowEvent::Error { flow_id, error } => {
            state.flow_error(flow_id, error).await;
        }
    }
}

mod kinesis_subscriber;
pub use kinesis_subscriber::KinesisShardSubscriber;

#[cfg(test)]
mod tests;
