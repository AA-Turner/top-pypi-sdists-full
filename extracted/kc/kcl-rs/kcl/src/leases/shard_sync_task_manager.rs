//! Port of `software.amazon.kinesis.leases.ShardSyncTaskManager`.
//!
//! Ensures at most **one** [`ShardSyncTask`] is in flight at a time by tracking a
//! spawned task's [`JoinHandle`] and re-using/replacing it via a lock-guarded
//! check, coalescing requests that arrive while a sync is already running into a
//! single pending flag.
//!
//! # Concurrency (deviation)
//!
//! Java uses a `ReentrantLock` guarding `checkAndSubmitNextTask()`, a
//! `CompletableFuture<TaskResult>` from
//! `CompletableFuture.supplyAsync(() -> task.call(), executorService)
//!  .whenComplete(...)`, and an `AtomicBoolean shardSyncRequestPending`. The Rust
//! port uses:
//!
//! - `lock` → [`tokio::sync::Mutex`] guarding the check-and-submit critical
//!   section.
//! - `future` → an `Option<JoinHandle<TaskResult>>` (the spawned tokio task).
//!   "future is null OR cancelled OR done" becomes "handle is `None` OR
//!   `is_finished()`".
//! - `shardSyncRequestPending` → an [`AtomicBool`] (write-only here, exactly as
//!   in Java — the flag is set but not consumed in this class; an external
//!   scheduler polls it).
//!
//! [`JoinHandle`]: tokio::task::JoinHandle

use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

use tokio::sync::Mutex;
use tokio::task::JoinHandle;

use crate::common::InitialPositionInStreamExtended;
use crate::leases::hierarchical_shard_syncer::HierarchicalShardSyncer;
use crate::leases::shard_sync_task::ShardSyncTask;
use crate::leases::{LeaseRefresher, ShardDetector};
use crate::lifecycle::{ConsumerTask, TaskResult};
use crate::metrics::MetricsFactory;

/// Tracks the single outstanding shard-sync task.
pub struct ShardSyncTaskManager {
    shard_detector: Arc<dyn ShardDetector>,
    lease_refresher: Arc<dyn LeaseRefresher>,
    initial_position_in_stream: InitialPositionInStreamExtended,
    cleanup_leases_upon_shard_completion: bool,
    garbage_collect_leases: bool,
    ignore_unexpected_child_shards: bool,
    shard_sync_idle_time_millis: i64,
    hierarchical_shard_syncer: Arc<HierarchicalShardSyncer>,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,

    inner: Mutex<Inner>,
    shard_sync_request_pending: AtomicBool,
}

#[derive(Default)]
struct Inner {
    future: Option<JoinHandle<TaskResult>>,
}

impl ShardSyncTaskManager {
    /// Construct a shard-sync task manager (mirrors the primary Java constructor;
    /// `garbageCollectLeases` is always `true` there).
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        shard_detector: Arc<dyn ShardDetector>,
        lease_refresher: Arc<dyn LeaseRefresher>,
        initial_position_in_stream: InitialPositionInStreamExtended,
        cleanup_leases_upon_shard_completion: bool,
        ignore_unexpected_child_shards: bool,
        shard_sync_idle_time_millis: i64,
        hierarchical_shard_syncer: Arc<HierarchicalShardSyncer>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Self {
        Self {
            shard_detector,
            lease_refresher,
            initial_position_in_stream,
            cleanup_leases_upon_shard_completion,
            garbage_collect_leases: true,
            ignore_unexpected_child_shards,
            shard_sync_idle_time_millis,
            hierarchical_shard_syncer,
            metrics_factory,
            inner: Mutex::new(Inner::default()),
            shard_sync_request_pending: AtomicBool::new(false),
        }
    }

    /// The [`ShardDetector`] this manager syncs against (Java Lombok `@Getter`
    /// `shardDetector()`). Used by the periodic shard-sync manager to backfill
    /// missing lease hash ranges from Kinesis shards.
    pub fn shard_detector(&self) -> Arc<dyn ShardDetector> {
        self.shard_detector.clone()
    }

    fn new_task(&self) -> ShardSyncTask {
        ShardSyncTask::new(
            self.shard_detector.clone(),
            self.lease_refresher.clone(),
            self.initial_position_in_stream,
            self.cleanup_leases_upon_shard_completion,
            self.garbage_collect_leases,
            self.ignore_unexpected_child_shards,
            self.shard_sync_idle_time_millis,
            self.hierarchical_shard_syncer.clone(),
            self.metrics_factory.clone(),
        )
    }

