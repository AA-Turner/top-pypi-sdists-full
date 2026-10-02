//! Port of `software.amazon.kinesis.lifecycle.LeaseGracefulShutdownHandler`.
//!
//! Handles worker-initiated graceful lease handoff: when a lease is marked
//! `shutdownRequested()`, [`enqueue_shutdown`](LeaseGracefulShutdownHandler::enqueue_shutdown)
//! triggers [`ShardConsumer::graceful_shutdown`] and the background poller
//! monitors for completion or a timeout, after which it force-transfers the lease
//! to its designated new owner.
//!
//! # Concurrency model (tokio task + interval, replacing ScheduledExecutorService)
//!
//! Java uses a single-thread daemon `ScheduledExecutorService` running
//! `monitorGracefulShutdownLeases` at a fixed 2000ms rate. The Rust port:
//!
//! * The shard-info → consumer map is an injected
//!   `Arc<StdMutex<HashMap<ShardInfo, Arc<ShardConsumer>>>>` (Java's injected
//!   `ConcurrentMap`). The pending-shutdown tracker map is owned similarly.
//! * `start()` spawns a **tokio task** driving a [`tokio::time::interval`] at the
//!   (injectable) check period, cancelled via a [`tokio::sync::Notify`] on
//!   `stop()`. The period is injectable so tests can drive the loop directly (the
//!   test seam replaces the Java `scheduleAtFixedRate` `Runnable` capture — tests
//!   call [`monitor_graceful_shutdown_leases`](LeaseGracefulShutdownHandler::monitor_graceful_shutdown_leases)
//!   directly).
//! * `System::currentTimeMillis` → an injectable `TimeProvider`
//!   (`Arc<dyn Fn() -> i64>`) so timeouts are deterministically testable.
//! * `isRunning` (Java `volatile`) → `AtomicBool`.

use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex as StdMutex};
use std::time::Duration;

use tokio::sync::Notify;

use crate::leases::dynamodb::DynamoDBLeaseCoordinator;
use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, LeaseCoordinator, ShardInfo};
use crate::lifecycle::ShardConsumer;

/// The default poll interval (ms). Port of `SHUTDOWN_CHECK_INTERVAL_MILLIS`.
pub const SHUTDOWN_CHECK_INTERVAL_MILLIS: u64 = 2000;

/// Injectable wall-clock source (ms). Port of the Java `Supplier<Long>`
/// `System::currentTimeMillis`.
pub type TimeProvider = Arc<dyn Fn() -> i64 + Send + Sync>;

/// A shared map of shard-info → shard-consumer (Java's injected `ConcurrentMap`).
pub type ShardConsumerMap = Arc<StdMutex<HashMap<ShardInfo, Arc<ShardConsumer>>>>;

/// Per-lease shutdown tracking. Port of the private `LeasePendingShutdown`.
struct LeasePendingShutdown {
    lease: Lease,
    /// The consumer being shut down. Kept to mirror Java's `LeasePendingShutdown`
    /// (consumer lookups themselves go through the shared map, so this is not read
    /// on the monitor path).
    #[allow(dead_code)]
    shard_consumer: Arc<ShardConsumer>,
    timeout_timestamp_millis: i64,
    #[allow(dead_code)]
    shutdown_requested: bool,
    lease_transfer_called: bool,
}

/// Background poller for worker-initiated graceful lease handoff. Port of
/// `LeaseGracefulShutdownHandler`.
pub struct LeaseGracefulShutdownHandler {
    shutdown_timeout_millis: i64,
    shard_info_shard_consumer_map: ShardConsumerMap,
    lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    current_time_supplier: TimeProvider,
    shard_info_lease_pending_shutdown_map: StdMutex<HashMap<ShardInfo, LeasePendingShutdown>>,
    check_interval: Duration,

    is_running: AtomicBool,
    stop_notify: Notify,
}

impl LeaseGracefulShutdownHandler {
    /// Factory (Java `create(...)`), using `System::currentTimeMillis` and the
    /// default 2000ms interval.
    pub fn create(
        shutdown_timeout_millis: i64,
        shard_info_shard_consumer_map: ShardConsumerMap,
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    ) -> Arc<Self> {
        Self::new(
            shutdown_timeout_millis,
            shard_info_shard_consumer_map,
            lease_coordinator,
            Arc::new(|| chrono::Utc::now().timestamp_millis()),
            Duration::from_millis(SHUTDOWN_CHECK_INTERVAL_MILLIS),
        )
    }

    /// Full constructor (Java `@RequiredArgsConstructor` — used by tests to inject
    /// the time supplier + poll interval).
    pub fn new(
        shutdown_timeout_millis: i64,
        shard_info_shard_consumer_map: ShardConsumerMap,
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
        current_time_supplier: TimeProvider,
        check_interval: Duration,
    ) -> Arc<Self> {
        Arc::new(Self {
            shutdown_timeout_millis,
            shard_info_shard_consumer_map,
            lease_coordinator,
            current_time_supplier,
            shard_info_lease_pending_shutdown_map: StdMutex::new(HashMap::new()),
            check_interval,
            is_running: AtomicBool::new(false),
            stop_notify: Notify::new(),
        })
    }

