//! Port of `software.amazon.kinesis.retrieval.GetRecordsResponseAdapter`.

use aws_sdk_kinesis::types::ChildShard;

use crate::lifecycle::events::process_records_input::ProcessRecordsInput;
use crate::retrieval::kinesis_client_record::KinesisClientRecord;

/// Adapter unifying the fields KCL needs from a GetRecords-like response
/// (records / millisBehindLatest / childShards / nextShardIterator / requestId)
/// regardless of the underlying SDK response shape.
///
/// Port of the Java interface. Introduced to decouple from the deprecated raw
/// `GetRecordsResponse`; the sole impl here is
/// [`KinesisGetRecordsResponseAdapter`](crate::retrieval::KinesisGetRecordsResponseAdapter).
///
/// The trait is object-safe (`Box<dyn GetRecordsResponseAdapter>`), so
/// [`DataFetcherResult`](crate::retrieval::DataFetcherResult) can hand one back.
pub trait GetRecordsResponseAdapter: Send + Sync {
    /// The records retrieved from GetRecords, converted to
    /// [`KinesisClientRecord`]s.
    fn records(&self) -> Vec<KinesisClientRecord>;

    /// The number of milliseconds the response is from the tip of the stream
    /// (Java `Long`, nullable → `Option`).
    fn millis_behind_latest(&self) -> Option<i64>;

    /// The child shards of the shard, present on shard-end.
    fn child_shards(&self) -> Vec<ChildShard>;

    /// The next shard iterator, or `None` at shard end.
    fn next_shard_iterator(&self) -> Option<String>;

    /// The request id of the GetRecords operation.
    fn request_id(&self) -> Option<String>;

    /// Transform into a [`ProcessRecordsInput`] (the downstream payload).
    ///
    /// Port of the Java default method. Sets `records`, `millisBehindLatest`,
    /// and `childShards` (leaving cache/shard-end/checkpointer fields at their
    /// defaults, exactly as Java's `ProcessRecordsInput.builder()` call does).
    fn to_process_records_input(&self) -> ProcessRecordsInput {
        ProcessRecordsInput::builder()
            .records(self.records())
            .maybe_millis_behind_latest(self.millis_behind_latest())
            .child_shards(self.child_shards())
            .build()
    }
}
