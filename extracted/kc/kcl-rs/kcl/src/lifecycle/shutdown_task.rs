//! Port of `software.amazon.kinesis.lifecycle.ShutdownTask`.

use std::collections::HashSet;
use std::sync::{Arc, Mutex};
use std::time::Duration;

use async_trait::async_trait;
use aws_sdk_kinesis::types::ChildShard;

use crate::checkpoint::ShardRecordProcessorCheckpointer;
use crate::common::{InitialPositionInStreamExtended, StreamIdentifier};
use crate::exceptions::BoxError;
use crate::leases::exceptions::{CustomerApplicationError, LeasePendingDeletion, LeasingError};
use crate::leases::{
    HierarchicalShardSyncer, Lease, LeaseCleanupManager, LeaseCoordinator, ShardDetector,
    ShardInfo, UpdateField,
};
use crate::lifecycle::events::{LeaseLostInput, ShardEndedInput};
use crate::lifecycle::lease_graceful_shutdown_handler::attempt_lease_transfer;
use crate::lifecycle::{ConsumerTask, ShutdownReason, TaskResult, TaskType};
use crate::metrics::{self, MetricsFactory, MetricsLevel, MetricsScope};
use crate::processor::{RecordProcessorCheckpointer, ShardRecordProcessor};
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::RecordsPublisher;

const SHUTDOWN_TASK_OPERATION: &str = "ShutdownTask";
const RECORD_PROCESSOR_SHUTDOWN_METRIC: &str = "RecordProcessor.shutdown";

/// 1-in-N probability constant for the partial-merge-parent race decision.
pub const RETRY_RANDOM_MAX_RANGE: i32 = 30;

/// Errors that classify like the Java exception families used by the
/// shard-end path.
enum ShutdownError {
    /// Non-recoverable-near-term (Java `InvalidStateException`): triggers the
    /// SHARD_END → LEASE_LOST reason downgrade.
    InvalidState(String),
    /// A merge-parent race that should keep the lease and back off (Java
    /// `BlockedOnParentShardException`).
    BlockedOnParentShard(String),
    /// A customer callback threw (Java `CustomerApplicationException`).
    CustomerApplication(CustomerApplicationError),
    /// Any other error (dependency/provisioned-throughput/etc.).
    Other(BoxError),
}

impl ShutdownError {
    fn into_box(self) -> BoxError {
        match self {
            ShutdownError::InvalidState(m) => Box::new(LeasingError::invalid_state(m)) as BoxError,
            ShutdownError::BlockedOnParentShard(m) => {
                Box::<dyn std::error::Error + Send + Sync>::from(format!(
                    "BlockedOnParentShardException: {m}"
                ))
            }
            ShutdownError::CustomerApplication(e) => Box::new(e) as BoxError,
            ShutdownError::Other(e) => e,
        }
    }
}

impl From<LeasingError> for ShutdownError {
    fn from(e: LeasingError) -> Self {
        // A leasing `InvalidStateException` triggers the SHARD_END -> LEASE_LOST
        // reason downgrade (Java `catch (InvalidStateException e)`), so it must
        // classify as `InvalidState` — every other leasing failure is `Other`.
        match e {
            LeasingError::InvalidState { .. } => ShutdownError::InvalidState(e.to_string()),
            other => ShutdownError::Other(Box::new(other)),
        }
    }
}

/// Injectable factory for a child-shard lease (Java
/// `hierarchicalShardSyncer.createLeaseForChildShard`). A closure seam so tests
/// can inject a throwing variant (Java mocks the method to throw).
pub type ChildLeaseFactory =
    Arc<dyn Fn(&ChildShard, &StreamIdentifier) -> Result<Lease, LeasingError> + Send + Sync>;

/// Injectable `1-in-N` probability (Java's `@VisibleForTesting isOneInNProbability`,
/// which the tests spy). The production default uses a thread RNG.
pub type OneInNProbability = Arc<dyn Fn(i32) -> bool + Send + Sync>;

/// Task for invoking the record processor's shutdown callback.
///
/// Distinguishes SHARD_END (create child leases, checkpoint at SHARD_END, enqueue
/// for cleanup) from LEASE_LOST/REQUESTED-cascaded (invoke `leaseLost()`,
/// best-effort transfer+drop a shutdown-requested lease). See PORTING.md.
///
/// Customer callbacks (`shardEnded`/`leaseLost`) run via
/// [`tokio::task::spawn_blocking`].
pub struct ShutdownTask {
    shard_info: ShardInfo,
    shard_detector: Arc<dyn ShardDetector>,
    shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
    record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
    reason: ShutdownReason,
    #[allow(dead_code)]
    initial_position_in_stream: InitialPositionInStreamExtended,
    #[allow(dead_code)]
    cleanup_leases_of_completed_shards: bool,
    #[allow(dead_code)]
    ignore_unexpected_child_shards: bool,
    lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    backoff_time_millis: i64,
    records_publisher: Arc<dyn RecordsPublisher>,
    #[allow(dead_code)]
    hierarchical_shard_syncer: Arc<HierarchicalShardSyncer>,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    child_shards: Option<Vec<ChildShard>>,
    stream_identifier: StreamIdentifier,
    lease_cleanup_manager: Arc<LeaseCleanupManager>,
    child_lease_factory: ChildLeaseFactory,
    one_in_n_probability: OneInNProbability,
}

