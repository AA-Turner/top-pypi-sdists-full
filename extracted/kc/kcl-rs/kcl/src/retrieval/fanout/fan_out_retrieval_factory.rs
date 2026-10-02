//! Port of `software.amazon.kinesis.retrieval.fanout.FanOutRetrievalFactory`.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use crate::common::{StreamConfig, StreamIdentifier};
use crate::leases::ShardInfo;
use crate::metrics::MetricsFactory;
use crate::retrieval::fanout::fan_out_records_publisher::FanOutRecordsPublisher;
use crate::retrieval::records_publisher::RecordsPublisher;
use crate::retrieval::retrieval_factory::RetrievalFactory;

/// A synchronous callback that resolves (creating on demand) a consumer ARN for a
/// stream name.
///
/// Port of Java's `Function<String, String> consumerArnCreator` (which internally
/// blocks on the EFO consumer registration). The default production wiring
/// (`FanOutConfig`) supplies one that drives [`FanOutConsumerRegistration`]; tests
/// inject a counting stub.
pub type ConsumerArnCreator = Arc<dyn Fn(&str) -> String + Send + Sync>;

/// [`RetrievalFactory`] for EFO: builds a [`FanOutRecordsPublisher`] per shard,
/// memoizing implicitly-created consumer ARNs per [`StreamIdentifier`].
///
/// Port of the Java `@RequiredArgsConstructor` class.
pub struct FanOutRetrievalFactory {
    kinesis_client: aws_sdk_kinesis::Client,
    #[allow(dead_code)]
    default_stream_name: Option<String>,
    default_consumer_arn: Option<String>,
    consumer_arn_creator: ConsumerArnCreator,
    /// Memoizes implicitly-created consumer ARNs per stream (Java
    /// `implicitConsumerArnTracker`). **Deviation:** the Java field is a plain
    /// non-thread-safe `HashMap`; we harden it with a `Mutex` (a bug fix under
    /// concurrent multi-stream startup — see the arch-map note), preserving the
    /// once-per-stream memoization semantics.
    implicit_consumer_arn_tracker: Mutex<HashMap<String, String>>,
}

impl FanOutRetrievalFactory {
    /// Construct.
    pub fn new(
        kinesis_client: aws_sdk_kinesis::Client,
        default_stream_name: Option<String>,
        default_consumer_arn: Option<String>,
        consumer_arn_creator: ConsumerArnCreator,
    ) -> Self {
        Self {
            kinesis_client,
            default_stream_name,
            default_consumer_arn,
            consumer_arn_creator,
            implicit_consumer_arn_tracker: Mutex::new(HashMap::new()),
        }
    }

    /// Java `getOrCreateConsumerArn`: an explicit `consumer_arn` is used directly
    /// (never cached); otherwise the creator runs once per stream (memoized).
    fn get_or_create_consumer_arn(
        &self,
        stream_identifier: &StreamIdentifier,
        consumer_arn: Option<&str>,
    ) -> String {
        if let Some(arn) = consumer_arn {
            return arn.to_string();
        }
        let key = stream_identifier.serialize();
        let mut tracker = self.implicit_consumer_arn_tracker.lock().unwrap();
        if let Some(existing) = tracker.get(&key) {
            return existing.clone();
        }
        let created = (self.consumer_arn_creator)(stream_identifier.stream_name());
        tracker.insert(key, created.clone());
        created
    }
}

impl RetrievalFactory for FanOutRetrievalFactory {
    fn create_get_records_cache(
        &self,
        shard_info: &ShardInfo,
        stream_config: &StreamConfig,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _consumer_id: Option<&str>,
    ) -> Arc<dyn RecordsPublisher> {
        match shard_info.stream_identifier_ser_opt() {
            Some(ser) => {
                // Multi-stream: consumer ARN from the per-stream override.
                let arn = self.get_or_create_consumer_arn(
                    stream_config.stream_identifier(),
                    stream_config.consumer_arn(),
                );
                Arc::new(FanOutRecordsPublisher::new_multi_stream(
                    self.kinesis_client.clone(),
                    shard_info.shard_id(),
                    arn,
                    ser.to_string(),
                    stream_config.stream_identifier().clone(),
                ))
            }
            None => {
                let arn = self.get_or_create_consumer_arn(
                    stream_config.stream_identifier(),
                    self.default_consumer_arn.as_deref(),
                );
                Arc::new(FanOutRecordsPublisher::new(
                    self.kinesis_client.clone(),
                    shard_info.shard_id(),
                    arn,
                    stream_config.stream_identifier().clone(),
                ))
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended, StreamConfig};
    use crate::leases::ShardInfo;
    use crate::metrics::NullMetricsFactory;
    use std::sync::atomic::{AtomicUsize, Ordering};

    fn client() -> aws_sdk_kinesis::Client {
        aws_sdk_kinesis::Client::from_conf(
            aws_sdk_kinesis::Config::builder()
                .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
                .region(aws_sdk_kinesis::config::Region::new("us-east-1"))
                .build(),
        )
    }

    fn shard_info() -> ShardInfo {
        ShardInfo::single_stream("shardId-0", None, Vec::<String>::new(), None)
    }

    fn stream_config() -> StreamConfig {
        StreamConfig::new(
            StreamIdentifier::single_stream_instance("stream"),
            InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest),
        )
    }

    // Port of FanOutConfigTest.testNoRegisterIfConsumerArnSet + factory behavior:
    // an explicit default consumer ARN is used directly, the creator is never called.
    #[test]
    fn explicit_consumer_arn_skips_creator() {
        let calls = Arc::new(AtomicUsize::new(0));
        let calls2 = Arc::clone(&calls);
        let creator: ConsumerArnCreator = Arc::new(move |_name: &str| {
            calls2.fetch_add(1, Ordering::SeqCst);
            "created-arn".to_string()
        });
        let factory = FanOutRetrievalFactory::new(
            client(),
            Some("stream".to_string()),
            Some("explicit-arn".to_string()),
            creator,
        );
        let _ = factory.create_get_records_cache(
            &shard_info(),
            &stream_config(),
            Arc::new(NullMetricsFactory),
            None,
        );
        assert_eq!(
            calls.load(Ordering::SeqCst),
            0,
            "creator must not run when ARN is set"
        );
    }

    // The creator runs once per stream identifier (memoized) — Java
    // implicitConsumerArnTracker.computeIfAbsent.
    #[test]
    fn creator_memoized_per_stream() {
        let calls = Arc::new(AtomicUsize::new(0));
        let calls2 = Arc::clone(&calls);
        let creator: ConsumerArnCreator = Arc::new(move |_name: &str| {
            calls2.fetch_add(1, Ordering::SeqCst);
            "created-arn".to_string()
        });
        let factory =
            FanOutRetrievalFactory::new(client(), Some("stream".to_string()), None, creator);
        for _ in 0..3 {
            let _ = factory.create_get_records_cache(
                &shard_info(),
                &stream_config(),
                Arc::new(NullMetricsFactory),
                None,
            );
        }
        assert_eq!(
            calls.load(Ordering::SeqCst),
            1,
            "creator runs once per stream"
        );
    }
}
