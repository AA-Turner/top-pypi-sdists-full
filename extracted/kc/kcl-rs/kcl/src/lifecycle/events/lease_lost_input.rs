//! Port of `software.amazon.kinesis.lifecycle.events.LeaseLostInput`.

/// Data about the loss of a lease, passed to `ShardRecordProcessor::lease_lost`.
///
/// Port of the Lombok `@Builder @Getter @Accessors(fluent=true)
/// @EqualsAndHashCode @ToString` class. This currently has no members but exists
/// for forward compatibility, mirroring Java.
#[derive(Debug, Clone, Default, PartialEq, Eq, Hash, bon::Builder)]
pub struct LeaseLostInput {}

impl LeaseLostInput {
    /// Construct an empty [`LeaseLostInput`].
    pub fn new() -> Self {
        Self {}
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_inputs_are_equal() {
        assert_eq!(LeaseLostInput::new(), LeaseLostInput::builder().build());
    }
}
