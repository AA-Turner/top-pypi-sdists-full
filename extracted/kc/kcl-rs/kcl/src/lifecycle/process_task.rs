//! Port of `software.amazon.kinesis.lifecycle.ProcessTask`.

use std::sync::{Arc, Mutex};
use std::time::Duration;

use aws_sdk_cloudwatch::types::StandardUnit;
use num_bigint::BigInt;

use async_trait::async_trait;

use crate::checkpoint::ShardRecordProcessorCheckpointer;
use crate::common::StreamIdentifier;
use crate::exceptions::BoxError;
use crate::leases::{LeaseStats, LeaseStatsRecorder, ShardDetector, ShardInfo};
use crate::lifecycle::events::ProcessRecordsInput;
use crate::lifecycle::{ConsumerTask, TaskResult, TaskType};
use crate::metrics::{self, MetricsFactory, MetricsLevel, MetricsScope};
use crate::processor::{RecordProcessorCheckpointer, ShardRecordProcessor};
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::{AggregatorUtil, KinesisClientRecord, ThrottlingReporter};

const PROCESS_TASK_OPERATION: &str = "ProcessTask";
const APPLICATION_TRACKER_OPERATION: &str = "ApplicationTracker";
const DATA_BYTES_PROCESSED_METRIC: &str = "DataBytesProcessed";
const RECORDS_PROCESSED_METRIC: &str = "RecordsProcessed";
const RECORD_PROCESSOR_PROCESS_RECORDS_METRIC: &str = "RecordProcessor.processRecords";
const MILLIS_BEHIND_LATEST_METRIC: &str = "MillisBehindLatest";

/// The starting/ending hash-key range of the shard, resolved from
/// [`ShardDetector::shard`], used for KPL de-aggregation dedup across resharding.
struct HashKeyRange {
    starting: BigInt,
    ending: BigInt,
}

/// Task for fetching data records and invoking `processRecords()` on the record
/// processor.
///
/// The customer `processRecords()` callback is invoked via
/// [`tokio::task::spawn_blocking`] (see the concurrency notes on
/// [`ShardConsumerArgument`]) — it may call the checkpointer, which bridges to
/// async internally.
///
/// [`ShardConsumerArgument`]: crate::lifecycle::ShardConsumerArgument
pub struct ProcessTask {
    shard_info: ShardInfo,
    shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
    record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
    backoff_time_millis: i64,
    skip_shard_sync_at_worker_initialization_if_leases_exist: bool,
    shard_detector: Arc<dyn ShardDetector>,
    throttling_reporter: Mutex<ThrottlingReporter>,
    process_records_input: ProcessRecordsInput,
    should_call_process_records_even_for_empty_record_list: bool,
    #[allow(dead_code)]
    idle_time_in_milliseconds: i64,
    aggregator_util: Arc<AggregatorUtil>,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    lease_stats_recorder: Arc<LeaseStatsRecorder>,
    shard_info_id: String,
}

