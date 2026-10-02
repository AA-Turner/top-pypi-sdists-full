//! Reimplementation of the DynamoDB distributed-lock algorithm that Java's
//! `com.amazonaws.services.dynamodbv2.AmazonDynamoDBLockClient` provides.
//!
//! There is **no Rust equivalent** of the `amazon-dynamodb-lock-client` Java
//! library, so this module reimplements exactly the subset of its behavior that
//! [`DynamoDBLockBasedLeaderDecider`](super::dynamodb_lock_based_leader_decider::DynamoDBLockBasedLeaderDecider)
//! relies on, using `aws_sdk_dynamodb::Client` conditional writes against the
//! coordinator-state table (the lock item shares the table with the leader-lock
//! `CoordinatorState` record, keyed by the `"Leader"` hash key).
//!
//! # DDB item schema (wire-compatible with the Java lock client)
//!
//! The lock is a single DDB item at hash key `<partitionKey> = "Leader"` with:
//! - `ownerName` (S) — the worker id that currently holds the lock,
//! - `recordVersionNumber` (RVN, S) — a fresh UUID rewritten on every
//!   acquire/heartbeat; used as the fencing token for steal detection,
//! - `leaseDuration` (S, milliseconds) — how long the lock is valid without a
//!   heartbeat,
//! - plus any `additional_attributes` (here: the `entityType` attribute from
//!   the `LeaderLock` `CoordinatorState`).
//!
//! # Algorithm (faithful to what the decider needs)
//!
//! - **`get_lock`** — `GetItem`; returns [`LockItem`] snapshot (owner + RVN +
//!   leaseDuration) + a local `lookup_instant` captured from the injectable
//!   [`LockClock`]. `None` if absent. Records the observed `(rvn, lookup_instant)`
//!   in an in-memory session map keyed by lock key so a *later* `try_acquire`
//!   can detect "RVN unchanged for at least one lease-duration" -> stealable.
//! - **`try_acquire_lock`** (non-blocking, `shouldSkipBlockingWait=true`) —
//!   1. Re-read the current item.
//!   2. If absent: conditional `PutItem` with `attribute_not_exists(pk)` claiming
//!      the lock with our owner + a fresh RVN. On `ConditionalCheckFailed` (a
//!      race) -> not acquired.
//!   3. If present and its RVN matches what we previously observed **and** at
//!      least `leaseDuration` has elapsed since we first observed that RVN
//!      (local timing) -> steal: conditional `PutItem` guarded by
//!      `recordVersionNumber = <observed>` writing our owner + a fresh RVN.
//!   4. Otherwise (fresh/updated lock, or not yet expired) -> not acquired. When
//!      first seeing another owner's lock we record its RVN + lookup instant so
//!      the *next* call can steal after the lease elapses (this reproduces the
//!      Java library's "first call starts the expiry timer, does not acquire").
//! - **`release_lock`** — conditional `DeleteItem` guarded by
//!   `ownerName = <me> AND recordVersionNumber = <held>`; a no-op if we don't
//!   own it (matches `LockItem.close()`).
//!
//! # Concurrency / timing
//!
//! Timing uses an injectable [`LockClock`] (default: `std::time::Instant`) so
//! acquire/renew/steal can be driven deterministically in tests. Session state
//! (held RVN + observed-other RVN/instant) lives in a `std::sync::Mutex`.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use aws_sdk_dynamodb::types::AttributeValue;
use aws_sdk_dynamodb::Client;
use uuid::Uuid;

/// Attribute name for the lock owner (Java lock client `ownerName`).
pub const OWNER_NAME: &str = "ownerName";
/// Attribute name for the fencing token (Java lock client `recordVersionNumber`).
pub const RECORD_VERSION_NUMBER: &str = "recordVersionNumber";
/// Attribute name for the lease duration in millis (Java lock client `leaseDuration`).
pub const LEASE_DURATION: &str = "leaseDuration";

/// Injectable monotonic clock for lock timing (test seam replacing the Java
/// lock client's internal wall/monotonic timing).
pub type LockClock = Arc<dyn Fn() -> Instant + Send + Sync>;

fn default_clock() -> LockClock {
    Arc::new(Instant::now)
}

/// A snapshot of the lock item as returned by [`DdbLockClient::get_lock`].
#[derive(Clone, Debug)]
pub struct LockItem {
    owner_name: String,
    record_version_number: String,
    lease_duration_millis: i64,
    /// Local instant when this snapshot was fetched (for [`LockItem::is_expired`]).
    lookup_instant: Instant,
    now: Instant,
}

impl LockItem {
    /// Java `LockItem.getOwnerName()`.
    pub fn owner_name(&self) -> &str {
        &self.owner_name
    }

    /// Java `LockItem.isExpired()`: elapsed since fetch exceeds the lease.
    pub fn is_expired(&self) -> bool {
        self.now.duration_since(self.lookup_instant)
            > Duration::from_millis(self.lease_duration_millis.max(0) as u64)
    }
}

