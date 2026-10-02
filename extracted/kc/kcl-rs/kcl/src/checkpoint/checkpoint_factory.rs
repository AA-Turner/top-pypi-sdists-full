//! Port of `software.amazon.kinesis.checkpoint.CheckpointFactory`.

use std::sync::Arc;

use crate::leases::{LeaseCoordinator, LeaseRefresher};
use crate::processor::Checkpointer;

/// Factory abstraction for constructing a [`Checkpointer`] given the lease
/// coordination collaborators.
///
/// The default implementation is
/// [`DynamoDBCheckpointFactory`](crate::checkpoint::dynamodb::DynamoDBCheckpointFactory),
/// which is wired into [`CheckpointConfig`](crate::checkpoint::CheckpointConfig)
/// by default.
pub trait CheckpointFactory: Send + Sync {
    /// Create a [`Checkpointer`] backed by the given lease coordinator and lease
    /// refresher.
    fn create_checkpointer(
        &self,
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
        lease_refresher: Arc<dyn LeaseRefresher>,
    ) -> Box<dyn Checkpointer + Send + Sync>;
}
