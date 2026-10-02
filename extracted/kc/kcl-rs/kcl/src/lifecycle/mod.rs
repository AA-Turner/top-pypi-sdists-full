//! Port of `software.amazon.kinesis.lifecycle`.
//!
//! Sub-wave **7a**: the `ConsumerTask` framework + all concrete task
//! implementations. The [`TaskType`]/[`TaskOutcome`] enums and the `events`
//! value types are also here.
//!
//! # Concurrency model (see PORTING.md)
//!
//! * [`ConsumerTask`] is an **async trait** (`async fn call`). Tasks do async
//!   I/O (lease refresher, shard detector, shard-sync) with direct `.await`.
//! * The **sync `ShardRecordProcessor` callbacks** are invoked via
//!   [`tokio::task::spawn_blocking`], because the checkpointer they may call
//!   bridges to async via `Handle::block_on` (which must not run on a runtime
//!   worker nor be nested inside another `block_on`). The processor is stored as
//!   `Arc<std::sync::Mutex<Box<dyn ShardRecordProcessor + Send>>>` in
//!   [`ShardConsumerArgument`].
//! * `Thread.sleep` backoff → [`tokio::time::sleep`] (interrupt-swallow ⇒
//!   cooperative cancellation).
//!
//! # Sub-wave 7b (the state machine + driver)
//!
//! `ShardConsumer` (the tokio-actor driver), `ConsumerState`/`ConsumerStates`
//! (the closed-enum state machine), `ShardConsumerSubscriber` (the channel-based
//! subscriber loop), the full `LeaseGracefulShutdownHandler` background poller,
//! `ShardConsumerShutdownNotification`, and `LifecycleConfig`.

pub mod block_on_parent_shard_task;
pub mod consumer_state;
pub mod consumer_task;
pub mod events;
pub mod initialize_task;
pub mod lease_graceful_shutdown_handler;
pub mod lifecycle_config;
pub mod process_task;
pub mod shard_consumer;
pub mod shard_consumer_argument;
pub mod shard_consumer_shutdown_notification;
pub mod shard_consumer_subscriber;
pub mod shutdown_input;
pub mod shutdown_notification;
pub mod shutdown_notification_task;
pub mod shutdown_reason;
pub mod shutdown_task;
pub mod task_execution_listener;
pub mod task_outcome;
pub mod task_type;

#[cfg(test)]
pub mod test_support;

pub use block_on_parent_shard_task::BlockOnParentShardTask;
pub use consumer_state::{ConsumerState, ShardConsumerState};
pub use consumer_task::{
    ConsumerTask, ConsumerTaskFactory, KinesisConsumerTaskFactory, TaskResult,
};
pub use initialize_task::InitializeTask;
pub use lease_graceful_shutdown_handler::{
    attempt_lease_transfer, LeaseGracefulShutdownHandler, ShardConsumerMap,
    SHUTDOWN_CHECK_INTERVAL_MILLIS,
};
pub use lifecycle_config::{LifecycleConfig, DEFAULT_READ_TIMEOUTS_TO_IGNORE};
pub use process_task::ProcessTask;
pub use shard_consumer::{ShardConsumer, MAX_TIME_BETWEEN_REQUEST_RESPONSE};
pub use shard_consumer_argument::ShardConsumerArgument;
pub use shard_consumer_shutdown_notification::{CountDownLatch, ShardConsumerShutdownNotification};
pub use shard_consumer_subscriber::{InputHandler, ShardConsumerSubscriber};
pub use shutdown_input::ShutdownInput;
pub use shutdown_notification::ShutdownNotification;
pub use shutdown_notification_task::ShutdownNotificationTask;
pub use shutdown_reason::ShutdownReason;
pub use shutdown_task::ShutdownTask;
pub use task_execution_listener::{NoOpTaskExecutionListener, TaskExecutionListener};
pub use task_outcome::TaskOutcome;
pub use task_type::TaskType;
