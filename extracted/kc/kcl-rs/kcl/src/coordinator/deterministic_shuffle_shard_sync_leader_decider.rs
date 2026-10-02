//! Port of
//! `software.amazon.kinesis.coordinator.DeterministicShuffleShardSyncLeaderDecider`.
//!
//! Elects leader(s) that perform periodic shard-sync, based on `workerId`. The
//! distinct, sorted set of lease owners is shuffled with a **fixed seed**
//! ([`DETERMINISTIC_SHUFFLE_SEED`] = 1947) so that every worker computes the
//! *identical* ordering and therefore agrees on the leader set without
//! coordination. Shuffling (rather than natural string ordering) spreads the
//! elected leaders across hosts even when worker ids share a common prefix
//! (e.g. an IP address), improving shard-sync redundancy during host failures.
//!
//! # Byte-identical shuffle (critical)
//!
//! To keep the leader set stable across a fleet, the shuffle must be
//! **byte-identical to Java**. [`JavaRandom`] replicates `java.util.Random`'s
//! 48-bit LCG (`nextInt(int)` power-of-two fast path + rejection loop) exactly,
//! and [`java_shuffle`] replicates `java.util.Collections.shuffle`'s algorithm
//! (iterate `i` from `size-1` down to `1`, swap `i` with `nextInt(i+1)`).
//!
//! # Concurrency (deviation)
//!
//! Java double-locks: the `isLeader`/`shutdown` methods are `synchronized` **and**
//! an inner `ReadWriteLock` guards the `leaders` set. In Rust this collapses to a
//! single [`std::sync::Mutex<Option<HashSet<String>>>`] for `leaders` (held in a
//! shared [`Inner`] so the trait's `&self` methods can hand it to spawned tasks
//! and the async→sync bridge). The [`LeaderDecider::is_leader`] trait method is
//! **sync** but [`LeaseRefresher::list_leases`] is **async**, so the synchronous
//! first-call election bridges async→sync via
//! [`tokio::task::block_in_place`] + `Handle::block_on` (mirroring
//! [`StreamIdCacheResolverBridge`](crate::coordinator::stream_info::StreamIdCacheResolverBridge)).
//! The periodic re-election (Java `scheduleWithFixedDelay`, 60s initial delay /
//! 5min period) runs as a spawned tokio interval task; [`shutdown`] aborts it.
//!
//! [`shutdown`]: DeterministicShuffleShardSyncLeaderDecider::shutdown

use std::collections::HashSet;
use std::sync::{Arc, Mutex};

use aws_sdk_cloudwatch::types::StandardUnit;
use tokio::sync::Mutex as AsyncMutex;
use tokio::task::JoinHandle;

use crate::coordinator::leader_decider::{
    LeaderDecider, METRIC_OPERATION_LEADER_DECIDER, METRIC_OPERATION_LEADER_DECIDER_IS_LEADER,
};
use crate::leases::LeaseRefresher;
use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};
use crate::utils::panic_util;

/// Fixed seed so the shuffle order is preserved across workers. Java
/// `DeterministicShuffleShardSyncLeaderDecider.DETERMINISTIC_SHUFFLE_SEED`.
pub const DETERMINISTIC_SHUFFLE_SEED: i64 = 1947;

const ELECTION_INITIAL_DELAY_MILLIS: u64 = 60 * 1000;
const ELECTION_SCHEDULING_INTERVAL_MILLIS: u64 = 5 * 60 * 1000;

/// A faithful re-implementation of `java.util.Random` sufficient to reproduce
/// `Collections.shuffle`. Only the pieces used by the shuffle are ported:
/// the 48-bit linear-congruential generator, `next(bits)`, and `nextInt(bound)`.
#[derive(Debug)]
pub struct JavaRandom {
    seed: i64,
}

impl JavaRandom {
    const MULTIPLIER: i64 = 0x5DEECE66D;
    const ADDEND: i64 = 0xB;
    const MASK: i64 = (1 << 48) - 1;

    /// Java `new Random(seed)` — scrambles the seed identically.
    pub fn new(seed: i64) -> Self {
        Self {
            seed: (seed ^ Self::MULTIPLIER) & Self::MASK,
        }
    }

