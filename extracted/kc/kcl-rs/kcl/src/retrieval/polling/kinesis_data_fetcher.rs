//! Port of `software.amazon.kinesis.retrieval.polling.KinesisDataFetcher`.
//!
//! Stateful per-shard polling iterator manager over the async
//! `aws_sdk_kinesis::Client`. Owns the current shard-iterator state machine,
//! issues `GetShardIterator`/`GetRecords`, tracks shard-end and last-known
//! sequence number, and records per-call metrics.
//!
//! # Async / interior-mutability deviation
//!
//! Java blocks over the async SDK client and mutates fields with no
//! synchronization (single-threaded use). The Rust port stays async and, because
//! a [`KinesisDataFetcher`] is shared behind an `Arc<dyn DataFetcher>`, guards its
//! mutable iterator state with a `std::sync::Mutex` (short critical sections,
//! never held across `.await`): the async I/O reads state under the lock,
//! releases it, awaits the SDK call, then re-locks to commit. The prefetch task
//! drives it serially, matching the Java single-thread invariant.
//!
//! # Deviations
//!
//! * The `streamId` request field is populated via
//!   [`StreamIdCache::try_get_for`] (Java `StreamIdCache.get(streamIdentifier)`).
//!   It yields `None` until the Scheduler initializes the process-global cache
//!   (or in unit tests that never initialize it), leaving the field unset — the
//!   common uninitialized path. This is the retrieval side of the StreamIdCache
//!   async→sync bridge seam.
//! * `getShardIterator`/`getRecords` use `tokio::time::timeout` with the
//!   configured `kinesis_request_timeout`, mirroring Java's
//!   `resolveOrCancelFuture(..., maxFutureWait)` → `TimeoutException` →
//!   [`FetchError::Retryable`].

use std::sync::{Arc, Mutex};
use std::time::Duration;

use async_trait::async_trait;
use aws_sdk_kinesis::operation::get_records::GetRecordsOutput;
use aws_smithy_types::error::display::DisplayErrorContext;

use crate::common::InitialPositionInStreamExtended;
use crate::common::StreamIdentifier;
use crate::coordinator::stream_info::StreamIdCache;
use crate::metrics::{self, MetricsFactory, MetricsLevel};
use crate::retrieval::data_retrieval_util::is_valid_result;
use crate::retrieval::get_records_response_adapter::GetRecordsResponseAdapter;
use crate::retrieval::iterator_builder;
use crate::retrieval::kinesis_get_records_response_adapter::KinesisGetRecordsResponseAdapter;
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::polling::data_fetcher::{DataFetcher, DataFetcherResult, FetchError};

const METRICS_PREFIX: &str = "KinesisDataFetcher";
const OPERATION: &str = "ProcessTask";

/// Current wall-clock milliseconds (Java `System.currentTimeMillis()`).
fn now_millis() -> i64 {
    chrono::Utc::now().timestamp_millis()
}

/// Mutable iterator state, guarded by a `Mutex`.
#[derive(Default)]
struct FetcherState {
    next_iterator: Option<String>,
    is_shard_end_reached: bool,
    is_initialized: bool,
    last_known_sequence_number: Option<String>,
    initial_position_in_stream: Option<InitialPositionInStreamExtended>,
}

/// Stateful per-shard polling data fetcher over `aws_sdk_kinesis::Client`.
pub struct KinesisDataFetcher {
    kinesis_client: aws_sdk_kinesis::Client,
    stream_identifier: StreamIdentifier,
    shard_id: String,
    max_records: i32,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    max_future_wait: Duration,
    stream_and_shard_id: String,
    /// The EFO consumer id, if any. Retained for parity with Java (which threads
    /// it into request building / user-agent); the per-request user-agent override
    /// is applied at the client level, so this is not read per-request here.
    #[allow(dead_code)]
    consumer_id: Option<String>,
    state: Arc<Mutex<FetcherState>>,
}

impl KinesisDataFetcher {
    /// Construct from a Kinesis client + a
    /// [`DataFetcherProviderConfig`](crate::retrieval::DataFetcherProviderConfig).
    pub fn new(
        kinesis_client: aws_sdk_kinesis::Client,
        config: &dyn crate::retrieval::DataFetcherProviderConfig,
    ) -> Self {
        let consumer = config.consumer_id();
        let consumer_id = (!consumer.is_empty()).then(|| consumer.to_string());
        let stream_identifier = config.stream_identifier().clone();
        let shard_id = config.shard_id().to_string();
        let stream_and_shard_id = format!("{}:{}", stream_identifier.serialize(), shard_id);
        Self {
            kinesis_client,
            stream_identifier,
            shard_id,
            max_records: config.max_records(),
            metrics_factory: config.metrics_factory(),
            max_future_wait: config.kinesis_request_timeout(),
            stream_and_shard_id,
            consumer_id,
            state: Arc::new(Mutex::new(FetcherState::default())),
        }
    }

    /// Perform a `GetRecords` call for the given iterator, classifying failures.
    async fn get_records_for_iterator(
        &self,
        next_iterator: &str,
    ) -> Result<GetRecordsOutput, FetchError> {
        let mut builder = self
            .kinesis_client
            .get_records()
            .shard_iterator(next_iterator)
            .limit(self.max_records);
        if let Some(arn) = self.stream_identifier.stream_arn_optional() {
            builder = builder.stream_arn(arn.to_string());
        }
        // StreamIdCache async→sync bridge: populate the streamId request field
        // (Java `builder.streamId(StreamIdCache.get(streamIdentifier))`). Returns
        // None until the Scheduler has initialized the cache, in which case the
        // field is left unset (the common uninitialized path).
        builder = builder.set_stream_id(StreamIdCache::try_get_for(Some(&self.stream_identifier)));
        let fut = builder.send();

        let response: GetRecordsOutput = match tokio::time::timeout(self.max_future_wait, fut).await
        {
            Err(_elapsed) => {
                return Err(FetchError::Retryable {
                    message: format!(
                        "Timeout waiting for GetRecords on shard {}",
                        self.stream_and_shard_id
                    ),
                    source: None,
                })
            }
            Ok(Ok(resp)) => resp,
            Ok(Err(sdk_err)) => {
                return Err(classify_sdk_error(sdk_err));
            }
        };

        if !is_valid_result(response.next_shard_iterator(), response.child_shards()) {
            return Err(FetchError::Retryable {
                message: format!(
                    "GetRecords response is not valid for shard: {}. nextShardIterator: {:?}. childShards: {:?}. Will retry GetRecords with the same nextIterator.",
                    self.stream_and_shard_id,
                    response.next_shard_iterator(),
                    response.child_shards()
                ),
                source: None,
            });
        }
        Ok(response)
    }

