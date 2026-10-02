//! Port of `software.amazon.kinesis.leases.EntityType`.

/// Global enum representing all entity types that can be stored in the DynamoDB
/// tables used by KCL (lease table, coordinator-state table). Each entity type
/// has a unique DDB value that is persisted as the `entityType` attribute.
///
/// **This enum is persisted in storage**, so any change to a `ddb_value` string
/// must remain backward compatible.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum EntityType {
    /// Lease entities tracking shard ownership across workers.
    Lease,
    /// Stream metadata tracking stream identifiers and their IDs.
    StreamInfo,
    /// Leader-election lock entry.
    LeaderLock,
    /// Client version migration state (KCLv2.x -> KCLv3.x).
    ClientVersionMigration,
    /// Table migration state (legacy coordinator/worker-metrics table ->
    /// lease table).
    TableMigration,
    /// Worker metric stats for resource-based lease assignment.
    WorkerMetricStats,
}

impl EntityType {
    /// The string value persisted in DynamoDB as the `entityType` attribute.
    pub fn ddb_value(&self) -> &'static str {
        match self {
            Self::Lease => "LEASE",
            Self::StreamInfo => "STREAM",
            Self::LeaderLock => "LEADER",
            Self::ClientVersionMigration => "CLIENT_VERSION_MIGRATION",
            Self::TableMigration => "TABLE_MIGRATION",
            Self::WorkerMetricStats => "WORKER_METRIC_STATS",
        }
    }

    /// Look up an [`EntityType`] by its DDB value. Returns `None` if not found
    /// (Java `fromDdbValue` returns `null`), so old/foreign data does not panic.
    pub fn from_ddb_value(ddb_value: &str) -> Option<Self> {
        [
            Self::Lease,
            Self::StreamInfo,
            Self::LeaderLock,
            Self::ClientVersionMigration,
            Self::TableMigration,
            Self::WorkerMetricStats,
        ]
        .into_iter()
        .find(|t| t.ddb_value() == ddb_value)
    }
}

/// Subset enum for entity types that are specifically coordinator-state
/// entities. Each value maps back to its parent [`EntityType`]. Port of the
/// nested Java `EntityType.CoordinatorStateType`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum CoordinatorStateType {
    StreamInfo,
    LeaderLock,
    ClientVersionMigration,
    TableMigration,
}

impl CoordinatorStateType {
    /// The parent [`EntityType`] for this coordinator-state type.
    pub fn entity_type(&self) -> EntityType {
        match self {
            Self::StreamInfo => EntityType::StreamInfo,
            Self::LeaderLock => EntityType::LeaderLock,
            Self::ClientVersionMigration => EntityType::ClientVersionMigration,
            Self::TableMigration => EntityType::TableMigration,
        }
    }

    /// The DDB value string (delegates to the parent [`EntityType`]).
    pub fn ddb_value(&self) -> &'static str {
        self.entity_type().ddb_value()
    }

    /// Look up a [`CoordinatorStateType`] by its DDB value. Returns `None` if
    /// not found.
    pub fn from_ddb_value(ddb_value: &str) -> Option<Self> {
        [
            Self::StreamInfo,
            Self::LeaderLock,
            Self::ClientVersionMigration,
            Self::TableMigration,
        ]
        .into_iter()
        .find(|t| t.ddb_value() == ddb_value)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ddb_values_are_verbatim() {
        assert_eq!(EntityType::Lease.ddb_value(), "LEASE");
        assert_eq!(EntityType::StreamInfo.ddb_value(), "STREAM");
        assert_eq!(EntityType::LeaderLock.ddb_value(), "LEADER");
        assert_eq!(
            EntityType::ClientVersionMigration.ddb_value(),
            "CLIENT_VERSION_MIGRATION"
        );
        assert_eq!(EntityType::TableMigration.ddb_value(), "TABLE_MIGRATION");
        assert_eq!(
            EntityType::WorkerMetricStats.ddb_value(),
            "WORKER_METRIC_STATS"
        );
    }

    #[test]
    fn from_ddb_value_round_trips_and_returns_none_for_unknown() {
        assert_eq!(
            EntityType::from_ddb_value("STREAM"),
            Some(EntityType::StreamInfo)
        );
        assert_eq!(EntityType::from_ddb_value("LEASE"), Some(EntityType::Lease));
        assert_eq!(EntityType::from_ddb_value("nope"), None);
    }

    #[test]
    fn coordinator_state_type_delegates() {
        assert_eq!(
            CoordinatorStateType::LeaderLock.entity_type(),
            EntityType::LeaderLock
        );
        assert_eq!(CoordinatorStateType::LeaderLock.ddb_value(), "LEADER");
        assert_eq!(
            CoordinatorStateType::from_ddb_value("STREAM"),
            Some(CoordinatorStateType::StreamInfo)
        );
        assert_eq!(CoordinatorStateType::from_ddb_value("LEASE"), None);
    }

    /// Port of `EntityTypeTest.fromDdbValue_emptyString_returnsNull`.
    #[test]
    fn from_ddb_value_empty_string_returns_none() {
        assert_eq!(EntityType::from_ddb_value(""), None);
    }

    /// Port of `EntityTypeTest.fromDdbValue_caseSensitive`.
    #[test]
    fn from_ddb_value_case_sensitive() {
        // "lease" (lowercase) should not match "LEASE"
        assert_eq!(EntityType::from_ddb_value("lease"), None);
    }

    /// Port of `EntityTypeTest.allDdbValues_areUnique`.
    #[test]
    fn all_ddb_values_are_unique() {
        use std::collections::HashSet;
        let all = [
            EntityType::Lease,
            EntityType::StreamInfo,
            EntityType::LeaderLock,
            EntityType::ClientVersionMigration,
            EntityType::TableMigration,
            EntityType::WorkerMetricStats,
        ];
        let mut ddb_values: HashSet<&'static str> = HashSet::new();
        for type_ in all {
            let added = ddb_values.insert(type_.ddb_value());
            assert!(added, "Duplicate ddbValue found: {}", type_.ddb_value());
        }
    }

    /// Port of `EntityTypeTest.coordinatorStateType_allDdbValues_areUnique`.
    #[test]
    fn coordinator_state_type_all_ddb_values_are_unique() {
        use std::collections::HashSet;
        let all = [
            CoordinatorStateType::StreamInfo,
            CoordinatorStateType::LeaderLock,
            CoordinatorStateType::ClientVersionMigration,
            CoordinatorStateType::TableMigration,
        ];
        let mut ddb_values: HashSet<&'static str> = HashSet::new();
        for cs_type in all {
            let added = ddb_values.insert(cs_type.ddb_value());
            assert!(
                added,
                "Duplicate ddbValue in CoordinatorStateType: {}",
                cs_type.ddb_value()
            );
        }
    }
}
