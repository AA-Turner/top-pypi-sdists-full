//! Port of `software.amazon.kinesis.lifecycle.ShardConsumerShutdownNotification`.
//!
//! Coordinates two "count-down-once" latches (notification-complete,
//! shutdown-complete) with the [`LeaseCoordinator`] to drop a lease once
//! notification completes and to guarantee both latches eventually fire even on
//! abnormal completion order.
//!
//! # Concurrency model
//!
//! Java uses a pair of `CountDownLatch(1)` an external caller (the Scheduler)
//! blocks on, plus two plain (non-volatile) `boolean` idempotency guards. The
//! Rust port models each latch as a [`CountDownLatch`] — a
//! [`tokio::sync::Notify`] gated by an [`AtomicBool`] (`count_down` is idempotent;
//! `await_latch` returns immediately once fired). The idempotency guards
//! (`notification_complete`/`all_notification_completed`) become `AtomicBool`s
//! (safer than Java's unsynchronized fields — the state machine guarantees no
//! concurrent same-instance calls, but atomics make it robust either way).

use std::sync::atomic::{AtomicBool, AtomicI64, Ordering};
use std::sync::Arc;

use tokio::sync::Notify;

use crate::leases::{Lease, LeaseCoordinator};
use crate::lifecycle::ShutdownNotification;

/// A counting count-down latch (`java.util.concurrent.CountDownLatch`).
///
/// [`new`](Self::new) creates a `CountDownLatch(1)` (the common single-use case,
/// used by [`ShardConsumerShutdownNotification`]); [`new_with_count`](Self::new_with_count)
/// creates a latch initialized to `n` (used by the graceful-shutdown coordinator,
/// which shares one latch across all shard consumers). `count_down` decrements
/// toward zero (never below), `await_latch` awaits it reaching zero, and
/// `get_count` reports the remaining count (Java `getCount()`).
#[derive(Default)]
pub struct CountDownLatch {
    count: AtomicI64,
    notify: Notify,
}

impl CountDownLatch {
    /// A new latch with count 1 (`CountDownLatch(1)`).
    pub fn new() -> Self {
        Self::new_with_count(1)
    }

    /// A new latch initialized to `count` (Java `new CountDownLatch(count)`).
    pub fn new_with_count(count: i64) -> Self {
        Self {
            count: AtomicI64::new(count.max(0)),
            notify: Notify::new(),
        }
    }

    /// Decrement the count toward zero (Java `countDown()`); a no-op once zero.
    /// Wakes all waiters when the count reaches zero.
    pub fn count_down(&self) {
        // Decrement but never below zero.
        let prev = self
            .count
            .fetch_update(Ordering::SeqCst, Ordering::SeqCst, |c| {
                if c > 0 {
                    Some(c - 1)
                } else {
                    None
                }
            });
        if let Ok(1) = prev {
            // Just transitioned to zero: wake all waiters.
            self.notify.notify_waiters();
        }
    }

    /// The remaining count (Java `getCount()`).
    pub fn get_count(&self) -> i64 {
        self.count.load(Ordering::SeqCst).max(0)
    }

    /// Whether the latch has fully counted down to zero.
    pub fn is_fired(&self) -> bool {
        self.count.load(Ordering::SeqCst) <= 0
    }

    /// Await the latch reaching zero (Java `await()`); returns immediately if
    /// already zero.
    pub async fn await_latch(&self) {
        loop {
            if self.is_fired() {
                return;
            }
            let notified = self.notify.notified();
            // Re-check after arming the future to avoid a lost wakeup.
            if self.is_fired() {
                return;
            }
            notified.await;
        }
    }
}

/// Production [`ShutdownNotification`] coordinating the two latches with the
/// [`LeaseCoordinator`]. Port of `ShardConsumerShutdownNotification`.
pub struct ShardConsumerShutdownNotification {
    lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    lease: Lease,
    notification_complete_latch: Arc<CountDownLatch>,
    shutdown_complete_latch: Arc<CountDownLatch>,

