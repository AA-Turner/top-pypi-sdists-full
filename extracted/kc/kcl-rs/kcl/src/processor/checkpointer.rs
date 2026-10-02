//! Port of `software.amazon.kinesis.processor.Checkpointer`.

use crate::checkpoint::Checkpoint;
use crate::exceptions::KinesisClientLibError;
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Lower-level SPI for the actual checkpoint storage backend (backed by the
/// lease / DynamoDB table): set/get checkpoints and pending ("prepared")
/// checkpoints per lease key, plus a mutable "current operation" tag used for
/// diagnostics/metrics.
///
/// Ported as a **synchronous** trait (the concrete DynamoDB-backed impl lives in
/// `checkpoint::dynamodb`, out of scope). Checked-exception methods
/// (`KinesisClientLibException`) return
/// `Result<_, KinesisClientLibError>`; the nullable getters return `Option`.
///
/// `#[automock]` provides a Mockito-equivalent mock for tests (the Java tests
/// mock this interface).
#[cfg_attr(test, mockall::automock)]
pub trait Checkpointer {
    /// Record a checkpoint for a shard. Upon failover, record processing resumes
    /// from this point.
    ///
    /// The `concurrency_token` enables optimistic-locking / conditional writes so
    /// a failed-over worker does not clobber a checkpoint written by a new owner.
    fn set_checkpoint(
        &self,
        lease_key: &str,
        checkpoint_value: &ExtendedSequenceNumber,
        concurrency_token: &str,
    ) -> Result<(), KinesisClientLibError>;

    /// Get the current checkpoint stored for the specified shard, or `None` if
    /// there is no record for the shard.
    fn get_checkpoint(
        &self,
        lease_key: &str,
    ) -> Result<Option<ExtendedSequenceNumber>, KinesisClientLibError>;

    /// Get the current checkpoint object stored for the specified shard (holding
    /// both the committed and pending checkpoint), or `None` if there is no
    /// record for the shard.
    fn get_checkpoint_object(
        &self,
        lease_key: &str,
    ) -> Result<Option<Checkpoint>, KinesisClientLibError>;

    /// Record intent to checkpoint for a shard. Upon failover, the pending
    /// checkpoint is passed to the new record processor's `initialize()`.
    fn prepare_checkpoint(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: &str,
    ) -> Result<(), KinesisClientLibError>;

    /// Record intent to checkpoint for a shard, carrying opaque application state.
    fn prepare_checkpoint_with_state(
        &self,
        lease_key: &str,
        pending_checkpoint: &ExtendedSequenceNumber,
        concurrency_token: &str,
        pending_checkpoint_state: &[u8],
    ) -> Result<(), KinesisClientLibError>;

    /// Set the current logical operation tag (for logging/metrics correlation).
    fn set_operation(&self, operation: &str);

    /// Get the current logical operation tag.
    fn operation(&self) -> String;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn mock_get_checkpoint_returns_optional() {
        let mut mock = MockCheckpointer::new();
        mock.expect_get_checkpoint()
            .withf(|k| k == "lease-1")
            .returning(|_| Ok(Some(ExtendedSequenceNumber::from_sequence_number("100"))));
        mock.expect_get_checkpoint_object().returning(|_| Ok(None));

        let cp = mock.get_checkpoint("lease-1").unwrap();
        assert_eq!(
            cp,
            Some(ExtendedSequenceNumber::from_sequence_number("100"))
        );
        assert_eq!(mock.get_checkpoint_object("lease-1").unwrap(), None);
    }

    #[test]
    fn mock_set_checkpoint_error_is_surfaced() {
        let mut mock = MockCheckpointer::new();
        mock.expect_set_checkpoint()
            .returning(|_, _, _| Err(KinesisClientLibError::dependency("db down")));
        let esn = ExtendedSequenceNumber::from_sequence_number("1");
        let err = mock.set_checkpoint("lease-1", &esn, "token").unwrap_err();
        assert!(err.is_retryable());
    }
}
