//! Port of `software.amazon.kinesis.retrieval.polling.SynchronousBlockingRetrievalFactory`.

use std::sync::Arc;
use std::time::Duration;

use crate::common::{StreamConfig, StreamIdentifier};
use crate::leases::ShardInfo;
use crate::metrics::MetricsFactory;
use crate::retrieval::data_fetcher_provider_config::{
    DataFetcherProviderConfig, KinesisDataFetcherProviderConfig,
};
use crate::retrieval::polling::data_fetcher::DataFetcher;
use crate::retrieval::polling::kinesis_data_fetcher::KinesisDataFetcher;
use crate::retrieval::polling::simple_records_fetcher_factory::SimpleRecordsFetcherFactory;
use crate::retrieval::polling::sleep_time_controller::{
    KinesisSleepTimeController, SleepTimeController,
};
use crate::retrieval::polling::synchronous_get_records_retrieval_strategy::SynchronousGetRecordsRetrievalStrategy;
use crate::retrieval::records_fetcher_factory::RecordsFetcherFactory;
use crate::retrieval::records_publisher::RecordsPublisher;
use crate::retrieval::retrieval_factory::RetrievalFactory;

/// A factory that builds a data fetcher from a config (injectable override hook).
///
/// Port of Java's `Function<DataFetcherProviderConfig, DataFetcher>`. The default
/// wraps `KinesisDataFetcher::new`.
pub type DataFetcherProvider =
    Arc<dyn Fn(&dyn DataFetcherProviderConfig) -> Arc<dyn DataFetcher> + Send + Sync>;

/// [`RetrievalFactory`] for the polling path: wires a [`KinesisDataFetcher`]
/// (or an injected override) + [`SynchronousGetRecordsRetrievalStrategy`] +
/// the configured [`RecordsFetcherFactory`] into a per-shard [`RecordsPublisher`]
/// (normally a `PrefetchRecordsPublisher`).
///
/// Port of the Java `@Data` class. `dataFetcherProvider` null → the default
/// `KinesisDataFetcher` provider closing over the Kinesis client.
pub struct SynchronousBlockingRetrievalFactory {
    #[allow(dead_code)]
    stream_name: Option<String>,
    kinesis_client: aws_sdk_kinesis::Client,
    records_fetcher_factory: Arc<dyn RecordsFetcherFactory>,
    max_records: i32,
    #[allow(dead_code)]
    kinesis_request_timeout: Duration,
    data_fetcher_provider: DataFetcherProvider,
    sleep_time_controller: Arc<dyn SleepTimeController>,
}

impl SynchronousBlockingRetrievalFactory {
    /// Construct.
    ///
    /// `data_fetcher_provider` `None` substitutes the default provider
    /// (`|cfg| KinesisDataFetcher::new(client, cfg)`).
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        stream_name: Option<String>,
        kinesis_client: aws_sdk_kinesis::Client,
        records_fetcher_factory: Arc<dyn RecordsFetcherFactory>,
        max_records: i32,
        kinesis_request_timeout: Duration,
        data_fetcher_provider: Option<DataFetcherProvider>,
        sleep_time_controller: Arc<dyn SleepTimeController>,
    ) -> Self {
        let client_for_default = kinesis_client.clone();
        let data_fetcher_provider = data_fetcher_provider.unwrap_or_else(|| {
            Arc::new(move |cfg: &dyn DataFetcherProviderConfig| {
                Arc::new(KinesisDataFetcher::new(client_for_default.clone(), cfg))
                    as Arc<dyn DataFetcher>
            })
        });
        Self {
            stream_name,
            kinesis_client,
            records_fetcher_factory,
            max_records,
            kinesis_request_timeout,
            data_fetcher_provider,
            sleep_time_controller,
        }
    }

    /// Convenience constructor with the default `SimpleRecordsFetcherFactory` +
    /// `KinesisSleepTimeController` + default fetcher provider.
    pub fn with_defaults(
        stream_name: Option<String>,
        kinesis_client: aws_sdk_kinesis::Client,
        max_records: i32,
        kinesis_request_timeout: Duration,
    ) -> Self {
        Self::new(
            stream_name,
            kinesis_client,
            Arc::new(SimpleRecordsFetcherFactory::new()),
            max_records,
            kinesis_request_timeout,
            None,
            Arc::new(KinesisSleepTimeController),
        )
    }

    fn create_strategy(
        &self,
        shard_info: &ShardInfo,
        stream_identifier: &StreamIdentifier,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        consumer_id: Option<&str>,
    ) -> Arc<SynchronousGetRecordsRetrievalStrategy> {
        let config: KinesisDataFetcherProviderConfig = match consumer_id {
            Some(id) => KinesisDataFetcherProviderConfig::with_consumer_id(
                stream_identifier.clone(),
                shard_info.shard_id(),
                metrics_factory,
                self.max_records,
                self.kinesis_request_timeout,
                id,
            ),
            None => KinesisDataFetcherProviderConfig::new(
                stream_identifier.clone(),
                shard_info.shard_id(),
                metrics_factory,
                self.max_records,
                self.kinesis_request_timeout,
            ),
        };
        let data_fetcher = (self.data_fetcher_provider)(&config);
        Arc::new(SynchronousGetRecordsRetrievalStrategy::new(data_fetcher))
    }
}

impl RetrievalFactory for SynchronousBlockingRetrievalFactory {
    fn create_get_records_cache(
        &self,
        shard_info: &ShardInfo,
        stream_config: &StreamConfig,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        consumer_id: Option<&str>,
    ) -> Arc<dyn RecordsPublisher> {
        let strategy = self.create_strategy(
            shard_info,
            stream_config.stream_identifier(),
            Arc::clone(&metrics_factory),
            consumer_id,
        );
        self.records_fetcher_factory.create_records_fetcher(
            strategy,
            shard_info.shard_id(),
            metrics_factory,
            self.max_records,
            Arc::clone(&self.sleep_time_controller),
        )
    }
}

/// Keep the Kinesis client field referenced (used only via the default provider
/// closure; suppresses dead-code in configurations that inject a custom provider).
impl SynchronousBlockingRetrievalFactory {
    #[allow(dead_code)]
    fn kinesis_client(&self) -> &aws_sdk_kinesis::Client {
        &self.kinesis_client
    }
}
