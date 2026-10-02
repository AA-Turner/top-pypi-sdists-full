//! Doc-only stub for the deprecated
//! `software.amazon.kinesis.leases.exceptions.ShardSyncer`.
//!
//! `ShardSyncer` is a `@Deprecated` thin static-facade wrapper that delegates to
//! a shared `HierarchicalShardSyncer` singleton — its single method,
//! `checkAndCreateLeasesForNewShards`, simply forwards to
//! `HierarchicalShardSyncer.checkAndCreateLeaseForNewShards`.
//!
//! TODO(port): This cannot be ported in sub-wave 6a because it depends on types
//! not yet ported — `HierarchicalShardSyncer`, `LeaseRefresher`,
//! `ShardDetector` (full), `MetricsScope` (already ported), and
//! `InitialPositionInStreamExtended` (already ported). It belongs to the
//! shard-sync sub-wave alongside `HierarchicalShardSyncer`. Because the class is
//! deprecated and is a pure delegation shim, it will likely be folded directly
//! into `HierarchicalShardSyncer` (or dropped) rather than reproduced verbatim.
//! No runtime code or tests are emitted here.
