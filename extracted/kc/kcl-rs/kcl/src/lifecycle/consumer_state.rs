//! Ports of `software.amazon.kinesis.lifecycle.{ConsumerState, ConsumerStates}`.
//!
//! # Design (enum, not trait objects)
//!
//! Java models the state machine as a package-private `interface ConsumerState`
//! with six singleton implementations nested in `ConsumerStates`. The full state
//! set is **closed** and the states are effectively stateless singletons, so —
//! per the arch-map's recommendation — the Rust port models them as a closed
//! [`ConsumerState`] enum with match-based dispatch (`create_task`,
//! `success_transition`, `failure_transition`, `shutdown_transition`, `task_type`,
//! `state`, `is_terminal`, `requires_data_availability`, `requires_awake`).
//!
//! **The two `SHUTDOWN_REQUESTED` instances are kept distinct.** Java has *two*
//! `ConsumerState` singletons that both report `ShardConsumerState.SHUTDOWN_REQUESTED`
//! from `state()` but differ in `createTask`/transitions: `ShutdownNotificationState`
//! (creates a `ShutdownNotificationTask`) and `ShutdownNotificationCompletionState`
//! (creates no task, `requiresAwake()=true`). They are modeled as two distinct
//! enum variants ([`ConsumerState::ShutdownNotification`] and
//! [`ConsumerState::ShutdownNotificationCompletion`]) whose [`state`](ConsumerState::state)
//! both return [`ShardConsumerState::ShutdownRequested`] — do not collapse them.
//!
//! `createTask` may return `null` in Java (no task for the state) → `Option`.

use aws_sdk_kinesis::types::ChildShard;

use crate::lifecycle::events::ProcessRecordsInput;
use crate::lifecycle::{
    ConsumerTask, ConsumerTaskFactory, ShardConsumerArgument, ShutdownReason, TaskType,
};

/// The kind of processing state a shard consumer is in.
///
/// Port of the Java `enum ConsumerStates.ShardConsumerState`. Different
/// [`ConsumerState`] variants may report the same `ShardConsumerState` (the two
/// shutdown-notification states both report [`ShutdownRequested`](Self::ShutdownRequested)).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ShardConsumerState {
    /// Blocked waiting for parent shards to complete.
    WaitingOnParentShards,
    /// Initializing the record processor.
    Initializing,
    /// Retrieving and dispatching records.
    Processing,
    /// A graceful shutdown was requested (notification or its completion idle).
    ShutdownRequested,
    /// Performing final shutdown (lease lost / shard end).
    ShuttingDown,
    /// Terminal: all shutdown activities complete.
    ShutdownComplete,
}

/// The current state of a shard consumer's state machine.
///
/// Port of the six `ConsumerState` implementations in `ConsumerStates`, plus the
/// distinct `ShutdownNotificationCompletionState` singleton
/// (`ConsumerStates.SHUTDOWN_REQUEST_COMPLETION_STATE`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ConsumerState {
    /// `ConsumerStates.BlockedOnParentState` — the initial state.
    BlockedOnParent,
    /// `ConsumerStates.InitializingState`.
    Initializing,
    /// `ConsumerStates.ProcessingState`.
    Processing,
    /// `ConsumerStates.ShutdownNotificationState` — creates a
    /// `ShutdownNotificationTask`.
    ShutdownNotification,
    /// `ConsumerStates.ShutdownNotificationCompletionState`
    /// (`SHUTDOWN_REQUEST_COMPLETION_STATE`) — creates no task, `requiresAwake`.
    ShutdownNotificationCompletion,
    /// `ConsumerStates.ShuttingDownState`.
    ShuttingDown,
    /// `ConsumerStates.ShutdownCompleteState` — terminal.
    ShutdownComplete,
}

impl ConsumerState {
    /// The initial state (Java `ConsumerStates.INITIAL_STATE`).
    pub fn initial_state() -> ConsumerState {
        ConsumerState::BlockedOnParent
    }