impl ProcessTask {
    /// Public in Java. The Java constructor also eagerly calls
    /// `shardDetector.shard(...)`; here that lookup is async so it is deferred to
    /// [`ConsumerTask::call`] (see [`Self::resolve_shard`]). The
    /// `recordProcessorCheckpointer.checkpointer().operation(PROCESS_TASK_OPERATION)`
    /// side effect is preserved here in the constructor.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        shard_info: ShardInfo,
        shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
        record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
        backoff_time_millis: i64,
        skip_shard_sync_at_worker_initialization_if_leases_exist: bool,
        shard_detector: Arc<dyn ShardDetector>,
        throttling_reporter: ThrottlingReporter,
        process_records_input: ProcessRecordsInput,
        should_call_process_records_even_for_empty_record_list: bool,
        idle_time_in_milliseconds: i64,
        aggregator_util: Arc<AggregatorUtil>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        lease_stats_recorder: Arc<LeaseStatsRecorder>,
    ) -> Self {
        let shard_info_id = shard_info.lease_key();
        // Constructor side effect (Java): tag the checkpointer's operation.
        record_processor_checkpointer
            .checkpointer()
            .set_operation(PROCESS_TASK_OPERATION);
        Self {
            shard_info,
            shard_record_processor,
            record_processor_checkpointer,
            backoff_time_millis,
            skip_shard_sync_at_worker_initialization_if_leases_exist,
            shard_detector,
            throttling_reporter: Mutex::new(throttling_reporter),
            process_records_input,
            should_call_process_records_even_for_empty_record_list,
            idle_time_in_milliseconds,
            aggregator_util,
            metrics_factory,
            lease_stats_recorder,
            shard_info_id,
        }
    }

    /// Resolve the shard's hash-key-range (Java's constructor `shardDetector.shard`
    /// side effect). Best-effort: a missing shard just warns and proceeds with
    /// `None`. Deferred to `call()` because `ShardDetector::shard` is async.
    async fn resolve_shard(&self) -> Option<HashKeyRange> {
        if self.skip_shard_sync_at_worker_initialization_if_leases_exist {
            return None;
        }
        let shard = match self.shard_detector.shard(self.shard_info.shard_id()).await {
            Ok(Some(shard)) => Some(shard),
            _ => None,
        };
        if shard.is_none() {
            tracing::warn!(
                "Cannot get the shard for this ProcessTask, so duplicate KPL user records \
                 in the event of resharding will not be dropped during deaggregation of Amazon \
                 Kinesis records."
            );
        }
        shard.and_then(|s| {
            let range = s.hash_key_range()?;
            let starting = range.starting_hash_key().parse::<BigInt>().ok()?;
            let ending = range.ending_hash_key().parse::<BigInt>().ok()?;
            Some(HashKeyRange { starting, ending })
        })
    }

    fn deaggregate(
        &self,
        records: Vec<KinesisClientRecord>,
        range: &Option<HashKeyRange>,
    ) -> Vec<KinesisClientRecord> {
        match range {
            None => self.aggregator_util.deaggregate(records),
            Some(range) => {
                self.aggregator_util
                    .deaggregate_with_range(records, &range.starting, &range.ending)
            }
        }
    }

    fn should_call_process_records(&self, records: &[KinesisClientRecord]) -> bool {
        !records.is_empty() || self.should_call_process_records_even_for_empty_record_list
    }

    fn publish_lease_stats(&self, records: &[KinesisClientRecord]) {
        let bytes: i64 = records
            .iter()
            .map(|r| r.data().map(|b| b.len()).unwrap_or(0) as i64)
            .sum();
        self.lease_stats_recorder.record_stats(LeaseStats::new(
            self.shard_info.lease_key(),
            bytes,
            metrics::current_time_millis(),
        ));
    }

    /// Scans `records`, dropping any with ESN <= `last_checkpoint_value`
    /// (mutating in place, via `retain`), emitting `DataBytesProcessed` for
    /// retained records, and returning the largest ESN among retained records
    /// (seeded from `last_largest_permitted`, so the value is monotonic
    /// non-decreasing even if all records are filtered).
    ///
    /// Port of `filterAndGetMaxExtendedSequenceNumber`.
    fn filter_and_get_max_extended_sequence_number(
        &self,
        scope: &mut (dyn MetricsScope + Send),
        records: &mut Vec<KinesisClientRecord>,
        last_checkpoint_value: Option<&ExtendedSequenceNumber>,
        last_largest_permitted: Option<&ExtendedSequenceNumber>,
    ) -> Option<ExtendedSequenceNumber> {
        let mut largest: Option<ExtendedSequenceNumber> = last_largest_permitted.cloned();
        let mut retained: Vec<KinesisClientRecord> = Vec::with_capacity(records.len());
        for record in records.drain(..) {
            let esn = ExtendedSequenceNumber::new(
                record.sequence_number().unwrap_or("").to_string(),
                Some(record.sub_sequence_number()),
            );
            // Drop records at or before the last checkpoint.
            if compare_le(&esn, last_checkpoint_value) {
                tracing::debug!(
                    "{} : removing record with ESN {} because the ESN is <= checkpoint ({:?})",
                    self.shard_info_id,
                    esn,
                    last_checkpoint_value
                );
                continue;
            }
            if largest
                .as_ref()
                .map(|l| l.compare_to(&esn).is_lt())
                .unwrap_or(true)
            {
                largest = Some(esn.clone());
            }
            scope.add_data_with_level(
                DATA_BYTES_PROCESSED_METRIC,
                record.data().map(|b| b.len()).unwrap_or(0) as f64,
                StandardUnit::Bytes,
                MetricsLevel::Summary,
            );
            retained.push(record);
        }
        *records = retained;
        largest
    }

    /// Dispatches the batch to the customer processor via `spawn_blocking`, and
    /// swallows any error/panic from the callback (matching Java's caught +
    /// logged + swallowed behavior). Returns the derived `ProcessRecordsInput`
    /// that was handed to the customer (the `records`-replaced + checkpointer copy).
    async fn call_process_records(&self, records: Vec<KinesisClientRecord>) -> ProcessRecordsInput {
        tracing::debug!(
            "Calling application processRecords() with {} records from {}",
            records.len(),
            self.shard_info_id
        );
        let checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync> =
            self.record_processor_checkpointer.clone();
        let derived = rebuild_with_records(&self.process_records_input, records, checkpointer);

        let mut scope = metrics::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            PROCESS_TASK_OPERATION,
        );
        if let Some(stream_id) = self.shard_info.stream_identifier_ser_opt() {
            metrics::add_stream_id(
                scope.as_mut(),
                &StreamIdentifier::multi_stream_instance(stream_id),
            );
        }
        metrics::add_shard_id(scope.as_mut(), self.shard_info.shard_id());
        let start_time = metrics::current_time_millis();

        let processor = self.shard_record_processor.clone();
        let input_for_processor = derived.clone();
        let call_result = tokio::task::spawn_blocking(move || {
            let mut guard = processor
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            guard.process_records(input_for_processor);
        })
        .await;
        if let Err(e) = call_result {
            tracing::error!(
                "ShardId {}: Application processRecords() threw an exception: {}",
                self.shard_info_id,
                e
            );
        }

        metrics::add_latency(
            scope.as_mut(),
            Some(RECORD_PROCESSOR_PROCESS_RECORDS_METRIC),
            start_time,
            MetricsLevel::Summary,
        );
        metrics::end_scope(scope.as_mut());
        derived
    }

    /// The main processing body (everything inside Java's inner `try`), returning
    /// an error to be captured (framework/de-agg exception). Shard-end short
    /// circuits are handled by the caller.
    async fn process(
        &self,
        shard_scope: &mut (dyn MetricsScope + Send),
        app_scope: &mut (dyn MetricsScope + Send),
        range: &Option<HashKeyRange>,
    ) -> Result<(), BoxError> {
        let input = &self.process_records_input;
        if let Some(mbl) = input.millis_behind_latest() {
            shard_scope.add_data_with_level(
                MILLIS_BEHIND_LATEST_METRIC,
                mbl as f64,
                StandardUnit::Milliseconds,
                MetricsLevel::Summary,
            );
            app_scope.add_data_with_level(
                MILLIS_BEHIND_LATEST_METRIC,
                mbl as f64,
                StandardUnit::Milliseconds,
                MetricsLevel::Summary,
            );
        }

        // The at-shard-end-and-empty short circuit is handled in `call()` before
        // this method runs (so throttlingReporter.success() is NOT called there).

        self.throttling_reporter
            .lock()
            .unwrap_or_else(std::sync::PoisonError::into_inner)
            .success();

        let input_records = input.records().map(<[_]>::to_vec).unwrap_or_default();
        let mut records = self.deaggregate(input_records, range);

        // schemaRegistryDecoder is deferred (always absent); no decode step.

        if !records.is_empty() {
            shard_scope.add_data_with_level(
                RECORDS_PROCESSED_METRIC,
                records.len() as f64,
                StandardUnit::Count,
                MetricsLevel::Summary,
            );
        }

        let new_largest = self.filter_and_get_max_extended_sequence_number(
            shard_scope,
            &mut records,
            self.record_processor_checkpointer
                .last_checkpoint_value()
                .as_ref(),
            self.record_processor_checkpointer
                .largest_permitted_checkpoint_value()
                .as_ref(),
        );
        if let Some(v) = new_largest {
            self.record_processor_checkpointer
                .set_largest_permitted_checkpoint_value(v);
        }

        if self.should_call_process_records(&records) {
            self.publish_lease_stats(&records);
            self.call_process_records(records).await;
        }
        Ok(())
    }
}

