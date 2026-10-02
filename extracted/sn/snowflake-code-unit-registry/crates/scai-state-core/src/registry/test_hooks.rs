//! Test-only injection points for exercising tricky concurrency contracts.
//!
//! Production code never calls these directly; the call sites in
//! `registry.rs` are `#[cfg(test)]`-gated.

use std::cell::RefCell;

thread_local! {
    /// Fires once after `refresh_and_sync` finishes loading + computing the
    /// graph and immediately before the first per-unit write. Tests use this
    /// to simulate an uncooperating external writer modifying a registry file
    /// in the load → write window.
    static AFTER_LOAD_HOOK: RefCell<Option<Box<dyn Fn()>>> = const { RefCell::new(None) };
}

/// Install a hook that runs once between load and the first write of the
/// next `refresh_*` call on this thread.
pub(crate) fn set_after_load_hook<F: Fn() + 'static>(hook: F) {
    AFTER_LOAD_HOOK.with(|cell| {
        *cell.borrow_mut() = Some(Box::new(hook));
    });
}

/// Remove any installed after-load hook on this thread. Safe to call when
/// none is installed.
pub(crate) fn clear_after_load_hook() {
    AFTER_LOAD_HOOK.with(|cell| {
        cell.borrow_mut().take();
    });
}

/// Invoke the installed hook, if any. Called by `refresh_and_sync`.
pub(crate) fn run_after_load_hook() {
    AFTER_LOAD_HOOK.with(|cell| {
        if let Some(hook) = cell.borrow().as_ref() {
            hook();
        }
    });
}
