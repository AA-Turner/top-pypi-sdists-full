//! Port of `software.amazon.kinesis.processor.PreparedCheckpointer`.

use crate::exceptions::KinesisClientLibError;
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Represents a two-phase "pending" checkpoint that has already been durably
/// recorded; calling [`checkpoint`](PreparedCheckpointer::checkpoint) commits it
/// to the actual checkpoint. Enables idempotent side effects across failover.
///
/// Ported as a **synchronous**, object-safe trait (used as
/// `Box<dyn PreparedCheckpointer + Send + Sync>`). The `checkpoint()` call is
/// subject to the same monotonicity ("didn't go backwards") validation as a
/// normal checkpoint, and shares its error set. Java's `IllegalArgumentException`
/// (out-of-range sequence number) maps to a `panic!`; the checked exceptions map
/// to [`KinesisClientLibError`].
///
/// `#[automock]` provides a mock for tests (the Java tests mock this interface).
#[cfg_attr(test, mockall::automock)]
pub trait PreparedCheckpointer {
    /// The sequence number of the pending checkpoint.
    fn pending_checkpoint(&self) -> ExtendedSequenceNumber;

    /// Commit the pending checkpoint.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if the sequence number being
    /// checkpointed is out of range.
    fn checkpoint(&self) -> Result<(), KinesisClientLibError>;
}
