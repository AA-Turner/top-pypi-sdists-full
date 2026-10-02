//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBLeaseTaker`.
//!
//! Implements [`LeaseTaker`] using DynamoDB via a [`LeaseRefresher`]: the core
//! lease-count-based load-balancing algorithm (KCLv2.x-style
//! `DEFAULT_LEASE_COUNT_BASED_ASSIGNMENT`). Periodically scans all leases,
//! computes a fair per-worker target lease count, and takes/steals leases via
//! [`LeaseRefresher::take_lease`] to converge toward that target.
//!
//! # Concurrency
//!
//! Java `synchronized`-es the whole `takeLeases(Callable<Long>)` pass and the
//! `allLeases()` accessor, since the internal `allLeases` `HashMap` is a plain
//! (non-concurrent) map mutated only under that lock. The Rust port wraps the
//! mutable state (`all_leases` + `last_scan_time_nanos`) in a
//! `tokio::sync::Mutex<TakerState>`; `take_leases` holds the lock for the whole
//! scan/compute/take pass (the safety net Java provides). The sync
//! `all_leases()` accessor reads a `std::sync::Mutex` snapshot refreshed once
//! per take pass — observationally equivalent to Java (whose `synchronized`
//! `allLeases()` also only ever sees pre-/post-pass state) and, unlike a
//! `blocking_lock`, callable from any context (async worker, blocking pool, or
//! plain thread) without panicking.
//!
//! # Selection math (preserved exactly)
//!
//! - `compute_lease_counts`: per-worker owned-lease counts, counting only
//!   NON-available leases; always includes this worker with count ≥ 0.
//! - `target` = 1 if `num_workers >= num_leases`, else `ceil(num_leases /
//!   num_workers)`, clamped down to `max_leases_for_worker` (emitting the
//!   `LeaseSpillover` metric on clamp).
//! - Priority / very-old-lease short-circuit (`enable_priority_lease_assignment`):
//!   leases older than `very_old_lease_duration_nanos_multiplier * lease_duration`
//!   are shuffled and taken up to `max_leases_for_worker - current`, returning
//!   early and bypassing the fairness target.
//! - Otherwise greedily take up to `num_leases_to_reach_target` from the shuffled
//!   available pool, or steal from the single most-loaded worker.
//! - Random shuffles use `rand::rng()` (Java `Collections.shuffle`) — no
//!   attempt at bit-for-bit reproduction.

use std::collections::{HashMap, HashSet};

use async_trait::async_trait;
use rand::seq::SliceRandom;

use crate::common::get_renewer_taker_interval_millis;
use crate::coordinator::StreamIdCacheManager;
use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, LeaseRefresher, LeaseTaker};
use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};

use std::sync::Arc;

use aws_sdk_cloudwatch::types::StandardUnit;

const TAKE_RETRIES: i32 = 3;
const SCAN_RETRIES: i32 = 1;
const RENEWAL_SLACK_PERCENTAGE: f64 = 0.5;
const TAKE_LEASES_DIMENSION: &str = "TakeLeases";

/// A time provider returning nanoseconds (Java `Callable<Long>`), injectable so
/// tests can provide a fixed "now" without `Thread.sleep`.
pub type NanoTimeProvider = Arc<dyn Fn() -> i64 + Send + Sync>;

/// DynamoDB implementation of [`LeaseTaker`].
pub struct DynamoDBLeaseTaker {
    lease_refresher: Arc<dyn LeaseRefresher>,
    worker_identifier: String,
    lease_duration_nanos: i64,
    lease_renewal_interval_millis: i64,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    #[allow(dead_code)]
    stream_id_cache_manager: Option<StreamIdCacheManager>,

    max_leases_for_worker: i32,
    max_leases_to_steal_at_one_time: i32,
    enable_priority_lease_assignment: bool,
    very_old_lease_duration_nanos_multiplier: i32,

    // Java `System::nanoTime` clock; injectable for the whole take pass in tests.
    time_provider: NanoTimeProvider,

    state: tokio::sync::Mutex<TakerState>,
    /// Sync snapshot of `TakerState::all_leases`, refreshed after each take
    /// pass, so `all_leases()` never blocks on the async state lock.
    all_leases_snapshot: std::sync::Mutex<Vec<Lease>>,
}

#[derive(Default)]
struct TakerState {
    /// Key is leaseKey (Java `final Map<String, Lease> allLeases`).
    all_leases: HashMap<String, Lease>,
    last_scan_time_nanos: i64,
}

