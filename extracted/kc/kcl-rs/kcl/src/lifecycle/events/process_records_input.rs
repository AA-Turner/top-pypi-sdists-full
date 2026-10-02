//! Port of `software.amazon.kinesis.lifecycle.events.ProcessRecordsInput`.

use std::sync::Arc;

use aws_sdk_kinesis::types::ChildShard;
use chrono::{DateTime, Utc};

use crate::processor::RecordProcessorCheckpointer;
use crate::retrieval::KinesisClientRecord;

/// Parameters to `ShardRecordProcessor::process_records`.
///
/// Port of the Lombok `@Builder(toBuilder=true) @Getter @Accessors(fluent=true)
/// @EqualsAndHashCode @ToString` class. `cacheEntryTime`/`cacheExitTime`
/// (`Instant`, used as wall-clock timestamps) map to [`DateTime<Utc>`];
/// `millisBehindLatest` (`Long`) maps to `Option<i64>`.
///
/// `PartialEq`/`Eq`/`Hash` are hand-implemented over the data fields, excluding
/// the (trait-object) checkpointer. The AWS SDK [`ChildShard`] type only
/// implements `PartialEq` (not `Eq`/`Hash`), so `Eq` is a marker over structural
/// `PartialEq` and `Hash` uses each child shard's shard id. See PORTING.md.
#[derive(Clone, bon::Builder)]
pub struct ProcessRecordsInput {
    /// The time this batch of records was received by the KCL.
    cache_entry_time: Option<DateTime<Utc>>,
    /// The time this batch of records was prepared to be provided to the processor.
    cache_exit_time: Option<DateTime<Utc>>,
    /// Whether this batch of records is at the end of the shard.
    #[builder(default)]
    is_at_shard_end: bool,
    /// The records received from Kinesis (possibly de-aggregated).
    records: Option<Vec<KinesisClientRecord>>,
    /// A checkpointer the processor can use to checkpoint its progress.
    checkpointer: Option<Arc<dyn RecordProcessorCheckpointer + Send + Sync>>,
    /// How far behind this batch of records was when received from Kinesis.
    /// Does not include [`time_spent_in_cache`](Self::time_spent_in_cache).
    millis_behind_latest: Option<i64>,
    /// Child shards, if this GetRecords request reached the shard end (else empty).
    child_shards: Option<Vec<ChildShard>>,
}

impl ProcessRecordsInput {
    /// The time this batch of records was received by the KCL.
    pub fn cache_entry_time(&self) -> Option<DateTime<Utc>> {
        self.cache_entry_time
    }

    /// The time this batch of records was prepared to be provided to the processor.
    pub fn cache_exit_time(&self) -> Option<DateTime<Utc>> {
        self.cache_exit_time
    }

    /// Whether this batch of records is at the end of the shard.
    pub fn is_at_shard_end(&self) -> bool {
        self.is_at_shard_end
    }

    /// The records received from Kinesis.
    pub fn records(&self) -> Option<&[KinesisClientRecord]> {
        self.records.as_deref()
    }

    /// The checkpointer the processor can use to checkpoint its progress.
    pub fn checkpointer(&self) -> Option<&Arc<dyn RecordProcessorCheckpointer + Send + Sync>> {
        self.checkpointer.as_ref()
    }

    /// How far behind (in milliseconds) this batch was when received.
    pub fn millis_behind_latest(&self) -> Option<i64> {
        self.millis_behind_latest
    }

    /// Child shards, if this request reached the shard end.
    pub fn child_shards(&self) -> Option<&[ChildShard]> {
        self.child_shards.as_deref()
    }

    /// How long the records spent waiting to be dispatched to the processor.
    ///
    /// Port of `timeSpentInCache()`: `Duration.between(cacheEntryTime,
    /// cacheExitTime)`, or zero if either timestamp is unset.
    pub fn time_spent_in_cache(&self) -> chrono::Duration {
        match (self.cache_entry_time, self.cache_exit_time) {
            (Some(entry), Some(exit)) => exit - entry,
            _ => chrono::Duration::zero(),
        }
    }

