//! Port of `software.amazon.kinesis.leases.HierarchicalShardSyncer`.
//!
//! The core shard-graph reconciliation engine: given the current live shard
//! list from Kinesis and the current lease-table contents, it determines which
//! NEW leases must be created (for genuinely new shards and/or for ancestor
//! shards needed to preserve ordered processing), handles resharding
//! (splits/merges) via parent/child hierarchy traversal, validates hash-range
//! completeness, and creates leases for newly-discovered child shards at
//! `SHARD_END`.
//!
//! # Key behaviors preserved EXACTLY
//!
//! - [`check_if_descendant_and_add_new_leases_for_ancestors`]: the memoized
//!   ancestor-DFS. Memoization uses a [`MemoizationContext`]
//!   (`is_descendant_map` + `should_create_lease_map` keyed by shard id).
//! - Two lease-synchronization strategies, selected purely by whether the lease
//!   table was empty at the start of the pass:
//!   [`LeaseSynchronizer::Empty`] (bootstrap: create a lease for **every** shard)
//!   vs [`LeaseSynchronizer::NonEmpty`] (steady-state incremental ancestor-DFS
//!   over open shards).
//! - [`is_hash_range_of_shards_complete`]: sort by starting hash key, first
//!   starts at `0`, last ends at `2^128-1`, adjacent `end+1 == start` **exactly**
//!   (`num_bigint::BigInt`), with up to `RETRIES_FOR_COMPLETE_HASH_RANGE` (3)
//!   retries `DELAY_BETWEEN_LIST_SHARDS_MILLIS` (1s) apart.
//! - Final ordering by `StartingSequenceNumberAndShardIdBasedComparator`
//!   (BigInt starting sequence number, tie-broken by shard-id string) so a lease
//!   creation interrupted partway resumes order-safe.
//!
//! # Deviations
//!
//! - Async: [`check_and_create_lease_for_new_shards`] /
//!   [`check_and_create_lease_for_new_shards_with_list`] are `async` (the
//!   [`ShardDetector`] / [`LeaseRefresher`] traits are async). Per-instance
//!   serialization (Java method-level `synchronized`) is a
//!   [`tokio::sync::Mutex`] held for the call.
//! - `KinesisClientLibIOException` (hash-range / stream-state failures) →
//!   [`KinesisClientLibError::Io`]. Leasing failures propagate as
//!   [`LeasingError`], wrapped into [`KinesisClientLibError::Io`] where Java's
//!   signature only allows the IO/checked-leasing family.
//! - The `StreamIdCache` / `StreamInfoManager` global-singleton conditional
//!   error handling in `createStreamInfo` is **elided** (the stubs carry no
//!   behavior yet); the coordinator wave will wire dependency-injected
//!   equivalents. A `// TODO(port)` documents this.
//! - Multi-stream vs single-stream is threaded via [`MultiStreamArgs`] exactly
//!   as Java does; `MultiStreamLease` construction uses the unified `Lease`
//!   (with `stream_identifier`/`shard_id` set).

use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use num_bigint::BigInt;
use tokio::sync::Mutex;

use aws_sdk_kinesis::types::{ChildShard, Shard, ShardFilter, ShardFilterType};

use crate::common::{
    HashKeyRangeForLease, InitialPositionInStream, InitialPositionInStreamExtended,
    StreamIdentifier,
};
use crate::coordinator::DeletedStreamListProvider;
use crate::exceptions::KinesisClientLibError;
use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, LeaseRefresher, ShardDetector};
use crate::metrics::{self, MetricsLevel, MetricsScope};
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// `BigInteger.ZERO`.
fn min_hash_key() -> BigInt {
    BigInt::from(0)
}

/// `2^128 - 1`.
fn max_hash_key() -> BigInt {
    (BigInt::from(1) << 128) - 1
}

const RETRIES_FOR_COMPLETE_HASH_RANGE: usize = 3;
const DELAY_BETWEEN_LIST_SHARDS_MILLIS: u64 = 1000;

/// Threads `isMultiStreamMode` + `streamIdentifier` through the algorithm to
/// select multi-stream vs single-stream lease construction. Port of the Java
/// `MultiStreamArgs`.
#[derive(Debug, Clone)]
pub struct MultiStreamArgs {
    is_multi_stream_mode: bool,
    stream_identifier: Option<StreamIdentifier>,
}

impl MultiStreamArgs {
    pub fn new(is_multi_stream_mode: bool, stream_identifier: Option<StreamIdentifier>) -> Self {
        Self {
            is_multi_stream_mode,
            stream_identifier,
        }
    }
    pub fn is_multi_stream_mode(&self) -> bool {
        self.is_multi_stream_mode
    }
    pub fn stream_identifier(&self) -> Option<&StreamIdentifier> {
        self.stream_identifier.as_ref()
    }
}

