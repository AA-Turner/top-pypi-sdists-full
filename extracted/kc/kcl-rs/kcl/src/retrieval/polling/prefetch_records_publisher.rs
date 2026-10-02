//! Port of `software.amazon.kinesis.retrieval.polling.PrefetchRecordsPublisher`.
//!
//! The core polling [`RecordsPublisher`]: a background prefetch loop repeatedly
//! calls the [`GetRecordsRetrievalStrategy`], buffers results in a bounded queue,
//! and drains them to a single downstream subscriber driven by demand
//! (`request(n)`) and delivery acks (`notify`).
//!
//! # Actor-model translation (Java → Rust)
//!
//! Java runs a per-shard daemon thread + a `ReentrantReadWriteLock` reset
//! protocol + intrinsic-monitor producer/consumer counters. This port collapses
//! all of that into a **single spawned tokio task** ([`run_task`]) that owns all
//! mutable state ([`PublisherState`]). The three Java call-paths (daemon,
//! demand-notifier, ack-notifier) become messages on one
//! [`Command`] channel, so no shared locking is needed:
//!
//! * The prefetch loop fetches (`get_records_adapter`) and offers into a bounded
//!   in-task [`std::collections::VecDeque`] buffer (Java's `LinkedBlockingQueue`,
//!   capacity `max(max_pending_process_records_input, 1)`).
//! * `request(n)` / `cancel` arrive as [`Command::Demand`]; `notify(ack)` as
//!   [`Command::Ack`]; `restart_from` as [`Command::RestartFrom`]; `shutdown` as
//!   [`Command::Shutdown`].
//! * Delivery goes over the retrieval-core
//!   [`RecordsPublisherSink`]; the consumer's `request(1)`/`recv()`/`notify(ack)`
//!   drive the cycle exactly as the trait contract describes.
//!
//! The reset-while-enqueuing race (Java's read/write-lock dance + `PositionResetException`)
//! is trivially correct here: because a single task processes commands and the
//! fetch step serially, a `RestartFrom` command is handled between fetch steps
//! and discards the in-flight/queued records before the next fetch — there is no
//! concurrent enqueue to abort.
//!
//! Preserved behaviors: max-pending buffer sizing (min 1), the three-way
//! byte/record/pending backpressure gate, idle-time/reduced-TPS sleep pacing (via
//! [`SleepTimeController`]) with the skip-first-call quirk, reset semantics,
//! `millisBehindLatest` propagation, `ExpiredIterator`/`InvalidArgument` iterator
//! restart, throttling reporting, and stale-ack tolerance.

use std::collections::VecDeque;
use std::sync::{Arc, Mutex};
use std::time::Instant;

use async_trait::async_trait;
use tokio::sync::mpsc;

use crate::common::request_details::RequestDetails;
use crate::common::InitialPositionInStreamExtended;
use crate::exceptions::BoxError;
use crate::metrics::MetricsFactory;
use crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier;
use crate::retrieval::get_records_retrieval_strategy::GetRecordsRetrievalStrategy;
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::polling::data_fetcher::FetchError;
use crate::retrieval::polling::prefetch_records_retrieved::PrefetchRecordsRetrieved;
use crate::retrieval::polling::sleep_time_controller::{
    SleepTimeController, SleepTimeControllerConfig,
};
use crate::retrieval::records_delivery_ack::RecordsDeliveryAck;
use crate::retrieval::records_publisher::{
    new_subscription, DemandSignal, RecordsPublisher, RecordsPublisherSink,
    RecordsPublisherSubscription,
};
use crate::retrieval::records_retrieved::RecordsRetrieved;
use crate::retrieval::throttling_reporter::ThrottlingReporter;

/// Default graceful-shutdown await timeout (Java
/// `DEFAULT_AWAIT_TERMINATION_TIMEOUT_MILLIS`).
pub const DEFAULT_AWAIT_TERMINATION_TIMEOUT_MILLIS: u64 = 60_000;

/// Commands sent to the single publisher task.
enum Command {
    /// Additive demand or cancel (Java `Subscription.request(n)` / `cancel()`).
    Demand(DemandSignal),
    /// A delivery ack (Java `notify(RecordsDeliveryAck)`).
    Ack(BatchUniqueIdentifier),
    /// Attach/replace the downstream subscriber on the running task (Java
    /// `subscribe(Subscriber)`, which overwrites the `subscriber` field of the
    /// live publisher — the consumer re-subscribes after a health-check restart).
    Subscribe(RecordsPublisherSink),
    /// Reset + restart from the given batch (Java `restartFrom`).
    RestartFrom(PrefetchRecordsRetrieved),
    /// Shut the publisher down (Java `shutdown`).
    Shutdown(tokio::sync::oneshot::Sender<()>),
}

/// Configuration snapshot shared with the task.
struct PublisherConfig {
    max_pending_process_records_input: usize,
    max_byte_size: i64,
    max_records_count: i64,
    max_records_per_call: i32,
    idle_millis_between_calls: i64,
    millis_behind_latest_threshold_for_reduced_tps: i64,
    stream_and_shard_id: String,
}

/// All mutable state owned by the single publisher task.
struct PublisherState {
    config: PublisherConfig,
    strategy: Arc<dyn GetRecordsRetrievalStrategy>,
    sleep_time_controller: Arc<dyn SleepTimeController>,
    throttling_reporter: ThrottlingReporter,
    #[allow(dead_code)]
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,

    // Session state (Java PublisherSession).
    queue: VecDeque<PrefetchRecordsRetrieved>,
    requested_responses: u64,
    // Three-way backpressure counters (Java PrefetchCounters).
    counter_size: i64,
    counter_byte_size: i64,
    counter_pending: i64,
    highest_sequence_number: String,
    initial_position: InitialPositionInStreamExtended,

    // Pacing state (Java sleepBeforeNextCall bookkeeping).
    last_successful_call: Option<Instant>,
    last_get_records_returned_records_count: Option<i32>,
    last_millis_behind_latest: Option<i64>,
    is_first_get_call_try: bool,

    // Delivery + diagnostics. `None` until a subscriber attaches (Java's
    // `subscriber` field is null until `subscribe`; the daemon prefetches and
    // buffers regardless) and after the subscription is dropped.
    sink: Option<RecordsPublisherSink>,
    last_successful_request_details: Arc<Mutex<RequestDetails>>,
    cancelled: bool,
    // Scratch queue for commands drained in a batch each loop iteration.
    pending_commands: VecDeque<Command>,
}

impl PublisherState {
    /// Java `PrefetchCounters.shouldGetNewRecords`.
    fn should_get_new_records(&self) -> bool {
        if self.config.max_pending_process_records_input == 0 && self.requested_responses == 0 {
            return false;
        }
        if self.counter_pending == 0 {
            return true;
        }
        self.counter_size < self.config.max_records_count
            && self.counter_byte_size < self.config.max_byte_size
            && self.counter_pending < self.config.max_pending_process_records_input as i64
    }

    fn record_size(
        input: &crate::lifecycle::events::process_records_input::ProcessRecordsInput,
    ) -> i64 {
        input.records().map(|r| r.len()).unwrap_or(0) as i64
    }

    fn byte_size(
        input: &crate::lifecycle::events::process_records_input::ProcessRecordsInput,
    ) -> i64 {
        input
            .records()
            .map(|records| {
                records
                    .iter()
                    .map(|r| r.data().map(|d| d.len()).unwrap_or(0) as i64)
                    .sum()
            })
            .unwrap_or(0)
    }

    /// Java `PrefetchCounters.added`.
    fn counters_added(&mut self, batch: &PrefetchRecordsRetrieved) {
        let input = batch.process_records_input();
        self.counter_size += Self::record_size(input);
        self.counter_byte_size += Self::byte_size(input);
        self.counter_pending += 1;
    }

    /// Java `PrefetchCounters.removed`.
    fn counters_removed(&mut self, batch: &PrefetchRecordsRetrieved) {
        let input = batch.process_records_input();
        self.counter_size -= Self::record_size(input);
        self.counter_byte_size -= Self::byte_size(input);
        self.counter_pending -= 1;
    }

    /// Java `PublisherSession.reset` — discard queued/in-flight records and
    /// restart the iterator from the acked batch.
    fn reset(&mut self, batch: &PrefetchRecordsRetrieved) {
        self.requested_responses = 0;
        self.queue.clear();
        self.counter_size = 0;
        self.counter_byte_size = 0;
        self.counter_pending = 0;
        self.highest_sequence_number = batch.last_batch_sequence_number().to_string();
        self.strategy.get_data_fetcher().reset_iterator(
            batch.shard_iterator().map(str::to_string),
            &self.highest_sequence_number,
            &self.initial_position,
        );
    }

    fn has_demand_to_publish(&self) -> bool {
        self.requested_responses > 0
    }

