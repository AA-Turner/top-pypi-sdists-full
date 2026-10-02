//! Tests for the Scheduler, focused on the config-driven [`Scheduler::new`]
//! end-to-end construction path (the shape the PyO3 bindings will use).
//!
//! No network I/O: AWS clients are built with a dummy region + test credentials
//! and never actually invoked (construction wires collaborators lazily; the
//! caller would drive `start`/`run`/`shutdown`).

use std::sync::Arc;

use super::*;
use crate::common::ConfigsBuilder;
use crate::processor::shard_record_processor::{MockShardRecordProcessor, ShardRecordProcessor};
use crate::processor::ShardRecordProcessorFactory;

struct TestFactory;

impl ShardRecordProcessorFactory for TestFactory {
    fn shard_record_processor(&self) -> Box<dyn ShardRecordProcessor + Send + Sync> {
        Box::new(MockShardRecordProcessor::new())
    }
}

fn clients() -> (
    aws_sdk_kinesis::Client,
    aws_sdk_dynamodb::Client,
    aws_sdk_cloudwatch::Client,
) {
    let region = "us-east-1";
    let kinesis = aws_sdk_kinesis::Client::from_conf(
        aws_sdk_kinesis::Config::builder()
            .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
            .region(aws_sdk_kinesis::config::Region::new(region))
            .credentials_provider(aws_sdk_kinesis::config::Credentials::for_tests())
            .build(),
    );
    let ddb = aws_sdk_dynamodb::Client::from_conf(
        aws_sdk_dynamodb::Config::builder()
            .behavior_version(aws_sdk_dynamodb::config::BehaviorVersion::latest())
            .region(aws_sdk_dynamodb::config::Region::new(region))
            .credentials_provider(aws_sdk_dynamodb::config::Credentials::for_tests())
            .build(),
    );
    let cw = aws_sdk_cloudwatch::Client::from_conf(
        aws_sdk_cloudwatch::Config::builder()
            .behavior_version(aws_sdk_cloudwatch::config::BehaviorVersion::latest())
            .region(aws_sdk_cloudwatch::config::Region::new(region))
            .credentials_provider(aws_sdk_cloudwatch::config::Credentials::for_tests())
            .build(),
    );
    (kinesis, ddb, cw)
}

fn configs_builder() -> ConfigsBuilder {
    let (kinesis, ddb, cw) = clients();
    ConfigsBuilder::from_stream_name(
        "my-stream",
        "my-app",
        kinesis,
        ddb,
        cw,
        "worker-1",
        Arc::new(TestFactory),
    )
}

/// The headline end-to-end path: `ConfigsBuilder` → 7 configs → `Scheduler::new`
/// → an `Arc<Scheduler>` that can (later) `start`/`run`/`shutdown`.
#[tokio::test]
async fn build_scheduler_from_configs_builder() {
    let cb = configs_builder();
    let scheduler = Scheduler::new(
        cb.checkpoint_config(),
        cb.coordinator_config(),
        cb.lease_management_config(),
        cb.lifecycle_config(),
        cb.metrics_config(),
        cb.processor_config(),
        cb.retrieval_config(),
    )
    .expect("scheduler construction should succeed");

    assert_eq!(scheduler.application_name(), "my-app");
    assert_eq!(scheduler.worker_identifier(), "worker-1");
    // Freshly constructed: nothing tracked, shutdown not complete.
    assert_eq!(scheduler.shard_consumer_count(), 0);
    assert!(!scheduler.shutdown_complete());
    assert!(!scheduler.has_graceful_shutdown_started());
}

