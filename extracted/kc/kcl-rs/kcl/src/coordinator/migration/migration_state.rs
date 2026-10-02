//! Port of `software.amazon.kinesis.coordinator.migration.MigrationState`.
//!
//! Data model / DynamoDB item representing global client-version migration
//! progress. In Java this `extends CoordinatorState`; here it is a standalone
//! struct wrapped by the [`CoordinatorState::MigrationState`] enum variant
//! (see [`crate::coordinator::coordinator_state`]).

use std::collections::HashMap;

use aws_sdk_dynamodb::types::{
    AttributeAction, AttributeValue, AttributeValueUpdate, ExpectedAttributeValue,
};

use crate::coordinator::migration::client_version::ClientVersion;
use crate::leases::{CoordinatorStateType, EntityType};

/// Java `MigrationState.MIGRATION_HASH_KEY`.
pub const MIGRATION_HASH_KEY: &str = "Migration3.0";
/// Java `MigrationState.CLIENT_VERSION_ATTRIBUTE_NAME`.
pub const CLIENT_VERSION_ATTRIBUTE_NAME: &str = "cv";
/// Java `MigrationState.MODIFIED_BY_ATTRIBUTE_NAME`.
pub const MODIFIED_BY_ATTRIBUTE_NAME: &str = "mb";
/// Java `MigrationState.MODIFIED_TIMESTAMP_ATTRIBUTE_NAME`.
pub const MODIFIED_TIMESTAMP_ATTRIBUTE_NAME: &str = "mts";
/// Java `MigrationState.HISTORY_ATTRIBUTE_NAME`.
pub const HISTORY_ATTRIBUTE_NAME: &str = "h";

const MAX_HISTORY_ENTRIES: usize = 10;

/// A bounded history entry (Java nested `MigrationState.HistoryEntry`).
#[derive(Debug, Clone, PartialEq)]
pub struct HistoryEntry {
    pub last_client_version: ClientVersion,
    pub last_modified_by: String,
    pub last_modified_timestamp: i64,
}

impl HistoryEntry {
    pub fn new(
        last_client_version: ClientVersion,
        last_modified_by: impl Into<String>,
        last_modified_timestamp: i64,
    ) -> Self {
        Self {
            last_client_version,
            last_modified_by: last_modified_by.into(),
            last_modified_timestamp,
        }
    }

    /// Java `serialize()`.
    pub fn serialize(&self) -> HashMap<String, AttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            CLIENT_VERSION_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.last_client_version.name().to_string()),
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

    /// Java `toAv()`.
    pub fn to_av(&self) -> AttributeValue {
        AttributeValue::M(self.serialize())
    }

    /// Java `deserialize(Map)`. Returns `None` on any missing/malformed field.
    pub fn deserialize(map: &HashMap<String, AttributeValue>) -> Option<Self> {
        let cv = map.get(CLIENT_VERSION_ATTRIBUTE_NAME)?.as_s().ok()?;
        let client_version = ClientVersion::from_name(cv)?;
        let modified_by = map.get(MODIFIED_BY_ATTRIBUTE_NAME)?.as_s().ok()?.clone();
        let ts = map.get(MODIFIED_TIMESTAMP_ATTRIBUTE_NAME)?.as_n().ok()?;
        let modified_timestamp = ts.parse::<i64>().ok()?;
        Some(HistoryEntry::new(
            client_version,
            modified_by,
            modified_timestamp,
        ))
    }
}

/// Global (fleet-wide) client-version migration state persisted as the single
/// row keyed by [`MIGRATION_HASH_KEY`] in the CoordinatorState table.
#[derive(Debug, Clone, PartialEq)]
pub struct MigrationState {
    key: String,
    client_version: ClientVersion,
    modified_by: String,
    modified_timestamp: i64,
    history: Vec<HistoryEntry>,
    /// Inherited generic attributes (forward-compat), Java base `attributes`.
    attributes: HashMap<String, AttributeValue>,
}

impl MigrationState {
    /// Java public `MigrationState(String modifiedBy)`: INIT state, `now`.
    pub fn new(modified_by: impl Into<String>) -> Self {
        Self::with_all(
            MIGRATION_HASH_KEY.to_string(),
            ClientVersion::ClientVersionInit,
            modified_by.into(),
            chrono::Utc::now().timestamp_millis(),
            Vec::new(),
            HashMap::new(),
        )
    }

    #[allow(clippy::too_many_arguments)]
    fn with_all(
        key: String,
        client_version: ClientVersion,
        modified_by: String,
        modified_timestamp: i64,
        history: Vec<HistoryEntry>,
        attributes: HashMap<String, AttributeValue>,
    ) -> Self {
        Self {
            key,
            client_version,
            modified_by,
            modified_timestamp,
            history,
            attributes,
        }
    }

    // ---- getters (Java @Getter) ----

