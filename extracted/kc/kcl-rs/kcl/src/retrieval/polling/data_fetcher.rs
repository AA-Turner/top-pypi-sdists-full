//! Port of `software.amazon.kinesis.retrieval.polling.DataFetcher`.
//!
//! A stateful, single-shard iterator-tracking fetcher of Kinesis records via
//! classic `GetRecords` polling. The sole implementation is
//! [`KinesisDataFetcher`](crate::retrieval::polling::KinesisDataFetcher).
//!
//! # Async deviation
//!
//! Java's `DataFetcher` is used synchronously (it blocks over the async SDK
//! client via `FutureUtils.resolveOrCancelFuture`). The Rust port stays async:
//! the I/O methods are `async fn`. Because a `DataFetcher` is held behind an
//! `Arc<dyn ...>` (shared by the strategy and used from the prefetch task) and
//! mutates iterator state, all methods take `&self` and the implementation guards
//! its state internally.
//!
//! # Two-phase get/accept protocol (load-bearing)
//!
//! [`get_records`](DataFetcher::get_records) performs the fetch (the network call)
//! and returns a [`DataFetcherResult`]. Calling
//! [`accept_adapter`](DataFetcherResult::accept_adapter) on that result is what
//! **advances** the fetcher's internal iterator (`next_iterator`,
//! `last_known_sequence_number`, `is_shard_end_reached`). Merely inspecting the
//! result via [`get_result_adapter`](DataFetcherResult::get_result_adapter) does
//! not mutate state. This asymmetry is preserved exactly.

use async_trait::async_trait;

use crate::common::InitialPositionInStreamExtended;
use crate::common::StreamIdentifier;
use crate::exceptions::BoxError;
use crate::retrieval::get_records_response_adapter::GetRecordsResponseAdapter;
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Classification of a `GetRecords` failure, distinguishing the cases the
/// prefetch daemon recovers from differently.
///
/// Port of the distinct `catch` branches in
/// `PrefetchRecordsPublisher.makeRetrievalAttempt`: `RetryableRetrievalException`
/// (retry naturally), `ExpiredIteratorException` (restart iterator + metric),
/// `InvalidArgumentException` (restart iterator), `ProvisionedThroughputExceededException`
/// (throttle), and generic `SdkException` (log + retry).
#[derive(Debug)]
pub enum FetchError {
    /// A retryable retrieval failure (timeout / invalid result) — the daemon
    /// simply retries. Port of `RetryableRetrievalException`.
    Retryable {
        /// The message.
        message: String,
        /// The cause, if any.
        source: Option<BoxError>,
    },
    /// The shard iterator expired — the daemon restarts the iterator and emits
    /// the `ExpiredIterator` metric. Port of `ExpiredIteratorException`.
    ExpiredIterator {
        /// The message.
        message: String,
    },
    /// A request argument became invalid — the daemon restarts the iterator.
    /// Port of `InvalidArgumentException`.
    InvalidArgument {
        /// The message.
        message: String,
    },
    /// Provisioned throughput exceeded — the daemon reports throttling. Port of
    /// `ProvisionedThroughputExceededException`.
    ProvisionedThroughputExceeded {
        /// The message.
        message: String,
    },
    /// Any other SDK failure — the daemon logs and retries. Port of the generic
    /// `SdkException` branch.
    Sdk {
        /// The message.
        message: String,
        /// The cause, if any.
        source: Option<BoxError>,
    },
}

impl std::fmt::Display for FetchError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            FetchError::Retryable { message, .. } => {
                write!(f, "RetryableRetrievalException: {message}")
            }
            FetchError::ExpiredIterator { message } => {
                write!(f, "ExpiredIteratorException: {message}")
            }
            FetchError::InvalidArgument { message } => {
                write!(f, "InvalidArgumentException: {message}")
            }
            FetchError::ProvisionedThroughputExceeded { message } => {
                write!(f, "ProvisionedThroughputExceededException: {message}")
            }
            FetchError::Sdk { message, .. } => write!(f, "SdkException: {message}"),
        }
    }
}

impl std::error::Error for FetchError {}

