//! Port of `software.amazon.kinesis.leases.LeaseCleanupManager`.
//!
//! Background manager that periodically deletes leases for shards that have
//! either (a) been fully processed (`SHARD_END`, all children now processing,
//! all parent leases already deleted) or (b) become "garbage" (the shard no
//! longer exists — discovered via `ResourceNotFoundException`).
//!
//! # Concurrency (deviation)
//!
//! Java uses an injected `ScheduledExecutorService` +
//! `scheduleAtFixedRate(LeaseCleanupThread, 0, leaseCleanupIntervalMillis)` and
//! a lock-free `ConcurrentLinkedQueue`, with two Guava `Stopwatch` timers gating
//! the two independent cleanup checks. The Rust port:
//!
//! - queue → `Mutex<VecDeque<LeasePendingDeletion>>`.
//! - two Guava stopwatches → two [`Stopwatch`]es backed by an **injectable
//!   clock** ([`Clock`]) so the cadence is deterministically testable. The
//!   "only reset the stopwatch if progress was made" semantic is preserved.
//! - the periodic thread → a spawned tokio task started by [`start`], stopped
//!   via a `tokio::sync::Notify` shutdown signal in [`shutdown`]. The task calls
//!   the same [`cleanup_leases`](LeaseCleanupManager::cleanup_leases) entry point
//!   that tests drive directly (Java's `@VisibleForTesting cleanupLeases()`).
//!
//! # Deletion gate preserved EXACTLY
//!
//! `cleanup_lease_for_completed_shard`: a completed shard's lease is deletable
//! only when the **full** child-lease-key set exactly equals the subset whose
//! checkpoint has progressed past `TRIM_HORIZON`/`AT_TIMESTAMP` (children have
//! started real processing) **AND** all parent leases are gone. A child lease
//! unexpectedly missing from the table is a hard error (Java
//! `IllegalStateException`). Completed-shard-path exceptions are **swallowed** so
//! garbage collection can still run in the same call.

use std::collections::HashSet;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Duration;

use tokio::sync::Notify;

use crate::leases::exceptions::{LeasePendingDeletion, LeasingError};
use crate::leases::{Lease, LeaseCoordinator, ShardInfo, UpdateField};
use crate::metrics::MetricsFactory;
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Injectable monotonic clock (elapsed milliseconds). Java uses Guava
/// `Stopwatch` (a `System.nanoTime`-based elapsed timer); the Rust port abstracts
/// "now in millis" so tests can control cadence deterministically.
pub type Clock = Arc<dyn Fn() -> i64 + Send + Sync>;

fn default_clock() -> Clock {
    Arc::new(|| {
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.as_millis() as i64)
            .unwrap_or(0)
    })
}

/// Elapsed-time timer (Java Guava `Stopwatch`), driven by an injectable clock.
struct Stopwatch {
    clock: Clock,
    started_at: Mutex<Option<i64>>,
}

impl Stopwatch {
    fn new(clock: Clock) -> Self {
        Self {
            clock,
            started_at: Mutex::new(None),
        }
    }
    fn reset_and_start(&self) {
        *self.started_at.lock().unwrap() = Some((self.clock)());
    }
    fn stop(&self) {
        *self.started_at.lock().unwrap() = None;
    }
    fn elapsed_millis(&self) -> i64 {
        match *self.started_at.lock().unwrap() {
            Some(start) => (self.clock)() - start,
            None => 0,
        }
    }
}

/// Result of attempting to clean up one lease. Port of the nested
/// `@Value LeaseCleanupResult`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LeaseCleanupResult {
    cleaned_up_completed_lease: bool,
    cleaned_up_garbage_lease: bool,
    were_child_shards_present: bool,
    was_resource_not_found: bool,
}

