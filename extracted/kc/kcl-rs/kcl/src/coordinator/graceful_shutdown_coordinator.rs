//! Port of `software.amazon.kinesis.coordinator.GracefulShutdownCoordinator`
//! (package-private).
//!
//! Wraps a shutdown "callable" in an async future and implements the blocking
//! wait logic that polls two count-down latches (notification-complete,
//! final-shutdown-complete) with 1-second poll intervals, tolerating cancellation
//! and detecting when the Scheduler itself already finished shutting down
//! out-of-band.
//!
//! # Concurrency model
//!
//! Java uses `CompletableFuture.runAsync` on the implicit common `ForkJoinPool`
//! plus `CountDownLatch.await(1, SECONDS)` polling. The Rust port:
//!
//! * `start_graceful_shutdown` spawns the shutdown work on a **dedicated tokio
//!   task** (there is no implicit global pool — matching the Java intent of NOT
//!   using the Scheduler's configurable executor) and returns a
//!   [`oneshot::Receiver`] resolving to the `Result<bool>` (the
//!   `CompletableFuture<Boolean>` analog).
//! * The `CountDownLatch.await(1, SECONDS)` poll loops become
//!   `tokio::time::timeout(Duration::from_secs(1), latch.await_latch())` loops,
//!   preserving the once-per-second "still waiting" logging + the
//!   `workerShutdownWithRemaining` early-exit check.
//! * The `Thread.interrupted()` checks have no direct Rust analog (tokio tasks
//!   are cancelled by dropping, not interrupted); they are omitted — a dropped
//!   task simply stops awaiting.

use async_trait::async_trait;
use tokio::sync::oneshot;

use crate::coordinator::graceful_shutdown_context::GracefulShutdownContext;

/// Arbitrary wait time for the worker's `finalShutdown` (Java
/// `FINAL_SHUTDOWN_WAIT_TIME_SECONDS`).
const FINAL_SHUTDOWN_WAIT_TIME_SECONDS: u64 = 60;

/// The back-reference the coordinator needs into the running Scheduler (Java
/// `GracefulShutdownContext.scheduler()`), abstracted as a trait to break the
/// `Scheduler`↔`GracefulShutdownCoordinator` cycle. Implemented by `Scheduler`
/// (wave 10d).
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait SchedulerHandle: Send + Sync {
    /// Java `scheduler.shutdownComplete()`.
    fn shutdown_complete(&self) -> bool;
    /// Java `scheduler.shardInfoShardConsumerMap().isEmpty()`.
    fn shard_consumer_map_is_empty(&self) -> bool;
    /// Java `scheduler.shardInfoShardConsumerMap().size()`.
    fn shard_consumer_map_size(&self) -> usize;
    /// Java `scheduler.shutdown()`.
    async fn shutdown(&self);
}

/// Produces a [`GracefulShutdownContext`] (Java
/// `Callable<GracefulShutdownContext> startWorkerShutdown`). The Scheduler builds
/// this closure; it stops lease-taking, notifies the record processors, and
/// returns the context carrying the latches + scheduler handle.
pub type StartWorkerShutdown = Box<
    dyn FnOnce() -> futures::future::BoxFuture<
            'static,
            Result<GracefulShutdownContext, GracefulShutdownError>,
        > + Send,
>;

/// An error from the graceful-shutdown process.
#[derive(Debug, thiserror::Error)]
#[error("{0}")]
pub struct GracefulShutdownError(pub String);

/// Wraps the shutdown callable and implements the polling wait logic. Java
/// `GracefulShutdownCoordinator`.
#[derive(Debug, Default, Clone)]
pub struct GracefulShutdownCoordinator;

impl GracefulShutdownCoordinator {
    /// A new coordinator.
    pub fn new() -> Self {
        Self
    }

