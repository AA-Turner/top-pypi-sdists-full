//! Port of `software.amazon.kinesis.retrieval.BatchUniqueIdentifier`.

/// Immutable value identifying a specific delivered record batch by
/// `(recordBatchIdentifier, flowIdentifier)`, used for ack correlation between a
/// [`RecordsPublisher`](crate::retrieval::RecordsPublisher) and its subscriber.
///
/// Port of the Lombok `@Data` class: field-based getters plus
/// equals/hashCode/toString (here derived).
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct BatchUniqueIdentifier {
    record_batch_identifier: String,
    flow_identifier: String,
}

impl BatchUniqueIdentifier {
    /// Construct from a record-batch identifier and a flow identifier.
    pub fn new(
        record_batch_identifier: impl Into<String>,
        flow_identifier: impl Into<String>,
    ) -> Self {
        Self {
            record_batch_identifier: record_batch_identifier.into(),
            flow_identifier: flow_identifier.into(),
        }
    }

    /// The identifier of the record batch (unique per delivered batch).
    pub fn record_batch_identifier(&self) -> &str {
        &self.record_batch_identifier
    }

    /// The identifier of the flow/connection that produced the batch.
    pub fn flow_identifier(&self) -> &str {
        &self.flow_identifier
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn equality_is_field_based() {
        let a = BatchUniqueIdentifier::new("batch-1", "flow-1");
        let b = BatchUniqueIdentifier::new("batch-1", "flow-1");
        let c = BatchUniqueIdentifier::new("batch-2", "flow-1");
        assert_eq!(a, b);
        assert_ne!(a, c);
        assert_eq!(a.record_batch_identifier(), "batch-1");
        assert_eq!(a.flow_identifier(), "flow-1");
    }
}
