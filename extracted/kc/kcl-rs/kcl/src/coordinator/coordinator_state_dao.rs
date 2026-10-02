//! Port of `software.amazon.kinesis.coordinator.CoordinatorStateDAO`.
//!
//! Router over the legacy standalone CoordinatorState table and the single
//! (lease) table, dispatching CRUD based on the live [`TableMigrationStatus`].
//!
//! # Preserved routing asymmetry (exact)
//!
//! - **Reads** use a dynamic fallback+merge: when status != `Complete`, `get`
//!   tries legacy first then lease table; `list*` merges both **without
//!   deduplication**. Once status == `Complete`, reads go lease-table-only.
//! - **Writes** route on a `cached_status` snapshot captured once at
//!   `initialize()` (Complete/Pending → lease table; Init/Deployed → legacy) and
//!   do NOT re-route afterward (Java's documented best-effort behavior).
//!
//! # Deviations
//!
//! - Async over a real `aws_sdk_dynamodb::Client`; checked exceptions →
//!   [`LeasingError`].
//! - The DDB lock-client methods (`initializeLockClients`, `getDDBLockClient`,
//!   `shutdownLockClients`) are NOT ported — the `AmazonDynamoDBLockClient`
//!   dependency is a wave-10c concern (needs a Rust DDB-lock reimplementation).
//!   The `getDDBLockClientOptionsBuilder` and `DynamoDbAsyncToSyncClientAdapter`
//!   are likewise skipped. // TODO(port): wave 10c DDB lock client.

use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};

use async_trait::async_trait;
use aws_sdk_dynamodb::types::{ExpectedAttributeValue, TransactWriteItem};
use aws_sdk_dynamodb::Client;

use crate::coordinator::coordinator_config::CoordinatorStateTableConfig;
use crate::coordinator::coordinator_state::CoordinatorState;
use crate::coordinator::delegate::CoordinatorStateDaoDelegate;
use crate::coordinator::migration::table_migration_status::TableMigrationStatus;
use crate::coordinator::migration::table_migration_status_provider::TableMigrationStatusProvider;
use crate::leases::exceptions::LeasingError;
use crate::leases::CoordinatorStateType;

/// The subset of [`CoordinatorStateDao`] operations consumed by higher-level
/// DAOs (`StreamInfoDAO`, `StreamIdCacheManager`). Java code holds a concrete
/// `CoordinatorStateDAO`; this trait lets the Rust ports depend on
/// `Arc<dyn CoordinatorStateAccess>` so they can be unit-tested against a mock
/// (`#[automock]`), matching the Java tests that mock `CoordinatorStateDAO`.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait CoordinatorStateAccess: Send + Sync {
    async fn get_coordinator_state(
        &self,
        key: &str,
    ) -> Result<Option<CoordinatorState>, LeasingError>;

    async fn list_coordinator_state_by_entity_type(
        &self,
        entity_type: CoordinatorStateType,
    ) -> Result<Vec<CoordinatorState>, LeasingError>;

    async fn create_coordinator_state_if_not_exists(
        &self,
        state: &CoordinatorState,
    ) -> Result<bool, LeasingError>;

    async fn update_coordinator_state_with_expectation(
        &self,
        state: &CoordinatorState,
        expectations: HashMap<String, ExpectedAttributeValue>,
    ) -> Result<bool, LeasingError>;

    async fn delete_coordinator_state(&self, key: &str) -> Result<bool, LeasingError>;
}

/// Data Access Object routing [`CoordinatorState`] operations to the appropriate
/// DDB table based on the current [`TableMigrationStatus`]. Java
/// `CoordinatorStateDAO` (`@ThreadSafe`).
pub struct CoordinatorStateDao {
    client: Client,
    lease_table_delegate: CoordinatorStateDaoDelegate,
    legacy_table_delegate: CoordinatorStateDaoDelegate,
    table_migration_status_provider: Arc<dyn TableMigrationStatusProvider>,
    cached_status: Mutex<Option<TableMigrationStatus>>,
    initialized: AtomicBool,
}

