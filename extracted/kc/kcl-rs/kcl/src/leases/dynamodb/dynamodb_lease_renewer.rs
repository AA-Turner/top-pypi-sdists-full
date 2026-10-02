//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBLeaseRenewer`.
//!
//! Implements [`LeaseRenewer`] using DynamoDB via a [`LeaseRefresher`]:
//! maintains the authoritative in-memory map of leases owned by this worker
//! (`owned_leases`), periodically renews them in DynamoDB **in parallel**,
//! tracks per-lease throughput stats, supports application-driven checkpoint
//! updates, and cooperates with graceful lease handoff.
//!
//! # Concurrency model
//!
//! Java uses a `ConcurrentSkipListMap<String, Lease>` (`owned_leases`) plus a
//! per-`Lease` intrinsic monitor (`synchronized(lease)`) to guard each
//! read-modify-write, and an `ExecutorService` fan-out (one `Callable` per
//! lease, joined in submission order) for renewal.
//!
//! The Rust port models each held lease as an `Arc<tokio::sync::Mutex<Lease>>`
//! (the per-lease monitor) stored in a `BTreeMap<String, ...>` behind a
//! `std::sync::Mutex` (the map lock — never held across `.await`). The
//! `BTreeMap` preserves the sorted key order so `renew_leases` can iterate in
//! **descending** key order like Java. Renewal fans out with
//! [`futures::future::join_all`] over per-lease async tasks (tokio's equivalent
//! of the executor), preserving the property that a lease's renewal locks only
//! its own lease. Getters return `.copy()` snapshots, never the live object.
//!
//! # Graceful-handoff wiring
//!
//! Java's `Consumer<Lease> leaseGracefulShutdownCallback` (wired to
//! `LeaseGracefulShutdownHandler::enqueueShutdown`, a lifecycle-wave type) →
//! [`GracefulShutdownCallback`] = `Arc<dyn Fn(Lease) + Send + Sync>`. The
//! coordinator supplies a no-op placeholder until the lifecycle wave (7) ports
//! the real handler.
//!
//! # Deviations
//!
//! - The Java `ExecutorService` + `Future` fan-out becomes `join_all`; there is
//!   no distinct "interrupted" vs "execution-exception" split (Rust tasks don't
//!   throw `InterruptedException`), so `leases_in_unknown_state` counts only
//!   genuine renewal errors (Java's `ExecutionException` path). The
//!   "throw `DependencyException` if any lease is in an unknown state" behavior
//!   is preserved.

use std::collections::BTreeMap;
use std::sync::{Arc, Mutex};

use async_trait::async_trait;
use uuid::Uuid;

use crate::leases::exceptions::LeasingError;
use crate::leases::{
    Lease, LeaseRefresher, LeaseRenewer, LeaseStats, LeaseStatsRecorder, BYTES_PER_KB,
};
use crate::metrics::MetricsFactory;

const RENEWAL_RETRIES: i32 = 2;
/// 6 digits after the decimal gives 0.001 byte/second granularity.
const DEFAULT_THROUGHPUT_DIGIT_AFTER_DECIMAL: u32 = 6;

/// The graceful-shutdown callback (Java `Consumer<Lease>`), invoked with a
/// defensive copy of a shutdown-requested lease during renewal.
pub type GracefulShutdownCallback = Arc<dyn Fn(Lease) + Send + Sync>;

/// A held lease and its per-lease monitor (Java `synchronized(lease)`).
type HeldLease = Arc<tokio::sync::Mutex<Lease>>;

/// DynamoDB implementation of [`LeaseRenewer`].
pub struct DynamoDBLeaseRenewer {
    lease_refresher: Arc<dyn LeaseRefresher>,
    worker_identifier: String,
    lease_duration_nanos: i64,
    #[allow(dead_code)]
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    lease_stats_recorder: Arc<LeaseStatsRecorder>,
    lease_graceful_shutdown_callback: GracefulShutdownCallback,
    lease_table_scan_total_segments: i32,
    /// Authoritative held-lease map (Java `ConcurrentSkipListMap`). `BTreeMap`
    /// keeps keys sorted so `renew_leases` iterates in descending order.
    owned_leases: Mutex<BTreeMap<String, HeldLease>>,
    /// Injectable monotonic-nanos clock (Java `System.nanoTime()`).
    time_provider: NanoTimeProvider,
}

/// A time provider returning nanoseconds (Java `System.nanoTime()`).
pub type NanoTimeProvider = Arc<dyn Fn() -> i64 + Send + Sync>;

