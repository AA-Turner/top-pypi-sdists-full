//! Port of `software.amazon.kinesis.lifecycle.ShardConsumerArgument`.

use std::sync::{Arc, Mutex};

use crate::checkpoint::ShardRecordProcessorCheckpointer;
use crate::common::{InitialPositionInStreamExtended, StreamIdentifier};
use crate::leases::{
    HierarchicalShardSyncer, LeaseCleanupManager, LeaseCoordinator, ShardDetector, ShardInfo,
};
use crate::metrics::MetricsFactory;
use crate::processor::{Checkpointer, ShardRecordProcessor};
use crate::retrieval::{AggregatorUtil, RecordsPublisher};

/// The shared parameter bag threading all shard/task construction dependencies
/// from the Scheduler down into the [`ConsumerTaskFactory`] task constructors.
///
/// Port of the Lombok `@Data @Accessors(fluent=true)` data holder. Java's
/// generated `equals`/`hashCode`/`toString` over these DI fields is not
/// replicated (it is dead weight — this is a pure DI parameter object).
///
/// # Concurrency model (see PORTING.md / the lifecycle arch-map)
///
/// * The customer [`ShardRecordProcessor`] is stored as
///   `Arc<std::sync::Mutex<Box<dyn ShardRecordProcessor + Send>>>`. Its sync
///   callbacks (`initialize`/`process_records`/`lease_lost`/`shard_ended`/
///   `shutdown_requested`) may call the checkpointer, which bridges to async via
///   `Handle::block_on`; that must **not** run on a runtime worker. Tasks
///   therefore invoke the processor via [`tokio::task::spawn_blocking`], never
///   from inside an async `.await`/`block_on`.
/// * The [`ShardRecordProcessorCheckpointer`] is the concrete type (held as
///   `Arc<ShardRecordProcessorCheckpointer>`) because the tasks need its state
///   accessors (`largest_permitted_checkpoint_value()`,
///   `last_checkpoint_value()`, …); it also coerces to
///   `Arc<dyn RecordProcessorCheckpointer + Send + Sync>` when building the
///   `*Input` events handed to the processor.
#[derive(Clone)]
pub struct ShardConsumerArgument {
    shard_info: ShardInfo,
    stream_identifier: StreamIdentifier,
    lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
    records_publisher: Arc<dyn RecordsPublisher>,
    /// The customer processor, guarded by a `std::sync::Mutex` so its `&mut self`
    /// sync callbacks can be invoked from `spawn_blocking`.
    shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
    checkpoint: Arc<dyn Checkpointer + Send + Sync>,
    record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
    parent_shard_poll_interval_millis: i64,
    task_backoff_time_millis: i64,
    skip_shard_sync_at_worker_initialization_if_leases_exist: bool,
    list_shards_backoff_time_in_millis: i64,
    max_list_shards_retry_attempts: i32,
    should_call_process_records_even_for_empty_record_list: bool,
    idle_time_in_milliseconds: i64,
    initial_position_in_stream: InitialPositionInStreamExtended,
    cleanup_leases_of_completed_shards: bool,
    ignore_unexpected_child_shards: bool,
    shard_detector: Arc<dyn ShardDetector>,
    aggregator_util: Arc<AggregatorUtil>,
    hierarchical_shard_syncer: Arc<HierarchicalShardSyncer>,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    lease_cleanup_manager: Arc<LeaseCleanupManager>,
    // NOTE(port): `schemaRegistryDecoder` is omitted — the Glue Schema Registry
    // integration is deferred (see PORTING.md schemaregistry deferral). ProcessTask
    // treats it as always-absent.
    consumer_id: Option<String>,
}

