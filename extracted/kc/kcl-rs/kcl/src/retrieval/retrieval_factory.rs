//! Port of `software.amazon.kinesis.retrieval.RetrievalFactory`.

use std::sync::Arc;

use crate::common::StreamConfig;
use crate::leases::ShardInfo;
use crate::metrics::MetricsFactory;
use crate::retrieval::records_publisher::RecordsPublisher;

/// Factory producing a [`RecordsPublisher`] for a given shard/stream.
///
/// Port of the Java interface. The Java cascading default-method deprecation
/// chain (`createGetRecordsCache` 4-arg → 3-arg → 2-arg[deprecated] and the
/// deprecated `createGetRecordsRetrievalStrategy`) is collapsed (arch-map: "skip
/// the deprecated chain") into a single modern factory method
/// [`create_get_records_cache`] taking an `Option<consumer_id>`.
///
/// The two Java implementations (`FanOutRetrievalFactory`,
/// `SynchronousBlockingRetrievalFactory`) are in the fan-out / polling waves;
/// they will implement this trait.
///
/// [`create_get_records_cache`]: RetrievalFactory::create_get_records_cache
pub trait RetrievalFactory: Send + Sync {
    /// Create a [`RecordsPublisher`] to retrieve records for `shard_info` on the
    /// stream described by `stream_config`.
    ///
    /// Port of `createGetRecordsCache(ShardInfo, StreamConfig, MetricsFactory,
    /// String consumerId)` (the modern 4-arg form; `consumer_id` is `None` for
    /// the 3-arg form).
    fn create_get_records_cache(
        &self,
        shard_info: &ShardInfo,
        stream_config: &StreamConfig,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        consumer_id: Option<&str>,
    ) -> Arc<dyn RecordsPublisher>;
}
