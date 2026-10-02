//! Port of `software.amazon.kinesis.coordinator.Scheduler` — the top-level
//! orchestrator of the KCL worker.
//!
//! The Scheduler owns the worker's main loop: it initializes all subsystems
//! (lease coordination, migration state machines, stream tracking), assigns /
//! creates / cleans up [`ShardConsumer`]s per lease, drives periodic multi-stream
//! sync, and manages graceful / forced shutdown.
//!
//! # Structure (deviations from Java)
//!
//! Java's `Scheduler implements Runnable` is a blocking single-threaded loop on a
//! caller-supplied thread that fans work out to numerous thread pools. The Rust
//! port models the Scheduler as a struct owning `Arc`-wrapped collaborators, with:
//!
//! * `new(7 configs)` — the production constructor. It builds the lease
//!   serializer, lease-management factory, coordinator-state DAO, migration state
//!   machines, stream-info manager / cache manager, lease coordinator, periodic
//!   shard-sync manager, lease-cleanup manager, checkpointer, and diagnostic
//!   logger from the configs (matching the Java constructor's wiring).
//! * `from_components(...)` — a dependency-injection constructor taking
//!   pre-built collaborators; used by tests (the Java `@VisibleForTesting`
//!   constructor + Mockito mocks) and by callers wanting to override wiring.
//! * `run()` — `async`: `initialize()` (retried), then loop `run_process_loop()`
//!   until `should_shutdown()`, then `final_shutdown()`. A caller drives this on a
//!   spawned task; `start()` spawns it and returns immediately.
//! * The process loop is a plain `async fn` (not a background OS thread); its
//!   `Thread.sleep(pollInterval)` becomes `tokio::time::sleep`.
//! * Shutdown uses a `shutdown: AtomicBool` flag + the existing count-down latch
//!   machinery; `shutdown()` is idempotent (Java `synchronized(lock)` +
//!   `shutdown` flag).
//!
//! Concurrency: the coarse `synchronized(lock)` around `initialize()`/`shutdown()`
//! becomes a `tokio::sync::Mutex<()>` (`init_lock`); `shardInfoShardConsumerMap`
//! is a `std::sync::Mutex<HashMap<ShardInfo, Arc<ShardConsumer>>>`; the
//! `currentStreamConfigMap` is a `std::sync::Mutex<HashMap<StreamIdentifier,
//! StreamConfig>>`. `shutdown`/`shutdown_complete`/`consumer_id` are atomics /
//! locked fields for cross-task visibility.

use std::collections::{HashMap, HashSet};
use std::sync::atomic::{AtomicBool, AtomicI64, Ordering};
use std::sync::{Arc, Mutex as StdMutex};

use async_trait::async_trait;
use tokio::sync::Mutex as AsyncMutex;

use crate::checkpoint::CheckpointConfig;
use crate::common::{StreamConfig, StreamIdentifier};
use crate::coordinator::coordinator_config::CoordinatorConfig;
use crate::coordinator::coordinator_factory::SchedulerExecutorService;
use crate::coordinator::graceful_shutdown_context::GracefulShutdownContext;
use crate::coordinator::graceful_shutdown_coordinator::{
    GracefulShutdownCoordinator, GracefulShutdownError, SchedulerHandle, StartWorkerShutdown,
};
use crate::coordinator::leader_decider::LeaderDecider;
use crate::coordinator::migration::table_migration_state_machine::TableMigrationStateMachineImpl;
use crate::coordinator::migration::table_migration_status_provider::TableMigrationStatusProvider;
use crate::coordinator::periodic_shard_sync_manager::{
    PeriodicShardSyncManager, ShardSyncTaskManagerProvider,
};
use crate::coordinator::worker_state_change_listener::{WorkerState, WorkerStateChangeListener};
use crate::coordinator::{
    DeletedStreamListProvider, MigrationAdaptiveLeaseAssignmentModeProvider, StreamInfoManager,
};
use crate::leases::lease_management_factory::LeaseManagementFactory;
use crate::leases::{
    Lease, LeaseCleanupManager, LeaseCoordinator, LeaseRefresher, ShardInfo, ShardPrioritization,
    ShardSyncTaskManager,
};
use crate::lifecycle::{
    CountDownLatch, LifecycleConfig, ShardConsumer, ShardConsumerShutdownNotification,
    ShutdownReason,
};
use crate::metrics::{self, MetricsFactory, MetricsLevel};
use crate::processor::{ProcessorConfig, StreamTracker};
use crate::retrieval::RetrievalConfig;
use crate::utils::panic_util;

/// Java `NEW_STREAM_CHECK_INTERVAL_MILLIS`: the periodic multi-stream sync
/// interval (see `check_and_sync_stream_shards_and_leases`).
const NEW_STREAM_CHECK_INTERVAL_MILLIS: i64 = 60_000;
const MIN_WAIT_TIME_FOR_LEASE_TABLE_CHECK_MILLIS: u64 = 1_000;
const MAX_WAIT_TIME_FOR_LEASE_TABLE_CHECK_MILLIS: u64 = 30 * 1000;
const LEASE_TABLE_CHECK_FREQUENCY_MILLIS: u64 = 3 * 1000;

/// A `ShardConsumer` provider: given a [`ShardInfo`], build the consumer for it.
/// Isolates the (large) consumer-construction wiring so the Scheduler's loop
/// logic is testable. The production provider is
/// [`build_consumer`](SchedulerComponents::consumer_provider); tests inject a
/// recording stub.
pub type ConsumerProvider = Arc<
    dyn Fn(&ShardInfo) -> futures::future::BoxFuture<'static, Arc<ShardConsumer>> + Send + Sync,
>;

/// The injected collaborators the Scheduler orchestrates. Groups the pieces so
/// both the production `new` and the test `from_components` paths funnel through
/// one struct.
pub struct SchedulerComponents {
    pub metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    pub lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    pub lease_refresher: Arc<dyn LeaseRefresher>,
    pub lease_cleanup_manager: Arc<LeaseCleanupManager>,
    pub periodic_shard_sync_manager: Arc<PeriodicShardSyncManager>,
    pub leader_decider: Arc<dyn LeaderDecider>,
    pub stream_info_manager: Arc<StreamInfoManager>,
    pub lease_assignment_mode_provider: Arc<MigrationAdaptiveLeaseAssignmentModeProvider>,
    /// The table-consolidation state machine (Java `tableMigrationStateMachine`).
    /// `Some` on the production `new` path — `Scheduler::initialize` drives its
    /// `initialize()` (which enables the CoordinatorStateDAO) and `shutdown()`
    /// stops it. `None` in component-injected tests that don't exercise the
    /// coordinator-state path.
    pub table_migration_state_machine: Option<Arc<TableMigrationStateMachineImpl>>,
    pub deleted_stream_list_provider: Arc<DeletedStreamListProvider>,
    pub worker_state_change_listener: Arc<dyn WorkerStateChangeListener + Send + Sync>,
    pub graceful_shutdown_coordinator: GracefulShutdownCoordinator,
    pub shard_prioritization: Arc<dyn ShardPrioritization + Send + Sync>,
    pub executor_service: SchedulerExecutorService,
    /// Builds a `ShardConsumer` for a shard (the Java `buildConsumer`).
    pub consumer_provider: ConsumerProvider,
    /// The tracked stream configs (Java `currentStreamConfigMap`), **shared**
    /// with the periodic-shard-sync manager and the consumer provider so a
    /// deleted-stream purge is observed by all of them.
    pub current_stream_config_map: Arc<StdMutex<HashMap<StreamIdentifier, StreamConfig>>>,
}

/// Top-level orchestrator. Java `Scheduler`.
pub struct Scheduler {
    checkpoint_config: CheckpointConfig,
    coordinator_config: CoordinatorConfig,
    lifecycle_config: LifecycleConfig,
    processor_config: ProcessorConfig,
    retrieval_config: RetrievalConfig,