impl CoordinatorStateDao {
    /// Java constructor
    /// `CoordinatorStateDAO(DynamoDbAsyncClient, CoordinatorStateTableConfig, leaseTableName, TableMigrationStatusProvider)`.
    pub fn new(
        client: Client,
        coordinator_state_table_config: &CoordinatorStateTableConfig,
        lease_table_name: impl Into<String>,
        table_migration_status_provider: Arc<dyn TableMigrationStatusProvider>,
    ) -> Self {
        let lease_table_delegate =
            CoordinatorStateDaoDelegate::lease_table(client.clone(), lease_table_name);
        let legacy_table_delegate = CoordinatorStateDaoDelegate::legacy_table(
            client.clone(),
            coordinator_state_table_config.table_name(),
        );
        Self {
            client,
            lease_table_delegate,
            legacy_table_delegate,
            table_migration_status_provider,
            cached_status: Mutex::new(None),
            initialized: AtomicBool::new(false),
        }
    }

    pub fn legacy_table_dao_delegate(&self) -> &CoordinatorStateDaoDelegate {
        &self.legacy_table_delegate
    }

    pub fn lease_table_dao_delegate(&self) -> &CoordinatorStateDaoDelegate {
        &self.lease_table_delegate
    }

    /// The underlying DDB client (used by the DDB lock-client reimplementation).
    pub fn client(&self) -> &Client {
        &self.client
    }

    /// Whether the DDB lock should currently route to the **lease** table
    /// (COMPLETE/PENDING) vs the **legacy** table (INIT/DEPLOYED), based on the
    /// **live** [`TableMigrationStatus`] (Java `getDDBLockClient()` routes live,
    /// switching legacy->lease when migration flips to COMPLETE mid-cycle).
    pub fn lock_routes_to_lease_table(&self) -> bool {
        matches!(
            self.table_migration_status_provider
                .get_table_migration_status(),
            TableMigrationStatus::Complete | TableMigrationStatus::Pending
        )
    }

    /// Java `initializeDelegates()`. Must run before `initialize()`.
    pub async fn initialize_delegates(&self) -> Result<(), LeasingError> {
        self.legacy_table_delegate.initialize().await?;
        self.lease_table_delegate.initialize().await?;
        tracing::info!(
            legacy_enabled = self.legacy_table_delegate.is_enabled(),
            "CoordinatorStateDAO delegates initialized"
        );
        Ok(())
    }

    /// Java `initialize()`. Enables writes; errors if the provider is still
    /// `Unknown`. Idempotent.
    pub fn initialize(&self) -> Result<(), LeasingError> {
        if self.initialized.load(Ordering::SeqCst) {
            tracing::info!("CoordinatorStateDAO already initialized");
            return Ok(());
        }
        let status = self
            .table_migration_status_provider
            .get_table_migration_status();
        if status == TableMigrationStatus::Unknown {
            return Err(LeasingError::invalid_state(
                "Cannot initialize CoordinatorStateDAO: TableMigrationStatusProvider is still UNKNOWN",
            ));
        }
        *self.cached_status.lock().expect("cached_status poisoned") = Some(status);
        self.initialized.store(true, Ordering::SeqCst);
        tracing::info!(?status, "CoordinatorStateDAO initialized for writes");
        Ok(())
    }

    // ==================== Read Operations ====================

    /// Java `getCoordinatorState(key)`.
    pub async fn get_coordinator_state(
        &self,
        key: &str,
    ) -> Result<Option<CoordinatorState>, LeasingError> {
        self.ensure_initialized()?;
        if self.is_table_migration_complete() {
            return self.lease_table_delegate.get_coordinator_state(key).await;
        }
        // Try legacy first (None if disabled), fall back to lease table.
        if let Some(legacy) = self
            .legacy_table_delegate
            .get_coordinator_state(key)
            .await?
        {
            return Ok(Some(legacy));
        }
        self.lease_table_delegate.get_coordinator_state(key).await
    }

    /// Java `listCoordinatorState()`.
    pub async fn list_coordinator_state(&self) -> Result<Vec<CoordinatorState>, LeasingError> {
        self.ensure_initialized()?;
        if self.is_table_migration_complete() {
            return self.lease_table_delegate.list_coordinator_state().await;
        }
        let mut result = self.legacy_table_delegate.list_coordinator_state().await?;
        result.extend(self.lease_table_delegate.list_coordinator_state().await?);
        Ok(result)
    }

