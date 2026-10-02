//! Port of the `coordinator.delegate` package:
//! `CoordinatorStateDAODelegate` (abstract base) plus the two concrete
//! subclasses `LeaseTableCoordinatorStateDAODelegate` and
//! `LegacyTableCoordinatorStateDAODelegate`.
//!
//! # Deviations
//!
//! - **Async DDB.** Java blocks on `DynamoDbAsyncClient` futures via
//!   `FutureUtils.unwrappingFuture`; the Rust port stays async and `.await`s the
//!   real `aws_sdk_dynamodb::Client`. Checked exceptions collapse into
//!   [`LeasingError`] (`Dependency`/`InvalidState`/`ProvisionedThroughput`), the
//!   same enum the leases subsystem uses.
//! - **No inheritance.** The abstract base + two subclasses fold into one
//!   [`CoordinatorStateDaoDelegate`] struct discriminated by [`DelegateKind`].
//!   The legacy delegate's `enabled` gate (set by `initialize()`'s
//!   `DescribeTable` probe) is an `AtomicBool`; the lease-table delegate's
//!   `initialize()` is a no-op and it is always enabled.
//! - **Deserializer registry → match.** Java keeps a `Map<entityType, deserializer>`.
//!   Rust dispatches with a match in [`from_dynamo_record`]. Migration subtypes
//!   (wave 10b) are not yet typed, so their records deserialize into the generic
//!   [`CoordinatorState::Generic`] fallback (as does the leader lock).
//! - **`DynamoDbAsyncToSyncClientAdapter` / DDB lock-client options** are NOT
//!   ported (all-async model + the lock client is a wave-10c concern). See
//!   the coordinator module docs. // TODO(port): wave 10c lock client.

use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};

use aws_sdk_dynamodb::types::{
    AttributeValue, Delete, ExpectedAttributeValue, Put, TransactWriteItem,
};
use aws_sdk_dynamodb::Client;

use crate::coordinator::coordinator_state::{CoordinatorState, ENTITY_TYPE_ATTRIBUTE_NAME};
use crate::coordinator::migration::migration_state::{MigrationState, MIGRATION_HASH_KEY};
use crate::coordinator::migration::table_migration_state::{
    TableMigrationState, TABLE_MIGRATION_HASH_KEY,
};
use crate::coordinator::stream_info::StreamInfo;
use crate::leases::dynamo_utils;
use crate::leases::exceptions::LeasingError;
use crate::leases::{CoordinatorStateType, EntityType};

const DDB_ENTITY_TYPE_PLACEHOLDER: &str = ":entityType";

/// Which backing table this delegate targets.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DelegateKind {
    /// The single (lease) table — always available, `initialize()` is a no-op.
    LeaseTable,
    /// The legacy standalone CoordinatorState table — `initialize()` probes
    /// existence and disables reads/writes if absent.
    LegacyTable,
}

/// DAO delegate abstracting `CoordinatorState` access from the DDB table it is
/// stored in. See the module docs for how it folds the Java class hierarchy.
pub struct CoordinatorStateDaoDelegate {
    client: Client,
    table_name: String,
    partition_key_attribute_name: String,
    kind: DelegateKind,
    /// Legacy: set by `initialize()`. Lease table: always `true`.
    enabled: AtomicBool,
}

impl CoordinatorStateDaoDelegate {
    /// Lease-table delegate. Java `LeaseTableCoordinatorStateDAODelegate`
    /// (partition key = `DynamoDBLeaseSerializer.LEASE_KEY_KEY`).
    pub fn lease_table(client: Client, lease_table_name: impl Into<String>) -> Self {
        Self {
            client,
            table_name: lease_table_name.into(),
            partition_key_attribute_name: crate::leases::dynamodb::LEASE_KEY_KEY.to_string(),
            kind: DelegateKind::LeaseTable,
            enabled: AtomicBool::new(true),
        }
    }

    /// Legacy-table delegate. Java `LegacyTableCoordinatorStateDAODelegate`
    /// (partition key = `"key"`). Starts enabled; `initialize()` may disable it.
    pub fn legacy_table(client: Client, table_name: impl Into<String>) -> Self {
        Self {
            client,
            table_name: table_name.into(),
            partition_key_attribute_name: LEGACY_COORDINATOR_STATE_HASH_KEY.to_string(),
            kind: DelegateKind::LegacyTable,
            enabled: AtomicBool::new(true),
        }
    }