    /// Java `calculateHighestSequenceNumber`.
    fn calculate_highest_sequence_number(
        &self,
        input: &crate::lifecycle::events::process_records_input::ProcessRecordsInput,
    ) -> String {
        if let Some(records) = input.records() {
            if let Some(last) = records.last() {
                if let Some(seq) = last.sequence_number() {
                    return seq.to_string();
                }
            }
        }
        self.highest_sequence_number.clone()
    }

    /// Java `drainQueueForRequests` — deliver the head batch if there is demand
    /// and it hasn't been dispatched. Returns the batch to deliver (so the async
    /// send happens outside the borrow).
    fn take_deliverable(&mut self) -> Option<PrefetchRecordsRetrieved> {
        if self.cancelled {
            return None;
        }
        if !self.has_demand_to_publish() {
            return None;
        }
        let head = self.queue.front_mut()?;
        if head.is_dispatched() {
            return None;
        }
        head.mark_dispatched();
        Some(head.prepare_for_publish())
    }

    /// Java `PublisherSession.handleRecordsDeliveryAck` — evict the head batch iff
    /// its id matches the ack; otherwise ignore (stale ack).
    fn handle_ack(&mut self, ack_id: &BatchUniqueIdentifier) {
        match self.queue.front() {
            Some(head) if head.batch_id() == ack_id => {
                if let Some(evicted) = self.queue.pop_front() {
                    self.counters_removed(&evicted);
                    self.requested_responses = self.requested_responses.saturating_sub(1);
                }
            }
            _ => {
                tracing::info!(
                    "{}: Received a stale notification with id {:?}. Will ignore.",
                    self.config.stream_and_shard_id,
                    ack_id
                );
            }
        }
    }

    /// Java `sleepBeforeNextCall`: skip the very first call, else compute + sleep,
    /// then null out the pacing bookkeeping.
    async fn sleep_before_next_call(&mut self) {
        if self.last_successful_call.is_none() && self.is_first_get_call_try {
            self.is_first_get_call_try = false;
            return;
        }
        let cfg = SleepTimeControllerConfig::builder()
            .maybe_last_successful_call(self.last_successful_call)
            .idle_millis_between_calls(self.config.idle_millis_between_calls)
            .maybe_last_records_count(self.last_get_records_returned_records_count)
            .maybe_last_millis_behind_latest(self.last_millis_behind_latest)
            .millis_behind_latest_threshold_for_reduced_tps(
                self.config.millis_behind_latest_threshold_for_reduced_tps,
            )
            .build();
        let sleep_ms = self
            .sleep_time_controller
            .get_sleep_time_millis(&cfg, Instant::now());
        if sleep_ms > 0 {
            tokio::time::sleep(std::time::Duration::from_millis(sleep_ms as u64)).await;
        }
        // Avoid immediate-retry storms.
        self.last_successful_call = None;
        self.last_get_records_returned_records_count = None;
        self.last_millis_behind_latest = None;
    }
}

/// The publisher handle (Java `PrefetchRecordsPublisher`).
///
/// Holds only a command sender to the single owning task plus the shared
/// `last_successful_request_details`. `subscribe` mints a subscription/sink
/// pair and hands the sink to the task: directly (as a [`Command::Subscribe`])
/// when the task is already running — the production order, since the lifecycle
/// calls `start` from `InitializeTask` before the `ShardConsumerSubscriber`
/// subscribes, and re-subscribes on health-check restarts — or stashed in
/// `pending_sink` for `start` to pick up when subscribing first.
pub struct PrefetchRecordsPublisher {
    inner: Mutex<PublisherHandleState>,
    last_successful_request_details: Arc<Mutex<RequestDetails>>,
    // Fields needed to construct the task's state at `start`.
    build: Mutex<Option<TaskBuildParams>>,
}

struct PublisherHandleState {
    command_tx: Option<mpsc::UnboundedSender<Command>>,
    started: bool,
    shutdown: bool,
    // Sink stored by a `subscribe` that happens before `start`.
    pending_sink: Option<RecordsPublisherSink>,
}

/// Parameters captured at construction, consumed once at `start` to build the task.
struct TaskBuildParams {
    config: PublisherConfig,
    strategy: Arc<dyn GetRecordsRetrievalStrategy>,
    sleep_time_controller: Arc<dyn SleepTimeController>,
    throttling_reporter: ThrottlingReporter,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
}

impl PrefetchRecordsPublisher {
    /// Construct a publisher.
    ///
    /// Port of the primary Java constructor. `operation` must be non-empty (Java
    /// `Validate.notEmpty`).
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        max_pending_process_records_input: usize,
        max_byte_size: i64,
        max_records_count: i64,
        max_records_per_call: i32,
        strategy: Arc<dyn GetRecordsRetrievalStrategy>,
        idle_millis_between_calls: i64,
        millis_behind_latest_threshold_for_reduced_tps: i64,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        operation: &str,
        shard_id: &str,
        throttling_reporter: ThrottlingReporter,
        sleep_time_controller: Arc<dyn SleepTimeController>,
    ) -> Self {
        if operation.is_empty() {
            panic!("Operation cannot be empty");
        }
        let stream_id = strategy.get_data_fetcher().stream_identifier();
        let stream_and_shard_id = format!("{}:{}", stream_id.serialize(), shard_id);
        let config = PublisherConfig {
            max_pending_process_records_input,
            max_byte_size,
            max_records_count,
            max_records_per_call,
            idle_millis_between_calls,
            millis_behind_latest_threshold_for_reduced_tps,
            stream_and_shard_id,
        };
        Self {
            inner: Mutex::new(PublisherHandleState {
                command_tx: None,
                started: false,
                shutdown: false,
                pending_sink: None,
            }),
            last_successful_request_details: Arc::new(Mutex::new(RequestDetails::empty())),
            build: Mutex::new(Some(TaskBuildParams {
                config,
                strategy,
                sleep_time_controller,
                throttling_reporter,
                metrics_factory,
            })),
        }
    }
}

#[async_trait]
impl RecordsPublisher for PrefetchRecordsPublisher {
    async fn start(
        &self,
        extended_sequence_number: ExtendedSequenceNumber,
        initial_position_in_stream_extended: InitialPositionInStreamExtended,
    ) -> Result<(), BoxError> {
        // Take the params + sink under the lock, then release it before the async
        // fetcher init (the MutexGuard is not Send and must not be held across an
        // await).
        let (params, sink) = {
            let mut inner = self.inner.lock().unwrap();
            if inner.shutdown {
                panic!("ExecutorService has been shutdown.");
            }
            if inner.started {
                // Idempotent (Java logs "Skipping publisher start").
                return Ok(());
            }
            let params = self
                .build
                .lock()
                .unwrap()
                .take()
                .expect("start called twice or after shutdown");
            // A subscriber may or may not exist yet: the production lifecycle
            // starts the publisher from `InitializeTask` and only subscribes once
            // initialization completes, so the task must run without a sink and
            // accept one later (Java: the daemon prefetches; `subscriber` is
            // attached whenever `subscribe` is called).
            let sink = inner.pending_sink.take();
            (params, sink)
        };

        // Initialize the data fetcher's iterator (Java PublisherSession.init).
        // 2026-07-14 fix: this can fail (GetShardIterator timeout / non-
        // ResourceNotFound SDK error) — Java's exception propagates out of
        // `init` -> `start` -> `InitializeTask`, which retries the whole task
        // (including this `start` call) after a backoff. On failure we must
        // NOT spawn the task or flip `started`, and we must put the params/sink
        // back so a subsequent `start()` retry works exactly like the first
        // attempt (no double-take panic, no orphaned pending subscribe).
        let data_fetcher = params.strategy.get_data_fetcher();
        if let Err(fetch_err) = data_fetcher
            .initialize_from_extended(
                &extended_sequence_number,
                &initial_position_in_stream_extended,
            )
            .await
        {
            let mut inner = self.inner.lock().unwrap();
            if let Some(sink) = sink {
                inner.pending_sink = Some(sink);
            }
            *self.build.lock().unwrap() = Some(params);
            return Err(Box::new(fetch_err));
        }

        let (command_tx, command_rx) = mpsc::unbounded_channel();

        let state = PublisherState {
            counter_size: 0,
            counter_byte_size: 0,
            counter_pending: 0,
            queue: VecDeque::new(),
            requested_responses: 0,
            highest_sequence_number: extended_sequence_number.sequence_number().to_string(),
            initial_position: initial_position_in_stream_extended,
            last_successful_call: None,
            last_get_records_returned_records_count: None,
            last_millis_behind_latest: Some(i64::MAX),
            is_first_get_call_try: true,
            strategy: params.strategy,
            sleep_time_controller: params.sleep_time_controller,
            throttling_reporter: params.throttling_reporter,
            metrics_factory: params.metrics_factory,
            config: params.config,
            sink,
            last_successful_request_details: Arc::clone(&self.last_successful_request_details),
            cancelled: false,
            pending_commands: VecDeque::new(),
        };

        tokio::spawn(run_task(state, command_rx));

        let mut inner = self.inner.lock().unwrap();
        inner.command_tx = Some(command_tx.clone());
        inner.started = true;
        // Close the command_tx==None window minimally (item 6, defensive parity
        // with fan-out's ensure-task-started guarantee): a `subscribe()` that
        // landed while we were awaiting `initialize_from_extended` above (i.e.
        // after our earlier `pending_sink.take()`, while `command_tx` was still
        // `None`) would have stashed its sink back into `pending_sink` instead
        // of sending it to the (not-yet-installed) command channel. Forward it
        // now so it isn't orphaned. Not reachable from the current production
        // lifecycle ordering (subscribe always happens after `start` completes),
        // but cheap to close.
        if let Some(orphaned_sink) = inner.pending_sink.take() {
            let _ = command_tx.send(Command::Subscribe(orphaned_sink));
        }
        Ok(())
    }

