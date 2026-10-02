//! End-to-end consumer integration tests — ports of the Java
//! `application/*IntegrationTest.java` "release canary" suite:
//! `BasicStreamConsumerIntegrationTest`, `MultiStreamConsumerIntegrationTest`,
//! `ReshardIntegrationTest`, and `CrossAccountStreamConsumerIntegrationTest`.
//!
//! Each Java test wires a real [`Scheduler`] against Kinesis + DynamoDB +
//! CloudWatch via `TestConsumer`, produces records, consumes them through a
//! [`ShardRecordProcessor`], checkpoints, and validates delivery + ordering with
//! a `RecordValidatorQueue`. This file ports that scaffolding:
//!
//! * [`RecordValidatorQueue`] / [`RecordValidationStatus`] — the exact
//!   per-shard increasing-order + no-missing-record validator from
//!   `utils/RecordValidatorQueue.java`.
//! * [`RecordingProcessor`] / [`RecordingProcessorFactory`] — the port of
//!   `TestRecordProcessor` / `TestRecordProcessorFactory` (log + validate +
//!   `checkpoint()` on `process_records`, `shard_ended`, and
//!   `shutdown_requested`).
//! * [`put_records_with_retry`] — the port of `TestConsumer.putRecordsWithRetry`
//!   (each record's payload is the JSON-encoded monotonically increasing counter,
//!   matching Java's `wrapWithCounter(BigInteger)`), retrying partial failures.
//! * [`ReshardOption`] / [`scale_stream`] — the port of `utils/ReshardOptions`
//!   and `TestConsumer.StreamScaler` (SPLIT doubles / MERGE halves the open
//!   shard count via `UpdateShardCount`).
//! * [`TestConsumer::run`] — the produce → consume → assert → teardown driver.
//!
//! # Deviation from the Java timing model
//!
//! The Java `TestConsumer.run()` sleeps a fixed ~15 minutes to let a 4-shard
//! lease-table GSI come up and leases get assigned (its own TODO calls this out
//! as something to optimize). Here the driver instead **polls the validator
//! until all expected records are observed** (or a timeout elapses — default
//! 600s, overridable via `KCLRS_IT_AWAIT_SECS`), then triggers
//! `start_graceful_shutdown()`. This preserves the produce→consume→assert
//! contract while keeping the test bounded and deterministic against
//! LocalStack.
//!
//! Every test is `#[ignore]` (see the module doc in `common/mod.rs`) and uses a
//! `multi_thread` runtime because the Scheduler bridges sync↔async with
//! `block_in_place`/`spawn_blocking`. Run with `cargo test -p kcl -- --ignored`
//! (optionally `AWS_ENDPOINT_URL=...` to redirect to LocalStack).
//!
//! **Run the canaries serially against real AWS.** Each canary creates its own
//! stream(s) and lease table; cargo's default parallel test threads make 5
//! canaries create ~7 streams simultaneously and share account API quotas —
//! which both slows cold start (lease-table wait, shard sync, lease
//! assignment) and exposes freshly-created streams to data-plane propagation
//! races Java's sequential Failsafe run never sees. Prefer:
//!
//! ```bash
//! cargo test -p kcl --test application_consumer_it -- --ignored --test-threads=1
//! ```
//!
//! ## LocalStack / environment caveats
//!
//! * **Resharding** (`UpdateShardCount`) and **EFO** (`SubscribeToShard` +
//!   registered consumers) support varies by LocalStack tier/version; the
//!   reshard and streaming tests degrade gracefully (they log and continue
//!   rather than hard-fail) when the API is unavailable.
//! * **Cross-account** genuinely needs a second AWS account/role a single
//!   endpoint cannot model; the cross-account tests are structurally ported but
//!   gated behind the `KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN` env var (unset → skip),
//!   mirroring Java's `assumeTrue(getCrossAccountCredentialsProvider() != null)`.

mod common;

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};
use std::time::Duration;

use aws_sdk_kinesis::primitives::Blob;
use aws_sdk_kinesis::types::{PutRecordsRequestEntry, ScalingType};

use kcl::common::{
    ConfigsBuilder, InitialPositionInStream, InitialPositionInStreamExtended, StreamConfig,
    StreamIdentifier,
};
use kcl::coordinator::Scheduler;
use kcl::lifecycle::events::{
    InitializationInput, LeaseLostInput, ProcessRecordsInput, ShardEndedInput,
    ShutdownRequestedInput,
};
use kcl::processor::{
    FormerStreamsLeasesDeletionStrategy, NoLeaseDeletionStrategy, ShardRecordProcessor,
    ShardRecordProcessorFactory, SingleStreamTracker, StreamTracker,
};

use common::{
    cloudwatch_client, create_stream_and_wait, delete_stream_best_effort, delete_table_best_effort,
    dynamodb_client, kinesis_client, unique_table_name, RESOURCE_PREFIX,
};

// ===========================================================================
// RetrievalMode — port of `application/config/RetrievalMode.java`
// ===========================================================================

/// The two retrieval strategies the canary configs exercise. Port of the Java
/// `RetrievalMode` enum.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum RetrievalMode {
    /// Polling consumer (`GetRecords`) — Java `PollingConfig`.
    Polling,
    /// Enhanced fan-out streaming consumer (`SubscribeToShard`) — Java
    /// `FanOutConfig`.
    Streaming,
}

// ===========================================================================
// RecordValidationStatus + RecordValidatorQueue — ports of
// `utils/RecordValidationStatus.java` and `utils/RecordValidatorQueue.java`.
// ===========================================================================

/// Possible outcomes of record validation. Port of `RecordValidationStatus`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum RecordValidationStatus {
    OutOfOrder,
    MissingRecord,
    NoError,
}

