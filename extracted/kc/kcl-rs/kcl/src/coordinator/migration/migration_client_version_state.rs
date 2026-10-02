//! Port of the `MigrationClientVersionState` interface + its 5 concrete states.
//!
//! # Modeling: trait-objects
//!
//! Java uses a State interface with `enter`/`leave`/`clientVersion`. Each state
//! owns per-state monitor handles and does async DDB I/O in `enter`/`leave`.
//! We model this as an `#[async_trait]` trait + concrete structs
//! (`Box<dyn MigrationClientVersionState + Send + Sync>`), matching Java's
//! one-active-state-at-a-time design. Interior mutability (`Mutex`) guards each
//! state's `entered`/`left` flags and monitor handles.
//!
//! ## Preserved Java flag bugs (flagged, not "fixed")
//!
//! - `MigrationClientVersion2xState.leave()` sets `left = false` (sibling states
//!   set `true`).
//! - `MigrationClientVersionUpgradeFrom2xState.leave()` sets `entered = false`
//!   but never `left = true`.
//! - Only `3xWithRollback` and `3x` set both flags consistently.
//!
//! These are preserved verbatim (a fresh state instance is built per
//! transition, so the practical blast radius is a stale monitor callback firing
//! after `leave()`).

use std::sync::{Arc, Mutex, Weak};

use async_trait::async_trait;

use crate::coordinator::coordinator_state::CoordinatorState;
use crate::coordinator::coordinator_state_dao::CoordinatorStateAccess;
use crate::coordinator::migration::client_version::ClientVersion;
use crate::coordinator::migration::client_version_change_monitor::{
    ClientVersionChangeCallback, ClientVersionChangeMonitor, RandomDouble,
};
use crate::coordinator::migration::dynamic_migration_components_initializer::DynamicMigrationComponentsInitializer;
use crate::coordinator::migration::migration_ready_monitor::{
    MigrationReadyMonitor, ReadyCallback, TimeProvider,
};
use crate::coordinator::migration::migration_state::MigrationState;
use crate::coordinator::migration::migration_state_machine::MigrationStateMachineImpl;
use crate::coordinator::migration::monitor_scheduler::MonitorScheduler;
use crate::leases::exceptions::LeasingError;
use crate::metrics::MetricsFactory;

/// Java `MigrationClientVersionState` interface.
#[async_trait]
pub trait MigrationClientVersionState: Send + Sync {
    /// Java `clientVersion()`.
    fn client_version(&self) -> ClientVersion;
    /// Java `enter(fromClientVersion)`.
    async fn enter(&self, from_client_version: ClientVersion) -> Result<(), LeasingError>;
    /// Java `leave()`.
    async fn leave(&self);
}

// ---------------------------------------------------------------------------
// Shared collaborators passed to each state (the state-machine construction ctx)
// ---------------------------------------------------------------------------

/// Bundle of collaborators the concrete states share (the arguments the Java
/// `MigrationStateMachineImpl.createMigrationClientVersionState` switch passes).
#[derive(Clone)]
pub struct StateContext {
    pub state_machine: Weak<MigrationStateMachineImpl>,
    pub time_provider: TimeProvider,
    pub coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
    pub scheduler: Arc<dyn MonitorScheduler>,
    pub initializer: Arc<dyn DynamicMigrationComponentsInitializer>,
    pub random: RandomDouble,
    pub worker_id: String,
    pub flip_to_3x_stabilizer_time_in_seconds: i64,
}

/// Shared `enter`/`leave` flag pair (Java `AbstractMigrationClientVersionState`
/// protected `entered`/`left`).
#[derive(Default)]
struct Flags {
    entered: bool,
    left: bool,
}

// ---------------------------------------------------------------------------
// Template-method helper for the four DDB-writing states (Java
// AbstractMigrationClientVersionState.ensureDdbStateMatchesClientVersion).
// ---------------------------------------------------------------------------

