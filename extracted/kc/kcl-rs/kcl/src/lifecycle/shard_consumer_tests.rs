// Behavioral tests for `ShardConsumer` (included from `shard_consumer.rs`).
//
// Java's `ShardConsumerTest` mocks `ConsumerState`/`ConsumerTask` (Mockito) and
// drives an RxJava barrier harness. In the Rust port `ConsumerState` is a closed
// enum (not mockable) and the subscriber is channel-based, so those mock-of-state
// and reflection/barrier tests are not portable (see WAVE-PLAN TEST-PARITY GAPS).
// Instead we drive the *real* state machine with a controllable
// `ConsumerTaskFactory` (a trait) whose tasks return canned `TaskResult`s, and
// assert the observable state transitions + listener callbacks — the behavioral
// core of `simpleTest` / `testDataArrivesAfterProcessing2` /
// `testSuccessfulConsumerStateTransition`.

use super::*;
use crate::checkpoint::in_memory_checkpointer::InMemoryCheckpointer;
use crate::checkpoint::ShardRecordProcessorCheckpointer;
use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended, StreamIdentifier};
use crate::leases::{
    HierarchicalShardSyncer, LeaseCleanupManager, MockLeaseCoordinator, ShardInfo,
};
use crate::lifecycle::events::ProcessRecordsInput;
use crate::lifecycle::test_support::RecordingRecordsPublisher;
use crate::lifecycle::events::TaskExecutionListenerInput;
use crate::lifecycle::{
    ConsumerTask, ConsumerTaskFactory, NoOpTaskExecutionListener, TaskExecutionListener, TaskResult,
    TaskType,
};
use crate::metrics::NullMetricsFactory;
use crate::processor::{Checkpointer, MockShardRecordProcessor, ShardRecordProcessor};
use crate::retrieval::AggregatorUtil;
use aws_sdk_kinesis::types::ChildShard;
use async_trait::async_trait;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex as StdMutex};

const SHARD_ID: &str = "shardId-000000000000";

fn shard_info() -> ShardInfo {
    ShardInfo::new(
        SHARD_ID,
        Some("token".to_string()),
        Vec::<String>::new(),
        None,
        Some(StreamIdentifier::single_stream_instance("TestStream").serialize()),
    )
}

/// A task that returns a canned outcome, recording each `call()`.
struct CannedTask {
    task_type: TaskType,
    result: StdMutex<Option<TaskResult>>,
    calls: Arc<AtomicUsize>,
    /// If set, subsequent calls (after the first canned result is consumed)
    /// return a fresh success/shard-end/failure per this closure.
    default_shard_end: bool,
}

#[async_trait]
impl ConsumerTask for CannedTask {
    async fn call(&self) -> TaskResult {
        self.calls.fetch_add(1, Ordering::SeqCst);
        if let Some(r) = self.result.lock().unwrap().take() {
            r
        } else if self.default_shard_end {
            TaskResult::shard_end(true)
        } else {
            TaskResult::shard_end(false)
        }
    }
    fn task_type(&self) -> TaskType {
        self.task_type
    }
    fn task_name(&self) -> &'static str {
        "CannedTask"
    }
}

/// A controllable factory: hands out canned tasks per task type and counts how
/// many of each it created.
#[derive(Default)]
struct ControllableFactory {
    block_calls: Arc<AtomicUsize>,
    init_calls: Arc<AtomicUsize>,
    process_calls: Arc<AtomicUsize>,
    shutdown_calls: Arc<AtomicUsize>,
    shutdown_notification_calls: Arc<AtomicUsize>,
    /// Task-call counters per type (call() invocations).
    block_task_calls: Arc<AtomicUsize>,
    init_task_calls: Arc<AtomicUsize>,
    process_task_calls: Arc<AtomicUsize>,
    shutdown_task_calls: Arc<AtomicUsize>,
    /// Whether the process task should report shard-end on its (n-th) call.
    process_shard_end: Arc<AtomicUsize>, // >0 → the process task reports shard end
}