impl DynamoDBLeaseTaker {
    /// Construct a taker (Java 4-arg constructor, no `StreamIdCacheManager`).
    pub fn new(
        lease_refresher: Arc<dyn LeaseRefresher>,
        worker_identifier: impl Into<String>,
        lease_duration_millis: i64,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Self {
        Self::new_with_cache_manager(
            lease_refresher,
            worker_identifier,
            lease_duration_millis,
            metrics_factory,
            None,
        )
    }

    /// Construct a taker with an optional `StreamIdCacheManager` (Java 5-arg
    /// constructor).
    pub fn new_with_cache_manager(
        lease_refresher: Arc<dyn LeaseRefresher>,
        worker_identifier: impl Into<String>,
        lease_duration_millis: i64,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        stream_id_cache_manager: Option<StreamIdCacheManager>,
    ) -> Self {
        Self {
            lease_refresher,
            worker_identifier: worker_identifier.into(),
            lease_duration_nanos: lease_duration_millis * 1_000_000,
            lease_renewal_interval_millis: get_renewer_taker_interval_millis(
                lease_duration_millis,
                0,
            ),
            metrics_factory,
            stream_id_cache_manager,
            max_leases_for_worker: i32::MAX,
            max_leases_to_steal_at_one_time: 1,
            enable_priority_lease_assignment: true,
            very_old_lease_duration_nanos_multiplier: 3,
            time_provider: default_nano_time_provider(),
            state: tokio::sync::Mutex::new(TakerState::default()),
            all_leases_snapshot: std::sync::Mutex::new(Vec::new()),
        }
    }

    /// Java `withMaxLeasesForWorker`.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if `< 1`.
    pub fn with_max_leases_for_worker(mut self, max_leases_for_worker: i32) -> Self {
        if max_leases_for_worker <= 0 {
            panic!("maxLeasesForWorker should be >= 1");
        }
        self.max_leases_for_worker = max_leases_for_worker;
        self
    }

    /// Java `withVeryOldLeaseDurationNanosMultiplier`.
    pub fn with_very_old_lease_duration_nanos_multiplier(mut self, multiplier: i32) -> Self {
        self.very_old_lease_duration_nanos_multiplier = multiplier;
        self
    }

    /// Java `withEnablePriorityLeaseAssignment`.
    pub fn with_enable_priority_lease_assignment(mut self, enable: bool) -> Self {
        self.enable_priority_lease_assignment = enable;
        self
    }

    /// Java `withMaxLeasesToStealAtOneTime`.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if `< 1`.
    pub fn with_max_leases_to_steal_at_one_time(mut self, max_leases: i32) -> Self {
        if max_leases <= 0 {
            panic!("maxLeasesToStealAtOneTime should be >= 1");
        }
        self.max_leases_to_steal_at_one_time = max_leases;
        self
    }

    /// Override the time provider (test seam; Java `takeLeases(Callable<Long>)`).
    pub fn with_time_provider(mut self, time_provider: NanoTimeProvider) -> Self {
        self.time_provider = time_provider;
        self
    }

    /// The internal take-leases pass. Ports Java `takeLeases(Callable<Long>)`
    /// (whole-method `synchronized`; here the state Mutex is held for the pass).
    async fn take_leases_impl(&self) -> Result<HashMap<String, Lease>, LeasingError> {
        let mut state = self.state.lock().await;

        let mut taken_leases: HashMap<String, Lease> = HashMap::new();

        let mut scope = metrics_util::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            TAKE_LEASES_DIMENSION,
        );
        metrics_util::add_worker_identifier(scope.as_mut(), &self.worker_identifier);

        let start_time = now_millis();
        let mut success = false;
        let mut last_exception: Option<LeasingError> = None;

        // SCAN_RETRIES loop (runs exactly once).
        for _ in 1..=SCAN_RETRIES {
            match self.update_all_leases(&mut state).await {
                Ok(()) => success = true,
                Err(e) if is_provisioned_throughput(&e) => {
                    last_exception = Some(e);
                }
                Err(e) => {
                    metrics_util::add_success_and_latency_with_dimension(
                        scope.as_mut(),
                        Some("ListLeases"),
                        success,
                        start_time,
                        MetricsLevel::Detailed,
                    );
                    metrics_util::end_scope(scope.as_mut());
                    return Err(e);
                }
            }
        }
        let update_all_leases_total_time_millis = now_millis() - start_time;
        metrics_util::add_success_and_latency_with_dimension(
            scope.as_mut(),
            Some("ListLeases"),
            success,
            start_time,
            MetricsLevel::Detailed,
        );

        if last_exception.is_some() {
            // Could not scan leases table; abort.
            metrics_util::end_scope(scope.as_mut());
            return Ok(taken_leases);
        }

        let available_leases = self.get_available_leases(&state);
        let leases_to_take = self
            .compute_leases_to_take(&state, available_leases)
            .await?;
        let leases_to_take = self
            .update_stale_leases_with_latest_state(
                update_all_leases_total_time_millis,
                leases_to_take,
            )
            .await;

        let mut untaken_lease_keys: HashSet<String> = HashSet::new();

        for mut lease in leases_to_take {
            let lease_key = lease.lease_key().unwrap_or("").to_string();

            let take_start = now_millis();
            let mut take_success = false;

            for _ in 1..=TAKE_RETRIES {
                match self
                    .lease_refresher
                    .take_lease(&mut lease, &self.worker_identifier)
                    .await
                {
                    Ok(true) => {
                        lease.set_last_counter_increment_nanos(Some(self.now_nanos()));
                        taken_leases.insert(lease_key.clone(), lease.clone());
                        self.resolve_stream_id(&lease);
                        take_success = true;
                        break;
                    }
                    Ok(false) => {
                        untaken_lease_keys.insert(lease_key.clone());
                        take_success = true;
                        break;
                    }
                    Err(e) if is_provisioned_throughput(&e) => {
                        // retry (capacity)
                    }
                    Err(e) => {
                        metrics_util::add_success_and_latency_with_dimension(
                            scope.as_mut(),
                            Some("TakeLease"),
                            take_success,
                            take_start,
                            MetricsLevel::Detailed,
                        );
                        metrics_util::end_scope(scope.as_mut());
                        return Err(e);
                    }
                }
            }

            metrics_util::add_success_and_latency_with_dimension(
                scope.as_mut(),
                Some("TakeLease"),
                take_success,
                take_start,
                MetricsLevel::Detailed,
            );
        }

        scope.add_data_with_level(
            "TakenLeases",
            taken_leases.len() as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "UntakenLeases",
            untaken_lease_keys.len() as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        metrics_util::end_scope(scope.as_mut());

        Ok(taken_leases)
    }

    /// Java `updateStaleLeasesWithLatestState`: if the scan took longer than the
    /// renewal slack, re-fetch the current DDB state for leases marked for steal.
    async fn update_stale_leases_with_latest_state(
        &self,
        update_all_leases_end_time: i64,
        leases_to_take: HashSet<Lease>,
    ) -> HashSet<Lease> {
        if update_all_leases_end_time as f64
            > self.lease_renewal_interval_millis as f64 * RENEWAL_SLACK_PERCENTAGE
        {
            let mut result: HashSet<Lease> = HashSet::new();
            for lease in leases_to_take {
                if lease.is_marked_for_lease_steal() {
                    let key = lease.lease_key().unwrap_or("").to_string();
                    match self.lease_refresher.get_lease(&key).await {
                        Ok(Some(fresh)) => {
                            result.insert(fresh);
                            continue;
                        }
                        Ok(None) => {
                            // Java returns null -> the stream .map yields null; a
                            // null in the resulting Set is possible in Java. We
                            // fall back to the existing lease (safer, equivalent
                            // for the steal-marker purpose).
                            result.insert(lease);
                            continue;
                        }
                        Err(_e) => {
                            // Failed to fetch latest state; default to existing.
                            result.insert(lease);
                            continue;
                        }
                    }
                }
                result.insert(lease);
            }
            result
        } else {
            leases_to_take
        }
    }

    /// Java `updateAllLeases`: fresh scan, diff counters to derive
    /// `lastCounterIncrementNanos`, add new / remove dead leases.
    async fn update_all_leases(&self, state: &mut TakerState) -> Result<(), LeasingError> {
        let fresh_list = self.lease_refresher.list_leases().await?;
        state.last_scan_time_nanos = self.now_nanos();
        let last_scan_time_nanos = state.last_scan_time_nanos;

        // Lease keys not (re)seen by this scan.
        let mut not_updated: HashSet<String> = state.all_leases.keys().cloned().collect();

        for mut lease in fresh_list {
            let lease_key = lease.lease_key().unwrap_or("").to_string();
            not_updated.remove(&lease_key);

            let old_lease = state.all_leases.get(&lease_key).cloned();

            match old_lease {
                Some(old) => {
                    if old.lease_counter() == lease.lease_counter() {
                        // Counter unchanged: keep the old renewal clock.
                        lease.set_last_counter_increment_nanos(old.last_counter_increment_nanos());
                    } else {
                        // Counter changed: stamp with the scan time.
                        lease.set_last_counter_increment_nanos(Some(last_scan_time_nanos));
                    }
                }
                None => {
                    if lease.lease_owner().is_none() {
                        // New + unowned: never renewed (instantly available).
                        lease.set_last_counter_increment_nanos(Some(0));
                    } else {
                        // New + owned: treat as freshly renewed.
                        lease.set_last_counter_increment_nanos(Some(last_scan_time_nanos));
                    }
                }
            }

            state.all_leases.insert(lease_key, lease);
        }

        for key in not_updated {
            state.all_leases.remove(&key);
        }

        Ok(())
    }

    fn resolve_stream_id(&self, _lease: &Lease) {
        // TODO(port) — coordinator wave (10): the StreamIdCacheManager singleton
        // is a `port_stubs` placeholder with no behavior yet. Java best-effort
        // resolves the multi-stream stream id post-take (exceptions swallowed);
        // here it is a no-op until the coordinator wave injects the real cache.
    }

    /// Java `getAvailableLeases`: filter `allLeases` by `is_available`.
    fn get_available_leases(&self, state: &TakerState) -> Vec<Lease> {
        state
            .all_leases
            .values()
            .filter(|lease| {
                lease.is_available(self.lease_duration_nanos, state.last_scan_time_nanos)
            })
            .cloned()
            .collect()
    }

    /// Java `computeLeasesToTake`: the selection math (see module docs).
    async fn compute_leases_to_take(
        &self,
        state: &TakerState,
        mut available_leases: Vec<Lease>,
    ) -> Result<HashSet<Lease>, LeasingError> {
        let lease_counts = self.compute_lease_counts(state, &available_leases);
        let mut leases_to_take: HashSet<Lease> = HashSet::new();

        let mut scope = metrics_util::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            TAKE_LEASES_DIMENSION,
        );
        metrics_util::add_worker_identifier(scope.as_mut(), &self.worker_identifier);

        let num_available_leases = available_leases.len();
        let num_leases = state.all_leases.len();
        let num_workers = lease_counts.len();
        let mut num_leases_to_reach_target = 0i32;
        let mut lease_spillover = 0i32;
        let mut very_old_lease_count = 0i32;

        // `finally`-equivalent metric emission via a closure at the end.
        let result: Result<HashSet<Lease>, LeasingError> = (|| {
            if num_leases == 0 {
                // No leases -> take none.
                return Ok(leases_to_take.clone());
            }

            let target: i32;
            if num_workers >= num_leases {
                target = 1;
            } else {
                let n_leases = num_leases as i32;
                let n_workers = num_workers as i32;
                let mut t = n_leases / n_workers + if n_leases % n_workers == 0 { 0 } else { 1 };
                lease_spillover = 0.max(t - self.max_leases_for_worker);
                if t > self.max_leases_for_worker {
                    t = self.max_leases_for_worker;
                }
                target = t;
            }

            let my_count = *lease_counts.get(&self.worker_identifier).unwrap_or(&0);
            num_leases_to_reach_target = target - my_count;
            let current_lease_count = my_count;

            // Priority / very-old-lease short-circuit.
            if self.enable_priority_lease_assignment {
                let current_nano_time = self.now_nanos();
                let nano_threshold = current_nano_time
                    - (self.very_old_lease_duration_nanos_multiplier as i64
                        * self.lease_duration_nanos);
                let mut very_old_leases: Vec<Lease> = state
                    .all_leases
                    .values()
                    .filter(|lease| {
                        nano_threshold > lease.last_counter_increment_nanos().unwrap_or(0)
                    })
                    .cloned()
                    .collect();

                if !very_old_leases.is_empty() {
                    very_old_leases.shuffle(&mut rand::rng());
                    very_old_lease_count = 0.max(
                        (self.max_leases_for_worker - current_lease_count)
                            .min(very_old_leases.len() as i32),
                    );
                    let take_n = very_old_lease_count.max(0) as usize;
                    let result: HashSet<Lease> = very_old_leases.into_iter().take(take_n).collect();
                    return Ok(result);
                }
            }

            if num_leases_to_reach_target <= 0 {
                return Ok(leases_to_take.clone());
            }

            // Shuffle so workers don't all contend for the same leases.
            available_leases.shuffle(&mut rand::rng());

            if !available_leases.is_empty() {
                while num_leases_to_reach_target > 0 && !available_leases.is_empty() {
                    leases_to_take.insert(available_leases.remove(0));
                    num_leases_to_reach_target -= 1;
                }
            } else {
                // No available leases and we need some -> consider stealing.
                let leases_to_steal = self.choose_leases_to_steal(
                    state,
                    &lease_counts,
                    num_leases_to_reach_target,
                    target,
                );
                for lease_to_steal in leases_to_steal {
                    leases_to_take.insert(lease_to_steal);
                }
            }

            Ok(leases_to_take.clone())
        })();

        // finally: emit the summary metrics + end scope.
        scope.add_data_with_level(
            "ExpiredLeases",
            num_available_leases as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "LeaseSpillover",
            lease_spillover as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        let leases_to_take_len = result.as_ref().map(|s| s.len()).unwrap_or(0);
        scope.add_data_with_level(
            "LeasesToTake",
            leases_to_take_len as f64,
            StandardUnit::Count,
            MetricsLevel::Detailed,
        );
        scope.add_data_with_level(
            "NeededLeases",
            num_leases_to_reach_target.max(0) as f64,
            StandardUnit::Count,
            MetricsLevel::Detailed,
        );
        scope.add_data_with_level(
            "NumWorkers",
            num_workers as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "TotalLeases",
            num_leases as f64,
            StandardUnit::Count,
            MetricsLevel::Detailed,
        );
        scope.add_data_with_level(
            "VeryOldLeases",
            very_old_lease_count as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        metrics_util::end_scope(scope.as_mut());

        result
    }

    /// Java `chooseLeasesToSteal`: pick from the single most-loaded worker.
    fn choose_leases_to_steal(
        &self,
        state: &TakerState,
        lease_counts: &HashMap<String, i32>,
        needed: i32,
        target: i32,
    ) -> Vec<Lease> {
        let mut leases_to_steal: Vec<Lease> = Vec::new();

        // Find the most loaded worker (first-max-wins on ties, over the map's
        // iteration order — unspecified in both Java and Rust).
        let mut most_loaded: Option<(&String, &i32)> = None;
        for (worker, count) in lease_counts.iter() {
            match most_loaded {
                None => most_loaded = Some((worker, count)),
                Some((_, mc)) if mc < count => most_loaded = Some((worker, count)),
                _ => {}
            }
        }

        let most_loaded = match most_loaded {
            Some(m) => m,
            None => return leases_to_steal,
        };
        let most_loaded_count = *most_loaded.1;

        let mut num_leases_to_steal = 0i32;
        if most_loaded_count >= target && needed > 0 {
            let leases_over_target = most_loaded_count - target;
            num_leases_to_steal = needed.min(leases_over_target);
            // Steal 1 if we need > 1 and the most-loaded worker is exactly at target.
            if needed > 1 && num_leases_to_steal == 0 {
                num_leases_to_steal = 1;
            }
            num_leases_to_steal = num_leases_to_steal.min(self.max_leases_to_steal_at_one_time);
        }

        if num_leases_to_steal <= 0 {
            return leases_to_steal;
        }

        let most_loaded_worker_identifier = most_loaded.0.clone();
        let mut candidates: Vec<Lease> = state
            .all_leases
            .values()
            .filter(|lease| lease.lease_owner() == Some(most_loaded_worker_identifier.as_str()))
            .cloned()
            .collect();

        candidates.shuffle(&mut rand::rng());
        let to_index = candidates.len().min(num_leases_to_steal as usize);
        for mut lease in candidates.into_iter().take(to_index) {
            lease.set_marked_for_lease_steal(true);
            leases_to_steal.push(lease);
        }
        leases_to_steal
    }

    /// Java `computeLeaseCounts`: count leases per host, ignoring available
    /// leases; always includes this worker.
    fn compute_lease_counts(
        &self,
        state: &TakerState,
        available_leases: &[Lease],
    ) -> HashMap<String, i32> {
        let mut lease_counts: HashMap<String, i32> = HashMap::new();
        let available_leases_set: HashSet<&Lease> = available_leases.iter().collect();

        for lease in state.all_leases.values() {
            if !available_leases_set.contains(lease) {
                // Java uses `null` as a map key for an unowned-but-not-available
                // lease's owner; we key on the owner string (using "" for None to
                // preserve the "counted but no owner" bucket — though a
                // non-available lease normally has an owner).
                let owner = lease.lease_owner().unwrap_or("").to_string();
                *lease_counts.entry(owner).or_insert(0) += 1;
            }
        }

        lease_counts
            .entry(self.worker_identifier.clone())
            .or_insert(0);

        lease_counts
    }

    fn now_nanos(&self) -> i64 {
        (self.time_provider)()
    }
}

#[async_trait]
impl LeaseTaker for DynamoDBLeaseTaker {
    async fn take_leases(&self) -> Result<HashMap<String, Lease>, LeasingError> {
        let result = self.take_leases_impl().await;
        // Refresh the sync snapshot once per pass (also on error — Java's
        // updateAllLeases may have mutated the map before a later step threw,
        // and its allLeases() would observe that).
        let state = self.state.lock().await;
        *self.all_leases_snapshot.lock().unwrap() = state.all_leases.values().cloned().collect();
        result
    }

    fn get_worker_identifier(&self) -> String {
        self.worker_identifier.clone()
    }

    fn all_leases(&self) -> Vec<Lease> {
        // Java `synchronized List<Lease> allLeases()`: callers block during a
        // take pass and only observe pre-/post-pass state. Reading the per-pass
        // snapshot is observationally equivalent and callable from any context
        // (a `blocking_lock` here panicked inside a tokio runtime).
        self.all_leases_snapshot.lock().unwrap().clone()
    }
}

/// Java `System::nanoTime` — the process-wide monotonic clock. Must share its
/// epoch with the renewer/discoverer (they compare stamps from this clock
/// against their own readings).
fn default_nano_time_provider() -> NanoTimeProvider {
    Arc::new(crate::utils::monotonic_clock::monotonic_nanos)
}

fn now_millis() -> i64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

/// Whether a [`LeasingError`] is a provisioned-throughput error (the only
/// retryable case in the take loops).
fn is_provisioned_throughput(e: &LeasingError) -> bool {
    matches!(e, LeasingError::ProvisionedThroughput { .. })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::kpl::ExtendedSequenceNumber;

    const WORKER_IDENTIFIER: &str = "foo";
    const LEASE_DURATION_MILLIS: i64 = 1000;
    const DEFAULT_VERY_OLD_LEASE_DURATION_MULTIPLIER: i32 = 3;
    const VERY_OLD_LEASE_DURATION_MULTIPLIER: i32 = 5;
    const MOCK_CURRENT_TIME: i64 = 10_000_000_000;

    fn create_lease(lease_owner: Option<&str>, lease_key: &str) -> Lease {
        let mut lease = Lease::default();
        lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number("checkpoint"));
        lease.set_owner_switches_since_checkpoint(0);
        lease.set_lease_counter(0);
        lease.set_lease_owner(lease_owner.map(|s| s.to_string()));
        lease.set_parent_shard_ids(["parentShardId".to_string()]);
        lease.set_child_shard_ids(HashSet::<String>::new());
        lease.set_lease_key(lease_key);
        lease
    }

    fn create_lease_with_nanos(
        lease_owner: Option<&str>,
        lease_key: &str,
        last_counter_increment_nanos: i64,
    ) -> Lease {
        let mut lease = create_lease(lease_owner, lease_key);
        lease.set_last_counter_increment_nanos(Some(last_counter_increment_nanos));
        lease
    }

    fn taker() -> DynamoDBLeaseTaker {
        DynamoDBLeaseTaker::new(
            Arc::new(MockLeaseRefresher::new()),
            WORKER_IDENTIFIER,
            LEASE_DURATION_MILLIS,
            Arc::new(NullMetricsFactory),
        )
    }

    async fn put_all(taker: &DynamoDBLeaseTaker, leases: Vec<Lease>) {
        let mut state = taker.state.lock().await;
        for lease in leases {
            state
                .all_leases
                .insert(lease.lease_key().unwrap().to_string(), lease);
        }
    }

    #[test]
    fn test_string_join() {
        // Rust equivalent of the Java stringJoin helper: join keys with ", ".
        let single = ["foo".to_string()];
        assert_eq!(single.join(", "), "foo");
        let two = ["foo".to_string(), "bar".to_string()];
        assert_eq!(two.join(", "), "foo, bar");
    }

    #[tokio::test]
    async fn test_compute_lease_counts_no_expired_lease() {
        let taker = taker();
        put_all(
            &taker,
            vec![
                create_lease(None, "1"),
                create_lease(Some("foo"), "2"),
                create_lease(Some("bar"), "3"),
                create_lease(Some("baz"), "4"),
            ],
        )
        .await;

        let state = taker.state.lock().await;
        let actual = taker.compute_lease_counts(&state, &[]);

        let mut expected: HashMap<String, i32> = HashMap::new();
        // Java uses `null` owner key; here that lease (key "1", no owner) buckets
        // under "".
        expected.insert("".to_string(), 1);
        expected.insert("foo".to_string(), 1);
        expected.insert("bar".to_string(), 1);
        expected.insert("baz".to_string(), 1);
        assert_eq!(actual, expected);
    }

    #[tokio::test]
    async fn test_compute_lease_counts_with_expired_lease() {
        let taker = taker();
        let leases = vec![
            create_lease(Some("foo"), "2"),
            create_lease(Some("bar"), "3"),
            create_lease(Some("baz"), "4"),
        ];
        put_all(&taker, leases.clone()).await;

        let state = taker.state.lock().await;
        // All three passed as "available" -> excluded from counts; only the
        // always-included self ("foo") remains at 0.
        let actual = taker.compute_lease_counts(&state, &leases);

        let mut expected: HashMap<String, i32> = HashMap::new();
        expected.insert("foo".to_string(), 0);
        assert_eq!(actual, expected);
    }

    #[tokio::test]
    async fn test_very_old_lease_duration_nanos_multiplier_gets_correct_leases() {
        let very_old_threshold = MOCK_CURRENT_TIME
            - (LEASE_DURATION_MILLIS * 1_000_000 * VERY_OLD_LEASE_DURATION_MULTIPLIER as i64);
        let taker = DynamoDBLeaseTaker::new(
            Arc::new(MockLeaseRefresher::new()),
            WORKER_IDENTIFIER,
            LEASE_DURATION_MILLIS,
            Arc::new(NullMetricsFactory),
        )
        .with_very_old_lease_duration_nanos_multiplier(VERY_OLD_LEASE_DURATION_MULTIPLIER)
        .with_time_provider(Arc::new(move || MOCK_CURRENT_TIME));

        let all_leases = vec![
            create_lease_with_nanos(Some("foo"), "2", MOCK_CURRENT_TIME),
            create_lease_with_nanos(Some("bar"), "3", very_old_threshold - 1),
            create_lease_with_nanos(Some("baz"), "4", very_old_threshold),
        ];
        let expired_leases = all_leases[1..3].to_vec();
        put_all(&taker, all_leases.clone()).await;

        let state = taker.state.lock().await;
        let output = taker
            .compute_leases_to_take(&state, expired_leases)
            .await
            .unwrap();

        // Only the lease strictly older than the threshold (key "3") is taken.
        let mut expected: HashSet<Lease> = HashSet::new();
        expected.insert(all_leases[1].clone());
        assert_eq!(output, expected);
    }

    // --- Ported DynamoDBLeaseTakerIntegrationTest scenarios ---
    //
    // Java runs these against a real DynamoDB via a TestHarnessBuilder. Here we
    // drive the same take/steal selection logic through a `MockLeaseRefresher`
    // (whose `list_leases` returns the seeded leases and whose `take_lease`
    // records the taken keys), plus a fixed nano clock for determinism. `foo` is
    // always this taker's worker id.

    use std::sync::Arc as StdArc;
    use std::sync::Mutex as StdMutex;

    /// A lease as a fresh-scan row (no `lastCounterIncrementNanos` yet; that is
    /// stamped by `update_all_leases`).
    fn scan_lease(lease_key: &str, owner: Option<&str>) -> Lease {
        create_lease(owner, lease_key)
    }

    /// Build a taker over a `MockLeaseRefresher` that returns `leases` from
    /// `list_leases` and records taken keys into `taken`. Uses a fixed nano clock.
    fn taker_with_leases(
        leases: Vec<Lease>,
        lease_duration_millis: i64,
        taken: StdArc<StdMutex<Vec<String>>>,
    ) -> DynamoDBLeaseTaker {
        let mut refresher = MockLeaseRefresher::new();
        let leases_clone = leases.clone();
        refresher
            .expect_list_leases()
            .returning(move || Ok(leases_clone.clone()));
        let taken_clone = taken.clone();
        refresher
            .expect_take_lease()
            .returning(move |lease, owner| {
                lease.set_lease_owner(Some(owner.to_string()));
                taken_clone
                    .lock()
                    .unwrap()
                    .push(lease.lease_key().unwrap().to_string());
                Ok(true)
            });
        // Re-fetch path (updateStaleLeasesWithLatestState) may call get_lease.
        let leases_for_get = leases.clone();
        refresher.expect_get_lease().returning(move |key| {
            Ok(leases_for_get
                .iter()
                .find(|l| l.lease_key() == Some(key))
                .cloned())
        });

        DynamoDBLeaseTaker::new(
            Arc::new(refresher),
            WORKER_IDENTIFIER,
            lease_duration_millis,
            Arc::new(NullMetricsFactory),
        )
        .with_time_provider(Arc::new(move || MOCK_CURRENT_TIME))
    }

    /// Port of `DynamoDBLeaseTakerIntegrationTest.testGetAllLeases`.
    ///
    /// `allLeases()` returns the cache built during `takeLeases()` (empty
    /// before). Called directly from the async test context — regression
    /// coverage for the old `blocking_lock` accessor, which panicked when
    /// invoked from inside a tokio runtime.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_get_all_leases() {
        let leases = vec![
            scan_lease("1", Some("bar")),
            scan_lease("2", Some("bar")),
            scan_lease("3", Some("baz")),
            scan_lease("4", Some("baz")),
            scan_lease("5", Some("foo")),
        ];
        let taken = StdArc::new(StdMutex::new(Vec::new()));
        let taker = Arc::new(taker_with_leases(
            leases.clone(),
            LEASE_DURATION_MILLIS,
            taken,
        ));

        assert_eq!(taker.all_leases().len(), 0);

        taker.take_leases().await.unwrap();

        let all_leases = taker.all_leases();
        assert_eq!(all_leases.len(), leases.len());
        let all_keys: HashSet<String> = all_leases
            .iter()
            .map(|l| l.lease_key().unwrap().to_string())
            .collect();
        let expected_keys: HashSet<String> = leases
            .iter()
            .map(|l| l.lease_key().unwrap().to_string())
            .collect();
        assert_eq!(all_keys, expected_keys);
    }

