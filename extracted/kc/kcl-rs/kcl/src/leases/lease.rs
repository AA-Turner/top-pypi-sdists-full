//! Port of `software.amazon.kinesis.leases.Lease` **and**
//! `software.amazon.kinesis.leases.MultiStreamLease`.
//!
//! # Unified `Lease` model (no inheritance)
//!
//! Java has `MultiStreamLease extends Lease`, adding a `streamIdentifier` and a
//! `shardId`, and downcasts pervasively via `instanceof` / `validateAndCast`.
//! Rust has no inheritance, so the two classes are **unified into a single
//! [`Lease`] struct** carrying all base fields plus optional multi-stream
//! fields ([`Lease::stream_identifier`]-style accessors returning
//! `Option<&str>`). A lease is "multi-stream" iff it has a stream identifier
//! ([`Lease::is_multi_stream`]); the Java `instanceof MultiStreamLease` checks
//! become `is_multi_stream()`, and `MultiStreamLease.validateAndCast` becomes
//! [`Lease::validate_multi_stream`].
//!
//! The multi-stream `stream_identifier` is stored as a **serialized `String`**
//! (matching the Java `MultiStreamLease.streamIdentifier: String` field and the
//! `ShardInfo.streamIdentifierSerOpt` form), not a `common::StreamIdentifier`.
//!
//! # Equality / hashing
//!
//! Java's `@EqualsAndHashCode(exclude = {...})` on `Lease` and
//! `@EqualsAndHashCode(callSuper = true)` on `MultiStreamLease` are
//! behaviorally load-bearing (they define the lease-identity / dedup contract).
//! They are hand-implemented here over the **included** fields only:
//! `lease_key`, `lease_owner`, `lease_counter`, `checkpoint`,
//! `pending_checkpoint`, `owner_switches_since_checkpoint`, `parent_shard_ids`,
//! `hash_key_range_for_lease`, **plus** `stream_identifier` and `shard_id`
//! (the multi-stream additions). The excluded fields are `concurrency_token`,
//! `last_counter_increment_nanos`, `child_shard_ids`, `pending_checkpoint_state`,
//! `is_marked_for_lease_steal`, `throughput_kbps`, `checkpoint_owner`,
//! `checkpoint_owner_timeout_timestamp_millis`, and `is_expired_or_unassigned`.
//!
//! Note `parent_shard_ids` and `child_shard_ids` are `HashSet<String>`
//! (matching Java), so equality over `parent_shard_ids` is order-independent.

use std::collections::HashSet;
use std::hash::{Hash, Hasher};

use uuid::Uuid;

use crate::common::HashKeyRangeForLease;
use crate::leases::EntityType;
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// See `System.nanoTime` javadoc: `nanoTime` values can wrap on overflow, in
/// which case the difference between two values is very large. We treat leases
/// older than a year as expired. `365 * 24 * 60 * 60 * 1_000_000_000`.
const MAX_ABS_AGE_NANOS: i64 = 365 * 24 * 60 * 60 * 1_000_000_000;

/// Data pertaining to a lease — the fundamental unit of the leasing protocol.
///
/// Distributed systems use leases to partition work across a fleet of workers.
/// Each unit of work (identified by a `lease_key`) has a corresponding `Lease`.
/// Every worker contends for all leases; only one worker successfully takes
/// each one, and holds it until it stops processing or fails.
///
/// This type is **heavily mutated** by the (later) lease renewer/taker, so
/// fields are owned and exposed through getters + setters rather than made
/// immutable.
#[derive(Debug, Clone)]
pub struct Lease {
    // --- included in equals/hashCode ---
    lease_key: Option<String>,
    lease_owner: Option<String>,
    lease_counter: i64,
    checkpoint: Option<ExtendedSequenceNumber>,
    pending_checkpoint: Option<ExtendedSequenceNumber>,
    owner_switches_since_checkpoint: i64,
    parent_shard_ids: HashSet<String>,
    hash_key_range_for_lease: Option<HashKeyRangeForLease>,
    // multi-stream additions (also included in equals/hashCode via callSuper)
    stream_identifier: Option<String>,
    shard_id: Option<String>,

