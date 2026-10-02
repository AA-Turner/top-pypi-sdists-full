//! Port of `software.amazon.kinesis.coordinator.CoordinatorConfig`.

use std::sync::Arc;

use crate::common::DdbTableConfig;
use crate::coordinator::coordinator_factory::{CoordinatorFactory, SchedulerCoordinatorFactory};
use crate::coordinator::worker_state_change_listener::{
    NoOpWorkerStateChangeListener, WorkerStateChangeListener,
};
use crate::leases::shard_prioritization::{NoOpShardPrioritization, ShardPrioritization};

/// Version the KCL must operate in, controlling the 2.x → 3.x migration phase.
/// Java `CoordinatorConfig.ClientVersionConfig`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ClientVersionConfig {
    /// Phase 1 of 2.x → 3.x migration (pure 2.x-compatible mode).
    CompatibleWith2xPhase1,
    /// Phase 2 of 2.x → 3.x migration (starts the migration state machine).
    CompatibleWith2x,
    /// 3.x. Default for new applications. Terminal, no rollback.
    ClientVersionConfig3x,
}

const HOUR_SECONDS: i64 = 3600;
const DAY_SECONDS: i64 = 86_400;
const WEEK_SECONDS: i64 = 7 * DAY_SECONDS;

const TABLE_MIGRATION_COMPLETE_BAKE_TIME_MIN_SECONDS: i64 = HOUR_SECONDS;
const TABLE_MIGRATION_COMPLETE_BAKE_TIME_MAX_SECONDS: i64 = WEEK_SECONDS;

/// Configuration for the CoordinatorState DDB table. Java nested
/// `CoordinatorConfig.CoordinatorStateTableConfig extends DdbTableConfig`.
///
/// In Rust `DdbTableConfig` is a plain struct (no inheritance); this wrapper
/// carries one so the default table name `applicationName-CoordinatorState` can
/// be resolved exactly as Java's `super(applicationName, "CoordinatorState")`.
#[derive(Debug, Clone)]
pub struct CoordinatorStateTableConfig {
    inner: DdbTableConfig,
    table_name: String,
}

impl CoordinatorStateTableConfig {
    fn new(application_name: &str) -> Self {
        Self {
            inner: DdbTableConfig::default(),
            table_name: format!("{}-CoordinatorState", application_name),
        }
    }

    /// The resolved table name (default `applicationName-CoordinatorState`).
    pub fn table_name(&self) -> &str {
        &self.table_name
    }

    /// Override the table name (Java `DdbTableConfig.tableName(String)`).
    pub fn set_table_name(mut self, table_name: impl Into<String>) -> Self {
        self.table_name = table_name.into();
        self
    }

    /// The underlying [`DdbTableConfig`] (billing mode, capacity, tags).
    pub fn ddb_table_config(&self) -> &DdbTableConfig {
        &self.inner
    }

    pub fn ddb_table_config_mut(&mut self) -> &mut DdbTableConfig {
        &mut self.inner
    }
}

/// Used by the KCL to configure the coordinator. Java `CoordinatorConfig`
/// (Lombok `@Data @Accessors(fluent = true)`); fluent chainable setters.
pub struct CoordinatorConfig {
    application_name: String,
    max_initialization_attempts: i32,
    parent_shard_poll_interval_millis: i64,
    skip_shard_sync_at_worker_initialization_if_leases_exist: bool,
    shard_consumer_dispatch_poll_interval_millis: i64,
    shard_prioritization: Arc<dyn ShardPrioritization + Send + Sync>,
    worker_state_change_listener: Arc<dyn WorkerStateChangeListener + Send + Sync>,
    coordinator_factory: Arc<dyn CoordinatorFactory + Send + Sync>,
    scheduler_initialization_backoff_time_millis: i64,
    client_version_config: ClientVersionConfig,
    migrate_all_entities_to_lease_table: bool,
    table_migration_complete_bake_time_seconds: i64,
    coordinator_state_table_config: CoordinatorStateTableConfig,
}

