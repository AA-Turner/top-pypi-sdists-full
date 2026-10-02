//! Port of `software.amazon.kinesis.retrieval.KinesisGetRecordsResponseAdapter`.

use aws_sdk_kinesis::operation::get_records::GetRecordsOutput;
use aws_sdk_kinesis::types::ChildShard;
use aws_types::request_id::RequestId;

use crate::retrieval::get_records_response_adapter::GetRecordsResponseAdapter;
use crate::retrieval::kinesis_client_record::KinesisClientRecord;

/// [`GetRecordsResponseAdapter`] implementation wrapping a raw AWS SDK
/// `GetRecordsOutput` (the Rust SDK's `GetRecordsResponse`).
///
/// Port of the Java `@RequiredArgsConstructor @Getter(fluent) @EqualsAndHashCode`
/// class over the single `getRecordsResponse` field.
#[derive(Debug, Clone)]
pub struct KinesisGetRecordsResponseAdapter {
    get_records_response: GetRecordsOutput,
}

impl KinesisGetRecordsResponseAdapter {
    /// Wrap a raw `GetRecordsOutput`.
    pub fn new(get_records_response: GetRecordsOutput) -> Self {
        Self {
            get_records_response,
        }
    }

    /// The wrapped raw response.
    pub fn get_records_response(&self) -> &GetRecordsOutput {
        &self.get_records_response
    }
}

// `GetRecordsOutput` implements `PartialEq`, so field equality over the single
// field matches the Lombok `@EqualsAndHashCode`.
impl PartialEq for KinesisGetRecordsResponseAdapter {
    fn eq(&self, other: &Self) -> bool {
        self.get_records_response == other.get_records_response
    }
}

impl GetRecordsResponseAdapter for KinesisGetRecordsResponseAdapter {
    fn records(&self) -> Vec<KinesisClientRecord> {
        self.get_records_response
            .records()
            .iter()
            .map(KinesisClientRecord::from_record)
            .collect()
    }

    fn millis_behind_latest(&self) -> Option<i64> {
        self.get_records_response.millis_behind_latest()
    }

    fn child_shards(&self) -> Vec<ChildShard> {
        self.get_records_response.child_shards().to_vec()
    }

    fn next_shard_iterator(&self) -> Option<String> {
        self.get_records_response
            .next_shard_iterator()
            .map(str::to_string)
    }

    fn request_id(&self) -> Option<String> {
        self.get_records_response.request_id().map(str::to_string)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use aws_sdk_kinesis::types::Record;
    use aws_smithy_types::Blob;

    #[test]
    fn records_are_converted_to_client_records() {
        let response = GetRecordsOutput::builder()
            .records(
                Record::builder()
                    .sequence_number("seq-1")
                    .partition_key("pk-1")
                    .data(Blob::new(b"hello".to_vec()))
                    .build()
                    .unwrap(),
            )
            .millis_behind_latest(42)
            .next_shard_iterator("next-iter")
            .build()
            .unwrap();

        let adapter = KinesisGetRecordsResponseAdapter::new(response);
        let records = adapter.records();
        assert_eq!(records.len(), 1);
        assert_eq!(records[0].sequence_number(), Some("seq-1"));
        assert_eq!(adapter.millis_behind_latest(), Some(42));
        assert_eq!(adapter.next_shard_iterator().as_deref(), Some("next-iter"));
        assert!(adapter.child_shards().is_empty());
    }

    #[test]
    fn to_process_records_input_maps_fields() {
        let response = GetRecordsOutput::builder()
            .records(
                Record::builder()
                    .sequence_number("seq-2")
                    .partition_key("pk-2")
                    .data(Blob::new(b"data".to_vec()))
                    .build()
                    .unwrap(),
            )
            .millis_behind_latest(100)
            .build()
            .unwrap();

        let adapter = KinesisGetRecordsResponseAdapter::new(response);
        let input = adapter.to_process_records_input();
        assert_eq!(input.records().map(|r| r.len()), Some(1));
        assert_eq!(input.millis_behind_latest(), Some(100));
        assert!(!input.is_at_shard_end());
    }
}