    /// Acquire a fresh iterator (Java `advanceIteratorTo`), recording metrics.
    ///
    /// Port of the exact Java try/catch/finally shape: only
    /// `ResourceNotFoundException` is caught (logged at info, iterator cleared,
    /// `Ok(())`); a timeout becomes `FetchError::Retryable` (Java
    /// `RetryableRetrievalException`) and any other SDK error is classified the
    /// same way `get_records_for_iterator` classifies `GetRecords` failures —
    /// both propagate as `Err`. Metrics (success + latency) are always recorded,
    /// matching Java's `finally`. `last_known_sequence_number` /
    /// `initial_position_in_stream` are only updated on the `Ok` paths (success
    /// or caught `ResourceNotFoundException`): in Java the equivalent
    /// unconditional assignments sit *after* the try/finally, so they are simply
    /// unreachable when a non-`ResourceNotFoundException` propagates out of the
    /// method — this preserves that.
    async fn advance_iterator_impl(
        &self,
        sequence_number: &str,
        initial_position: &InitialPositionInStreamExtended,
        is_iterator_restart: bool,
    ) -> Result<(), FetchError> {
        let mut builder = self
            .kinesis_client
            .get_shard_iterator()
            .stream_name(self.stream_identifier.stream_name())
            .shard_id(&self.shard_id);
        if let Some(arn) = self.stream_identifier.stream_arn_optional() {
            builder = builder.stream_arn(arn.to_string());
        }
        // StreamIdCache async→sync bridge: Java
        // `builder.streamId(StreamIdCache.get(streamIdentifier))`.
        builder = builder.set_stream_id(StreamIdCache::try_get_for(Some(&self.stream_identifier)));
        // IteratorBuilder builds a request *input*; translate its fields onto the
        // fluent builder. Build a throwaway input to compute the iterator type /
        // sequence / timestamp, then apply.
        let gsi_input_builder =
            aws_sdk_kinesis::operation::get_shard_iterator::GetShardIteratorInput::builder();
        let gsi_input = if is_iterator_restart {
            iterator_builder::get_shard_iterator_reconnect_request(
                gsi_input_builder,
                sequence_number,
                initial_position,
            )
        } else {
            iterator_builder::get_shard_iterator_request(
                gsi_input_builder,
                sequence_number,
                initial_position,
            )
        }
        .build()
        .expect("GetShardIterator input builds with the (always-set) iterator type");

        builder = builder
            .set_shard_iterator_type(gsi_input.shard_iterator_type().cloned())
            .set_starting_sequence_number(gsi_input.starting_sequence_number().map(str::to_string))
            .set_timestamp(gsi_input.timestamp().cloned());

        let mut scope =
            metrics::create_metrics_with_operation(self.metrics_factory.as_ref(), OPERATION);
        metrics::add_stream_id(scope.as_mut(), &self.stream_identifier);
        metrics::add_shard_id(scope.as_mut(), &self.shard_id);
        let start = now_millis();
        let mut success = false;

        let fut = builder.send();
        let outcome: Result<
            Result<
                aws_sdk_kinesis::operation::get_shard_iterator::GetShardIteratorOutput,
                aws_sdk_kinesis::error::SdkError<
                    aws_sdk_kinesis::operation::get_shard_iterator::GetShardIteratorError,
                    aws_smithy_runtime_api::http::Response,
                >,
            >,
            tokio::time::error::Elapsed,
        > = tokio::time::timeout(self.max_future_wait, fut).await;

        let result: Result<(), FetchError> = {
            let mut st = self.state.lock().unwrap();
            let advance_result = match outcome {
                Ok(Ok(resp)) => {
                    st.next_iterator = resp.shard_iterator().map(str::to_string);
                    success = true;
                    Ok(())
                }
                Ok(Err(sdk_err)) => {
                    if is_resource_not_found(&sdk_err) {
                        // Java: caught specially, logged at info, iterator
                        // cleared -> treated as shard-end below, not an error.
                        tracing::info!(
                            "Caught ResourceNotFoundException when getting an iterator for shard {}",
                            self.stream_and_shard_id
                        );
                        st.next_iterator = None;
                        Ok(())
                    } else {
                        // This is the definitive error a field failure needs and
                        // previously had nowhere to surface: a bare `SdkError`
                        // `Display` renders only "dispatch failure"/"service
                        // error"/"response error" with no message (see its own
                        // doc comment, which recommends exactly this
                        // `DisplayErrorContext` wrapper) -- without the full
                        // `.source()` chain, a connection-refused/DNS/TLS
                        // failure (`DispatchFailure`, request never left the
                        // client) is indistinguishable from a `ServiceError` 500
                        // or throttling response. Log it here, at the source,
                        // before classifying and returning.
                        tracing::warn!(
                            "GetShardIterator failed for shard {}: {}",
                            self.stream_and_shard_id,
                            DisplayErrorContext(&sdk_err)
                        );
                        // Java: AWS_EXCEPTION_MANAGER.apply rethrows the same
                        // exception uncaught by advanceIteratorTo; classify it
                        // the same way the GetRecords path does.
                        Err(classify_sdk_error(sdk_err))
                    }
                }
                Err(_elapsed) => {
                    // Java: TimeoutException -> RetryableRetrievalException,
                    // uncaught by advanceIteratorTo (propagates to the caller).
                    // This is a CLIENT-SIDE deadline, not a server-side error:
                    // log it as such (distinct from a slow/failing service) and
                    // include the configured budget so it reads as "our
                    // timeout", not "their failure".
                    tracing::warn!(
                        "GetShardIterator for {} did not complete within the configured \
                         kinesis request timeout ({:?}); the request may never have \
                         reached the endpoint",
                        self.stream_and_shard_id,
                        self.max_future_wait
                    );
                    Err(FetchError::Retryable {
                        message: format!(
                            "Timeout waiting for GetShardIterator on shard {} (configured kinesis request timeout: {:?})",
                            self.stream_and_shard_id, self.max_future_wait
                        ),
                        source: None,
                    })
                }
            };

            // Java: these assignments sit textually after the try/finally, so
            // they never execute when an exception propagated out of the method
            // (i.e. the Err arms above) — only on success or the internally
            // caught ResourceNotFoundException.
            if advance_result.is_ok() {
                if st.next_iterator.is_none() {
                    st.is_shard_end_reached = true;
                }
                st.last_known_sequence_number = Some(sequence_number.to_string());
                st.initial_position_in_stream = Some(*initial_position);
            }

            advance_result
        };

        // Java `finally`: success/latency metrics are recorded on every path,
        // Ok or Err.
        metrics::add_success_and_latency_with_dimension(
            scope.as_mut(),
            Some(&format!("{METRICS_PREFIX}.getShardIterator")),
            success,
            start,
            MetricsLevel::Detailed,
        );
        metrics::end_scope(scope.as_mut());

        result
    }