/// Maps a per-shard key to the ordered list of record payloads processed by that
/// shard, and validates that (1) records within a shard are in non-decreasing
/// order (duplicates allowed) and (2) the total number of *unique* records over
/// all shards equals the number of records put on the stream(s).
///
/// Port of `utils/RecordValidatorQueue.java` (`ConcurrentHashMap` → a
/// `Mutex<HashMap>`; KCL calls the processor callbacks from multiple shard
/// threads).
#[derive(Clone, Default)]
struct RecordValidatorQueue {
    dict: Arc<Mutex<HashMap<String, Vec<String>>>>,
}

impl RecordValidatorQueue {
    fn new() -> Self {
        Self::default()
    }

    /// Java `add(shardId, data)`.
    fn add(&self, shard_key: &str, data: &str) {
        let mut dict = self.dict.lock().unwrap();
        dict.entry(shard_key.to_string())
            .or_default()
            .push(data.to_string());
    }

    /// Total number of unique records observed across all shards (diagnostic).
    fn unique_count(&self) -> usize {
        let dict = self.dict.lock().unwrap();
        dict.values()
            .flat_map(|records| records.iter())
            .cloned()
            .collect::<HashSet<_>>()
            .len()
    }

    /// Java `validateRecords(expectedRecordCount)`.
    fn validate_records(&self, expected_record_count: usize) -> RecordValidationStatus {
        let dict = self.dict.lock().unwrap();

        // 1. Each shard's records must be in non-decreasing order (dupes ok).
        for records_per_shard in dict.values() {
            let mut prev_val: i64 = -1;
            for record in records_per_shard {
                let next_val: i64 = record
                    .parse()
                    .expect("record payload should be an integer counter");
                if prev_val > next_val {
                    eprintln!(
                        "The records are not in increasing order. Saw record data {prev_val} before {next_val}."
                    );
                    return RecordValidationStatus::OutOfOrder;
                }
                prev_val = next_val;
            }
        }

        // 2. No records missing across all shards (unique count == expected).
        let actual_record_count: usize = dict
            .values()
            .map(|records| records.iter().cloned().collect::<HashSet<_>>().len())
            .sum();

        if actual_record_count != expected_record_count {
            eprintln!(
                "Failed to get correct number of records processed. Should be {expected_record_count} but was {actual_record_count}"
            );
            return RecordValidationStatus::MissingRecord;
        }

        RecordValidationStatus::NoError
    }
}

// ===========================================================================
// RecordingProcessor + factory — ports of `TestRecordProcessor.java` /
// `TestRecordProcessorFactory.java`.
// ===========================================================================

/// Port of `TestRecordProcessor`: on each batch it validates (records the
/// payload keyed by `streamIdentifier-shardId`) and checkpoints; it also
/// checkpoints at shard end and on shutdown-requested. Any error while
/// processing aborts (Java `Runtime.getRuntime().halt(1)` → `panic!`).
struct RecordingProcessor {
    stream_identifier: Option<StreamIdentifier>,
    shard_id: Option<String>,
    validator: RecordValidatorQueue,
}

impl RecordingProcessor {
    fn new(stream_identifier: Option<StreamIdentifier>, validator: RecordValidatorQueue) -> Self {
        Self {
            stream_identifier,
            shard_id: None,
            validator,
        }
    }

    /// The per-shard validator key: `<streamIdentifier>-<shardId>` (Java uses
    /// `streamIdentifier.toString() + "-" + shardId`; single-stream mode has no
    /// stream identifier, so it degrades to just the shard id).
    fn validator_key(&self) -> String {
        match &self.stream_identifier {
            Some(si) => format!(
                "{}-{}",
                si.serialize(),
                self.shard_id.as_deref().unwrap_or("")
            ),
            None => self.shard_id.clone().unwrap_or_default(),
        }
    }
}

impl ShardRecordProcessor for RecordingProcessor {
    fn initialize(&mut self, initialization_input: InitializationInput) {
        self.shard_id = initialization_input.shard_id().map(str::to_string);
        tracing::info!(
            "Initializing @ Sequence: {:?}",
            initialization_input.extended_sequence_number()
        );
    }

    fn process_records(&mut self, process_records_input: ProcessRecordsInput) {
        let records = process_records_input.records().unwrap_or(&[]);
        tracing::info!("Processing {} record(s)", records.len());
        let key = self.validator_key();
        for record in records {
            let data = record
                .data()
                .map(|b| String::from_utf8_lossy(b).to_string())
                .unwrap_or_default();
            // Java stores the raw JSON payload (a bare integer) verbatim.
            self.validator.add(&key, &data);
        }
        // Java: processRecordsInput.checkpointer().checkpoint();
        if let Some(checkpointer) = process_records_input.checkpointer() {
            if let Err(e) = checkpointer.checkpoint() {
                // Java aborts the JVM on any throwable here; we surface it.
                panic!("Caught error while processing records. Aborting. {e}");
            }
        }
    }

    fn lease_lost(&mut self, _lease_lost_input: LeaseLostInput) {
        tracing::info!("Lost lease, so terminating.");
    }

    fn shard_ended(&mut self, shard_ended_input: ShardEndedInput) {
        tracing::info!("Reached shard end checkpointing.");
        if let Err(e) = shard_ended_input.checkpointer().checkpoint() {
            tracing::error!("Exception while checkpointing at shard end. Giving up. {e}");
        }
    }

    fn shutdown_requested(&mut self, shutdown_requested_input: ShutdownRequestedInput) {
        tracing::info!("Scheduler is shutting down, checkpointing.");
        if let Err(e) = shutdown_requested_input.checkpointer().checkpoint() {
            tracing::error!("Exception while checkpointing at requested shutdown. Giving up. {e}");
        }
    }
}

/// Port of `TestRecordProcessorFactory`: hands each shard a fresh
/// [`RecordingProcessor`] sharing the one validator queue.
struct RecordingProcessorFactory {
    validator: RecordValidatorQueue,
}

impl RecordingProcessorFactory {
    fn new(validator: RecordValidatorQueue) -> Self {
        Self { validator }
    }
}

