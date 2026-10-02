//! Port of `software.amazon.kinesis.lifecycle.ShutdownNotificationTask`.

use std::sync::{Arc, Mutex};

use async_trait::async_trait;

use crate::checkpoint::ShardRecordProcessorCheckpointer;
use crate::exceptions::BoxError;
use crate::leases::{LeaseCoordinator, ShardInfo};
use crate::lifecycle::events::ShutdownRequestedInput;
use crate::lifecycle::lease_graceful_shutdown_handler::attempt_lease_transfer;
use crate::lifecycle::{ConsumerTask, ShutdownNotification, TaskResult, TaskType};
use crate::processor::{RecordProcessorCheckpointer, ShardRecordProcessor};

/// Notifies the record processor of an incoming shutdown request, giving it a
/// chance to checkpoint, then either signals the [`ShutdownNotification`] (worker
/// level) or drops the lease directly (shard level).
///
/// # Concurrency
///
/// The customer `shutdownRequested()` callback is invoked via
/// [`tokio::task::spawn_blocking`]. The finally-equivalent (signal notification
/// / drop lease) **always** runs regardless of success/exception.
pub struct ShutdownNotificationTask {
    shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
    record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
    shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
    shard_info: ShardInfo,
    lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
}

impl ShutdownNotificationTask {
    /// Package-private in Java (`@RequiredArgsConstructor(access = PACKAGE)`).
    pub fn new(
        shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
        record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
        shutdown_notification: Option<Arc<dyn ShutdownNotification>>,
        shard_info: ShardInfo,
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    ) -> Self {
        Self {
            shard_record_processor,
            record_processor_checkpointer,
            shutdown_notification,
            shard_info,
            lease_coordinator,
        }
    }

    /// The inner try/catch: run the customer callback + attempt lease transfer;
    /// any error is returned (no backoff, unlike other tasks).
    async fn inner(
        &self,
        current_shard_lease: &mut Option<crate::leases::Lease>,
    ) -> Result<(), BoxError> {
        let checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync> =
            self.record_processor_checkpointer.clone();
        let input = ShutdownRequestedInput::builder()
            .checkpointer(checkpointer)
            .build();

        let processor = self.shard_record_processor.clone();
        tokio::task::spawn_blocking(move || {
            let mut guard = processor
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            guard.shutdown_requested(input);
        })
        .await
        .map_err(|e| Box::new(e) as BoxError)?;

        attempt_lease_transfer(
            current_shard_lease.as_mut(),
            self.lease_coordinator.as_ref(),
        )
        .await
        .map_err(|e| Box::new(e) as BoxError)?;
        Ok(())
    }
}

#[async_trait]
impl ConsumerTask for ShutdownNotificationTask {
    async fn call(&self) -> TaskResult {
        let lease_key = self.shard_info.lease_key();
        let mut current_shard_lease = self.lease_coordinator.get_currently_held_lease(&lease_key);

        let result = match self.inner(&mut current_shard_lease).await {
            Ok(()) => TaskResult::new(None),
            Err(e) => TaskResult::new(Some(e)),
        };

        // finally: always signal notification-complete, or drop the lease if this
        // is a shard-level (no ShutdownNotification) graceful shutdown.
        match &self.shutdown_notification {
            Some(notification) => notification.shutdown_notification_complete(),
            None => {
                if let Some(lease) = &current_shard_lease {
                    self.lease_coordinator.drop_lease(lease);
                }
            }
        }

        result
    }

    fn task_type(&self) -> TaskType {
        TaskType::ShutdownNotification
    }

    fn task_name(&self) -> &'static str {
        "ShutdownNotificationTask"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::leases::{Lease, MockLeaseCoordinator, MockLeaseRefresher};
    use crate::processor::{Checkpointer, MockShardRecordProcessor};
    use crate::retrieval::kpl::ExtendedSequenceNumber;
    use std::sync::atomic::{AtomicUsize, Ordering};

    const LEASE_OWNER: &str = "leaseOwner";
    const SHARD_ID: &str = "shardId-9";

    fn shard_info() -> ShardInfo {
        ShardInfo::single_stream(SHARD_ID, Some("token".into()), Vec::<String>::new(), None)
    }

