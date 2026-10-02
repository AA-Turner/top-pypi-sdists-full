//! Port of `software.amazon.kinesis.coordinator.migration.TableMigrationStateMachine`
//! (interface) and `TableMigrationStateMachineImpl`.

use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};

use async_trait::async_trait;
use aws_sdk_dynamodb::types::{AttributeValue, ConditionCheck, Put, TransactWriteItem};

use crate::coordinator::coordinator_config::CoordinatorConfig;
use crate::coordinator::coordinator_state::CoordinatorState;
use crate::coordinator::coordinator_state_dao::CoordinatorStateDao;
use crate::coordinator::migration::table_migration_state::{
    TableMigrationState, TABLE_MIGRATION_HASH_KEY, TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME,
};
use crate::coordinator::migration::table_migration_status::TableMigrationStatus;
use crate::coordinator::migration::table_migration_status_provider::DefaultTableMigrationStatusProvider;
use crate::coordinator::migration::table_migration_summary::TableMigrationSummary;
use crate::leases::exceptions::LeasingError;

/// Well-known leader-lock partition key. Java `LeaderLock.LEADER_HASH_KEY`
/// (`leader` package, wave 10c). Reproduced here to skip the lock row during
/// entry moves + the lock-owner condition check.
const LEADER_HASH_KEY: &str = "Leader";

/// SINGLE_TABLE_MIGRATION feature ordinal (Java
/// `WorkerMetricStats.Features.SINGLE_TABLE_MIGRATION.ordinal()`). See
/// [`crate::worker::metricstats::worker_metric_stats::Features`].
const SINGLE_TABLE_MIGRATION_ORDINAL: i32 = 1;

const TRANSACTION_BATCH_SIZE: usize = 25;

/// Error type for the table migration state machine. The `InvalidState` /
/// `LockHandoffRequired` variants are used as **control flow**: the caller (the
/// leader-lock loop, wave 10c/10d) must release the current lock and re-acquire.
#[derive(Debug)]
pub enum TableMigrationError {
    /// DDB failure — caller should treat as transient and retry next cycle.
    Dependency(LeasingError),
    /// Inconsistent state (Java `InvalidStateException` for invalid config combos).
    InvalidState(String),
    /// PENDING -> COMPLETE succeeded (or another leader completed): release the
    /// current lock so the correct one is acquired next cycle.
    LockHandoffRequired,
}

impl std::fmt::Display for TableMigrationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            TableMigrationError::Dependency(e) => write!(f, "Dependency: {e}"),
            TableMigrationError::InvalidState(m) => write!(f, "InvalidState: {m}"),
            TableMigrationError::LockHandoffRequired => write!(f, "LockHandoffRequired"),
        }
    }
}

impl std::error::Error for TableMigrationError {}

impl From<LeasingError> for TableMigrationError {
    fn from(e: LeasingError) -> Self {
        TableMigrationError::Dependency(e)
    }
}

/// Java `TableMigrationStateMachine` interface.
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait TableMigrationStateMachine: Send + Sync {
    /// Java `initialize()`.
    async fn initialize(&self) -> Result<(), TableMigrationError>;
    /// Java `handleLeaderLockResult(isLeader)`.
    async fn handle_leader_lock_result(&self, is_leader: bool) -> Result<(), TableMigrationError>;
    /// Java `shutdown()`.
    async fn shutdown(&self);
}

struct Inner {
    initialized: bool,
    is_shutdown: bool,
    latest_migration_summary: Option<TableMigrationSummary>,
    /// In-flight async move: the join handle + a cancel flag polled between
    /// batches. Java `pendingMoveFuture` + `Thread.isInterrupted()`.
    pending_move: Option<PendingMove>,
}

struct PendingMove {
    handle: tokio::task::JoinHandle<bool>,
    cancel: Arc<AtomicBool>,
}

impl PendingMove {
    fn is_done(&self) -> bool {
        self.handle.is_finished()
    }
    fn cancel(&self) {
        self.cancel.store(true, Ordering::SeqCst);
        self.handle.abort();
    }
}

/// Concrete driver of the table-consolidation state machine. Java
/// `TableMigrationStateMachineImpl`.
pub struct TableMigrationStateMachineImpl {
    status_provider: Arc<DefaultTableMigrationStatusProvider>,
    coordinator_state_dao: Arc<CoordinatorStateDao>,
    worker_id: String,
    migrate_all_entities_to_lease_table: bool,
    bake_time_overrides: HashMap<TableMigrationStatus, i64>,
    inner: Mutex<Inner>,
}

impl TableMigrationStateMachineImpl {
    /// Java constructor.
    pub fn new(
        status_provider: Arc<DefaultTableMigrationStatusProvider>,
        coordinator_state_dao: Arc<CoordinatorStateDao>,
        worker_id: impl Into<String>,
        coordinator_config: &CoordinatorConfig,
    ) -> Self {
        let mut bake_time_overrides = HashMap::new();
        bake_time_overrides.insert(
            TableMigrationStatus::Complete,
            coordinator_config.effective_table_migration_complete_bake_time_seconds(),
        );
        Self {
            status_provider,
            coordinator_state_dao,
            worker_id: worker_id.into(),
            migrate_all_entities_to_lease_table: coordinator_config
                .migrate_all_entities_to_lease_table(),
            bake_time_overrides,
            inner: Mutex::new(Inner {
                initialized: false,
                is_shutdown: false,
                latest_migration_summary: None,
                pending_move: None,
            }),
        }
    }

    // ==================== Lifecycle ====================

    /// Java `initialize()`.
    pub async fn initialize(&self) -> Result<(), TableMigrationError> {
        {
            let inner = self.inner.lock().expect("poisoned");
            if inner.initialized {
                return Ok(());
            }
        }
        tracing::info!(
            migrate_all = self.migrate_all_entities_to_lease_table,
            "Initializing TableMigrationStateMachine"
        );
        // 1. delegates
        self.coordinator_state_dao
            .initialize_delegates()
            .await
            .map_err(TableMigrationError::Dependency)?;
        // 2. read legacy state
        let state_from_ddb = self.read_state_from_legacy().await?;
        // 3. determine effective status
        let effective_status = self.determine_status_for_initialization(state_from_ddb.as_ref())?;
        // 4. publish
        self.status_provider.initialize(
            effective_status != TableMigrationStatus::Complete,
            effective_status,
        );
        // 5. enable writes
        self.coordinator_state_dao
            .initialize()
            .map_err(TableMigrationError::Dependency)?;

        self.inner.lock().expect("poisoned").initialized = true;
        tracing::info!(?effective_status, "TableMigrationStateMachine initialized");
        Ok(())
    }