impl ShardRecordProcessorFactory for RecordingProcessorFactory {
    fn shard_record_processor(&self) -> Box<dyn ShardRecordProcessor + Send + Sync> {
        Box::new(RecordingProcessor::new(None, self.validator.clone()))
    }

    fn shard_record_processor_for_stream(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Box<dyn ShardRecordProcessor + Send + Sync> {
        Box::new(RecordingProcessor::new(
            Some(stream_identifier.clone()),
            self.validator.clone(),
        ))
    }
}

// ===========================================================================
// Multi-stream tracker — port of the anonymous `MultiStreamTracker` in
// `KCLAppConfig.getConfigsBuilder`.
// ===========================================================================

/// A [`StreamTracker`] over several streams, with a no-op former-streams
/// deletion strategy (Java `new FormerStreamsLeasesDeletionStrategy.NoLeaseDeletionStrategy()`).
struct TestMultiStreamTracker {
    stream_configs: Vec<StreamConfig>,
}

impl StreamTracker for TestMultiStreamTracker {
    fn stream_config_list(&self) -> Vec<StreamConfig> {
        self.stream_configs.clone()
    }

    fn former_streams_leases_deletion_strategy(
        &self,
    ) -> Box<dyn FormerStreamsLeasesDeletionStrategy + Send + Sync> {
        Box::new(NoLeaseDeletionStrategy)
    }

    fn is_multi_stream(&self) -> bool {
        true
    }
}

// ===========================================================================
// ReshardOption + StreamScaler — ports of `utils/ReshardOptions.java` and
// `TestConsumer.StreamScaler`.
// ===========================================================================

/// Port of `utils/ReshardOptions`: SPLIT doubles the shard count, MERGE halves
/// it.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum ReshardOption {
    Split,
    Merge,
}

impl ReshardOption {
    /// Java `calculateShardCount(currentShards)`.
    fn calculate_shard_count(self, current_shards: i32) -> i32 {
        match self {
            ReshardOption::Split => 2 * current_shards,
            ReshardOption::Merge => (0.5 * current_shards as f64) as i32,
        }
    }
}

/// Port of `TestConsumer.StreamScaler.scaleStream`: describe the stream summary,
/// compute the target open-shard count for the given factor, and issue an
/// `UpdateShardCount`. Returns `Ok(false)` (rather than failing the test) when
/// the endpoint does not support `UpdateShardCount` — LocalStack support varies
/// — so the reshard test can note-and-continue exactly as the Java scaler logs
/// and continues on error.
async fn scale_stream(
    client: &aws_sdk_kinesis::Client,
    stream_name: &str,
    factor: ReshardOption,
) -> Result<bool, String> {
    let response = client
        .describe_stream_summary()
        .stream_name(stream_name)
        .send()
        .await
        .map_err(|e| format!("describeStreamSummary failed: {e}"))?;
    let open_shard_count = response
        .stream_description_summary()
        .map(|s| s.open_shard_count())
        .unwrap_or(0);
    let target_shard_count = factor.calculate_shard_count(open_shard_count).max(1);

    tracing::info!(
        "Scaling stream {stream_name} from {open_shard_count} shards to {target_shard_count} shards w/ factor {factor:?}"
    );

    match client
        .update_shard_count()
        .stream_name(stream_name)
        .target_shard_count(target_shard_count)
        .scaling_type(ScalingType::UniformScaling)
        .send()
        .await
    {
        Ok(_) => Ok(true),
        Err(e) => {
            // Java logs the error and continues; we report it so the driver can
            // note-and-continue (LocalStack may not support UpdateShardCount).
            Err(format!("updateShardCount not supported / failed: {e}"))
        }
    }
}

// ===========================================================================
// Record producer — port of `TestConsumer.putRecordsWithRetry` /
// `wrapWithCounter`.
// ===========================================================================

/// Number of records put per stream per publish call (Java
/// `NUM_RECORDS_PUT_PER_STREAM`).
const NUM_RECORDS_PUT_PER_STREAM: usize = 100;

/// Encode the counter exactly as Java's `wrapWithCounter(BigInteger)` does:
/// Jackson serializes a `BigInteger` as its decimal digits with no quotes, so
/// the payload bytes are the ASCII decimal string.
fn wrap_with_counter(counter: u64) -> Vec<u8> {
    counter.to_string().into_bytes()
}

/// A small random alphabetic partition key (Java
/// `RandomStringUtils.randomAlphabetic(5, 20)`).
fn random_partition_key() -> String {
    use rand::RngExt;
    let mut rng = rand::rng();
    let len = rng.random_range(5..20);
    (0..len)
        .map(|_| {
            let c = rng.random_range(0..52);
            if c < 26 {
                (b'a' + c) as char
            } else {
                (b'A' + (c - 26)) as char
            }
        })
        .collect()
}

/// Whole-call PutRecords failures worth retrying on a *fresh* stream: a stream
/// can be describable-ACTIVE while briefly not yet data-plane visible
/// (`ResourceNotFoundException`), and parallel canaries sharing account quotas
/// can throttle.
fn is_transient_put_records_error(
    e: &aws_sdk_kinesis::error::SdkError<
        aws_sdk_kinesis::operation::put_records::PutRecordsError,
        aws_smithy_runtime_api::http::Response,
    >,
) -> bool {
    match e.as_service_error() {
        Some(se) => {
            se.is_resource_not_found_exception()
                || se.is_provisioned_throughput_exceeded_exception()
                || se.is_kms_throttling_exception()
                || matches!(
                    se.meta().code(),
                    Some("LimitExceededException" | "ThrottlingException")
                )
        }
        // Dispatch/timeout-level failures (connection reset etc.) are also
        // worth retrying under the deadline.
        None => true,
    }
}