    /// Java `listCoordinatorStateByEntityType(entityType)`.
    pub async fn list_coordinator_state_by_entity_type(
        &self,
        entity_type: CoordinatorStateType,
    ) -> Result<Vec<CoordinatorState>, LeasingError> {
        self.ensure_initialized()?;
        if self.is_table_migration_complete() {
            return self
                .lease_table_delegate
                .list_coordinator_state_by_entity_type(entity_type)
                .await;
        }
        let mut result = self
            .legacy_table_delegate
            .list_coordinator_state_by_entity_type(entity_type)
            .await?;
        result.extend(
            self.lease_table_delegate
                .list_coordinator_state_by_entity_type(entity_type)
                .await?,
        );
        Ok(result)
    }

    // ==================== Write Operations ====================

    /// Java `createCoordinatorStateIfNotExists(state)`.
    pub async fn create_coordinator_state_if_not_exists(
        &self,
        state: &CoordinatorState,
    ) -> Result<bool, LeasingError> {
        self.ensure_initialized()?;
        self.write_delegate()?
            .create_coordinator_state_if_not_exists(state)
            .await
    }

    /// Java `updateCoordinatorStateWithExpectation(state, expectations)`.
    pub async fn update_coordinator_state_with_expectation(
        &self,
        state: &CoordinatorState,
        expectations: HashMap<String, ExpectedAttributeValue>,
    ) -> Result<bool, LeasingError> {
        self.ensure_initialized()?;
        self.write_delegate()?
            .update_coordinator_state_with_expectation(state, expectations)
            .await
    }

    /// Java `deleteCoordinatorState(key)`.
    pub async fn delete_coordinator_state(&self, key: &str) -> Result<bool, LeasingError> {
        self.ensure_initialized()?;
        self.write_delegate()?.delete_coordinator_state(key).await
    }

    // ==================== Transactional Operations ====================

    /// Java `executeTransactWrite(List<TransactWriteItem>)`.
    pub async fn execute_transact_write(
        &self,
        transact_write_items: Vec<TransactWriteItem>,
    ) -> Result<(), LeasingError> {
        let fut = self
            .client
            .transact_write_items()
            .set_transact_items(Some(transact_write_items))
            .send();
        match fut.await {
            Ok(_) => Ok(()),
            Err(sdk_err) => {
                let e = sdk_err.into_service_error();
                if e.is_transaction_canceled_exception() {
                    Err(LeasingError::dependency_caused_by(
                        "TransactWriteItems cancelled",
                        Box::new(e),
                    ))
                } else {
                    Err(LeasingError::dependency_caused_by(
                        "TransactWriteItems failed",
                        Box::new(e),
                    ))
                }
            }
        }
    }

    // ==================== Private Helpers ====================

    fn is_table_migration_complete(&self) -> bool {
        self.table_migration_status_provider
            .get_table_migration_status()
            == TableMigrationStatus::Complete
    }

    /// Java `getWriteDelegate()` — routes on the cached-once status.
    fn write_delegate(&self) -> Result<&CoordinatorStateDaoDelegate, LeasingError> {
        match *self.cached_status.lock().expect("cached_status poisoned") {
            Some(TableMigrationStatus::Complete) | Some(TableMigrationStatus::Pending) => {
                Ok(&self.lease_table_delegate)
            }
            Some(TableMigrationStatus::Init) | Some(TableMigrationStatus::Deployed) => {
                Ok(&self.legacy_table_delegate)
            }
            other => Err(LeasingError::invalid_state(format!(
                "Cannot determine write delegate for cached status: {other:?}"
            ))),
        }
    }

    fn ensure_initialized(&self) -> Result<(), LeasingError> {
        if !self.initialized.load(Ordering::SeqCst) {
            return Err(LeasingError::invalid_state(
                "CoordinatorStateDAO is not initialized. Call initialize() first.",
            ));
        }
        Ok(())
    }
}

#[async_trait]
impl CoordinatorStateAccess for CoordinatorStateDao {
    async fn get_coordinator_state(
        &self,
        key: &str,
    ) -> Result<Option<CoordinatorState>, LeasingError> {
        CoordinatorStateDao::get_coordinator_state(self, key).await
    }

    async fn list_coordinator_state_by_entity_type(
        &self,
        entity_type: CoordinatorStateType,
    ) -> Result<Vec<CoordinatorState>, LeasingError> {
        CoordinatorStateDao::list_coordinator_state_by_entity_type(self, entity_type).await
    }

    async fn create_coordinator_state_if_not_exists(
        &self,
        state: &CoordinatorState,
    ) -> Result<bool, LeasingError> {
        CoordinatorStateDao::create_coordinator_state_if_not_exists(self, state).await
    }