    // --- excluded from equals/hashCode ---
    concurrency_token: Option<Uuid>,
    last_counter_increment_nanos: Option<i64>,
    child_shard_ids: HashSet<String>,
    pending_checkpoint_state: Option<Vec<u8>>,
    is_marked_for_lease_steal: bool,
    is_expired_or_unassigned: bool,
    throughput_kbps: Option<f64>,
    checkpoint_owner: Option<String>,
    checkpoint_owner_timeout_timestamp_millis: Option<i64>,
}

impl Default for Lease {
    /// Java `@NoArgsConstructor`: `lease_counter` and
    /// `owner_switches_since_checkpoint` default to `0`, sets are empty,
    /// everything else is unset/`false`.
    fn default() -> Self {
        Self {
            lease_key: None,
            lease_owner: None,
            lease_counter: 0,
            checkpoint: None,
            pending_checkpoint: None,
            owner_switches_since_checkpoint: 0,
            parent_shard_ids: HashSet::new(),
            hash_key_range_for_lease: None,
            stream_identifier: None,
            shard_id: None,
            concurrency_token: None,
            last_counter_increment_nanos: None,
            child_shard_ids: HashSet::new(),
            pending_checkpoint_state: None,
            is_marked_for_lease_steal: false,
            is_expired_or_unassigned: false,
            throughput_kbps: None,
            checkpoint_owner: None,
            checkpoint_owner_timeout_timestamp_millis: None,
        }
    }
}

impl PartialEq for Lease {
    fn eq(&self, other: &Self) -> bool {
        self.lease_key == other.lease_key
            && self.lease_owner == other.lease_owner
            && self.lease_counter == other.lease_counter
            && self.checkpoint == other.checkpoint
            && self.pending_checkpoint == other.pending_checkpoint
            && self.owner_switches_since_checkpoint == other.owner_switches_since_checkpoint
            && self.parent_shard_ids == other.parent_shard_ids
            && self.hash_key_range_for_lease == other.hash_key_range_for_lease
            && self.stream_identifier == other.stream_identifier
            && self.shard_id == other.shard_id
    }
}

impl Eq for Lease {}

impl Hash for Lease {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.lease_key.hash(state);
        self.lease_owner.hash(state);
        self.lease_counter.hash(state);
        self.checkpoint.hash(state);
        self.pending_checkpoint.hash(state);
        self.owner_switches_since_checkpoint.hash(state);
        // HashSet has no Hash; combine element hashes order-independently via XOR.
        let mut parents_hash: u64 = 0;
        for p in &self.parent_shard_ids {
            let mut h = std::collections::hash_map::DefaultHasher::new();
            p.hash(&mut h);
            parents_hash ^= h.finish();
        }
        parents_hash.hash(state);
        self.hash_key_range_for_lease.hash(state);
        self.stream_identifier.hash(state);
        self.shard_id.hash(state);
    }
}