/// Port of `TestConsumer.putRecordsWithRetry`: build `record_count` entries with
/// increasing-counter payloads and PutRecords them, retrying any partially
/// failed records. Returns the updated payload counter.
///
/// Deviation from Java (which tolerates no whole-call errors): transient
/// whole-call failures ([`is_transient_put_records_error`]) are retried with a
/// 2s backoff under a 90s deadline, because the ported canaries create their
/// streams seconds before publishing (Java's sequential Failsafe run gives
/// streams far longer to propagate).
async fn put_records_with_retry(
    client: &aws_sdk_kinesis::Client,
    stream_name: &str,
    record_count: usize,
    mut payload_counter: u64,
) -> u64 {
    let mut records_pending: Vec<PutRecordsRequestEntry> = Vec::with_capacity(record_count);
    for _ in 0..record_count {
        let entry = PutRecordsRequestEntry::builder()
            .partition_key(random_partition_key())
            .data(Blob::new(wrap_with_counter(payload_counter)))
            .build()
            .expect("PutRecordsRequestEntry builder");
        records_pending.push(entry);
        payload_counter += 1;
    }

    let put_deadline = tokio::time::Instant::now() + Duration::from_secs(90);
    while !records_pending.is_empty() {
        let response = match client
            .put_records()
            .stream_name(stream_name)
            .set_records(Some(records_pending.clone()))
            .send()
            .await
        {
            Ok(response) => response,
            Err(e)
                if is_transient_put_records_error(&e)
                    && tokio::time::Instant::now() < put_deadline =>
            {
                tracing::warn!("putRecords({stream_name}) failed transiently; retrying in 2s: {e}");
                tokio::time::sleep(Duration::from_secs(2)).await;
                continue;
            }
            Err(e) => panic!(
                "putRecords({stream_name}) failed (after retrying transient errors \
                 for up to 90s): {e:?}"
            ),
        };

        let mut failed: Vec<PutRecordsRequestEntry> = Vec::new();
        for (i, result) in response.records().iter().enumerate() {
            if result.error_code().is_some() {
                failed.push(records_pending[i].clone());
            }
        }
        records_pending = failed;
        if !records_pending.is_empty() {
            tracing::info!(
                "For stream {stream_name}: {} records failed and will be retried.",
                records_pending.len()
            );
            // Don't hot-loop against a throttling stream.
            tokio::time::sleep(Duration::from_millis(200)).await;
        }
    }
    tracing::info!(
        "For stream {stream_name}: all {record_count} records published. Payload counter is now {payload_counter}."
    );
    payload_counter
}

/// Render a scheduler-task [`JoinError`](tokio::task::JoinError), extracting the
/// panic payload when there is one.
fn join_error_message(e: tokio::task::JoinError) -> String {
    if e.is_panic() {
        let payload = e.into_panic();
        if let Some(s) = payload.downcast_ref::<&str>() {
            format!("panicked: {s}")
        } else if let Some(s) = payload.downcast_ref::<String>() {
            format!("panicked: {s}")
        } else {
            "panicked (non-string payload)".to_string()
        }
    } else {
        format!("{e}")
    }
}

/// Fail fast if the scheduler task has already exited: a `JoinHandle` that is
/// finished mid-run means initialization failed (the run loop logs and shuts
/// down) or the task panicked — either way the real cause would otherwise be
/// masked as a `MissingRecord` validation error.
async fn ensure_scheduler_alive(handle: &mut tokio::task::JoinHandle<()>) -> Result<(), String> {
    if !handle.is_finished() {
        return Ok(());
    }
    Err(match handle.await {
        Ok(()) => "scheduler exited early — initialization likely failed after retries \
                   (see the Scheduler:Initialize error in the captured logs)"
            .to_string(),
        Err(join_err) => format!("scheduler task died: {}", join_error_message(join_err)),
    })
}

// ===========================================================================
// TestConsumer — port of `application/TestConsumer.java`.
// ===========================================================================

/// The consumer config for one canary run — the shape of a `KCLAppConfig`
/// subclass (test name, stream count, retrieval mode, optional reshard factors).
struct ConsumerConfig {
    /// Human-readable test/application label (Java `getTestName`).
    test_name: String,
    /// Base stream name (each stream gets a unique suffix).
    stream_base_name: String,
    /// Number of streams (1 = single-stream, >1 = multi-stream tracker).
    num_streams: usize,
    /// Shards per stream at creation (Java `getShardCount`, default 4).
    shard_count: i32,
    /// Polling vs streaming retrieval.
    retrieval_mode: RetrievalMode,
    /// Reshard factors applied mid-run (Java `getReshardFactorList`); empty = no
    /// reshard.
    reshard_factors: Vec<ReshardOption>,
}

impl ConsumerConfig {
    fn is_multi_stream(&self) -> bool {
        self.num_streams > 1
    }
}

/// Owns the streams + lease table for one run and drives the produce → consume →
/// assert → teardown flow (port of `TestConsumer`).
struct TestConsumer {
    config: ConsumerConfig,
    run_id: String,
    application_name: String,
    lease_table_name: String,
    stream_names: Vec<String>,
    kinesis: aws_sdk_kinesis::Client,
    dynamodb: aws_sdk_dynamodb::Client,
    cloudwatch: aws_sdk_cloudwatch::Client,
    validator: RecordValidatorQueue,
    /// Total records put across all streams (Java `payloadCounter`, aggregated).
    payload_counter: u64,
}

impl TestConsumer {
    async fn new(config: ConsumerConfig) -> Self {
        let run_id = uuid::Uuid::new_v4().simple().to_string();
        // Java: applicationName = RESOURCE_PREFIX_<testId>_<testName>. We use the
        // shared harness prefix so leaked tables are swept the same way, and keep
        // the lease-table name unique per run.
        let application_name = format!("{RESOURCE_PREFIX}{}-{}", config.test_name, run_id);
        let lease_table_name = unique_table_name(&format!("app-{}", config.test_name));
        let stream_names: Vec<String> = (0..config.num_streams)
            .map(|i| {
                format!(
                    "{RESOURCE_PREFIX}{}-{}-s{i}",
                    config.stream_base_name, run_id
                )
            })
            .collect();

        Self {
            config,
            run_id,
            application_name,
            lease_table_name,
            stream_names,
            kinesis: kinesis_client().await,
            dynamodb: dynamodb_client().await,
            cloudwatch: cloudwatch_client().await,
            validator: RecordValidatorQueue::new(),
            payload_counter: 0,
        }
    }