/// Memoization of shards evaluated during the ancestor DFS. Port of the Java
/// `MemoizationContext`.
#[derive(Debug, Default)]
pub struct MemoizationContext {
    is_descendant_map: HashMap<String, bool>,
    should_create_lease_map: HashMap<String, bool>,
}

impl MemoizationContext {
    pub fn new() -> Self {
        Self::default()
    }
    fn is_descendant(&self, shard_id: Option<&str>) -> Option<bool> {
        shard_id.and_then(|s| self.is_descendant_map.get(s).copied())
    }
    fn set_is_descendant(&mut self, shard_id: Option<&str>, is_descendant: bool) {
        if let Some(s) = shard_id {
            self.is_descendant_map.insert(s.to_string(), is_descendant);
        }
    }
    /// Java uses `computeIfAbsent(shardId, x -> FALSE)` — returns `false` for an
    /// unknown key (and stores it).
    fn should_create_lease(&mut self, shard_id: &str) -> bool {
        *self
            .should_create_lease_map
            .entry(shard_id.to_string())
            .or_insert(false)
    }
    fn set_should_create_lease(&mut self, shard_id: &str, should: bool) {
        self.should_create_lease_map
            .insert(shard_id.to_string(), should);
    }
}

/// Selects the lease-creation strategy. Port of the Java `LeaseSynchronizer`
/// interface + its two implementations, selected by lease-table-empty.
pub enum LeaseSynchronizer {
    /// Bootstrap / cold-start: create a lease for **every** shard.
    Empty,
    /// Steady-state resharding: ancestor-DFS over open shards.
    NonEmpty {
        shard_id_to_shard_map: HashMap<String, Shard>,
        shard_id_to_child_shard_ids_map: HashMap<String, HashSet<String>>,
    },
}

/// The central resharding/backfill engine.
pub struct HierarchicalShardSyncer {
    is_multi_stream_mode: bool,
    /// Serialized stream identifier; in multi-stream mode this is the
    /// `account:name:epoch` form that [`StreamIdentifier::multi_stream_instance`]
    /// parses when recording a deleted stream.
    stream_identifier: String,
    /// Java `deletedStreamListProvider` — where a `ResourceNotFoundException`
    /// during steady-state shard sync registers the stream for the Scheduler's
    /// deleted-stream lease cleanup (multi-stream mode only).
    deleted_stream_list_provider: Option<Arc<DeletedStreamListProvider>>,
    /// Per-instance serialization of `check_and_create_lease_for_new_shards`
    /// (Java method-level `synchronized`).
    sync_lock: Mutex<()>,
}

impl Default for HierarchicalShardSyncer {
    fn default() -> Self {
        Self::new()
    }
}

impl HierarchicalShardSyncer {
    /// Single-stream mode (Java no-arg constructor).
    pub fn new() -> Self {
        Self::with_mode(false, "SingleStreamMode".to_string())
    }

    /// Multi-stream-aware constructor (Java `(boolean, String)`).
    pub fn with_mode(is_multi_stream_mode: bool, stream_identifier: String) -> Self {
        Self::with_deleted_stream_list_provider(is_multi_stream_mode, stream_identifier, None)
    }

    /// Full constructor (Java `(boolean, String, DeletedStreamListProvider)`).
    pub fn with_deleted_stream_list_provider(
        is_multi_stream_mode: bool,
        stream_identifier: String,
        deleted_stream_list_provider: Option<Arc<DeletedStreamListProvider>>,
    ) -> Self {
        Self {
            is_multi_stream_mode,
            stream_identifier,
            deleted_stream_list_provider,
            sync_lock: Mutex::new(()),
        }
    }

    // ------------------------------------------------------------------
    // Public entry points
    // ------------------------------------------------------------------

    /// Check and create leases for new shards. Fetches the shard list itself
    /// (bootstrap vs steady-state), then delegates. Returns `true` if a shard
    /// sync was performed.
    #[allow(clippy::too_many_arguments)]
    pub async fn check_and_create_lease_for_new_shards(
        &self,
        shard_detector: &dyn ShardDetector,
        lease_refresher: &dyn LeaseRefresher,
        initial_position: &InitialPositionInStreamExtended,
        scope: &mut (dyn MetricsScope + Send),
        ignore_unexpected_child_shards: bool,
        is_lease_table_empty: bool,
    ) -> Result<bool, KinesisClientLibError> {
        let _guard = self.sync_lock.lock().await;
        let consumer_id = lease_refresher
            .get_lease_table_identifier()
            .await
            .map_err(leasing_to_io)?;
        let latest_shards = if is_lease_table_empty {
            self.get_shard_list_at_initial_position(shard_detector, initial_position, &consumer_id)
                .await?
        } else {
            self.get_shard_list(shard_detector, &consumer_id).await?
        };
        self.check_and_create_lease_for_new_shards_inner(
            shard_detector,
            lease_refresher,
            initial_position,
            latest_shards,
            ignore_unexpected_child_shards,
            scope,
            is_lease_table_empty,
        )
        .await
    }

