//! Port of `software.amazon.kinesis.checkpoint.dynamodb.DynamoDBCheckpointFactory`.

use std::sync::Arc;

use tokio::runtime::Handle;

use crate::checkpoint::dynamodb::DynamoDBCheckpointer;
use crate::checkpoint::CheckpointFactory;
use crate::leases::{LeaseCoordinator, LeaseRefresher};
use crate::processor::Checkpointer;

/// Default [`CheckpointFactory`] that produces [`DynamoDBCheckpointer`]
/// instances. This is the default wired into
/// [`CheckpointConfig`](crate::checkpoint::CheckpointConfig).
///
/// Stateless (Java `@Data` on a field-less class — effectively a marker /
/// singleton).
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub struct DynamoDBCheckpointFactory;

impl DynamoDBCheckpointFactory {
    pub fn new() -> Self {
        Self
    }
}

impl CheckpointFactory for DynamoDBCheckpointFactory {
    /// Create a [`DynamoDBCheckpointer`].
    ///
    /// The tokio runtime [`Handle`] used by the checkpointer's sync→async bridge
    /// is captured from the current runtime context ([`Handle::current`]). The
    /// KCL scheduler always creates the checkpointer from within its runtime, so
    /// a runtime is in scope.
    ///
    /// # Panics
    /// Panics if called outside a tokio runtime (no current [`Handle`]).
    fn create_checkpointer(
        &self,
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
        lease_refresher: Arc<dyn LeaseRefresher>,
    ) -> Box<dyn Checkpointer + Send + Sync> {
        Box::new(DynamoDBCheckpointer::new(
            lease_coordinator,
            lease_refresher,
            Handle::current(),
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::{MockLeaseCoordinator, MockLeaseRefresher};

    #[tokio::test]
    async fn factory_creates_checkpointer() {
        let factory = DynamoDBCheckpointFactory::new();
        let checkpointer = factory.create_checkpointer(
            Arc::new(MockLeaseCoordinator::new()),
            Arc::new(MockLeaseRefresher::new()),
        );
        // Operation defaults to empty on a fresh checkpointer.
        assert_eq!(checkpointer.operation(), "");
    }
}