    /// Port of `TestConsumer.run()` (adapted timing — see module docs). Produces,
    /// consumes until all records are seen or a timeout elapses, optionally
    /// reshards + produces again, then gracefully shuts down and validates. Always
    /// tears down resources (best-effort) at the end.
    async fn run(mut self) {
        let outcome = self.run_inner().await;
        self.delete_resources().await;
        outcome.expect("consumer run failed");
    }

    async fn run_inner(&mut self) -> Result<(), String> {
        // 1. Create streams (Java StreamExistenceManager.checkStreamsAndCreateIfNecessary).
        for stream_name in &self.stream_names {
            create_stream_and_wait(&self.kinesis, stream_name, self.config.shard_count).await;
        }

        // 2. Set up KCL configs + Scheduler (Java setUpConsumerResources).
        let scheduler = self.build_scheduler().await?;

        // 3. Publish the initial batch of records (Java publishRecords).
        self.publish_records(NUM_RECORDS_PUT_PER_STREAM).await;

        // 4. Start the consumer (Java startConsumer → scheduler runs on its executor).
        let mut handle = scheduler.start();

        // 5. Wait for all initial records to be consumed (adapted from Java's
        //    fixed 15-minute sleep; poll the validator instead — budget via
        //    KCLRS_IT_AWAIT_SECS, see common::await_records_timeout).
        self.await_records(
            self.payload_counter as usize,
            common::await_records_timeout(),
        )
        .await;
        ensure_scheduler_alive(&mut handle).await?;

        // 6. Reshard mid-run if configured (Java performStreamScale + restart producer).
        if !self.config.reshard_factors.is_empty() {
            let factors = self.config.reshard_factors.clone();
            let mut any_scaled = false;
            for factor in factors {
                for stream_name in self.stream_names.clone() {
                    match scale_stream(&self.kinesis, &stream_name, factor).await {
                        Ok(true) => any_scaled = true,
                        Ok(false) => {}
                        Err(e) => tracing::warn!("Reshard step skipped for {stream_name}: {e}"),
                    }
                }
                // Give resharding a moment to settle, then produce across the new
                // shard topology (Java restarts the producer at 10s intervals).
                tokio::time::sleep(Duration::from_secs(10)).await;
                self.publish_records(NUM_RECORDS_PUT_PER_STREAM).await;
            }
            if !any_scaled {
                tracing::warn!(
                    "No reshard operation succeeded (endpoint may not support UpdateShardCount); \
                     continuing with the pre-reshard topology."
                );
            }
            // Consume the post-reshard records (across child shards when scaled).
            self.await_records(
                self.payload_counter as usize,
                common::await_records_timeout(),
            )
            .await;
            ensure_scheduler_alive(&mut handle).await?;
        }

        // 7. Brief settle, then graceful shutdown (Java sleep 30s + awaitConsumerFinish).
        tokio::time::sleep(Duration::from_secs(2)).await;
        self.await_consumer_finish(&scheduler).await;
        // Drive the worker loop to completion so tasks are torn down — and
        // surface a panicked scheduler task instead of masking it as a
        // record-validation failure.
        match tokio::time::timeout(Duration::from_secs(30), &mut handle).await {
            Ok(Ok(())) => {}
            Ok(Err(join_err)) => {
                return Err(format!(
                    "scheduler task died during shutdown: {}",
                    join_error_message(join_err)
                ));
            }
            Err(_) => tracing::warn!("Scheduler loop did not exit within 30s of shutdown."),
        }

        // 8. Validate (Java validateRecordProcessor).
        self.validate_record_processor()
    }

    /// Port of `setUpConsumerResources`: build the `ConfigsBuilder`, apply the
    /// polling/streaming retrieval config + TRIM_HORIZON initial position, and
    /// construct the `Scheduler`.
    async fn build_scheduler(&self) -> Result<Arc<Scheduler>, String> {
        let worker_id = format!("worker-{}", self.run_id);
        let factory = Arc::new(RecordingProcessorFactory::new(self.validator.clone()));

        let trim_horizon = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );

        let configs_builder = if self.config.is_multi_stream() {
            // Multi-stream: build a StreamConfig per stream from its ARN +
            // creation epoch (Java StreamIdentifier.multiStreamInstance).
            let mut stream_configs = Vec::with_capacity(self.stream_names.len());
            for stream_name in &self.stream_names {
                let (arn, creation_epoch) = self.describe_stream_arn_and_epoch(stream_name).await?;
                let identifier =
                    StreamIdentifier::multi_stream_instance_from_arn(arn, creation_epoch);
                stream_configs.push(StreamConfig::new(identifier, trim_horizon));
            }
            let tracker = Arc::new(TestMultiStreamTracker { stream_configs });
            ConfigsBuilder::new(
                tracker,
                self.application_name.clone(),
                self.kinesis.clone(),
                self.dynamodb.clone(),
                self.cloudwatch.clone(),
                worker_id,
                factory,
            )
        } else {
            // Single-stream: the initial position that governs shard-sync lease
            // checkpoints and the consumer start lives on the stream tracker's
            // StreamConfig (Java KCLAppConfig builds a SingleStreamTracker with
            // an explicit TRIM_HORIZON StreamConfig; `from_stream_name` would
            // default to LATEST and skip records published before startup).
            ConfigsBuilder::new(
                Arc::new(SingleStreamTracker::from_stream_name_with_position(
                    &self.stream_names[0],
                    trim_horizon,
                )),
                self.application_name.clone(),
                self.kinesis.clone(),
                self.dynamodb.clone(),
                self.cloudwatch.clone(),
                worker_id,
                factory,
            )
        }
        .set_table_name(self.lease_table_name.clone());