impl CoordinatorConfig {
    /// Java `CoordinatorConfig(String applicationName)`.
    pub fn new(application_name: impl Into<String>) -> Self {
        let application_name = application_name.into();
        let coordinator_state_table_config = CoordinatorStateTableConfig::new(&application_name);
        Self {
            application_name,
            max_initialization_attempts: 20,
            parent_shard_poll_interval_millis: 10_000,
            skip_shard_sync_at_worker_initialization_if_leases_exist: false,
            shard_consumer_dispatch_poll_interval_millis: 1_000,
            shard_prioritization: Arc::new(NoOpShardPrioritization::new()),
            worker_state_change_listener: Arc::new(NoOpWorkerStateChangeListener::new()),
            coordinator_factory: Arc::new(SchedulerCoordinatorFactory::new()),
            scheduler_initialization_backoff_time_millis: 1_000,
            client_version_config: ClientVersionConfig::ClientVersionConfig3x,
            migrate_all_entities_to_lease_table: false,
            table_migration_complete_bake_time_seconds: DAY_SECONDS,
            coordinator_state_table_config,
        }
    }

    // ---- getters (fluent, no prefix) ----

    pub fn application_name(&self) -> &str {
        &self.application_name
    }

    pub fn max_initialization_attempts(&self) -> i32 {
        self.max_initialization_attempts
    }

    pub fn parent_shard_poll_interval_millis(&self) -> i64 {
        self.parent_shard_poll_interval_millis
    }

    pub fn skip_shard_sync_at_worker_initialization_if_leases_exist(&self) -> bool {
        self.skip_shard_sync_at_worker_initialization_if_leases_exist
    }

    pub fn shard_consumer_dispatch_poll_interval_millis(&self) -> i64 {
        self.shard_consumer_dispatch_poll_interval_millis
    }

    pub fn shard_prioritization(&self) -> &Arc<dyn ShardPrioritization + Send + Sync> {
        &self.shard_prioritization
    }

    pub fn worker_state_change_listener(
        &self,
    ) -> &Arc<dyn WorkerStateChangeListener + Send + Sync> {
        &self.worker_state_change_listener
    }

    pub fn coordinator_factory(&self) -> &Arc<dyn CoordinatorFactory + Send + Sync> {
        &self.coordinator_factory
    }

    pub fn scheduler_initialization_backoff_time_millis(&self) -> i64 {
        self.scheduler_initialization_backoff_time_millis
    }

    pub fn client_version_config(&self) -> ClientVersionConfig {
        self.client_version_config
    }

    pub fn migrate_all_entities_to_lease_table(&self) -> bool {
        self.migrate_all_entities_to_lease_table
    }

    pub fn table_migration_complete_bake_time_seconds(&self) -> i64 {
        self.table_migration_complete_bake_time_seconds
    }

    pub fn coordinator_state_table_config(&self) -> &CoordinatorStateTableConfig {
        &self.coordinator_state_table_config
    }

    /// Java `effectiveTableMigrationCompleteBakeTimeSeconds()` — clamped to
    /// `[1 hour, 1 week]`.
    pub fn effective_table_migration_complete_bake_time_seconds(&self) -> i64 {
        TABLE_MIGRATION_COMPLETE_BAKE_TIME_MIN_SECONDS.max(
            TABLE_MIGRATION_COMPLETE_BAKE_TIME_MAX_SECONDS
                .min(self.table_migration_complete_bake_time_seconds),
        )
    }

    // ---- fluent setters (chainable, return Self) ----

    pub fn set_max_initialization_attempts(mut self, v: i32) -> Self {
        self.max_initialization_attempts = v;
        self
    }

    pub fn set_parent_shard_poll_interval_millis(mut self, v: i64) -> Self {
        self.parent_shard_poll_interval_millis = v;
        self
    }

