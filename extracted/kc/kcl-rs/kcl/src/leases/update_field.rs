//! Port of `software.amazon.kinesis.leases.UpdateField`.

/// Fields that are updated only once during the lifetime of a lease.
///
/// Since these are metadata that will not affect lease ownership or data
/// durability, any elected leader or worker may set these fields directly
/// without conditional (optimistic-lock) checks.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum UpdateField {
    /// The child shard IDs discovered at `SHARD_END`.
    ChildShards,
    /// The hash-key range of the shard (kept for backfilling while rolling
    /// forward to newer versions).
    HashKeyRange,
}