    async fn restart_from(&self, records_retrieved: Arc<dyn RecordsRetrieved>) {
        // Downcast to PrefetchRecordsRetrieved (Java instanceof check).
        let batch = downcast_prefetch(&records_retrieved).unwrap_or_else(|| {
            panic!("Provided RecordsRetrieved was not produced by the PrefetchRecordsPublisher")
        });
        let inner = self.inner.lock().unwrap();
        if let Some(tx) = &inner.command_tx {
            let _ = tx.send(Command::RestartFrom(batch));
        }
    }

    async fn shutdown(&self) {
        let rx = {
            let mut inner = self.inner.lock().unwrap();
            inner.shutdown = true;
            inner.started = false;
            match inner.command_tx.take() {
                Some(tx) => {
                    let (done_tx, done_rx) = tokio::sync::oneshot::channel();
                    if tx.send(Command::Shutdown(done_tx)).is_ok() {
                        Some(done_rx)
                    } else {
                        None
                    }
                }
                None => None,
            }
        };
        if let Some(rx) = rx {
            let _ = rx.await;
        }
    }

    fn last_successful_request_details(&self) -> RequestDetails {
        self.last_successful_request_details.lock().unwrap().clone()
    }

    async fn notify(&self, ack: Box<dyn RecordsDeliveryAck>) {
        let inner = self.inner.lock().unwrap();
        if let Some(tx) = &inner.command_tx {
            let _ = tx.send(Command::Ack(ack.batch_unique_identifier().clone()));
        }
    }

    fn subscribe(&self) -> RecordsPublisherSubscription {
        // The retrieval-core `new_subscription` returns a matched pair: the
        // subscription (returned to the consumer) carries the demand sender + the
        // delivery receiver; the sink carries the demand receiver + the delivery
        // sender. If the task is already running (the production order — start
        // from `InitializeTask`, subscribe afterwards, and again on every
        // health-check restart), hand it the sink directly so it replaces any
        // previous subscriber (Java `subscribe` overwrites the `subscriber`
        // field of the live publisher). Otherwise stash it for `start`.
        let (subscription, sink) = new_subscription();
        let mut inner = self.inner.lock().unwrap();
        if let Some(tx) = &inner.command_tx {
            if let Err(unsent) = tx.send(Command::Subscribe(sink)) {
                // Task already gone (shutdown); dropping the sink closes the
                // subscription's channels.
                drop(unsent);
            }
        } else {
            inner.pending_sink = Some(sink);
        }
        subscription
    }
}

/// Recover a [`PrefetchRecordsRetrieved`] from a `dyn RecordsRetrieved` via the
/// `as_any` downcast hook (Java `instanceof PrefetchRecordsRetrieved`).
fn downcast_prefetch(r: &Arc<dyn RecordsRetrieved>) -> Option<PrefetchRecordsRetrieved> {
    r.as_any()
        .and_then(|any| any.downcast_ref::<PrefetchRecordsRetrieved>())
        .cloned()
}

/// The single owning task (Java `DefaultGetRecordsCacheDaemon.run` + the
/// demand/ack call-paths, unified). Reads demand from the sink (the consumer's
/// `request(n)`/`cancel()`) and other commands (ack/restart/shutdown) from the
/// command channel.
async fn run_task(mut state: PublisherState, mut command_rx: mpsc::UnboundedReceiver<Command>) {
    loop {
        // 1) Drain any pending demand + commands without blocking.
        drain_pending(&mut state, &mut command_rx);
        // Handle drained commands (which may include Shutdown).
        while let Some(cmd) = state.pending_commands.pop_front() {
            if handle_command_guarded(&mut state, cmd).await {
                return;
            }
        }

        // 2) Fetch step if the backpressure gate allows.
        if state.should_get_new_records() {
            // Ports the catch (Throwable e) in Java
            // DefaultGetRecordsCacheDaemon.run around makeRetrievalAttempt: a
            // panicking attempt is logged and the daemon keeps looping.
            let attempt = crate::utils::panic_util::catch_tick(async {
                state.sleep_before_next_call().await;
                let fetch = state
                    .strategy
                    .get_records_adapter(state.config.max_records_per_call)
                    .await;
                handle_fetch_result(&mut state, fetch).await;
                deliver_if_possible(&mut state).await;
            })
            .await;
            if let Err(panic) = attempt {
                tracing::error!(
                    "{}: Unexpected exception was thrown. This could probably be an issue or a \
                     bug. Please search for the exception/error online to check what is going \
                     on. If the issue persists or is a recurring problem, feel free to open an \
                     issue on, https://github.com/awslabs/amazon-kinesis-client. {}",
                    state.config.stream_and_shard_id,
                    panic
                );
            }
        } else {
            // 3) Not ready to fetch: wait for demand or a command (or a short idle
            // timeout re-evaluating the gate, matching Java's bounded
            // `waitForConsumer(idleMillisBetweenCalls)`).
            let idle = std::time::Duration::from_millis(
                state.config.idle_millis_between_calls.max(1) as u64,
            );
            tokio::select! {
                // With no live subscriber this arm must park (not poll a closed
                // channel, which resolves instantly and busy-spins the select) —
                // same guard as the fan-out task.
                demand = async {
                    match state.sink.as_mut() {
                        Some(sink) => sink.next_demand().await,
                        None => std::future::pending().await,
                    }
                } => {
                    match demand {
                        Some(signal) => {
                            if handle_command_guarded(&mut state, Command::Demand(signal)).await {
                                return;
                            }
                        }
                        None => {
                            // Subscription dropped; detach the sink (a later
                            // `subscribe` installs a fresh one) and keep serving
                            // commands.
                            state.sink = None;
                        }
                    }
                }
                maybe_cmd = command_rx.recv() => {
                    match maybe_cmd {
                        Some(cmd) => {
                            if handle_command_guarded(&mut state, cmd).await {
                                return;
                            }
                        }
                        None => return,
                    }
                }
                _ = tokio::time::sleep(idle) => {}
            }
        }
    }
}

/// Non-blocking drain of pending demand + commands into `state.pending_commands`.
fn drain_pending(state: &mut PublisherState, command_rx: &mut mpsc::UnboundedReceiver<Command>) {
    // Demand first (mirrors the request()/notify() interleaving).
    if let Some(sink) = state.sink.as_mut() {
        loop {
            match sink.try_next_demand() {
                Ok(signal) => state.pending_commands.push_back(Command::Demand(signal)),
                Err(mpsc::error::TryRecvError::Empty) => break,
                Err(mpsc::error::TryRecvError::Disconnected) => {
                    // Subscription dropped; detach so the select arm parks.
                    state.sink = None;
                    break;
                }
            }
        }
    }
    while let Ok(cmd) = command_rx.try_recv() {
        state.pending_commands.push_back(cmd);
    }
}

/// Guard [`handle_command`] with the same per-tick `catch (Throwable)`
/// containment the fetch step already gets (Java wraps the *whole* daemon-loop
/// body, not just `makeRetrievalAttempt` — see
/// `DefaultGetRecordsCacheDaemon.run`). Without this a panic while handling a
/// command (drained in a batch, or from a select arm) would unwind out of
/// `run_task` and silently kill the publisher's owning task: every later
/// `subscribe()`/`notify()`/demand send would hit a dead channel, permanently
/// wedging the consumer (health checks would keep re-subscribing into a
/// channel nothing is listening on). A caught panic is logged and never
/// treated as a shutdown request.
async fn handle_command_guarded(state: &mut PublisherState, cmd: Command) -> bool {
    match crate::utils::panic_util::catch_tick(handle_command(state, cmd)).await {
        Ok(shutdown) => shutdown,
        Err(panic) => {
            tracing::error!(
                "{}: Unexpected exception was thrown while handling a command. This could probably be an issue or a bug. Please search for the exception/error online to check what is going on. If the issue persists or is a recurring problem, feel free to open an issue on, https://github.com/awslabs/amazon-kinesis-client. {}",
                state.config.stream_and_shard_id,
                panic
            );
            false
        }
    }
}