    async fn update_coordinator_state_with_expectation(
        &self,
        state: &CoordinatorState,
        expectations: HashMap<String, ExpectedAttributeValue>,
    ) -> Result<bool, LeasingError> {
        CoordinatorStateDao::update_coordinator_state_with_expectation(self, state, expectations)
            .await
    }

    async fn delete_coordinator_state(&self, key: &str) -> Result<bool, LeasingError> {
        CoordinatorStateDao::delete_coordinator_state(self, key).await
    }
}

#[cfg(test)]
mod tests {
    //! Port of `CoordinatorStateDAODelegateRoutingTest` and the mock-portable
    //! subset of `CoordinatorStateDAOTest`.
    //!
    //! The Java tests run against an embedded DynamoDB (`DynamoDBEmbedded`) and
    //! verify behavior via read-back / raw scans. The Rust port replaces that with
    //! `aws-smithy-mocks`, using `match_requests` on the target table name to
    //! assert **routing** (which delegate/table an operation hits) and canned
    //! responses/errors to assert CRUD outcomes. The lock-item test
    //! (`testCreatingLeaderAndMigrationKey`) is skipped (documented wave-10c DDB
    //! lock-client gap).

    use super::*;
    use crate::coordinator::coordinator_config::CoordinatorConfig;
    use crate::coordinator::delegate::coordinator_state_dao_delegate::LEGACY_COORDINATOR_STATE_HASH_KEY;
    use crate::coordinator::migration::table_migration_status_provider::MockTableMigrationStatusProvider;
    use crate::coordinator::stream_info::StreamInfo;
    use aws_sdk_dynamodb::operation::delete_item::DeleteItemOutput;
    use aws_sdk_dynamodb::operation::describe_table::DescribeTableOutput;
    use aws_sdk_dynamodb::operation::get_item::GetItemOutput;
    use aws_sdk_dynamodb::operation::put_item::{PutItemError, PutItemOutput};
    use aws_sdk_dynamodb::operation::scan::ScanOutput;
    use aws_sdk_dynamodb::operation::update_item::{UpdateItemError, UpdateItemOutput};
    use aws_sdk_dynamodb::types::error::ConditionalCheckFailedException;
    use aws_sdk_dynamodb::types::AttributeValue;
    use aws_sdk_dynamodb::Client;
    use aws_smithy_mocks::{mock, mock_client, Rule, RuleMode};

    const LEGACY_TABLE: &str = "TestApp-CoordinatorState";
    const LEASE_TABLE: &str = "routing-test-LeaseTable";
    const LEASE_KEY_KEY: &str = crate::leases::dynamodb::LEASE_KEY_KEY;

    fn status_provider(status: TableMigrationStatus) -> Arc<dyn TableMigrationStatusProvider> {
        let mut m = MockTableMigrationStatusProvider::new();
        m.expect_get_table_migration_status()
            .returning(move || status);
        Arc::new(m)
    }

    fn table_config() -> CoordinatorStateTableConfig {
        // Java: new CoordinatorConfig("TestApp").coordinatorStateTableConfig()
        // (default table name "TestApp-CoordinatorState").
        CoordinatorConfig::new("TestApp")
            .coordinator_state_table_config()
            .clone()
    }

    /// A `describe_table` rule that reports the legacy table exists (so the legacy
    /// delegate is enabled by `initialize_delegates`).
    fn legacy_table_exists_rule() -> Rule {
        mock!(Client::describe_table)
            .match_requests(|r| r.table_name() == Some(LEGACY_TABLE))
            .then_output(|| DescribeTableOutput::builder().build())
    }

    fn dao_with(client: Client, status: TableMigrationStatus) -> CoordinatorStateDao {
        CoordinatorStateDao::new(
            client,
            &table_config(),
            LEASE_TABLE,
            status_provider(status),
        )
    }

    fn stream_info_item(key: &str, pk_attr: &str) -> HashMap<String, AttributeValue> {
        let mut item = HashMap::new();
        item.insert(pk_attr.to_string(), AttributeValue::S(key.to_string()));
        for (k, v) in StreamInfo::new(key, format!("{key}Id")).serialize() {
            item.insert(k, v);
        }
        item
    }

    // ==================== Routing tests (DelegateRoutingTest) ====================