impl DynamoDBLeaseRenewer {
    /// Java constructor.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        lease_refresher: Arc<dyn LeaseRefresher>,
        worker_identifier: impl Into<String>,
        lease_duration_millis: i64,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        lease_stats_recorder: Arc<LeaseStatsRecorder>,
        lease_graceful_shutdown_callback: GracefulShutdownCallback,
        lease_table_scan_total_segments: i32,
    ) -> Self {
        Self {
            lease_refresher,
            worker_identifier: worker_identifier.into(),
            lease_duration_nanos: lease_duration_millis * 1_000_000,
            metrics_factory,
            lease_stats_recorder,
            lease_graceful_shutdown_callback,
            lease_table_scan_total_segments,
            owned_leases: Mutex::new(BTreeMap::new()),
            time_provider: default_nano_time_provider(),
        }
    }

    /// Override the time provider (test seam).
    pub fn with_time_provider(mut self, time_provider: NanoTimeProvider) -> Self {
        self.time_provider = time_provider;
        self
    }

    fn now_nanos(&self) -> i64 {
        (self.time_provider)()
    }

    /// Snapshot the held-lease handles in **descending** key order (Java
    /// `ownedLeases.descendingMap().values()`).
    fn snapshot_descending(&self) -> Vec<(String, HeldLease)> {
        let map = self.owned_leases.lock().unwrap();
        map.iter()
            .rev()
            .map(|(k, v)| (k.clone(), v.clone()))
            .collect()
    }

    /// Java `isCheckpointOwner`: whether this worker should renew the lease.
    ///
    /// If graceful shutdown is requested (`checkpointOwner` set), the only valid
    /// state for this worker to renew is `checkpointOwner == workerId` AND
    /// `leaseOwner != workerId` (this worker is the OLD owner still finishing).
    fn is_checkpoint_owner(&self, lease: &Lease) -> bool {
        if !lease.shutdown_requested() {
            return true;
        }
        lease.checkpoint_owner() == Some(self.worker_identifier.as_str())
            && lease.lease_owner() != Some(self.worker_identifier.as_str())
    }

    /// Java `renewLease(lease, renewEvenIfExpired)` — renews a single held lease.
    ///
    /// Returns `Ok(true)` if the lease was renewed. Removes the lease from
    /// `owned_leases` on loss / checkpoint-owner-mismatch.
    async fn renew_lease(
        &self,
        held: &HeldLease,
        lease_key: &str,
        renew_even_if_expired: bool,
    ) -> Result<bool, LeasingError> {
        // Check (outside the per-lease lock) whether this worker should renew.
        {
            let lease = held.lock().await;
            if !self.is_checkpoint_owner(&lease) {
                drop(lease);
                self.owned_leases.lock().unwrap().remove(lease_key);
                return Ok(false);
            }
        }

        let mut renewed_lease = false;

        for _ in 1..=RENEWAL_RETRIES {
            // synchronized(lease): the whole read-modify-write of one lease.
            let mut lease = held.lock().await;

            let result: Result<(), LeasingError> = async {
                let is_lease_expired =
                    lease.is_expired(self.lease_duration_nanos, self.now_nanos());
                if renew_even_if_expired || !is_lease_expired {
                    if let Some(throughput) =
                        self.lease_stats_recorder.get_throughput_kbps(lease_key)
                    {
                        lease.set_throughput_kbps(round_half_up(
                            throughput,
                            DEFAULT_THROUGHPUT_DIGIT_AFTER_DECIMAL,
                        ));
                    }
                    renewed_lease = self.lease_refresher.renew_lease(&mut lease).await?;
                }
                if renewed_lease {
                    lease.set_last_counter_increment_nanos(Some(self.now_nanos()));
                }
                if lease.shutdown_requested() {
                    // The underlying handler dedups.
                    (self.lease_graceful_shutdown_callback)(lease.copy());
                }
                Ok(())
            }
            .await;

            match result {
                Ok(()) => {
                    if !renewed_lease {
                        drop(lease);
                        self.owned_leases.lock().unwrap().remove(lease_key);
                    }
                    break;
                }
                Err(e) if is_provisioned_throughput(&e) => {
                    // retry on capacity errors only
                }
                Err(e) => return Err(e),
            }
        }

        Ok(renewed_lease)
    }

    /// Internal: a lease with a specific key only if we currently hold it and it
    /// isn't stale (Java `getCopyOfHeldLease`).
    async fn get_copy_of_held_lease(&self, lease_key: &str, now: i64) -> Option<Lease> {
        let held = {
            let map = self.owned_leases.lock().unwrap();
            map.get(lease_key).cloned()
        }?;
        let copy = {
            let lease = held.lock().await;
            lease.copy()
        };
        if copy.is_expired(self.lease_duration_nanos, now) {
            None
        } else {
            Some(copy)
        }
    }

    /// Async form of [`get_currently_held_leases`](LeaseRenewer::get_currently_held_leases).
    async fn currently_held_leases_async(&self) -> std::collections::HashMap<String, Lease> {
        let mut result = std::collections::HashMap::new();
        let now = self.now_nanos();
        let keys: Vec<String> = {
            let map = self.owned_leases.lock().unwrap();
            map.keys().cloned().collect()
        };
        for key in keys {
            if let Some(copy) = self.get_copy_of_held_lease(&key, now).await {
                if let Some(k) = copy.lease_key() {
                    result.insert(k.to_string(), copy);
                }
            }
        }
        result
    }

    /// Async form of [`add_leases_to_renew`](LeaseRenewer::add_leases_to_renew).
    fn add_leases_to_renew_impl(&self, new_leases: Vec<Lease>) {
        for lease in new_leases {
            if lease.last_counter_increment_nanos().is_none() {
                // Callers MUST set lastCounterIncrementNanos first; skip otherwise.
                continue;
            }

            let mut authoritative_lease = lease.copy();
            // Fresh concurrency token on every acquisition.
            authoritative_lease.set_concurrency_token(Uuid::new_v4());

            if let Some(throughput) = lease.throughput_kbps() {
                self.lease_stats_recorder.record_stats(LeaseStats::new(
                    lease.lease_key().unwrap_or("").to_string(),
                    (throughput * BYTES_PER_KB).round() as i64,
                    now_millis(),
                ));
            }

            let key = authoritative_lease.lease_key().unwrap_or("").to_string();
            self.owned_leases
                .lock()
                .unwrap()
                .insert(key, Arc::new(tokio::sync::Mutex::new(authoritative_lease)));
        }
    }
}

