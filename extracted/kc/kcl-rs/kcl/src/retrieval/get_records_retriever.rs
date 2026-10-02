//! Port of `software.amazon.kinesis.retrieval.GetRecordsRetriever`.

use async_trait::async_trait;
use aws_sdk_kinesis::operation::get_records::GetRecordsOutput;

/// Minimal legacy interface: get the next batch of records given `max_records`.
///
/// Port of the Java interface. The arch-map notes this is legacy with no known
/// implementers; it is ported for API-surface completeness. Async because it
/// retrieves from Kinesis. `GetRecordsResponse` maps to the Rust SDK's
/// [`GetRecordsOutput`].
#[async_trait]
pub trait GetRecordsRetriever: Send + Sync {
    /// Retrieve the next set of records, restricting the count to `max_records`.
    async fn get_next_records(&self, max_records: i32) -> GetRecordsOutput;
}
