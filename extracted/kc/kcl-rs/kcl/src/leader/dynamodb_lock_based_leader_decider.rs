//! Port of `software.amazon.kinesis.leader.DynamoDBLockBasedLeaderDecider`.
//!
//! Elects a leader via a distributed lock in a DynamoDB table. Java wraps the
//! external `AmazonDynamoDBLockClient` library; this port uses the
//! reimplemented [`DdbLockClient`](super::ddb_lock::DdbLockClient) (see that
//! module for the acquire/heartbeat/steal/release algorithm).
//!
//! # Lock-client routing (Java `CoordinatorStateDAO.getDDBLockClient()`)
//!
//! Java creates two lock clients (legacy + lease table) via
//! `initializeLockClients` and returns whichever the current
//! `TableMigrationStatus` routes to. This port owns two persistent
//! [`DdbLockClient`]s (each with its own in-memory session/expiry state) and
//! selects the one for the **live** status on each `isLeader` cycle — so a
//! mid-cycle PENDING->COMPLETE migration flip transparently switches from the
//! legacy to the lease table (the lock client for a cycle is captured once so
//! `releaseLeadershipIfHeld` in the same cycle uses the same client).
//!
//! # Sync trait over async I/O
//!
//! [`LeaderDecider::is_leader`] is a **sync** trait method (consumed by
//! `PeriodicShardSyncManager`/`LeaseAssignmentManager` loops), but the lock
//! client + [`TableMigrationStateMachine`] are async. The public sync methods
//! bridge to the async core ([`Self::is_leader_async`] etc.) via a
//! `block_in_place`/`block_on` helper (production runs a multi-thread runtime).
//! Tests drive the async core directly under `#[tokio::test]`.

use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

use aws_sdk_cloudwatch::types::StandardUnit;
use tokio::sync::Mutex as AsyncMutex;

use super::ddb_lock::{DdbLockClient, LockClock};
use super::leader_lock::{leader_lock_state, LEADER_HASH_KEY};
use crate::coordinator::coordinator_state_dao::CoordinatorStateDao;
use crate::coordinator::leader_decider::{
    LeaderDecider, METRIC_OPERATION_LEADER_DECIDER, METRIC_OPERATION_LEADER_DECIDER_IS_LEADER,
};
use crate::coordinator::migration::table_migration_state_machine::{
    TableMigrationError, TableMigrationStateMachine,
};
use crate::metrics::metrics_level::MetricsLevel;
use crate::metrics::{metrics_util, MetricsFactory};

/// Guarded mutable state (Java: fields under the intrinsic `synchronized` monitor).
struct State {
    last_check_time_millis: i64,
    last_is_leader_result: bool,
}

/// DynamoDB-lock-based [`LeaderDecider`].
pub struct DynamoDBLockBasedLeaderDecider {
    worker_id: String,
    heartbeat_period_millis: i64,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    table_migration_state_machine: Arc<dyn TableMigrationStateMachine>,
    coordinator_state_dao: Arc<CoordinatorStateDao>,
    /// Persistent lock client for the legacy coordinator-state table.
    legacy_lock_client: DdbLockClient,
    /// Persistent lock client for the lease table.
    lease_lock_client: DdbLockClient,
    /// Injectable millis-clock for the debounce window (test seam).
    now_millis: Arc<dyn Fn() -> i64 + Send + Sync>,
    is_shutdown: AtomicBool,
    /// Coarse async monitor guarding the whole is_leader/shutdown/release critical
    /// section (Java's `synchronized`: blocks for the full duration incl. I/O).
    state: AsyncMutex<State>,
}

