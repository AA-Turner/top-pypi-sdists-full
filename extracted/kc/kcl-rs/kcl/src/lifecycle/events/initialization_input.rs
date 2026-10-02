//! Port of `software.amazon.kinesis.lifecycle.events.InitializationInput`.

use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Parameters to `ShardRecordProcessor::initialize`.
///
/// Port of the Lombok `@Builder @Getter @Accessors(fluent=true)
/// @EqualsAndHashCode @ToString` class. No checkpointer field, so structural
/// equality/hashing can be derived directly.
#[derive(Debug, Clone, PartialEq, Eq, Hash, bon::Builder)]
pub struct InitializationInput {
    /// The shard id that the record processor is being initialized for.
    #[builder(into)]
    shard_id: Option<String>,
    /// The last extended sequence number successfully checkpointed by the
    /// previous record processor.
    extended_sequence_number: Option<ExtendedSequenceNumber>,
    /// The pending extended sequence number that may have been started by the
    /// previous record processor (only set if it prepared a checkpoint but lost
    /// its lease before completing it).
    pending_checkpoint_sequence_number: Option<ExtendedSequenceNumber>,
    /// The last pending application state of the previous record processor.
    /// Only set if it prepared a checkpoint but lost its lease before completing.
    pending_checkpoint_state: Option<Vec<u8>>,
}

impl InitializationInput {
    /// The shard id being initialized.
    pub fn shard_id(&self) -> Option<&str> {
        self.shard_id.as_deref()
    }

    /// The last checkpointed extended sequence number.
    pub fn extended_sequence_number(&self) -> Option<&ExtendedSequenceNumber> {
        self.extended_sequence_number.as_ref()
    }

    /// The pending checkpoint extended sequence number, if any.
    pub fn pending_checkpoint_sequence_number(&self) -> Option<&ExtendedSequenceNumber> {
        self.pending_checkpoint_sequence_number.as_ref()
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
    fn builder_and_getters() {
        let input = InitializationInput::builder()
            .shard_id("shard-0001")
            .extended_sequence_number(ExtendedSequenceNumber::from_sequence_number("42"))
            .build();
        assert_eq!(input.shard_id(), Some("shard-0001"));
        assert_eq!(
            input.extended_sequence_number(),
            Some(&ExtendedSequenceNumber::from_sequence_number("42"))
        );
        assert_eq!(input.pending_checkpoint_sequence_number(), None);
        assert_eq!(input.pending_checkpoint_state(), None);
    }

    #[test]
    fn equality_is_field_based() {
        let a = InitializationInput::builder().shard_id("s").build();
        let b = InitializationInput::builder().shard_id("s").build();
        assert_eq!(a, b);
    }
}
