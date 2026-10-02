//! Scheduling seam for the migration monitors.
//!
//! Java uses a shared `ScheduledExecutorService.scheduleWithFixedDelay(runnable,
//! initialDelay, period)`. This trait abstracts that so:
//!
//! - production ([`TokioMonitorScheduler`]) spawns a tokio task that ticks on an
//!   interval and awaits the (async) periodic task, with a `Notify`-based stop;
//! - tests use a recording scheduler (see the migration test modules) that
//!   captures the periodic task closure so the polling logic can be driven
//!   synchronously, mirroring the Java tests' `ArgumentCaptor<Runnable>.run()`.

use std::future::Future;
use std::pin::Pin;
use std::sync::Arc;

use tokio::sync::Notify;

/// A periodic task: an async closure re-run on each tick. Boxed so it is
/// storable/clonable behind an `Arc`.
pub type PeriodicTask = Arc<dyn Fn() -> Pin<Box<dyn Future<Output = ()> + Send>> + Send + Sync>;

/// Handle to a scheduled periodic task, used to cancel it. Java
/// `ScheduledFuture.cancel(...)`.
pub struct ScheduledHandle {
    stop: Arc<Notify>,
    handle: std::sync::Mutex<Option<tokio::task::JoinHandle<()>>>,
}

impl ScheduledHandle {
    /// A no-op handle (used by recording/test schedulers that never spawn).
    pub fn noop() -> Self {
        Self {
            stop: Arc::new(Notify::new()),
            handle: std::sync::Mutex::new(None),
        }
    }

    /// Cancel the scheduled task. Idempotent. Java `ScheduledFuture.cancel(...)`.
    pub fn cancel(&self) {
        self.stop.notify_waiters();
        if let Some(h) = self.handle.lock().expect("poisoned").take() {
            h.abort();
            // Reap the JoinHandle so a panic that escaped the loop is logged
            // rather than silently discarded. `cancel` may run outside a
            // runtime (e.g. via `Drop`), so only spawn if one is available.
            if let Ok(rt) = tokio::runtime::Handle::try_current() {
                rt.spawn(async move {
                    if let Err(e) = h.await {
                        if e.is_panic() {
                            tracing::error!(
                                "Scheduled migration monitor task panicked: {}",
                                crate::utils::panic_util::panic_message(e.into_panic().as_ref())
                            );
                        }
                    }
                });
            }
        }
    }
}

impl Drop for ScheduledHandle {
    fn drop(&mut self) {
        self.cancel();
    }
}

/// Schedules periodic tasks. Java `ScheduledExecutorService` (the subset used by
/// the migration monitors).
pub trait MonitorScheduler: Send + Sync {
    /// Java `scheduleWithFixedDelay(task, initialDelay, period)` (milliseconds).
    fn schedule_with_fixed_delay(
        &self,
        task: PeriodicTask,
        initial_delay_ms: u64,
        period_ms: u64,
    ) -> ScheduledHandle;
}

/// Production scheduler: spawns a tokio task with an interval ticker.
#[derive(Default, Clone)]
pub struct TokioMonitorScheduler;

impl TokioMonitorScheduler {
    pub fn new() -> Self {
        Self
    }
}

/// A record of one `schedule_with_fixed_delay` call.
#[cfg(test)]
#[derive(Clone)]
pub struct ScheduledCall {
    pub task: PeriodicTask,
    pub initial_delay_ms: u64,
    pub period_ms: u64,
}

/// Test scheduler that records the scheduled periodic task closures so tests can
/// drive the polling logic synchronously (mirrors the Java tests' captured
/// `Runnable`). Never spawns.
#[cfg(test)]
#[derive(Clone, Default)]
pub struct RecordingScheduler {
    calls: Arc<std::sync::Mutex<Vec<ScheduledCall>>>,
}

#[cfg(test)]
impl RecordingScheduler {
    pub fn new() -> Self {
        Self::default()
    }

    /// All scheduled calls captured so far.
    pub fn calls(&self) -> Vec<ScheduledCall> {
        self.calls.lock().expect("poisoned").clone()
    }

    /// The single most recently scheduled task (panics if none).
    pub fn last_task(&self) -> PeriodicTask {
        self.calls
            .lock()
            .expect("poisoned")
            .last()
            .expect("no scheduled task")
            .task
            .clone()
    }

    /// Number of scheduled calls.
    pub fn call_count(&self) -> usize {
        self.calls.lock().expect("poisoned").len()
    }

    /// Clear the recorded calls (mirrors Mockito `reset(scheduler)`).
    pub fn reset(&self) {
        self.calls.lock().expect("poisoned").clear();
    }
}

#[cfg(test)]
impl MonitorScheduler for RecordingScheduler {
    fn schedule_with_fixed_delay(
        &self,
        task: PeriodicTask,
        initial_delay_ms: u64,
        period_ms: u64,
    ) -> ScheduledHandle {
        self.calls.lock().expect("poisoned").push(ScheduledCall {
            task,
            initial_delay_ms,
            period_ms,
        });
        ScheduledHandle::noop()
    }
}

impl MonitorScheduler for TokioMonitorScheduler {
    fn schedule_with_fixed_delay(
        &self,
        task: PeriodicTask,
        initial_delay_ms: u64,
        period_ms: u64,
    ) -> ScheduledHandle {
        let stop = Arc::new(Notify::new());
        let stop_clone = stop.clone();
        let handle = tokio::spawn(async move {
            tokio::select! {
                _ = stop_clone.notified() => return,
                _ = tokio::time::sleep(std::time::Duration::from_millis(initial_delay_ms)) => {}
            }
            let mut interval =
                tokio::time::interval(std::time::Duration::from_millis(period_ms.max(1)));
            loop {
                // fixed-delay semantics: run then wait `period` before next run.
                // Ports Java ClientVersionChangeMonitor.run's catch (Exception)
                // and MigrationReadyMonitor.run's catch (Throwable): a panicking
                // tick is logged and the schedule keeps polling.
                if let Err(panic) = crate::utils::panic_util::catch_tick(task()).await {
                    tracing::error!(
                        "Scheduled migration monitor task failed, will retry: {}",
                        panic
                    );
                }
                tokio::select! {
                    _ = stop_clone.notified() => return,
                    _ = interval.tick() => {}
                }
            }
        });
        ScheduledHandle {
            stop,
            handle: std::sync::Mutex::new(Some(handle)),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};

    /// A periodic task that panics on its first invocations must keep getting
    /// re-invoked: the loop's `catch_tick` ports Java
    /// `ClientVersionChangeMonitor.run` catch (Exception) /
    /// `MigrationReadyMonitor.run` catch (Throwable), where a throwing tick is
    /// logged and the schedule keeps polling.
    #[tokio::test(start_paused = true)]
    async fn panicking_tick_does_not_kill_the_schedule() {
        let invocations = Arc::new(AtomicUsize::new(0));
        let task_invocations = invocations.clone();
        let task: PeriodicTask = Arc::new(move || {
            let count = task_invocations.clone();
            Box::pin(async move {
                let n = count.fetch_add(1, Ordering::SeqCst);
                if n < 2 {
                    panic!("monitor tick {} panics", n);
                }
            })
        });

        let handle = TokioMonitorScheduler::new().schedule_with_fixed_delay(task, 0, 100);

        // Paused clock: sleeping auto-advances time across many 100ms periods.
        tokio::time::sleep(std::time::Duration::from_millis(1_000)).await;

        let n = invocations.load(Ordering::SeqCst);
        assert!(
            n >= 3,
            "schedule died after panicking ticks (ran {} times)",
            n
        );
        handle.cancel();
    }
}
