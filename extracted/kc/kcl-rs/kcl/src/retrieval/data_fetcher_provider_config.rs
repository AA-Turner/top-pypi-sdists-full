//! Port of `software.amazon.kinesis.retrieval.DataFetcherProviderConfig` and
//! `software.amazon.kinesis.retrieval.KinesisDataFetcherProviderConfig`.

use std::sync::Arc;
use std::time::Duration;

use crate::common::StreamIdentifier;
use crate::metrics::MetricsFactory;

/// Configuration bundle needed to construct a `DataFetcher` (stream identity,
/// shard id, metrics, max records, timeout, consumer id).
///
/// Port of the Java interface. Implemented by [`KinesisDataFetcherProviderConfig`].
/// The metrics factory is held as `Arc<dyn MetricsFactory>` (shared, per the
/// leases-wave convention).
pub trait DataFetcherProviderConfig: Send + Sync {
    /// The stream identifier for the data fetcher.
    fn stream_identifier(&self) -> &StreamIdentifier;

    /// The shard id.
    fn shard_id(&self) -> &str;

    /// The metrics factory.
    fn metrics_factory(&self) -> Arc<dyn MetricsFactory + Send + Sync>;

    /// The maximum number of records to fetch per call.
    fn max_records(&self) -> i32;

    /// The Kinesis request timeout.
    fn kinesis_request_timeout(&self) -> Duration;

    /// The consumer id (empty string when unset, matching Java's default).
    fn consumer_id(&self) -> &str;
}

/// Concrete [`DataFetcherProviderConfig`] carrying the fields needed by
/// `KinesisDataFetcher`.
///
/// Port of the Java `@Data` value/config class. The `@NonNull` fields become
/// non-`Option` fields (compile-time non-nullability). Two Java constructors
/// (with/without `consumerId`) become [`new`](Self::new) (default empty consumer
/// id) and [`with_consumer_id`](Self::with_consumer_id).
#[derive(Clone)]
pub struct KinesisDataFetcherProviderConfig {
    stream_identifier: StreamIdentifier,
    shard_id: String,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    max_records: i32,
    kinesis_request_timeout: Duration,
    consumer_id: String,
}

impl KinesisDataFetcherProviderConfig {
    /// Construct with an empty consumer id (Java 5-arg constructor delegating
    /// with `""`).
    pub fn new(
        stream_identifier: StreamIdentifier,
        shard_id: impl Into<String>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        max_records: i32,
        kinesis_request_timeout: Duration,
    ) -> Self {
        Self::with_consumer_id(
            stream_identifier,
            shard_id,
            metrics_factory,
            max_records,
            kinesis_request_timeout,
            "",
        )
    }

    /// Construct with an explicit consumer id (Java 6-arg constructor).
    pub fn with_consumer_id(
        stream_identifier: StreamIdentifier,
        shard_id: impl Into<String>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        max_records: i32,
        kinesis_request_timeout: Duration,
        consumer_id: impl Into<String>,
    ) -> Self {
        Self {
            stream_identifier,
            shard_id: shard_id.into(),
            metrics_factory,
            max_records,
            kinesis_request_timeout,
            consumer_id: consumer_id.into(),
        }
    }
}

impl DataFetcherProviderConfig for KinesisDataFetcherProviderConfig {
    fn stream_identifier(&self) -> &StreamIdentifier {
        &self.stream_identifier
    }

    fn shard_id(&self) -> &str {
        &self.shard_id
    }

    fn metrics_factory(&self) -> Arc<dyn MetricsFactory + Send + Sync> {
        Arc::clone(&self.metrics_factory)
    }

    fn max_records(&self) -> i32 {
        self.max_records
    }

    fn kinesis_request_timeout(&self) -> Duration {
        self.kinesis_request_timeout
    }

    fn consumer_id(&self) -> &str {
        &self.consumer_id
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::NullMetricsFactory;

    #[test]
    fn default_consumer_id_is_empty() {
        let cfg = KinesisDataFetcherProviderConfig::new(
            StreamIdentifier::single_stream_instance("my-stream"),
            "shardId-000000000000",
            Arc::new(NullMetricsFactory),
            1000,
            Duration::from_secs(30),
        );
        assert_eq!(cfg.consumer_id(), "");
        assert_eq!(cfg.shard_id(), "shardId-000000000000");
        assert_eq!(cfg.max_records(), 1000);
        assert_eq!(cfg.kinesis_request_timeout(), Duration::from_secs(30));
        assert_eq!(cfg.stream_identifier().stream_name(), "my-stream");
    }

    #[test]
    fn explicit_consumer_id() {
        let cfg = KinesisDataFetcherProviderConfig::with_consumer_id(
            StreamIdentifier::single_stream_instance("s"),
            "shardId-000000000001",
            Arc::new(NullMetricsFactory),
            500,
            Duration::from_secs(10),
            "consumer-abc",
        );
        assert_eq!(cfg.consumer_id(), "consumer-abc");
    }
}
