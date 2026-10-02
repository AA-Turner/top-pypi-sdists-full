//! Port of `software.amazon.kinesis.common.ConfigsBuilderTest`.
//!
//! Java's test asserts on the deprecated `appStreamTracker` `Either` (dropped in
//! this port). We instead assert the observable equivalent: the resolved
//! [`StreamTracker`] (single- vs multi-stream, first stream name) and that all
//! seven `*_config()` factory methods materialize, plus the eager
//! `table_name`/`namespace` defaulting.

use std::sync::Arc;

use super::ConfigsBuilder;
use crate::common::Arn;
use crate::processor::shard_record_processor::{MockShardRecordProcessor, ShardRecordProcessor};
use crate::processor::{
    MultiStreamTracker, ShardRecordProcessorFactory, SingleStreamTracker, StreamTracker,
};

const APPLICATION_NAME: &str = "ConfigsBuilderTest";
const WORKER_IDENTIFIER: &str = "worker-id";

struct TestFactory;

impl ShardRecordProcessorFactory for TestFactory {
    fn shard_record_processor(&self) -> Box<dyn ShardRecordProcessor + Send + Sync> {
        Box::new(MockShardRecordProcessor::new())
    }
}

fn clients() -> (
    aws_sdk_kinesis::Client,
    aws_sdk_dynamodb::Client,
    aws_sdk_cloudwatch::Client,
) {
    let region = "us-east-1";
    let kinesis = aws_sdk_kinesis::Client::from_conf(
        aws_sdk_kinesis::Config::builder()
            .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
            .region(aws_sdk_kinesis::config::Region::new(region))
            .build(),
    );
    let ddb = aws_sdk_dynamodb::Client::from_conf(
        aws_sdk_dynamodb::Config::builder()
            .behavior_version(aws_sdk_dynamodb::config::BehaviorVersion::latest())
            .region(aws_sdk_dynamodb::config::Region::new(region))
            .build(),
    );
    let cw = aws_sdk_cloudwatch::Client::from_conf(
        aws_sdk_cloudwatch::Config::builder()
            .behavior_version(aws_sdk_cloudwatch::config::BehaviorVersion::latest())
            .region(aws_sdk_cloudwatch::config::Region::new(region))
            .build(),
    );
    (kinesis, ddb, cw)
}

fn create_config(tracker: Arc<dyn StreamTracker + Send + Sync>) -> ConfigsBuilder {
    let (kinesis, ddb, cw) = clients();
    ConfigsBuilder::new(
        tracker,
        APPLICATION_NAME,
        kinesis,
        ddb,
        cw,
        WORKER_IDENTIFIER,
        Arc::new(TestFactory),
    )
}

fn create_arn(stream_name: &str) -> Arn {
    // arn:aws:kinesis:us-east-1:123456789012:stream/<name>
    Arn::new(
        "aws",
        "kinesis",
        Some("us-east-1".to_string()),
        Some("123456789012".to_string()),
        format!("stream/{stream_name}"),
    )
}

#[test]
fn test_single_stream_tracker_construction() {
    let stream_name = "single-stream";
    let stream_arn = create_arn(stream_name);

    let (kinesis, ddb, cw) = clients();
    let builders = vec![
        ConfigsBuilder::from_stream_name(
            stream_name,
            APPLICATION_NAME,
            kinesis.clone(),
            ddb.clone(),
            cw.clone(),
            WORKER_IDENTIFIER,
            Arc::new(TestFactory),
        ),
        create_config(Arc::new(SingleStreamTracker::from_stream_name(stream_name))),
        ConfigsBuilder::from_stream_arn(
            stream_arn.clone(),
            APPLICATION_NAME,
            kinesis,
            ddb,
            cw,
            WORKER_IDENTIFIER,
            Arc::new(TestFactory),
        ),
        create_config(Arc::new(SingleStreamTracker::from_arn(stream_arn))),
    ];

    for cb in &builders {
        assert!(!cb.stream_tracker().is_multi_stream());
        let configs = cb.stream_tracker().stream_config_list();
        assert_eq!(configs[0].stream_identifier().stream_name(), stream_name);
    }
}

#[test]
fn test_multi_stream_tracker_construction() {
    // A minimal MultiStreamTracker impl (Java mocks MultiStreamTracker.class).
    struct EmptyMultiTracker;
    impl StreamTracker for EmptyMultiTracker {
        fn stream_config_list(&self) -> Vec<crate::common::StreamConfig> {
            Vec::new()
        }
        fn former_streams_leases_deletion_strategy(
            &self,
        ) -> Box<
            dyn crate::processor::former_streams_leases_deletion_strategy::FormerStreamsLeasesDeletionStrategy
                + Send
                + Sync,
        >{
            Box::new(
                crate::processor::former_streams_leases_deletion_strategy::NoLeaseDeletionStrategy,
            )
        }
        fn is_multi_stream(&self) -> bool {
            true
        }
    }
    impl MultiStreamTracker for EmptyMultiTracker {}

    let cb = create_config(Arc::new(EmptyMultiTracker));
    assert!(cb.stream_tracker().is_multi_stream());
}

#[test]
fn table_name_and_namespace_default_to_application_name() {
    let cb = create_config(Arc::new(SingleStreamTracker::from_stream_name("s")));
    assert_eq!(cb.table_name(), APPLICATION_NAME);
    assert_eq!(cb.namespace(), APPLICATION_NAME);

    let cb = cb.set_table_name("custom-table").set_namespace("custom-ns");
    assert_eq!(cb.table_name(), "custom-table");
    assert_eq!(cb.namespace(), "custom-ns");
}

#[tokio::test]
async fn all_seven_config_factories_materialize() {
    let cb = create_config(Arc::new(SingleStreamTracker::from_stream_name("my-stream")));

    let _checkpoint = cb.checkpoint_config();
    let coordinator = cb.coordinator_config();
    assert_eq!(coordinator.application_name(), APPLICATION_NAME);

    let lease = cb.lease_management_config();
    assert_eq!(lease.table_name(), APPLICATION_NAME);
    assert_eq!(lease.worker_identifier(), WORKER_IDENTIFIER);

    let _lifecycle = cb.lifecycle_config();
    let metrics = cb.metrics_config();
    assert_eq!(metrics.namespace(), APPLICATION_NAME);

    let _processor = cb.processor_config();
    let retrieval = cb.retrieval_config();
    assert!(!retrieval.stream_tracker().is_multi_stream());

    // Each factory returns a fresh instance (Java: not memoized).
    let c1 = cb.coordinator_config();
    let c2 = cb.coordinator_config();
    assert_eq!(c1.application_name(), c2.application_name());
}