    notification_complete: AtomicBool,
    all_notification_completed: AtomicBool,
}

impl ShardConsumerShutdownNotification {
    /// Create a new shutdown request object.
    ///
    /// * `lease_coordinator` — used to drop the lease once the initial shutdown
    ///   request is complete.
    /// * `lease` — the lease freed once initial shutdown is complete.
    /// * `notification_complete_latch` — informs the caller the record processor
    ///   has been notified of the shutdown request.
    /// * `shutdown_complete_latch` — informs the caller the record processor is
    ///   fully shut down.
    pub fn new(
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
        lease: Lease,
        notification_complete_latch: Arc<CountDownLatch>,
        shutdown_complete_latch: Arc<CountDownLatch>,
    ) -> Self {
        Self {
            lease_coordinator,
            lease,
            notification_complete_latch,
            shutdown_complete_latch,
            notification_complete: AtomicBool::new(false),
            all_notification_completed: AtomicBool::new(false),
        }
    }
}

impl ShutdownNotification for ShardConsumerShutdownNotification {
    fn shutdown_notification_complete(&self) {
        if self.notification_complete.load(Ordering::SeqCst) {
            return;
        }
        // Once the notification has been completed, the lease needs to be dropped
        // to allow the worker to complete shutdown of the record processor.
        // Ordering matters: the lease is dropped BEFORE counting down the latch,
        // so callers awaiting the latch can assume the lease is already dropped.
        self.lease_coordinator.drop_lease(&self.lease);
        self.notification_complete_latch.count_down();
        self.notification_complete.store(true, Ordering::SeqCst);
    }

    fn shutdown_complete(&self) {
        if self.all_notification_completed.load(Ordering::SeqCst) {
            return;
        }
        // If shutdown jumped straight to complete without an explicit notification
        // step (e.g. lease-lost path skipping ShutdownNotificationTask), still
        // count down the notification latch so callers aren't blocked forever.
        if !self.notification_complete.load(Ordering::SeqCst) {
            self.notification_complete_latch.count_down();
        }
        self.shutdown_complete_latch.count_down();
        self.all_notification_completed
            .store(true, Ordering::SeqCst);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::MockLeaseCoordinator;

    fn lease() -> Lease {
        let mut l = Lease::default();
        l.set_lease_key("shardId-0".to_string());
        l
    }

    #[tokio::test]
    async fn notification_complete_drops_lease_then_fires_latch() {
        let mut coord = MockLeaseCoordinator::new();
        coord.expect_drop_lease().times(1).return_const(());
        let notif = Arc::new(CountDownLatch::new());
        let complete = Arc::new(CountDownLatch::new());
        let n = ShardConsumerShutdownNotification::new(
            Arc::new(coord),
            lease(),
            notif.clone(),
            complete.clone(),
        );

        n.shutdown_notification_complete();
        assert!(notif.is_fired());
        // Idempotent: a second call does not drop the lease again (times(1) above).
        n.shutdown_notification_complete();
    }

    #[tokio::test]
    async fn shutdown_complete_fires_both_latches_when_no_prior_notification() {
        let mut coord = MockLeaseCoordinator::new();
        coord.expect_drop_lease().return_const(());
        let notif = Arc::new(CountDownLatch::new());
        let complete = Arc::new(CountDownLatch::new());
        let n = ShardConsumerShutdownNotification::new(
            Arc::new(coord),
            lease(),
            notif.clone(),
            complete.clone(),
        );

        n.shutdown_complete();
        assert!(notif.is_fired());
        assert!(complete.is_fired());
        // Idempotent.
        n.shutdown_complete();
    }

    #[tokio::test]
    async fn latch_await_returns_after_count_down() {
        let latch = Arc::new(CountDownLatch::new());
        let l2 = latch.clone();
        let h = tokio::spawn(async move { l2.await_latch().await });
        // Give the task a chance to start awaiting, then fire.
        tokio::task::yield_now().await;
        latch.count_down();
        h.await.unwrap();
    }
}