/// Handle one command. Returns `true` on shutdown.
async fn handle_command(state: &mut PublisherState, cmd: Command) -> bool {
    match cmd {
        Command::Demand(DemandSignal::Request(n)) => {
            state.requested_responses += n;
            if state.config.max_pending_process_records_input != 0 {
                deliver_if_possible(state).await;
            }
        }
        Command::Demand(DemandSignal::Cancel) => {
            // Java `Subscription.cancel()`: zero the demand so nothing further is
            // dispatched; the session state is reset when the consumer calls
            // `restartFrom` and re-subscribes.
            state.requested_responses = 0;
            state.cancelled = true;
        }
        Command::Subscribe(sink) => {
            // Java `subscribe(Subscriber)` on the live publisher: replace the
            // subscriber and accept demand from the new subscription (the old
            // sink, if any, is dropped here → its delivery channel closes).
            state.sink = Some(sink);
            state.cancelled = false;
        }
        Command::Ack(id) => {
            state.handle_ack(&id);
            if state.config.max_pending_process_records_input != 0 {
                deliver_if_possible(state).await;
            }
        }
        Command::RestartFrom(batch) => {
            state.reset(&batch);
        }
        Command::Shutdown(done) => {
            if !state.strategy.is_shutdown() {
                state.strategy.shutdown();
            }
            let _ = done.send(());
            return true;
        }
    }
    false
}

/// Deliver the head batch to the subscriber if there is demand (Java
/// `drainQueueForRequests`).
async fn deliver_if_possible(state: &mut PublisherState) {
    // No subscriber attached: don't take (and mark dispatched) a batch that
    // could not be delivered.
    if state.sink.is_none() {
        return;
    }
    if let Some(batch) = state.take_deliverable() {
        let arc: Arc<dyn RecordsRetrieved> = Arc::new(batch);
        // Best-effort: if the consumer is gone the send fails; detach the sink
        // (the select arm then parks) and the task continues.
        let delivered = match state.sink.as_ref() {
            Some(sink) => sink.deliver(arc).await,
            None => false,
        };
        if !delivered {
            state.sink = None;
        }
    }
}

/// Process the outcome of a `get_records_adapter` call (Java
/// `makeRetrievalAttempt` body).
async fn handle_fetch_result(
    state: &mut PublisherState,
    fetch: Result<Box<dyn crate::retrieval::GetRecordsResponseAdapter>, FetchError>,
) {
    match fetch {
        Ok(adapter) => {
            state.last_successful_call = Some(Instant::now());
            state.last_millis_behind_latest = adapter.millis_behind_latest();
            state.last_get_records_returned_records_count = Some(adapter.records().len() as i32);
            if let Some(req_id) = adapter.request_id() {
                *state.last_successful_request_details.lock().unwrap() =
                    RequestDetails::new(req_id, chrono::Utc::now().to_rfc3339());
            }

            let is_at_shard_end = state.strategy.get_data_fetcher().is_shard_end_reached();
            let base_input = adapter.to_process_records_input();
            // Rebuild with cacheEntryTime + isAtShardEnd (Java toBuilder()...).
            let input = rebuild_input(&base_input, state.last_successful_call, is_at_shard_end);

            let highest = state.calculate_highest_sequence_number(&input);
            let batch = PrefetchRecordsRetrieved::new(
                input,
                highest.clone(),
                adapter.next_shard_iterator(),
                PrefetchRecordsRetrieved::generate_batch_unique_identifier(),
            );
            state.highest_sequence_number = highest;
            enqueue(state, batch);
            state.throttling_reporter.success();
        }
        Err(FetchError::Retryable { .. }) => {
            tracing::info!(
                "{}: Timeout occurred while waiting for response from Kinesis. Will retry.",
                state.config.stream_and_shard_id
            );
        }
        Err(FetchError::InvalidArgument { .. }) => {
            tracing::info!(
                "{}: records threw InvalidArgumentException - iterator will be refreshed before retrying",
                state.config.stream_and_shard_id
            );
            // The re-acquire itself can now fail (timeout / non-ResourceNotFound
            // SDK error on the internal GetShardIterator call). This is a
            // retryable tick failure, not shard-end and not a panic: log it and
            // let the loop's next tick retry (matching the `catch_tick`
            // containment's "log and keep looping" behavior for the fetch step).
            if let Err(restart_err) = state.strategy.get_data_fetcher().restart_iterator().await {
                tracing::error!(
                    "{}: Failed to refresh the iterator after an InvalidArgumentException; will retry on the next loop iteration: {restart_err}",
                    state.config.stream_and_shard_id
                );
            }
        }
        Err(FetchError::ExpiredIterator { .. }) => {
            tracing::info!(
                "{}: records threw ExpiredIteratorException - restarting after greatest seqNum passed to customer",
                state.config.stream_and_shard_id
            );
            // Java emits the EXPIRED_ITERATOR metric here (SUMMARY).
            // Same non-fatal handling as above: a failed re-acquire is logged
            // and retried on the next tick, not treated as shard-end.
            if let Err(restart_err) = state.strategy.get_data_fetcher().restart_iterator().await {
                tracing::error!(
                    "{}: Failed to restart the iterator after an ExpiredIteratorException; will retry on the next loop iteration: {restart_err}",
                    state.config.stream_and_shard_id
                );
            }
        }
        Err(FetchError::ProvisionedThroughputExceeded { .. }) => {
            tracing::error!(
                "{}: ProvisionedThroughputExceededException thrown while fetching records",
                state.config.stream_and_shard_id
            );
            state.throttling_reporter.throttled();
        }
        Err(FetchError::Sdk { message, .. }) => {
            // `message` now carries the full `DisplayErrorContext` chain (see
            // `classify_sdk_error`/`error_chain_string` in
            // `kinesis_data_fetcher.rs`) -- this is the ONE log for an
            // unclassified GetRecords SDK failure; the data-fetcher layer
            // deliberately does not also log it, to avoid double-logging the
            // same error.
            tracing::warn!(
                "{}: Exception thrown while fetching records from Kinesis: {message}",
                state.config.stream_and_shard_id
            );
        }
    }
}

/// Rebuild a `ProcessRecordsInput` copying data fields, setting `cacheEntryTime`
/// and `isAtShardEnd` (bon has no `to_builder`; the lifecycle type is not
/// editable here).
fn rebuild_input(
    src: &crate::lifecycle::events::process_records_input::ProcessRecordsInput,
    cache_entry_time: Option<Instant>,
    is_at_shard_end: bool,
) -> crate::lifecycle::events::process_records_input::ProcessRecordsInput {
    let _ = cache_entry_time; // wall-clock stamp below
    use crate::lifecycle::events::process_records_input::ProcessRecordsInput;
    ProcessRecordsInput::builder()
        .cache_entry_time(chrono::Utc::now())
        .is_at_shard_end(is_at_shard_end)
        .maybe_records(src.records().map(|r| r.to_vec()))
        .maybe_checkpointer(src.checkpointer().cloned())
        .maybe_millis_behind_latest(src.millis_behind_latest())
        .maybe_child_shards(src.child_shards().map(|c| c.to_vec()))
        .build()
}

