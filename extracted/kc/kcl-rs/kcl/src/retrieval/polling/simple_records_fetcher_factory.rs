//! Port of `software.amazon.kinesis.retrieval.polling.SimpleRecordsFetcherFactory`.

use std::sync::Arc;

use crate::metrics::MetricsFactory;
use crate::retrieval::data_fetching_strategy::DataFetchingStrategy;
use crate::retrieval::get_records_retrieval_strategy::GetRecordsRetrievalStrategy;
use crate::retrieval::polling::prefetch_records_publisher::PrefetchRecordsPublisher;
use crate::retrieval::polling::sleep_time_controller::SleepTimeController;
use crate::retrieval::records_fetcher_factory::RecordsFetcherFactory;
use crate::retrieval::records_publisher::RecordsPublisher;
use crate::retrieval::throttling_reporter::ThrottlingReporter;

/// The default reduced-TPS threshold (Java
/// `PollingConfig.DEFAULT_MILLIS_BEHIND_LATEST_THRESHOLD_FOR_REDUCED_TPS`).
const DEFAULT_MILLIS_BEHIND_LATEST_THRESHOLD_FOR_REDUCED_TPS: i64 = 0;

/// The default [`RecordsFetcherFactory`], producing a
/// [`PrefetchRecordsPublisher`] per shard.
///
/// Port of the Java class. The Java per-shard single-thread daemon
/// `ExecutorService` maps to the publisher's single spawned tokio task (created
/// on `start`), so no executor is stored here. Default tuning knobs mirror Java:
/// `maxPendingProcessRecordsInput=3`, `maxByteSize=8MB`, `maxRecordsCount=30000`,
/// `idleMillisBetweenCalls=1500`, `maxConsecutiveThrottles=5` (hardcoded).
pub struct SimpleRecordsFetcherFactory {
    max_pending_process_records_input: i32,
    max_byte_size: i32,
    max_records_count: i32,
    idle_millis_between_calls: i64,
    millis_behind_latest_threshold_for_reduced_tps: i64,
    max_consecutive_throttles: i32,
    data_fetching_strategy: DataFetchingStrategy,
}

impl Default for SimpleRecordsFetcherFactory {
    fn default() -> Self {
        Self {
            max_pending_process_records_input: 3,
            max_byte_size: 8 * 1024 * 1024,
            max_records_count: 30_000,
            idle_millis_between_calls: 1500,
            millis_behind_latest_threshold_for_reduced_tps:
                DEFAULT_MILLIS_BEHIND_LATEST_THRESHOLD_FOR_REDUCED_TPS,
            max_consecutive_throttles: 5,
            data_fetching_strategy: DataFetchingStrategy::Default,
        }
    }
}

impl SimpleRecordsFetcherFactory {
    /// Construct with Java defaults.
    pub fn new() -> Self {
        Self::default()
    }

    /// Construct from explicit config values (used by `PollingConfig` to snapshot
    /// a configured factory into an owned `Arc`). `max_consecutive_throttles`
    /// stays at the Java default (5, not exposed on the interface).
    pub fn from_values(
        max_pending_process_records_input: i32,
        max_byte_size: i32,
        max_records_count: i32,
        idle_millis_between_calls: i64,
        millis_behind_latest_threshold_for_reduced_tps: i64,
        data_fetching_strategy: DataFetchingStrategy,
    ) -> Self {
        Self {
            max_pending_process_records_input,
            max_byte_size,
            max_records_count,
            idle_millis_between_calls,
            millis_behind_latest_threshold_for_reduced_tps,
            max_consecutive_throttles: 5,
            data_fetching_strategy,
        }
    }
}

impl RecordsFetcherFactory for SimpleRecordsFetcherFactory {
    fn create_records_fetcher(
        &self,
        get_records_retrieval_strategy: Arc<dyn GetRecordsRetrievalStrategy>,
        shard_id: &str,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        max_records: i32,
        sleep_time_controller: Arc<dyn SleepTimeController>,
    ) -> Arc<dyn RecordsPublisher> {
        Arc::new(PrefetchRecordsPublisher::new(
            self.max_pending_process_records_input as usize,
            self.max_byte_size as i64,
            self.max_records_count as i64,
            max_records,
            get_records_retrieval_strategy,
            self.idle_millis_between_calls,
            self.millis_behind_latest_threshold_for_reduced_tps,
            metrics_factory,
            "ProcessTask",
            shard_id,
            ThrottlingReporter::new(self.max_consecutive_throttles, shard_id),
            sleep_time_controller,
        ))
    }