#[async_trait]
impl LeaseRenewer for DynamoDBLeaseRenewer {
    async fn initialize(&self) -> Result<(), LeasingError> {
        // Java swallows ANY exception during initialize (logs a warning), relying
        // on the lease-assignment logic to reassign anything missed.
        let result: Result<(), LeasingError> = async {
            let (leases, failed_keys) = self
                .lease_refresher
                .list_leases_parallely(self.lease_table_scan_total_segments)
                .await?;

            if !failed_keys.is_empty() {
                tracing::warn!("List of leaseKeys failed to deserialize: {:?}", failed_keys);
            }

            let mut my_leases: Vec<Lease> = Vec::new();
            for mut lease in leases {
                if lease.lease_owner() == Some(self.worker_identifier.as_str()) {
                    // Skip leases in pending-checkpoint state (being shut down by
                    // the previous owner).
                    if lease.checkpoint_owner().is_some() {
                        continue;
                    }
                    // Renew even if expired: nothing has been exposed to the
                    // application yet, and we only add on successful renew.
                    let key = lease.lease_key().unwrap_or("").to_string();
                    let held: HeldLease = Arc::new(tokio::sync::Mutex::new(lease.clone()));
                    if self.renew_lease(&held, &key, true).await? {
                        // Copy back the mutated (counter/throughput) lease.
                        lease = held.lock().await.copy();
                        my_leases.push(lease);
                    }
                }
            }

            self.add_leases_to_renew_impl(my_leases);
            Ok(())
        }
        .await;

        if let Err(e) = result {
            tracing::warn!(
                "LeaseRefresher failed in initialization during renewing of pre assigned leases: {}",
                e
            );
        }
        Ok(())
    }

    async fn renew_leases(&self) -> Result<(), LeasingError> {
        let handles = self.snapshot_descending();

        // Fan out: each future renews one lease (locking only its own monitor).
        let futures = handles
            .iter()
            .map(|(key, held)| self.renew_lease(held, key, false))
            .collect::<Vec<_>>();
        let results = futures::future::join_all(futures).await;

        let mut leases_in_unknown_state = 0;
        let mut last_error: Option<LeasingError> = None;
        for r in results {
            match r {
                Ok(true) => {}
                Ok(false) => { /* lost lease */ }
                Err(e) => {
                    leases_in_unknown_state += 1;
                    last_error = Some(e);
                }
            }
        }

        if leases_in_unknown_state > 0 {
            let msg = format!(
                "Encountered an exception while renewing leases. The number of leases which might not have been renewed is {}",
                leases_in_unknown_state
            );
            return Err(match last_error {
                Some(e) => LeasingError::dependency_caused_by(msg, Box::new(e)),
                None => LeasingError::dependency(msg),
            });
        }

        Ok(())
    }

    fn get_currently_held_leases(&self) -> std::collections::HashMap<String, Lease> {
        // Sync accessor over async internals: drive the async snapshot on a
        // dedicated current-thread runtime block. In practice callers run inside
        // the tokio runtime; use `block_in_place` + a handle when available,
        // else a fresh runtime.
        run_sync(self.currently_held_leases_async())
    }

    fn get_currently_held_lease(&self, lease_key: &str) -> Option<Lease> {
        let now = self.now_nanos();
        run_sync(self.get_copy_of_held_lease(lease_key, now))
    }

    fn add_leases_to_renew(&self, new_leases: Vec<Lease>) {
        self.add_leases_to_renew_impl(new_leases);
    }

    fn clear_currently_held_leases(&self) {
        self.owned_leases.lock().unwrap().clear();
    }

    fn drop_lease(&self, lease: &Lease) {
        if let Some(key) = lease.lease_key() {
            self.lease_stats_recorder.drop_lease_stats(key);
            self.owned_leases.lock().unwrap().remove(key);
        }
    }