    /// Test-only seam: mark the fetcher initialized with a preset iterator,
    /// bypassing a `GetShardIterator` network round-trip. Used by the
    /// `GetRecords`-timeout test (which needs an initialized fetcher over a
    /// never-completing HTTP client so `GetShardIterator` cannot be used to seed
    /// the iterator).
    #[cfg(test)]
    fn seed_initialized(&self, iterator: &str) {
        let mut st = self.state.lock().unwrap();
        st.next_iterator = Some(iterator.to_string());
        st.is_initialized = true;
    }
}

/// Classify an SDK `GetRecords` error into a [`FetchError`] the daemon can act
/// on. Uses type-name/message sniffing over the error chain (the Rust SDK
/// exposes typed operation errors, but a uniform chain walk keeps this robust to
/// the exact wrapping).
fn classify_sdk_error<E: std::error::Error + Send + Sync + 'static>(err: E) -> FetchError {
    let chain = error_chain_string(&err);
    if chain.contains("ExpiredIterator") {
        FetchError::ExpiredIterator { message: chain }
    } else if chain.contains("InvalidArgument") {
        FetchError::InvalidArgument { message: chain }
    } else if chain.contains("ProvisionedThroughputExceeded") {
        FetchError::ProvisionedThroughputExceeded { message: chain }
    } else if chain.contains("ResourceNotFound") {
        // GetRecords ResourceNotFound is surfaced as a terminal shard-end in Java
        // (the caller catches it in getRecords()); model it as a distinct Sdk
        // error carrying the marker so the fetcher can convert to TERMINAL_RESULT.
        FetchError::Sdk {
            message: RESOURCE_NOT_FOUND_MARKER.to_string(),
            source: Some(Box::new(err)),
        }
    } else {
        FetchError::Sdk {
            message: chain,
            source: Some(Box::new(err)),
        }
    }
}

/// Render an error and its full `.source()` cause chain via
/// [`DisplayErrorContext`] -- the aws-smithy-recommended way to surface an
/// otherwise-shallow `SdkError` `Display` (whose own doc comment says a bare
/// `SdkError` renders only "service error"/"dispatch failure"/etc. with no
/// message). This is both how `classify_sdk_error` classifies the failure
/// (every generated AWS exception type's `Display` embeds its own name, e.g.
/// `ExpiredIteratorException: <message>`, so the `chain.contains(...)` checks
/// below still work) and what gets stored as the [`FetchError`]'s `message`,
/// so every downstream `{e}`/`{message}` log carries the chain end-to-end.
fn error_chain_string(err: &(dyn std::error::Error + 'static)) -> String {
    DisplayErrorContext(err).to_string()
}

fn is_resource_not_found<E: std::error::Error + 'static>(err: &E) -> bool {
    error_chain_string(err).contains("ResourceNotFound")
}

/// Sentinel identifying a `GetRecords` `ResourceNotFoundException` (converted to
/// a terminal result by the fetcher).
const RESOURCE_NOT_FOUND_MARKER: &str = "__RESOURCE_NOT_FOUND__";

/// The result of one successful async `GetRecords`; `accept_adapter` commits the
/// iterator advance (port of Java `AdvancingResult`).
struct AdvancingResult {
    state: Arc<Mutex<FetcherState>>,
    response: GetRecordsOutput,
}

impl DataFetcherResult for AdvancingResult {
    fn get_result_adapter(&self) -> Box<dyn GetRecordsResponseAdapter> {
        Box::new(KinesisGetRecordsResponseAdapter::new(self.response.clone()))
    }

    fn accept_adapter(&self) -> Box<dyn GetRecordsResponseAdapter> {
        {
            let mut st = self.state.lock().unwrap();
            st.next_iterator = self.response.next_shard_iterator().map(str::to_string);
            let records = self.response.records();
            if !records.is_empty() {
                st.last_known_sequence_number =
                    Some(records[records.len() - 1].sequence_number().to_string());
            }
            if st.next_iterator.is_none() {
                st.is_shard_end_reached = true;
            }
        }
        self.get_result_adapter()
    }

    fn is_shard_end(&self) -> bool {
        self.state.lock().unwrap().is_shard_end_reached
    }
}

/// The terminal result returned when the iterator is exhausted (port of Java
/// `TERMINAL_RESULT`): accepting it marks shard-end.
struct TerminalResult {
    state: Arc<Mutex<FetcherState>>,
}

impl DataFetcherResult for TerminalResult {
    fn get_result_adapter(&self) -> Box<dyn GetRecordsResponseAdapter> {
        Box::new(KinesisGetRecordsResponseAdapter::new(
            GetRecordsOutput::builder()
                .set_records(Some(vec![]))
                .set_millis_behind_latest(None)
                .set_next_shard_iterator(None)
                .build()
                .expect("empty GetRecordsOutput"),
        ))
    }

    fn accept_adapter(&self) -> Box<dyn GetRecordsResponseAdapter> {
        self.state.lock().unwrap().is_shard_end_reached = true;
        self.get_result_adapter()
    }

    fn is_shard_end(&self) -> bool {
        self.state.lock().unwrap().is_shard_end_reached
    }
}

