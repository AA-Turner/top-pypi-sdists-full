//! Per-OS-thread hook state, read once at the top of every Kolo callback.
//!
//! One native thread-local byte answers every per-thread question a callback
//! must settle before doing any work: is this one of Kolo's own threads, is
//! Kolo suspended here while it saves, and is an assignment waiting to be
//! recorded. Native (`std::thread_local!`) storage is never recycled and is
//! shared by every monitor and profiler generation, so a mark set before a
//! session starts still applies to it, and it costs a single TLS read.
use std::cell::{Cell, RefCell};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;

/// One of Kolo's own background threads (save, emit, upload, trace-point
/// save/replay, attach control), for the rest of its life. Never recorded.
pub(crate) const WORKER: u8 = 1 << 0;
/// Kolo is running its own work (e.g. a save) on this thread; events it
/// triggers are not recorded.
pub(crate) const SUSPENDED: u8 = 1 << 1;
/// Some monitor has assignment bookkeeping waiting on this thread; which
/// monitor, and what, is in `assignments_for`.
pub(crate) const ASSIGNMENTS: u8 = 1 << 2;

/// Per monitor (see `assignments_for`): an instruction whose assignment the
/// monitor's next event on this thread records.
pub(crate) const PENDING_ASSIGNMENT: u8 = 1 << 0;
/// Per monitor: the deferred second target of a double store.
pub(crate) const DEFERRED_STORE: u8 = 1 << 1;

/// Nothing on this thread is recorded.
pub(crate) const OFF: u8 = WORKER | SUSPENDED;

std::thread_local! {
    // `const` and drop-free: no lazy initialisation check and no destructor,
    // so reads stay valid even while the thread is being torn down.
    static STATE: Cell<u8> = const { Cell::new(0) };
    /// Assignment bookkeeping on this thread, per monitor: `(owner id, the
    /// owner's liveness, PENDING_ASSIGNMENT | DEFERRED_STORE)`. A monitor
    /// keeps its entry (flags may be 0) while it lives, so setting a flag
    /// costs no allocation; entries of dead monitors are dropped when a new
    /// one is added or when `ASSIGNMENTS` points at one. Per monitor, so one
    /// monitor's callbacks can never clear (or claim) another's.
    static WAITING: RefCell<Vec<(u64, Arc<AtomicBool>, u8)>> = const { RefCell::new(Vec::new()) };
}

static NEXT_OWNER: AtomicU64 = AtomicU64::new(1);

/// A monitor's identity in the per-thread assignment bookkeeping: a never
/// reused id and a liveness flag shared with the entries it leaves on
/// threads. Dropping it (with the monitor, or when constructing the monitor
/// fails) marks those entries dead. No lock anywhere, so nothing here can
/// be left held across a fork.
pub(crate) struct AssignmentOwner {
    id: u64,
    alive: Arc<AtomicBool>,
}

impl AssignmentOwner {
    pub(crate) fn new() -> Self {
        AssignmentOwner {
            id: NEXT_OWNER.fetch_add(1, Ordering::Relaxed),
            alive: Arc::new(AtomicBool::new(true)),
        }
    }
}

impl AssignmentOwner {
    /// Whether this owner's entries are worth keeping: a monitor's waiting
    /// assignments only matter while its session runs, so it retires them
    /// when the session ends, and other monitors' events then drop them.
    pub(crate) fn set_live(&self, live: bool) {
        self.alive.store(live, Ordering::Release);
    }
}

impl Drop for AssignmentOwner {
    fn drop(&mut self) {
        self.alive.store(false, Ordering::Release);
    }
}

fn update_summary(waiting: &[(u64, Arc<AtomicBool>, u8)]) {
    set(ASSIGNMENTS, waiting.iter().any(|(_, _, flags)| *flags != 0));
}

/// What `owner` has waiting on this thread (0 if nothing). Only worth calling
/// when `get()` has `ASSIGNMENTS`.
#[inline]
pub(crate) fn assignments_for(owner: &AssignmentOwner) -> u8 {
    WAITING
        .try_with(|waiting| {
            waiting
                .try_borrow()
                .ok()
                .and_then(|waiting| {
                    waiting
                        .iter()
                        .find(|(id, _, _)| *id == owner.id)
                        .map(|(_, _, flags)| *flags)
                })
                .unwrap_or(0)
        })
        .unwrap_or(0)
}

/// Set or clear `flag` (`PENDING_ASSIGNMENT` / `DEFERRED_STORE`) for `owner`
/// on this thread.
pub(crate) fn set_assignment(owner: &AssignmentOwner, flag: u8, value: bool) {
    let _ = WAITING.try_with(|waiting| {
        let Ok(mut waiting) = waiting.try_borrow_mut() else {
            return;
        };
        match waiting.iter_mut().find(|(id, _, _)| *id == owner.id) {
            Some((_, _, flags)) if value => *flags |= flag,
            Some((_, _, flags)) => *flags &= !flag,
            None if value => {
                waiting.retain(|(_, alive, _)| alive.load(Ordering::Acquire));
                waiting.push((owner.id, owner.alive.clone(), flag));
            }
            None => {}
        }
        update_summary(&waiting);
    });
}