    /// Provide a pre-collected shard list to avoid calling `ListShards`.
    #[allow(clippy::too_many_arguments)]
    pub async fn check_and_create_lease_for_new_shards_with_list(
        &self,
        shard_detector: &dyn ShardDetector,
        lease_refresher: &dyn LeaseRefresher,
        initial_position: &InitialPositionInStreamExtended,
        latest_shards: Vec<Shard>,
        ignore_unexpected_child_shards: bool,
        scope: &mut (dyn MetricsScope + Send),
        is_lease_table_empty: bool,
    ) -> Result<bool, KinesisClientLibError> {
        let _guard = self.sync_lock.lock().await;
        self.check_and_create_lease_for_new_shards_inner(
            shard_detector,
            lease_refresher,
            initial_position,
            latest_shards,
            ignore_unexpected_child_shards,
            scope,
            is_lease_table_empty,
        )
        .await
    }

    #[allow(clippy::too_many_arguments)]
    async fn check_and_create_lease_for_new_shards_inner(
        &self,
        shard_detector: &dyn ShardDetector,
        lease_refresher: &dyn LeaseRefresher,
        initial_position: &InitialPositionInStreamExtended,
        latest_shards: Vec<Shard>,
        ignore_unexpected_child_shards: bool,
        scope: &mut (dyn MetricsScope + Send),
        is_lease_table_empty: bool,
    ) -> Result<bool, KinesisClientLibError> {
        if latest_shards.is_empty() {
            // Skip shard sync — no shards found.
            return Ok(false);
        }

        // back-fill stream info before creating lease.
        // TODO(port): createStreamInfo relies on the coordinator-wave
        // StreamInfoManager / StreamIdCache singletons (not yet ported); elided.

        let shard_id_to_shard_map = construct_shard_id_to_shard_map(&latest_shards);
        let shard_id_to_child_shard_ids_map =
            construct_shard_id_to_child_shard_ids_map(&shard_id_to_shard_map);
        let inconsistent_shard_ids =
            find_inconsistent_shard_ids(&shard_id_to_child_shard_ids_map, &shard_id_to_shard_map);
        if !ignore_unexpected_child_shards {
            assert_all_parent_shards_are_closed(&inconsistent_shard_ids)?;
        }

        let stream_id = shard_detector.stream_identifier().map_err(leasing_to_io)?;
        let current_leases = if self.is_multi_stream_mode {
            lease_refresher
                .list_leases_for_stream(&stream_id)
                .await
                .map_err(leasing_to_io)?
        } else {
            lease_refresher.list_leases().await.map_err(leasing_to_io)?
        };

        let multi_stream_args = MultiStreamArgs::new(self.is_multi_stream_mode, Some(stream_id));
        let lease_synchronizer = if is_lease_table_empty {
            LeaseSynchronizer::Empty
        } else {
            LeaseSynchronizer::NonEmpty {
                shard_id_to_shard_map: shard_id_to_shard_map.clone(),
                shard_id_to_child_shard_ids_map,
            }
        };

        let new_leases_to_create = determine_new_leases_to_create(
            &lease_synchronizer,
            &latest_shards,
            &current_leases,
            initial_position,
            &inconsistent_shard_ids,
            &multi_stream_args,
        );

        for lease in &new_leases_to_create {
            let start_time = current_time_millis();
            let mut success = false;
            let result = lease_refresher.create_lease_if_not_exists(lease).await;
            if result.is_ok() {
                success = true;
            }
            metrics::add_success_and_latency_with_dimension(
                scope,
                Some("CreateLease"),
                success,
                start_time,
                MetricsLevel::Detailed,
            );
            if let Some(checkpoint) = lease.checkpoint() {
                let metric_name = if checkpoint.is_sentinel_checkpoint() {
                    checkpoint.sequence_number().to_string()
                } else {
                    "SEQUENCE_NUMBER".to_string()
                };
                metrics::add_success(
                    scope,
                    Some(&format!("CreateLease_{}", metric_name)),
                    true,
                    MetricsLevel::Detailed,
                );
            }
            // Propagate the leasing error after recording metrics (Java records
            // in a `finally` then lets the exception escape the loop).
            result.map_err(leasing_to_io)?;
        }
        Ok(true)
    }

    /// Materialize a lease for a just-discovered child shard (Java
    /// `createLeaseForChildShard`).
    pub fn create_lease_for_child_shard(
        &self,
        child_shard: &ChildShard,
        stream_identifier: &StreamIdentifier,
    ) -> Result<Lease, KinesisClientLibError> {
        if self.is_multi_stream_mode {
            new_kcl_multi_stream_lease_for_child_shard(child_shard, stream_identifier)
        } else {
            new_kcl_lease_for_child_shard(child_shard)
        }
    }

