//! Port of
//! `software.amazon.kinesis.coordinator.migration.MigrationClientVersionStateInitializer`.

use std::sync::Arc;

use crate::coordinator::coordinator_config::ClientVersionConfig;
use crate::coordinator::coordinator_state_dao::CoordinatorStateAccess;
use crate::coordinator::migration::client_version::ClientVersion;
use crate::coordinator::migration::migration_state::{MigrationState, MIGRATION_HASH_KEY};
use crate::leases::exceptions::LeasingError;

/// Injectable RNG returning `random.nextDouble()` (0.0..1.0). Java `Random`.
pub type RandomDouble = Arc<dyn Fn() -> f64 + Send + Sync>;

const MAX_INITIALIZATION_RETRY: i32 = 1;
const INITIALIZATION_RETRY_DELAY_MILLIS: i64 = 1000;
const JITTER_FACTOR: f64 = 0.1;

/// One-shot, read-only computation of the state machine's starting
/// [`ClientVersion`] at KCL startup, combining the configured
/// [`ClientVersionConfig`] with the current [`MigrationState`] in DDB.
pub struct MigrationClientVersionStateInitializer {
    coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
    client_version_config: ClientVersionConfig,
    random: RandomDouble,
    worker_identifier: String,
}

impl MigrationClientVersionStateInitializer {
    /// Java constructor.
    pub fn new(
        coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
        client_version_config: ClientVersionConfig,
        random: RandomDouble,
        worker_identifier: impl Into<String>,
    ) -> Self {
        Self {
            coordinator_state_dao,
            client_version_config,
            random,
            worker_identifier: worker_identifier.into(),
        }
    }

    /// Java `getInitialState()`: `(ClientVersion, MigrationState)`. This is a
    /// **read-only** operation. On a DDB read failure the caller (Scheduler)
    /// retries the whole initialization.
    ///
    /// `InvalidStateException` is wrapped into `DependencyException` (here:
    /// `LeasingError::Dependency`).
    pub async fn get_initial_state(&self) -> Result<(ClientVersion, MigrationState), LeasingError> {
        tracing::info!(
            config = ?self.client_version_config,
            "Initializing migration state machine starting state"
        );
        match self.get_migration_state_from_dynamo().await {
            Ok(migration_state) => {
                let initial = self.get_client_version_for_initialization(&migration_state);
                tracing::info!(?initial, "Determined initial client version from DDB state");
                Ok((initial, migration_state))
            }
            Err(e) => {
                // InvalidState is non-retryable; the Java code wraps it into a
                // DependencyException. Other retryable failures already exhausted
                // the single attempt and surfaced as a generic error.
                tracing::error!(?e, "Unable to initialize state machine");
                Err(LeasingError::dependency_caused_by(
                    "Unable to determine initial state for migration state machine",
                    Box::new(e),
                ))
            }
        }
    }

    /// Java `getClientVersionForInitialization(MigrationState)` — pure decision
    /// function over the DDB-observed client version. See the class javadoc for
    /// the full decision table (ported verbatim).
    pub fn get_client_version_for_initialization(
        &self,
        migration_state: &MigrationState,
    ) -> ClientVersion {
        match migration_state.client_version() {
            ClientVersion::ClientVersionInit => {
                // No state in DDB: derive from configured version.
                let next = self.get_next_client_version_based_on_config_version();
                tracing::info!(?next, "Application is starting");
                next
            }
            ClientVersion::ClientVersion3xWithRollback => {
                if self.client_version_config == ClientVersionConfig::ClientVersionConfig3x {
                    // upgrade successful, allow transition to 3x.
                    ClientVersion::ClientVersion3x
                } else {
                    migration_state.client_version()
                }
            }
            ClientVersion::ClientVersion2x => migration_state.client_version(),
            ClientVersion::ClientVersionUpgradeFrom2x => migration_state.client_version(),
            ClientVersion::ClientVersion3x => migration_state.client_version(),
        }
    }