    /// The distinct shutdown-request-completion singleton
    /// (`ConsumerStates.SHUTDOWN_REQUEST_COMPLETION_STATE`).
    pub fn shutdown_request_completion_state() -> ConsumerState {
        ConsumerState::ShutdownNotificationCompletion
    }

    /// Create a new task for this state, or `None` if the state has no task.
    ///
    /// Port of `createTask(argument, consumer, input, taskFactory)`. The Java
    /// `ShardConsumer consumer` parameter is threaded in the driver via `reason`
    /// (for the shutdown task) and `shutdown_notification` (for the
    /// shutdown-notification task) — see [`ConsumerTaskFactory`]. Since only the
    /// `ShuttingDown` and `ShutdownNotification` states need those, they are
    /// passed here.
    pub fn create_task(
        &self,
        argument: &ShardConsumerArgument,
        input: Option<ProcessRecordsInput>,
        task_factory: &dyn ConsumerTaskFactory,
        reason: Option<ShutdownReason>,
        shutdown_notification: Option<std::sync::Arc<dyn crate::lifecycle::ShutdownNotification>>,
    ) -> Option<Box<dyn ConsumerTask>> {
        match self {
            ConsumerState::BlockedOnParent => {
                Some(task_factory.create_block_on_parent_task(argument))
            }
            ConsumerState::Initializing => Some(task_factory.create_initialize_task(argument)),
            ConsumerState::Processing => Some(
                task_factory
                    .create_process_task(argument, input.unwrap_or_else(process_input_default)),
            ),
            ConsumerState::ShutdownNotification => Some(
                task_factory.create_shutdown_notification_task(argument, shutdown_notification),
            ),
            ConsumerState::ShutdownNotificationCompletion => None,
            ConsumerState::ShuttingDown => {
                // Java passes `input == null ? null : input.childShards()`.
                let child_shards: Option<Vec<ChildShard>> = input
                    .as_ref()
                    .and_then(|i| i.child_shards().map(|s| s.to_vec()));
                Some(task_factory.create_shutdown_task(
                    argument,
                    reason.unwrap_or(ShutdownReason::ShardEnd),
                    child_shards,
                ))
            }
            ConsumerState::ShutdownComplete => None,
        }
    }

    /// The state to transition to on task success. Port of `successTransition()`.
    pub fn success_transition(&self) -> ConsumerState {
        match self {
            ConsumerState::BlockedOnParent => ConsumerState::Initializing,
            ConsumerState::Initializing => ConsumerState::Processing,
            ConsumerState::Processing => ConsumerState::Processing,
            ConsumerState::ShutdownNotification => ConsumerState::ShutdownNotificationCompletion,
            ConsumerState::ShutdownNotificationCompletion => {
                ConsumerState::ShutdownNotificationCompletion
            }
            ConsumerState::ShuttingDown => ConsumerState::ShutdownComplete,
            ConsumerState::ShutdownComplete => ConsumerState::ShutdownComplete,
        }
    }

    /// The state to transition to on task failure. Port of `failureTransition()`
    /// (the Java interface default is `this` — no state change — and none of the
    /// six states override it).
    pub fn failure_transition(&self) -> ConsumerState {
        *self
    }

    /// The state to transition to when a shutdown is requested. Port of
    /// `shutdownTransition(ShutdownReason)`.
    pub fn shutdown_transition(&self, shutdown_reason: ShutdownReason) -> ConsumerState {
        match self {
            // Never initialized: go straight to SHUTTING_DOWN on ANY reason.
            ConsumerState::BlockedOnParent => ConsumerState::ShuttingDown,
            // Defer entirely to the reason's target state.
            ConsumerState::Initializing => shutdown_reason.shutdown_state(),
            ConsumerState::Processing => shutdown_reason.shutdown_state(),
            // REQUESTED → the completion singleton (idempotent); else the reason's state.
            ConsumerState::ShutdownNotification => {
                if shutdown_reason == ShutdownReason::Requested {
                    ConsumerState::ShutdownNotificationCompletion
                } else {
                    shutdown_reason.shutdown_state()
                }
            }
            // Non-REQUESTED → the reason's state; REQUESTED → stay.
            ConsumerState::ShutdownNotificationCompletion => {
                if shutdown_reason != ShutdownReason::Requested {
                    shutdown_reason.shutdown_state()
                } else {
                    ConsumerState::ShutdownNotificationCompletion
                }
            }
            // ANY reason → SHUTDOWN_COMPLETE.
            ConsumerState::ShuttingDown => ConsumerState::ShutdownComplete,
            // Terminal: stay.
            ConsumerState::ShutdownComplete => ConsumerState::ShutdownComplete,
        }
    }

