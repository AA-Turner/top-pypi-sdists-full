//! Port of `software.amazon.kinesis.coordinator.PeriodicShardSyncManager`.
//!
//! Top-level orchestrator for periodic shard-sync. On the elected leader worker
//! it periodically audits every stream's leases for **holes in the hash-key
//! range** (a gap that indicates missing leases) and, when a hole persists for a
//! configured number of consecutive audits (the "confidence threshold"),
//! submits a shard-sync task to recover the missing leases.
//!
//! # Concurrency (deviation)
//!
//! - Java's `ScheduledExecutorService` (`scheduleWithFixedDelay`, 60s initial
//!   delay, `frequency` period) → a spawned tokio interval task; [`stop`]
//!   cancels it via a level-triggered [`CancellationToken`] and awaits the task
//!   bounded by [`STOP_WAIT_MILLIS`] before aborting. (Java's
//!   `shardSyncThreadPool.shutdown()` never interrupts an in-flight sync; the
//!   bounded wait + abort avoids leaking a hung task while still letting a
//!   normal in-flight sync finish.) The `synchronized start/stop` critical
//!   sections → a [`tokio::sync::Mutex`] guarding the task handle.
//!
//! [`CancellationToken`]: tokio_util::sync::CancellationToken
//! - Java's `Function<StreamConfig, ShardSyncTaskManager>` provider → an
//!   `Arc<dyn Fn(&StreamConfig) -> Arc<ShardSyncTaskManager> + Send + Sync>`.
//! - The `currentStreamConfigMap` / `streamToShardSyncTaskManagerMap` are shared
//!   with the Scheduler, so both are `Arc<Mutex<HashMap<...>>>`.
//! - `hashRangeHoleTrackerMap` is `PeriodicShardSyncManager`-private mutable
//!   state; a `Mutex<HashMap<...>>` gives it interior mutability so
//!   [`check_for_shard_sync`] can take `&self`.
//! - `runShardSync` is invoked from the async interval task, so the Java methods
//!   that block on Kinesis (`fillWithHashRangesIfRequired` → `listShards`,
//!   `updateLeaseWithMetaInfo`) stay **async** and are `.await`ed directly.
//!
//! [`stop`]: PeriodicShardSyncManager::stop
//! [`check_for_shard_sync`]: PeriodicShardSyncManager::check_for_shard_sync

use std::collections::{HashMap, HashSet};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};

use aws_sdk_cloudwatch::types::StandardUnit;
use num_bigint::BigInt;
use tokio::sync::Mutex as AsyncMutex;
use tokio::task::JoinHandle;

use crate::common::{HashKeyRangeForLease, StreamConfig, StreamIdentifier, STREAM_TYPE_KINESIS};
use crate::coordinator::leader_decider::LeaderDecider;
use crate::exceptions::BoxError;
use crate::leases::lease::Lease;
use crate::leases::{LeaseRefresher, ShardSyncTaskManager, UpdateField};
use crate::lifecycle::TaskResult;
use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};
use crate::utils::panic_util;

const INITIAL_DELAY_MILLIS: u64 = 60 * 1000;

/// Grace period [`stop`](PeriodicShardSyncManager::stop) waits for an in-flight
/// shard sync before aborting the interval task (mirrors the lease
/// coordinator's `STOP_WAIT_TIME_MILLIS`).
const STOP_WAIT_MILLIS: u64 = 2000;

/// Java `PeriodicShardSyncManager.PERIODIC_SHARD_SYNC_MANAGER` (metric operation).
pub const PERIODIC_SHARD_SYNC_MANAGER: &str = "PeriodicShardSyncManager";

/// Provider that maps a [`StreamConfig`] to its [`ShardSyncTaskManager`]. Java
/// `Function<StreamConfig, ShardSyncTaskManager>`.
pub type ShardSyncTaskManagerProvider =
    Arc<dyn Fn(&StreamConfig) -> Arc<ShardSyncTaskManager> + Send + Sync>;

/// `MIN_HASH_KEY = 0`. Java `PeriodicShardSyncManager.MIN_HASH_KEY`.
fn min_hash_key() -> BigInt {
    BigInt::from(0)
}

/// `MAX_HASH_KEY = 2^128 - 1`. Java `PeriodicShardSyncManager.MAX_HASH_KEY`.
fn max_hash_key() -> BigInt {
    (BigInt::from(1) << 128) - 1
}

/// Object containing metadata about the state of a shard sync. Java
/// `PeriodicShardSyncManager.ShardSyncResponse`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ShardSyncResponse {
    should_do_shard_sync: bool,
    is_hole_detected: bool,
    reason_for_decision: String,
}

impl ShardSyncResponse {
    fn new(
        should_do_shard_sync: bool,
        is_hole_detected: bool,
        reason_for_decision: String,
    ) -> Self {
        Self {
            should_do_shard_sync,
            is_hole_detected,
            reason_for_decision,
        }
    }

    /// Whether a shard sync is necessary. Java `shouldDoShardSync()`.
    pub fn should_do_shard_sync(&self) -> bool {
        self.should_do_shard_sync
    }

    /// Whether a hash-range hole was detected. Java `isHoleDetected()`.
    pub fn is_hole_detected(&self) -> bool {
        self.is_hole_detected
    }

    /// The reason behind the `should_do_shard_sync` state. Java
    /// `reasonForDecision()`.
    pub fn reason_for_decision(&self) -> &str {
        &self.reason_for_decision
    }
}

/// The two boundary hash ranges of a detected (possible) hole. Java
/// `PeriodicShardSyncManager.HashRangeHole` (a `@Value`; both fields `null` for
/// the "no valid hash ranges at all" case).
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct HashRangeHole {
    hash_range_at_start_of_possible_hole: Option<HashKeyRangeForLease>,
    hash_range_at_end_of_possible_hole: Option<HashKeyRangeForLease>,
}

impl HashRangeHole {
    /// Java no-arg `HashRangeHole()` — both boundaries `null`.
    fn empty() -> Self {
        Self {
            hash_range_at_start_of_possible_hole: None,
            hash_range_at_end_of_possible_hole: None,
        }
    }

    /// Java 2-arg `HashRangeHole(start, end)`.
    fn new(start: HashKeyRangeForLease, end: HashKeyRangeForLease) -> Self {
        Self {
            hash_range_at_start_of_possible_hole: Some(start),
            hash_range_at_end_of_possible_hole: Some(end),
        }
    }
}

/// Tracks how many consecutive audits have observed the *same* hole. Java
/// `PeriodicShardSyncManager.HashRangeHoleTracker`.
#[derive(Debug, Default)]
struct HashRangeHoleTracker {
    hash_range_hole: Option<HashRangeHole>,
    num_consecutive_holes: i32,
}

impl HashRangeHoleTracker {
    /// Java `hasHighConfidenceOfHoleWith(hashRangeHole)`: if the same hole
    /// repeats, increment the consecutive counter, else reset to 1. Returns
    /// whether the counter has reached the confidence threshold.
    fn has_high_confidence_of_hole_with(
        &mut self,
        hash_range_hole: HashRangeHole,
        threshold: i32,
    ) -> bool {
        if Some(&hash_range_hole) == self.hash_range_hole.as_ref() {
            self.num_consecutive_holes += 1;
        } else {
            self.hash_range_hole = Some(hash_range_hole);
            self.num_consecutive_holes = 1;
        }
        self.num_consecutive_holes >= threshold
    }