/// Ensures the DDB migration-state row matches `next_version`. No-op if already
/// matching. Otherwise: if the pre-mutation version was INIT, conditional
/// create; else conditional update with the pre-mutation expectation. All
/// non-Dependency exceptions become `Dependency` (Java behavior).
async fn ensure_ddb_state_matches_client_version(
    dao: &Arc<dyn CoordinatorStateAccess>,
    current: &Mutex<MigrationState>,
    next_version: ClientVersion,
    worker_id: &str,
) -> Result<(), LeasingError> {
    // Snapshot + decide under the lock, but perform DDB I/O outside it.
    enum Action {
        Noop,
        Create(MigrationState),
        Update {
            updated: MigrationState,
            expectation:
                std::collections::HashMap<String, aws_sdk_dynamodb::types::ExpectedAttributeValue>,
            previous: MigrationState,
        },
    }
    let action = {
        let mut cur = current.lock().expect("poisoned");
        if cur.client_version() == next_version {
            tracing::info!(
                ?next_version,
                "DDB migration state already matches, skipping update"
            );
            Action::Noop
        } else {
            let previous = cur.copy();
            cur.update(next_version, worker_id);
            if previous.client_version() == ClientVersion::ClientVersionInit {
                Action::Create(cur.clone())
            } else {
                Action::Update {
                    updated: cur.clone(),
                    expectation: previous.get_dynamo_client_version_expectation(),
                    previous,
                }
            }
        }
    };

    match action {
        Action::Noop => Ok(()),
        Action::Create(state) => {
            tracing::info!("Creating migration state");
            let created = dao
                .create_coordinator_state_if_not_exists(&CoordinatorState::MigrationState(state))
                .await?;
            if !created {
                return Err(LeasingError::dependency(format!(
                    "Failed to create migration state for {next_version:?}"
                )));
            }
            Ok(())
        }
        Action::Update {
            updated,
            expectation,
            previous,
        } => {
            tracing::info!(?previous, ?next_version, "Updating migration state");
            let updated_ok = dao
                .update_coordinator_state_with_expectation(
                    &CoordinatorState::MigrationState(updated),
                    expectation,
                )
                .await?;
            if !updated_ok {
                return Err(LeasingError::dependency(format!(
                    "Failed to update migration state to {next_version:?}, current DDB state: {previous:?}"
                )));
            }
            Ok(())
        }
    }
}

// ---------------------------------------------------------------------------
// CLIENT_VERSION_INIT — the only state that never touches DDB.
// ---------------------------------------------------------------------------

/// Java `MigrationClientVersionInitState`.
pub struct MigrationClientVersionInitState {
    initializer: Arc<dyn DynamicMigrationComponentsInitializer>,
    entered: Mutex<bool>,
}

impl MigrationClientVersionInitState {
    pub fn new(initializer: Arc<dyn DynamicMigrationComponentsInitializer>) -> Self {
        Self {
            initializer,
            entered: Mutex::new(false),
        }
    }
}

#[async_trait]
impl MigrationClientVersionState for MigrationClientVersionInitState {
    fn client_version(&self) -> ClientVersion {
        ClientVersion::ClientVersionInit
    }

    async fn enter(&self, _from: ClientVersion) -> Result<(), LeasingError> {
        {
            let mut entered = self.entered.lock().expect("poisoned");
            if *entered {
                tracing::info!("Already entered INIT state");
                return Ok(());
            }
            *entered = true;
        }
        tracing::info!("Entering Phase 1 INIT state - pure 2.x compatible mode");
        self.initializer
            .initialize_client_version_for_phase1()
            .await;
        Ok(())
    }

    async fn leave(&self) {
        tracing::info!("Leaving INIT state");
    }
}

// ---------------------------------------------------------------------------
// Helper: async fire-and-forget monitor cancellation (Java uses
// CompletableFuture.supplyAsync on the common pool to avoid deadlock).
// ---------------------------------------------------------------------------

fn spawn_cancel_client_version_monitor(monitor: Arc<ClientVersionChangeMonitor>) {
    tokio::spawn(async move {
        tracing::info!("Cancelling client version change monitor");
        monitor.cancel();
    });
}

fn spawn_cancel_migration_ready_monitor(monitor: Arc<MigrationReadyMonitor>) {
    tokio::spawn(async move {
        tracing::info!("Cancelling migration ready monitor");
        monitor.cancel();
    });
}

fn metrics_factory_of(ctx: &StateContext) -> Arc<dyn MetricsFactory + Send + Sync> {
    ctx.initializer.metrics_factory()
}

// ---------------------------------------------------------------------------
// CLIENT_VERSION_2X
// ---------------------------------------------------------------------------

/// Java `MigrationClientVersion2xState`.
pub struct MigrationClientVersion2xState {
    ctx: StateContext,
    current_migration_state: Mutex<MigrationState>,
    flags: Mutex<Flags>,
    roll_forward_monitor: Mutex<Option<Arc<ClientVersionChangeMonitor>>>,
}

