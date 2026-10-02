//! Port of `software.amazon.kinesis.leases.dynamodb.DynamoDBLeaseManagementFactory`.
//!
//! The sole concrete [`LeaseManagementFactory`] — the DI composition root that
//! wires together the DynamoDB-backed lease-management collaborators
//! ([`LeaseCoordinator`], [`LeaseRefresher`], [`ShardDetector`],
//! [`LeaseCleanupManager`], `ShardSyncTaskManager`, and the stream-info managers)
//! from a bag of configuration fields copied off a [`LeaseManagementConfig`].
//!
//! # Construction
//!
//! Per the arch-map recommendation, only the **config-based constructor** is
//! ported ([`DynamoDBLeaseManagementFactory::new`]); the deprecated 34-arg
//! positional Java constructor is dropped. It takes the config, a
//! [`LeaseSerializer`], and the multi-stream flag, copying every needed field.
//!
//! # Deviations
//!
//! - Lombok `@Data`'s generated `equals`/`hashCode`/`toString` are **not**
//!   derived: this is a config/builder bean, never compared for equality.
//! - Java `@NonNull` on ctor params → the fields are non-`Option` (a missing
//!   value is a construction-time programming error, i.e. the Rust type system
//!   enforces presence).
//! - The Java single-thread `ScheduledExecutorService`s created per collaborator
//!   have no analog: the ported [`LeaseCleanupManager`] / `ShardSyncTaskManager`
//!   own their own tokio-task cadence.
//! - `TableCreatorCallback`: the config's `table_creator_callback()` slot is
//!   still the `port_stubs` unit-struct placeholder, so the refresher is wired
//!   with [`NoopTableCreatorCallback`]. `// TODO(port)` — leases-6d: reconcile the
//!   config's callback field with the real trait.
//! - `customShardDetectorProvider` (a `Function<StreamConfig, ShardDetector>` DI
//!   override) is not modeled; `create_shard_detector_for_stream` always builds a
//!   [`KinesisShardDetector`]. `// TODO(port)` — coordinator/config wave.
//! - `create_stream_id_cache_manager` / `create_stream_info_manager` return the
//!   `port_stubs` placeholders (coordinator wave 10).

use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;

use aws_sdk_dynamodb::types::{BillingMode, Tag};

use crate::common::{LeaseCleanupConfig, StreamConfig, StreamIdentifier};
use crate::coordinator::{
    DeletedStreamListProvider, StreamIdCacheManager, StreamIdOnboardingState, StreamInfoDAO,
    StreamInfoManager, StreamInfoMode,
};
use crate::leases::exceptions::LeasingError;
use crate::leases::lease_cleanup_manager::LeaseCleanupManager;
use crate::leases::lease_management_config::{
    GracefulLeaseHandoffConfig, LeaseManagementConfig, WorkerUtilizationAwareAssignmentConfig,
};
use crate::leases::shard_sync_task_manager::ShardSyncTaskManager;
use crate::leases::{
    HierarchicalShardSyncer, KinesisShardDetector, LeaseCoordinator, LeaseManagementFactory,
    LeaseRefresher, LeaseSerializer, ShardDetector, ShardInfo,
};
use crate::lifecycle::ShardConsumer;
use crate::metrics::MetricsFactory;

use super::dynamodb_lease_coordinator::DynamoDBLeaseCoordinator;
use super::dynamodb_lease_refresher::{DynamoDBLeaseRefresher, RefresherTableConfig};
use super::table_creator_callback::NoopTableCreatorCallback;

/// The concrete DynamoDB-backed [`LeaseManagementFactory`].
pub struct DynamoDBLeaseManagementFactory {
    kinesis_client: aws_sdk_kinesis::Client,
    dynamo_db_client: aws_sdk_dynamodb::Client,
    table_name: String,
    worker_identifier: String,
    lease_serializer: Arc<dyn LeaseSerializer + Send + Sync>,
    // Java's deprecated single-`StreamConfig` factory field is NOT ported: it
    // was never read (production paths pass a per-stream `StreamConfig` into
    // `create_shard_sync_task_manager_with`/`create_shard_detector_for_stream`).
    failover_time_millis: i64,
    enable_priority_lease_assignment: bool,
    epsilon_millis: i64,
    max_leases_for_worker: i32,
    max_leases_to_steal_at_one_time: i32,
    max_lease_renewal_threads: i32,
    cleanup_leases_upon_shard_completion: bool,
    ignore_unexpected_child_shards: bool,
    shard_sync_interval_millis: i64,
    consistent_reads: bool,
    list_shards_backoff_time_millis: i64,
    max_list_shards_retry_attempts: i32,
    max_cache_misses_before_reload: i32,
    list_shards_cache_allowed_age_in_seconds: i64,
    cache_miss_warning_modulus: i32,
    initial_lease_table_read_capacity: i64,
    initial_lease_table_write_capacity: i64,
    dynamo_db_request_timeout: Duration,
    billing_mode: BillingMode,
    lease_table_deletion_protection_enabled: bool,
    lease_table_pitr_enabled: bool,
    tags: Vec<Tag>,
    is_multi_stream_mode: bool,
    lease_cleanup_config: LeaseCleanupConfig,
    worker_utilization_aware_assignment_config: WorkerUtilizationAwareAssignmentConfig,
    graceful_lease_handoff_config: GracefulLeaseHandoffConfig,
    lease_assignment_interval_millis: i64,
    lease_table_scan_total_segments: i32,
}

