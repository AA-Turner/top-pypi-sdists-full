//! Port of `PrefetchRecordsPublisher.PrefetchRecordsRetrieved` (the nested
//! `RecordsRetrieved` value type for the polling path).

use chrono::Utc;
use uuid::Uuid;

use crate::lifecycle::events::process_records_input::ProcessRecordsInput;
use crate::retrieval::batch_unique_identifier::BatchUniqueIdentifier;
use crate::retrieval::records_retrieved::RecordsRetrieved;

/// One queued/delivered batch of records plus the bookkeeping needed to
/// ack/evict it and detect duplicate dispatch.
///
/// Port of the Java nested `@Data @Accessors(fluent=true)` class. `dispatched`
/// is tracked to prevent double delivery of the head-of-queue element.
#[derive(Debug, Clone)]
pub struct PrefetchRecordsRetrieved {
    process_records_input: ProcessRecordsInput,
    last_batch_sequence_number: String,
    shard_iterator: Option<String>,
    batch_unique_identifier: BatchUniqueIdentifier,
    dispatched: bool,
}

impl PrefetchRecordsRetrieved {
    /// Construct a batch.
    pub fn new(
        process_records_input: ProcessRecordsInput,
        last_batch_sequence_number: impl Into<String>,
        shard_iterator: Option<String>,
        batch_unique_identifier: BatchUniqueIdentifier,
    ) -> Self {
        Self {
            process_records_input,
            last_batch_sequence_number: last_batch_sequence_number.into(),
            shard_iterator,
            batch_unique_identifier,
            dispatched: false,
        }
    }

    /// The sequence number of the last record in the batch (or the session's
    /// highest sequence number if the batch is empty).
    pub fn last_batch_sequence_number(&self) -> &str {
        &self.last_batch_sequence_number
    }

    /// The shard iterator that produced the batch (used on reset).
    pub fn shard_iterator(&self) -> Option<&str> {
        self.shard_iterator.as_deref()
    }

    /// The unique identifier of this batch.
    pub fn batch_id(&self) -> &BatchUniqueIdentifier {
        &self.batch_unique_identifier
    }

    /// Whether this batch was already dispatched for delivery.
    pub fn is_dispatched(&self) -> bool {
        self.dispatched
    }

    /// Mark this batch as dispatched.
    pub fn mark_dispatched(&mut self) {
        self.dispatched = true;
    }

    /// Produce a copy stamped with the cache-exit time (Java `prepareForPublish`).
    ///
    /// Rebuilds the [`ProcessRecordsInput`] from its getters (bon does not derive
    /// a `to_builder`; the lifecycle-owned type has no such method), copying every
    /// data field and setting `cache_exit_time` to now.
    pub fn prepare_for_publish(&self) -> PrefetchRecordsRetrieved {
        let src = &self.process_records_input;
        let input = ProcessRecordsInput::builder()
            .maybe_cache_entry_time(src.cache_entry_time())
            .cache_exit_time(Utc::now())
            .is_at_shard_end(src.is_at_shard_end())
            .maybe_records(src.records().map(|r| r.to_vec()))
            .maybe_checkpointer(src.checkpointer().cloned())
            .maybe_millis_behind_latest(src.millis_behind_latest())
            .maybe_child_shards(src.child_shards().map(|c| c.to_vec()))
            .build();
        PrefetchRecordsRetrieved {
            process_records_input: input,
            last_batch_sequence_number: self.last_batch_sequence_number.clone(),
            shard_iterator: self.shard_iterator.clone(),
            batch_unique_identifier: self.batch_unique_identifier.clone(),
            dispatched: self.dispatched,
        }
    }

    /// Generate a fresh batch unique identifier (Java
    /// `generateBatchUniqueIdentifier`): a random UUID with an empty flow string.
    pub fn generate_batch_unique_identifier() -> BatchUniqueIdentifier {
        BatchUniqueIdentifier::new(Uuid::new_v4().to_string(), "")
    }
}

impl RecordsRetrieved for PrefetchRecordsRetrieved {
    fn process_records_input(&self) -> &ProcessRecordsInput {
        &self.process_records_input
    }

    fn batch_unique_identifier(&self) -> BatchUniqueIdentifier {
        self.batch_unique_identifier.clone()
    }

    fn as_any(&self) -> Option<&dyn std::any::Any> {
        Some(self)
    }
}
