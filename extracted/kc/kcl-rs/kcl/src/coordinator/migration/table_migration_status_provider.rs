//! Port of `software.amazon.kinesis.coordinator.migration.TableMigrationStatusProvider`.
//!
//! # Trait vs concrete split (unifies the two former stubs)
//!
//! Java has a single concrete `TableMigrationStatusProvider` class. The DAO
//! layers (`CoordinatorStateDAO`, `WorkerMetricStatsDAO`) only read
//! `getTableMigrationStatus()` and are unit-tested against a mock. To preserve
//! that, the read surface is the [`TableMigrationStatusProvider`] **trait**
//! (`#[automock]`), and the real holder is [`DefaultTableMigrationStatusProvider`],
//! which additionally exposes the package-private `initialize` /
//! `update_table_migration_status` mutators (scoped `pub` — only the table
//! migration state machine calls them, mirroring Java's package-private access).

use std::sync::Mutex;

use crate::coordinator::migration::table_migration_status::TableMigrationStatus;

/// Read-only view of the current [`TableMigrationStatus`], consumed by DAO-layer
/// routing. Java `TableMigrationStatusProvider.getTableMigrationStatus()`.
///
/// Modeled as a trait so DAO routing can be unit-tested against a mock.
#[cfg_attr(test, mockall::automock)]
pub trait TableMigrationStatusProvider: Send + Sync {
    /// Java `getTableMigrationStatus()` — returns `Unknown` before initialize.
    fn get_table_migration_status(&self) -> TableMigrationStatus;
}

struct Inner {
    current_mode: TableMigrationStatus,
    initialized: bool,
    dynamic_mode_change_support_needed: bool,
}

/// Thread-safe holder/broadcaster of the current effective
/// [`TableMigrationStatus`]. Java `TableMigrationStatusProvider` (`@ThreadSafe`,
/// all methods `synchronized`).
pub struct DefaultTableMigrationStatusProvider {
    inner: Mutex<Inner>,
}

impl Default for DefaultTableMigrationStatusProvider {
    fn default() -> Self {
        Self::new()
    }
}

impl DefaultTableMigrationStatusProvider {
    /// Java no-arg constructor: `UNKNOWN`, uninitialized.
    pub fn new() -> Self {
        Self {
            inner: Mutex::new(Inner {
                current_mode: TableMigrationStatus::Unknown,
                initialized: false,
                dynamic_mode_change_support_needed: false,
            }),
        }
    }

    /// Java `dynamicModeChangeSupportNeeded()`.
    pub fn dynamic_mode_change_support_needed(&self) -> bool {
        self.inner
            .lock()
            .expect("poisoned")
            .dynamic_mode_change_support_needed
    }

    /// Java `getTableMigrationStatus()`.
    pub fn get_table_migration_status(&self) -> TableMigrationStatus {
        self.inner.lock().expect("poisoned").current_mode
    }

    /// Java package-private `initialize(...)` — one-shot; later calls are
    /// ignored + logged.
    pub fn initialize(&self, dynamic_mode_change_support_needed: bool, mode: TableMigrationStatus) {
        let mut inner = self.inner.lock().expect("poisoned");
        if !inner.initialized {
            tracing::info!(
                dynamic_mode_change_support_needed,
                ?mode,
                "Initializing table migration status provider"
            );
            inner.dynamic_mode_change_support_needed = dynamic_mode_change_support_needed;
            inner.current_mode = mode;
            inner.initialized = true;
            return;
        }
        tracing::info!(
            existing_dynamic = inner.dynamic_mode_change_support_needed,
            existing_mode = ?inner.current_mode,
            ignored_dynamic = dynamic_mode_change_support_needed,
            ignored_mode = ?mode,
            "Already initialized, ignoring new values"
        );
    }

    /// Java package-private `updateTableMigrationStatus(mode)` — panics
    /// (Java `IllegalStateException`) if called before initialize or if dynamic
    /// mode change is not supported.
    pub fn update_table_migration_status(&self, mode: TableMigrationStatus) {
        // The Java-parity panics below must not fire while `inner` is held:
        // panicking with the guard alive would poison the lock, so a
        // `catch_unwind` in the calling loop would wedge every subsequent
        // reader. Snapshot what the message needs, drop the guard, then panic.
        let current_mode = {
            let mut inner = self.inner.lock().expect("poisoned");
            if inner.initialized && inner.dynamic_mode_change_support_needed {
                tracing::info!(from = ?inner.current_mode, to = ?mode, "Changing table migration status");
                inner.current_mode = mode;
                return;
            }
            if !inner.initialized {
                None
            } else {
                Some(inner.current_mode)
            }
        };
        match current_mode {
            None => panic!("Cannot change mode before initializing"),
            Some(current_mode) => panic!(
                "TableMigrationStatus already initialized to {:?} cannot change to {:?}",
                current_mode, mode
            ),
        }
    }
}

