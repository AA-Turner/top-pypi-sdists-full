//! Port of `software.amazon.kinesis.leases`.
//!
//! Lease value types, shard prioritization, lease statistics, and the leasing
//! exception family (under [`exceptions`]).
//!
//! # Lease / MultiStreamLease model
//!
//! Java has `MultiStreamLease extends Lease`. Rust has no inheritance, so both
//! are unified into a single [`Lease`] struct that carries the base fields plus
//! optional multi-stream fields (`stream_identifier`, `shard_id`);
//! `Lease::is_multi_stream()` replaces `instanceof MultiStreamLease`. See the
//! [`lease`] module docs for the full rationale.

pub mod dynamo_utils;
pub mod dynamodb;
pub mod entity_dao;
pub mod entity_type;
pub mod exceptions;
pub mod hierarchical_shard_syncer;
pub mod kinesis_shard_detector;
pub mod lease;
pub mod lease_assignment_strategy;
pub mod lease_cleanup_manager;
pub mod lease_coordinator;
pub mod lease_discoverer;
pub mod lease_management_config;
pub mod lease_management_factory;
pub mod lease_refresher;
pub mod lease_renewer;
pub mod lease_serializer;
pub mod lease_stats_recorder;
pub mod lease_taker;
pub mod port_stubs;
pub mod shard_detector;
pub mod shard_info;
pub mod shard_prioritization;
pub mod shard_sync_task;
pub mod shard_sync_task_manager;
pub mod update_field;

pub use entity_dao::{Entity, EntityDAO, EntityScanList};
pub use entity_type::{CoordinatorStateType, EntityType};
pub use hierarchical_shard_syncer::HierarchicalShardSyncer;
pub use kinesis_shard_detector::KinesisShardDetector;
pub use lease::Lease;
pub use lease_assignment_strategy::LeaseAssignmentStrategy;
pub use lease_cleanup_manager::{LeaseCleanupManager, LeaseCleanupResult};
pub use lease_coordinator::LeaseCoordinator;
pub use lease_discoverer::LeaseDiscoverer;
pub use lease_management_config::LeaseManagementConfig;
pub use lease_management_factory::LeaseManagementFactory;
pub use lease_refresher::LeaseRefresher;
pub use lease_renewer::LeaseRenewer;
pub use lease_serializer::LeaseSerializer;
pub use lease_stats_recorder::{LeaseStats, LeaseStatsRecorder, TimeProvider, BYTES_PER_KB};
pub use lease_taker::LeaseTaker;
pub use shard_detector::ShardDetector;
pub use shard_info::ShardInfo;
pub use shard_prioritization::{
    NoOpShardPrioritization, ParentsFirstShardPrioritization, ShardPrioritization,
};
pub use shard_sync_task::ShardSyncTask;
pub use shard_sync_task_manager::ShardSyncTaskManager;
pub use update_field::UpdateField;

// Re-export the mockall-generated mocks for cross-module tests.
#[cfg(test)]
pub use lease_coordinator::MockLeaseCoordinator;
#[cfg(test)]
pub use lease_refresher::MockLeaseRefresher;
