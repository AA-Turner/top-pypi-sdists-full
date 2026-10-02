//! Port of `software.amazon.kinesis.coordinator.CoordinatorFactory` (interface)
//! and `SchedulerCoordinatorFactory` (default impl).

use std::sync::Arc;

use crate::checkpoint::ShardRecordProcessorCheckpointer;
use crate::coordinator::graceful_shutdown_coordinator::GracefulShutdownCoordinator;
use crate::coordinator::worker_state_change_listener::{
    NoOpWorkerStateChangeListener, WorkerStateChangeListener,
};
use crate::leases::ShardInfo;
use crate::processor::Checkpointer;

/// The Scheduler's record-processor task executor. Java `ExecutorService`
/// (default: `SchedulerThreadPoolExecutor`, an unbounded, `SynchronousQueue`-
/// backed, 60s-keep-alive cached thread pool).
///
/// In the async Rust port, ShardConsumers spawn their own tokio tasks, so this
/// carries no thread pool — it is a marker recording whether the executor is
/// **Scheduler-owned** (the Scheduler may forcibly shut it down at
/// `finalShutdown`) or **user-supplied** (left running). This preserves the Java
/// `instanceof SchedulerThreadPoolExecutor` decision in `finalShutdown`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SchedulerExecutorService {
    /// The internal `SchedulerThreadPoolExecutor` (may be force-shut-down).
    SchedulerOwned,
    /// A user-supplied executor (left running by the Scheduler).
    UserSupplied,
}

impl SchedulerExecutorService {
    /// Whether this is the internal executor the Scheduler is allowed to shut
    /// down (Java `instanceof SchedulerThreadPoolExecutor`).
    pub fn is_scheduler_owned(&self) -> bool {
        matches!(self, SchedulerExecutorService::SchedulerOwned)
    }
}

/// Factory SPI for pluggable coordinator components. Java `CoordinatorFactory`.
pub trait CoordinatorFactory: Send + Sync {
    /// Java `createExecutorService()`. Returns the marker for the internal
    /// (Scheduler-owned) executor; a custom factory can return
    /// [`SchedulerExecutorService::UserSupplied`] to opt out of force-shutdown.
    fn create_executor_service(&self) -> SchedulerExecutorService {
        SchedulerExecutorService::SchedulerOwned
    }

    /// Java deprecated default `createGracefulShutdownCoordinator()`.
    fn create_graceful_shutdown_coordinator(&self) -> GracefulShutdownCoordinator {
        GracefulShutdownCoordinator::new()
    }

    /// Java `createRecordProcessorCheckpointer(ShardInfo, Checkpointer)`.
    fn create_record_processor_checkpointer(
        &self,
        shard_info: ShardInfo,
        checkpoint: Arc<dyn Checkpointer + Send + Sync>,
    ) -> Arc<ShardRecordProcessorCheckpointer>;

    /// Java deprecated default `createWorkerStateChangeListener()` — returns a
    /// [`NoOpWorkerStateChangeListener`].
    fn create_worker_state_change_listener(
        &self,
    ) -> Arc<dyn WorkerStateChangeListener + Send + Sync> {
        Arc::new(NoOpWorkerStateChangeListener::new())
    }
}

/// Default production [`CoordinatorFactory`]. Java `SchedulerCoordinatorFactory`.
#[derive(Debug, Default, Clone, Copy)]
pub struct SchedulerCoordinatorFactory;

impl SchedulerCoordinatorFactory {
    pub fn new() -> Self {
        Self
    }
}

impl CoordinatorFactory for SchedulerCoordinatorFactory {
    fn create_record_processor_checkpointer(
        &self,
        shard_info: ShardInfo,
        checkpoint: Arc<dyn Checkpointer + Send + Sync>,
    ) -> Arc<ShardRecordProcessorCheckpointer> {
        ShardRecordProcessorCheckpointer::new(shard_info, checkpoint)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::ShardInfo;
    use crate::processor::MockCheckpointer;

    #[test]
    fn scheduler_factory_creates_checkpointer() {
        let factory = SchedulerCoordinatorFactory::new();
        let shard_info = ShardInfo::new("shard-000", None, Vec::<String>::new(), None, None);
        let checkpointer: Arc<dyn Checkpointer + Send + Sync> = Arc::new(MockCheckpointer::new());
        // Constructing the per-shard checkpointer must succeed.
        let _cp = factory.create_record_processor_checkpointer(shard_info, checkpointer);
    }

    #[test]
    fn default_worker_state_change_listener_is_noop() {
        let factory = SchedulerCoordinatorFactory::new();
        let listener = factory.create_worker_state_change_listener();
        // A NoOp listener does nothing; exercising it must not panic.
        listener.on_worker_state_change(
            crate::coordinator::worker_state_change_listener::WorkerState::Started,
        );
    }
}