    pub fn key(&self) -> &str {
        &self.key
    }
    pub fn client_version(&self) -> ClientVersion {
        self.client_version
    }
    pub fn modified_by(&self) -> &str {
        &self.modified_by
    }
    pub fn modified_timestamp(&self) -> i64 {
        self.modified_timestamp
    }
    pub fn history(&self) -> &[HistoryEntry] {
        &self.history
    }
    pub fn attributes(&self) -> &HashMap<String, AttributeValue> {
        &self.attributes
    }

    /// Java `getEntityType()` (from `CoordinatorState`).
    pub fn entity_type(&self) -> EntityType {
        EntityType::ClientVersionMigration
    }

    /// Java `getCoordinatorStateEntityType()`.
    pub fn coordinator_state_entity_type(&self) -> CoordinatorStateType {
        CoordinatorStateType::ClientVersionMigration
    }

    /// Java base `CoordinatorState.serialize()` plus this subclass's fields.
    pub fn serialize(&self) -> HashMap<String, AttributeValue> {
        let mut result: HashMap<String, AttributeValue> = HashMap::new();
        // super.serialize(): entityType + generic attributes.
        result.insert(
            crate::coordinator::coordinator_state::ENTITY_TYPE_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.coordinator_state_entity_type().ddb_value().to_string()),
        );
        for (k, v) in &self.attributes {
            result.insert(k.clone(), v.clone());
        }
        result.insert(
            CLIENT_VERSION_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(self.client_version.name().to_string()),
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

    /// Java `deserialize(key, attributes)`. `None` for a non-matching key OR any
    /// exception during parse (Java catches and returns null).
    pub fn deserialize(key: &str, attributes: &HashMap<String, AttributeValue>) -> Option<Self> {
        if key != MIGRATION_HASH_KEY {
            return None;
        }
        let mut mutable = attributes.clone();

        let cv_av = mutable.remove(CLIENT_VERSION_ATTRIBUTE_NAME)?;
        let client_version = ClientVersion::from_name(cv_av.as_s().ok()?)?;
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
                history.push(HistoryEntry::deserialize(entry.as_m().ok()?)?);
            }
        }