#[async_trait]
impl ConsumerTask for ProcessTask {
    async fn call(&self) -> TaskResult {
        let range = self.resolve_shard().await;

        let mut app_scope = metrics::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            APPLICATION_TRACKER_OPERATION,
        );
        let mut shard_scope = metrics::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            PROCESS_TASK_OPERATION,
        );
        if let Some(stream_id) = self.shard_info.stream_identifier_ser_opt() {
            metrics::add_stream_id(
                shard_scope.as_mut(),
                &StreamIdentifier::multi_stream_instance(stream_id),
            );
        }
        metrics::add_shard_id(shard_scope.as_mut(), self.shard_info.shard_id());
        let start_time_millis = metrics::current_time_millis();
        let mut success = false;

        // finally-equivalent: metrics recorded on every return path.
        let result = {
            shard_scope.add_data_with_level(
                RECORDS_PROCESSED_METRIC,
                0.0,
                StandardUnit::Count,
                MetricsLevel::Summary,
            );
            shard_scope.add_data_with_level(
                DATA_BYTES_PROCESSED_METRIC,
                0.0,
                StandardUnit::Bytes,
                MetricsLevel::Summary,
            );

            let input = &self.process_records_input;
            let records_empty = input.records().map(<[_]>::is_empty).unwrap_or(true);

            // Short-circuit success if at shard end and no records (empty final
            // batch): return TaskResult(null, true) without any processing, and
            // WITHOUT calling throttlingReporter.success().
            if input.is_at_shard_end() && records_empty {
                tracing::info!(
                    "Reached end of shard {} and have no records to process",
                    self.shard_info_id
                );
                // Note: `success` remains false here, matching Java (the finally
                // block reports success=false for this early-return path).
                Some(TaskResult::shard_end(true))
            } else {
                let mut exception: Option<BoxError> = None;
                match self
                    .process(shard_scope.as_mut(), app_scope.as_mut(), &range)
                    .await
                {
                    Ok(()) => success = true,
                    Err(e) => {
                        tracing::error!("ShardId {}: Caught exception: {}", self.shard_info_id, e);
                        exception = Some(e);
                        // backoff on exception (swallow sleep cancellation)
                        tokio::time::sleep(Duration::from_millis(
                            self.backoff_time_millis.max(0) as u64
                        ))
                        .await;
                    }
                }

                // The final shard-end check happens AFTER the try/catch: even if an
                // exception occurred, reaching shard end still reports (null, true)
                // — the captured exception is discarded. Load-bearing behavior.
                if input.is_at_shard_end() {
                    tracing::info!(
                        "Reached end of shard {}, and processed {} records",
                        self.shard_info_id,
                        input.records().map(<[_]>::len).unwrap_or(0)
                    );
                    Some(TaskResult::shard_end(true))
                } else {
                    Some(TaskResult::new(exception))
                }
            }
        };

        metrics::add_success_and_latency(
            shard_scope.as_mut(),
            success,
            start_time_millis,
            MetricsLevel::Summary,
        );
        metrics::end_scope(shard_scope.as_mut());
        metrics::end_scope(app_scope.as_mut());

        result.expect("result is always set")
    }

    fn task_type(&self) -> TaskType {
        TaskType::Process
    }

    fn task_name(&self) -> &'static str {
        "ProcessTask"
    }
}