impl ShutdownTask {
    /// Public in Java (`@RequiredArgsConstructor`).
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        shard_info: ShardInfo,
        shard_detector: Arc<dyn ShardDetector>,
        shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
        record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
        reason: ShutdownReason,
        initial_position_in_stream: InitialPositionInStreamExtended,
        cleanup_leases_of_completed_shards: bool,
        ignore_unexpected_child_shards: bool,
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
        backoff_time_millis: i64,
        records_publisher: Arc<dyn RecordsPublisher>,
        hierarchical_shard_syncer: Arc<HierarchicalShardSyncer>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        child_shards: Option<Vec<ChildShard>>,
        stream_identifier: StreamIdentifier,
        lease_cleanup_manager: Arc<LeaseCleanupManager>,
    ) -> Self {
        let syncer = hierarchical_shard_syncer.clone();
        let child_lease_factory: ChildLeaseFactory = Arc::new(move |child, sid| {
            syncer
                .create_lease_for_child_shard(child, sid)
                .map_err(|e| LeasingError::invalid_state(e.to_string()))
        });
        let one_in_n_probability: OneInNProbability =
            Arc::new(|n| rand::random::<u32>().is_multiple_of(n.max(1) as u32));
        Self {
            shard_info,
            shard_detector,
            shard_record_processor,
            record_processor_checkpointer,
            reason,
            initial_position_in_stream,
            cleanup_leases_of_completed_shards,
            ignore_unexpected_child_shards,
            lease_coordinator,
            backoff_time_millis,
            records_publisher,
            hierarchical_shard_syncer,
            metrics_factory,
            child_shards,
            stream_identifier,
            lease_cleanup_manager,
            child_lease_factory,
            one_in_n_probability,
        }
    }

    /// The shutdown reason (Java `@VisibleForTesting getReason()`).
    pub fn reason(&self) -> ShutdownReason {
        self.reason
    }

    /// Override the child-lease factory seam (test-only; Java mocks
    /// `createLeaseForChildShard`).
    #[cfg(test)]
    pub fn set_child_lease_factory(&mut self, f: ChildLeaseFactory) {
        self.child_lease_factory = f;
    }

    /// Override the `1-in-N` probability seam (Java `spy(...).isOneInNProbability`).
    #[cfg(test)]
    pub fn set_one_in_n_probability(&mut self, f: OneInNProbability) {
        self.one_in_n_probability = f;
    }

    /// Invoke the customer `leaseLost(LeaseLostInput)` via spawn_blocking.
    async fn invoke_lease_lost(&self) -> Result<(), BoxError> {
        let processor = self.shard_record_processor.clone();
        self.throw_on_application_exception(move || {
            let mut guard = processor
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            guard.lease_lost(LeaseLostInput::new());
        })
        .await
    }

    /// Java `throwOnApplicationException`: run the (blocking) action, wrapping any
    /// error/panic into a [`CustomerApplicationError`], always recording the
    /// shutdown-latency metric afterwards.
    async fn throw_on_application_exception<F>(&self, action: F) -> Result<(), BoxError>
    where
        F: FnOnce() + Send + 'static,
    {
        let start_time = metrics::current_time_millis();
        let result = tokio::task::spawn_blocking(action).await;

        let mut scope = metrics::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            SHUTDOWN_TASK_OPERATION,
        );
        metrics::add_latency(
            scope.as_mut(),
            Some(RECORD_PROCESSOR_SHUTDOWN_METRIC),
            start_time,
            MetricsLevel::Summary,
        );
        metrics::end_scope(scope.as_mut());

        match result {
            Ok(()) => Ok(()),
            Err(join_err) => Err(Box::new(CustomerApplicationError::with_cause(
                format!(
                    "Customer application throws exception for shard {}: ",
                    self.shard_info.lease_key()
                ),
                Box::<dyn std::error::Error + Send + Sync>::from(join_err.to_string()),
            )) as BoxError),
        }
    }

    /// The body inside Java's inner try (returns an error to be captured + backed
    /// off in `call`).
    async fn run(&self, scope: &mut (dyn MetricsScope + Send)) -> Result<(), BoxError> {
        let lease_key = self.shard_info.lease_key();
        let current_shard_lease = self.lease_coordinator.get_currently_held_lease(&lease_key);

        if self.reason == ShutdownReason::ShardEnd {
            match self
                .take_shard_end_action(current_shard_lease.clone(), &lease_key, scope)
                .await
            {
                Ok(()) => {}
                Err(ShutdownError::InvalidState(msg)) => {
                    // Non-recoverable near-term: drop the lease and downgrade to
                    // LEASE_LOST (customer gets leaseLost() instead of shardEnded()).
                    tracing::warn!(
                        "Lease {}: Invalid state encountered while shutting down with SHARD_END. \
                         Dropping the lease and shutting down using LEASE_LOST. ({})",
                        lease_key,
                        msg
                    );
                    self.drop_lease(current_shard_lease.as_ref(), &lease_key);
                    self.invoke_lease_lost().await?;
                }
                Err(other) => return Err(other.into_box()),
            }
        } else {
            // LEASE_LOST / REQUESTED-cascaded path.
            if let Some(lease) = &current_shard_lease {
                if lease.shutdown_requested() {
                    tracing::info!(
                        "Attempting to transfer and drop shutdown requested lease {}",
                        lease_key
                    );
                    let mut lease_copy = lease.clone();
                    if let Err(e) = attempt_lease_transfer(
                        Some(&mut lease_copy),
                        self.lease_coordinator.as_ref(),
                    )
                    .await
                    {
                        tracing::warn!("Unable to transfer lease {}: {}", lease_key, e);
                    }
                    self.drop_lease(current_shard_lease.as_ref(), &lease_key);
                }
            }
            self.invoke_lease_lost().await?;
        }

        tracing::debug!("Shutting down retrieval strategy for shard {}.", lease_key);
        self.records_publisher.shutdown().await;
        tracing::debug!(
            "Record processor completed shutdown() for shard {}",
            lease_key
        );
        Ok(())
    }

    /// Java `takeShardEndAction`: persist child shard info, checkpoint at
    /// SHARD_END, enqueue lease for cleanup.
    async fn take_shard_end_action(
        &self,
        current_shard_lease: Option<Lease>,
        lease_key: &str,
        scope: &mut (dyn MetricsScope + Send),
    ) -> Result<(), ShutdownError> {
        let current_shard_lease = current_shard_lease.ok_or_else(|| {
            ShutdownError::InvalidState(format!(
                "{lease_key} : Lease not owned by the current worker. Leaving ShardEnd handling to new owner."
            ))
        })?;

        let has_children = self
            .child_shards
            .as_ref()
            .map(|c| !c.is_empty())
            .unwrap_or(false);
        if has_children {
            self.create_leases_for_child_shards_if_not_exist(scope)
                .await?;
            self.update_lease_with_child_shards(&current_shard_lease)
                .await?;
        }

        let lease_pending_deletion = LeasePendingDeletion::new(
            self.stream_identifier.clone(),
            current_shard_lease,
            self.shard_info.clone(),
            self.shard_detector.clone(),
        );
        if !self
            .lease_cleanup_manager
            .is_enqueued_for_deletion(&lease_pending_deletion)
        {
            let checkpoint_result = self.attempt_shard_end_checkpointing(lease_key).await;
            let is_success = matches!(checkpoint_result, Ok(true));
            // finally: enqueue for deletion iff the checkpoint succeeded OR there
            // are no child shards (RNF/reprocessed-completed-shard cases).
            if is_success || !has_children {
                self.lease_cleanup_manager
                    .enqueue_for_deletion(lease_pending_deletion);
            }
            checkpoint_result?;
        }
        Ok(())
    }

    /// Java `attemptShardEndCheckpointing`.
    async fn attempt_shard_end_checkpointing(
        &self,
        lease_key: &str,
    ) -> Result<bool, ShutdownError> {
        let lease_from_ddb = self
            .lease_coordinator
            .lease_refresher()
            .get_lease(lease_key)
            .await?
            .ok_or_else(|| {
                ShutdownError::InvalidState(format!("Lease for shard {lease_key} does not exist."))
            })?;

        if lease_from_ddb.checkpoint() != Some(&ExtendedSequenceNumber::shard_end()) {
            self.application_checkpoint_and_verification(lease_key)
                .await?;
        }
        Ok(true)
    }

    /// Java `applicationCheckpointAndVerification` (wrapped by
    /// `throwOnApplicationException`): checkpoint at SHARD_END and verify.
    async fn application_checkpoint_and_verification(
        &self,
        lease_key: &str,
    ) -> Result<(), ShutdownError> {
        let largest = self
            .record_processor_checkpointer
            .largest_permitted_checkpoint_value();
        if let Some(largest) = largest {
            self.record_processor_checkpointer
                .set_sequence_number_at_shard_end(largest);
        }
        self.record_processor_checkpointer
            .set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::shard_end());

        let checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync> =
            self.record_processor_checkpointer.clone();
        let processor = self.shard_record_processor.clone();
        let input = ShardEndedInput::builder()
            .checkpointer(checkpointer)
            .build();
        self.throw_on_application_exception(move || {
            let mut guard = processor
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            guard.shard_ended(input);
        })
        .await
        .map_err(|e| match e.downcast::<CustomerApplicationError>() {
            Ok(cae) => ShutdownError::CustomerApplication(*cae),
            Err(e) => ShutdownError::Other(e),
        })?;

        // Verify the customer actually checkpointed at SHARD_END.
        let last = self.record_processor_checkpointer.last_checkpoint_value();
        if last != Some(ExtendedSequenceNumber::shard_end()) {
            return Err(ShutdownError::CustomerApplication(
                CustomerApplicationError::new(format!(
                    "Customer application throws exception for shard {lease_key}: \
                     Application didn't checkpoint at end of shard {lease_key}. \
                     Application must checkpoint upon shard end. \
                     See ShardRecordProcessor.shardEnded javadocs for more information."
                )),
            ));
        }
        Ok(())
    }

    /// Java `createLeasesForChildShardsIfNotExist`.
    async fn create_leases_for_child_shards_if_not_exist(
        &self,
        scope: &mut (dyn MetricsScope + Send),
    ) -> Result<(), ShutdownError> {
        let child_shards = self.child_shards.as_deref().unwrap_or(&[]);
        let lease_refresher = self.lease_coordinator.lease_refresher();

        // Merge (single child, two parents) special case.
        if child_shards.len() == 1 {
            let child_shard = &child_shards[0];
            let parent_lease_keys: Vec<String> = child_shard
                .parent_shards()
                .iter()
                .map(|p| self.shard_info.lease_key_with_override(p))
                .collect();
            if parent_lease_keys.len() != 2 {
                metrics::add_count(scope, "MissingMergeParent", 1, MetricsLevel::Summary);
                return Err(ShutdownError::InvalidState(format!(
                    "Shard {}'s only child shard {:?} does not contain other parent information.",
                    self.shard_info.shard_id(),
                    child_shard.shard_id()
                )));
            }
            let parent0 = lease_refresher.get_lease(&parent_lease_keys[0]).await?;
            let parent1 = lease_refresher.get_lease(&parent_lease_keys[1]).await?;
            if parent0.is_none() != parent1.is_none() {
                metrics::add_count(scope, "MissingMergeParentLease", 1, MetricsLevel::Summary);
                let message = format!(
                    "Shard {}'s only child shard {:?} has partial parent information in lease table. \
                     Hence deferring lease creation of child shard.",
                    self.shard_info.shard_id(),
                    child_shard.shard_id()
                );
                if (self.one_in_n_probability)(RETRY_RANDOM_MAX_RANGE) {
                    // Abort and drop the lease; lease will be reassigned.
                    return Err(ShutdownError::InvalidState(message));
                } else {
                    // Keep the lease and back off (decreases lease-reassignment churn).
                    return Err(ShutdownError::BlockedOnParentShard(message));
                }
            }
        }

        for child_shard in child_shards {
            let lease_key = self
                .shard_info
                .lease_key_with_override(child_shard.shard_id());
            if lease_refresher.get_lease(&lease_key).await?.is_none() {
                let stream_id = self
                    .shard_detector
                    .stream_identifier()
                    .unwrap_or_else(|_| self.stream_identifier.clone());
                let lease_to_create = (self.child_lease_factory)(child_shard, &stream_id)?;

                let start_time = metrics::current_time_millis();
                let create_result = lease_refresher
                    .create_lease_if_not_exists(&lease_to_create)
                    .await;
                let success = create_result.is_ok();
                metrics::add_success_and_latency_with_dimension(
                    scope,
                    Some("CreateLease"),
                    success,
                    start_time,
                    MetricsLevel::Detailed,
                );
                if let Some(checkpoint) = lease_to_create.checkpoint() {
                    let metric_name = if checkpoint.is_sentinel_checkpoint() {
                        checkpoint.sequence_number().to_string()
                    } else {
                        "SEQUENCE_NUMBER".to_string()
                    };
                    metrics::add_success(
                        scope,
                        Some(&format!("CreateLease_{metric_name}")),
                        true,
                        MetricsLevel::Detailed,
                    );
                }
                create_result?;
                tracing::info!(
                    "Shard {}: Created child shard lease: {}",
                    self.shard_info.shard_id(),
                    lease_key
                );
            }
        }
        Ok(())
    }

    /// Java `updateLeaseWithChildShards`.
    async fn update_lease_with_child_shards(
        &self,
        current_lease: &Lease,
    ) -> Result<(), ShutdownError> {
        let child_shard_ids: HashSet<String> = self
            .child_shards
            .as_deref()
            .unwrap_or(&[])
            .iter()
            .map(|c| c.shard_id().to_string())
            .collect();
        let mut updated_lease = current_lease.copy();
        updated_lease.set_child_shard_ids(child_shard_ids);
        self.lease_coordinator
            .lease_refresher()
            .update_lease_with_meta_info(&updated_lease, UpdateField::ChildShards)
            .await?;
        Ok(())
    }

    /// Java `dropLease`.
    fn drop_lease(&self, current_lease: Option<&Lease>, lease_key: &str) {
        match current_lease {
            None => tracing::warn!(
                "Shard {}: Unable to find the lease for shard. Will shutdown the shardConsumer directly.",
                lease_key
            ),
            Some(lease) => {
                self.lease_coordinator.drop_lease(lease);
                tracing::info!("Dropped lease for shutting down ShardConsumer: {:?}", lease.lease_key());
            }
        }
    }
}