    /// Java `handleLeaderLockResult(isLeader)`.
    pub async fn handle_leader_lock_result(
        &self,
        is_leader: bool,
    ) -> Result<(), TableMigrationError> {
        {
            let inner = self.inner.lock().expect("poisoned");
            if !inner.initialized {
                // Java throws IllegalStateException (unchecked) — panic to match.
                drop(inner);
                panic!("TableMigrationStateMachine not initialized");
            }
        }
        if self.status_provider.get_table_migration_status() == TableMigrationStatus::Complete {
            return Ok(());
        }

        // Refresh from legacy DDB and reconcile the provider.
        let state_from_ddb = self.read_state_from_legacy().await?;
        if let Some(state) = &state_from_ddb {
            let status_from_ddb = state.table_migration_status();
            if status_from_ddb == TableMigrationStatus::Complete {
                self.status_provider
                    .update_table_migration_status(TableMigrationStatus::Complete);
                return Err(TableMigrationError::LockHandoffRequired);
            }
            let effective = self.apply_config_override_safe(status_from_ddb);
            if effective != self.status_provider.get_table_migration_status() {
                tracing::info!(
                    from = ?self.status_provider.get_table_migration_status(),
                    to = ?effective,
                    ddb = ?status_from_ddb,
                    "Refreshed local status"
                );
                self.status_provider
                    .update_table_migration_status(effective);
            }
        }

        if !is_leader {
            // Cancel any in-progress move.
            let pending = self.inner.lock().expect("poisoned").pending_move.take();
            if let Some(p) = pending {
                if !p.is_done() {
                    tracing::info!("Lost leadership, cancelling in-progress async move");
                    p.cancel();
                }
            }
            return Ok(());
        }

        match self.status_provider.get_table_migration_status() {
            TableMigrationStatus::Init => self.handle_init_state(state_from_ddb.as_ref()).await,
            TableMigrationStatus::Deployed => {
                self.handle_deployed_state(state_from_ddb.as_ref()).await;
                Ok(())
            }
            TableMigrationStatus::Pending => {
                self.handle_pending_state(state_from_ddb.as_ref()).await
            }
            _ => Ok(()),
        }
    }

    fn apply_config_override_safe(
        &self,
        status_from_ddb: TableMigrationStatus,
    ) -> TableMigrationStatus {
        match Self::apply_config_override(status_from_ddb, self.migrate_all_entities_to_lease_table)
        {
            Ok(s) => s,
            Err(_) => {
                tracing::warn!(
                    ?status_from_ddb,
                    "Invalid state during refresh, using DDB value as-is"
                );
                status_from_ddb
            }
        }
    }

    // ==================== Initialization decision table ====================

    fn determine_status_for_initialization(
        &self,
        state_from_ddb: Option<&TableMigrationState>,
    ) -> Result<TableMigrationStatus, TableMigrationError> {
        match state_from_ddb {
            None => {
                if !self
                    .coordinator_state_dao
                    .legacy_table_dao_delegate()
                    .is_enabled()
                {
                    tracing::info!("No state in DDB, no legacy table -> COMPLETE (2->3 migration)");
                    return Ok(TableMigrationStatus::Complete);
                }
                if self.migrate_all_entities_to_lease_table {
                    return Err(TableMigrationError::InvalidState(
                        "Cannot deploy Phase 2 (migrateAllEntitiesToLeaseTable=true) without deploying \
                         Phase 1 first. No table migration state exists in DDB, indicating Phase 1 was \
                         never deployed."
                            .to_string(),
                    ));
                }
                tracing::info!("No state in DDB, legacy exists, config=false -> local INIT");
                Ok(TableMigrationStatus::Init)
            }
            Some(state) => {
                let status_from_ddb = state.table_migration_status();
                if status_from_ddb == TableMigrationStatus::Complete {
                    return Ok(TableMigrationStatus::Complete);
                }
                let effective = Self::apply_config_override(
                    status_from_ddb,
                    self.migrate_all_entities_to_lease_table,
                )?;
                tracing::info!(?status_from_ddb, ?effective, "Effective local status");
                Ok(effective)
            }
        }
    }

    /// Java `applyConfigOverride`. Pure decision function (testable in isolation).
    pub fn apply_config_override(
        status_from_ddb: TableMigrationStatus,
        migrate_all: bool,
    ) -> Result<TableMigrationStatus, TableMigrationError> {
        if status_from_ddb == TableMigrationStatus::Init && migrate_all {
            return Err(TableMigrationError::InvalidState(
                "Cannot deploy Phase 2 (migrateAllEntitiesToLeaseTable=true) while Phase 1 is still \
                 in INIT. Phase 1 must reach DEPLOYED first."
                    .to_string(),
            ));
        }
        if status_from_ddb == TableMigrationStatus::Deployed && migrate_all {
            return Ok(TableMigrationStatus::Pending);
        }
        if status_from_ddb == TableMigrationStatus::Pending && !migrate_all {
            return Ok(TableMigrationStatus::Deployed);
        }
        Ok(status_from_ddb)
    }

    // ==================== Leader State Handlers ====================

    async fn handle_init_state(
        &self,
        state_from_ddb: Option<&TableMigrationState>,
    ) -> Result<(), TableMigrationError> {
        if !self.is_min_support_code_met() {
            if let Some(state) = state_from_ddb {
                tracing::info!("INIT: min support code NOT met but DDB has INIT — deleting state (best effort)");
                self.delete_state_safe(state).await;
            }
            tracing::debug!("INIT: waiting for min support code across all workers");
            return Ok(());
        }

        // Min support met.
        let Some(state) = state_from_ddb else {
            tracing::info!("INIT: min support code met, writing INIT to legacy DDB");
            self.write_status_to_legacy_safe(TableMigrationStatus::Init, None)
                .await;
            return Ok(());
        };

        if state.table_migration_status() == TableMigrationStatus::Deployed {
            tracing::info!(
                "INIT: DDB state is DEPLOYED (provider update missed), reconciling to DEPLOYED"
            );
            self.status_provider
                .update_table_migration_status(TableMigrationStatus::Deployed);
            return Ok(());
        }

        if state.table_migration_status() != TableMigrationStatus::Init {
            tracing::warn!(status = ?state.table_migration_status(), "INIT: unexpected DDB state, skipping bake");
            return Ok(());
        }

        let steady_since_seconds = state.modified_timestamp() / 1000;
        let now_seconds = chrono::Utc::now().timestamp_millis() / 1000;
        let elapsed_seconds = now_seconds - steady_since_seconds;
        let bake_time_seconds =
            TableMigrationStatus::Deployed.get_bake_time_seconds(&self.bake_time_overrides);
        if elapsed_seconds >= bake_time_seconds {
            tracing::info!(
                elapsed_seconds,
                bake_time_seconds,
                "INIT -> DEPLOYED: bake time elapsed"
            );
            if self
                .write_status_to_legacy_safe(TableMigrationStatus::Deployed, Some(state))
                .await
            {
                self.status_provider
                    .update_table_migration_status(TableMigrationStatus::Deployed);
            }
        } else {
            tracing::debug!(elapsed_seconds, bake_time_seconds, "INIT: baking");
        }
        Ok(())
    }

    async fn handle_deployed_state(&self, state_from_ddb: Option<&TableMigrationState>) {
        if let Some(state) = state_from_ddb {
            if state.table_migration_status() == TableMigrationStatus::Pending {
                tracing::info!("DEPLOYED: DDB has PENDING but config=false, writing DEPLOYED back");
                self.write_status_to_legacy_safe(TableMigrationStatus::Deployed, Some(state))
                    .await;
                return;
            }
        }
        tracing::debug!("DEPLOYED: Phase 1 leader steady state, waiting for Phase 2");
    }

