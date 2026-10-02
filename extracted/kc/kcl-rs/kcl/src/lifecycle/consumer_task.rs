//! Ports of `software.amazon.kinesis.lifecycle.{ConsumerTask, TaskResult,
//! ConsumerTaskFactory, KinesisConsumerTaskFactory}`.
//!
//! # Design
//!
//! - `ConsumerTask` (Java `interface ConsumerTask extends Callable<TaskResult>`)
//!   → an async trait. Java's `call()` is synchronous/blocking but the concrete
//!   tasks perform async I/O (lease refresher, shard detector), so the Rust port
//!   makes `call` an `async fn`. The sync `ShardRecordProcessor` callbacks are
//!   invoked inside tasks via `tokio::task::spawn_blocking` (see the lifecycle
//!   module docs and `ShardConsumerArgument`).
//! - `TaskResult` (Java `class TaskResult`) → a struct carrying an optional
//!   error (Java `Exception exception`) plus the `shard_end_reached` flag.
//! - `ConsumerTaskFactory` (Java `interface ConsumerTaskFactory`) →
//!   [`ConsumerTaskFactory`] + [`KinesisConsumerTaskFactory`]. The Java
//!   `createShutdownTask`/`createShutdownNotificationTask` methods take a
//!   `ShardConsumer` (sub-wave 7b); here their needed values (`reason` /
//!   `shutdown_notification`) are passed directly.
//! - `getClass().getSimpleName()` task naming has no Rust equivalent (no
//!   reflection), so `ConsumerTask` exposes an explicit
//!   [`task_name`](ConsumerTask::task_name) returning the exact Java simple class
//!   name (e.g. `"ProcessTask"`), used by the metrics-collecting decorator.

use std::sync::Arc;

use async_trait::async_trait;
use aws_sdk_kinesis::types::ChildShard;

use crate::exceptions::BoxError;
use crate::lifecycle::events::ProcessRecordsInput;
use crate::lifecycle::{
    BlockOnParentShardTask, InitializeTask, ProcessTask, ShardConsumerArgument,
    ShutdownNotification, ShutdownNotificationTask, ShutdownReason, ShutdownTask, TaskType,
};
use crate::retrieval::ThrottlingReporter;

/// Result of running a [`ConsumerTask`]. Port of
/// `software.amazon.kinesis.lifecycle.TaskResult`.
///
/// Carries an optional error (Java `Exception exception`; failures are returned
/// as data, not propagated) and whether the shard end was reached.
#[derive(Debug, Default)]
pub struct TaskResult {
    shard_end_reached: bool,
    exception: Option<BoxError>,
}

impl TaskResult {
    /// Port of `TaskResult(Exception e)` — `shardEndReached` defaults to `false`.
    pub fn new(exception: Option<BoxError>) -> Self {
        Self {
            shard_end_reached: false,
            exception,
        }
    }

    /// Port of `TaskResult(boolean isShardEndReached)`.
    pub fn shard_end(shard_end_reached: bool) -> Self {
        Self {
            shard_end_reached,
            exception: None,
        }
    }

    /// Port of `TaskResult(Exception e, boolean isShardEndReached)`.
    pub fn with_exception_and_shard_end(
        exception: Option<BoxError>,
        shard_end_reached: bool,
    ) -> Self {
        Self {
            shard_end_reached,
            exception,
        }
    }

    /// Java `isShardEndReached()`.
    pub fn is_shard_end_reached(&self) -> bool {
        self.shard_end_reached
    }

    /// Java `getException()`.
    pub fn exception(&self) -> Option<&BoxError> {
        self.exception.as_ref()
    }

    /// Take ownership of the error, if any.
    pub fn take_exception(self) -> Option<BoxError> {
        self.exception
    }
}

/// A unit of work executed by the KCL task-execution framework. Port of
/// `software.amazon.kinesis.lifecycle.ConsumerTask` (Java
/// `interface ConsumerTask extends Callable<TaskResult>`).
///
/// `call` is `async` in the Rust port because concrete tasks (shard sync) do
/// async I/O; Java's `call()` is blocking but wraps the same work.
#[async_trait]
pub trait ConsumerTask: Send + Sync {
    /// Execute the task, returning its [`TaskResult`]. Java `TaskResult call()`.
    async fn call(&self) -> TaskResult;

    /// The type of this task. Java `TaskType taskType()`.
    fn task_type(&self) -> TaskType;

    /// The task's name for metrics dimensions.
    ///
    /// Java uses `other.getClass().getSimpleName()` via reflection; Rust has no
    /// equivalent, so each task returns its exact Java simple class name (e.g.
    /// `"ShardSyncTask"`).
    fn task_name(&self) -> &'static str;
}

/// Factory that constructs [`ConsumerTask`]s. Port of
/// `software.amazon.kinesis.lifecycle.ConsumerTaskFactory`.
///
/// # Deviation from Java
///
/// The Java `createShutdownTask`/`createShutdownNotificationTask` take a
/// `ShardConsumer` (to read `consumer.shutdownReason()` /
/// `consumer.shutdownNotification()`). `ShardConsumer` belongs to sub-wave 7b;
/// here those values are passed **directly** as parameters (`reason` /
/// `shutdown_notification`) so the factory is usable now. The state machine
/// (7b) will supply them from the `ShardConsumer`.
pub trait ConsumerTaskFactory: Send + Sync {
    /// Create a shutdown task. `reason` + `child_shards` come from the
    /// `ShardConsumer`/`ProcessRecordsInput` in Java.
    fn create_shutdown_task(
        &self,
        argument: &ShardConsumerArgument,
        reason: ShutdownReason,
        child_shards: Option<Vec<ChildShard>>,
    ) -> Box<dyn ConsumerTask>;