    pub fn table_name(&self) -> &str {
        &self.table_name
    }

    pub fn partition_key_attribute_name(&self) -> &str {
        &self.partition_key_attribute_name
    }

    pub fn kind(&self) -> DelegateKind {
        self.kind
    }

    /// Java `isEnabled()` (legacy delegate). The lease table is always enabled.
    pub fn is_enabled(&self) -> bool {
        self.enabled.load(Ordering::SeqCst)
    }

    /// Java `initialize()`. Lease table: no-op. Legacy table: `DescribeTable`;
    /// on `ResourceNotFoundException` disable the delegate; any other error →
    /// [`LeasingError::Dependency`].
    pub async fn initialize(&self) -> Result<(), LeasingError> {
        match self.kind {
            DelegateKind::LeaseTable => Ok(()),
            DelegateKind::LegacyTable => {
                let fut = self
                    .client
                    .describe_table()
                    .table_name(&self.table_name)
                    .send();
                match fut.await {
                    Ok(_) => {
                        tracing::info!(table = %self.table_name, "Legacy coordinator state table exists, delegate enabled");
                        self.enabled.store(true, Ordering::SeqCst);
                        Ok(())
                    }
                    Err(sdk_err) => {
                        let e = sdk_err.into_service_error();
                        if e.is_resource_not_found_exception() {
                            tracing::info!(table = %self.table_name, "Legacy coordinator state table does not exist, delegate not enabled");
                            self.enabled.store(false, Ordering::SeqCst);
                            Ok(())
                        } else {
                            Err(LeasingError::dependency_caused_by(
                                format!(
                                    "Unable to determine if legacy table {} exists",
                                    self.table_name
                                ),
                                Box::new(e),
                            ))
                        }
                    }
                }
            }
        }
    }

    // ==================== Read Operations ====================

    /// Java `listCoordinatorState()`. Legacy delegate returns an empty list when
    /// disabled.
    pub async fn list_coordinator_state(&self) -> Result<Vec<CoordinatorState>, LeasingError> {
        if !self.is_enabled() {
            return Ok(Vec::new());
        }
        let mut states = Vec::new();
        let mut start_key: Option<HashMap<String, AttributeValue>> = None;
        loop {
            let mut builder = self
                .client
                .scan()
                .table_name(&self.table_name)
                .consistent_read(true);
            if let Some(k) = &start_key {
                builder = builder.set_exclusive_start_key(Some(k.clone()));
            }
            let response = self.send_scan(builder, "list coordinatorState").await?;
            for item in response.items() {
                states.push(self.from_dynamo_record(item));
            }
            match response.last_evaluated_key() {
                Some(k) if !k.is_empty() => start_key = Some(k.clone()),
                _ => break,
            }
        }
        Ok(states)
    }

    /// Java `listCoordinatorStateByEntityType(...)`. Legacy delegate returns an
    /// empty list when disabled.
    pub async fn list_coordinator_state_by_entity_type(
        &self,
        entity_type: CoordinatorStateType,
    ) -> Result<Vec<CoordinatorState>, LeasingError> {
        if !self.is_enabled() {
            return Ok(Vec::new());
        }
        let mut states = Vec::new();
        let mut start_key: Option<HashMap<String, AttributeValue>> = None;
        let filter = format!(
            "{} = {}",
            ENTITY_TYPE_ATTRIBUTE_NAME, DDB_ENTITY_TYPE_PLACEHOLDER
        );
        loop {
            let mut builder = self
                .client
                .scan()
                .table_name(&self.table_name)
                .filter_expression(&filter)
                .expression_attribute_values(
                    DDB_ENTITY_TYPE_PLACEHOLDER,
                    AttributeValue::S(entity_type.ddb_value().to_string()),
                );
            if let Some(k) = &start_key {
                builder = builder.set_exclusive_start_key(Some(k.clone()));
            }
            let response = self.send_scan(builder, "list coordinatorState").await?;
            for item in response.items() {
                states.push(self.from_dynamo_record(item));
            }
            match response.last_evaluated_key() {
                Some(k) if !k.is_empty() => start_key = Some(k.clone()),
                _ => break,
            }
        }
        Ok(states)
    }