impl DynamoDBLeaseManagementFactory {
    /// Construct from a [`LeaseManagementConfig`] (Java's preferred config-object
    /// constructor). Copies every needed field off the config.
    pub fn new(
        config: &LeaseManagementConfig,
        lease_serializer: Arc<dyn LeaseSerializer + Send + Sync>,
        is_multi_stream_mode: bool,
    ) -> Self {
        Self {
            kinesis_client: config.kinesis_client().clone(),
            dynamo_db_client: config.dynamo_db_client().clone(),
            table_name: config.table_name().to_string(),
            worker_identifier: config.worker_identifier().to_string(),
            lease_serializer,
            failover_time_millis: config.failover_time_millis(),
            enable_priority_lease_assignment: config.enable_priority_lease_assignment(),
            epsilon_millis: config.epsilon_millis(),
            max_leases_for_worker: config.max_leases_for_worker(),
            max_leases_to_steal_at_one_time: config.max_leases_to_steal_at_one_time(),
            max_lease_renewal_threads: config.max_lease_renewal_threads(),
            cleanup_leases_upon_shard_completion: config.cleanup_leases_upon_shard_completion(),
            ignore_unexpected_child_shards: config.ignore_unexpected_child_shards(),
            shard_sync_interval_millis: config.shard_sync_interval_millis(),
            consistent_reads: config.consistent_reads(),
            list_shards_backoff_time_millis: config.list_shards_backoff_time_in_millis(),
            max_list_shards_retry_attempts: config.max_list_shards_retry_attempts(),
            max_cache_misses_before_reload: config.max_cache_misses_before_reload(),
            list_shards_cache_allowed_age_in_seconds: config
                .list_shards_cache_allowed_age_in_seconds(),
            cache_miss_warning_modulus: config.cache_miss_warning_modulus(),
            initial_lease_table_read_capacity: config.initial_lease_table_read_capacity() as i64,
            initial_lease_table_write_capacity: config.initial_lease_table_write_capacity() as i64,
            dynamo_db_request_timeout: config.dynamo_db_request_timeout(),
            billing_mode: config.billing_mode().clone(),
            lease_table_deletion_protection_enabled: config
                .lease_table_deletion_protection_enabled(),
            lease_table_pitr_enabled: config.lease_table_pitr_enabled(),
            tags: config.tags().to_vec(),
            is_multi_stream_mode,
            lease_cleanup_config: config.lease_cleanup_config(),
            worker_utilization_aware_assignment_config: config
                .worker_utilization_aware_assignment_config()
                .clone(),
            graceful_lease_handoff_config: config.graceful_lease_handoff_config().clone(),
            lease_assignment_interval_millis: config.lease_assignment_interval_millis(),
            lease_table_scan_total_segments: config.lease_table_scan_total_segments(),
        }
    }

    /// Build a concrete [`DynamoDBLeaseCoordinator`] (Java
    /// `createLeaseCoordinator`), optionally wired with a stream-id cache manager.
    fn build_lease_coordinator(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        stream_id_cache_manager: Option<StreamIdCacheManager>,
    ) -> DynamoDBLeaseCoordinator {
        DynamoDBLeaseCoordinator::new(
            Arc::new(self.build_lease_refresher()),
            self.worker_identifier.clone(),
            self.failover_time_millis,
            self.enable_priority_lease_assignment,
            self.epsilon_millis,
            self.max_leases_for_worker,
            self.max_leases_to_steal_at_one_time,
            self.max_lease_renewal_threads,
            self.initial_lease_table_read_capacity,
            self.initial_lease_table_write_capacity,
            metrics_factory,
            self.worker_utilization_aware_assignment_config.clone(),
            self.graceful_lease_handoff_config.clone(),
            self.lease_assignment_interval_millis,
            stream_id_cache_manager,
            self.lease_table_scan_total_segments,
        )
    }