/// The production `new` path initializes the lease-assignment mode provider to
/// Java's Phase-1 / 2.x-compatible shape (`initializeClientVersionForPhase1`:
/// dual-mode=false, DEFAULT_LEASE_COUNT_BASED_ASSIGNMENT) so the lease taker
/// starts through the `Ok` path, not the `NotInitialized` error arm.
#[tokio::test]
async fn new_initializes_lease_assignment_mode_provider() {
    let cb = configs_builder();
    let scheduler = Scheduler::new(
        cb.checkpoint_config(),
        cb.coordinator_config(),
        cb.lease_management_config(),
        cb.lifecycle_config(),
        cb.metrics_config(),
        cb.processor_config(),
        cb.retrieval_config(),
    )
    .expect("scheduler construction should succeed");

    let provider = &scheduler.components.lease_assignment_mode_provider;
    assert!(!provider.dynamic_mode_change_support_needed());
    assert_eq!(
        provider.get_lease_assignment_mode(),
        Ok(crate::coordinator::LeaseAssignmentMode::DefaultLeaseCountBasedAssignment)
    );
}

/// The production `new` path constructs the table-migration state machine
/// (driven by `Scheduler::initialize`); the status provider starts UNKNOWN
/// until that initialize runs.
#[tokio::test]
async fn new_wires_table_migration_state_machine() {
    let cb = configs_builder();
    let scheduler = Scheduler::new(
        cb.checkpoint_config(),
        cb.coordinator_config(),
        cb.lease_management_config(),
        cb.lifecycle_config(),
        cb.metrics_config(),
        cb.processor_config(),
        cb.retrieval_config(),
    )
    .expect("scheduler construction should succeed");

    assert!(
        scheduler.components.table_migration_state_machine.is_some(),
        "production Scheduler::new must wire the table migration state machine"
    );
}

/// `shutdown()` on a never-initialized Scheduler is safe and idempotent (does
/// not touch the network — the lease coordinator was never started).
#[tokio::test]
async fn shutdown_without_run_is_safe_and_idempotent() {
    let cb = configs_builder();
    let scheduler = Scheduler::new(
        cb.checkpoint_config(),
        cb.coordinator_config(),
        cb.lease_management_config(),
        cb.lifecycle_config(),
        cb.metrics_config(),
        cb.processor_config(),
        cb.retrieval_config(),
    )
    .expect("scheduler construction should succeed");

    scheduler.shutdown().await;
    assert!(scheduler.should_shutdown());
    // Second shutdown is a no-op (idempotent guard).
    scheduler.shutdown().await;
}

// ---- deleted-stream purge (multi-stream) ----

