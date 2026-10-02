//! Port of `software.amazon.kinesis.leases.ShardSyncTask`.
//!
//! A single [`ConsumerTask`] that performs one shard-sync pass by delegating to
//! [`HierarchicalShardSyncer::check_and_create_lease_for_new_shards`], optionally
//! sleeping afterward iff a sync was actually performed.
//!
//! # Behavior preserved
//!
//! - `call()` wraps the sync in a try/catch, converting any error into a
//!   [`TaskResult`] carrying the error (task-framework convention: failures are
//!   returned as data, not propagated).
//! - It **always** records a boolean `SyncShards` success/failure metric at
//!   `DETAILED` level in a `finally`-equivalent, and ends the scope.
//! - If `did_perform_shard_sync` is `true` **and** `shard_sync_task_idle_time_millis
//!   > 0`, it sleeps afterward (an async `tokio::time::sleep` in place of Java's
//!   `Thread.sleep`). The sleep is SKIPPED when no sync was performed.
//! - `task_type()` = [`TaskType::ShardSync`]; `task_name()` = `"ShardSyncTask"`
//!   (Java `getClass().getSimpleName()`).

use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;

use crate::common::InitialPositionInStreamExtended;
use crate::leases::hierarchical_shard_syncer::HierarchicalShardSyncer;
use crate::leases::{LeaseRefresher, ShardDetector};
use crate::lifecycle::{ConsumerTask, TaskResult, TaskType};
use crate::metrics::{self, MetricsFactory, MetricsLevel};

const SHARD_SYNC_TASK_OPERATION: &str = "ShardSyncTask";

/// Syncs leases with shards of the stream (one pass).
pub struct ShardSyncTask {
    shard_detector: Arc<dyn ShardDetector>,
    lease_refresher: Arc<dyn LeaseRefresher>,
    initial_position: InitialPositionInStreamExtended,
    #[allow(dead_code)]
    cleanup_leases_upon_shard_completion: bool,
    #[allow(dead_code)]
    garbage_collect_leases: bool,
    ignore_unexpected_child_shards: bool,
    shard_sync_task_idle_time_millis: i64,
    hierarchical_shard_syncer: Arc<HierarchicalShardSyncer>,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
}

impl ShardSyncTask {
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        shard_detector: Arc<dyn ShardDetector>,
        lease_refresher: Arc<dyn LeaseRefresher>,
        initial_position: InitialPositionInStreamExtended,
        cleanup_leases_upon_shard_completion: bool,
        garbage_collect_leases: bool,
        ignore_unexpected_child_shards: bool,
        shard_sync_task_idle_time_millis: i64,
        hierarchical_shard_syncer: Arc<HierarchicalShardSyncer>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Self {
        Self {
            shard_detector,
            lease_refresher,
            initial_position,
            cleanup_leases_upon_shard_completion,
            garbage_collect_leases,
            ignore_unexpected_child_shards,
            shard_sync_task_idle_time_millis,
            hierarchical_shard_syncer,
            metrics_factory,
        }
    }
}

#[async_trait]
impl ConsumerTask for ShardSyncTask {
    async fn call(&self) -> TaskResult {
        let mut scope = metrics::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            SHARD_SYNC_TASK_OPERATION,
        );
        let mut shard_sync_success = true;
        let mut exception: Option<crate::exceptions::BoxError> = None;

        // First determine whether the lease table is empty (Java calls
        // leaseRefresher.isLeaseTableEmpty() as an argument to the sync).
        let is_lease_table_empty = match self.lease_refresher.is_lease_table_empty().await {
            Ok(empty) => Some(empty),
            Err(e) => {
                exception = Some(Box::new(e));
                shard_sync_success = false;
                None
            }
        };

        if let Some(is_lease_table_empty) = is_lease_table_empty {
            match self
                .hierarchical_shard_syncer
                .check_and_create_lease_for_new_shards(
                    self.shard_detector.as_ref(),
                    self.lease_refresher.as_ref(),
                    &self.initial_position,
                    scope.as_mut(),
                    self.ignore_unexpected_child_shards,
                    is_lease_table_empty,
                )
                .await
            {
                Ok(did_perform_shard_sync) => {
                    if did_perform_shard_sync && self.shard_sync_task_idle_time_millis > 0 {
                        tokio::time::sleep(Duration::from_millis(
                            self.shard_sync_task_idle_time_millis as u64,
                        ))
                        .await;
                    }
                }
                Err(e) => {
                    exception = Some(Box::new(e));
                    shard_sync_success = false;
                }
            }
        }

