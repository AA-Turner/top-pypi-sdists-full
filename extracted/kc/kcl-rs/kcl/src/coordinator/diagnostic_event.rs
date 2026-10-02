//! Port of the coordinator diagnostic-event family:
//! `DiagnosticEvent`, `DiagnosticEventHandler`, `ExecutorStateEvent`,
//! `RejectedTaskEvent`, `DiagnosticEventFactory`, `DiagnosticEventLogger`.
//!
//! # Deviations
//!
//! - **Visitor → enum.** Java uses a GoF visitor (`DiagnosticEvent.accept` +
//!   `DiagnosticEventHandler.visit`). Rust does not need double dispatch to add
//!   event types, but the KCL tests exercise the `accept`/`visit` handshake and
//!   custom handlers, so the [`DiagnosticEvent`] enum keeps an [`accept`]
//!   method that dispatches to a [`DiagnosticEventHandler`] trait — preserving
//!   the "only a `ThreadPoolExecutor`-backed `ExecutorStateEvent` actually
//!   visits" quirk.
//! - **`ExecutorStateEvent` stats are explicit.** Java reads a live
//!   `ThreadPoolExecutor`'s internal counters. Rust's async runtime exposes no
//!   equivalent, so the event carries the stats directly (constructed by the
//!   Scheduler wave from whatever executor abstraction it uses). The
//!   `isThreadPoolExecutor` flag is preserved as `is_thread_pool_executor`.

use std::sync::atomic::{AtomicI64, Ordering};
use std::time::{SystemTime, UNIX_EPOCH};

use crate::exceptions::BoxError;

const MESSAGE: &str = "Current thread pool executor state: ";
const REJECTED_MESSAGE: &str =
    "Review your thread configuration to prevent task rejections. Task rejections will slow down \
     your application and some shards may stop processing. ";
const EXECUTOR_LOG_INTERVAL_MILLIS: i64 = 30_000;

/// Snapshot of the record-processor executor's stats plus owned-lease count.
/// Java `ExecutorStateEvent`.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct ExecutorStateEvent {
    is_thread_pool_executor: bool,
    executor_name: String,
    current_queue_size: i32,
    active_threads: i32,
    core_threads: i32,
    leases_owned: i32,
    largest_pool_size: i32,
    maximum_pool_size: i32,
}

impl ExecutorStateEvent {
    /// Construct from explicit executor stats. Mirrors Java's 1-arg constructor
    /// applied to a `ThreadPoolExecutor` (so `is_thread_pool_executor = true`);
    /// `leases_owned` starts at 0.
    pub fn from_thread_pool_stats(
        executor_name: impl Into<String>,
        current_queue_size: i32,
        active_threads: i32,
        core_threads: i32,
        largest_pool_size: i32,
        maximum_pool_size: i32,
    ) -> Self {
        Self {
            is_thread_pool_executor: true,
            executor_name: executor_name.into(),
            current_queue_size,
            active_threads,
            core_threads,
            largest_pool_size,
            maximum_pool_size,
            leases_owned: 0,
        }
    }

    /// Mirrors Java's 2-arg constructor: sets `leases_owned` from the lease
    /// coordinator's assignment count.
    pub fn with_leases_owned(mut self, leases_owned: i32) -> Self {
        self.leases_owned = leases_owned;
        self
    }

    /// An inert event for a non-`ThreadPoolExecutor` (user-supplied) executor —
    /// `accept` is a no-op. Mirrors Java's 1-arg ctor on a plain
    /// `ExecutorService`.
    pub fn inert() -> Self {
        Self::default()
    }

