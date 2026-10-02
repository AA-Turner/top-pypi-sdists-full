//! Port of `software.amazon.kinesis.lifecycle.events`.
//!
//! The `*Input` value types passed into the [`ShardRecordProcessor`] callback
//! methods, plus [`TaskExecutionListenerInput`].
//!
//! The inputs that carry a checkpointer
//! ([`ProcessRecordsInput`], [`ShardEndedInput`], [`ShutdownRequestedInput`])
//! hold it as `Arc<dyn RecordProcessorCheckpointer + Send + Sync>` and
//! hand-implement `PartialEq`/`Eq`/`Hash` over the data fields only (the
//! checkpointer is excluded, since trait objects cannot derive those traits).
//!
//! [`ShardRecordProcessor`]: crate::processor::ShardRecordProcessor

pub mod initialization_input;
pub mod lease_lost_input;
pub mod process_records_input;
pub mod shard_ended_input;
pub mod shutdown_requested_input;
pub mod task_execution_listener_input;

pub use initialization_input::InitializationInput;
pub use lease_lost_input::LeaseLostInput;
pub use process_records_input::ProcessRecordsInput;
pub use shard_ended_input::ShardEndedInput;
pub use shutdown_requested_input::ShutdownRequestedInput;
pub use task_execution_listener_input::TaskExecutionListenerInput;