    async fn handle_pending_state(
        &self,
        state_from_ddb: Option<&TableMigrationState>,
    ) -> Result<(), TableMigrationError> {
        let Some(state) = state_from_ddb else {
            tracing::warn!(
                "PENDING: no state in DDB (manually deleted?), creating DEPLOYED to unblock"
            );
            self.write_status_to_legacy_safe(TableMigrationStatus::Deployed, None)
                .await;
            return Ok(());
        };

        let status_from_ddb = state.table_migration_status();

        if status_from_ddb == TableMigrationStatus::Deployed {
            if !self.is_legacy_worker_metrics_empty() {
                // Rollback detected: cancel any in-progress move.
                let pending = self.inner.lock().expect("poisoned").pending_move.take();
                if let Some(p) = pending {
                    if !p.is_done() {
                        tracing::info!(
                            "PENDING: DDB=DEPLOYED, legacy non-empty — cancelling async move"
                        );
                        p.cancel();
                    }
                }
                tracing::debug!(
                    "PENDING: DDB=DEPLOYED, waiting for all workers to emit to lease table"
                );
                return Ok(());
            }

            // All workers emitting to lease table only — start/check async move.
            let has_pending = self.inner.lock().expect("poisoned").pending_move.is_some();
            if has_pending {
                let done = {
                    let inner = self.inner.lock().expect("poisoned");
                    inner
                        .pending_move
                        .as_ref()
                        .map(|p| p.is_done())
                        .unwrap_or(false)
                };
                if !done {
                    tracing::debug!("PENDING: DDB=DEPLOYED, async move in progress, waiting");
                    return Ok(());
                }
                // Move finished — join for result.
                let pending = self.inner.lock().expect("poisoned").pending_move.take();
                let move_success = match pending {
                    Some(p) => p.handle.await.unwrap_or(false),
                    None => false,
                };
                if move_success {
                    if !self.is_legacy_coordinator_state_empty().await {
                        tracing::warn!("PENDING: async move reported success but legacy table not empty, retry");
                        return Ok(());
                    }
                    tracing::info!(
                        "PENDING: async move succeeded + legacy verified empty, writing PENDING"
                    );
                    self.write_status_to_legacy_safe(TableMigrationStatus::Pending, Some(state))
                        .await;
                } else {
                    tracing::warn!("PENDING: async move reported failure, will retry next cycle");
                }
            } else {
                tracing::info!("PENDING: DDB=DEPLOYED, legacy empty — starting async move");
                self.start_async_move();
            }
            return Ok(());
        }

        if status_from_ddb == TableMigrationStatus::Pending {
            if !self.is_legacy_worker_metrics_empty()
                || !self.is_legacy_coordinator_state_empty().await
            {
                tracing::info!(
                    "PENDING: DDB=PENDING but legacy non-empty — writing DEPLOYED (rollback)"
                );
                self.write_status_to_legacy_safe(TableMigrationStatus::Deployed, Some(state))
                    .await;
                let pending = self.inner.lock().expect("poisoned").pending_move.take();
                if let Some(p) = pending {
                    if !p.is_done() {
                        p.cancel();
                    }
                }
                return Ok(());
            }

            let steady_since_seconds = state.modified_timestamp() / 1000;
            let now_seconds = chrono::Utc::now().timestamp_millis() / 1000;
            let elapsed_seconds = now_seconds - steady_since_seconds;
            let bake_time_seconds =
                TableMigrationStatus::Complete.get_bake_time_seconds(&self.bake_time_overrides);
            if elapsed_seconds >= bake_time_seconds {
                tracing::info!(
                    elapsed_seconds,
                    bake_time_seconds,
                    "PENDING -> COMPLETE: bake time elapsed"
                );
                return self.finalize_migration_complete(state).await;
            }
            tracing::debug!(elapsed_seconds, bake_time_seconds, "PENDING: baking");
        }
        Ok(())
    }

    // ==================== Shutdown ====================

    /// Java `shutdown()`.
    pub async fn shutdown(&self) {
        let pending = {
            let mut inner = self.inner.lock().expect("poisoned");
            if inner.is_shutdown {
                tracing::info!("TableMigrationStateMachine already shut down");
                return;
            }
            inner.is_shutdown = true;
            inner.pending_move.take()
        };
        tracing::info!("Shutting down TableMigrationStateMachine");
        if let Some(p) = pending {
            if !p.is_done() {
                tracing::info!("Cancelling in-flight async move during shutdown");
                p.cancel();
            }
        }
        tracing::info!("TableMigrationStateMachine shutdown complete");
    }

    // ==================== Migration summary consumer ====================

    /// Java `updateMigrationSummary(summary)` — called from the LAM thread.
    pub fn update_migration_summary(&self, summary: TableMigrationSummary) {
        self.inner
            .lock()
            .expect("poisoned")
            .latest_migration_summary = Some(summary);
    }

    // ==================== Condition checks ====================

    fn is_min_support_code_met(&self) -> bool {
        let inner = self.inner.lock().expect("poisoned");
        match &inner.latest_migration_summary {
            None => {
                tracing::debug!("No migration summary yet, conservatively false for min support");
                false
            }
            Some(summary) => {
                let met = summary.min_support_code() >= SINGLE_TABLE_MIGRATION_ORDINAL;
                tracing::info!(met, min = summary.min_support_code(), "isMinSupportCodeMet");
                met
            }
        }
    }

    fn is_legacy_worker_metrics_empty(&self) -> bool {
        let inner = self.inner.lock().expect("poisoned");
        match &inner.latest_migration_summary {
            None => {
                tracing::debug!("No migration summary yet, conservatively false");
                false
            }
            Some(summary) => {
                let all_emitting = summary.lease_owners_with_active_metrics()
                    == summary.workers_with_unexpired_leases();
                let legacy_empty = summary.active_workers_with_metrics_in_legacy_table() == 0;
                let result = all_emitting && legacy_empty;
                tracing::info!(result, "isLegacyWorkerMetricsEmpty");
                result
            }
        }
    }

    async fn is_legacy_coordinator_state_empty(&self) -> bool {
        match self
            .coordinator_state_dao
            .legacy_table_dao_delegate()
            .list_coordinator_state()
            .await
        {
            Ok(entries) => {
                for entry in entries {
                    let key = entry.key().unwrap_or("");
                    if key == LEADER_HASH_KEY || key == TABLE_MIGRATION_HASH_KEY {
                        continue;
                    }
                    tracing::info!(key, "isLegacyCoordinatorStateEmpty: unexpected entry");
                    return false;
                }
                true
            }
            Err(e) => {
                tracing::warn!(?e, "Failed to list coordinator state from legacy table");
                false
            }
        }
    }

    // ==================== DDB operations ====================

    async fn read_state_from_legacy(
        &self,
    ) -> Result<Option<TableMigrationState>, TableMigrationError> {
        match self
            .coordinator_state_dao
            .legacy_table_dao_delegate()
            .get_coordinator_state(TABLE_MIGRATION_HASH_KEY)
            .await
        {
            Ok(Some(cs)) => Ok(cs.as_table_migration_state().cloned()),
            Ok(None) => Ok(None),
            Err(e) => Err(TableMigrationError::Dependency(
                LeasingError::dependency_caused_by(
                    "Failed to read table migration state from legacy table",
                    Box::new(e),
                ),
            )),
        }
    }

    async fn delete_state_safe(&self, state: &TableMigrationState) {
        match self
            .coordinator_state_dao
            .legacy_table_dao_delegate()
            .delete_coordinator_state(state.key())
            .await
        {
            Ok(_) => {
                tracing::info!("Deleted table migration state from legacy (best effort reset)")
            }
            Err(e) => tracing::warn!(?e, "Failed to delete table migration state (best effort)"),
        }
    }

    async fn write_status_to_legacy_safe(
        &self,
        status: TableMigrationStatus,
        existing_state: Option<&TableMigrationState>,
    ) -> bool {
        match self.write_status_to_legacy(status, existing_state).await {
            Ok(()) => true,
            Err(e) => {
                tracing::warn!(?e, ?status, "Unable to write table migration status");
                false
            }
        }
    }