impl LeaseCleanupResult {
    pub fn cleaned_up_completed_lease(&self) -> bool {
        self.cleaned_up_completed_lease
    }
    pub fn cleaned_up_garbage_lease(&self) -> bool {
        self.cleaned_up_garbage_lease
    }
    pub fn were_child_shards_present(&self) -> bool {
        self.were_child_shards_present
    }
    pub fn was_resource_not_found(&self) -> bool {
        self.was_resource_not_found
    }
    /// Java `leaseCleanedUp()` = OR of the two cleaned-up flags.
    pub fn lease_cleaned_up(&self) -> bool {
        self.cleaned_up_completed_lease || self.cleaned_up_garbage_lease
    }
}

/// The lease-cleanup manager.
pub struct LeaseCleanupManager {
    lease_coordinator: Arc<dyn LeaseCoordinator>,
    #[allow(dead_code)]
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    cleanup_leases_upon_shard_completion: bool,
    lease_cleanup_interval_millis: i64,
    completed_lease_cleanup_interval_millis: i64,
    garbage_lease_cleanup_interval_millis: i64,

    completed_lease_stopwatch: Stopwatch,
    garbage_lease_stopwatch: Stopwatch,
    deletion_queue: Mutex<std::collections::VecDeque<LeasePendingDeletion>>,
    is_running: AtomicBool,
    shutdown_signal: Arc<Notify>,
}

impl LeaseCleanupManager {
    /// Construct a lease-cleanup manager (mirrors the Java
    /// `@RequiredArgsConstructor`), using the wall clock.
    pub fn new(
        lease_coordinator: Arc<dyn LeaseCoordinator>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        cleanup_leases_upon_shard_completion: bool,
        lease_cleanup_interval_millis: i64,
        completed_lease_cleanup_interval_millis: i64,
        garbage_lease_cleanup_interval_millis: i64,
    ) -> Self {
        Self::with_clock(
            lease_coordinator,
            metrics_factory,
            cleanup_leases_upon_shard_completion,
            lease_cleanup_interval_millis,
            completed_lease_cleanup_interval_millis,
            garbage_lease_cleanup_interval_millis,
            default_clock(),
        )
    }

    /// Construct with an injectable clock (test seam for cadence).
    #[allow(clippy::too_many_arguments)]
    pub fn with_clock(
        lease_coordinator: Arc<dyn LeaseCoordinator>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        cleanup_leases_upon_shard_completion: bool,
        lease_cleanup_interval_millis: i64,
        completed_lease_cleanup_interval_millis: i64,
        garbage_lease_cleanup_interval_millis: i64,
        clock: Clock,
    ) -> Self {
        Self {
            lease_coordinator,
            metrics_factory,
            cleanup_leases_upon_shard_completion,
            lease_cleanup_interval_millis,
            completed_lease_cleanup_interval_millis,
            garbage_lease_cleanup_interval_millis,
            completed_lease_stopwatch: Stopwatch::new(clock.clone()),
            garbage_lease_stopwatch: Stopwatch::new(clock),
            deletion_queue: Mutex::new(std::collections::VecDeque::new()),
            is_running: AtomicBool::new(false),
            shutdown_signal: Arc::new(Notify::new()),
        }
    }

    /// Whether the cleanup loop is running (Java `isRunning`).
    pub fn is_running(&self) -> bool {
        self.is_running.load(Ordering::SeqCst)
    }

    /// Start the periodic lease-cleanup task. Idempotent (Java `start`).
    ///
    /// Requires `self` to be shared via `Arc` so the spawned task can call back.
    pub fn start(self: &Arc<Self>) {
        if !self.is_running.swap(true, Ordering::SeqCst) {
            self.completed_lease_stopwatch.reset_and_start();
            self.garbage_lease_stopwatch.reset_and_start();
            let this = self.clone();
            let interval_ms = self.lease_cleanup_interval_millis.max(1) as u64;
            let shutdown = self.shutdown_signal.clone();
            tokio::spawn(async move {
                let mut ticker = tokio::time::interval(Duration::from_millis(interval_ms));
                loop {
                    tokio::select! {
                        _ = ticker.tick() => {
                            // Java LeaseCleanupManager catches per-lease Exception
                            // inside cleanupLeases; contain panics (Java unchecked
                            // exceptions) too so a bad lease cannot kill the loop.
                            if let Err(panic) =
                                crate::utils::panic_util::catch_tick(this.cleanup_leases()).await
                            {
                                tracing::error!("Failed to cleanup leases: {}", panic);
                            }
                        }
                        _ = shutdown.notified() => break,
                    }
                }
            });
        }
    }

