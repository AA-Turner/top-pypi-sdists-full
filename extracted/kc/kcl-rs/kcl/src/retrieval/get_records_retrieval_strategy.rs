//! Port of `software.amazon.kinesis.retrieval.GetRecordsRetrievalStrategy`.

use std::sync::Arc;

use async_trait::async_trait;

use crate::retrieval::get_records_response_adapter::GetRecordsResponseAdapter;
use crate::retrieval::polling::data_fetcher::{DataFetcher, FetchError};

/// Strategy for retrieving a batch of records from Kinesis (sync vs async
/// thread-pool-backed variants in Java), plus lifecycle (`shutdown`) and access
/// to the underlying data fetcher.
///
/// Port of the Java interface. Async because [`get_records_adapter`] hits Kinesis
/// (Java blocks over the async client via `FutureUtils`; the Rust port stays
/// async). `#[automock]` because Java mocks this in its polling tests.
///
/// # Deviations
///
/// * The deprecated raw-`GetRecordsResponse` `getRecords` overload is dropped.
/// * [`get_records_adapter`] returns a `Result<_, FetchError>`: Java throws the
///   underlying SDK exception (`RetryableRetrievalException` / `ExpiredIteratorException`
///   / `InvalidArgumentException` / `ProvisionedThroughputExceededException` /
///   `SdkException`) out of the strategy, and `PrefetchRecordsPublisher`'s daemon
///   `catch`es each distinctly. The Rust port surfaces that classification as a
///   [`FetchError`].
/// * [`get_data_fetcher`](Self::get_data_fetcher) returns the underlying
///   [`DataFetcher`] (Java's `dataFetcher()` accessor). The deprecated
///   `getDataFetcher()`-throws quirk is dropped.
///
/// [`get_records_adapter`]: GetRecordsRetrievalStrategy::get_records_adapter
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait GetRecordsRetrievalStrategy: Send + Sync {
    /// Get a set of records from Kinesis (up to `max_records`).
    ///
    /// Port of the default `getRecordsAdapter(int)` fused with the exception
    /// classification. `max_records` is ignored by the sync strategy (the fetcher
    /// carries its own configured max), matching Java.
    async fn get_records_adapter(
        &self,
        max_records: i32,
    ) -> Result<Box<dyn GetRecordsResponseAdapter>, FetchError>;

    /// Release any resources used by the strategy. After shutdown it is no longer
    /// safe to call [`get_records_adapter`](Self::get_records_adapter).
    fn shutdown(&self);

    /// Whether this strategy has been shut down.
    fn is_shutdown(&self) -> bool;

    /// The underlying [`DataFetcher`] (Java `dataFetcher()`).
    fn get_data_fetcher(&self) -> Arc<dyn DataFetcher>;
}
