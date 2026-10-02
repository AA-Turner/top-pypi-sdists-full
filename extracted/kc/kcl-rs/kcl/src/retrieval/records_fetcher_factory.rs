//! Port of `software.amazon.kinesis.retrieval.RecordsFetcherFactory`.

use std::sync::Arc;

use crate::metrics::MetricsFactory;
use crate::retrieval::data_fetching_strategy::DataFetchingStrategy;
use crate::retrieval::get_records_retrieval_strategy::GetRecordsRetrievalStrategy;
use crate::retrieval::polling::sleep_time_controller::SleepTimeController;
use crate::retrieval::records_publisher::RecordsPublisher;

/// Factory + mutable configuration surface for constructing a
/// [`RecordsPublisher`] (queue sizing, byte/record limits, fetch strategy, idle
/// sleep, reduced-TPS threshold) given a [`GetRecordsRetrievalStrategy`].
///
/// Port of the Java interface. Java uses same-named fluent get/set overloads
/// (`maxByteSize()` / `maxByteSize(int)`); Rust has no overloading, so each pair
/// is split into a getter (`fn max_byte_size(&self) -> i32`) and a setter
/// (`fn set_max_byte_size(&mut self, v: i32)`).
///
/// The sole implementation is `polling.SimpleRecordsFetcherFactory` (polling wave
/// 8), which constructs a `PrefetchRecordsPublisher` backed by a background
/// prefetch task per shard.
///
/// The [`SleepTimeController`] (polling wave) is now wired through
/// [`create_records_fetcher`](Self::create_records_fetcher), matching Java's
/// modern `createRecordsFetcher(..., SleepTimeController)` overload (the
/// deprecated no-controller overload is dropped).
pub trait RecordsFetcherFactory: Send + Sync {
    /// Create a [`RecordsPublisher`] for the given shard.
    ///
    /// Port of `createRecordsFetcher(GetRecordsRetrievalStrategy, String,
    /// MetricsFactory, int maxRecords, SleepTimeController)`.
    fn create_records_fetcher(
        &self,
        get_records_retrieval_strategy: Arc<dyn GetRecordsRetrievalStrategy>,
        shard_id: &str,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        max_records: i32,
        sleep_time_controller: Arc<dyn SleepTimeController>,
    ) -> Arc<dyn RecordsPublisher>;

    /// The maximum number of `ProcessRecordsInput` objects the publisher may
    /// hold before further requests block.
    fn max_pending_process_records_input(&self) -> i32;
    /// Set [`max_pending_process_records_input`](Self::max_pending_process_records_input).
    fn set_max_pending_process_records_input(&mut self, value: i32);

    /// The maximum byte size the publisher may hold before blocking.
    fn max_byte_size(&self) -> i32;
    /// Set [`max_byte_size`](Self::max_byte_size).
    fn set_max_byte_size(&mut self, value: i32);

    /// The maximum record count the publisher may hold before blocking.
    fn max_records_count(&self) -> i32;
    /// Set [`max_records_count`](Self::max_records_count).
    fn set_max_records_count(&mut self, value: i32);

    /// The data-fetching strategy determining the publisher type.
    fn data_fetching_strategy(&self) -> DataFetchingStrategy;
    /// Set [`data_fetching_strategy`](Self::data_fetching_strategy).
    fn set_data_fetching_strategy(&mut self, value: DataFetchingStrategy);

    /// The idle time (millis) between two get calls.
    fn idle_millis_between_calls(&self) -> i64;
    /// Set [`idle_millis_between_calls`](Self::idle_millis_between_calls).
    fn set_idle_millis_between_calls(&mut self, value: i64);

    /// The `millisBehindLatest` threshold that triggers reduced throughput near
    /// the tip of the stream.
    fn millis_behind_latest_threshold_for_reduced_tps(&self) -> i64;
    /// Set [`millis_behind_latest_threshold_for_reduced_tps`](Self::millis_behind_latest_threshold_for_reduced_tps).
    fn set_millis_behind_latest_threshold_for_reduced_tps(&mut self, value: i64);
}
