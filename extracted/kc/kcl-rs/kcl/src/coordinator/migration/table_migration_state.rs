//! Port of `software.amazon.kinesis.coordinator.migration.TableMigrationState`.
//!
//! Structurally near-identical to [`MigrationState`](super::migration_state)
//! but for the independent table-consolidation migration axis (different hash
//! key `TableMigration3.5` and attribute short-code `tm` vs `cv`).

use std::collections::HashMap;

use aws_sdk_dynamodb::types::{
    AttributeAction, AttributeValue, AttributeValueUpdate, ExpectedAttributeValue,
};

use crate::coordinator::migration::table_migration_status::TableMigrationStatus;
use crate::leases::{CoordinatorStateType, EntityType};

/// Java `TableMigrationState.TABLE_MIGRATION_HASH_KEY`.
pub const TABLE_MIGRATION_HASH_KEY: &str = "TableMigration3.5";
/// Java `TableMigrationState.TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME`.
pub const TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME: &str = "tm";
/// Java `TableMigrationState.MODIFIED_BY_ATTRIBUTE_NAME`.
pub const MODIFIED_BY_ATTRIBUTE_NAME: &str = "mb";
/// Java `TableMigrationState.MODIFIED_TIMESTAMP_ATTRIBUTE_NAME`.
pub const MODIFIED_TIMESTAMP_ATTRIBUTE_NAME: &str = "mts";
/// Java `TableMigrationState.HISTORY_ATTRIBUTE_NAME`.
pub const HISTORY_ATTRIBUTE_NAME: &str = "h";
/// Java `TableMigrationState.DEFAULT_BAKE_TIME_SECONDS` = 1 hour.
pub const DEFAULT_BAKE_TIME_SECONDS: i64 = 3600;

const MAX_HISTORY_ENTRIES: usize = 10;

/// Bounded history entry (Java nested `TableMigrationStateHistoryEntry`).
#[derive(Debug, Clone, PartialEq)]
pub struct TableMigrationStateHistoryEntry {
    pub last_table_migration_status: TableMigrationStatus,
    pub last_modified_by: String,
    pub last_modified_timestamp: i64,
}

impl TableMigrationStateHistoryEntry {
    pub fn new(
        last_table_migration_status: TableMigrationStatus,
        last_modified_by: impl Into<String>,
        last_modified_timestamp: i64,
    ) -> Self {
        Self {
            last_table_migration_status,
            last_modified_by: last_modified_by.into(),
            last_modified_timestamp,
        }
    }

    pub fn serialize(&self) -> HashMap<String, AttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.last_table_migration_status.name().to_string()),
        );
        m.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.last_modified_by.clone()),
        );
        m.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValue::N(self.last_modified_timestamp.to_string()),
        );
        m
    }

    pub fn to_av(&self) -> AttributeValue {
        AttributeValue::M(self.serialize())
    }

    pub fn deserialize(map: &HashMap<String, AttributeValue>) -> Option<Self> {
        let tm = map
            .get(TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME)?
            .as_s()
            .ok()?;
        let status = TableMigrationStatus::from_name(tm)?;
        let modified_by = map.get(MODIFIED_BY_ATTRIBUTE_NAME)?.as_s().ok()?.clone();
        let ts = map.get(MODIFIED_TIMESTAMP_ATTRIBUTE_NAME)?.as_n().ok()?;
        let modified_timestamp = ts.parse::<i64>().ok()?;
        Some(TableMigrationStateHistoryEntry::new(
            status,
            modified_by,
            modified_timestamp,
        ))
    }
}

/// Global state for the KCLv3.4 -> 3.5+ table-consolidation migration.
#[derive(Debug, Clone, PartialEq)]
pub struct TableMigrationState {
    key: String,
    table_migration_status: TableMigrationStatus,
    modified_by: String,
    modified_timestamp: i64,
    history: Vec<TableMigrationStateHistoryEntry>,
    attributes: HashMap<String, AttributeValue>,
}

impl TableMigrationState {
    /// Java public `TableMigrationState(String modifiedBy)`: INIT, `now`.
    pub fn new(modified_by: impl Into<String>) -> Self {
        Self::with_all(
            TABLE_MIGRATION_HASH_KEY.to_string(),
            TableMigrationStatus::Init,
            modified_by.into(),
            chrono::Utc::now().timestamp_millis(),
            Vec::new(),
            HashMap::new(),
        )
    }

