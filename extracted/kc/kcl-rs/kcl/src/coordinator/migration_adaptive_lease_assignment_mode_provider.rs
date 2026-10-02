//! Port of
//! `software.amazon.kinesis.coordinator.MigrationAdaptiveLeaseAssignmentModeProvider`.

use std::sync::Mutex;

/// The lease-assignment mode KCL operates in. Java nested
/// `MigrationAdaptiveLeaseAssignmentModeProvider.LeaseAssignmentMode`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum LeaseAssignmentMode {
    /// 2.x mode — lease-count-based assignment (each worker independently
    /// picks/steals leases).
    DefaultLeaseCountBasedAssignment,
    /// 3.x mode — worker-utilization-aware assignment (leader assigns based on
    /// `WorkerMetricStats`).
    WorkerUtilizationAwareAssignment,
}

/// Error returned by the mode provider for reachable ordering/config bugs (Java
/// throws `IllegalStateException`; the arch-map recommends `Result` over
/// `panic!` here since these are reachable via configuration).
#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum ModeProviderError {
    #[error("AssignmentMode is not initialized")]
    NotInitialized,
    #[error(
        "Lease assignment mode already initialized to {current:?} cannot change to {requested:?}"
    )]
    DynamicChangeNotSupported {
        current: LeaseAssignmentMode,
        requested: LeaseAssignmentMode,
    },
}

#[derive(Debug, Default)]
struct State {
    current_mode: Option<LeaseAssignmentMode>,
    initialized: bool,
    dynamic_mode_change_support_needed: bool,
}

/// Holds the live [`LeaseAssignmentMode`] that both lease-assignment algorithms
/// consult concurrently, plus whether dynamic mode-switching is permitted.
/// Java `MigrationAdaptiveLeaseAssignmentModeProvider` (`@ThreadSafe`,
/// `@NoArgsConstructor`).
///
/// Java guards every method with `synchronized(this)`; the Rust port uses a
/// single `Mutex<State>`.
#[derive(Debug, Default)]
pub struct MigrationAdaptiveLeaseAssignmentModeProvider {
    state: Mutex<State>,
}

impl MigrationAdaptiveLeaseAssignmentModeProvider {
    /// Java `@NoArgsConstructor`.
    pub fn new() -> Self {
        Self::default()
    }

    /// Java `dynamicModeChangeSupportNeeded()`.
    pub fn dynamic_mode_change_support_needed(&self) -> bool {
        self.lock().dynamic_mode_change_support_needed
    }

    /// Java `getLeaseAssignmentMode()` — errors (`IllegalStateException`) if not
    /// yet initialized.
    pub fn get_lease_assignment_mode(&self) -> Result<LeaseAssignmentMode, ModeProviderError> {
        let state = self.lock();
        if !state.initialized {
            return Err(ModeProviderError::NotInitialized);
        }
        Ok(state.current_mode.expect("initialized implies mode set"))
    }

    /// Java package-visible `initialize(boolean, LeaseAssignmentMode)` —
    /// idempotent (a second call logs and ignores the new values).
    pub fn initialize(&self, dynamic_mode_change_support_needed: bool, mode: LeaseAssignmentMode) {
        let mut state = self.lock();
        if !state.initialized {
            tracing::info!(
                dynamic_mode_change_support_needed,
                ?mode,
                "Initializing lease assignment mode provider"
            );
            state.dynamic_mode_change_support_needed = dynamic_mode_change_support_needed;
            state.current_mode = Some(mode);
            state.initialized = true;
            return;
        }
        tracing::info!(
            current_dynamic = state.dynamic_mode_change_support_needed,
            current_mode = ?state.current_mode,
            "Already initialized; ignoring new values"
        );
    }

    /// Java package-visible `updateLeaseAssignmentMode(LeaseAssignmentMode)` —
    /// errors if not initialized or if dynamic mode change is not supported.
    pub fn update_lease_assignment_mode(
        &self,
        mode: LeaseAssignmentMode,
    ) -> Result<(), ModeProviderError> {
        let mut state = self.lock();
        if !state.initialized {
            return Err(ModeProviderError::NotInitialized);
        }
        if state.dynamic_mode_change_support_needed {
            tracing::info!(from = ?state.current_mode, to = ?mode, "Changing lease assignment mode");
            state.current_mode = Some(mode);
            return Ok(());
        }
        Err(ModeProviderError::DynamicChangeNotSupported {
            current: state.current_mode.expect("initialized implies mode set"),
            requested: mode,
        })
    }

    fn lock(&self) -> std::sync::MutexGuard<'_, State> {
        self.state.lock().expect("mode provider mutex poisoned")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn get_before_initialize_errors() {
        let p = MigrationAdaptiveLeaseAssignmentModeProvider::new();
        assert_eq!(
            p.get_lease_assignment_mode(),
            Err(ModeProviderError::NotInitialized)
        );
    }

    #[test]
    fn initialize_sets_mode_and_dynamic_flag() {
        let p = MigrationAdaptiveLeaseAssignmentModeProvider::new();
        p.initialize(true, LeaseAssignmentMode::DefaultLeaseCountBasedAssignment);
        assert!(p.dynamic_mode_change_support_needed());
        assert_eq!(
            p.get_lease_assignment_mode().unwrap(),
            LeaseAssignmentMode::DefaultLeaseCountBasedAssignment
        );
    }

    #[test]
    fn initialize_is_idempotent() {
        let p = MigrationAdaptiveLeaseAssignmentModeProvider::new();
        p.initialize(false, LeaseAssignmentMode::WorkerUtilizationAwareAssignment);
        // Second initialize is ignored.
        p.initialize(true, LeaseAssignmentMode::DefaultLeaseCountBasedAssignment);
        assert!(!p.dynamic_mode_change_support_needed());
        assert_eq!(
            p.get_lease_assignment_mode().unwrap(),
            LeaseAssignmentMode::WorkerUtilizationAwareAssignment
        );
    }

    #[test]
    fn update_before_initialize_errors() {
        let p = MigrationAdaptiveLeaseAssignmentModeProvider::new();
        assert_eq!(
            p.update_lease_assignment_mode(LeaseAssignmentMode::WorkerUtilizationAwareAssignment),
            Err(ModeProviderError::NotInitialized)
        );
    }

    #[test]
    fn update_with_dynamic_support_succeeds() {
        let p = MigrationAdaptiveLeaseAssignmentModeProvider::new();
        p.initialize(true, LeaseAssignmentMode::DefaultLeaseCountBasedAssignment);
        p.update_lease_assignment_mode(LeaseAssignmentMode::WorkerUtilizationAwareAssignment)
            .unwrap();
        assert_eq!(
            p.get_lease_assignment_mode().unwrap(),
            LeaseAssignmentMode::WorkerUtilizationAwareAssignment
        );
    }

    #[test]
    fn update_without_dynamic_support_errors() {
        let p = MigrationAdaptiveLeaseAssignmentModeProvider::new();
        p.initialize(false, LeaseAssignmentMode::DefaultLeaseCountBasedAssignment);
        assert_eq!(
            p.update_lease_assignment_mode(LeaseAssignmentMode::WorkerUtilizationAwareAssignment),
            Err(ModeProviderError::DynamicChangeNotSupported {
                current: LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
                requested: LeaseAssignmentMode::WorkerUtilizationAwareAssignment,
            })
        );
    }
}
