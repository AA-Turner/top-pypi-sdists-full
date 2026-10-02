//! Port of `software.amazon.kinesis.retrieval.polling.SynchronousGetRecordsRetrievalStrategy`.

use std::sync::Arc;

use async_trait::async_trait;

use crate::retrieval::get_records_response_adapter::GetRecordsResponseAdapter;
use crate::retrieval::get_records_retrieval_strategy::GetRecordsRetrievalStrategy;
use crate::retrieval::polling::data_fetcher::{DataFetcher, FetchError};

/// The simplest [`GetRecordsRetrievalStrategy`]: directly fetch via the
/// [`DataFetcher`] and accept the result inline (no thread pool, no retry loop).
///
/// Port of the Java `@Data` class over a single `@NonNull` `DataFetcher` field.
/// `getRecordsAdapter(maxRecords)` maps to `data_fetcher.get_records()?.accept_adapter()`:
/// the fetch may fail with a [`FetchError`] (propagated), and on success the
/// two-phase `accept_adapter` advances the iterator. `max_records` is ignored (the
/// fetcher carries its own configured max), matching Java.
pub struct SynchronousGetRecordsRetrievalStrategy {
    data_fetcher: Arc<dyn DataFetcher>,
}

impl SynchronousGetRecordsRetrievalStrategy {
    /// Construct wrapping the given [`DataFetcher`].
    pub fn new(data_fetcher: Arc<dyn DataFetcher>) -> Self {
        Self { data_fetcher }
    }
}

#[async_trait]
impl GetRecordsRetrievalStrategy for SynchronousGetRecordsRetrievalStrategy {
    async fn get_records_adapter(
        &self,
        _max_records: i32,
    ) -> Result<Box<dyn GetRecordsResponseAdapter>, FetchError> {
        let result = self.data_fetcher.get_records().await?;
        Ok(result.accept_adapter())
    }

    fn shutdown(&self) {
        // No resources to release.
    }

    fn is_shutdown(&self) -> bool {
        false
    }

    fn get_data_fetcher(&self) -> Arc<dyn DataFetcher> {
        Arc::clone(&self.data_fetcher)
    }
}
