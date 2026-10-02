//! Port of `software.amazon.kinesis.retrieval.RecordsPublisher`.
//!
//! This is the **central abstraction** of the retrieval subsystem. In Java it
//! extends `org.reactivestreams.Publisher<RecordsRetrieved>` and adds the
//! KCL-specific lifecycle (`start` / `restartFrom` / `shutdown` /
//! `getLastSuccessfulRequestDetails` / `notify(ack)`). The reactive-streams
//! demand/ack backpressure is bespoke: a single active subscriber, manual
//! `request(n)` credit, exactly one in-flight `onNext` at a time, and a separate
//! ack path decoupled from `request(n)` that drives which batch is delivered
//! next.
//!
//! # Rust design (actor / channel model)
//!
//! Following the arch-map's actor-model recommendation and the
//! [`PORTING.md`] convention (reactive `Publisher`/`Subscriber` →
//! `futures::Stream` + tokio channels), the reactive contract is expressed as:
//!
//! * **[`RecordsPublisher`]** — an object-safe `async_trait` with `start`,
//!   `shutdown`, `restart_from`, `last_successful_request_details`, `notify`, and
//!   `subscribe`. Implementations own their state behind a single mutex or a
//!   dedicated task (the "actor"), exactly mirroring Java's coarse `lockObject`.
//!
//! * **[`RecordsPublisherSubscription`]** — the handle handed back by
//!   `subscribe`, wiring three things to the single downstream consumer
//!   (the lifecycle wave's `ShardConsumer`):
//!     1. a **delivery channel** `mpsc::Receiver<Arc<dyn RecordsRetrieved>>` the
//!        consumer awaits (the `onNext` stream — at most one item is in flight
//!        because the consumer requests one at a time);
//!     2. a **demand path** [`request`](RecordsPublisherSubscription::request) —
//!        the consumer's `Subscription.request(n)` (additive credit; the consumer
//!        calls `request(1)` on subscribe and again after each processed batch);
//!     3. a **cancel path** [`cancel`](RecordsPublisherSubscription::cancel) —
//!        the consumer's `Subscription.cancel()`.
//!
//!   Acks flow back through [`RecordsPublisher::notify`]: the consumer builds a
//!   [`SimpleRecordsDeliveryAck`] from the delivered batch's
//!   [`BatchUniqueIdentifier`] and calls `notify(ack)`, keeping the ack path
//!   decoupled from `request(n)` exactly as in Java.
//!
//! ## Consumer usage (mirrors `ShardConsumerSubscriber`)
//!
//! ```no_run
//! use std::sync::Arc;
//!
//! use kcl::retrieval::records_delivery_ack::SimpleRecordsDeliveryAck;
//! use kcl::retrieval::records_publisher::RecordsPublisher;
//! use kcl::retrieval::records_retrieved::RecordsRetrieved;
//!
//! // The consumer side (mirrors `ShardConsumerSubscriber`): subscribe, then run
//! // the request → recv → ack → request loop until the publisher completes.
//! async fn consume(publisher: Arc<dyn RecordsPublisher>) {
//!     let mut sub = publisher.subscribe();            // ~ onSubscribe
//!     sub.request(1);                                 // request one batch (additive demand)
//!     // (start()'s Result is omitted here for brevity; a real caller must
//!     // handle Err by retrying start, not proceeding to subscribe.)
//!     while let Some(delivery) = sub.recv().await {   // ~ onNext / onError (one in flight)
//!         let batch = match delivery {
//!             Ok(batch) => batch,
//!             // ~ onError → ShardConsumerSubscriber::note_retrieval_failure
//!             Err(err) => { eprintln!("retrieval failed: {err}"); break; }
//!         };
//!         let ack = SimpleRecordsDeliveryAck::new(batch.batch_unique_identifier());
//!         let _input = batch.process_records_input(); // hand to the record processor
//!         publisher.notify(Box::new(ack)).await;      // ack this batch
//!         sub.request(1);                             // request the next one
//!     }
//! }
//! # fn main() { let _ = consume; }
//! ```
//!
//! ## Publisher-side wiring
//!
//! `subscribe` returns both the consumer handle and, internally, the sink side
//! (the `DeliverySender` + demand/cancel receivers) that the implementation's
//! task/state uses to push batches and observe demand. To keep the trait
//! object-safe and let each implementation choose how it holds the sink, the
//! plumbing pieces are exposed via [`new_subscription`], which mints a matched
//! `(RecordsPublisherSubscription, RecordsPublisherSink)` pair. A publisher's
//! `subscribe` calls `new_subscription()`, stores the [`RecordsPublisherSink`],
//! and returns the [`RecordsPublisherSubscription`].
//!
//! [`PORTING.md`]: ../../../PORTING.md
//! [`SimpleRecordsDeliveryAck`]: crate::retrieval::records_delivery_ack::SimpleRecordsDeliveryAck
//! [`BatchUniqueIdentifier`]: crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier

use std::sync::Arc;

use async_trait::async_trait;
use tokio::sync::mpsc;

use crate::common::request_details::RequestDetails;
use crate::common::InitialPositionInStreamExtended;
use crate::exceptions::BoxError;
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::records_delivery_ack::RecordsDeliveryAck;
use crate::retrieval::records_retrieved::RecordsRetrieved;
use crate::retrieval::RetrievalError;

/// One item flowing through the publisher→consumer delivery channel: either a
/// delivered batch (`onNext`) or a retrieval failure (`onError`).
///
/// # Integration seam (subscriber↔publisher error path)
///
/// Java's reactive `Subscriber` has both `onNext(RecordsRetrieved)` and
/// `onError(Throwable)`. The ported channel originally carried only the batch
/// (`Arc<dyn RecordsRetrieved>`), signalling completion by closing the channel
/// (`recv() -> None` = `onComplete`) but having **no way to signal an error**.
/// This alias adds the `Err` arm so the concrete publishers
/// (`PrefetchRecordsPublisher` / `FanOutRecordsPublisher`) can deliver a
/// [`RetrievalError`] that [`ShardConsumerSubscriber`] turns into
/// `note_retrieval_failure(err, is_read_timeout)` — driving its restart /
/// health-check logic exactly as Java's `onError`.
///
/// [`ShardConsumerSubscriber`]: crate::lifecycle::ShardConsumerSubscriber
pub type RecordsDelivery = Result<Arc<dyn RecordsRetrieved>, RetrievalError>;

/// A demand or cancel signal sent from the consumer to the publisher.
///
/// The reactive-streams `Subscription.request(n)` and `Subscription.cancel()`
/// calls become messages on this control channel, so the publisher's state
/// (whether a task or a mutex-guarded struct) can observe them without shared
/// locking — the actor-model translation of Java's `lockObject`-guarded
/// `availableQueueSpace`/cancel handling.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DemandSignal {
    /// Additive demand: request `n` more batches (Java `Subscription.request(n)`).
    Request(u64),
    /// Cancel the subscription; deliver no further batches (Java
    /// `Subscription.cancel()`).
    Cancel,
}

/// The consumer-facing subscription handle returned by
/// [`RecordsPublisher::subscribe`].
///
/// Holds the receiving end of the delivery channel and the sending end of the
/// demand/cancel control channel. Dropping it (or calling
/// [`cancel`](Self::cancel)) tears down the subscription.
pub struct RecordsPublisherSubscription {
    delivery_rx: mpsc::Receiver<RecordsDelivery>,
    demand_tx: mpsc::UnboundedSender<DemandSignal>,
}

impl RecordsPublisherSubscription {
    /// Receive the next delivery: `Some(Ok(batch))` (`onNext`),
    /// `Some(Err(error))` (`onError`), or `None` when the publisher has
    /// completed/shut down and closed the delivery channel (`onComplete`).
    ///
    /// The consumer requests one batch at a time, so at most one batch is in
    /// flight — matching Java's single-in-flight `onNext` guarantee.
    pub async fn recv(&mut self) -> Option<RecordsDelivery> {
        self.delivery_rx.recv().await
    }