    /// Java `getCoordinatorState(String key)`. Legacy delegate returns `None`
    /// when disabled.
    pub async fn get_coordinator_state(
        &self,
        key: &str,
    ) -> Result<Option<CoordinatorState>, LeasingError> {
        if !self.is_enabled() {
            return Ok(None);
        }
        let fut = self
            .client
            .get_item()
            .table_name(&self.table_name)
            .set_key(Some(self.coordinator_state_key(key)))
            .consistent_read(true)
            .send();
        match fut.await {
            Ok(resp) => {
                let item = resp.item();
                match item {
                    Some(rec) if !rec.is_empty() => Ok(Some(self.from_dynamo_record(rec))),
                    _ => Ok(None),
                }
            }
            Err(sdk_err) => Err(self.convert_error("get", key, sdk_err.into_service_error())),
        }
    }

    // ==================== Write Operations ====================

    /// Java `createCoordinatorStateIfNotExists(...)`. Legacy delegate throws
    /// [`LeasingError::InvalidState`] when disabled.
    pub async fn create_coordinator_state_if_not_exists(
        &self,
        state: &CoordinatorState,
    ) -> Result<bool, LeasingError> {
        if !self.is_enabled() {
            return Err(LeasingError::invalid_state(
                "Legacy table does not exist, cannot create coordinator state",
            ));
        }
        let fut = self
            .client
            .put_item()
            .table_name(&self.table_name)
            .set_item(Some(self.to_dynamo_record(state)))
            .set_expected(Some(self.non_existent_expectation()))
            .send();
        match fut.await {
            Ok(_) => Ok(true),
            Err(sdk_err) => {
                let e = sdk_err.into_service_error();
                if e.is_conditional_check_failed_exception() {
                    tracing::info!("Not creating coordinator state because the key already exists");
                    Ok(false)
                } else {
                    Err(self.convert_error("create", state.key().unwrap_or(""), e))
                }
            }
        }
    }

    /// Java `updateCoordinatorStateWithExpectation(...)`. Legacy delegate throws
    /// [`LeasingError::InvalidState`] when disabled.
    pub async fn update_coordinator_state_with_expectation(
        &self,
        state: &CoordinatorState,
        expectations: HashMap<String, ExpectedAttributeValue>,
    ) -> Result<bool, LeasingError> {
        if !self.is_enabled() {
            return Err(LeasingError::invalid_state(
                "Legacy table does not exist, cannot update coordinator state",
            ));
        }
        let key = state.key().unwrap_or("");
        let mut expectation_map = self.existent_expectation(key);
        expectation_map.extend(expectations);
        let fut = self
            .client
            .update_item()
            .table_name(&self.table_name)
            .set_key(Some(self.coordinator_state_key(key)))
            .set_expected(Some(expectation_map))
            .set_attribute_updates(Some(state.get_dynamo_update()))
            .send();
        match fut.await {
            Ok(_) => Ok(true),
            Err(sdk_err) => {
                let e = sdk_err.into_service_error();
                if e.is_conditional_check_failed_exception() {
                    tracing::debug!(
                        "CoordinatorState update failed because conditions were not met"
                    );
                    Ok(false)
                } else {
                    Err(self.convert_error("update", key, e))
                }
            }
        }
    }

    /// Java `deleteCoordinatorState(String key)`. Legacy delegate throws
    /// [`LeasingError::InvalidState`] when disabled.
    pub async fn delete_coordinator_state(&self, key: &str) -> Result<bool, LeasingError> {
        if !self.is_enabled() {
            return Err(LeasingError::invalid_state(
                "Legacy table does not exist, cannot delete coordinator state",
            ));
        }
        let fut = self
            .client
            .delete_item()
            .table_name(&self.table_name)
            .set_key(Some(self.coordinator_state_key(key)))
            .send();
        match fut.await {
            Ok(_) => Ok(true),
            Err(sdk_err) => Err(self.convert_error("delete", key, sdk_err.into_service_error())),
        }
    }

    // ==================== Transactional Helpers ====================

    /// Java `createTransactPut(...)` — conditional Put (item must not exist).
    pub fn create_transact_put(&self, state: &CoordinatorState) -> TransactWriteItem {
        let put = Put::builder()
            .table_name(&self.table_name)
            .set_item(Some(self.to_dynamo_record(state)))
            .condition_expression(format!(
                "attribute_not_exists({})",
                self.partition_key_attribute_name
            ))
            .build()
            .expect("valid Put");
        TransactWriteItem::builder().put(put).build()
    }