    /// Port of `DynamoDBLeaseTakerIntegrationTest.testSlowGetAllLeases`.
    ///
    /// `leaseDurationMillis = 0` exercises the "get to update the existing lease
    /// after computing" path; `allLeases()` still returns every added lease.
    #[tokio::test(flavor = "multi_thread")]
    async fn test_slow_get_all_leases() {
        let leases = vec![
            scan_lease("1", Some("bar")),
            scan_lease("2", Some("bar")),
            scan_lease("5", Some("foo")),
        ];
        let taken = StdArc::new(StdMutex::new(Vec::new()));
        let taker = Arc::new(taker_with_leases(leases.clone(), 0, taken));

        assert_eq!(taker.all_leases().len(), 0);

        taker.take_leases().await.unwrap();

        assert_eq!(taker.all_leases().len(), leases.len());
    }

    /// Port of `DynamoDBLeaseTakerIntegrationTest.testNoStealWhenOffByOne`.
    ///
    /// bar holds 2, baz holds 2, foo holds 1; foo is only short by one and both
    /// others are at target, so foo steals nothing.
    #[tokio::test]
    async fn test_no_steal_when_off_by_one() {
        let leases = vec![
            scan_lease("1", Some("bar")),
            scan_lease("2", Some("bar")),
            scan_lease("3", Some("baz")),
            scan_lease("4", Some("baz")),
            scan_lease("5", Some("foo")),
        ];
        let taken = StdArc::new(StdMutex::new(Vec::new()));
        let taker = taker_with_leases(leases, LEASE_DURATION_MILLIS, taken.clone());

        let result = taker.take_leases().await.unwrap();

        assert!(result.is_empty());
        assert!(taken.lock().unwrap().is_empty());
    }