impl DynamoDBLockBasedLeaderDecider {
    /// Java `create(CoordinatorStateDAO, workerId, leaseDuration, heartbeatPeriod,
    /// MetricsFactory, TableMigrationStateMachine)` (the `@VisibleForTesting`
    /// overload). Creates both lock clients (Java `initializeLockClients`).
    pub fn create(
        coordinator_state_dao: Arc<CoordinatorStateDao>,
        worker_id: impl Into<String>,
        lease_duration_millis: i64,
        heartbeat_period_millis: i64,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        table_migration_state_machine: Arc<dyn TableMigrationStateMachine>,
    ) -> Self {
        let worker_id = worker_id.into();
        let legacy = coordinator_state_dao.legacy_table_dao_delegate();
        let lease = coordinator_state_dao.lease_table_dao_delegate();
        let legacy_lock_client = DdbLockClient::new(
            coordinator_state_dao.client().clone(),
            legacy.table_name(),
            legacy.partition_key_attribute_name(),
            worker_id.clone(),
            lease_duration_millis,
        );
        let lease_lock_client = DdbLockClient::new(
            coordinator_state_dao.client().clone(),
            lease.table_name(),
            lease.partition_key_attribute_name(),
            worker_id.clone(),
            lease_duration_millis,
        );
        Self {
            worker_id,
            heartbeat_period_millis,
            metrics_factory,
            table_migration_state_machine,
            coordinator_state_dao,
            legacy_lock_client,
            lease_lock_client,
            now_millis: Arc::new(now_epoch_millis),
            is_shutdown: AtomicBool::new(false),
            state: AsyncMutex::new(State {
                last_check_time_millis: 0,
                last_is_leader_result: false,
            }),
        }
    }

    /// Test seam: override the debounce millis-clock and both lock clients' clocks.
    pub fn with_clocks(
        mut self,
        now_millis: Arc<dyn Fn() -> i64 + Send + Sync>,
        lock_clock: LockClock,
    ) -> Self {
        self.now_millis = now_millis;
        // Rebuild lock clients with the injected clock (they carry no state yet).
        self.legacy_lock_client = std::mem::replace(
            &mut self.legacy_lock_client,
            DdbLockClient::new(
                self.coordinator_state_dao.client().clone(),
                "x",
                "x",
                "x",
                0,
            ),
        )
        .with_clock(lock_clock.clone());
        self.lease_lock_client = std::mem::replace(
            &mut self.lease_lock_client,
            DdbLockClient::new(
                self.coordinator_state_dao.client().clone(),
                "x",
                "x",
                "x",
                0,
            ),
        )
        .with_clock(lock_clock);
        self
    }

    fn lock_client_for_cycle(&self) -> &DdbLockClient {
        if self.coordinator_state_dao.lock_routes_to_lease_table() {
            &self.lease_lock_client
        } else {
            &self.legacy_lock_client
        }
    }

    fn lock_attributes(&self) -> HashMap<String, aws_sdk_dynamodb::types::AttributeValue> {
        // Java getLockAttributes(): `new LeaderLock().serialize()`.
        leader_lock_state().serialize()
    }