    /// The type of task this state creates. Port of `taskType()` (always valid,
    /// even when `create_task` returns `None`).
    pub fn task_type(&self) -> TaskType {
        match self {
            ConsumerState::BlockedOnParent => TaskType::BlockOnParentShards,
            ConsumerState::Initializing => TaskType::Initialize,
            ConsumerState::Processing => TaskType::Process,
            ConsumerState::ShutdownNotification => TaskType::ShutdownNotification,
            ConsumerState::ShutdownNotificationCompletion => TaskType::ShutdownNotification,
            ConsumerState::ShuttingDown => TaskType::Shutdown,
            ConsumerState::ShutdownComplete => TaskType::ShutdownComplete,
        }
    }

    /// The [`ShardConsumerState`] enum value for this state. Port of `state()`.
    pub fn state(&self) -> ShardConsumerState {
        match self {
            ConsumerState::BlockedOnParent => ShardConsumerState::WaitingOnParentShards,
            ConsumerState::Initializing => ShardConsumerState::Initializing,
            ConsumerState::Processing => ShardConsumerState::Processing,
            ConsumerState::ShutdownNotification => ShardConsumerState::ShutdownRequested,
            ConsumerState::ShutdownNotificationCompletion => ShardConsumerState::ShutdownRequested,
            ConsumerState::ShuttingDown => ShardConsumerState::ShuttingDown,
            ConsumerState::ShutdownComplete => ShardConsumerState::ShutdownComplete,
        }
    }

    /// Whether this is the terminal state. Port of `isTerminal()`.
    pub fn is_terminal(&self) -> bool {
        matches!(self, ConsumerState::ShutdownComplete)
    }

    /// Whether the state requires data to be available before the task can be
    /// created. Port of `requiresDataAvailability()` (default `false`, only
    /// `ProcessingState` returns `true`).
    pub fn requires_data_availability(&self) -> bool {
        matches!(self, ConsumerState::Processing)
    }

    /// Whether the state requires an external event to re-awaken processing.
    /// Port of `requiresAwake()` (default `false`, only
    /// `ShutdownNotificationCompletionState` returns `true`).
    pub fn requires_awake(&self) -> bool {
        matches!(self, ConsumerState::ShutdownNotificationCompletion)
    }
}

/// Default (empty) `ProcessRecordsInput` used when the `Processing` state builds
/// its task with no incoming data (a control-message step). Java passes the
/// (possibly `null`) input straight through; ProcessTask tolerates it.
fn process_input_default() -> ProcessRecordsInput {
    ProcessRecordsInput::builder().build()
}

#[cfg(test)]
mod tests {
    use super::*;

    // Port of ConsumerStatesTest transition-table assertions (the reflection-based
    // field-inspection assertions are not portable — see WAVE-PLAN TEST-PARITY GAPS).

    #[test]
    fn block_on_parent_state() {
        let state = ConsumerState::BlockedOnParent;
        assert_eq!(state.success_transition(), ConsumerState::Initializing);
        for reason in [
            ShutdownReason::LeaseLost,
            ShutdownReason::ShardEnd,
            ShutdownReason::Requested,
        ] {
            assert_eq!(
                state.shutdown_transition(reason),
                ConsumerState::ShuttingDown
            );
        }
        assert_eq!(state.state(), ShardConsumerState::WaitingOnParentShards);
        assert_eq!(state.task_type(), TaskType::BlockOnParentShards);
        assert!(!state.is_terminal());
    }

