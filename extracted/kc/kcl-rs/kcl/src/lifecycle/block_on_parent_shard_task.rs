//! Port of `software.amazon.kinesis.lifecycle.BlockOnParentShardTask`.

use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;

use crate::exceptions::BoxError;
use crate::leases::{LeaseRefresher, ShardInfo};
use crate::lifecycle::{ConsumerTask, TaskResult, TaskType};
use crate::retrieval::kpl::ExtendedSequenceNumber;

/// Task to block until processing of all data records in the parent shard(s) is
/// complete.
///
/// For each parent shard, fetch its lease; if a lease exists with a checkpoint
/// that is not `SHARD_END`, we are blocked (return a
/// `BlockedOnParentShardException` after sleeping the poll interval). If no lease
/// exists for a parent it is assumed trimmed and we proceed. If nothing blocks,
/// return immediately with no exception and no sleep.
///
/// `call` is `async` (the Rust `ConsumerTask` contract): the `getLease` I/O uses
/// `.await` and the backoff sleep uses [`tokio::time::sleep`] (Java's
/// `Thread.sleep`, whose interrupt-swallow semantics map to cooperative
/// cancellation — a dropped future silently stops the sleep).
pub struct BlockOnParentShardTask {
    shard_info: ShardInfo,
    lease_refresher: Arc<dyn LeaseRefresher>,
    /// Sleep for this duration if the parent shards have not completed processing
    /// or an exception is encountered.
    parent_shard_poll_interval_millis: i64,
}

impl BlockOnParentShardTask {
    /// Package-private in Java (`@RequiredArgsConstructor(access = PACKAGE)`).
    pub fn new(
        shard_info: ShardInfo,
        lease_refresher: Arc<dyn LeaseRefresher>,
        parent_shard_poll_interval_millis: i64,
    ) -> Self {
        Self {
            shard_info,
            lease_refresher,
            parent_shard_poll_interval_millis,
        }
    }
}

#[async_trait]
impl ConsumerTask for BlockOnParentShardTask {
    async fn call(&self) -> TaskResult {
        let mut exception: Option<BoxError> = None;
        let shard_info_id = self.shard_info.lease_key();

        // The Java `try` block: any exception (including the deliberately-created
        // BlockedOnParentShardException) is captured into `exception`.
        let mut blocked_on_parent_shard = false;
        let mut caught_error = false;
        for shard_id in self.shard_info.parent_shard_ids() {
            let lease_key = self.shard_info.lease_key_with_override(&shard_id);
            match self.lease_refresher.get_lease(&lease_key).await {
                Ok(Some(lease)) => {
                    let checkpoint = lease.checkpoint();
                    if checkpoint != Some(&ExtendedSequenceNumber::shard_end()) {
                        tracing::debug!(
                            "Shard {} is not yet done. Its current checkpoint is {:?}",
                            shard_info_id,
                            checkpoint
                        );
                        blocked_on_parent_shard = true;
                        exception = Some(Box::<dyn std::error::Error + Send + Sync>::from(
                            "BlockedOnParentShardException: Parent shard not yet done",
                        ));
                        break;
                    } else {
                        tracing::debug!("Shard {} has been completely processed.", shard_info_id);
                    }
                }
                Ok(None) => {
                    tracing::info!(
                        "No lease found for shard {}. Not blocking on completion of this shard.",
                        shard_info_id
                    );
                }
                Err(e) => {
                    tracing::error!(
                        "Caught exception when checking for parent shard checkpoint: {}",
                        e
                    );
                    exception = Some(Box::new(e));
                    caught_error = true;
                    break;
                }
            }
        }

        if !blocked_on_parent_shard && !caught_error {
            tracing::info!(
                "No need to block on parents {:?} of shard {}",
                self.shard_info.parent_shard_ids(),
                shard_info_id
            );
            return TaskResult::new(None);
        }

        // Sleep happens on both the blocked path and the caught-exception path.
        tokio::time::sleep(Duration::from_millis(
            self.parent_shard_poll_interval_millis.max(0) as u64,
        ))
        .await;

        TaskResult::new(exception)
    }

    fn task_type(&self) -> TaskType {
        TaskType::BlockOnParentShards
    }

    fn task_name(&self) -> &'static str {
        "BlockOnParentShardTask"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::{Lease, MockLeaseRefresher};

    const SHARD_ID: &str = "shardId-97";
    const STREAM_ID: &str = "123:stream:146";
    const CONCURRENCY_TOKEN: &str = "testToken";
    const BACKOFF: i64 = 50;

    fn shard_info(parents: Vec<String>, stream_id: Option<&str>) -> ShardInfo {
        ShardInfo::new(
            SHARD_ID,
            Some(CONCURRENCY_TOKEN.to_string()),
            parents,
            Some(ExtendedSequenceNumber::trim_horizon()),
            stream_id.map(str::to_string),
        )
    }

    fn lease_with_checkpoint(cp: ExtendedSequenceNumber) -> Lease {
        let mut lease = Lease::default();
        lease.set_checkpoint(cp);
        lease
    }

