//! Port of `software.amazon.kinesis.checkpoint.dynamodb` — the DynamoDB-backed
//! checkpoint storage.
//!
//! [`DynamoDBCheckpointer`] implements the synchronous
//! [`Checkpointer`](crate::processor::Checkpointer) SPI over the **async**
//! [`LeaseCoordinator`](crate::leases::LeaseCoordinator) /
//! [`LeaseRefresher`](crate::leases::LeaseRefresher) via a
//! [`tokio::runtime::Handle`] bridge (see the invariant on
//! [`DynamoDBCheckpointer`]). [`DynamoDBCheckpointFactory`] is the default
//! [`CheckpointFactory`](crate::checkpoint::CheckpointFactory).

pub mod dynamodb_checkpoint_factory;
pub mod dynamodb_checkpointer;

pub use dynamodb_checkpoint_factory::DynamoDBCheckpointFactory;
pub use dynamodb_checkpointer::DynamoDBCheckpointer;
