//! Port of `software.amazon.kinesis.coordinator.WorkerStateChangeListener`
//! and `NoOpWorkerStateChangeListener`.

use crate::exceptions::BoxError;

/// Worker lifecycle state. Java `WorkerStateChangeListener.WorkerState`.
///
/// The Scheduler only ever emits `Initializing -> Started -> ShutDownStarted ->
/// ShutDown` (`Created` is never emitted by the Scheduler itself).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum WorkerState {
    Created,
    Initializing,
    Started,
    ShutDownStarted,
    ShutDown,
}

/// A listener for callbacks on changes to worker state. Java
/// `@FunctionalInterface WorkerStateChangeListener`.
#[cfg_attr(test, mockall::automock)]
pub trait WorkerStateChangeListener: Send + Sync {
    /// Java `onWorkerStateChange(WorkerState newState)`.
    fn on_worker_state_change(&self, new_state: WorkerState);

    /// Java default `onAllInitializationAttemptsFailed(Throwable e)` — no-op.
    /// Called when the `initialize()` retry loop is exhausted.
    fn on_all_initialization_attempts_failed(&self, _e: BoxError) {}
}

/// Default no-op [`WorkerStateChangeListener`]. Java
/// `NoOpWorkerStateChangeListener`.
#[derive(Debug, Default, Clone, Copy)]
pub struct NoOpWorkerStateChangeListener;

impl NoOpWorkerStateChangeListener {
    pub fn new() -> Self {
        Self
    }
}

impl WorkerStateChangeListener for NoOpWorkerStateChangeListener {
    fn on_worker_state_change(&self, _new_state: WorkerState) {}
}