    application_name: String,
    worker_identifier: String,
    max_initialization_attempts: i32,
    shard_consumer_dispatch_poll_interval_millis: i64,
    scheduler_initialization_backoff_time_millis: i64,
    failover_time_millis: i64,
    is_multi_stream_mode: bool,
    skip_shard_sync_at_worker_initialization_if_leases_exist: bool,

    components: SchedulerComponents,
    /// The stream tracker (Java `streamTracker`); consulted by the multi-stream
    /// deleted-stream purge for the latest desired stream set.
    stream_tracker: Arc<dyn StreamTracker + Send + Sync>,

    /// Consumers for shards the worker is currently tracking (Java
    /// `shardInfoShardConsumerMap`).
    shard_info_shard_consumer_map: Arc<StdMutex<HashMap<ShardInfo, Arc<ShardConsumer>>>>,
    /// Currently tracked stream configs (Java `currentStreamConfigMap`); an
    /// alias of [`SchedulerComponents::current_stream_config_map`].
    current_stream_config_map: Arc<StdMutex<HashMap<StreamIdentifier, StreamConfig>>>,
    /// Java `streamSyncWatch` (`Stopwatch.createUnstarted()`): `None` until
    /// `initialize()` starts it; reset after each periodic stream sync.
    stream_sync_watch: StdMutex<Option<std::time::Instant>>,

    shutdown: Arc<AtomicBool>,
    shutdown_start_time_millis: AtomicI64,
    shutdown_complete: Arc<AtomicBool>,
    leader_synced: Arc<AtomicBool>,
    consumer_id: StdMutex<String>,

    /// Java `synchronized(lock)` for `initialize`/`shutdown`.
    init_lock: AsyncMutex<()>,
    /// Java `finalShutdownLatch` (final-shutdown done).
    final_shutdown_latch: Arc<CountDownLatch>,
    /// Java `gracefuleShutdownStarted` guard.
    graceful_shutdown_started: AtomicBool,
}

impl Scheduler {
    /// Dependency-injection constructor: build a Scheduler from pre-wired
    /// collaborators (the Java `@VisibleForTesting` constructor path). The
    /// production `new(7 configs)` wraps this after building the components.
    #[allow(clippy::too_many_arguments)]
    pub fn from_components(
        checkpoint_config: CheckpointConfig,
        coordinator_config: CoordinatorConfig,
        lifecycle_config: LifecycleConfig,
        processor_config: ProcessorConfig,
        retrieval_config: RetrievalConfig,
        worker_identifier: impl Into<String>,
        failover_time_millis: i64,
        stream_tracker: Arc<dyn StreamTracker + Send + Sync>,
        components: SchedulerComponents,
    ) -> Arc<Self> {
        let application_name = coordinator_config.application_name().to_string();
        let max_initialization_attempts = coordinator_config.max_initialization_attempts();
        let shard_consumer_dispatch_poll_interval_millis =
            coordinator_config.shard_consumer_dispatch_poll_interval_millis();
        let scheduler_initialization_backoff_time_millis =
            coordinator_config.scheduler_initialization_backoff_time_millis();
        let skip_shard_sync_at_worker_initialization_if_leases_exist =
            coordinator_config.skip_shard_sync_at_worker_initialization_if_leases_exist();
        let is_multi_stream_mode = stream_tracker.is_multi_stream();

        // The tracked stream configs live in `components` (shared with the
        // periodic-shard-sync manager / consumer provider); alias them here.
        let current_stream_config_map = Arc::clone(&components.current_stream_config_map);

        Arc::new(Self {
            checkpoint_config,
            coordinator_config,
            lifecycle_config,
            processor_config,
            retrieval_config,
            application_name,
            worker_identifier: worker_identifier.into(),
            max_initialization_attempts,
            shard_consumer_dispatch_poll_interval_millis,
            scheduler_initialization_backoff_time_millis,
            failover_time_millis,
            is_multi_stream_mode,
            skip_shard_sync_at_worker_initialization_if_leases_exist,
            components,
            stream_tracker,
            shard_info_shard_consumer_map: Arc::new(StdMutex::new(HashMap::new())),
            current_stream_config_map,
            stream_sync_watch: StdMutex::new(None),
            shutdown: Arc::new(AtomicBool::new(false)),
            shutdown_start_time_millis: AtomicI64::new(0),
            shutdown_complete: Arc::new(AtomicBool::new(false)),
            leader_synced: Arc::new(AtomicBool::new(false)),
            consumer_id: StdMutex::new(String::new()),
            init_lock: AsyncMutex::new(()),
            final_shutdown_latch: Arc::new(CountDownLatch::new()),
            graceful_shutdown_started: AtomicBool::new(false),
        })
    }

