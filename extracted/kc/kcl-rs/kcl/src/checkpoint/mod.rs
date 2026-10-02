//! Port of `software.amazon.kinesis.checkpoint`.

// `checkpoint::checkpoint` mirrors the Java `checkpoint` package containing the
// `Checkpoint` class (one Java class -> one snake_case file); the repeated name
// is intentional under the 1:1 package/class mapping, not an oversight.
#[allow(clippy::module_inception)]
pub mod checkpoint;
pub mod checkpoint_config;
pub mod checkpoint_factory;
pub mod does_nothing_prepared_checkpointer;
pub mod dynamodb;
pub mod sentinel_checkpoint;
pub mod sequence_number_validator;
pub mod shard_prepared_checkpointer;
pub mod shard_record_processor_checkpointer;

#[cfg(test)]
pub(crate) mod in_memory_checkpointer;

pub use checkpoint::Checkpoint;
pub use checkpoint_config::CheckpointConfig;
pub use checkpoint_factory::CheckpointFactory;
pub use does_nothing_prepared_checkpointer::DoesNothingPreparedCheckpointer;
pub use sentinel_checkpoint::SentinelCheckpoint;
pub use sequence_number_validator::SequenceNumberValidator;
pub use shard_prepared_checkpointer::ShardPreparedCheckpointer;
pub use shard_record_processor_checkpointer::ShardRecordProcessorCheckpointer;