    /// Create a process task.
    fn create_process_task(
        &self,
        argument: &ShardConsumerArgument,
        process_records_input: ProcessRecordsInput,
    ) -> Box<dyn ConsumerTask>;

    /// Create an initialize task.
    fn create_initialize_task(&self, argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask>;

    /// Create a block-on-parent task.
    fn create_block_on_parent_task(
        &self,
        argument: &ShardConsumerArgument,
    ) -> Box<dyn ConsumerTask>;

    /// Create a shutdown-notification task. `shutdown_notification` comes from
    /// the `ShardConsumer` in Java.
    fn create_shutdown_notification_task(
        &self,
        argument: &ShardConsumerArgument,
        shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
    ) -> Box<dyn ConsumerTask>;
}

/// Default `ConsumerTaskFactory` for Kinesis. Port of
/// `software.amazon.kinesis.lifecycle.KinesisConsumerTaskFactory` (stateless).
#[derive(Debug, Default, Clone)]
pub struct KinesisConsumerTaskFactory;

impl ConsumerTaskFactory for KinesisConsumerTaskFactory {
    fn create_shutdown_task(
        &self,
        argument: &ShardConsumerArgument,
        reason: ShutdownReason,
        child_shards: Option<Vec<ChildShard>>,
    ) -> Box<dyn ConsumerTask> {
        Box::new(ShutdownTask::new(
            argument.shard_info().clone(),
            argument.shard_detector().clone(),
            argument.shard_record_processor().clone(),
            argument.record_processor_checkpointer().clone(),
            reason,
            *argument.initial_position_in_stream(),
            argument.cleanup_leases_of_completed_shards(),
            argument.ignore_unexpected_child_shards(),
            argument.lease_coordinator().clone(),
            argument.task_backoff_time_millis(),
            argument.records_publisher().clone(),
            argument.hierarchical_shard_syncer().clone(),
            argument.metrics_factory().clone(),
            child_shards,
            argument.stream_identifier().clone(),
            argument.lease_cleanup_manager().clone(),
        ))
    }

    fn create_process_task(
        &self,
        argument: &ShardConsumerArgument,
        process_records_input: ProcessRecordsInput,
    ) -> Box<dyn ConsumerTask> {
        // Java constructs a fresh ThrottlingReporter(5, shardId) per task.
        let throttling_reporter = ThrottlingReporter::new(5, argument.shard_info().shard_id());
        Box::new(ProcessTask::new(
            argument.shard_info().clone(),
            argument.shard_record_processor().clone(),
            argument.record_processor_checkpointer().clone(),
            argument.task_backoff_time_millis(),
            argument.skip_shard_sync_at_worker_initialization_if_leases_exist(),
            argument.shard_detector().clone(),
            throttling_reporter,
            process_records_input,
            argument.should_call_process_records_even_for_empty_record_list(),
            argument.idle_time_in_milliseconds(),
            argument.aggregator_util().clone(),
            argument.metrics_factory().clone(),
            argument.lease_coordinator().lease_stats_recorder(),
        ))
    }

    fn create_initialize_task(&self, argument: &ShardConsumerArgument) -> Box<dyn ConsumerTask> {
        Box::new(InitializeTask::new(
            argument.shard_info().clone(),
            argument.shard_record_processor().clone(),
            argument.checkpoint().clone(),
            argument.record_processor_checkpointer().clone(),
            *argument.initial_position_in_stream(),
            argument.records_publisher().clone(),
            argument.task_backoff_time_millis(),
            argument.metrics_factory().clone(),
        ))
    }

    fn create_block_on_parent_task(
        &self,
        argument: &ShardConsumerArgument,
    ) -> Box<dyn ConsumerTask> {
        Box::new(BlockOnParentShardTask::new(
            argument.shard_info().clone(),
            argument.lease_coordinator().lease_refresher(),
            argument.parent_shard_poll_interval_millis(),
        ))
    }

    fn create_shutdown_notification_task(
        &self,
        argument: &ShardConsumerArgument,
        shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
    ) -> Box<dyn ConsumerTask> {
        Box::new(ShutdownNotificationTask::new(
            argument.shard_record_processor().clone(),
            argument.record_processor_checkpointer().clone(),
            shutdown_notification,
            argument.shard_info().clone(),
            argument.lease_coordinator().clone(),
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn task_result_carries_exception_and_flags() {
        let ok = TaskResult::shard_end(true);
        assert!(ok.is_shard_end_reached());
        assert!(ok.exception().is_none());

        let err = TaskResult::new(Some(Box::<dyn std::error::Error + Send + Sync>::from(
            "boom",
        )));
        assert!(!err.is_shard_end_reached());
        assert!(err.exception().is_some());
        assert_eq!(err.take_exception().unwrap().to_string(), "boom");
    }
}