impl TableMigrationStatusProvider for DefaultTableMigrationStatusProvider {
    fn get_table_migration_status(&self) -> TableMigrationStatus {
        DefaultTableMigrationStatusProvider::get_table_migration_status(self)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_state_returns_unknown() {
        let provider = DefaultTableMigrationStatusProvider::new();
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Unknown
        );
    }

    #[test]
    fn initialize_sets_status_and_dynamic_mode() {
        let provider = DefaultTableMigrationStatusProvider::new();
        provider.initialize(true, TableMigrationStatus::Init);
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );
        assert!(provider.dynamic_mode_change_support_needed());
    }

    #[test]
    fn initialize_without_dynamic_mode_change_sets_status_correctly() {
        let provider = DefaultTableMigrationStatusProvider::new();
        provider.initialize(false, TableMigrationStatus::Complete);
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Complete
        );
        assert!(!provider.dynamic_mode_change_support_needed());
    }

    #[test]
    fn initialize_called_twice_ignores_second_call() {
        let provider = DefaultTableMigrationStatusProvider::new();
        provider.initialize(true, TableMigrationStatus::Init);
        provider.initialize(false, TableMigrationStatus::Complete);
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Init
        );
        assert!(provider.dynamic_mode_change_support_needed());
    }

    #[test]
    fn update_table_mode_with_dynamic_mode_support_updates_status() {
        let provider = DefaultTableMigrationStatusProvider::new();
        provider.initialize(true, TableMigrationStatus::Init);
        provider.update_table_migration_status(TableMigrationStatus::Deployed);
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Deployed
        );
    }

    #[test]
    fn update_table_mode_with_dynamic_mode_support_multiple_updates() {
        let provider = DefaultTableMigrationStatusProvider::new();
        provider.initialize(true, TableMigrationStatus::Init);
        provider.update_table_migration_status(TableMigrationStatus::Deployed);
        provider.update_table_migration_status(TableMigrationStatus::Complete);
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Complete
        );
    }

    #[test]
    #[should_panic(expected = "cannot change")]
    fn update_table_mode_without_dynamic_mode_support_panics() {
        let provider = DefaultTableMigrationStatusProvider::new();
        provider.initialize(false, TableMigrationStatus::Complete);
        provider.update_table_migration_status(TableMigrationStatus::Init);
    }

    #[test]
    #[should_panic(expected = "Cannot change mode before initializing")]
    fn update_table_mode_before_initialization_panics() {
        let provider = DefaultTableMigrationStatusProvider::new();
        provider.update_table_migration_status(TableMigrationStatus::Init);
    }

    #[test]
    fn dynamic_mode_change_support_needed_default_is_false() {
        let provider = DefaultTableMigrationStatusProvider::new();
        assert!(!provider.dynamic_mode_change_support_needed());
    }

    // The Java-parity panics in `update_table_migration_status` must not poison
    // `inner`: after a caught panic (as in a `catch_unwind`-guarded background
    // loop) the provider must remain fully usable.
    #[test]
    fn update_panics_do_not_poison_the_lock() {
        use std::panic::{catch_unwind, AssertUnwindSafe};

        let provider = DefaultTableMigrationStatusProvider::new();

        // Uninitialized -> panic, caught by the caller.
        let err = catch_unwind(AssertUnwindSafe(|| {
            provider.update_table_migration_status(TableMigrationStatus::Init)
        }))
        .unwrap_err();
        assert_eq!(
            err.downcast_ref::<&str>().copied(),
            Some("Cannot change mode before initializing")
        );
        // Lock is not poisoned: reads and initialize still work.
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Unknown
        );
        provider.initialize(false, TableMigrationStatus::Complete);

        // Initialized without dynamic-mode support -> the other panic.
        let err = catch_unwind(AssertUnwindSafe(|| {
            provider.update_table_migration_status(TableMigrationStatus::Init)
        }))
        .unwrap_err();
        let msg = err.downcast_ref::<String>().cloned().unwrap();
        assert!(
            msg.contains("already initialized") && msg.contains("cannot change"),
            "unexpected panic message: {msg}"
        );
        // Still not poisoned.
        assert_eq!(
            provider.get_table_migration_status(),
            TableMigrationStatus::Complete
        );
        assert!(!provider.dynamic_mode_change_support_needed());
    }
}