#[async_trait]
impl ConsumerTask for ShutdownTask {
    async fn call(&self) -> TaskResult {
        self.record_processor_checkpointer
            .checkpointer()
            .set_operation(SHUTDOWN_TASK_OPERATION);
        let mut scope = metrics::create_metrics_with_operation(
            self.metrics_factory.as_ref(),
            SHUTDOWN_TASK_OPERATION,
        );

        let result = match self.run(scope.as_mut()).await {
            Ok(()) => TaskResult::new(None),
            Err(e) => {
                if e.downcast_ref::<CustomerApplicationError>().is_some() {
                    tracing::error!(
                        "Shard {}: Application exception. {}",
                        self.shard_info.lease_key(),
                        e
                    );
                } else {
                    tracing::error!(
                        "Shard {}: Caught exception: {}",
                        self.shard_info.lease_key(),
                        e
                    );
                }
                tokio::time::sleep(Duration::from_millis(self.backoff_time_millis.max(0) as u64))
                    .await;
                TaskResult::new(Some(e))
            }
        };

        metrics::end_scope(scope.as_mut());
        result
    }

    fn task_type(&self) -> TaskType {
        TaskType::Shutdown
    }

    fn task_name(&self) -> &'static str {
        "ShutdownTask"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::InitialPositionInStream;
    use crate::leases::shard_detector::MockShardDetector;
    use crate::leases::{MockLeaseCoordinator, MockLeaseRefresher};
    use crate::lifecycle::test_support::RecordingRecordsPublisher;
    use crate::metrics::NullMetricsFactory;
    use crate::processor::{Checkpointer, MockShardRecordProcessor};
    use aws_sdk_kinesis::types::HashKeyRange;
    use std::sync::atomic::{AtomicUsize, Ordering};

