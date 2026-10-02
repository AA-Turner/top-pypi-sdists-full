//! Port of `software.amazon.kinesis.retrieval.RecordsRetrieved`.

use crate::lifecycle::events::process_records_input::ProcessRecordsInput;
use crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier;

/// A single delivered unit of retrieved records, plus optional identity for ack
/// correlation.
///
/// Port of the Java interface. Implemented by the fan-out and polling publishers'
/// nested `*RecordsRetrieved` types (both of which override
/// [`batch_unique_identifier`](Self::batch_unique_identifier)); a simple test
/// impl lives in [`crate::retrieval::records_publisher`]'s test module.
///
/// The trait is object-safe so publishers can deliver `Box<dyn RecordsRetrieved>`
/// (or `Arc`) over the delivery channel.
pub trait RecordsRetrieved: Send + Sync + std::fmt::Debug {
    /// The batch of retrieved records to hand to the processor.
    fn process_records_input(&self) -> &ProcessRecordsInput;

    /// The identifier that uniquely identifies this batch (for ack correlation).
    ///
    /// Port of the Java default method, which throws
    /// `UnsupportedOperationException` unless overridden. Here the default
    /// `panic!`s with the same message (matching the convention: unchecked Java
    /// exception → panic with the same message). Real publisher impls override
    /// this.
    fn batch_unique_identifier(&self) -> BatchUniqueIdentifier {
        panic!("Retrieval of batch unique identifier is not supported")
    }

    /// Downcast hook for the publishers' `restart_from`.
    ///
    /// Java's `PrefetchRecordsPublisher.restartFrom` / `FanOutRecordsPublisher.restartFrom`
    /// cast the `RecordsRetrieved` to their own nested concrete type (throwing
    /// `IllegalArgumentException` if it is a foreign impl). Rust has no
    /// trait-object downcasting, so the concrete publisher record types override
    /// this to return `Some(self as &dyn Any)`; the default returns `None`
    /// (a foreign impl → the publisher raises the Java `IllegalArgumentException`).
    fn as_any(&self) -> Option<&dyn std::any::Any> {
        None
    }
}
