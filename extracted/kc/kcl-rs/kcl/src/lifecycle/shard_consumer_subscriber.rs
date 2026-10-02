//! Port of `software.amazon.kinesis.lifecycle.{ShardConsumerSubscriber,
//! NotifyingSubscriber, ShardConsumerNotifyingSubscriber}`.
//!
//! # Rust design (tokio task + channels, replacing RxJava)
//!
//! Java bridges the reactive-streams [`RecordsPublisher`] (a `Flowable`) to the
//! `ShardConsumer` with RxJava3 (`subscribeOn`/`observeOn`, a private
//! `lockObject`, and explicit `request(n)` demand). Rust has no RxJava; the port
//! uses the retrieval subsystem's channel-based [`RecordsPublisherSubscription`]
//! (see `retrieval::records_publisher`) driven by a **spawned tokio task** — the
//! "subscription loop":
//!
//! 1. `subscribe()` → a fresh [`RecordsPublisherSubscription`].
//! 2. `request(1)` (the `onSubscribe` initial pull).
//! 3. `recv().await` a batch (`onNext`), stamp `cacheExitTime`, dispatch to the
//!    `ShardConsumer` via `handle_input`, then `notify(ack)` back to the publisher
//!    (the `NotifyingSubscriber` ack-before-delegate ordering), then `request(1)`
//!    again (the `onNext` finally-block request).
//! 4. Channel close → `onComplete` (no automatic restart — restart is driven by
//!    `health_check`).
//!
//! **The `NotifyingSubscriber`/`ShardConsumerNotifyingSubscriber` decorator** is
//! folded into the loop: the ack (built from the batch's
//! `BatchUniqueIdentifier`) is sent via `RecordsPublisher::notify` **before**
//! dispatching to the consumer, exactly as `NotifyingSubscriber.onNext` does.
//!
//! `lastRequestTime`/`lastAccepted`/`dispatchFailure`/`retrievalFailure` live in
//! a single `std::sync::Mutex<SubscriberState>` (Java's `lockObject`); the
//! volatile `lastDataArrival`/`dispatchFailure`/`retrievalFailure` are read via
//! that mutex. `read_timeout_since_last_read` is an `AtomicI32`.
//!
//! # Deviation — the retrieval error path
//!
//! Java's publisher calls `subscriber.onError(t)`; the ported channel trait has
//! no `onError` (channel close = `onComplete`). The subscriber therefore exposes
//! [`note_retrieval_failure`](ShardConsumerSubscriber::note_retrieval_failure)
//! (the `onError` equivalent) which a publisher's error path calls; the wave-8
//! concrete publishers will wire it (`// TODO(port)`). The restart/health-check
//! logic is fully ported and tested via that seam.

use std::sync::atomic::{AtomicI32, Ordering};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use tokio::sync::mpsc;

use crate::exceptions::BoxError;
use crate::retrieval::{RecordsPublisher, RecordsRetrieved, SimpleRecordsDeliveryAck};

/// Which `onError` warning (if any) the ReadTimeout grace-period logic emitted.
///
/// Port of the `logOnErrorWarning` / `logOnErrorReadTimeoutWarning` seam that the
/// Java test overrides to count log emissions. Exposing it as the return value of
/// [`ShardConsumerSubscriber::note_retrieval_failure`] lets the suppression logic
/// be unit-tested without a logging-capture harness (the production call site
/// simply discards it).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RetrievalWarning {
    /// No warning was logged (an intermittent ReadTimeout within the ignore quota).
    None,
    /// The generic `logOnErrorWarning` was emitted (non-ReadTimeout failure).
    Generic,
    /// The `logOnErrorReadTimeoutWarning` was emitted (ReadTimeout past the quota).
    ReadTimeout,
}

/// A shutdown/handle-input target for the subscriber. The real
/// [`ShardConsumer`](crate::lifecycle::ShardConsumer) implements this; tests use a
/// recording stub.
///
/// Port of the `shardConsumer.handleInput(input, subscription)` call the RxJava
/// `onNext` makes. The `subscription`-cancel argument is folded into the return:
/// returning `true` means "cancel the subscription and stop the loop" (the Java
/// `subscription.cancel()` inside `handleInput`, e.g. on shutdown-requested /
/// end-of-shard).
pub trait InputHandler: Send + Sync {
    /// Dispatch a batch. Returns `true` if the subscription should be cancelled
    /// (stop delivering) — mirrors `ShardConsumer.handleInput` calling
    /// `subscription.cancel()`.
    fn handle_input(&self, input: crate::lifecycle::events::ProcessRecordsInput) -> bool;
}

/// State guarded by the subscriber's single mutex (Java's `lockObject`).
#[derive(Default)]
struct SubscriberState {
    /// Last time a request to upstream was made (incl. the initial subscription
    /// attempt); `None` once a response has been received but not re-armed.
    last_request_time: Option<Instant>,
    /// The last successfully delivered batch (the resume point on restart).
    last_accepted: Option<Arc<dyn RecordsRetrieved>>,
    /// Last time data arrived (for the "no data retrieved" health log).
    last_data_arrival: Option<Instant>,
    /// A failure from `handle_input` on the dispatch path (skipped batch).
    dispatch_failure: Option<BoxError>,
    /// A retrieval failure from the publisher (to be picked up by `health_check`).
    retrieval_failure: Option<BoxError>,
    /// Whether the loop task is currently running (a live subscription exists).
    running: bool,
    /// Cancel signal to the live subscription loop (Java's `subscription` field:
    /// `cancel()` forwards to `Subscription.cancel()`). The loop owns the
    /// subscription handle, so cancellation is relayed to it.
    cancel_tx: Option<mpsc::UnboundedSender<()>>,
}

/// Subscribes to a [`RecordsPublisher`] and pumps batches to the
/// [`InputHandler`] (`ShardConsumer`), with stall/error detection and automatic
/// resubscription. Port of `ShardConsumerSubscriber`.
pub struct ShardConsumerSubscriber {
    records_publisher: Arc<dyn RecordsPublisher>,
    /// RxJava `observeOn` buffer size; `0` = fully synchronous. Retained for
    /// fidelity (the channel model already applies backpressure via demand).
    #[allow(dead_code)]
    buffer_size: i32,
    shard_consumer: Arc<dyn InputHandler>,
    read_timeouts_to_ignore_before_warning: i32,
    shard_info_id: String,

    read_timeout_since_last_read: AtomicI32,
    state: Mutex<SubscriberState>,
}