    /// Port of `DynamoDBLeaseTakerIntegrationTest.testSteal`.
    ///
    /// bar holds 1, baz holds 5, foo holds 0 (6 leases / 3 workers -> target 2).
    /// foo needs 2 leases; none are available, so it steals exactly one (clamped by
    /// the default `maxLeasesToStealAtOneTime = 1`) from the most-loaded worker
    /// (baz). The stolen lease must be one of baz's (shardId != "1").
    #[tokio::test]
    async fn test_steal() {
        let mut leases = vec![scan_lease("1", Some("bar"))];
        for i in 2..=6 {
            leases.push(scan_lease(&i.to_string(), Some("baz")));
        }
        let taken = StdArc::new(StdMutex::new(Vec::new()));
        let taker = taker_with_leases(leases, LEASE_DURATION_MILLIS, taken.clone());

        let result = taker.take_leases().await.unwrap();

        assert_eq!(result.len(), 1);
        let stolen_key = result.keys().next().unwrap().clone();
        assert_ne!(stolen_key, "1", "must steal from baz, not bar's lease 1");
    }

    /// Port of `DynamoDBLeaseTakerIntegrationTest.testNoStealWhenExpiredLeases`.
    ///
    /// Lease "1" is unassigned (available); "2".."4" belong to bar. foo takes the
    /// available lease "1" and does NOT steal even though it needs more.
    #[tokio::test]
    async fn test_no_steal_when_expired_leases() {
        let mut leases = vec![scan_lease("1", None)];
        for i in 2..=4 {
            leases.push(scan_lease(&i.to_string(), Some("bar")));
        }
        let taken = StdArc::new(StdMutex::new(Vec::new()));
        let taker = taker_with_leases(leases, LEASE_DURATION_MILLIS, taken.clone());

        let result = taker.take_leases().await.unwrap();

        let taken_keys: HashSet<String> = result.keys().cloned().collect();
        assert_eq!(taken_keys, HashSet::from(["1".to_string()]));
    }

