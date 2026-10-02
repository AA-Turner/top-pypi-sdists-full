//! Port of `software.amazon.kinesis.lifecycle.ShardConsumer`.
//!
//! # Concurrency model (tokio actor, see PORTING.md / the lifecycle arch-map)
//!
//! Java uses `CompletableFuture.supplyAsync(executorService)` per state step +
//! `synchronized(this)` (state mutation & task execution) + a **separate**
//! `shutdownLock` object (shutdownReason/notification). The Rust port:
//!
//! * **State** (`current_state`, `task_outcome`,
//!   `shard_end_process_records_input`) lives in a
//!   [`tokio::sync::Mutex<StateInner>`] — the `synchronized(this)` domain. A
//!   task executes while holding this lock (Java holds the monitor across
//!   `task.call()`), which serializes the data path (`handle_input`) with the
//!   lifecycle steps — the "no two tasks in flight per consumer" invariant.
//! * **`execute_lifecycle` never blocks on the state lock.** Like Java's
//!   scheduler thread (unsynchronized `executeLifecycle` + the
//!   `stateChangeFuture.isDone()` guard + `supplyAsync(executorService)`), it
//!   *spawns* the init/shutdown step as a tokio task and tracks the
//!   `JoinHandle` (`lifecycle_future`); while the step (or a data task holding
//!   the state lock) runs, subsequent calls return immediately. One stuck
//!   record processor therefore never stalls the Scheduler's dispatch loop.
//! * **Shutdown** (`shutdown_reason`, `shutdown_notification`) lives in a
//!   **separate** [`tokio::sync::Mutex<ShutdownInner>`] — the `shutdownLock`. The
//!   Java lock ordering (`this` before `shutdownLock`) is preserved as sequential
//!   awaits: `update_state` (holds the state lock) then locks the shutdown mutex
//!   inside `handle_shutdown_transition`.
//! * **Volatile fields** → read without the state lock, exactly the fields Java
//!   reads without the monitor: `task_dispatched_at`, `task_is_running`
//!   (atomics), `needs_initialization` (atomic; Java: a scheduler-thread-only
//!   plain field), `current_task_type` (brief `std::sync::Mutex`; Java: the
//!   `currentTask` plain field read by `logLongRunningTask`), and a
//!   `state_snapshot` mirror of `current_state` (brief `std::sync::Mutex`;
//!   Java reads `currentState` racily — see its "we don't do much
//!   coordination/synchronization" comment). `is_shutdown()` is sync and reads
//!   the snapshot, so the Scheduler loop never parks on a busy consumer.
//!
//! Tasks are **async** (7a `ConsumerTask::call().await`); the state machine
//! awaits them. `ConsumerState` is a closed enum (see `consumer_state.rs`).

use std::sync::atomic::{AtomicBool, AtomicI64, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};

use tokio::sync::Mutex;

use crate::leases::ShardInfo;
use crate::lifecycle::consumer_state::{ConsumerState, ShardConsumerState};
use crate::lifecycle::events::{ProcessRecordsInput, TaskExecutionListenerInput};
use crate::lifecycle::shard_consumer_subscriber::{InputHandler, ShardConsumerSubscriber};
use crate::lifecycle::{
    ConsumerTaskFactory, ShardConsumerArgument, ShutdownNotification, ShutdownReason,
    TaskExecutionListener, TaskOutcome, TaskResult, TaskType,
};
use crate::retrieval::RecordsPublisher;

/// The maximum time (ms) permitted between a request and its response before the
/// subscription is considered stalled. Port of
/// `ShardConsumer.MAX_TIME_BETWEEN_REQUEST_RESPONSE`.
pub const MAX_TIME_BETWEEN_REQUEST_RESPONSE: i64 = 60 * 1000;

/// The `synchronized(this)` state domain.
struct StateInner {
    current_state: ConsumerState,
    task_outcome: Option<TaskOutcome>,
    /// The `ProcessRecordsInput` captured at shard-end (needed by `ShutdownTask`
    /// for `childShards`).
    shard_end_process_records_input: Option<ProcessRecordsInput>,
}