    /// Java `protected int next(int bits)`.
    fn next(&mut self, bits: u32) -> i32 {
        // seed = (seed * MULTIPLIER + ADDEND) & MASK, in wrapping i64 arithmetic
        // then masked back to 48 bits (matching Java's `& ((1L << 48) - 1)`).
        self.seed = self
            .seed
            .wrapping_mul(Self::MULTIPLIER)
            .wrapping_add(Self::ADDEND)
            & Self::MASK;
        // Java: `(int)(seed >>> (48 - bits))`. `seed` is non-negative (masked to
        // 48 bits) so a logical shift equals an arithmetic shift; the truncation
        // to `int` matches the `as i32` cast.
        (self.seed >> (48 - bits)) as i32
    }

    /// Java `int nextInt(int bound)` — verbatim, including the power-of-two fast
    /// path and the rejection loop that removes modulo bias.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if `bound <= 0`.
    pub fn next_int(&mut self, bound: i32) -> i32 {
        if bound <= 0 {
            panic!("bound must be positive");
        }

        // Power-of-two fast path: (bound & -bound) == bound.
        if (bound & -bound) == bound {
            return ((bound as i64 * self.next(31) as i64) >> 31) as i32;
        }

        let mut bits;
        let mut val;
        loop {
            bits = self.next(31);
            val = bits % bound;
            // Rejection to avoid modulo bias. Java's test relies on int
            // overflow wrapping negative when `bits` falls in the incomplete
            // top interval of the 31-bit range, so the arithmetic must wrap.
            if bits.wrapping_sub(val).wrapping_add(bound - 1) >= 0 {
                break;
            }
        }
        val
    }
}

/// Java `Collections.shuffle(list, new Random(seed))` — the size-`n` Fisher-Yates
/// that iterates `i` from `n-1` down to `1`, swapping index `i` with
/// `random.nextInt(i + 1)`.
pub fn java_shuffle<T>(list: &mut [T], random: &mut JavaRandom) {
    let size = list.len();
    if size < 2 {
        return;
    }
    // Java: `for (int i = size; i > 1; i--) swap(list, i - 1, rnd.nextInt(i));`
    for i in (1..size).rev() {
        let j = random.next_int((i + 1) as i32) as usize;
        list.swap(i, j);
    }
}

/// Shared mutable/async state, held behind an `Arc` so the sync trait methods
/// can hand it to spawned tasks and the async→sync bridge.
struct Inner {
    lease_refresher: Arc<dyn LeaseRefresher>,
    num_periodic_shard_sync_workers: i32,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    /// Runtime handle used to drive [`LeaseRefresher::list_leases`] (async) from
    /// the sync [`LeaderDecider::is_leader`].
    handle: tokio::runtime::Handle,
    /// Java `volatile Set<String> leaders`, guarded by the RW lock. `None`
    /// mirrors Java's `null` (not yet elected) — permissive.
    leaders: Mutex<Option<HashSet<String>>>,
    /// The spawned periodic re-election task, started on first election.
    election_task: AsyncMutex<Option<JoinHandle<()>>>,
}

impl Inner {
    /// Async election: list leases → distinct+sorted non-null owners → shuffle
    /// with the fixed seed → take `min(unique, numWorkers)`. On any error the
    /// `leaders` set is left unchanged (Java logs and returns), so the decider
    /// stays permissive. Java `electLeaders()`.
    async fn elect_leaders(&self) {
        tracing::debug!("Started leader election");
        let leases = match self.lease_refresher.list_leases().await {
            Ok(leases) => leases,
            Err(e) => {
                tracing::error!(
                    error = %e,
                    "Exception occurred while trying to fetch all leases for leader election"
                );
                return;
            }
        };

        // distinct + sorted non-null lease owners.
        let mut unique_hosts: Vec<String> = leases
            .iter()
            .filter_map(|l| l.lease_owner().map(str::to_string))
            .collect();
        unique_hosts.sort();
        unique_hosts.dedup();

        let mut random = JavaRandom::new(DETERMINISTIC_SHUFFLE_SEED);
        java_shuffle(&mut unique_hosts, &mut random);

        let num_shard_sync_workers = std::cmp::min(
            unique_hosts.len(),
            self.num_periodic_shard_sync_workers.max(0) as usize,
        );
        let elected: HashSet<String> = unique_hosts
            .into_iter()
            .take(num_shard_sync_workers)
            .collect();
        tracing::info!(leaders = ?elected, "Elected leaders");

        *self.leaders.lock().expect("leaders lock poisoned") = Some(elected);
    }