    fn num_consecutive_holes(&self) -> i32 {
        self.num_consecutive_holes
    }
}

/// Handles for the spawned periodic shard-sync task.
struct RunningTask {
    handle: JoinHandle<()>,
    stop: tokio_util::sync::CancellationToken,
}

/// Top-level orchestrator for periodic shard sync. Java
/// `PeriodicShardSyncManager`.
pub struct PeriodicShardSyncManager {
    worker_id: String,
    lease_refresher: Arc<dyn LeaseRefresher>,
    current_stream_config_map: Arc<Mutex<HashMap<StreamIdentifier, StreamConfig>>>,
    shard_sync_task_manager_provider: ShardSyncTaskManagerProvider,
    stream_to_shard_sync_task_manager_map:
        Arc<Mutex<HashMap<StreamConfig, Arc<ShardSyncTaskManager>>>>,
    is_multi_streaming_mode: bool,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    leases_recovery_auditor_execution_frequency_millis: i64,
    leases_recovery_auditor_inconsistency_confidence_threshold: i32,
    leader_synced: Arc<AtomicBool>,

    /// Java `hashRangeHoleTrackerMap` — private mutable audit state.
    hash_range_hole_tracker_map: Mutex<HashMap<StreamIdentifier, HashRangeHoleTracker>>,
    /// The leader decider, set on `start`.
    leader_decider: Mutex<Option<Arc<dyn LeaderDecider>>>,
    /// The spawned interval task; `Some` iff running (Java `isRunning`).
    task: AsyncMutex<Option<RunningTask>>,
}