        // Retrieval config: polling → PollingConfig; streaming → default FanOut.
        let mut retrieval_config = configs_builder.retrieval_config();
        match self.config.retrieval_mode {
            RetrievalMode::Polling => {
                retrieval_config.set_retrieval_specific_config(Box::new(
                    kcl::retrieval::polling::PollingConfig::new(self.kinesis.clone()),
                ));
            }
            RetrievalMode::Streaming => {
                // Default FanOutConfig (Java: configsBuilder.retrievalConfig() with
                // no override registers/uses an EFO consumer). Left as the builder
                // default, which lazily creates a FanOutConfig.
            }
        }

        // The initial position lives on the stream tracker's StreamConfig
        // (set above); the lease-management config needs no position knob.
        let lease_management_config = configs_builder.lease_management_config();

        Scheduler::new(
            configs_builder.checkpoint_config(),
            configs_builder.coordinator_config(),
            lease_management_config,
            configs_builder.lifecycle_config(),
            configs_builder.metrics_config(),
            configs_builder.processor_config(),
            retrieval_config,
        )
        .map_err(|e| format!("Scheduler::new failed: {e}"))
    }

    /// Fetch a stream's ARN + creation-epoch millis via DescribeStreamSummary
    /// (Java `getCreationEpoch`, needed for multi-stream `StreamIdentifier`s).
    async fn describe_stream_arn_and_epoch(
        &self,
        stream_name: &str,
    ) -> Result<(kcl::common::Arn, i64), String> {
        let response = self
            .kinesis
            .describe_stream_summary()
            .stream_name(stream_name)
            .send()
            .await
            .map_err(|e| format!("describeStreamSummary({stream_name}) failed: {e}"))?;
        let summary = response
            .stream_description_summary()
            .ok_or_else(|| format!("no stream description summary for {stream_name}"))?;
        let arn = kcl::common::Arn::from_string(summary.stream_arn())
            .map_err(|e| format!("invalid stream ARN {}: {e}", summary.stream_arn()))?;
        let creation_epoch = summary.stream_creation_timestamp().to_millis().unwrap_or(0);
        Ok((arn, creation_epoch))
    }

    /// Port of `publishRecords`: put `per_stream` records to every stream,
    /// advancing the shared payload counter.
    async fn publish_records(&mut self, per_stream: usize) {
        for stream_name in self.stream_names.clone() {
            tracing::info!("Publishing {per_stream} records for stream {stream_name}");
            self.payload_counter = put_records_with_retry(
                &self.kinesis,
                &stream_name,
                per_stream,
                self.payload_counter,
            )
            .await;
        }
    }

    /// Poll the validator until `expected` unique records are observed or the
    /// timeout elapses (adapted from Java's fixed 15-minute sleep — see module
    /// docs). Does not assert; the final validation is done by
    /// [`validate_record_processor`].
    async fn await_records(&self, expected: usize, timeout: Duration) {
        let start = tokio::time::Instant::now();
        let deadline = start + timeout;
        let mut last_progress_log = start;
        loop {
            let now = tokio::time::Instant::now();
            let seen = self.validator.unique_count();
            if seen >= expected {
                tracing::info!("Observed {seen}/{expected} records.");
                return;
            }
            if now >= deadline {
                tracing::warn!(
                    "Timed out awaiting records after {}s: observed {seen}/{expected} \
                     (validation will report the shortfall).",
                    timeout.as_secs()
                );
                return;
            }
            if now - last_progress_log >= Duration::from_secs(30) {
                tracing::info!(
                    "Still awaiting records: observed {seen}/{expected} after {}s.",
                    (now - start).as_secs()
                );
                last_progress_log = now;
            }
            tokio::time::sleep(Duration::from_secs(2)).await;
        }
    }

    /// Port of `awaitConsumerFinish`: request graceful shutdown, wait up to 20s;
    /// fall back to a hard `shutdown()` on timeout/error.
    async fn await_consumer_finish(&self, scheduler: &Arc<Scheduler>) {
        let shutdown_future = scheduler.start_graceful_shutdown();
        tracing::info!("Waiting up to 20 seconds for shutdown to complete.");
        match tokio::time::timeout(Duration::from_secs(20), shutdown_future).await {
            Ok(Ok(Ok(_))) => tracing::info!("Graceful shutdown completed."),
            Ok(_) | Err(_) => {
                tracing::info!("Graceful shutdown did not complete; forcing shutdown.");
                scheduler.shutdown().await;
            }
        }
    }

    /// Port of `validateRecordProcessor`.
    fn validate_record_processor(&self) -> Result<(), String> {
        let expected = self.payload_counter as usize;
        tracing::info!("The number of expected records is: {expected}");
        match self.validator.validate_records(expected) {
            RecordValidationStatus::NoError => {
                tracing::info!("Completed validation of processed records.");
                Ok(())
            }
            status => Err(format!(
                "There was an error validating the records that were processed: {status:?}"
            )),
        }
    }

    /// Port of `deleteResources`: delete streams + the lease table (best-effort).
    async fn delete_resources(&self) {
        for stream_name in &self.stream_names {
            tracing::info!("Deleting stream {stream_name}");
            delete_stream_best_effort(&self.kinesis, stream_name).await;
        }
        tracing::info!("Deleting lease table {}", self.lease_table_name);
        delete_table_best_effort(&self.dynamodb, &self.lease_table_name).await;
    }
}

// ===========================================================================
// Tests — ports of the four `application/*IntegrationTest.java` classes.
// ===========================================================================

