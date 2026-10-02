//! Port of `software.amazon.kinesis.coordinator.migration.TableMigrationStatus`.
//!
//! This is the **real** `TableMigrationStatus` — it replaces the stub previously
//! defined in both `coordinator::port_stubs` and
//! `worker::metricstats::migration_stub`. Both the `CoordinatorStateDAO` and
//! `WorkerMetricStatsDAO` routing now consume this type.

use std::collections::HashMap;

use crate::coordinator::migration::table_migration_state::DEFAULT_BAKE_TIME_SECONDS;

/// The 5 states of the table-consolidation (3.4 -> 3.5+) migration.
///
/// Persisted via `name()` string to DynamoDB — never reorder/rename/reuse.
/// Each variant carries a **default bake time (seconds)** used before advancing
/// to the state (keyed by the *destination* status, see `get_bake_time_seconds`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TableMigrationStatus {
    /// Local-only state before the status is resolved from DDB + config.
    Unknown,
    /// All workers emit min support code; bake time to DEPLOYED has started.
    Init,
    /// Steady Phase 1 state; ready for Phase 2 deployment.
    Deployed,
    /// Phase 2 deployed; workers write to lease table; leader moved entries.
    Pending,
    /// Migration complete; lease-table-only. Terminal, no rollback.
    Complete,
}

impl TableMigrationStatus {
    /// The Java `name()` string used for DynamoDB persistence. **Wire-format
    /// contract** — matches Java exactly.
    pub fn name(&self) -> &'static str {
        match self {
            TableMigrationStatus::Unknown => "TABLE_MIGRATION_STATUS_UNKNOWN",
            TableMigrationStatus::Init => "TABLE_MIGRATION_STATUS_INIT",
            TableMigrationStatus::Deployed => "TABLE_MIGRATION_STATUS_DEPLOYED",
            TableMigrationStatus::Pending => "TABLE_MIGRATION_STATUS_PENDING",
            TableMigrationStatus::Complete => "TABLE_MIGRATION_STATUS_COMPLETE",
        }
    }

    /// Java `TableMigrationStatus.valueOf(String)` — returns `None` for unknown.
    pub fn from_name(s: &str) -> Option<Self> {
        match s {
            "TABLE_MIGRATION_STATUS_UNKNOWN" => Some(TableMigrationStatus::Unknown),
            "TABLE_MIGRATION_STATUS_INIT" => Some(TableMigrationStatus::Init),
            "TABLE_MIGRATION_STATUS_DEPLOYED" => Some(TableMigrationStatus::Deployed),
            "TABLE_MIGRATION_STATUS_PENDING" => Some(TableMigrationStatus::Pending),
            "TABLE_MIGRATION_STATUS_COMPLETE" => Some(TableMigrationStatus::Complete),
            _ => None,
        }
    }

    /// The default bake time (seconds) associated with this status as a
    /// transition *destination*. DEPLOYED and COMPLETE default to
    /// [`DEFAULT_BAKE_TIME_SECONDS`]; the rest are 0 (unused as targets).
    fn default_bake_time_seconds(&self) -> i64 {
        match self {
            TableMigrationStatus::Deployed | TableMigrationStatus::Complete => {
                DEFAULT_BAKE_TIME_SECONDS
            }
            _ => 0,
        }
    }

    /// Java `getBakeTimeSeconds(Map<TableMigrationStatus, Long> overrides)` —
    /// returns the override for this status if present, else the default.
    pub fn get_bake_time_seconds(&self, overrides: &HashMap<TableMigrationStatus, i64>) -> i64 {
        overrides
            .get(self)
            .copied()
            .unwrap_or_else(|| self.default_bake_time_seconds())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn get_bake_time_seconds_with_default_returns_default() {
        let bake = TableMigrationStatus::Deployed.get_bake_time_seconds(&HashMap::new());
        assert_eq!(bake, DEFAULT_BAKE_TIME_SECONDS);
    }

    #[test]
    fn get_bake_time_seconds_with_override_returns_override() {
        let mut overrides = HashMap::new();
        overrides.insert(TableMigrationStatus::Deployed, 999);
        let bake = TableMigrationStatus::Deployed.get_bake_time_seconds(&overrides);
        assert_eq!(bake, 999);
    }

    #[test]
    fn all_status_values_exist() {
        assert_eq!(
            TableMigrationStatus::Unknown.name(),
            "TABLE_MIGRATION_STATUS_UNKNOWN"
        );
        assert_eq!(
            TableMigrationStatus::Init.name(),
            "TABLE_MIGRATION_STATUS_INIT"
        );
        assert_eq!(
            TableMigrationStatus::Deployed.name(),
            "TABLE_MIGRATION_STATUS_DEPLOYED"
        );
        assert_eq!(
            TableMigrationStatus::Pending.name(),
            "TABLE_MIGRATION_STATUS_PENDING"
        );
        assert_eq!(
            TableMigrationStatus::Complete.name(),
            "TABLE_MIGRATION_STATUS_COMPLETE"
        );
    }

    #[test]
    fn name_round_trips() {
        for v in [
            TableMigrationStatus::Unknown,
            TableMigrationStatus::Init,
            TableMigrationStatus::Deployed,
            TableMigrationStatus::Pending,
            TableMigrationStatus::Complete,
        ] {
            assert_eq!(TableMigrationStatus::from_name(v.name()), Some(v));
        }
    }
}