impl Lease {
    /// Full constructor mirroring the 12-arg Java `Lease(...)` constructor.
    ///
    /// `parent_shard_ids` / `child_shard_ids` are copied into the internal sets
    /// (Java adds them into fresh `HashSet`s). Produces a single-stream lease.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        lease_key: Option<String>,
        lease_owner: Option<String>,
        lease_counter: i64,
        concurrency_token: Option<Uuid>,
        last_counter_increment_nanos: Option<i64>,
        checkpoint: Option<ExtendedSequenceNumber>,
        pending_checkpoint: Option<ExtendedSequenceNumber>,
        owner_switches_since_checkpoint: i64,
        parent_shard_ids: HashSet<String>,
        child_shard_ids: HashSet<String>,
        pending_checkpoint_state: Option<Vec<u8>>,
        hash_key_range_for_lease: Option<HashKeyRangeForLease>,
    ) -> Self {
        Self {
            lease_key,
            lease_owner,
            lease_counter,
            concurrency_token,
            last_counter_increment_nanos,
            checkpoint,
            pending_checkpoint,
            owner_switches_since_checkpoint,
            parent_shard_ids,
            child_shard_ids,
            pending_checkpoint_state,
            hash_key_range_for_lease,
            is_marked_for_lease_steal: false,
            ..Default::default()
        }
    }

    /// Construct a multi-stream lease from a base lease plus its stream
    /// identifier (serialized) and shard id. Mirrors constructing a
    /// `MultiStreamLease` then setting its two fields.
    pub fn new_multi_stream(
        mut base: Lease,
        stream_identifier: impl Into<String>,
        shard_id: impl Into<String>,
    ) -> Self {
        base.stream_identifier = Some(stream_identifier.into());
        base.shard_id = Some(shard_id.into());
        base
    }

    // ---- Entity ----

    /// Java `getEntityType()` — a `Lease` is always [`EntityType::Lease`].
    pub fn entity_type(&self) -> EntityType {
        EntityType::Lease
    }

    // ---- getters (Lombok fluent @Getter) ----

    pub fn lease_key(&self) -> Option<&str> {
        self.lease_key.as_deref()
    }
    pub fn lease_owner(&self) -> Option<&str> {
        self.lease_owner.as_deref()
    }
    pub fn lease_counter(&self) -> i64 {
        self.lease_counter
    }
    pub fn concurrency_token(&self) -> Option<Uuid> {
        self.concurrency_token
    }
    pub fn last_counter_increment_nanos(&self) -> Option<i64> {
        self.last_counter_increment_nanos
    }
    pub fn checkpoint(&self) -> Option<&ExtendedSequenceNumber> {
        self.checkpoint.as_ref()
    }
    pub fn pending_checkpoint(&self) -> Option<&ExtendedSequenceNumber> {
        self.pending_checkpoint.as_ref()
    }
    pub fn pending_checkpoint_state(&self) -> Option<&[u8]> {
        self.pending_checkpoint_state.as_deref()
    }
    pub fn is_marked_for_lease_steal(&self) -> bool {
        self.is_marked_for_lease_steal
    }
    pub fn is_expired_or_unassigned(&self) -> bool {
        self.is_expired_or_unassigned
    }
    pub fn throughput_kbps(&self) -> Option<f64> {
        self.throughput_kbps
    }
    pub fn checkpoint_owner(&self) -> Option<&str> {
        self.checkpoint_owner.as_deref()
    }
    pub fn checkpoint_owner_timeout_timestamp_millis(&self) -> Option<i64> {
        self.checkpoint_owner_timeout_timestamp_millis
    }
    pub fn owner_switches_since_checkpoint(&self) -> i64 {
        self.owner_switches_since_checkpoint
    }
    pub fn hash_key_range_for_lease(&self) -> Option<&HashKeyRangeForLease> {
        self.hash_key_range_for_lease.as_ref()
    }

    /// Serialized stream identifier (multi-stream only). Java
    /// `MultiStreamLease.streamIdentifier()`.
    pub fn stream_identifier(&self) -> Option<&str> {
        self.stream_identifier.as_deref()
    }
    /// Shard id (multi-stream only). Java `MultiStreamLease.shardId()`.
    pub fn shard_id(&self) -> Option<&str> {
        self.shard_id.as_deref()
    }

    /// Whether this is a multi-stream lease (Java `instanceof MultiStreamLease`).
    pub fn is_multi_stream(&self) -> bool {
        self.stream_identifier.is_some()
    }

    /// Defensive copy of the parent shard IDs (Java `parentShardIds()`).
    pub fn parent_shard_ids(&self) -> HashSet<String> {
        self.parent_shard_ids.clone()
    }

    /// Defensive copy of the child shard IDs (Java `childShardIds()`).
    pub fn child_shard_ids(&self) -> HashSet<String> {
        self.child_shard_ids.clone()
    }

    // ---- expiry / availability ----

    /// Whether the lease is ready to be taken: unassigned OR expired.
    pub fn is_available(&self, lease_duration_nanos: i64, as_of_nanos: i64) -> bool {
        self.is_unassigned() || self.is_expired(lease_duration_nanos, as_of_nanos)
    }

    /// Whether the lease is expired as of the given time.
    ///
    /// Treats `|as_of - last_increment| > 365 days` as always-expired (the
    /// `System.nanoTime` overflow guard); otherwise `age > lease_duration`.
    pub fn is_expired(&self, lease_duration_nanos: i64, as_of_nanos: i64) -> bool {
        match self.last_counter_increment_nanos {
            None => true,
            Some(last) => {
                let age = as_of_nanos.wrapping_sub(last);
                if age.wrapping_abs() > MAX_ABS_AGE_NANOS {
                    true
                } else {
                    age > lease_duration_nanos
                }
            }
        }
    }

    fn is_unassigned(&self) -> bool {
        self.lease_owner.is_none()
    }

    /// Whether the checkpoint owner is set, indicating a requested shutdown.
    pub fn shutdown_requested(&self) -> bool {
        self.checkpoint_owner.is_some()
    }

    /// Whether the lease should be blocked on a pending checkpoint.
    ///
    /// Ports the Java De Morgan boolean gate verbatim. We DON'T block if the
    /// lease is expired/unassigned, is `SHARD_END`, is not requested for
    /// shutdown, or its shutdown deadline has passed.
    ///
    /// Java relies on `checkpointOwnerTimeoutTimestampMillis` being non-null
    /// whenever `shutdownRequested()` is true (else an unboxing NPE). We model
    /// it as `Option<i64>`; when it is `None` we treat the deadline term as
    /// `false` (i.e. deadline not yet passed) so the boolean structure matches
    /// the non-null Java path.
    pub fn blocked_on_pending_checkpoint(&self, current_time_millis: i64) -> bool {
        let shard_end = self.checkpoint.as_ref() == Some(&ExtendedSequenceNumber::shard_end());
        let deadline_passed = match self.checkpoint_owner_timeout_timestamp_millis {
            Some(deadline) => current_time_millis - deadline >= 0,
            None => false,
        };
        !(self.is_expired_or_unassigned
            || shard_end
            || !self.shutdown_requested()
            || deadline_passed)
    }

    /// Whether the lease is eligible for graceful shutdown: still assigned (not
    /// expired), not `SHARD_END`, and not already requested for shutdown.
    pub fn is_eligible_for_graceful_shutdown(&self) -> bool {
        let shard_end = self.checkpoint.as_ref() == Some(&ExtendedSequenceNumber::shard_end());
        !self.is_expired_or_unassigned && !shard_end && !self.shutdown_requested()
    }

    /// The actual owner: the checkpoint owner if set (during graceful-shutdown
    /// handoff), else the lease owner.
    pub fn actual_owner(&self) -> Option<&str> {
        match &self.checkpoint_owner {
            Some(o) => Some(o),
            None => self.lease_owner.as_deref(),
        }
    }

    // ---- update / copy ----

    /// Update this lease's mutable, application-specific fields from another
    /// lease. Does not update leasing-library-internal fields (`lease_key`,
    /// `lease_owner`, `lease_counter`).
    ///
    /// If both leases are multi-stream, also copies `stream_identifier` /
    /// `shard_id` (matching `MultiStreamLease.update`, which casts + copies).
    pub fn update(&mut self, other: &Lease) {
        self.owner_switches_since_checkpoint = other.owner_switches_since_checkpoint;
        self.checkpoint = other.checkpoint.clone();
        self.pending_checkpoint = other.pending_checkpoint.clone();
        self.pending_checkpoint_state = other.pending_checkpoint_state.clone();
        // parentShardIds setter clears+replaces
        self.parent_shard_ids = other.parent_shard_ids.clone();
        // childShardIds setter only ADDS (asymmetry preserved)
        self.child_shard_ids
            .extend(other.child_shard_ids.iter().cloned());
        if self.is_multi_stream() && other.is_multi_stream() {
            self.stream_identifier = other.stream_identifier.clone();
            self.shard_id = other.shard_id.clone();
        }
    }

    /// Deep copy (Java `copy()` / `MultiStreamLease.copy()`).
    pub fn copy(&self) -> Lease {
        self.clone()
    }

    // ---- setters (Lombok fluent; heavily used by renewer/taker) ----

    /// Set `last_counter_increment_nanos`.
    pub fn set_last_counter_increment_nanos(&mut self, v: Option<i64>) {
        self.last_counter_increment_nanos = v;
    }

    /// Set `concurrency_token` (Java `@NonNull`).
    pub fn set_concurrency_token(&mut self, v: Uuid) {
        self.concurrency_token = Some(v);
    }

    /// Set `lease_key`. Immutable once set.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if already set.
    pub fn set_lease_key(&mut self, lease_key: impl Into<String>) {
        if self.lease_key.is_some() {
            panic!("LeaseKey is immutable once set");
        }
        self.lease_key = Some(lease_key.into());
    }

    /// Set `lease_counter`.
    pub fn set_lease_counter(&mut self, v: i64) {
        self.lease_counter = v;
    }

    /// Set `checkpoint` (Java `@NonNull`).
    pub fn set_checkpoint(&mut self, v: ExtendedSequenceNumber) {
        self.checkpoint = Some(v);
    }

    /// Set `pending_checkpoint` (nullable).
    pub fn set_pending_checkpoint(&mut self, v: Option<ExtendedSequenceNumber>) {
        self.pending_checkpoint = v;
    }

    /// Set `pending_checkpoint_state` (nullable).
    pub fn set_pending_checkpoint_state(&mut self, v: Option<Vec<u8>>) {
        self.pending_checkpoint_state = v;
    }

    /// Set `owner_switches_since_checkpoint`.
    pub fn set_owner_switches_since_checkpoint(&mut self, v: i64) {
        self.owner_switches_since_checkpoint = v;
    }

    /// Set `parent_shard_ids`: clears then replaces (Java setter semantics).
    pub fn set_parent_shard_ids<I: IntoIterator<Item = String>>(&mut self, ids: I) {
        self.parent_shard_ids.clear();
        self.parent_shard_ids.extend(ids);
    }

    /// Set `child_shard_ids`: only ADDS, does not clear (Java asymmetry).
    pub fn set_child_shard_ids<I: IntoIterator<Item = String>>(&mut self, ids: I) {
        self.child_shard_ids.extend(ids);
    }

    /// Set `throughput_kbps`.
    pub fn set_throughput_kbps(&mut self, v: f64) {
        self.throughput_kbps = Some(v);
    }

    /// Set the hash-key range. Immutable once set.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if a *different* value is
    /// already set. Re-setting the same value is a no-op.
    pub fn set_hash_key_range(&mut self, v: HashKeyRangeForLease) {
        match &self.hash_key_range_for_lease {
            None => self.hash_key_range_for_lease = Some(v),
            Some(existing) if existing != &v => panic!("hashKeyRange is immutable"),
            Some(_) => {}
        }
    }

    /// Set `lease_owner` (nullable).
    pub fn set_lease_owner(&mut self, v: Option<String>) {
        self.lease_owner = v;
    }

    /// Set `is_marked_for_lease_steal`.
    pub fn set_marked_for_lease_steal(&mut self, v: bool) {
        self.is_marked_for_lease_steal = v;
    }

    /// Set `is_expired_or_unassigned`.
    pub fn set_expired_or_unassigned(&mut self, v: bool) {
        self.is_expired_or_unassigned = v;
    }

    /// Set `checkpoint_owner` (nullable).
    pub fn set_checkpoint_owner(&mut self, v: Option<String>) {
        self.checkpoint_owner = v;
    }

    /// Set `checkpoint_owner_timeout_timestamp_millis` (nullable).
    pub fn set_checkpoint_owner_timeout_timestamp_millis(&mut self, v: Option<i64>) {
        self.checkpoint_owner_timeout_timestamp_millis = v;
    }

    /// Set the serialized stream identifier (multi-stream). Java `@NonNull`
    /// `MultiStreamLease.streamIdentifier(String)`.
    pub fn set_stream_identifier(&mut self, v: impl Into<String>) {
        self.stream_identifier = Some(v.into());
    }

    /// Set the shard id (multi-stream). Java `@NonNull`
    /// `MultiStreamLease.shardId(String)`.
    pub fn set_shard_id(&mut self, v: impl Into<String>) {
        self.shard_id = Some(v.into());
    }

    // ---- MultiStreamLease statics ----

    /// Compute a multi-stream lease key: `streamIdentifier:shardId`. Java
    /// `MultiStreamLease.getLeaseKey`.
    pub fn multi_stream_lease_key(stream_identifier: &str, shard_id: &str) -> String {
        format!("{}:{}", stream_identifier, shard_id)
    }

    /// Validate that this lease is a multi-stream lease (Java
    /// `MultiStreamLease.validateAndCast`, which uses
    /// `Validate.isInstanceOf`).
    ///
    /// # Panics
    /// Panics if this is not a multi-stream lease.
    pub fn validate_multi_stream(&self) -> &Lease {
        if !self.is_multi_stream() {
            panic!("Expected subclass software.amazon.kinesis.leases.MultiStreamLease but was a single-stream Lease");
        }
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashSet;

    const MOCK_CURRENT_TIME: i64 = 10_000_000_000;
    const LEASE_DURATION_MILLIS: i64 = 1000;
    const LEASE_DURATION_NANOS: i64 = LEASE_DURATION_MILLIS * 1_000_000;
    const LEASE_CHECKPOINT_TIMEOUT: i64 = 1000;

    fn create_lease(
        lease_owner: Option<&str>,
        lease_key: &str,
        last_counter_increment_nanos: i64,
    ) -> Lease {
        let mut lease = Lease::default();
        lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number("checkpoint"));
        lease.set_owner_switches_since_checkpoint(0);
        lease.set_lease_counter(0);
        lease.set_lease_owner(lease_owner.map(|s| s.to_string()));
        lease.set_parent_shard_ids(["parentShardId".to_string()]);
        lease.set_child_shard_ids(HashSet::<String>::new());
        lease.set_lease_key(lease_key);
        lease.set_last_counter_increment_nanos(Some(last_counter_increment_nanos));
        lease
    }

    fn create_shutdown_requested_lease() -> Lease {
        let mut lease = create_lease(Some("leaseOwner"), "leaseKey", 0);
        lease.set_checkpoint_owner(Some("checkpointOwner".to_string()));
        lease.set_checkpoint_owner_timeout_timestamp_millis(Some(LEASE_CHECKPOINT_TIMEOUT));
        lease.set_expired_or_unassigned(false);
        lease
    }

    fn create_eligible_for_graceful_shutdown_lease() -> Lease {
        let mut lease = create_lease(Some("leaseOwner"), "leaseKey", 0);
        lease.set_expired_or_unassigned(false);
        lease.set_checkpoint(ExtendedSequenceNumber::trim_horizon());
        lease
    }

    // --- expiry / availability (LeaseTest) ---

    #[test]
    fn lease_owner_null_and_expired() {
        let expired = MOCK_CURRENT_TIME - LEASE_DURATION_NANOS - 1;
        let lease = create_lease(None, "leaseKey", expired);
        assert!(lease.is_available(LEASE_DURATION_NANOS, MOCK_CURRENT_TIME));
        assert_eq!(lease.lease_owner(), None);
    }

    #[test]
    fn lease_owner_not_null_and_expired() {
        let expired = MOCK_CURRENT_TIME - LEASE_DURATION_NANOS - 1;
        let lease = create_lease(Some("leaseOwner"), "leaseKey", expired);
        assert!(lease.is_available(LEASE_DURATION_NANOS, MOCK_CURRENT_TIME));
        assert_eq!(lease.lease_owner(), Some("leaseOwner"));
    }

    #[test]
    fn lease_owner_not_null_and_not_expired() {
        let not_expired = MOCK_CURRENT_TIME - LEASE_DURATION_NANOS + 1;
        let lease = create_lease(Some("leaseOwner"), "leaseKey", not_expired);
        assert!(!lease.is_available(LEASE_DURATION_NANOS, MOCK_CURRENT_TIME));
        assert_eq!(lease.lease_owner(), Some("leaseOwner"));
    }

    #[test]
    fn lease_owner_null_and_not_expired() {
        let not_expired = MOCK_CURRENT_TIME - LEASE_DURATION_NANOS + 1;
        let lease = create_lease(None, "leaseKey", not_expired);
        assert!(lease.is_available(LEASE_DURATION_NANOS, MOCK_CURRENT_TIME));
        assert_eq!(lease.lease_owner(), None);
    }

    // --- blockedOnPendingCheckpoint (LeaseTest) ---

    #[test]
    fn blocked_lease_assigned_and_checkpoint_not_expired_true() {
        let lease = create_shutdown_requested_lease();
        assert!(lease.blocked_on_pending_checkpoint(LEASE_CHECKPOINT_TIMEOUT - 1));
    }

    #[test]
    fn blocked_lease_unassigned_false() {
        let mut lease = create_shutdown_requested_lease();
        lease.set_expired_or_unassigned(true);
        assert!(!lease.blocked_on_pending_checkpoint(LEASE_CHECKPOINT_TIMEOUT));
    }

    #[test]
    fn blocked_shard_end_false() {
        let mut lease = create_shutdown_requested_lease();
        lease.set_checkpoint(ExtendedSequenceNumber::shard_end());
        assert!(!lease.blocked_on_pending_checkpoint(LEASE_CHECKPOINT_TIMEOUT));
    }

    #[test]
    fn blocked_shutdown_not_requested_false() {
        let mut lease = create_shutdown_requested_lease();
        lease.set_checkpoint_owner(None);
        assert!(!lease.blocked_on_pending_checkpoint(LEASE_CHECKPOINT_TIMEOUT));
    }

    #[test]
    fn blocked_checkpoint_timeout_expired_false() {
        let lease = create_shutdown_requested_lease();
        assert!(!lease.blocked_on_pending_checkpoint(LEASE_CHECKPOINT_TIMEOUT + 1000));
    }

    // --- isEligibleForGracefulShutdown (LeaseTest) ---

    #[test]
    fn eligible_for_graceful_shutdown_true() {
        let lease = create_eligible_for_graceful_shutdown_lease();
        assert!(lease.is_eligible_for_graceful_shutdown());
    }

    #[test]
    fn eligible_shard_end_false() {
        // Mirrors the Java test which mutates the eligible lease but asserts on
        // the shutdown-requested lease (which has a checkpointOwner set).
        let shutdown = create_shutdown_requested_lease();
        assert!(!shutdown.is_eligible_for_graceful_shutdown());
    }

    #[test]
    fn eligible_shutdown_requested_false() {
        let mut lease = create_eligible_for_graceful_shutdown_lease();
        lease.set_checkpoint_owner(Some("owner".to_string()));
        assert!(!lease.is_eligible_for_graceful_shutdown());
    }

    // --- copy (LeaseTest) ---

    #[test]
    fn copying_lease_preserves_checkpoint_owner() {
        let mut original = Lease::default();
        original.set_checkpoint_owner(Some("checkpointOwner".to_string()));
        let copy = original.copy();
        assert_eq!(copy.checkpoint_owner(), Some("checkpointOwner"));
    }

    // --- Entity type (LeaseTest) ---

    #[test]
    fn get_entity_type_always_lease() {
        assert_eq!(Lease::default().entity_type(), EntityType::Lease);
        let lease = create_lease(Some("owner"), "key", 0);
        assert_eq!(lease.entity_type(), EntityType::Lease);
        assert_eq!(lease.entity_type().ddb_value(), "LEASE");
    }

    // --- MultiStreamLease (MultiStreamLeaseTest) ---

    #[test]
    fn copying_multi_stream_lease() {
        let mut original = Lease::default();
        original.set_checkpoint_owner(Some("checkpointOwner".to_string()));
        original.set_stream_identifier("identifier");
        original.set_shard_id("shardId");
        let copy = original.copy();
        assert_eq!(copy.checkpoint_owner(), Some("checkpointOwner"));
        assert!(copy.is_multi_stream());
        assert_eq!(copy.stream_identifier(), Some("identifier"));
        assert_eq!(copy.shard_id(), Some("shardId"));
    }

    #[test]
    fn multi_stream_lease_key_format() {
        assert_eq!(
            Lease::multi_stream_lease_key("stream", "shard"),
            "stream:shard"
        );
    }

    #[test]
    #[should_panic(expected = "MultiStreamLease")]
    fn validate_multi_stream_panics_on_single_stream() {
        Lease::default().validate_multi_stream();
    }

    // --- equality excludes transient fields ---

    #[test]
    fn equality_excludes_concurrency_token_and_owner_switches_included() {
        let mut a = create_lease(Some("o"), "k", 0);
        let mut b = create_lease(Some("o"), "k", 999);
        a.set_concurrency_token(Uuid::new_v4());
        b.set_concurrency_token(Uuid::new_v4());
        // concurrency_token and last_counter_increment_nanos are excluded.
        assert_eq!(a, b);
        // lease_counter is included.
        b.set_lease_counter(42);
        assert_ne!(a, b);
    }

    // --- overflow guard ---

    #[test]
    fn expired_when_age_exceeds_max_abs_age() {
        let mut lease = create_lease(Some("o"), "k", 0);
        // as_of far in the "past" relative to last increment -> abs(age) huge
        lease.set_last_counter_increment_nanos(Some(MAX_ABS_AGE_NANOS + 100));
        assert!(lease.is_expired(LEASE_DURATION_NANOS, 0));
    }

    #[test]
    fn expired_when_last_increment_none() {
        let mut lease = create_lease(Some("o"), "k", 0);
        lease.set_last_counter_increment_nanos(None);
        assert!(lease.is_expired(LEASE_DURATION_NANOS, MOCK_CURRENT_TIME));
    }
}