    /// Stop the periodic task. Idempotent (Java `shutdown`).
    pub fn shutdown(&self) {
        if self.is_running.swap(false, Ordering::SeqCst) {
            self.completed_lease_stopwatch.stop();
            self.garbage_lease_stopwatch.stop();
            self.shutdown_signal.notify_waiters();
        }
    }

    /// Enqueue a lease for deferred deletion (no dedup — Java `enqueueForDeletion`).
    pub fn enqueue_for_deletion(&self, lease_pending_deletion: LeasePendingDeletion) {
        // Java warns if the lease is null; our LeasePendingDeletion always holds
        // a lease, so there is no null case to guard.
        self.deletion_queue
            .lock()
            .unwrap()
            .push_back(lease_pending_deletion);
    }

    /// Whether a lease is already enqueued (dedup by lease key — see the
    /// [`LeasePendingDeletion`] note about why this is by lease key, not by
    /// full structural equality). Java `isEnqueuedForDeletion` scans the queue.
    pub fn is_enqueued_for_deletion(&self, lease_pending_deletion: &LeasePendingDeletion) -> bool {
        let target = lease_pending_deletion.lease().lease_key();
        self.deletion_queue
            .lock()
            .unwrap()
            .iter()
            .any(|p| p.lease().lease_key() == target)
    }

    fn leases_pending_deletion(&self) -> usize {
        self.deletion_queue.lock().unwrap().len()
    }

    /// Number of leases currently enqueued for deferred deletion. Exposed for
    /// tests (the lifecycle `ShutdownTask` tests assert on enqueue behavior).
    pub fn pending_deletion_count(&self) -> usize {
        self.deletion_queue.lock().unwrap().len()
    }

    fn time_to_check_for_completed_shard(&self) -> bool {
        self.completed_lease_stopwatch.elapsed_millis()
            >= self.completed_lease_cleanup_interval_millis
    }

    fn time_to_check_for_garbage_shard(&self) -> bool {
        self.garbage_lease_stopwatch.elapsed_millis() >= self.garbage_lease_cleanup_interval_millis
    }

    /// Core per-lease decision logic (Java `cleanupLease`).
    pub async fn cleanup_lease(
        &self,
        lease_pending_deletion: &LeasePendingDeletion,
        time_to_check_for_completed_shard: bool,
        time_to_check_for_garbage_shard: bool,
    ) -> Result<LeaseCleanupResult, LeasingError> {
        let lease = lease_pending_deletion.lease();
        let shard_info = lease_pending_deletion.shard_info();

        let mut cleaned_up_completed_lease = false;
        let mut cleaned_up_garbage_lease = false;
        let mut already_checked_for_garbage_collection = false;
        let mut were_child_shards_present = false;
        let mut was_resource_not_found = false;

        // --- completed-shard path (exceptions swallowed except RNF) ---
        let mut resource_not_found = false;
        if self.cleanup_leases_upon_shard_completion && time_to_check_for_completed_shard {
            let lease_from_ddb = self
                .lease_coordinator
                .lease_refresher()
                .get_lease(lease.lease_key().unwrap_or_default())
                .await?;
            match lease_from_ddb {
                Some(lease_from_ddb) => {
                    let mut child_shard_keys = lease_from_ddb.child_shard_ids();
                    if child_shard_keys.is_empty() {
                        already_checked_for_garbage_collection = true;
                        match lease_pending_deletion.get_child_shards_from_service().await {
                            Ok(keys) => {
                                child_shard_keys = keys;
                                if child_shard_keys.is_empty() {
                                    // No child shards from service; leave as-is.
                                } else {
                                    were_child_shards_present = true;
                                    self.update_lease_with_child_shards(
                                        lease_pending_deletion,
                                        &child_shard_keys,
                                    )
                                    .await?;
                                }
                            }
                            Err(e) => {
                                if is_resource_not_found(&e) {
                                    resource_not_found = true;
                                } else {
                                    return Err(e);
                                }
                            }
                        }
                    } else {
                        were_child_shards_present = true;
                    }

                    if !resource_not_found {
                        // Suppress errors so garbage cleanup can still be attempted.
                        match self
                            .cleanup_lease_for_completed_shard(lease, shard_info, &child_shard_keys)
                            .await
                        {
                            Ok(cleaned) => cleaned_up_completed_lease = cleaned,
                            Err(_e) => { /* swallowed (Java log.warn) */ }
                        }
                    }
                }
                None => {
                    // Lease not present in table → treat as cleaned up.
                    cleaned_up_completed_lease = true;
                }
            }
        }

        // --- garbage-shard path ---
        if !resource_not_found
            && !already_checked_for_garbage_collection
            && time_to_check_for_garbage_shard
        {
            match lease_pending_deletion.get_child_shards_from_service().await {
                Ok(keys) => were_child_shards_present = !keys.is_empty(),
                Err(e) => {
                    if is_resource_not_found(&e) {
                        resource_not_found = true;
                    } else {
                        return Err(e);
                    }
                }
            }
        }

        if resource_not_found {
            was_resource_not_found = true;
            cleaned_up_garbage_lease = self.cleanup_lease_for_garbage_shard(lease).await?;
        }

        Ok(LeaseCleanupResult {
            cleaned_up_completed_lease,
            cleaned_up_garbage_lease,
            were_child_shards_present,
            was_resource_not_found,
        })
    }

