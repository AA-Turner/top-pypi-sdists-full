//! Port of `software.amazon.kinesis.lifecycle.events.ShutdownRequestedInput`.

use std::sync::Arc;

use crate::processor::RecordProcessorCheckpointer;

/// Provides access to a checkpointer so a `ShardRecordProcessor` can checkpoint
/// before the lease is released during shutdown. Passed to
/// `ShardRecordProcessor::shutdown_requested`.
///
/// Port of the Lombok `@Builder @Getter @Accessors(fluent=true)
/// @EqualsAndHashCode @ToString` class. `PartialEq`/`Eq`/`Hash` are
/// hand-implemented over the data fields, excluding the (trait-object)
/// checkpointer. See PORTING.md.
#[derive(Clone, bon::Builder)]
pub struct ShutdownRequestedInput {
    /// Checkpointer used to record the current progress of the record processor.
    checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync>,
}

impl ShutdownRequestedInput {
    /// The checkpointer for recording progress before shutdown.
    pub fn checkpointer(&self) -> &Arc<dyn RecordProcessorCheckpointer + Send + Sync> {
        &self.checkpointer
    }
}

impl std::fmt::Debug for ShutdownRequestedInput {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ShutdownRequestedInput")
            .finish_non_exhaustive()
    }
}

impl PartialEq for ShutdownRequestedInput {
    fn eq(&self, _other: &Self) -> bool {
        true
    }
}

impl Eq for ShutdownRequestedInput {}

impl std::hash::Hash for ShutdownRequestedInput {
    fn hash<H: std::hash::Hasher>(&self, _state: &mut H) {}
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::processor::MockRecordProcessorCheckpointer;

    #[test]
    fn holds_checkpointer() {
        let cp: Arc<dyn RecordProcessorCheckpointer + Send + Sync> =
            Arc::new(MockRecordProcessorCheckpointer::new());
        let input = ShutdownRequestedInput::builder()
            .checkpointer(cp.clone())
            .build();
        assert!(Arc::ptr_eq(input.checkpointer(), &cp));
    }
}