/// The `shutdownLock` domain.
struct ShutdownInner {
    shutdown_reason: Option<ShutdownReason>,
    shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
}

/// Consumes data records of one shard, driving the [`ConsumerState`] state
/// machine and the [`ShardConsumerSubscriber`]. Port of
/// `software.amazon.kinesis.lifecycle.ShardConsumer`.
pub struct ShardConsumer {
    records_publisher: Arc<dyn RecordsPublisher>,
    shard_info: ShardInfo,
    shard_consumer_argument: ShardConsumerArgument,
    log_warning_for_task_after_millis: Option<i64>,
    buffer_size: i32,
    task_execution_listener: Arc<dyn TaskExecutionListener>,
    stream_identifier: String,
    task_factory: Arc<dyn ConsumerTaskFactory>,

    state: Mutex<StateInner>,
    shutdown: Mutex<ShutdownInner>,

    /// The in-flight lifecycle step, if any (Java `stateChangeFuture`). Only
    /// `execute_lifecycle` takes this lock, and never holds it across a task
    /// execution — the step itself runs on a spawned tokio task.
    lifecycle_future: Mutex<Option<tokio::task::JoinHandle<bool>>>,

    // volatile fields (read without the state lock — see the module doc)
    task_dispatched_at_nanos: AtomicI64,
    task_is_running: AtomicBool,
    /// Java `needsInitialization` (a plain scheduler-thread field).
    needs_initialization: AtomicBool,
    /// Mirror of `StateInner::current_state` for lock-free-in-practice reads
    /// (Java reads `currentState` without the monitor). Held only for a copy.
    state_snapshot: std::sync::Mutex<ConsumerState>,
    /// The type of the last dispatched task (Java `currentTask.taskType()`,
    /// read by `logLongRunningTask` without the monitor).
    current_task_type: std::sync::Mutex<Option<TaskType>>,

    subscriber: Mutex<Option<Arc<ShardConsumerSubscriber>>>,
    read_timeouts_to_ignore_before_warning: i32,

    /// A late-bound self-reference so the subscriber's `handle_input` can call
    /// back into this consumer. Set once via [`ShardConsumer::install`].
    self_weak: Mutex<Option<std::sync::Weak<ShardConsumer>>>,
}

impl ShardConsumer {
    /// Construct a shard consumer. Mirrors the Java 10-arg constructor (minus
    /// `executorService` — tokio tasks). `consumer_state = None` defaults to
    /// [`ConsumerState::initial_state`].
    ///
    /// Returns an `Arc<Self>` and installs the self-reference the subscriber needs
    /// (Java constructs its `ShardConsumerSubscriber` internally). The constructor
    /// side effect (if `shardInfo.isCompleted()` → `markForShutdown(SHARD_END)`)
    /// is applied.
    #[allow(clippy::too_many_arguments)]
    pub async fn new(
        records_publisher: Arc<dyn RecordsPublisher>,
        shard_info: ShardInfo,
        log_warning_for_task_after_millis: Option<i64>,
        shard_consumer_argument: ShardConsumerArgument,
        consumer_state: Option<ConsumerState>,
        buffer_size: i32,
        task_execution_listener: Arc<dyn TaskExecutionListener>,
        read_timeouts_to_ignore_before_warning: i32,
        task_factory: Arc<dyn ConsumerTaskFactory>,
    ) -> Arc<Self> {
        let stream_identifier = shard_info
            .stream_identifier_ser_opt()
            .map(str::to_string)
            .unwrap_or_else(|| "single_stream_mode".to_string());
        let completed = shard_info.is_completed();

        let initial_state = consumer_state.unwrap_or_else(ConsumerState::initial_state);
        let consumer = Arc::new(Self {
            records_publisher,
            shard_info,
            shard_consumer_argument,
            log_warning_for_task_after_millis,
            buffer_size,
            task_execution_listener,
            stream_identifier,
            task_factory,
            state: Mutex::new(StateInner {
                current_state: initial_state,
                task_outcome: None,
                shard_end_process_records_input: None,
            }),
            shutdown: Mutex::new(ShutdownInner {
                shutdown_reason: None,
                shutdown_notification: None,
            }),
            lifecycle_future: Mutex::new(None),
            task_dispatched_at_nanos: AtomicI64::new(-1),
            task_is_running: AtomicBool::new(false),
            needs_initialization: AtomicBool::new(true),
            state_snapshot: std::sync::Mutex::new(initial_state),
            current_task_type: std::sync::Mutex::new(None),
            subscriber: Mutex::new(None),
            read_timeouts_to_ignore_before_warning,
            self_weak: Mutex::new(None),
        });

        // Install the self-reference + build the subscriber (Java does this in the
        // constructor). The subscriber holds a `dyn InputHandler` = this consumer.
        *consumer.self_weak.lock().await = Some(Arc::downgrade(&consumer));
        let subscriber = Arc::new(ShardConsumerSubscriber::new(
            consumer.records_publisher.clone(),
            consumer.buffer_size,
            Arc::clone(&consumer) as Arc<dyn InputHandler>,
            consumer.read_timeouts_to_ignore_before_warning,
            consumer.shard_info.lease_key(),
        ));
        *consumer.subscriber.lock().await = Some(subscriber);

        if completed {
            consumer.mark_for_shutdown(ShutdownReason::ShardEnd).await;
        }

        consumer
    }