#[derive(Default)]
struct SessionState {
    /// RVN this client currently believes it holds (set on successful acquire).
    held_rvn: Option<String>,
    /// The last RVN observed for a lock owned by *someone else* + when we first
    /// saw it — used for steal-after-lease-elapsed detection.
    observed_rvn: Option<String>,
    observed_instant: Option<Instant>,
}

/// A reimplementation of the Java `AmazonDynamoDBLockClient` scoped to a single
/// lock item on one DynamoDB table.
pub struct DdbLockClient {
    client: Client,
    table_name: String,
    partition_key_attribute_name: String,
    lease_duration_millis: i64,
    owner_name: String,
    clock: LockClock,
    session: Mutex<SessionState>,
}

impl DdbLockClient {
    /// Construct a lock client for `table_name` with the given owner + lease.
    pub fn new(
        client: Client,
        table_name: impl Into<String>,
        partition_key_attribute_name: impl Into<String>,
        owner_name: impl Into<String>,
        lease_duration_millis: i64,
    ) -> Self {
        Self {
            client,
            table_name: table_name.into(),
            partition_key_attribute_name: partition_key_attribute_name.into(),
            lease_duration_millis,
            owner_name: owner_name.into(),
            clock: default_clock(),
            session: Mutex::new(SessionState::default()),
        }
    }

    /// Test seam: override the timing clock.
    pub fn with_clock(mut self, clock: LockClock) -> Self {
        self.clock = clock;
        self
    }

    fn pk(&self, key: &str) -> HashMap<String, AttributeValue> {
        let mut m = HashMap::new();
        m.insert(
            self.partition_key_attribute_name.clone(),
            AttributeValue::S(key.to_string()),
        );
        m
    }

    /// Java `getLock(key, Optional.empty())` — read the current lock item (if
    /// any) and record session state for later steal detection.
    pub async fn get_lock(&self, key: &str) -> Result<Option<LockItem>, LockError> {
        let out = self
            .client
            .get_item()
            .table_name(&self.table_name)
            .set_key(Some(self.pk(key)))
            .consistent_read(true)
            .send()
            .await
            .map_err(|e| LockError::Dependency(format!("getLock failed: {e}")))?;

        let now = (self.clock)();
        match out.item {
            None => {
                // No lock present; clear any stale observation.
                let mut s = self.session.lock().unwrap_or_else(|e| e.into_inner());
                s.observed_rvn = None;
                s.observed_instant = None;
                Ok(None)
            }
            Some(item) => {
                let owner_name = item
                    .get(OWNER_NAME)
                    .and_then(|v| v.as_s().ok())
                    .cloned()
                    .unwrap_or_default();
                let rvn = item
                    .get(RECORD_VERSION_NUMBER)
                    .and_then(|v| v.as_s().ok())
                    .cloned()
                    .unwrap_or_default();
                let lease_duration_millis = item
                    .get(LEASE_DURATION)
                    .and_then(|v| v.as_s().ok())
                    .and_then(|s| s.parse::<i64>().ok())
                    .unwrap_or(self.lease_duration_millis);

                // Update session observation for lock owned by someone else.
                {
                    let mut s = self.session.lock().unwrap_or_else(|e| e.into_inner());
                    if owner_name != self.owner_name {
                        if s.observed_rvn.as_deref() != Some(rvn.as_str()) {
                            // First time (or changed) seeing this RVN: (re)start expiry timer.
                            s.observed_rvn = Some(rvn.clone());
                            s.observed_instant = Some(now);
                        }
                    } else {
                        // We own it; no foreign observation to track.
                        s.observed_rvn = None;
                        s.observed_instant = None;
                    }
                }

                Ok(Some(LockItem {
                    owner_name,
                    record_version_number: rvn,
                    lease_duration_millis,
                    lookup_instant: now,
                    now,
                }))
            }
        }
    }

    /// Java non-blocking `tryAcquireLock(...withShouldSkipBlockingWait(true))`.
    /// Returns `Ok(true)` iff this worker now holds the lock.
    pub async fn try_acquire_lock(
        &self,
        key: &str,
        additional_attributes: &HashMap<String, AttributeValue>,
    ) -> Result<bool, LockError> {
        let current = self.get_lock(key).await?;
        match current {
            None => self.claim_new(key, additional_attributes).await,
            Some(item) => {
                if item.owner_name == self.owner_name {
                    // Already ours: refresh (heartbeat) with a fresh RVN.
                    return self
                        .steal_or_renew(key, &item.record_version_number, additional_attributes)
                        .await;
                }
                // Owned by someone else — steal iff observed-RVN is unchanged and
                // at least one lease-duration has elapsed since we first observed it.
                let (observed_rvn, observed_instant) = {
                    let s = self.session.lock().unwrap_or_else(|e| e.into_inner());
                    (s.observed_rvn.clone(), s.observed_instant)
                };
                let now = (self.clock)();
                let elapsed_ok = observed_instant
                    .map(|t| {
                        now.duration_since(t)
                            > Duration::from_millis(self.lease_duration_millis.max(0) as u64)
                    })
                    .unwrap_or(false);
                if observed_rvn.as_deref() == Some(item.record_version_number.as_str())
                    && elapsed_ok
                {
                    self.steal_or_renew(key, &item.record_version_number, additional_attributes)
                        .await
                } else {
                    Ok(false)
                }
            }
        }
    }