    /// Signal additive demand for `n` more batches (Java
    /// `Subscription.request(n)`). Returns `false` if the publisher is gone.
    pub fn request(&self, n: u64) -> bool {
        self.demand_tx.send(DemandSignal::Request(n)).is_ok()
    }

    /// Cancel the subscription (Java `Subscription.cancel()`). No further batches
    /// will be delivered.
    pub fn cancel(&self) {
        let _ = self.demand_tx.send(DemandSignal::Cancel);
    }
}

/// The publisher-side sink paired with a [`RecordsPublisherSubscription`].
///
/// A [`RecordsPublisher`] implementation stores this after `subscribe`, pushes
/// batches to the consumer via [`deliver`](Self::deliver), observes demand/cancel
/// via [`next_demand`](Self::next_demand), and completes the stream by dropping
/// the sink (or calling [`complete`](Self::complete)).
pub struct RecordsPublisherSink {
    delivery_tx: mpsc::Sender<RecordsDelivery>,
    demand_rx: mpsc::UnboundedReceiver<DemandSignal>,
}

impl RecordsPublisherSink {
    /// Deliver a batch to the consumer (`onNext`). Returns `false` if the
    /// consumer's receiver is gone (subscription cancelled/dropped).
    pub async fn deliver(&self, records: Arc<dyn RecordsRetrieved>) -> bool {
        self.delivery_tx.send(Ok(records)).await.is_ok()
    }

    /// Deliver a retrieval error to the consumer (`onError`). Returns `false` if
    /// the consumer's receiver is gone.
    ///
    /// Part of the subscriber↔publisher error-path seam: concrete publishers call
    /// this when a retrieval fails so the [`ShardConsumerSubscriber`] can invoke
    /// `note_retrieval_failure` and restart, instead of silently completing.
    ///
    /// [`ShardConsumerSubscriber`]: crate::lifecycle::ShardConsumerSubscriber
    pub async fn deliver_error(&self, error: RetrievalError) -> bool {
        self.delivery_tx.send(Err(error)).await.is_ok()
    }

    /// Observe the next demand/cancel signal from the consumer, or `None` when
    /// the subscription handle has been dropped.
    pub async fn next_demand(&mut self) -> Option<DemandSignal> {
        self.demand_rx.recv().await
    }

    /// Non-blocking poll of the next demand/cancel signal.
    ///
    /// Returns `Err(TryRecvError)` when no signal is currently queued (or the
    /// channel is closed). Used by actor-style publishers that batch-drain demand
    /// alongside their own command channel each loop iteration.
    pub fn try_next_demand(&mut self) -> Result<DemandSignal, mpsc::error::TryRecvError> {
        self.demand_rx.try_recv()
    }

    /// Complete the stream (`onComplete`): closing the delivery channel makes the
    /// consumer's [`recv`](RecordsPublisherSubscription::recv) return `None`.
    /// Equivalent to dropping the sink.
    pub fn complete(self) {}
}

/// Mint a matched subscription/sink pair.
///
/// The delivery channel has capacity 1: because the consumer requests one batch
/// at a time and the publisher only delivers on demand, a capacity of 1 is
/// sufficient and keeps at most one batch buffered in the channel (backpressure
/// is driven by the demand path, not the channel depth).
pub fn new_subscription() -> (RecordsPublisherSubscription, RecordsPublisherSink) {
    let (delivery_tx, delivery_rx) = mpsc::channel(1);
    let (demand_tx, demand_rx) = mpsc::unbounded_channel();
    (
        RecordsPublisherSubscription {
            delivery_rx,
            demand_tx,
        },
        RecordsPublisherSink {
            delivery_tx,
            demand_rx,
        },
    )
}