    // ---- package-scope fluent getters (Java `@Getter(AccessLevel.PACKAGE)`) ----

    /// The shard being consumed.
    pub fn shard_info(&self) -> &ShardInfo {
        &self.shard_info
    }
    /// The records publisher.
    pub fn records_publisher(&self) -> &Arc<dyn RecordsPublisher> {
        &self.records_publisher
    }
    /// The stream identifier (or `"single_stream_mode"`).
    pub fn stream_identifier(&self) -> &str {
        &self.stream_identifier
    }
    /// The DI argument bag.
    pub fn shard_consumer_argument(&self) -> &ShardConsumerArgument {
        &self.shard_consumer_argument
    }
    /// The buffer size.
    pub fn buffer_size(&self) -> i32 {
        self.buffer_size
    }
    /// The long-running-task warning threshold (ms).
    pub fn log_warning_for_task_after_millis(&self) -> Option<i64> {
        self.log_warning_for_task_after_millis
    }

    // ---- the main driver ----

    /// The main state-machine driver, invoked repeatedly by the Scheduler. Port
    /// of `executeLifecycle()`.
    ///
    /// **Never blocks on the state lock.** Mirrors Java's scheduler-thread
    /// behavior: an in-flight step (`lifecycle_future`, the `stateChangeFuture`
    /// analogue) makes this a no-op (`!stateChangeFuture.isDone()` → return);
    /// otherwise the next init/shutdown step is *spawned* (Java
    /// `supplyAsync(executorService)`) and awaited by a later call. The spawned
    /// step serializes with the data path on the state lock, exactly as Java's
    /// `synchronized executeTask` serializes with `synchronized handleInput`.
    pub async fn execute_lifecycle(self: &Arc<Self>) {
        if self.is_shutdown() {
            return;
        }

        {
            let mut fut = self.lifecycle_future.lock().await;
            if let Some(handle) = fut.as_ref() {
                if !handle.is_finished() {
                    // Java: stateChangeFuture != null && !isDone() → return.
                    return;
                }
            }

            // The `try` block in Java. We don't have InterruptedException; a
            // RejectedExecution equivalent can't occur (no executor).
            if self.is_shutdown_requested().await {
                let this = Arc::clone(self);
                *fut = Some(tokio::spawn(async move { this.shutdown_complete().await }));
            } else if self.needs_initialization.load(Ordering::SeqCst) {
                if let Some(handle) = fut.take() {
                    // The handle is finished (guard above), so this await is
                    // immediate — Java's `stateChangeFuture.get()`.
                    let init_done = match handle.await {
                        Ok(done) => done,
                        Err(join_error) => {
                            // A panicked step (Java: ExecutionException →
                            // RuntimeException). Log and keep driving; the next
                            // step re-runs from the recorded state.
                            tracing::error!(
                                "{} : lifecycle step panicked: {join_error}",
                                self.stream_identifier
                            );
                            false
                        }
                    };
                    if init_done {
                        // Java: subscribe(), then needsInitialization = false.
                        self.subscribe().await;
                        self.needs_initialization.store(false, Ordering::SeqCst);
                    }
                }
                let this = Arc::clone(self);
                *fut = Some(tokio::spawn(
                    async move { this.initialize_complete().await },
                ));
            }
        }

        // healthCheck only while PROCESSING (snapshot read — Java reads
        // `currentState` without the monitor here).
        if self.current_state_snapshot().state() == ShardConsumerState::Processing {
            // A returned failure is observed (logged); fatal Errors have no Rust
            // analogue (we don't `panic!` on a health-check failure — see NOTE).
            let _ = self.health_check().await;
        }
    }