    #[test]
    fn initializing_state() {
        let state = ConsumerState::Initializing;
        assert_eq!(state.success_transition(), ConsumerState::Processing);
        assert_eq!(
            state.shutdown_transition(ShutdownReason::LeaseLost),
            ConsumerState::ShuttingDown
        );
        assert_eq!(
            state.shutdown_transition(ShutdownReason::ShardEnd),
            ConsumerState::ShuttingDown
        );
        assert_eq!(
            state.shutdown_transition(ShutdownReason::Requested),
            ConsumerState::ShutdownNotification
        );
        assert_eq!(state.state(), ShardConsumerState::Initializing);
        assert_eq!(state.task_type(), TaskType::Initialize);
    }

    #[test]
    fn processing_state() {
        let state = ConsumerState::Processing;
        assert_eq!(state.success_transition(), ConsumerState::Processing);
        assert_eq!(
            state.shutdown_transition(ShutdownReason::LeaseLost),
            ConsumerState::ShuttingDown
        );
        assert_eq!(
            state.shutdown_transition(ShutdownReason::ShardEnd),
            ConsumerState::ShuttingDown
        );
        assert_eq!(
            state.shutdown_transition(ShutdownReason::Requested),
            ConsumerState::ShutdownNotification
        );
        assert_eq!(state.state(), ShardConsumerState::Processing);
        assert_eq!(state.task_type(), TaskType::Process);
        assert!(state.requires_data_availability());
    }

    #[test]
    fn shutdown_request_state() {
        let state = ConsumerState::ShutdownNotification;
        assert_eq!(
            state.success_transition(),
            ConsumerState::shutdown_request_completion_state()
        );
        assert_eq!(
            state.shutdown_transition(ShutdownReason::Requested),
            ConsumerState::shutdown_request_completion_state()
        );
        assert_eq!(
            state.shutdown_transition(ShutdownReason::LeaseLost),
            ConsumerState::ShuttingDown
        );
        assert_eq!(
            state.shutdown_transition(ShutdownReason::ShardEnd),
            ConsumerState::ShuttingDown
        );
        assert_eq!(state.state(), ShardConsumerState::ShutdownRequested);
        assert_eq!(state.task_type(), TaskType::ShutdownNotification);
    }

    #[test]
    fn shutdown_request_complete_state() {
        let state = ConsumerState::shutdown_request_completion_state();
        assert_eq!(state.success_transition(), state);
        assert_eq!(state.shutdown_transition(ShutdownReason::Requested), state);
        assert_eq!(
            state.shutdown_transition(ShutdownReason::LeaseLost),
            ConsumerState::ShuttingDown
        );
        assert_eq!(
            state.shutdown_transition(ShutdownReason::ShardEnd),
            ConsumerState::ShuttingDown
        );
        assert_eq!(state.state(), ShardConsumerState::ShutdownRequested);
        assert_eq!(state.task_type(), TaskType::ShutdownNotification);
        assert!(state.requires_awake());
    }

    #[test]
    fn shutting_down_state() {
        let state = ConsumerState::ShuttingDown;
        assert_eq!(state.success_transition(), ConsumerState::ShutdownComplete);
        for reason in [
            ShutdownReason::LeaseLost,
            ShutdownReason::ShardEnd,
            ShutdownReason::Requested,
        ] {
            assert_eq!(
                state.shutdown_transition(reason),
                ConsumerState::ShutdownComplete
            );
        }
        assert_eq!(state.state(), ShardConsumerState::ShuttingDown);
        assert_eq!(state.task_type(), TaskType::Shutdown);
    }

    #[test]
    fn shutdown_complete_state() {
        let state = ConsumerState::ShutdownComplete;
        assert_eq!(state.success_transition(), state);
        for reason in [
            ShutdownReason::LeaseLost,
            ShutdownReason::ShardEnd,
            ShutdownReason::Requested,
        ] {
            assert_eq!(state.shutdown_transition(reason), state);
        }
        assert!(state.is_terminal());
        assert_eq!(state.state(), ShardConsumerState::ShutdownComplete);
        assert_eq!(state.task_type(), TaskType::ShutdownComplete);
    }
}