#[async_trait]
impl DataFetcher for KinesisDataFetcher {
    async fn get_records(&self) -> Result<Box<dyn DataFetcherResult>, FetchError> {
        let (initialized, next_iterator) = {
            let st = self.state.lock().unwrap();
            (st.is_initialized, st.next_iterator.clone())
        };
        if !initialized {
            panic!("KinesisDataFetcher.records called before initialization.");
        }

        let iter = match next_iterator {
            Some(iter) => iter,
            None => {
                return Ok(Box::new(TerminalResult {
                    state: Arc::clone(&self.state),
                }))
            }
        };

        let mut scope =
            metrics::create_metrics_with_operation(self.metrics_factory.as_ref(), OPERATION);
        metrics::add_stream_id(scope.as_mut(), &self.stream_identifier);
        metrics::add_shard_id(scope.as_mut(), &self.shard_id);
        let start = now_millis();

        let result = self.get_records_for_iterator(&iter).await;

        let (outcome, success): (Result<Box<dyn DataFetcherResult>, FetchError>, bool) =
            match result {
                Ok(response) => (
                    Ok(Box::new(AdvancingResult {
                        state: Arc::clone(&self.state),
                        response,
                    })),
                    true,
                ),
                // GetRecords ResourceNotFoundException -> terminal (Java catches it in
                // getRecords() and returns TERMINAL_RESULT).
                Err(FetchError::Sdk { message, .. }) if message == RESOURCE_NOT_FOUND_MARKER => (
                    Ok(Box::new(TerminalResult {
                        state: Arc::clone(&self.state),
                    })),
                    false,
                ),
                Err(e) => (Err(e), false),
            };

        metrics::add_success_and_latency_with_dimension(
            scope.as_mut(),
            Some(&format!("{METRICS_PREFIX}.getRecords")),
            success,
            start,
            MetricsLevel::Detailed,
        );
        metrics::end_scope(scope.as_mut());
        outcome
    }

    async fn initialize(
        &self,
        initial_checkpoint: &str,
        initial_position: &InitialPositionInStreamExtended,
    ) -> Result<(), FetchError> {
        // Java: `isInitialized = true` sits after `advanceIteratorTo`, so it is
        // only reached if that call doesn't throw.
        self.advance_iterator_impl(initial_checkpoint, initial_position, false)
            .await?;
        self.state.lock().unwrap().is_initialized = true;
        Ok(())
    }

    async fn initialize_from_extended(
        &self,
        initial_checkpoint: &ExtendedSequenceNumber,
        initial_position: &InitialPositionInStreamExtended,
    ) -> Result<(), FetchError> {
        self.advance_iterator_impl(
            initial_checkpoint.sequence_number(),
            initial_position,
            false,
        )
        .await?;
        self.state.lock().unwrap().is_initialized = true;
        Ok(())
    }

    async fn advance_iterator_to(
        &self,
        sequence_number: &str,
        initial_position: &InitialPositionInStreamExtended,
    ) -> Result<(), FetchError> {
        self.advance_iterator_impl(sequence_number, initial_position, false)
            .await
    }

    async fn restart_iterator(&self) -> Result<(), FetchError> {
        // The Java-parity panic must not fire while `state` is held: panicking
        // with the guard alive would poison the lock, so a `catch_unwind` in
        // the calling loop would wedge every subsequent reader. Snapshot under
        // the lock, drop the guard, then panic (same shape as the
        // before-initialization panic in `get_records`).
        let restart_from = {
            let st = self.state.lock().unwrap();
            match (
                &st.last_known_sequence_number,
                st.initial_position_in_stream,
            ) {
                (Some(seq), Some(pos)) if !seq.is_empty() => Some((seq.clone(), pos)),
                _ => None,
            }
        };
        let Some((seq, pos)) = restart_from else {
            panic!(
                "Make sure to initialize the KinesisDataFetcher before restarting the iterator."
            );
        };
        self.advance_iterator_impl(&seq, &pos, true).await
    }

    fn reset_iterator(
        &self,
        shard_iterator: Option<String>,
        sequence_number: &str,
        initial_position: &InitialPositionInStreamExtended,
    ) {
        let mut st = self.state.lock().unwrap();
        st.next_iterator = shard_iterator;
        st.last_known_sequence_number = Some(sequence_number.to_string());
        st.initial_position_in_stream = Some(*initial_position);
    }

    fn stream_identifier(&self) -> StreamIdentifier {
        self.stream_identifier.clone()
    }

    fn is_shard_end_reached(&self) -> bool {
        self.state.lock().unwrap().is_shard_end_reached
    }

    fn next_iterator(&self) -> Option<String> {
        self.state.lock().unwrap().next_iterator.clone()
    }
}

#[cfg(test)]
mod tests {
    // Each test holds `stream_id_guard()` (a `std::sync::MutexGuard` over the
    // global `StreamIdCache`) for its whole body to serialize tests that mutate
    // that shared cache. The guard is deliberately held across `.await`s — the
    // whole point is to keep concurrently-running tests off the shared global —
    // and these are single-threaded `#[tokio::test]`s, so the deadlock risk the
    // lint guards against does not apply.
    #![allow(clippy::await_holding_lock)]

    use super::*;
    use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::data_fetcher_provider_config::KinesisDataFetcherProviderConfig;
    use crate::retrieval::polling::test_support::mock_kinesis_client;
    use aws_sdk_kinesis::operation::get_records::GetRecordsOutput;
    use aws_sdk_kinesis::operation::get_shard_iterator::GetShardIteratorOutput;
    use aws_sdk_kinesis::types::{Record, ShardIteratorType};
    use aws_smithy_mocks::mock;
    use aws_smithy_types::Blob;

    use crate::coordinator::stream_info::{
        MockStreamIdResolver, StreamIdCache, StreamIdOnboardingState,
    };

    const STREAM_NAME: &str = "streamName";
    const SHARD_ID: &str = "shardId-1";

    /// Serialization lock for the process-global `StreamIdCache` singleton that
    /// every test in this module touches (each constructs a `KinesisDataFetcher`,
    /// which consults the singleton via `try_get_for`). Holding it keeps the
    /// streamId onboarding-state tests — which `initialize()` the singleton — from
    /// racing the other fetcher tests in this module.
    static STREAM_ID_TEST_LOCK: std::sync::Mutex<()> = std::sync::Mutex::new(());