    const SHARD_ID: &str = "shardId-0";
    const LEASE_OWNER: &str = "leaseOwner";

    fn stream_identifier() -> StreamIdentifier {
        StreamIdentifier::single_stream_instance("streamName")
    }

    fn shard_info(shard_id: &str) -> ShardInfo {
        ShardInfo::single_stream(
            shard_id,
            Some("concurrencyToken".into()),
            Vec::<String>::new(),
            Some(ExtendedSequenceNumber::latest()),
        )
    }

    fn create_lease(lease_key: &str) -> Lease {
        let mut lease = Lease::default();
        lease.set_lease_key(lease_key);
        lease.set_lease_owner(Some(LEASE_OWNER.to_string()));
        lease.set_checkpoint(ExtendedSequenceNumber::latest());
        lease
    }

    fn hash_key_range(start: &str, end: &str) -> HashKeyRange {
        HashKeyRange::builder()
            .starting_hash_key(start)
            .ending_hash_key(end)
            .build()
            .unwrap()
    }

    fn children_from_split() -> Vec<ChildShard> {
        vec![
            ChildShard::builder()
                .shard_id("ShardId-1")
                .parent_shards(SHARD_ID)
                .hash_key_range(hash_key_range("0", "49"))
                .build()
                .unwrap(),
            ChildShard::builder()
                .shard_id("ShardId-2")
                .parent_shards(SHARD_ID)
                .hash_key_range(hash_key_range("50", "99"))
                .build()
                .unwrap(),
        ]
    }