/// Port of `BasicStreamConsumerIntegrationTest.kclReleaseCanaryPollingH2Test`:
/// a single-stream polling consumer produces N records, consumes all, and
/// validates count + ordering. (Java's H1 variant is `@Ignore`d; the HTTP
/// protocol is a client-transport detail with no bearing on the Rust SDK, so it
/// is not ported.)
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_polling_h2_test() {
    common::init_test_tracing();
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "PollingH2Test".to_string(),
        stream_base_name: "PollingH2TestStream".to_string(),
        num_streams: 1,
        shard_count: 4,
        retrieval_mode: RetrievalMode::Polling,
        reshard_factors: vec![],
    })
    .await;
    consumer.run().await;
}

/// Port of `BasicStreamConsumerIntegrationTest.kclReleaseCanaryStreamingTest`:
/// a single-stream EFO (streaming) consumer. Java `@Ignore`s this in the canary
/// suite; ported here as `#[ignore]` like the rest. EFO/`SubscribeToShard`
/// support varies by LocalStack tier — if unsupported the Scheduler receives no
/// data and validation reports the shortfall.
#[ignore = "integration: runs against AWS; EFO/SubscribeToShard support varies (LocalStack tier)"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_streaming_test() {
    common::init_test_tracing();
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "StreamingTest".to_string(),
        stream_base_name: "StreamingTestStream".to_string(),
        num_streams: 1,
        shard_count: 4,
        retrieval_mode: RetrievalMode::Streaming,
        reshard_factors: vec![],
    })
    .await;
    consumer.run().await;
}

/// Port of `MultiStreamConsumerIntegrationTest.kclReleaseCanaryMultiStreamPollingTest`:
/// a two-stream polling consumer (multi-stream lease tracker).
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_multi_stream_polling_test() {
    common::init_test_tracing();
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "MultiStreamPollingH2Test".to_string(),
        stream_base_name: "MultiStreamPollingH2TestStream".to_string(),
        num_streams: 2,
        shard_count: 4,
        retrieval_mode: RetrievalMode::Polling,
        reshard_factors: vec![],
    })
    .await;
    consumer.run().await;
}

/// Port of `MultiStreamConsumerIntegrationTest.kclReleaseCanaryMultiStreamStreamingTest`:
/// a two-stream EFO (streaming) consumer.
#[ignore = "integration: runs against AWS; EFO/SubscribeToShard support varies (LocalStack tier)"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_multi_stream_streaming_test() {
    common::init_test_tracing();
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "MultiStreamStreamingTest".to_string(),
        stream_base_name: "MultiStreamStreamingTestStream".to_string(),
        num_streams: 2,
        shard_count: 4,
        retrieval_mode: RetrievalMode::Streaming,
        reshard_factors: vec![],
    })
    .await;
    consumer.run().await;
}

/// Port of `ReshardIntegrationTest.kclReleaseCanaryStreamingReshardingTest`:
/// produce, then SPLIT and MERGE the stream mid-run and verify consumption
/// continues across the child shards. Java starts with 20 shards; scaled down
/// here to keep the LocalStack run bounded. Resharding (`UpdateShardCount`)
/// support varies by LocalStack tier — the driver notes-and-continues if a scale
/// step is unsupported (mirroring the Java scaler which logs and continues).
#[ignore = "integration: runs against AWS; UpdateShardCount (resharding) support varies (LocalStack tier)"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_streaming_resharding_test() {
    common::init_test_tracing();
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "StreamingReshardingTest".to_string(),
        stream_base_name: "StreamingReshardingTestStream".to_string(),
        num_streams: 1,
        // Java uses 20; a smaller start keeps SPLIT→MERGE bounded on LocalStack.
        shard_count: 4,
        // Java's reshard test is streaming; use polling to be robust when EFO is
        // unavailable — resharding behavior (child-shard consumption) is what is
        // under test, independent of the retrieval transport.
        retrieval_mode: RetrievalMode::Polling,
        reshard_factors: vec![ReshardOption::Split, ReshardOption::Merge],
    })
    .await;
    consumer.run().await;
}

// ---------------------------------------------------------------------------
// CrossAccountStreamConsumerIntegrationTest — structurally ported but gated.
//
// The Java cross-account tests differ from the same-account tests only in that
// the *stream owner* client uses a second account's credentials (via
// `-DawsCrossAccountProfile`) and, for EFO, the consumer is registered
// cross-account. `TestConsumer.run()` opens with
// `assumeTrue(getCrossAccountCredentialsProvider() != null)` — i.e. the test is
// SKIPPED when no cross-account credentials are configured.
//
// A single AWS endpoint (one LocalStack, or one account's credential chain)
// cannot model two distinct accounts + a cross-account role assumption, so this
// is gated behind `KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN`. When unset, the test skips
// (the faithful port of the Java `assumeTrue`). When set, it runs the same
// produce→consume→assert flow (the cross-account wiring — assuming the role for
// the producer client — is documented as deferred since it needs real
// two-account infrastructure).
// ---------------------------------------------------------------------------

/// Returns `Some(role_arn)` if a cross-account role is configured, else `None`
/// (Java `getCrossAccountCredentialsProvider()`).
fn cross_account_role_arn() -> Option<String> {
    std::env::var("KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN")
        .ok()
        .filter(|s| !s.is_empty())
}

/// Port of `CrossAccountStreamConsumerIntegrationTest.kclReleaseCanaryCrossAccountPollingH2Test`:
/// single-stream polling, but with the stream owned by a second account. Gated —
/// skips unless `KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN` is set (the Java `assumeTrue`).
#[ignore = "integration: cross-account; needs a second account/role — set KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_cross_account_polling_h2_test() {
    common::init_test_tracing();
    if cross_account_role_arn().is_none() {
        eprintln!(
            "SKIP kcl_release_canary_cross_account_polling_h2_test: no cross-account role configured \
             (set KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN). Mirrors the Java assumeTrue guard."
        );
        return;
    }
    // With a real second account the flow is identical to the single-stream
    // polling test, differing only in the producer/stream-owner client's
    // credentials. Cross-account client wiring is deferred (needs real
    // two-account infra); run the standard flow so the code path is exercised.
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "CrossAccountPollingH2Test".to_string(),
        stream_base_name: "CrossAccountPollingH2TestStream".to_string(),
        num_streams: 1,
        shard_count: 4,
        retrieval_mode: RetrievalMode::Polling,
        reshard_factors: vec![],
    })
    .await;
    consumer.run().await;
}

