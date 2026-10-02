//! Port of `software.amazon.kinesis.processor`.
//!
//! The customer-facing processing SPI: the [`ShardRecordProcessor`] callback
//! interface and its factory, the checkpointing interfaces
//! ([`RecordProcessorCheckpointer`], [`Checkpointer`], [`PreparedCheckpointer`]),
//! stream tracking ([`StreamTracker`], [`SingleStreamTracker`],
//! [`MultiStreamTracker`], [`FormerStreamsLeasesDeletionStrategy`]) and
//! [`ProcessorConfig`].
//!
//! These are pure interface/data-holder types. The callback and checkpointing
//! traits are **synchronous** (the Java methods are `void`/blocking and the
//! Python interface is synchronous).

pub mod checkpointer;
pub mod former_streams_leases_deletion_strategy;
pub mod multi_stream_tracker;
pub mod prepared_checkpointer;
pub mod processor_config;
pub mod record_processor_checkpointer;
pub mod shard_record_processor;
pub mod shard_record_processor_factory;
pub mod shutdown_notification_aware;
pub mod single_stream_tracker;
pub mod stream_tracker;

pub use checkpointer::Checkpointer;
pub use former_streams_leases_deletion_strategy::{
    AutoDetectionAndDeferredDeletionStrategy, FormerStreamsLeasesDeletionStrategy,
    NoLeaseDeletionStrategy, ProvidedStreamsDeferredDeletionStrategy, StreamsLeasesDeletionType,
};
pub use multi_stream_tracker::MultiStreamTracker;
pub use prepared_checkpointer::PreparedCheckpointer;
pub use processor_config::ProcessorConfig;
pub use record_processor_checkpointer::RecordProcessorCheckpointer;
pub use shard_record_processor::ShardRecordProcessor;
pub use shard_record_processor_factory::ShardRecordProcessorFactory;
#[allow(deprecated)]
pub use shutdown_notification_aware::ShutdownNotificationAware;
pub use single_stream_tracker::SingleStreamTracker;
pub use stream_tracker::StreamTracker;

#[cfg(test)]
pub use checkpointer::MockCheckpointer;
#[cfg(test)]
pub use prepared_checkpointer::MockPreparedCheckpointer;
#[cfg(test)]
pub use record_processor_checkpointer::MockRecordProcessorCheckpointer;
#[cfg(test)]
pub use shard_record_processor::MockShardRecordProcessor;