    /// Config-driven production constructor. Port of the Java
    /// `Scheduler(checkpointConfig, coordinatorConfig, leaseManagementConfig,
    /// lifecycleConfig, metricsConfig, processorConfig, retrievalConfig)`.
    ///
    /// Assembles the runtime collaborators the Java constructor wires — the
    /// metrics factory, the DynamoDB lease-management factory →
    /// `LeaseCoordinator`/`LeaseRefresher`/`LeaseCleanupManager`, the
    /// checkpointer, the retrieval factory, the stream-info / stream-id-cache
    /// managers, the periodic-shard-sync manager, the leader decider, and the
    /// per-shard `ShardConsumer` provider (Java `buildConsumer`) — into a
    /// [`SchedulerComponents`] and delegates to [`from_components`](Self::from_components).
    ///
    /// # Runtime requirement (deviation)
    ///
    /// **This constructor MUST be called from within a tokio runtime.** Two
    /// collaborators capture the current runtime at construction:
    /// [`MetricsConfig::metrics_factory`](crate::metrics::MetricsConfig::metrics_factory)
    /// spawns the CloudWatch publisher task, and the DynamoDB checkpointer
    /// captures [`tokio::runtime::Handle::current`] for its sync→async bridge. No
    /// network I/O is performed during construction — the caller drives
    /// `start`/`run`/`shutdown`.
    ///
    /// # Deviations from the Java wiring
    ///
    /// * The migration state machines (`MigrationStateMachine` /
    ///   `TableMigrationStateMachine`) and their `DynamicMigrationComponentsInitializer`
    ///   are **not** driven here; the runtime process loop consumes the leader
    ///   decider directly. A [`DeterministicShuffleShardSyncLeaderDecider`] is used
    ///   (constructible without a live DynamoDB lock client), matching the
    ///   non-migration default leader-election path.
    /// * The `StreamInfoManager` / `StreamIdCacheManager` are constructed directly
    ///   here (their factory DI entry points are later-wave stubs).
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        checkpoint_config: CheckpointConfig,
        coordinator_config: CoordinatorConfig,
        lease_management_config: crate::leases::lease_management_config::LeaseManagementConfig,
        lifecycle_config: LifecycleConfig,
        metrics_config: crate::metrics::MetricsConfig,
        processor_config: ProcessorConfig,
        mut retrieval_config: RetrievalConfig,
    ) -> Result<Arc<Self>, SchedulerError> {
        use std::collections::HashMap as StdHashMap;

        let stream_tracker: Arc<dyn StreamTracker + Send + Sync> =
            Arc::clone(retrieval_config.stream_tracker());
        let is_multi_stream_mode = stream_tracker.is_multi_stream();
        let worker_identifier = lease_management_config.worker_identifier().to_string();
        let failover_time_millis = lease_management_config.failover_time_millis();

        // Metrics factory (Java `metricsConfig.metricsFactory()`; spawns the
        // CloudWatch publisher — requires a tokio runtime).
        let metrics_factory = metrics_config.metrics_factory();

        // Lease serializer (Java: multi vs single stream).
        let lease_serializer: Arc<dyn crate::leases::LeaseSerializer + Send + Sync> =
            if is_multi_stream_mode {
                Arc::new(crate::leases::dynamodb::DynamoDBMultiStreamLeaseSerializer::new())
            } else {
                Arc::new(crate::leases::dynamodb::DynamoDBLeaseSerializer::new())
            };

        // Lease-management factory (the DI composition root).
        let lease_management_factory = Arc::new(
            crate::leases::dynamodb::DynamoDBLeaseManagementFactory::new(
                &lease_management_config,
                Arc::clone(&lease_serializer),
                is_multi_stream_mode,
            ),
        );

        // Seed the current stream config map (Java constructor).
        let mut initial_stream_config_map: StdHashMap<StreamIdentifier, StreamConfig> =
            StdHashMap::new();
        for sc in stream_tracker.stream_config_list() {
            initial_stream_config_map.insert(sc.stream_identifier().clone(), sc);
        }

        // Coordinator-state DAO (needed by StreamInfoDAO). Uses the leases DDB client.
        // The table-migration status provider is SHARED between the DAO (which
        // routes reads/writes on it) and the TableMigrationStateMachine (which
        // drives it during `Scheduler::initialize`) — Java wires the same
        // instance into both (Scheduler.java constructor).
        let table_migration_status_provider =
            Arc::new(crate::coordinator::migration::DefaultTableMigrationStatusProvider::new());
        let coordinator_state_dao_concrete =
            Arc::new(crate::coordinator::CoordinatorStateDao::new(
                lease_management_config.dynamo_db_client().clone(),
                coordinator_config.coordinator_state_table_config(),
                lease_management_config.table_name().to_string(),
                Arc::clone(&table_migration_status_provider)
                    as Arc<dyn TableMigrationStatusProvider>,
            ));
        // The table-consolidation state machine (Java `tableMigrationStateMachine`).
        // Its `initialize()` runs in `Scheduler::initialize` (network I/O); for a
        // fresh application with no legacy coordinator-state table it resolves
        // COMPLETE in-memory and enables the DAO for reads+writes.
        let table_migration_state_machine = Arc::new(TableMigrationStateMachineImpl::new(
            Arc::clone(&table_migration_status_provider),
            Arc::clone(&coordinator_state_dao_concrete),
            worker_identifier.clone(),
            &coordinator_config,
        ));
        let coordinator_state_dao: Arc<dyn crate::coordinator::CoordinatorStateAccess> =
            coordinator_state_dao_concrete;
        let stream_info_dao: Arc<dyn crate::coordinator::stream_info::StreamInfoStore> =
            Arc::new(crate::coordinator::StreamInfoDAO::new(
                Arc::clone(&coordinator_state_dao),
                lease_management_config.kinesis_client().clone(),
            ));

        // Stream-info / stream-id-cache managers (Java factory entry points;
        // constructed directly here, see deviation).
        let stream_info_manager = Arc::new(StreamInfoManager::new(
            initial_stream_config_map.clone(),
            Arc::clone(&stream_info_dao),
            Arc::clone(&metrics_factory),
            is_multi_stream_mode,
            lease_management_config.shard_sync_interval_millis().max(0) as u64,
            *lease_management_config.stream_info_mode(),
            *lease_management_config.stream_id_onboarding_state(),
        ));
        let stream_id_cache_manager = crate::coordinator::StreamIdCacheManager::new(
            Arc::clone(&stream_info_dao),
            initial_stream_config_map.clone(),
            *lease_management_config.stream_id_onboarding_state(),
            is_multi_stream_mode,
            Arc::clone(&metrics_factory),
        );

        // Lease coordinator (Java `createLeaseCoordinator`).
        let lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync> = Arc::from(
            lease_management_factory
                .create_lease_coordinator_with_cache_manager(
                    Arc::clone(&metrics_factory),
                    StdHashMap::new(),
                    stream_id_cache_manager,
                )
                .map_err(SchedulerError::from)?,
        );
        let lease_refresher: Arc<dyn LeaseRefresher> = lease_coordinator.lease_refresher();

        // Checkpointer (Java `checkpointConfig.checkpointFactory().createCheckpointer(...)`).
        // Captures the current runtime handle for its sync→async bridge.
        let _checkpoint: Arc<dyn crate::processor::Checkpointer + Send + Sync> = Arc::from(
            checkpoint_config
                .checkpoint_factory()
                .create_checkpointer(Arc::clone(&lease_coordinator), Arc::clone(&lease_refresher)),
        );

        // Lease cleanup manager (Java `createLeaseCleanupManager`).
        let lease_cleanup_manager: Arc<LeaseCleanupManager> = Arc::from(
            lease_management_factory.create_lease_cleanup_manager(Arc::clone(&metrics_factory)),
        );

        // Leader decider (Java migration path builds this via the components
        // initializer; the non-migration default is the deterministic-shuffle one,
        // which is constructible without a live DDB lock client).
        let leader_decider: Arc<dyn LeaderDecider> = Arc::new(
            crate::coordinator::DeterministicShuffleShardSyncLeaderDecider::new(
                Arc::clone(&lease_refresher),
                1,
                Arc::clone(&metrics_factory),
            ),
        );

        // Providers + shared maps for the periodic-shard-sync manager (Java
        // `shardSyncTaskManagerProvider` + `streamToShardSyncTaskManagerMap`).
        let current_stream_config_map: Arc<StdMutex<HashMap<StreamIdentifier, StreamConfig>>> =
            Arc::new(StdMutex::new(initial_stream_config_map));
        let stream_to_ssm_map: Arc<StdMutex<HashMap<StreamConfig, Arc<ShardSyncTaskManager>>>> =
            Arc::new(StdMutex::new(HashMap::new()));
        let leader_synced = Arc::new(AtomicBool::new(false));

        // ONE shared provider: the shard syncers record deleted streams into it
        // and the Scheduler purges it during the periodic stream sync (Java
        // wires `this.deletedStreamListProvider` into every syncer).
        let deleted_stream_list_provider = Arc::new(DeletedStreamListProvider::new());

        let ssm_provider: ShardSyncTaskManagerProvider = {
            let factory = Arc::clone(&lease_management_factory);
            let mf = Arc::clone(&metrics_factory);
            let map = Arc::clone(&stream_to_ssm_map);
            let deleted_streams = Arc::clone(&deleted_stream_list_provider);
            Arc::new(move |stream_config: &StreamConfig| {
                let mut guard = map.lock().unwrap();
                if let Some(existing) = guard.get(stream_config) {
                    return Arc::clone(existing);
                }
                let ssm: Arc<ShardSyncTaskManager> = Arc::from(
                    factory
                        .create_shard_sync_task_manager_with_deleted_streams(
                            Arc::clone(&mf),
                            stream_config.clone(),
                            Arc::clone(&deleted_streams),
                        )
                        .expect("shard sync task manager construction"),
                );
                guard.insert(stream_config.clone(), Arc::clone(&ssm));
                ssm
            })
        };

        let periodic_shard_sync_manager = PeriodicShardSyncManager::new(
            worker_identifier.clone(),
            Arc::clone(&lease_refresher),
            Arc::clone(&current_stream_config_map),
            ssm_provider,
            Arc::clone(&stream_to_ssm_map),
            is_multi_stream_mode,
            Arc::clone(&metrics_factory),
            lease_management_config.leases_recovery_auditor_execution_frequency_millis(),
            lease_management_config.leases_recovery_auditor_inconsistency_confidence_threshold(),
            Arc::clone(&leader_synced),
        );

        // Worker-state-change listener + graceful-shutdown coordinator + executor.
        let worker_state_change_listener =
            Arc::clone(coordinator_config.worker_state_change_listener());
        let graceful_shutdown_coordinator = coordinator_config
            .coordinator_factory()
            .create_graceful_shutdown_coordinator();
        let executor_service = coordinator_config
            .coordinator_factory()
            .create_executor_service();
        let shard_prioritization = Arc::clone(coordinator_config.shard_prioritization());

        // The per-shard `ShardConsumer` provider (Java `buildConsumer`).
        let consumer_provider = build_consumer_provider(ConsumerProviderDeps {
            coordinator_factory: Arc::clone(coordinator_config.coordinator_factory()),
            checkpoint: Arc::clone(&_checkpoint),
            lease_coordinator: Arc::clone(&lease_coordinator),
            lease_management_factory: Arc::clone(&lease_management_factory),
            lease_cleanup_manager: Arc::clone(&lease_cleanup_manager),
            retrieval_factory: {
                // Materialize + own the retrieval factory (Java `retrievalConfig.retrievalFactory()`).
                let _ = retrieval_config.retrieval_factory();
                retrieval_config
                    .retrieval_specific_config()
                    .expect("retrieval specific config set")
                    .retrieval_factory()
                    .into()
            },
            metrics_factory: Arc::clone(&metrics_factory),
            aggregator_util: Arc::clone(lifecycle_config.aggregator_util()),
            stream_tracker: Arc::clone(&stream_tracker),
            processor_factory: Arc::clone(processor_config.shard_record_processor_factory()),
            current_stream_config_map: Arc::clone(&current_stream_config_map),
            consumer_task_factory: Arc::new(
                lease_management_config.consumer_task_factory().clone(),
            ),
            log_warning_for_task_after_millis: lifecycle_config.log_warning_for_task_after_millis(),
            task_execution_listener: Arc::clone(lifecycle_config.task_execution_listener()),
            read_timeouts_to_ignore_before_warning: lifecycle_config
                .read_timeouts_to_ignore_before_warning(),
            parent_shard_poll_interval_millis: coordinator_config
                .parent_shard_poll_interval_millis(),
            task_backoff_time_millis: lifecycle_config.task_backoff_time_millis(),
            skip_shard_sync_at_worker_initialization_if_leases_exist: coordinator_config
                .skip_shard_sync_at_worker_initialization_if_leases_exist(),
            list_shards_backoff_time_in_millis: retrieval_config
                .list_shards_backoff_time_in_millis(),
            max_list_shards_retry_attempts: retrieval_config.max_list_shards_retry_attempts(),
            should_call_process_records_even_for_empty_record_list: processor_config
                .call_process_records_even_for_empty_record_list(),
            shard_consumer_dispatch_poll_interval_millis: coordinator_config
                .shard_consumer_dispatch_poll_interval_millis(),
            cleanup_leases_upon_shard_completion: lease_management_config
                .cleanup_leases_upon_shard_completion(),
            ignore_unexpected_child_shards: lease_management_config
                .ignore_unexpected_child_shards(),
        });

        // Lease-assignment mode: the port wires the deterministic-shuffle leader
        // decider and does NOT run the LeaseAssignmentManager / worker-metrics
        // machinery, which is Java's "Phase 1" / 2.x-compatible shape
        // (`DynamicMigrationComponentsInitializer.initializeClientVersionForPhase1`:
        // `initialize(false, DEFAULT_LEASE_COUNT_BASED_ASSIGNMENT)`). Initialize
        // the provider explicitly so the taker starts through the Ok path rather
        // than as an accident of the NotInitialized error arm. See the PORTING.md
        // decisions-log entry on the un-wired migration/LAM machinery.
        let lease_assignment_mode_provider =
            Arc::new(MigrationAdaptiveLeaseAssignmentModeProvider::new());
        lease_assignment_mode_provider.initialize(
            false,
            crate::coordinator::LeaseAssignmentMode::DefaultLeaseCountBasedAssignment,
        );

        let components = SchedulerComponents {
            metrics_factory,
            lease_coordinator,
            lease_refresher,
            lease_cleanup_manager,
            periodic_shard_sync_manager,
            leader_decider,
            stream_info_manager,
            lease_assignment_mode_provider,
            table_migration_state_machine: Some(table_migration_state_machine),
            deleted_stream_list_provider,
            worker_state_change_listener,
            graceful_shutdown_coordinator,
            shard_prioritization,
            executor_service,
            consumer_provider,
            current_stream_config_map,
        };

        Ok(Self::from_components(
            checkpoint_config,
            coordinator_config,
            lifecycle_config,
            processor_config,
            retrieval_config,
            worker_identifier,
            failover_time_millis,
            stream_tracker,
            components,
        ))
    }

    // ---- accessors (Java fluent @Getter) ----

    pub fn application_name(&self) -> &str {
        &self.application_name
    }

    pub fn worker_identifier(&self) -> &str {
        &self.worker_identifier
    }

    pub fn checkpoint_config(&self) -> &CheckpointConfig {
        &self.checkpoint_config
    }

    pub fn coordinator_config(&self) -> &CoordinatorConfig {
        &self.coordinator_config
    }

    pub fn lifecycle_config(&self) -> &LifecycleConfig {
        &self.lifecycle_config
    }

    pub fn processor_config(&self) -> &ProcessorConfig {
        &self.processor_config
    }

    pub fn retrieval_config(&self) -> &RetrievalConfig {
        &self.retrieval_config
    }

    pub fn lease_coordinator(&self) -> &Arc<dyn LeaseCoordinator + Send + Sync> {
        &self.components.lease_coordinator
    }

    /// Java `shutdownComplete()`.
    pub fn shutdown_complete(&self) -> bool {
        self.shutdown_complete.load(Ordering::SeqCst)
    }

    /// Java `hasGracefulShutdownStarted()`.
    pub fn has_graceful_shutdown_started(&self) -> bool {
        self.graceful_shutdown_started.load(Ordering::SeqCst)
    }

    /// Number of shard consumers currently tracked (test/diagnostic).
    pub fn shard_consumer_count(&self) -> usize {
        self.shard_info_shard_consumer_map.lock().unwrap().len()
    }

    // ---- the main loop ----

    /// Spawn the worker loop on a tokio task and return immediately. The join
    /// handle completes when the loop exits (after final shutdown).
    pub fn start(self: &Arc<Self>) -> tokio::task::JoinHandle<()> {
        let this = Arc::clone(self);
        tokio::spawn(async move { this.run().await })
    }

    /// Java `run()`: initialize (retried), then loop the process loop until
    /// `should_shutdown()`, then final shutdown.
    pub async fn run(self: &Arc<Self>) {
        if self.shutdown.load(Ordering::SeqCst) {
            return;
        }

        let mut scope = metrics::create_metrics_with_operation(
            self.components.metrics_factory.as_ref(),
            "Scheduler:Initialize",
        );
        let init_result = self.initialize().await;
        let success = init_result.is_ok();
        if let Err(e) = init_result {
            tracing::error!(
                "Unable to initialize after {} attempts. Shutting down: {e}",
                self.max_initialization_attempts
            );
            self.components
                .worker_state_change_listener
                .on_all_initialization_attempts_failed(Box::new(e));
            self.shutdown().await;
        } else {
            tracing::info!("Initialization complete. Starting worker loop.");
        }
        metrics::add_success(
            scope.as_mut(),
            Some("Initialize"),
            success,
            MetricsLevel::Summary,
        );
        metrics::end_scope(scope.as_mut());

        while !self.should_shutdown() {
            self.run_process_loop().await;
        }

        self.final_shutdown().await;
        tracing::info!("Worker loop is complete. Exiting from worker.");
    }

    /// Java `initialize()` (synchronized on `lock`): retry loop bringing up the
    /// lease coordinator, migration state machines, stream-id cache, lease
    /// cleanup, and periodic shard sync.
    ///
    /// # Deviation
    ///
    /// Performs the lease-coordinator bring-up, the **table**-migration
    /// state-machine initialize (enabling the CoordinatorStateDAO), and the
    /// periodic-shard-sync + lease-cleanup bring-up, faithful to the Java
    /// ordering. The **client-version** migration state machine
    /// (`migrationStateMachine.initialize()` in Java) is NOT wired — the worker
    /// runs Java's Phase-1 / 2.x-compatible shape (see the PORTING.md
    /// decisions-log entry on the un-wired migration/LAM machinery).
    pub async fn initialize(self: &Arc<Self>) -> Result<(), SchedulerError> {
        let _guard = self.init_lock.lock().await;
        self.components
            .worker_state_change_listener
            .on_worker_state_change(WorkerState::Initializing);

        let mut last_error: Option<SchedulerError> = None;
        let mut done = false;
        for attempt in 0..self.max_initialization_attempts {
            tracing::info!("Initializing LeaseCoordinator attempt {}", attempt + 1);
            match self.try_initialize().await {
                Ok(()) => {
                    done = true;
                    break;
                }
                Err(e) => {
                    tracing::error!("Caught exception when initializing LeaseCoordinator: {e}");
                    last_error = Some(e);
                    // Back off, then stop the periodic sync / stream-info managers
                    // before retrying (Java sleep + stop).
                    tokio::time::sleep(std::time::Duration::from_millis(
                        self.scheduler_initialization_backoff_time_millis.max(0) as u64,
                    ))
                    .await;
                    self.components.periodic_shard_sync_manager.stop().await;
                    self.components.stream_info_manager.stop(false);
                }
            }
        }

        if !done {
            return Err(
                last_error.unwrap_or_else(|| SchedulerError("initialization failed".to_string()))
            );
        }
        *self.consumer_id.lock().unwrap() = self.components.lease_coordinator.get_consumer_id();
        self.components
            .worker_state_change_listener
            .on_worker_state_change(WorkerState::Started);
        Ok(())
    }

    /// A single initialization attempt (Java's per-iteration body).
    async fn try_initialize(self: &Arc<Self>) -> Result<(), SchedulerError> {
        self.components
            .lease_coordinator
            .initialize()
            .await
            .map_err(SchedulerError::from)?;

        // Initialize the table migration state machine first (Java ordering). This:
        // 1. Calls coordinatorStateDAO.initializeDelegates() (legacy checks table existence)
        // 2. Determines TableMigrationStatus and sets the TableMigrationStatusProvider
        // 3. Calls coordinatorStateDAO.initialize() to enable writes
        // After this, CoordinatorStateDAO is fully operational for reads and writes.
        if let Some(sm) = &self.components.table_migration_state_machine {
            sm.initialize()
                .await
                .map_err(|e| SchedulerError(format!("TableMigrationStateMachine: {e}")))?;
        }

        // shard-sync-at-init decision (Java `skipShardSyncAtWorkerInitializationIfLeasesExist`).
        let lease_table_empty = self
            .components
            .lease_refresher
            .is_lease_table_empty()
            .await
            .map_err(SchedulerError::from)?;
        if !self.skip_shard_sync_at_worker_initialization_if_leases_exist || lease_table_empty {
            if self.should_initiate_lease_sync().await?
                && self
                    .components
                    .leader_decider
                    .is_leader(&self.worker_identifier)
            {
                tracing::info!(
                    "Worker {} is initiating the lease sync.",
                    self.worker_identifier
                );
                self.components
                    .periodic_shard_sync_manager
                    .sync_shards_once()
                    .await
                    .map_err(|e| SchedulerError(e.to_string()))?;
            }
        } else {
            tracing::info!("Skipping shard sync per configuration (lease table not empty)");
        }

        self.components.lease_cleanup_manager.start();

        if !self.components.lease_coordinator.is_running() {
            tracing::info!("Starting LeaseCoordinator");
            self.components
                .lease_coordinator
                .start(Arc::clone(&self.components.lease_assignment_mode_provider))
                .await
                .map_err(SchedulerError::from)?;
        } else {
            tracing::info!("LeaseCoordinator is already running.");
        }
        tracing::info!("Scheduling periodicShardSync");
        self.components
            .periodic_shard_sync_manager
            .start(Arc::clone(&self.components.leader_decider))
            .await;
        // Java: `streamSyncWatch.start()`.
        self.stream_sync_watch
            .lock()
            .unwrap()
            .get_or_insert_with(std::time::Instant::now);
        Ok(())
    }

    /// Java `shouldInitiateLeaseSync()`: randomized bounded wait, polling every 3s
    /// while the lease table is still empty (minimizes bootstrap contention).
    async fn should_initiate_lease_sync(self: &Arc<Self>) -> Result<bool, SchedulerError> {
        let wait_time = {
            use rand::RngExt;
            rand::rng().random_range(
                MIN_WAIT_TIME_FOR_LEASE_TABLE_CHECK_MILLIS
                    ..MAX_WAIT_TIME_FOR_LEASE_TABLE_CHECK_MILLIS,
            )
        };
        let deadline = std::time::Instant::now() + std::time::Duration::from_millis(wait_time);
        let mut should_initiate = true;
        while std::time::Instant::now() < deadline {
            should_initiate = self
                .components
                .lease_refresher
                .is_lease_table_empty()
                .await
                .map_err(SchedulerError::from)?;
            if !should_initiate {
                break;
            }
            tracing::info!("Lease table is still empty. Checking again shortly.");
            tokio::time::sleep(std::time::Duration::from_millis(
                LEASE_TABLE_CHECK_FREQUENCY_MILLIS,
            ))
            .await;
        }
        Ok(should_initiate)
    }

    /// Java `runProcessLoop()`: create/reuse a `ShardConsumer` per assigned shard,
    /// drop stale-but-held leases, execute each consumer's lifecycle, clean up
    /// unassigned consumers, and (if leader) sync streams. Never propagates —
    /// catches errors and sleeps (matching Java's "never crash the loop").
    pub async fn run_process_loop(self: &Arc<Self>) {
        // Java Scheduler#runProcessLoop catch(Exception): a panicking pass must
        // not kill the worker loop — log and sleep exactly like the Err path.
        match panic_util::catch_tick(self.run_process_loop_inner()).await {
            Ok(Ok(())) => {}
            Ok(Err(e)) => tracing::error!(
                "Worker.run caught exception, sleeping for {} ms: {e}",
                self.shard_consumer_dispatch_poll_interval_millis
            ),
            Err(panic_msg) => tracing::error!(
                "Worker.run caught exception, sleeping for {} ms: {panic_msg}",
                self.shard_consumer_dispatch_poll_interval_millis
            ),
        }
        tokio::time::sleep(std::time::Duration::from_millis(
            self.shard_consumer_dispatch_poll_interval_millis.max(0) as u64,
        ))
        .await;
    }

    async fn run_process_loop_inner(self: &Arc<Self>) -> Result<(), SchedulerError> {
        let mut assigned_shards: HashSet<ShardInfo> = HashSet::new();
        for shard_info in self.get_shard_info_for_assignments() {
            let consumer = self.create_or_get_shard_consumer(&shard_info).await;
            // Drop a lease that is shut down (non-SHARD_END) but still held, so
            // the heartbeat stops and it gets cleaned up next round.
            if consumer.is_shutdown()
                && consumer.shutdown_reason().await != Some(ShutdownReason::ShardEnd)
            {
                let lease_key = shard_info.lease_key();
                if let Some(current_lease) = self
                    .components
                    .lease_coordinator
                    .get_currently_held_lease(&lease_key)
                {
                    let token_matches = match (
                        shard_info.concurrency_token(),
                        current_lease.concurrency_token(),
                    ) {
                        (Some(si_tok), Some(lease_tok)) => si_tok == lease_tok.to_string(),
                        _ => false,
                    };
                    if token_matches {
                        tracing::warn!(
                            "Unexpected that lease is shutdown but still held. Stop heartbeat {}",
                            lease_key
                        );
                        self.components.lease_coordinator.drop_lease(&current_lease);
                    }
                }
            }
            consumer.execute_lifecycle().await;
            assigned_shards.insert(shard_info);
        }

        self.cleanup_shard_consumers(&assigned_shards).await;

        if self.is_leader() {
            self.check_and_sync_stream_shards_and_leases().await?;
            self.leader_synced.store(true, Ordering::SeqCst);
            self.components.stream_info_manager.start();
        } else {
            self.leader_synced.store(false, Ordering::SeqCst);
            self.components.stream_info_manager.stop(false);
        }
        Ok(())
    }

    fn is_leader(&self) -> bool {
        self.components
            .leader_decider
            .is_leader(&self.worker_identifier)
    }

    fn get_shard_info_for_assignments(&self) -> Vec<ShardInfo> {
        let assigned = self.components.lease_coordinator.get_current_assignments();
        self.components.shard_prioritization.prioritize(assigned)
    }

    /// Java `createOrGetShardConsumer`: reuse the tracked consumer unless absent
    /// or shut down with `LEASE_LOST` (in which case rebuild).
    pub async fn create_or_get_shard_consumer(
        self: &Arc<Self>,
        shard_info: &ShardInfo,
    ) -> Arc<ShardConsumer> {
        let existing = {
            let map = self.shard_info_shard_consumer_map.lock().unwrap();
            map.get(shard_info).cloned()
        };
        if let Some(consumer) = existing {
            let rebuild = consumer.is_shutdown()
                && consumer.shutdown_reason().await == Some(ShutdownReason::LeaseLost);
            if !rebuild {
                return consumer;
            }
        }
        let consumer = (self.components.consumer_provider)(shard_info).await;
        self.shard_info_shard_consumer_map
            .lock()
            .unwrap()
            .insert(shard_info.clone(), Arc::clone(&consumer));
        tracing::info!("Created new shardConsumer for: {}", shard_info.lease_key());
        consumer
    }

    /// Java `cleanupShardConsumers`: shut down consumers whose shards are no
    /// longer assigned; drop those that lost their lease.
    pub async fn cleanup_shard_consumers(self: &Arc<Self>, assigned_shards: &HashSet<ShardInfo>) {
        let tracked: Vec<ShardInfo> = {
            let map = self.shard_info_shard_consumer_map.lock().unwrap();
            map.keys().cloned().collect()
        };
        for shard in tracked {
            if assigned_shards.contains(&shard) {
                continue;
            }
            let consumer = {
                let map = self.shard_info_shard_consumer_map.lock().unwrap();
                map.get(&shard).cloned()
            };
            let consumer = match consumer {
                Some(c) => c,
                None => continue,
            };
            if consumer.lease_lost().await {
                self.shard_info_shard_consumer_map
                    .lock()
                    .unwrap()
                    .remove(&shard);
                tracing::debug!(
                    "Removed consumer for {} as lease has been lost",
                    shard.lease_key()
                );
            } else {
                consumer.execute_lifecycle().await;
            }
        }
        self.cleanup_stream_id_cache();
    }

    /// Java `cleanupStreamIdCache`: (multi-stream only) drop cached stream ids the
    /// worker no longer owns a shard for. Best-effort.
    fn cleanup_stream_id_cache(&self) {
        // Multi-stream only. The stream-id cache-manager cleanup mirrors Java,
        // but is a non-critical, best-effort operation; leaving it to the cache
        // manager's own cleanup is acceptable (Java swallows all errors here).
        // Non-multi-stream mode has nothing to clean up. See TEST-PARITY GAPS.
        let _ = self.is_multi_stream_mode;
    }

    /// Java `shouldSyncStreamsNow()`: multi-stream mode and the periodic
    /// stream-sync interval has elapsed (the watch is unstarted until
    /// `initialize()`).
    fn should_sync_streams_now(&self) -> bool {
        if !self.is_multi_stream_mode {
            return false;
        }
        match *self.stream_sync_watch.lock().unwrap() {
            Some(started) => {
                started.elapsed().as_millis() as i64 > NEW_STREAM_CHECK_INTERVAL_MILLIS
            }
            None => false,
        }
    }

    /// Java `checkAndSyncStreamShardsAndLeases` (multi-stream reconciliation).
    ///
    /// # Deviation
    ///
    /// The full multi-stream reconciliation (new-stream onboarding, the
    /// former-streams-leases deferred-deletion strategies and their
    /// `staleStreamDeletionMap`) is large and remains a later-wave gap (tracked
    /// in TEST-PARITY GAPS). What IS ported is the **deleted-stream
    /// consumption** (Java `Scheduler.java`, the `deletedStreamListProvider`
    /// drain): streams the shard syncer found deleted in Kinesis
    /// (ResourceNotFound) are purged from the tracked stream set and their
    /// leases deleted, so a deleted stream stops sync-erroring and its leases
    /// get cleaned up. Single-stream mode is a no-op (`shouldSyncStreamsNow()`
    /// is false), matching Java (the provider is only populated in
    /// multi-stream mode).
    async fn check_and_sync_stream_shards_and_leases(
        self: &Arc<Self>,
    ) -> Result<HashSet<StreamIdentifier>, SchedulerError> {
        let mut streams_synced: HashSet<StreamIdentifier> = HashSet::new();
        if !self.should_sync_streams_now() {
            return Ok(streams_synced);
        }

        // Java: `newStreamConfigMap = streamTracker.streamConfigList()` — the
        // latest desired set; deleted streams still desired by the tracker are
        // never purged ("don't override input to KCL in any case").
        let new_stream_config_set: HashSet<StreamIdentifier> = self
            .stream_tracker
            .stream_config_list()
            .iter()
            .map(|sc| sc.stream_identifier().clone())
            .collect();

        let deleted_stream_set: HashSet<StreamIdentifier> = self
            .components
            .deleted_stream_list_provider
            .purge_all_deleted_stream()
            .into_iter()
            .filter(|sid| !new_stream_config_set.contains(sid))
            .collect();
        if !deleted_stream_set.is_empty() {
            tracing::info!("Stale streams to delete: {:?}", deleted_stream_set);
            let deleted = self.delete_multi_stream_leases(&deleted_stream_set).await;
            streams_synced.extend(deleted);
        }

        // Java: `streamSyncWatch.reset().start()`.
        *self.stream_sync_watch.lock().unwrap() = Some(std::time::Instant::now());
        Ok(streams_synced)
    }

    /// Java `deleteMultiStreamLeases(streamIdentifiers)`: for each deleted
    /// stream, remove it from the tracked stream set (so the periodic shard
    /// sync stops treating its shards as holes) and delete its leases (which
    /// makes workers shut down the record processors for those shards).
    ///
    /// Deviation: Java re-enqueues failed deletions via `staleStreamDeletionMap`
    /// (not ported); here the stream is re-added to the
    /// `DeletedStreamListProvider` so the next sync pass retries.
    async fn delete_multi_stream_leases(
        self: &Arc<Self>,
        stream_identifiers: &HashSet<StreamIdentifier>,
    ) -> HashSet<StreamIdentifier> {
        let mut streams_synced = HashSet::new();
        if stream_identifiers.is_empty() {
            return streams_synced;
        }
        tracing::info!("Deleting streams: {:?}", stream_identifiers);
        for stream_identifier in stream_identifiers {
            tracing::warn!(
                "Found old/deleted stream: {}. Directly deleting leases of this stream.",
                stream_identifier
            );
            // Removing the stream first so the PSSM doesn't think there is a
            // hole in the stream while deletion is in progress (Java comment).
            self.current_stream_config_map
                .lock()
                .unwrap()
                .remove(stream_identifier);

            let all_deleted = match self
                .components
                .lease_refresher
                .list_leases_for_stream(stream_identifier)
                .await
            {
                Ok(leases) => {
                    let mut ok = true;
                    for lease in &leases {
                        if let Err(e) = self.components.lease_refresher.delete_lease(lease).await {
                            tracing::error!(
                                "Unable to delete stale stream lease {}. Skipping further \
                                 deletions for this stream. Will retry later. {e}",
                                lease.lease_key().unwrap_or_default()
                            );
                            ok = false;
                            break;
                        }
                    }
                    ok
                }
                Err(e) => {
                    tracing::error!(
                        "Unable to list leases for deleted stream {stream_identifier}. \
                         Will retry later. {e}"
                    );
                    false
                }
            };

            if all_deleted {
                if let Err(e) = self
                    .components
                    .stream_info_manager
                    .delete_stream_info(stream_identifier)
                    .await
                {
                    tracing::warn!("Unable to delete stream info for {stream_identifier}: {e}");
                }
                streams_synced.insert(stream_identifier.clone());
            } else {
                // Retry on the next sync pass (see the deviation note above).
                self.components
                    .deleted_stream_list_provider
                    .add(stream_identifier.clone());
            }
        }
        streams_synced
    }

    /// Java `shouldShutdown()`: called before each loop; returns whether the
    /// worker should stop immediately.
    pub fn should_shutdown(&self) -> bool {
        if self.shutdown.load(Ordering::SeqCst) {
            if self
                .shard_info_shard_consumer_map
                .lock()
                .unwrap()
                .is_empty()
            {
                tracing::info!("All record processors have been shutdown successfully.");
                return true;
            }
            let now = now_millis();
            if now - self.shutdown_start_time_millis.load(Ordering::SeqCst)
                >= self.failover_time_millis
            {
                tracing::info!("Lease failover time is reached, so forcing shutdown.");
                return true;
            }
        }
        false
    }

    /// Java `shutdown()` (synchronized on `lock`, idempotent): signal shutdown,
    /// tear down the migration components, entity DAO, lease coordinator, lease
    /// cleanup manager, periodic shard sync manager, and stream-info managers.
    pub async fn shutdown(self: &Arc<Self>) {
        let _guard = self.init_lock.lock().await;
        if self.shutdown.swap(true, Ordering::SeqCst) {
            tracing::warn!("Shutdown requested a second time.");
            return;
        }
        self.components
            .worker_state_change_listener
            .on_worker_state_change(WorkerState::ShutDownStarted);
        tracing::info!("Worker shutdown requested.");
        self.shutdown_start_time_millis
            .store(now_millis(), Ordering::SeqCst);

        // Stop lease coordinator so leases are not renewed/stolen; lost leases
        // force the loop to shut down each consumer.
        self.components.lease_coordinator.stop().await;
        // Stop the lease cleanup manager.
        self.components.lease_cleanup_manager.shutdown();
        self.components.periodic_shard_sync_manager.stop().await;
        // Java `finalShutdown()` stops the table migration state machine
        // (cancels any in-flight async entity move; no network I/O).
        if let Some(sm) = &self.components.table_migration_state_machine {
            sm.shutdown().await;
        }
        self.components
            .worker_state_change_listener
            .on_worker_state_change(WorkerState::ShutDown);
        self.components.stream_info_manager.stop(true);
    }

    /// Java `finalShutdown()`: force-shut-down the internal executor (only if
    /// Scheduler-owned) and the metrics factory, mark shutdown complete, count
    /// down the final latch.
    async fn final_shutdown(self: &Arc<Self>) {
        tracing::info!("Starting worker's final shutdown.");
        if self.components.executor_service.is_scheduler_owned() {
            // Scheduler-owned executor: in the tokio model, ShardConsumer tasks
            // are torn down as their consumers complete; nothing to force here.
        }
        // A CloudWatch/Otel metrics factory shutdown would happen here; the
        // factory is held as a trait object and shut down by its owner.
        self.shutdown_complete.store(true, Ordering::SeqCst);
        self.final_shutdown_latch.count_down();
    }

    // ---- graceful shutdown ----

    /// Java `startGracefulShutdown()`: request a graceful shutdown, returning a
    /// receiver resolving to the outcome. Idempotent-ish: each call starts a fresh
    /// callable (the Java single-future guard is simplified here — callers
    /// typically call once).
    pub fn start_graceful_shutdown(
        self: &Arc<Self>,
    ) -> tokio::sync::oneshot::Receiver<Result<bool, GracefulShutdownError>> {
        let callable = self.create_worker_shutdown_callable();
        self.components
            .graceful_shutdown_coordinator
            .start_graceful_shutdown(callable)
    }

    /// Java `createWorkerShutdownCallable()`: builds the callable that stops
    /// lease-taking, notifies each held lease's consumer, and returns the
    /// [`GracefulShutdownContext`].
    fn create_worker_shutdown_callable(self: &Arc<Self>) -> StartWorkerShutdown {
        let this = Arc::clone(self);
        Box::new(move || {
            Box::pin(async move { this.begin_worker_shutdown().await })
                as futures::future::BoxFuture<
                    'static,
                    Result<GracefulShutdownContext, GracefulShutdownError>,
                >
        })
    }

    async fn begin_worker_shutdown(
        self: &Arc<Self>,
    ) -> Result<GracefulShutdownContext, GracefulShutdownError> {
        if self.graceful_shutdown_started.swap(true, Ordering::SeqCst) {
            return Err(GracefulShutdownError(
                "Requested shutdown has already been started".to_string(),
            ));
        }
        // Stop accepting new leases.
        self.components.lease_coordinator.stop_lease_taker();

        let leases: Vec<Lease> = self.components.lease_coordinator.get_assignments();
        if leases.is_empty() {
            // Nothing to notify; still need to shut the worker down.
            self.shutdown().await;
            return Ok(GracefulShutdownContext::new(
                None,
                None,
                Some(Arc::clone(&self.final_shutdown_latch)),
                None,
            ));
        }
        let n = leases.len() as i64;
        let shutdown_complete_latch = Arc::new(CountDownLatch::new_with_count(n));
        let notification_complete_latch = Arc::new(CountDownLatch::new_with_count(n));
        for lease in leases {
            let notification: Arc<dyn crate::lifecycle::ShutdownNotification> =
                Arc::new(ShardConsumerShutdownNotification::new(
                    Arc::clone(&self.components.lease_coordinator),
                    lease.clone(),
                    Arc::clone(&notification_complete_latch),
                    Arc::clone(&shutdown_complete_latch),
                ));
            let shard_info =
                crate::leases::dynamodb::DynamoDBLeaseCoordinator::convert_lease_to_assignment(
                    &lease,
                );
            let consumer = {
                let map = self.shard_info_shard_consumer_map.lock().unwrap();
                map.get(&shard_info).cloned()
            };
            match consumer {
                Some(c) if !c.is_shutdown() => {
                    c.graceful_shutdown(Some(notification)).await;
                }
                _ => {
                    // Race: the lease was lost between fetching assignments and
                    // creating the notification. Clear the latches for it.
                    notification_complete_latch.count_down();
                    shutdown_complete_latch.count_down();
                }
            }
        }
        Ok(GracefulShutdownContext::new(
            Some(shutdown_complete_latch),
            Some(notification_complete_latch),
            Some(Arc::clone(&self.final_shutdown_latch)),
            Some(Arc::clone(self) as Arc<dyn SchedulerHandle>),
        ))
    }
}

