//! Port of `software.amazon.kinesis.coordinator`.
//!
//! This is the **10a foundational layer** of the coordinator subsystem:
//! coordinator-state persistence + routing, streamInfo tracking, config, and
//! the core value types / interfaces. The Scheduler (10d), migration state
//! machines (10b), and assignment/leader components (10c) land in later waves;
//! their cross-cutting dependencies are named via [`port_stubs`].
//!
//! # `DynamoDbAsyncToSyncClientAdapter` (skipped)
//!
//! Java's `DynamoDbAsyncToSyncClientAdapter` wraps the async DDB client as a
//! **sync** `DynamoDbClient` purely so the third-party `AmazonDynamoDBLockClient`
//! (which requires a sync client) can be used for leader-election locking. In
//! this all-async Rust port there is no sync-client requirement, and the DDB
//! lock client itself is a wave-10c concern (needs a Rust reimplementation of
//! the lock-item-with-heartbeat protocol). The adapter is therefore **not
//! ported**. // TODO(port): wave 10c DDB lock client + its (unlikely-needed) adapter.

pub mod assignment;
pub mod coordinator_config;
pub mod coordinator_factory;
pub mod coordinator_state;
pub mod coordinator_state_dao;
pub mod delegate;
pub mod deleted_stream_list_provider;
pub mod deterministic_shuffle_shard_sync_leader_decider;
pub mod diagnostic_event;
pub mod dynamic_migration_components_initializer;
pub mod graceful_shutdown_context;
pub mod graceful_shutdown_coordinator;
pub mod leader_decider;
pub mod migration;
pub mod migration_adaptive_lease_assignment_mode_provider;
pub mod periodic_shard_sync_manager;
pub mod port_stubs;
pub mod scheduler;
pub mod stream_info;
pub mod stream_info_manager;
pub mod worker_state_change_listener;

pub use coordinator_config::{ClientVersionConfig, CoordinatorConfig, CoordinatorStateTableConfig};
pub use coordinator_factory::{
    CoordinatorFactory, SchedulerCoordinatorFactory, SchedulerExecutorService,
};
pub use coordinator_state::{
    CoordinatorState, GenericCoordinatorState, ENTITY_TYPE_ATTRIBUTE_NAME,
};
pub use coordinator_state_dao::{CoordinatorStateAccess, CoordinatorStateDao};
pub use deleted_stream_list_provider::DeletedStreamListProvider;
pub use deterministic_shuffle_shard_sync_leader_decider::DeterministicShuffleShardSyncLeaderDecider;
pub use diagnostic_event::{
    DiagnosticEvent, DiagnosticEventFactory, DiagnosticEventHandler, DiagnosticEventLogger,
    ExecutorStateEvent, RejectedTaskEvent,
};
pub use dynamic_migration_components_initializer::DefaultDynamicMigrationComponentsInitializer;
pub use graceful_shutdown_context::GracefulShutdownContext;
pub use graceful_shutdown_coordinator::{
    GracefulShutdownCoordinator, GracefulShutdownError, SchedulerHandle, StartWorkerShutdown,
};
pub use leader_decider::{
    LeaderDecider, METRIC_OPERATION_LEADER_DECIDER, METRIC_OPERATION_LEADER_DECIDER_IS_LEADER,
};
pub use migration_adaptive_lease_assignment_mode_provider::{
    LeaseAssignmentMode, MigrationAdaptiveLeaseAssignmentModeProvider, ModeProviderError,
};
pub use periodic_shard_sync_manager::PeriodicShardSyncManager;
pub use scheduler::{Scheduler, SchedulerComponents, SchedulerError};
pub use stream_info::{
    StreamIdCache, StreamIdCacheManager, StreamIdCacheResolverBridge, StreamIdOnboardingState,
    StreamIdResolver, StreamInfo, StreamInfoDAO, StreamInfoMode, StreamInfoStore,
};
pub use stream_info_manager::StreamInfoManager;
pub use worker_state_change_listener::{
    NoOpWorkerStateChangeListener, WorkerState, WorkerStateChangeListener,
};

#[cfg(test)]
pub use coordinator_state_dao::MockCoordinatorStateAccess;
