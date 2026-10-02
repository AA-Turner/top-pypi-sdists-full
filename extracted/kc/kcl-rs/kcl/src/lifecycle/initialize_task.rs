//! Port of `software.amazon.kinesis.lifecycle.InitializeTask`.

use std::sync::{Arc, Mutex};
use std::time::Duration;

use async_trait::async_trait;

use crate::checkpoint::ShardRecordProcessorCheckpointer;
use crate::common::InitialPositionInStreamExtended;
use crate::exceptions::BoxError;
use crate::leases::ShardInfo;
use crate::lifecycle::events::InitializationInput;
use crate::lifecycle::{ConsumerTask, TaskResult, TaskType};
use crate::metrics::{self, MetricsFactory, MetricsLevel};
use crate::processor::{Checkpointer, ShardRecordProcessor};

const INITIALIZE_TASK_OPERATION: &str = "InitializeTask";
const RECORD_PROCESSOR_INITIALIZE_METRIC: &str = "RecordProcessor.initialize";

/// Task for initializing shard position and invoking the record processor's
/// `initialize()` callback.
///
/// The customer `initialize()` callback is invoked via
/// [`tokio::task::spawn_blocking`] (see [`ShardConsumerArgument`] concurrency
/// notes) — it may call the checkpointer, which bridges to async internally, so
/// it must not run on a runtime worker.
///
/// [`ShardConsumerArgument`]: crate::lifecycle::ShardConsumerArgument
pub struct InitializeTask {
    shard_info: ShardInfo,
    shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
    checkpoint: Arc<dyn Checkpointer + Send + Sync>,
    record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
    initial_position_in_stream: InitialPositionInStreamExtended,
    cache: Arc<dyn crate::retrieval::RecordsPublisher>,
    backoff_time_millis: i64,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
}

impl InitializeTask {
    /// Public in Java (`@RequiredArgsConstructor`).
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        shard_info: ShardInfo,
        shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
        checkpoint: Arc<dyn Checkpointer + Send + Sync>,
        record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
        initial_position_in_stream: InitialPositionInStreamExtended,
        cache: Arc<dyn crate::retrieval::RecordsPublisher>,
        backoff_time_millis: i64,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Self {
        Self {
            shard_info,
            shard_record_processor,
            checkpoint,
            record_processor_checkpointer,
            initial_position_in_stream,
            cache,
            backoff_time_millis,
            metrics_factory,
        }
    }

    /// The framework-side initialization work, factored out so the single Java
    /// `try` block maps to one fallible async function.
    async fn try_call(&self) -> Result<(), BoxError> {
        let lease_key = self.shard_info.lease_key();
        // The sync `Checkpointer` store bridges to async internally (the
        // DynamoDB-backed impl uses `Handle::block_on`), so it must be called
        // from a blocking thread, never a runtime worker.
        let checkpoint_store = self.checkpoint.clone();
        let store_lease_key = lease_key.clone();
        let initial_checkpoint_object = tokio::task::spawn_blocking(move || {
            checkpoint_store.get_checkpoint_object(&store_lease_key)
        })
        .await??
        .ok_or_else(|| {
            Box::<dyn std::error::Error + Send + Sync>::from(format!(
                "No checkpoint found for shard {lease_key}"
            ))
        })?;
        let initial_checkpoint = initial_checkpoint_object.checkpoint().clone();
        tracing::debug!(
            "[{}]: Checkpoint: {} -- Initial Position: {:?}",
            lease_key,
            initial_checkpoint,
            self.initial_position_in_stream
        );

        // 2026-07-14 fix: `start` can now fail (e.g. the polling publisher's
        // GetShardIterator times out or hits a non-ResourceNotFound SDK error).
        // Java: `cache.start(...)`'s exception propagates out of this same try
        // block uncaught, so `?` here (surfacing it the same way as any other
        // failure in this method) reproduces that — the outer `call()` catch
        // backs off and returns a failed `TaskResult`, and the state machine
        // re-runs `InitializeTask` (see `ConsumerState::failure_transition`,
        // which is the identity for `Initializing`).
        self.cache
            .start(initial_checkpoint.clone(), self.initial_position_in_stream)
            .await?;

        self.record_processor_checkpointer
            .set_largest_permitted_checkpoint_value(initial_checkpoint.clone());
        self.record_processor_checkpointer
            .set_initial_checkpoint_value(initial_checkpoint.clone());

        let initialization_input = InitializationInput::builder()
            .shard_id(self.shard_info.shard_id())
            .extended_sequence_number(initial_checkpoint)
            .maybe_pending_checkpoint_sequence_number(
                initial_checkpoint_object.pending_checkpoint().cloned(),
            )
            .maybe_pending_checkpoint_state(
                initial_checkpoint_object
                    .pending_checkpoint_state()
                    .map(<[u8]>::to_vec),
            )
            .build();

        // Invoke the sync `initialize()` callback via spawn_blocking (it may call
        // the checkpointer, which bridges to async via block_on).
        let processor = self.shard_record_processor.clone();
        let start_time = metrics::current_time_millis();
        let app_result = tokio::task::spawn_blocking(move || {
            let mut guard = processor
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            guard.initialize(initialization_input);
        })
        .await;

        let mut scope = metrics::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            INITIALIZE_TASK_OPERATION,
        );
        metrics::add_latency(
            scope.as_mut(),
            Some(RECORD_PROCESSOR_INITIALIZE_METRIC),
            start_time,
            MetricsLevel::Summary,
        );
        metrics::end_scope(scope.as_mut());