        // finally: always record the SyncShards metric + end scope.
        metrics::add_success(
            scope.as_mut(),
            Some("SyncShards"),
            shard_sync_success,
            MetricsLevel::Detailed,
        );
        metrics::end_scope(scope.as_mut());

        TaskResult::new(exception)
    }

    fn task_type(&self) -> TaskType {
        TaskType::ShardSync
    }

    fn task_name(&self) -> &'static str {
        "ShardSyncTask"
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

    struct FakeDetector {
        shards: Vec<Shard>,
    }
    #[async_trait]
    impl ShardDetector for FakeDetector {
        async fn shard(&self, _id: &str) -> Result<Option<Shard>, LeasingError> {
            Ok(None)
        }
        async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
            Ok(self.shards.clone())
        }
        async fn list_shards_with_filter_for_consumer(
            &self,
            _f: aws_sdk_kinesis::types::ShardFilter,
            _c: &str,
        ) -> Result<Vec<Shard>, LeasingError> {
            Ok(self.shards.clone())
        }
        fn stream_identifier(&self) -> Result<StreamIdentifier, LeasingError> {
            Ok(StreamIdentifier::single_stream_instance("my-stream"))
        }
    }

    #[tokio::test]
    async fn call_syncs_and_returns_success() {
        // Two open shards covering the full hash range → bootstrap creates 2 leases.
        let shards = vec![
            open_shard("shardId-0", "0", "99"),
            open_shard(
                "shardId-1",
                "100",
                "340282366920938463463374607431768211455",
            ),
        ];
        let detector: Arc<dyn ShardDetector> = Arc::new(FakeDetector { shards });

        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_is_lease_table_empty()
            .returning(|| Ok(true));
        refresher.expect_list_leases().returning(|| Ok(Vec::new()));
        refresher
            .expect_get_lease_table_identifier()
            .returning(|| Ok(String::new()));
        let created = Arc::new(std::sync::Mutex::new(0usize));
        let created_clone = created.clone();
        refresher
            .expect_create_lease_if_not_exists()
            .returning(move |_| {
                *created_clone.lock().unwrap() += 1;
                Ok(true)
            });
        let refresher: Arc<dyn LeaseRefresher> = Arc::new(refresher);

        let task = ShardSyncTask::new(
            detector,
            refresher,
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            true,
            true,
            false,
            0, // no idle sleep
            Arc::new(HierarchicalShardSyncer::new()),
            Arc::new(NullMetricsFactory),
        );

        let result = task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(*created.lock().unwrap(), 2);
        assert_eq!(task.task_type(), TaskType::ShardSync);
        assert_eq!(task.task_name(), "ShardSyncTask");
    }

    #[tokio::test]
    async fn call_records_failure_on_error() {
        struct FailingDetector;
        #[async_trait]
        impl ShardDetector for FailingDetector {
            async fn shard(&self, _id: &str) -> Result<Option<Shard>, LeasingError> {
                Ok(None)
            }
            async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
                Ok(Vec::new())
            }
            async fn list_shards_with_filter_for_consumer(
                &self,
                _f: aws_sdk_kinesis::types::ShardFilter,
                _c: &str,
            ) -> Result<Vec<Shard>, LeasingError> {
                Err(LeasingError::dependency("boom"))
            }
            fn stream_identifier(&self) -> Result<StreamIdentifier, LeasingError> {
                Ok(StreamIdentifier::single_stream_instance("my-stream"))
            }
        }
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_is_lease_table_empty()
            .returning(|| Ok(true));
        refresher.expect_list_leases().returning(|| Ok(Vec::new()));
        refresher
            .expect_get_lease_table_identifier()
            .returning(|| Ok(String::new()));
        let refresher: Arc<dyn LeaseRefresher> = Arc::new(refresher);

        let task = ShardSyncTask::new(
            Arc::new(FailingDetector),
            refresher,
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            true,
            true,
            false,
            0,
            Arc::new(HierarchicalShardSyncer::new()),
            Arc::new(NullMetricsFactory),
        );
        let result = task.call().await;
        assert!(result.exception().is_some());
    }
}