    /// Health check: long-running/no-data logging + subscriber restart. Port of
    /// `healthCheck()`. Returns the surfaced failure, if any.
    pub async fn health_check(self: &Arc<Self>) -> Option<crate::exceptions::BoxError> {
        self.log_no_data_retrieved_after_time().await;
        self.log_long_running_task().await;

        let subscriber = self.subscriber.lock().await.clone()?;
        if let Some(failure) = subscriber.health_check(MAX_TIME_BETWEEN_REQUEST_RESPONSE) {
            return Some(failure);
        }
        if let Some(dispatch_failure) = subscriber.get_and_reset_dispatch_failure() {
            tracing::warn!(
                "{} : Exception occurred while dispatching incoming data. The incoming data has been skipped: {}",
                self.stream_identifier,
                dispatch_failure
            );
            return Some(dispatch_failure);
        }
        None
    }

    /// The elapsed time of the currently-running task, if one is running. Port of
    /// `taskRunningTime()`. Package-visible in Java (exercised by
    /// `ShardConsumerTest.testLongRunningTasks`).
    pub(crate) fn task_running_time(&self) -> Option<Duration> {
        let dispatched = self.task_dispatched_at_nanos.load(Ordering::SeqCst);
        if dispatched >= 0 && self.task_is_running.load(Ordering::SeqCst) {
            let elapsed_nanos = monotonic_now_nanos().saturating_sub(dispatched);
            Some(Duration::from_nanos(elapsed_nanos.max(0) as u64))
        } else {
            None
        }
    }

    /// The monotonic timestamp (nanos since process start) at which the current
    /// task was dispatched, or `None` if no task has been dispatched. Port of the
    /// package getter `taskDispatchedAt()` (used by `testLongRunningTasks` to
    /// assert consecutive tasks get distinct dispatch times).
    #[cfg(test)]
    pub(crate) fn task_dispatched_at(&self) -> Option<i64> {
        let dispatched = self.task_dispatched_at_nanos.load(Ordering::SeqCst);
        if dispatched >= 0 {
            Some(dispatched)
        } else {
            None
        }
    }

    async fn log_no_data_retrieved_after_time(&self) {
        let Some(threshold) = self.log_warning_for_task_after_millis else {
            return;
        };
        let subscriber = self.subscriber.lock().await.clone();
        if let Some(subscriber) = subscriber {
            if let Some(last) = subscriber.last_data_arrival() {
                let since = Instant::now().duration_since(last);
                if since.as_millis() as i64 > threshold {
                    tracing::warn!(
                        "{} : Last time data arrived: {:?} ({:?})",
                        self.stream_identifier,
                        last,
                        since
                    );
                }
            }
        }
    }