    /// Return a copy with `cache_exit_time` set — the Java
    /// `toBuilder().cacheExitTime(...).build()` used by
    /// `ShardConsumerSubscriber.onNext` to stamp the cache-exit timestamp.
    pub fn with_cache_exit_time(mut self, cache_exit_time: DateTime<Utc>) -> Self {
        self.cache_exit_time = Some(cache_exit_time);
        self
    }

    /// Return a copy with `records` replaced and a `checkpointer` attached — the
    /// Java `toBuilder().records(...).checkpointer(...).build()` derived copy the
    /// customer's `processRecords` callback sees (records de-aggregated/filtered).
    pub fn with_records_and_checkpointer(
        mut self,
        records: Vec<KinesisClientRecord>,
        checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync>,
    ) -> Self {
        self.records = Some(records);
        self.checkpointer = Some(checkpointer);
        self
    }
}

impl std::fmt::Debug for ProcessRecordsInput {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ProcessRecordsInput")
            .field("cache_entry_time", &self.cache_entry_time)
            .field("cache_exit_time", &self.cache_exit_time)
            .field("is_at_shard_end", &self.is_at_shard_end)
            .field("records", &self.records)
            .field("millis_behind_latest", &self.millis_behind_latest)
            .field("child_shards", &self.child_shards)
            .finish_non_exhaustive()
    }
}

impl PartialEq for ProcessRecordsInput {
    fn eq(&self, other: &Self) -> bool {
        self.cache_entry_time == other.cache_entry_time
            && self.cache_exit_time == other.cache_exit_time
            && self.is_at_shard_end == other.is_at_shard_end
            && self.records == other.records
            && self.millis_behind_latest == other.millis_behind_latest
            && self.child_shards == other.child_shards
    }
}

impl Eq for ProcessRecordsInput {}

impl std::hash::Hash for ProcessRecordsInput {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.cache_entry_time.hash(state);
        self.cache_exit_time.hash(state);
        self.is_at_shard_end.hash(state);
        self.records.hash(state);
        self.millis_behind_latest.hash(state);
        // ChildShard has no Hash impl; hash by its (stable) shard id.
        match &self.child_shards {
            None => state.write_u8(0),
            Some(shards) => {
                state.write_u8(1);
                for s in shards {
                    s.shard_id().hash(state);
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::processor::MockRecordProcessorCheckpointer;
    use chrono::TimeZone;

    #[test]
    fn defaults_and_getters() {
        let input = ProcessRecordsInput::builder()
            .records(vec![])
            .millis_behind_latest(100)
            .build();
        assert!(!input.is_at_shard_end());
        assert_eq!(input.records(), Some(&[][..]));
        assert_eq!(input.millis_behind_latest(), Some(100));
        assert_eq!(input.child_shards(), None);
        assert!(input.checkpointer().is_none());
    }

    #[test]
    fn time_spent_in_cache_is_zero_without_timestamps() {
        let input = ProcessRecordsInput::builder().build();
        assert_eq!(input.time_spent_in_cache(), chrono::Duration::zero());
    }

    #[test]
    fn time_spent_in_cache_computes_difference() {
        let entry = Utc.timestamp_opt(1_000, 0).unwrap();
        let exit = Utc.timestamp_opt(1_005, 0).unwrap();
        let input = ProcessRecordsInput::builder()
            .cache_entry_time(entry)
            .cache_exit_time(exit)
            .build();
        assert_eq!(input.time_spent_in_cache(), chrono::Duration::seconds(5));
    }

    #[test]
    fn equality_excludes_checkpointer() {
        let a = ProcessRecordsInput::builder()
            .millis_behind_latest(7)
            .checkpointer(Arc::new(MockRecordProcessorCheckpointer::new()))
            .build();
        let b = ProcessRecordsInput::builder()
            .millis_behind_latest(7)
            .checkpointer(Arc::new(MockRecordProcessorCheckpointer::new()))
            .build();
        assert_eq!(a, b);

        let c = ProcessRecordsInput::builder()
            .millis_behind_latest(8)
            .build();
        assert_ne!(a, c);
    }
}