    /// Java `createLeaseRefresher()` (returns the concrete
    /// `DynamoDBLeaseRefresher`; here the concrete struct).
    fn build_lease_refresher(&self) -> DynamoDBLeaseRefresher {
        let ddb_table_config = RefresherTableConfig {
            billing_mode: self.billing_mode.clone(),
            read_capacity: self.initial_lease_table_read_capacity,
            write_capacity: self.initial_lease_table_write_capacity,
        };
        DynamoDBLeaseRefresher::new(
            self.table_name.clone(),
            self.dynamo_db_client.clone(),
            self.lease_serializer.clone(),
            self.consistent_reads,
            // TODO(port) — leases-6d: reconcile config.table_creator_callback()
            // (a port_stubs placeholder) with the real TableCreatorCallback trait.
            Arc::new(NoopTableCreatorCallback),
            self.dynamo_db_request_timeout,
            ddb_table_config,
            self.lease_table_deletion_protection_enabled,
            self.lease_table_pitr_enabled,
            self.tags.clone(),
        )
    }

    /// Java `createShardDetector(StreamConfig)`. `// TODO(port)`: the
    /// `customShardDetectorProvider` DI override isn't modeled.
    fn build_shard_detector(&self, stream_config: &StreamConfig) -> KinesisShardDetector {
        KinesisShardDetector::new(
            self.kinesis_client.clone(),
            stream_config.stream_identifier().clone(),
            self.list_shards_backoff_time_millis.max(0) as u64,
            self.max_list_shards_retry_attempts,
            self.list_shards_cache_allowed_age_in_seconds,
            self.max_cache_misses_before_reload,
            self.cache_miss_warning_modulus,
            self.dynamo_db_request_timeout,
        )
    }

    fn build_shard_sync_task_manager(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        stream_config: &StreamConfig,
        deleted_stream_list_provider: Option<Arc<DeletedStreamListProvider>>,
    ) -> ShardSyncTaskManager {
        let detector: Arc<dyn ShardDetector> = Arc::new(self.build_shard_detector(stream_config));
        let refresher: Arc<dyn LeaseRefresher> = Arc::new(self.build_lease_refresher());
        let syncer = Arc::new(HierarchicalShardSyncer::with_deleted_stream_list_provider(
            self.is_multi_stream_mode,
            stream_config.stream_identifier().to_string(),
            deleted_stream_list_provider,
        ));
        ShardSyncTaskManager::new(
            detector,
            refresher,
            *stream_config.initial_position_in_stream_extended(),
            self.cleanup_leases_upon_shard_completion,
            self.ignore_unexpected_child_shards,
            self.shard_sync_interval_millis,
            syncer,
            metrics_factory,
        )
    }
}

