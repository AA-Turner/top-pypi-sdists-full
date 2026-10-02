//! Port of `software.amazon.kinesis.common.DdbTableConfig`.

use aws_sdk_dynamodb::types::{BillingMode, Tag};

/// Configuration of a DynamoDB table created by KCL for its internal operations
/// (leases, coordinator state, etc.): name, billing mode, provisioned capacity,
/// point-in-time recovery, deletion protection, and tags.
///
/// Port of the Lombok `@Data @Accessors(fluent = true) @NoArgsConstructor` class.
/// All fields are settable via chainable fluent setters (matching Lombok's
/// fluent setters returning the mutated instance).
///
/// # Equality
///
/// Java `@Data` derives `equals`/`hashCode` over all fields. `BillingMode` and
/// `Tag` from the AWS SDK implement `PartialEq`, so `#[derive(PartialEq)]`
/// works. `Eq`/`Hash` are **not** derived: the SDK types do not implement them.
#[derive(Debug, Clone, PartialEq)]
pub struct DdbTableConfig {
    /// Name to use for the DDB table. If `None`, defaults to
    /// `applicationName-tableSuffix`. If multiple KCL applications run in the
    /// same account, a unique table name must be provided.
    table_name: Option<String>,

    /// Billing mode used to create the DDB table (default `PAY_PER_REQUEST`).
    billing_mode: BillingMode,

    /// Read capacity to provision during table creation, if billing mode is
    /// `PROVISIONED`.
    read_capacity: i64,

    /// Write capacity to provision during table creation, if billing mode is
    /// `PROVISIONED`.
    write_capacity: i64,

    /// Flag to enable Point in Time Recovery on the DDB table.
    point_in_time_recovery_enabled: bool,

    /// Flag to enable deletion protection on the DDB table.
    deletion_protection_enabled: bool,

    /// Tags to add to the DDB table.
    tags: Vec<Tag>,
}

impl Default for DdbTableConfig {
    /// Java `@NoArgsConstructor` + field initializers: `PAY_PER_REQUEST` billing
    /// mode, `false` PITR / deletion protection, empty tags, `0` capacities,
    /// no table name.
    fn default() -> Self {
        Self {
            table_name: None,
            billing_mode: BillingMode::PayPerRequest,
            read_capacity: 0,
            write_capacity: 0,
            point_in_time_recovery_enabled: false,
            deletion_protection_enabled: false,
            tags: Vec::new(),
        }
    }
}

impl DdbTableConfig {
    /// Java `@NoArgsConstructor`.
    pub fn new() -> Self {
        Self::default()
    }

    /// Java protected 2-arg constructor: derives `tableName = applicationName +
    /// "-" + tableSuffix`. Rust has no inheritance; this is a helper for
    /// per-purpose configs (e.g. a coordinator-state-table config) to derive a
    /// default table name.
    pub fn with_application_name_and_suffix(application_name: &str, table_suffix: &str) -> Self {
        Self {
            table_name: Some(format!("{}-{}", application_name, table_suffix)),
            ..Self::default()
        }
    }

    // ---- accessors (Lombok fluent @Getter) ----

    pub fn table_name(&self) -> Option<&str> {
        self.table_name.as_deref()
    }

    pub fn billing_mode(&self) -> &BillingMode {
        &self.billing_mode
    }

    pub fn read_capacity(&self) -> i64 {
        self.read_capacity
    }

    pub fn write_capacity(&self) -> i64 {
        self.write_capacity
    }

    pub fn point_in_time_recovery_enabled(&self) -> bool {
        self.point_in_time_recovery_enabled
    }

    pub fn deletion_protection_enabled(&self) -> bool {
        self.deletion_protection_enabled
    }

    pub fn tags(&self) -> &[Tag] {
        &self.tags
    }

    // ---- fluent setters (Lombok @Accessors(fluent = true)) ----

    pub fn set_table_name(mut self, table_name: impl Into<String>) -> Self {
        self.table_name = Some(table_name.into());
        self
    }

    pub fn set_billing_mode(mut self, billing_mode: BillingMode) -> Self {
        self.billing_mode = billing_mode;
        self
    }

    pub fn set_read_capacity(mut self, read_capacity: i64) -> Self {
        self.read_capacity = read_capacity;
        self
    }

    pub fn set_write_capacity(mut self, write_capacity: i64) -> Self {
        self.write_capacity = write_capacity;
        self
    }

    pub fn set_point_in_time_recovery_enabled(mut self, enabled: bool) -> Self {
        self.point_in_time_recovery_enabled = enabled;
        self
    }

    pub fn set_deletion_protection_enabled(mut self, enabled: bool) -> Self {
        self.deletion_protection_enabled = enabled;
        self
    }

    pub fn set_tags(mut self, tags: Vec<Tag>) -> Self {
        self.tags = tags;
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn defaults_match_java() {
        let c = DdbTableConfig::new();
        assert_eq!(c.table_name(), None);
        assert_eq!(c.billing_mode(), &BillingMode::PayPerRequest);
        assert_eq!(c.read_capacity(), 0);
        assert_eq!(c.write_capacity(), 0);
        assert!(!c.point_in_time_recovery_enabled());
        assert!(!c.deletion_protection_enabled());
        assert!(c.tags().is_empty());
    }

    #[test]
    fn derives_table_name_from_application_and_suffix() {
        let c = DdbTableConfig::with_application_name_and_suffix("MyApp", "CoordinatorState");
        assert_eq!(c.table_name(), Some("MyApp-CoordinatorState"));
        // Other fields keep defaults.
        assert_eq!(c.billing_mode(), &BillingMode::PayPerRequest);
    }

    #[test]
    fn fluent_setters_chain() {
        let c = DdbTableConfig::new()
            .set_table_name("t")
            .set_billing_mode(BillingMode::Provisioned)
            .set_read_capacity(5)
            .set_write_capacity(7)
            .set_point_in_time_recovery_enabled(true)
            .set_deletion_protection_enabled(true);
        assert_eq!(c.table_name(), Some("t"));
        assert_eq!(c.billing_mode(), &BillingMode::Provisioned);
        assert_eq!(c.read_capacity(), 5);
        assert_eq!(c.write_capacity(), 7);
        assert!(c.point_in_time_recovery_enabled());
        assert!(c.deletion_protection_enabled());
    }

    #[test]
    fn equality_over_all_fields() {
        let a = DdbTableConfig::new().set_read_capacity(3);
        let b = DdbTableConfig::new().set_read_capacity(3);
        let c = DdbTableConfig::new().set_read_capacity(4);
        assert_eq!(a, b);
        assert_ne!(a, c);
    }

    #[test]
    fn tags_are_stored() {
        let tag = Tag::builder().key("k").value("v").build().unwrap();
        let c = DdbTableConfig::new().set_tags(vec![tag.clone()]);
        assert_eq!(c.tags(), &[tag]);
    }
}
