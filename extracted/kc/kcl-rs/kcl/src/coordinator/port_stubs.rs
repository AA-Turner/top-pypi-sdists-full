//! Minimal `// TODO(port)` stubs for coordinator dependencies owned by **later
//! coordinator sub-waves** (10c assignment/leader, 10d Scheduler) that the
//! earlier layers must name to compile.
//!
//! # 10b unification (done)
//!
//! The former `TableMigrationStatus` + `TableMigrationStatusProvider` stubs
//! (which also lived in `worker::metricstats::migration_stub`) are **removed**:
//! the real types now live in
//! [`crate::coordinator::migration::table_migration_status`] and
//! [`crate::coordinator::migration::table_migration_status_provider`]. Both the
//! `CoordinatorStateDAO` and the worker `WorkerMetricStatsDAO` routing were
//! re-pointed to them, and `worker::metricstats::migration_stub` now re-exports
//! the real types.
//!
//! No coordinator forward-ref stubs remain here at present: the table-migration
//! state machine's `LeaderLock.LEADER_HASH_KEY` is inlined as a `const` in the
//! state machine (the `leader` package lands in wave 10c), and
//! `DynamicMigrationComponentsInitializer` is ported as a mockable trait in
//! `coordinator::migration` (its full concrete impl — LAM / leader-decider
//! wiring — lands in wave 10c/10d).