        match app_result {
            Ok(()) => {
                tracing::debug!("Record processor initialize() completed.");
                Ok(())
            }
            Err(join_err) => {
                // The customer initialize() panicked; surface it as an error.
                tracing::error!("Application initialize() threw exception: {join_err}");
                Err(Box::new(join_err))
            }
        }
    }
}

#[async_trait]
impl ConsumerTask for InitializeTask {
    async fn call(&self) -> TaskResult {
        match self.try_call().await {
            Ok(()) => TaskResult::new(None),
            Err(exception) => {
                // Exactly one WARN per failed attempt, with the shard id, the
                // full underlying error (after the data-fetcher fix, a
                // `FetchError`'s `Display` carries the `DisplayErrorContext`
                // chain end-to-end), and the retry intent -- this was the
                // "definitive error condition" that used to be unknowable in
                // the field (see PORTING.md's 2026-07-14 observability entry).
                // `ShardConsumer::result_to_outcome` additionally logs at DEBUG
                // (Java parity: `ShardConsumer.logTaskException`); this WARN is
                // the one line an operator sees by default.
                tracing::warn!(
                    "Shard {}: InitializeTask failed: {exception}; initialization will be retried",
                    self.shard_info.shard_id()
                );
                // Back off on exception (swallow cancellation of the sleep).
                tokio::time::sleep(Duration::from_millis(self.backoff_time_millis.max(0) as u64))
                    .await;
                TaskResult::new(Some(exception))
            }
        }
    }

    fn task_type(&self) -> TaskType {
        TaskType::Initialize
    }

    fn task_name(&self) -> &'static str {
        "InitializeTask"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::checkpoint::Checkpoint;
    use crate::common::InitialPositionInStream;
    use crate::lifecycle::test_support::RecordingRecordsPublisher;
    use crate::processor::{MockCheckpointer, MockShardRecordProcessor};
    use crate::retrieval::kpl::ExtendedSequenceNumber;

    fn shard_info() -> ShardInfo {
        ShardInfo::single_stream(
            "shardId-0",
            Some("token".into()),
            Vec::<String>::new(),
            None,
        )
    }

    fn checkpointer_for(
        store: Arc<dyn Checkpointer + Send + Sync>,
    ) -> Arc<ShardRecordProcessorCheckpointer> {
        ShardRecordProcessorCheckpointer::new(shard_info(), store)
    }