impl ShardConsumerSubscriber {
    /// Construct a subscriber. `shard_info_id` is the lease key of the shard (Java
    /// `ShardInfo.getLeaseKey(shardConsumer.shardInfo())`, used only for logging).
    pub fn new(
        records_publisher: Arc<dyn RecordsPublisher>,
        buffer_size: i32,
        shard_consumer: Arc<dyn InputHandler>,
        read_timeouts_to_ignore_before_warning: i32,
        shard_info_id: String,
    ) -> Self {
        Self {
            records_publisher,
            buffer_size,
            shard_consumer,
            read_timeouts_to_ignore_before_warning,
            shard_info_id,
            read_timeout_since_last_read: AtomicI32::new(0),
            state: Mutex::new(SubscriberState::default()),
        }
    }

    /// Start (or restart) the subscription. Port of `startSubscriptions()`.
    ///
    /// Arms the stall-detection timer, restarts the publisher from the last
    /// accepted batch (if any), subscribes fresh, and spawns the delivery loop.
    pub fn start_subscriptions(self: &Arc<Self>) {
        let (cancel_tx, mut cancel_rx) = mpsc::unbounded_channel::<()>();
        let last_accepted = {
            let mut st = self.state.lock().unwrap();
            st.last_request_time = Some(Instant::now());
            st.running = true;
            st.cancel_tx = Some(cancel_tx);
            st.last_accepted.clone()
        };

        let this = Arc::clone(self);
        tokio::spawn(async move {
            if let Some(last) = last_accepted {
                this.records_publisher.restart_from(last).await;
            }
            let mut subscription = this.records_publisher.subscribe();
            // onSubscribe: request the first batch.
            subscription.request(1);

            loop {
                // Java `subscription.cancel()`: `cancel()` signals this loop,
                // which cancels the subscription it owns and stops.
                let delivery = tokio::select! {
                    biased;
                    _ = cancel_rx.recv() => {
                        subscription.cancel();
                        break;
                    }
                    delivery = subscription.recv() => delivery,
                };
                let Some(delivery) = delivery else { break };
                // onError: a publisher delivered a retrieval failure. Record it
                // (applying the ReadTimeout grace period) and stop the loop; the
                // next health_check restarts the subscription. This is the
                // subscriber side of the subscriber↔publisher error-path seam.
                let batch = match delivery {
                    Ok(batch) => batch,
                    Err(err) => {
                        let is_read_timeout =
                            err.is_retryable() && err.message().contains("ReadTimeout");
                        subscription.cancel();
                        let _ = this.note_retrieval_failure(Box::new(err), is_read_timeout);
                        break;
                    }
                };
                // onNext: mark the request as answered, stamp arrival.
                {
                    let mut st = this.state.lock().unwrap();
                    st.last_request_time = None;
                    st.last_data_arrival = Some(Instant::now());
                }

                // NotifyingSubscriber: ack the batch to the publisher BEFORE
                // delegating to the real subscriber's onNext logic.
                let ack = SimpleRecordsDeliveryAck::new(batch.batch_unique_identifier());
                this.records_publisher.notify(Box::new(ack)).await;

                // Dispatch to the ShardConsumer, stamping cacheExitTime.
                let input = batch
                    .process_records_input()
                    .clone()
                    .with_cache_exit_time(chrono::Utc::now());
                let cancel = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                    this.shard_consumer.handle_input(input)
                }));
                let cancel = match cancel {
                    Ok(c) => c,
                    Err(_) => {
                        // handleInput threw: store as dispatchFailure, skip batch.
                        let mut st = this.state.lock().unwrap();
                        st.dispatch_failure =
                            Some(Box::<dyn std::error::Error + Send + Sync>::from(
                                "Exception occurred while dispatching incoming data",
                            ));
                        false
                    }
                };

                // finally: re-arm and record the accepted batch.
                {
                    let mut st = this.state.lock().unwrap();
                    st.last_accepted = Some(Arc::clone(&batch));
                    st.last_request_time = Some(Instant::now());
                }
                this.reset_read_timeout_counter();

                if cancel {
                    subscription.cancel();
                    break;
                }
                // Request the next batch (onNext finally-block request(1)).
                subscription.request(1);
            }