    async fn get_shard_list_at_initial_position(
        &self,
        shard_detector: &dyn ShardDetector,
        initial_position: &InitialPositionInStreamExtended,
        consumer_id: &str,
    ) -> Result<Vec<Shard>, KinesisClientLibError> {
        let shard_filter = shard_filter_from_initial_position(initial_position);
        let stream_name = shard_detector
            .stream_identifier()
            .map_err(leasing_to_io)?
            .stream_name()
            .to_string();

        for _ in 0..RETRIES_FOR_COMPLETE_HASH_RANGE {
            let shards = shard_detector
                .list_shards_with_filter_for_consumer(shard_filter.clone(), consumer_id)
                .await;

            let shards = match shards {
                Ok(s) => s,
                // A transient not-ACTIVE/UPDATING state maps to the same IO
                // error Java throws for a `null` shard list.
                Err(_) => {
                    return Err(KinesisClientLibError::io(format!(
                        "Stream {} is not in ACTIVE OR UPDATING state - will retry getting the shard list.",
                        stream_name
                    )))
                }
            };

            if is_hash_range_of_shards_complete(shards.clone())? {
                return Ok(shards);
            }

            tokio::time::sleep(std::time::Duration::from_millis(
                DELAY_BETWEEN_LIST_SHARDS_MILLIS,
            ))
            .await;
        }

        Err(KinesisClientLibError::io(format!(
            "Hash range of shards returned for {} was incomplete after {} retries.",
            stream_name, RETRIES_FOR_COMPLETE_HASH_RANGE
        )))
    }

    async fn get_shard_list(
        &self,
        shard_detector: &dyn ShardDetector,
        consumer_id: &str,
    ) -> Result<Vec<Shard>, KinesisClientLibError> {
        // Fallback to existing behavior for backward compatibility. Java
        // catches ResourceNotFoundException: the deleted stream is recorded in
        // the DeletedStreamListProvider (multi-stream mode) and an EMPTY shard
        // list is returned, so the sync pass skips gracefully ("no shards
        // found") instead of failing. Any other error is an IO error.
        match shard_detector
            .list_shards_without_consuming_resource_not_found_exception_for_consumer(consumer_id)
            .await
        {
            Ok(shards) => Ok(shards),
            Err(e) if is_resource_not_found(&e) => {
                if let Some(provider) = self
                    .deleted_stream_list_provider
                    .as_ref()
                    .filter(|_| self.is_multi_stream_mode)
                {
                    provider.add(StreamIdentifier::multi_stream_instance(
                        &self.stream_identifier,
                    ));
                }
                Ok(Vec::new())
            }
            Err(_) => Err(KinesisClientLibError::io(format!(
                "Stream {} is not in ACTIVE OR UPDATING state - will retry getting the shard list.",
                shard_detector
                    .stream_identifier()
                    .map(|s| s.stream_name().to_string())
                    .unwrap_or_default()
            ))),
        }
    }
}

/// Whether a detector error is the propagated Kinesis `ResourceNotFoundException`.
///
/// Java catches the raw unchecked `ResourceNotFoundException` that
/// `listShardsWithoutConsumingResourceNotFoundException` lets through; the Rust
/// detector wraps it in a [`LeasingError::Dependency`] whose source is the SDK
/// `ListShardsError` — unwrap and check.
fn is_resource_not_found(err: &LeasingError) -> bool {
    let LeasingError::Dependency {
        source: Some(source),
        ..
    } = err
    else {
        return false;
    };
    source
        .downcast_ref::<aws_sdk_kinesis::operation::list_shards::ListShardsError>()
        .is_some_and(|e| e.is_resource_not_found_exception())
}

// ----------------------------------------------------------------------------
// Free functions (Java static helpers) — public(crate) for testing.
// ----------------------------------------------------------------------------

fn current_time_millis() -> i64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

/// Map a leasing error into the IO/checked family Java's shard-syncer surface uses.
fn leasing_to_io(e: LeasingError) -> KinesisClientLibError {
    KinesisClientLibError::io_caused_by(e.message().to_string(), Box::new(e))
}

fn get_shard_id_from_lease(lease: &Lease, multi_stream_args: &MultiStreamArgs) -> String {
    if multi_stream_args.is_multi_stream_mode() {
        lease
            .shard_id()
            .expect("multi-stream lease has a shard id")
            .to_string()
    } else {
        lease
            .lease_key()
            .expect("lease has a lease key")
            .to_string()
    }
}

/// Detects a race condition between paginated shard fetches and a reshard.
pub fn assert_all_parent_shards_are_closed(
    inconsistent_shard_ids: &HashSet<String>,
) -> Result<(), KinesisClientLibError> {
    if !inconsistent_shard_ids.is_empty() {
        let mut ids: Vec<&String> = inconsistent_shard_ids.iter().collect();
        ids.sort();
        let joined = ids.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(" ");
        return Err(KinesisClientLibError::io(format!(
            "{} open child shards ({}) are inconsistent. This can happen due to a race condition between describeStream and a reshard operation.",
            inconsistent_shard_ids.len(),
            joined
        )));
    }
    Ok(())
}

