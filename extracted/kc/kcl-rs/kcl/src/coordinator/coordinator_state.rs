//! Port of `software.amazon.kinesis.coordinator.CoordinatorState`.
//!
//! # Deviation from Java: sum type instead of subclass polymorphism
//!
//! Java has a base `CoordinatorState` class (implementing `EntityDAO.Entity`)
//! with subclasses `StreamInfo`, `MigrationState`, `TableMigrationState`, and a
//! generic fallback used for the leader-lock item. The DAO delegate keeps a
//! registry of per-`entityType` deserializers and dispatches `serialize()` /
//! `getDynamoUpdate()` via subclass overrides.
//!
//! Rust has no inheritance, so — following the arch-map's recommendation — the
//! polymorphism collapses into a single [`CoordinatorState`] enum. The
//! `StreamInfo` variant carries the fully-typed [`StreamInfo`] value; migration
//! subtypes (wave 10b) are not yet ported, so their records land in the
//! [`CoordinatorState::Generic`] variant (matching the generic-fallback path).
//! `instanceof StreamInfo` becomes a `matches!(state, CoordinatorState::StreamInfo(_))`.

use std::collections::HashMap;

use aws_sdk_dynamodb::types::{AttributeAction, AttributeValue, AttributeValueUpdate};

use crate::coordinator::migration::migration_state::MigrationState;
use crate::coordinator::migration::table_migration_state::TableMigrationState;
use crate::coordinator::stream_info::StreamInfo;
use crate::leases::{CoordinatorStateType, EntityType};

/// The DDB attribute name storing the entity type. Java
/// `CoordinatorState.ENTITY_TYPE_ATTRIBUTE_NAME`.
pub const ENTITY_TYPE_ATTRIBUTE_NAME: &str = "entityType";

/// A generic/base coordinator-state record. Mirrors Java's base
/// `CoordinatorState` (the shape used for the leader-lock item and any
/// not-yet-typed record).
///
/// The `key` is stored separately (the DAO adds/removes it based on the table's
/// partition key attribute), matching Java where `serialize()` deliberately
/// does not include the key.
#[derive(Debug, Clone, Default, PartialEq)]
pub struct GenericCoordinatorState {
    pub key: Option<String>,
    pub coordinator_state_entity_type: Option<CoordinatorStateType>,
    pub attributes: Option<HashMap<String, AttributeValue>>,
}

impl GenericCoordinatorState {
    /// Java `getEntityType()` — delegates to the parent [`EntityType`], or
    /// `None` when the coordinator-state type is unset.
    pub fn entity_type(&self) -> Option<EntityType> {
        self.coordinator_state_entity_type.map(|t| t.entity_type())
    }

    /// Java `serialize()`: writes the `entityType` attribute (if set) plus any
    /// generic attributes. The key is added by the DAO, not here.
    pub fn serialize(&self) -> HashMap<String, AttributeValue> {
        let mut result = HashMap::new();
        if let Some(t) = self.coordinator_state_entity_type {
            result.insert(
                ENTITY_TYPE_ATTRIBUTE_NAME.to_string(),
                AttributeValue::S(t.ddb_value().to_string()),
            );
        }
        if let Some(attrs) = &self.attributes {
            for (k, v) in attrs {
                result.insert(k.clone(), v.clone());
            }
        }
        result
    }

    /// Java `getDynamoUpdate()`: converts all attributes to `PUT` updates.
    pub fn get_dynamo_update(&self) -> HashMap<String, AttributeValueUpdate> {
        let mut updates = HashMap::new();
        if let Some(attrs) = &self.attributes {
            for (attribute, value) in attrs {
                updates.insert(
                    attribute.clone(),
                    AttributeValueUpdate::builder()
                        .value(value.clone())
                        .action(AttributeAction::Put)
                        .build(),
                );
            }
        }
        updates
    }
}