impl ConsumerTaskFactory for ControllableFactory {
    fn create_shutdown_task(
        &self,
        _argument: &ShardConsumerArgument,
        _reason: ShutdownReason,
        _child_shards: Option<Vec<ChildShard>>,
    ) -> Box<dyn ConsumerTask> {
        self.shutdown_calls.fetch_add(1, Ordering::SeqCst);
        Box::new(CannedTask {
            task_type: TaskType::Shutdown,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: self.shutdown_task_calls.clone(),
            default_shard_end: false,
        })
    }
    fn create_process_task(
        &self,
        _argument: &ShardConsumerArgument,
        _input: ProcessRecordsInput,
    ) -> Box<dyn ConsumerTask> {
        self.process_calls.fetch_add(1, Ordering::SeqCst);
        let shard_end = self.process_shard_end.load(Ordering::SeqCst) > 0;
        Box::new(CannedTask {
            task_type: TaskType::Process,
            result: StdMutex::new(Some(TaskResult::shard_end(shard_end))),
            calls: self.process_task_calls.clone(),
            default_shard_end: shard_end,
        })
    }
    fn create_initialize_task(&self, _argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        self.init_calls.fetch_add(1, Ordering::SeqCst);
        Box::new(CannedTask {
            task_type: TaskType::Initialize,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: self.init_task_calls.clone(),
            default_shard_end: false,
        })
    }
    fn create_block_on_parent_task(&self, _argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        self.block_calls.fetch_add(1, Ordering::SeqCst);
        Box::new(CannedTask {
            task_type: TaskType::BlockOnParentShards,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: self.block_task_calls.clone(),
            default_shard_end: false,
        })
    }
    fn create_shutdown_notification_task(
        &self,
        _argument: &ShardConsumerArgument,
        _shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
    ) -> Box<dyn ConsumerTask> {
        self.shutdown_notification_calls.fetch_add(1, Ordering::SeqCst);
        Box::new(CannedTask {
            task_type: TaskType::ShutdownNotification,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: self.shutdown_task_calls.clone(),
            default_shard_end: false,
        })
    }
}

/// A recording listener capturing before/after inputs.
#[derive(Default)]
struct RecordingListener {
    before: Arc<StdMutex<Vec<TaskExecutionListenerInput>>>,
    after: Arc<StdMutex<Vec<TaskExecutionListenerInput>>>,
}
impl TaskExecutionListener for RecordingListener {
    fn before_task_execution(&self, input: &TaskExecutionListenerInput) {
        self.before.lock().unwrap().push(input.clone());
    }
    fn after_task_execution(&self, input: &TaskExecutionListenerInput) {
        self.after.lock().unwrap().push(input.clone());
    }
}

fn build_argument(shard_info: ShardInfo) -> ShardConsumerArgument {
    let store: Arc<dyn Checkpointer + Send + Sync> = Arc::new(InMemoryCheckpointer::new());
    let checkpointer = ShardRecordProcessorCheckpointer::new(shard_info.clone(), store.clone());

    let mut coord = MockLeaseCoordinator::new();
    coord
        .expect_lease_stats_recorder()
        .returning(|| Arc::new(crate::leases::LeaseStatsRecorder::new(60_000, Arc::new(|| 0i64) as crate::leases::lease_stats_recorder::TimeProvider)));
    coord.expect_get_currently_held_lease().returning(|_| None);
    coord.expect_worker_identifier().returning(|| "worker".to_string());
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

    ShardConsumerArgument::new(
        shard_info,
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
    )
}

async fn build_consumer(
    factory: Arc<ControllableFactory>,
    listener: Arc<dyn TaskExecutionListener>,
    completed: bool,
) -> Arc<ShardConsumer> {
    let info = if completed {
        // A shard whose checkpoint is at SHARD_END is "completed".
        ShardInfo::new(
            SHARD_ID,
            Some("token".to_string()),
            Vec::<String>::new(),
            Some(crate::retrieval::kpl::ExtendedSequenceNumber::shard_end()),
            Some(StreamIdentifier::single_stream_instance("TestStream").serialize()),
        )
    } else {
        shard_info()
    };
    let argument = build_argument(info.clone());
    ShardConsumer::new(
        Arc::new(RecordingRecordsPublisher::new()),
        info,
        None,
        argument,
        None,
        1,
        listener,
        0,
        factory,
    )
    .await
}