    async fn log_long_running_task(&self) {
        if let Some(taken) = self.task_running_time() {
            if let Some(threshold) = self.log_warning_for_task_after_millis {
                if taken.as_millis() as i64 > threshold {
                    // Read without the state lock (Java: the volatile-ish
                    // `currentTask` field) — this fires exactly while a task is
                    // stuck holding the state lock.
                    let task_type = *self.current_task_type.lock().unwrap();
                    tracing::warn!(
                        "{} : Previous {:?} task still pending for shard {} since {:?} ago.",
                        self.stream_identifier,
                        task_type,
                        self.shard_info.shard_id(),
                        taken
                    );
                }
            }
        }
    }

    /// Start the subscriber's subscriptions. Port of `subscribe()`.
    pub async fn subscribe(self: &Arc<Self>) {
        let subscriber = self.subscriber.lock().await.clone();
        if let Some(subscriber) = subscriber {
            subscriber.start_subscriptions();
        }
    }

    /// Advance initialization. Port of `initializeComplete()`.
    ///
    /// Returns `true` once initialization is complete (state is PROCESSING or was
    /// already past init); `false` if another init step ran. Runs the task inline
    /// (Java `supplyAsync`).
    pub async fn initialize_complete(self: &Arc<Self>) -> bool {
        if !self.needs_initialization.load(Ordering::SeqCst) {
            // Already complete: data-driven from here (publisher → handleInput).
            return true;
        }
        let mut st = self.state.lock().await;
        if let Some(outcome) = st.task_outcome {
            self.update_state_locked(&mut st, outcome).await;
        }
        if st.current_state.state() == ShardConsumerState::Processing {
            return true;
        }
        // supplyAsync body: abort if shutdown requested before/after the task.
        if self.is_shutdown_requested().await {
            // Java throws IllegalStateException; the driver would convert the
            // future's ExecutionException to a RuntimeException. Here we simply
            // stop this init step (the next tick observes the shutdown request and
            // drives shutdownComplete).
            return false;
        }
        self.execute_task_locked(&mut st, None).await;
        // returns false: the caller must not subscribe yet.
        false
    }

    /// Complete a shutdown step. Port of `shutdownComplete()`.
    ///
    /// Returns `true` once the terminal state is reached. Runs the task inline.
    pub async fn shutdown_complete(self: &Arc<Self>) -> bool {
        let mut st = self.state.lock().await;
        if let Some(outcome) = st.task_outcome {
            self.update_state_locked(&mut st, outcome).await;
        } else {
            // Shutdown requested before any task ran (e.g. lease lost while
            // WAITING_ON_PARENT_SHARDS). Force a successful outcome to proceed.
            self.update_state_locked(&mut st, TaskOutcome::Successful)
                .await;
        }
        if st.current_state.is_terminal() {
            return true;
        }
        let shard_end_input = st.shard_end_process_records_input.clone();
        self.execute_task_locked(&mut st, shard_end_input).await;

        // If shutting down as part of a graceful (worker) shutdown, notify.
        let in_shutting_down = st.current_state.state() == ShardConsumerState::ShuttingDown;
        let outcome_successful = st.task_outcome == Some(TaskOutcome::Successful);
        if in_shutting_down && outcome_successful {
            let notification = self.shutdown.lock().await.shutdown_notification.clone();
            if let Some(notification) = notification {
                notification.shutdown_complete();
            }
        }
        false
    }

    /// Execute the current state's task. Port of `executeTask(input)` (assumes the
    /// state lock `st` is held — the `synchronized(this)` domain).
    async fn execute_task_locked(
        self: &Arc<Self>,
        st: &mut StateInner,
        input: Option<ProcessRecordsInput>,
    ) {
        let task_type = st.current_state.task_type();
        *self.current_task_type.lock().unwrap() = Some(task_type);

        let mut listener_input = TaskExecutionListenerInput::builder()
            .shard_info(self.shard_info.clone())
            .task_type(task_type)
            .build();
        self.task_execution_listener
            .before_task_execution(&listener_input);

        let reason = self.shutdown.lock().await.shutdown_reason;
        let notification = self.shutdown.lock().await.shutdown_notification.clone();
        let task = st.current_state.create_task(
            &self.shard_consumer_argument,
            input,
            self.task_factory.as_ref(),
            reason,
            notification,
        );

        if let Some(task) = task {
            self.task_dispatched_at_nanos
                .store(monotonic_now_nanos(), Ordering::SeqCst);
            self.task_is_running.store(true, Ordering::SeqCst);
            let result = task.call().await;
            self.task_is_running.store(false, Ordering::SeqCst);
            let outcome = self.result_to_outcome(result);
            st.task_outcome = Some(outcome);
            listener_input = TaskExecutionListenerInput::builder()
                .shard_info(self.shard_info.clone())
                .task_type(task_type)
                .task_outcome(outcome)
                .build();
        }
        self.task_execution_listener
            .after_task_execution(&listener_input);
    }