    async fn cleanup_lease_for_garbage_shard(&self, lease: &Lease) -> Result<bool, LeasingError> {
        self.lease_coordinator
            .lease_refresher()
            .delete_lease(lease)
            .await?;
        Ok(true)
    }

    /// Whether all parent shard leases for `lease` are already deleted (Java
    /// `allParentShardLeasesDeleted`).
    async fn all_parent_shard_leases_deleted(
        &self,
        lease: &Lease,
        shard_info: &ShardInfo,
    ) -> Result<bool, LeasingError> {
        for parent_shard in lease.parent_shard_ids() {
            let parent_lease_key = shard_info.lease_key_with_override(&parent_shard);
            let parent_lease = self
                .lease_coordinator
                .lease_refresher()
                .get_lease(&parent_lease_key)
                .await?;
            if parent_lease.is_some() {
                return Ok(false);
            }
        }
        Ok(true)
    }

    /// The deletion gate for a completed shard (Java `cleanupLeaseForCompletedShard`).
    ///
    /// # Errors
    /// Returns [`LeasingError::InvalidState`] if a child lease is unexpectedly
    /// missing from the table (Java `IllegalStateException`; the caller swallows
    /// it for the completed path).
    async fn cleanup_lease_for_completed_shard(
        &self,
        lease: &Lease,
        shard_info: &ShardInfo,
        child_shard_keys: &HashSet<String>,
    ) -> Result<bool, LeasingError> {
        let mut processed_child_shard_lease_keys: HashSet<String> = HashSet::new();
        let child_shard_lease_keys: HashSet<String> = child_shard_keys
            .iter()
            .map(|ck| shard_info.lease_key_with_override(ck))
            .collect();

        for child_shard_lease_key in &child_shard_lease_keys {
            let child_shard_lease = self
                .lease_coordinator
                .lease_refresher()
                .get_lease(child_shard_lease_key)
                .await?;
            let child_shard_lease = match child_shard_lease {
                Some(l) => l,
                None => {
                    return Err(LeasingError::invalid_state(format!(
                        "Child lease {} for completed shard not found in lease table - not cleaning up lease {:?}",
                        child_shard_lease_key,
                        lease.lease_key()
                    )))
                }
            };

            let cp = child_shard_lease.checkpoint();
            let is_trim_horizon = cp == Some(&ExtendedSequenceNumber::trim_horizon());
            let is_at_timestamp = cp == Some(&ExtendedSequenceNumber::at_timestamp());
            if !is_trim_horizon && !is_at_timestamp {
                processed_child_shard_lease_keys
                    .insert(child_shard_lease.lease_key().unwrap().to_string());
            }
        }

        if !self
            .all_parent_shard_leases_deleted(lease, shard_info)
            .await?
            || child_shard_lease_keys != processed_child_shard_lease_keys
        {
            return Ok(false);
        }

        self.lease_coordinator
            .lease_refresher()
            .delete_lease(lease)
            .await?;
        Ok(true)
    }

