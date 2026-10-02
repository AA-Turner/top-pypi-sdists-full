//! Port of `software.amazon.kinesis.retrieval.polling`.
//!
//! Classic `GetRecords`/`GetShardIterator` polling retrieval: the async
//! [`DataFetcher`]/[`KinesisDataFetcher`] iterator state machine, the
//! [`GetRecordsRetrievalStrategy`](crate::retrieval::GetRecordsRetrievalStrategy)
//! implementations, the prefetching [`PrefetchRecordsPublisher`] (a single spawned
//! tokio task owning all state), the [`SimpleRecordsFetcherFactory`] /
//! [`SynchronousBlockingRetrievalFactory`] wiring, [`PollingConfig`], and the
//! [`SleepTimeController`] pacing strategy.

pub mod asynchronous_get_records_retrieval_strategy;
pub mod blocking_records_publisher;
pub mod data_fetcher;
pub mod kinesis_data_fetcher;
pub mod polling_config;
pub mod prefetch_records_publisher;
pub mod prefetch_records_retrieved;
pub mod simple_records_fetcher_factory;
pub mod sleep_time_controller;
pub mod synchronous_blocking_retrieval_factory;
pub mod synchronous_get_records_retrieval_strategy;

#[cfg(test)]
pub(crate) mod test_support;

pub use asynchronous_get_records_retrieval_strategy::AsynchronousGetRecordsRetrievalStrategy;
pub use blocking_records_publisher::BlockingRecordsPublisher;
pub use data_fetcher::{DataFetcher, DataFetcherResult, FetchError};
pub use kinesis_data_fetcher::KinesisDataFetcher;
pub use polling_config::PollingConfig;
pub use prefetch_records_publisher::PrefetchRecordsPublisher;
pub use prefetch_records_retrieved::PrefetchRecordsRetrieved;
pub use simple_records_fetcher_factory::SimpleRecordsFetcherFactory;
pub use sleep_time_controller::{
    KinesisSleepTimeController, SleepTimeController, SleepTimeControllerConfig,
};
pub use synchronous_blocking_retrieval_factory::{
    DataFetcherProvider, SynchronousBlockingRetrievalFactory,
};
pub use synchronous_get_records_retrieval_strategy::SynchronousGetRecordsRetrievalStrategy;

#[cfg(test)]
pub use data_fetcher::MockDataFetcher;