/// A coordinator-state record. Sum type over the known concrete subtypes plus a
/// generic fallback (see the module docs).
#[derive(Debug, Clone, PartialEq)]
pub enum CoordinatorState {
    /// A `StreamInfo` record (`entityType = STREAM`).
    StreamInfo(StreamInfo),
    /// A client-version `MigrationState` record (`entityType = CLIENT_VERSION_MIGRATION`).
    MigrationState(MigrationState),
    /// A `TableMigrationState` record (`entityType = TABLE_MIGRATION`).
    TableMigrationState(TableMigrationState),
    /// Any other record — the leader lock or an unknown/untyped record.
    Generic(GenericCoordinatorState),
}

impl CoordinatorState {
    /// Build a generic record via a builder-like helper (Java
    /// `CoordinatorState.builder()`).
    pub fn generic(
        key: Option<String>,
        coordinator_state_entity_type: Option<CoordinatorStateType>,
        attributes: Option<HashMap<String, AttributeValue>>,
    ) -> Self {
        CoordinatorState::Generic(GenericCoordinatorState {
            key,
            coordinator_state_entity_type,
            attributes,
        })
    }

    /// The record's partition key, if set.
    pub fn key(&self) -> Option<&str> {
        match self {
            CoordinatorState::StreamInfo(s) => Some(s.key()),
            CoordinatorState::MigrationState(m) => Some(m.key()),
            CoordinatorState::TableMigrationState(t) => Some(t.key()),
            CoordinatorState::Generic(g) => g.key.as_deref(),
        }
    }

    /// Java `getEntityType()`.
    pub fn entity_type(&self) -> Option<EntityType> {
        match self {
            CoordinatorState::StreamInfo(_) => Some(EntityType::StreamInfo),
            CoordinatorState::MigrationState(_) => Some(EntityType::ClientVersionMigration),
            CoordinatorState::TableMigrationState(_) => Some(EntityType::TableMigration),
            CoordinatorState::Generic(g) => g.entity_type(),
        }
    }

    /// The nested `CoordinatorStateType`, if any.
    pub fn coordinator_state_entity_type(&self) -> Option<CoordinatorStateType> {
        match self {
            CoordinatorState::StreamInfo(_) => Some(CoordinatorStateType::StreamInfo),
            CoordinatorState::MigrationState(_) => {
                Some(CoordinatorStateType::ClientVersionMigration)
            }
            CoordinatorState::TableMigrationState(_) => Some(CoordinatorStateType::TableMigration),
            CoordinatorState::Generic(g) => g.coordinator_state_entity_type,
        }
    }

    /// If this is a `MigrationState` record, borrow it (Java `instanceof` +
    /// cast). Returns `None` otherwise.
    pub fn as_migration_state(&self) -> Option<&MigrationState> {
        match self {
            CoordinatorState::MigrationState(m) => Some(m),
            _ => None,
        }
    }

    /// If this is a `TableMigrationState` record, borrow it. Returns `None`
    /// otherwise.
    pub fn as_table_migration_state(&self) -> Option<&TableMigrationState> {
        match self {
            CoordinatorState::TableMigrationState(t) => Some(t),
            _ => None,
        }
    }

    /// Java `serialize()` (polymorphic).
    pub fn serialize(&self) -> HashMap<String, AttributeValue> {
        match self {
            CoordinatorState::StreamInfo(s) => s.serialize(),
            CoordinatorState::MigrationState(m) => m.serialize(),
            CoordinatorState::TableMigrationState(t) => t.serialize(),
            CoordinatorState::Generic(g) => g.serialize(),
        }
    }