    /// Java `startGracefulShutdown(Callable<Boolean>)`: run the shutdown work on a
    /// dedicated task and return a receiver resolving to the outcome (the
    /// `CompletableFuture<Boolean>` analog).
    ///
    /// `true` = graceful shutdown completed; `false` = a non-exception case
    /// terminated it early; `Err` = the callable itself failed.
    pub fn start_graceful_shutdown(
        &self,
        start_worker_shutdown: StartWorkerShutdown,
    ) -> oneshot::Receiver<Result<bool, GracefulShutdownError>> {
        let (tx, rx) = oneshot::channel();
        tokio::spawn(async move {
            let result = Self::run_graceful_shutdown(start_worker_shutdown).await;
            let _ = tx.send(result);
        });
        rx
    }

    /// Java `GracefulShutdownCallable.call()`: obtain the context, then
    /// `waitForRecordProcessors(ctx) && waitForFinalShutdown(ctx)`.
    ///
    /// Exposed (not just via [`start_graceful_shutdown`](Self::start_graceful_shutdown))
    /// so callers can drive the shutdown synchronously / in their own executor
    /// (Java `createGracefulShutdownCallable`).
    pub async fn run_graceful_shutdown(
        start_worker_shutdown: StartWorkerShutdown,
    ) -> Result<bool, GracefulShutdownError> {
        let context = start_worker_shutdown().await.map_err(|e| {
            tracing::warn!("Caught exception while requesting initial worker shutdown: {e}");
            e
        })?;
        Ok(Self::wait_for_record_processors(&context).await
            && Self::wait_for_final_shutdown(&context).await)
    }

    fn is_worker_shutdown_complete(context: &GracefulShutdownContext) -> bool {
        match context.scheduler() {
            Some(s) => s.shutdown_complete() || s.shard_consumer_map_is_empty(),
            None => true,
        }
    }

    /// Java `workerShutdownWithRemaining`: the worker already hit its shutdown
    /// target while record processors remain outstanding.
    fn worker_shutdown_with_remaining(outstanding: i64, context: &GracefulShutdownContext) -> bool {
        if Self::is_worker_shutdown_complete(context) && outstanding != 0 {
            tracing::info!(
                "Shutdown completed, but shutdownCompleteLatch still had outstanding {outstanding}"
            );
            return true;
        }
        false
    }

    /// Java `waitForRecordProcessors`.
    async fn wait_for_record_processors(context: &GracefulShutdownContext) -> bool {
        if context.is_record_processor_shutdown_complete() {
            return true;
        }

        let notification_latch = match context.notification_complete_latch() {
            Some(l) => l,
            None => return true,
        };
        let shutdown_latch = context.shutdown_complete_latch();

        // Await notification-complete, polling once per second for the
        // early-exit condition (Java `notificationCompleteLatch.await(1, SECONDS)`).
        while !Self::await_latch_with_timeout(notification_latch).await {
            tracing::info!(
                "Waiting for {} record processors to complete shutdown notification",
                notification_latch.get_count()
            );
            let outstanding = shutdown_latch.map(|l| l.get_count()).unwrap_or(0);
            if Self::worker_shutdown_with_remaining(outstanding, context) {
                return false;
            }
        }

        // Once all record processors are notified, let the worker start its own
        // shutdown (Java `context.scheduler().shutdown()`).
        if let Some(scheduler) = context.scheduler() {
            scheduler.shutdown().await;
        }

        // Wait for the remaining shard consumers to complete final shutdown.
        if let Some(shutdown_latch) = shutdown_latch {
            while !Self::await_latch_with_timeout(shutdown_latch).await {
                tracing::info!(
                    "Waiting for {} record processors to complete final shutdown",
                    shutdown_latch.get_count()
                );
                if Self::worker_shutdown_with_remaining(shutdown_latch.get_count(), context) {
                    return false;
                }
            }
        }
        true
    }

    /// Java `waitForFinalShutdown`: bounded (60s) await on the final-shutdown
    /// latch.
    async fn wait_for_final_shutdown(context: &GracefulShutdownContext) -> bool {
        let latch = match context.final_shutdown_latch() {
            Some(l) => l,
            None => return true,
        };
        tokio::time::timeout(
            std::time::Duration::from_secs(FINAL_SHUTDOWN_WAIT_TIME_SECONDS),
            latch.await_latch(),
        )
        .await
        .is_ok()
    }