/// Retrieves records from Kinesis for processing and delivers them to a single
/// downstream subscriber (the `ShardConsumer`) with demand/ack backpressure.
///
/// Port of the Java `RecordsPublisher` interface. Object-safe and
/// `Send + Sync` so it can be held as `Arc<dyn RecordsPublisher>` and driven from
/// the lifecycle state machine. Both `FanOutRecordsPublisher` (EFO) and
/// `PrefetchRecordsPublisher` (polling) — read in the retrieval-impl wave — will
/// implement this trait; a simple in-memory test impl in this module's test
/// submodule validates the mechanism.
#[async_trait]
pub trait RecordsPublisher: Send + Sync {
    /// Initialize the publisher with where to start processing. If there is a
    /// stored sequence number the publisher begins from it; otherwise it uses
    /// `initial_position`.
    ///
    /// Port of `start(ExtendedSequenceNumber, InitialPositionInStreamExtended)`.
    /// Async because implementations perform Kinesis I/O to establish the
    /// subscription/iterator.
    ///
    /// # Error semantics (2026-07-14 fix)
    ///
    /// Returns `Err` if that I/O fails (e.g. `PrefetchRecordsPublisher`'s
    /// `GetShardIterator` call times out or hits a non-`ResourceNotFound` SDK
    /// error). This mirrors Java, where `advanceIteratorTo`'s exception
    /// propagates out of `PublisherSession.init` → `start` → `InitializeTask`,
    /// which is caught there, backed off, and the task (and thus this `start`
    /// call) is retried. `FanOutRecordsPublisher::start` never does synchronous
    /// I/O (Java: `void`, no throws) and always returns `Ok(())`; a caller must
    /// not spawn/attach a delivery task on `Err` — the publisher must remain
    /// startable again on retry (not `started`).
    async fn start(
        &self,
        extended_sequence_number: ExtendedSequenceNumber,
        initial_position_in_stream_extended: InitialPositionInStreamExtended,
    ) -> Result<(), BoxError>;

    /// Restart delivery from the last accepted and processed batch.
    ///
    /// Port of `restartFrom(RecordsRetrieved)`. `BlockingRecordsPublisher`
    /// (retrieval-impl wave) leaves this unsupported (panics).
    async fn restart_from(&self, records_retrieved: Arc<dyn RecordsRetrieved>);

    /// Shut the publisher down. After this returns the publisher provides no
    /// further records. Port of `shutdown()`.
    async fn shutdown(&self);

    /// Details of the last successful retrieval request (for operator
    /// diagnostics). Port of `getLastSuccessfulRequestDetails()`.
    fn last_successful_request_details(&self) -> RequestDetails;

    /// Notify the publisher of a delivery ack from the subscriber.
    ///
    /// Port of the Java default `notify(RecordsDeliveryAck)`, which throws
    /// `UnsupportedOperationException` unless overridden. Real publishers (EFO /
    /// polling) override this to drive their ack-based delivery. The default here
    /// `panic!`s with the same message.
    async fn notify(&self, _ack: Box<dyn RecordsDeliveryAck>) {
        panic!("RecordsPublisher does not support acknowledgement from Subscriber")
    }

    /// Subscribe the single downstream consumer, returning the
    /// [`RecordsPublisherSubscription`] handle it uses to receive batches, signal
    /// demand, and cancel.
    ///
    /// Port of `Publisher::subscribe(Subscriber)`. Implementations call
    /// [`new_subscription`], store the [`RecordsPublisherSink`], and return the
    /// subscription. Enforcing "at most one active subscriber" (Java's
    /// `MultipleSubscriberException`) is the implementation's responsibility.
    fn subscribe(&self) -> RecordsPublisherSubscription;
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lifecycle::events::process_records_input::ProcessRecordsInput;
    use crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier;
    use crate::retrieval::kinesis_client_record::KinesisClientRecord;
    use crate::retrieval::records_delivery_ack::SimpleRecordsDeliveryAck;
    use crate::retrieval::records_retrieved::RecordsRetrieved;
    use std::sync::Mutex;

    /// A minimal [`RecordsRetrieved`] carrying a pre-built input + batch id.
    #[derive(Debug)]
    struct TestRecordsRetrieved {
        input: ProcessRecordsInput,
        batch_id: BatchUniqueIdentifier,
    }

