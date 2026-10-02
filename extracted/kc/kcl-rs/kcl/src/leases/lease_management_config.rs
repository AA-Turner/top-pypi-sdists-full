//! Port of `software.amazon.kinesis.leases.LeaseManagementConfig`.
//!
//! Large configuration object holding every tunable for lease management:
//! DynamoDB/Kinesis clients, timing intervals, capacity, worker-utilization
//! sub-config, graceful-handoff sub-config, and factory wiring.
//!
//! # Conventions
//!
//! - Lombok `@Data @Accessors(fluent = true)` → a plain struct with fluent
//!   no-prefix getters (`fn field(&self) -> ...`) and chainable setters
//!   (`fn field(mut self, v) -> Self`) per [`PORTING.md`].
//! - Required `@NonNull` fields (`table_name`, `dynamo_db_client`,
//!   `kinesis_client`, `stream_name`, `worker_identifier`) are constructor args.
//! - Every numeric DEFAULT is preserved verbatim (other classes depend on them).
//! - The **derived default** `lease_assignment_interval_millis` (Java: `2 *
//!   failoverTimeMillis` iff unset) is an `Option<i64>` with a computed accessor.
//! - `lease_table_scan_total_segments` setter validates `> 0` (Java
//!   `IllegalArgumentException` → panic).
//!
//! # Deviations
//!
//! - The Java "lazy singleton computed on first getter" idiom for
//!   `leaseManagementFactory` / (deprecated) `hierarchicalShardSyncer` is
//!   modeled as plain `Option` fields with explicit setters (idiomatic Rust
//!   favors explicit construction; the coordinator wave wires the factory).
//! - `LeaseCleanupConfig` / `DdbTableConfig` are the real `common`-wave ports
//!   (`crate::common::{LeaseCleanupConfig, DdbTableConfig}`); `TableCreatorCallback`
//!   is the real `leases::dynamodb` trait (held as `Arc<dyn TableCreatorCallback>`,
//!   defaulting to [`NoopTableCreatorCallback`]).
//! - The `LeaseManagementThreadPool` (an unbounded cached `ThreadPoolExecutor`)
//!   has no field here — tokio tasks replace it; a `// TODO(port)` notes it.

use std::time::Duration;

use aws_sdk_dynamodb::types::{BillingMode, Tag};

use crate::common::{DdbTableConfig, LeaseCleanupConfig};
use std::sync::Arc;

use crate::coordinator::{StreamIdOnboardingState, StreamInfoMode};
use crate::leases::dynamodb::{NoopTableCreatorCallback, TableCreatorCallback};
use crate::leases::LeaseAssignmentStrategy;
use crate::lifecycle::KinesisConsumerTaskFactory;
use crate::worker::metric::WorkerMetric;

/// Default request timeout (1 minute).
pub fn default_request_timeout() -> Duration {
    Duration::from_secs(60)
}

pub const DEFAULT_LEASE_CLEANUP_INTERVAL_MILLIS: i64 = 60 * 1000;
pub const DEFAULT_COMPLETED_LEASE_CLEANUP_INTERVAL_MILLIS: i64 = 5 * 60 * 1000;
pub const DEFAULT_GARBAGE_LEASE_CLEANUP_INTERVAL_MILLIS: i64 = 30 * 60 * 1000;
pub const DEFAULT_PERIODIC_SHARD_SYNC_INTERVAL_MILLIS: i64 = 2 * 60 * 1000;
pub const DEFAULT_LEASE_TABLE_DELETION_PROTECTION_ENABLED: bool = false;
pub const DEFAULT_LEASE_TABLE_PITR_ENABLED: bool = false;
pub const DEFAULT_ENABLE_PRIORITY_LEASE_ASSIGNMENT: bool = true;
pub const DEFAULT_CONSECUTIVE_HOLES_FOR_TRIGGERING_LEASE_RECOVERY: i32 = 3;

/// Default lease-cleanup config (1m / 5m / 30m).
pub fn default_lease_cleanup_config() -> LeaseCleanupConfig {
    LeaseCleanupConfig {
        lease_cleanup_interval_millis: DEFAULT_LEASE_CLEANUP_INTERVAL_MILLIS,
        completed_lease_cleanup_interval_millis: DEFAULT_COMPLETED_LEASE_CLEANUP_INTERVAL_MILLIS,
        garbage_lease_cleanup_interval_millis: DEFAULT_GARBAGE_LEASE_CLEANUP_INTERVAL_MILLIS,
    }
}

