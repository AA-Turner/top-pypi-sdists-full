//! Port of `software.amazon.kinesis.lifecycle.TaskExecutionListener` and
//! `NoOpTaskExecutionListener`.

use crate::lifecycle::events::TaskExecutionListenerInput;

/// A listener for callbacks on the task-execution lifecycle for a shard.
///
/// Invoked immediately before and after each `ConsumerTask` execution for a
/// shard, for external observability/instrumentation.
///
/// **Note:** implementations should be non-blocking — these methods sit directly
/// in the `ShardConsumer`'s task-dispatch critical path, so a slow listener
/// serializes/delays all processing for that shard.
pub trait TaskExecutionListener: Send + Sync {
    /// Invoked immediately before a task executes.
    fn before_task_execution(&self, input: &TaskExecutionListenerInput);

    /// Invoked immediately after a task executes.
    fn after_task_execution(&self, input: &TaskExecutionListenerInput);
}

/// A do-nothing [`TaskExecutionListener`] used when no listener is configured.
///
/// Port of `NoOpTaskExecutionListener`.
#[derive(Debug, Default, Clone, Copy)]
pub struct NoOpTaskExecutionListener;

impl TaskExecutionListener for NoOpTaskExecutionListener {
    fn before_task_execution(&self, _input: &TaskExecutionListenerInput) {}

    fn after_task_execution(&self, _input: &TaskExecutionListenerInput) {}
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lifecycle::TaskType;

    #[test]
    fn no_op_listener_does_nothing() {
        let listener = NoOpTaskExecutionListener;
        let input = TaskExecutionListenerInput::builder()
            .task_type(TaskType::Process)
            .build();
        listener.before_task_execution(&input);
        listener.after_task_execution(&input);
    }
}
