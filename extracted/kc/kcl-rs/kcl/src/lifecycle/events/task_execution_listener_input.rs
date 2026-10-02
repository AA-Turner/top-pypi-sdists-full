//! Port of `software.amazon.kinesis.lifecycle.events.TaskExecutionListenerInput`.

use crate::leases::ShardInfo;
use crate::lifecycle::{TaskOutcome, TaskType};

/// Parameters to the `TaskExecutionListener`'s `before_task_execution` /
/// `after_task_execution` methods.
///
/// Port of the Lombok `@Data @Builder(toBuilder=true) @Accessors(fluent=true)`
/// class. `shard_info` (the Java `ShardInfo` field) is included now that
/// `leases::ShardInfo` is ported; the `ShardConsumer` state machine constructs
/// this input with the shard being processed.
#[derive(Debug, Clone, PartialEq, Eq, Hash, bon::Builder)]
pub struct TaskExecutionListenerInput {
    /// The shard for which the task is executing.
    shard_info: Option<ShardInfo>,
    /// The type of task being executed for the shard (corresponds to the shard's state).
    task_type: Option<TaskType>,
    /// The outcome of the task execution for the shard.
    task_outcome: Option<TaskOutcome>,
}

impl TaskExecutionListenerInput {
    /// The shard the task is executing for.
    pub fn shard_info(&self) -> Option<&ShardInfo> {
        self.shard_info.as_ref()
    }

    /// The type of task being executed.
    pub fn task_type(&self) -> Option<TaskType> {
        self.task_type
    }

    /// The outcome of the task execution.
    pub fn task_outcome(&self) -> Option<TaskOutcome> {
        self.task_outcome
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builder_and_getters() {
        let input = TaskExecutionListenerInput::builder()
            .task_type(TaskType::Process)
            .task_outcome(TaskOutcome::Successful)
            .build();
        assert_eq!(input.task_type(), Some(TaskType::Process));
        assert_eq!(input.task_outcome(), Some(TaskOutcome::Successful));
    }

    #[test]
    fn equality_is_field_based() {
        let a = TaskExecutionListenerInput::builder()
            .task_type(TaskType::Initialize)
            .build();
        let b = TaskExecutionListenerInput::builder()
            .task_type(TaskType::Initialize)
            .build();
        assert_eq!(a, b);
    }
}
