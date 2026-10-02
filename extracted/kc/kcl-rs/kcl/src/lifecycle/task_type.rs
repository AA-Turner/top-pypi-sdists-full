//! Port of `software.amazon.kinesis.lifecycle.TaskType`.

/// Types of tasks executed as part of processing a shard.
///
/// Ported here (in the `lifecycle` module, its Java home) because
/// [`TaskExecutionListenerInput`](crate::lifecycle::events::TaskExecutionListenerInput)
/// references it.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TaskType {
    /// Polls and waits until parent shard(s) have been fully processed.
    BlockOnParentShards,
    /// Initialization of the record processor (and KCL internal state) for a shard.
    Initialize,
    /// Fetching and processing of records.
    Process,
    /// Shutdown of the record processor.
    Shutdown,
    /// Graceful shutdown requested; the record processor will be notified.
    ShutdownNotification,
    /// Occurs once the shutdown has completed.
    ShutdownComplete,
    /// Sync leases/activities corresponding to Kinesis shards.
    ShardSync,
}
