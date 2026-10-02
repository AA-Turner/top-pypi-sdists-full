//! Port of `software.amazon.kinesis.lifecycle.ShutdownInput`.

use std::sync::Arc;

use crate::lifecycle::ShutdownReason;
use crate::processor::RecordProcessorCheckpointer;

/// Container for the parameters to the (legacy/back-compat)
/// `ShardRecordProcessor::shutdown(ShutdownInput)` callback, carrying the
/// [`ShutdownReason`] and a checkpointer.
///
/// Port of the Lombok `@Builder @Getter @Accessors(fluent=true)
/// @EqualsAndHashCode @ToString` class. Because the checkpointer is a trait
/// object, `PartialEq`/`Eq`/`Hash` are hand-implemented over the data fields
/// (just `shutdown_reason`), excluding the checkpointer.
#[derive(Clone, bon::Builder)]
pub struct ShutdownInput {
    /// The reason the record processor is being shut down.
    shutdown_reason: Option<ShutdownReason>,
    /// The checkpointer the record processor should use to checkpoint.
    checkpointer: Option<Arc<dyn RecordProcessorCheckpointer + Send + Sync>>,
}

impl ShutdownInput {
    /// The reason for the shutdown.
    pub fn shutdown_reason(&self) -> Option<ShutdownReason> {
        self.shutdown_reason
    }

    /// The checkpointer the record processor should use.
    pub fn checkpointer(&self) -> Option<&Arc<dyn RecordProcessorCheckpointer + Send + Sync>> {
        self.checkpointer.as_ref()
    }
}

impl std::fmt::Debug for ShutdownInput {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ShutdownInput")
            .field("shutdown_reason", &self.shutdown_reason)
            .finish_non_exhaustive()
    }
}

impl PartialEq for ShutdownInput {
    fn eq(&self, other: &Self) -> bool {
        self.shutdown_reason == other.shutdown_reason
    }
}

impl Eq for ShutdownInput {}

impl std::hash::Hash for ShutdownInput {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.shutdown_reason.hash(state);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builder_and_eq_excludes_checkpointer() {
        let a = ShutdownInput::builder()
            .shutdown_reason(ShutdownReason::ShardEnd)
            .build();
        let b = ShutdownInput::builder()
            .shutdown_reason(ShutdownReason::ShardEnd)
            .build();
        assert_eq!(a, b);
        assert_eq!(a.shutdown_reason(), Some(ShutdownReason::ShardEnd));
        assert!(a.checkpointer().is_none());
    }
}