    fn publish_is_leader_metrics(&self, response: bool) {
        let mut scope = metrics_util::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            METRIC_OPERATION_LEADER_DECIDER,
        );
        scope.add_data_with_level(
            METRIC_OPERATION_LEADER_DECIDER_IS_LEADER,
            if response { 1.0 } else { 0.0 },
            StandardUnit::Count,
            MetricsLevel::Detailed,
        );
        metrics_util::end_scope(scope.as_mut());
    }

    /// Async core of Java `synchronized Boolean isLeader(String workerId)`.
    pub async fn is_leader_async(&self, worker_id: &str) -> bool {
        let mut state = self.state.lock().await;

        // 1. Shut down: return false, no lock attempt.
        if self.is_shutdown.load(Ordering::SeqCst) {
            self.publish_is_leader_metrics(false);
            return false;
        }

        // 2. Debounce: if last result was false and within heartbeat window, cache.
        let now = (self.now_millis)();
        if !state.last_is_leader_result
            && state.last_check_time_millis + self.heartbeat_period_millis > now
        {
            self.publish_is_leader_metrics(state.last_is_leader_result);
            return state.last_is_leader_result;
        }

        // 3. Get the lock client once for this cycle (routing captured).
        let lock_client = self.lock_client_for_cycle();
        let mut response;

        // 4. Read current lock.
        let lock_item = lock_client.get_lock(LEADER_HASH_KEY).await.unwrap_or(None);

        // 5. If absent or expired, try to acquire (non-blocking).
        let is_absent_or_expired = lock_item.as_ref().map(|i| i.is_expired()).unwrap_or(true);
        if is_absent_or_expired {
            match lock_client
                .try_acquire_lock(LEADER_HASH_KEY, &self.lock_attributes())
                .await
            {
                Ok(acquired) => response = acquired,
                Err(_) => {
                    // Defensive: release just in case and don't assume leadership.
                    let _ = Self::release_on(lock_client, &self.worker_id).await;
                    response = false;
                }
            }
        } else {
            // 6. Lock present & valid: leader iff we own it.
            response = lock_item
                .as_ref()
                .map(|i| i.owner_name() == worker_id)
                .unwrap_or(false);
        }

        // 7. Always call handleLeaderLockResult; on Dependency/InvalidState:
        //    release + force false (Java catches both uniformly).
        match self
            .table_migration_state_machine
            .handle_leader_lock_result(response)
            .await
        {
            Ok(()) => {}
            Err(TableMigrationError::Dependency(_)) | Err(TableMigrationError::InvalidState(_)) => {
                tracing::warn!("handleLeaderLockResult failed, releasing lock and returning false");
                let _ = Self::release_on(lock_client, &self.worker_id).await;
                response = false;
            }
            Err(TableMigrationError::LockHandoffRequired) => {
                // Treated like an InvalidState signal (migration requires releasing).
                tracing::warn!("handleLeaderLockResult signaled lock handoff, releasing lock and returning false");
                let _ = Self::release_on(lock_client, &self.worker_id).await;
                response = false;
            }
        }

        state.last_check_time_millis = (self.now_millis)();
        state.last_is_leader_result = response;
        self.publish_is_leader_metrics(response);
        response
    }

    /// Async core of Java `synchronized void shutdown()` (idempotent).
    pub async fn shutdown_async(&self) {
        if !self.is_shutdown.swap(true, Ordering::SeqCst) {
            self.release_leadership_if_held_async().await;
            tracing::info!(
                "Shutting down DynamoDB lock clients for worker {}",
                self.worker_id
            );
        }
    }

    /// Async core of Java `synchronized void releaseLeadershipIfHeld()`.
    pub async fn release_leadership_if_held_async(&self) {
        let lock_client = self.lock_client_for_cycle();
        let _ = Self::release_on(lock_client, &self.worker_id).await;
    }

    /// Java private `releaseLeadershipIfHeld(lockClient)`: release iff we own an
    /// unexpired lock. Errors are swallowed (release never throws).
    async fn release_on(lock_client: &DdbLockClient, worker_id: &str) -> Result<(), ()> {
        match lock_client.get_lock(LEADER_HASH_KEY).await {
            Ok(Some(item)) if !item.is_expired() && item.owner_name() == worker_id => {
                tracing::info!(
                    "Current worker : {} holds the lock, releasing it.",
                    worker_id
                );
                if let Err(e) = lock_client.release_lock(LEADER_HASH_KEY, &item).await {
                    tracing::error!("Failed to complete releaseLeadershipIfHeld call: {e}");
                }
            }
            Ok(_) => {}
            Err(e) => tracing::error!("Failed to complete releaseLeadershipIfHeld call: {e}"),
        }
        Ok(())
    }
}

impl LeaderDecider for DynamoDBLockBasedLeaderDecider {
    fn is_leader(&self, worker_id: &str) -> bool {
        let wid = worker_id.to_string();
        run_sync(self.is_leader_async(&wid))
    }

    fn shutdown(&self) {
        run_sync(self.shutdown_async());
    }

    fn initialize(&self) {
        tracing::info!("Initializing DDB Lock based leader decider");
    }

    fn release_leadership_if_held(&self) {
        run_sync(self.release_leadership_if_held_async());
    }

    fn metric_name(&self) -> &'static str {
        "DynamoDBLockBasedLeaderDecider"
    }
}

fn now_epoch_millis() -> i64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

/// Bridge a `Send` future to a sync call — see the module docs. Mirrors the
/// `DynamoDBLeaseRenewer::run_sync` helper.
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
mod tests;