    async fn update_lease(
        &self,
        lease: &Lease,
        concurrency_token: Uuid,
        _operation: &str,
        _single_stream_shard_id: &str,
    ) -> Result<bool, LeasingError> {
        let lease_key = match lease.lease_key() {
            Some(k) => k.to_string(),
            None => panic!("leaseKey cannot be null"),
        };

        let held = {
            let map = self.owned_leases.lock().unwrap();
            map.get(&lease_key).cloned()
        };
        let held = match held {
            Some(h) => h,
            None => {
                // We don't hold it.
                return Ok(false);
            }
        };

        // Concurrency-token guard: refuse if it doesn't match the authoritative
        // lease's token (lease was lost + regained since the caller acquired it).
        {
            let authoritative = held.lock().await;
            if authoritative.concurrency_token() != Some(concurrency_token) {
                return Ok(false);
            }
        }

        // synchronized(authoritativeLease): mutate, write, and either bump the
        // counter clock or pro-actively remove on conditional failure.
        let mut authoritative = held.lock().await;
        let authoritative_lease_copy = authoritative.copy();
        authoritative.update(lease);

        match self.lease_refresher.update_lease(&mut authoritative).await {
            Ok(true) => {
                authoritative.set_last_counter_increment_nanos(Some(self.now_nanos()));
                Ok(true)
            }
            Ok(false) => {
                // Someone took the lease. Remove only if the value currently in
                // the map is still the SAME authoritative lease object (Java
                // `ownedLeases.remove(key, value)`) — guards the lost+reacquired
                // race. We compare by `Arc` identity, which is even stricter than
                // Java's value equality but has the same effect: if the map entry
                // was swapped out (lease lost + regained puts a new `Arc`), we
                // don't remove it (the fresh `Arc` from add_leases_to_renew is a
                // distinct object, mirroring the counter-based inequality Java
                // relies on).
                drop(authoritative);
                let mut map = self.owned_leases.lock().unwrap();
                if let Some(cur) = map.get(&lease_key) {
                    if Arc::ptr_eq(cur, &held) {
                        map.remove(&lease_key);
                    }
                }
                Ok(false)
            }
            Err(e) => {
                // On DDB failure, revert the in-memory mutation.
                authoritative.update(&authoritative_lease_copy);
                Err(e)
            }
        }
    }
}

/// Java `BigDecimal.setScale(scale, HALF_UP).doubleValue()`.
fn round_half_up(value: f64, scale: u32) -> f64 {
    let factor = 10f64.powi(scale as i32);
    (value * factor).round() / factor
}

fn is_provisioned_throughput(e: &LeasingError) -> bool {
    matches!(e, LeasingError::ProvisionedThroughput { .. })
}

/// Java `System::nanoTime` — the process-wide monotonic clock. Must share its
/// epoch with the taker/discoverer: leases arrive here carrying
/// `last_counter_increment_nanos` stamps from THEIR clocks, and the expiry
/// check compares those stamps against this one.
fn default_nano_time_provider() -> NanoTimeProvider {
    Arc::new(crate::utils::monotonic_clock::monotonic_nanos)
}

fn now_millis() -> i64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