impl MigrationClientVersion2xState {
    pub fn new(ctx: StateContext, migration_state: MigrationState) -> Arc<Self> {
        Arc::new(Self {
            ctx,
            current_migration_state: Mutex::new(migration_state),
            flags: Mutex::new(Flags::default()),
            roll_forward_monitor: Mutex::new(None),
        })
    }

    fn cancel_roll_forward_monitor(&self) {
        let monitor = self.roll_forward_monitor.lock().expect("poisoned").take();
        if let Some(m) = monitor {
            spawn_cancel_client_version_monitor(m);
        }
    }
}

#[async_trait]
impl MigrationClientVersionState for MigrationClientVersion2xState {
    fn client_version(&self) -> ClientVersion {
        ClientVersion::ClientVersion2x
    }

    async fn enter(&self, from: ClientVersion) -> Result<(), LeasingError> {
        {
            let flags = self.flags.lock().expect("poisoned");
            if flags.entered {
                tracing::info!("Not entering already-entered/exited 2x state");
                return Ok(());
            }
        }
        ensure_ddb_state_matches_client_version(
            &self.ctx.coordinator_state_dao,
            &self.current_migration_state,
            self.client_version(),
            &self.ctx.worker_id,
        )
        .await?;
        // doEnter
        self.ctx
            .initializer
            .initialize_client_version_for_2x(from)
            .await;
        tracing::info!("Starting roll-forward monitor");
        let monitor = build_client_version_change_monitor(
            &self.ctx,
            self.client_version(),
            make_on_client_version_change_2x(self.ctx.clone()),
        );
        monitor.start_monitor();
        *self.roll_forward_monitor.lock().expect("poisoned") = Some(monitor);
        self.flags.lock().expect("poisoned").entered = true;
        Ok(())
    }

    async fn leave(&self) {
        let flags = self.flags.lock().expect("poisoned");
        if flags.entered && !flags.left {
            tracing::info!("Leaving 2x state");
            drop(flags);
            self.cancel_roll_forward_monitor();
            // BUG preserved: Java sets left = false here (should be true).
            self.flags.lock().expect("poisoned").left = false;
        } else {
            tracing::info!("Cannot leave 2x state (not active)");
        }
    }
}

// ---------------------------------------------------------------------------
// CLIENT_VERSION_UPGRADE_FROM_2X
// ---------------------------------------------------------------------------

/// Java `MigrationClientVersionUpgradeFrom2xState`.
pub struct MigrationClientVersionUpgradeFrom2xState {
    ctx: StateContext,
    current_migration_state: Mutex<MigrationState>,
    flags: Mutex<Flags>,
    migration_monitor: Mutex<Option<Arc<MigrationReadyMonitor>>>,
    client_version_change_monitor: Mutex<Option<Arc<ClientVersionChangeMonitor>>>,
    /// The mutable current state used by `on_migration_ready` (Java
    /// `curentMigrationState`), shared with the enter path.
    self_arc: Mutex<Weak<MigrationClientVersionUpgradeFrom2xState>>,
}

impl MigrationClientVersionUpgradeFrom2xState {
    pub fn new(ctx: StateContext, migration_state: MigrationState) -> Arc<Self> {
        let arc = Arc::new(Self {
            ctx,
            current_migration_state: Mutex::new(migration_state),
            flags: Mutex::new(Flags::default()),
            migration_monitor: Mutex::new(None),
            client_version_change_monitor: Mutex::new(None),
            self_arc: Mutex::new(Weak::new()),
        });
        *arc.self_arc.lock().expect("poisoned") = Arc::downgrade(&arc);
        arc
    }

    fn cancel_migration_ready_monitor(&self) {
        let m = self.migration_monitor.lock().expect("poisoned").take();
        if let Some(m) = m {
            spawn_cancel_migration_ready_monitor(m);
        }
    }

    fn cancel_client_change_version_monitor(&self) {
        let m = self
            .client_version_change_monitor
            .lock()
            .expect("poisoned")
            .take();
        if let Some(m) = m {
            spawn_cancel_client_version_monitor(m);
        }
    }