    #[tokio::test(start_paused = true)]
    async fn initialize_seeds_checkpointer_and_calls_processor() {
        let mut store = MockCheckpointer::new();
        store.expect_get_checkpoint_object().returning(|_| {
            Ok(Some(Checkpoint::without_state(
                ExtendedSequenceNumber::trim_horizon(),
                None,
            )))
        });
        let store: Arc<dyn Checkpointer + Send + Sync> = Arc::new(store);
        let checkpointer = checkpointer_for(store.clone());

        let mut proc = MockShardRecordProcessor::new();
        proc.expect_initialize()
            .times(1)
            .withf(|input| {
                input.shard_id() == Some("shardId-0")
                    && input.extended_sequence_number()
                        == Some(&ExtendedSequenceNumber::trim_horizon())
            })
            .returning(|_| ());
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));

        let task = InitializeTask::new(
            shard_info(),
            processor,
            store,
            checkpointer.clone(),
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            Arc::new(RecordingRecordsPublisher::new()),
            1,
            Arc::new(crate::metrics::NullMetricsFactory),
        );

        let result = task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(
            checkpointer.largest_permitted_checkpoint_value(),
            Some(ExtendedSequenceNumber::trim_horizon())
        );
        assert_eq!(
            checkpointer.last_checkpoint_value(),
            Some(ExtendedSequenceNumber::trim_horizon())
        );
    }

    #[tokio::test(start_paused = true)]
    async fn initialize_returns_exception_when_checkpoint_missing() {
        let mut store = MockCheckpointer::new();
        store.expect_get_checkpoint_object().returning(|_| Ok(None));
        let store: Arc<dyn Checkpointer + Send + Sync> = Arc::new(store);
        let checkpointer = checkpointer_for(store.clone());
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(MockShardRecordProcessor::new())));

        let task = InitializeTask::new(
            shard_info(),
            processor,
            store,
            checkpointer,
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            Arc::new(RecordingRecordsPublisher::new()),
            1,
            Arc::new(crate::metrics::NullMetricsFactory),
        );
        assert!(task.call().await.exception().is_some());
    }

    // New (2026-07-14 bug fix): a failing `RecordsPublisher::start` (e.g. the
    // polling publisher's `GetShardIterator` timing out or hitting a
    // non-ResourceNotFound SDK error) must fail the whole task — Java's
    // exception from `cache.start(...)` propagates out of the same `try` block
    // uncaught, so `shardRecordProcessor.initialize()` is never reached and
    // `TaskResult` carries the exception. This is the port of the bug this fix
    // closes: previously `RecordsPublisher::start` was infallible, so a failed
    // `GetShardIterator` on the very first call was silently treated as
    // success (false shard-end).
    #[tokio::test(start_paused = true)]
    async fn initialize_fails_task_when_cache_start_fails() {
        let mut store = MockCheckpointer::new();
        store.expect_get_checkpoint_object().returning(|_| {
            Ok(Some(Checkpoint::without_state(
                ExtendedSequenceNumber::trim_horizon(),
                None,
            )))
        });
        let store: Arc<dyn Checkpointer + Send + Sync> = Arc::new(store);
        let checkpointer = checkpointer_for(store.clone());

        let mut proc = MockShardRecordProcessor::new();
        proc.expect_initialize().times(0); // never reached: cache.start() fails first
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));

        let cache = Arc::new(RecordingRecordsPublisher::new().fail_start_times(1));

        let task = InitializeTask::new(
            shard_info(),
            processor,
            store,
            checkpointer.clone(),
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            cache.clone(),
            1,
            Arc::new(crate::metrics::NullMetricsFactory),
        );

        let result = task.call().await;
        assert!(
            result.exception().is_some(),
            "a failed cache.start() must surface as a failed TaskResult"
        );
        assert_eq!(cache.start_calls(), 1);
        // The checkpointer bookkeeping that follows cache.start() in Java's try
        // block never ran either (short-circuited by the propagated exception).
        assert_eq!(checkpointer.largest_permitted_checkpoint_value(), None);
    }

    // New (observability follow-up to the 2026-07-14 fix, "make retrieval
    // failures loudly diagnosable"): the WARN in `ConsumerTask::call`'s failure
    // arm is `tracing::warn!("Shard {}: InitializeTask failed: {exception}; \
    // initialization will be retried", self.shard_info.shard_id())` -- i.e. the
    // shard id and the retry-intent wording are literal parts of that one
    // format string (verified by inspection above), and `exception` is
    // `result.exception()` verbatim. This test pins down the one part that
    // isn't visible by code inspection alone: that a distinctive substring
    // from a synthetic source error survives end-to-end from
    // `RecordsPublisher::start`'s `Err` through `InitializeTask::try_call`'s
    // `?` propagation into that `exception`, unmangled -- i.e. what actually
    // reaches `{exception}` in the log line.
    //
    // This deliberately asserts on `TaskResult::exception()`'s rendered
    // `Display` rather than capturing real `tracing::warn!` output: capturing
    // process-wide `tracing` output is flaky under `cargo test`'s default
    // parallel execution (`tracing-core`'s per-callsite `Interest` cache is
    // shared process-wide across every concurrently-running test in this
    // `--lib` binary, so whether an event reaches a locally-installed
    // subscriber can depend on unrelated tests' execution order/timing).
    #[tokio::test(start_paused = true)]
    async fn initialize_failure_exception_carries_full_underlying_error_text() {
        let mut store = MockCheckpointer::new();
        store.expect_get_checkpoint_object().returning(|_| {
            Ok(Some(Checkpoint::without_state(
                ExtendedSequenceNumber::trim_horizon(),
                None,
            )))
        });
        let store: Arc<dyn Checkpointer + Send + Sync> = Arc::new(store);
        let checkpointer = checkpointer_for(store.clone());
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(MockShardRecordProcessor::new())));
        let cache = Arc::new(RecordingRecordsPublisher::new().fail_start_times(1));

        let task = InitializeTask::new(
            shard_info(),
            processor,
            store,
            checkpointer,
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            cache,
            1,
            Arc::new(crate::metrics::NullMetricsFactory),
        );

        let result = task.call().await;
        let exception = result
            .exception()
            .expect("a failed cache.start() must surface as a failed TaskResult");
        let message = exception.to_string();
        assert!(
            message.contains("injected start failure"),
            "expected the synthetic source error's distinctive text in the \
             propagated error (what `{{exception}}` renders in the WARN log), \
             got: {message}"
        );
    }

    /// A store that bridges sync→async via `Handle::block_on`, exactly like the
    /// production `DynamoDBCheckpointer`. `block_on` panics when called on a
    /// runtime worker, so this pins that `InitializeTask` dispatches the store
    /// call to a blocking thread (regression test: the task used to call it
    /// directly from its async context and panicked on every initialization).
    struct BlockOnCheckpointer {
        handle: tokio::runtime::Handle,
    }

    impl Checkpointer for BlockOnCheckpointer {
        fn set_checkpoint(
            &self,
            _: &str,
            _: &ExtendedSequenceNumber,
            _: &str,
        ) -> Result<(), crate::exceptions::KinesisClientLibError> {
            unimplemented!()
        }

        fn get_checkpoint(
            &self,
            _: &str,
        ) -> Result<Option<ExtendedSequenceNumber>, crate::exceptions::KinesisClientLibError>
        {
            unimplemented!()
        }

        fn get_checkpoint_object(
            &self,
            _: &str,
        ) -> Result<Option<Checkpoint>, crate::exceptions::KinesisClientLibError> {
            self.handle.block_on(async {
                tokio::task::yield_now().await;
                Ok(Some(Checkpoint::without_state(
                    ExtendedSequenceNumber::trim_horizon(),
                    None,
                )))
            })
        }

        fn prepare_checkpoint(
            &self,
            _: &str,
            _: &ExtendedSequenceNumber,
            _: &str,
        ) -> Result<(), crate::exceptions::KinesisClientLibError> {
            unimplemented!()
        }

        fn prepare_checkpoint_with_state(
            &self,
            _: &str,
            _: &ExtendedSequenceNumber,
            _: &str,
            _: &[u8],
        ) -> Result<(), crate::exceptions::KinesisClientLibError> {
            unimplemented!()
        }

        fn set_operation(&self, _: &str) {}

        fn operation(&self) -> String {
            String::new()
        }
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_supports_block_on_bridging_checkpointer() {
        let store: Arc<dyn Checkpointer + Send + Sync> = Arc::new(BlockOnCheckpointer {
            handle: tokio::runtime::Handle::current(),
        });
        let checkpointer = checkpointer_for(store.clone());

        let mut proc = MockShardRecordProcessor::new();
        proc.expect_initialize().times(1).returning(|_| ());
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));

        let task = InitializeTask::new(
            shard_info(),
            processor,
            store,
            checkpointer.clone(),
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            Arc::new(RecordingRecordsPublisher::new()),
            1,
            Arc::new(crate::metrics::NullMetricsFactory),
        );

        let result = task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(
            checkpointer.largest_permitted_checkpoint_value(),
            Some(ExtendedSequenceNumber::trim_horizon())
        );
    }

    #[tokio::test]
    async fn task_type_is_initialize() {
        let store: Arc<dyn Checkpointer + Send + Sync> = Arc::new(MockCheckpointer::new());
        let checkpointer = checkpointer_for(store.clone());
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(MockShardRecordProcessor::new())));
        let task = InitializeTask::new(
            shard_info(),
            processor,
            store,
            checkpointer,
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            Arc::new(RecordingRecordsPublisher::new()),
            1,
            Arc::new(crate::metrics::NullMetricsFactory),
        );
        assert_eq!(task.task_type(), TaskType::Initialize);
    }
}