#[async_trait]
impl SchedulerHandle for Scheduler {
    fn shutdown_complete(&self) -> bool {
        self.shutdown_complete.load(Ordering::SeqCst)
    }
    fn shard_consumer_map_is_empty(&self) -> bool {
        self.shard_info_shard_consumer_map
            .lock()
            .unwrap()
            .is_empty()
    }
    fn shard_consumer_map_size(&self) -> usize {
        self.shard_info_shard_consumer_map.lock().unwrap().len()
    }
    async fn shutdown(&self) {
        // SchedulerHandle::shutdown is called from the graceful-shutdown
        // coordinator with a `&self` (not `&Arc<Self>`); route through the
        // same idempotent shutdown sequence via a re-created Arc is not possible
        // here, so inline the idempotent guard + core teardown.
        if self.shutdown.swap(true, Ordering::SeqCst) {
            return;
        }
        self.components
            .worker_state_change_listener
            .on_worker_state_change(WorkerState::ShutDownStarted);
        self.shutdown_start_time_millis
            .store(now_millis(), Ordering::SeqCst);
        self.components.lease_coordinator.stop().await;
        self.components.lease_cleanup_manager.shutdown();
        self.components.periodic_shard_sync_manager.stop().await;
        if let Some(sm) = &self.components.table_migration_state_machine {
            sm.shutdown().await;
        }
        self.components
            .worker_state_change_listener
            .on_worker_state_change(WorkerState::ShutDown);
        self.components.stream_info_manager.stop(true);
    }
}

