//! Port of `software.amazon.kinesis.common.LeaseCleanupConfig`.

/// Configuration for lease cleanup: the three interval knobs controlling the
/// cadence of the background lease-cleanup thread.
///
/// Port of the Lombok `@Builder @Getter @Accessors(fluent = true)` value holder.
/// The Java fields are `final long`s with **no** `@Builder.Default`, so an unset
/// field defaults to Java's `0`; the [`bon::Builder`] here mirrors that by
/// defaulting each field to `0`.
///
/// The fields remain `pub` so callers can also construct this with a plain
/// struct literal (matching how the leases-management defaults are wired), and
/// fluent getters (`lease_cleanup_interval_millis()`, ...) mirror the Java
/// accessors.
#[derive(Debug, Clone, Copy, PartialEq, Eq, bon::Builder)]
pub struct LeaseCleanupConfig {
    /// Interval at which to run lease cleanup thread.
    #[builder(default = 0)]
    pub lease_cleanup_interval_millis: i64,
    /// Interval at which to check if a lease is completed or not.
    #[builder(default = 0)]
    pub completed_lease_cleanup_interval_millis: i64,
    /// Interval at which to check if a lease is garbage (i.e. trimmed past the
    /// stream's retention period) or not.
    #[builder(default = 0)]
    pub garbage_lease_cleanup_interval_millis: i64,
}

impl LeaseCleanupConfig {
    /// Fluent getter (Lombok `leaseCleanupIntervalMillis()`).
    pub fn lease_cleanup_interval_millis(&self) -> i64 {
        self.lease_cleanup_interval_millis
    }

    /// Fluent getter (Lombok `completedLeaseCleanupIntervalMillis()`).
    pub fn completed_lease_cleanup_interval_millis(&self) -> i64 {
        self.completed_lease_cleanup_interval_millis
    }

    /// Fluent getter (Lombok `garbageLeaseCleanupIntervalMillis()`).
    pub fn garbage_lease_cleanup_interval_millis(&self) -> i64 {
        self.garbage_lease_cleanup_interval_millis
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builder_sets_all_fields() {
        let c = LeaseCleanupConfig::builder()
            .lease_cleanup_interval_millis(1000)
            .completed_lease_cleanup_interval_millis(2000)
            .garbage_lease_cleanup_interval_millis(3000)
            .build();
        assert_eq!(c.lease_cleanup_interval_millis(), 1000);
        assert_eq!(c.completed_lease_cleanup_interval_millis(), 2000);
        assert_eq!(c.garbage_lease_cleanup_interval_millis(), 3000);
    }

    #[test]
    fn unset_fields_default_to_zero() {
        // Java @Builder without @Builder.Default leaves long fields at 0.
        let c = LeaseCleanupConfig::builder().build();
        assert_eq!(c.lease_cleanup_interval_millis(), 0);
        assert_eq!(c.completed_lease_cleanup_interval_millis(), 0);
        assert_eq!(c.garbage_lease_cleanup_interval_millis(), 0);
    }

    #[test]
    fn struct_literal_construction() {
        let c = LeaseCleanupConfig {
            lease_cleanup_interval_millis: 1,
            completed_lease_cleanup_interval_millis: 2,
            garbage_lease_cleanup_interval_millis: 3,
        };
        assert_eq!(c.garbage_lease_cleanup_interval_millis(), 3);
    }
}