    pub fn set_skip_shard_sync_at_worker_initialization_if_leases_exist(mut self, v: bool) -> Self {
        self.skip_shard_sync_at_worker_initialization_if_leases_exist = v;
        self
    }

    pub fn set_shard_consumer_dispatch_poll_interval_millis(mut self, v: i64) -> Self {
        self.shard_consumer_dispatch_poll_interval_millis = v;
        self
    }

    pub fn set_shard_prioritization(
        mut self,
        v: Arc<dyn ShardPrioritization + Send + Sync>,
    ) -> Self {
        self.shard_prioritization = v;
        self
    }

    pub fn set_worker_state_change_listener(
        mut self,
        v: Arc<dyn WorkerStateChangeListener + Send + Sync>,
    ) -> Self {
        self.worker_state_change_listener = v;
        self
    }

    pub fn set_coordinator_factory(mut self, v: Arc<dyn CoordinatorFactory + Send + Sync>) -> Self {
        self.coordinator_factory = v;
        self
    }

    pub fn set_scheduler_initialization_backoff_time_millis(mut self, v: i64) -> Self {
        self.scheduler_initialization_backoff_time_millis = v;
        self
    }

    pub fn set_client_version_config(mut self, v: ClientVersionConfig) -> Self {
        self.client_version_config = v;
        self
    }

    pub fn set_migrate_all_entities_to_lease_table(mut self, v: bool) -> Self {
        self.migrate_all_entities_to_lease_table = v;
        self
    }