/// Drop entries of monitors that no longer exist (their data died with
/// them), so a later monitor's events don't keep paying for them. Only
/// called when `ASSIGNMENTS` is set but the calling monitor has nothing
/// waiting, i.e. another monitor's entry has flags set.
pub(crate) fn drop_dead_assignments() {
    let _ = WAITING.try_with(|waiting| {
        let Ok(mut waiting) = waiting.try_borrow_mut() else {
            return;
        };
        waiting.retain(|(_, alive, _)| alive.load(Ordering::Acquire));
        update_summary(&waiting);
    });
}

#[inline(always)]
pub(crate) fn get() -> u8 {
    STATE.with(Cell::get)
}

/// Set or clear `flag` on the calling thread, returning whether it was set.
#[inline]
pub(crate) fn set(flag: u8, value: bool) -> bool {
    STATE.with(|state| {
        let previous = state.get();
        state.set(if value {
            previous | flag
        } else {
            previous & !flag
        });
        previous & flag != 0
    })
}

/// Suspends hooks on the calling thread until dropped (including during a
/// panic unwind), then restores the previous suspension.
///
/// It only ever touches `SUSPENDED`: a save section can neither clear a
/// worker's lifetime mark nor end an enclosing suspension.
#[must_use]
pub(crate) struct Suspended {
    was_suspended: bool,
}

impl Suspended {
    pub(crate) fn new() -> Self {
        Self {
            was_suspended: set(SUSPENDED, true),
        }
    }
}

impl Drop for Suspended {
    fn drop(&mut self) {
        if !self.was_suspended {
            set(SUSPENDED, false);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn suspension_restores_and_never_clears_the_worker_mark() {
        std::thread::spawn(|| {
            assert_eq!(get(), 0);
            set(WORKER, true);
            {
                let _outer = Suspended::new();
                {
                    let _inner = Suspended::new();
                    assert_eq!(get(), WORKER | SUSPENDED);
                }
                // The inner section doesn't end the outer one.
                assert_eq!(get(), WORKER | SUSPENDED);
            }
            assert_eq!(get(), WORKER);
            // Even an explicit unsuspend leaves the worker mark alone.
            set(SUSPENDED, true);
            set(SUSPENDED, false);
            assert_eq!(get(), WORKER);
        })
        .join()
        .expect("test thread");
    }

    #[test]
    fn suspension_is_restored_after_a_panic() {
        std::thread::spawn(|| {
            let result = std::panic::catch_unwind(|| {
                let _suspended = Suspended::new();
                panic!("save failed");
            });
            assert!(result.is_err());
            assert_eq!(get() & SUSPENDED, 0);
        })
        .join()
        .expect("test thread");
    }

    #[test]
    fn assignments_are_per_owner_and_dead_owners_are_dropped() {
        std::thread::spawn(|| {
            let first = AssignmentOwner::new();
            let second = AssignmentOwner::new();
            set_assignment(&first, PENDING_ASSIGNMENT, true);
            assert_eq!(get() & ASSIGNMENTS, ASSIGNMENTS);
            // Another owner never sees, clears or claims the first's.
            assert_eq!(assignments_for(&second), 0);
            set_assignment(&second, PENDING_ASSIGNMENT, false);
            assert_eq!(assignments_for(&first), PENDING_ASSIGNMENT);
            set_assignment(&second, DEFERRED_STORE, true);
            set_assignment(&second, DEFERRED_STORE, false);
            assert_eq!(assignments_for(&first), PENDING_ASSIGNMENT);
            assert_eq!(get() & ASSIGNMENTS, ASSIGNMENTS);
            // A live owner's entry survives pruning; a dead one's doesn't.
            drop_dead_assignments();
            assert_eq!(assignments_for(&first), PENDING_ASSIGNMENT);
            drop(first);
            drop_dead_assignments();
            assert_eq!(get() & ASSIGNMENTS, 0);
            assert_eq!(WAITING.with(|waiting| waiting.borrow().len()), 1);
            // Clearing a flag never needs to remove or allocate an entry.
            set_assignment(&second, PENDING_ASSIGNMENT, true);
            set_assignment(&second, PENDING_ASSIGNMENT, false);
            assert_eq!(get() & ASSIGNMENTS, 0);
            assert_eq!(WAITING.with(|waiting| waiting.borrow().len()), 1);
        })
        .join()
        .expect("test thread");
    }

    #[test]
    fn state_is_per_os_thread() {
        set(WORKER, true);
        std::thread::spawn(|| assert_eq!(get(), 0))
            .join()
            .expect("test thread");
        set(WORKER, false);
    }
}
