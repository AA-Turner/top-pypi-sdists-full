//! Port of `software.amazon.kinesis.checkpoint.DoesNothingPreparedCheckpointer`.

use crate::exceptions::KinesisClientLibError;
use crate::processor::PreparedCheckpointer;
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// A special [`PreparedCheckpointer`] that does nothing, used when preparing a
/// checkpoint at the current checkpoint sequence number where another checkpoint
/// is never necessary.
///
/// This simplifies programming by preventing application developers from having
/// to reason about whether their application has processed records before calling
/// `prepare_checkpoint`.
///
/// It is safe to do nothing here: the only way to checkpoint at the current
/// checkpoint value is to have a record processor that gets initialized,
/// processes 0 records, then calls `prepare_checkpoint`. The value in the table
/// is the same, so there's no reason to overwrite it with another copy of itself.
#[derive(Debug, Clone)]
pub struct DoesNothingPreparedCheckpointer {
    sequence_number: ExtendedSequenceNumber,
}

impl DoesNothingPreparedCheckpointer {
    /// Constructor.
    pub fn new(sequence_number: ExtendedSequenceNumber) -> Self {
        Self { sequence_number }
    }
}

impl PreparedCheckpointer for DoesNothingPreparedCheckpointer {
    fn pending_checkpoint(&self) -> ExtendedSequenceNumber {
        self.sequence_number.clone()
    }

    fn checkpoint(&self) -> Result<(), KinesisClientLibError> {
        // This method does nothing.
        Ok(())
    }
}