    pub fn set_table_migration_complete_bake_time_seconds(mut self, v: i64) -> Self {
        self.table_migration_complete_bake_time_seconds = v;
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const APPLICATION_NAME: &str = "TestApp";

    #[test]
    fn default_client_version_config_is_3x() {
        let config = CoordinatorConfig::new(APPLICATION_NAME);
        assert_eq!(
            config.client_version_config(),
            ClientVersionConfig::ClientVersionConfig3x
        );
    }

    #[test]
    fn default_migrate_all_entities_to_lease_table_is_false() {
        let config = CoordinatorConfig::new(APPLICATION_NAME);
        assert!(!config.migrate_all_entities_to_lease_table());
    }

    #[test]
    fn default_table_migration_complete_bake_time_seconds_is_one_day() {
        let config = CoordinatorConfig::new(APPLICATION_NAME);
        assert_eq!(
            config.table_migration_complete_bake_time_seconds(),
            DAY_SECONDS
        );
    }

    #[test]
    fn effective_bake_time_default_returns_default() {
        let config = CoordinatorConfig::new(APPLICATION_NAME);
        assert_eq!(
            config.effective_table_migration_complete_bake_time_seconds(),
            DAY_SECONDS
        );
    }

    #[test]
    fn effective_bake_time_below_min_clamped_to_min() {
        let config = CoordinatorConfig::new(APPLICATION_NAME)
            .set_table_migration_complete_bake_time_seconds(60);
        assert_eq!(
            config.effective_table_migration_complete_bake_time_seconds(),
            HOUR_SECONDS
        );
    }

    #[test]
    fn effective_bake_time_zero_clamped_to_min() {
        let config = CoordinatorConfig::new(APPLICATION_NAME)
            .set_table_migration_complete_bake_time_seconds(0);
        assert_eq!(
            config.effective_table_migration_complete_bake_time_seconds(),
            HOUR_SECONDS
        );
    }

    #[test]
    fn effective_bake_time_above_max_clamped_to_max() {
        let config = CoordinatorConfig::new(APPLICATION_NAME)
            .set_table_migration_complete_bake_time_seconds(30 * DAY_SECONDS);
        assert_eq!(
            config.effective_table_migration_complete_bake_time_seconds(),
            WEEK_SECONDS
        );
    }

    #[test]
    fn effective_bake_time_exactly_min_returns_min() {
        let config = CoordinatorConfig::new(APPLICATION_NAME)
            .set_table_migration_complete_bake_time_seconds(HOUR_SECONDS);
        assert_eq!(
            config.effective_table_migration_complete_bake_time_seconds(),
            HOUR_SECONDS
        );
    }

    #[test]
    fn effective_bake_time_exactly_max_returns_max() {
        let config = CoordinatorConfig::new(APPLICATION_NAME)
            .set_table_migration_complete_bake_time_seconds(WEEK_SECONDS);
        assert_eq!(
            config.effective_table_migration_complete_bake_time_seconds(),
            WEEK_SECONDS
        );
    }

    #[test]
    fn effective_bake_time_within_range_returns_value() {
        let two_days = 2 * DAY_SECONDS;
        let config = CoordinatorConfig::new(APPLICATION_NAME)
            .set_table_migration_complete_bake_time_seconds(two_days);
        assert_eq!(
            config.effective_table_migration_complete_bake_time_seconds(),
            two_days
        );
    }

    #[test]
    fn set_client_version_config_phase1() {
        let config = CoordinatorConfig::new(APPLICATION_NAME)
            .set_client_version_config(ClientVersionConfig::CompatibleWith2xPhase1);
        assert_eq!(
            config.client_version_config(),
            ClientVersionConfig::CompatibleWith2xPhase1
        );
    }

    #[test]
    fn set_client_version_config_phase2() {
        let config = CoordinatorConfig::new(APPLICATION_NAME)
            .set_client_version_config(ClientVersionConfig::CompatibleWith2x);
        assert_eq!(
            config.client_version_config(),
            ClientVersionConfig::CompatibleWith2x
        );
    }

    #[test]
    fn client_version_config_enum_has_all_expected_values() {
        // Java `testClientVersionConfigEnum_hasAllExpectedValues`: assert the
        // enum has exactly 3 variants and each expected value exists. Rust has
        // no `values()` reflection; enumerate the variants exhaustively so the
        // count is checked by the compiler (adding/removing a variant forces
        // this list to change) and assert each is distinct.
        let all = [
            ClientVersionConfig::CompatibleWith2xPhase1,
            ClientVersionConfig::CompatibleWith2x,
            ClientVersionConfig::ClientVersionConfig3x,
        ];
        assert_eq!(all.len(), 3);
        // Distinctness (mirrors assertNotNull on three distinct constants).
        assert_ne!(all[0], all[1]);
        assert_ne!(all[1], all[2]);
        assert_ne!(all[0], all[2]);
        // Exhaustive match guards against silently adding a fourth variant.
        for v in all {
            match v {
                ClientVersionConfig::CompatibleWith2xPhase1
                | ClientVersionConfig::CompatibleWith2x
                | ClientVersionConfig::ClientVersionConfig3x => {}
            }
        }
    }

    #[test]
    fn coordinator_state_table_config_default_table_name() {
        let config = CoordinatorConfig::new(APPLICATION_NAME);
        assert_eq!(
            config.coordinator_state_table_config().table_name(),
            "TestApp-CoordinatorState"
        );
    }

    #[test]
    fn set_migrate_all_entities_to_lease_table() {
        let config =
            CoordinatorConfig::new(APPLICATION_NAME).set_migrate_all_entities_to_lease_table(true);
        assert!(config.migrate_all_entities_to_lease_table());
    }

    #[test]
    fn defaults_match_java() {
        let config = CoordinatorConfig::new(APPLICATION_NAME);
        assert_eq!(config.max_initialization_attempts(), 20);
        assert_eq!(config.parent_shard_poll_interval_millis(), 10_000);
        assert!(!config.skip_shard_sync_at_worker_initialization_if_leases_exist());
        assert_eq!(config.shard_consumer_dispatch_poll_interval_millis(), 1_000);
        assert_eq!(config.scheduler_initialization_backoff_time_millis(), 1_000);
    }
}