    pub fn is_thread_pool_executor(&self) -> bool {
        self.is_thread_pool_executor
    }
    pub fn executor_name(&self) -> &str {
        &self.executor_name
    }
    pub fn current_queue_size(&self) -> i32 {
        self.current_queue_size
    }
    pub fn active_threads(&self) -> i32 {
        self.active_threads
    }
    pub fn core_threads(&self) -> i32 {
        self.core_threads
    }
    pub fn leases_owned(&self) -> i32 {
        self.leases_owned
    }
    pub fn largest_pool_size(&self) -> i32 {
        self.largest_pool_size
    }
    pub fn maximum_pool_size(&self) -> i32 {
        self.maximum_pool_size
    }

    /// Java `message()`.
    pub fn message(&self) -> String {
        format!(
            "{}ExecutorStateEvent(executorName={}, currentQueueSize={}, activeThreads={}, \
             coreThreads={}, leasesOwned={}, largestPoolSize={}, maximumPoolSize={})",
            MESSAGE,
            self.executor_name,
            self.current_queue_size,
            self.active_threads,
            self.core_threads,
            self.leases_owned,
            self.largest_pool_size,
            self.maximum_pool_size,
        )
    }
}

/// Wraps a rejected-task error together with the [`ExecutorStateEvent`] snapshot
/// at rejection time. Java `RejectedTaskEvent`.
#[derive(Debug)]
pub struct RejectedTaskEvent {
    executor_state_event: ExecutorStateEvent,
    throwable: BoxError,
}

impl RejectedTaskEvent {
    /// Java `RejectedTaskEvent(ExecutorStateEvent, Throwable)`.
    pub fn new(executor_state_event: ExecutorStateEvent, throwable: BoxError) -> Self {
        Self {
            executor_state_event,
            throwable,
        }
    }

    pub fn executor_state_event(&self) -> &ExecutorStateEvent {
        &self.executor_state_event
    }

    pub fn throwable(&self) -> &BoxError {
        &self.throwable
    }

    /// Java `message()` — fixed warning prefix + delegate event message.
    pub fn message(&self) -> String {
        format!(
            "{}{}",
            REJECTED_MESSAGE,
            self.executor_state_event.message()
        )
    }
}

/// A diagnostic/telemetry event. Java `DiagnosticEvent` (visitor element).
#[derive(Debug)]
pub enum DiagnosticEvent {
    ExecutorState(ExecutorStateEvent),
    RejectedTask(RejectedTaskEvent),
}

impl DiagnosticEvent {
    /// Java `accept(DiagnosticEventHandler)`. For an `ExecutorStateEvent`, only
    /// actually visits when it was backed by a `ThreadPoolExecutor` (matching
    /// Java's guard); a `RejectedTaskEvent` always visits.
    pub fn accept(&self, visitor: &mut dyn DiagnosticEventHandler) {
        match self {
            DiagnosticEvent::ExecutorState(e) => {
                if e.is_thread_pool_executor {
                    visitor.visit_executor_state(e);
                }
            }
            DiagnosticEvent::RejectedTask(e) => visitor.visit_rejected_task(e),
        }
    }

    /// Java `message()`.
    pub fn message(&self) -> String {
        match self {
            DiagnosticEvent::ExecutorState(e) => e.message(),
            DiagnosticEvent::RejectedTask(e) => e.message(),
        }
    }
}

/// Behavior for reacting to each [`DiagnosticEvent`] variant. Java
/// `DiagnosticEventHandler` (visitor).
pub trait DiagnosticEventHandler {
    /// Java `visit(ExecutorStateEvent)`.
    fn visit_executor_state(&mut self, event: &ExecutorStateEvent);
    /// Java `visit(RejectedTaskEvent)`.
    fn visit_rejected_task(&mut self, event: &RejectedTaskEvent);
}

/// Factory for constructing diagnostic events (exists to allow test doubles).
/// Java `DiagnosticEventFactory`.
#[derive(Debug, Default, Clone, Copy)]
pub struct DiagnosticEventFactory;

impl DiagnosticEventFactory {
    pub fn new() -> Self {
        Self
    }

