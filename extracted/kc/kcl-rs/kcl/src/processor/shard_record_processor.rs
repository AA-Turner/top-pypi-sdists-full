//! Port of `software.amazon.kinesis.processor.ShardRecordProcessor`.

use crate::lifecycle::events::{
    InitializationInput, LeaseLostInput, ProcessRecordsInput, ShardEndedInput,
    ShutdownRequestedInput,
};

/// The core customer-implemented callback interface for processing a single
/// shard's lifecycle.
///
/// Ported as a **synchronous** trait (the Java methods are `void`/blocking and
/// the Python interface is synchronous). KCL invokes these methods sequentially
/// per shard.
///
/// Contract subtleties preserved from Java (documented, not compiler-enforced):
/// * [`shard_ended`](ShardRecordProcessor::shard_ended) **must** call
///   `checkpoint()` before returning, or child shards never make progress.
/// * [`shutdown_requested`](ShardRecordProcessor::shutdown_requested) is called
///   while the lease is still held (checkpointing is still possible).
/// * Once [`lease_lost`](ShardRecordProcessor::lease_lost) fires, checkpointing
///   is no longer valid.
///
/// `#[automock]` provides a mock for tests (the Java tests mock this interface).
#[cfg_attr(test, mockall::automock)]
pub trait ShardRecordProcessor {
    /// Invoked before any records are delivered to this processor.
    fn initialize(&mut self, initialization_input: InitializationInput);

    /// Deliver a batch of data records to the application.
    fn process_records(&mut self, process_records_input: ProcessRecordsInput);

    /// Called when the lease tied to this record processor has been lost. Once
    /// lost, the record processor can no longer checkpoint.
    fn lease_lost(&mut self, lease_lost_input: LeaseLostInput);

    /// Called when the shard this processor handles has been completed.
    ///
    /// The processor **must** call `checkpoint()` on the input's checkpointer
    /// before returning.
    fn shard_ended(&mut self, shard_ended_input: ShardEndedInput);

    /// Called when the Scheduler has been requested to shut down, while the lease
    /// is still held (so checkpointing is possible).
    fn shutdown_requested(&mut self, shutdown_requested_input: ShutdownRequestedInput);
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::processor::MockRecordProcessorCheckpointer;
    use std::sync::Arc;

    #[test]
    fn mock_dispatches_lifecycle_methods() {
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_initialize().times(1).returning(|_| ());
        proc.expect_process_records().times(1).returning(|_| ());
        proc.expect_shard_ended().times(1).returning(|_| ());

        proc.initialize(InitializationInput::builder().shard_id("s").build());
        proc.process_records(ProcessRecordsInput::builder().records(vec![]).build());
        let cp: Arc<dyn RecordProcessorCheckpointer + Send + Sync> =
            Arc::new(MockRecordProcessorCheckpointer::new());
        proc.shard_ended(ShardEndedInput::builder().checkpointer(cp).build());
    }

    use crate::processor::RecordProcessorCheckpointer;
}