impl LeaseManagementFactory for DynamoDBLeaseManagementFactory {
    fn create_lease_coordinator(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Box<dyn LeaseCoordinator + Send + Sync> {
        Box::new(self.build_lease_coordinator(metrics_factory, None))
    }

    fn create_lease_coordinator_with_consumer_map(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _shard_info_shard_consumer_map: HashMap<ShardInfo, Arc<ShardConsumer>>,
    ) -> Result<Box<dyn LeaseCoordinator + Send + Sync>, LeasingError> {
        Ok(Box::new(
            self.build_lease_coordinator(metrics_factory, None),
        ))
    }

    fn create_lease_coordinator_with_cache_manager(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _shard_info_shard_consumer_map: HashMap<ShardInfo, Arc<ShardConsumer>>,
        stream_id_cache_manager: StreamIdCacheManager,
    ) -> Result<Box<dyn LeaseCoordinator + Send + Sync>, LeasingError> {
        Ok(Box::new(self.build_lease_coordinator(
            metrics_factory,
            Some(stream_id_cache_manager),
        )))
    }

    fn create_shard_sync_task_manager_with_deleted_streams(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        stream_config: StreamConfig,
        deleted_stream_list_provider: Arc<DeletedStreamListProvider>,
    ) -> Result<Box<ShardSyncTaskManager>, LeasingError> {
        Ok(Box::new(self.build_shard_sync_task_manager(
            metrics_factory,
            &stream_config,
            Some(deleted_stream_list_provider),
        )))
    }

    fn create_shard_sync_task_manager_with_stream_info(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        stream_config: StreamConfig,
        deleted_stream_list_provider: Arc<DeletedStreamListProvider>,
        _stream_info_manager: StreamInfoManager,
    ) -> Result<Box<ShardSyncTaskManager>, LeasingError> {
        Ok(Box::new(self.build_shard_sync_task_manager(
            metrics_factory,
            &stream_config,
            Some(deleted_stream_list_provider),
        )))
    }

    fn create_lease_refresher(&self) -> Box<dyn LeaseRefresher> {
        Box::new(self.build_lease_refresher())
    }

    fn create_shard_detector_for_stream(
        &self,
        stream_config: StreamConfig,
    ) -> Result<Box<dyn ShardDetector>, LeasingError> {
        Ok(Box::new(self.build_shard_detector(&stream_config)))
    }

    fn create_lease_cleanup_manager(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Box<LeaseCleanupManager> {
        let coordinator: Arc<dyn LeaseCoordinator> =
            Arc::new(self.build_lease_coordinator(metrics_factory.clone(), None));
        Box::new(LeaseCleanupManager::new(
            coordinator,
            metrics_factory,
            self.cleanup_leases_upon_shard_completion,
            self.lease_cleanup_config.lease_cleanup_interval_millis,
            self.lease_cleanup_config
                .completed_lease_cleanup_interval_millis,
            self.lease_cleanup_config
                .garbage_lease_cleanup_interval_millis,
        ))
    }

    fn create_stream_id_cache_manager(
        &self,
        _stream_info_dao: StreamInfoDAO,
        _current_stream_config_map: HashMap<StreamIdentifier, StreamConfig>,
        _stream_id_onboarding_state: StreamIdOnboardingState,
        _is_multi_stream_mode: bool,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> StreamIdCacheManager {
        // TODO(port) — coordinator wave (10c/10d): wire the real
        // StreamIdCacheManager (needs the StreamInfoDAO + scheduled task) into
        // the factory. The real type is ported (`coordinator::StreamIdCacheManager`)
        // but this DI entry point is a later-wave concern and is never invoked yet.
        unimplemented!("StreamIdCacheManager wiring lands in coordinator wave 10c/10d")
    }

    fn create_stream_info_manager(
        &self,
        _current_stream_config_map: HashMap<StreamIdentifier, StreamConfig>,
        _stream_info_dao: StreamInfoDAO,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _is_multi_stream_mode: bool,
        _stream_info_backfill_interval_millis: i64,
        _stream_info_mode: StreamInfoMode,
        _stream_id_onboarding_state: StreamIdOnboardingState,
    ) -> StreamInfoManager {
        // TODO(port) — coordinator wave (10c/10d): wire the real StreamInfoManager
        // (the type is ported; this DI entry point is a later-wave concern and is
        // never invoked yet).
        unimplemented!("StreamInfoManager wiring lands in coordinator wave 10c/10d")
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
    use crate::leases::dynamodb::DynamoDBLeaseSerializer;
    use crate::metrics::NullMetricsFactory;

    async fn dummy_clients() -> (aws_sdk_kinesis::Client, aws_sdk_dynamodb::Client) {
        let conf = aws_config::defaults(aws_config::BehaviorVersion::latest())
            .region(aws_config::Region::new("us-east-1"))
            .credentials_provider(aws_sdk_dynamodb::config::Credentials::for_tests())
            .load()
            .await;
        (
            aws_sdk_kinesis::Client::new(&conf),
            aws_sdk_dynamodb::Client::new(&conf),
        )
    }

    fn stream_config() -> StreamConfig {
        StreamConfig::new(
            StreamIdentifier::single_stream_instance("test-stream"),
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
        )
    }

    async fn factory() -> DynamoDBLeaseManagementFactory {
        let (kinesis, dynamo) = dummy_clients().await;
        let config =
            LeaseManagementConfig::new("lease-table", dynamo, kinesis, "test-stream", "worker-1");
        DynamoDBLeaseManagementFactory::new(
            &config,
            Arc::new(DynamoDBLeaseSerializer::new()),
            false,
        )
    }

    #[tokio::test]
    async fn creates_lease_refresher_and_coordinator() {
        let f = factory().await;
        let _refresher = f.create_lease_refresher();
        let mf: Arc<dyn MetricsFactory + Send + Sync> = Arc::new(NullMetricsFactory);
        let coordinator = f.create_lease_coordinator(mf);
        assert_eq!(coordinator.worker_identifier(), "worker-1");
        assert!(!coordinator.is_running());
    }

    #[tokio::test]
    async fn creates_shard_detector_and_cleanup_manager() {
        let f = factory().await;
        let detector = f.create_shard_detector_for_stream(stream_config());
        assert!(detector.is_ok());
        let mf: Arc<dyn MetricsFactory + Send + Sync> = Arc::new(NullMetricsFactory);
        let cleanup = f.create_lease_cleanup_manager(mf);
        assert!(!cleanup.is_running());
    }
}