    /// Build and run a [`ShardSyncTask`] synchronously (Java `callShardSyncTask`),
    /// bypassing the future-tracking machinery.
    pub async fn call_shard_sync_task(&self) -> TaskResult {
        self.new_task().call().await
    }

    /// Submit a shard-sync task, returning `true` iff a NEW task was actually
    /// submitted this call (Java `submitShardSyncTask`).
    pub async fn submit_shard_sync_task(self: &Arc<Self>) -> bool {
        let mut inner = self.inner.lock().await;
        self.check_and_submit_next_task(&mut inner)
    }

    fn check_and_submit_next_task(self: &Arc<Self>, inner: &mut Inner) -> bool {
        let can_submit = match &inner.future {
            None => true,
            Some(handle) => handle.is_finished(),
        };

        if can_submit {
            // If a previous task finished, drop its handle (Java `future.get()`
            // to surface any exception via logging — we just discard the result).
            inner.future = None;

            let task = self.new_task();
            let handle = tokio::spawn(async move { task.call().await });
            inner.future = Some(handle);
            true
        } else {
            // Coalesce into the pending flag (write-only, as in Java).
            self.shard_sync_request_pending
                .compare_exchange(false, true, Ordering::SeqCst, Ordering::SeqCst)
                .ok();
            false
        }
    }

    /// Test accessor for the (write-only) pending flag.
    pub fn shard_sync_request_pending(&self) -> bool {
        self.shard_sync_request_pending.load(Ordering::SeqCst)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::{InitialPositionInStream, StreamIdentifier};
    use crate::leases::exceptions::LeasingError;
    use crate::leases::MockLeaseRefresher;
    use crate::metrics::NullMetricsFactory;
    use aws_sdk_kinesis::types::{HashKeyRange, SequenceNumberRange, Shard};

    fn open_shard(id: &str, hstart: &str, hend: &str) -> Shard {
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
                    .starting_hash_key(hstart)
                    .ending_hash_key(hend)
                    .build()
                    .unwrap(),
            )
            .build()
            .unwrap()
    }

    struct FakeDetector;
    #[async_trait::async_trait]
    impl ShardDetector for FakeDetector {
        async fn shard(&self, _id: &str) -> Result<Option<Shard>, LeasingError> {
            Ok(None)
        }
        async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
            Ok(vec![
                open_shard("shardId-0", "0", "99"),
                open_shard(
                    "shardId-1",
                    "100",
                    "340282366920938463463374607431768211455",
                ),
            ])
        }
        async fn list_shards_with_filter_for_consumer(
            &self,
            _f: aws_sdk_kinesis::types::ShardFilter,
            _c: &str,
        ) -> Result<Vec<Shard>, LeasingError> {
            self.list_shards().await
        }
        fn stream_identifier(&self) -> Result<StreamIdentifier, LeasingError> {
            Ok(StreamIdentifier::single_stream_instance("my-stream"))
        }
    }

    fn manager() -> Arc<ShardSyncTaskManager> {
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_is_lease_table_empty()
            .returning(|| Ok(true));
        refresher.expect_list_leases().returning(|| Ok(Vec::new()));
        refresher
            .expect_get_lease_table_identifier()
            .returning(|| Ok(String::new()));
        refresher
            .expect_create_lease_if_not_exists()
            .returning(|_| Ok(true));

        Arc::new(ShardSyncTaskManager::new(
            Arc::new(FakeDetector),
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

    #[tokio::test]
    async fn call_shard_sync_task_runs_synchronously() {
        let m = manager();
        let result = m.call_shard_sync_task().await;
        assert!(result.exception().is_none());
    }

    #[tokio::test]
    async fn submit_returns_true_for_new_task_and_completes() {
        let m = manager();
        assert!(m.submit_shard_sync_task().await);
        // Let the spawned task finish.
        {
            let mut inner = m.inner.lock().await;
            if let Some(handle) = inner.future.take() {
                let _ = handle.await;
            }
        }
        // After completion, a new submit succeeds again.
        assert!(m.submit_shard_sync_task().await);
        let mut inner = m.inner.lock().await;
        if let Some(handle) = inner.future.take() {
            let _ = handle.await;
        }
    }
}