/// `a <= b` under `ExtendedSequenceNumber::compare_to`, where `b == None` means
/// there is no last checkpoint (nothing is <= a missing checkpoint).
fn compare_le(a: &ExtendedSequenceNumber, b: Option<&ExtendedSequenceNumber>) -> bool {
    match b {
        None => false,
        Some(b) => a.compare_to(b).is_le(),
    }
}

/// Rebuild a [`ProcessRecordsInput`] with replaced `records` and attached
/// `checkpointer`, preserving the other fields (Java `input.toBuilder()`).
fn rebuild_with_records(
    input: &ProcessRecordsInput,
    records: Vec<KinesisClientRecord>,
    checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync>,
) -> ProcessRecordsInput {
    ProcessRecordsInput::builder()
        .is_at_shard_end(input.is_at_shard_end())
        .records(records)
        .checkpointer(checkpointer)
        .maybe_cache_entry_time(input.cache_entry_time())
        .maybe_cache_exit_time(input.cache_exit_time())
        .maybe_millis_behind_latest(input.millis_behind_latest())
        .maybe_child_shards(input.child_shards().map(<[_]>::to_vec))
        .build()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::processor::{Checkpointer, MockShardRecordProcessor};
    use bytes::Bytes;
    use std::sync::Mutex as StdMutex;

    // A simple in-memory Checkpointer store so we can build a real
    // ShardRecordProcessorCheckpointer (which is concrete, not mockable).
    #[derive(Default)]
    struct InMemoryCheckpointStore {
        operation: StdMutex<Option<String>>,
    }

    impl Checkpointer for InMemoryCheckpointStore {
        fn set_checkpoint(
            &self,
            _lease_key: &str,
            _checkpoint: &ExtendedSequenceNumber,
            _concurrency_token: &str,
        ) -> Result<(), crate::exceptions::KinesisClientLibError> {
            Ok(())
        }
        fn get_checkpoint(
            &self,
            _lease_key: &str,
        ) -> Result<Option<ExtendedSequenceNumber>, crate::exceptions::KinesisClientLibError>
        {
            Ok(None)
        }
        fn get_checkpoint_object(
            &self,
            _lease_key: &str,
        ) -> Result<Option<crate::checkpoint::Checkpoint>, crate::exceptions::KinesisClientLibError>
        {
            Ok(None)
        }
        fn prepare_checkpoint(
            &self,
            _lease_key: &str,
            _pending_checkpoint: &ExtendedSequenceNumber,
            _concurrency_token: &str,
        ) -> Result<(), crate::exceptions::KinesisClientLibError> {
            Ok(())
        }
        fn prepare_checkpoint_with_state(
            &self,
            _lease_key: &str,
            _pending_checkpoint: &ExtendedSequenceNumber,
            _concurrency_token: &str,
            _pending_checkpoint_state: &[u8],
        ) -> Result<(), crate::exceptions::KinesisClientLibError> {
            Ok(())
        }
        fn set_operation(&self, operation: &str) {
            *self.operation.lock().unwrap() = Some(operation.to_string());
        }
        fn operation(&self) -> String {
            self.operation.lock().unwrap().clone().unwrap_or_default()
        }
    }

    const SHARD_ID: &str = "shard-test";

    fn shard_info() -> ShardInfo {
        ShardInfo::single_stream(SHARD_ID, None, Vec::<String>::new(), None)
    }

    fn checkpointer() -> Arc<ShardRecordProcessorCheckpointer> {
        let store: Arc<dyn Checkpointer + Send + Sync> =
            Arc::new(InMemoryCheckpointStore::default());
        ShardRecordProcessorCheckpointer::new(shard_info(), store)
    }

    fn make_record(pk: &str, sqn: &str) -> KinesisClientRecord {
        KinesisClientRecord::builder()
            .partition_key(pk)
            .sequence_number(sqn)
            .data(Bytes::from_static(&[1, 2, 3, 4]))
            .build()
    }

    // ---- KPL aggregation test helpers (port of ProcessTaskTest's ----
    // ---- generateAggregatedRecord / md5 / ControlledHashAggregatorUtil) ----

    use crate::retrieval::kpl::messages::{AggregatedRecord, Record as KplRecord};
    use md5::{Digest, Md5};

    const TEST_DATA: &[u8] = &[1, 2, 3, 4];

    fn md5(data: &[u8]) -> Vec<u8> {
        let mut h = Md5::new();
        h.update(data);
        h.finalize().to_vec()
    }

    /// Wrap a KPL `AggregatedRecord` protobuf in the KPL magic + body + MD5
    /// envelope (the on-wire payload a real aggregated Kinesis record carries).
    /// Port of the header/footer wrapping in `generateAggregatedRecord`.
    fn envelope(ar: &AggregatedRecord) -> Bytes {
        use crate::retrieval::AGGREGATED_RECORD_MAGIC;
        let body = ar.encode_to_vec();
        let digest = md5(&body);
        let mut buf = Vec::with_capacity(AGGREGATED_RECORD_MAGIC.len() + body.len() + digest.len());
        buf.extend_from_slice(&AGGREGATED_RECORD_MAGIC);
        buf.extend_from_slice(&body);
        buf.extend_from_slice(&digest);
        Bytes::from(buf)
    }

    /// Port of `generateAggregatedRecord(pk)`: one partition key, three identical
    /// sub-records each carrying `TEST_DATA`, wrapped in the KPL envelope.
    fn generate_aggregated_record(pk: &str) -> Bytes {
        let r = KplRecord {
            partition_key_index: 0,
            explicit_hash_key_index: None,
            data: TEST_DATA.to_vec(),
            tags: vec![],
        };
        let ar = AggregatedRecord {
            partition_key_table: vec![pk.to_string()],
            explicit_hash_key_table: vec![],
            records: vec![r.clone(), r.clone(), r],
        };
        envelope(&ar)
    }

    /// The SDK `Shard` used to give ProcessTask a hash-key range (drives the
    /// resharding drop). Port of the `Shard.builder().hashKeyRange(...)` stub.
    fn shard_with_range(low: &str, high: &str) -> aws_sdk_kinesis::types::Shard {
        use aws_sdk_kinesis::types::{HashKeyRange, SequenceNumberRange, Shard};
        Shard::builder()
            .shard_id("Shard-01")
            .sequence_number_range(
                SequenceNumberRange::builder()
                    .starting_sequence_number("1")
                    .build()
                    .unwrap(),
            )
            .hash_key_range(
                HashKeyRange::builder()
                    .starting_hash_key(low)
                    .ending_hash_key(high)
                    .build()
                    .unwrap(),
            )
            .build()
            .unwrap()
    }

    #[allow(clippy::too_many_arguments)]
    fn make_task(
        input: ProcessRecordsInput,
        processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
        cp: Arc<ShardRecordProcessorCheckpointer>,
        detector: Arc<dyn ShardDetector>,
        skip_shard_sync: bool,
    ) -> ProcessTask {
        ProcessTask::new(
            shard_info(),
            processor,
            cp,
            1,
            skip_shard_sync,
            detector,
            ThrottlingReporter::new(5, SHARD_ID),
            input,
            true, // shouldCallProcessRecordsEvenForEmptyRecordList
            100,
            Arc::new(AggregatorUtil::new()),
            Arc::new(crate::metrics::NullMetricsFactory),
            Arc::new(LeaseStatsRecorder::new(
                30_000,
                Arc::new(metrics::current_time_millis),
            )),
        )
    }

    #[tokio::test(start_paused = true)]
    async fn process_task_with_shard_end_reached_no_records() {
        // isAtShardEnd + empty records -> (null, true) with no processor interaction.
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records().never();
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));

        let mut detector = crate::leases::shard_detector::MockShardDetector::new();
        detector.expect_shard().never();
        let input = ProcessRecordsInput::builder()
            .records(vec![])
            .is_at_shard_end(true)
            .build();
        let task = make_task(input, processor, checkpointer(), Arc::new(detector), true);
        let result = task.call().await;
        assert!(result.is_shard_end_reached());
        assert!(result.exception().is_none());
    }

    #[tokio::test(start_paused = true)]
    async fn non_aggregated_record_is_passed_through() {
        let cp = checkpointer();
        cp.set_initial_checkpoint_value(ExtendedSequenceNumber::trim_horizon());
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::trim_horizon());

        let captured: Arc<Mutex<Option<ProcessRecordsInput>>> = Arc::new(Mutex::new(None));
        let cap2 = captured.clone();
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records()
            .times(1)
            .returning(move |input| {
                *cap2.lock().unwrap() = Some(input);
            });
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));

        let detector = crate::leases::shard_detector::MockShardDetector::new();
        let record = make_record("pk", "12345678901234567890");
        let input = ProcessRecordsInput::builder().records(vec![record]).build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), true);
        let result = task.call().await;
        assert!(!result.is_shard_end_reached());
        assert!(result.exception().is_none());

        let captured = captured.lock().unwrap().take().unwrap();
        assert_eq!(captured.records().unwrap().len(), 1);
        assert_eq!(captured.records().unwrap()[0].partition_key(), Some("pk"));
        // largest permitted advances to the record's ESN.
        assert_eq!(
            cp.largest_permitted_checkpoint_value(),
            Some(ExtendedSequenceNumber::from_sequence_number(
                "12345678901234567890"
            ))
        );
    }

    #[tokio::test(start_paused = true)]
    async fn largest_permitted_unchanged_with_empty_records() {
        let cp = checkpointer();
        let base = ExtendedSequenceNumber::from_sequence_number("1000");
        let largest = ExtendedSequenceNumber::from_sequence_number("1100");
        cp.set_initial_checkpoint_value(base);
        cp.set_largest_permitted_checkpoint_value(largest.clone());

        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records().returning(|_| ());
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));
        let detector = crate::leases::shard_detector::MockShardDetector::new();

        let input = ProcessRecordsInput::builder().records(vec![]).build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), true);
        task.call().await;
        assert_eq!(cp.largest_permitted_checkpoint_value(), Some(largest));
    }

    #[tokio::test(start_paused = true)]
    async fn filters_records_at_or_below_last_checkpoint() {
        let cp = checkpointer();
        // last checkpoint at "500"; records "400","600" -> "400" dropped.
        cp.set_initial_checkpoint_value(ExtendedSequenceNumber::from_sequence_number("500"));
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::from_sequence_number(
            "500",
        ));

        let captured: Arc<Mutex<Option<ProcessRecordsInput>>> = Arc::new(Mutex::new(None));
        let cap2 = captured.clone();
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records().returning(move |input| {
            *cap2.lock().unwrap() = Some(input);
        });
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));
        let detector = crate::leases::shard_detector::MockShardDetector::new();

        let input = ProcessRecordsInput::builder()
            .records(vec![make_record("p", "400"), make_record("p", "600")])
            .build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), true);
        task.call().await;
        let captured = captured.lock().unwrap().take().unwrap();
        assert_eq!(captured.records().unwrap().len(), 1);
        assert_eq!(
            captured.records().unwrap()[0].sequence_number(),
            Some("600")
        );
    }

    #[tokio::test(start_paused = true)]
    async fn process_task_with_records_and_shard_end_reached() {
        // Port of testProcessTaskWithRecordsAndShardEndReached: a non-empty batch
        // AND is_at_shard_end -> the empty-shard-end short circuit does NOT fire,
        // so processRecords IS called with the (unchanged) record, and the task
        // still returns (null, true).
        let cp = checkpointer();
        cp.set_initial_checkpoint_value(ExtendedSequenceNumber::trim_horizon());
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::trim_horizon());

        let captured: Arc<Mutex<Option<ProcessRecordsInput>>> = Arc::new(Mutex::new(None));
        let cap2 = captured.clone();
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records()
            .times(1)
            .returning(move |input| {
                *cap2.lock().unwrap() = Some(input);
            });
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));
        let detector = crate::leases::shard_detector::MockShardDetector::new();

        let record = make_record("pk", "170141183460469231731687303715884105727");
        let child = aws_sdk_kinesis::types::ChildShard::builder()
            .shard_id("child-0")
            .parent_shards(SHARD_ID)
            .hash_key_range(
                aws_sdk_kinesis::types::HashKeyRange::builder()
                    .starting_hash_key("0")
                    .ending_hash_key("99")
                    .build()
                    .unwrap(),
            )
            .build()
            .unwrap();
        let input = ProcessRecordsInput::builder()
            .records(vec![record.clone()])
            .is_at_shard_end(true)
            .child_shards(vec![child])
            .build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), true);
        let result = task.call().await;
        assert!(result.is_shard_end_reached());
        assert!(result.exception().is_none());

        let captured = captured.lock().unwrap().take().unwrap();
        assert_eq!(captured.records().unwrap().len(), 1);
        assert_eq!(captured.records().unwrap()[0].partition_key(), Some("pk"));
    }

    #[tokio::test(start_paused = true)]
    async fn deaggregates_record() {
        // Port of testDeaggregatesRecord: one KPL-aggregated record with three
        // identical sub-records deaggregates into three records that all share the
        // partition key / arrival timestamp; largest permitted checkpoint advances
        // to (sqn, subSeq=2).
        let sqn = "42535295865117307932921825928971026432";
        let pk = "aggregated-pk";
        let ts = chrono::Utc::now() - chrono::Duration::hours(4);
        let record = KinesisClientRecord::builder()
            .partition_key("-")
            .data(generate_aggregated_record(pk))
            .sequence_number(sqn)
            .approximate_arrival_timestamp(ts)
            .build();

        let cp = checkpointer();
        cp.set_initial_checkpoint_value(ExtendedSequenceNumber::trim_horizon());
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::trim_horizon());

        let captured: Arc<Mutex<Option<ProcessRecordsInput>>> = Arc::new(Mutex::new(None));
        let cap2 = captured.clone();
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records()
            .times(1)
            .returning(move |input| {
                *cap2.lock().unwrap() = Some(input);
            });
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));
        let detector = crate::leases::shard_detector::MockShardDetector::new();

        let input = ProcessRecordsInput::builder().records(vec![record]).build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), true);
        task.call().await;

        let captured = captured.lock().unwrap().take().unwrap();
        let actual = captured.records().unwrap();
        assert_eq!(actual.len(), 3);
        for (i, pr) in actual.iter().enumerate() {
            assert_eq!(pr.partition_key(), Some(pk));
            assert_eq!(pr.approximate_arrival_timestamp(), Some(ts));
            assert_eq!(pr.data().unwrap().as_ref(), TEST_DATA);
            assert_eq!(pr.sub_sequence_number(), i as i64);
        }
        // checkpointCall = (sqn, actualRecords.size() - 1).
        assert_eq!(
            cp.largest_permitted_checkpoint_value(),
            Some(ExtendedSequenceNumber::new(sqn, Some(2)))
        );
    }

    #[tokio::test(start_paused = true)]
    async fn deaggregates_record_with_no_arrival_timestamp() {
        // Port of testDeaggregatesRecordWithNoArrivalTimestamp: same as above but
        // the source record has no arrival timestamp -> all deaggregated records
        // carry a None timestamp.
        let sqn = "42535295865117307932921825928971026432";
        let pk = "aggregated-pk";
        let record = KinesisClientRecord::builder()
            .partition_key("-")
            .data(generate_aggregated_record(pk))
            .sequence_number(sqn)
            .build();

        let cp = checkpointer();
        cp.set_initial_checkpoint_value(ExtendedSequenceNumber::trim_horizon());
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::trim_horizon());

        let captured: Arc<Mutex<Option<ProcessRecordsInput>>> = Arc::new(Mutex::new(None));
        let cap2 = captured.clone();
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records()
            .times(1)
            .returning(move |input| {
                *cap2.lock().unwrap() = Some(input);
            });
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));
        let detector = crate::leases::shard_detector::MockShardDetector::new();

        let input = ProcessRecordsInput::builder().records(vec![record]).build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), true);
        task.call().await;

        let captured = captured.lock().unwrap().take().unwrap();
        let actual = captured.records().unwrap();
        assert_eq!(actual.len(), 3);
        for pr in actual {
            assert_eq!(pr.partition_key(), Some(pk));
            assert_eq!(pr.approximate_arrival_timestamp(), None);
        }
    }

    #[tokio::test(start_paused = true)]
    async fn filter_based_on_last_checkpoint_value() {
        // Port of testFilterBasedOnLastCheckpointValue: an aggregate of 3
        // sub-records (X.0, X.1, X.2). The last checkpoint is X.1, so X.0 and X.1
        // are filtered out and only X.2 survives; largest permitted becomes X.2.
        let sqn = "42535295865117307932921825928971026432";
        let previous_ssqn: i64 = 1;
        let pk = "aggregated-pk";
        let record = KinesisClientRecord::builder()
            .partition_key("-")
            .data(generate_aggregated_record(pk))
            .sequence_number(sqn)
            .build();

        let cp = checkpointer();
        cp.set_initial_checkpoint_value(ExtendedSequenceNumber::new(sqn, Some(previous_ssqn)));
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::new(
            sqn,
            Some(previous_ssqn),
        ));

        let captured: Arc<Mutex<Option<ProcessRecordsInput>>> = Arc::new(Mutex::new(None));
        let cap2 = captured.clone();
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records()
            .times(1)
            .returning(move |input| {
                *cap2.lock().unwrap() = Some(input);
            });
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));
        let detector = crate::leases::shard_detector::MockShardDetector::new();

        let input = ProcessRecordsInput::builder().records(vec![record]).build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), true);
        task.call().await;

        let captured = captured.lock().unwrap().take().unwrap();
        let actual = captured.records().unwrap();
        // First two sub-records dropped; one remaining.
        assert_eq!(actual.len(), 1);
        let r = &actual[0];
        assert_eq!(r.partition_key(), Some(pk));
        assert_eq!(r.sequence_number(), Some(sqn));
        assert_eq!(r.sub_sequence_number(), previous_ssqn + 1);
        assert_eq!(r.approximate_arrival_timestamp(), None);
        // Largest permitted = last sub-record ESN = (sqn, 2).
        assert_eq!(
            cp.largest_permitted_checkpoint_value(),
            Some(ExtendedSequenceNumber::new(sqn, Some(2)))
        );
    }

    #[tokio::test(start_paused = true)]
    async fn discard_resharded_kpl_data() {
        // Port of testDiscardReshardedKplData: one aggregate containing 5 in-range,
        // then 5 below-range, then 5 above-range sub-records (against the shard's
        // hash-key range). The first out-of-range sub-record rolls back the whole
        // current aggregate, so ProcessTask sees an EMPTY record list.
        //
        // Java overrides AggregatorUtil.effectiveHashKey via a subclass; the Rust
        // AggregatorUtil is concrete, so we drive the same in/below/above-range
        // outcome deterministically via explicit hash keys relative to the shard
        // range [2^60, 2^68].
        let low = (BigInt::from(1) << 60u32).to_string();
        let high = (BigInt::from(1) << 68u32).to_string();
        let below = (BigInt::from(1) << 59u32).to_string(); // < low
        let in_range = (BigInt::from(1) << 64u32).to_string(); // within [low, high]
        let above = (BigInt::from(1) << 69u32).to_string(); // > high
        let sqn = "1329227995784915872903807060280344576"; // 2^120

        let r = |pk_idx: u64, ehk_idx: u64| KplRecord {
            partition_key_index: pk_idx,
            explicit_hash_key_index: Some(ehk_idx),
            data: TEST_DATA.to_vec(),
            tags: vec![],
        };
        // 5 in-range (ehk idx 0), 5 below-range (idx 1), 5 above-range (idx 2).
        let mut records = Vec::new();
        for _ in 0..5 {
            records.push(r(0, 0));
        }
        for _ in 0..5 {
            records.push(r(0, 1));
        }
        for _ in 0..5 {
            records.push(r(0, 2));
        }
        let ar = AggregatedRecord {
            partition_key_table: vec!["p-01".to_string()],
            explicit_hash_key_table: vec![in_range, below, above],
            records,
        };
        let raw = KinesisClientRecord::builder()
            .partition_key("p-01")
            .data(envelope(&ar))
            .sequence_number(sqn)
            .approximate_arrival_timestamp(chrono::Utc::now())
            .build();

        let mut detector = crate::leases::shard_detector::MockShardDetector::new();
        detector
            .expect_shard()
            .returning(move |_| Ok(Some(shard_with_range(&low, &high))));

        let cp = checkpointer();
        cp.set_initial_checkpoint_value(ExtendedSequenceNumber::new(
            "1329227995784915872903807060280344476",
            Some(0),
        ));
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::new(sqn, Some(16)));

        let captured: Arc<Mutex<Option<ProcessRecordsInput>>> = Arc::new(Mutex::new(None));
        let cap2 = captured.clone();
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records()
            .times(1)
            .returning(move |input| {
                *cap2.lock().unwrap() = Some(input);
            });
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));

        // skip_shard_sync=false so ProcessTask resolves the shard's hash key range.
        let input = ProcessRecordsInput::builder().records(vec![raw]).build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), false);
        task.call().await;

        let captured = captured.lock().unwrap().take().unwrap();
        assert!(captured.records().unwrap().is_empty());
    }

    #[tokio::test(start_paused = true)]
    async fn all_in_shard_kpl_data() {
        // Port of testAllInShardKplData: three raw records, each an aggregate of
        // two in-range sub-records. All six are within the shard's hash-key range,
        // so all six survive deaggregation.
        let low = (BigInt::from(1) << 60u32).to_string();
        let high = (BigInt::from(1) << 68u32).to_string();
        let in_range = (BigInt::from(1) << 64u32).to_string();

        let mut raw_records = Vec::new();
        // sequence numbers are increasing (2^120 + 1, +2, +3).
        let base: BigInt = "1329227995784915872903807060280344576".parse().unwrap();
        let mut last_sqn = String::new();
        for i in 0..3u32 {
            let sqn = (&base + BigInt::from(i + 1)).to_string();
            last_sqn = sqn.clone();
            let mk = |pk_idx: u64| KplRecord {
                partition_key_index: pk_idx,
                explicit_hash_key_index: Some(0),
                data: TEST_DATA.to_vec(),
                tags: vec![],
            };
            let ar = AggregatedRecord {
                partition_key_table: vec![format!("pa-{i}-0"), format!("pa-{i}-1")],
                explicit_hash_key_table: vec![in_range.clone()],
                records: vec![mk(0), mk(1)],
            };
            let raw = KinesisClientRecord::builder()
                .partition_key(format!("pa-{i}"))
                .data(envelope(&ar))
                .sequence_number(sqn)
                .build();
            raw_records.push(raw);
        }

        let mut detector = crate::leases::shard_detector::MockShardDetector::new();
        detector
            .expect_shard()
            .returning(move |_| Ok(Some(shard_with_range(&low, &high))));

        let cp = checkpointer();
        cp.set_initial_checkpoint_value(ExtendedSequenceNumber::new(
            "1329227995784915872903807060280344476",
            Some(0),
        ));
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::new(&last_sqn, Some(0)));

        let captured: Arc<Mutex<Option<ProcessRecordsInput>>> = Arc::new(Mutex::new(None));
        let cap2 = captured.clone();
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_process_records()
            .times(1)
            .returning(move |input| {
                *cap2.lock().unwrap() = Some(input);
            });
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));

        let input = ProcessRecordsInput::builder().records(raw_records).build();
        let task = make_task(input, processor, cp.clone(), Arc::new(detector), false);
        task.call().await;

        let captured = captured.lock().unwrap().take().unwrap();
        assert_eq!(captured.records().unwrap().len(), 6);
    }

    #[tokio::test]
    async fn task_type_is_process() {
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(MockShardRecordProcessor::new())));
        let detector = crate::leases::shard_detector::MockShardDetector::new();
        let input = ProcessRecordsInput::builder().records(vec![]).build();
        let task = make_task(input, processor, checkpointer(), Arc::new(detector), true);
        assert_eq!(task.task_type(), TaskType::Process);
    }

    // ensure the CheckpointerTrait alias is referenced (operation side effect).
    #[test]
    fn constructor_sets_operation() {
        let store = Arc::new(InMemoryCheckpointStore::default());
        let cp = ShardRecordProcessorCheckpointer::new(
            shard_info(),
            store.clone() as Arc<dyn Checkpointer + Send + Sync>,
        );
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(MockShardRecordProcessor::new())));
        let detector = crate::leases::shard_detector::MockShardDetector::new();
        let input = ProcessRecordsInput::builder().records(vec![]).build();
        let _task = make_task(input, processor, cp, Arc::new(detector), true);
        assert_eq!(Checkpointer::operation(&*store), "ProcessTask");
    }
}