    #[tokio::test]
    async fn test_disable_enable_priority_lease_assignment_gets_correct_leases() {
        let very_old_threshold = MOCK_CURRENT_TIME
            - (LEASE_DURATION_MILLIS
                * 1_000_000
                * DEFAULT_VERY_OLD_LEASE_DURATION_MULTIPLIER as i64);
        let taker = DynamoDBLeaseTaker::new(
            Arc::new(MockLeaseRefresher::new()),
            WORKER_IDENTIFIER,
            LEASE_DURATION_MILLIS,
            Arc::new(NullMetricsFactory),
        )
        .with_enable_priority_lease_assignment(false)
        .with_time_provider(Arc::new(move || MOCK_CURRENT_TIME));

        let all_leases = vec![
            create_lease_with_nanos(Some("bar"), "2", MOCK_CURRENT_TIME),
            create_lease_with_nanos(Some("bar"), "3", MOCK_CURRENT_TIME),
            create_lease_with_nanos(Some("bar"), "4", MOCK_CURRENT_TIME),
            create_lease_with_nanos(Some("baz"), "5", very_old_threshold - 1),
            create_lease_with_nanos(Some("baz"), "6", very_old_threshold + 1),
            create_lease(None, "7"),
        ];
        let expired_leases = all_leases[3..6].to_vec();
        put_all(&taker, all_leases.clone()).await;

        let state = taker.state.lock().await;
        let output = taker
            .compute_leases_to_take(&state, expired_leases.clone())
            .await
            .unwrap();

        // Priority disabled: with 6 leases / 2 workers -> target 3, myCount(foo)=0
        // -> needs 3 available leases; all 3 expired leases get taken.
        let expected: HashSet<Lease> = expired_leases.into_iter().collect();
        assert_eq!(output, expected);
    }
}