    fn result_to_outcome(&self, result: TaskResult) -> TaskOutcome {
        if result.exception().is_none() {
            if result.is_shard_end_reached() {
                TaskOutcome::EndOfShard
            } else {
                TaskOutcome::Successful
            }
        } else {
            if let Some(e) = result.exception() {
                tracing::debug!(
                    "{} : Caught exception running task: {}",
                    self.stream_identifier,
                    e
                );
            }
            TaskOutcome::Failure
        }
    }

    /// Compute and apply the next state. Port of `updateState(outcome)` (assumes
    /// the state lock `st` is held).
    async fn update_state_locked(self: &Arc<Self>, st: &mut StateInner, outcome: TaskOutcome) {
        let mut next_state = st.current_state;
        match outcome {
            TaskOutcome::Successful => next_state = st.current_state.success_transition(),
            TaskOutcome::EndOfShard => {
                self.mark_for_shutdown(ShutdownReason::ShardEnd).await;
                // next_state stays; handleShutdownTransition below will override.
            }
            TaskOutcome::Failure => next_state = st.current_state.failure_transition(),
        }
        next_state = self
            .handle_shutdown_transition(st.current_state, outcome, next_state)
            .await;
        st.current_state = next_state;
        *self.state_snapshot.lock().unwrap() = next_state;
    }

    /// Port of `handleShutdownTransition(outcome, nextState)`: a pending shutdown
    /// request takes priority over a success transition (but NOT over a FAILURE).
    /// Locks the `shutdownLock` (after the state lock — preserving Java's order).
    async fn handle_shutdown_transition(
        &self,
        current_state: ConsumerState,
        outcome: TaskOutcome,
        next_state: ConsumerState,
    ) -> ConsumerState {
        let sd = self.shutdown.lock().await;
        match sd.shutdown_reason {
            Some(reason) if outcome != TaskOutcome::Failure => {
                current_state.shutdown_transition(reason)
            }
            _ => next_state,
        }
    }

    /// Record a shutdown reason (respecting precedence). Port of
    /// `markForShutdown(reason)` (locks the `shutdownLock`).
    pub async fn mark_for_shutdown(&self, reason: ShutdownReason) {
        let mut sd = self.shutdown.lock().await;
        match sd.shutdown_reason {
            None => sd.shutdown_reason = Some(reason),
            Some(existing) if existing.can_transition_to(reason) => {
                sd.shutdown_reason = Some(reason)
            }
            _ => {}
        }
    }

    /// Request a graceful shutdown (worker-initiated). Port of
    /// `gracefulShutdown(notification)`.
    pub async fn graceful_shutdown(
        self: &Arc<Self>,
        shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
    ) {
        let subscriber = self.subscriber.lock().await.clone();
        if let Some(subscriber) = subscriber {
            subscriber.cancel();
        }
        if let Some(notification) = shutdown_notification {
            // Only set if non-null (never clears a previously set notification).
            self.shutdown.lock().await.shutdown_notification = Some(notification);
        }
        self.mark_for_shutdown(ShutdownReason::Requested).await;
    }

