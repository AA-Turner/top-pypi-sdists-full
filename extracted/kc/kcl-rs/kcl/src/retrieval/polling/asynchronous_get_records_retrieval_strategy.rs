//! Port of `software.amazon.kinesis.retrieval.polling.AsynchronousGetRecordsRetrievalStrategy`.
//!
//! A retry-with-timeout [`GetRecordsRetrievalStrategy`]. Java submits the blocking
//! `dataFetcher.getRecords()` to a bounded thread pool via a `CompletionService`,
//! polling with a `retryGetRecordsInSeconds` timeout and resubmitting on timeout,
//! to bound how long one logical `getRecords()` can hang.
//!
//! # Deviation (secondary/legacy path)
//!
//! This strategy is **not** wired into the default polling pipeline
//! (`SynchronousBlockingRetrievalFactory` always uses the synchronous strategy).
//! The Rust port replaces the thread-pool + `CompletionService` retry loop with
//! an async loop: each attempt awaits `data_fetcher.get_records()` under a
//! `tokio::time::timeout(retry_get_records)`; on timeout it retries, and an
//! `ExpiredIterator` failure short-circuits immediately (Java rethrows
//! `ExpiredIteratorException` out of the loop). The Java tests that mock
//! `ExecutorService`/`CompletionService`/`Future` scheduling are not ported
//! (they exercise Java threadpool wiring with no Rust analog); the equivalent
//! retry-loop behaviors are covered here.

use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;

use crate::retrieval::get_records_response_adapter::GetRecordsResponseAdapter;
use crate::retrieval::get_records_retrieval_strategy::GetRecordsRetrievalStrategy;
use crate::retrieval::polling::data_fetcher::{DataFetcher, FetchError};

/// A retry-with-timeout retrieval strategy over an async [`DataFetcher`].
pub struct AsynchronousGetRecordsRetrievalStrategy {
    data_fetcher: Arc<dyn DataFetcher>,
    retry_get_records: Duration,
    shard_id: String,
    shutdown: AtomicBool,
}

impl AsynchronousGetRecordsRetrievalStrategy {
    /// Construct with the retry timeout (seconds) and shard id.
    pub fn new(
        data_fetcher: Arc<dyn DataFetcher>,
        retry_get_records_in_seconds: u64,
        shard_id: impl Into<String>,
    ) -> Self {
        Self {
            data_fetcher,
            retry_get_records: Duration::from_secs(retry_get_records_in_seconds),
            shard_id: shard_id.into(),
            shutdown: AtomicBool::new(false),
        }
    }
}

#[async_trait]
impl GetRecordsRetrievalStrategy for AsynchronousGetRecordsRetrievalStrategy {
    async fn get_records_adapter(
        &self,
        _max_records: i32,
    ) -> Result<Box<dyn GetRecordsResponseAdapter>, FetchError> {
        if self.shutdown.load(Ordering::SeqCst) {
            panic!("Strategy has been shutdown");
        }
        loop {
            match tokio::time::timeout(self.retry_get_records, self.data_fetcher.get_records())
                .await
            {
                // Timed out: retry (Java resubmits on poll timeout).
                Err(_elapsed) => {
                    tracing::debug!("{}: GetRecords attempt timed out; retrying.", self.shard_id);
                    continue;
                }
                // Fetch failed with ExpiredIterator: propagate immediately.
                Ok(Err(e @ FetchError::ExpiredIterator { .. })) => return Err(e),
                // Other fetch failures: log and retry (Java logs + loops).
                Ok(Err(e)) => {
                    tracing::error!(
                        "{}: {} while trying to get records; retrying.",
                        self.shard_id,
                        e
                    );
                    continue;
                }
                // Success: accept + return.
                Ok(Ok(result)) => return Ok(result.accept_adapter()),
            }
        }
    }

    fn shutdown(&self) {
        self.shutdown.store(true, Ordering::SeqCst);
    }

    fn is_shutdown(&self) -> bool {
        self.shutdown.load(Ordering::SeqCst)
    }

    fn get_data_fetcher(&self) -> Arc<dyn DataFetcher> {
        Arc::clone(&self.data_fetcher)
    }
}
