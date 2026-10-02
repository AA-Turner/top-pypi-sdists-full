//! Port of `software.amazon.kinesis.retrieval.fanout`.
//!
//! Enhanced-fan-out (EFO) retrieval: the [`FanOutRecordsPublisher`] (a single
//! spawned tokio task driving the `SubscribeToShard` event stream with 1-at-a-time
//! credit + a bounded ack queue), [`FanOutConsumerRegistration`] (register/describe
//! the EFO consumer with retry/backoff), [`FanOutConfig`], and [`FanOutRetrievalFactory`].

pub mod fan_out_config;
pub mod fan_out_consumer_registration;
pub mod fan_out_records_publisher;
pub mod fan_out_retrieval_factory;
pub mod fanout_records_retrieved;

pub use fan_out_config::FanOutConfig;
pub use fan_out_consumer_registration::FanOutConsumerRegistration;
pub use fan_out_records_publisher::{
    FanOutRecordsPublisher, FlowError, FlowEvent, KinesisShardSubscriber, MultipleSubscriberError,
    ShardSubscriber, MAX_EVENT_BURST_FROM_SERVICE,
};
pub use fan_out_retrieval_factory::FanOutRetrievalFactory;
pub use fanout_records_retrieved::FanoutRecordsRetrieved;