    fn child_from_merge() -> ChildShard {
        ChildShard::builder()
            .shard_id("shardId-2")
            .parent_shards(SHARD_ID)
            .parent_shards("shardId-1")
            .hash_key_range(hash_key_range("0", "49"))
            .build()
            .unwrap()
    }

    fn checkpointer_seeded(last: ExtendedSequenceNumber) -> Arc<ShardRecordProcessorCheckpointer> {
        let store: Arc<dyn Checkpointer + Send + Sync> =
            Arc::new(crate::checkpoint::in_memory_checkpointer::InMemoryCheckpointer::new());
        let cp = ShardRecordProcessorCheckpointer::new(shard_info(SHARD_ID), store);
        cp.set_initial_checkpoint_value(last);
        cp.set_largest_permitted_checkpoint_value(ExtendedSequenceNumber::latest());
        cp
    }

    /// Records what the mock coordinator/refresher/processor observe.
    struct Harness {
        assign_calls: Arc<AtomicUsize>,
        drop_calls: Arc<AtomicUsize>,
        update_meta_calls: Arc<AtomicUsize>,
        create_lease_calls: Arc<AtomicUsize>,
        shard_ended_calls: Arc<AtomicUsize>,
        lease_lost_calls: Arc<AtomicUsize>,
        get_lease_keys: Arc<Mutex<Vec<String>>>,
    }