#[allow(clippy::too_many_arguments)]
impl ShardConsumerArgument {
    /// Construct a [`ShardConsumerArgument`]. Mirrors the Java 25-arg constructor
    /// (with `consumerId` defaulting to `None`), minus `executorService` (tokio
    /// tasks) and `schemaRegistryDecoder` (deferred).
    pub fn new(
        shard_info: ShardInfo,
        stream_identifier: StreamIdentifier,
        lease_coordinator: Arc<dyn LeaseCoordinator + Send + Sync>,
        records_publisher: Arc<dyn RecordsPublisher>,
        shard_record_processor: Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>>,
        checkpoint: Arc<dyn Checkpointer + Send + Sync>,
        record_processor_checkpointer: Arc<ShardRecordProcessorCheckpointer>,
        parent_shard_poll_interval_millis: i64,
        task_backoff_time_millis: i64,
        skip_shard_sync_at_worker_initialization_if_leases_exist: bool,
        list_shards_backoff_time_in_millis: i64,
        max_list_shards_retry_attempts: i32,
        should_call_process_records_even_for_empty_record_list: bool,
        idle_time_in_milliseconds: i64,
        initial_position_in_stream: InitialPositionInStreamExtended,
        cleanup_leases_of_completed_shards: bool,
        ignore_unexpected_child_shards: bool,
        shard_detector: Arc<dyn ShardDetector>,
        aggregator_util: Arc<AggregatorUtil>,
        hierarchical_shard_syncer: Arc<HierarchicalShardSyncer>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        lease_cleanup_manager: Arc<LeaseCleanupManager>,
    ) -> Self {
        Self {
            shard_info,
            stream_identifier,
            lease_coordinator,
            records_publisher,
            shard_record_processor,
            checkpoint,
            record_processor_checkpointer,
            parent_shard_poll_interval_millis,
            task_backoff_time_millis,
            skip_shard_sync_at_worker_initialization_if_leases_exist,
            list_shards_backoff_time_in_millis,
            max_list_shards_retry_attempts,
            should_call_process_records_even_for_empty_record_list,
            idle_time_in_milliseconds,
            initial_position_in_stream,
            cleanup_leases_of_completed_shards,
            ignore_unexpected_child_shards,
            shard_detector,
            aggregator_util,
            hierarchical_shard_syncer,
            metrics_factory,
            lease_cleanup_manager,
            consumer_id: None,
        }
    }

    // ---- fluent getters (Java `@Accessors(fluent = true)`) ----

    pub fn shard_info(&self) -> &ShardInfo {
        &self.shard_info
    }
    pub fn stream_identifier(&self) -> &StreamIdentifier {
        &self.stream_identifier
    }
    pub fn lease_coordinator(&self) -> &Arc<dyn LeaseCoordinator + Send + Sync> {
        &self.lease_coordinator
    }
    pub fn records_publisher(&self) -> &Arc<dyn RecordsPublisher> {
        &self.records_publisher
    }
    pub fn shard_record_processor(&self) -> &Arc<Mutex<Box<dyn ShardRecordProcessor + Send>>> {
        &self.shard_record_processor
    }
    pub fn checkpoint(&self) -> &Arc<dyn Checkpointer + Send + Sync> {
        &self.checkpoint
    }
    pub fn record_processor_checkpointer(&self) -> &Arc<ShardRecordProcessorCheckpointer> {
        &self.record_processor_checkpointer
    }
    pub fn parent_shard_poll_interval_millis(&self) -> i64 {
        self.parent_shard_poll_interval_millis
    }
    pub fn task_backoff_time_millis(&self) -> i64 {
        self.task_backoff_time_millis
    }
    pub fn skip_shard_sync_at_worker_initialization_if_leases_exist(&self) -> bool {
        self.skip_shard_sync_at_worker_initialization_if_leases_exist
    }
    pub fn list_shards_backoff_time_in_millis(&self) -> i64 {
        self.list_shards_backoff_time_in_millis
    }
    pub fn max_list_shards_retry_attempts(&self) -> i32 {
        self.max_list_shards_retry_attempts
    }
    pub fn should_call_process_records_even_for_empty_record_list(&self) -> bool {
        self.should_call_process_records_even_for_empty_record_list
    }
    pub fn idle_time_in_milliseconds(&self) -> i64 {
        self.idle_time_in_milliseconds
    }
    pub fn initial_position_in_stream(&self) -> &InitialPositionInStreamExtended {
        &self.initial_position_in_stream
    }
    pub fn cleanup_leases_of_completed_shards(&self) -> bool {
        self.cleanup_leases_of_completed_shards
    }
    pub fn ignore_unexpected_child_shards(&self) -> bool {
        self.ignore_unexpected_child_shards
    }
    pub fn shard_detector(&self) -> &Arc<dyn ShardDetector> {
        &self.shard_detector
    }
    pub fn aggregator_util(&self) -> &Arc<AggregatorUtil> {
        &self.aggregator_util
    }
    pub fn hierarchical_shard_syncer(&self) -> &Arc<HierarchicalShardSyncer> {
        &self.hierarchical_shard_syncer
    }
    pub fn metrics_factory(&self) -> &Arc<dyn MetricsFactory + Send + Sync> {
        &self.metrics_factory
    }
    pub fn lease_cleanup_manager(&self) -> &Arc<LeaseCleanupManager> {
        &self.lease_cleanup_manager
    }
    pub fn consumer_id(&self) -> Option<&str> {
        self.consumer_id.as_deref()
    }

    /// Set the consumer id (Java `@Data` generates a setter for the sole
    /// non-final field `consumerId`).
    pub fn set_consumer_id(&mut self, consumer_id: Option<String>) {
        self.consumer_id = consumer_id;
    }
}