    fn get_next_client_version_based_on_config_version(&self) -> ClientVersion {
        match self.client_version_config {
            ClientVersionConfig::CompatibleWith2xPhase1 => ClientVersion::ClientVersionInit,
            ClientVersionConfig::CompatibleWith2x => ClientVersion::ClientVersionUpgradeFrom2x,
            ClientVersionConfig::ClientVersionConfig3x => ClientVersion::ClientVersion3x,
        }
    }

    /// Java `getMigrationStateFromDynamo()`: reads the DDB row with retries.
    /// Absent row -> a fresh local `MigrationState(INIT)`. Wrong type ->
    /// `InvalidState` (non-retryable).
    ///
    /// **Retry note (arch-map-flagged):** Java's `MAX_INITIALIZATION_RETRY=1`
    /// combined with the post-increment loop condition means the DDB read runs
    /// **exactly once**; this port preserves that single-attempt behavior.
    async fn get_migration_state_from_dynamo(&self) -> Result<MigrationState, LeasingError> {
        let mut retry_count = 0;
        loop {
            let can_retry = retry_count < MAX_INITIALIZATION_RETRY;
            retry_count += 1;
            match self.read_migration_state_once().await {
                Ok(state) => return Ok(state),
                Err(e) => {
                    // InvalidState is non-retryable; rethrow immediately.
                    if matches!(e, LeasingError::InvalidState { .. }) {
                        return Err(e);
                    }
                    if !can_retry {
                        return Err(LeasingError::dependency(format!(
                            "Failed to get MigrationState from DDB after {MAX_INITIALIZATION_RETRY} retries, giving up"
                        )));
                    }
                    let delay = self.get_initialization_retry_delay();
                    tracing::warn!(
                        ?e,
                        delay,
                        "Failed to get MigrationState from DDB, retry after delay"
                    );
                    if delay > 0 {
                        tokio::time::sleep(std::time::Duration::from_millis(delay as u64)).await;
                    }
                }
            }
        }
    }

    async fn read_migration_state_once(&self) -> Result<MigrationState, LeasingError> {
        let state = self
            .coordinator_state_dao
            .get_coordinator_state(MIGRATION_HASH_KEY)
            .await?;
        match state {
            None => {
                tracing::info!("No Migration state available in DDB");
                Ok(MigrationState::new(self.worker_identifier.clone()))
            }
            Some(cs) => match cs.as_migration_state() {
                Some(m) => Ok(m.clone()),
                None => Err(LeasingError::invalid_state(format!(
                    "Unexpected state found not confirming to MigrationState schema {cs:?}"
                ))),
            },
        }
    }