    /// Java `onMigrationReady()` (leader-only). Idempotent via the
    /// `migration_monitor == null` guard.
    async fn on_migration_ready(self: Arc<Self>) {
        {
            let flags = self.flags.lock().expect("poisoned");
            let has_monitor = self.migration_monitor.lock().expect("poisoned").is_some();
            if !flags.entered || flags.left || !has_monitor {
                tracing::info!("Ignoring migration ready, state already transitioned");
                return;
            }
        }
        if self.update_dynamo_state_for_transition().await {
            self.cancel_migration_ready_monitor();
        }
    }

    async fn update_dynamo_state_for_transition(&self) -> bool {
        let (new_state, expectation) = {
            let cur = self.current_migration_state.lock().expect("poisoned");
            let mut new_state = cur.copy();
            new_state.update(
                ClientVersion::ClientVersion3xWithRollback,
                &self.ctx.worker_id,
            );
            (new_state, cur.get_dynamo_client_version_expectation())
        };
        tracing::info!("Updating Migration State in DDB to 3x with rollback");
        match self
            .ctx
            .coordinator_state_dao
            .update_coordinator_state_with_expectation(
                &CoordinatorState::MigrationState(new_state),
                expectation,
            )
            .await
        {
            Ok(updated) => updated,
            Err(e) => {
                tracing::warn!(
                    ?e,
                    "Exception toggling to 3x with rollback, monitor will retry"
                );
                false
            }
        }
    }
}

#[async_trait]
impl MigrationClientVersionState for MigrationClientVersionUpgradeFrom2xState {
    fn client_version(&self) -> ClientVersion {
        ClientVersion::ClientVersionUpgradeFrom2x
    }

    async fn enter(&self, from: ClientVersion) -> Result<(), LeasingError> {
        {
            let flags = self.flags.lock().expect("poisoned");
            if flags.entered {
                tracing::info!("Not entering already-entered upgrade-from-2x state");
                return Ok(());
            }
        }
        ensure_ddb_state_matches_client_version(
            &self.ctx.coordinator_state_dao,
            &self.current_migration_state,
            self.client_version(),
            &self.ctx.worker_id,
        )
        .await?;
        // doEnter
        self.ctx
            .initializer
            .initialize_client_version_for_upgrade_from_2x(from)
            .await?;

        tracing::info!("Starting migration ready monitor");
        let self_weak = self.self_arc.lock().expect("poisoned").clone();
        let ready_cb: ReadyCallback = {
            let self_weak = self_weak.clone();
            Arc::new(move || {
                let self_weak = self_weak.clone();
                Box::pin(async move {
                    // Java onMigrationReady runs synchronously inside the monitor
                    // tick; we run it inline here.
                    if let Some(state) = self_weak.upgrade() {
                        state.on_migration_ready().await;
                    }
                })
                    as std::pin::Pin<Box<dyn std::future::Future<Output = ()> + Send>>
            })
        };
        let migration_monitor = Arc::new(MigrationReadyMonitor::new(
            metrics_factory_of(&self.ctx),
            self.ctx.time_provider.clone(),
            self.ctx.initializer.leader_decider(),
            self.ctx.initializer.worker_identifier(),
            self.ctx.initializer.worker_metrics_dao(),
            self.ctx.initializer.worker_metrics_expiry_seconds(),
            self.ctx.initializer.lease_refresher(),
            self.ctx.scheduler.clone(),
            ready_cb,
            self.ctx.flip_to_3x_stabilizer_time_in_seconds,
        ));
        migration_monitor.start_monitor();
        *self.migration_monitor.lock().expect("poisoned") = Some(migration_monitor);

        tracing::info!("Starting monitor for rollback and flip to 3.x");
        let cv_monitor = build_client_version_change_monitor(
            &self.ctx,
            self.client_version(),
            make_on_client_version_change_upgrade_from_2x(self.ctx.clone(), self_weak),
        );
        cv_monitor.start_monitor();
        *self.client_version_change_monitor.lock().expect("poisoned") = Some(cv_monitor);

        self.flags.lock().expect("poisoned").entered = true;
        Ok(())
    }

    async fn leave(&self) {
        let flags_active = {
            let flags = self.flags.lock().expect("poisoned");
            flags.entered && !flags.left
        };
        if flags_active {
            tracing::info!("Leaving upgrade-from-2x state");
            self.cancel_migration_ready_monitor();
            self.cancel_client_change_version_monitor();
            // BUG preserved: Java sets entered = false but never left = true.
            self.flags.lock().expect("poisoned").entered = false;
        } else {
            tracing::info!("Cannot leave upgrade-from-2x state (not active)");
        }
    }
}