        let state = MigrationState::with_all(
            MIGRATION_HASH_KEY.to_string(),
            client_version,
            modified_by,
            modified_timestamp,
            history,
            mutable.clone(),
        );
        if !mutable.is_empty() {
            tracing::info!(unknown = ?mutable, "Unknown attributes for migration state");
        }
        Some(state)
    }

    /// Java `getDynamoClientVersionExpectation()`.
    pub fn get_dynamo_client_version_expectation(&self) -> HashMap<String, ExpectedAttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            CLIENT_VERSION_ATTRIBUTE_NAME.to_string(),
            ExpectedAttributeValue::builder()
                .value(AttributeValue::S(self.client_version.name().to_string()))
                .build(),
        );
        m
    }

    /// Java `copy()`.
    pub fn copy(&self) -> Self {
        MigrationState::with_all(
            self.key.clone(),
            self.client_version,
            self.modified_by.clone(),
            self.modified_timestamp,
            self.history.clone(),
            self.attributes.clone(),
        )
    }

    /// Java `update(clientVersion, modifiedBy)` — mutates in place, pushes the
    /// old value onto the (bounded) history front, bumps the timestamp.
    pub fn update(
        &mut self,
        client_version: ClientVersion,
        modified_by: impl Into<String>,
    ) -> &mut Self {
        tracing::info!(?client_version, "Migration state is being updated");
        self.add_history_entry(
            self.client_version,
            self.modified_by.clone(),
            self.modified_timestamp,
        );
        self.client_version = client_version;
        self.modified_by = modified_by.into();
        self.modified_timestamp = chrono::Utc::now().timestamp_millis();
        self
    }

    /// Java `addHistoryEntry(...)` — prepend (index 0) and trim tail past cap.
    pub fn add_history_entry(
        &mut self,
        last_client_version: ClientVersion,
        last_modified_by: impl Into<String>,
        last_modified_timestamp: i64,
    ) {
        self.history.insert(
            0,
            HistoryEntry::new(
                last_client_version,
                last_modified_by,
                last_modified_timestamp,
            ),
        );
        if self.history.len() > MAX_HISTORY_ENTRIES {
            let dropped = self.history.pop();
            tracing::info!(?dropped, "History limit reached, dropping oldest");
        }
    }

    /// Java `getDynamoUpdate()`.
    pub fn get_dynamo_update(&self) -> HashMap<String, AttributeValueUpdate> {
        let mut updates = HashMap::new();
        updates.insert(
            CLIENT_VERSION_ATTRIBUTE_NAME.to_string(),
            AttributeValueUpdate::builder()
                .value(AttributeValue::S(self.client_version.name().to_string()))
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

    #[test]
    fn get_entity_type_returns_client_version_migration() {
        let state = MigrationState::new("test-worker");
        assert_eq!(state.entity_type(), EntityType::ClientVersionMigration);
        assert_eq!(state.entity_type().ddb_value(), "CLIENT_VERSION_MIGRATION");
        assert_eq!(
            state.coordinator_state_entity_type(),
            CoordinatorStateType::ClientVersionMigration
        );
    }

    #[test]
    fn test_serialize() {
        let state = MigrationState::new("worker-1");
        let serialized = state.serialize();
        assert_eq!(
            serialized
                .get(CLIENT_VERSION_ATTRIBUTE_NAME)
                .unwrap()
                .as_s()
                .unwrap(),
            ClientVersion::ClientVersionInit.name()
        );
        assert_eq!(
            serialized
                .get(MODIFIED_BY_ATTRIBUTE_NAME)
                .unwrap()
                .as_s()
                .unwrap(),
            "worker-1"
        );
        assert!(serialized
            .get(MODIFIED_TIMESTAMP_ATTRIBUTE_NAME)
            .unwrap()
            .as_n()
            .is_ok());
        assert_eq!(
            serialized.get("entityType").unwrap().as_s().unwrap(),
            "CLIENT_VERSION_MIGRATION"
        );
    }

    #[test]
    fn deserialize_valid_key_preserves_entity_type() {
        let mut attrs = HashMap::new();
        attrs.insert(
            CLIENT_VERSION_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(ClientVersion::ClientVersionInit.name().to_string()),
        );
        attrs.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S("worker-1".to_string()),
        );
        attrs.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValue::N("1234567890".to_string()),
        );

        let d = MigrationState::deserialize(MIGRATION_HASH_KEY, &attrs).unwrap();
        assert_eq!(d.client_version(), ClientVersion::ClientVersionInit);
        assert_eq!(d.modified_by(), "worker-1");
        assert_eq!(d.modified_timestamp(), 1234567890);
        assert_eq!(d.entity_type(), EntityType::ClientVersionMigration);
    }

    #[test]
    fn deserialize_invalid_key_returns_none() {
        let mut attrs = HashMap::new();
        attrs.insert(
            CLIENT_VERSION_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(ClientVersion::ClientVersionInit.name().to_string()),
        );
        attrs.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S("worker-1".to_string()),
        );
        attrs.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValue::N("1234567890".to_string()),
        );
        assert!(MigrationState::deserialize("wrong-key", &attrs).is_none());
    }

    #[test]
    fn deserialize_then_reserialize_includes_entity_type() {
        let mut attrs = HashMap::new();
        attrs.insert(
            CLIENT_VERSION_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(ClientVersion::ClientVersion2x.name().to_string()),
        );
        attrs.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S("old-worker".to_string()),
        );
        attrs.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValue::N("1000000000".to_string()),
        );

        let d = MigrationState::deserialize(MIGRATION_HASH_KEY, &attrs).unwrap();
        assert_eq!(d.entity_type(), EntityType::ClientVersionMigration);
        let re = d.serialize();
        assert_eq!(
            re.get("entityType").unwrap().as_s().unwrap(),
            "CLIENT_VERSION_MIGRATION"
        );
    }

    #[test]
    fn update_preserves_entity_type() {
        let mut state = MigrationState::new("worker-1");
        state.update(ClientVersion::ClientVersion3x, "worker-2");
        assert_eq!(state.entity_type(), EntityType::ClientVersionMigration);
        assert_eq!(state.client_version(), ClientVersion::ClientVersion3x);
        assert_eq!(state.history().len(), 1);
    }

    #[test]
    fn get_dynamo_update_contains_expected_attributes() {
        let state = MigrationState::new("worker-1");
        let updates = state.get_dynamo_update();
        assert!(updates.contains_key(CLIENT_VERSION_ATTRIBUTE_NAME));
        assert!(updates.contains_key(MODIFIED_BY_ATTRIBUTE_NAME));
        assert!(updates.contains_key(MODIFIED_TIMESTAMP_ATTRIBUTE_NAME));
    }

    #[test]
    fn copy_preserves_entity_type() {
        let original = MigrationState::new("worker-1");
        let copy = original.copy();
        assert_eq!(original.entity_type(), copy.entity_type());
        assert_eq!(copy.entity_type(), EntityType::ClientVersionMigration);
    }

    #[test]
    fn new_migration_state_has_init_client_version() {
        let state = MigrationState::new("worker-1");
        assert_eq!(state.client_version(), ClientVersion::ClientVersionInit);
    }

    #[test]
    fn history_is_capped_at_ten() {
        let mut state = MigrationState::new("w");
        for _ in 0..15 {
            state.update(ClientVersion::ClientVersion2x, "w");
        }
        assert_eq!(state.history().len(), 10);
    }
}