/// Run an async future to completion from a **sync** context. Used by the sync
/// accessors (`get_currently_held_lease(s)`) whose internals touch per-lease
/// `tokio::sync::Mutex`es.
///
/// - Inside a **multi-thread** runtime: `block_in_place` + `block_on` (the
///   canonical bridge; the KCL scheduler runs multi-threaded in production).
/// - Inside a **current-thread** runtime (e.g. `#[tokio::test(start_paused)]`):
///   `block_in_place` would panic, so drive the future on a fresh current-thread
///   runtime running on a **separate OS thread** (safe: the future only touches
///   in-process `tokio::sync::Mutex`es, no I/O bound to the outer runtime).
/// - No runtime at all: a tiny current-thread runtime inline.
fn run_sync<F>(fut: F) -> F::Output
where
    F: std::future::Future + Send,
    F::Output: Send,
{
    match tokio::runtime::Handle::try_current() {
        Ok(handle) => match handle.runtime_flavor() {
            tokio::runtime::RuntimeFlavor::CurrentThread => std::thread::scope(|s| {
                s.spawn(|| {
                    tokio::runtime::Builder::new_current_thread()
                        .enable_all()
                        .build()
                        .unwrap()
                        .block_on(fut)
                })
                .join()
                .unwrap()
            }),
            _ => tokio::task::block_in_place(|| handle.block_on(fut)),
        },
        Err(_) => tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .unwrap()
            .block_on(fut),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::kpl::ExtendedSequenceNumber;
    use std::sync::atomic::{AtomicUsize, Ordering};

    const WORKER_ID: &str = "WorkerId";

    fn recorder() -> Arc<LeaseStatsRecorder> {
        Arc::new(LeaseStatsRecorder::new(1000, Arc::new(now_millis)))
    }

    fn noop_callback() -> GracefulShutdownCallback {
        Arc::new(|_lease| {})
    }

    fn create_dummy_lease(lease_key: &str, lease_owner: &str) -> Lease {
        let mut lease = Lease::default();
        lease.set_lease_key(lease_key);
        lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
        lease.set_lease_owner(Some(lease_owner.to_string()));
        lease.set_lease_counter(123);
        lease.set_throughput_kbps(1.0);
        lease.set_last_counter_increment_nanos(Some(1)); // non-null, "just now"
        lease
    }

    fn renewer(
        refresher: Arc<dyn LeaseRefresher>,
        stats: Arc<LeaseStatsRecorder>,
    ) -> DynamoDBLeaseRenewer {
        DynamoDBLeaseRenewer::new(
            refresher,
            WORKER_ID,
            60 * 60 * 1000, // 1 hour
            Arc::new(NullMetricsFactory),
            stats,
            noop_callback(),
            1,
        )
        // Fixed monotonic clock at a small value so freshly-added leases (nanos=1)
        // aren't considered expired.
        .with_time_provider(Arc::new(|| 2))
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn add_and_get_currently_held_leases() {
        let refresher = Arc::new(MockLeaseRefresher::new());
        let r = renewer(refresher, recorder());
        r.add_leases_to_renew(vec![create_dummy_lease("key-1", WORKER_ID)]);
        let held = r.get_currently_held_leases();
        assert_eq!(held.len(), 1);
        assert!(held.contains_key("key-1"));
        // The returned copy carries a fresh concurrency token.
        assert!(held.get("key-1").unwrap().concurrency_token().is_some());
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn add_leases_skips_leases_without_last_counter_increment_nanos() {
        let refresher = Arc::new(MockLeaseRefresher::new());
        let r = renewer(refresher, recorder());
        let mut lease = create_dummy_lease("key-1", WORKER_ID);
        lease.set_last_counter_increment_nanos(None);
        r.add_leases_to_renew(vec![lease]);
        assert!(r.get_currently_held_leases().is_empty());
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn renew_leases_success_keeps_lease() {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let r = renewer(Arc::new(refresher), recorder());
        r.add_leases_to_renew(vec![create_dummy_lease("key-1", WORKER_ID)]);
        r.renew_leases().await.unwrap();
        assert_eq!(r.get_currently_held_leases().len(), 1);
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn renew_leases_lost_lease_removed() {
        let mut refresher = MockLeaseRefresher::new();
        // renew_lease returns false -> lease is lost.
        refresher.expect_renew_lease().returning(|_lease| Ok(false));
        let r = renewer(Arc::new(refresher), recorder());
        r.add_leases_to_renew(vec![create_dummy_lease("key-1", WORKER_ID)]);
        r.renew_leases().await.unwrap();
        assert_eq!(r.get_currently_held_leases().len(), 0);
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn renew_leases_error_throws_dependency() {
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_renew_lease()
            .returning(|_lease| Err(LeasingError::invalid_state("boom")));
        let r = renewer(Arc::new(refresher), recorder());
        r.add_leases_to_renew(vec![create_dummy_lease("key-1", WORKER_ID)]);
        let err = r.renew_leases().await.unwrap_err();
        assert!(matches!(err, LeasingError::Dependency { .. }));
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn renewal_drops_lease_when_checkpoint_owner_mismatch() {
        // checkpointOwner set to "other worker" (not WORKER_ID) -> not renewable,
        // dropped without contacting DDB.
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(|_l| Ok(true));
        let r = renewer(Arc::new(refresher), recorder());
        let mut lease = create_dummy_lease("testLease", WORKER_ID);
        lease.set_checkpoint_owner(Some("other worker".to_string()));
        r.add_leases_to_renew(vec![lease]);
        assert_eq!(r.get_currently_held_leases().len(), 1);
        r.renew_leases().await.unwrap();
        assert_eq!(r.get_currently_held_leases().len(), 0);
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn renewal_renews_shutdown_requested_lease_if_checkpoint_owner_matches() {
        // leaseOwner="random", checkpointOwner=WORKER_ID -> this worker is the
        // OLD owner and should keep renewing.
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let r = renewer(Arc::new(refresher), recorder());
        let mut lease = create_dummy_lease("testLease", "random");
        lease.set_checkpoint_owner(Some(WORKER_ID.to_string()));
        r.add_leases_to_renew(vec![lease]);
        assert_eq!(r.get_currently_held_leases().len(), 1);
        r.renew_leases().await.unwrap();
        assert_eq!(r.get_currently_held_leases().len(), 1);
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn enqueue_shutdown_requested_lease_calls_callback() {
        // A shutdown-requested lease held by this worker triggers the callback on
        // each renewal pass.
        let count = Arc::new(AtomicUsize::new(0));
        let count2 = count.clone();
        let callback: GracefulShutdownCallback = Arc::new(move |_lease| {
            count2.fetch_add(1, Ordering::SeqCst);
        });
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let r = DynamoDBLeaseRenewer::new(
            Arc::new(refresher),
            WORKER_ID,
            60 * 60 * 1000,
            Arc::new(NullMetricsFactory),
            recorder(),
            callback,
            1,
        )
        .with_time_provider(Arc::new(|| 2));

        // Lease held by this worker (leaseOwner=random, checkpointOwner=WORKER_ID)
        // is shutdown-requested (checkpointOwner set) -> callback fires.
        let mut lease = create_dummy_lease("key-1", "random");
        lease.set_checkpoint_owner(Some(WORKER_ID.to_string()));
        r.add_leases_to_renew(vec![lease]);

        r.renew_leases().await.unwrap();
        assert_eq!(count.load(Ordering::SeqCst), 1);
        r.renew_leases().await.unwrap();
        assert_eq!(count.load(Ordering::SeqCst), 2);
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn update_lease_rejects_wrong_concurrency_token() {
        let refresher = Arc::new(MockLeaseRefresher::new());
        let r = renewer(refresher, recorder());
        r.add_leases_to_renew(vec![create_dummy_lease("key-1", WORKER_ID)]);
        let updated = create_dummy_lease("key-1", WORKER_ID);
        // A random token that won't match the authoritative one.
        let ok = r
            .update_lease(&updated, Uuid::new_v4(), "test", "shard")
            .await
            .unwrap();
        assert!(!ok);
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn update_lease_reverts_in_memory_on_ddb_failure() {
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_update_lease()
            .returning(|_l| Err(LeasingError::dependency("ddb down")));
        let r = renewer(Arc::new(refresher), recorder());
        r.add_leases_to_renew(vec![create_dummy_lease("leaseToUpdate", WORKER_ID)]);
        let token = r
            .get_currently_held_lease("leaseToUpdate")
            .unwrap()
            .concurrency_token()
            .unwrap();
        let mut updated = create_dummy_lease("leaseToUpdate", WORKER_ID);
        updated.set_checkpoint(ExtendedSequenceNumber::latest());
        let err = r
            .update_lease(&updated, token, "test", "shard")
            .await
            .unwrap_err();
        assert!(matches!(err, LeasingError::Dependency { .. }));
        // Counter unchanged and checkpoint reverted to TRIM_HORIZON.
        let current = r.get_currently_held_leases();
        let current = current.get("leaseToUpdate").unwrap();
        assert_eq!(current.lease_counter(), 123);
        assert_eq!(
            current.checkpoint(),
            Some(&ExtendedSequenceNumber::trim_horizon())
        );
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn update_lease_success_increments_and_persists() {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_update_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let r = renewer(Arc::new(refresher), recorder());
        r.add_leases_to_renew(vec![create_dummy_lease("k", WORKER_ID)]);
        let token = r
            .get_currently_held_lease("k")
            .unwrap()
            .concurrency_token()
            .unwrap();
        let mut updated = create_dummy_lease("k", WORKER_ID);
        updated.set_checkpoint(ExtendedSequenceNumber::latest());
        let ok = r
            .update_lease(&updated, token, "test", "shard")
            .await
            .unwrap();
        assert!(ok);
        let held = r.get_currently_held_leases();
        assert_eq!(
            held.get("k").unwrap().checkpoint(),
            Some(&ExtendedSequenceNumber::latest())
        );
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_picks_up_own_leases_skipping_pending_checkpoint() {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_list_leases_parallely().returning(|_seg| {
            let mut normal = create_dummy_lease("normalLease", WORKER_ID);
            normal.set_last_counter_increment_nanos(Some(1));
            let mut pending = create_dummy_lease("pendingLease", WORKER_ID);
            pending.set_checkpoint_owner(Some("OtherWorker".to_string()));
            let other = create_dummy_lease("otherOwnerLease", "leaseOwner2");
            Ok((vec![normal, pending, other], vec![]))
        });
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let r = renewer(Arc::new(refresher), recorder());
        r.initialize().await.unwrap();
        let held = r.get_currently_held_leases();
        assert_eq!(held.len(), 1);
        assert!(held.contains_key("normalLease"));
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_swallows_errors() {
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_list_leases_parallely()
            .returning(|_seg| Err(LeasingError::dependency("scan failed")));
        let r = renewer(Arc::new(refresher), recorder());
        // Must not propagate.
        r.initialize().await.unwrap();
        assert!(r.get_currently_held_leases().is_empty());
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn drop_lease_removes_from_held() {
        let refresher = Arc::new(MockLeaseRefresher::new());
        let r = renewer(refresher, recorder());
        let lease = create_dummy_lease("key-1", WORKER_ID);
        r.add_leases_to_renew(vec![lease.clone()]);
        assert_eq!(r.get_currently_held_leases().len(), 1);
        r.drop_lease(&lease);
        assert_eq!(r.get_currently_held_leases().len(), 0);
    }

    // --- round_half_up (throughput persistence) ---

    /// Port of the parameterized
    /// `DynamoDBLeaseRenewerTest.renewLeases_withDifferentInputFromLeaseRecorder_assertNoFailureAndExpectedValue`
    /// CSV cases (plus the `withHighInitialDecimalDigit` value). The renewer
    /// applies `round_half_up(throughput, 6)` before persisting; these cover the
    /// below-DDB-range, higher-precision, mid-range, and all-zero-decimal inputs.
    #[test]
    fn round_half_up_matches_java_csv_cases() {
        const SCALE: u32 = DEFAULT_THROUGHPUT_DIGIT_AFTER_DECIMAL;
        // (inputNumber string, expected)
        let below_ddb_range = "0.00000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000001";
        let higher_precision = "1.00000000000000000000000000000000000001";
        let high_decimal = "0.00000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000016843473634062791";
        let all_zero_decimal = "0.00000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000";

        let cases: &[(&str, f64)] = &[
            (below_ddb_range, 0.0),
            (higher_precision, 1.0),
            ("1.024", 1.024),
            ("1024.1024", 1024.1024),
            ("1024.102412324", 1024.102412),
            ("1999999.123213213123123213213", 1999999.123213),
            (high_decimal, 0.0),
            (all_zero_decimal, 0.0),
            // withHighInitialDecimalDigit: recorder reports ~0.1.
            ("0.10000000000000000001", 0.1),
        ];

        for (input, expected) in cases {
            let value: f64 = input.parse().unwrap();
            let rounded = round_half_up(value, SCALE);
            assert_eq!(
                rounded, *expected,
                "round_half_up({input}) = {rounded}, expected {expected}"
            );
        }
    }

    /// Port of `DynamoDBLeaseRenewerTest.renewLeases_withHighInitialDecimalDigit_assertUpdateWithoutFailureAndNewStats`
    /// at the renewer level: a lease whose throughput came from the recorder is
    /// persisted with the rounded value (the pre-existing tiny throughput is
    /// overwritten). Uses a real `LeaseStatsRecorder` fed a single sample and
    /// asserts the persisted throughput equals `round_half_up(recorder_value, 6)`.
    #[tokio::test(flavor = "multi_thread")]
    async fn renew_leases_rounds_recorder_throughput_before_persisting() {
        use crate::leases::lease_stats_recorder::LeaseStats;

        // Deterministic recorder: renewer frequency 60s, fixed clock.
        let stats = Arc::new(LeaseStatsRecorder::new(60_000, Arc::new(|| 1_000)));
        // 3 MB over the window -> a value with many fractional digits.
        for _ in 0..3 {
            stats.record_stats(LeaseStats::new("key-1", 1024 * 1024, 0));
        }
        let recorder_value = stats.get_throughput_kbps("key-1").unwrap();
        let expected = round_half_up(recorder_value, DEFAULT_THROUGHPUT_DIGIT_AFTER_DECIMAL);

        let persisted = std::sync::Arc::new(std::sync::Mutex::new(None::<f64>));
        let persisted_clone = persisted.clone();
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(move |lease| {
            *persisted_clone.lock().unwrap() = lease.throughput_kbps();
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });

        let r = renewer(Arc::new(refresher), stats);
        // Pre-existing lease throughput is an unrelated tiny value.
        let mut lease = create_dummy_lease("key-1", WORKER_ID);
        lease.set_throughput_kbps(0.000_000_000_1);
        r.add_leases_to_renew(vec![lease]);
        r.renew_leases().await.unwrap();

        let persisted = persisted.lock().unwrap().expect("renew_lease was called");
        assert_eq!(persisted, expected);
    }

    // --- initialize with a bad (undeserializable) lease in the table ---

    /// Port of `DynamoDBLeaseRenewerTest.initialize_badLeaseInTableExists_assertInitializationWithOtherLeases`.
    ///
    /// The parallel scan returns four leases owned by this worker, two owned by a
    /// different worker, and one deserialization failure (the "bad lease" key).
    /// After `initialize()`, only this worker's four (deserializable) leases are
    /// held.
    #[tokio::test(flavor = "multi_thread")]
    async fn initialize_bad_lease_in_table_exists_initializes_with_other_leases() {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_list_leases_parallely().returning(|_seg| {
            let mut mine = Vec::new();
            for key in ["leaseKey1", "leaseKey2", "leaseKey3", "leaseKey4"] {
                let mut l = create_dummy_lease(key, WORKER_ID);
                l.set_last_counter_increment_nanos(Some(1));
                mine.push(l);
            }
            let other1 = create_dummy_lease("leaseKey5", "leaseOwner2");
            let other2 = create_dummy_lease("leaseKey6", "leaseOwner2");
            let mut leases = mine;
            leases.push(other1);
            leases.push(other2);
            // The "bad lease" surfaces as a deserialization failure key.
            Ok((leases, vec!["badLeaseKey".to_string()]))
        });
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });

        let r = renewer(Arc::new(refresher), recorder());
        r.initialize().await.unwrap();

        let held = r.get_currently_held_leases();
        assert_eq!(held.len(), 4);
        assert!(held.contains_key("leaseKey1"));
        assert!(held.contains_key("leaseKey2"));
        assert!(held.contains_key("leaseKey3"));
        assert!(held.contains_key("leaseKey4"));
    }

    // --- Ported DynamoDBLeaseRenewerIntegrationTest scenarios ---
    //
    // Java runs these against a real DynamoDB; here the refresher is a
    // `MockLeaseRefresher` scripted to model the DB side effects (renew/take
    // returning true/false). A lease starting at counter 0 that increments on
    // each successful renew matches the Java harness (renew -> counter 1).

    fn lease_counter0(lease_key: &str, owner: &str) -> Lease {
        let mut lease = create_dummy_lease(lease_key, owner);
        lease.set_lease_counter(0);
        lease
    }

    /// Port of `DynamoDBLeaseRenewerIntegrationTest.testGetCurrentlyHeldLease`.
    ///
    /// `get_currently_held_lease` returns a defensive copy that does not track
    /// subsequent renewals of the authoritative lease.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_get_currently_held_lease() {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let r = renewer(Arc::new(refresher), recorder());
        r.add_leases_to_renew(vec![lease_counter0("1", WORKER_ID)]);
        r.renew_leases().await.unwrap();

        // Copy after the first renewal: counter == 1.
        let lease = r.get_currently_held_lease("1").unwrap();
        assert_eq!(lease.lease_counter(), 1);

        // Another renewal advances the authoritative counter...
        r.renew_leases().await.unwrap();
        // ...but the previously returned copy is unchanged.
        assert_eq!(lease.lease_counter(), 1);
    }

    /// Port of `DynamoDBLeaseRenewerIntegrationTest.testUpdateOldLease`.
    ///
    /// After the lease is lost to another owner and the renewer notices (a failing
    /// renew drops it), `update_lease` returns `false`.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_update_old_lease() {
        // renew: succeed once (add), then fail (lease taken by "bar") -> dropped.
        let renew_calls = Arc::new(AtomicUsize::new(0));
        let renew_calls2 = renew_calls.clone();
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(move |lease| {
            let n = renew_calls2.fetch_add(1, Ordering::SeqCst);
            if n == 0 {
                lease.set_lease_counter(lease.lease_counter() + 1);
                Ok(true)
            } else {
                Ok(false) // lease lost
            }
        });
        let r = renewer(Arc::new(refresher), recorder());
        r.add_leases_to_renew(vec![lease_counter0("1", WORKER_ID)]);
        r.renew_leases().await.unwrap();

        let mut lease = r.get_currently_held_lease("1").unwrap();
        // Lost the lease: the next renewal fails and drops it from the renewer.
        r.renew_leases().await.unwrap();
        assert!(r.get_currently_held_lease("1").is_none());

        lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number(
            "new checkpoint",
        ));
        let token = lease.concurrency_token().unwrap();
        let ok = r.update_lease(&lease, token, "test", "1").await.unwrap();
        assert!(!ok);
    }

    /// Port of `DynamoDBLeaseRenewerIntegrationTest.testUpdateRegainedLease`.
    ///
    /// After losing the lease and re-adding it (fresh concurrency token), an
    /// update using the *old* token returns `false`.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_update_regained_lease() {
        let renew_calls = Arc::new(AtomicUsize::new(0));
        let renew_calls2 = renew_calls.clone();
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(move |lease| {
            let n = renew_calls2.fetch_add(1, Ordering::SeqCst);
            if n == 0 {
                lease.set_lease_counter(lease.lease_counter() + 1);
                Ok(true)
            } else {
                Ok(false) // lease lost
            }
        });
        let r = renewer(Arc::new(refresher), recorder());
        r.add_leases_to_renew(vec![lease_counter0("1", WORKER_ID)]);
        r.renew_leases().await.unwrap();

        let mut lease = r.get_currently_held_lease("1").unwrap();
        // Lose the lease.
        r.renew_leases().await.unwrap();
        assert!(r.get_currently_held_lease("1").is_none());

        // Regain it: a fresh add mints a new concurrency token.
        r.add_leases_to_renew(vec![lease_counter0("1", WORKER_ID)]);

        lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number(
            "new checkpoint",
        ));
        // Update with the OLD token -> rejected.
        let old_token = lease.concurrency_token().unwrap();
        let ok = r
            .update_lease(&lease, old_token, "test", "1")
            .await
            .unwrap();
        assert!(!ok);
    }

    /// Port of `DynamoDBLeaseRenewerIntegrationTest.testIgnoreNoRenewalTimestamp`.
    ///
    /// A lease with no `lastCounterIncrementNanos` is not added to the renewer.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_ignore_no_renewal_timestamp() {
        let refresher = Arc::new(MockLeaseRefresher::new());
        let r = renewer(refresher, recorder());
        let mut lease = create_dummy_lease("1", "foo");
        lease.set_last_counter_increment_nanos(None);
        r.add_leases_to_renew(vec![lease]);
        assert_eq!(r.get_currently_held_leases().len(), 0);
    }

    /// Port of `DynamoDBLeaseRenewerIntegrationTest.testLeaseTimeout`.
    ///
    /// Once the lease's age exceeds the lease duration, it is filtered out of the
    /// currently-held set. Uses a controllable clock that jumps past the duration.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_lease_timeout() {
        use std::sync::atomic::AtomicI64;
        // Clock starts at 10 (so the freshly-added lease at nanos=10 is fresh),
        // then jumps past the lease duration on later reads.
        let clock = Arc::new(AtomicI64::new(10));
        let clock2 = clock.clone();
        let lease_duration_millis: i64 = 1000;
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let r = DynamoDBLeaseRenewer::new(
            Arc::new(refresher),
            WORKER_ID,
            lease_duration_millis,
            Arc::new(NullMetricsFactory),
            recorder(),
            noop_callback(),
            1,
        )
        .with_time_provider(Arc::new(move || clock2.load(Ordering::SeqCst)));

        let mut lease = create_dummy_lease("1", WORKER_ID);
        lease.set_last_counter_increment_nanos(Some(10));
        r.add_leases_to_renew(vec![lease]);
        r.renew_leases().await.unwrap();
        assert_eq!(r.get_currently_held_leases().len(), 1);

        // Advance well beyond the lease duration (in nanos) -> the lease times out.
        clock.store(10 + lease_duration_millis * 1_000_000 * 2, Ordering::SeqCst);
        assert_eq!(r.get_currently_held_leases().len(), 0);
    }

    /// Port of `DynamoDBLeaseRenewerIntegrationTest.testInitializeBillingMode`
    /// (identical assertions to `testInitialize`): `initialize()` picks up the
    /// worker's pre-assigned leases.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_initialize_billing_mode() {
        const OWNER: &str = "foo:8000";
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_list_leases_parallely().returning(|_seg| {
            let mut lease = create_dummy_lease("shd-0-0", OWNER);
            lease.set_last_counter_increment_nanos(Some(1));
            Ok((vec![lease], vec![]))
        });
        refresher.expect_renew_lease().returning(|lease| {
            lease.set_lease_counter(lease.lease_counter() + 1);
            Ok(true)
        });
        let r = DynamoDBLeaseRenewer::new(
            Arc::new(refresher),
            OWNER,
            30_000,
            Arc::new(NullMetricsFactory),
            recorder(),
            noop_callback(),
            1,
        )
        .with_time_provider(Arc::new(|| 2));

        r.initialize().await.unwrap();

        let held = r.get_currently_held_leases();
        assert_eq!(held.len(), 1);
        assert!(held.contains_key("shd-0-0"));
    }
}