    fn max_pending_process_records_input(&self) -> i32 {
        self.max_pending_process_records_input
    }
    fn set_max_pending_process_records_input(&mut self, value: i32) {
        self.max_pending_process_records_input = value;
    }

    fn max_byte_size(&self) -> i32 {
        self.max_byte_size
    }
    fn set_max_byte_size(&mut self, value: i32) {
        self.max_byte_size = value;
    }

    fn max_records_count(&self) -> i32 {
        self.max_records_count
    }
    fn set_max_records_count(&mut self, value: i32) {
        self.max_records_count = value;
    }

    fn data_fetching_strategy(&self) -> DataFetchingStrategy {
        self.data_fetching_strategy
    }
    fn set_data_fetching_strategy(&mut self, value: DataFetchingStrategy) {
        self.data_fetching_strategy = value;
    }

    fn idle_millis_between_calls(&self) -> i64 {
        self.idle_millis_between_calls
    }
    fn set_idle_millis_between_calls(&mut self, value: i64) {
        self.idle_millis_between_calls = value;
    }

    fn millis_behind_latest_threshold_for_reduced_tps(&self) -> i64 {
        self.millis_behind_latest_threshold_for_reduced_tps
    }
    fn set_millis_behind_latest_threshold_for_reduced_tps(&mut self, value: i64) {
        self.millis_behind_latest_threshold_for_reduced_tps = value;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::get_records_retrieval_strategy::MockGetRecordsRetrievalStrategy;
    use crate::retrieval::polling::data_fetcher::MockDataFetcher;
    use crate::retrieval::polling::sleep_time_controller::KinesisSleepTimeController;

    // Port of RecordsFetcherFactoryTest.createPrefetchRecordsFetcherTest: the
    // factory constructs a PrefetchRecordsPublisher (the only publisher type it
    // produces). We assert construction succeeds and the config getters/setters
    // round-trip; the concrete return type is `Arc<dyn RecordsPublisher>` so a
    // downcast type-check is not possible (the Java `instanceof` assertion becomes
    // a successful-construction assertion here).
    #[tokio::test]
    async fn creates_prefetch_records_publisher() {
        let mut fetcher = MockDataFetcher::new();
        fetcher
            .expect_stream_identifier()
            .returning(|| crate::common::StreamIdentifier::single_stream_instance("stream"));
        let fetcher: Arc<dyn crate::retrieval::polling::data_fetcher::DataFetcher> =
            Arc::new(fetcher);

        let mut strategy = MockGetRecordsRetrievalStrategy::new();
        strategy
            .expect_get_data_fetcher()
            .returning(move || Arc::clone(&fetcher));
        let strategy: Arc<dyn GetRecordsRetrievalStrategy> = Arc::new(strategy);

        let factory = SimpleRecordsFetcherFactory::new();
        let _publisher = factory.create_records_fetcher(
            strategy,
            "TestShard",
            Arc::new(NullMetricsFactory),
            1,
            Arc::new(KinesisSleepTimeController),
        );
    }

    #[test]
    fn config_setters_round_trip() {
        let mut f = SimpleRecordsFetcherFactory::new();
        assert_eq!(f.max_pending_process_records_input(), 3);
        assert_eq!(f.max_byte_size(), 8 * 1024 * 1024);
        assert_eq!(f.max_records_count(), 30_000);
        assert_eq!(f.idle_millis_between_calls(), 1500);
        f.set_max_pending_process_records_input(2);
        f.set_max_byte_size(1024);
        f.set_max_records_count(100);
        f.set_idle_millis_between_calls(500);
        f.set_millis_behind_latest_threshold_for_reduced_tps(42);
        f.set_data_fetching_strategy(DataFetchingStrategy::PrefetchCached);
        assert_eq!(f.max_pending_process_records_input(), 2);
        assert_eq!(f.max_byte_size(), 1024);
        assert_eq!(f.max_records_count(), 100);
        assert_eq!(f.idle_millis_between_calls(), 500);
        assert_eq!(f.millis_behind_latest_threshold_for_reduced_tps(), 42);
        assert_eq!(
            f.data_fetching_strategy(),
            DataFetchingStrategy::PrefetchCached
        );
    }
}