    struct BuiltTask {
        task: ShutdownTask,
        cleanup: Arc<LeaseCleanupManager>,
        publisher: Arc<RecordingRecordsPublisher>,
        harness: Harness,
    }

    #[allow(clippy::too_many_arguments)]
    fn build_task(
        reason: ShutdownReason,
        child_shards: Option<Vec<ChildShard>>,
        shard_info_arg: ShardInfo,
        current_lease: Option<Lease>,
        // leases returned by refresher.get_lease, keyed by lease key
        get_lease_map: std::collections::HashMap<String, Lease>,
        worker_id: &str,
        checkpointer: Arc<ShardRecordProcessorCheckpointer>,
        assign_fails: bool,
    ) -> BuiltTask {
        let assign_calls = Arc::new(AtomicUsize::new(0));
        let drop_calls = Arc::new(AtomicUsize::new(0));
        let update_meta_calls = Arc::new(AtomicUsize::new(0));
        let create_lease_calls = Arc::new(AtomicUsize::new(0));
        let shard_ended_calls = Arc::new(AtomicUsize::new(0));
        let lease_lost_calls = Arc::new(AtomicUsize::new(0));
        let get_lease_keys = Arc::new(Mutex::new(Vec::<String>::new()));

        // ---- refresher ----
        let mut refresher = MockLeaseRefresher::new();
        {
            let ac = assign_calls.clone();
            refresher.expect_assign_lease().returning(move |_, _| {
                ac.fetch_add(1, Ordering::SeqCst);
                if assign_fails {
                    Err(LeasingError::dependency("assign failed"))
                } else {
                    Ok(true)
                }
            });
        }
        {
            let keys = get_lease_keys.clone();
            let map = get_lease_map.clone();
            refresher.expect_get_lease().returning(move |k| {
                keys.lock().unwrap().push(k.to_string());
                Ok(map.get(k).cloned())
            });
        }
        {
            let cc = create_lease_calls.clone();
            refresher
                .expect_create_lease_if_not_exists()
                .returning(move |_| {
                    cc.fetch_add(1, Ordering::SeqCst);
                    Ok(true)
                });
        }
        {
            let uc = update_meta_calls.clone();
            refresher
                .expect_update_lease_with_meta_info()
                .returning(move |_, _| {
                    uc.fetch_add(1, Ordering::SeqCst);
                    Ok(())
                });
        }
        let refresher: Arc<dyn crate::leases::LeaseRefresher> = Arc::new(refresher);

        // ---- coordinator ----
        let mut coordinator = MockLeaseCoordinator::new();
        {
            let lease = current_lease.clone();
            coordinator
                .expect_get_currently_held_lease()
                .returning(move |_| lease.clone());
        }
        {
            let r = refresher.clone();
            coordinator
                .expect_lease_refresher()
                .returning(move || r.clone());
        }
        {
            let wid = worker_id.to_string();
            coordinator
                .expect_worker_identifier()
                .returning(move || wid.clone());
        }
        {
            let dc = drop_calls.clone();
            coordinator.expect_drop_lease().returning(move |_| {
                dc.fetch_add(1, Ordering::SeqCst);
            });
        }
        let coordinator: Arc<dyn LeaseCoordinator + Send + Sync> = Arc::new(coordinator);

        // ---- cleanup manager (real, with its own mock coordinator) ----
        let mut cleanup_coord = MockLeaseCoordinator::new();
        cleanup_coord
            .expect_get_currently_held_lease()
            .returning(|_| None);
        let cleanup = Arc::new(LeaseCleanupManager::new(
            Arc::new(cleanup_coord),
            Arc::new(NullMetricsFactory),
            false,
            1000,
            1000,
            1000,
        ));

        // ---- shard detector ----
        let mut detector = MockShardDetector::new();
        detector
            .expect_stream_identifier()
            .returning(|| Ok(stream_identifier()));
        let detector: Arc<dyn ShardDetector> = Arc::new(detector);

        // ---- processor ----
        let mut proc = MockShardRecordProcessor::new();
        {
            let sc = shard_ended_calls.clone();
            proc.expect_shard_ended().returning(move |_| {
                sc.fetch_add(1, Ordering::SeqCst);
            });
        }
        {
            let lc = lease_lost_calls.clone();
            proc.expect_lease_lost().returning(move |_| {
                lc.fetch_add(1, Ordering::SeqCst);
            });
        }
        let processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> =
            Arc::new(Mutex::new(Box::new(proc)));

        let publisher = Arc::new(RecordingRecordsPublisher::new());

        let task = ShutdownTask::new(
            shard_info_arg,
            detector,
            processor,
            checkpointer,
            reason,
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
            false,
            false,
            coordinator,
            1,
            publisher.clone() as Arc<dyn RecordsPublisher>,
            Arc::new(HierarchicalShardSyncer::new()),
            Arc::new(NullMetricsFactory),
            child_shards,
            stream_identifier(),
            cleanup.clone(),
        );

        BuiltTask {
            task,
            cleanup,
            publisher,
            harness: Harness {
                assign_calls,
                drop_calls,
                update_meta_calls,
                create_lease_calls,
                shard_ended_calls,
                lease_lost_calls,
                get_lease_keys,
            },
        }
    }