    /// Shut this consumer down because the lease was lost. Port of `leaseLost()`.
    /// Returns whether shutdown is already complete.
    pub async fn lease_lost(self: &Arc<Self>) -> bool {
        let subscriber = self.subscriber.lock().await.clone();
        if let Some(subscriber) = subscriber {
            subscriber.cancel();
        }
        self.mark_for_shutdown(ShutdownReason::LeaseLost).await;
        self.is_shutdown()
    }

    /// Whether this consumer has fully shut down (terminal state). Port of
    /// `isShutdown()`.
    ///
    /// Sync + lock-free-in-practice (a snapshot read): Java reads `currentState`
    /// without the monitor, so the Scheduler loop never parks on a consumer
    /// whose state lock is held by a running task.
    pub fn is_shutdown(&self) -> bool {
        self.current_state_snapshot().is_terminal()
    }

    /// The current state, from the racy snapshot mirror (the Java plain-field
    /// read). Authoritative state lives under the state lock.
    fn current_state_snapshot(&self) -> ConsumerState {
        *self.state_snapshot.lock().unwrap()
    }

    /// Whether a shutdown has been requested. Port of `isShutdownRequested()`
    /// (locks the `shutdownLock`).
    pub async fn is_shutdown_requested(&self) -> bool {
        self.shutdown.lock().await.shutdown_reason.is_some()
    }

    /// The recorded shutdown reason, if any. Port of the `shutdownReason()` getter.
    pub async fn shutdown_reason(&self) -> Option<ShutdownReason> {
        self.shutdown.lock().await.shutdown_reason
    }

    /// The current state (for testing / diagnostics).
    pub async fn current_state(&self) -> ConsumerState {
        self.state.lock().await.current_state
    }
}

/// Implement the subscriber's [`InputHandler`] — the `handleInput` callback the
/// subscription loop makes. Port of `synchronized void handleInput(input, subscription)`.
///
/// The subscription-cancel decision is returned (`true` = cancel & stop the loop),
/// preserving Java's `subscription.cancel()` on shutdown-requested / end-of-shard.
impl InputHandler for ShardConsumer {
    fn handle_input(&self, input: ProcessRecordsInput) -> bool {
        // The subscription loop runs on the tokio runtime; `handle_input` is sync
        // (the subscriber's `dyn InputHandler`), so we hop onto a blocking context
        // to run the async state step. This mirrors Java's synchronous
        // `handleInput` running on the RxJava callback thread. The flavor-aware
        // bridge keeps this from panicking on a current-thread runtime.
        let this = match self.self_weak.try_lock() {
            Ok(guard) => guard.as_ref().and_then(|w| w.upgrade()),
            Err(_) => None,
        };
        let Some(this) = this else {
            return true;
        };
        crate::utils::sync_bridge::run_sync_on(
            tokio::runtime::Handle::current(),
            this.handle_input_async(input),
        )
    }
}

impl ShardConsumer {
    /// Async body of [`InputHandler::handle_input`].
    async fn handle_input_async(self: &Arc<Self>, input: ProcessRecordsInput) -> bool {
        if self.is_shutdown_requested().await {
            // Drop in-flight data once a shutdown has been requested; cancel.
            return true;
        }
        let mut st = self.state.lock().await;
        // processData(input) → executeTask(input).
        self.execute_task_locked(&mut st, Some(input.clone())).await;
        if st.task_outcome == Some(TaskOutcome::EndOfShard) {
            drop(st);
            self.mark_for_shutdown(ShutdownReason::ShardEnd).await;
            let mut st = self.state.lock().await;
            st.shard_end_process_records_input = Some(input);
            return true; // cancel the subscription
        }
        // With the channel model, demand is already re-requested by the loop
        // (matching onNext's finally-block request(1)); Java's extra conditional
        // request(1) here (bufferSize != 0) is subsumed by the loop's request.
        false
    }
}

/// Monotonic "now" in nanoseconds — the process-wide `System.nanoTime()` clock
/// (shared epoch with every other component's nano stamps).
fn monotonic_now_nanos() -> i64 {
    crate::utils::monotonic_clock::monotonic_nanos()
}

#[cfg(test)]
mod tests {
    include!("shard_consumer_tests.rs");
}
