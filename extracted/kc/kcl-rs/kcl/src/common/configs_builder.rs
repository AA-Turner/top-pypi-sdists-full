//! Port of `software.amazon.kinesis.common.ConfigsBuilder`.
//!
//! Convenience facade that builds all seven KCL sub-configs (Checkpoint,
//! Coordinator, LeaseManagement, Lifecycle, Metrics, Processor, Retrieval) with
//! sensible defaults from a small set of required inputs (application name, AWS
//! clients, worker id, processor factory, stream tracker).
//!
//! # Deviations from Java
//!
//! * **The deprecated `appStreamTracker` `Either` dual-representation is dropped.**
//!   Java kept a `@Deprecated Either<MultiStreamTracker, String> appStreamTracker`
//!   field kept in sync with `streamTracker` via `DeprecationUtils`. Per PORTING.md
//!   we expose only the modern [`StreamTracker`] surface.
//! * **`tableName()`/`namespace()` lazy defaulting is resolved eagerly on read.**
//!   Java memoizes the default (`applicationName`) on first read into a private
//!   mutable field; here [`table_name`](ConfigsBuilder::table_name) /
//!   [`namespace`](ConfigsBuilder::namespace) return the override if set, else the
//!   application name (same observable semantics — the resolution is idempotent).
//! * Lombok `@NonNull` constructor null-checks are subsumed by Rust's
//!   non-`Option` parameter types (the invalid state is unrepresentable).
//! * The seven `*_config()` factory methods return a **new** instance every call
//!   (matching Java — they are not cached/memoized).

use std::sync::Arc;

use aws_sdk_cloudwatch::Client as CloudWatchClient;
use aws_sdk_dynamodb::Client as DynamoDbClient;
use aws_sdk_kinesis::Client as KinesisClient;

use crate::checkpoint::CheckpointConfig;
use crate::common::Arn;
use crate::coordinator::coordinator_config::CoordinatorConfig;
use crate::leases::lease_management_config::LeaseManagementConfig;
use crate::lifecycle::LifecycleConfig;
use crate::metrics::MetricsConfig;
use crate::processor::{
    ProcessorConfig, ShardRecordProcessorFactory, SingleStreamTracker, StreamTracker,
};
use crate::retrieval::RetrievalConfig;

/// Builds all seven KCL sub-configs with default values from a small set of
/// required inputs. Java `ConfigsBuilder`.
///
/// Construct via [`ConfigsBuilder::from_stream_name`],
/// [`ConfigsBuilder::from_stream_arn`], or [`ConfigsBuilder::new`] (the
/// [`StreamTracker`] form). Fluent setters (`set_table_name`, `set_namespace`,
/// `set_stream_tracker`) override the defaults. Call
/// [`checkpoint_config`](Self::checkpoint_config) etc. to materialize each config.
#[derive(Clone)]
pub struct ConfigsBuilder {
    stream_tracker: Arc<dyn StreamTracker + Send + Sync>,
    application_name: String,
    kinesis_client: KinesisClient,
    dynamodb_client: DynamoDbClient,
    cloudwatch_client: CloudWatchClient,
    worker_identifier: String,
    shard_record_processor_factory: Arc<dyn ShardRecordProcessorFactory + Send + Sync>,
    /// Lease table name override; when `None`, defaults to `application_name`.
    table_name: Option<String>,
    /// CloudWatch namespace override; when `None`, defaults to `application_name`.
    namespace: Option<String>,
}

impl ConfigsBuilder {
    /// Construct for a single stream identified by name. Java
    /// `ConfigsBuilder(String streamName, ...)`.
    #[allow(clippy::too_many_arguments)]
    pub fn from_stream_name(
        stream_name: &str,
        application_name: impl Into<String>,
        kinesis_client: KinesisClient,
        dynamodb_client: DynamoDbClient,
        cloudwatch_client: CloudWatchClient,
        worker_identifier: impl Into<String>,
        shard_record_processor_factory: Arc<dyn ShardRecordProcessorFactory + Send + Sync>,
    ) -> Self {
        Self::new(
            Arc::new(SingleStreamTracker::from_stream_name(stream_name)),
            application_name,
            kinesis_client,
            dynamodb_client,
            cloudwatch_client,
            worker_identifier,
            shard_record_processor_factory,
        )
    }

    /// Construct for a single stream identified by ARN. Java
    /// `ConfigsBuilder(Arn streamArn, ...)`.
    #[allow(clippy::too_many_arguments)]
    pub fn from_stream_arn(
        stream_arn: Arn,
        application_name: impl Into<String>,
        kinesis_client: KinesisClient,
        dynamodb_client: DynamoDbClient,
        cloudwatch_client: CloudWatchClient,
        worker_identifier: impl Into<String>,
        shard_record_processor_factory: Arc<dyn ShardRecordProcessorFactory + Send + Sync>,
    ) -> Self {
        Self::new(
            Arc::new(SingleStreamTracker::from_arn(stream_arn)),
            application_name,
            kinesis_client,
            dynamodb_client,
            cloudwatch_client,
            worker_identifier,
            shard_record_processor_factory,
        )
    }

