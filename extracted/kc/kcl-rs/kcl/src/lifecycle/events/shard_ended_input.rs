//! Port of `software.amazon.kinesis.lifecycle.events.ShardEndedInput`.

use std::sync::Arc;

use crate::processor::RecordProcessorCheckpointer;

/// Provides a checkpointer that **must** be used to signal completion of the
/// shard to the Scheduler, passed to `ShardRecordProcessor::shard_ended`.
///
/// Port of the Lombok `@Builder @Getter @Accessors(fluent=true)
/// @EqualsAndHashCode @ToString` class. Because the checkpointer is a trait
/// object it cannot participate in derived `PartialEq`/`Eq`/`Hash`; those are
/// hand-implemented over the (currently empty) data fields, excluding the
/// checkpointer. See PORTING.md.
#[derive(Clone, bon::Builder)]
pub struct ShardEndedInput {
    /// The checkpointer used to record that the record processor has completed
    /// the shard.
    checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync>,
}

impl ShardEndedInput {
    /// The checkpointer for completing processing of the shard.
    pub fn checkpointer(&self) -> &Arc<dyn RecordProcessorCheckpointer + Send + Sync> {
        &self.checkpointer
    }
}

impl std::fmt::Debug for ShardEndedInput {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ShardEndedInput").finish_non_exhaustive()
    }
}

// Equality/hashing exclude the (trait-object) checkpointer — there are no other
// fields, so all instances compare equal, matching Lombok's `@EqualsAndHashCode`
// over the same (empty) data-field set.
impl PartialEq for ShardEndedInput {
    fn eq(&self, _other: &Self) -> bool {
        true
    }
}

impl Eq for ShardEndedInput {}

impl std::hash::Hash for ShardEndedInput {
    fn hash<H: std::hash::Hasher>(&self, _state: &mut H) {}
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::processor::MockRecordProcessorCheckpointer;

    #[test]
    fn holds_checkpointer_and_ignores_it_for_eq() {
        let cp: Arc<dyn RecordProcessorCheckpointer + Send + Sync> =
            Arc::new(MockRecordProcessorCheckpointer::new());
        let input = ShardEndedInput::builder().checkpointer(cp.clone()).build();
        assert!(Arc::ptr_eq(input.checkpointer(), &cp));

        let other = ShardEndedInput::builder()
            .checkpointer(Arc::new(MockRecordProcessorCheckpointer::new()))
            .build();
        assert_eq!(input, other);
    }
}