    /// Conditional put claiming an absent lock (`attribute_not_exists(pk)`).
    async fn claim_new(
        &self,
        key: &str,
        additional_attributes: &HashMap<String, AttributeValue>,
    ) -> Result<bool, LockError> {
        let new_rvn = Uuid::new_v4().to_string();
        let item = self.build_item(key, &new_rvn, additional_attributes);
        let res = self
            .client
            .put_item()
            .table_name(&self.table_name)
            .set_item(Some(item))
            .condition_expression("attribute_not_exists(#pk)")
            .expression_attribute_names("#pk", &self.partition_key_attribute_name)
            .send()
            .await;
        match res {
            Ok(_) => {
                self.mark_held(new_rvn);
                Ok(true)
            }
            Err(e) => {
                let se = e.into_service_error();
                if se.is_conditional_check_failed_exception() {
                    Ok(false)
                } else {
                    Err(LockError::Dependency(format!(
                        "acquireLock put failed: {se}"
                    )))
                }
            }
        }
    }

    /// Conditional put stealing/renewing when the RVN matches `expected_rvn`.
    async fn steal_or_renew(
        &self,
        key: &str,
        expected_rvn: &str,
        additional_attributes: &HashMap<String, AttributeValue>,
    ) -> Result<bool, LockError> {
        let new_rvn = Uuid::new_v4().to_string();
        let item = self.build_item(key, &new_rvn, additional_attributes);
        let res = self
            .client
            .put_item()
            .table_name(&self.table_name)
            .set_item(Some(item))
            .condition_expression("#rvn = :expected")
            .expression_attribute_names("#rvn", RECORD_VERSION_NUMBER)
            .expression_attribute_values(":expected", AttributeValue::S(expected_rvn.to_string()))
            .send()
            .await;
        match res {
            Ok(_) => {
                self.mark_held(new_rvn);
                Ok(true)
            }
            Err(e) => {
                let se = e.into_service_error();
                if se.is_conditional_check_failed_exception() {
                    Ok(false)
                } else {
                    Err(LockError::Dependency(format!(
                        "acquireLock steal failed: {se}"
                    )))
                }
            }
        }
    }

    /// Java `LockItem.close()` — release the lock iff we still own it.
    /// Conditional `DeleteItem` guarded by owner + held RVN.
    pub async fn release_lock(&self, key: &str, item: &LockItem) -> Result<(), LockError> {
        if item.owner_name != self.owner_name {
            return Ok(());
        }
        let res = self
            .client
            .delete_item()
            .table_name(&self.table_name)
            .set_key(Some(self.pk(key)))
            .condition_expression("#owner = :owner AND #rvn = :rvn")
            .expression_attribute_names("#owner", OWNER_NAME)
            .expression_attribute_names("#rvn", RECORD_VERSION_NUMBER)
            .expression_attribute_values(":owner", AttributeValue::S(self.owner_name.clone()))
            .expression_attribute_values(
                ":rvn",
                AttributeValue::S(item.record_version_number.clone()),
            )
            .send()
            .await;
        match res {
            Ok(_) => {
                self.clear_held();
                Ok(())
            }
            Err(e) => {
                let se = e.into_service_error();
                if se.is_conditional_check_failed_exception() {
                    // We don't own it anymore — no-op (matches close() semantics).
                    Ok(())
                } else {
                    Err(LockError::Dependency(format!("release lock failed: {se}")))
                }
            }
        }
    }

    fn build_item(
        &self,
        key: &str,
        rvn: &str,
        additional_attributes: &HashMap<String, AttributeValue>,
    ) -> HashMap<String, AttributeValue> {
        let mut item = self.pk(key);
        item.insert(
            OWNER_NAME.to_string(),
            AttributeValue::S(self.owner_name.clone()),
        );
        item.insert(
            RECORD_VERSION_NUMBER.to_string(),
            AttributeValue::S(rvn.to_string()),
        );
        item.insert(
            LEASE_DURATION.to_string(),
            AttributeValue::S(self.lease_duration_millis.to_string()),
        );
        for (k, v) in additional_attributes {
            item.entry(k.clone()).or_insert_with(|| v.clone());
        }
        item
    }

    fn mark_held(&self, rvn: String) {
        let mut s = self.session.lock().unwrap_or_else(|e| e.into_inner());
        s.held_rvn = Some(rvn);
        s.observed_rvn = None;
        s.observed_instant = None;
    }

    fn clear_held(&self) {
        let mut s = self.session.lock().unwrap_or_else(|e| e.into_inner());
        s.held_rvn = None;
    }
}

/// Errors surfaced by [`DdbLockClient`]. Modeled minimally: the decider treats
/// all as best-effort (swallowed on the release path).
#[derive(Debug, thiserror::Error)]
pub enum LockError {
    #[error("{0}")]
    Dependency(String),
}