    /// Construct from a [`StreamTracker`] (single- or multi-stream). Java
    /// `ConfigsBuilder(StreamTracker streamTracker, ...)`.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        stream_tracker: Arc<dyn StreamTracker + Send + Sync>,
        application_name: impl Into<String>,
        kinesis_client: KinesisClient,
        dynamodb_client: DynamoDbClient,
        cloudwatch_client: CloudWatchClient,
        worker_identifier: impl Into<String>,
        shard_record_processor_factory: Arc<dyn ShardRecordProcessorFactory + Send + Sync>,
    ) -> Self {
        Self {
            stream_tracker,
            application_name: application_name.into(),
            kinesis_client,
            dynamodb_client,
            cloudwatch_client,
            worker_identifier: worker_identifier.into(),
            shard_record_processor_factory,
            table_name: None,
            namespace: None,
        }
    }

    // ---- accessors (Java fluent @Getter) ----

    pub fn stream_tracker(&self) -> &Arc<dyn StreamTracker + Send + Sync> {
        &self.stream_tracker
    }

    pub fn application_name(&self) -> &str {
        &self.application_name
    }

    pub fn kinesis_client(&self) -> &KinesisClient {
        &self.kinesis_client
    }

    pub fn dynamodb_client(&self) -> &DynamoDbClient {
        &self.dynamodb_client
    }

    pub fn cloudwatch_client(&self) -> &CloudWatchClient {
        &self.cloudwatch_client
    }

    pub fn worker_identifier(&self) -> &str {
        &self.worker_identifier
    }

    pub fn shard_record_processor_factory(
        &self,
    ) -> &Arc<dyn ShardRecordProcessorFactory + Send + Sync> {
        &self.shard_record_processor_factory
    }

    /// Lease table name used for lease management and checkpointing. Defaults to
    /// the application name when not explicitly set (Java lazy `tableName()`).
    pub fn table_name(&self) -> &str {
        self.table_name.as_deref().unwrap_or(&self.application_name)
    }

    /// CloudWatch namespace for KCL metrics. Defaults to the application name
    /// when not explicitly set (Java lazy `namespace()`).
    pub fn namespace(&self) -> &str {
        self.namespace.as_deref().unwrap_or(&self.application_name)
    }

    // ---- fluent setters (Java @Setter, chainable) ----

    pub fn set_stream_tracker(
        mut self,
        stream_tracker: Arc<dyn StreamTracker + Send + Sync>,
    ) -> Self {
        self.stream_tracker = stream_tracker;
        self
    }

    pub fn set_table_name(mut self, table_name: impl Into<String>) -> Self {
        self.table_name = Some(table_name.into());
        self
    }

    pub fn set_namespace(mut self, namespace: impl Into<String>) -> Self {
        self.namespace = Some(namespace.into());
        self
    }

    // ---- config factory methods (each returns a NEW instance) ----

    /// Creates a new [`CheckpointConfig`]. Java `checkpointConfig()`.
    pub fn checkpoint_config(&self) -> CheckpointConfig {
        CheckpointConfig::new()
    }

    /// Creates a new [`CoordinatorConfig`]. Java `coordinatorConfig()`.
    pub fn coordinator_config(&self) -> CoordinatorConfig {
        CoordinatorConfig::new(self.application_name())
    }

    /// Creates a new [`LeaseManagementConfig`]. Java `leaseManagementConfig()`.
    ///
    /// # Deviation
    ///
    /// The Rust [`LeaseManagementConfig::new`] takes `stream_name` (not
    /// `applicationName` like Java) so the lease-management factory can derive a
    /// single-stream `StreamConfig`. We pass the tracker's first stream name
    /// (its `serialize()` form) for the single-stream common case; multi-stream
    /// mode derives per-stream configs from the tracker elsewhere.
    pub fn lease_management_config(&self) -> LeaseManagementConfig {
        let stream_name = self
            .stream_tracker
            .stream_config_list()
            .first()
            .map(|sc| sc.stream_identifier().serialize())
            .unwrap_or_default();
        LeaseManagementConfig::new(
            self.table_name(),
            self.dynamodb_client.clone(),
            self.kinesis_client.clone(),
            stream_name,
            self.worker_identifier(),
        )
    }

    /// Creates a new [`LifecycleConfig`]. Java `lifecycleConfig()`.
    pub fn lifecycle_config(&self) -> LifecycleConfig {
        LifecycleConfig::new()
    }

    /// Creates a new [`MetricsConfig`]. Java `metricsConfig()`.
    pub fn metrics_config(&self) -> MetricsConfig {
        MetricsConfig::new(self.cloudwatch_client.clone(), self.namespace())
    }

    /// Creates a new [`ProcessorConfig`]. Java `processorConfig()`.
    pub fn processor_config(&self) -> ProcessorConfig {
        ProcessorConfig::new(Arc::clone(&self.shard_record_processor_factory))
    }

    /// Creates a new [`RetrievalConfig`]. Java `retrievalConfig()`.
    pub fn retrieval_config(&self) -> RetrievalConfig {
        RetrievalConfig::new(
            self.kinesis_client.clone(),
            Arc::clone(&self.stream_tracker),
            self.application_name(),
        )
    }
}

#[cfg(test)]
mod tests;
