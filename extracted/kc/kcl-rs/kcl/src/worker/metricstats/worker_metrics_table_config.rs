//! Port of `LeaseManagementConfig.WorkerMetricsTableConfig`.
//!
//! Java: `WorkerMetricsTableConfig extends DdbTableConfig` with the table name
//! defaulting to `"{applicationName}-WorkerMetricStats"`. The port keeps a thin
//! wrapper exposing the resolved table name (the only field the DAO consumes).

/// Legacy worker-metrics table config (the table name source for the
/// [`LegacyTableWorkerMetricStatsDAODelegate`](super::delegate::LegacyTableWorkerMetricStatsDAODelegate)).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorkerMetricsTableConfig {
    table_name: Option<String>,
}

impl WorkerMetricsTableConfig {
    /// Construct from an optional application name (Java ctor takes
    /// `applicationName`; the suffix is `"WorkerMetricStats"`). `None` leaves the
    /// table name unresolved (matching Java's lazy default when no app name).
    pub fn new(application_name: Option<&str>) -> Self {
        let table_name = application_name.map(|app| format!("{}-WorkerMetricStats", app));
        Self { table_name }
    }

    /// Construct with an explicit table name.
    pub fn with_table_name(table_name: impl Into<String>) -> Self {
        Self {
            table_name: Some(table_name.into()),
        }
    }

    /// The resolved table name, if any (Java `tableName()`).
    pub fn table_name(&self) -> Option<&str> {
        self.table_name.as_deref()
    }
}