    /// Java `executorStateEvent(ExecutorService, LeaseCoordinator)` — here the
    /// caller supplies the stats snapshot + owned-lease count directly.
    pub fn executor_state_event(
        &self,
        state: ExecutorStateEvent,
        leases_owned: i32,
    ) -> ExecutorStateEvent {
        state.with_leases_owned(leases_owned)
    }

    /// Java `rejectedTaskEvent(ExecutorStateEvent, Throwable)`.
    pub fn rejected_task_event(
        &self,
        executor_state_event: ExecutorStateEvent,
        throwable: BoxError,
    ) -> RejectedTaskEvent {
        RejectedTaskEvent::new(executor_state_event, throwable)
    }
}

/// Default [`DiagnosticEventHandler`]: throttles `ExecutorStateEvent` INFO
/// logging to once per 30s (DEBUG otherwise), always logs `RejectedTaskEvent`
/// at ERROR. Java `DiagnosticEventLogger`.
///
/// The `next_executor_log_time` uses an `AtomicI64` (Java's plain field is a
/// benign race; the atomic is a strict improvement).
#[derive(Debug)]
pub struct DiagnosticEventLogger {
    next_executor_log_time: AtomicI64,
}

impl Default for DiagnosticEventLogger {
    fn default() -> Self {
        Self::new()
    }
}

impl DiagnosticEventLogger {
    pub fn new() -> Self {
        Self {
            next_executor_log_time: AtomicI64::new(now_millis() + EXECUTOR_LOG_INTERVAL_MILLIS),
        }
    }
}

impl DiagnosticEventHandler for DiagnosticEventLogger {
    fn visit_executor_state(&mut self, event: &ExecutorStateEvent) {
        let now = now_millis();
        if now >= self.next_executor_log_time.load(Ordering::Relaxed) {
            tracing::info!("{}", event.message());
            self.next_executor_log_time
                .store(now + EXECUTOR_LOG_INTERVAL_MILLIS, Ordering::Relaxed);
        } else {
            tracing::debug!("{}", event.message());
        }
    }

    fn visit_rejected_task(&mut self, event: &RejectedTaskEvent) {
        tracing::error!(error = %event.throwable(), "{}", event.message());
    }
}

