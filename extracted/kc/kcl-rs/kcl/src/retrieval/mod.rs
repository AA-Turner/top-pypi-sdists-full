//! Port of `software.amazon.kinesis.retrieval`.
//!
//! Record retrieval: the [`RecordsPublisher`] abstraction and its polling and
//! enhanced-fan-out implementations (later waves), plus KPL de-aggregation types,
//! response adapters, iterator building, and the retrieval configuration/factory
//! traits.
//!
//! # `RecordsPublisher` trait (the central abstraction)
//!
//! See [`records_publisher`] for the full design. The reactive-streams
//! `Publisher<RecordsRetrieved>` + demand/ack backpressure is modeled with an
//! object-safe async trait plus a channel-based
//! [`RecordsPublisherSubscription`]/[`RecordsPublisherSink`] pair (the
//! actor/channel translation of Java's coarse-lock reactive contract). Both
//! `FanOutRecordsPublisher` and `PrefetchRecordsPublisher` (retrieval-impl wave)
//! implement it; the lifecycle wave's `ShardConsumer` consumes it.

pub mod aggregator_util;
pub mod aws_exception_manager;
pub mod batch_unique_identifier;
pub mod consumer_registration;
pub mod data_fetcher_provider_config;
pub mod data_fetcher_result;
pub mod data_fetching_strategy;
pub mod data_retrieval_util;
pub mod fanout;
pub mod get_records_response_adapter;
pub mod get_records_retrieval_strategy;
pub mod get_records_retriever;
pub mod iterator_builder;
pub mod kinesis_client_record;
pub mod kinesis_get_records_response_adapter;
pub mod kpl;
pub mod polling;
pub mod records_delivery_ack;
pub mod records_fetcher_factory;
pub mod records_publisher;
pub mod records_retrieved;
pub mod retrieval_config;
pub mod retrieval_factory;
pub mod retrieval_specific_config;
pub mod retryable_retrieval_exception;
pub mod throttling_reporter;

pub use aggregator_util::{AggregatorUtil, AGGREGATED_RECORD_MAGIC};
pub use aws_exception_manager::AwsExceptionManager;
pub use batch_unique_identifier::BatchUniqueIdentifier;
pub use consumer_registration::ConsumerRegistration;
pub use data_fetcher_provider_config::{
    DataFetcherProviderConfig, KinesisDataFetcherProviderConfig,
};
pub use data_fetcher_result::DataFetcherResult;
pub use data_fetching_strategy::DataFetchingStrategy;
pub use data_retrieval_util::is_valid_result;
pub use get_records_response_adapter::GetRecordsResponseAdapter;
pub use get_records_retrieval_strategy::GetRecordsRetrievalStrategy;
pub use get_records_retriever::GetRecordsRetriever;
pub use kinesis_client_record::KinesisClientRecord;
pub use kinesis_get_records_response_adapter::KinesisGetRecordsResponseAdapter;
pub use records_delivery_ack::{RecordsDeliveryAck, SimpleRecordsDeliveryAck};
pub use records_fetcher_factory::RecordsFetcherFactory;
pub use records_publisher::{
    new_subscription, DemandSignal, RecordsDelivery, RecordsPublisher, RecordsPublisherSink,
    RecordsPublisherSubscription,
};
pub use records_retrieved::RecordsRetrieved;
pub use retrieval_config::RetrievalConfig;
pub use retrieval_factory::RetrievalFactory;
pub use retrieval_specific_config::RetrievalSpecificConfig;
pub use retryable_retrieval_exception::RetrievalError;
pub use throttling_reporter::{ThrottleLogLevel, ThrottleLogSink, ThrottlingReporter};

// Concrete polling + fan-out publisher/factory/config implementations.
pub use fanout::{
    FanOutConfig, FanOutConsumerRegistration, FanOutRecordsPublisher, FanOutRetrievalFactory,
    FanoutRecordsRetrieved,
};
pub use polling::{
    AsynchronousGetRecordsRetrievalStrategy, BlockingRecordsPublisher, DataFetcher,
    KinesisDataFetcher, KinesisSleepTimeController, PollingConfig, PrefetchRecordsPublisher,
    PrefetchRecordsRetrieved, SimpleRecordsFetcherFactory, SleepTimeController,
    SleepTimeControllerConfig, SynchronousBlockingRetrievalFactory,
    SynchronousGetRecordsRetrievalStrategy,
};

#[cfg(test)]
pub use get_records_retrieval_strategy::MockGetRecordsRetrievalStrategy;

/// User-agent name identifying the KCL library, applied to Kinesis requests.
///
/// Port of `RetrievalConfig.KINESIS_CLIENT_LIB_USER_AGENT`. This exact string is
/// load-bearing (AWS-side traffic attribution).
pub const KINESIS_CLIENT_LIB_USER_AGENT: &str = "amazon-kinesis-client-library-java";

/// User-agent version for the KCL library.
///
/// Port of `RetrievalConfig.KINESIS_CLIENT_LIB_USER_AGENT_VERSION`, which in Java
/// resolves to `KinesisClientLibraryPackage.VERSION` (the Maven
/// `${project.version}`). Here it resolves to this crate's Cargo package version.
pub const KINESIS_CLIENT_LIB_USER_AGENT_VERSION: &str = env!("CARGO_PKG_VERSION");