    fn lease_map(leases: &[Lease]) -> std::collections::HashMap<String, Lease> {
        leases
            .iter()
            .map(|l| (l.lease_key().unwrap().to_string(), l.clone()))
            .collect()
    }

    // ---- tests ----

    #[tokio::test(start_paused = true)]
    async fn call_when_true_shard_end() {
        let lease = create_lease(SHARD_ID);
        let built = build_task(
            ShutdownReason::ShardEnd,
            Some(children_from_split()),
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::shard_end()),
            false,
        );
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.publisher.shutdown_calls(), 1);
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.harness.shard_ended_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.harness.update_meta_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.harness.create_lease_calls.load(Ordering::SeqCst), 2);
        assert_eq!(built.cleanup.pending_deletion_count(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn call_when_application_does_not_checkpoint() {
        // last checkpoint != SHARD_END after shardEnded -> CustomerApplicationError.
        let lease = create_lease(SHARD_ID);
        let built = build_task(
            ShutdownReason::ShardEnd,
            Some(children_from_split()),
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::from_sequence_number("3298")),
            false,
        );
        let result = built.task.call().await;
        let err = result.exception().expect("should error");
        assert!(err.to_string().contains("CustomerApplicationException"));
    }

    #[tokio::test(start_paused = true)]
    async fn call_when_creating_new_leases_throws_downgrades_to_lease_lost() {
        let lease = create_lease(SHARD_ID);
        let mut built = build_task(
            ShutdownReason::ShardEnd,
            Some(children_from_split()),
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::shard_end()),
            false,
        );
        // Inject a throwing child-lease factory (Java mocks createLeaseForChildShard).
        built.task.set_child_lease_factory(Arc::new(|_, _| {
            Err(LeasingError::invalid_state(
                "InvalidStateException is thrown",
            ))
        }));
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.publisher.shutdown_calls(), 1);
        assert_eq!(built.harness.shard_ended_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.harness.lease_lost_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn call_when_shard_not_found_empty_children() {
        let lease = create_lease("shardId-4");
        let si = shard_info("shardId-4");
        let built = build_task(
            ShutdownReason::ShardEnd,
            Some(vec![]),
            si,
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::shard_end()),
            false,
        );
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.publisher.shutdown_calls(), 1);
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.harness.create_lease_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.cleanup.pending_deletion_count(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn call_when_lease_lost() {
        let lease = create_lease(SHARD_ID);
        let built = build_task(
            ShutdownReason::LeaseLost,
            Some(vec![]),
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::latest()),
            false,
        );
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.publisher.shutdown_calls(), 1);
        assert_eq!(built.harness.shard_ended_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.harness.lease_lost_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.harness.create_lease_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 0);
    }

    #[tokio::test(start_paused = true)]
    async fn null_child_shards_still_enqueues() {
        let lease = create_lease(SHARD_ID);
        let built = build_task(
            ShutdownReason::ShardEnd,
            None,
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::shard_end()),
            false,
        );
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.publisher.shutdown_calls(), 1);
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.harness.create_lease_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.cleanup.pending_deletion_count(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn lease_lost_with_shutdown_requested_transfers_and_drops() {
        let mut lease = create_lease(SHARD_ID);
        lease.set_checkpoint_owner(Some(LEASE_OWNER.to_string())); // shutdownRequested == true
        let built = build_task(
            ShutdownReason::LeaseLost,
            Some(vec![]),
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::latest()),
            false,
        );
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.harness.assign_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.publisher.shutdown_calls(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn lease_lost_with_shutdown_requested_drops_even_on_transfer_failure() {
        let mut lease = create_lease(SHARD_ID);
        lease.set_checkpoint_owner(Some(LEASE_OWNER.to_string()));
        let built = build_task(
            ShutdownReason::LeaseLost,
            Some(vec![]),
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::latest()),
            true, // assign fails
        );
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.publisher.shutdown_calls(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn lease_lost_without_shutdown_requested_does_not_transfer_or_drop() {
        let lease = create_lease(SHARD_ID); // no checkpointOwner -> not shutdown-requested
        let built = build_task(
            ShutdownReason::LeaseLost,
            Some(vec![]),
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::latest()),
            false,
        );
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.harness.assign_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.publisher.shutdown_calls(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn merge_child_one_parent_invalid_state_drops_lease() {
        // Only SHARD_ID parent accessible; probability -> InvalidState (abort+downgrade).
        let parent = create_lease(SHARD_ID);
        let mut built = build_task(
            ShutdownReason::ShardEnd,
            Some(vec![child_from_merge()]),
            shard_info(SHARD_ID),
            Some(parent.clone()),
            lease_map(&[parent]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::shard_end()),
            false,
        );
        built.task.set_one_in_n_probability(Arc::new(|_| true)); // invalid-state branch
        let result = built.task.call().await;
        // InvalidState from child-lease creation -> downgrade to LEASE_LOST, drop + leaseLost.
        assert!(result.exception().is_none());
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.harness.lease_lost_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.publisher.shutdown_calls(), 1);
        assert_eq!(built.cleanup.pending_deletion_count(), 0);
    }

    #[tokio::test(start_paused = true)]
    async fn merge_child_one_parent_block_on_parent_keeps_lease() {
        let parent = create_lease(SHARD_ID);
        let mut built = build_task(
            ShutdownReason::ShardEnd,
            Some(vec![child_from_merge()]),
            shard_info(SHARD_ID),
            Some(parent.clone()),
            lease_map(&[parent]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::shard_end()),
            false,
        );
        built.task.set_one_in_n_probability(Arc::new(|_| false)); // block-on-parent branch
        let result = built.task.call().await;
        let err = result.exception().expect("should error");
        assert!(err.to_string().contains("BlockedOnParentShardException"));
        assert_eq!(built.harness.drop_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.harness.lease_lost_calls.load(Ordering::SeqCst), 0);
        assert_eq!(built.publisher.shutdown_calls(), 0);
        assert_eq!(built.cleanup.pending_deletion_count(), 0);
    }

    #[tokio::test(start_paused = true)]
    async fn merge_child_both_parents_have_leases() {
        let parent0 = create_lease(SHARD_ID);
        let parent1 = create_lease("shardId-1");
        let built = build_task(
            ShutdownReason::ShardEnd,
            Some(vec![child_from_merge()]),
            shard_info(SHARD_ID),
            Some(parent0.clone()),
            lease_map(&[parent0, parent1]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::shard_end()),
            false,
        );
        let result = built.task.call().await;
        assert!(result.exception().is_none());
        assert_eq!(built.cleanup.pending_deletion_count(), 1);
        assert_eq!(built.harness.update_meta_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.harness.create_lease_calls.load(Ordering::SeqCst), 1);
        assert_eq!(built.harness.shard_ended_calls.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn get_task_type_and_reason() {
        let lease = create_lease(SHARD_ID);
        let built = build_task(
            ShutdownReason::ShardEnd,
            Some(children_from_split()),
            shard_info(SHARD_ID),
            Some(lease.clone()),
            lease_map(&[lease]),
            LEASE_OWNER,
            checkpointer_seeded(ExtendedSequenceNumber::shard_end()),
            false,
        );
        assert_eq!(built.task.task_type(), TaskType::Shutdown);
        assert_eq!(built.task.reason(), ShutdownReason::ShardEnd);
        // Reference the get_lease-key recorder so the field is exercised.
        let _ = built.harness.get_lease_keys.lock().unwrap().len();
    }
}