/// Everything [`build_consumer_provider`] captures to build a [`ShardConsumer`]
/// per shard (Java `buildConsumer`'s enclosing-instance fields). Grouped into a
/// struct so the (large) closure capture list is named once.
struct ConsumerProviderDeps {
    coordinator_factory: Arc<dyn crate::coordinator::CoordinatorFactory + Send + Sync>,
    checkpoint: Arc<dyn crate::processor::Checkpointer + Send + Sync>,
    lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    lease_management_factory: Arc<crate::leases::dynamodb::DynamoDBLeaseManagementFactory>,
    lease_cleanup_manager: Arc<LeaseCleanupManager>,
    retrieval_factory: Arc<dyn crate::retrieval::RetrievalFactory>,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    aggregator_util: Arc<crate::retrieval::AggregatorUtil>,
    stream_tracker: Arc<dyn StreamTracker + Send + Sync>,
    processor_factory: Arc<dyn crate::processor::ShardRecordProcessorFactory + Send + Sync>,
    current_stream_config_map: Arc<StdMutex<HashMap<StreamIdentifier, StreamConfig>>>,
    consumer_task_factory: Arc<crate::lifecycle::KinesisConsumerTaskFactory>,
    log_warning_for_task_after_millis: Option<i64>,
    task_execution_listener: Arc<dyn crate::lifecycle::TaskExecutionListener>,
    read_timeouts_to_ignore_before_warning: i32,
    parent_shard_poll_interval_millis: i64,
    task_backoff_time_millis: i64,
    skip_shard_sync_at_worker_initialization_if_leases_exist: bool,
    list_shards_backoff_time_in_millis: i64,
    max_list_shards_retry_attempts: i32,
    should_call_process_records_even_for_empty_record_list: bool,
    shard_consumer_dispatch_poll_interval_millis: i64,
    cleanup_leases_upon_shard_completion: bool,
    ignore_unexpected_child_shards: bool,
}

