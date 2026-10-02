//! Re-export shim for the coordinator-migration types that drive
//! [`WorkerMetricStatsDAO`](super::WorkerMetricStatsDAO) read/write routing.
//!
//! # Unified in coordinator wave 10b
//!
//! This module used to define stub `TableMigrationStatus` +
//! `TableMigrationStatusProvider` types. The **real** types now live in
//! [`crate::coordinator::migration`]; this module re-exports them so all worker
//! call sites (the DAO + its delegate) keep compiling unchanged. The stubs are
//! gone; both DAOs consume the single real type.

pub use crate::coordinator::migration::table_migration_status::TableMigrationStatus;
pub use crate::coordinator::migration::table_migration_status_provider::TableMigrationStatusProvider;

#[cfg(test)]
pub use crate::coordinator::migration::table_migration_status_provider::MockTableMigrationStatusProvider;