/// Construct the set of inconsistent shards: open shards with non-closed
/// ancestor parent(s). Port of `findInconsistentShardIds`.
pub fn find_inconsistent_shard_ids(
    shard_id_to_child_shard_ids_map: &HashMap<String, HashSet<String>>,
    shard_id_to_shard_map: &HashMap<String, Shard>,
) -> HashSet<String> {
    let mut result = HashSet::new();
    for (parent_id, children) in shard_id_to_child_shard_ids_map {
        // Java: key == null OR the parent's endingSequenceNumber is null.
        let parent_open = shard_id_to_shard_map
            .get(parent_id)
            .map(|shard| {
                shard
                    .sequence_number_range()
                    .and_then(|r| r.ending_sequence_number())
                    .is_none()
            })
            .unwrap_or(true);
        if parent_open {
            for child in children {
                result.insert(child.clone());
            }
        }
    }
    result
}

/// Construct `shardId -> set of child shard ids`. Port of
/// `constructShardIdToChildShardIdsMap`.
pub fn construct_shard_id_to_child_shard_ids_map(
    shard_id_to_shard_map: &HashMap<String, Shard>,
) -> HashMap<String, HashSet<String>> {
    let mut map: HashMap<String, HashSet<String>> = HashMap::new();
    for (shard_id, shard) in shard_id_to_shard_map {
        if let Some(parent_id) = non_empty(shard.parent_shard_id()) {
            if shard_id_to_shard_map.contains_key(parent_id) {
                map.entry(parent_id.to_string())
                    .or_default()
                    .insert(shard_id.clone());
            }
        }
        if let Some(adjacent_id) = non_empty(shard.adjacent_parent_shard_id()) {
            if shard_id_to_shard_map.contains_key(adjacent_id) {
                map.entry(adjacent_id.to_string())
                    .or_default()
                    .insert(shard_id.clone());
            }
        }
    }
    map
}

/// Construct a `shardId -> Shard` map. Port of `constructShardIdToShardMap`.
pub fn construct_shard_id_to_shard_map(shards: &[Shard]) -> HashMap<String, Shard> {
    shards
        .iter()
        .map(|s| (s.shard_id().to_string(), s.clone()))
        .collect()
}

/// Return all open shards (no ending sequence number). Port of `getOpenShards`.
pub fn get_open_shards(all_shards: &[Shard]) -> Vec<Shard> {
    all_shards
        .iter()
        .filter(|shard| {
            shard
                .sequence_number_range()
                .and_then(|r| r.ending_sequence_number())
                .is_none()
        })
        .cloned()
        .collect()
}

/// Parent shard ids (present in the map). Port of `getParentShardIds`.
pub fn get_parent_shard_ids(
    shard: &Shard,
    shard_id_to_shard_map: &HashMap<String, Shard>,
) -> HashSet<String> {
    let mut parents = HashSet::new();
    if let Some(parent_id) = non_empty(shard.parent_shard_id()) {
        if shard_id_to_shard_map.contains_key(parent_id) {
            parents.insert(parent_id.to_string());
        }
    }
    if let Some(adjacent_id) = non_empty(shard.adjacent_parent_shard_id()) {
        if shard_id_to_shard_map.contains_key(adjacent_id) {
            parents.insert(adjacent_id.to_string());
        }
    }
    parents
}

/// Java treats null AND empty strings as "no parent" (`StringUtils.isNotEmpty`).
fn non_empty(s: Option<&str>) -> Option<&str> {
    match s {
        Some(v) if !v.is_empty() => Some(v),
        _ => None,
    }
}

fn shard_filter_from_initial_position(pos: &InitialPositionInStreamExtended) -> ShardFilter {
    let builder = ShardFilter::builder();
    let builder = match pos.initial_position_in_stream() {
        InitialPositionInStream::Latest => builder.r#type(ShardFilterType::AtLatest),
        InitialPositionInStream::TrimHorizon => builder.r#type(ShardFilterType::AtTrimHorizon),
        InitialPositionInStream::AtTimestamp => {
            let ts = pos.timestamp().expect("AT_TIMESTAMP has a timestamp");
            let smithy_ts = aws_smithy_types::DateTime::from_millis(ts.timestamp_millis());
            builder
                .r#type(ShardFilterType::AtTimestamp)
                .timestamp(smithy_ts)
        }
    };
    builder.build().expect("ShardFilter with a type is valid")
}