    /// Java `isWorkerLeaderForShardSync` — `null`/empty leaders ⇒ permissive.
    fn is_worker_leader_for_shard_sync(&self, worker_id: &str) -> bool {
        let guard = self.leaders.lock().expect("leaders lock poisoned");
        match guard.as_ref() {
            None => true,
            Some(set) if set.is_empty() => true,
            Some(set) => set.contains(worker_id),
        }
    }

    fn leaders_is_null_or_empty(&self) -> bool {
        let guard = self.leaders.lock().expect("leaders lock poisoned");
        guard.as_ref().map(HashSet::is_empty).unwrap_or(true)
    }
}

/// Elects periodic-shard-sync leaders via a deterministic shuffle of lease
/// owners. Java `DeterministicShuffleShardSyncLeaderDecider`.
pub struct DeterministicShuffleShardSyncLeaderDecider {
    inner: Arc<Inner>,
}

impl DeterministicShuffleShardSyncLeaderDecider {
    /// Java constructor
    /// `DeterministicShuffleShardSyncLeaderDecider(leaseRefresher,
    /// leaderElectionThreadPool, numPeriodicShardSyncWorkers, metricsFactory)`.
    /// The Java `ScheduledExecutorService` is replaced by a spawned tokio task,
    /// so the current runtime handle is captured here.
    pub fn new(
        lease_refresher: Arc<dyn LeaseRefresher>,
        num_periodic_shard_sync_workers: i32,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Self {
        Self::with_handle(
            lease_refresher,
            num_periodic_shard_sync_workers,
            metrics_factory,
            tokio::runtime::Handle::current(),
        )
    }

    /// Test/non-current-runtime constructor taking an explicit runtime handle
    /// (the async→sync bridge needs a handle to `block_on`).
    pub fn with_handle(
        lease_refresher: Arc<dyn LeaseRefresher>,
        num_periodic_shard_sync_workers: i32,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        handle: tokio::runtime::Handle,
    ) -> Self {
        Self {
            inner: Arc::new(Inner {
                lease_refresher,
                num_periodic_shard_sync_workers,
                metrics_factory,
                handle,
                leaders: Mutex::new(None),
                election_task: AsyncMutex::new(None),
            }),
        }
    }

    /// Start the periodic re-election task (Java `scheduleWithFixedDelay` with a
    /// 60s initial delay and 5min period). Idempotent: a second call is a no-op.
    fn spawn_election_task(inner: &Arc<Inner>) {
        let inner = Arc::clone(inner);
        let handle = inner.handle.clone();
        crate::utils::sync_bridge::run_sync_on(handle.clone(), async move {
            let mut guard = inner.election_task.lock().await;
            if guard.is_some() {
                return;
            }
            let task_inner = Arc::clone(&inner);
            // Spawn onto the captured runtime explicitly so the periodic task
            // outlives this bridge regardless of which thread drives it.
            let join = handle.spawn(async move {
                // 60s initial delay, then every 5min (fixed delay).
                let start = tokio::time::Instant::now()
                    + std::time::Duration::from_millis(ELECTION_INITIAL_DELAY_MILLIS);
                let mut ticker = tokio::time::interval_at(
                    start,
                    std::time::Duration::from_millis(ELECTION_SCHEDULING_INTERVAL_MILLIS),
                );
                ticker.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
                loop {
                    ticker.tick().await;
                    // Java DeterministicShuffleShardSyncLeaderDecider
                    // catch(Throwable): a panicking election must not kill the
                    // re-election loop.
                    if let Err(panic_msg) = panic_util::catch_tick(task_inner.elect_leaders()).await
                    {
                        tracing::error!(
                            error = %panic_msg,
                            "Unknown exception during leader election."
                        );
                    }
                }
            });
            *guard = Some(join);
        });
    }
}

impl LeaderDecider for DeterministicShuffleShardSyncLeaderDecider {
    fn is_leader(&self, worker_id: &str) -> bool {
        // First call with no leaders yet: synchronously elect (blocking) + start
        // the periodic re-election task. This matches Java's first-shard-sync
        // election path.
        if self.inner.leaders_is_null_or_empty() {
            let inner = Arc::clone(&self.inner);
            let handle = inner.handle.clone();
            // Bridge async election to this sync method (flavor-aware: yields a
            // multi-thread worker; no panic on a current-thread runtime).
            crate::utils::sync_bridge::run_sync_on(handle, async move {
                inner.elect_leaders().await;
            });
            Self::spawn_election_task(&self.inner);
        }

        let response = self.inner.is_worker_leader_for_shard_sync(worker_id);

        let mut scope = metrics_util::create_metrics_with_operation(
            self.inner.metrics_factory.as_ref(),
            METRIC_OPERATION_LEADER_DECIDER,
        );
        scope.add_data_with_level(
            METRIC_OPERATION_LEADER_DECIDER_IS_LEADER,
            if response { 1.0 } else { 0.0 },
            StandardUnit::Count,
            MetricsLevel::Detailed,
        );
        metrics_util::end_scope(scope.as_mut());

        response
    }