/// Configuration controlling graceful lease handoff. Port of the nested
/// `@Data @Builder GracefulLeaseHandoffConfig`.
#[derive(Debug, Clone, PartialEq)]
pub struct GracefulLeaseHandoffConfig {
    graceful_lease_handoff_timeout_millis: i64,
    is_graceful_lease_handoff_enabled: bool,
}

impl Default for GracefulLeaseHandoffConfig {
    fn default() -> Self {
        Self {
            graceful_lease_handoff_timeout_millis: 30_000,
            is_graceful_lease_handoff_enabled: true,
        }
    }
}

impl GracefulLeaseHandoffConfig {
    pub fn graceful_lease_handoff_timeout_millis(&self) -> i64 {
        self.graceful_lease_handoff_timeout_millis
    }
    pub fn is_graceful_lease_handoff_enabled(&self) -> bool {
        self.is_graceful_lease_handoff_enabled
    }
    pub fn set_graceful_lease_handoff_timeout_millis(mut self, v: i64) -> Self {
        self.graceful_lease_handoff_timeout_millis = v;
        self
    }
    pub fn set_graceful_lease_handoff_enabled(mut self, v: bool) -> Self {
        self.is_graceful_lease_handoff_enabled = v;
        self
    }
}

/// Worker-utilization-aware assignment tunables. Port of the nested
/// `@Data WorkerUtilizationAwareAssignmentConfig`.
#[derive(Debug, Clone)]
pub struct WorkerUtilizationAwareAssignmentConfig {
    pub in_memory_worker_metrics_capture_frequency_millis: i64,
    pub worker_metrics_reporter_freq_in_millis: i64,
    pub no_of_persisted_metrics_per_worker_metrics: i32,
    pub disable_worker_metrics: bool,
    pub worker_metric_list: Vec<std::sync::Arc<dyn WorkerMetric>>,
    pub max_throughput_per_host_kbps: f64,
    pub dampening_percentage: i32,
    pub re_balance_threshold_percentage: i32,
    pub allow_throughput_overshoot: bool,
    pub stale_worker_metrics_entry_cleanup_duration: Duration,
    /// Deprecated: KCL no longer creates a separate WorkerMetrics table.
    pub worker_metrics_table_config: Option<DdbTableConfig>,
    pub variance_balancing_frequency: i32,
    pub worker_metrics_ema_alpha: f64,
}

impl Default for WorkerUtilizationAwareAssignmentConfig {
    fn default() -> Self {
        Self {
            in_memory_worker_metrics_capture_frequency_millis: 1_000,
            worker_metrics_reporter_freq_in_millis: 30_000,
            no_of_persisted_metrics_per_worker_metrics: 10,
            disable_worker_metrics: false,
            worker_metric_list: Vec::new(),
            max_throughput_per_host_kbps: f64::MAX,
            dampening_percentage: 60,
            re_balance_threshold_percentage: 10,
            allow_throughput_overshoot: true,
            stale_worker_metrics_entry_cleanup_duration: Duration::from_secs(24 * 60 * 60),
            worker_metrics_table_config: None,
            variance_balancing_frequency: 3,
            worker_metrics_ema_alpha: 0.5,
        }
    }
}

/// Lease-management configuration.
///
/// `Debug` is hand-implemented (skipping the `table_creator_callback` trait
/// object, which is not `Debug`); `Clone` is derived (the callback is an `Arc`).
#[derive(Clone)]
pub struct LeaseManagementConfig {
    // --- required (@NonNull) ---
    table_name: String,
    dynamo_db_client: aws_sdk_dynamodb::Client,
    kinesis_client: aws_sdk_kinesis::Client,
    stream_name: String,
    worker_identifier: String,

