//! Port of `software.amazon.kinesis.processor.RecordProcessorCheckpointer`.

use aws_sdk_kinesis::types::Record;

use crate::exceptions::KinesisClientLibError;
use crate::processor::checkpointer::Checkpointer;
use crate::processor::prepared_checkpointer::PreparedCheckpointer;

/// Used by record processors to checkpoint their progress at various
/// granularities, and to "prepare" a checkpoint (two-phase checkpoint for
/// idempotent side effects across failover) with optional opaque application
/// state bytes.
///
/// Ported as a **synchronous**, object-safe trait (used as
/// `Arc<dyn RecordProcessorCheckpointer + Send + Sync>`). Java has many
/// overloads of `checkpoint`/`prepareCheckpoint`; since Rust has no overloading
/// they are renamed (see the individual methods).
///
/// Checked exceptions map to [`KinesisClientLibError`]; Java's
/// `IllegalArgumentException` (out-of-range/invalid sequence number) maps to a
/// `panic!`. `#[automock]` provides a mock for tests.
#[cfg_attr(test, mockall::automock)]
pub trait RecordProcessorCheckpointer {
    /// Checkpoint at the last data record delivered to the record processor.
    /// Java: `checkpoint()`.
    fn checkpoint(&self) -> Result<(), KinesisClientLibError>;

    /// Checkpoint at the provided record. Java: `checkpoint(Record)`.
    fn checkpoint_record(&self, record: &Record) -> Result<(), KinesisClientLibError>;

    /// Checkpoint at the provided sequence number. Java: `checkpoint(String)`.
    fn checkpoint_sequence(&self, sequence_number: &str) -> Result<(), KinesisClientLibError>;

    /// Checkpoint at the provided sequence and sub-sequence number.
    /// Java: `checkpoint(String, long)`.
    fn checkpoint_sequence_sub(
        &self,
        sequence_number: &str,
        sub_sequence_number: i64,
    ) -> Result<(), KinesisClientLibError>;

    /// Prepare a pending checkpoint at the last data record delivered.
    /// Java: `prepareCheckpoint()`.
    fn prepare_checkpoint(
        &self,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError>;

    /// Prepare a pending checkpoint at the last data record, carrying application
    /// state. Java: `prepareCheckpoint(byte[])`.
    fn prepare_checkpoint_state(
        &self,
        application_state: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError>;

    /// Prepare a pending checkpoint at the provided record.
    /// Java: `prepareCheckpoint(Record)`.
    fn prepare_checkpoint_record(
        &self,
        record: &Record,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError>;

    /// Prepare a pending checkpoint at the provided record, carrying application
    /// state. Java: `prepareCheckpoint(Record, byte[])`.
    fn prepare_checkpoint_record_state(
        &self,
        record: &Record,
        application_state: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError>;

    /// Prepare a pending checkpoint at the provided sequence number.
    /// Java: `prepareCheckpoint(String)`.
    fn prepare_checkpoint_sequence(
        &self,
        sequence_number: &str,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError>;

    /// Prepare a pending checkpoint at the provided sequence number, carrying
    /// application state. Java: `prepareCheckpoint(String, byte[])`.
    fn prepare_checkpoint_sequence_state(
        &self,
        sequence_number: &str,
        application_state: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError>;

    /// Prepare a pending checkpoint at the provided sequence and sub-sequence
    /// number. Java: `prepareCheckpoint(String, long)`.
    fn prepare_checkpoint_sequence_sub(
        &self,
        sequence_number: &str,
        sub_sequence_number: i64,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError>;

    /// Prepare a pending checkpoint at the provided sequence and sub-sequence
    /// number, carrying application state.
    /// Java: `prepareCheckpoint(String, long, byte[])`.
    fn prepare_checkpoint_sequence_sub_state(
        &self,
        sequence_number: &str,
        sub_sequence_number: i64,
        application_state: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError>;

    /// The underlying checkpoint-store [`Checkpointer`]. Java: `checkpointer()`.
    fn checkpointer(&self) -> Box<dyn Checkpointer + Send + Sync>;
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::processor::checkpointer::MockCheckpointer;
    use crate::processor::prepared_checkpointer::MockPreparedCheckpointer;

    #[test]
    fn mock_checkpoint_variants_dispatch() {
        let mut mock = MockRecordProcessorCheckpointer::new();
        mock.expect_checkpoint().times(1).returning(|| Ok(()));
        mock.expect_checkpoint_sequence_sub()
            .withf(|seq, sub| seq == "42" && *sub == 3)
            .times(1)
            .returning(|_, _| Ok(()));
        mock.expect_prepare_checkpoint_sequence_state()
            .times(1)
            .returning(|_, _| Ok(Box::new(MockPreparedCheckpointer::new())));
        mock.expect_checkpointer()
            .times(1)
            .returning(|| Box::new(MockCheckpointer::new()));

        assert!(mock.checkpoint().is_ok());
        assert!(mock.checkpoint_sequence_sub("42", 3).is_ok());
        assert!(mock
            .prepare_checkpoint_sequence_state("42", b"state")
            .is_ok());
        let _ = mock.checkpointer();
    }

    #[test]
    fn checkpoint_error_is_surfaced() {
        let mut mock = MockRecordProcessorCheckpointer::new();
        mock.expect_checkpoint()
            .returning(|| Err(KinesisClientLibError::shutdown("shut down")));
        let err = mock.checkpoint().unwrap_err();
        assert!(matches!(err, KinesisClientLibError::Shutdown { .. }));
    }
}