    fn checkpointer() -> Arc<ShardRecordProcessorCheckpointer> {
        let store: Arc<dyn Checkpointer + Send + Sync> =
            Arc::new(crate::checkpoint::in_memory_checkpointer::InMemoryCheckpointer::new());
        ShardRecordProcessorCheckpointer::new(shard_info(), store)
    }

    fn lease_shutdown_requested(checkpoint_owner: Option<&str>) -> Lease {
        let mut lease = Lease::default();
        lease.set_lease_key(SHARD_ID);
        lease.set_lease_owner(Some(LEASE_OWNER.to_string()));
        lease.set_checkpoint(ExtendedSequenceNumber::latest());
        lease.set_checkpoint_owner(checkpoint_owner.map(str::to_string));
        lease
    }

    #[tokio::test]
    async fn lease_transfer_called_when_checkpoint_owner_matches() {
        // checkpointOwner == worker id -> assignLease called; then dropLease (null notification).
        let assign_count = Arc::new(AtomicUsize::new(0));
        let ac = assign_count.clone();
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_assign_lease().returning(move |_, _| {
            ac.fetch_add(1, Ordering::SeqCst);
            Ok(true)
        });
        let refresher: Arc<dyn LeaseRefresherTrait> = Arc::new(refresher);

        let drop_count = Arc::new(AtomicUsize::new(0));
        let dc = drop_count.clone();
        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .returning(|_| Some(lease_shutdown_requested(Some(LEASE_OWNER))));
        coordinator
            .expect_worker_identifier()
            .returning(|| LEASE_OWNER.to_string());
        coordinator
            .expect_lease_refresher()
            .returning(move || refresher.clone());
        coordinator.expect_drop_lease().returning(move |_| {
            dc.fetch_add(1, Ordering::SeqCst);
        });

        let mut proc = MockShardRecordProcessor::new();
        proc.expect_shutdown_requested().times(1).returning(|_| ());

        let task = ShutdownNotificationTask::new(
            Arc::new(Mutex::new(Box::new(proc))),
            checkpointer(),
            None,
            shard_info(),
            Arc::new(coordinator),
        );
        let result = task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(assign_count.load(Ordering::SeqCst), 1);
        assert_eq!(drop_count.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn lease_transfer_not_called_when_checkpoint_owner_mismatch() {
        // checkpointOwner is None (not shutdown-requested) -> no assign; still dropLease.
        let mut refresher = MockLeaseRefresher::new();
        refresher.expect_assign_lease().never();
        let refresher: Arc<dyn LeaseRefresherTrait> = Arc::new(refresher);

        let drop_count = Arc::new(AtomicUsize::new(0));
        let dc = drop_count.clone();
        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .returning(|_| Some(lease_shutdown_requested(None)));
        coordinator
            .expect_worker_identifier()
            .returning(|| LEASE_OWNER.to_string());
        coordinator
            .expect_lease_refresher()
            .returning(move || refresher.clone());
        coordinator.expect_drop_lease().returning(move |_| {
            dc.fetch_add(1, Ordering::SeqCst);
        });

        let mut proc = MockShardRecordProcessor::new();
        proc.expect_shutdown_requested().returning(|_| ());

        let task = ShutdownNotificationTask::new(
            Arc::new(Mutex::new(Box::new(proc))),
            checkpointer(),
            None,
            shard_info(),
            Arc::new(coordinator),
        );
        assert!(task.call().await.exception().is_none());
        assert_eq!(drop_count.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn task_type_is_shutdown_notification() {
        let mut coordinator = MockLeaseCoordinator::new();
        coordinator
            .expect_get_currently_held_lease()
            .returning(|_| None);
        let mut proc = MockShardRecordProcessor::new();
        proc.expect_shutdown_requested().returning(|_| ());
        let task = ShutdownNotificationTask::new(
            Arc::new(Mutex::new(Box::new(proc))),
            checkpointer(),
            None,
            shard_info(),
            Arc::new(coordinator),
        );
        assert_eq!(task.task_type(), TaskType::ShutdownNotification);
    }

    use crate::leases::LeaseRefresher as LeaseRefresherTrait;
}