/// The outcome of a single async `GetRecords` fetch, plus the control point for
/// advancing the fetcher's iterator.
///
/// Port of `software.amazon.kinesis.retrieval.DataFetcherResult`. In Java the
/// network call happens in `getRecords()` and `acceptAdapter()` is pure state
/// mutation on the (single-threaded) fetcher; here `get_records()` returns this
/// object *after* a successful fetch, and [`accept_adapter`](Self::accept_adapter)
/// commits the iterator advance via the fetcher's interior-mutable state.
pub trait DataFetcherResult: Send {
    /// The retrieved batch, as a [`GetRecordsResponseAdapter`], **without**
    /// advancing the iterator (idempotent).
    fn get_result_adapter(&self) -> Box<dyn GetRecordsResponseAdapter>;

    /// Accept the result, **advancing the shard iterator** (side-effecting).
    fn accept_adapter(&self) -> Box<dyn GetRecordsResponseAdapter>;

    /// Whether this result is at the end of the shard.
    fn is_shard_end(&self) -> bool;
}

/// A stateful, single-shard iterator manager over classic `GetRecords` polling.
///
/// Port of the Java `DataFetcher` interface (async). The deprecated raw-response
/// overloads collapse to the adapter path; the SDK-request-building helpers are
/// internal to [`KinesisDataFetcher`].
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait DataFetcher: Send + Sync {
    /// Get records from the current position (up to the configured max).
    ///
    /// Returns a [`DataFetcherResult`] whose `accept_adapter` advances the
    /// iterator on success, or a [`FetchError`] classifying the failure. Port of
    /// `getRecords(): DataFetcherResult` fused with the exception classification
    /// that Java surfaces from the underlying SDK call. Panics (Java
    /// `IllegalArgumentException`) if called before `initialize`.
    async fn get_records(&self) -> Result<Box<dyn DataFetcherResult>, FetchError>;

    /// Initialize the iterator from a sequence-number string.
    ///
    /// Port of `initialize(String, InitialPositionInStreamExtended)`, which
    /// calls the fallible `advanceIteratorTo` and only flips `isInitialized` to
    /// `true` if it doesn't throw. Returns [`FetchError`] on a `GetShardIterator`
    /// failure (timeout / non-`ResourceNotFound` SDK error) — matching Java,
    /// which lets `advanceIteratorTo`'s exception propagate out of `initialize`
    /// uncaught, leaving `isInitialized` `false`. A `ResourceNotFoundException`
    /// is not an error here: it is caught internally, the iterator is cleared
    /// (shard-end), and `Ok(())` is returned with `isInitialized` set `true`.
    async fn initialize(
        &self,
        initial_checkpoint: &str,
        initial_position: &InitialPositionInStreamExtended,
    ) -> Result<(), FetchError>;

    /// Initialize the iterator from an [`ExtendedSequenceNumber`]. See
    /// [`initialize`](Self::initialize) for the error semantics.
    async fn initialize_from_extended(
        &self,
        initial_checkpoint: &ExtendedSequenceNumber,
        initial_position: &InitialPositionInStreamExtended,
    ) -> Result<(), FetchError>;

    /// Advance the iterator to the given sequence number. See
    /// [`initialize`](Self::initialize) for the error semantics (this is the
    /// same `advanceIteratorTo` under the hood).
    async fn advance_iterator_to(
        &self,
        sequence_number: &str,
        initial_position: &InitialPositionInStreamExtended,
    ) -> Result<(), FetchError>;

    /// Get a fresh iterator from the last known sequence number (reconnect).
    ///
    /// Port of `restartIterator()`. Panics (Java `IllegalStateException`) if the
    /// fetcher was never initialized. Otherwise see
    /// [`initialize`](Self::initialize) for the error semantics.
    async fn restart_iterator(&self) -> Result<(), FetchError>;

    /// Reset iterator state directly (no network call): used by the publisher on
    /// `restartFrom`. Port of `resetIterator(...)`.
    fn reset_iterator(
        &self,
        shard_iterator: Option<String>,
        sequence_number: &str,
        initial_position: &InitialPositionInStreamExtended,
    );

    /// The stream identifier. Port of `getStreamIdentifier()`.
    fn stream_identifier(&self) -> StreamIdentifier;

    /// Whether shard end has been reached. Port of `isShardEndReached()`.
    fn is_shard_end_reached(&self) -> bool;

    /// The current next iterator (exposed for tests). Port of `getNextIterator()`.
    fn next_iterator(&self) -> Option<String>;
}