    /// Acquire [`STREAM_ID_TEST_LOCK`] and reset the singleton to uninitialized so
    /// `try_get_for` is a no-op for tests that don't exercise the streamId path.
    /// Returns a guard whose lifetime must span the test body.
    fn stream_id_guard() -> std::sync::MutexGuard<'static, ()> {
        let g = STREAM_ID_TEST_LOCK
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        // Default to an uninitialized cache so `try_get_for` is a no-op for tests
        // that don't care about the streamId path.
        StreamIdCache::reset();
        g
    }

    fn fetcher(client: aws_sdk_kinesis::Client) -> KinesisDataFetcher {
        let cfg = KinesisDataFetcherProviderConfig::new(
            StreamIdentifier::single_stream_instance(STREAM_NAME),
            SHARD_ID,
            std::sync::Arc::new(NullMetricsFactory),
            1,
            std::time::Duration::from_secs(30),
        );
        KinesisDataFetcher::new(client, &cfg)
    }

    fn latest() -> InitialPositionInStreamExtended {
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest)
    }

    // Port of KinesisDataFetcherTest.testInitializeLatest: initialize acquires an
    // iterator with the LATEST type and records it.
    #[tokio::test]
    async fn initialize_latest_acquires_iterator() {
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(|req| {
                req.shard_iterator_type() == Some(&ShardIteratorType::Latest)
                    && req.shard_id() == Some(SHARD_ID)
            })
            .then_output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("iter-A")
                    .build()
            });
        let client = mock_kinesis_client(&[&gsi]);
        let f = fetcher(client);
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
            &latest(),
        )
        .await
        .unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-A"));
        assert!(!f.is_shard_end_reached());
    }

    // Port of KinesisDataFetcherTest.testRestartIteratorUsesAfterSequenceNumberIteratorType.
    #[tokio::test]
    async fn restart_iterator_uses_after_sequence_number() {
        let _g = stream_id_guard();
        // initialize (AT_SEQUENCE_NUMBER), then restart (AFTER_SEQUENCE_NUMBER).
        let init = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(|req| {
                req.shard_iterator_type() == Some(&ShardIteratorType::AtSequenceNumber)
                    && req.starting_sequence_number() == Some("123")
            })
            .then_output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("iter-1")
                    .build()
            });
        let restart = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(|req| {
                req.shard_iterator_type() == Some(&ShardIteratorType::AfterSequenceNumber)
                    && req.starting_sequence_number() == Some("123")
            })
            .then_output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("iter-2")
                    .build()
            });
        let client = mock_kinesis_client(&[&init, &restart]);
        let f = fetcher(client);
        f.initialize("123", &latest()).await.unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-1"));
        f.restart_iterator().await.unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-2"));
    }

    // Port of KinesisDataFetcherTest.testRestartIteratorNotInitialized.
    #[tokio::test]
    #[should_panic(expected = "Make sure to initialize the KinesisDataFetcher before restarting")]
    async fn restart_iterator_not_initialized_panics() {
        let _g = stream_id_guard();
        let f = fetcher(mock_kinesis_client(&[]));
        let _ = f.restart_iterator().await;
    }

    // Companion to restart_iterator_not_initialized_panics: the Java-parity
    // panic must not poison the `state` lock — after a caught panic (as in a
    // `catch_unwind`-guarded background loop) the fetcher must remain usable.
    #[tokio::test]
    async fn restart_iterator_panic_does_not_poison_the_lock() {
        use futures::FutureExt;

        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator).then_output(|| {
            GetShardIteratorOutput::builder()
                .shard_iterator("iter-A")
                .build()
        });
        let f = fetcher(mock_kinesis_client(&[&gsi]));

        // Not initialized -> Java-parity panic, caught by the caller.
        let err = std::panic::AssertUnwindSafe(f.restart_iterator())
            .catch_unwind()
            .await
            .unwrap_err();
        assert_eq!(
            err.downcast_ref::<&str>().copied(),
            Some("Make sure to initialize the KinesisDataFetcher before restarting the iterator.")
        );

        // Lock is not poisoned: normal initialization on the same instance
        // still succeeds.
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
            &latest(),
        )
        .await
        .unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-A"));
    }

    // Port of KinesisDataFetcherTest.testGetRecordsWithResourceNotFoundException:
    // a ResourceNotFoundException from GetRecords marks the shard as ended
    // (terminal result on accept).
    #[tokio::test]
    async fn get_records_resource_not_found_marks_shard_end() {
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator).then_output(|| {
            GetShardIteratorOutput::builder()
                .shard_iterator("TestShardIterator")
                .build()
        });
        let get = mock!(aws_sdk_kinesis::Client::get_records).then_error(|| {
            aws_sdk_kinesis::operation::get_records::GetRecordsError::ResourceNotFoundException(
                aws_sdk_kinesis::types::error::ResourceNotFoundException::builder()
                    .message("gone")
                    .build(),
            )
        });
        let client = mock_kinesis_client(&[&gsi, &get]);
        let f = fetcher(client);
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
            &latest(),
        )
        .await
        .unwrap();
        let result = f.get_records().await.expect("terminal, not error");
        result.accept_adapter();
        assert!(f.is_shard_end_reached());
    }

    // Port of KinesisDataFetcherTest.testFetcherDoesNotAdvanceWithoutAccept: the
    // two-phase protocol — get_records() does not advance the iterator until
    // accept_adapter() is called.
    #[tokio::test]
    async fn fetcher_does_not_advance_without_accept() {
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator).then_output(|| {
            GetShardIteratorOutput::builder()
                .shard_iterator("iter-0")
                .build()
        });
        // Two GetRecords calls, both returning nextShardIterator "iter-1".
        let get = mock!(aws_sdk_kinesis::Client::get_records)
            .sequence()
            .output(|| {
                GetRecordsOutput::builder()
                    .records(
                        Record::builder()
                            .sequence_number("seq-1")
                            .partition_key("pk")
                            .data(Blob::new(b"x".to_vec()))
                            .build()
                            .unwrap(),
                    )
                    .next_shard_iterator("iter-1")
                    .build()
                    .unwrap()
            })
            .output(|| {
                GetRecordsOutput::builder()
                    .records(
                        Record::builder()
                            .sequence_number("seq-2")
                            .partition_key("pk")
                            .data(Blob::new(b"x".to_vec()))
                            .build()
                            .unwrap(),
                    )
                    .next_shard_iterator("iter-2")
                    .build()
                    .unwrap()
            })
            .build();
        let client = mock_kinesis_client(&[&gsi, &get]);
        let f = fetcher(client);
        f.initialize("TRIM_HORIZON", &latest()).await.unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-0"));

        // First get: without accept, iterator stays at iter-0.
        let r1 = f.get_records().await.unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-0"));
        // Accept advances to iter-1.
        r1.accept_adapter();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-1"));

        // Second get + accept advances to iter-2.
        let r2 = f.get_records().await.unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-1"));
        r2.accept_adapter();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-2"));
    }

    // Port of KinesisDataFetcherTest.testAdvanceIteratorToTrimHorizonLatestAndAtTimestamp
    // (the TRIM_HORIZON + LATEST cases; timestamp validated separately in IteratorBuilder tests).
    #[tokio::test]
    async fn advance_iterator_to_sentinels() {
        let _g = stream_id_guard();
        let horizon = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(|req| {
                req.shard_iterator_type() == Some(&ShardIteratorType::TrimHorizon)
            })
            .then_output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("iter-horizon")
                    .build()
            });
        let latest_rule = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(|req| req.shard_iterator_type() == Some(&ShardIteratorType::Latest))
            .then_output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("iter-latest")
                    .build()
            });
        let client = mock_kinesis_client(&[&horizon, &latest_rule]);
        let f = fetcher(client);
        f.advance_iterator_to(
            crate::checkpoint::SentinelCheckpoint::TrimHorizon.as_str(),
            &InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
        )
        .await
        .unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-horizon"));
        f.advance_iterator_to(
            crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
            &latest(),
        )
        .await
        .unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-latest"));
    }

    #[tokio::test]
    #[should_panic(expected = "called before initialization")]
    async fn get_records_before_initialize_panics() {
        let _g = stream_id_guard();
        let f = fetcher(mock_kinesis_client(&[]));
        let _ = f.get_records().await;
    }

    fn trim_horizon() -> InitialPositionInStreamExtended {
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::TrimHorizon)
    }

    fn at_timestamp() -> InitialPositionInStreamExtended {
        InitialPositionInStreamExtended::new_initial_position_at_timestamp(
            chrono::DateTime::<chrono::Utc>::from_timestamp_millis(1000).unwrap(),
        )
    }

    // Port of KinesisDataFetcherTest.testInitializeTimeZero: initialize with the
    // TRIM_HORIZON iterator instruction.
    #[tokio::test]
    async fn initialize_time_zero_acquires_iterator() {
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(|req| {
                req.shard_iterator_type() == Some(&ShardIteratorType::TrimHorizon)
                    && req.shard_id() == Some(SHARD_ID)
                    && req.stream_name() == Some(STREAM_NAME)
            })
            .then_output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("iter-th")
                    .build()
            });
        let client = mock_kinesis_client(&[&gsi]);
        let f = fetcher(client);
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::TrimHorizon.as_str(),
            &trim_horizon(),
        )
        .await
        .unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-th"));
        assert!(!f.is_shard_end_reached());
    }

    // Port of KinesisDataFetcherTest.testInitializeAtTimestamp: initialize with
    // the AT_TIMESTAMP iterator instruction, which carries a timestamp.
    #[tokio::test]
    async fn initialize_at_timestamp_acquires_iterator() {
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(|req| {
                req.shard_iterator_type() == Some(&ShardIteratorType::AtTimestamp)
                    && req.timestamp().is_some()
                    && req.shard_id() == Some(SHARD_ID)
            })
            .then_output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("iter-ts")
                    .build()
            });
        let client = mock_kinesis_client(&[&gsi]);
        let f = fetcher(client);
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::AtTimestamp.as_str(),
            &at_timestamp(),
        )
        .await
        .unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("iter-ts"));
        assert!(!f.is_shard_end_reached());
    }

    // Port of KinesisDataFetcherTest.testAdvanceIteratorTo: initialize +
    // advanceIteratorTo(seqA) + advanceIteratorTo(seqB) all issue an
    // AT_SEQUENCE_NUMBER GetShardIterator with the expected stream/shard/sequence.
    #[tokio::test]
    async fn advance_iterator_to_uses_at_sequence_number() {
        let _g = stream_id_guard();
        let seq_a = "123";
        let seq_b = "456";
        // Two calls with seqA (initialize + first advance), one with seqB.
        let for_a = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(move |req| {
                req.shard_iterator_type() == Some(&ShardIteratorType::AtSequenceNumber)
                    && req.starting_sequence_number() == Some(seq_a)
                    && req.stream_name() == Some(STREAM_NAME)
                    && req.shard_id() == Some(SHARD_ID)
            })
            .sequence()
            .output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("foo")
                    .build()
            })
            .output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("foo")
                    .build()
            })
            .build();
        let for_b = mock!(aws_sdk_kinesis::Client::get_shard_iterator)
            .match_requests(move |req| {
                req.shard_iterator_type() == Some(&ShardIteratorType::AtSequenceNumber)
                    && req.starting_sequence_number() == Some(seq_b)
            })
            .then_output(|| {
                GetShardIteratorOutput::builder()
                    .shard_iterator("bar")
                    .build()
            });
        let client = mock_kinesis_client(&[&for_a, &for_b]);
        let f = fetcher(client);
        f.initialize(seq_a, &latest()).await.unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("foo"));
        f.advance_iterator_to(seq_a, &latest()).await.unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("foo"));
        f.advance_iterator_to(seq_b, &latest()).await.unwrap();
        assert_eq!(f.next_iterator().as_deref(), Some("bar"));
    }

    // Port of KinesisDataFetcherTest.testGetRecordsThrowsSdkException: a generic
    // SdkException from GetRecords surfaces (the Rust getRecords returns a
    // FetchError::Sdk rather than a terminal result).
    #[tokio::test]
    async fn get_records_throws_sdk_exception() {
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator).then_output(|| {
            GetShardIteratorOutput::builder()
                .shard_iterator("test")
                .build()
        });
        let get = mock!(aws_sdk_kinesis::Client::get_records).then_error(|| {
            aws_sdk_kinesis::operation::get_records::GetRecordsError::KmsThrottlingException(
                aws_sdk_kinesis::types::error::KmsThrottlingException::builder()
                    .message("Test Exception")
                    .build(),
            )
        });
        let client = mock_kinesis_client(&[&gsi, &get]);
        let f = fetcher(client);
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
            &latest(),
        )
        .await
        .unwrap();
        match f.get_records().await {
            Err(FetchError::Sdk { message, .. }) => assert!(
                message.contains("Test Exception"),
                "expected message to contain 'Test Exception', got: {message}"
            ),
            Err(other) => panic!("expected FetchError::Sdk, got {other:?}"),
            Ok(_) => panic!("expected an error, got a result"),
        }
    }

    // Port of KinesisDataFetcherTest.testNonNullGetRecords: a ResourceNotFound
    // from GetRecords yields a non-null (terminal) result, not an error.
    #[tokio::test]
    async fn non_null_get_records() {
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator).then_output(|| {
            GetShardIteratorOutput::builder()
                .shard_iterator("TestIterator")
                .build()
        });
        let get = mock!(aws_sdk_kinesis::Client::get_records).then_error(|| {
            aws_sdk_kinesis::operation::get_records::GetRecordsError::ResourceNotFoundException(
                aws_sdk_kinesis::types::error::ResourceNotFoundException::builder()
                    .message("Test Exception")
                    .build(),
            )
        });
        let client = mock_kinesis_client(&[&gsi, &get]);
        let f = fetcher(client);
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
            &latest(),
        )
        .await
        .unwrap();
        // Non-null result (Ok), terminal on accept.
        let _result = f.get_records().await.expect("terminal result, not error");
    }

    fn timeout_fetcher(client: aws_sdk_kinesis::Client) -> KinesisDataFetcher {
        let cfg = KinesisDataFetcherProviderConfig::new(
            StreamIdentifier::single_stream_instance(STREAM_NAME),
            SHARD_ID,
            std::sync::Arc::new(NullMetricsFactory),
            1,
            std::time::Duration::from_millis(10),
        );
        KinesisDataFetcher::new(client, &cfg)
    }

    // Port of KinesisDataFetcherTest.testTimeoutExceptionIsRetryableForGetShardIterator:
    // a GetShardIterator that times out on the FIRST (init) call must surface as
    // an error, NOT silently become shard-end (the bug this test now pins down:
    // Java raises a RetryableRetrievalException caused by a TimeoutException,
    // which propagates out of `advanceIteratorTo`/`initialize` uncaught so
    // `isInitialized`/`isShardEndReached` are never touched — the caller
    // (`InitializeTask` via `PrefetchRecordsPublisher::start`) retries the whole
    // init on the next lifecycle step). Uses a hanging HTTP client under a
    // paused clock so the fetcher's own request timeout fires.
    #[tokio::test(flavor = "current_thread", start_paused = true)]
    async fn timeout_is_retryable_for_get_shard_iterator() {
        let _g = stream_id_guard();
        use crate::retrieval::polling::test_support::hanging_kinesis_client;
        let f = std::sync::Arc::new(timeout_fetcher(hanging_kinesis_client()));
        let f2 = std::sync::Arc::clone(&f);
        let init = tokio::spawn(async move {
            f2.initialize(
                crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
                &latest(),
            )
            .await
        });
        tokio::time::advance(std::time::Duration::from_millis(50)).await;
        let result = init.await.unwrap();
        match result {
            Err(FetchError::Retryable { message, .. }) => {
                assert!(
                    message.contains("Timeout"),
                    "expected 'Timeout' in: {message}"
                );
            }
            Err(other) => panic!("expected FetchError::Retryable, got {other:?}"),
            Ok(()) => panic!("expected a timeout error, got Ok"),
        }
        // NOT shard-end: the exception path never reaches the
        // `isShardEndReached`/iterator-commit code (Java: it's textually after
        // the try/finally that the exception already escaped).
        assert_eq!(f.next_iterator(), None);
        assert!(!f.is_shard_end_reached());
    }

    // New (Java parity gap this bug fix closes): a non-timeout, non-
    // ResourceNotFound SDK failure on the FIRST GetShardIterator call must also
    // surface as an error, not silently become shard-end. Port-motivated test
    // for the "field failure": InternalFailureException on init.
    #[tokio::test]
    async fn init_sdk_error_from_get_shard_iterator_is_error_not_shard_end() {
        use futures::FutureExt;
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator).then_error(|| {
            aws_sdk_kinesis::operation::get_shard_iterator::GetShardIteratorError::InternalFailureException(
                aws_sdk_kinesis::types::error::InternalFailureException::builder()
                    .message("internal failure")
                    .build(),
            )
        });
        let client = mock_kinesis_client(&[&gsi]);
        let f = fetcher(client);
        match f
            .initialize(
                crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
                &latest(),
            )
            .await
        {
            Err(FetchError::Sdk { message, .. }) => {
                assert!(
                    message.contains("internal failure") || message.contains("InternalFailure"),
                    "expected the SDK error in the message, got: {message}"
                );
            }
            Err(other) => panic!("expected FetchError::Sdk, got {other:?}"),
            Ok(()) => panic!("expected an error, got Ok"),
        }
        assert!(
            !f.is_shard_end_reached(),
            "a non-ResourceNotFound SDK failure on init must not mark shard-end"
        );
        assert_eq!(f.next_iterator(), None);
        // is_initialized was never flipped true, so get_records still panics
        // (Java: IllegalArgumentException, "records called before initialization").
        let panicked = std::panic::AssertUnwindSafe(f.get_records())
            .catch_unwind()
            .await;
        assert!(
            panicked.is_err(),
            "get_records should still panic: init never completed"
        );
    }

    // New: a ResourceNotFoundException on the FIRST GetShardIterator call is the
    // one case that legitimately IS shard-end (existing behavior, preserved by
    // this fix): caught internally, logged at info, `Ok(())` returned.
    #[tokio::test]
    async fn init_resource_not_found_from_get_shard_iterator_marks_shard_end() {
        let _g = stream_id_guard();
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator).then_error(|| {
            aws_sdk_kinesis::operation::get_shard_iterator::GetShardIteratorError::ResourceNotFoundException(
                aws_sdk_kinesis::types::error::ResourceNotFoundException::builder()
                    .message("no such shard")
                    .build(),
            )
        });
        let client = mock_kinesis_client(&[&gsi]);
        let f = fetcher(client);
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
            &latest(),
        )
        .await
        .expect("ResourceNotFoundException on GetShardIterator is not an error");
        assert!(f.is_shard_end_reached());
        assert_eq!(f.next_iterator(), None);
        // is_initialized WAS flipped true (Java: advanceIteratorTo did not
        // throw), so get_records() now returns the terminal result instead of
        // panicking.
        let result = f.get_records().await.expect("terminal, not error");
        result.accept_adapter();
        assert!(f.is_shard_end_reached());
    }

    // Port of KinesisDataFetcherTest.testTimeoutExceptionIsRetryableForGetRecords:
    // a GetRecords that times out surfaces as FetchError::Retryable with a
    // "Timeout" message (Java RetryableRetrievalException caused by
    // TimeoutException). The iterator is pre-seeded (the HTTP client hangs, so
    // GetShardIterator cannot be used to acquire it).
    #[tokio::test(flavor = "current_thread", start_paused = true)]
    async fn timeout_is_retryable_for_get_records() {
        let _g = stream_id_guard();
        use crate::retrieval::polling::test_support::hanging_kinesis_client;
        let f = std::sync::Arc::new(timeout_fetcher(hanging_kinesis_client()));
        f.seed_initialized("TestShardIterator");
        let f2 = std::sync::Arc::clone(&f);
        let handle = tokio::spawn(async move { f2.get_records().await });
        tokio::time::advance(std::time::Duration::from_millis(50)).await;
        let result = handle.await.unwrap();
        match result {
            Err(FetchError::Retryable { message, .. }) => {
                assert!(
                    message.contains("Timeout"),
                    "expected 'Timeout' in: {message}"
                );
            }
            Err(other) => panic!("expected FetchError::Retryable, got {other:?}"),
            Ok(_) => panic!("expected a timeout error, got a result"),
        }
    }

    // ---- StreamIdCache (streamId request field) onboarding-state tests ----
    //
    // These drive the process-global `StreamIdCache` singleton, which the fetcher
    // consults (via `try_get_for`) once in `initialize` and once in `getRecords`.
    // They hold the crate-wide `TEST_LOCK` (via `stream_id_guard`) so they don't
    // race the other fetcher tests or the `stream_id_cache` module's own tests.

    /// Build the GetShardIterator + (ResourceNotFound) GetRecords mock client the
    /// Java `setupForStreamIdTest` uses, and initialize + getRecords the fetcher.
    async fn run_stream_id_fetch() -> KinesisDataFetcher {
        let gsi = mock!(aws_sdk_kinesis::Client::get_shard_iterator).then_output(|| {
            GetShardIteratorOutput::builder()
                .shard_iterator("TestIterator")
                .build()
        });
        let get = mock!(aws_sdk_kinesis::Client::get_records).then_error(|| {
            aws_sdk_kinesis::operation::get_records::GetRecordsError::ResourceNotFoundException(
                aws_sdk_kinesis::types::error::ResourceNotFoundException::builder()
                    .message("Test Exception")
                    .build(),
            )
        });
        let client = mock_kinesis_client(&[&gsi, &get]);
        let f = fetcher(client);
        f.initialize(
            crate::checkpoint::SentinelCheckpoint::Latest.as_str(),
            &latest(),
        )
        .await
        .unwrap();
        let _result = f.get_records().await.expect("terminal result");
        f
    }

    // Port of testGetRecordsWithStreamIdAndOnboardingStateAsNotOnboarding:
    // NOT_ONBOARDED -> the resolver `get` is never called.
    #[tokio::test(flavor = "multi_thread")]
    async fn get_records_stream_id_not_onboarding() {
        let _g = stream_id_guard();
        let mut m = MockStreamIdResolver::new();
        m.expect_get().never();
        StreamIdCache::initialize(Arc::new(m), StreamIdOnboardingState::NotOnboarded);
        let _f = run_stream_id_fetch().await;
        StreamIdCache::reset();
    }

    // Port of testGetRecordsWithStreamIdAndOnboardingStateAsInTransition:
    // IN_TRANSITION -> resolver `get` called twice (initialize + getRecords).
    #[tokio::test(flavor = "multi_thread")]
    async fn get_records_stream_id_in_transition() {
        let _g = stream_id_guard();
        let mut m = MockStreamIdResolver::new();
        m.expect_get()
            .times(2)
            .returning(|_| Ok(Some("test-stream-id".to_string())));
        StreamIdCache::initialize(Arc::new(m), StreamIdOnboardingState::InTransition);
        let _f = run_stream_id_fetch().await;
        StreamIdCache::reset();
    }

    // Port of testGetRecordsWithStreamIdAndOnboardingStateAsOnboarding:
    // ONBOARDED -> resolver `get` called twice (initialize + getRecords).
    #[tokio::test(flavor = "multi_thread")]
    async fn get_records_stream_id_onboarding() {
        let _g = stream_id_guard();
        let mut m = MockStreamIdResolver::new();
        m.expect_get()
            .times(2)
            .returning(|_| Ok(Some("test-stream-id".to_string())));
        StreamIdCache::initialize(Arc::new(m), StreamIdOnboardingState::Onboarded);
        let _f = run_stream_id_fetch().await;
        StreamIdCache::reset();
    }

    // Port of testGetRecordsWithStreamIdAndOnboardingStateAsInTransitionNoRuntimeException:
    // IN_TRANSITION + resolver error -> error swallowed (no panic), still called twice.
    #[tokio::test(flavor = "multi_thread")]
    async fn get_records_stream_id_in_transition_no_runtime_exception() {
        let _g = stream_id_guard();
        let mut m = MockStreamIdResolver::new();
        m.expect_get()
            .times(2)
            .returning(|_| Err(crate::leases::exceptions::LeasingError::dependency("boom")));
        StreamIdCache::initialize(Arc::new(m), StreamIdOnboardingState::InTransition);
        let _f = run_stream_id_fetch().await;
        StreamIdCache::reset();
    }

    // Port of testGetRecordsWithStreamIdAndOnboardingStateAsOnboardingThrowsRuntimeException:
    // ONBOARDED + resolver error -> panics (Java RuntimeException).
    #[tokio::test(flavor = "multi_thread")]
    #[should_panic(expected = "Error getting stream ID")]
    async fn get_records_stream_id_onboarding_throws() {
        let _g = stream_id_guard();
        let mut m = MockStreamIdResolver::new();
        m.expect_get()
            .returning(|_| Err(crate::leases::exceptions::LeasingError::dependency("boom")));
        StreamIdCache::initialize(Arc::new(m), StreamIdOnboardingState::Onboarded);
        // Panics during initialize (the first streamId lookup).
        let _f = run_stream_id_fetch().await;
    }
}