/// Enqueue a fetched batch, updating the backpressure counters (Java
/// `addArrivedRecordsInput` + `PrefetchCounters.added`).
fn enqueue(state: &mut PublisherState, batch: PrefetchRecordsRetrieved) {
    state.counters_added(&batch);
    state.queue.push_back(batch);
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::InitialPositionInStream;
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::get_records_response_adapter::GetRecordsResponseAdapter;
    use crate::retrieval::kinesis_client_record::KinesisClientRecord;
    use crate::retrieval::polling::data_fetcher::{DataFetcher, DataFetcherResult};
    use crate::retrieval::records_delivery_ack::SimpleRecordsDeliveryAck;
    use aws_sdk_kinesis::types::ChildShard;
    use std::sync::atomic::{AtomicUsize, Ordering};

    // A GetRecordsResponseAdapter over a fixed record list (test double).
    struct TestAdapter {
        records: Vec<KinesisClientRecord>,
        millis_behind: Option<i64>,
        next_iterator: Option<String>,
        child_shards: Vec<ChildShard>,
    }
    impl GetRecordsResponseAdapter for TestAdapter {
        fn records(&self) -> Vec<KinesisClientRecord> {
            self.records.clone()
        }
        fn millis_behind_latest(&self) -> Option<i64> {
            self.millis_behind
        }
        fn child_shards(&self) -> Vec<ChildShard> {
            self.child_shards.clone()
        }
        fn next_shard_iterator(&self) -> Option<String> {
            self.next_iterator.clone()
        }
        fn request_id(&self) -> Option<String> {
            Some("req-1".to_string())
        }
    }

    // A fake DataFetcher (only used for stream_identifier + shard-end + reset).
    // Counts `initialize`/`restart_iterator` calls so tests can verify them
    // (mirroring Mockito `verify(dataFetcher).initialize(...)`/`.restartIterator()`).
    // `fail_init_times` lets a test make the next N `initialize_from_extended`
    // calls fail (2026-07-14 fix: `PrefetchRecordsPublisher::start` must
    // surface such a failure instead of proceeding as if it succeeded).
    // `panic_on_reset` lets a test make `reset_iterator` panic, to verify
    // command-handling panic containment (2026-07-14 hardening item 5):
    // `Command::RestartFrom` synchronously calls `reset_iterator`.
    struct FakeDataFetcher {
        shard_end: std::sync::atomic::AtomicBool,
        init_count: AtomicUsize,
        restart_count: AtomicUsize,
        fail_init_times: AtomicUsize,
        panic_on_reset: std::sync::atomic::AtomicBool,
    }
    impl FakeDataFetcher {
        fn new() -> Self {
            Self {
                shard_end: std::sync::atomic::AtomicBool::new(false),
                init_count: AtomicUsize::new(0),
                restart_count: AtomicUsize::new(0),
                fail_init_times: AtomicUsize::new(0),
                panic_on_reset: std::sync::atomic::AtomicBool::new(false),
            }
        }
        fn with_shard_end(shard_end: bool) -> Self {
            let f = Self::new();
            f.shard_end.store(shard_end, Ordering::SeqCst);
            f
        }
        /// The next `n` calls to `initialize`/`initialize_from_extended` return
        /// `Err`; calls after that succeed.
        fn failing_init_times(n: usize) -> Self {
            let f = Self::new();
            f.fail_init_times.store(n, Ordering::SeqCst);
            f
        }
        /// `reset_iterator` panics every time it's called.
        fn panicking_on_reset() -> Self {
            let f = Self::new();
            f.panic_on_reset.store(true, Ordering::SeqCst);
            f
        }
    }
    #[async_trait]
    impl DataFetcher for FakeDataFetcher {
        async fn get_records(&self) -> Result<Box<dyn DataFetcherResult>, FetchError> {
            unreachable!("strategy is mocked directly")
        }
        async fn initialize(
            &self,
            _c: &str,
            _p: &InitialPositionInStreamExtended,
        ) -> Result<(), FetchError> {
            self.init_count.fetch_add(1, Ordering::SeqCst);
            Ok(())
        }
        async fn initialize_from_extended(
            &self,
            _c: &ExtendedSequenceNumber,
            _p: &InitialPositionInStreamExtended,
        ) -> Result<(), FetchError> {
            self.init_count.fetch_add(1, Ordering::SeqCst);
            let mut remaining = self.fail_init_times.load(Ordering::SeqCst);
            while remaining > 0 {
                match self.fail_init_times.compare_exchange(
                    remaining,
                    remaining - 1,
                    Ordering::SeqCst,
                    Ordering::SeqCst,
                ) {
                    Ok(_) => {
                        return Err(FetchError::Sdk {
                            message: "injected init failure".to_string(),
                            source: None,
                        })
                    }
                    Err(actual) => remaining = actual,
                }
            }
            Ok(())
        }
        async fn advance_iterator_to(
            &self,
            _s: &str,
            _p: &InitialPositionInStreamExtended,
        ) -> Result<(), FetchError> {
            Ok(())
        }
        async fn restart_iterator(&self) -> Result<(), FetchError> {
            self.restart_count.fetch_add(1, Ordering::SeqCst);
            Ok(())
        }
        fn reset_iterator(
            &self,
            _shard_iterator: Option<String>,
            _seq: &str,
            _p: &InitialPositionInStreamExtended,
        ) {
            if self.panic_on_reset.load(Ordering::SeqCst) {
                panic!("injected reset_iterator panic (command-handling containment test)");
            }
        }
        fn stream_identifier(&self) -> crate::common::StreamIdentifier {
            crate::common::StreamIdentifier::single_stream_instance("stream")
        }
        fn is_shard_end_reached(&self) -> bool {
            self.shard_end.load(Ordering::SeqCst)
        }
        fn next_iterator(&self) -> Option<String> {
            Some("iter".to_string())
        }
    }

    // A strategy that returns canned adapters in sequence, then empty responses.
    struct SeqStrategy {
        responses: Mutex<VecDeque<Result<TestAdapter, FetchError>>>,
        idx: AtomicUsize,
        fetcher: Arc<FakeDataFetcher>,
    }
    impl SeqStrategy {
        /// Number of `get_records_adapter` invocations so far (Java Mockito
        /// `verify(strategy, times(n)).getRecordsAdapter(...)`).
        fn fetch_count(&self) -> usize {
            self.idx.load(Ordering::SeqCst)
        }
    }
    #[async_trait]
    impl GetRecordsRetrievalStrategy for SeqStrategy {
        async fn get_records_adapter(
            &self,
            _max_records: i32,
        ) -> Result<Box<dyn GetRecordsResponseAdapter>, FetchError> {
            self.idx.fetch_add(1, Ordering::SeqCst);
            let mut q = self.responses.lock().unwrap();
            match q.pop_front() {
                Some(Ok(a)) => Ok(Box::new(a)),
                Some(Err(e)) => Err(e),
                None => Ok(Box::new(TestAdapter {
                    records: vec![],
                    millis_behind: Some(0),
                    next_iterator: Some("iter".to_string()),
                    child_shards: vec![],
                })),
            }
        }
        fn shutdown(&self) {}
        fn is_shutdown(&self) -> bool {
            false
        }
        fn get_data_fetcher(&self) -> Arc<dyn DataFetcher> {
            Arc::clone(&self.fetcher) as Arc<dyn DataFetcher>
        }
    }

    fn record(seq: &str, data: &[u8]) -> KinesisClientRecord {
        KinesisClientRecord::builder()
            .sequence_number(seq.to_string())
            .partition_key("pk")
            .data(bytes::Bytes::copy_from_slice(data))
            .build()
    }

    fn adapter(seq: &str, next_iter: &str) -> TestAdapter {
        TestAdapter {
            records: vec![record(seq, b"data")],
            millis_behind: Some(0),
            next_iterator: Some(next_iter.to_string()),
            child_shards: vec![],
        }
    }

    fn build_publisher(
        max_pending: usize,
        responses: VecDeque<Result<TestAdapter, FetchError>>,
    ) -> Arc<PrefetchRecordsPublisher> {
        build_publisher_full(max_pending, 10, responses, Arc::new(FakeDataFetcher::new())).0
    }

    /// Build a publisher with an explicit idle time + fetcher, returning both the
    /// publisher and the `SeqStrategy` (whose `idx` counts `getRecordsAdapter`
    /// calls — the Rust analog of Mockito `verify(strategy, times(n)).getRecordsAdapter`).
    fn build_publisher_full(
        max_pending: usize,
        idle_millis: i64,
        responses: VecDeque<Result<TestAdapter, FetchError>>,
        fetcher: Arc<FakeDataFetcher>,
    ) -> (Arc<PrefetchRecordsPublisher>, Arc<SeqStrategy>) {
        let strategy = Arc::new(SeqStrategy {
            responses: Mutex::new(responses),
            idx: AtomicUsize::new(0),
            fetcher,
        });
        let publisher = Arc::new(PrefetchRecordsPublisher::new(
            max_pending,
            3 * 1024 * 1024,
            15_000,
            10_000,
            Arc::clone(&strategy) as Arc<dyn GetRecordsRetrievalStrategy>,
            idle_millis,
            0,
            Arc::new(NullMetricsFactory),
            "ProcessTask",
            "shardId-000000000000",
            ThrottlingReporter::new(5, "shardId-000000000000"),
            Arc::new(crate::retrieval::polling::KinesisSleepTimeController),
        ));
        (publisher, strategy)
    }

    fn latest_pos() -> InitialPositionInStreamExtended {
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest)
    }

    // Port of PrefetchRecordsPublisherTest.testGetRecords: two batches prefetched
    // and delivered in order via the subscription request/ack cycle.
    #[tokio::test]
    async fn get_records_delivers_batches_in_order() {
        let mut responses = VecDeque::new();
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        responses.push_back(Ok(adapter("seq-2", "iter-2")));
        let publisher = build_publisher(3, responses);

        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();

        let mut received = Vec::new();
        sub.request(1);
        for _ in 0..2 {
            let batch = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
                .await
                .expect("delivery timed out")
                .expect("channel closed")
                .expect("no retrieval error");
            let seq = batch.process_records_input().records().unwrap()[0]
                .sequence_number()
                .unwrap()
                .to_string();
            received.push(seq);
            let ack = SimpleRecordsDeliveryAck::new(batch.batch_unique_identifier());
            publisher.notify(Box::new(ack)).await;
            sub.request(1);
        }
        assert_eq!(received, vec!["seq-1", "seq-2"]);
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testMaxPendingProcessRecordsInputIsZero:
    // demand-driven mode fetches one at a time only when demand exists.
    #[tokio::test]
    async fn max_pending_zero_is_demand_driven() {
        let mut responses = VecDeque::new();
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        responses.push_back(Ok(adapter("seq-2", "iter-2")));
        let publisher = build_publisher(0, responses);

        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();

        sub.request(1);
        let b1 = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            b1.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-1")
        );
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                b1.batch_unique_identifier(),
            )))
            .await;
        sub.request(1);
        let b2 = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            b2.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-2")
        );
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testRetryableRetrievalExceptionContinues:
    // a retryable failure is retried and millisBehindLatest propagates.
    #[tokio::test]
    async fn retryable_exception_continues_and_propagates_millis_behind() {
        let mut responses = VecDeque::new();
        responses.push_back(Err(FetchError::Retryable {
            message: "Timeout".to_string(),
            source: None,
        }));
        responses.push_back(Ok(TestAdapter {
            records: vec![],
            millis_behind: Some(100),
            next_iterator: Some("iter-1".to_string()),
            child_shards: vec![],
        }));
        let publisher = build_publisher(3, responses);

        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(3), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            batch.process_records_input().millis_behind_latest(),
            Some(100)
        );
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testGetRecordsWithShardEnd: child shards
    // + isAtShardEnd propagate.
    #[tokio::test]
    async fn shard_end_propagates_child_shards() {
        let child = ChildShard::builder()
            .shard_id("shardId-000000000001")
            .parent_shards("shardId-000000000000")
            .build()
            .unwrap();
        let mut responses = VecDeque::new();
        responses.push_back(Ok(TestAdapter {
            records: vec![],
            millis_behind: Some(0),
            next_iterator: None,
            child_shards: vec![child.clone()],
        }));
        // FakeDataFetcher reports shard end.
        let (publisher, _strategy) = build_publisher_full(
            3,
            10,
            responses,
            Arc::new(FakeDataFetcher::with_shard_end(true)),
        );

        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        let input = batch.process_records_input();
        assert!(input.records().unwrap().is_empty());
        assert!(input.is_at_shard_end());
        assert_eq!(input.child_shards().unwrap().len(), 1);
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testResetClearsRemainingData: restartFrom
    // discards queued/in-flight records and restarts delivery from the reset point.
    #[tokio::test]
    async fn reset_clears_remaining_data_and_restarts() {
        // Ten distinct batches; the publisher prefetches several, then we reset
        // from the first-delivered batch and expect the next delivery to be the
        // batch that followed it (re-fetched), not a stale queued batch.
        let mut responses = VecDeque::new();
        for i in 0..10 {
            responses.push_back(Ok(adapter(&format!("seq-{i}"), &format!("iter-{}", i + 1))));
        }
        let publisher = build_publisher(5, responses);

        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();

        sub.request(1);
        let first = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        let first_seq = first.process_records_input().records().unwrap()[0]
            .sequence_number()
            .unwrap()
            .to_string();
        assert_eq!(first_seq, "seq-0");

        // Ack + request the next so the queue advances a bit.
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                first.batch_unique_identifier(),
            )))
            .await;
        sub.request(1);
        let second = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            second.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-1")
        );

        // Restart from the first batch: clears the queue + resets the iterator.
        publisher.restart_from(Arc::clone(&first)).await;
        // Let the reset command be processed (it zeroes demand) before requesting,
        // mirroring the consumer's restartFrom-then-request ordering.
        tokio::time::sleep(std::time::Duration::from_millis(50)).await;

        // After the reset, request again; the publisher re-fetches from the reset
        // point. The next delivered batch is a fresh fetch (the queue was cleared).
        sub.request(1);
        let post = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        // A batch is delivered (proving the loop resumed after reset).
        assert!(post.process_records_input().records().is_some());
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testProvisionedThroughputExceededExceptionReporter
    // (behavioral core): a throttle failure is reported, then success resets — the
    // publisher recovers and delivers.
    #[tokio::test]
    async fn provisioned_throughput_exceeded_is_reported_then_recovers() {
        let mut responses = VecDeque::new();
        responses.push_back(Err(FetchError::ProvisionedThroughputExceeded {
            message: "throttled".to_string(),
        }));
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        let publisher = build_publisher(3, responses);
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(3), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            batch.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-1")
        );
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testExpiredIteratorException: an expired
    // iterator triggers restart + recovery.
    #[tokio::test]
    async fn expired_iterator_restarts_and_recovers() {
        let mut responses = VecDeque::new();
        responses.push_back(Err(FetchError::ExpiredIterator {
            message: "expired".to_string(),
        }));
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        let publisher = build_publisher(3, responses);
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(3), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            batch.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-1")
        );
        publisher.shutdown().await;
    }

    // A stale ack (mismatched batch id) is ignored — the head is not evicted, so
    // the next delivery still requires a matching ack.
    #[tokio::test]
    async fn stale_ack_is_ignored() {
        let mut responses = VecDeque::new();
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        responses.push_back(Ok(adapter("seq-2", "iter-2")));
        let publisher = build_publisher(3, responses);
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let first = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        // Send a stale ack (unknown id) — should be ignored (head not evicted).
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                BatchUniqueIdentifier::new("bogus", ""),
            )))
            .await;
        // The correct ack still evicts and lets the next batch flow.
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                first.batch_unique_identifier(),
            )))
            .await;
        sub.request(1);
        let second = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            second.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-2")
        );
        publisher.shutdown().await;
    }

    // subscribe before start; a request before start does not deliver, but after
    // start the cycle proceeds (mirrors the ordering contract).
    #[tokio::test]
    async fn last_successful_request_details_updates_after_fetch() {
        let mut responses = VecDeque::new();
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        let publisher = build_publisher(3, responses);
        assert_eq!(
            publisher.last_successful_request_details().request_id(),
            "NONE"
        );
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let _ = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            publisher.last_successful_request_details().request_id(),
            "req-1"
        );
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testDataFetcherIsNotReInitializedOnMultipleCacheStarts:
    // multiple start() calls initialize the data fetcher exactly once (start is
    // idempotent).
    #[tokio::test]
    async fn data_fetcher_not_reinitialized_on_multiple_starts() {
        let fetcher = Arc::new(FakeDataFetcher::new());
        let (publisher, _strategy) =
            build_publisher_full(3, 10, VecDeque::new(), Arc::clone(&fetcher));
        let _sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        assert_eq!(fetcher.init_count.load(Ordering::SeqCst), 1);
        publisher.shutdown().await;
    }

    // New (2026-07-14 bug fix): a `start()` whose data-fetcher init fails must
    // return `Err`, must NOT spawn the prefetch task / flip `started`, and a
    // later `start()` retry (the `InitializeTask` retry path) must work exactly
    // like a first attempt — proving the publisher is retry-able rather than
    // wedged. This directly exercises the false-shard-end bug: before the fix,
    // `initialize_from_extended` never returned an error at all, so `start`
    // always "succeeded" even when the very first `GetShardIterator` failed.
    #[tokio::test]
    async fn start_fails_when_data_fetcher_init_fails_then_retry_succeeds() {
        let fetcher = Arc::new(FakeDataFetcher::failing_init_times(1));
        let mut responses = VecDeque::new();
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        let (publisher, _strategy) = build_publisher_full(3, 10, responses, Arc::clone(&fetcher));

        let mut sub = publisher.subscribe();
        let first = publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await;
        assert!(
            first.is_err(),
            "the first start() should surface the init failure"
        );
        assert_eq!(
            fetcher.init_count.load(Ordering::SeqCst),
            1,
            "the failing init attempt still counts as an attempt"
        );

        // Retry: a second start() call must actually retry the data-fetcher
        // init (not short-circuit as already-started) and this time succeed.
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .expect("retry should succeed once the data fetcher stops failing");
        assert_eq!(
            fetcher.init_count.load(Ordering::SeqCst),
            2,
            "the retry must re-attempt initialization, proving `start` isn't wedged"
        );

        // And the publisher now works normally: the pre-existing subscription
        // (from before either start() call) still receives deliveries.
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("delivery timed out")
            .expect("channel closed")
            .expect("no retrieval error");
        assert_eq!(
            batch.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-1")
        );
        publisher.shutdown().await;
    }

    // New (2026-07-14 hardening item 5): a panic while handling a command
    // (here, `RestartFrom` -> `PublisherState::reset` ->
    // `DataFetcher::reset_iterator`, made to panic) must not kill the
    // publisher's owning `run_task`. Before this fix only the fetch step was
    // wrapped in `catch_tick`; a panic here would have silently ended the task,
    // wedging the consumer (dead delivery channel forever).
    #[tokio::test]
    async fn panic_in_command_handling_does_not_kill_run_task() {
        let mut responses = VecDeque::new();
        for i in 0..3 {
            responses.push_back(Ok(adapter(&format!("seq-{i}"), &format!("iter-{}", i + 1))));
        }
        let (publisher, _strategy) = build_publisher_full(
            3,
            10,
            responses,
            Arc::new(FakeDataFetcher::panicking_on_reset()),
        );

        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();

        sub.request(1);
        let first = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");

        // Triggers `Command::RestartFrom` on the publisher's owning task, which
        // synchronously panics inside `reset_iterator`. `handle_command_guarded`
        // must catch it, log it, and let the loop keep running.
        publisher.restart_from(Arc::clone(&first)).await;
        tokio::time::sleep(std::time::Duration::from_millis(50)).await;

        // The task survived: a further request still gets delivered.
        sub.request(1);
        let recovered = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv()).await;
        assert!(
            matches!(recovered, Ok(Some(Ok(_)))),
            "run_task should survive a panic in command handling and keep delivering, got {recovered:?}"
        );

        // shutdown() still completes: a wedged/dead task would hang this
        // forever waiting on the oneshot shutdown ack.
        tokio::time::timeout(std::time::Duration::from_secs(2), publisher.shutdown())
            .await
            .expect("shutdown should still complete after a contained command panic");
    }

    // Port of PrefetchRecordsPublisherTest.testGetRecordsWithInitialFailures_AdequateWait_Success:
    // two initial retryable failures followed by success still deliver the batch
    // when the consumer waits long enough.
    #[tokio::test]
    async fn initial_failures_adequate_wait_success() {
        let mut responses = VecDeque::new();
        responses.push_back(Err(FetchError::Retryable {
            message: "Timed out".to_string(),
            source: None,
        }));
        responses.push_back(Err(FetchError::Retryable {
            message: "Timed out again".to_string(),
            source: None,
        }));
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        // Short idle time so the retries + success fit inside the recv timeout.
        let (publisher, strategy) =
            build_publisher_full(3, 10, responses, Arc::new(FakeDataFetcher::new()));
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(4), sub.recv())
            .await
            .expect("adequate wait should succeed")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            batch.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-1")
        );
        // At least 3 fetches (2 failed + 1 success).
        assert!(
            strategy.fetch_count() >= 3,
            "fetches: {}",
            strategy.fetch_count()
        );
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testGetRecordsWithInitialFailures_LessThanRequiredWait_Throws:
    // with a large idle time between calls, a consumer that waits less than the
    // required retry span sees no delivery (Java: the blocking wait throws).
    #[tokio::test]
    async fn initial_failures_less_than_required_wait_throws() {
        let mut responses = VecDeque::new();
        responses.push_back(Err(FetchError::Retryable {
            message: "Timed out".to_string(),
            source: None,
        }));
        responses.push_back(Err(FetchError::Retryable {
            message: "Timed out again".to_string(),
            source: None,
        }));
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        // 1s idle time: the second/third calls are paced ~1s apart, so a short
        // recv timeout elapses before a record is available.
        let (publisher, _strategy) =
            build_publisher_full(3, 1000, responses, Arc::new(FakeDataFetcher::new()));
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let result = tokio::time::timeout(std::time::Duration::from_millis(200), sub.recv()).await;
        assert!(
            result.is_err(),
            "should time out before a record is available"
        );
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testFullCacheSize: with no consumer
    // demand, the prefetch queue fills to max_pending and backpressure stops
    // further fetches (the strategy is not called unboundedly).
    #[tokio::test]
    async fn full_cache_size_backpressure_stops_fetching() {
        let max_size = 5;
        // Supply plenty of non-empty batches; without consumption the queue caps.
        let mut responses = VecDeque::new();
        for i in 0..50 {
            responses.push_back(Ok(adapter(&format!("seq-{i}"), &format!("iter-{}", i + 1))));
        }
        let (publisher, strategy) =
            build_publisher_full(max_size, 1, responses, Arc::new(FakeDataFetcher::new()));
        let _sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        // Never request/consume; let the cache fill.
        tokio::time::sleep(std::time::Duration::from_millis(300)).await;
        // Backpressure caps fetches near the queue capacity; nowhere near the 50
        // available responses.
        let count = strategy.fetch_count();
        assert!(
            count <= max_size + 1,
            "backpressure should cap fetches near {max_size}, got {count}"
        );
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testFullCacheRecordsCount: with a
    // records-count cap far above per-batch size, the derived call rate stays
    // below the queue capacity (the Java test asserts only this arithmetic).
    #[tokio::test]
    async fn full_cache_records_count_call_rate_below_capacity() {
        const MAX_RECORDS_COUNT: i64 = 15_000;
        const MAX_SIZE: i64 = 5;
        let records_size = 4500i64;
        let call_rate = (MAX_RECORDS_COUNT as f64 / records_size as f64).ceil() as i64;
        assert!(call_rate < MAX_SIZE, "Call Rate is {call_rate}");
    }

    // Port of PrefetchRecordsPublisherTest.testInvalidArgumentExceptionIsRetried:
    // an InvalidArgumentException restarts the iterator once, then recovers.
    #[tokio::test]
    async fn invalid_argument_exception_is_retried() {
        let mut responses = VecDeque::new();
        responses.push_back(Err(FetchError::InvalidArgument {
            message: "bad arg".to_string(),
        }));
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        let fetcher = Arc::new(FakeDataFetcher::new());
        let (publisher, _strategy) = build_publisher_full(3, 10, responses, Arc::clone(&fetcher));
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(3), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            batch.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-1")
        );
        // restart_iterator was called exactly once (Java verify(dataFetcher, times(1))).
        assert_eq!(fetcher.restart_count.load(Ordering::SeqCst), 1);
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testExpiredIteratorExceptionWithIllegalStateException:
    // two ExpiredIteratorException cycles each restart the iterator and the loop
    // survives (recovers). NOTE: the Java variant additionally makes
    // `restartIterator` throw IllegalStateException to prove the daemon does not
    // die; the Rust `restart_iterator` is infallible, so that specific throw is
    // not reproducible — the resilience-across-two-cycles behavior is covered.
    #[tokio::test]
    async fn expired_iterator_two_cycles_restarts_twice() {
        let mut responses = VecDeque::new();
        responses.push_back(Err(FetchError::ExpiredIterator {
            message: "expired".to_string(),
        }));
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        responses.push_back(Err(FetchError::ExpiredIterator {
            message: "expired again".to_string(),
        }));
        responses.push_back(Ok(adapter("seq-2", "iter-2")));
        let fetcher = Arc::new(FakeDataFetcher::new());
        let (publisher, _strategy) = build_publisher_full(3, 10, responses, Arc::clone(&fetcher));
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();

        // Consume both delivered batches (across the two expired cycles).
        for expected in ["seq-1", "seq-2"] {
            sub.request(1);
            let batch = tokio::time::timeout(std::time::Duration::from_secs(3), sub.recv())
                .await
                .expect("timed out")
                .unwrap()
                .expect("no retrieval error");
            assert_eq!(
                batch.process_records_input().records().unwrap()[0].sequence_number(),
                Some(expected)
            );
            publisher
                .notify(Box::new(SimpleRecordsDeliveryAck::new(
                    batch.batch_unique_identifier(),
                )))
                .await;
        }
        // restart_iterator invoked once per expired cycle (2 total).
        assert_eq!(fetcher.restart_count.load(Ordering::SeqCst), 2);
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherTest.testRepeatSdkExceptionLoop: a repeated
    // generic SDK exception keeps the fetch loop retrying (the publisher does not
    // die and does not deliver); a consumer waiting a bounded time sees no record.
    #[tokio::test]
    async fn repeat_sdk_exception_loop() {
        let mut responses = VecDeque::new();
        // First a success (Java: "return a valid response to cause lastSuccessfulCall
        // to initialize"), then a run of SDK exceptions.
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        // Enough SDK errors that the loop keeps failing throughout the bounded
        // wait window below (Java's mock throws indefinitely).
        for _ in 0..500 {
            responses.push_back(Err(FetchError::Sdk {
                message: "lose yourself to dance".to_string(),
                source: None,
            }));
        }
        let (publisher, strategy) =
            build_publisher_full(3, 10, responses, Arc::new(FakeDataFetcher::new()));
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();

        // First call succeeds and delivers.
        sub.request(1);
        let first = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("first call should succeed")
            .unwrap()
            .expect("no retrieval error");
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                first.batch_unique_identifier(),
            )))
            .await;

        // Now request again; the SDK exceptions loop (no delivery, no crash).
        sub.request(1);
        let result = tokio::time::timeout(std::time::Duration::from_millis(300), sub.recv()).await;
        assert!(
            result.is_err(),
            "SDK exception loop should not deliver a record"
        );
        // The loop kept retrying (multiple fetch attempts beyond the initial success).
        assert!(
            strategy.fetch_count() >= 3,
            "fetches: {}",
            strategy.fetch_count()
        );
        publisher.shutdown().await;
    }

    // ---- Ported from PrefetchRecordsPublisherIntegrationTest ----

    /// An adapter with empty records + a given millisBehindLatest (Java's
    /// `KinesisDataFetcherForTest.getRecords` empty-record response).
    fn empty_adapter(millis_behind: i64) -> TestAdapter {
        TestAdapter {
            records: vec![],
            millis_behind: Some(millis_behind),
            next_iterator: Some("testNextShardIterator".to_string()),
            child_shards: vec![],
        }
    }

    // Port of PrefetchRecordsPublisherIntegrationTest.testRollingCache: two
    // successive (empty, millisBehindLatest=1000) batches are delivered and are
    // distinct objects, with cacheEntryTime set.
    #[tokio::test]
    async fn rolling_cache() {
        let mut responses = VecDeque::new();
        for _ in 0..5 {
            responses.push_back(Ok(empty_adapter(1000)));
        }
        let (publisher, _strategy) =
            build_publisher_full(3, 10, responses, Arc::new(FakeDataFetcher::new()));
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();

        sub.request(1);
        let b1 = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no error");
        let input1 = b1.process_records_input();
        assert!(input1.records().unwrap().is_empty());
        assert_eq!(input1.millis_behind_latest(), Some(1000));
        assert!(input1.cache_entry_time().is_some());
        let id1 = b1.batch_unique_identifier();
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(id1.clone())))
            .await;

        sub.request(1);
        let b2 = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no error");
        // Distinct batch (rolling): different unique identifier.
        assert_ne!(b2.batch_unique_identifier(), id1);
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherIntegrationTest.testFullCache: with no
    // consumption the queue fills to MAX_SIZE, and two subsequently-evicted
    // batches are distinct.
    #[tokio::test]
    async fn full_cache_two_distinct_batches() {
        let mut responses = VecDeque::new();
        for _ in 0..20 {
            responses.push_back(Ok(empty_adapter(1000)));
        }
        let max_size = 3;
        let (publisher, strategy) =
            build_publisher_full(max_size, 1, responses, Arc::new(FakeDataFetcher::new()));
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();

        // Let the cache fill up without consuming.
        tokio::time::sleep(std::time::Duration::from_millis(200)).await;
        // Backpressure caps prefetch at ~max_size.
        assert!(
            strategy.fetch_count() <= max_size + 1,
            "prefetch should cap near {max_size}, got {}",
            strategy.fetch_count()
        );

        // Evict two batches; they must be distinct.
        sub.request(1);
        let p1 = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no error");
        let id1 = p1.batch_unique_identifier();
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(id1.clone())))
            .await;
        sub.request(1);
        let p2 = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no error");
        assert_ne!(p2.batch_unique_identifier(), id1);
        publisher.shutdown().await;
    }

    // Port of PrefetchRecordsPublisherIntegrationTest.testExpiredIteratorException:
    // one ExpiredIteratorException then a real (empty-record) response; the
    // iterator is restarted and an empty batch is delivered.
    //
    // NOTE: the sibling PrefetchRecordsPublisherIntegrationTest
    // .testExpiredIteratorExceptionWithInnerRestartIteratorException (2 expired
    // cycles while `restartIterator` throws IllegalStateException) is covered by
    // `expired_iterator_two_cycles_restarts_twice`; the "throwing restart does not
    // kill the loop" nuance is not reproducible because the Rust `restart_iterator`
    // is infallible.
    #[tokio::test]
    async fn integration_expired_iterator_restarts_and_delivers_empty() {
        let mut responses = VecDeque::new();
        responses.push_back(Err(FetchError::ExpiredIterator {
            message: "ExpiredIterator".to_string(),
        }));
        responses.push_back(Ok(empty_adapter(1000)));
        let fetcher = Arc::new(FakeDataFetcher::new());
        let (publisher, _strategy) = build_publisher_full(3, 10, responses, Arc::clone(&fetcher));
        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(3), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no error");
        assert!(batch.process_records_input().records().unwrap().is_empty());
        assert_eq!(fetcher.restart_count.load(Ordering::SeqCst), 1);
        publisher.shutdown().await;
    }

    // The production lifecycle order: `InitializeTask` starts the publisher
    // first; the `ShardConsumerSubscriber` subscribes only after initialization
    // completes (Java `subscribe` even *requires* a prior `start`). The task must
    // run and buffer without a subscriber, then deliver once one attaches.
    #[tokio::test]
    async fn start_before_subscribe_delivers() {
        let mut responses = VecDeque::new();
        responses.push_back(Ok(adapter("seq-1", "iter-1")));
        responses.push_back(Ok(adapter("seq-2", "iter-2")));
        let publisher = build_publisher(3, responses);

        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        // Give the prefetch loop a moment to buffer with no subscriber attached.
        tokio::time::sleep(std::time::Duration::from_millis(100)).await;

        let mut sub = publisher.subscribe();
        sub.request(1);
        let batch = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("delivery timed out")
            .expect("channel closed")
            .expect("no retrieval error");
        assert_eq!(
            batch.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-1")
        );
        publisher.shutdown().await;
    }

    // The health-check restart flow (`ShardConsumerSubscriber::start_subscriptions`
    // after a stall): cancel + drop the old subscription, `restart_from` the last
    // delivered batch, subscribe fresh — the new subscription's demand must reach
    // the live task and delivery must resume (previously the new sink was parked
    // in `pending_sink`, which only the one-shot `start` consumed → dead shard).
    #[tokio::test]
    async fn resubscribe_after_restart_resumes_delivery() {
        let mut responses = VecDeque::new();
        for i in 0..10 {
            responses.push_back(Ok(adapter(&format!("seq-{i}"), &format!("iter-{}", i + 1))));
        }
        let publisher = build_publisher(3, responses);

        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let first = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        assert_eq!(
            first.process_records_input().records().unwrap()[0].sequence_number(),
            Some("seq-0")
        );

        // Simulate the subscriber restart: cancel, drop the subscription, reset
        // to the last successfully processed batch.
        sub.cancel();
        drop(sub);
        publisher.restart_from(Arc::clone(&first)).await;
        tokio::time::sleep(std::time::Duration::from_millis(50)).await;

        // Fresh subscription on the already-running task.
        let mut sub2 = publisher.subscribe();
        sub2.request(1);
        let resumed = tokio::time::timeout(std::time::Duration::from_secs(2), sub2.recv())
            .await
            .expect("re-subscribe must resume delivery")
            .expect("channel closed")
            .expect("no retrieval error");
        assert!(resumed.process_records_input().records().is_some());
        publisher.shutdown().await;
    }

    // A dropped subscription (no cancel, handle just goes away) detaches the sink;
    // the publisher keeps running and a later re-subscribe still gets deliveries.
    #[tokio::test]
    async fn dropped_subscription_then_resubscribe_recovers() {
        let mut responses = VecDeque::new();
        for i in 0..10 {
            responses.push_back(Ok(adapter(&format!("seq-{i}"), &format!("iter-{}", i + 1))));
        }
        let publisher = build_publisher(2, responses);

        let mut sub = publisher.subscribe();
        publisher
            .start(ExtendedSequenceNumber::latest(), latest_pos())
            .await
            .unwrap();
        sub.request(1);
        let first = tokio::time::timeout(std::time::Duration::from_secs(2), sub.recv())
            .await
            .expect("timed out")
            .unwrap()
            .expect("no retrieval error");
        drop(sub);
        // Let the task observe the closed demand channel (and not busy-spin).
        tokio::time::sleep(std::time::Duration::from_millis(100)).await;

        publisher.restart_from(first).await;
        let mut sub2 = publisher.subscribe();
        sub2.request(1);
        let resumed = tokio::time::timeout(std::time::Duration::from_secs(2), sub2.recv())
            .await
            .expect("re-subscribe after drop must resume delivery")
            .expect("channel closed")
            .expect("no retrieval error");
        assert!(resumed.process_records_input().records().is_some());
        publisher.shutdown().await;
    }
}