    #[tokio::test]
    async fn get_coordinator_state_when_complete_reads_from_lease_table() {
        // Java `getCoordinatorState_whenComplete_readsFromLeaseTable`.
        let legacy_get = mock!(Client::get_item)
            .match_requests(|r| r.table_name() == Some(LEGACY_TABLE))
            .then_output(|| GetItemOutput::builder().build());
        let lease_get = mock!(Client::get_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| {
                GetItemOutput::builder()
                    .set_item(Some(stream_info_item("test-key-1", LEASE_KEY_KEY)))
                    .build()
            });
        let client = mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&legacy_table_exists_rule(), &legacy_get, &lease_get]
        );
        let dao = dao_with(client, TableMigrationStatus::Complete);
        dao.initialize_delegates().await.unwrap();
        dao.initialize().unwrap();

        let result = dao
            .get_coordinator_state("test-key-1")
            .await
            .unwrap()
            .unwrap();
        assert_eq!(result.key(), Some("test-key-1"));
        // When COMPLETE, reads go lease-table-only — the legacy table is never hit.
        assert_eq!(legacy_get.num_calls(), 0);
        assert_eq!(lease_get.num_calls(), 1);
    }

    #[tokio::test]
    async fn get_coordinator_state_when_init_reads_from_legacy_first() {
        // Java `getCoordinatorState_whenInit_readsFromLegacyFirst`.
        let legacy_get = mock!(Client::get_item)
            .match_requests(|r| r.table_name() == Some(LEGACY_TABLE))
            .then_output(|| {
                GetItemOutput::builder()
                    .set_item(Some(stream_info_item(
                        "legacy-key",
                        LEGACY_COORDINATOR_STATE_HASH_KEY,
                    )))
                    .build()
            });
        let lease_get = mock!(Client::get_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| GetItemOutput::builder().build());
        let client = mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&legacy_table_exists_rule(), &legacy_get, &lease_get]
        );
        let dao = dao_with(client, TableMigrationStatus::Init);
        dao.initialize_delegates().await.unwrap();
        dao.initialize().unwrap();

        let result = dao
            .get_coordinator_state("legacy-key")
            .await
            .unwrap()
            .unwrap();
        assert_eq!(result.key(), Some("legacy-key"));
        // Legacy is read first and found → the lease table is not consulted.
        assert_eq!(legacy_get.num_calls(), 1);
        assert_eq!(lease_get.num_calls(), 0);
    }

    #[tokio::test]
    async fn get_coordinator_state_when_init_falls_back_to_lease_table() {
        // Java `getCoordinatorState_whenInit_fallsBackToLeaseTable`.
        let legacy_get = mock!(Client::get_item)
            .match_requests(|r| r.table_name() == Some(LEGACY_TABLE))
            .then_output(|| GetItemOutput::builder().build()); // not found in legacy
        let lease_get = mock!(Client::get_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| {
                GetItemOutput::builder()
                    .set_item(Some(stream_info_item("only-in-lease", LEASE_KEY_KEY)))
                    .build()
            });
        let client = mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&legacy_table_exists_rule(), &legacy_get, &lease_get]
        );
        let dao = dao_with(client, TableMigrationStatus::Init);
        dao.initialize_delegates().await.unwrap();
        dao.initialize().unwrap();

        let result = dao
            .get_coordinator_state("only-in-lease")
            .await
            .unwrap()
            .unwrap();
        assert_eq!(result.key(), Some("only-in-lease"));
        // Legacy misses → falls back to the lease table.
        assert_eq!(legacy_get.num_calls(), 1);
        assert_eq!(lease_get.num_calls(), 1);
    }

    #[tokio::test]
    async fn write_operation_before_initialize_throws_invalid_state() {
        // Java `writeOperation_beforeInitialize_throwsInvalidStateException`.
        let client = mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&legacy_table_exists_rule()]
        );
        let dao = dao_with(client, TableMigrationStatus::Complete);
        dao.initialize_delegates().await.unwrap();
        // Deliberately do NOT call dao.initialize().
        let state = CoordinatorState::generic(Some("test-key".to_string()), None, None);
        let err = dao
            .create_coordinator_state_if_not_exists(&state)
            .await
            .unwrap_err();
        assert!(matches!(err, LeasingError::InvalidState { .. }));
    }

    #[tokio::test]
    async fn initialize_when_status_unknown_throws_invalid_state() {
        // Java `initialize_whenStatusUnknown_throwsInvalidStateException`.
        let client = mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&legacy_table_exists_rule()]
        );
        let dao = dao_with(client, TableMigrationStatus::Unknown);
        dao.initialize_delegates().await.unwrap();
        let err = dao.initialize().unwrap_err();
        assert!(matches!(err, LeasingError::InvalidState { .. }));
    }

    #[tokio::test]
    async fn create_coordinator_state_when_init_writes_to_legacy() {
        // Java `createCoordinatorState_whenInit_writesToLegacy`.
        let legacy_put = mock!(Client::put_item)
            .match_requests(|r| r.table_name() == Some(LEGACY_TABLE))
            .then_output(|| PutItemOutput::builder().build());
        let lease_put = mock!(Client::put_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| PutItemOutput::builder().build());
        let client = mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&legacy_table_exists_rule(), &legacy_put, &lease_put]
        );
        let dao = dao_with(client, TableMigrationStatus::Init);
        dao.initialize_delegates().await.unwrap();
        dao.initialize().unwrap();
        dao.initialize().unwrap(); // idempotent (Java calls it twice)

        let state = CoordinatorState::StreamInfo(StreamInfo::new("write-test-init", "id"));
        assert!(dao
            .create_coordinator_state_if_not_exists(&state)
            .await
            .unwrap());
        // INIT routes writes to the legacy table.
        assert_eq!(legacy_put.num_calls(), 1);
        assert_eq!(lease_put.num_calls(), 0);
    }

    #[tokio::test]
    async fn create_coordinator_state_when_complete_writes_to_lease_table() {
        // Java `createCoordinatorState_whenComplete_writesToLeaseTable`.
        let legacy_put = mock!(Client::put_item)
            .match_requests(|r| r.table_name() == Some(LEGACY_TABLE))
            .then_output(|| PutItemOutput::builder().build());
        let lease_put = mock!(Client::put_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| PutItemOutput::builder().build());
        let client = mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&legacy_table_exists_rule(), &legacy_put, &lease_put]
        );
        let dao = dao_with(client, TableMigrationStatus::Complete);
        dao.initialize_delegates().await.unwrap();
        dao.initialize().unwrap();
        dao.initialize().unwrap();

        let state = CoordinatorState::StreamInfo(StreamInfo::new("write-test-complete", "id"));
        assert!(dao
            .create_coordinator_state_if_not_exists(&state)
            .await
            .unwrap());
        assert_eq!(lease_put.num_calls(), 1);
        assert_eq!(legacy_put.num_calls(), 0);
    }

    #[tokio::test]
    async fn create_coordinator_state_when_pending_writes_to_lease_table() {
        // Java `createCoordinatorState_whenPending_writesToLeaseTable`.
        let legacy_put = mock!(Client::put_item)
            .match_requests(|r| r.table_name() == Some(LEGACY_TABLE))
            .then_output(|| PutItemOutput::builder().build());
        let lease_put = mock!(Client::put_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| PutItemOutput::builder().build());
        let client = mock_client!(
            aws_sdk_dynamodb,
            RuleMode::MatchAny,
            &[&legacy_table_exists_rule(), &legacy_put, &lease_put]
        );
        let dao = dao_with(client, TableMigrationStatus::Pending);
        dao.initialize_delegates().await.unwrap();
        dao.initialize().unwrap();
        dao.initialize().unwrap();

        let state = CoordinatorState::StreamInfo(StreamInfo::new("write-test-pending", "id"));
        assert!(dao
            .create_coordinator_state_if_not_exists(&state)
            .await
            .unwrap());
        assert_eq!(lease_put.num_calls(), 1);
        assert_eq!(legacy_put.num_calls(), 0);
    }

    // ==================== CRUD tests (CoordinatorStateDAOTest, COMPLETE routing) ====================

    /// A DAO in COMPLETE mode (all reads/writes go to the lease table only, so
    /// `initialize_delegates` still needs the legacy describe_table probe).
    async fn complete_dao(rules: &[&Rule]) -> CoordinatorStateDao {
        let describe = legacy_table_exists_rule();
        let mut all: Vec<&Rule> = vec![&describe];
        all.extend_from_slice(rules);
        let client = mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, &all);
        let dao = dao_with(client, TableMigrationStatus::Complete);
        dao.initialize_delegates().await.unwrap();
        dao.initialize().unwrap();
        dao
    }

    #[tokio::test]
    async fn list_coordinator_state_returns_typed_items() {
        // Java `testListCoordinatorState`: a mix of StreamInfo + a MigrationState
        // record; assert count and typed deserialization.
        use crate::coordinator::migration::client_version::ClientVersion;
        use crate::coordinator::migration::migration_state::MigrationState;
        let mut migration_state = MigrationState::new("worker");
        migration_state.update(ClientVersion::ClientVersionUpgradeFrom2x, "worker");
        let mut migration_item = migration_state.serialize();
        migration_item.insert(
            LEASE_KEY_KEY.to_string(),
            AttributeValue::S("Migration3.0".to_string()),
        );
        let scan_rule = mock!(Client::scan)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(move || {
                ScanOutput::builder()
                    .set_items(Some(vec![
                        stream_info_item("key1", LEASE_KEY_KEY),
                        stream_info_item("key2", LEASE_KEY_KEY),
                        stream_info_item("key3", LEASE_KEY_KEY),
                        stream_info_item("key4", LEASE_KEY_KEY),
                        migration_item.clone(),
                    ]))
                    .build()
            });
        let dao = complete_dao(&[&scan_rule]).await;
        let states = dao.list_coordinator_state().await.unwrap();
        assert_eq!(states.len(), 5);
        let mut stream_infos = 0;
        let mut migrations = 0;
        for s in &states {
            match s {
                CoordinatorState::StreamInfo(info) => {
                    assert_eq!(info.stream_id(), format!("{}Id", info.key()));
                    stream_infos += 1;
                }
                CoordinatorState::MigrationState(m) => {
                    assert_eq!(
                        m.client_version(),
                        ClientVersion::ClientVersionUpgradeFrom2x
                    );
                    migrations += 1;
                }
                _ => {}
            }
        }
        assert_eq!(stream_infos, 4);
        assert_eq!(migrations, 1);
    }

    #[tokio::test]
    async fn list_coordinator_state_by_entity_type_returns_stream_infos() {
        // Java `testListCoordinatorStateByEntityType`.
        let scan_rule = mock!(Client::scan)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| {
                ScanOutput::builder()
                    .set_items(Some(
                        (1..=5)
                            .map(|i| stream_info_item(&format!("key{i}"), LEASE_KEY_KEY))
                            .collect(),
                    ))
                    .build()
            });
        let dao = complete_dao(&[&scan_rule]).await;
        let states = dao
            .list_coordinator_state_by_entity_type(CoordinatorStateType::StreamInfo)
            .await
            .unwrap();
        assert_eq!(states.len(), 5);
        for s in &states {
            match s {
                CoordinatorState::StreamInfo(info) => {
                    assert_eq!(info.stream_id(), format!("{}Id", info.key()));
                }
                _ => panic!("expected StreamInfo"),
            }
        }
    }

    #[tokio::test]
    async fn create_coordinator_state_item_not_exists_returns_true() {
        // Java `testCreateCoordinatorState_ItemNotExists` (put succeeds → true).
        let put_rule = mock!(Client::put_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| PutItemOutput::builder().build());
        let dao = complete_dao(&[&put_rule]).await;
        let state = CoordinatorState::StreamInfo(StreamInfo::new("key1", "id"));
        assert!(dao
            .create_coordinator_state_if_not_exists(&state)
            .await
            .unwrap());
    }

    #[tokio::test]
    async fn create_coordinator_state_item_exists_returns_false() {
        // Java `testCreateCoordinatorState_ItemExists` (conditional-check failed →
        // key already exists → false).
        let put_rule = mock!(Client::put_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_error(|| {
                PutItemError::ConditionalCheckFailedException(
                    ConditionalCheckFailedException::builder().build(),
                )
            });
        let dao = complete_dao(&[&put_rule]).await;
        let state = CoordinatorState::StreamInfo(StreamInfo::new("key1", "id"));
        assert!(!dao
            .create_coordinator_state_if_not_exists(&state)
            .await
            .unwrap());
    }

    #[tokio::test]
    async fn update_coordinator_state_with_expectation_success() {
        // Java `testUpdateCoordinatorStateWithExpectation_Success`.
        let update_rule = mock!(Client::update_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| UpdateItemOutput::builder().build());
        let dao = complete_dao(&[&update_rule]).await;
        let state = CoordinatorState::StreamInfo(StreamInfo::new("Migration3.0", "id"));
        assert!(dao
            .update_coordinator_state_with_expectation(&state, HashMap::new())
            .await
            .unwrap());
    }

    #[tokio::test]
    async fn update_coordinator_state_with_expectation_condition_failed() {
        // Java `testUpdateCoordinatorStateWithExpectation_ConditionFailed` (the
        // conditional-check failed → returns false).
        let update_rule = mock!(Client::update_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_error(|| {
                UpdateItemError::ConditionalCheckFailedException(
                    ConditionalCheckFailedException::builder().build(),
                )
            });
        let dao = complete_dao(&[&update_rule]).await;
        let state = CoordinatorState::StreamInfo(StreamInfo::new("Migration3.0", "id"));
        assert!(!dao
            .update_coordinator_state_with_expectation(&state, HashMap::new())
            .await
            .unwrap());
    }

    #[tokio::test]
    async fn update_coordinator_state_with_expectation_non_existent_key() {
        // Java `testUpdateCoordinatorStateWithExpectation_NonExistentKey`: the
        // existence guard means updating a non-existent key fails the condition →
        // returns false.
        let update_rule = mock!(Client::update_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_error(|| {
                UpdateItemError::ConditionalCheckFailedException(
                    ConditionalCheckFailedException::builder().build(),
                )
            });
        let dao = complete_dao(&[&update_rule]).await;
        let state = CoordinatorState::StreamInfo(StreamInfo::new("does-not-exist", "id"));
        assert!(!dao
            .update_coordinator_state_with_expectation(&state, HashMap::new())
            .await
            .unwrap());
    }

    #[tokio::test]
    async fn delete_coordinator_state_existing_key_returns_true() {
        // Java `testDeleteCoordinatorState_ExistingKey`.
        let delete_rule = mock!(Client::delete_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| DeleteItemOutput::builder().build());
        let dao = complete_dao(&[&delete_rule]).await;
        assert!(dao.delete_coordinator_state("key1").await.unwrap());
    }

    #[tokio::test]
    async fn delete_coordinator_state_non_existent_key_returns_true() {
        // Java `testDeleteCoordinatorState_NonExistentKey`: DynamoDB delete is
        // idempotent — deleting a missing key still returns true.
        let delete_rule = mock!(Client::delete_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| DeleteItemOutput::builder().build());
        let dao = complete_dao(&[&delete_rule]).await;
        assert!(dao
            .delete_coordinator_state("nonExistentKey")
            .await
            .unwrap());
    }

    #[tokio::test]
    async fn delete_coordinator_state_multiple_items() {
        // Java `testDeleteCoordinatorState_MultipleItems`: after deleting one of
        // three items, a subsequent list returns the remaining two. Modeled with a
        // scan sequence: first scan → 3 items, delete → ok, second scan → 2 items.
        let scan_rule = mock!(Client::scan)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .sequence()
            .output(|| {
                ScanOutput::builder()
                    .set_items(Some(vec![
                        stream_info_item("key1", LEASE_KEY_KEY),
                        stream_info_item("key2", LEASE_KEY_KEY),
                        stream_info_item("key3", LEASE_KEY_KEY),
                    ]))
                    .build()
            })
            .output(|| {
                ScanOutput::builder()
                    .set_items(Some(vec![
                        stream_info_item("key1", LEASE_KEY_KEY),
                        stream_info_item("key3", LEASE_KEY_KEY),
                    ]))
                    .build()
            })
            .build();
        let delete_rule = mock!(Client::delete_item)
            .match_requests(|r| r.table_name() == Some(LEASE_TABLE))
            .then_output(|| DeleteItemOutput::builder().build());
        let dao = complete_dao(&[&scan_rule, &delete_rule]).await;

        assert_eq!(dao.list_coordinator_state().await.unwrap().len(), 3);
        assert!(dao.delete_coordinator_state("key2").await.unwrap());
        let remaining = dao.list_coordinator_state().await.unwrap();
        assert_eq!(remaining.len(), 2);
        let keys: HashSet<String> = remaining
            .iter()
            .filter_map(|s| s.key().map(str::to_string))
            .collect();
        assert!(keys.contains("key1"));
        assert!(keys.contains("key3"));
        assert!(!keys.contains("key2"));
    }

    use std::collections::HashSet;
}