    // --- tunables with defaults ---
    failover_time_millis: i64,
    lease_assignment_interval_millis: Option<i64>,
    enable_priority_lease_assignment: bool,
    shard_sync_interval_millis: i64,
    cleanup_leases_upon_shard_completion: bool,
    lease_cleanup_config: LeaseCleanupConfig,
    max_leases_for_worker: i32,
    max_leases_to_steal_at_one_time: i32,
    initial_lease_table_read_capacity: i32,
    initial_lease_table_write_capacity: i32,
    max_lease_renewal_threads: i32,
    lease_table_scan_total_segments: i32,
    ignore_unexpected_child_shards: bool,
    consistent_reads: bool,
    list_shards_backoff_time_in_millis: i64,
    max_list_shards_retry_attempts: i32,
    epsilon_millis: i64,
    dynamo_db_request_timeout: Duration,
    billing_mode: BillingMode,
    worker_utilization_aware_assignment_config: WorkerUtilizationAwareAssignmentConfig,
    lease_assignment_strategy: LeaseAssignmentStrategy,
    lease_table_deletion_protection_enabled: bool,
    lease_table_pitr_enabled: bool,
    tags: Vec<Tag>,
    leases_recovery_auditor_execution_frequency_millis: i64,
    leases_recovery_auditor_inconsistency_confidence_threshold: i32,
    // Java's `initialPositionInStream` field is NOT ported: it has been dead
    // since multi-stream support moved the position onto the StreamTracker's
    // per-stream `StreamConfig` (Java keeps it only for API compatibility).
    // Set the initial position on the stream tracker instead.
    max_cache_misses_before_reload: i32,
    list_shards_cache_allowed_age_in_seconds: i64,
    cache_miss_warning_modulus: i32,
    dynamo_db_lock_based_leader_lease_duration_in_millis: i64,
    dynamo_db_lock_based_leader_heartbeat_period_in_millis: i64,
    stream_info_mode: StreamInfoMode,
    stream_id_onboarding_state: StreamIdOnboardingState,
    table_creator_callback: Arc<dyn TableCreatorCallback>,
    graceful_lease_handoff_config: GracefulLeaseHandoffConfig,
    consumer_task_factory: KinesisConsumerTaskFactory,
    // TODO(port): `executorService` (LeaseManagementThreadPool) is replaced by
    // tokio tasks — no field here. The coordinator/lifecycle waves manage task
    // spawning directly.
    // TODO(port): `leaseManagementFactory` / (deprecated) `hierarchicalShardSyncer`
    // lazy-singleton fields are deferred to the coordinator wave (they require
    // the concrete DynamoDBLeaseManagementFactory, wave 6d).
}

impl std::fmt::Debug for LeaseManagementConfig {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("LeaseManagementConfig")
            .field("table_name", &self.table_name)
            .field("stream_name", &self.stream_name)
            .field("worker_identifier", &self.worker_identifier)
            .field("failover_time_millis", &self.failover_time_millis)
            .field("billing_mode", &self.billing_mode)
            .field("table_creator_callback", &"<dyn TableCreatorCallback>")
            .finish_non_exhaustive()
    }
}

impl LeaseManagementConfig {
    /// Construct with the required fields (mirrors the newer 5-arg-with-app-name
    /// Java constructor, without the WorkerMetricsTableConfig wiring which needs
    /// `applicationName` — see the note below). Everything else defaults.
    pub fn new(
        table_name: impl Into<String>,
        dynamo_db_client: aws_sdk_dynamodb::Client,
        kinesis_client: aws_sdk_kinesis::Client,
        stream_name: impl Into<String>,
        worker_identifier: impl Into<String>,
    ) -> Self {
        Self {
            table_name: table_name.into(),
            dynamo_db_client,
            kinesis_client,
            stream_name: stream_name.into(),
            worker_identifier: worker_identifier.into(),
            failover_time_millis: 10_000,
            lease_assignment_interval_millis: None,
            enable_priority_lease_assignment: DEFAULT_ENABLE_PRIORITY_LEASE_ASSIGNMENT,
            shard_sync_interval_millis: 60_000,
            cleanup_leases_upon_shard_completion: true,
            lease_cleanup_config: default_lease_cleanup_config(),
            max_leases_for_worker: i32::MAX,
            max_leases_to_steal_at_one_time: 1,
            initial_lease_table_read_capacity: 10,
            initial_lease_table_write_capacity: 10,
            max_lease_renewal_threads: 20,
            lease_table_scan_total_segments: 0,
            ignore_unexpected_child_shards: false,
            consistent_reads: false,
            list_shards_backoff_time_in_millis: 1_500,
            max_list_shards_retry_attempts: 50,
            epsilon_millis: 25,
            dynamo_db_request_timeout: default_request_timeout(),
            billing_mode: BillingMode::PayPerRequest,
            worker_utilization_aware_assignment_config:
                WorkerUtilizationAwareAssignmentConfig::default(),
            lease_assignment_strategy: LeaseAssignmentStrategy::WorkerUtilizationAware,
            lease_table_deletion_protection_enabled:
                DEFAULT_LEASE_TABLE_DELETION_PROTECTION_ENABLED,
            lease_table_pitr_enabled: DEFAULT_LEASE_TABLE_PITR_ENABLED,
            tags: Vec::new(),
            leases_recovery_auditor_execution_frequency_millis:
                DEFAULT_PERIODIC_SHARD_SYNC_INTERVAL_MILLIS,
            leases_recovery_auditor_inconsistency_confidence_threshold:
                DEFAULT_CONSECUTIVE_HOLES_FOR_TRIGGERING_LEASE_RECOVERY,
            max_cache_misses_before_reload: 1_000,
            list_shards_cache_allowed_age_in_seconds: 30,
            cache_miss_warning_modulus: 250,
            dynamo_db_lock_based_leader_lease_duration_in_millis: 120_000,
            dynamo_db_lock_based_leader_heartbeat_period_in_millis: 30_000,
            stream_info_mode: StreamInfoMode::Disabled,
            stream_id_onboarding_state: StreamIdOnboardingState::NotOnboarded,
            table_creator_callback: Arc::new(NoopTableCreatorCallback),
            graceful_lease_handoff_config: GracefulLeaseHandoffConfig::default(),
            consumer_task_factory: KinesisConsumerTaskFactory,
        }
    }