    /// Start the poller. Port of `start()` — idempotent (a second `start` is a
    /// no-op). Spawns the interval-driven monitor task.
    pub fn start(self: &Arc<Self>) {
        if self.is_running.swap(true, Ordering::SeqCst) {
            tracing::info!("Graceful lease handoff thread already running, no need to start.");
            return;
        }
        tracing::info!("Starting graceful lease handoff thread.");
        let this = Arc::clone(self);
        let period = self.check_interval;
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(period);
            interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
            loop {
                tokio::select! {
                    _ = interval.tick() => {
                        this.monitor_graceful_shutdown_leases().await;
                    }
                    _ = this.stop_notify.notified() => break,
                }
            }
        });
    }

    /// Stop the poller. Port of `stop()` — idempotent.
    pub fn stop(&self) {
        if self.is_running.swap(false, Ordering::SeqCst) {
            tracing::info!("Stopping graceful lease handoff thread.");
            self.stop_notify.notify_waiters();
        } else {
            tracing::info!("Graceful lease handoff thread already stopped.");
        }
    }

    /// Whether the poller is running (Java `isRunning`).
    pub fn is_running(&self) -> bool {
        self.is_running.load(Ordering::SeqCst)
    }

    /// Enqueue a shutdown request for a lease. Port of `enqueueShutdown(lease)`.
    ///
    /// No-op if the lease is `None`, not `shutdownRequested()`, or the handler is
    /// not running. If the corresponding consumer is missing/already-shutdown,
    /// removes any stale tracking entry. Otherwise inserts a tracker (once) and
    /// initiates the shutdown on first insertion.
    pub async fn enqueue_shutdown(self: &Arc<Self>, lease: Option<&Lease>) {
        let Some(lease) = lease else { return };
        if !lease.shutdown_requested() || !self.is_running() {
            return;
        }
        let shard_info = DynamoDBLeaseCoordinator::convert_lease_to_assignment(lease);
        let consumer = self
            .shard_info_shard_consumer_map
            .lock()
            .unwrap()
            .get(&shard_info)
            .cloned();

        match consumer {
            None => {
                self.shard_info_lease_pending_shutdown_map
                    .lock()
                    .unwrap()
                    .remove(&shard_info);
            }
            Some(consumer) => {
                if consumer.is_shutdown() {
                    self.shard_info_lease_pending_shutdown_map
                        .lock()
                        .unwrap()
                        .remove(&shard_info);
                    return;
                }
                // computeIfAbsent: initiate shutdown only on first insertion.
                let already_present = self
                    .shard_info_lease_pending_shutdown_map
                    .lock()
                    .unwrap()
                    .contains_key(&shard_info);
                if !already_present {
                    tracing::info!(
                        "Calling graceful shutdown for lease {:?}",
                        lease.lease_key()
                    );
                    // initiateShutdown: gracefulShutdown(None) + compute timeout.
                    consumer.graceful_shutdown(None).await;
                    let timeout = (self.current_time_supplier)() + self.shutdown_timeout_millis;
                    self.shard_info_lease_pending_shutdown_map
                        .lock()
                        .unwrap()
                        .insert(
                            shard_info,
                            LeasePendingShutdown {
                                lease: lease.clone(),
                                shard_consumer: consumer,
                                timeout_timestamp_millis: timeout,
                                shutdown_requested: true,
                                lease_transfer_called: false,
                            },
                        );
                }
            }
        }
    }

    /// Wait for shutdown completion or transfer the lease on timeout. Port of
    /// `monitorGracefulShutdownLeases()`. **Public test seam** (the Java
    /// `scheduleAtFixedRate` `Runnable` capture): tests call this directly.
    pub async fn monitor_graceful_shutdown_leases(self: &Arc<Self>) {
        // Snapshot the tracked shard infos (Java iterates the ConcurrentMap).
        let shard_infos: Vec<ShardInfo> = self
            .shard_info_lease_pending_shutdown_map
            .lock()
            .unwrap()
            .keys()
            .cloned()
            .collect();

        for shard_info in shard_infos {
            let result = self.monitor_one(&shard_info).await;
            if let Err(e) = result {
                let lease_key = self
                    .shard_info_lease_pending_shutdown_map
                    .lock()
                    .unwrap()
                    .get(&shard_info)
                    .map(|t| t.lease.lease_key().map(str::to_string));
                tracing::error!(
                    "Error in graceful shutdown for lease {:?}: {}",
                    lease_key,
                    e
                );
            }
        }
    }

    async fn monitor_one(self: &Arc<Self>, shard_info: &ShardInfo) -> Result<(), LeasingError> {
        // Read the tracker fields we need (lease key, timeout, transfer-called).
        let (lease_key, timeout_ts, transfer_called) = {
            let map = self.shard_info_lease_pending_shutdown_map.lock().unwrap();
            let Some(t) = map.get(shard_info) else {
                return Ok(());
            };
            (
                t.lease.lease_key().map(str::to_string).unwrap_or_default(),
                t.timeout_timestamp_millis,
                t.lease_transfer_called,
            )
        };

        let consumer_present = self
            .shard_info_shard_consumer_map
            .lock()
            .unwrap()
            .contains_key(shard_info);
        let held = self
            .lease_coordinator
            .get_currently_held_lease(&lease_key)
            .is_some();

        if !consumer_present || !held {
            // SUCCESS / cleanup path: log a timeout message if a transfer was
            // attempted, then remove the tracking entry.
            self.log_timeout_message(shard_info);
            self.shard_info_lease_pending_shutdown_map
                .lock()
                .unwrap()
                .remove(shard_info);
        } else if (self.current_time_supplier)() >= timeout_ts && !transfer_called {
            tracing::info!(
                "Timeout {} ms reached waiting for lease {} to graceful handoff. Attempting to transfer.",
                self.shutdown_timeout_millis,
                lease_key
            );
            self.transfer_lease_if_owner(shard_info).await?;
        }
        Ok(())
    }

    fn log_timeout_message(&self, shard_info: &ShardInfo) {
        let map = self.shard_info_lease_pending_shutdown_map.lock().unwrap();
        if let Some(t) = map.get(shard_info) {
            if t.lease_transfer_called {
                let elapsed = (self.current_time_supplier)() - t.timeout_timestamp_millis
                    + self.shutdown_timeout_millis;
                tracing::info!(
                    "Lease {:?} took {} ms to complete the shutdown. \
                     Consider tuning the GracefulLeaseHandoffTimeoutMillis if necessary.",
                    t.lease.lease_key(),
                    elapsed
                );
            }
        }
    }

    async fn transfer_lease_if_owner(
        self: &Arc<Self>,
        shard_info: &ShardInfo,
    ) -> Result<(), LeasingError> {
        // Clone the lease so we can pass a `&mut Lease` to `attempt_lease_transfer`
        // (which mutates the lease's owner/counter). Then mark transfer-called.
        let mut lease = {
            let map = self.shard_info_lease_pending_shutdown_map.lock().unwrap();
            match map.get(shard_info) {
                Some(t) => t.lease.clone(),
                None => return Ok(()),
            }
        };
        attempt_lease_transfer(Some(&mut lease), self.lease_coordinator.as_ref()).await?;
        // Mark it true so we don't attempt again (update isn't possible anymore).
        if let Some(t) = self
            .shard_info_lease_pending_shutdown_map
            .lock()
            .unwrap()
            .get_mut(shard_info)
        {
            t.lease = lease;
            t.lease_transfer_called = true;
        }
        Ok(())
    }

    /// Number of leases currently pending shutdown (test accessor).
    pub fn pending_shutdown_count(&self) -> usize {
        self.shard_info_lease_pending_shutdown_map
            .lock()
            .unwrap()
            .len()
    }
}

