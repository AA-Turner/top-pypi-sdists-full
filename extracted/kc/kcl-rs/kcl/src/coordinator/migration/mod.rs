//! Port of `software.amazon.kinesis.coordinator.migration` — coordinator
//! sub-wave 10b.
//!
//! Two independent state machines:
//!
//! 1. **Client-version migration** (KCL v2.x -> v3.x behavior migration):
//!    [`MigrationStateMachine`] + [`MigrationStateMachineImpl`], the
//!    [`ClientVersion`] enum, the [`MigrationClientVersionState`] trait + the 5
//!    concrete states, [`MigrationClientVersionStateInitializer`],
//!    [`ClientVersionChangeMonitor`], and the persisted [`MigrationState`].
//! 2. **Table migration** (KCL 3.4 -> 3.5+ table consolidation):
//!    [`TableMigrationStateMachine`] + [`TableMigrationStateMachineImpl`],
//!    [`TableMigrationState`], [`TableMigrationStatus`],
//!    [`TableMigrationStatusProvider`] (+ [`DefaultTableMigrationStatusProvider`]),
//!    [`TableMigrationSummary`], and [`MigrationReadyMonitor`].
//!
//! # State-machine modeling (documented deviation)
//!
//! The client-version states are modeled as **trait-objects**
//! (`Box<dyn MigrationClientVersionState>`) rather than a closed enum. Each
//! concrete state owns its running monitor handles (interior-mutability
//! `Mutex`) and does per-state async `enter`/`leave` I/O; trait-objects keep
//! that ownership local to each state and let the state machine hold exactly one
//! active state at a time (mirroring Java's `currentMigrationClientVersionState`
//! field). The table-migration state machine keeps its status in a
//! `TableMigrationStatusProvider` and dispatches with a `match` on the current
//! status (Java has no state-object hierarchy there).
//!
//! # Monitors (documented deviation)
//!
//! Java's `ScheduledExecutorService.scheduleWithFixedDelay` is replaced by an
//! injectable [`MonitorScheduler`] seam. Production
//! ([`TokioMonitorScheduler`]) spawns a tokio task with an interval ticker and a
//! `Notify`-based stop; tests use a recording scheduler that captures the
//! periodic task closure so the polling logic can be driven synchronously —
//! preserving the exact `ArgumentCaptor<Runnable>.run()` structure of the Java
//! tests.

pub mod client_version;
pub mod client_version_change_monitor;
pub mod dynamic_migration_components_initializer;
pub mod migration_client_version_state;
pub mod migration_client_version_state_initializer;
pub mod migration_ready_monitor;
pub mod migration_state;
pub mod migration_state_machine;
pub mod monitor_scheduler;
pub mod table_migration_state;
pub mod table_migration_state_machine;
pub mod table_migration_status;
pub mod table_migration_status_provider;
pub mod table_migration_summary;

pub use client_version::ClientVersion;
pub use client_version_change_monitor::{ClientVersionChangeCallback, ClientVersionChangeMonitor};
pub use dynamic_migration_components_initializer::DynamicMigrationComponentsInitializer;
pub use migration_client_version_state::MigrationClientVersionState;
pub use migration_client_version_state_initializer::MigrationClientVersionStateInitializer;
pub use migration_ready_monitor::{MigrationReadyMonitor, WorkerMetricStatsSource};
pub use migration_state::{HistoryEntry, MigrationState, MIGRATION_HASH_KEY};
pub use migration_state_machine::{MigrationStateMachine, MigrationStateMachineImpl};
pub use monitor_scheduler::{MonitorScheduler, ScheduledHandle, TokioMonitorScheduler};
pub use table_migration_state::{TableMigrationState, TABLE_MIGRATION_HASH_KEY};
#[cfg(test)]
pub use table_migration_state_machine::MockTableMigrationStateMachine;
pub use table_migration_state_machine::{
    TableMigrationError, TableMigrationStateMachine, TableMigrationStateMachineImpl,
};
pub use table_migration_status::TableMigrationStatus;
pub use table_migration_status_provider::{
    DefaultTableMigrationStatusProvider, TableMigrationStatusProvider,
};
pub use table_migration_summary::TableMigrationSummary;