    async fn write_status_to_legacy(
        &self,
        status: TableMigrationStatus,
        existing_state: Option<&TableMigrationState>,
    ) -> Result<(), TableMigrationError> {
        let delegate = self.coordinator_state_dao.legacy_table_dao_delegate();
        match existing_state {
            None => {
                let mut new_state = TableMigrationState::new(&self.worker_id);
                new_state.update(status, &self.worker_id);
                let created = delegate
                    .create_coordinator_state_if_not_exists(&CoordinatorState::TableMigrationState(
                        new_state,
                    ))
                    .await
                    .map_err(|e| TableMigrationError::Dependency(wrap_write(status, e)))?;
                if created {
                    tracing::info!(?status, "Created table migration state in legacy");
                } else {
                    tracing::info!("Table migration state already exists in legacy");
                }
            }
            Some(existing) => {
                let mut updated = existing.copy();
                updated.update(status, &self.worker_id);
                let ok = delegate
                    .update_coordinator_state_with_expectation(
                        &CoordinatorState::TableMigrationState(updated),
                        existing.get_dynamo_table_migration_status_expectation(),
                    )
                    .await
                    .map_err(|e| TableMigrationError::Dependency(wrap_write(status, e)))?;
                if ok {
                    tracing::info!(?status, "Updated table migration state in legacy");
                } else {
                    tracing::warn!(
                        ?status,
                        "Conditional write to legacy failed; another worker advanced state"
                    );
                }
            }
        }
        Ok(())
    }

    // ==================== Async copy logic ====================

    fn start_async_move(&self) {
        let cancel = Arc::new(AtomicBool::new(false));
        let dao = self.coordinator_state_dao.clone();
        let worker_id = self.worker_id.clone();
        let cancel_task = cancel.clone();
        let handle = tokio::spawn(async move {
            move_coordinator_state_entries(dao, worker_id, cancel_task)
                .await
                .unwrap_or_else(|e| {
                    tracing::error!(?e, "Async move of coordinator state entries failed");
                    false
                })
        });
        self.inner.lock().expect("poisoned").pending_move = Some(PendingMove { handle, cancel });
    }

    /// Java `finalizeMigrationComplete(existingState)`. On success ALWAYS returns
    /// `LockHandoffRequired` (Java throws `InvalidStateException`); a DDB failure
    /// is caught + logged + returns `Ok(())` (retry next cycle).
    async fn finalize_migration_complete(
        &self,
        existing_state: &TableMigrationState,
    ) -> Result<(), TableMigrationError> {
        let mut lease_table_state = existing_state.copy();
        lease_table_state.update(TableMigrationStatus::Complete, &self.worker_id);
        let mut updated_legacy = existing_state.copy();
        updated_legacy.update(TableMigrationStatus::Complete, &self.worker_id);

        let legacy = self.coordinator_state_dao.legacy_table_dao_delegate();
        let lease = self.coordinator_state_dao.lease_table_dao_delegate();

        let mut transact_items: Vec<TransactWriteItem> = Vec::with_capacity(3);
        transact_items.push(self.create_lock_owner_condition_check());
        transact_items.push(
            lease.create_transact_put(&CoordinatorState::TableMigrationState(lease_table_state)),
        );

        // Overwrite legacy with COMPLETE conditional on existing status == PENDING.
        let mut expr_values = HashMap::new();
        expr_values.insert(
            ":expectedStatus".to_string(),
            AttributeValue::S(TableMigrationStatus::Pending.name().to_string()),
        );
        let legacy_put = Put::builder()
            .table_name(legacy.table_name())
            .set_item(Some(legacy.to_transact_record(
                &CoordinatorState::TableMigrationState(updated_legacy),
            )))
            .condition_expression(format!(
                "{TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME} = :expectedStatus"
            ))
            .set_expression_attribute_values(Some(expr_values))
            .build()
            .expect("valid Put");
        transact_items.push(TransactWriteItem::builder().put(legacy_put).build());

        match self
            .coordinator_state_dao
            .execute_transact_write(transact_items)
            .await
        {
            Ok(()) => {
                tracing::info!(
                    "Transactionally wrote COMPLETE to both lease table and legacy table"
                );
            }
            Err(e) => {
                tracing::warn!(
                    ?e,
                    "Failed to write COMPLETE transactionally; will retry next cycle"
                );
                return Ok(());
            }
        }

        self.status_provider
            .update_table_migration_status(TableMigrationStatus::Complete);
        tracing::info!(
            "Table migration COMPLETE. Release legacy lock for lease table lock acquisition"
        );
        Err(TableMigrationError::LockHandoffRequired)
    }

    fn create_lock_owner_condition_check(&self) -> TransactWriteItem {
        let legacy = self.coordinator_state_dao.legacy_table_dao_delegate();
        let mut key = HashMap::new();
        key.insert(
            legacy.partition_key_attribute_name().to_string(),
            AttributeValue::S(LEADER_HASH_KEY.to_string()),
        );
        let mut expr_values = HashMap::new();
        expr_values.insert(
            ":owner".to_string(),
            AttributeValue::S(self.worker_id.clone()),
        );
        let check = ConditionCheck::builder()
            .table_name(legacy.table_name())
            .set_key(Some(key))
            .condition_expression("ownerName = :owner")
            .set_expression_attribute_values(Some(expr_values))
            .build()
            .expect("valid ConditionCheck");
        TransactWriteItem::builder().condition_check(check).build()
    }
}

fn wrap_write(status: TableMigrationStatus, e: LeasingError) -> LeasingError {
    LeasingError::dependency_caused_by(
        format!("Failed to write table migration status {status:?} to legacy"),
        Box::new(e),
    )
}

/// Java `moveCoordinatorStateEntries()` + `moveBatch()`. Runs on a dedicated
/// task (Java `migrationExecutor`); checks the cancel flag between batches.
async fn move_coordinator_state_entries(
    dao: Arc<CoordinatorStateDao>,
    worker_id: String,
    cancel: Arc<AtomicBool>,
) -> Result<bool, LeasingError> {
    let legacy = dao.legacy_table_dao_delegate();
    let lease = dao.lease_table_dao_delegate();
    let legacy_entries = legacy.list_coordinator_state().await?;
    let entries_to_move: Vec<CoordinatorState> = legacy_entries
        .into_iter()
        .filter(|e| {
            let key = e.key().unwrap_or("");
            key != LEADER_HASH_KEY && key != TABLE_MIGRATION_HASH_KEY
        })
        .collect();

    tracing::info!(
        count = entries_to_move.len(),
        "Moving coordinator state entries to lease table"
    );

    let mut i = 0;
    while i < entries_to_move.len() {
        if cancel.load(Ordering::SeqCst) {
            tracing::info!(
                processed = i,
                total = entries_to_move.len(),
                "Async move interrupted, aborting"
            );
            return Ok(false);
        }
        let end = (i + TRANSACTION_BATCH_SIZE).min(entries_to_move.len());
        let batch = &entries_to_move[i..end];

        let mut transact_items: Vec<TransactWriteItem> = Vec::with_capacity(batch.len() * 2 + 1);
        // Leader fencing.
        let mut key = HashMap::new();
        key.insert(
            legacy.partition_key_attribute_name().to_string(),
            AttributeValue::S(LEADER_HASH_KEY.to_string()),
        );
        let mut expr_values = HashMap::new();
        expr_values.insert(":owner".to_string(), AttributeValue::S(worker_id.clone()));
        let check = ConditionCheck::builder()
            .table_name(legacy.table_name())
            .set_key(Some(key))
            .condition_expression("ownerName = :owner")
            .set_expression_attribute_values(Some(expr_values))
            .build()
            .expect("valid ConditionCheck");
        transact_items.push(TransactWriteItem::builder().condition_check(check).build());

        for entry in batch {
            transact_items.push(lease.create_transact_put(entry));
            transact_items.push(legacy.create_transact_delete(entry.key().unwrap_or("")));
        }
        dao.execute_transact_write(transact_items).await?;
        tracing::info!(
            batch = batch.len(),
            "Transactionally moved batch (with lock fencing)"
        );
        i = end;
    }
    tracing::info!(
        count = entries_to_move.len(),
        "Successfully moved all coordinator state entries"
    );
    Ok(true)
}