impl PeriodicShardSyncManager {
    /// Java constructor. `workerId` must be non-blank (Java `Validate.notBlank`).
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if `worker_id` is blank.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        worker_id: impl Into<String>,
        lease_refresher: Arc<dyn LeaseRefresher>,
        current_stream_config_map: Arc<Mutex<HashMap<StreamIdentifier, StreamConfig>>>,
        shard_sync_task_manager_provider: ShardSyncTaskManagerProvider,
        stream_to_shard_sync_task_manager_map: Arc<
            Mutex<HashMap<StreamConfig, Arc<ShardSyncTaskManager>>>,
        >,
        is_multi_streaming_mode: bool,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        leases_recovery_auditor_execution_frequency_millis: i64,
        leases_recovery_auditor_inconsistency_confidence_threshold: i32,
        leader_synced: Arc<AtomicBool>,
    ) -> Arc<Self> {
        let worker_id = worker_id.into();
        if worker_id.trim().is_empty() {
            panic!("WorkerID is required to initialize PeriodicShardSyncManager.");
        }
        Arc::new(Self {
            worker_id,
            lease_refresher,
            current_stream_config_map,
            shard_sync_task_manager_provider,
            stream_to_shard_sync_task_manager_map,
            is_multi_streaming_mode,
            metrics_factory,
            leases_recovery_auditor_execution_frequency_millis,
            leases_recovery_auditor_inconsistency_confidence_threshold,
            leader_synced,
            hash_range_hole_tracker_map: Mutex::new(HashMap::new()),
            leader_decider: Mutex::new(None),
            task: AsyncMutex::new(None),
        })
    }

    /// Java `synchronized TaskResult start(leaderDecider)`. Spawns the interval
    /// loop (60s initial delay, `frequency` period). Idempotent.
    pub async fn start(self: &Arc<Self>, leader_decider: Arc<dyn LeaderDecider>) -> TaskResult {
        *self
            .leader_decider
            .lock()
            .expect("leader_decider lock poisoned") = Some(Arc::clone(&leader_decider));

        let mut guard = self.task.lock().await;
        if guard.is_none() {
            let this = Arc::clone(self);
            let period_millis = self
                .leases_recovery_auditor_execution_frequency_millis
                .max(1) as u64;
            let stop = tokio_util::sync::CancellationToken::new();
            let stop_task = stop.clone();
            let handle = tokio::spawn(async move {
                let start = tokio::time::Instant::now()
                    + std::time::Duration::from_millis(INITIAL_DELAY_MILLIS);
                let mut ticker = tokio::time::interval_at(
                    start,
                    std::time::Duration::from_millis(period_millis),
                );
                ticker.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
                loop {
                    tokio::select! {
                        biased;
                        _ = stop_task.cancelled() => break,
                        _ = ticker.tick() => {
                            // Java PeriodicShardSyncManager catch(Throwable): a
                            // panicking sync must not kill the periodic loop.
                            match panic_util::catch_tick(this.run_shard_sync()).await {
                                Ok(Ok(())) => {}
                                Ok(Err(e)) => {
                                    tracing::error!(error = %e, "Error during runShardSync.");
                                }
                                Err(panic_msg) => {
                                    tracing::error!(error = %panic_msg, "Error during runShardSync.");
                                }
                            }
                        }
                    }
                }
            });
            *guard = Some(RunningTask { handle, stop });
        }
        TaskResult::new(None)
    }

    /// Java `synchronized void syncShardsOnce()` — run shard sync once for every
    /// stream config, propagating the first exception. Does not schedule the
    /// periodic sync.
    pub async fn sync_shards_once(&self) -> Result<(), BoxError> {
        let configs: Vec<StreamConfig> = self
            .current_stream_config_map
            .lock()
            .expect("current_stream_config_map lock poisoned")
            .values()
            .cloned()
            .collect();
        for stream_config in configs {
            tracing::info!(?stream_config, "Syncing Kinesis shard info");
            let shard_sync_task_manager = (self.shard_sync_task_manager_provider)(&stream_config);
            let task_result = shard_sync_task_manager.call_shard_sync_task().await;
            if let Some(e) = task_result.take_exception() {
                return Err(e);
            }
        }
        Ok(())
    }

    /// Java `void stop()` — shut down the leader decider + abort the interval
    /// task.
    pub async fn stop(&self) {
        if let Some(task) = self.task.lock().await.take() {
            tracing::info!(worker = %self.worker_id, "Shutting down leader decider on worker");
            if let Some(ld) = self
                .leader_decider
                .lock()
                .expect("leader_decider lock poisoned")
                .as_ref()
            {
                ld.shutdown();
            }
            tracing::info!(
                worker = %self.worker_id,
                "Shutting down periodic shard sync task scheduler on worker"
            );
            // Signal (level-triggered, so a mid-sync task sees it on its next
            // loop iteration), then give an in-flight sync a bounded grace
            // period before aborting — Java's `shutdown()` never interrupts,
            // but never awaiting risks leaking a hung task.
            task.stop.cancel();
            let mut handle = task.handle;
            match tokio::time::timeout(
                std::time::Duration::from_millis(STOP_WAIT_MILLIS),
                &mut handle,
            )
            .await
            {
                Ok(Err(e)) if e.is_panic() => {
                    let payload = e.into_panic();
                    tracing::error!(
                        "Periodic shard sync task had panicked: {}",
                        panic_util::panic_message(payload.as_ref())
                    );
                }
                Ok(_) => {}
                Err(_) => handle.abort(),
            }
        }
    }

    fn leader_decider(&self) -> Option<Arc<dyn LeaderDecider>> {
        self.leader_decider
            .lock()
            .expect("leader_decider lock poisoned")
            .clone()
    }

    /// Java `runShardSync()` — the one-shot audit + submit. Runs only if this
    /// worker is the leader and the leader has synced.
    async fn run_shard_sync(&self) -> Result<(), BoxError> {
        let is_leader = self
            .leader_decider()
            .map(|ld| ld.is_leader(&self.worker_id))
            .unwrap_or(false);
        if !(is_leader && self.leader_synced.load(Ordering::SeqCst)) {
            tracing::debug!(
                worker = %self.worker_id,
                "WorkerId is not a leader, not running the shard sync task"
            );
            return Ok(());
        }
        tracing::info!(worker = %self.worker_id, "WorkerId is leader, running the periodic shard sync task");

        let mut scope = metrics_util::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            PERIODIC_SHARD_SYNC_MANAGER,
        );
        let mut num_streams_with_partial_leases = 0i64;
        let mut num_streams_to_sync = 0i64;
        let mut num_skipped_shard_sync_task = 0i64;
        let mut is_run_success = false;
        let run_start_millis = metrics_util::current_time_millis();

        // Wrap the fallible body so the `finally` metric emission always runs.
        let result: Result<(), BoxError> = async {
            // Copy the stream set to avoid a data race with the Scheduler.
            let stream_config_map: HashSet<StreamIdentifier> = self
                .current_stream_config_map
                .lock()
                .expect("current_stream_config_map lock poisoned")
                .keys()
                .cloned()
                .collect();

            let stream_to_leases_map = self.get_stream_to_leases_map(&stream_config_map).await?;

            for stream_identifier in &stream_config_map {
                if !self
                    .current_stream_config_map
                    .lock()
                    .expect("current_stream_config_map lock poisoned")
                    .contains_key(stream_identifier)
                {
                    tracing::info!(?stream_identifier, "Skipping shard sync task as stream is purged");
                    continue;
                }
                let mut leases = stream_to_leases_map.get(stream_identifier).cloned();
                let shard_sync_response = self
                    .check_for_shard_sync(stream_identifier, leases.as_mut())
                    .await;

                if shard_sync_response.is_hole_detected {
                    num_streams_with_partial_leases += 1;
                }
                if shard_sync_response.should_do_shard_sync {
                    num_streams_to_sync += 1;
                }

                if shard_sync_response.should_do_shard_sync {
                    tracing::info!(
                        ?stream_identifier,
                        reason = %shard_sync_response.reason_for_decision,
                        "Periodic shard syncer initiating shard sync"
                    );
                    let stream_config = self
                        .current_stream_config_map
                        .lock()
                        .expect("current_stream_config_map lock poisoned")
                        .get(stream_identifier)
                        .cloned();
                    let stream_config = match stream_config {
                        Some(c) => c,
                        None => {
                            tracing::info!(
                                ?stream_identifier,
                                "Skipping shard sync task as stream is purged"
                            );
                            continue;
                        }
                    };
                    let shard_sync_task_manager = self.get_or_create_task_manager(&stream_config);

                    if !shard_sync_task_manager.submit_shard_sync_task().await {
                        tracing::warn!(
                            ?stream_identifier,
                            "Failed to submit shard sync task. This could be due to the previous pending shard sync task."
                        );
                        num_skipped_shard_sync_task += 1;
                    } else {
                        tracing::info!(
                            ?stream_identifier,
                            reason = %shard_sync_response.reason_for_decision,
                            "Submitted shard sync task"
                        );
                    }
                } else {
                    tracing::info!(
                        ?stream_identifier,
                        reason = %shard_sync_response.reason_for_decision,
                        "Skipping shard sync"
                    );
                }
            }
            is_run_success = true;
            Ok(())
        }
        .await;

        if let Err(ref e) = result {
            tracing::error!(error = %e, "Caught exception while running periodic shard syncer.");
        }

        // finally block: emit SUMMARY metrics + success/latency, then end scope.
        scope.add_data_with_level(
            "NumStreamsWithPartialLeases",
            num_streams_with_partial_leases as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "NumStreamsToSync",
            num_streams_to_sync as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "NumSkippedShardSyncTask",
            num_skipped_shard_sync_task as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        metrics_util::add_success_and_latency(
            scope.as_mut(),
            is_run_success,
            run_start_millis,
            MetricsLevel::Summary,
        );
        metrics_util::end_scope(scope.as_mut());

        // Java swallows the exception inside the try/catch (logs only); the
        // interval loop expects `Ok` here so the schedule continues.
        let _ = result;
        Ok(())
    }

    /// Look up an existing `ShardSyncTaskManager` for the stream config, creating
    /// (and caching) one via the provider if absent. Java's `computeIfAbsent`.
    fn get_or_create_task_manager(
        &self,
        stream_config: &StreamConfig,
    ) -> Arc<ShardSyncTaskManager> {
        let mut map = self
            .stream_to_shard_sync_task_manager_map
            .lock()
            .expect("stream_to_shard_sync_task_manager_map lock poisoned");
        if let Some(existing) = map.get(stream_config) {
            return Arc::clone(existing);
        }
        let created = (self.shard_sync_task_manager_provider)(stream_config);
        map.insert(stream_config.clone(), Arc::clone(&created));
        created
    }

    /// Java `getStreamToLeasesMap(streamIdentifiersToFilter)`.
    async fn get_stream_to_leases_map(
        &self,
        stream_identifiers_to_filter: &HashSet<StreamIdentifier>,
    ) -> Result<HashMap<StreamIdentifier, Vec<Lease>>, BoxError> {
        let leases = self.lease_refresher.list_leases().await?;
        if !self.is_multi_streaming_mode {
            if stream_identifiers_to_filter.len() != 1 {
                return Err(Box::<dyn std::error::Error + Send + Sync>::from(format!(
                    "Expected exactly one stream identifier in single-stream mode, got {}",
                    stream_identifiers_to_filter.len()
                )));
            }
            let only = stream_identifiers_to_filter.iter().next().unwrap().clone();
            let mut map = HashMap::new();
            map.insert(only, leases);
            Ok(map)
        } else {
            let mut map: HashMap<StreamIdentifier, Vec<Lease>> = HashMap::new();
            for lease in leases {
                let stream_identifier = StreamIdentifier::multi_stream_instance(
                    lease
                        .stream_identifier()
                        .expect("multi-stream lease must carry a stream identifier"),
                );
                if stream_identifiers_to_filter.contains(&stream_identifier) {
                    map.entry(stream_identifier).or_default().push(lease);
                }
            }
            Ok(map)
        }
    }

    /// Java `checkForShardSync(streamIdentifier, leases)`. `leases` is `&mut`
    /// (and `Option` for Java's nullable list) because
    /// `fillWithHashRangesIfRequired` mutates the leases in place.
    pub async fn check_for_shard_sync(
        &self,
        stream_identifier: &StreamIdentifier,
        leases: Option<&mut Vec<Lease>>,
    ) -> ShardSyncResponse {
        let leases = match leases {
            Some(l) if !l.is_empty() => l,
            _ => {
                tracing::info!(
                    ?stream_identifier,
                    "No leases found. Will be triggering shard sync"
                );
                return ShardSyncResponse::new(
                    true,
                    false,
                    format!("No leases found for {stream_identifier:?}"),
                );
            }
        };

        let hash_range_hole_opt = self.has_hole_in_leases(stream_identifier, leases).await;
        if let Some(hash_range_hole) = hash_range_hole_opt {
            let mut trackers = self
                .hash_range_hole_tracker_map
                .lock()
                .expect("hash_range_hole_tracker_map lock poisoned");
            let tracker = trackers.entry(stream_identifier.clone()).or_default();
            let has_hole_with_high_confidence = tracker.has_high_confidence_of_hole_with(
                hash_range_hole,
                self.leases_recovery_auditor_inconsistency_confidence_threshold,
            );
            let num = tracker.num_consecutive_holes();
            ShardSyncResponse::new(
                has_hole_with_high_confidence,
                true,
                format!(
                    "Detected same hole for {num} times. Shard sync will be initiated when threshold reaches {}",
                    self.leases_recovery_auditor_inconsistency_confidence_threshold
                ),
            )
        } else {
            self.hash_range_hole_tracker_map
                .lock()
                .expect("hash_range_hole_tracker_map lock poisoned")
                .remove(stream_identifier);
            ShardSyncResponse::new(
                false,
                false,
                format!("Hash Ranges are complete for {stream_identifier:?}"),
            )
        }
    }

    /// Java `hasHoleInLeases(streamIdentifier, leases)`. Filters to active leases
    /// (checkpoint present and not SHARD_END), backfills missing hash ranges,
    /// then checks for a hole.
    async fn has_hole_in_leases(
        &self,
        stream_identifier: &StreamIdentifier,
        leases: &mut [Lease],
    ) -> Option<HashRangeHole> {
        // Active-lease indices: checkpoint present and not shard-end.
        let active_indices: Vec<usize> = leases
            .iter()
            .enumerate()
            .filter(|(_, l)| l.checkpoint().map(|c| !c.is_shard_end()).unwrap_or(false))
            .map(|(i, _)| i)
            .collect();

        let active_with_hash_ranges = self
            .fill_with_hash_ranges_if_required(stream_identifier, leases, &active_indices)
            .await;
        Self::check_for_hole_in_hash_key_ranges_inner(stream_identifier, &active_with_hash_ranges)
    }

    /// Java `fillWithHashRangesIfRequired(streamIdentifier, activeLeases)`. If
    /// any active lease is missing its hash range, look up the Kinesis shards and
    /// backfill (in-memory + best-effort persist). Returns the set of active
    /// leases that now have a hash range (as clones, mirroring the returned
    /// list); the passed-in `leases` are also mutated in place so callers holding
    /// them observe the backfill.
    async fn fill_with_hash_ranges_if_required(
        &self,
        stream_identifier: &StreamIdentifier,
        leases: &mut [Lease],
        active_indices: &[usize],
    ) -> Vec<Lease> {
        // Any active lease missing a hash range?
        let missing_any = active_indices
            .iter()
            .any(|&i| leases[i].hash_key_range_for_lease().is_none());

        if !missing_any {
            // Return the active leases as-is (all already have hash ranges).
            return active_indices.iter().map(|&i| leases[i].clone()).collect();
        }

        // Fetch Kinesis shards for this stream via the provider's shard detector.
        let stream_config = self
            .current_stream_config_map
            .lock()
            .expect("current_stream_config_map lock poisoned")
            .get(stream_identifier)
            .cloned();
        let kinesis_shards: HashMap<String, HashKeyRangeForLease> = match stream_config {
            Some(cfg) => {
                let shard_detector = (self.shard_sync_task_manager_provider)(&cfg).shard_detector();
                match shard_detector.list_shards().await {
                    Ok(shards) => shards
                        .into_iter()
                        .filter_map(|s| {
                            let id = s.shard_id().to_string();
                            s.hash_key_range()
                                .map(|hkr| (id, HashKeyRangeForLease::from_hash_key_range(hkr)))
                        })
                        .collect(),
                    Err(e) => {
                        tracing::warn!(error = %e, ?stream_identifier, "Unable to list shards for hash-range backfill");
                        HashMap::new()
                    }
                }
            }
            None => HashMap::new(),
        };

        // Backfill each active lease missing a hash range, then keep only those
        // that now have a hash range.
        let mut result = Vec::new();
        for &i in active_indices {
            if leases[i].hash_key_range_for_lease().is_none() {
                // shardId = multiStream ? shardId() : leaseKey()
                let shard_id = if leases[i].is_multi_stream() {
                    leases[i].shard_id().map(str::to_string)
                } else {
                    leases[i].lease_key().map(str::to_string)
                };
                if let Some(shard_id) = shard_id {
                    if let Some(hkr) = kinesis_shards.get(&shard_id) {
                        leases[i].set_hash_key_range(hkr.clone());
                        if let Err(e) = self
                            .lease_refresher
                            .update_lease_with_meta_info(&leases[i], UpdateField::HashKeyRange)
                            .await
                        {
                            tracing::warn!(
                                error = %e,
                                lease_key = ?leases[i].lease_key(),
                                ?stream_identifier,
                                "Unable to update hash range key information for lease. This may result in explicit lease sync."
                            );
                        }
                    }
                }
            }
            if leases[i].hash_key_range_for_lease().is_some() {
                result.push(leases[i].clone());
            }
        }
        result
    }

    /// Java `static Optional<HashRangeHole> checkForHoleInHashKeyRanges(...)`.
    /// Sorts by starting hash key, validates the `[MIN, MAX]` bounds, then walks
    /// the sorted intervals looking for a gap (`rangeDiff > 1`), merging
    /// overlapping intervals as it goes. `Some(_)` iff a hole is present (Java
    /// `Optional.isPresent()`).
    fn check_for_hole_in_hash_key_ranges_inner(
        stream_identifier: &StreamIdentifier,
        leases_with_hash_key_ranges: &[Lease],
    ) -> Option<HashRangeHole> {
        let sorted = Self::sort_leases_by_hash_range(leases_with_hash_key_ranges);
        if sorted.is_empty() {
            if Self::is_hash_range_error_logging_enabled(stream_identifier) {
                tracing::error!(
                    ?stream_identifier,
                    "No leases with valid hashranges found for stream"
                );
            }
            return Some(HashRangeHole::empty());
        }

        let first_hkr = sorted[0].hash_key_range_for_lease().unwrap();
        let last_hkr = sorted[sorted.len() - 1].hash_key_range_for_lease().unwrap();
        // Validate the bounds: first.start == MIN and last.end == MAX.
        if *first_hkr.starting_hash_key() != min_hash_key()
            || *last_hkr.ending_hash_key() != max_hash_key()
        {
            if Self::is_hash_range_error_logging_enabled(stream_identifier) {
                tracing::error!(
                    ?stream_identifier,
                    "Incomplete hash range found for stream."
                );
            }
            return Some(HashRangeHole::new(first_hkr.clone(), last_hkr.clone()));
        }

        // Walk the sorted intervals for a hole.
        if sorted.len() > 1 {
            let mut leftmost_lease_hkr = sorted[0].hash_key_range_for_lease().unwrap().clone();
            let mut left_lease_hash_range = leftmost_lease_hkr.clone();
            for lease in sorted.iter().skip(1) {
                let right_lease_hash_range = lease.hash_key_range_for_lease().unwrap();
                let range_diff = right_lease_hash_range.starting_hash_key()
                    - left_lease_hash_range.ending_hash_key();
                // signum <= 0 => overlapping; merge.
                if range_diff.sign() != num_bigint::Sign::Plus {
                    let merged_end = std::cmp::max(
                        left_lease_hash_range.ending_hash_key().clone(),
                        right_lease_hash_range.ending_hash_key().clone(),
                    );
                    left_lease_hash_range = HashKeyRangeForLease::new(
                        left_lease_hash_range.starting_hash_key().clone(),
                        merged_end,
                    );
                } else {
                    // rangeDiff > 0. If not exactly 1, it is a hole.
                    if range_diff != BigInt::from(1) {
                        if Self::is_hash_range_error_logging_enabled(stream_identifier) {
                            tracing::error!(?stream_identifier, "Incomplete hash range found.");
                        }
                        return Some(HashRangeHole::new(
                            leftmost_lease_hkr.clone(),
                            right_lease_hash_range.clone(),
                        ));
                    }
                    leftmost_lease_hkr = right_lease_hash_range.clone();
                    left_lease_hash_range = right_lease_hash_range.clone();
                }
            }
        }
        None
    }

    /// Java `static List<Lease> sortLeasesByHashRange(...)`. Sorts by
    /// (startingHashKey, endingHashKey). Returns a cloned, sorted vector (the
    /// Java in-place sort is not observable here).
    pub fn sort_leases_by_hash_range(leases_with_hash_key_ranges: &[Lease]) -> Vec<Lease> {
        let mut v: Vec<Lease> = leases_with_hash_key_ranges.to_vec();
        if v.len() <= 1 {
            return v;
        }
        v.sort_by(|a, b| {
            let ah = a
                .hash_key_range_for_lease()
                .expect("lease must have hash range");
            let bh = b
                .hash_key_range_for_lease()
                .expect("lease must have hash range");
            ah.starting_hash_key()
                .cmp(bh.starting_hash_key())
                .then_with(|| ah.ending_hash_key().cmp(bh.ending_hash_key()))
        });
        v
    }

    /// Java `isHashRangeErrorLoggingEnabled` — only Kinesis-typed streams log.
    fn is_hash_range_error_logging_enabled(stream_identifier: &StreamIdentifier) -> bool {
        stream_identifier.stream_type() == STREAM_TYPE_KINESIS
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::StreamConfig;
    use crate::leases::shard_detector::ShardDetector;
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;
    use crate::retrieval::kpl::ExtendedSequenceNumber;
    use aws_sdk_kinesis::types::{HashKeyRange, SequenceNumberRange, Shard};

    const DEFAULT_CONSECUTIVE_HOLES: i32 =
        crate::leases::lease_management_config::DEFAULT_CONSECUTIVE_HOLES_FOR_TRIGGERING_LEASE_RECOVERY;

    fn stream_identifier() -> StreamIdentifier {
        StreamIdentifier::multi_stream_instance("123456789012:stream:456")
    }

    fn max_hash_key_string() -> String {
        max_hash_key().to_string()
    }

    /// A lease with a hash range (from serialized strings) and a checkpoint.
    fn lease_with_hash_range(start: &str, end: &str, checkpoint: ExtendedSequenceNumber) -> Lease {
        let mut lease = Lease::default();
        lease.set_hash_key_range(HashKeyRangeForLease::deserialize(start, end));
        lease.set_checkpoint(checkpoint);
        lease
    }

    /// Build the tested `PeriodicShardSyncManager` with mocked/empty collaborators.
    /// `provider` supplies the shard-sync task managers (used by the backfill
    /// tests; the pure hole tests never call it).
    fn manager_with(
        provider: ShardSyncTaskManagerProvider,
        current_stream_config_map: Arc<Mutex<HashMap<StreamIdentifier, StreamConfig>>>,
        confidence_threshold: i32,
    ) -> Arc<PeriodicShardSyncManager> {
        let mut refresher = MockLeaseRefresher::new();
        // The hash-range backfill path persists filled leases via
        // update_lease_with_meta_info; permit it (no-op) for all manager_with callers.
        refresher
            .expect_update_lease_with_meta_info()
            .returning(|_, _| Ok(()));
        PeriodicShardSyncManager::new(
            "worker",
            Arc::new(refresher),
            current_stream_config_map,
            provider,
            Arc::new(Mutex::new(HashMap::new())),
            true,
            Arc::new(NullMetricsFactory),
            2 * 60 * 1000,
            confidence_threshold,
            Arc::new(AtomicBool::new(true)),
        )
    }

    fn panicking_provider() -> ShardSyncTaskManagerProvider {
        Arc::new(|_: &StreamConfig| -> Arc<ShardSyncTaskManager> {
            panic!("provider should not be called in this test")
        })
    }

    fn manager() -> Arc<PeriodicShardSyncManager> {
        manager_with(
            panicking_provider(),
            Arc::new(Mutex::new(HashMap::new())),
            DEFAULT_CONSECUTIVE_HOLES,
        )
    }

    // ---- checkForHoleInHashKeyRanges (static) ----

    fn multi_stream_leases_from(
        ranges: &[(&str, &str)],
        checkpoint: ExtendedSequenceNumber,
    ) -> Vec<Lease> {
        ranges
            .iter()
            .map(|(s, e)| lease_with_hash_range(s, e, checkpoint.clone()))
            .collect()
    }

    #[test]
    fn for_failure_when_hash_ranges_are_incomplete() {
        let max = max_hash_key_string();
        let leases = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("4", "23"),
                ("6", "23"),
                ("25", &max),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        assert!(
            PeriodicShardSyncManager::check_for_hole_in_hash_key_ranges_inner(
                &stream_identifier(),
                &leases
            )
            .is_some()
        );
    }

    #[test]
    fn for_success_when_hash_ranges_are_complete() {
        let max = max_hash_key_string();
        let leases = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("4", "23"),
                ("6", "23"),
                ("24", &max),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        assert!(
            PeriodicShardSyncManager::check_for_hole_in_hash_key_ranges_inner(
                &stream_identifier(),
                &leases
            )
            .is_none()
        );
    }

    #[test]
    fn for_success_when_unsorted_hash_ranges_are_complete() {
        let max = max_hash_key_string();
        let leases = multi_stream_leases_from(
            &[
                ("4", "23"),
                ("2", "3"),
                ("0", "1"),
                ("24", &max),
                ("6", "23"),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        assert!(
            PeriodicShardSyncManager::check_for_hole_in_hash_key_ranges_inner(
                &stream_identifier(),
                &leases
            )
            .is_none()
        );
    }

    #[test]
    fn for_success_when_hash_ranges_are_complete_for_overlapping_leases_at_end() {
        let max = max_hash_key_string();
        let leases = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("4", "23"),
                ("6", "23"),
                ("24", &max),
                ("24", "45"),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        assert!(
            PeriodicShardSyncManager::check_for_hole_in_hash_key_ranges_inner(
                &stream_identifier(),
                &leases
            )
            .is_none()
        );
    }

    // ---- checkForShardSync ----

    #[tokio::test]
    async fn shard_sync_initiated_when_no_leases_passed() {
        let m = manager();
        assert!(m
            .check_for_shard_sync(&stream_identifier(), None)
            .await
            .should_do_shard_sync());
    }

    #[tokio::test]
    async fn shard_sync_initiated_when_empty_leases_passed() {
        let m = manager();
        let mut empty = Vec::new();
        assert!(m
            .check_for_shard_sync(&stream_identifier(), Some(&mut empty))
            .await
            .should_do_shard_sync());
    }

    #[tokio::test]
    async fn shard_sync_not_initiated_when_confidence_factor_not_reached() {
        let m = manager();
        let max = max_hash_key_string();
        let mut leases = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("4", "23"),
                ("6", "23"),
                ("25", &max),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
                .await
                .should_do_shard_sync());
        }
    }

    #[tokio::test]
    async fn shard_sync_initiated_when_confidence_factor_reached() {
        let m = manager();
        let max = max_hash_key_string();
        let mut leases = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("4", "23"),
                ("6", "23"),
                ("25", &max),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
                .await
                .should_do_shard_sync());
        }
        assert!(m
            .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
            .await
            .should_do_shard_sync());
    }

    #[tokio::test]
    async fn shard_sync_initiated_when_hole_is_due_to_shard_end() {
        let m = manager();
        let max = max_hash_key_string();
        // A hole is introduced by SHARD_END-checkpointing the ("4","23") lease.
        let ranges = [
            ("0", "1"),
            ("2", "3"),
            ("4", "23"),
            ("6", "23"),
            ("24", &max),
        ];
        let mut leases: Vec<Lease> = ranges
            .iter()
            .map(|(s, e)| {
                let checkpoint = if *s == "4" {
                    ExtendedSequenceNumber::shard_end()
                } else {
                    ExtendedSequenceNumber::trim_horizon()
                };
                lease_with_hash_range(s, e, checkpoint)
            })
            .collect();
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
                .await
                .should_do_shard_sync());
        }
        assert!(m
            .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
            .await
            .should_do_shard_sync());
    }

    #[tokio::test]
    async fn shard_sync_initiated_when_no_leases_used_due_to_shard_end() {
        let m = manager();
        let max = max_hash_key_string();
        // Every lease is SHARD_END → no active leases → empty sorted list → hole.
        let mut leases = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("4", "23"),
                ("6", "23"),
                ("24", &max),
            ],
            ExtendedSequenceNumber::shard_end(),
        );
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
                .await
                .should_do_shard_sync());
        }
        assert!(m
            .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
            .await
            .should_do_shard_sync());
    }

    #[tokio::test]
    async fn shard_sync_not_initiated_when_hole_shifts() {
        let m = manager();
        let max = max_hash_key_string();
        let mut leases1 = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("4", "23"),
                ("6", "23"),
                ("25", &max),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases1))
                .await
                .should_do_shard_sync());
        }
        // A different hole resets the consecutive counter.
        let mut leases2 = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("5", "23"),
                ("6", "23"),
                ("24", &max),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases2))
                .await
                .should_do_shard_sync());
        }
        assert!(m
            .check_for_shard_sync(&stream_identifier(), Some(&mut leases2))
            .await
            .should_do_shard_sync());
    }

    #[tokio::test]
    async fn shard_sync_not_initiated_when_hole_shifts_more_than_once() {
        let m = manager();
        let max = max_hash_key_string();
        let mut leases1 = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("4", "23"),
                ("6", "23"),
                ("25", &max),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases1))
                .await
                .should_do_shard_sync());
        }
        let mut leases2 = multi_stream_leases_from(
            &[
                ("0", "1"),
                ("2", "3"),
                ("5", "23"),
                ("6", "23"),
                ("24", &max),
            ],
            ExtendedSequenceNumber::trim_horizon(),
        );
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases2))
                .await
                .should_do_shard_sync());
        }
        // Shift back to the first hole; the counter is reset again.
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases1))
                .await
                .should_do_shard_sync());
        }
        assert!(m
            .check_for_shard_sync(&stream_identifier(), Some(&mut leases1))
            .await
            .should_do_shard_sync());
    }

    // ---- fill hash ranges via a shard detector ----

    fn shard_with(id: &str, hkr: &HashKeyRangeForLease) -> Shard {
        Shard::builder()
            .shard_id(id)
            .sequence_number_range(
                SequenceNumberRange::builder()
                    .starting_sequence_number("1")
                    .build()
                    .unwrap(),
            )
            .hash_key_range(
                HashKeyRange::builder()
                    .starting_hash_key(hkr.serialized_starting_hash_key())
                    .ending_hash_key(hkr.serialized_ending_hash_key())
                    .build()
                    .unwrap(),
            )
            .build()
            .unwrap()
    }

    struct StaticShardDetector {
        shards: Vec<Shard>,
    }

    #[async_trait::async_trait]
    impl ShardDetector for StaticShardDetector {
        async fn shard(
            &self,
            _id: &str,
        ) -> Result<Option<Shard>, crate::leases::exceptions::LeasingError> {
            Ok(None)
        }
        async fn list_shards(&self) -> Result<Vec<Shard>, crate::leases::exceptions::LeasingError> {
            Ok(self.shards.clone())
        }
        async fn list_shards_with_filter_for_consumer(
            &self,
            _f: aws_sdk_kinesis::types::ShardFilter,
            _c: &str,
        ) -> Result<Vec<Shard>, crate::leases::exceptions::LeasingError> {
            self.list_shards().await
        }
        fn stream_identifier(
            &self,
        ) -> Result<StreamIdentifier, crate::leases::exceptions::LeasingError> {
            Ok(stream_identifier())
        }
    }

    /// Build a `ShardSyncTaskManager` whose shard detector returns `shards` and
    /// whose lease refresher is a no-op mock.
    fn task_manager_with_shards(shards: Vec<Shard>) -> Arc<ShardSyncTaskManager> {
        use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
        use crate::leases::hierarchical_shard_syncer::HierarchicalShardSyncer;
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_list_leases().returning(|| Ok(Vec::new()));
        refresher
            .expect_update_lease_with_meta_info()
            .returning(|_, _| Ok(()));
        Arc::new(ShardSyncTaskManager::new(
            Arc::new(StaticShardDetector { shards }),
            Arc::new(refresher),
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            true,
            false,
            0,
            Arc::new(HierarchicalShardSyncer::new()),
            Arc::new(NullMetricsFactory),
        ))
    }

    /// Build leases mirroring the Java backfill tests: multi-stream leases keyed
    /// `stream:shard-N`, with hash ranges set only for the leases whose index is
    /// >= 3 (1-based). Returns (leases, shards) where shard-N maps to the Nth
    /// > hash range.
    fn backfill_leases_and_shards(ranges: &[(&str, &str)]) -> (Vec<Lease>, Vec<Shard>) {
        let sid = stream_identifier().serialize();
        let mut leases = Vec::new();
        let mut shards = Vec::new();
        for (i, (s, e)) in ranges.iter().enumerate() {
            let n = i + 1; // 1-based
            let shard_id = format!("shard-{n}");
            let hkr = HashKeyRangeForLease::deserialize(s, e);
            shards.push(shard_with(&shard_id, &hkr));

            let mut base = Lease::default();
            base.set_lease_key(Lease::multi_stream_lease_key(&sid, &shard_id));
            base.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
            let mut lease = Lease::new_multi_stream(base, sid.clone(), shard_id.clone());
            if n >= 3 {
                lease.set_hash_key_range(hkr);
            }
            leases.push(lease);
        }
        (leases, shards)
    }

    #[tokio::test]
    async fn missing_hash_range_information_is_filled_no_hole() {
        let max = max_hash_key_string();
        let ranges = [
            ("0", "1"),
            ("2", "3"),
            ("4", "20"),
            ("21", "23"),
            ("24", max.as_str()),
        ];
        let (leases, shards) = backfill_leases_and_shards(&ranges);

        let tm = task_manager_with_shards(shards);
        let provider: ShardSyncTaskManagerProvider = {
            let tm = tm.clone();
            Arc::new(move |_: &StreamConfig| tm.clone())
        };

        // current_stream_config_map must contain the stream so the provider is
        // consulted.
        let cfg = StreamConfig::new(
            stream_identifier(),
            crate::common::InitialPositionInStreamExtended::new_initial_position(
                crate::common::InitialPositionInStream::TrimHorizon,
            ),
        );
        let map = Arc::new(Mutex::new(HashMap::from([(stream_identifier(), cfg)])));
        let m = manager_with(provider, map, DEFAULT_CONSECUTIVE_HOLES);

        let mut leases = leases;
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
                .await
                .should_do_shard_sync());
        }
        assert!(!m
            .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
            .await
            .should_do_shard_sync());
        // All leases now have hash ranges.
        for lease in &leases {
            assert!(lease.hash_key_range_for_lease().is_some());
        }
    }

    #[tokio::test]
    async fn missing_hash_range_information_is_filled_hole_scenario() {
        let max = max_hash_key_string();
        // Hole between 3 and 5.
        let ranges = [
            ("0", "1"),
            ("2", "3"),
            ("5", "20"),
            ("21", "23"),
            ("24", max.as_str()),
        ];
        let (leases, shards) = backfill_leases_and_shards(&ranges);

        let tm = task_manager_with_shards(shards);
        let provider: ShardSyncTaskManagerProvider = {
            let tm = tm.clone();
            Arc::new(move |_: &StreamConfig| tm.clone())
        };
        let cfg = StreamConfig::new(
            stream_identifier(),
            crate::common::InitialPositionInStreamExtended::new_initial_position(
                crate::common::InitialPositionInStream::TrimHorizon,
            ),
        );
        let map = Arc::new(Mutex::new(HashMap::from([(stream_identifier(), cfg)])));
        let m = manager_with(provider, map, DEFAULT_CONSECUTIVE_HOLES);

        let mut leases = leases;
        for _ in 1..DEFAULT_CONSECUTIVE_HOLES {
            assert!(!m
                .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
                .await
                .should_do_shard_sync());
        }
        assert!(m
            .check_for_shard_sync(&stream_identifier(), Some(&mut leases))
            .await
            .should_do_shard_sync());
        for lease in &leases {
            assert!(lease.hash_key_range_for_lease().is_some());
        }
    }

    // ---- sortLeasesByHashRange ----

    #[test]
    fn sort_leases_by_hash_range_orders_by_start_then_end() {
        let leases = vec![
            lease_with_hash_range("10", "20", ExtendedSequenceNumber::trim_horizon()),
            lease_with_hash_range("0", "5", ExtendedSequenceNumber::trim_horizon()),
            lease_with_hash_range("0", "3", ExtendedSequenceNumber::trim_horizon()),
        ];
        let sorted = PeriodicShardSyncManager::sort_leases_by_hash_range(&leases);
        let starts: Vec<String> = sorted
            .iter()
            .map(|l| {
                l.hash_key_range_for_lease()
                    .unwrap()
                    .serialized_starting_hash_key()
            })
            .collect();
        let ends: Vec<String> = sorted
            .iter()
            .map(|l| {
                l.hash_key_range_for_lease()
                    .unwrap()
                    .serialized_ending_hash_key()
            })
            .collect();
        assert_eq!(starts, vec!["0", "0", "10"]);
        assert_eq!(ends, vec!["3", "5", "20"]);
    }

    // ---- 1000-iteration randomized hierarchy fuzz tests (hasHoleInLeases) ----
    //
    // Faithful port of the Java `testFor1000Different...HierarchyTree...` tests.
    // They generate a complete initial hash-range partition, apply a random
    // sequence of splits/merges (which always preserve completeness), shuffle,
    // and assert `hasHoleInLeases` reports NO hole. `Math.random()` becomes the
    // `rand` crate.

    #[derive(Clone, Copy, PartialEq)]
    enum ReshardType {
        Split,
        Merge,
        Any,
    }

    /// Java depth used with the in-progress-parent variants.
    const MAX_DEPTH_WITH_IN_PROGRESS_PARENTS: i32 = 1;

    /// Java `generateInitialLeases(initialShardCount)`: a complete partition of
    /// `[0, MAX_HASH_KEY]` into `initialShardCount` contiguous ranges, each
    /// TRIM_HORIZON, keyed `shard-N` (single-stream leases).
    fn generate_initial_leases(initial_shard_count: i64) -> Vec<Lease> {
        let hash_range_internal_max: i64 = 10_000_000;
        let mut initial_leases = Vec::new();
        let mut lease_start_key: i64 = 0;
        for i in 1..=initial_shard_count {
            let mut lease = Lease::default();
            let lease_end_key: i64;
            if i != initial_shard_count {
                lease_end_key = (hash_range_internal_max / initial_shard_count) * i;
                lease.set_hash_key_range(HashKeyRangeForLease::deserialize(
                    &lease_start_key.to_string(),
                    &lease_end_key.to_string(),
                ));
            } else {
                lease_end_key = 0;
                lease.set_hash_key_range(HashKeyRangeForLease::deserialize(
                    &lease_start_key.to_string(),
                    &max_hash_key_string(),
                ));
            }
            lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
            lease.set_lease_key(format!("shard-{i}"));
            initial_leases.push(lease);
            lease_start_key = lease_end_key + 1;
        }
        initial_leases
    }

    fn is_heads() -> bool {
        rand::random::<f64>() <= 0.5
    }

    fn is_one_from_dice_roll() -> bool {
        rand::random::<f64>() <= 0.16
    }

    /// Java `split(initialLeases, leaseCounter)`.
    fn split(initial_leases: &mut Vec<Lease>, mut lease_counter: i64) -> i64 {
        // Snapshot of indices eligible for split (no child shard ids yet).
        let eligible: Vec<usize> = initial_leases
            .iter()
            .enumerate()
            .filter(|(_, l)| l.child_shard_ids().is_empty())
            .map(|(i, _)| i)
            .collect();
        let leases_to_split = (eligible.len() as f64 * rand::random::<f64>()) as usize;
        for &parent_idx in eligible.iter().take(leases_to_split) {
            let parent_hkr = initial_leases[parent_idx]
                .hash_key_range_for_lease()
                .unwrap()
                .clone();
            let parent_key = initial_leases[parent_idx].lease_key().unwrap().to_string();
            initial_leases[parent_idx].set_checkpoint(ExtendedSequenceNumber::shard_end());

            let mid =
                (parent_hkr.starting_hash_key() + parent_hkr.ending_hash_key()) / BigInt::from(2);

            lease_counter += 1;
            let child1_key = format!("shard-{lease_counter}");
            let mut child1 = Lease::default();
            child1.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
            child1.set_hash_key_range(HashKeyRangeForLease::new(
                parent_hkr.starting_hash_key().clone(),
                mid.clone(),
            ));
            child1.set_lease_key(child1_key.clone());
            child1.set_parent_shard_ids([parent_key.clone()]);

            lease_counter += 1;
            let child2_key = format!("shard-{lease_counter}");
            let mut child2 = Lease::default();
            child2.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
            child2.set_hash_key_range(HashKeyRangeForLease::new(
                mid + BigInt::from(1),
                parent_hkr.ending_hash_key().clone(),
            ));
            child2.set_lease_key(child2_key.clone());
            child2.set_parent_shard_ids([parent_key]);

            initial_leases[parent_idx].set_child_shard_ids([child1_key, child2_key]);
            initial_leases.push(child1);
            initial_leases.push(child2);
        }
        lease_counter
    }

    /// Java `merge(initialLeases, leaseCounter, shouldKeepSomeParentsInProgress)`.
    fn merge(
        initial_leases: &mut Vec<Lease>,
        mut lease_counter: i64,
        should_keep_some_parents_in_progress: bool,
    ) -> i64 {
        let eligible: Vec<usize> = initial_leases
            .iter()
            .enumerate()
            .filter(|(_, l)| l.child_shard_ids().is_empty())
            .map(|(i, _)| i)
            .collect();
        let leases_to_merge =
            ((eligible.len() as f64 - 1.0) / 2.0 * rand::random::<f64>()) as usize;
        let mut i = 0;
        while i < leases_to_merge {
            let p1_idx = eligible[i];
            let p2_idx = eligible[i + 1];
            let p1_hkr = initial_leases[p1_idx]
                .hash_key_range_for_lease()
                .unwrap()
                .clone();
            let p2_hkr = initial_leases[p2_idx]
                .hash_key_range_for_lease()
                .unwrap()
                .clone();
            // Only merge if adjacent: p2.start - p1.end == 1.
            if (p2_hkr.starting_hash_key() - p1_hkr.ending_hash_key()) == BigInt::from(1) {
                let p1_key = initial_leases[p1_idx].lease_key().unwrap().to_string();
                let p2_key = initial_leases[p2_idx].lease_key().unwrap().to_string();
                initial_leases[p1_idx].set_checkpoint(ExtendedSequenceNumber::shard_end());
                if !should_keep_some_parents_in_progress || is_one_from_dice_roll() {
                    initial_leases[p2_idx].set_checkpoint(ExtendedSequenceNumber::shard_end());
                }
                lease_counter += 1;
                let child_key = format!("shard-{lease_counter}");
                let mut child = Lease::default();
                child.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
                child.set_lease_key(child_key.clone());
                child.set_hash_key_range(HashKeyRangeForLease::new(
                    p1_hkr.starting_hash_key().clone(),
                    p2_hkr.ending_hash_key().clone(),
                ));
                child.set_parent_shard_ids([p1_key, p2_key]);
                initial_leases[p1_idx].set_child_shard_ids([child_key.clone()]);
                initial_leases[p2_idx].set_child_shard_ids([child_key]);
                initial_leases.push(child);
            }
            i += 2;
        }
        lease_counter
    }

    /// Java `reshard(initialLeases, depth, reshardType, leaseCounter, keep)`.
    fn reshard(
        initial_leases: &mut Vec<Lease>,
        depth: i32,
        reshard_type: ReshardType,
        mut lease_counter: i64,
        should_keep_some_parents_in_progress: bool,
    ) {
        for _ in 0..depth {
            match reshard_type {
                ReshardType::Split => lease_counter = split(initial_leases, lease_counter),
                ReshardType::Merge => {
                    lease_counter = merge(
                        initial_leases,
                        lease_counter,
                        should_keep_some_parents_in_progress,
                    )
                }
                ReshardType::Any => {
                    if is_heads() {
                        lease_counter = split(initial_leases, lease_counter);
                    } else {
                        lease_counter = merge(
                            initial_leases,
                            lease_counter,
                            should_keep_some_parents_in_progress,
                        );
                    }
                }
            }
        }
    }

    /// Shuffle in place (Java `Collections.shuffle(leases)` — unseeded).
    fn shuffle_leases(leases: &mut [Lease]) {
        use rand::seq::SliceRandom;
        leases.shuffle(&mut rand::rng());
    }

    async fn assert_no_hole_after_reshard(
        reshard_type: ReshardType,
        depth: i32,
        keep_in_progress: bool,
    ) {
        let m = manager();
        let sid = stream_identifier();
        for _ in 0..1000 {
            let max_initial_lease_count: i64 = 100;
            let mut leases = generate_initial_leases(max_initial_lease_count);
            reshard(
                &mut leases,
                depth,
                reshard_type,
                max_initial_lease_count,
                keep_in_progress,
            );
            shuffle_leases(&mut leases);
            assert!(
                m.has_hole_in_leases(&sid, &mut leases).await.is_none(),
                "hash ranges should always be complete after a valid reshard"
            );
        }
    }

    #[tokio::test]
    async fn for_1000_different_valid_split_hierarchy_the_hash_ranges_are_always_complete() {
        assert_no_hole_after_reshard(ReshardType::Split, 5, false).await;
    }

    #[tokio::test]
    async fn for_1000_different_valid_merge_hierarchy_the_hash_ranges_are_always_complete() {
        assert_no_hole_after_reshard(ReshardType::Merge, 5, false).await;
    }

    #[tokio::test(start_paused = true)]
    async fn stop_joins_interval_task_gracefully() {
        use crate::coordinator::leader_decider::MockLeaderDecider;
        let m = manager();
        let mut ld = MockLeaderDecider::new();
        ld.expect_is_leader().returning(|_| false);
        ld.expect_shutdown().returning(|| ());
        m.start(Arc::new(ld)).await;
        // The interval task parks on its 60 s initial delay; `stop` cancels the
        // level-triggered token and must join the task without the STOP_WAIT
        // grace elapsing (the 1 ms outer timeout only fires if the clock has to
        // advance, i.e. if the signal were lost or the task had to be aborted).
        tokio::time::timeout(std::time::Duration::from_millis(1), m.stop())
            .await
            .expect("stop() should join the interval task without aborting it");
    }

    #[tokio::test]
    async fn for_1000_different_valid_reshard_hierarchy_the_hash_ranges_are_always_complete() {
        assert_no_hole_after_reshard(ReshardType::Any, 5, false).await;
    }

    #[tokio::test]
    async fn for_1000_valid_merge_hierarchy_with_some_in_progress_parents_hash_ranges_complete() {
        assert_no_hole_after_reshard(ReshardType::Merge, MAX_DEPTH_WITH_IN_PROGRESS_PARENTS, true)
            .await;
    }

    #[tokio::test]
    async fn for_1000_valid_reshard_hierarchy_with_some_in_progress_parents_hash_ranges_complete() {
        assert_no_hole_after_reshard(ReshardType::Any, MAX_DEPTH_WITH_IN_PROGRESS_PARENTS, true)
            .await;
    }

    #[test]
    fn worker_id_blank_panics() {
        let refresher = MockLeaseRefresher::new();
        let r = std::panic::catch_unwind(|| {
            PeriodicShardSyncManager::new(
                "   ",
                Arc::new(refresher),
                Arc::new(Mutex::new(HashMap::new())),
                panicking_provider(),
                Arc::new(Mutex::new(HashMap::new())),
                true,
                Arc::new(NullMetricsFactory),
                2 * 60 * 1000,
                3,
                Arc::new(AtomicBool::new(true)),
            );
        });
        assert!(r.is_err());
    }
}