    // ---- getters ----

    pub fn table_name(&self) -> &str {
        &self.table_name
    }
    pub fn dynamo_db_client(&self) -> &aws_sdk_dynamodb::Client {
        &self.dynamo_db_client
    }
    pub fn kinesis_client(&self) -> &aws_sdk_kinesis::Client {
        &self.kinesis_client
    }
    pub fn stream_name(&self) -> &str {
        &self.stream_name
    }
    pub fn worker_identifier(&self) -> &str {
        &self.worker_identifier
    }
    pub fn failover_time_millis(&self) -> i64 {
        self.failover_time_millis
    }
    /// Derived default: `2 * failover_time_millis` iff unset (Java custom accessor).
    pub fn lease_assignment_interval_millis(&self) -> i64 {
        self.lease_assignment_interval_millis
            .unwrap_or(2 * self.failover_time_millis)
    }
    pub fn enable_priority_lease_assignment(&self) -> bool {
        self.enable_priority_lease_assignment
    }
    pub fn shard_sync_interval_millis(&self) -> i64 {
        self.shard_sync_interval_millis
    }
    pub fn cleanup_leases_upon_shard_completion(&self) -> bool {
        self.cleanup_leases_upon_shard_completion
    }
    pub fn lease_cleanup_config(&self) -> LeaseCleanupConfig {
        self.lease_cleanup_config
    }
    pub fn max_leases_for_worker(&self) -> i32 {
        self.max_leases_for_worker
    }
    pub fn max_leases_to_steal_at_one_time(&self) -> i32 {
        self.max_leases_to_steal_at_one_time
    }
    pub fn initial_lease_table_read_capacity(&self) -> i32 {
        self.initial_lease_table_read_capacity
    }
    pub fn initial_lease_table_write_capacity(&self) -> i32 {
        self.initial_lease_table_write_capacity
    }
    pub fn max_lease_renewal_threads(&self) -> i32 {
        self.max_lease_renewal_threads
    }
    pub fn lease_table_scan_total_segments(&self) -> i32 {
        self.lease_table_scan_total_segments
    }
    pub fn ignore_unexpected_child_shards(&self) -> bool {
        self.ignore_unexpected_child_shards
    }
    pub fn consistent_reads(&self) -> bool {
        self.consistent_reads
    }
    pub fn list_shards_backoff_time_in_millis(&self) -> i64 {
        self.list_shards_backoff_time_in_millis
    }
    pub fn max_list_shards_retry_attempts(&self) -> i32 {
        self.max_list_shards_retry_attempts
    }
    pub fn epsilon_millis(&self) -> i64 {
        self.epsilon_millis
    }
    pub fn dynamo_db_request_timeout(&self) -> Duration {
        self.dynamo_db_request_timeout
    }
    pub fn billing_mode(&self) -> &BillingMode {
        &self.billing_mode
    }
    pub fn worker_utilization_aware_assignment_config(
        &self,
    ) -> &WorkerUtilizationAwareAssignmentConfig {
        &self.worker_utilization_aware_assignment_config
    }
    pub fn lease_assignment_strategy(&self) -> LeaseAssignmentStrategy {
        self.lease_assignment_strategy
    }
    pub fn lease_table_deletion_protection_enabled(&self) -> bool {
        self.lease_table_deletion_protection_enabled
    }
    pub fn lease_table_pitr_enabled(&self) -> bool {
        self.lease_table_pitr_enabled
    }
    pub fn tags(&self) -> &[Tag] {
        &self.tags
    }
    pub fn leases_recovery_auditor_execution_frequency_millis(&self) -> i64 {
        self.leases_recovery_auditor_execution_frequency_millis
    }
    pub fn leases_recovery_auditor_inconsistency_confidence_threshold(&self) -> i32 {
        self.leases_recovery_auditor_inconsistency_confidence_threshold
    }
    pub fn max_cache_misses_before_reload(&self) -> i32 {
        self.max_cache_misses_before_reload
    }
    pub fn list_shards_cache_allowed_age_in_seconds(&self) -> i64 {
        self.list_shards_cache_allowed_age_in_seconds
    }
    pub fn cache_miss_warning_modulus(&self) -> i32 {
        self.cache_miss_warning_modulus
    }
    pub fn dynamo_db_lock_based_leader_lease_duration_in_millis(&self) -> i64 {
        self.dynamo_db_lock_based_leader_lease_duration_in_millis
    }
    pub fn dynamo_db_lock_based_leader_heartbeat_period_in_millis(&self) -> i64 {
        self.dynamo_db_lock_based_leader_heartbeat_period_in_millis
    }
    pub fn graceful_lease_handoff_config(&self) -> &GracefulLeaseHandoffConfig {
        &self.graceful_lease_handoff_config
    }
    pub fn consumer_task_factory(&self) -> &KinesisConsumerTaskFactory {
        &self.consumer_task_factory
    }
    pub fn table_creator_callback(&self) -> &Arc<dyn TableCreatorCallback> {
        &self.table_creator_callback
    }
    /// Set a custom [`TableCreatorCallback`] (fluent). Java
    /// `tableCreatorCallback(TableCreatorCallback)`.
    pub fn set_table_creator_callback(
        mut self,
        table_creator_callback: Arc<dyn TableCreatorCallback>,
    ) -> Self {
        self.table_creator_callback = table_creator_callback;
        self
    }
    pub fn stream_info_mode(&self) -> &StreamInfoMode {
        &self.stream_info_mode
    }
    pub fn stream_id_onboarding_state(&self) -> &StreamIdOnboardingState {
        &self.stream_id_onboarding_state
    }