    #[allow(clippy::too_many_arguments)]
    fn with_all(
        key: String,
        table_migration_status: TableMigrationStatus,
        modified_by: String,
        modified_timestamp: i64,
        history: Vec<TableMigrationStateHistoryEntry>,
        attributes: HashMap<String, AttributeValue>,
    ) -> Self {
        Self {
            key,
            table_migration_status,
            modified_by,
            modified_timestamp,
            history,
            attributes,
        }
    }

    pub fn key(&self) -> &str {
        &self.key
    }
    pub fn table_migration_status(&self) -> TableMigrationStatus {
        self.table_migration_status
    }
    pub fn modified_by(&self) -> &str {
        &self.modified_by
    }
    pub fn modified_timestamp(&self) -> i64 {
        self.modified_timestamp
    }
    pub fn history(&self) -> &[TableMigrationStateHistoryEntry] {
        &self.history
    }
    pub fn attributes(&self) -> &HashMap<String, AttributeValue> {
        &self.attributes
    }

    pub fn entity_type(&self) -> EntityType {
        EntityType::TableMigration
    }

    pub fn coordinator_state_entity_type(&self) -> CoordinatorStateType {
        CoordinatorStateType::TableMigration
    }

    pub fn serialize(&self) -> HashMap<String, AttributeValue> {
        let mut result: HashMap<String, AttributeValue> = HashMap::new();
        result.insert(
            crate::coordinator::coordinator_state::ENTITY_TYPE_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.coordinator_state_entity_type().ddb_value().to_string()),
        );
        for (k, v) in &self.attributes {
            result.insert(k.clone(), v.clone());
        }
        result.insert(
            TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.table_migration_status.name().to_string()),
        );
        result.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.modified_by.clone()),
        );
        result.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValue::N(self.modified_timestamp.to_string()),
        );
        if !self.history.is_empty() {
            let history_list: Vec<AttributeValue> = self
                .history
                .iter()
                .map(|e| AttributeValue::M(e.serialize()))
                .collect();
            result.insert(
                HISTORY_ATTRIBUTE_NAME.to_string(),
                AttributeValue::L(history_list),
            );
        }
        result
    }

    pub fn deserialize(key: &str, attributes: &HashMap<String, AttributeValue>) -> Option<Self> {
        if key != TABLE_MIGRATION_HASH_KEY {
            return None;
        }
        let mut mutable = attributes.clone();

        let tm_av = mutable.remove(TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME)?;
        let status = TableMigrationStatus::from_name(tm_av.as_s().ok()?)?;
        let modified_by = mutable
            .remove(MODIFIED_BY_ATTRIBUTE_NAME)?
            .as_s()
            .ok()?
            .clone();
        let modified_timestamp = mutable
            .remove(MODIFIED_TIMESTAMP_ATTRIBUTE_NAME)?
            .as_n()
            .ok()?
            .parse::<i64>()
            .ok()?;

        let mut history = Vec::new();
        if attributes.contains_key(HISTORY_ATTRIBUTE_NAME) {
            let list = mutable.remove(HISTORY_ATTRIBUTE_NAME)?;
            for entry in list.as_l().ok()? {
                history.push(TableMigrationStateHistoryEntry::deserialize(
                    entry.as_m().ok()?,
                )?);
            }
        }

        let state = TableMigrationState::with_all(
            TABLE_MIGRATION_HASH_KEY.to_string(),
            status,
            modified_by,
            modified_timestamp,
            history,
            mutable.clone(),
        );
        if !mutable.is_empty() {
            tracing::info!(unknown = ?mutable, "Unknown attributes for table migration state");
        }
        Some(state)
    }

    /// Java `getDynamoTableMigrationStatusExpectation()`.
    pub fn get_dynamo_table_migration_status_expectation(
        &self,
    ) -> HashMap<String, ExpectedAttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME.to_string(),
            ExpectedAttributeValue::builder()
                .value(AttributeValue::S(
                    self.table_migration_status.name().to_string(),
                ))
                .build(),
        );
        m
    }

    pub fn copy(&self) -> Self {
        TableMigrationState::with_all(
            self.key.clone(),
            self.table_migration_status,
            self.modified_by.clone(),
            self.modified_timestamp,
            self.history.clone(),
            self.attributes.clone(),
        )
    }

    pub fn update(
        &mut self,
        table_migration_status: TableMigrationStatus,
        modified_by: impl Into<String>,
    ) -> &mut Self {
        tracing::info!(
            ?table_migration_status,
            "Table Migration state is being updated"
        );
        self.add_table_migration_state_history_entry(
            self.table_migration_status,
            self.modified_by.clone(),
            self.modified_timestamp,
        );
        self.table_migration_status = table_migration_status;
        self.modified_by = modified_by.into();
        self.modified_timestamp = chrono::Utc::now().timestamp_millis();
        self
    }

    pub fn add_table_migration_state_history_entry(
        &mut self,
        last_status: TableMigrationStatus,
        last_modified_by: impl Into<String>,
        last_modified_timestamp: i64,
    ) {
        self.history.insert(
            0,
            TableMigrationStateHistoryEntry::new(
                last_status,
                last_modified_by,
                last_modified_timestamp,
            ),
        );
        if self.history.len() > MAX_HISTORY_ENTRIES {
            let dropped = self.history.pop();
            tracing::info!(?dropped, "History limit reached, dropping oldest");
        }
    }

    pub fn get_dynamo_update(&self) -> HashMap<String, AttributeValueUpdate> {
        let mut updates = HashMap::new();
        updates.insert(
            TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME.to_string(),
            AttributeValueUpdate::builder()
                .value(AttributeValue::S(
                    self.table_migration_status.name().to_string(),
                ))
                .action(AttributeAction::Put)
                .build(),
        );
        updates.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValueUpdate::builder()
                .value(AttributeValue::S(self.modified_by.clone()))
                .action(AttributeAction::Put)
                .build(),
        );
        updates.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValueUpdate::builder()
                .value(AttributeValue::N(self.modified_timestamp.to_string()))
                .action(AttributeAction::Put)
                .build(),
        );
        if !self.history.is_empty() {
            let list: Vec<AttributeValue> = self.history.iter().map(|e| e.to_av()).collect();
            updates.insert(
                HISTORY_ATTRIBUTE_NAME.to_string(),
                AttributeValueUpdate::builder()
                    .value(AttributeValue::L(list))
                    .action(AttributeAction::Put)
                    .build(),
            );
        }
        updates
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const WORKER_ID: &str = "test-worker";

    #[test]
    fn constructor_sets_default_state_to_init() {
        let state = TableMigrationState::new(WORKER_ID);
        assert_eq!(state.table_migration_status(), TableMigrationStatus::Init);
        assert_eq!(state.modified_by(), WORKER_ID);
        assert!(state.history().is_empty());
    }

    #[test]
    fn serialize_includes_all_fields() {
        let state = TableMigrationState::new(WORKER_ID);
        let serialized = state.serialize();
        assert!(serialized.contains_key(TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME));
        assert!(serialized.contains_key(MODIFIED_BY_ATTRIBUTE_NAME));
        assert!(serialized.contains_key(MODIFIED_TIMESTAMP_ATTRIBUTE_NAME));
        assert_eq!(
            serialized
                .get(TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME)
                .unwrap()
                .as_s()
                .unwrap(),
            TableMigrationStatus::Init.name()
        );
        assert_eq!(
            serialized
                .get(MODIFIED_BY_ATTRIBUTE_NAME)
                .unwrap()
                .as_s()
                .unwrap(),
            WORKER_ID
        );
        assert_eq!(
            serialized.get("entityType").unwrap().as_s().unwrap(),
            "TABLE_MIGRATION"
        );
    }

    #[test]
    fn deserialize_valid_attributes_round_trips() {
        let original = TableMigrationState::new(WORKER_ID);
        let mut serialized = original.serialize();
        serialized.remove("entityType"); // DAO strips entityType before deserialize
        let d = TableMigrationState::deserialize(TABLE_MIGRATION_HASH_KEY, &serialized).unwrap();
        assert_eq!(
            original.table_migration_status(),
            d.table_migration_status()
        );
        assert_eq!(original.modified_by(), d.modified_by());
        assert_eq!(original.modified_timestamp(), d.modified_timestamp());
        assert_eq!(d.entity_type(), EntityType::TableMigration);
        assert!(d.serialize().contains_key("entityType"));
    }

    #[test]
    fn deserialize_wrong_key_returns_none() {
        let mut attrs = HashMap::new();
        attrs.insert(
            TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(TableMigrationStatus::Init.name().to_string()),
        );
        attrs.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(WORKER_ID.to_string()),
        );
        attrs.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValue::N("1000".to_string()),
        );
        assert!(TableMigrationState::deserialize("wrong-key", &attrs).is_none());
    }

    #[test]
    fn deserialize_missing_required_field_returns_none() {
        let mut attrs = HashMap::new();
        attrs.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(WORKER_ID.to_string()),
        );
        attrs.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValue::N("1000".to_string()),
        );
        assert!(TableMigrationState::deserialize(TABLE_MIGRATION_HASH_KEY, &attrs).is_none());
    }

    #[test]
    fn update_changes_status_and_modified_by_adds_history() {
        let mut state = TableMigrationState::new("worker-1");
        state.update(TableMigrationStatus::Deployed, "worker-2");
        assert_eq!(
            state.table_migration_status(),
            TableMigrationStatus::Deployed
        );
        assert_eq!(state.modified_by(), "worker-2");
        assert_eq!(state.history().len(), 1);
    }

    #[test]
    fn update_multiple_transitions_preserves_history() {
        let mut state = TableMigrationState::new("worker-1");
        state.update(TableMigrationStatus::Deployed, "worker-2");
        state.update(TableMigrationStatus::Pending, "worker-3");
        state.update(TableMigrationStatus::Complete, "worker-4");
        assert_eq!(
            state.table_migration_status(),
            TableMigrationStatus::Complete
        );
        assert_eq!(state.history().len(), 3);
    }

    #[test]
    fn serialize_after_update_includes_new_state() {
        let mut state = TableMigrationState::new(WORKER_ID);
        state.update(TableMigrationStatus::Deployed, "leader-1");
        let serialized = state.serialize();
        assert_eq!(
            serialized
                .get(TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME)
                .unwrap()
                .as_s()
                .unwrap(),
            TableMigrationStatus::Deployed.name()
        );
    }

    #[test]
    fn deserialize_with_history_preserves_history_entries() {
        let mut state = TableMigrationState::new("worker-1");
        state.update(TableMigrationStatus::Deployed, "worker-2");
        state.update(TableMigrationStatus::Pending, "worker-3");
        let mut serialized = state.serialize();
        serialized.remove("entityType");
        let d = TableMigrationState::deserialize(TABLE_MIGRATION_HASH_KEY, &serialized).unwrap();
        assert_eq!(d.history().len(), 2);
        assert_eq!(d.table_migration_status(), TableMigrationStatus::Pending);
    }

    #[test]
    fn all_status_transitions_init_to_complete() {
        let mut state = TableMigrationState::new(WORKER_ID);
        assert_eq!(state.table_migration_status(), TableMigrationStatus::Init);
        state.update(TableMigrationStatus::Deployed, "leader");
        assert_eq!(
            state.table_migration_status(),
            TableMigrationStatus::Deployed
        );
        state.update(TableMigrationStatus::Pending, "leader");
        assert_eq!(
            state.table_migration_status(),
            TableMigrationStatus::Pending
        );
        state.update(TableMigrationStatus::Complete, "leader");
        assert_eq!(
            state.table_migration_status(),
            TableMigrationStatus::Complete
        );
    }

    #[test]
    fn rollback_transition_pending_to_deployed() {
        let mut state = TableMigrationState::new(WORKER_ID);
        state.update(TableMigrationStatus::Deployed, "leader");
        state.update(TableMigrationStatus::Pending, "leader");
        state.update(TableMigrationStatus::Deployed, "leader");
        assert_eq!(
            state.table_migration_status(),
            TableMigrationStatus::Deployed
        );
        assert_eq!(state.history().len(), 3);
    }
}