/// Build the per-shard [`ConsumerProvider`] closure. Port of the Java
/// `Scheduler.buildConsumer(shardInfo, ...)` (invoked lazily from the process
/// loop, so any Kinesis/DynamoDB work happens at consume-time, never at
/// Scheduler construction).
fn build_consumer_provider(deps: ConsumerProviderDeps) -> ConsumerProvider {
    let deps = Arc::new(deps);
    Arc::new(move |shard_info: &ShardInfo| {
        let deps = Arc::clone(&deps);
        let shard_info = shard_info.clone();
        Box::pin(async move { build_consumer(&deps, shard_info).await })
            as futures::future::BoxFuture<'static, Arc<ShardConsumer>>
    })
}

async fn build_consumer(deps: &ConsumerProviderDeps, shard_info: ShardInfo) -> Arc<ShardConsumer> {
    // Resolve the stream identifier for the shard (Java `getStreamIdentifier`).
    let stream_identifier = match shard_info.stream_identifier_ser_opt() {
        Some(ser) => StreamIdentifier::multi_stream_instance(ser),
        None => deps
            .stream_tracker
            .stream_config_list()
            .first()
            .map(|sc| sc.stream_identifier().clone())
            .unwrap_or_else(|| StreamIdentifier::single_stream_instance("single_stream_mode")),
    };

    // Resolve the StreamConfig (Java `currentStreamConfigMap.get(...)`, else create
    // an orphan config via the tracker).
    let stream_config = {
        let map = deps.current_stream_config_map.lock().unwrap();
        map.get(&stream_identifier).cloned()
    }
    .unwrap_or_else(|| {
        deps.stream_tracker
            .create_stream_config(stream_identifier.clone())
    });

    // Per-shard record-processor checkpointer (Java
    // `coordinatorFactory().createRecordProcessorCheckpointer`).
    let record_processor_checkpointer = deps
        .coordinator_factory
        .create_record_processor_checkpointer(shard_info.clone(), Arc::clone(&deps.checkpoint));

    // The retrieval records cache/publisher (Java `retrievalFactory().createGetRecordsCache`).
    let records_publisher = deps.retrieval_factory.create_get_records_cache(
        &shard_info,
        &stream_config,
        Arc::clone(&deps.metrics_factory),
        None,
    );

    // Shard detector + hierarchical shard syncer for this stream (Java
    // `shardDetectorProvider`/`hierarchicalShardSyncerProvider`).
    let shard_detector: Arc<dyn crate::leases::ShardDetector> = Arc::from(
        deps.lease_management_factory
            .create_shard_detector_for_stream(stream_config.clone())
            .expect("shard detector construction"),
    );
    let hierarchical_shard_syncer = Arc::new(crate::leases::HierarchicalShardSyncer::with_mode(
        deps.stream_tracker.is_multi_stream(),
        stream_config.stream_identifier().to_string(),
    ));

    // The customer record processor, guarded so its sync `&mut self` callbacks
    // run under `spawn_blocking`. The factory itself is also invoked under
    // `spawn_blocking`: `build_consumer` runs on a runtime worker and a user
    // factory may block (the PyO3 factory acquires the GIL), which must not
    // stall the async workers. The factory returns a `+ Send + Sync` box; the
    // argument only requires `+ Send`, so coerce.
    let processor: Box<dyn crate::processor::ShardRecordProcessor + Send> = {
        let factory = Arc::clone(&deps.processor_factory);
        let stream_identifier = stream_config.stream_identifier().clone();
        tokio::task::spawn_blocking(move || {
            factory.shard_record_processor_for_stream(&stream_identifier)
        })
        .await
        // A panicking factory keeps its previous behavior: propagate the panic.
        .expect("shard record processor factory panicked")
    };
    let processor = std::sync::Mutex::new(processor);

    let argument = crate::lifecycle::ShardConsumerArgument::new(
        shard_info.clone(),
        stream_config.stream_identifier().clone(),
        Arc::clone(&deps.lease_coordinator),
        Arc::clone(&records_publisher),
        Arc::new(processor),
        Arc::clone(&deps.checkpoint),
        record_processor_checkpointer,
        deps.parent_shard_poll_interval_millis,
        deps.task_backoff_time_millis,
        deps.skip_shard_sync_at_worker_initialization_if_leases_exist,
        deps.list_shards_backoff_time_in_millis,
        deps.max_list_shards_retry_attempts,
        deps.should_call_process_records_even_for_empty_record_list,
        deps.shard_consumer_dispatch_poll_interval_millis,
        *stream_config.initial_position_in_stream_extended(),
        deps.cleanup_leases_upon_shard_completion,
        deps.ignore_unexpected_child_shards,
        shard_detector,
        Arc::clone(&deps.aggregator_util),
        hierarchical_shard_syncer,
        Arc::clone(&deps.metrics_factory),
        Arc::clone(&deps.lease_cleanup_manager),
    );

    // Java `shardConsumerSubscriberBufferSize` = 8 (0 iff a PollingConfig with
    // maxPendingProcessRecordsInput == 0 — not modeled; default 8).
    let buffer_size = 8;

    ShardConsumer::new(
        Arc::clone(&records_publisher),
        shard_info,
        deps.log_warning_for_task_after_millis,
        argument,
        None,
        buffer_size,
        Arc::clone(&deps.task_execution_listener),
        deps.read_timeouts_to_ignore_before_warning,
        deps.consumer_task_factory.clone(),
    )
    .await
}

/// An error surfaced by the Scheduler's initialization / process loop.
#[derive(Debug, thiserror::Error)]
#[error("{0}")]
pub struct SchedulerError(pub String);

impl From<crate::leases::exceptions::LeasingError> for SchedulerError {
    fn from(e: crate::leases::exceptions::LeasingError) -> Self {
        SchedulerError(e.to_string())
    }
}

fn now_millis() -> i64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

#[cfg(test)]
mod tests;