// ---------------------------------------------------------------------------
// CLIENT_VERSION_3X_WITH_ROLLBACK
// ---------------------------------------------------------------------------

/// Java `MigrationClientVersion3xWithRollbackState`.
pub struct MigrationClientVersion3xWithRollbackState {
    ctx: StateContext,
    current_migration_state: Mutex<MigrationState>,
    flags: Mutex<Flags>,
    rollback_monitor: Mutex<Option<Arc<ClientVersionChangeMonitor>>>,
}

impl MigrationClientVersion3xWithRollbackState {
    pub fn new(ctx: StateContext, migration_state: MigrationState) -> Arc<Self> {
        Arc::new(Self {
            ctx,
            current_migration_state: Mutex::new(migration_state),
            flags: Mutex::new(Flags::default()),
            rollback_monitor: Mutex::new(None),
        })
    }

    fn cancel_rollback_monitor(&self) {
        let m = self.rollback_monitor.lock().expect("poisoned").take();
        if let Some(m) = m {
            spawn_cancel_client_version_monitor(m);
        }
    }
}

#[async_trait]
impl MigrationClientVersionState for MigrationClientVersion3xWithRollbackState {
    fn client_version(&self) -> ClientVersion {
        ClientVersion::ClientVersion3xWithRollback
    }

    async fn enter(&self, from: ClientVersion) -> Result<(), LeasingError> {
        {
            let flags = self.flags.lock().expect("poisoned");
            if flags.entered {
                tracing::info!("Not entering already-entered 3x-with-rollback state");
                return Ok(());
            }
        }
        ensure_ddb_state_matches_client_version(
            &self.ctx.coordinator_state_dao,
            &self.current_migration_state,
            self.client_version(),
            &self.ctx.worker_id,
        )
        .await?;
        self.ctx
            .initializer
            .initialize_client_version_for_3x_with_rollback(from)
            .await?;
        tracing::info!("Starting rollback monitor");
        let monitor = build_client_version_change_monitor(
            &self.ctx,
            self.client_version(),
            make_on_client_version_change_3x_with_rollback(self.ctx.clone()),
        );
        monitor.start_monitor();
        *self.rollback_monitor.lock().expect("poisoned") = Some(monitor);
        self.flags.lock().expect("poisoned").entered = true;
        Ok(())
    }

    async fn leave(&self) {
        let active = {
            let flags = self.flags.lock().expect("poisoned");
            flags.entered && !flags.left
        };
        if active {
            tracing::info!("Leaving 3x-with-rollback state");
            self.cancel_rollback_monitor();
            let mut flags = self.flags.lock().expect("poisoned");
            flags.entered = false;
            flags.left = true;
        } else {
            tracing::info!("Cannot leave 3x-with-rollback state (not active)");
        }
    }
}

// ---------------------------------------------------------------------------
// CLIENT_VERSION_3X (terminal)
// ---------------------------------------------------------------------------

/// Java `MigrationClientVersion3xState`.
pub struct MigrationClientVersion3xState {
    ctx: StateContext,
    current_migration_state: Mutex<MigrationState>,
    flags: Mutex<Flags>,
}

impl MigrationClientVersion3xState {
    pub fn new(ctx: StateContext, migration_state: MigrationState) -> Arc<Self> {
        Arc::new(Self {
            ctx,
            current_migration_state: Mutex::new(migration_state),
            flags: Mutex::new(Flags::default()),
        })
    }
}

#[async_trait]
impl MigrationClientVersionState for MigrationClientVersion3xState {
    fn client_version(&self) -> ClientVersion {
        ClientVersion::ClientVersion3x
    }

    async fn enter(&self, from: ClientVersion) -> Result<(), LeasingError> {
        {
            let flags = self.flags.lock().expect("poisoned");
            if flags.entered {
                tracing::info!("Not entering already-entered 3x state");
                return Ok(());
            }
        }
        ensure_ddb_state_matches_client_version(
            &self.ctx.coordinator_state_dao,
            &self.current_migration_state,
            self.client_version(),
            &self.ctx.worker_id,
        )
        .await?;
        self.ctx
            .initializer
            .initialize_client_version_for_3x(from)
            .await?;
        self.flags.lock().expect("poisoned").entered = true;
        Ok(())
    }