    fn get_initialization_retry_delay(&self) -> i64 {
        let jitter =
            ((self.random)() * JITTER_FACTOR * INITIALIZATION_RETRY_DELAY_MILLIS as f64) as i64;
        INITIALIZATION_RETRY_DELAY_MILLIS + jitter
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::coordinator::coordinator_state::CoordinatorState;
    use crate::coordinator::coordinator_state_dao::MockCoordinatorStateAccess;

    const WORKER_ID: &str = "testWorker";

    fn random_half() -> RandomDouble {
        Arc::new(|| 0.5)
    }

    fn initializer(
        dao: MockCoordinatorStateAccess,
        config: ClientVersionConfig,
    ) -> MigrationClientVersionStateInitializer {
        MigrationClientVersionStateInitializer::new(Arc::new(dao), config, random_half(), WORKER_ID)
    }

    fn migration_state_with(cv: ClientVersion) -> MigrationState {
        let mut s = MigrationState::new(WORKER_ID);
        s.update(cv, WORKER_ID);
        s
    }

    #[tokio::test]
    async fn phase1_config_no_state_in_ddb_returns_init() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| Ok(None));
        dao.expect_create_coordinator_state_if_not_exists().never();
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2xPhase1);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersionInit);
    }

    #[tokio::test]
    async fn phase1_config_with_existing_3x_with_rollback_returns_3x_with_rollback() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| {
            Ok(Some(CoordinatorState::MigrationState(
                migration_state_with(ClientVersion::ClientVersion3xWithRollback),
            )))
        });
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2xPhase1);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersion3xWithRollback);
    }

    #[tokio::test]
    async fn phase1_config_with_existing_2x_returns_2x() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| {
            Ok(Some(CoordinatorState::MigrationState(
                migration_state_with(ClientVersion::ClientVersion2x),
            )))
        });
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2xPhase1);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersion2x);
    }

    #[tokio::test]
    async fn phase1_config_with_existing_upgrade_from_2x_returns_upgrade_from_2x() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| {
            Ok(Some(CoordinatorState::MigrationState(
                migration_state_with(ClientVersion::ClientVersionUpgradeFrom2x),
            )))
        });
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2xPhase1);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersionUpgradeFrom2x);
    }

    #[tokio::test]
    async fn phase1_config_with_existing_3x_returns_3x() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| {
            Ok(Some(CoordinatorState::MigrationState(
                migration_state_with(ClientVersion::ClientVersion3x),
            )))
        });
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2xPhase1);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersion3x);
    }

    #[tokio::test]
    async fn phase2_config_no_state_in_ddb_returns_upgrade_from_2x() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| Ok(None));
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2x);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersionUpgradeFrom2x);
    }

    #[tokio::test]
    async fn phase2_config_with_3x_with_rollback_returns_3x_with_rollback() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| {
            Ok(Some(CoordinatorState::MigrationState(
                migration_state_with(ClientVersion::ClientVersion3xWithRollback),
            )))
        });
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2x);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersion3xWithRollback);
    }

    #[tokio::test]
    async fn phase3_config_no_state_in_ddb_returns_3x() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| Ok(None));
        let init = initializer(dao, ClientVersionConfig::ClientVersionConfig3x);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersion3x);
    }

    #[tokio::test]
    async fn phase3_config_with_3x_with_rollback_returns_3x() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| {
            Ok(Some(CoordinatorState::MigrationState(
                migration_state_with(ClientVersion::ClientVersion3xWithRollback),
            )))
        });
        let init = initializer(dao, ClientVersionConfig::ClientVersionConfig3x);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersion3x);
    }

    #[tokio::test]
    async fn phase3_config_with_2x_returns_2x() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state().returning(|_| {
            Ok(Some(CoordinatorState::MigrationState(
                migration_state_with(ClientVersion::ClientVersion2x),
            )))
        });
        let init = initializer(dao, ClientVersionConfig::ClientVersionConfig3x);
        let (cv, _) = init.get_initial_state().await.unwrap();
        assert_eq!(cv, ClientVersion::ClientVersion2x);
    }

    #[tokio::test]
    async fn get_initial_state_throws_when_ddb_read_fails() {
        let mut dao = MockCoordinatorStateAccess::new();
        dao.expect_get_coordinator_state()
            .returning(|_| Err(LeasingError::dependency("DDB unavailable")));
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2xPhase1);
        assert!(init.get_initial_state().await.is_err());
    }

    #[test]
    fn get_client_version_for_initialization_init_state_phase1_returns_init() {
        let dao = MockCoordinatorStateAccess::new();
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2xPhase1);
        let state = MigrationState::new(WORKER_ID);
        assert_eq!(
            init.get_client_version_for_initialization(&state),
            ClientVersion::ClientVersionInit
        );
    }

    #[test]
    fn get_client_version_for_initialization_init_state_phase2_returns_upgrade_from_2x() {
        let dao = MockCoordinatorStateAccess::new();
        let init = initializer(dao, ClientVersionConfig::CompatibleWith2x);
        let state = MigrationState::new(WORKER_ID);
        assert_eq!(
            init.get_client_version_for_initialization(&state),
            ClientVersion::ClientVersionUpgradeFrom2x
        );
    }

    #[test]
    fn get_client_version_for_initialization_init_state_phase3_returns_3x() {
        let dao = MockCoordinatorStateAccess::new();
        let init = initializer(dao, ClientVersionConfig::ClientVersionConfig3x);
        let state = MigrationState::new(WORKER_ID);
        assert_eq!(
            init.get_client_version_for_initialization(&state),
            ClientVersion::ClientVersion3x
        );
    }
}