/// Validate that a shard list forms a contiguous hash-range partition from `0`
/// to `2^128-1`. Port of `isHashRangeOfShardsComplete`.
///
/// # Errors
/// Returns [`KinesisClientLibError::Io`] if the list is empty (Java
/// `IllegalStateException`, mapped to the IO family used by callers).
pub fn is_hash_range_of_shards_complete(
    mut shards: Vec<Shard>,
) -> Result<bool, KinesisClientLibError> {
    if shards.is_empty() {
        return Err(KinesisClientLibError::io(
            "No shards found when attempting to validate complete hash range.",
        ));
    }

    shards.sort_by(|a, b| {
        let ha: BigInt = starting_hash_key(a);
        let hb: BigInt = starting_hash_key(b);
        ha.cmp(&hb)
    });

    let first_start = starting_hash_key(&shards[0]);
    let last_end = ending_hash_key(&shards[shards.len() - 1]);
    if first_start != min_hash_key() || last_end != max_hash_key() {
        return Ok(false);
    }

    if shards.len() > 1 {
        for i in 1..shards.len() {
            let start_of_hole = ending_hash_key(&shards[i - 1]);
            let end_of_hole = starting_hash_key(&shards[i]);
            if end_of_hole - start_of_hole != BigInt::from(1) {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

fn starting_hash_key(shard: &Shard) -> BigInt {
    shard
        .hash_key_range()
        .expect("shard has a hash key range")
        .starting_hash_key()
        .parse()
        .expect("startingHashKey is an integer")
}

fn ending_hash_key(shard: &Shard) -> BigInt {
    shard
        .hash_key_range()
        .expect("shard has a hash key range")
        .ending_hash_key()
        .parse()
        .expect("endingHashKey is an integer")
}

fn convert_to_checkpoint(
    position: &InitialPositionInStreamExtended,
) -> Option<ExtendedSequenceNumber> {
    match position.initial_position_in_stream() {
        InitialPositionInStream::TrimHorizon => Some(ExtendedSequenceNumber::trim_horizon()),
        InitialPositionInStream::Latest => Some(ExtendedSequenceNumber::latest()),
        InitialPositionInStream::AtTimestamp => Some(ExtendedSequenceNumber::at_timestamp()),
    }
}

// ---- lease construction helpers ----

fn new_kcl_lease(shard: &Shard) -> Lease {
    let mut lease = Lease::default();
    lease.set_lease_key(shard.shard_id());
    let mut parents = Vec::new();
    if let Some(p) = non_empty(shard.parent_shard_id()) {
        parents.push(p.to_string());
    }
    if let Some(p) = non_empty(shard.adjacent_parent_shard_id()) {
        parents.push(p.to_string());
    }
    lease.set_parent_shard_ids(parents);
    lease.set_owner_switches_since_checkpoint(0);
    lease.set_hash_key_range(HashKeyRangeForLease::from_hash_key_range(
        shard.hash_key_range().expect("shard has a hash key range"),
    ));
    lease
}

fn new_kcl_multi_stream_lease(shard: &Shard, stream_identifier: &StreamIdentifier) -> Lease {
    let serialized = stream_identifier.serialize();
    let mut lease = Lease::default();
    lease.set_lease_key(Lease::multi_stream_lease_key(&serialized, shard.shard_id()));
    let mut parents = Vec::new();
    if let Some(p) = non_empty(shard.parent_shard_id()) {
        parents.push(p.to_string());
    }
    if let Some(p) = non_empty(shard.adjacent_parent_shard_id()) {
        parents.push(p.to_string());
    }
    lease.set_parent_shard_ids(parents);
    lease.set_owner_switches_since_checkpoint(0);
    lease.set_stream_identifier(serialized);
    lease.set_shard_id(shard.shard_id());
    lease.set_hash_key_range(HashKeyRangeForLease::from_hash_key_range(
        shard.hash_key_range().expect("shard has a hash key range"),
    ));
    lease
}

fn new_kcl_lease_for_child_shard(child_shard: &ChildShard) -> Result<Lease, KinesisClientLibError> {
    let mut lease = Lease::default();
    lease.set_lease_key(child_shard.shard_id());
    if !child_shard.parent_shards().is_empty() {
        lease.set_parent_shard_ids(child_shard.parent_shards().iter().cloned());
    } else {
        return Err(KinesisClientLibError::invalid_state(format!(
            "Unable to populate new lease for child shard {} because parent shards cannot be found.",
            child_shard.shard_id()
        )));
    }
    lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
    lease.set_owner_switches_since_checkpoint(0);
    lease.set_hash_key_range(HashKeyRangeForLease::from_hash_key_range(
        child_shard
            .hash_key_range()
            .expect("child shard has a hash key range"),
    ));
    Ok(lease)
}

fn new_kcl_multi_stream_lease_for_child_shard(
    child_shard: &ChildShard,
    stream_identifier: &StreamIdentifier,
) -> Result<Lease, KinesisClientLibError> {
    let serialized = stream_identifier.serialize();
    let mut lease = Lease::default();
    lease.set_lease_key(Lease::multi_stream_lease_key(
        &serialized,
        child_shard.shard_id(),
    ));
    if !child_shard.parent_shards().is_empty() {
        lease.set_parent_shard_ids(child_shard.parent_shards().iter().cloned());
    } else {
        return Err(KinesisClientLibError::invalid_state(format!(
            "Unable to populate new lease for child shard {} because parent shards cannot be found.",
            child_shard.shard_id()
        )));
    }
    lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
    lease.set_owner_switches_since_checkpoint(0);
    lease.set_stream_identifier(serialized);
    lease.set_shard_id(child_shard.shard_id());
    lease.set_hash_key_range(HashKeyRangeForLease::from_hash_key_range(
        child_shard
            .hash_key_range()
            .expect("child shard has a hash key range"),
    ));
    Ok(lease)
}

// ---- determineNewLeasesToCreate + strategies ----

/// Determine new leases to create (delegates to the selected strategy). Port of
/// `determineNewLeasesToCreate`.
pub fn determine_new_leases_to_create(
    lease_synchronizer: &LeaseSynchronizer,
    shards: &[Shard],
    current_leases: &[Lease],
    initial_position: &InitialPositionInStreamExtended,
    inconsistent_shard_ids: &HashSet<String>,
    multi_stream_args: &MultiStreamArgs,
) -> Vec<Lease> {
    match lease_synchronizer {
        LeaseSynchronizer::Empty => {
            determine_new_leases_empty(shards, initial_position, multi_stream_args)
        }
        LeaseSynchronizer::NonEmpty { .. } => determine_new_leases_non_empty(
            shards,
            current_leases,
            initial_position,
            inconsistent_shard_ids,
            multi_stream_args,
        ),
    }
}

/// `EmptyLeaseTableSynchronizer`: create a lease for **every** shard.
fn determine_new_leases_empty(
    shards: &[Shard],
    initial_position: &InitialPositionInStreamExtended,
    multi_stream_args: &MultiStreamArgs,
) -> Vec<Lease> {
    let mut shard_id_to_new_lease_map: HashMap<String, Lease> = HashMap::new();
    for shard in shards {
        let shard_id = shard.shard_id().to_string();
        let mut lease = if multi_stream_args.is_multi_stream_mode() {
            new_kcl_multi_stream_lease(shard, multi_stream_args.stream_identifier().unwrap())
        } else {
            new_kcl_lease(shard)
        };
        if let Some(cp) = convert_to_checkpoint(initial_position) {
            lease.set_checkpoint(cp);
        }
        shard_id_to_new_lease_map.insert(shard_id, lease);
    }

    let shard_id_to_shard_map = construct_shard_id_to_shard_map(shards);
    let mut new_leases: Vec<Lease> = shard_id_to_new_lease_map.into_values().collect();
    sort_leases_by_starting_sequence_number(
        &mut new_leases,
        &shard_id_to_shard_map,
        multi_stream_args,
    );
    new_leases
}

/// `NonEmptyLeaseTableSynchronizer`: ancestor-DFS over open shards.
fn determine_new_leases_non_empty(
    shards: &[Shard],
    current_leases: &[Lease],
    initial_position: &InitialPositionInStreamExtended,
    inconsistent_shard_ids: &HashSet<String>,
    multi_stream_args: &MultiStreamArgs,
) -> Vec<Lease> {
    let mut shard_id_to_new_lease_map: HashMap<String, Lease> = HashMap::new();
    let shard_id_to_shard_map = construct_shard_id_to_shard_map(shards);

    let shard_ids_of_current_leases: HashSet<String> = current_leases
        .iter()
        .map(|lease| get_shard_id_from_lease(lease, multi_stream_args))
        .collect();

    let open_shards = get_open_shards(shards);
    let mut memoization_context = MemoizationContext::new();

    for shard in &open_shards {
        let shard_id = shard.shard_id().to_string();
        // Skip shards that already have a lease or are inconsistent children.
        if shard_ids_of_current_leases.contains(&shard_id)
            || inconsistent_shard_ids.contains(&shard_id)
        {
            continue;
        }
        let is_descendant = check_if_descendant_and_add_new_leases_for_ancestors(
            Some(&shard_id),
            initial_position,
            &shard_ids_of_current_leases,
            &shard_id_to_shard_map,
            &mut shard_id_to_new_lease_map,
            &mut memoization_context,
            multi_stream_args,
        );

        if !is_descendant {
            let mut new_lease = if multi_stream_args.is_multi_stream_mode() {
                new_kcl_multi_stream_lease(shard, multi_stream_args.stream_identifier().unwrap())
            } else {
                new_kcl_lease(shard)
            };
            if let Some(cp) = convert_to_checkpoint(initial_position) {
                new_lease.set_checkpoint(cp);
            }
            shard_id_to_new_lease_map.insert(shard_id, new_lease);
        }
    }

    let mut new_leases: Vec<Lease> = shard_id_to_new_lease_map.into_values().collect();
    sort_leases_by_starting_sequence_number(
        &mut new_leases,
        &shard_id_to_shard_map,
        multi_stream_args,
    );
    new_leases
}

/// The central memoized ancestor DFS. Port of
/// `checkIfDescendantAndAddNewLeasesForAncestors`.
#[allow(clippy::too_many_arguments)]
pub fn check_if_descendant_and_add_new_leases_for_ancestors(
    shard_id: Option<&str>,
    initial_position: &InitialPositionInStreamExtended,
    shard_ids_of_current_leases: &HashSet<String>,
    shard_id_to_shard_map_of_all_kinesis_shards: &HashMap<String, Shard>,
    shard_id_to_lease_map_of_new_shards: &mut HashMap<String, Lease>,
    memoization_context: &mut MemoizationContext,
    multi_stream_args: &MultiStreamArgs,
) -> bool {
    if let Some(previous) = memoization_context.is_descendant(shard_id) {
        return previous;
    }

    let mut is_descendant = false;
    let mut descendant_parent_shard_ids: HashSet<String> = HashSet::new();

    if let Some(shard_id) = shard_id {
        if let Some(shard) = shard_id_to_shard_map_of_all_kinesis_shards.get(shard_id) {
            if shard_ids_of_current_leases.contains(shard_id) {
                // Descendant of a current shard.
                is_descendant = true;
            } else {
                let shard = shard.clone();
                let parent_shard_ids =
                    get_parent_shard_ids(&shard, shard_id_to_shard_map_of_all_kinesis_shards);
                for parent_shard_id in &parent_shard_ids {
                    let is_parent_descendant = check_if_descendant_and_add_new_leases_for_ancestors(
                        Some(parent_shard_id),
                        initial_position,
                        shard_ids_of_current_leases,
                        shard_id_to_shard_map_of_all_kinesis_shards,
                        shard_id_to_lease_map_of_new_shards,
                        memoization_context,
                        multi_stream_args,
                    );
                    if is_parent_descendant
                        || memoization_context.should_create_lease(parent_shard_id)
                    {
                        is_descendant = true;
                        descendant_parent_shard_ids.insert(parent_shard_id.clone());
                    }
                }

                if is_descendant {
                    for parent_shard_id in &parent_shard_ids {
                        if !shard_ids_of_current_leases.contains(parent_shard_id) {
                            let lease_exists =
                                shard_id_to_lease_map_of_new_shards.contains_key(parent_shard_id);

                            if !lease_exists
                                && (memoization_context.should_create_lease(parent_shard_id)
                                    || !descendant_parent_shard_ids.contains(parent_shard_id))
                            {
                                let parent_shard = shard_id_to_shard_map_of_all_kinesis_shards
                                    .get(parent_shard_id)
                                    .expect("parent shard present");
                                let lease = if multi_stream_args.is_multi_stream_mode() {
                                    new_kcl_multi_stream_lease(
                                        parent_shard,
                                        multi_stream_args.stream_identifier().unwrap(),
                                    )
                                } else {
                                    new_kcl_lease(parent_shard)
                                };
                                shard_id_to_lease_map_of_new_shards
                                    .insert(parent_shard_id.clone(), lease);
                            }

                            if let Some(lease) =
                                shard_id_to_lease_map_of_new_shards.get_mut(parent_shard_id)
                            {
                                if descendant_parent_shard_ids.contains(parent_shard_id)
                                    && initial_position.initial_position_in_stream()
                                        != InitialPositionInStream::AtTimestamp
                                {
                                    lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
                                } else if let Some(cp) = convert_to_checkpoint(initial_position) {
                                    lease.set_checkpoint(cp);
                                }
                            }
                        }
                    }
                } else {
                    // Not a descendant, but should be flagged so a sibling
                    // traversal can pick up shared ancestors.
                    let pos = initial_position.initial_position_in_stream();
                    if pos == InitialPositionInStream::TrimHorizon
                        || pos == InitialPositionInStream::AtTimestamp
                    {
                        memoization_context.set_should_create_lease(shard_id, true);
                    }
                }
            }
        }
    }

    memoization_context.set_is_descendant(shard_id, is_descendant);
    is_descendant
}

fn sort_leases_by_starting_sequence_number(
    leases: &mut [Lease],
    shard_id_to_shard_map: &HashMap<String, Shard>,
    multi_stream_args: &MultiStreamArgs,
) {
    leases.sort_by(|l1, l2| {
        let shard_id1 = get_shard_id_from_lease(l1, multi_stream_args);
        let shard_id2 = get_shard_id_from_lease(l2, multi_stream_args);
        let shard1 = shard_id_to_shard_map.get(&shard_id1);
        let shard2 = shard_id_to_shard_map.get(&shard_id2);

        let mut result = std::cmp::Ordering::Equal;
        if let (Some(s1), Some(s2)) = (shard1, shard2) {
            let seq1: BigInt = s1
                .sequence_number_range()
                .expect("shard has a sequence number range")
                .starting_sequence_number()
                .parse()
                .expect("starting sequence number is an integer");
            let seq2: BigInt = s2
                .sequence_number_range()
                .expect("shard has a sequence number range")
                .starting_sequence_number()
                .parse()
                .expect("starting sequence number is an integer");
            result = seq1.cmp(&seq2);
        }
        if result == std::cmp::Ordering::Equal {
            result = shard_id1.cmp(&shard_id2);
        }
        result
    });
}

#[cfg(test)]
mod tests;