    impl RecordsRetrieved for TestRecordsRetrieved {
        fn process_records_input(&self) -> &ProcessRecordsInput {
            &self.input
        }
        fn batch_unique_identifier(&self) -> BatchUniqueIdentifier {
            self.batch_id.clone()
        }
    }

    /// A simple in-memory publisher for validating the subscription/demand/ack
    /// mechanism. It spawns a task that, on each `request(1)`, delivers one of a
    /// fixed set of pre-canned batches, and records every ack it receives.
    struct InMemoryPublisher {
        sink: Mutex<Option<RecordsPublisherSink>>,
        batches: Mutex<Vec<Arc<dyn RecordsRetrieved>>>,
        acks: Arc<Mutex<Vec<BatchUniqueIdentifier>>>,
        started: Mutex<bool>,
        last_request: Mutex<RequestDetails>,
    }

    impl InMemoryPublisher {
        fn new(batches: Vec<Arc<dyn RecordsRetrieved>>) -> Self {
            Self {
                sink: Mutex::new(None),
                batches: Mutex::new(batches),
                acks: Arc::new(Mutex::new(Vec::new())),
                started: Mutex::new(false),
                last_request: Mutex::new(RequestDetails::empty()),
            }
        }
    }

    #[async_trait]
    impl RecordsPublisher for InMemoryPublisher {
        async fn start(
            &self,
            _extended_sequence_number: ExtendedSequenceNumber,
            _initial_position: InitialPositionInStreamExtended,
        ) -> Result<(), BoxError> {
            *self.started.lock().unwrap() = true;
            *self.last_request.lock().unwrap() = RequestDetails::new("req-1", "2024-01-01");

            // Take the sink and spawn the delivery loop: on each Request(n),
            // deliver up to n queued batches (one at a time, honoring demand).
            let mut sink = self
                .sink
                .lock()
                .unwrap()
                .take()
                .expect("subscribe must be called before start");
            let batches: Vec<_> = std::mem::take(&mut *self.batches.lock().unwrap());
            tokio::spawn(async move {
                let mut idx = 0usize;
                while let Some(signal) = sink.next_demand().await {
                    match signal {
                        DemandSignal::Request(n) => {
                            for _ in 0..n {
                                if idx >= batches.len() {
                                    // Nothing more to deliver: complete.
                                    return;
                                }
                                if !sink.deliver(batches[idx].clone()).await {
                                    return;
                                }
                                idx += 1;
                            }
                        }
                        DemandSignal::Cancel => return,
                    }
                }
            });
            Ok(())
        }

        async fn restart_from(&self, _records_retrieved: Arc<dyn RecordsRetrieved>) {}

        async fn shutdown(&self) {}

        fn last_successful_request_details(&self) -> RequestDetails {
            self.last_request.lock().unwrap().clone()
        }

        async fn notify(&self, ack: Box<dyn RecordsDeliveryAck>) {
            self.acks
                .lock()
                .unwrap()
                .push(ack.batch_unique_identifier().clone());
        }

        fn subscribe(&self) -> RecordsPublisherSubscription {
            let (subscription, sink) = new_subscription();
            *self.sink.lock().unwrap() = Some(sink);
            subscription
        }
    }

    fn batch(seq: &str) -> Arc<dyn RecordsRetrieved> {
        let input = ProcessRecordsInput::builder()
            .records(vec![KinesisClientRecord::builder()
                .sequence_number(seq.to_string())
                .build()])
            .build();
        Arc::new(TestRecordsRetrieved {
            input,
            batch_id: BatchUniqueIdentifier::new(seq, "flow-1"),
        })
    }