    /// Java `createTransactDelete(String key)`.
    pub fn create_transact_delete(&self, key: &str) -> TransactWriteItem {
        let delete = Delete::builder()
            .table_name(&self.table_name)
            .set_key(Some(self.coordinator_state_key(key)))
            .build()
            .expect("valid Delete");
        TransactWriteItem::builder().delete(delete).build()
    }

    /// Java `toTransactRecord(...)` — public wrapper over `toDynamoRecord`.
    pub fn to_transact_record(&self, state: &CoordinatorState) -> HashMap<String, AttributeValue> {
        self.to_dynamo_record(state)
    }

    // ==================== (de)serialization ====================

    /// Java `fromDynamoRecord(...)`. Strips the partition key, resolves the
    /// entity type, and dispatches to the right typed deserializer, falling back
    /// to a generic [`CoordinatorState::Generic`] (matching Java's behavior for
    /// the leader lock and unknown/untyped records).
    pub fn from_dynamo_record(
        &self,
        dynamo_record: &HashMap<String, AttributeValue>,
    ) -> CoordinatorState {
        let mut attributes = dynamo_record.clone();
        let key_value = attributes
            .remove(&self.partition_key_attribute_name)
            .and_then(|v| v.as_s().ok().cloned())
            .unwrap_or_default();

        // resolveEntityType: read+remove the entityType attribute; infer for
        // legacy records missing it.
        let entity_type = resolve_entity_type(&key_value, &mut attributes);

        match entity_type {
            Some(EntityType::StreamInfo) => {
                if let Some(stream_info) = StreamInfo::deserialize(&key_value, Some(&attributes)) {
                    return CoordinatorState::StreamInfo(stream_info);
                }
            }
            Some(EntityType::ClientVersionMigration) => {
                if let Some(m) = MigrationState::deserialize(&key_value, &attributes) {
                    return CoordinatorState::MigrationState(m);
                }
            }
            Some(EntityType::TableMigration) => {
                if let Some(t) = TableMigrationState::deserialize(&key_value, &attributes) {
                    return CoordinatorState::TableMigrationState(t);
                }
            }
            _ => {}
        }
        // The leader lock and any unknown/undeserializable records become the
        // generic fallback. The generic record keeps the resolved
        // coordinator-state type when known (mirrors Java preserving entityType).
        let coordinator_state_entity_type = entity_type.and_then(coordinator_state_type_of);
        CoordinatorState::generic(
            Some(key_value),
            coordinator_state_entity_type,
            Some(attributes),
        )
    }

    fn to_dynamo_record(&self, state: &CoordinatorState) -> HashMap<String, AttributeValue> {
        let mut result = HashMap::new();
        result.insert(
            self.partition_key_attribute_name.clone(),
            dynamo_utils::create_attribute_value_string(state.key().unwrap_or("")),
        );
        for (k, v) in state.serialize() {
            result.insert(k, v);
        }
        result
    }

