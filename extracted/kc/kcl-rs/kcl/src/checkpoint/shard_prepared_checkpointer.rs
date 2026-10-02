//! Port of `software.amazon.kinesis.checkpoint.ShardPreparedCheckpointer`.

use std::sync::Arc;

use crate::exceptions::KinesisClientLibError;
use crate::processor::{PreparedCheckpointer, RecordProcessorCheckpointer};
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// A [`PreparedCheckpointer`] prepared to checkpoint at a specific sequence
/// number. It uses a [`RecordProcessorCheckpointer`] to do the actual
/// checkpointing, so its checkpoint is subject to the same "didn't go backwards"
/// validation as a normal checkpoint.
///
/// Because [`checkpoint`](ShardPreparedCheckpointer::checkpoint) re-invokes the
/// parent checkpointer's `checkpoint_sequence_sub`, it re-validates against the
/// *current* `lastCheckpointValue`/`largestPermittedCheckpointValue` at call
/// time (not at prepare time): a stale `ShardPreparedCheckpointer` can therefore
/// panic (Java `IllegalArgumentException`) if the checkpointer's state has moved
/// on. This is preserved by holding a shared reference (`Arc`) back to the owning
/// checkpointer, not a snapshot.
pub struct ShardPreparedCheckpointer {
    pending_checkpoint_sequence_number: ExtendedSequenceNumber,
    /// The owning checkpointer. Optional so that (like the Java tests) it can be
    /// constructed without one when only [`pending_checkpoint`] is exercised.
    ///
    /// [`pending_checkpoint`]: ShardPreparedCheckpointer::pending_checkpoint
    checkpointer: Option<Arc<dyn RecordProcessorCheckpointer + Send + Sync>>,
}

impl ShardPreparedCheckpointer {
    /// Constructor.
    ///
    /// * `pending_checkpoint_sequence_number` — sequence number to checkpoint at.
    /// * `checkpointer` — the checkpointer to use for the actual commit.
    pub fn new(
        pending_checkpoint_sequence_number: ExtendedSequenceNumber,
        checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync>,
    ) -> Self {
        Self {
            pending_checkpoint_sequence_number,
            checkpointer: Some(checkpointer),
        }
    }

    /// Construct without an owning checkpointer (Java `new
    /// ShardPreparedCheckpointer(sn, null)`), used only where
    /// [`checkpoint`](Self::checkpoint) is never called.
    pub fn without_checkpointer(
        pending_checkpoint_sequence_number: ExtendedSequenceNumber,
    ) -> Self {
        Self {
            pending_checkpoint_sequence_number,
            checkpointer: None,
        }
    }
}

impl PreparedCheckpointer for ShardPreparedCheckpointer {
    fn pending_checkpoint(&self) -> ExtendedSequenceNumber {
        self.pending_checkpoint_sequence_number.clone()
    }

    fn checkpoint(&self) -> Result<(), KinesisClientLibError> {
        // Mirrors Java: NPE if the checkpointer is null. In the real code path a
        // checkpointer is always supplied.
        let checkpointer = self
            .checkpointer
            .as_ref()
            .expect("ShardPreparedCheckpointer has no checkpointer");
        checkpointer.checkpoint_sequence_sub(
            self.pending_checkpoint_sequence_number.sequence_number(),
            self.pending_checkpoint_sequence_number
                .sub_sequence_number(),
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::checkpoint::DoesNothingPreparedCheckpointer;
    use crate::processor::MockRecordProcessorCheckpointer;

    /// Verifies the relationship between the constructor and `pendingCheckpoint`.
    #[test]
    fn get_sequence_number() {
        let sn = ExtendedSequenceNumber::from_sequence_number("sn");
        let checkpointer = ShardPreparedCheckpointer::without_checkpointer(sn.clone());
        assert_eq!(checkpointer.pending_checkpoint(), sn);
    }

    /// Makes sure the PreparedCheckpointer calls the RecordProcessorCheckpointer
    /// properly (Java `testCheckpoint`).
    #[test]
    fn checkpoint_delegates_to_record_processor_checkpointer() {
        let sn = ExtendedSequenceNumber::from_sequence_number("sn");
        let mut mock = MockRecordProcessorCheckpointer::new();
        mock.expect_checkpoint_sequence_sub()
            .withf(|seq, sub| seq == "sn" && *sub == 0)
            .times(1)
            .returning(|_, _| Ok(()));
        let checkpointer = ShardPreparedCheckpointer::new(sn, Arc::new(mock));
        checkpointer.checkpoint().unwrap();
    }

    /// The `DoesNothingPreparedCheckpointer` returns its sequence number and its
    /// `checkpoint()` is a no-op (Java `testDoesNothingPreparedCheckpoint`).
    #[test]
    fn does_nothing_prepared_checkpoint() {
        let sn = ExtendedSequenceNumber::from_sequence_number("sn");
        let checkpointer = DoesNothingPreparedCheckpointer::new(sn.clone());
        assert_eq!(checkpointer.pending_checkpoint(), sn);
        // Nothing happens here.
        checkpointer.checkpoint().unwrap();
    }
}