fn now_millis() -> i64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::Cell;

    const ACTIVE_THREAD_COUNT: i32 = 2;
    const CORE_POOL_SIZE: i32 = 4;
    const LARGEST_POOL_SIZE: i32 = 8;
    const MAXIMUM_POOL_SIZE: i32 = 16;

    fn executor_event() -> ExecutorStateEvent {
        ExecutorStateEvent::from_thread_pool_stats(
            "SchedulerThreadPoolExecutor",
            0,
            ACTIVE_THREAD_COUNT,
            CORE_POOL_SIZE,
            LARGEST_POOL_SIZE,
            MAXIMUM_POOL_SIZE,
        )
        .with_leases_owned(1)
    }

    /// Recording handler that counts visits (the Java `defaultHandler` mock).
    #[derive(Default)]
    struct RecordingHandler {
        executor_visits: u32,
        rejected_visits: u32,
    }
    impl DiagnosticEventHandler for RecordingHandler {
        fn visit_executor_state(&mut self, _event: &ExecutorStateEvent) {
            self.executor_visits += 1;
        }
        fn visit_rejected_task(&mut self, _event: &RejectedTaskEvent) {
            self.rejected_visits += 1;
        }
    }

    #[test]
    fn test_executor_state_event() {
        let event = executor_event();
        let mut handler = RecordingHandler::default();
        DiagnosticEvent::ExecutorState(event.clone()).accept(&mut handler);

        assert_eq!(event.active_threads(), ACTIVE_THREAD_COUNT);
        assert_eq!(event.core_threads(), CORE_POOL_SIZE);
        assert_eq!(event.largest_pool_size(), LARGEST_POOL_SIZE);
        assert_eq!(event.maximum_pool_size(), MAXIMUM_POOL_SIZE);
        assert_eq!(event.leases_owned(), 1);
        assert_eq!(event.current_queue_size(), 0);
        assert_eq!(handler.executor_visits, 1);
    }

    #[test]
    fn test_executor_state_event_with_custom_handler() {
        struct CustomHandler<'a>(&'a Cell<bool>);
        impl DiagnosticEventHandler for CustomHandler<'_> {
            fn visit_executor_state(&mut self, _e: &ExecutorStateEvent) {
                self.0.set(true);
            }
            fn visit_rejected_task(&mut self, _e: &RejectedTaskEvent) {
                self.0.set(true);
            }
        }
        let invoked = Cell::new(false);
        let mut handler = CustomHandler(&invoked);
        DiagnosticEvent::ExecutorState(executor_event()).accept(&mut handler);
        assert!(invoked.get());
    }

    #[test]
    fn test_rejected_task_event_with_custom_handler() {
        // Java `testRejectedTaskEventWithCustomHandler`: a custom handler's
        // visit(RejectedTaskEvent) is invoked when the event is accepted.
        struct CustomHandler<'a>(&'a Cell<bool>);
        impl DiagnosticEventHandler for CustomHandler<'_> {
            fn visit_executor_state(&mut self, _e: &ExecutorStateEvent) {
                self.0.set(true);
            }
            fn visit_rejected_task(&mut self, _e: &RejectedTaskEvent) {
                self.0.set(true);
            }
        }
        let invoked = Cell::new(false);
        let mut handler = CustomHandler(&invoked);
        let event = RejectedTaskEvent::new(executor_event(), "boom".into());
        DiagnosticEvent::RejectedTask(event).accept(&mut handler);
        assert!(invoked.get());
    }

    #[test]
    fn test_inert_executor_state_event_does_not_visit() {
        let mut handler = RecordingHandler::default();
        DiagnosticEvent::ExecutorState(ExecutorStateEvent::inert()).accept(&mut handler);
        assert_eq!(handler.executor_visits, 0);
    }

    #[test]
    fn test_rejected_task_event() {
        let event = RejectedTaskEvent::new(executor_event(), "boom".into());
        let mut handler = RecordingHandler::default();
        assert_eq!(
            event.executor_state_event().active_threads(),
            ACTIVE_THREAD_COUNT
        );
        assert_eq!(event.executor_state_event().core_threads(), CORE_POOL_SIZE);
        assert_eq!(
            event.executor_state_event().largest_pool_size(),
            LARGEST_POOL_SIZE
        );
        assert_eq!(
            event.executor_state_event().maximum_pool_size(),
            MAXIMUM_POOL_SIZE
        );
        assert_eq!(event.executor_state_event().leases_owned(), 1);
        assert_eq!(event.executor_state_event().current_queue_size(), 0);
        assert_eq!(event.throwable().to_string(), "boom");

        DiagnosticEvent::RejectedTask(event).accept(&mut handler);
        assert_eq!(handler.rejected_visits, 1);
    }

    #[test]
    fn test_diagnostic_event_factory() {
        let factory = DiagnosticEventFactory::new();
        let base = ExecutorStateEvent::from_thread_pool_stats(
            "SchedulerThreadPoolExecutor",
            0,
            ACTIVE_THREAD_COUNT,
            CORE_POOL_SIZE,
            LARGEST_POOL_SIZE,
            MAXIMUM_POOL_SIZE,
        );
        let executor_state_event = factory.executor_state_event(base, 1);
        assert_eq!(executor_state_event.active_threads(), ACTIVE_THREAD_COUNT);
        assert_eq!(executor_state_event.leases_owned(), 1);
        assert_eq!(executor_state_event.current_queue_size(), 0);

        let rejected = factory.rejected_task_event(executor_state_event, "rejected".into());
        assert_eq!(
            rejected.executor_state_event().core_threads(),
            CORE_POOL_SIZE
        );
        assert_eq!(rejected.throwable().to_string(), "rejected");
    }
}
