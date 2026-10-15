//! Test-only injection points for exercising tricky concurrency contracts.
//!
//! Production code never calls these directly; the call sites in
//! `registry.rs` are `#[cfg(test)]`-gated.

use std::cell::RefCell;
use std::sync::Arc;
use std::time::Duration;

type Hook = Arc<dyn Fn() + Send + Sync>;

thread_local! {
    /// Fires once after `refresh_and_sync` finishes loading + computing the
    /// graph and immediately before the first per-unit write. Tests use this
    /// to simulate an uncooperating external writer modifying a registry file
    /// in the load → write window.
    static AFTER_LOAD_HOOK: RefCell<Option<Hook>> = const { RefCell::new(None) };

    /// When set, reads on this thread bypass the index and come straight
    /// from the files — the reference result for index differential tests.
    static INDEX_DISABLED: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };

    /// When set, unfiltered projected reads on this thread fully parse every
    /// unit before projecting — the reference result for projection tests.
    static FAST_PROJECTION_DISABLED: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };

    /// Added to the index freshness clock on this thread (see
    /// [`with_clock_offset`]).
    static CLOCK_OFFSET: std::cell::Cell<Duration> = const { std::cell::Cell::new(Duration::ZERO) };
}

/// Run `f` with the projected-read fast path disabled on this thread.
pub(crate) fn without_fast_projection<T>(f: impl FnOnce() -> T) -> T {
    let previous = FAST_PROJECTION_DISABLED.with(|c| c.replace(true));
    let result = f();
    FAST_PROJECTION_DISABLED.with(|c| c.set(previous));
    result
}

/// Whether [`without_fast_projection`] is active on this thread.
pub(crate) fn fast_projection_disabled() -> bool {
    FAST_PROJECTION_DISABLED.with(|c| c.get())
}

/// Run `f` with the index bypassed on this thread (reads from files only).
pub(crate) fn without_index<T>(f: impl FnOnce() -> T) -> T {
    let previous = INDEX_DISABLED.with(|c| c.replace(true));
    let result = f();
    INDEX_DISABLED.with(|c| c.set(previous));
    result
}

/// Whether [`without_index`] is active on this thread.
pub(crate) fn index_disabled() -> bool {
    INDEX_DISABLED.with(|c| c.get())
}

/// Install a hook that runs once between load and the first write of the
/// next `refresh_*` call on this thread.
pub(crate) fn set_after_load_hook<F: Fn() + Send + Sync + 'static>(hook: F) {
    AFTER_LOAD_HOOK.with(|cell| {
        *cell.borrow_mut() = Some(Arc::new(hook));
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

/// This thread's hook settings, carried into a registry thread pool so
/// operations running on pool threads see the calling test's settings.
#[derive(Clone)]
pub(crate) struct Snapshot {
    after_load: Option<Hook>,
    index_disabled: bool,
    fast_projection_disabled: bool,
    clock_offset: Duration,
}

pub(crate) fn snapshot() -> Snapshot {
    Snapshot {
        after_load: AFTER_LOAD_HOOK.with(|c| c.borrow().clone()),
        index_disabled: index_disabled(),
        fast_projection_disabled: fast_projection_disabled(),
        clock_offset: clock_offset(),
    }
}

/// Run `f` on this thread with `snapshot`'s settings, restoring the
/// thread's own settings afterwards.
pub(crate) fn with_snapshot<T>(snapshot: Snapshot, f: impl FnOnce() -> T) -> T {
    let swap = |s: Snapshot| Snapshot {
        after_load: AFTER_LOAD_HOOK.with(|c| c.replace(s.after_load)),
        index_disabled: INDEX_DISABLED.with(|c| c.replace(s.index_disabled)),
        fast_projection_disabled: FAST_PROJECTION_DISABLED
            .with(|c| c.replace(s.fast_projection_disabled)),
        clock_offset: CLOCK_OFFSET.with(|c| c.replace(s.clock_offset)),
    };
    let previous = swap(snapshot);
    let result = f();
    swap(previous);
    result
}

/// Run `f` with the index freshness clock advanced by `offset` on this
/// thread, so tests can trigger the periodic sweep without sleeping.
pub(crate) fn with_clock_offset<T>(offset: Duration, f: impl FnOnce() -> T) -> T {
    let previous = CLOCK_OFFSET.with(|c| c.replace(offset));
    let result = f();
    CLOCK_OFFSET.with(|c| c.set(previous));
    result
}

/// The offset [`with_clock_offset`] applies on this thread.
pub(crate) fn clock_offset() -> Duration {
    CLOCK_OFFSET.with(|c| c.get())
}
