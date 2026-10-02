//! Port of `software.amazon.kinesis.coordinator.DeletedStreamListProvider`.

use std::collections::HashSet;
use std::sync::Mutex;

use crate::common::StreamIdentifier;

/// Thread-safe in-memory set of [`StreamIdentifier`]s discovered to be deleted
/// (e.g. via `ResourceNotFound` during shard sync) awaiting lease cleanup by the
/// Scheduler. Java `DeletedStreamListProvider`.
///
/// Java uses `ConcurrentHashMap.newKeySet()`; the Rust port uses a
/// `Mutex<HashSet>` (the access pattern is add + drain, low contention).
/// `purge_all_deleted_stream` drains via `std::mem::take` (a single atomic drain,
/// slightly stronger than Java's snapshot-then-`removeAll` best-effort idiom).
///
/// `StreamIdentifier`'s `Eq`/`Hash` exclude arn/type, matching the Java set
/// semantics.
#[derive(Debug, Default)]
pub struct DeletedStreamListProvider {
    deleted_streams: Mutex<HashSet<StreamIdentifier>>,
}

impl DeletedStreamListProvider {
    pub fn new() -> Self {
        Self::default()
    }

    /// Java `add(StreamIdentifier)`.
    pub fn add(&self, stream_identifier: StreamIdentifier) {
        tracing::info!(stream = %stream_identifier, "Added");
        self.deleted_streams
            .lock()
            .expect("deleted_streams mutex poisoned")
            .insert(stream_identifier);
    }

    /// Java `purgeAllDeletedStream()` — returns and empties the current set.
    pub fn purge_all_deleted_stream(&self) -> HashSet<StreamIdentifier> {
        let mut guard = self
            .deleted_streams
            .lock()
            .expect("deleted_streams mutex poisoned");
        std::mem::take(&mut *guard)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_then_purge_returns_and_empties() {
        let provider = DeletedStreamListProvider::new();
        let s1 = StreamIdentifier::single_stream_instance("stream-1");
        let s2 = StreamIdentifier::single_stream_instance("stream-2");
        provider.add(s1.clone());
        provider.add(s2.clone());

        let purged = provider.purge_all_deleted_stream();
        assert_eq!(purged.len(), 2);
        assert!(purged.contains(&s1));
        assert!(purged.contains(&s2));

        // Second purge is empty.
        assert!(provider.purge_all_deleted_stream().is_empty());
    }

    #[test]
    fn duplicate_adds_dedup() {
        let provider = DeletedStreamListProvider::new();
        let s1 = StreamIdentifier::single_stream_instance("stream-1");
        provider.add(s1.clone());
        provider.add(s1.clone());
        assert_eq!(provider.purge_all_deleted_stream().len(), 1);
    }
}
