//! Port of `software.amazon.kinesis.lifecycle.TaskOutcome`.

/// Outcome of a task executed as part of processing a shard.
///
/// Ported here (in the `lifecycle` module, its Java home) because
/// [`TaskExecutionListenerInput`](crate::lifecycle::events::TaskExecutionListenerInput)
/// references it.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TaskOutcome {
    /// A successful task outcome.
    Successful,
    /// The last record from the shard has been read/consumed.
    EndOfShard,
    /// A failure or exception during processing of the shard.
    Failure,
}