    #[tokio::test]
    async fn subscribe_request_deliver_ack_cycle() {
        let publisher = Arc::new(InMemoryPublisher::new(vec![
            batch("seq-1"),
            batch("seq-2"),
            batch("seq-3"),
        ]));

        // ~ ShardConsumerSubscriber: subscribe, then drive the request/ack loop.
        let mut subscription = publisher.subscribe();
        publisher
            .start(
                ExtendedSequenceNumber::latest(),
                InitialPositionInStreamExtended::new_initial_position(
                    crate::common::InitialPositionInStream::Latest,
                ),
            )
            .await
            .unwrap();

        let mut received = Vec::new();
        subscription.request(1);
        while let Some(batch) = subscription.recv().await {
            let batch = batch.expect("no error expected");
            let bid = batch.batch_unique_identifier();
            received.push(bid.record_batch_identifier().to_string());
            // Ack this batch, then request the next.
            let ack = SimpleRecordsDeliveryAck::new(bid);
            publisher.notify(Box::new(ack)).await;
            subscription.request(1);
        }

        assert_eq!(received, vec!["seq-1", "seq-2", "seq-3"]);
        let acks = publisher.acks.lock().unwrap();
        let acked: Vec<_> = acks.iter().map(|b| b.record_batch_identifier()).collect();
        assert_eq!(acked, vec!["seq-1", "seq-2", "seq-3"]);
    }

    #[tokio::test]
    async fn cancel_stops_delivery() {
        let publisher = Arc::new(InMemoryPublisher::new(vec![
            batch("a"),
            batch("b"),
            batch("c"),
        ]));
        let mut subscription = publisher.subscribe();
        publisher
            .start(
                ExtendedSequenceNumber::latest(),
                InitialPositionInStreamExtended::new_initial_position(
                    crate::common::InitialPositionInStream::Latest,
                ),
            )
            .await
            .unwrap();

        subscription.request(1);
        let first = subscription
            .recv()
            .await
            .unwrap()
            .expect("no error expected");
        assert_eq!(
            first.batch_unique_identifier().record_batch_identifier(),
            "a"
        );
        subscription.cancel();
        // After cancel the delivery loop returns and closes the channel.
        assert!(subscription.recv().await.is_none());
    }

    #[tokio::test]
    async fn last_successful_request_details_surfaced() {
        let publisher = Arc::new(InMemoryPublisher::new(vec![]));
        let _sub = publisher.subscribe();
        assert_eq!(
            publisher.last_successful_request_details().request_id(),
            "NONE"
        );
        publisher
            .start(
                ExtendedSequenceNumber::latest(),
                InitialPositionInStreamExtended::new_initial_position(
                    crate::common::InitialPositionInStream::Latest,
                ),
            )
            .await
            .unwrap();
        assert_eq!(
            publisher.last_successful_request_details().request_id(),
            "req-1"
        );
    }

    #[tokio::test]
    #[should_panic(expected = "RecordsPublisher does not support acknowledgement from Subscriber")]
    async fn default_notify_panics() {
        struct BarebonesPublisher;
        #[async_trait]
        impl RecordsPublisher for BarebonesPublisher {
            async fn start(
                &self,
                _: ExtendedSequenceNumber,
                _: InitialPositionInStreamExtended,
            ) -> Result<(), BoxError> {
                Ok(())
            }
            async fn restart_from(&self, _: Arc<dyn RecordsRetrieved>) {}
            async fn shutdown(&self) {}
            fn last_successful_request_details(&self) -> RequestDetails {
                RequestDetails::empty()
            }
            fn subscribe(&self) -> RecordsPublisherSubscription {
                new_subscription().0
            }
        }
        let p = BarebonesPublisher;
        p.notify(Box::new(SimpleRecordsDeliveryAck::new(
            BatchUniqueIdentifier::new("x", "y"),
        )))
        .await;
    }

    #[test]
    #[should_panic(expected = "Retrieval of batch unique identifier is not supported")]
    fn default_batch_unique_identifier_panics() {
        #[derive(Debug)]
        struct NoId(ProcessRecordsInput);
        impl RecordsRetrieved for NoId {
            fn process_records_input(&self) -> &ProcessRecordsInput {
                &self.0
            }
        }
        let r = NoId(ProcessRecordsInput::builder().build());
        let _ = r.batch_unique_identifier();
    }
}