    /// Java `getDynamoUpdate()` (polymorphic).
    pub fn get_dynamo_update(&self) -> HashMap<String, AttributeValueUpdate> {
        match self {
            // StreamInfo does not override getDynamoUpdate() in Java, so it uses
            // the base behavior (which operates on the generic attributes map,
            // usually empty for StreamInfo).
            CoordinatorState::StreamInfo(s) => s.get_dynamo_update(),
            CoordinatorState::MigrationState(m) => m.get_dynamo_update(),
            CoordinatorState::TableMigrationState(t) => t.get_dynamo_update(),
            CoordinatorState::Generic(g) => g.get_dynamo_update(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn generic_get_entity_type_with_coordinator_state_type() {
        let state = CoordinatorState::generic(
            Some("k".to_string()),
            Some(CoordinatorStateType::LeaderLock),
            None,
        );
        assert_eq!(state.entity_type(), Some(EntityType::LeaderLock));
    }

    #[test]
    fn generic_get_entity_type_with_null_type_returns_none() {
        let state = CoordinatorState::generic(Some("someKey".to_string()), None, None);
        assert_eq!(state.entity_type(), None);
    }

    #[test]
    fn serialize_includes_entity_type_attribute() {
        let state = CoordinatorState::generic(
            Some("Leader".to_string()),
            Some(CoordinatorStateType::LeaderLock),
            None,
        );
        let serialized = state.serialize();
        assert!(serialized.contains_key("entityType"));
        assert_eq!(
            serialized.get("entityType").unwrap().as_s().unwrap(),
            "LEADER"
        );
    }

    #[test]
    fn serialize_includes_attributes() {
        let mut attrs = HashMap::new();
        attrs.insert(
            "customAttr".to_string(),
            AttributeValue::S("customValue".to_string()),
        );
        attrs.insert(
            "anotherAttr".to_string(),
            AttributeValue::N("42".to_string()),
        );
        let state = CoordinatorState::generic(
            Some("streamKey".to_string()),
            Some(CoordinatorStateType::StreamInfo),
            Some(attrs),
        );
        let serialized = state.serialize();
        assert_eq!(
            serialized.get("entityType").unwrap().as_s().unwrap(),
            "STREAM"
        );
        assert_eq!(
            serialized.get("customAttr").unwrap().as_s().unwrap(),
            "customValue"
        );
        assert_eq!(serialized.get("anotherAttr").unwrap().as_n().unwrap(), "42");
    }

    #[test]
    fn serialize_with_null_attributes_returns_entity_type_only() {
        let state = CoordinatorState::generic(
            Some("migKey".to_string()),
            Some(CoordinatorStateType::TableMigration),
            None,
        );
        let serialized = state.serialize();
        assert_eq!(serialized.len(), 1);
        assert_eq!(
            serialized.get("entityType").unwrap().as_s().unwrap(),
            "TABLE_MIGRATION"
        );
    }

    #[test]
    fn get_dynamo_update_converts_attributes_to_put_updates() {
        let mut attrs = HashMap::new();
        attrs.insert("field1".to_string(), AttributeValue::S("val1".to_string()));
        attrs.insert("field2".to_string(), AttributeValue::N("123".to_string()));
        let state = CoordinatorState::generic(
            Some("Leader".to_string()),
            Some(CoordinatorStateType::LeaderLock),
            Some(attrs),
        );
        let updates = state.get_dynamo_update();
        assert_eq!(updates.len(), 2);
        assert_eq!(
            updates.get("field1").unwrap().action(),
            Some(&AttributeAction::Put)
        );
        assert_eq!(
            updates
                .get("field1")
                .unwrap()
                .value()
                .unwrap()
                .as_s()
                .unwrap(),
            "val1"
        );
        assert_eq!(
            updates.get("field2").unwrap().action(),
            Some(&AttributeAction::Put)
        );
        assert_eq!(
            updates
                .get("field2")
                .unwrap()
                .value()
                .unwrap()
                .as_n()
                .unwrap(),
            "123"
        );
    }

    #[test]
    fn get_dynamo_update_with_null_attributes_returns_empty_map() {
        let state = CoordinatorState::generic(
            Some("Leader".to_string()),
            Some(CoordinatorStateType::LeaderLock),
            None,
        );
        let updates = state.get_dynamo_update();
        assert!(updates.is_empty());
    }
}
