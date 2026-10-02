//! Port of `software.amazon.kinesis.retrieval.DataFetcherResult`.

use crate::retrieval::get_records_response_adapter::GetRecordsResponseAdapter;

/// The outcome of a single `GetRecords` fetch attempt, and the control point for
/// advancing the [`DataFetcher`](crate::retrieval::polling_stubs)'s internal
/// iterator.
///
/// Port of the Java interface. The deprecated raw-`GetRecordsResponse` overloads
/// (`getResult` / `accept`) are dropped (per the arch-map "skip deprecated
/// raw-response paths"); only the adapter-shaped surface is kept.
///
/// # Critical invariant
///
/// Calling [`accept_adapter`](Self::accept_adapter) is what **advances the shard
/// iterator** (a side effect). [`get_result_adapter`](Self::get_result_adapter)
/// must be idempotent / non-advancing. This asymmetry is load-bearing and
/// preserved exactly.
pub trait DataFetcherResult: Send {
    /// The result of the request, as a [`GetRecordsResponseAdapter`], **without**
    /// advancing the iterator (idempotent).
    fn get_result_adapter(&self) -> Box<dyn GetRecordsResponseAdapter>;

    /// Accept the result, **advancing the shard iterator** (side-effecting). A
    /// result must be accepted before any further progress can be made.
    fn accept_adapter(&mut self) -> Box<dyn GetRecordsResponseAdapter>;

    /// Whether this result is at the end of the shard.
    fn is_shard_end(&self) -> bool;
}