mod deleted_stream_purge {
    use super::*;
    use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended, StreamConfig};
    use crate::coordinator::leader_decider::MockLeaderDecider;
    use crate::coordinator::stream_info::stream_info_dao::MockStreamInfoStore;
    use crate::coordinator::worker_state_change_listener::NoOpWorkerStateChangeListener;
    use crate::coordinator::{StreamIdOnboardingState, StreamInfoMode};
    use crate::leases::exceptions::LeasingError;
    use crate::leases::shard_prioritization::NoOpShardPrioritization;
    use crate::leases::{Lease, LeaseCleanupManager, MockLeaseCoordinator, MockLeaseRefresher};
    use crate::metrics::NullMetricsFactory;
    use crate::processor::{
        FormerStreamsLeasesDeletionStrategy, NoLeaseDeletionStrategy, StreamTracker,
    };
    use std::collections::HashMap;
    use std::sync::atomic::AtomicBool;
    use std::sync::Mutex as StdMutex;

    /// Multi-stream tracker whose desired set is empty (so a deleted stream is
    /// never "still desired" and always eligible for purge).
    struct EmptyMultiTracker;
    impl StreamTracker for EmptyMultiTracker {
        fn stream_config_list(&self) -> Vec<StreamConfig> {
            Vec::new()
        }
        fn former_streams_leases_deletion_strategy(
            &self,
        ) -> Box<dyn FormerStreamsLeasesDeletionStrategy + Send + Sync> {
            Box::new(NoLeaseDeletionStrategy)
        }
        fn is_multi_stream(&self) -> bool {
            true
        }
    }

    fn stream_config(serialized: &str) -> StreamConfig {
        StreamConfig::new(
            StreamIdentifier::multi_stream_instance(serialized),
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
        )
    }

    /// Build a multi-stream Scheduler over mocks via `from_components`.
    fn multi_stream_scheduler(
        lease_refresher: Arc<dyn LeaseRefresher>,
        tracked: HashMap<StreamIdentifier, StreamConfig>,
    ) -> Arc<Scheduler> {
        let metrics: Arc<dyn MetricsFactory + Send + Sync> = Arc::new(NullMetricsFactory);
        let current_stream_config_map = Arc::new(StdMutex::new(tracked));
        let stream_to_ssm_map = Arc::new(StdMutex::new(HashMap::new()));
        let ssm_provider: ShardSyncTaskManagerProvider =
            Arc::new(|_sc: &StreamConfig| unreachable!("shard sync not exercised"));
        let periodic_shard_sync_manager = PeriodicShardSyncManager::new(
            "worker-1",
            Arc::clone(&lease_refresher),
            Arc::clone(&current_stream_config_map),
            ssm_provider,
            stream_to_ssm_map,
            true,
            Arc::clone(&metrics),
            120_000,
            3,
            Arc::new(AtomicBool::new(false)),
        );
        let mut cleanup_coord = MockLeaseCoordinator::new();
        cleanup_coord
            .expect_get_currently_held_lease()
            .returning(|_| None);
        let lease_cleanup_manager = Arc::new(LeaseCleanupManager::new(
            Arc::new(cleanup_coord),
            Arc::clone(&metrics),
            false,
            60_000,
            60_000,
            60_000,
        ));
        let stream_info_manager = Arc::new(StreamInfoManager::new(
            HashMap::new(),
            Arc::new(MockStreamInfoStore::new()),
            Arc::clone(&metrics),
            true,
            60_000,
            StreamInfoMode::Disabled, // delete_stream_info is a no-op
            StreamIdOnboardingState::NotOnboarded,
        ));
        let components = SchedulerComponents {
            metrics_factory: Arc::clone(&metrics),
            lease_coordinator: Arc::new(MockLeaseCoordinator::new()),
            lease_refresher,
            lease_cleanup_manager,
            periodic_shard_sync_manager,
            leader_decider: Arc::new(MockLeaderDecider::new()),
            stream_info_manager,
            lease_assignment_mode_provider: Arc::new(
                MigrationAdaptiveLeaseAssignmentModeProvider::new(),
            ),
            table_migration_state_machine: None,
            deleted_stream_list_provider: Arc::new(DeletedStreamListProvider::new()),
            worker_state_change_listener: Arc::new(NoOpWorkerStateChangeListener),
            graceful_shutdown_coordinator: GracefulShutdownCoordinator::new(),
            shard_prioritization: Arc::new(NoOpShardPrioritization),
            executor_service: SchedulerExecutorService::SchedulerOwned,
            consumer_provider: Arc::new(|_si: &ShardInfo| {
                unreachable!("consumer provider not exercised")
            }),
            current_stream_config_map,
        };
        let cb = configs_builder();
        Scheduler::from_components(
            cb.checkpoint_config(),
            cb.coordinator_config(),
            cb.lifecycle_config(),
            cb.processor_config(),
            cb.retrieval_config(),
            "worker-1",
            10_000,
            Arc::new(EmptyMultiTracker),
            components,
        )
    }

    fn lease(key: &str) -> Lease {
        Lease::new(
            Some(key.to_string()),
            None,
            0,
            None,
            None,
            None,
            None,
            0,
            Default::default(),
            Default::default(),
            None,
            None,
        )
    }

    fn expire_stream_sync_watch(scheduler: &Scheduler) {
        *scheduler.stream_sync_watch.lock().unwrap() =
            Some(std::time::Instant::now() - std::time::Duration::from_millis(61_000));
    }

    /// Java `Scheduler` deleted-stream drain: a stream recorded by the shard
    /// syncer (ResourceNotFound) is purged from the tracked set and its leases
    /// deleted during the periodic stream sync.
    #[tokio::test]
    async fn purges_deleted_stream_and_deletes_its_leases() {
        let sid = StreamIdentifier::multi_stream_instance("123456789012:deleted-stream:1");
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_list_leases_for_stream()
            .times(1)
            .returning(|_| Ok(vec![lease("123456789012:deleted-stream:1:shardId-0")]));
        refresher
            .expect_delete_lease()
            .times(1)
            .returning(|_| Ok(()));

        let mut tracked = HashMap::new();
        tracked.insert(sid.clone(), stream_config("123456789012:deleted-stream:1"));
        let scheduler = multi_stream_scheduler(Arc::new(refresher), tracked);

        scheduler
            .components
            .deleted_stream_list_provider
            .add(sid.clone());
        expire_stream_sync_watch(&scheduler);

        let synced = scheduler
            .check_and_sync_stream_shards_and_leases()
            .await
            .expect("sync should succeed");

        assert!(
            synced.contains(&sid),
            "the purged stream is reported synced"
        );
        assert!(
            !scheduler
                .current_stream_config_map
                .lock()
                .unwrap()
                .contains_key(&sid),
            "the deleted stream is removed from the tracked set"
        );
        assert!(
            scheduler
                .components
                .deleted_stream_list_provider
                .purge_all_deleted_stream()
                .is_empty(),
            "the provider is drained"
        );
        // The watch was reset: the next pass is gated again.
        assert!(!scheduler.should_sync_streams_now());
    }

    /// A failed lease deletion still removes the stream from the tracked set
    /// (Java removes it up front) but re-enqueues it for retry on the next
    /// sync pass (the port's analogue of Java's `staleStreamDeletionMap`).
    #[tokio::test]
    async fn failed_lease_deletion_is_retried_on_next_pass() {
        let sid = StreamIdentifier::multi_stream_instance("123456789012:deleted-stream:1");
        let mut refresher = MockLeaseRefresher::new();
        refresher
            .expect_list_leases_for_stream()
            .returning(|_| Ok(vec![lease("123456789012:deleted-stream:1:shardId-0")]));
        refresher
            .expect_delete_lease()
            .returning(|_| Err(LeasingError::dependency("ddb down")));

        let mut tracked = HashMap::new();
        tracked.insert(sid.clone(), stream_config("123456789012:deleted-stream:1"));
        let scheduler = multi_stream_scheduler(Arc::new(refresher), tracked);

        scheduler
            .components
            .deleted_stream_list_provider
            .add(sid.clone());
        expire_stream_sync_watch(&scheduler);

        let synced = scheduler
            .check_and_sync_stream_shards_and_leases()
            .await
            .expect("sync itself should not fail");

        assert!(synced.is_empty(), "nothing fully synced");
        assert!(
            !scheduler
                .current_stream_config_map
                .lock()
                .unwrap()
                .contains_key(&sid),
            "the stream is still removed from the tracked set (Java removes first)"
        );
        let requeued = scheduler
            .components
            .deleted_stream_list_provider
            .purge_all_deleted_stream();
        assert!(requeued.contains(&sid), "re-enqueued for the next pass");
    }

    /// `shouldSyncStreamsNow()` gating: unstarted watch → false; started and
    /// past the interval → true; single-stream mode → always false.
    #[tokio::test]
    async fn should_sync_streams_now_gates_the_purge() {
        let scheduler = multi_stream_scheduler(Arc::new(MockLeaseRefresher::new()), HashMap::new());
        // Watch unstarted (initialize() not run): gated.
        assert!(!scheduler.should_sync_streams_now());
        expire_stream_sync_watch(&scheduler);
        assert!(scheduler.should_sync_streams_now());

        // Single-stream (the configs_builder default): never syncs.
        let cb = configs_builder();
        let single = Scheduler::new(
            cb.checkpoint_config(),
            cb.coordinator_config(),
            cb.lease_management_config(),
            cb.lifecycle_config(),
            cb.metrics_config(),
            cb.processor_config(),
            cb.retrieval_config(),
        )
        .unwrap();
        expire_stream_sync_watch(&single);
        assert!(!single.should_sync_streams_now());
        assert!(single
            .check_and_sync_stream_shards_and_leases()
            .await
            .unwrap()
            .is_empty());
    }
}