    /// Await the latch for up to 1 second. Returns `true` if it fired within the
    /// window (Java `latch.await(1, SECONDS)`).
    async fn await_latch_with_timeout(latch: &crate::lifecycle::CountDownLatch) -> bool {
        tokio::time::timeout(std::time::Duration::from_secs(1), latch.await_latch())
            .await
            .is_ok()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lifecycle::CountDownLatch;
    use std::sync::Arc;

    #[tokio::test(start_paused = true)]
    async fn empty_context_completes_immediately() {
        // A context with only a final-shutdown latch (already fired) — the
        // Scheduler had zero leases at shutdown-request time.
        let final_latch = Arc::new(CountDownLatch::new());
        final_latch.count_down();
        let ctx = GracefulShutdownContext::new(None, None, Some(final_latch), None);
        assert!(GracefulShutdownCoordinator::wait_for_record_processors(&ctx).await);
        assert!(GracefulShutdownCoordinator::wait_for_final_shutdown(&ctx).await);
    }

    #[tokio::test(start_paused = true)]
    async fn waits_for_notification_then_final() {
        let notification = Arc::new(CountDownLatch::new_with_count(2));
        let shutdown = Arc::new(CountDownLatch::new_with_count(2));
        let final_latch = Arc::new(CountDownLatch::new());

        let mut scheduler = MockSchedulerHandle::new();
        scheduler.expect_shutdown_complete().returning(|| false);
        scheduler
            .expect_shard_consumer_map_is_empty()
            .returning(|| false);
        scheduler.expect_shard_consumer_map_size().returning(|| 2);
        scheduler.expect_shutdown().returning(|| ());

        let ctx = GracefulShutdownContext::new(
            Some(shutdown.clone()),
            Some(notification.clone()),
            Some(final_latch.clone()),
            Some(Arc::new(scheduler)),
        );

        // Drive the latches down from a background task.
        let n = notification.clone();
        let s = shutdown.clone();
        let f = final_latch.clone();
        tokio::spawn(async move {
            n.count_down();
            n.count_down();
            s.count_down();
            s.count_down();
            f.count_down();
        });

        let start = Box::new(move || {
            let ctx = ctx.clone();
            Box::pin(async move { Ok(ctx) })
                as futures::future::BoxFuture<
                    'static,
                    Result<GracefulShutdownContext, GracefulShutdownError>,
                >
        }) as StartWorkerShutdown;

        // Advance paused time so the 1s poll loops make progress.
        let handle =
            tokio::spawn(
                async move { GracefulShutdownCoordinator::run_graceful_shutdown(start).await },
            );
        for _ in 0..5 {
            tokio::time::advance(std::time::Duration::from_secs(1)).await;
            tokio::task::yield_now().await;
        }
        let result = handle.await.unwrap();
        assert!(result.unwrap());
    }

    /// Drive `run_graceful_shutdown` to completion under paused time, pumping the
    /// 1s poll loops (and the 60s final-shutdown timeout) forward.
    async fn drive_to_completion(
        ctx: GracefulShutdownContext,
    ) -> Result<bool, GracefulShutdownError> {
        let start = Box::new(move || {
            let ctx = ctx.clone();
            Box::pin(async move { Ok(ctx) })
                as futures::future::BoxFuture<
                    'static,
                    Result<GracefulShutdownContext, GracefulShutdownError>,
                >
        }) as StartWorkerShutdown;
        let handle =
            tokio::spawn(
                async move { GracefulShutdownCoordinator::run_graceful_shutdown(start).await },
            );
        // Pump enough 1s ticks to cover the poll loops plus the 60s final wait.
        for _ in 0..70 {
            tokio::time::advance(std::time::Duration::from_secs(1)).await;
            tokio::task::yield_now().await;
        }
        handle.await.unwrap()
    }

    fn scheduler_running(map_size: usize) -> MockSchedulerHandle {
        // A scheduler that is NOT shutdown-complete and still owns `map_size`
        // consumers (so the worker-shutdown-with-remaining early-exit never trips).
        let mut s = MockSchedulerHandle::new();
        s.expect_shutdown_complete().returning(|| false);
        s.expect_shard_consumer_map_is_empty()
            .returning(move || map_size == 0);
        s.expect_shard_consumer_map_size()
            .returning(move || map_size);
        s.expect_shutdown().returning(|| ());
        s
    }

    #[tokio::test(start_paused = true)]
    async fn notification_not_completed_yet_then_succeeds() {
        // Java `testNotificationNotCompletedYet`: the notification latch fires only
        // after the first (timed-out) await; the worker is still running, so the
        // loop retries, then shutdown proceeds and completes true.
        let notification = Arc::new(CountDownLatch::new_with_count(1));
        let shutdown = Arc::new(CountDownLatch::new_with_count(1));
        let final_latch = Arc::new(CountDownLatch::new());
        let ctx = GracefulShutdownContext::new(
            Some(shutdown.clone()),
            Some(notification.clone()),
            Some(final_latch.clone()),
            Some(Arc::new(scheduler_running(1))),
        );

        // Fire the notification only after ~2s (so the first 1s await times out),
        // then the shutdown + final latches.
        let (n, s, f) = (notification.clone(), shutdown.clone(), final_latch.clone());
        tokio::spawn(async move {
            tokio::time::sleep(std::time::Duration::from_millis(1500)).await;
            n.count_down();
            s.count_down();
            f.count_down();
        });

        assert!(drive_to_completion(ctx).await.unwrap());
    }

    #[tokio::test(start_paused = true)]
    async fn shutdown_not_completed_yet_then_succeeds() {
        // Java `testShutdownNotCompletedYet`: notification fires immediately, but
        // the shutdown-complete latch only fires after the first timed-out await.
        let notification = Arc::new(CountDownLatch::new_with_count(1));
        let shutdown = Arc::new(CountDownLatch::new_with_count(1));
        let final_latch = Arc::new(CountDownLatch::new());
        let ctx = GracefulShutdownContext::new(
            Some(shutdown.clone()),
            Some(notification.clone()),
            Some(final_latch.clone()),
            Some(Arc::new(scheduler_running(1))),
        );

        notification.count_down(); // notification already complete
        let (s, f) = (shutdown.clone(), final_latch.clone());
        tokio::spawn(async move {
            tokio::time::sleep(std::time::Duration::from_millis(1500)).await;
            s.count_down();
            f.count_down();
        });

        assert!(drive_to_completion(ctx).await.unwrap());
    }

    #[tokio::test(start_paused = true)]
    async fn multiple_attempts_for_notification_then_succeeds() {
        // Java `testMultipleAttemptsForNotification`: the notification latch fires
        // only after several 1s poll attempts.
        let notification = Arc::new(CountDownLatch::new_with_count(1));
        let shutdown = Arc::new(CountDownLatch::new_with_count(1));
        let final_latch = Arc::new(CountDownLatch::new());
        let ctx = GracefulShutdownContext::new(
            Some(shutdown.clone()),
            Some(notification.clone()),
            Some(final_latch.clone()),
            Some(Arc::new(scheduler_running(2))),
        );

        let (n, s, f) = (notification.clone(), shutdown.clone(), final_latch.clone());
        tokio::spawn(async move {
            tokio::time::sleep(std::time::Duration::from_millis(2500)).await; // 3rd attempt
            n.count_down();
            s.count_down();
            f.count_down();
        });

        assert!(drive_to_completion(ctx).await.unwrap());
    }

    #[tokio::test(start_paused = true)]
    async fn worker_already_shutdown_at_notification_returns_false() {
        // Java `testWorkerAlreadyShutdownAtNotification`: notification never fires,
        // but the scheduler reports shutdown-complete with an empty consumer map
        // while the shutdown-complete latch still has outstanding work → the
        // `workerShutdownWithRemaining` early-exit returns false.
        let notification = Arc::new(CountDownLatch::new_with_count(1));
        let shutdown = Arc::new(CountDownLatch::new_with_count(1)); // outstanding != 0
        let final_latch = Arc::new(CountDownLatch::new());

        let mut scheduler = MockSchedulerHandle::new();
        scheduler.expect_shutdown_complete().returning(|| true);
        scheduler
            .expect_shard_consumer_map_is_empty()
            .returning(|| true);
        scheduler.expect_shard_consumer_map_size().returning(|| 0);
        scheduler.expect_shutdown().returning(|| ());

        let ctx = GracefulShutdownContext::new(
            Some(shutdown),
            Some(notification),
            Some(final_latch),
            Some(Arc::new(scheduler)),
        );
        assert!(!drive_to_completion(ctx).await.unwrap());
    }

    #[tokio::test(start_paused = true)]
    async fn worker_already_shutdown_at_complete_returns_false() {
        // Java `testWorkerAlreadyShutdownAtComplete`: notification completes, but
        // the shutdown-complete latch never fires while the scheduler reports
        // shutdown-complete (empty map) with outstanding count → early-exit false.
        let notification = Arc::new(CountDownLatch::new_with_count(1));
        let shutdown = Arc::new(CountDownLatch::new_with_count(1)); // never fires, outstanding != 0
        let final_latch = Arc::new(CountDownLatch::new());

        let mut scheduler = MockSchedulerHandle::new();
        scheduler.expect_shutdown_complete().returning(|| true);
        scheduler
            .expect_shard_consumer_map_is_empty()
            .returning(|| true);
        scheduler.expect_shard_consumer_map_size().returning(|| 0);
        scheduler.expect_shutdown().returning(|| ());

        notification.count_down(); // notification complete
        let ctx = GracefulShutdownContext::new(
            Some(shutdown),
            Some(notification),
            Some(final_latch),
            Some(Arc::new(scheduler)),
        );
        assert!(!drive_to_completion(ctx).await.unwrap());
    }

    #[tokio::test(start_paused = true)]
    async fn shutdown_fails_due_to_record_processors() {
        // Java `testShutdownFailsDueToRecordProcessors`: notification completes,
        // the scheduler reports shutdown-complete but a consumer remains and the
        // shutdown-complete latch never fires → `workerShutdownWithRemaining` false.
        let notification = Arc::new(CountDownLatch::new_with_count(1));
        let shutdown = Arc::new(CountDownLatch::new_with_count(1)); // never fires
        let final_latch = Arc::new(CountDownLatch::new());

        let mut scheduler = MockSchedulerHandle::new();
        scheduler.expect_shutdown_complete().returning(|| true);
        // A consumer still remains (map not empty) — but shutdownComplete()==true
        // alone satisfies is_worker_shutdown_complete.
        scheduler
            .expect_shard_consumer_map_is_empty()
            .returning(|| false);
        scheduler.expect_shard_consumer_map_size().returning(|| 1);
        scheduler.expect_shutdown().returning(|| ());

        notification.count_down();
        let ctx = GracefulShutdownContext::new(
            Some(shutdown),
            Some(notification),
            Some(final_latch),
            Some(Arc::new(scheduler)),
        );
        assert!(!drive_to_completion(ctx).await.unwrap());
    }

    #[tokio::test(start_paused = true)]
    async fn shutdown_fails_due_to_worker() {
        // Java `testShutdownFailsDueToWorker`: record-processor shutdown succeeds,
        // but the final-shutdown latch never fires → the 60s bounded wait times
        // out and the callable returns false.
        let notification = Arc::new(CountDownLatch::new_with_count(1));
        let shutdown = Arc::new(CountDownLatch::new_with_count(1));
        let final_latch = Arc::new(CountDownLatch::new()); // never fires

        let ctx = GracefulShutdownContext::new(
            Some(shutdown.clone()),
            Some(notification.clone()),
            Some(final_latch),
            Some(Arc::new(scheduler_running(1))),
        );

        notification.count_down();
        shutdown.count_down();
        assert!(!drive_to_completion(ctx).await.unwrap());
    }

    #[tokio::test(start_paused = true)]
    async fn start_worker_shutdown_error_propagates() {
        let start = Box::new(move || {
            Box::pin(async move { Err(GracefulShutdownError("boom".to_string())) })
                as futures::future::BoxFuture<
                    'static,
                    Result<GracefulShutdownContext, GracefulShutdownError>,
                >
        }) as StartWorkerShutdown;
        let result = GracefulShutdownCoordinator::run_graceful_shutdown(start).await;
        assert!(result.is_err());
    }
}