#[async_trait]
impl TableMigrationStateMachine for TableMigrationStateMachineImpl {
    async fn initialize(&self) -> Result<(), TableMigrationError> {
        TableMigrationStateMachineImpl::initialize(self).await
    }
    async fn handle_leader_lock_result(&self, is_leader: bool) -> Result<(), TableMigrationError> {
        TableMigrationStateMachineImpl::handle_leader_lock_result(self, is_leader).await
    }
    async fn shutdown(&self) {
        TableMigrationStateMachineImpl::shutdown(self).await
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Decision-table unit tests for applyConfigOverride (the DDB-embedded
    // integration tests are skipped — see WAVE-PLAN.md TEST-PARITY GAPS).

    #[test]
    fn apply_config_override_init_config_true_is_invalid_state() {
        let r =
            TableMigrationStateMachineImpl::apply_config_override(TableMigrationStatus::Init, true);
        assert!(matches!(r, Err(TableMigrationError::InvalidState(_))));
    }

    #[test]
    fn apply_config_override_init_config_false_stays_init() {
        let r = TableMigrationStateMachineImpl::apply_config_override(
            TableMigrationStatus::Init,
            false,
        )
        .unwrap();
        assert_eq!(r, TableMigrationStatus::Init);
    }

    #[test]
    fn apply_config_override_deployed_config_true_becomes_pending() {
        let r = TableMigrationStateMachineImpl::apply_config_override(
            TableMigrationStatus::Deployed,
            true,
        )
        .unwrap();
        assert_eq!(r, TableMigrationStatus::Pending);
    }

    #[test]
    fn apply_config_override_deployed_config_false_stays_deployed() {
        let r = TableMigrationStateMachineImpl::apply_config_override(
            TableMigrationStatus::Deployed,
            false,
        )
        .unwrap();
        assert_eq!(r, TableMigrationStatus::Deployed);
    }

    #[test]
    fn apply_config_override_pending_config_false_becomes_deployed() {
        let r = TableMigrationStateMachineImpl::apply_config_override(
            TableMigrationStatus::Pending,
            false,
        )
        .unwrap();
        assert_eq!(r, TableMigrationStatus::Deployed);
    }

    #[test]
    fn apply_config_override_pending_config_true_stays_pending() {
        let r = TableMigrationStateMachineImpl::apply_config_override(
            TableMigrationStatus::Pending,
            true,
        )
        .unwrap();
        assert_eq!(r, TableMigrationStatus::Pending);
    }

    #[test]
    fn apply_config_override_complete_any_stays_complete() {
        let r = TableMigrationStateMachineImpl::apply_config_override(
            TableMigrationStatus::Complete,
            true,
        )
        .unwrap();
        assert_eq!(r, TableMigrationStatus::Complete);
        let r = TableMigrationStateMachineImpl::apply_config_override(
            TableMigrationStatus::Complete,
            false,
        )
        .unwrap();
        assert_eq!(r, TableMigrationStatus::Complete);
    }

    // =======================================================================
    // Port of TableMigrationStateMachineImplTest.java
    //
    // The Java tests use an embedded DynamoDB (`DynamoDBEmbedded`) with two real
    // tables (legacy CoordinatorState + lease table) and stateful conditional
    // writes/reads. `aws-smithy-mocks` only provides canned per-rule responses,
    // so this port replaces the embedded DB with a small **stateful** in-memory
    // DDB fake (`fake_ddb`) that models the exact operations the state machine
    // issues: consistent get, conditional put (`attribute_not_exists`), legacy
    // conditional update (existence guard + `tm` expectation), delete, scan, and
    // transactional writes with condition checks. It is keyed by (table,
    // partition-key) and implements the all-or-nothing transaction semantics
    // `finalize_migration_complete` / the async move rely on.
    // =======================================================================

    use crate::coordinator::coordinator_config::CoordinatorConfig;
    use crate::coordinator::migration::table_migration_state::{
        MODIFIED_BY_ATTRIBUTE_NAME, MODIFIED_TIMESTAMP_ATTRIBUTE_NAME,
    };
    use aws_sdk_dynamodb::types::AttributeValue;

    const LEGACY_TABLE: &str = "tmsm-test-CoordinatorState";
    const LEASE_TABLE: &str = "tmsm-test-LeaseTable";
    const WORKER_ID: &str = "test-worker";
    const LEGACY_PK: &str = "key";
    const LEASE_PK: &str = "leaseKey";

    /// Stateful in-memory DDB fake used to build a mocked `aws_sdk_dynamodb::Client`.
    mod fake_ddb {
        use super::*;
        use aws_sdk_dynamodb::operation::delete_item::DeleteItemOutput;
        use aws_sdk_dynamodb::operation::describe_table::{
            DescribeTableError, DescribeTableOutput,
        };
        use aws_sdk_dynamodb::operation::get_item::GetItemOutput;
        use aws_sdk_dynamodb::operation::put_item::{PutItemError, PutItemOutput};
        use aws_sdk_dynamodb::operation::scan::ScanOutput;
        use aws_sdk_dynamodb::operation::transact_write_items::{
            TransactWriteItemsError, TransactWriteItemsOutput,
        };
        use aws_sdk_dynamodb::operation::update_item::{UpdateItemError, UpdateItemOutput};
        use aws_sdk_dynamodb::types::error::{
            ConditionalCheckFailedException, ResourceNotFoundException,
            TransactionCanceledException,
        };
        use aws_sdk_dynamodb::types::TransactWriteItem;
        use aws_sdk_dynamodb::Client;
        use aws_smithy_mocks::{mock, mock_client, MockResponse, RuleMode};
        use std::collections::HashMap;
        use std::sync::{Arc, Mutex};

        type Item = HashMap<String, AttributeValue>;

        /// Shared store keyed by (table_name, partition_key_value) -> item.
        #[derive(Clone, Default)]
        pub struct Store {
            inner: Arc<Mutex<HashMap<(String, String), Item>>>,
        }

        /// Extract the partition-key value from an item, trying both known PK
        /// attribute names (legacy "key" and lease "leaseKey").
        fn pk_of(item: &Item) -> Option<String> {
            for attr in [LEGACY_PK, LEASE_PK] {
                if let Some(v) = item.get(attr) {
                    if let Ok(s) = v.as_s() {
                        return Some(s.clone());
                    }
                }
            }
            None
        }

        fn pk_of_key(key: &Item) -> Option<String> {
            pk_of(key)
        }

        impl Store {
            pub fn new() -> Self {
                Store::default()
            }

            /// Directly seed an item (test setup, mirrors the Java `putItem` seeds).
            pub fn put_raw(&self, table: &str, item: Item) {
                let pk = pk_of(&item).expect("item has a partition key");
                self.inner
                    .lock()
                    .unwrap()
                    .insert((table.to_string(), pk), item);
            }

            /// Directly delete an item (test setup, mirrors Java `deleteItem`).
            pub fn delete_raw(&self, table: &str, pk: &str) {
                self.inner
                    .lock()
                    .unwrap()
                    .remove(&(table.to_string(), pk.to_string()));
            }

            /// Read back an item (test assertions, mirrors Java `getItem`).
            pub fn get_raw(&self, table: &str, pk: &str) -> Option<Item> {
                self.inner
                    .lock()
                    .unwrap()
                    .get(&(table.to_string(), pk.to_string()))
                    .cloned()
            }
        }

        /// True iff a legacy `expected` map is satisfied by `existing`.
        /// Supports `exists=false` (item must not exist under that attr) and
        /// `value=X` (attr present and equal). Empty map => always satisfied.
        fn expected_satisfied(
            existing: Option<&Item>,
            expected: &HashMap<String, aws_sdk_dynamodb::types::ExpectedAttributeValue>,
        ) -> bool {
            for (attr, exp) in expected {
                if exp.exists() == Some(false) {
                    // Attribute must NOT exist (used with the partition key => item absent).
                    let present = existing.map(|it| it.contains_key(attr)).unwrap_or(false);
                    if present {
                        return false;
                    }
                } else if let Some(want) = exp.value() {
                    let got = existing.and_then(|it| it.get(attr));
                    if got != Some(want) {
                        return false;
                    }
                }
            }
            true
        }

        /// Evaluate a transaction condition-expression against an item. Only the
        /// two forms the state machine emits are supported:
        ///   `attribute_not_exists(<pk>)`  — item must be absent
        ///   `<attr> = :placeholder`       — attr present and equals the bound value
        fn condition_expr_satisfied(
            existing: Option<&Item>,
            expr: &str,
            values: Option<&HashMap<String, AttributeValue>>,
        ) -> bool {
            let expr = expr.trim();
            if let Some(rest) = expr.strip_prefix("attribute_not_exists(") {
                let attr = rest.trim_end_matches(')');
                return !existing.map(|it| it.contains_key(attr)).unwrap_or(false);
            }
            if let Some((attr, placeholder)) = expr.split_once('=') {
                let attr = attr.trim();
                let placeholder = placeholder.trim();
                let want = values.and_then(|v| v.get(placeholder));
                let got = existing.and_then(|it| it.get(attr));
                return want.is_some() && got == want;
            }
            // Unknown expression form: treat as satisfied (not used by these tests).
            true
        }

        /// Build a mocked stateful DDB `Client`. `existing_tables` lists the table
        /// names that `describe_table` should report as existing (others =>
        /// ResourceNotFound, disabling the legacy delegate).
        pub fn client(store: Store, existing_tables: &'static [&'static str]) -> Client {
            let describe = mock!(Client::describe_table).then_compute_response(move |req| {
                let name = req.table_name().unwrap_or("");
                if existing_tables.contains(&name) {
                    MockResponse::Output(DescribeTableOutput::builder().build())
                } else {
                    MockResponse::Error(DescribeTableError::ResourceNotFoundException(
                        ResourceNotFoundException::builder().build(),
                    ))
                }
            });

            let get = {
                let store = store.clone();
                mock!(Client::get_item).then_compute_output(move |req| {
                    let table = req.table_name().unwrap_or("").to_string();
                    let pk = req.key().and_then(pk_of_key);
                    let item = pk.and_then(|k| store.get_raw(&table, &k));
                    match item {
                        Some(it) => GetItemOutput::builder().set_item(Some(it)).build(),
                        None => GetItemOutput::builder().build(),
                    }
                })
            };

            let put = {
                let store = store.clone();
                mock!(Client::put_item).then_compute_response(move |req| {
                    let table = req.table_name().unwrap_or("").to_string();
                    let item = req.item().cloned().unwrap_or_default();
                    let pk = pk_of(&item).expect("put item has a pk");
                    let existing = store.get_raw(&table, &pk);
                    let expected: HashMap<_, _> = req.expected().cloned().unwrap_or_default();
                    if !expected_satisfied(existing.as_ref(), &expected) {
                        return MockResponse::Error(PutItemError::ConditionalCheckFailedException(
                            ConditionalCheckFailedException::builder().build(),
                        ));
                    }
                    store.put_raw(&table, item);
                    MockResponse::Output(PutItemOutput::builder().build())
                })
            };

            let update = {
                let store = store.clone();
                mock!(Client::update_item).then_compute_response(move |req| {
                    let table = req.table_name().unwrap_or("").to_string();
                    let pk = req.key().and_then(pk_of_key).expect("update key has a pk");
                    let existing = store.get_raw(&table, &pk);
                    let expected: HashMap<_, _> = req.expected().cloned().unwrap_or_default();
                    if !expected_satisfied(existing.as_ref(), &expected) {
                        return MockResponse::Error(
                            UpdateItemError::ConditionalCheckFailedException(
                                ConditionalCheckFailedException::builder().build(),
                            ),
                        );
                    }
                    // Apply the attribute updates (all PUT actions here) onto the
                    // existing item (or a fresh item carrying the pk).
                    let mut item = existing.unwrap_or_default();
                    for (attr, upd) in req.attribute_updates().unwrap_or(&HashMap::new()) {
                        if let Some(v) = upd.value() {
                            item.insert(attr.clone(), v.clone());
                        }
                    }
                    // Ensure the pk is present (the key attr comes from req.key()).
                    if let Some(key) = req.key() {
                        for (k, v) in key {
                            item.entry(k.clone()).or_insert_with(|| v.clone());
                        }
                    }
                    store.put_raw(&table, item);
                    MockResponse::Output(UpdateItemOutput::builder().build())
                })
            };

            let delete = {
                let store = store.clone();
                mock!(Client::delete_item).then_compute_output(move |req| {
                    let table = req.table_name().unwrap_or("").to_string();
                    if let Some(pk) = req.key().and_then(pk_of_key) {
                        store.delete_raw(&table, &pk);
                    }
                    DeleteItemOutput::builder().build()
                })
            };

            let scan = {
                let store = store.clone();
                mock!(Client::scan).then_compute_output(move |req| {
                    let table = req.table_name().unwrap_or("").to_string();
                    let guard = store.inner.lock().unwrap();
                    let items: Vec<Item> = guard
                        .iter()
                        .filter(|((t, _), _)| t == &table)
                        .map(|(_, v)| v.clone())
                        .collect();
                    ScanOutput::builder().set_items(Some(items)).build()
                })
            };

            let transact = {
                let store = store.clone();
                mock!(Client::transact_write_items).then_compute_response(move |req| {
                    let items: &[TransactWriteItem] = req.transact_items();
                    // Phase 1: check ALL conditions against the current store.
                    for twi in items {
                        if let Some(cc) = twi.condition_check() {
                            let table = cc.table_name();
                            let pk = pk_of_key(cc.key()).unwrap_or_default();
                            let existing = store.get_raw(table, &pk);
                            if !condition_expr_satisfied(
                                existing.as_ref(),
                                cc.condition_expression(),
                                cc.expression_attribute_values(),
                            ) {
                                return cancel();
                            }
                        }
                        if let Some(put) = twi.put() {
                            if let Some(expr) = put.condition_expression() {
                                let table = put.table_name();
                                let pk = pk_of(put.item()).unwrap_or_default();
                                let existing = store.get_raw(table, &pk);
                                if !condition_expr_satisfied(
                                    existing.as_ref(),
                                    expr,
                                    put.expression_attribute_values(),
                                ) {
                                    return cancel();
                                }
                            }
                        }
                    }
                    // Phase 2: apply all puts/deletes.
                    for twi in items {
                        if let Some(put) = twi.put() {
                            store.put_raw(put.table_name(), put.item().clone());
                        }
                        if let Some(del) = twi.delete() {
                            if let Some(pk) = pk_of_key(del.key()) {
                                store.delete_raw(del.table_name(), &pk);
                            }
                        }
                    }
                    MockResponse::Output(TransactWriteItemsOutput::builder().build())
                })
            };

            mock_client!(
                aws_sdk_dynamodb,
                RuleMode::MatchAny,
                &[&describe, &get, &put, &update, &delete, &scan, &transact]
            )
        }

        fn cancel() -> MockResponse<TransactWriteItemsOutput, TransactWriteItemsError> {
            MockResponse::Error(TransactWriteItemsError::TransactionCanceledException(
                TransactionCanceledException::builder().build(),
            ))
        }
    }

    // --- test harness helpers -------------------------------------------------

    fn coordinator_state_dao(
        client: aws_sdk_dynamodb::Client,
        legacy_table: &str,
        provider: Arc<DefaultTableMigrationStatusProvider>,
    ) -> Arc<CoordinatorStateDao> {
        let table_config = CoordinatorConfig::new("test-app")
            .coordinator_state_table_config()
            .clone()
            .set_table_name(legacy_table);
        Arc::new(CoordinatorStateDao::new(
            client,
            &table_config,
            LEASE_TABLE,
            provider,
        ))
    }

    fn coordinator_config(migrate_all: bool) -> CoordinatorConfig {
        CoordinatorConfig::new("test-app").set_migrate_all_entities_to_lease_table(migrate_all)
    }

    /// Build a `TableMigrationState` item (as it would be persisted in the legacy
    /// table) with the given status + timestamp. Mirrors Java's raw `putItem`.
    fn migration_item(
        status: TableMigrationStatus,
        modified_by: &str,
        ts_millis: i64,
    ) -> HashMap<String, AttributeValue> {
        let mut item = HashMap::new();
        item.insert(
            LEGACY_PK.to_string(),
            AttributeValue::S(TABLE_MIGRATION_HASH_KEY.to_string()),
        );
        item.insert(
            TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(status.name().to_string()),
        );
        item.insert(
            MODIFIED_BY_ATTRIBUTE_NAME.to_string(),
            AttributeValue::S(modified_by.to_string()),
        );
        item.insert(
            MODIFIED_TIMESTAMP_ATTRIBUTE_NAME.to_string(),
            AttributeValue::N(ts_millis.to_string()),
        );
        item
    }

    fn now_millis() -> i64 {
        chrono::Utc::now().timestamp_millis()
    }

    /// Seed a migration state row with a "recent" timestamp (bake time not
    /// elapsed) — Java's `putTableMigrationState`.
    fn seed_migration_state(store: &fake_ddb::Store, status: TableMigrationStatus) {
        store.put_raw(
            LEGACY_TABLE,
            migration_item(status, WORKER_ID, now_millis()),
        );
    }

    fn summary_min_support_met() -> TableMigrationSummary {
        TableMigrationSummary::builder()
            .min_support_code(1)
            .workers_with_unexpired_leases(1)
            .total_workers_with_leases(1)
            .total_active_workers_with_metrics(1)
            .lease_owners_with_active_metrics(1)
            .active_workers_with_metrics_in_lease_table(1)
            .active_workers_with_metrics_in_legacy_table(0)
            .build()
    }

    fn read_status_from_ddb(store: &fake_ddb::Store) -> Option<TableMigrationStatus> {
        store
            .get_raw(LEGACY_TABLE, TABLE_MIGRATION_HASH_KEY)
            .and_then(|item| {
                item.get(TABLE_MIGRATION_STATUS_ATTRIBUTE_NAME)
                    .and_then(|v| v.as_s().ok())
                    .and_then(|s| TableMigrationStatus::from_name(s))
            })
    }

    // --- Initialization: No legacy table (2→3 migration) ---

    /// Java `initialize_noLegacyTable_shortCircuitsToComplete`.
    #[tokio::test]
    async fn initialize_no_legacy_table_short_circuits_to_complete() {
        let store = fake_ddb::Store::new();
        // Only the LEASE_TABLE exists; the (non-existent) legacy table => COMPLETE.
        let client = fake_ddb::client(store.clone(), &[LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, "non-existent-table", provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Complete
        );
    }

    /// Java `initialize_noLegacyTable_doesNotPersistStateToDDB`.
    #[tokio::test]
    async fn initialize_no_legacy_table_does_not_persist_state_to_ddb() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, "non-existent-table", provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        // The 2→3 short-circuit must NOT persist anything to the lease table.
        assert!(store
            .get_raw(LEASE_TABLE, TABLE_MIGRATION_HASH_KEY)
            .is_none());
    }

    // --- Initialization: Legacy table exists, no state in DDB ---

    /// Java `initialize_legacyTableExists_noState_configFalse_setsInit`.
    #[tokio::test]
    async fn initialize_legacy_table_exists_no_state_config_false_sets_init() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );
    }

    /// Java `initialize_legacyTableExists_noState_configTrue_throwsInvalidState`.
    #[tokio::test]
    async fn initialize_legacy_table_exists_no_state_config_true_throws_invalid_state() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(true),
        );
        let err = sm.initialize().await.unwrap_err();
        assert!(matches!(err, TableMigrationError::InvalidState(_)));
    }

    // --- Initialization: DDB has a seeded state ---

    /// Java `initialize_ddbHasDeployed_configFalse_setsDeployed`.
    #[tokio::test]
    async fn initialize_ddb_has_deployed_config_false_sets_deployed() {
        let store = fake_ddb::Store::new();
        seed_migration_state(&store, TableMigrationStatus::Deployed);
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Deployed
        );
    }

    /// Java `initialize_ddbHasDeployed_configTrue_setsPending`.
    #[tokio::test]
    async fn initialize_ddb_has_deployed_config_true_sets_pending() {
        let store = fake_ddb::Store::new();
        seed_migration_state(&store, TableMigrationStatus::Deployed);
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(true),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Pending
        );
    }

    /// Java `initialize_ddbHasPending_configFalse_setsDeployed`.
    #[tokio::test]
    async fn initialize_ddb_has_pending_config_false_sets_deployed() {
        let store = fake_ddb::Store::new();
        seed_migration_state(&store, TableMigrationStatus::Pending);
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Deployed
        );
    }

    /// Java `initialize_ddbHasComplete_alwaysComplete`.
    #[tokio::test]
    async fn initialize_ddb_has_complete_always_complete() {
        let store = fake_ddb::Store::new();
        seed_migration_state(&store, TableMigrationStatus::Complete);
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Complete
        );
    }

    /// Java `initialize_calledTwice_isIdempotent`.
    #[tokio::test]
    async fn initialize_called_twice_is_idempotent() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        sm.initialize().await.unwrap(); // should not error
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );
    }

    // --- handleLeaderLockResult ---

    /// Java `handleLeaderLockResult_beforeInit_throws` (Java `IllegalStateException`
    /// => Rust `panic!`).
    #[tokio::test]
    #[should_panic(expected = "not initialized")]
    async fn handle_leader_lock_result_before_init_throws() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider,
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        // Not initialized.
        let _ = sm.handle_leader_lock_result(true).await;
    }

    /// Java `handleLeaderLockResult_whenComplete_isNoOp`.
    #[tokio::test]
    async fn handle_leader_lock_result_when_complete_is_no_op() {
        let store = fake_ddb::Store::new();
        seed_migration_state(&store, TableMigrationStatus::Complete);
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        // Should not error or change state.
        sm.handle_leader_lock_result(true).await.unwrap();
        sm.handle_leader_lock_result(false).await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Complete
        );
    }

    /// Java `handleLeaderLockResult_notLeader_noStateChange`.
    #[tokio::test]
    async fn handle_leader_lock_result_not_leader_no_state_change() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        sm.handle_leader_lock_result(false).await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );
    }

    /// Java `handleLeaderLockResult_initState_leader_noSummary_noStateChange`.
    #[tokio::test]
    async fn handle_leader_lock_result_init_state_leader_no_summary_no_state_change() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        // No summary pushed => min support conservatively false.
        sm.handle_leader_lock_result(true).await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );
    }

    /// Java `handleLeaderLockResult_initState_leader_minSupportMet_writesInitToDDB`.
    #[tokio::test]
    async fn handle_leader_lock_result_init_state_leader_min_support_met_writes_init_to_ddb() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();

        sm.update_migration_summary(
            TableMigrationSummary::builder()
                .min_support_code(1)
                .workers_with_unexpired_leases(1)
                .total_active_workers_with_metrics(1)
                .active_workers_with_metrics_in_legacy_table(0)
                .build(),
        );

        sm.handle_leader_lock_result(true).await.unwrap();

        // Status remains INIT locally (bake time hasn't elapsed).
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );
        // INIT was written to legacy DDB.
        assert_eq!(
            read_status_from_ddb(&store),
            Some(TableMigrationStatus::Init)
        );
    }

    /// Java `handleLeaderLockResult_initState_bakeTimeElapsed_transitionsToDeployed`.
    #[tokio::test]
    async fn handle_leader_lock_result_init_state_bake_time_elapsed_transitions_to_deployed() {
        let store = fake_ddb::Store::new();
        // Seed INIT with timestamp 0 so the bake time is already elapsed.
        store.put_raw(
            LEGACY_TABLE,
            migration_item(TableMigrationStatus::Init, WORKER_ID, 0),
        );
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();

        sm.update_migration_summary(summary_min_support_met());

        sm.handle_leader_lock_result(true).await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Deployed
        );
    }

    /// Java `handleLeaderLockResult_initState_ddbAlreadyDeployed_reconcilesProviderToDeployed`.
    #[tokio::test]
    async fn handle_leader_lock_result_init_state_ddb_already_deployed_reconciles_provider_to_deployed(
    ) {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );

        sm.update_migration_summary(summary_min_support_met());

        // First call writes INIT to DDB (no state exists yet).
        sm.handle_leader_lock_result(true).await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );

        // Simulate another leader externally writing DEPLOYED (recent timestamp).
        store.put_raw(
            LEGACY_TABLE,
            migration_item(TableMigrationStatus::Deployed, WORKER_ID, now_millis()),
        );

        // Next call: refresh reads DDB=DEPLOYED, reconciles provider INIT -> DEPLOYED.
        sm.handle_leader_lock_result(true).await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Deployed
        );
    }

    /// Java `handleLeaderLockResult_initState_ddbDeployed_doesNotUseBakeTimestamp`.
    #[tokio::test]
    async fn handle_leader_lock_result_init_state_ddb_deployed_does_not_use_bake_timestamp() {
        let store = fake_ddb::Store::new();
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );

        sm.update_migration_summary(summary_min_support_met());

        // Write INIT to DDB on first call.
        sm.handle_leader_lock_result(true).await.unwrap();

        // Overwrite DDB with DEPLOYED (recent timestamp — bake time NOT elapsed).
        store.put_raw(
            LEGACY_TABLE,
            migration_item(TableMigrationStatus::Deployed, "other-worker", now_millis()),
        );

        // Refresh detects DDB=DEPLOYED and reconciles the provider to DEPLOYED.
        sm.handle_leader_lock_result(true).await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Deployed
        );
    }

    /// Java `handleLeaderLockResult_deployedState_ddbPending_configFalse_rollsBackToDeployed`.
    #[tokio::test]
    async fn handle_leader_lock_result_deployed_state_ddb_pending_config_false_rolls_back_to_deployed(
    ) {
        let store = fake_ddb::Store::new();
        seed_migration_state(&store, TableMigrationStatus::Pending);
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();
        // Config=false + DDB=PENDING => local DEPLOYED after applyConfigOverride.
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Deployed
        );

        sm.handle_leader_lock_result(true).await.unwrap();

        // DDB rolled back to DEPLOYED.
        assert_eq!(
            read_status_from_ddb(&store),
            Some(TableMigrationStatus::Deployed)
        );
    }

    /// Java `handleLeaderLockResult_anotherLeaderCompletedMigration_throwsInvalidState`.
    #[tokio::test]
    async fn handle_leader_lock_result_another_leader_completed_migration_throws_invalid_state() {
        let store = fake_ddb::Store::new();
        seed_migration_state(&store, TableMigrationStatus::Deployed);
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(false),
        );
        sm.initialize().await.unwrap();

        // Another leader writes COMPLETE to DDB.
        store.delete_raw(LEGACY_TABLE, TABLE_MIGRATION_HASH_KEY);
        seed_migration_state(&store, TableMigrationStatus::Complete);

        // handle detects COMPLETE and returns LockHandoffRequired (Java throws
        // InvalidStateException — control-flow signal to release the lock).
        let err = sm.handle_leader_lock_result(true).await.unwrap_err();
        assert!(matches!(err, TableMigrationError::LockHandoffRequired));
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Complete
        );
    }

    /// Java `handleLeaderLockResult_pendingState_legacyNonEmpty_rollsBackToDeployed`.
    #[tokio::test]
    async fn handle_leader_lock_result_pending_state_legacy_non_empty_rolls_back_to_deployed() {
        let store = fake_ddb::Store::new();
        seed_migration_state(&store, TableMigrationStatus::Pending);
        let client = fake_ddb::client(store.clone(), &[LEGACY_TABLE, LEASE_TABLE]);
        let provider = Arc::new(DefaultTableMigrationStatusProvider::new());
        let dao = coordinator_state_dao(client, LEGACY_TABLE, provider.clone());
        let sm = TableMigrationStateMachineImpl::new(
            provider.clone(),
            dao,
            WORKER_ID,
            &coordinator_config(true),
        );
        sm.initialize().await.unwrap();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Pending
        );

        // Summary indicating legacy is NOT empty (rollback detected).
        sm.update_migration_summary(
            TableMigrationSummary::builder()
                .min_support_code(1)
                .workers_with_unexpired_leases(2)
                .total_workers_with_leases(2)
                .total_active_workers_with_metrics(2)
                .lease_owners_with_active_metrics(2)
                .active_workers_with_metrics_in_lease_table(1)
                .active_workers_with_metrics_in_legacy_table(1) // non-empty
                .build(),
        );

        sm.handle_leader_lock_result(true).await.unwrap();

        // DDB rolled back to DEPLOYED.
        assert_eq!(
            read_status_from_ddb(&store),
            Some(TableMigrationStatus::Deployed)
        );
    }
}
