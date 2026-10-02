//! Port of `software.amazon.kinesis.common.FutureUtils`.
//!
//! # Deviations from Java
//!
//! - `resolveOrCancelFuture(Future, Duration)` is a **blocking** get-with-timeout
//!   that calls `future.cancel(true)` on timeout. In this async port it becomes
//!   [`resolve_or_cancel`], an `async fn` using [`tokio::time::timeout`]. On
//!   timeout the wrapped future is **dropped**, which is Rust's cooperative
//!   cancellation. Java's `cancel(true)` (`mayInterruptIfRunning`) is a
//!   best-effort thread interrupt with different, non-guaranteed semantics; the
//!   drop-based cancellation here is the accepted equivalent (documented
//!   behavioral approximation).
//! - `unwrappingFuture(Supplier<CompletableFuture<T>>)` exists only to unwrap
//!   `CompletionException` down to its `RuntimeException` cause after `join()`.
//!   Rust async errors propagate via `Result`/`?` without an interposed wrapper,
//!   so there is **no equivalent** to port — call sites just `.await?`.

use std::future::Future;
use std::time::Duration;

/// Returned by [`resolve_or_cancel`] when the future does not complete within
/// the timeout (the wrapped future has been dropped/cancelled).
///
/// The async analog of Java's `TimeoutException` from
/// `resolveOrCancelFuture` — after which the underlying future is cancelled.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TimedOut;

impl std::fmt::Display for TimedOut {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "future did not complete within the timeout and was cancelled"
        )
    }
}

impl std::error::Error for TimedOut {}

/// Await `future`, cancelling it if it does not complete within `timeout`.
///
/// Async equivalent of Java's `resolveOrCancelFuture(future, timeout)`: returns
/// the resolved value, or [`TimedOut`] if the timeout elapses first (at which
/// point the future is dropped, i.e. cooperatively cancelled — the analog of
/// Java's `future.cancel(true)`).
pub async fn resolve_or_cancel<F, T>(future: F, timeout: Duration) -> Result<T, TimedOut>
where
    F: Future<Output = T>,
{
    match tokio::time::timeout(timeout, future).await {
        Ok(value) => Ok(value),
        Err(_elapsed) => Err(TimedOut),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicBool, Ordering};
    use std::sync::Arc;

    #[tokio::test]
    async fn resolves_within_timeout() {
        let result = resolve_or_cancel(async { 42 }, Duration::from_secs(1)).await;
        assert_eq!(result, Ok(42));
    }

    // Port of FutureUtilsTest.testTimeoutExceptionCancelsFuture: a future that
    // never completes times out AND is cancelled (dropped before running to
    // completion). We assert the "completed" flag was never set.
    #[tokio::test(start_paused = true)]
    async fn timeout_cancels_future() {
        let completed = Arc::new(AtomicBool::new(false));
        let completed_clone = completed.clone();

        let never = async move {
            // Sleep far longer than the timeout; if the future were not
            // cancelled it would eventually set `completed`.
            tokio::time::sleep(Duration::from_secs(3600)).await;
            completed_clone.store(true, Ordering::SeqCst);
        };

        let result = resolve_or_cancel(never, Duration::from_millis(10)).await;
        assert_eq!(result, Err(TimedOut));
        // The wrapped future was dropped on timeout, so it never completed.
        assert!(!completed.load(Ordering::SeqCst));
    }

    #[test]
    fn timed_out_displays() {
        assert!(!TimedOut.to_string().is_empty());
    }
}