    async fn leave(&self) {
        let mut flags = self.flags.lock().expect("poisoned");
        if flags.entered && !flags.left {
            tracing::info!("Leaving 3x state");
            flags.entered = false;
            flags.left = true;
        } else {
            tracing::info!("Cannot leave 3x state (not active)");
        }
    }
}

// ---------------------------------------------------------------------------
// Callback construction helpers (Java's `this::onClientVersionChange`).
// ---------------------------------------------------------------------------

fn build_client_version_change_monitor(
    ctx: &StateContext,
    expected: ClientVersion,
    callback: ClientVersionChangeCallback,
) -> Arc<ClientVersionChangeMonitor> {
    Arc::new(ClientVersionChangeMonitor::new(
        metrics_factory_of(ctx),
        ctx.coordinator_state_dao.clone(),
        ctx.scheduler.clone(),
        callback,
        expected,
        ctx.random.clone(),
    ))
}

/// 2X `onClientVersionChange`: only UPGRADE_FROM_2X is valid.
fn make_on_client_version_change_2x(ctx: StateContext) -> ClientVersionChangeCallback {
    Arc::new(move |new_state: MigrationState| {
        let ctx = ctx.clone();
        Box::pin(async move {
            if new_state.client_version() == ClientVersion::ClientVersionUpgradeFrom2x {
                tracing::info!("Roll-forward initiated, transition to UPGRADE_FROM_2X");
                transition(&ctx, ClientVersion::ClientVersionUpgradeFrom2x, new_state).await
            } else {
                tracing::error!(
                    ?new_state,
                    "Invalid client version, transition from 2x unsupported"
                );
                Err(LeasingError::invalid_state(format!(
                    "Unexpected new state {new_state:?}"
                )))
            }
        }) as _
    })
}

/// UPGRADE_FROM_2X `onClientVersionChange`: 2X or 3X_WITH_ROLLBACK.
fn make_on_client_version_change_upgrade_from_2x(
    ctx: StateContext,
    state_weak: Weak<MigrationClientVersionUpgradeFrom2xState>,
) -> ClientVersionChangeCallback {
    Arc::new(move |new_state: MigrationState| {
        let ctx = ctx.clone();
        let state_weak = state_weak.clone();
        Box::pin(async move {
            match new_state.client_version() {
                ClientVersion::ClientVersion2x => {
                    tracing::info!("Rollback initiated, transition to 2X");
                    if let Some(state) = state_weak.upgrade() {
                        state.cancel_migration_ready_monitor();
                    }
                    transition(&ctx, ClientVersion::ClientVersion2x, new_state).await
                }
                ClientVersion::ClientVersion3xWithRollback => {
                    tracing::info!("Workers 3.x compliant, transition to 3X_WITH_ROLLBACK");
                    if let Some(state) = state_weak.upgrade() {
                        state.cancel_migration_ready_monitor();
                    }
                    transition(&ctx, ClientVersion::ClientVersion3xWithRollback, new_state).await
                }
                _ => {
                    tracing::error!(?new_state, "Invalid client version");
                    Err(LeasingError::invalid_state(format!(
                        "Unexpected new state {new_state:?}"
                    )))
                }
            }
        }) as _
    })
}

/// 3X_WITH_ROLLBACK `onClientVersionChange`: 2X or 3X (terminal).
fn make_on_client_version_change_3x_with_rollback(
    ctx: StateContext,
) -> ClientVersionChangeCallback {
    Arc::new(move |new_state: MigrationState| {
        let ctx = ctx.clone();
        Box::pin(async move {
            match new_state.client_version() {
                ClientVersion::ClientVersion2x => {
                    tracing::info!("Rollback initiated, transition to 2X");
                    transition(&ctx, ClientVersion::ClientVersion2x, new_state).await
                }
                ClientVersion::ClientVersion3x => {
                    tracing::info!("Customer switched to 3.x, moving to terminal state");
                    transition(&ctx, ClientVersion::ClientVersion3x, new_state).await
                }
                _ => {
                    tracing::error!(?new_state, "Invalid client version");
                    Err(LeasingError::invalid_state(format!(
                        "Unexpected new state {new_state:?}"
                    )))
                }
            }
        }) as _
    })
}

/// Wraps `state_machine.transition_to(...)`, upgrading the weak reference.
async fn transition(
    ctx: &StateContext,
    next: ClientVersion,
    state: MigrationState,
) -> Result<(), LeasingError> {
    match ctx.state_machine.upgrade() {
        Some(sm) => sm.transition_to(next, state).await,
        None => Ok(()),
    }
}