/// Port of `CrossAccountStreamConsumerIntegrationTest.kclReleaseCanaryCrossAccountStreamingTest`:
/// single-stream EFO, cross-account. Gated (see above).
#[ignore = "integration: cross-account; needs a second account/role — set KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_cross_account_streaming_test() {
    common::init_test_tracing();
    if cross_account_role_arn().is_none() {
        eprintln!(
            "SKIP kcl_release_canary_cross_account_streaming_test: no cross-account role configured \
             (set KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN)."
        );
        return;
    }
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "CrossAccountStreamingTest".to_string(),
        stream_base_name: "CrossAccountStreamingTestStream".to_string(),
        num_streams: 1,
        shard_count: 4,
        retrieval_mode: RetrievalMode::Streaming,
        reshard_factors: vec![],
    })
    .await;
    consumer.run().await;
}

/// Port of `CrossAccountStreamConsumerIntegrationTest.kclReleaseCanaryCrossAccountMultiStreamStreamingTest`:
/// two-stream EFO, cross-account. Gated (see above).
#[ignore = "integration: cross-account; needs a second account/role — set KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_cross_account_multi_stream_streaming_test() {
    common::init_test_tracing();
    if cross_account_role_arn().is_none() {
        eprintln!(
            "SKIP kcl_release_canary_cross_account_multi_stream_streaming_test: no cross-account role \
             configured (set KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN)."
        );
        return;
    }
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "CrossAccountMultiStreamStreamingTest".to_string(),
        stream_base_name: "CrossAccountMultiStreamStreamingTestStream".to_string(),
        num_streams: 2,
        shard_count: 4,
        retrieval_mode: RetrievalMode::Streaming,
        reshard_factors: vec![],
    })
    .await;
    consumer.run().await;
}

/// Port of `CrossAccountStreamConsumerIntegrationTest.kclReleaseCanaryCrossAccountMultiStreamPollingH2Test`:
/// two-stream polling, cross-account. Gated (see above).
#[ignore = "integration: cross-account; needs a second account/role — set KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN"]
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn kcl_release_canary_cross_account_multi_stream_polling_h2_test() {
    common::init_test_tracing();
    if cross_account_role_arn().is_none() {
        eprintln!(
            "SKIP kcl_release_canary_cross_account_multi_stream_polling_h2_test: no cross-account role \
             configured (set KCLRS_IT_CROSS_ACCOUNT_ROLE_ARN)."
        );
        return;
    }
    let consumer = TestConsumer::new(ConsumerConfig {
        test_name: "CrossAccountMultiStreamPollingH2Test".to_string(),
        stream_base_name: "CrossAccountMultiStreamPollingH2TestStream".to_string(),
        num_streams: 2,
        shard_count: 4,
        retrieval_mode: RetrievalMode::Polling,
        reshard_factors: vec![],
    })
    .await;
    consumer.run().await;
}

// ===========================================================================
// Offline unit coverage for the pure helper logic (runs in the default suite —
// no AWS). Validates the RecordValidatorQueue + ReshardOption ports match Java.
// ===========================================================================

#[cfg(test)]
mod helper_tests {
    use super::*;

    #[test]
    fn validator_accepts_in_order_complete() {
        let v = RecordValidatorQueue::new();
        for i in 0..5 {
            v.add("shard-0", &i.to_string());
        }
        assert_eq!(v.validate_records(5), RecordValidationStatus::NoError);
        assert_eq!(v.unique_count(), 5);
    }

    #[test]
    fn validator_allows_duplicates_within_shard() {
        let v = RecordValidatorQueue::new();
        v.add("shard-0", "0");
        v.add("shard-0", "0");
        v.add("shard-0", "1");
        // Two unique records; duplicates allowed and not counted twice.
        assert_eq!(v.validate_records(2), RecordValidationStatus::NoError);
    }

    #[test]
    fn validator_flags_out_of_order() {
        let v = RecordValidatorQueue::new();
        v.add("shard-0", "5");
        v.add("shard-0", "2");
        assert_eq!(v.validate_records(2), RecordValidationStatus::OutOfOrder);
    }

    #[test]
    fn validator_flags_missing_record() {
        let v = RecordValidatorQueue::new();
        v.add("shard-0", "0");
        v.add("shard-0", "1");
        assert_eq!(v.validate_records(5), RecordValidationStatus::MissingRecord);
    }

    #[test]
    fn validator_spans_multiple_shards() {
        let v = RecordValidatorQueue::new();
        v.add("shard-0", "0");
        v.add("shard-0", "1");
        v.add("shard-1", "2");
        v.add("shard-1", "3");
        assert_eq!(v.validate_records(4), RecordValidationStatus::NoError);
    }

    #[test]
    fn reshard_split_doubles_and_merge_halves() {
        assert_eq!(ReshardOption::Split.calculate_shard_count(4), 8);
        assert_eq!(ReshardOption::Merge.calculate_shard_count(4), 2);
        assert_eq!(ReshardOption::Merge.calculate_shard_count(1), 0);
    }

    #[test]
    fn wrap_with_counter_is_decimal_ascii() {
        assert_eq!(wrap_with_counter(0), b"0");
        assert_eq!(wrap_with_counter(12345), b"12345");
    }

    #[test]
    fn random_partition_key_is_alphabetic_and_bounded() {
        for _ in 0..50 {
            let k = random_partition_key();
            assert!((5..20).contains(&k.len()), "len {} out of range", k.len());
            assert!(k.chars().all(|c| c.is_ascii_alphabetic()));
        }
    }
}