            let mut st = this.state.lock().unwrap();
            st.running = false;
        });
    }

    /// Health check: restart on a prior retrieval failure, else restart a stalled
    /// subscription. Port of `healthCheck(maxTimeBetweenRequests)`.
    ///
    /// Returns the prior retrieval failure (if any) so `ShardConsumer.healthCheck`
    /// can surface it.
    pub fn health_check(
        self: &Arc<Self>,
        max_time_between_requests_millis: i64,
    ) -> Option<BoxError> {
        let result = self.restart_if_failed();
        if result.is_none() {
            self.restart_if_request_timer_expired(max_time_between_requests_millis);
        }
        result
    }

    fn restart_if_failed(self: &Arc<Self>) -> Option<BoxError> {
        let old_failure = {
            let mut st = self.state.lock().unwrap();
            st.retrieval_failure.take()
        };
        if let Some(failure) = old_failure {
            tracing::debug!(
                "{}: Failure occurred in retrieval. Restarting data requests: {}",
                self.shard_info_id,
                failure
            );
            self.start_subscriptions();
            return Some(failure);
        }
        None
    }

    fn restart_if_request_timer_expired(self: &Arc<Self>, max_time_between_requests_millis: i64) {
        let expired = {
            let st = self.state.lock().unwrap();
            match st.last_request_time {
                Some(t) => {
                    Instant::now().duration_since(t)
                        > Duration::from_millis(max_time_between_requests_millis.max(0) as u64)
                }
                None => false,
            }
        };
        if expired {
            tracing::error!(
                "{}: request dispatched but no response. Cancelling subscription and restarting. \
                 Last successful request details -- {}",
                self.shard_info_id,
                self.records_publisher.last_successful_request_details()
            );
            self.cancel();
            self.start_subscriptions();
        }
    }

    /// Take and clear any dispatch failure. Port of `getAndResetDispatchFailure()`.
    pub fn get_and_reset_dispatch_failure(&self) -> Option<BoxError> {
        self.state.lock().unwrap().dispatch_failure.take()
    }

    /// Last time data arrived. Port of the `lastDataArrival` getter.
    pub fn last_data_arrival(&self) -> Option<Instant> {
        self.state.lock().unwrap().last_data_arrival
    }

    /// The stored retrieval failure (for testing). Port of the `retrievalFailure`
    /// package getter.
    pub fn retrieval_failure_is_set(&self) -> bool {
        self.state.lock().unwrap().retrieval_failure.is_some()
    }

    /// Cancel the current subscription. Port of `cancel()` (Java: `if
    /// (subscription != null) subscription.cancel()`). Signals the live loop,
    /// which calls `Subscription::cancel` on the handle it owns and exits — so
    /// the publisher observes the cancellation before a subsequent
    /// `start_subscriptions` re-subscribes.
    pub fn cancel(&self) {
        let mut st = self.state.lock().unwrap();
        st.running = false;
        if let Some(tx) = st.cancel_tx.take() {
            let _ = tx.send(());
        }
    }

    /// The `onError` equivalent: record a retrieval failure to be picked up by the
    /// next `health_check`, applying the `ReadTimeout` grace-period logic.
    ///
    /// A publisher's error path (wave 8) calls this instead of Java's
    /// `subscriber.onError(t)`. `is_read_timeout` is the port of the Java
    /// `t instanceof RetryableRetrievalException && t.getMessage().contains("ReadTimeout")`
    /// string-match (the retrieval subsystem's typed error can decide it).
    ///
    /// Returns which warning (if any) was logged — the port of Java's
    /// `logOnErrorWarning` / `logOnErrorReadTimeoutWarning` seam. The production
    /// call site discards it; tests assert on the suppression outcome.
    pub fn note_retrieval_failure(
        &self,
        failure: BoxError,
        is_read_timeout: bool,
    ) -> RetrievalWarning {
        let warning = if is_read_timeout {
            let count = self
                .read_timeout_since_last_read
                .fetch_add(1, Ordering::SeqCst)
                + 1;
            if count > self.read_timeouts_to_ignore_before_warning {
                tracing::warn!(
                    "{}: onError() ReadTimeout. Cancelling subscription and marking self as failed.",
                    self.shard_info_id
                );
                RetrievalWarning::ReadTimeout
            } else {
                RetrievalWarning::None
            }
        } else {
            tracing::warn!(
                "{}: onError(). Cancelling subscription and marking self as failed: {}",
                self.shard_info_id,
                failure
            );
            RetrievalWarning::Generic
        };
        let mut st = self.state.lock().unwrap();
        st.retrieval_failure = Some(failure);
        st.running = false;
        warning
    }

    /// Reset the consecutive-ReadTimeout counter on a successful read (Java
    /// `onNext`'s trailing `readTimeoutSinceLastRead = 0`). Extracted so the
    /// delivery loop and the suppression tests share one reset point.
    pub fn reset_read_timeout_counter(&self) {
        self.read_timeout_since_last_read.store(0, Ordering::SeqCst);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::{InitialPositionInStreamExtended, RequestDetails};
    use crate::lifecycle::events::ProcessRecordsInput;
    use crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier;
    use crate::retrieval::kinesis_client_record::KinesisClientRecord;
    use crate::retrieval::kpl::ExtendedSequenceNumber;
    use crate::retrieval::records_publisher::{
        new_subscription, RecordsPublisherSink, RecordsPublisherSubscription,
    };
    use crate::retrieval::{RecordsDeliveryAck, RetrievalError};
    use async_trait::async_trait;
    use std::sync::atomic::AtomicUsize;

    // ---- test doubles ----

    #[derive(Debug)]
    struct TestRecordsRetrieved {
        input: ProcessRecordsInput,
        id: BatchUniqueIdentifier,
    }
    impl RecordsRetrieved for TestRecordsRetrieved {
        fn process_records_input(&self) -> &ProcessRecordsInput {
            &self.input
        }
        fn batch_unique_identifier(&self) -> BatchUniqueIdentifier {
            self.id.clone()
        }
    }

    fn batch(key: &str) -> Arc<dyn RecordsRetrieved> {
        let input = ProcessRecordsInput::builder()
            .records(vec![KinesisClientRecord::builder()
                .partition_key(key.to_string())
                .build()])
            .build();
        Arc::new(TestRecordsRetrieved {
            input,
            id: BatchUniqueIdentifier::new(key, "flow"),
        })
    }

    /// A publisher whose delivery we drive from the test via a shared sink.
    struct TestPublisher {
        sink: Mutex<Option<RecordsPublisherSink>>,
        restarted_from: Mutex<Option<String>>,
        acks: Arc<Mutex<Vec<String>>>,
    }
    impl TestPublisher {
        fn new() -> Self {
            Self {
                sink: Mutex::new(None),
                restarted_from: Mutex::new(None),
                acks: Arc::new(Mutex::new(Vec::new())),
            }
        }
    }
    #[async_trait]
    impl RecordsPublisher for TestPublisher {
        async fn start(
            &self,
            _: ExtendedSequenceNumber,
            _: InitialPositionInStreamExtended,
        ) -> Result<(), crate::exceptions::BoxError> {
            Ok(())
        }
        async fn restart_from(&self, r: Arc<dyn RecordsRetrieved>) {
            *self.restarted_from.lock().unwrap() = Some(
                r.batch_unique_identifier()
                    .record_batch_identifier()
                    .to_string(),
            );
        }
        async fn shutdown(&self) {}
        fn last_successful_request_details(&self) -> RequestDetails {
            RequestDetails::empty()
        }
        async fn notify(&self, ack: Box<dyn RecordsDeliveryAck>) {
            self.acks.lock().unwrap().push(
                ack.batch_unique_identifier()
                    .record_batch_identifier()
                    .to_string(),
            );
        }
        fn subscribe(&self) -> RecordsPublisherSubscription {
            let (sub, sink) = new_subscription();
            *self.sink.lock().unwrap() = Some(sink);
            sub
        }
    }

    struct RecordingHandler {
        count: AtomicUsize,
        keys: Mutex<Vec<String>>,
        cancel_on: Option<usize>,
    }
    impl RecordingHandler {
        fn new(cancel_on: Option<usize>) -> Self {
            Self {
                count: AtomicUsize::new(0),
                keys: Mutex::new(Vec::new()),
                cancel_on,
            }
        }
    }
    impl InputHandler for RecordingHandler {
        fn handle_input(&self, input: ProcessRecordsInput) -> bool {
            let n = self.count.fetch_add(1, Ordering::SeqCst) + 1;
            if let Some(recs) = input.records() {
                if let Some(r) = recs.first() {
                    if let Some(pk) = r.partition_key() {
                        self.keys.lock().unwrap().push(pk.to_string());
                    }
                }
            }
            Some(n) == self.cancel_on
        }
    }

    /// Take the sink the loop stored on `subscribe()`, spawning a small driver
    /// task that answers each `request(n)` by delivering the next queued batch.
    /// This mirrors the retrieval publisher's demand-driven delivery.
    fn drive_sink(mut sink: RecordsPublisherSink, batches: Vec<Arc<dyn RecordsRetrieved>>) {
        use crate::retrieval::records_publisher::DemandSignal;
        tokio::spawn(async move {
            let mut idx = 0usize;
            while let Some(sig) = sink.next_demand().await {
                match sig {
                    DemandSignal::Request(n) => {
                        for _ in 0..n {
                            if idx >= batches.len() {
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
    }

    /// Poll `cond` until it returns true, with a generous wall-clock deadline so
    /// the assertion is robust under CPU contention (a bounded yield-count loop is
    /// not — heavy load can exhaust the count before the async work is scheduled).
    /// Returns whether the condition became true before the deadline.
    async fn wait_for<F: FnMut() -> bool>(mut cond: F) -> bool {
        let deadline = std::time::Instant::now() + Duration::from_secs(20);
        while std::time::Instant::now() < deadline {
            if cond() {
                return true;
            }
            tokio::time::sleep(Duration::from_millis(1)).await;
        }
        cond()
    }

    async fn take_sink(publisher: &Arc<TestPublisher>) -> RecordsPublisherSink {
        loop {
            if let Some(s) = publisher.sink.lock().unwrap().take() {
                return s;
            }
            tokio::task::yield_now().await;
        }
    }

    #[tokio::test]
    async fn dispatches_batches_and_acks() {
        let publisher = Arc::new(TestPublisher::new());
        let handler = Arc::new(RecordingHandler::new(None));
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-001".to_string(),
        ));

        subscriber.start_subscriptions();
        let sink = take_sink(&publisher).await;
        drive_sink(sink, vec![batch("a"), batch("b"), batch("c")]);

        for _ in 0..2000 {
            if handler.count.load(Ordering::SeqCst) >= 3 {
                break;
            }
            tokio::task::yield_now().await;
        }
        assert_eq!(handler.count.load(Ordering::SeqCst), 3);
        assert_eq!(*handler.keys.lock().unwrap(), vec!["a", "b", "c"]);
        assert_eq!(*publisher.acks.lock().unwrap(), vec!["a", "b", "c"]);
    }

    #[tokio::test]
    async fn cancel_stops_loop_on_handler_signal() {
        let publisher = Arc::new(TestPublisher::new());
        // handler cancels after the first batch (like end-of-shard).
        let handler = Arc::new(RecordingHandler::new(Some(1)));
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-001".to_string(),
        ));
        subscriber.start_subscriptions();
        let sink = take_sink(&publisher).await;
        drive_sink(sink, vec![batch("only"), batch("extra")]);
        for _ in 0..2000 {
            if handler.count.load(Ordering::SeqCst) >= 1 {
                break;
            }
            tokio::task::yield_now().await;
        }
        // Only the first batch is dispatched; the loop cancels after it.
        tokio::task::yield_now().await;
        assert_eq!(handler.count.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn note_retrieval_failure_surfaces_in_health_check() {
        let publisher = Arc::new(TestPublisher::new());
        let handler = Arc::new(RecordingHandler::new(None));
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-001".to_string(),
        ));
        subscriber.note_retrieval_failure(
            Box::<dyn std::error::Error + Send + Sync>::from("boom"),
            false,
        );
        assert!(subscriber.retrieval_failure_is_set());
        // health_check returns the failure and restarts (clears it).
        let f = subscriber.health_check(60_000);
        assert!(f.is_some());
        assert_eq!(f.unwrap().to_string(), "boom");
        assert!(!subscriber.retrieval_failure_is_set());
    }

    /// Subscriber↔publisher error-path seam: a publisher that delivers an
    /// `Err(RetrievalError)` through the delivery channel (instead of a batch)
    /// makes the subscriber record a retrieval failure that surfaces via
    /// `health_check` (Java `onError` → restart).
    #[tokio::test]
    async fn publisher_error_delivery_surfaces_as_retrieval_failure() {
        use crate::retrieval::RetrievalError;
        let publisher = Arc::new(TestPublisher::new());
        let handler = Arc::new(RecordingHandler::new(None));
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-err".to_string(),
        ));
        subscriber.start_subscriptions();
        let sink = take_sink(&publisher).await;
        // Deliver a retryable ReadTimeout error rather than a batch.
        tokio::spawn(async move {
            // Wait for the initial demand, then deliver an error.
            let _ = sink
                .deliver_error(RetrievalError::retryable("ReadTimeout on shard"))
                .await;
        });
        // The loop should note the failure and stop; poll until it's set.
        for _ in 0..2000 {
            if subscriber.retrieval_failure_is_set() {
                break;
            }
            tokio::task::yield_now().await;
        }
        assert!(subscriber.retrieval_failure_is_set());
        // No batch was dispatched.
        assert_eq!(handler.count.load(Ordering::SeqCst), 0);
        // health_check surfaces the failure (and restarts, clearing it).
        let f = subscriber.health_check(60_000);
        assert!(f.is_some());
        assert!(f.unwrap().to_string().contains("ReadTimeout"));
    }

    #[tokio::test]
    async fn read_timeout_grace_period() {
        let publisher = Arc::new(TestPublisher::new());
        let handler = Arc::new(RecordingHandler::new(None));
        // ignore 2 read timeouts before warning.
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher,
            8,
            handler,
            2,
            "shard-001".to_string(),
        ));
        for _ in 0..3 {
            subscriber.note_retrieval_failure(
                Box::<dyn std::error::Error + Send + Sync>::from(
                    "RetryableRetrievalException: ReadTimeout",
                ),
                true,
            );
            // clear so we can note again (health_check would restart; here just reset)
            let _ = subscriber.state.lock().unwrap().retrieval_failure.take();
        }
        assert_eq!(
            subscriber
                .read_timeout_since_last_read
                .load(Ordering::SeqCst),
            3
        );
    }

    // ---- A handler that panics on one specific invocation, else records. ----
    // Port of `consumerErrorSkipsEntryTest`'s doAnswer that throws once.
    struct PanicOnceHandler {
        count: AtomicUsize,
        panic_on: usize,
    }
    impl PanicOnceHandler {
        fn new(panic_on: usize) -> Self {
            Self {
                count: AtomicUsize::new(0),
                panic_on,
            }
        }
    }
    impl InputHandler for PanicOnceHandler {
        fn handle_input(&self, _input: ProcessRecordsInput) -> bool {
            let n = self.count.fetch_add(1, Ordering::SeqCst) + 1;
            if n == self.panic_on {
                panic!("ShardConsumerError");
            }
            false
        }
    }

    #[tokio::test]
    async fn consumer_error_skips_entry() {
        // Port of consumerErrorSkipsEntryTest: 20 batches; the handler throws on
        // one of them. The failing batch is captured as a dispatch failure (and
        // then reset to null on a second read), yet all 20 batches are dispatched
        // (skip-and-continue).
        let publisher = Arc::new(TestPublisher::new());
        let handler = Arc::new(PanicOnceHandler::new(10));
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-001".to_string(),
        ));
        subscriber.start_subscriptions();
        let sink = take_sink(&publisher).await;
        let batches: Vec<_> = (0..20).map(|i| batch(&format!("r-{i}"))).collect();
        drive_sink(sink, batches);

        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 20).await);
        assert_eq!(handler.count.load(Ordering::SeqCst), 20);
        // The captured dispatch failure surfaces once, then resets to None.
        let f = subscriber.get_and_reset_dispatch_failure();
        assert!(f.is_some());
        assert!(subscriber.get_and_reset_dispatch_failure().is_none());
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 3)]
    async fn synchronous_blocking_subscriber() {
        // Port of synchronousBlockingSubscriberTest: the subscription is
        // synchronous — the loop requests exactly one batch, and does not request
        // (nor accept) the next until the current dispatch returns. We block inside
        // the handler and assert the driver has delivered exactly one batch, then
        // release it and confirm the second is then delivered.

        // The handler blocks (busy-waits on a released-count) until the test bumps
        // `released`, standing in for Java's synchronous, in-thread onNext.
        struct BlockingHandler {
            count: AtomicUsize,
            released: AtomicUsize,
        }
        impl InputHandler for BlockingHandler {
            fn handle_input(&self, _input: ProcessRecordsInput) -> bool {
                let target = self.released.load(Ordering::SeqCst);
                self.count.fetch_add(1, Ordering::SeqCst);
                while self.released.load(Ordering::SeqCst) == target {
                    std::thread::yield_now();
                }
                false
            }
        }

        // Count how many batches the driver has physically delivered.
        let delivered = Arc::new(AtomicUsize::new(0));
        let publisher = Arc::new(TestPublisher::new());
        let handler = Arc::new(BlockingHandler {
            count: AtomicUsize::new(0),
            released: AtomicUsize::new(0),
        });
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            0, // buffer_size = 0 (synchronous)
            handler.clone(),
            0,
            "shard-001".to_string(),
        ));
        subscriber.start_subscriptions();
        let mut sink = take_sink(&publisher).await;

        // Custom driver that counts deliveries so we can observe backpressure.
        let batches = [batch("first"), batch("second")];
        let delivered2 = delivered.clone();
        tokio::spawn(async move {
            use crate::retrieval::records_publisher::DemandSignal;
            let mut idx = 0usize;
            while let Some(sig) = sink.next_demand().await {
                match sig {
                    DemandSignal::Request(n) => {
                        for _ in 0..n {
                            if idx >= batches.len() {
                                return;
                            }
                            if !sink.deliver(batches[idx].clone()).await {
                                return;
                            }
                            delivered2.fetch_add(1, Ordering::SeqCst);
                            idx += 1;
                        }
                    }
                    DemandSignal::Cancel => return,
                }
            }
        });

        // Wait until the handler is blocking on the first batch.
        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 1).await);
        // Give the driver a chance to (incorrectly) deliver a second batch.
        tokio::time::sleep(Duration::from_millis(20)).await;
        // Synchronous: only one batch has been dispatched and only one delivered —
        // the next is not requested until dispatch returns.
        assert_eq!(handler.count.load(Ordering::SeqCst), 1);
        assert_eq!(delivered.load(Ordering::SeqCst), 1);

        // Release the handler; the loop requests the next and the second is
        // delivered/dispatched.
        handler.released.fetch_add(1, Ordering::SeqCst);
        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 2).await);
        assert_eq!(handler.count.load(Ordering::SeqCst), 2);
        assert_eq!(delivered.load(Ordering::SeqCst), 2);
        // Release the final dispatch so the spawned handler thread can exit.
        handler.released.fetch_add(1, Ordering::SeqCst);
    }

    // ---- Restart-driven publisher for the restart-after-error / -stall tests ----
    //
    // Port of the Java `TestPublisher` (and `RecordPublisherWithInitialFailure...`):
    // a fixed response list (batches, and one optional error), a shared cursor, and
    // `restartFrom` that repositions the cursor to just after the matched batch.
    // Each `subscribe()` spawns a demand-driven driver over the shared cursor. A
    // subscription attempt can be made "silent" (delivers nothing, ignoring demand)
    // to model a stalled/failed initial subscription that `health_check` restarts.

    #[derive(Clone)]
    enum Response {
        Batch(Arc<dyn RecordsRetrieved>),
        /// An error delivered at most `throw_count` times (shared across restarts),
        /// then skipped — mirroring Java's `ResponseItem.throwCount` decrement.
        Error(String, Arc<AtomicUsize>),
    }

    struct RestartablePublisher {
        responses: Vec<Response>,
        cursor: Arc<Mutex<usize>>,
        subscribe_count: Arc<AtomicUsize>,
        /// Which 1-based subscription attempts deliver nothing (ignore demand).
        silent_attempts: Vec<usize>,
        restarted_from: Arc<Mutex<Option<String>>>,
    }
    impl RestartablePublisher {
        fn new(responses: Vec<Response>, silent_attempts: Vec<usize>) -> Self {
            Self {
                responses,
                cursor: Arc::new(Mutex::new(0)),
                subscribe_count: Arc::new(AtomicUsize::new(0)),
                silent_attempts,
                restarted_from: Arc::new(Mutex::new(None)),
            }
        }
    }
    #[async_trait]
    impl RecordsPublisher for RestartablePublisher {
        async fn start(
            &self,
            _: ExtendedSequenceNumber,
            _: InitialPositionInStreamExtended,
        ) -> Result<(), crate::exceptions::BoxError> {
            Ok(())
        }
        async fn restart_from(&self, r: Arc<dyn RecordsRetrieved>) {
            let id = r
                .batch_unique_identifier()
                .record_batch_identifier()
                .to_string();
            *self.restarted_from.lock().unwrap() = Some(id.clone());
            // Reposition the cursor to just after the matched batch (Java currentIndex = i+1).
            let pos = self.responses.iter().position(|resp| {
                matches!(resp, Response::Batch(b)
                    if b.batch_unique_identifier().record_batch_identifier() == id)
            });
            if let Some(p) = pos {
                *self.cursor.lock().unwrap() = p + 1;
            }
        }
        async fn shutdown(&self) {}
        fn last_successful_request_details(&self) -> RequestDetails {
            RequestDetails::empty()
        }
        async fn notify(&self, _ack: Box<dyn RecordsDeliveryAck>) {}
        fn subscribe(&self) -> RecordsPublisherSubscription {
            let attempt = self.subscribe_count.fetch_add(1, Ordering::SeqCst) + 1;
            let (sub, mut sink) = new_subscription();
            let silent = self.silent_attempts.contains(&attempt);
            let cursor = self.cursor.clone();
            let responses = self.responses.clone();
            tokio::spawn(async move {
                use crate::retrieval::records_publisher::DemandSignal;
                while let Some(sig) = sink.next_demand().await {
                    match sig {
                        DemandSignal::Request(n) => {
                            if silent {
                                continue; // failed/stalled subscription: ignore demand.
                            }
                            let mut remaining = n;
                            while remaining > 0 {
                                let idx = { *cursor.lock().unwrap() };
                                if idx >= responses.len() {
                                    return;
                                }
                                *cursor.lock().unwrap() = idx + 1;
                                let ok = match &responses[idx] {
                                    Response::Batch(b) => {
                                        remaining -= 1;
                                        sink.deliver(b.clone()).await
                                    }
                                    Response::Error(msg, throw_count) => {
                                        // Deliver the error only while throws remain
                                        // (Java's throwCount decrement); otherwise skip
                                        // it WITHOUT consuming demand.
                                        if throw_count.load(Ordering::SeqCst) > 0 {
                                            throw_count.fetch_sub(1, Ordering::SeqCst);
                                            remaining -= 1;
                                            sink.deliver_error(RetrievalError::retryable(
                                                msg.clone(),
                                            ))
                                            .await
                                        } else {
                                            continue;
                                        }
                                    }
                                };
                                if !ok {
                                    return;
                                }
                            }
                        }
                        DemandSignal::Cancel => return,
                    }
                }
            });
            sub
        }
    }

    fn count_handler() -> Arc<RecordingHandler> {
        Arc::new(RecordingHandler::new(None))
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn restart_after_error() {
        // Port of restartAfterErrorTest: 9 batches, an "edge" batch, then an error,
        // then 10 more. The subscriber stops on the error (retrieval failure set);
        // health_check surfaces the error and restarts from the edge batch; the
        // publisher resumes after it, so all 20 batches are dispatched.
        let mut responses = Vec::new();
        for i in 0..9 {
            responses.push(Response::Batch(batch(&format!("pre-{i}"))));
        }
        responses.push(Response::Batch(batch("edge")));
        responses.push(Response::Error(
            "whee".to_string(),
            Arc::new(AtomicUsize::new(1)),
        ));
        for i in 0..10 {
            responses.push(Response::Batch(batch(&format!("post-{i}"))));
        }

        let publisher = Arc::new(RestartablePublisher::new(responses, vec![]));
        let handler = count_handler();
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-err".to_string(),
        ));
        subscriber.start_subscriptions();

        // Wait until the error stops the loop (10 dispatched: 9 pre + edge).
        assert!(wait_for(|| subscriber.retrieval_failure_is_set()).await);
        assert_eq!(handler.count.load(Ordering::SeqCst), 10);

        // health_check surfaces the error and restarts from the edge batch.
        let f = subscriber.health_check(100_000);
        assert!(f.is_some());
        assert!(f.unwrap().to_string().contains("whee"));

        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 20).await);
        assert_eq!(handler.count.load(Ordering::SeqCst), 20);
        assert_eq!(
            publisher.restarted_from.lock().unwrap().as_deref(),
            Some("edge")
        );
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn restart_after_request_timer_expires() {
        // Port of restartAfterRequestTimerExpiresTest: the first subscription
        // stalls (delivers nothing); after the request timer expires,
        // health_check cancels and restarts, and the (second) subscription
        // delivers all 100 records.
        let responses: Vec<Response> = (0..100)
            .map(|i| Response::Batch(batch(&format!("Record-{i}"))))
            .collect();
        // First subscription attempt is silent; the restart (attempt 2) delivers.
        let publisher = Arc::new(RestartablePublisher::new(responses, vec![1]));
        let handler = count_handler();
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-stall".to_string(),
        ));
        subscriber.start_subscriptions();

        // Give the (silent) first subscription a chance: no records are dispatched.
        tokio::time::sleep(Duration::from_millis(10)).await;
        assert_eq!(handler.count.load(Ordering::SeqCst), 0);

        // The request timer has expired (last_request_time is in the past). A tiny
        // real delay guarantees a nonzero elapsed against max=0.
        tokio::time::sleep(Duration::from_millis(5)).await;
        // No retrieval failure, so health_check returns None but restarts the stall.
        assert!(subscriber.health_check(0).is_none());

        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 100).await);
        assert_eq!(handler.count.load(Ordering::SeqCst), 100);
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn restart_after_request_timer_expires_when_not_getting_records_after_initialization() {
        // Port of restartAfterRequestTimerExpiresWhenNotGettingRecordsAfter-
        // Initialization: identical restart-after-stall behavior, framed as the
        // initial subscription producing no records. (Same seam as above; kept as a
        // distinct case per the Java suite.)
        let responses: Vec<Response> = (0..100)
            .map(|i| Response::Batch(batch(&format!("Record-{i}"))))
            .collect();
        let publisher = Arc::new(RestartablePublisher::new(responses, vec![1]));
        let handler = count_handler();
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-init-fail".to_string(),
        ));
        subscriber.start_subscriptions();

        tokio::time::sleep(Duration::from_millis(10)).await;
        // No interactions on the initial (failed) subscription.
        assert_eq!(handler.count.load(Ordering::SeqCst), 0);

        tokio::time::sleep(Duration::from_millis(5)).await;
        assert!(subscriber.health_check(0).is_none());

        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 100).await);
        assert_eq!(handler.count.load(Ordering::SeqCst), 100);
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn restart_after_request_timer_expires_when_initial_task_execution_is_rejected() {
        // Port of restartAfterRequestTimerExpiresWhenInitialTaskExecutionIsRejected.
        // Java's distinguishing mechanism (mocking ExecutorService.execute() to
        // throw RejectedExecutionException on the first task) is unportable (no
        // mockable executor in the Rust port). Its OBSERVABLE behavior — the
        // restart-after-stall that recovers all 100 records when the initial
        // subscription produces nothing — is what we assert here.
        let responses: Vec<Response> = (0..100)
            .map(|i| Response::Batch(batch(&format!("Record-{i}"))))
            .collect();
        let publisher = Arc::new(RestartablePublisher::new(responses, vec![1]));
        let handler = count_handler();
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-rejected".to_string(),
        ));
        subscriber.start_subscriptions();

        tokio::time::sleep(Duration::from_millis(10)).await;
        assert_eq!(handler.count.load(Ordering::SeqCst), 0);

        tokio::time::sleep(Duration::from_millis(5)).await;
        assert!(subscriber.health_check(0).is_none());

        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 100).await);
        assert_eq!(handler.count.load(Ordering::SeqCst), 100);
    }

    // ---- Logging-suppression tests (port of the `logging*` methods) ----
    //
    // Java overrides `logOnErrorWarning` / `logOnErrorReadTimeoutWarning` in a
    // subclass to count log emissions across interleaved successes (`onNext`) and
    // failures (`onError`). Here the counting logic lives in
    // `note_retrieval_failure`, which returns the `RetrievalWarning` it emitted;
    // `mimic_success` resets the ReadTimeout counter (Java `onNext`'s reset). We
    // tally generic vs read-timeout warnings exactly as the Java test does.

    /// A tiny driver mirroring the Java `TestShardConsumerSubscriber` counters.
    struct WarningCounts {
        generic: usize,
        read_timeout: usize,
    }
    impl WarningCounts {
        fn new() -> Self {
            Self {
                generic: 0,
                read_timeout: 0,
            }
        }
        fn record(&mut self, w: RetrievalWarning) {
            match w {
                RetrievalWarning::Generic => self.generic += 1,
                RetrievalWarning::ReadTimeout => self.read_timeout += 1,
                RetrievalWarning::None => {}
            }
        }
    }

    fn suppression_subscriber(read_timeouts_to_ignore: i32) -> Arc<ShardConsumerSubscriber> {
        Arc::new(ShardConsumerSubscriber::new(
            Arc::new(TestPublisher::new()),
            8,
            Arc::new(RecordingHandler::new(None)),
            read_timeouts_to_ignore,
            "shard-001".to_string(),
        ))
    }

    fn mimic_success(sub: &Arc<ShardConsumerSubscriber>) {
        // Java: onNext(recordsRetrieved) -> readTimeoutSinceLastRead = 0.
        sub.reset_read_timeout_counter();
    }

    fn mimic_read_timeout(sub: &Arc<ShardConsumerSubscriber>, counts: &mut WarningCounts) {
        let w = sub.note_retrieval_failure(
            Box::<dyn std::error::Error + Send + Sync>::from(
                "RetryableRetrievalException: ReadTimeout",
            ),
            true,
        );
        counts.record(w);
        // clear the stored failure so we can note again (Java restarts subscriptions).
        let _ = sub.state.lock().unwrap().retrieval_failure.take();
    }

    fn mimic_generic(sub: &Arc<ShardConsumerSubscriber>, counts: &mut WarningCounts) {
        let w = sub.note_retrieval_failure(
            Box::<dyn std::error::Error + Send + Sync>::from("Uh oh Not a ReadTimeout"),
            false,
        );
        counts.record(w);
        let _ = sub.state.lock().unwrap().retrieval_failure.take();
    }

    #[test]
    fn no_logging_suppression_needed_on_happy_path() {
        // 5 successes, ignore=0 -> no logs.
        let sub = suppression_subscriber(0);
        let counts = WarningCounts::new();
        for _ in 0..5 {
            mimic_success(&sub);
        }
        assert_eq!(counts.generic, 0);
        assert_eq!(counts.read_timeout, 0);
    }

    #[test]
    fn logging_not_suppressed_after_timeout() {
        // ignore=0: success, success, RT, success, RT -> 2 RT logs.
        let sub = suppression_subscriber(0);
        let mut counts = WarningCounts::new();
        mimic_success(&sub);
        mimic_success(&sub);
        mimic_read_timeout(&sub, &mut counts);
        mimic_success(&sub);
        mimic_read_timeout(&sub, &mut counts);
        assert_eq!(counts.generic, 0);
        assert_eq!(counts.read_timeout, 2);
    }

    #[test]
    fn logging_suppressed_after_intermittent_timeout() {
        // ignore=1: success, success, RT, success, RT -> 0 logs (each RT isolated).
        let sub = suppression_subscriber(1);
        let mut counts = WarningCounts::new();
        mimic_success(&sub);
        mimic_success(&sub);
        mimic_read_timeout(&sub, &mut counts);
        mimic_success(&sub);
        mimic_read_timeout(&sub, &mut counts);
        assert_eq!(counts.generic, 0);
        assert_eq!(counts.read_timeout, 0);
    }

    #[test]
    fn logging_partially_suppressed_after_multiple_timeout() {
        // ignore=1: RT, RT, success, RT, RT -> logs on the 2nd and 5th (2 logs).
        let sub = suppression_subscriber(1);
        let mut counts = WarningCounts::new();
        mimic_read_timeout(&sub, &mut counts);
        mimic_read_timeout(&sub, &mut counts);
        mimic_success(&sub);
        mimic_read_timeout(&sub, &mut counts);
        mimic_read_timeout(&sub, &mut counts);
        assert_eq!(counts.generic, 0);
        assert_eq!(counts.read_timeout, 2);
    }

    #[test]
    fn logging_partially_suppressed_after_consecutive_timeout() {
        // ignore=2: 5 consecutive RTs -> logs on the 3rd, 4th, 5th (3 logs).
        let sub = suppression_subscriber(2);
        let mut counts = WarningCounts::new();
        for _ in 0..5 {
            mimic_read_timeout(&sub, &mut counts);
        }
        assert_eq!(counts.generic, 0);
        assert_eq!(counts.read_timeout, 3);
    }

    #[test]
    fn logging_not_suppressed_on_non_read_timeout_not_ignoring() {
        // ignore=0, generic exception on requests 3 and 5 -> 2 generic logs.
        let sub = suppression_subscriber(0);
        let mut counts = WarningCounts::new();
        mimic_success(&sub);
        mimic_success(&sub);
        mimic_generic(&sub, &mut counts);
        mimic_success(&sub);
        mimic_generic(&sub, &mut counts);
        assert_eq!(counts.generic, 2);
        assert_eq!(counts.read_timeout, 0);
    }

    #[test]
    fn logging_not_suppressed_on_non_read_timeout_ignoring_read_timeouts() {
        // ignore=2 but the exceptions are generic (never suppressed) -> 2 logs.
        let sub = suppression_subscriber(2);
        let mut counts = WarningCounts::new();
        mimic_success(&sub);
        mimic_success(&sub);
        mimic_generic(&sub, &mut counts);
        mimic_success(&sub);
        mimic_generic(&sub, &mut counts);
        assert_eq!(counts.generic, 2);
        assert_eq!(counts.read_timeout, 0);
    }

    // Java cancel(): `if (subscription != null) subscription.cancel()` — the
    // publisher must observe the cancellation, not just a flag flip.
    #[tokio::test]
    async fn cancel_cancels_live_subscription() {
        use crate::retrieval::records_publisher::DemandSignal;
        let publisher = Arc::new(TestPublisher::new());
        let handler = Arc::new(RecordingHandler::new(None));
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler,
            0,
            "shard-001".to_string(),
        ));
        subscriber.start_subscriptions();
        let mut sink = take_sink(&publisher).await;
        // The loop's onSubscribe request.
        assert_eq!(sink.next_demand().await, Some(DemandSignal::Request(1)));
        subscriber.cancel();
        // The cancel reaches the publisher, then the loop exits (handle drop).
        assert_eq!(sink.next_demand().await, Some(DemandSignal::Cancel));
        assert!(sink.next_demand().await.is_none());
    }

    // ---- Restart-after-stall against the REAL FanOutRecordsPublisher ----
    //
    // Regression for the restart path: health_check on a stalled subscription
    // cancels it and re-subscribes. Before the fix, cancel() did not cancel the
    // underlying subscription, so the fresh subscribe tripped the publisher's
    // single-subscriber enforcement (both sinks silently dropped, no new flow,
    // no recorded failure) and the shard stayed dead until the NEXT full
    // request-timeout cycle. Now the re-subscribe is granted a new flow — either
    // immediately, or (if the Subscribe command races the in-flight cancel) via
    // a MultipleSubscriberException retrieval failure that the next health-check
    // tick restarts from, matching Java.

    struct FakeShardSubscriber {
        inner: Mutex<FakeShardSubscriberInner>,
    }
    #[derive(Default)]
    struct FakeShardSubscriberInner {
        events: Option<tokio::sync::mpsc::UnboundedSender<crate::retrieval::fanout::FlowEvent>>,
        flows: Vec<u64>,
    }
    impl FakeShardSubscriber {
        fn new() -> Arc<Self> {
            Arc::new(Self {
                inner: Mutex::new(FakeShardSubscriberInner::default()),
            })
        }
        fn send(&self, ev: crate::retrieval::fanout::FlowEvent) {
            let tx = self
                .inner
                .lock()
                .unwrap()
                .events
                .clone()
                .expect("subscribed");
            let _ = tx.send(ev);
        }
        fn flow_count(&self) -> usize {
            self.inner.lock().unwrap().flows.len()
        }
        fn last_flow(&self) -> u64 {
            *self.inner.lock().unwrap().flows.last().expect("subscribed")
        }
    }
    #[async_trait]
    impl crate::retrieval::fanout::ShardSubscriber for FakeShardSubscriber {
        async fn subscribe(
            &self,
            flow_id: u64,
            _sequence_number: crate::retrieval::kpl::ExtendedSequenceNumber,
            _is_first_connection: bool,
            _initial_position: InitialPositionInStreamExtended,
            events: tokio::sync::mpsc::UnboundedSender<crate::retrieval::fanout::FlowEvent>,
        ) {
            let mut inner = self.inner.lock().unwrap();
            inner.events = Some(events);
            inner.flows.push(flow_id);
        }
        fn request_next(&self, _flow_id: u64) {}
        fn cancel(&self, _flow_id: u64) {}
    }

    fn fan_event(seq: &str, continuation: &str) -> aws_sdk_kinesis::types::SubscribeToShardEvent {
        aws_sdk_kinesis::types::SubscribeToShardEvent::builder()
            .millis_behind_latest(0)
            .continuation_sequence_number(continuation)
            .records(
                aws_sdk_kinesis::types::Record::builder()
                    .sequence_number(seq)
                    .partition_key("A")
                    .data(aws_smithy_types::Blob::new(b"d".to_vec()))
                    .build()
                    .unwrap(),
            )
            .build()
            .unwrap()
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn stall_restart_resubscribes_fanout_publisher() {
        use crate::retrieval::fanout::{FanOutRecordsPublisher, FlowEvent};

        let fake = FakeShardSubscriber::new();
        let publisher = Arc::new(FanOutRecordsPublisher::with_subscriber(
            fake.clone(),
            "shardId-000".to_string(),
        ));
        publisher
            .start(
                ExtendedSequenceNumber::latest(),
                InitialPositionInStreamExtended::new_initial_position(
                    crate::common::InitialPositionInStream::Latest,
                ),
            )
            .await
            .unwrap();

        let handler = Arc::new(RecordingHandler::new(None));
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            publisher.clone(),
            8,
            handler.clone(),
            0,
            "shard-stall".to_string(),
        ));
        subscriber.start_subscriptions();

        // Flow 1 comes up and delivers one batch.
        assert!(wait_for(|| fake.flow_count() >= 1).await);
        let flow1 = fake.last_flow();
        fake.send(FlowEvent::Started { flow_id: flow1 });
        fake.send(FlowEvent::Records {
            flow_id: flow1,
            event: Box::new(fan_event("seq-1", "cont-1")),
        });
        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 1).await);

        // The publisher stalls (no more events). One expired-timer health check
        // restarts; subsequent non-expiring ticks only pick up a recorded
        // failure (the race case). Recovery must NOT need another timer expiry.
        tokio::time::sleep(Duration::from_millis(5)).await;
        assert!(subscriber.health_check(0).is_none());
        let deadline = std::time::Instant::now() + Duration::from_secs(20);
        while fake.flow_count() < 2 && std::time::Instant::now() < deadline {
            tokio::time::sleep(Duration::from_millis(10)).await;
            let _ = subscriber.health_check(100_000);
        }
        assert!(
            fake.flow_count() >= 2,
            "restart did not obtain a new subscription"
        );
        let flow2 = fake.last_flow();
        assert_ne!(flow2, flow1);

        // The new flow is live end-to-end.
        fake.send(FlowEvent::Started { flow_id: flow2 });
        fake.send(FlowEvent::Records {
            flow_id: flow2,
            event: Box::new(fan_event("seq-2", "cont-2")),
        });
        assert!(wait_for(|| handler.count.load(Ordering::SeqCst) >= 2).await);
    }
}