    fn shutdown(&self) {
        // Abort the periodic re-election task (Java `threadPool.shutdown()`).
        let inner = Arc::clone(&self.inner);
        let handle = inner.handle.clone();
        crate::utils::sync_bridge::run_sync_on(handle, async move {
            if let Some(task) = inner.election_task.lock().await.take() {
                task.abort();
                tracing::info!("Successfully stopped leader election on the worker");
            }
        });
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::lease::Lease;
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::kpl::ExtendedSequenceNumber;

    // ---- JavaRandom / java_shuffle: pinned against real Java output ----

    #[test]
    fn java_random_next_int_sequence_matches_java() {
        // Real Java (`new Random(1947)`) nextInt sequence for bounds 10..=2:
        // 3,7,0,2,4,3,2,1,1
        let mut r = JavaRandom::new(1947);
        let expected = [3, 7, 0, 2, 4, 3, 2, 1, 1];
        for (i, bound) in (2..=10).rev().enumerate() {
            assert_eq!(r.next_int(bound), expected[i], "nextInt({bound})");
        }
    }

    #[test]
    fn java_random_next_int_rejection_overflow_wraps_like_java() {
        // Java's rejection guard `bits - val + (bound - 1) >= 0` RELIES on int
        // overflow wrapping negative to reject a draw from the incomplete top
        // interval of the 31-bit range. With bound = 2^31 - 1 the only rejected
        // draw is bits == 2^31 - 1 (val == 0, sum == 2^32 - 3 > i32::MAX).
        // Internal LCG state chosen (by inverting the LCG step) so the very
        // first next(31) yields exactly 2^31 - 1: pre-fix, debug builds panic
        // with 'attempt to add with overflow' here instead of retrying.
        let mut r = JavaRandom {
            seed: 0xA9C5_E77C_2AA9,
        };
        let bound = i32::MAX;
        let val = r.next_int(bound);
        // Java rejects the first draw and returns the second: 554899859.
        assert_eq!(val, 554_899_859);
        assert!((0..bound).contains(&val));
    }

    #[test]
    fn java_shuffle_ints_matches_java() {
        // Real Java `Collections.shuffle([0..9], new Random(1947))`:
        // [8, 5, 1, 6, 9, 4, 2, 0, 7, 3]
        let mut v: Vec<i32> = (0..10).collect();
        let mut r = JavaRandom::new(DETERMINISTIC_SHUFFLE_SEED);
        java_shuffle(&mut v, &mut r);
        assert_eq!(v, vec![8, 5, 1, 6, 9, 4, 2, 0, 7, 3]);
    }

    #[test]
    fn java_shuffle_strings_matches_java() {
        // Real Java shuffle of [lease_owner0..4] with seed 1947:
        // [lease_owner4, lease_owner0, lease_owner2, lease_owner1, lease_owner3]
        let mut v: Vec<String> = (0..5).map(|i| format!("lease_owner{i}")).collect();
        let mut r = JavaRandom::new(DETERMINISTIC_SHUFFLE_SEED);
        java_shuffle(&mut v, &mut r);
        assert_eq!(
            v,
            vec![
                "lease_owner4",
                "lease_owner0",
                "lease_owner2",
                "lease_owner1",
                "lease_owner3"
            ]
        );

        // And the 3-element case: [lease_owner2, lease_owner0, lease_owner1].
        let mut v3: Vec<String> = (0..3).map(|i| format!("lease_owner{i}")).collect();
        let mut r3 = JavaRandom::new(DETERMINISTIC_SHUFFLE_SEED);
        java_shuffle(&mut v3, &mut r3);
        assert_eq!(v3, vec!["lease_owner2", "lease_owner0", "lease_owner1"]);
    }

    #[test]
    fn java_shuffle_is_deterministic_across_runs() {
        let build = || {
            let mut v: Vec<String> = (0..7).map(|i| format!("host-{i}")).collect();
            let mut r = JavaRandom::new(DETERMINISTIC_SHUFFLE_SEED);
            java_shuffle(&mut v, &mut r);
            v
        };
        assert_eq!(build(), build());
    }

    #[test]
    fn seed_is_1947() {
        assert_eq!(DETERMINISTIC_SHUFFLE_SEED, 1947);
    }

    // ---- Leader election tests (port of the Java test cases) ----

    const LEASE_KEY: &str = "lease_key";
    const LEASE_OWNER: &str = "lease_owner";
    const WORKER_ID: &str = "worker-id";

    /// Mirrors the Java test's `getLeases(count, emptyLeaseOwner,
    /// duplicateLeaseOwner, activeLeases)`.
    fn get_leases(
        count: usize,
        empty_lease_owner: bool,
        duplicate_lease_owner: bool,
        active_leases: bool,
    ) -> Vec<Lease> {
        (0..count)
            .map(|i| {
                let mut lease = Lease::default();
                lease.set_lease_key(format!("{LEASE_KEY}{i}"));
                lease.set_checkpoint(if active_leases {
                    ExtendedSequenceNumber::latest()
                } else {
                    ExtendedSequenceNumber::shard_end()
                });
                if !empty_lease_owner {
                    let owner = if duplicate_lease_owner {
                        LEASE_OWNER.to_string()
                    } else {
                        format!("{LEASE_OWNER}{i}")
                    };
                    lease.set_lease_owner(Some(owner));
                }
                lease
            })
            .collect()
    }

    /// Mirrors the Java test's `getExpectedLeaders(leases)` — the same
    /// distinct+sorted+shuffle+take(min) pipeline.
    fn get_expected_leaders(leases: &[Lease], num_shard_sync_workers: i32) -> HashSet<String> {
        let mut unique_hosts: Vec<String> = leases
            .iter()
            .filter_map(|l| l.lease_owner().map(str::to_string))
            .collect();
        unique_hosts.sort();
        unique_hosts.dedup();
        let mut r = JavaRandom::new(DETERMINISTIC_SHUFFLE_SEED);
        java_shuffle(&mut unique_hosts, &mut r);
        let n = std::cmp::min(unique_hosts.len(), num_shard_sync_workers.max(0) as usize);
        unique_hosts.into_iter().take(n).collect()
    }

    fn refresher_returning(leases: Vec<Lease>) -> MockLeaseRefresher {
        let mut m = MockLeaseRefresher::new();
        m.expect_list_leases().returning(move || Ok(leases.clone()));
        m
    }

    fn decider(
        refresher: MockLeaseRefresher,
        num_workers: i32,
    ) -> DeterministicShuffleShardSyncLeaderDecider {
        DeterministicShuffleShardSyncLeaderDecider::with_handle(
            Arc::new(refresher),
            num_workers,
            Arc::new(NullMetricsFactory),
            tokio::runtime::Handle::current(),
        )
    }

    // Leader-election tests spawn a periodic task, so they need a multi-thread
    // runtime for `block_in_place`.

    #[tokio::test(flavor = "multi_thread")]
    async fn leader_election_with_empty_leases_is_permissive() {
        // Java `testLeaderElectionWithEmptyLeases`: no leases → leaders empty →
        // everyone is a leader.
        let d = decider(refresher_returning(Vec::new()), 1);
        assert!(d.is_leader(WORKER_ID));
        d.shutdown();
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn leader_election_with_empty_owner_leases_is_permissive() {
        // Java `testleaderElectionWithEmptyOwnerLeases`: leases with no owner →
        // no unique hosts → leaders empty → permissive.
        let leases = get_leases(5, true, true, true);
        let d = decider(refresher_returning(leases), 1);
        assert!(d.is_leader(WORKER_ID));
        d.shutdown();
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn elected_leaders_as_per_expected_shuffling_order() {
        // Java `testElectedLeadersAsPerExpectedShufflingOrder`.
        let leases = get_leases(5, false, false, true);
        let expected = get_expected_leaders(&leases, 1);
        // With seed 1947 the sole elected leader is `lease_owner4`.
        assert_eq!(
            expected,
            HashSet::from(["lease_owner4".to_string()]),
            "pinned leader set"
        );

        let d = decider(refresher_returning(leases.clone()), 1);
        for leader in &expected {
            assert!(d.is_leader(leader), "{leader} should be a leader");
        }
        for lease in &leases {
            let owner = lease.lease_owner().unwrap();
            if !expected.contains(owner) {
                assert!(!d.is_leader(owner), "{owner} should NOT be a leader");
            }
        }
        d.shutdown();
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn elected_leaders_when_unique_workers_less_than_max_leaders() {
        // Java
        // `testElectedLeadersAsPerExpectedShufflingOrderWhenUniqueWorkersLessThanMaxLeaders`.
        // 5 workers requested but only 3 unique owners → all 3 are leaders.
        let leases = get_leases(3, false, false, true);
        let expected = get_expected_leaders(&leases, 5);
        assert_eq!(expected.len(), 3);

        let d = decider(refresher_returning(leases.clone()), 5);
        for lease in &leases {
            let owner = lease.lease_owner().unwrap();
            assert!(d.is_leader(owner));
            assert!(expected.contains(owner));
        }
        d.shutdown();
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn leader_election_with_null_leases_is_permissive() {
        // Java `testLeaderElectionWithNullLeases`: before any election has run,
        // the `leaders` set is `null`, and `isWorkerLeaderForShardSync` treats
        // `null` as permissive. In the Rust design `is_leader` eagerly elects on
        // the first call, so we assert the true never-elected state directly on
        // the decider's `Inner` (leaders == None): permissive for any worker.
        let d = decider(refresher_returning(Vec::new()), 1);
        assert!(
            d.inner.leaders.lock().unwrap().is_none(),
            "leaders must start as null (never elected)"
        );
        assert!(
            d.inner.is_worker_leader_for_shard_sync(WORKER_ID),
            "null leaders should be permissive"
        );
        d.shutdown();
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn leader_election_does_not_mutate_leaders_on_list_leases_error() {
        // Java `testLeaderElectionDoesNotUseLocksOnListLeasesException`: when
        // `listLeases` throws, election returns early WITHOUT taking the write
        // lock (i.e. leaving `leaders` untouched), and `listLeases` is called
        // exactly once. Mockito's lock-verification doesn't apply to the
        // Mutex-based Rust design; we instead assert the observable behavior:
        // `elect_leaders` leaves `leaders == None` (unchanged) and calls
        // `list_leases` exactly once.
        use crate::leases::exceptions::LeasingError;
        let mut m = MockLeaseRefresher::new();
        m.expect_list_leases()
            .times(1)
            .returning(|| Err(LeasingError::dependency("error")));
        let d = decider(m, 1);
        // Drive one election directly (mirrors the first-call election path).
        d.inner.elect_leaders().await;
        assert!(
            d.inner.leaders.lock().unwrap().is_none(),
            "leaders must remain unchanged (null) after a listLeases error"
        );
        // Still permissive after the failed election.
        assert!(d.inner.is_worker_leader_for_shard_sync(WORKER_ID));
        d.shutdown();
    }

    #[tokio::test(flavor = "multi_thread")]
    async fn is_leader_is_stable_across_calls() {
        // Determinism: repeated `is_leader` calls (which do NOT re-elect once
        // leaders are set) return the same answer.
        let leases = get_leases(5, false, false, true);
        let d = decider(refresher_returning(leases), 1);
        let first = d.is_leader("lease_owner4");
        assert!(first);
        for _ in 0..5 {
            assert_eq!(d.is_leader("lease_owner4"), first);
            assert!(!d.is_leader("lease_owner0"));
        }
        d.shutdown();
    }
}