    async fn update_lease_with_child_shards(
        &self,
        lease_pending_deletion: &LeasePendingDeletion,
        child_shard_keys: &HashSet<String>,
    ) -> Result<(), LeasingError> {
        let mut updated_lease = lease_pending_deletion.lease().clone();
        updated_lease.set_child_shard_ids(child_shard_keys.iter().cloned());
        self.lease_coordinator
            .lease_refresher()
            .update_lease_with_meta_info(&updated_lease, UpdateField::ChildShards)
            .await
    }

    /// The periodic batch-processing entry point (Java `@VisibleForTesting
    /// cleanupLeases()`). Drains the entire queue, re-enqueues failures, and
    /// resets each stopwatch only if progress was made in that category.
    pub async fn cleanup_leases(&self) {
        if self.leases_pending_deletion() == 0 {
            return;
        }
        // Java uses bitwise OR so both are evaluated (both are side-effect-free
        // stopwatch reads); `||` is behaviorally identical here.
        if !(self.time_to_check_for_completed_shard() || self.time_to_check_for_garbage_shard()) {
            return;
        }

        let mut failed_deletions: Vec<LeasePendingDeletion> = Vec::new();
        let mut completed_lease_cleaned_up = false;
        let mut garbage_lease_cleaned_up = false;

        loop {
            let pending = { self.deletion_queue.lock().unwrap().pop_front() };
            let pending = match pending {
                Some(p) => p,
                None => break,
            };
            let mut deletion_succeeded = false;
            match self
                .cleanup_lease(
                    &pending,
                    self.time_to_check_for_completed_shard(),
                    self.time_to_check_for_garbage_shard(),
                )
                .await
            {
                Ok(result) => {
                    completed_lease_cleaned_up |= result.cleaned_up_completed_lease();
                    garbage_lease_cleaned_up |= result.cleaned_up_garbage_lease();
                    if result.lease_cleaned_up() {
                        deletion_succeeded = true;
                    }
                }
                Err(_e) => { /* log.error + re-enqueue */ }
            }
            if !deletion_succeeded {
                failed_deletions.push(pending);
            }
        }

        if completed_lease_cleaned_up {
            self.completed_lease_stopwatch.reset_and_start();
        }
        if garbage_lease_cleaned_up {
            self.garbage_lease_stopwatch.reset_and_start();
        }
        let mut queue = self.deletion_queue.lock().unwrap();
        for f in failed_deletions {
            queue.push_back(f);
        }
    }
}

/// Whether a leasing error wraps a Kinesis `ResourceNotFoundException` (Java's
/// AWSExceptionManager registered for `ResourceNotFoundException.class`).
fn is_resource_not_found(e: &LeasingError) -> bool {
    use std::error::Error;
    if let Some(source) = std::error::Error::source(e) {
        // Walk the cause chain looking for the SDK RNF error type.
        let mut current: Option<&(dyn Error + 'static)> = Some(source);
        while let Some(err) = current {
            if err
                .downcast_ref::<aws_sdk_kinesis::types::error::ResourceNotFoundException>()
                .is_some()
            {
                return true;
            }
            // The SDK often boxes the operation-error enum; match its Display.
            let msg = err.to_string();
            if msg.contains("ResourceNotFoundException") || msg.contains("Stream no longer exists")
            {
                return true;
            }
            current = err.source();
        }
    }
    // Fall back to matching the top-level message.
    e.message().contains("ResourceNotFoundException")
        || e.message().contains("Stream no longer exists")
}

#[cfg(test)]
mod tests;
