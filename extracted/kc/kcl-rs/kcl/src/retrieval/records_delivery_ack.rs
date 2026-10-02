//! Port of `software.amazon.kinesis.retrieval.RecordsDeliveryAck`.

use crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier;

/// Acknowledgement sent back to a [`RecordsPublisher`](crate::retrieval::RecordsPublisher)
/// confirming a batch was delivered/processed downstream.
///
/// Core of the ack-based backpressure/ordering protocol between publishers and
/// their subscriber (the `ShardConsumer` in the lifecycle wave). Port of the Java
/// interface.
///
/// A concrete value type [`SimpleRecordsDeliveryAck`] is provided for callers
/// that just need to wrap a [`BatchUniqueIdentifier`]; the object-safe trait lets
/// publishers accept any ack shape.
pub trait RecordsDeliveryAck: Send + Sync + std::fmt::Debug {
    /// The unique identifier of the acknowledged record batch and its source.
    fn batch_unique_identifier(&self) -> &BatchUniqueIdentifier;
}

/// A trivial [`RecordsDeliveryAck`] wrapping a [`BatchUniqueIdentifier`].
///
/// The consumer builds one of these from the [`BatchUniqueIdentifier`] it read
/// off a delivered [`RecordsRetrieved`](crate::retrieval::RecordsRetrieved) and
/// sends it back via the publisher's ack path.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SimpleRecordsDeliveryAck {
    batch_unique_identifier: BatchUniqueIdentifier,
}

impl SimpleRecordsDeliveryAck {
    /// Wrap a [`BatchUniqueIdentifier`].
    pub fn new(batch_unique_identifier: BatchUniqueIdentifier) -> Self {
        Self {
            batch_unique_identifier,
        }
    }
}

impl RecordsDeliveryAck for SimpleRecordsDeliveryAck {
    fn batch_unique_identifier(&self) -> &BatchUniqueIdentifier {
        &self.batch_unique_identifier
    }
}