    // ---- fluent setters (chainable, matching Lombok `this`-return) ----

    pub fn failover_time_millis_set(mut self, v: i64) -> Self {
        self.failover_time_millis = v;
        self
    }
    pub fn lease_assignment_interval_millis_set(mut self, v: i64) -> Self {
        self.lease_assignment_interval_millis = Some(v);
        self
    }
    pub fn shard_sync_interval_millis_set(mut self, v: i64) -> Self {
        self.shard_sync_interval_millis = v;
        self
    }
    pub fn cleanup_leases_upon_shard_completion_set(mut self, v: bool) -> Self {
        self.cleanup_leases_upon_shard_completion = v;
        self
    }
    pub fn max_leases_for_worker_set(mut self, v: i32) -> Self {
        self.max_leases_for_worker = v;
        self
    }
    pub fn max_leases_to_steal_at_one_time_set(mut self, v: i32) -> Self {
        self.max_leases_to_steal_at_one_time = v;
        self
    }
    pub fn billing_mode_set(mut self, v: BillingMode) -> Self {
        self.billing_mode = v;
        self
    }
    pub fn ignore_unexpected_child_shards_set(mut self, v: bool) -> Self {
        self.ignore_unexpected_child_shards = v;
        self
    }
    pub fn lease_assignment_strategy_set(mut self, v: LeaseAssignmentStrategy) -> Self {
        self.lease_assignment_strategy = v;
        self
    }
    pub fn graceful_lease_handoff_config_set(mut self, v: GracefulLeaseHandoffConfig) -> Self {
        self.graceful_lease_handoff_config = v;
        self
    }