// re-exports for construction elsewhere are via the module.

// ---------------------------------------------------------------------------
// Tests — port of MigrationClientVersionInitStateTest.java
// ---------------------------------------------------------------------------
#[cfg(test)]
mod tests {
    use super::*;
    use crate::coordinator::migration::dynamic_migration_components_initializer::MockDynamicMigrationComponentsInitializer;

    /// Java `MigrationClientVersionInitStateTest#testClientVersion_returnsInit`.
    #[tokio::test]
    async fn client_version_returns_init() {
        let initializer = MockDynamicMigrationComponentsInitializer::new();
        let state = MigrationClientVersionInitState::new(Arc::new(initializer));
        assert_eq!(ClientVersion::ClientVersionInit, state.client_version());
    }

    /// Java `MigrationClientVersionInitStateTest#testEnter_callsInitializeClientVersionForPhase1`.
    #[tokio::test]
    async fn enter_calls_initialize_client_version_for_phase1() {
        let mut initializer = MockDynamicMigrationComponentsInitializer::new();
        initializer
            .expect_initialize_client_version_for_phase1()
            .times(1)
            .returning(|| ());
        let state = MigrationClientVersionInitState::new(Arc::new(initializer));

        state.enter(ClientVersion::ClientVersionInit).await.unwrap();
    }

    /// Java `MigrationClientVersionInitStateTest#testEnter_idempotent_doesNotReinitialize`.
    #[tokio::test]
    async fn enter_idempotent_does_not_reinitialize() {
        let mut initializer = MockDynamicMigrationComponentsInitializer::new();
        // Should only be called once due to the entered flag.
        initializer
            .expect_initialize_client_version_for_phase1()
            .times(1)
            .returning(|| ());
        let state = MigrationClientVersionInitState::new(Arc::new(initializer));

        state.enter(ClientVersion::ClientVersionInit).await.unwrap();
        state.enter(ClientVersion::ClientVersionInit).await.unwrap();
    }

    /// Java `MigrationClientVersionInitStateTest#testEnter_fromAnyClientVersion_callsPhase1Init`.
    #[tokio::test]
    async fn enter_from_any_client_version_calls_phase1_init() {
        let mut initializer = MockDynamicMigrationComponentsInitializer::new();
        initializer
            .expect_initialize_client_version_for_phase1()
            .times(1)
            .returning(|| ());
        let state = MigrationClientVersionInitState::new(Arc::new(initializer));

        state
            .enter(ClientVersion::ClientVersionUpgradeFrom2x)
            .await
            .unwrap();
    }

    /// Java `MigrationClientVersionInitStateTest#testLeave_doesNotThrow`.
    #[tokio::test]
    async fn leave_does_not_throw() {
        let mut initializer = MockDynamicMigrationComponentsInitializer::new();
        initializer
            .expect_initialize_client_version_for_phase1()
            .returning(|| ());
        let state = MigrationClientVersionInitState::new(Arc::new(initializer));

        state.enter(ClientVersion::ClientVersionInit).await.unwrap();
        // leave() should not panic.
        state.leave().await;
    }

    /// Java `MigrationClientVersionInitStateTest#testLeave_withoutEnter_doesNotThrow`.
    #[tokio::test]
    async fn leave_without_enter_does_not_throw() {
        let initializer = MockDynamicMigrationComponentsInitializer::new();
        let state = MigrationClientVersionInitState::new(Arc::new(initializer));

        // leave() should be safe to call even without enter.
        state.leave().await;
    }

    /// Java `MigrationClientVersionInitStateTest#testEnter_thenLeave_thenEnter_doesNotReinitialize`.
    #[tokio::test]
    async fn enter_then_leave_then_enter_does_not_reinitialize() {
        let mut initializer = MockDynamicMigrationComponentsInitializer::new();
        // Even after leave, re-entering should not reinitialize (entered flag is permanent).
        initializer
            .expect_initialize_client_version_for_phase1()
            .times(1)
            .returning(|| ());
        let state = MigrationClientVersionInitState::new(Arc::new(initializer));

        state.enter(ClientVersion::ClientVersionInit).await.unwrap();
        state.leave().await;
        state.enter(ClientVersion::ClientVersionInit).await.unwrap();
    }
}