    fn coordinator_state_key(&self, key: &str) -> HashMap<String, AttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            self.partition_key_attribute_name.clone(),
            dynamo_utils::create_attribute_value_string(key),
        );
        m
    }

    fn non_existent_expectation(&self) -> HashMap<String, ExpectedAttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            self.partition_key_attribute_name.clone(),
            ExpectedAttributeValue::builder().exists(false).build(),
        );
        m
    }

    fn existent_expectation(&self, key: &str) -> HashMap<String, ExpectedAttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            self.partition_key_attribute_name.clone(),
            ExpectedAttributeValue::builder()
                .value(AttributeValue::S(key.to_string()))
                .build(),
        );
        m
    }

    // ==================== error helpers ====================

    async fn send_scan(
        &self,
        builder: aws_sdk_dynamodb::operation::scan::builders::ScanFluentBuilder,
        op: &str,
    ) -> Result<aws_sdk_dynamodb::operation::scan::ScanOutput, LeasingError> {
        match builder.send().await {
            Ok(resp) => Ok(resp),
            Err(sdk_err) => Err(self.convert_scan_error(op, sdk_err.into_service_error())),
        }
    }

    fn convert_scan_error(
        &self,
        op: &str,
        e: aws_sdk_dynamodb::operation::scan::ScanError,
    ) -> LeasingError {
        if e.is_provisioned_throughput_exceeded_exception() {
            tracing::warn!(table = %self.table_name, "Provisioned throughput exceeded; consider increasing IOPs");
            LeasingError::provisioned_throughput_caused_by(op.to_string(), Box::new(e))
        } else if e.is_resource_not_found_exception() {
            LeasingError::invalid_state_caused_by(
                format!(
                    "Cannot {op}, because table {} does not exist",
                    self.table_name
                ),
                Box::new(e),
            )
        } else {
            LeasingError::dependency_caused_by(op.to_string(), Box::new(e))
        }
    }

    fn convert_error<E>(&self, op: &str, key: &str, e: E) -> LeasingError
    where
        E: DdbErrorClassify + std::error::Error + Send + Sync + 'static,
    {
        if e.is_provisioned_throughput_exceeded() {
            tracing::warn!(table = %self.table_name, "Provisioned throughput exceeded; consider increasing IOPs");
            LeasingError::provisioned_throughput_caused_by(
                format!("{op} coordinatorState"),
                Box::new(e),
            )
        } else if e.is_resource_not_found() {
            LeasingError::invalid_state_caused_by(
                format!(
                    "Cannot {op} coordinatorState for key {key}, because table {} does not exist",
                    self.table_name
                ),
                Box::new(e),
            )
        } else {
            LeasingError::dependency_caused_by(format!("{op} coordinatorState"), Box::new(e))
        }
    }
}

/// Legacy CoordinatorState table partition key. Java
/// `LegacyTableCoordinatorStateDAODelegate.COORDINATOR_STATE_TABLE_HASH_KEY_ATTRIBUTE_NAME`.
pub const LEGACY_COORDINATOR_STATE_HASH_KEY: &str = "key";

/// resolveEntityType: read + remove the `entityType` attribute; if absent, infer
/// from well-known partition-key values for legacy records.
fn resolve_entity_type(
    key: &str,
    attributes: &mut HashMap<String, AttributeValue>,
) -> Option<EntityType> {
    if let Some(av) = attributes.remove(ENTITY_TYPE_ATTRIBUTE_NAME) {
        if let Ok(s) = av.as_s() {
            if let Some(resolved) = EntityType::from_ddb_value(s) {
                return Some(resolved);
            }
        }
    }
    if key == MIGRATION_HASH_KEY {
        return Some(EntityType::ClientVersionMigration);
    }
    if key == TABLE_MIGRATION_HASH_KEY {
        return Some(EntityType::TableMigration);
    }
    None
}

fn coordinator_state_type_of(entity_type: EntityType) -> Option<CoordinatorStateType> {
    match entity_type {
        EntityType::StreamInfo => Some(CoordinatorStateType::StreamInfo),
        EntityType::LeaderLock => Some(CoordinatorStateType::LeaderLock),
        EntityType::ClientVersionMigration => Some(CoordinatorStateType::ClientVersionMigration),
        EntityType::TableMigration => Some(CoordinatorStateType::TableMigration),
        EntityType::Lease | EntityType::WorkerMetricStats => None,
    }
}

/// Small classification trait so `convert_error` works uniformly across the
/// several DDB operation error enums.
trait DdbErrorClassify {
    fn is_provisioned_throughput_exceeded(&self) -> bool;
    fn is_resource_not_found(&self) -> bool;
}

macro_rules! impl_ddb_error_classify {
    ($ty:ty) => {
        impl DdbErrorClassify for $ty {
            fn is_provisioned_throughput_exceeded(&self) -> bool {
                self.is_provisioned_throughput_exceeded_exception()
            }
            fn is_resource_not_found(&self) -> bool {
                self.is_resource_not_found_exception()
            }
        }
    };
}

impl_ddb_error_classify!(aws_sdk_dynamodb::operation::get_item::GetItemError);
impl_ddb_error_classify!(aws_sdk_dynamodb::operation::put_item::PutItemError);
impl_ddb_error_classify!(aws_sdk_dynamodb::operation::update_item::UpdateItemError);
impl_ddb_error_classify!(aws_sdk_dynamodb::operation::delete_item::DeleteItemError);