impl LeaseGracefulShutdownHandler {
    /// Test accessor: whether the given shard-info's tracker has had a lease
    /// transfer attempted.
    #[cfg(test)]
    fn lease_transfer_called(&self, shard_info: &ShardInfo) -> bool {
        self.shard_info_lease_pending_shutdown_map
            .lock()
            .unwrap()
            .get(shard_info)
            .map(|t| t.lease_transfer_called)
            .unwrap_or(false)
    }
}

/// Port of the static `LeaseGracefulShutdownHandler.attemptLeaseTransfer`.
///
/// If the lease is non-null and has `shutdownRequested()` set (its
/// `checkpointOwner` is present), and the current worker is the recorded
/// `checkpointOwner` (a sanity check), hand the lease to its designated
/// `leaseOwner` via `leaseRefresher().assignLease(lease, lease.leaseOwner())`.
/// A worker-id mismatch just logs a warning.
pub async fn attempt_lease_transfer(
    lease: Option<&mut Lease>,
    lease_coordinator: &(dyn LeaseCoordinator + Send + Sync),
) -> Result<(), LeasingError> {
    let Some(lease) = lease else {
        return Ok(());
    };
    if !lease.shutdown_requested() {
        return Ok(());
    }
    let worker_id = lease_coordinator.worker_identifier();
    if Some(worker_id.as_str()) == lease.checkpoint_owner() {
        let new_owner = lease.lease_owner().map(str::to_string).unwrap_or_default();
        lease_coordinator
            .lease_refresher()
            .assign_lease(lease, &new_owner)
            .await?;
    } else {
        tracing::warn!(
            "Lease {:?} checkpoint owner mismatch found {:?} but it should be {}",
            lease.lease_key(),
            lease.checkpoint_owner(),
            worker_id
        );
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    include!("lease_graceful_shutdown_handler_tests.rs");
}
