//! Port of `software.amazon.kinesis.checkpoint.Checkpoint`.

use crate::retrieval::kpl::ExtendedSequenceNumber;

/// A class encapsulating the pieces of state stored in a checkpoint.
///
/// Port of the Lombok `@Data @Accessors(fluent = true)` class: field-based
/// equality/hashing and fluent (no-prefix) getters.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Checkpoint {
    checkpoint: ExtendedSequenceNumber,
    pending_checkpoint: Option<ExtendedSequenceNumber>,
    pending_checkpoint_state: Option<Vec<u8>>,
}

impl Checkpoint {
    /// Constructor.
    ///
    /// * `checkpoint` — the checkpoint sequence number; cannot be empty.
    /// * `pending_checkpoint` — the pending checkpoint sequence number; may be `None`.
    /// * `pending_checkpoint_state` — the pending checkpoint state; may be `None`.
    ///
    /// # Panics
    /// Panics (mirroring Java's `IllegalArgumentException`) if `checkpoint`'s
    /// sequence number is empty.
    pub fn new(
        checkpoint: ExtendedSequenceNumber,
        pending_checkpoint: Option<ExtendedSequenceNumber>,
        pending_checkpoint_state: Option<Vec<u8>>,
    ) -> Self {
        if checkpoint.sequence_number().is_empty() {
            panic!("Checkpoint cannot be null or empty");
        }
        Self {
            checkpoint,
            pending_checkpoint,
            pending_checkpoint_state,
        }
    }

    /// Two-argument constructor (deprecated in Java): no pending state.
    pub fn without_state(
        checkpoint: ExtendedSequenceNumber,
        pending_checkpoint: Option<ExtendedSequenceNumber>,
    ) -> Self {
        Self::new(checkpoint, pending_checkpoint, None)
    }

    /// The committed checkpoint sequence number.
    pub fn checkpoint(&self) -> &ExtendedSequenceNumber {
        &self.checkpoint
    }

    /// The pending (prepared) checkpoint sequence number, if any.
    pub fn pending_checkpoint(&self) -> Option<&ExtendedSequenceNumber> {
        self.pending_checkpoint.as_ref()
    }

    /// The pending checkpoint application state, if any.
    pub fn pending_checkpoint_state(&self) -> Option<&[u8]> {
        self.pending_checkpoint_state.as_deref()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn stores_and_returns_fields() {
        let cp = ExtendedSequenceNumber::from_sequence_number("123");
        let checkpoint = Checkpoint::new(cp.clone(), None, None);
        assert_eq!(checkpoint.checkpoint(), &cp);
        assert_eq!(checkpoint.pending_checkpoint(), None);
        assert_eq!(checkpoint.pending_checkpoint_state(), None);
    }

    #[test]
    #[should_panic(expected = "Checkpoint cannot be null or empty")]
    fn empty_checkpoint_panics() {
        Checkpoint::new(ExtendedSequenceNumber::from_sequence_number(""), None, None);
    }

    #[test]
    fn equality_is_field_based() {
        let a = Checkpoint::new(
            ExtendedSequenceNumber::from_sequence_number("1"),
            Some(ExtendedSequenceNumber::from_sequence_number("2")),
            Some(vec![1, 2, 3]),
        );
        let b = Checkpoint::new(
            ExtendedSequenceNumber::from_sequence_number("1"),
            Some(ExtendedSequenceNumber::from_sequence_number("2")),
            Some(vec![1, 2, 3]),
        );
        assert_eq!(a, b);
    }
}