    /// Set the number of parallel lease-table scan segments.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if `v <= 0` (leave unset for
    /// automatic sizing).
    pub fn lease_table_scan_total_segments_set(mut self, v: i32) -> Self {
        if v <= 0 {
            panic!("leaseTableScanTotalSegments must be a positive number; leave unset for automatic sizing");
        }
        self.lease_table_scan_total_segments = v;
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn clients() -> (aws_sdk_dynamodb::Client, aws_sdk_kinesis::Client) {
        let region = "us-east-1";
        let ddb = aws_sdk_dynamodb::Client::from_conf(
            aws_sdk_dynamodb::Config::builder()
                .behavior_version(aws_sdk_dynamodb::config::BehaviorVersion::latest())
                .region(aws_sdk_dynamodb::config::Region::new(region))
                .build(),
        );
        let kinesis = aws_sdk_kinesis::Client::from_conf(
            aws_sdk_kinesis::Config::builder()
                .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
                .region(aws_sdk_kinesis::config::Region::new(region))
                .build(),
        );
        (ddb, kinesis)
    }

    fn config() -> LeaseManagementConfig {
        let (ddb, kinesis) = clients();
        LeaseManagementConfig::new("myTable", ddb, kinesis, "myStream", "worker-1")
    }

    #[test]
    fn defaults_match_java() {
        let c = config();
        assert_eq!(c.failover_time_millis(), 10_000);
        assert_eq!(c.max_leases_for_worker(), i32::MAX);
        assert_eq!(c.max_leases_to_steal_at_one_time(), 1);
        assert_eq!(c.initial_lease_table_read_capacity(), 10);
        assert_eq!(c.initial_lease_table_write_capacity(), 10);
        assert_eq!(c.max_lease_renewal_threads(), 20);
        assert_eq!(c.list_shards_backoff_time_in_millis(), 1_500);
        assert_eq!(c.max_list_shards_retry_attempts(), 50);
        assert_eq!(c.epsilon_millis(), 25);
        assert_eq!(*c.billing_mode(), BillingMode::PayPerRequest);
        assert_eq!(
            c.lease_assignment_strategy(),
            LeaseAssignmentStrategy::WorkerUtilizationAware
        );
        assert!(c.cleanup_leases_upon_shard_completion());
        assert_eq!(c.max_cache_misses_before_reload(), 1_000);
        assert_eq!(c.list_shards_cache_allowed_age_in_seconds(), 30);
        assert_eq!(c.cache_miss_warning_modulus(), 250);
        assert_eq!(c.dynamo_db_request_timeout(), Duration::from_secs(60));
    }

    #[test]
    fn derived_lease_assignment_interval() {
        let c = config();
        // unset → 2 * failover.
        assert_eq!(c.lease_assignment_interval_millis(), 20_000);
        // explicitly set overrides the derived default.
        let c = config().lease_assignment_interval_millis_set(12_345);
        assert_eq!(c.lease_assignment_interval_millis(), 12_345);
        // changing failover after the fact recomputes the derived default.
        let c = config().failover_time_millis_set(5_000);
        assert_eq!(c.lease_assignment_interval_millis(), 10_000);
    }

    #[test]
    fn worker_utilization_defaults() {
        let w = WorkerUtilizationAwareAssignmentConfig::default();
        assert_eq!(w.in_memory_worker_metrics_capture_frequency_millis, 1_000);
        assert_eq!(w.worker_metrics_reporter_freq_in_millis, 30_000);
        assert_eq!(w.no_of_persisted_metrics_per_worker_metrics, 10);
        assert_eq!(w.dampening_percentage, 60);
        assert_eq!(w.re_balance_threshold_percentage, 10);
        assert!(w.allow_throughput_overshoot);
        assert_eq!(w.variance_balancing_frequency, 3);
        assert_eq!(w.worker_metrics_ema_alpha, 0.5);
        assert_eq!(w.max_throughput_per_host_kbps, f64::MAX);
        assert_eq!(
            w.stale_worker_metrics_entry_cleanup_duration,
            Duration::from_secs(86_400)
        );
    }

    #[test]
    fn graceful_handoff_defaults() {
        let g = GracefulLeaseHandoffConfig::default();
        assert_eq!(g.graceful_lease_handoff_timeout_millis(), 30_000);
        assert!(g.is_graceful_lease_handoff_enabled());
    }

    #[test]
    #[should_panic(expected = "leaseTableScanTotalSegments must be a positive number")]
    fn lease_table_scan_total_segments_rejects_non_positive() {
        config().lease_table_scan_total_segments_set(0);
    }

    #[test]
    fn fluent_setters_chain() {
        let c = config()
            .failover_time_millis_set(20_000)
            .max_leases_for_worker_set(5)
            .cleanup_leases_upon_shard_completion_set(false)
            .lease_table_scan_total_segments_set(4);
        assert_eq!(c.failover_time_millis(), 20_000);
        assert_eq!(c.max_leases_for_worker(), 5);
        assert!(!c.cleanup_leases_upon_shard_completion());
        assert_eq!(c.lease_table_scan_total_segments(), 4);
    }
}
