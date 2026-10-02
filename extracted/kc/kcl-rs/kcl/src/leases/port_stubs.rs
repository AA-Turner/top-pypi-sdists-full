//! Minimal `// TODO(port)` stub types for cross-subsystem dependencies of the
//! leases-6b interfaces that have **not yet been ported**.
//!
//! Each stub is the smallest surface needed for the leases traits
//! ([`LeaseCoordinator`](crate::leases::LeaseCoordinator),
//! [`LeaseManagementFactory`](crate::leases::LeaseManagementFactory)) to compile.
//! The **owning wave** listed on each stub must replace it with the real port.
//!
//! None of these carry real behavior. They exist purely so the interface
//! signatures can name the right types today.

// ---------------------------------------------------------------------------
// coordinator subsystem (wave 10a) — REPLACED by the real ports:
//   `MigrationAdaptiveLeaseAssignmentModeProvider`
//        -> `crate::coordinator::MigrationAdaptiveLeaseAssignmentModeProvider`
//   `DeletedStreamListProvider` -> `crate::coordinator::DeletedStreamListProvider`
//   `StreamInfoManager`         -> `crate::coordinator::StreamInfoManager`
//   `StreamIdCacheManager`      -> `crate::coordinator::StreamIdCacheManager`
//   `StreamInfoDAO`             -> `crate::coordinator::StreamInfoDAO`
//   `StreamIdOnboardingState`   -> `crate::coordinator::StreamIdOnboardingState` (enum)
//   `StreamInfoMode`            -> `crate::coordinator::StreamInfoMode` (enum)
// The leases importers now reference the real coordinator types directly.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// lifecycle subsystem (wave 7) — the `ShardConsumer` stub has been REPLACED by
// the real `crate::lifecycle::ShardConsumer` (7b). The deprecated
// `createLeaseCoordinator(..., shardInfoShardConsumerMap)` factory overloads now
// take `HashMap<ShardInfo, Arc<lifecycle::ShardConsumer>>`.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// worker subsystem (wave 9) — REPLACED by the real ports:
//   `WorkerMetric`      -> `crate::worker::metric::WorkerMetric` (trait)
//   `WorkerMetricStats` -> `crate::worker::metricstats::WorkerMetricStats`
// (previously stubbed here; removed once the worker wave landed).
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// common sub-configs — now REAL ports (common wave 1):
//   `LeaseCleanupConfig` -> `crate::common::LeaseCleanupConfig`
//   `DdbTableConfig`     -> `crate::common::DdbTableConfig`
// (previously stubbed here; removed once the common wave landed).
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// leases::dynamodb (wave 6d) — REPLACED by the real ports:
//   `TableCreatorCallback`           -> `crate::leases::dynamodb::TableCreatorCallback`
//        (a trait; `LeaseManagementConfig` now holds `Arc<dyn TableCreatorCallback>`,
//         defaulting to `NoopTableCreatorCallback`).
//   `DynamoDbLeaseManagementFactory` -> `crate::leases::dynamodb::DynamoDBLeaseManagementFactory`
//        (the config no longer holds a factory slot; the Scheduler wave 10d
//         constructs the factory directly).
// This module now contains no stubs — every leases cross-wave dependency is a
// real port.
// ---------------------------------------------------------------------------