    #[tokio::test(start_paused = true)]
    async fn test_call_no_parents() {
        // No parents -> immediate success, no getLease.
        let refresher = MockLeaseRefresher::new();
        let task =
            BlockOnParentShardTask::new(shard_info(vec![], None), Arc::new(refresher), BACKOFF);
        let result = task.call().await;
        assert!(result.exception().is_none());
    }

    #[tokio::test(start_paused = true)]
    async fn test_should_not_block_when_parents_finished() {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_get_lease().returning(|_| {
            Ok(Some(lease_with_checkpoint(
                ExtendedSequenceNumber::shard_end(),
            )))
        });
        let refresher = Arc::new(refresher);

        // single parent
        let task = BlockOnParentShardTask::new(
            shard_info(vec!["shardId-1".into()], None),
            refresher.clone(),
            BACKOFF,
        );
        assert!(task.call().await.exception().is_none());

        // two parents
        let task = BlockOnParentShardTask::new(
            shard_info(vec!["shardId-1".into(), "shardId-2".into()], None),
            refresher,
            BACKOFF,
        );
        assert!(task.call().await.exception().is_none());
    }

    #[tokio::test(start_paused = true)]
    async fn test_should_not_block_when_parents_finished_multi_stream() {
        let mut refresher = MockLeaseRefresher::new();
        // multi-stream lease keys are "123:stream:146:shardId-N"
        refresher
            .expect_get_lease()
            .withf(|k| k.starts_with(STREAM_ID))
            .returning(|_| {
                Ok(Some(lease_with_checkpoint(
                    ExtendedSequenceNumber::shard_end(),
                )))
            });
        let refresher = Arc::new(refresher);

        let task = BlockOnParentShardTask::new(
            shard_info(
                vec!["shardId-1".into(), "shardId-2".into()],
                Some(STREAM_ID),
            ),
            refresher,
            BACKOFF,
        );
        assert!(task.call().await.exception().is_none());
    }

    #[tokio::test(start_paused = true)]
    async fn test_call_when_parents_have_not_finished() {
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_get_lease().returning(|_| {
            Ok(Some(
                lease_with_checkpoint(ExtendedSequenceNumber::latest()),
            ))
        });
        let task = BlockOnParentShardTask::new(
            shard_info(vec!["shardId-1".into()], None),
            Arc::new(refresher),
            BACKOFF,
        );
        let result = task.call().await;
        assert!(result.exception().is_some());
    }

    #[tokio::test(start_paused = true)]
    async fn test_call_when_parents_have_not_finished_multi_stream() {
        // Multi-stream parents that have NOT been fully processed -> exception.
        // Lease keys are "123:stream:146:shardId-N"; the checkpoints are LATEST /
        // a raw sequence number (neither is SHARD_END), so we block.
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_get_lease()
            .withf(|k| k.starts_with(STREAM_ID))
            .returning(|_| {
                Ok(Some(
                    lease_with_checkpoint(ExtendedSequenceNumber::latest()),
                ))
            });
        let refresher = Arc::new(refresher);

        // single parent
        let task = BlockOnParentShardTask::new(
            shard_info(vec!["shardId-1".into()], Some(STREAM_ID)),
            refresher.clone(),
            BACKOFF,
        );
        assert!(task.call().await.exception().is_some());

        // two parents
        let task = BlockOnParentShardTask::new(
            shard_info(
                vec!["shardId-1".into(), "shardId-2".into()],
                Some(STREAM_ID),
            ),
            refresher,
            BACKOFF,
        );
        assert!(task.call().await.exception().is_some());
    }

    #[tokio::test(start_paused = true)]
    async fn test_before_and_after_a_parent_finishes() {
        // not-yet-finished parent -> exception
        let mut r1 = MockLeaseRefresher::new();
        r1.expect_get_lease().returning(|_| {
            Ok(Some(lease_with_checkpoint(
                ExtendedSequenceNumber::from_sequence_number("98182584034"),
            )))
        });
        let task = BlockOnParentShardTask::new(
            shard_info(vec!["shardId-1".into()], None),
            Arc::new(r1),
            BACKOFF,
        );
        assert!(task.call().await.exception().is_some());

        // fully-processed parent -> no exception
        let mut r2 = MockLeaseRefresher::new();
        r2.expect_get_lease().returning(|_| {
            Ok(Some(lease_with_checkpoint(
                ExtendedSequenceNumber::shard_end(),
            )))
        });
        let task = BlockOnParentShardTask::new(
            shard_info(vec!["shardId-1".into()], None),
            Arc::new(r2),
            BACKOFF,
        );
        assert!(task.call().await.exception().is_none());
    }

    #[tokio::test]
    async fn test_get_task_type() {
        let refresher = MockLeaseRefresher::new();
        let task =
            BlockOnParentShardTask::new(shard_info(vec![], None), Arc::new(refresher), BACKOFF);
        assert_eq!(task.task_type(), TaskType::BlockOnParentShards);
    }
}
