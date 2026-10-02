//! Port of `FanOutRecordsPublisher.FanoutRecordsRetrieved` (the nested
//! `RecordsRetrieved` value type for the EFO path).

use uuid::Uuid;

use crate::lifecycle::events::process_records_input::ProcessRecordsInput;
use crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier;
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::records_retrieved::RecordsRetrieved;

/// The concrete [`RecordsRetrieved`] for the fan-out path.
///
/// Port of the Java nested `@Data @Accessors(fluent=true)` class. `batch_id` is a
/// random UUID generated once at construction; `batch_unique_identifier()` wraps
/// it with the originating flow's identifier.
#[derive(Debug, Clone)]
pub struct FanoutRecordsRetrieved {
    process_records_input: ProcessRecordsInput,
    continuation_sequence_number: ExtendedSequenceNumber,
    flow_identifier: String,
    batch_id: String,
}

impl FanoutRecordsRetrieved {
    /// Construct (Java constructor: `batchUniqueIdentifier` = a fresh UUID).
    pub fn new(
        process_records_input: ProcessRecordsInput,
        continuation_sequence_number: ExtendedSequenceNumber,
        flow_identifier: impl Into<String>,
    ) -> Self {
        Self {
            process_records_input,
            continuation_sequence_number,
            flow_identifier: flow_identifier.into(),
            batch_id: Uuid::new_v4().to_string(),
        }
    }

    /// The continuation sequence number to resume from (SHARD_END sentinel at end).
    pub fn continuation_sequence_number(&self) -> &ExtendedSequenceNumber {
        &self.continuation_sequence_number
    }

    /// The identifier of the flow that produced this batch.
    pub fn flow_identifier(&self) -> &str {
        &self.flow_identifier
    }
}

impl RecordsRetrieved for FanoutRecordsRetrieved {
    fn process_records_input(&self) -> &ProcessRecordsInput {
        &self.process_records_input
    }

    fn batch_unique_identifier(&self) -> BatchUniqueIdentifier {
        BatchUniqueIdentifier::new(self.batch_id.clone(), self.flow_identifier.clone())
    }

    fn as_any(&self) -> Option<&dyn std::any::Any> {
        Some(self)
    }
}
