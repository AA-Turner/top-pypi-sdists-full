//! Port of `software.amazon.kinesis.coordinator.migration.TableMigrationSummary`.

use bon::Builder;

/// Immutable value object summarizing fleet-wide worker/lease/metrics counts,
/// computed once per LAM run and pushed to the table-migration state machine.
///
/// Java `@Value @Builder @ToString`. All fields default to 0 in the builder.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Builder)]
pub struct TableMigrationSummary {
    /// Total active workers with worker-metric stats (merged/deduplicated).
    #[builder(default)]
    pub total_active_workers_with_metrics: i32,
    /// Active workers with metrics in the legacy table (0 once complete).
    #[builder(default)]
    pub active_workers_with_metrics_in_legacy_table: i32,
    /// Active workers with metrics in the lease table.
    #[builder(default)]
    pub active_workers_with_metrics_in_lease_table: i32,
    /// Distinct workers owning at least one unexpired lease.
    #[builder(default)]
    pub workers_with_unexpired_leases: i32,
    /// Total distinct workers owning at least one lease (any expiry).
    #[builder(default)]
    pub total_workers_with_leases: i32,
    /// Lease owners emitting active worker metrics (in either table).
    #[builder(default)]
    pub lease_owners_with_active_metrics: i32,
    /// Fleet-wide minimum support code across all lease-owning workers.
    ///
    /// Sentinel semantics (preserved exactly, not collapsed into `Option`):
    /// - `-1` means "no lease owners to evaluate".
    /// - `0` means "at least one lease owner lacks support or has an expired
    ///   support-code heartbeat".
    /// - positive = actual minimum support-code ordinal.
    #[builder(default)]
    pub min_support_code: i32,
}

impl TableMigrationSummary {
    pub fn total_active_workers_with_metrics(&self) -> i32 {
        self.total_active_workers_with_metrics
    }
    pub fn active_workers_with_metrics_in_legacy_table(&self) -> i32 {
        self.active_workers_with_metrics_in_legacy_table
    }
    pub fn active_workers_with_metrics_in_lease_table(&self) -> i32 {
        self.active_workers_with_metrics_in_lease_table
    }
    pub fn workers_with_unexpired_leases(&self) -> i32 {
        self.workers_with_unexpired_leases
    }
    pub fn total_workers_with_leases(&self) -> i32 {
        self.total_workers_with_leases
    }
    pub fn lease_owners_with_active_metrics(&self) -> i32 {
        self.lease_owners_with_active_metrics
    }
    pub fn min_support_code(&self) -> i32 {
        self.min_support_code
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builder_all_fields_creates_correct_summary() {
        let summary = TableMigrationSummary::builder()
            .total_active_workers_with_metrics(5)
            .active_workers_with_metrics_in_legacy_table(2)
            .active_workers_with_metrics_in_lease_table(3)
            .workers_with_unexpired_leases(4)
            .total_workers_with_leases(6)
            .lease_owners_with_active_metrics(4)
            .min_support_code(2)
            .build();

        assert_eq!(summary.total_active_workers_with_metrics(), 5);
        assert_eq!(summary.active_workers_with_metrics_in_legacy_table(), 2);
        assert_eq!(summary.active_workers_with_metrics_in_lease_table(), 3);
        assert_eq!(summary.workers_with_unexpired_leases(), 4);
        assert_eq!(summary.total_workers_with_leases(), 6);
        assert_eq!(summary.lease_owners_with_active_metrics(), 4);
        assert_eq!(summary.min_support_code(), 2);
    }

    #[test]
    fn builder_defaults_zero_values() {
        let summary = TableMigrationSummary::builder().build();
        assert_eq!(summary.total_active_workers_with_metrics(), 0);
        assert_eq!(summary.active_workers_with_metrics_in_legacy_table(), 0);
        assert_eq!(summary.active_workers_with_metrics_in_lease_table(), 0);
        assert_eq!(summary.workers_with_unexpired_leases(), 0);
        assert_eq!(summary.total_workers_with_leases(), 0);
        assert_eq!(summary.lease_owners_with_active_metrics(), 0);
        assert_eq!(summary.min_support_code(), 0);
    }

    #[test]
    fn builder_migration_complete_legacy_is_zero() {
        let summary = TableMigrationSummary::builder()
            .total_active_workers_with_metrics(3)
            .active_workers_with_metrics_in_legacy_table(0)
            .active_workers_with_metrics_in_lease_table(3)
            .workers_with_unexpired_leases(3)
            .min_support_code(3)
            .build();
        assert_eq!(summary.active_workers_with_metrics_in_legacy_table(), 0);
        assert_eq!(summary.active_workers_with_metrics_in_lease_table(), 3);
        assert_eq!(
            summary.total_active_workers_with_metrics(),
            summary.active_workers_with_metrics_in_lease_table()
        );
    }

    #[test]
    fn builder_no_lease_owners_min_support_code_negative_one() {
        let summary = TableMigrationSummary::builder()
            .total_active_workers_with_metrics(2)
            .active_workers_with_metrics_in_legacy_table(1)
            .active_workers_with_metrics_in_lease_table(1)
            .workers_with_unexpired_leases(0)
            .min_support_code(-1)
            .build();
        assert_eq!(summary.min_support_code(), -1);
        assert_eq!(summary.workers_with_unexpired_leases(), 0);
    }

    #[test]
    fn builder_worker_without_support_code_min_support_code_zero() {
        let summary = TableMigrationSummary::builder()
            .total_active_workers_with_metrics(3)
            .active_workers_with_metrics_in_legacy_table(1)
            .active_workers_with_metrics_in_lease_table(2)
            .workers_with_unexpired_leases(3)
            .min_support_code(0)
            .build();
        assert_eq!(summary.min_support_code(), 0);
    }

    #[test]
    fn debug_contains_all_fields() {
        let summary = TableMigrationSummary::builder()
            .total_active_workers_with_metrics(5)
            .active_workers_with_metrics_in_legacy_table(2)
            .active_workers_with_metrics_in_lease_table(3)
            .workers_with_unexpired_leases(4)
            .min_support_code(2)
            .build();
        let s = format!("{summary:?}");
        assert!(s.contains('5'));
        assert!(s.contains('2'));
        assert!(s.contains('3'));
        assert!(s.contains('4'));
    }
}
