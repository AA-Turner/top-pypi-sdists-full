//! Port of `software.amazon.kinesis.checkpoint.CheckpointConfig`.

use crate::checkpoint::dynamodb::DynamoDBCheckpointFactory;
use crate::checkpoint::CheckpointFactory;

/// Used by the KCL to manage checkpointing.
///
/// Port of the Lombok `@Data @Accessors(fluent = true)` config bean: a single
/// mutable `checkpoint_factory` field defaulting to a
/// [`DynamoDBCheckpointFactory`], with a fluent getter/setter.
pub struct CheckpointConfig {
    checkpoint_factory: Box<dyn CheckpointFactory>,
}

impl Default for CheckpointConfig {
    fn default() -> Self {
        Self {
            checkpoint_factory: Box::new(DynamoDBCheckpointFactory::new()),
        }
    }
}

impl CheckpointConfig {
    /// A config with the default (DynamoDB-backed) checkpoint factory.
    pub fn new() -> Self {
        Self::default()
    }

    /// The configured [`CheckpointFactory`] (Java fluent getter
    /// `checkpointFactory()`).
    pub fn checkpoint_factory(&self) -> &dyn CheckpointFactory {
        self.checkpoint_factory.as_ref()
    }

    /// Set the [`CheckpointFactory`] (Java fluent setter
    /// `checkpointFactory(CheckpointFactory)`), returning `self` for chaining.
    pub fn set_checkpoint_factory(
        mut self,
        checkpoint_factory: Box<dyn CheckpointFactory>,
    ) -> Self {
        self.checkpoint_factory = checkpoint_factory;
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::{LeaseCoordinator, LeaseRefresher};
    use crate::processor::Checkpointer;
    use std::sync::Arc;

    #[test]
    fn default_uses_dynamodb_factory() {
        // The default config's factory should be usable (no panic constructing
        // the config itself; the DynamoDB factory only needs a runtime when it
        // creates a checkpointer).
        let _config = CheckpointConfig::new();
    }

    #[test]
    fn set_checkpoint_factory_overrides() {
        struct StubFactory;
        impl CheckpointFactory for StubFactory {
            fn create_checkpointer(
                &self,
                _lc: Arc<dyn LeaseCoordinator + Send + Sync>,
                _lr: Arc<dyn LeaseRefresher>,
            ) -> Box<dyn Checkpointer + Send + Sync> {
                unimplemented!()
            }
        }
        let config = CheckpointConfig::new().set_checkpoint_factory(Box::new(StubFactory));
        // Just verifying the setter compiles/chains and stores something.
        let _ = config.checkpoint_factory();
    }
}