/// A factory whose `InitializeTask` fails on its first creation and succeeds on
/// every one thereafter; every other task type always succeeds immediately.
/// Used to verify the state machine retries a failed `InitializeTask` instead
/// of wedging (2026-07-14 bug-fix parity test: `RecordsPublisher::start`
/// becoming fallible is exactly what can now produce this failure in
/// production, via `InitializeTask::try_call`'s `cache.start(...).await?`).
struct FailOnceInitializeFactory {
    init_calls: Arc<AtomicUsize>,
}
impl ConsumerTaskFactory for FailOnceInitializeFactory {
    fn create_shutdown_task(
        &self,
        _argument: &ShardConsumerArgument,
        _reason: ShutdownReason,
        _child_shards: Option<Vec<ChildShard>>,
    ) -> Box<dyn ConsumerTask> {
        Box::new(CannedTask {
            task_type: TaskType::Shutdown,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
    fn create_process_task(
        &self,
        _argument: &ShardConsumerArgument,
        _input: ProcessRecordsInput,
    ) -> Box<dyn ConsumerTask> {
        Box::new(CannedTask {
            task_type: TaskType::Process,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
    fn create_initialize_task(&self, _argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        let n = self.init_calls.fetch_add(1, Ordering::SeqCst);
        let result = if n == 0 {
            TaskResult::new(Some(Box::<dyn std::error::Error + Send + Sync>::from(
                "injected initialize failure (e.g. RecordsPublisher::start failed)",
            )))
        } else {
            TaskResult::shard_end(false)
        };
        Box::new(CannedTask {
            task_type: TaskType::Initialize,
            result: StdMutex::new(Some(result)),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
    fn create_block_on_parent_task(&self, _argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        Box::new(CannedTask {
            task_type: TaskType::BlockOnParentShards,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
    fn create_shutdown_notification_task(
        &self,
        _argument: &ShardConsumerArgument,
        _shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
    ) -> Box<dyn ConsumerTask> {
        Box::new(CannedTask {
            task_type: TaskType::ShutdownNotification,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
}

// ---- tests ----

#[tokio::test(flavor = "multi_thread")]
async fn state_transitions_waiting_initializing_processing() {
    let factory = Arc::new(ControllableFactory::default());
    let listener = Arc::new(NoOpTaskExecutionListener);
    let consumer = build_consumer(factory.clone(), listener, false).await;

    // Initial state.
    assert_eq!(consumer.current_state().await, ConsumerState::BlockedOnParent);

    // First init step: `taskOutcome` is null so no transition yet — it runs the
    // BlockOnParent task and records SUCCESSFUL. Java applies the recorded
    // outcome's transition only on the *next* call, so state stays BlockedOnParent.
    let done = consumer.initialize_complete().await;
    assert!(!done);
    assert_eq!(consumer.current_state().await, ConsumerState::BlockedOnParent);
    assert_eq!(factory.block_calls.load(Ordering::SeqCst), 1);

    // Second init step: applies BlockOnParent→Initializing, then runs Initialize.
    let done = consumer.initialize_complete().await;
    assert!(!done);
    assert_eq!(consumer.current_state().await, ConsumerState::Initializing);
    assert_eq!(factory.init_calls.load(Ordering::SeqCst), 1);

    // Third init step: applies Initializing→Processing; now PROCESSING → done.
    let done = consumer.initialize_complete().await;
    assert!(done);
    assert_eq!(consumer.current_state().await, ConsumerState::Processing);

    // Once PROCESSING, initialize_complete is a no-op fast path.
    let done = consumer.initialize_complete().await;
    assert!(done);
    assert_eq!(consumer.current_state().await, ConsumerState::Processing);
}

// New (2026-07-14 bug fix): a failed InitializeTask must not wedge or crash
// the consumer — `ConsumerState::failure_transition` is the identity for
// `Initializing` (Java's `ConsumerState` default, not overridden by
// `InitializingState`), so the state stays `Initializing` and the next
// `execute_lifecycle`/`initialize_complete` step re-creates and re-runs a
// fresh `InitializeTask` (mirroring Java: `updateState(FAILURE)` doesn't
// change state, and the Scheduler's driving loop simply calls
// `executeLifecycle` again on its next iteration — no special retry wiring is
// needed beyond "the state didn't move forward").
#[tokio::test(flavor = "multi_thread")]
async fn failed_initialize_task_is_retried_by_state_machine() {
    let factory = Arc::new(FailOnceInitializeFactory {
        init_calls: Arc::new(AtomicUsize::new(0)),
    });
    let consumer = build_consumer_with(Arc::new(RecordingRecordsPublisher::new()), factory.clone())
        .await;

    // Step 1: BlockOnParent runs (recorded, not yet applied) -> still BlockedOnParent.
    assert!(!consumer.initialize_complete().await);
    assert_eq!(consumer.current_state().await, ConsumerState::BlockedOnParent);

    // Step 2: BlockOnParent success applied -> Initializing; the FIRST
    // InitializeTask runs and fails.
    assert!(!consumer.initialize_complete().await);
    assert_eq!(consumer.current_state().await, ConsumerState::Initializing);
    assert_eq!(factory.init_calls.load(Ordering::SeqCst), 1);

    // Step 3: the Failure outcome is applied — `failure_transition` is the
    // identity, so the state stays Initializing — and a SECOND
    // InitializeTask is created and run (this one succeeds).
    assert!(!consumer.initialize_complete().await);
    assert_eq!(consumer.current_state().await, ConsumerState::Initializing);
    assert_eq!(
        factory.init_calls.load(Ordering::SeqCst),
        2,
        "a failed InitializeTask must be retried (re-created and re-run), not abandoned"
    );

    // Step 4: the Success outcome is applied -> Processing -> done. Only two
    // InitializeTask instances were ever created (one failure, one success) —
    // the state machine didn't spin or double-retry.
    assert!(consumer.initialize_complete().await);
    assert_eq!(consumer.current_state().await, ConsumerState::Processing);
    assert_eq!(factory.init_calls.load(Ordering::SeqCst), 2);
}

#[tokio::test(flavor = "multi_thread")]
async fn lease_lost_drives_to_shutdown_complete() {
    let factory = Arc::new(ControllableFactory::default());
    let listener = Arc::new(NoOpTaskExecutionListener);
    let consumer = build_consumer(factory.clone(), listener, false).await;

    // Drive to PROCESSING.
    while !consumer.initialize_complete().await {}
    assert_eq!(consumer.current_state().await, ConsumerState::Processing);

    // Lose the lease.
    let shutdown = consumer.lease_lost().await;
    assert!(!shutdown); // still needs a task to run
    assert!(consumer.is_shutdown_requested().await);
    assert_eq!(consumer.shutdown_reason().await, Some(ShutdownReason::LeaseLost));

    // Drive shutdown to completion.
    for _ in 0..10 {
        if consumer.shutdown_complete().await {
            break;
        }
    }
    assert!(consumer.is_shutdown());
    assert_eq!(consumer.current_state().await, ConsumerState::ShutdownComplete);
    // A shutdown task ran.
    assert_eq!(factory.shutdown_calls.load(Ordering::SeqCst), 1);
}

#[tokio::test(flavor = "multi_thread")]
async fn completed_shard_marks_shard_end_at_construction() {
    let factory = Arc::new(ControllableFactory::default());
    let listener = Arc::new(NoOpTaskExecutionListener);
    let consumer = build_consumer(factory.clone(), listener, true).await;

    // Constructor side effect: markForShutdown(SHARD_END).
    assert!(consumer.is_shutdown_requested().await);
    assert_eq!(consumer.shutdown_reason().await, Some(ShutdownReason::ShardEnd));
}

#[tokio::test(flavor = "multi_thread")]
async fn graceful_shutdown_records_requested_and_notification() {
    let factory = Arc::new(ControllableFactory::default());
    let listener = Arc::new(NoOpTaskExecutionListener);
    let consumer = build_consumer(factory.clone(), listener, false).await;
    while !consumer.initialize_complete().await {}

    struct DummyNotification;
    impl ShutdownNotification for DummyNotification {
        fn shutdown_notification_complete(&self) {}
        fn shutdown_complete(&self) {}
    }
    consumer
        .graceful_shutdown(Some(Arc::new(DummyNotification)))
        .await;
    assert_eq!(consumer.shutdown_reason().await, Some(ShutdownReason::Requested));
    assert!(consumer.is_shutdown_requested().await);
}

#[tokio::test(flavor = "multi_thread")]
async fn listener_before_and_after_fire_with_outcome() {
    let factory = Arc::new(ControllableFactory::default());
    let listener = Arc::new(RecordingListener::default());
    let listener_dyn: Arc<dyn TaskExecutionListener> = listener.clone();
    let consumer = build_consumer(factory.clone(), listener_dyn, false).await;

    // First step: BlockOnParent.
    consumer.initialize_complete().await;
    let before = listener.before.lock().unwrap();
    let after = listener.after.lock().unwrap();
    assert_eq!(before.len(), 1);
    assert_eq!(before[0].task_type(), Some(TaskType::BlockOnParentShards));
    assert_eq!(before[0].shard_info().map(|s| s.shard_id()), Some(SHARD_ID));
    assert_eq!(after.len(), 1);
    assert_eq!(after[0].task_outcome(), Some(TaskOutcome::Successful));
}

// ---- Support for testExceptionInProcessingStopsRequests / testLongRunningTasks ----

use crate::retrieval::{
    new_subscription, BatchUniqueIdentifier, RecordsDeliveryAck, RecordsPublisher,
    RecordsPublisherSink, RecordsPublisherSubscription, RecordsRetrieved,
};
use std::time::Duration;
use tokio::sync::{Notify, Semaphore};

/// Poll `cond` until true, with a generous wall-clock deadline (robust under the
/// CPU contention of a full-suite run, unlike a bounded yield-count loop).
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

/// Take the publisher's stored sink once the subscriber has subscribed.
async fn take_deliverable_sink(publisher: &Arc<DeliverablePublisher>) -> RecordsPublisherSink {
    loop {
        if let Some(s) = publisher.sink.lock().unwrap().take() {
            return s;
        }
        tokio::time::sleep(Duration::from_millis(1)).await;
    }
}

/// A publisher whose delivery `sink` the test drives directly (stored on
/// `subscribe`). Mirrors the subscriber-test `TestPublisher` but lives here so a
/// real `ShardConsumer` (which owns the publisher + builds its own subscriber) can
/// have batches pushed through `handle_input`.
struct DeliverablePublisher {
    sink: StdMutex<Option<RecordsPublisherSink>>,
}
impl DeliverablePublisher {
    fn new() -> Self {
        Self { sink: StdMutex::new(None) }
    }
}
#[async_trait]
impl RecordsPublisher for DeliverablePublisher {
    async fn start(
        &self,
        _: crate::retrieval::kpl::ExtendedSequenceNumber,
        _: InitialPositionInStreamExtended,
    ) -> Result<(), crate::exceptions::BoxError> {
        Ok(())
    }
    async fn restart_from(&self, _: Arc<dyn RecordsRetrieved>) {}
    async fn shutdown(&self) {}
    fn last_successful_request_details(&self) -> crate::common::RequestDetails {
        crate::common::RequestDetails::empty()
    }
    async fn notify(&self, _ack: Box<dyn RecordsDeliveryAck>) {}
    fn subscribe(&self) -> RecordsPublisherSubscription {
        let (sub, sink) = new_subscription();
        *self.sink.lock().unwrap() = Some(sink);
        sub
    }
}

#[derive(Debug)]
struct SimpleBatch {
    input: ProcessRecordsInput,
    id: BatchUniqueIdentifier,
}
impl RecordsRetrieved for SimpleBatch {
    fn process_records_input(&self) -> &ProcessRecordsInput {
        &self.input
    }
    fn batch_unique_identifier(&self) -> BatchUniqueIdentifier {
        self.id.clone()
    }
}
fn simple_batch(key: &str) -> Arc<dyn RecordsRetrieved> {
    Arc::new(SimpleBatch {
        input: ProcessRecordsInput::builder().records(vec![]).build(),
        id: BatchUniqueIdentifier::new(key, "flow"),
    })
}

/// A process task that panics when called (Java: `processingTask.call()` throws).
/// The subscriber's `catch_unwind` turns this into a dispatch failure surfaced by
/// `ShardConsumer::health_check`.
struct PanicTask;
#[async_trait]
impl ConsumerTask for PanicTask {
    async fn call(&self) -> TaskResult {
        panic!("Whee");
    }
    fn task_type(&self) -> TaskType {
        TaskType::Process
    }
    fn task_name(&self) -> &'static str {
        "PanicTask"
    }
}

/// A task that signals arrival, blocks until released, then returns a canned
/// outcome. Port of the Mockito barrier answer in `testLongRunningTasks`.
struct BarrierTask {
    task_type: TaskType,
    arrived: Arc<Notify>,
    release: Arc<Semaphore>,
    shard_end: bool,
}
#[async_trait]
impl ConsumerTask for BarrierTask {
    async fn call(&self) -> TaskResult {
        self.arrived.notify_one();
        let permit = self.release.acquire().await.expect("release semaphore closed");
        permit.forget();
        TaskResult::shard_end(self.shard_end)
    }
    fn task_type(&self) -> TaskType {
        self.task_type
    }
    fn task_name(&self) -> &'static str {
        "BarrierTask"
    }
}

/// Factory whose init/process/shutdown tasks are all barrier tasks sharing one
/// arrive/release pair (so the test can step each task through arrive→observe→
/// release). The block-on-parent task runs to completion immediately (no barrier)
/// so we reach the INITIALIZING step quickly.
struct BarrierFactory {
    arrived: Arc<Notify>,
    release: Arc<Semaphore>,
}
impl ConsumerTaskFactory for BarrierFactory {
    fn create_shutdown_task(
        &self,
        _argument: &ShardConsumerArgument,
        _reason: ShutdownReason,
        _child_shards: Option<Vec<ChildShard>>,
    ) -> Box<dyn ConsumerTask> {
        Box::new(BarrierTask {
            task_type: TaskType::Shutdown,
            arrived: self.arrived.clone(),
            release: self.release.clone(),
            shard_end: false,
        })
    }
    fn create_process_task(
        &self,
        _argument: &ShardConsumerArgument,
        _input: ProcessRecordsInput,
    ) -> Box<dyn ConsumerTask> {
        Box::new(BarrierTask {
            task_type: TaskType::Process,
            arrived: self.arrived.clone(),
            release: self.release.clone(),
            shard_end: false,
        })
    }
    fn create_initialize_task(&self, _argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        Box::new(BarrierTask {
            task_type: TaskType::Initialize,
            arrived: self.arrived.clone(),
            release: self.release.clone(),
            shard_end: false,
        })
    }
    fn create_block_on_parent_task(&self, _argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        // No barrier: complete immediately so we advance to INITIALIZING.
        Box::new(CannedTask {
            task_type: TaskType::BlockOnParentShards,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
    fn create_shutdown_notification_task(
        &self,
        _argument: &ShardConsumerArgument,
        _shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
    ) -> Box<dyn ConsumerTask> {
        Box::new(BarrierTask {
            task_type: TaskType::ShutdownNotification,
            arrived: self.arrived.clone(),
            release: self.release.clone(),
            shard_end: false,
        })
    }
}

/// A factory that produces a panicking process task (else immediate success),
/// used by testExceptionInProcessingStopsRequests.
struct PanicProcessFactory;
impl ConsumerTaskFactory for PanicProcessFactory {
    fn create_shutdown_task(
        &self,
        _argument: &ShardConsumerArgument,
        _reason: ShutdownReason,
        _child_shards: Option<Vec<ChildShard>>,
    ) -> Box<dyn ConsumerTask> {
        Box::new(CannedTask {
            task_type: TaskType::Shutdown,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
    fn create_process_task(
        &self,
        _argument: &ShardConsumerArgument,
        _input: ProcessRecordsInput,
    ) -> Box<dyn ConsumerTask> {
        Box::new(PanicTask)
    }
    fn create_initialize_task(&self, _argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        Box::new(CannedTask {
            task_type: TaskType::Initialize,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
    fn create_block_on_parent_task(&self, _argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        Box::new(CannedTask {
            task_type: TaskType::BlockOnParentShards,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
    fn create_shutdown_notification_task(
        &self,
        _argument: &ShardConsumerArgument,
        _shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
    ) -> Box<dyn ConsumerTask> {
        Box::new(CannedTask {
            task_type: TaskType::ShutdownNotification,
            result: StdMutex::new(Some(TaskResult::shard_end(false))),
            calls: Arc::new(AtomicUsize::new(0)),
            default_shard_end: false,
        })
    }
}

/// Build a real `ShardConsumer` around a caller-supplied publisher + factory.
async fn build_consumer_with(
    publisher: Arc<dyn RecordsPublisher>,
    factory: Arc<dyn ConsumerTaskFactory>,
) -> Arc<ShardConsumer> {
    let info = shard_info();
    let argument = build_argument(info.clone());
    ShardConsumer::new(
        publisher,
        info,
        None, // log_warning_for_task_after_millis = None (avoids the state-lock logging paths)
        argument,
        None,
        1,
        Arc::new(NoOpTaskExecutionListener),
        0,
        factory,
    )
    .await
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn exception_in_processing_stops_requests() {
    // Port of testExceptionInProcessingStopsRequests: once the consumer is
    // PROCESSING and a delivered batch makes the process task fail, health_check
    // surfaces the failure (Rust: the panic is caught by the subscriber as a
    // dispatch failure). The subscription stops making further requests.
    let publisher = Arc::new(DeliverablePublisher::new());
    let factory = Arc::new(PanicProcessFactory);
    let consumer = build_consumer_with(publisher.clone(), factory).await;

    // Drive to PROCESSING.
    while !consumer.initialize_complete().await {}
    assert_eq!(consumer.current_state().await, ConsumerState::Processing);

    // Subscribe, then take the sink the subscriber stored.
    consumer.subscribe().await;
    let sink = take_deliverable_sink(&publisher).await;

    // The subscriber requested the first batch; deliver one, which triggers the
    // panicking process task (captured as a dispatch failure).
    let delivered = sink.deliver(simple_batch("b-0")).await;
    assert!(delivered);

    // Poll health_check (safe: log threshold is None -> no state lock) until it
    // surfaces the dispatch failure the panicking task produced.
    let mut outcome = None;
    let deadline = std::time::Instant::now() + Duration::from_secs(20);
    while std::time::Instant::now() < deadline {
        if let Some(f) = consumer.health_check().await {
            outcome = Some(f);
            break;
        }
        tokio::time::sleep(Duration::from_millis(1)).await;
    }
    assert!(outcome.is_some(), "health_check should surface the processing failure");
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn long_running_tasks_expose_running_time_and_dispatch_time() {
    // Port of testLongRunningTasks: `task_running_time()` is Some while a task is
    // executing and None once it finishes, and `task_dispatched_at()` differs
    // between consecutive tasks. We drive the barrier tasks: arrive → observe →
    // release. (The Java interleaving of healthCheck() *while a task is blocked* is
    // not reproduced — the Rust port runs tasks inline under the state lock — but
    // the timing seams the test exercises are asserted directly.)
    let arrived = Arc::new(Notify::new());
    let release = Arc::new(Semaphore::new(0));
    let publisher = Arc::new(DeliverablePublisher::new());
    let factory = Arc::new(BarrierFactory {
        arrived: arrived.clone(),
        release: release.clone(),
    });
    let consumer = build_consumer_with(publisher.clone(), factory).await;

    // Idle: no task running.
    assert!(consumer.task_running_time().is_none());

    // Step 1: BlockOnParent completes immediately, then the Initialize barrier task
    // is dispatched. Run one init step in the background so we can observe.
    let c1 = consumer.clone();
    let init1 = tokio::spawn(async move { c1.initialize_complete().await });
    // First init_complete runs BlockOnParent (no barrier) and records SUCCESSFUL.
    let done = init1.await.unwrap();
    assert!(!done);

    // Second init step applies BlockOnParent→Initializing and dispatches the
    // Initialize barrier task (which blocks). Observe running-time while blocked.
    let c2 = consumer.clone();
    let init2 = tokio::spawn(async move { c2.initialize_complete().await });
    arrived.notified().await;
    assert!(consumer.task_running_time().is_some());
    let init_dispatch = consumer.task_dispatched_at();
    assert!(init_dispatch.is_some());
    // health_check is safe here (log threshold is None, so it takes no state lock).
    let _ = consumer.health_check().await;
    release.add_permits(1); // let the Initialize task depart
    let done = init2.await.unwrap();
    assert!(!done);
    // After the task finished, running time is None.
    assert!(consumer.task_running_time().is_none());

    // Third init step: Initializing→Processing → done (no barrier task).
    while !consumer.initialize_complete().await {}
    assert_eq!(consumer.current_state().await, ConsumerState::Processing);
    assert!(consumer.task_running_time().is_none());

    // Subscribe and deliver a batch → the Process barrier task is dispatched.
    consumer.subscribe().await;
    let sink = take_deliverable_sink(&publisher).await;
    let deliver1 = sink.deliver(simple_batch("p-0")).await;
    assert!(deliver1);
    arrived.notified().await;
    let first_process_dispatch = consumer.task_dispatched_at();
    assert!(consumer.task_running_time().is_some());
    // Distinct from the initialize task's dispatch time.
    assert_ne!(first_process_dispatch, init_dispatch);
    release.add_permits(1); // let the first process task depart

    // Wait until the process task finished (running time back to None).
    assert!(wait_for(|| consumer.task_running_time().is_none()).await);

    // A second batch dispatches another process task with a distinct dispatch time.
    let deliver2 = sink.deliver(simple_batch("p-1")).await;
    assert!(deliver2);
    arrived.notified().await;
    let second_process_dispatch = consumer.task_dispatched_at();
    assert!(consumer.task_running_time().is_some());
    assert_ne!(second_process_dispatch, first_process_dispatch);
    release.add_permits(1); // let the second process task depart

    assert!(wait_for(|| consumer.task_running_time().is_none()).await);
}

/// Drive a barrier-factory consumer to PROCESSING and block a ProcessTask at
/// the barrier (holding the state lock), returning the pieces the test drives.
async fn consumer_with_stuck_process_task() -> (
    Arc<ShardConsumer>,
    Arc<Notify>,
    Arc<Semaphore>,
    Arc<DeliverablePublisher>,
) {
    let arrived = Arc::new(Notify::new());
    let release = Arc::new(Semaphore::new(0));
    let publisher = Arc::new(DeliverablePublisher::new());
    let factory = Arc::new(BarrierFactory {
        arrived: arrived.clone(),
        release: release.clone(),
    });
    let consumer = build_consumer_with(publisher.clone(), factory).await;

    // One permit lets the Initialize barrier task pass; the ProcessTask later
    // finds the semaphore empty and blocks.
    release.add_permits(1);
    while !consumer.initialize_complete().await {}
    assert_eq!(consumer.current_state().await, ConsumerState::Processing);
    // Drain the notification the Initialize task stored on the Notify, so the
    // next `notified()` really waits for the ProcessTask.
    let _ = tokio::time::timeout(Duration::from_millis(50), arrived.notified()).await;

    consumer.subscribe().await;
    let sink = take_deliverable_sink(&publisher).await;
    assert!(sink.deliver(simple_batch("stuck-0")).await);
    // The ProcessTask has started (and now holds the state lock at the barrier).
    arrived.notified().await;
    assert!(wait_for(|| consumer.task_running_time().is_some()).await);
    (consumer, arrived, release, publisher)
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn stuck_process_task_does_not_block_scheduler_loop() {
    // Pre-fix, `execute_lifecycle` (and the async `is_shutdown`) parked on the
    // state lock held by a running ProcessTask, so ONE stuck record processor
    // stalled the Scheduler's dispatch over ALL shards. Java's scheduler thread
    // never touches the monitor; assert the port matches.
    let (consumer, _arrived, release, _publisher) = consumer_with_stuck_process_task().await;

    // Sync + snapshot-backed: cannot block, and the consumer is not shut down.
    assert!(!consumer.is_shutdown());

    // The dispatch tick must complete while the ProcessTask is still stuck.
    tokio::time::timeout(Duration::from_secs(5), consumer.execute_lifecycle())
        .await
        .expect("execute_lifecycle must not park behind a stuck ProcessTask");
    assert!(
        consumer.task_running_time().is_some(),
        "the ProcessTask is still running — the tick did not wait for it"
    );

    release.add_permits(10);
    assert!(wait_for(|| consumer.task_running_time().is_none()).await);
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn shutdown_requested_during_long_task_is_handled_at_next_boundary() {
    let (consumer, _arrived, release, _publisher) = consumer_with_stuck_process_task().await;

    // Request a graceful shutdown while the ProcessTask is stuck; neither the
    // request nor the next dispatch tick may block on it.
    consumer.graceful_shutdown(None).await;
    assert!(consumer.is_shutdown_requested().await);
    tokio::time::timeout(Duration::from_secs(5), consumer.execute_lifecycle())
        .await
        .expect("execute_lifecycle must not park while requesting shutdown");
    // The shutdown step was spawned but is waiting on the task boundary.
    assert!(!consumer.is_shutdown());

    // Unblock the ProcessTask (and every subsequent barrier task): the
    // spawned step acquires the lock at the task boundary and the graceful
    // shutdown drives through SHUTDOWN_NOTIFICATION into the
    // SHUTDOWN_REQUESTED wait-state (Java parks there until the worker
    // escalates by releasing the lease).
    release.add_permits(100);
    let deadline = std::time::Instant::now() + Duration::from_secs(20);
    let mut reached_wait_state = false;
    while std::time::Instant::now() < deadline {
        consumer.execute_lifecycle().await;
        if consumer.current_state().await == ConsumerState::ShutdownNotificationCompletion {
            reached_wait_state = true;
            break;
        }
        tokio::time::sleep(Duration::from_millis(5)).await;
    }
    assert!(
        reached_wait_state,
        "the shutdown request was applied at the task boundary"
    );

    // The worker escalates (lease released) → terminal.
    consumer.lease_lost().await;
    let deadline = std::time::Instant::now() + Duration::from_secs(20);
    while !consumer.is_shutdown() && std::time::Instant::now() < deadline {
        consumer.execute_lifecycle().await;
        tokio::time::sleep(Duration::from_millis(5)).await;
    }
    assert!(consumer.is_shutdown());
    assert_eq!(consumer.current_state().await, ConsumerState::ShutdownComplete);
}

#[tokio::test(flavor = "multi_thread")]
async fn shutdown_requested_while_processing_transitions_to_shutdown_requested() {
    let factory = Arc::new(ControllableFactory::default());
    let listener = Arc::new(NoOpTaskExecutionListener);
    let consumer = build_consumer(factory.clone(), listener, false).await;
    while !consumer.initialize_complete().await {}
    assert_eq!(consumer.current_state().await, ConsumerState::Processing);

    // Request graceful shutdown while processing.
    consumer.graceful_shutdown(None).await;
    // Drive one shutdown step: PROCESSING + REQUESTED → SHUTDOWN_REQUESTED
    // (a ShutdownNotificationTask is created).
    consumer.shutdown_complete().await;
    assert_eq!(consumer.current_state().await, ConsumerState::ShutdownNotification);
    assert_eq!(factory.shutdown_notification_calls.load(Ordering::SeqCst), 1);
}
