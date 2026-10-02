//! Port of the `WorkerMetricStatsDAODelegate` family (the abstract base plus the
//! `LeaseTableWorkerMetricStatsDAODelegate` and
//! `LegacyTableWorkerMetricStatsDAODelegate` subclasses), collapsed into one
//! delegate struct discriminated by [`DelegateKind`].
//!
//! # Async deviation
//! Java bridges the async Enhanced-Client calls to sync via
//! `FutureUtils.unwrappingFuture`. The Rust port stays **async** (`async fn`)
//! against the low-level `aws_sdk_dynamodb::Client`, since the SDK is
//! tokio-based (consistent with the rest of the leases/DAO ports). The Enhanced
//! Client `TableSchema.fromBean` mapping has no Rust analog — replaced by
//! [`super::super::ddb_serde`].
//!
//! # Test parity
//! The Java delegate tests (`WorkerMetricsDAOTest`) use `DynamoDBEmbedded` (a
//! real in-process DB) for CRUD round-trips + conditional-write semantics, which
//! mocks cannot replicate. Per the leases-6d-1 precedent, the CRUD/validation
//! **logic** is ported here but the end-to-end DB round-trip assertions are
//! **skipped** (see WAVE-PLAN TEST-PARITY GAPS). Validation is unit-tested
//! directly.

use std::collections::HashMap;

use aws_sdk_dynamodb::types::{AttributeValue, AttributeValueUpdate};
use aws_sdk_dynamodb::Client;

use super::super::ddb_serde::{self, partition_key_attribute_name};
use super::super::worker_metric_stats::{
    PartitionKeyVariant, WorkerMetricStats, KEY_LAST_UPDATE_TIME,
};
use crate::leases::dynamodb::dynamodb_lease_serializer::ENTITY_TYPE_ATTRIBUTE_NAME;
use crate::leases::exceptions::LeasingError;
use crate::leases::EntityType;

/// Which backing table the delegate targets.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DelegateKind {
    /// Legacy dedicated worker-metrics table (PK `wid`, no scan filter,
    /// DescribeTable-gated enablement).
    Legacy,
    /// Unified lease table (PK `leaseKey`, entityType scan filter, always
    /// enabled).
    LeaseTable,
}

impl DelegateKind {
    fn partition_variant(&self) -> PartitionKeyVariant {
        match self {
            DelegateKind::Legacy => PartitionKeyVariant::Legacy,
            DelegateKind::LeaseTable => PartitionKeyVariant::LeaseTable,
        }
    }
}

/// Shared delegate for reading/writing [`WorkerMetricStats`] from a DDB table.
pub struct WorkerMetricStatsDAODelegate {
    kind: DelegateKind,
    client: Client,
    table_name: String,
    worker_metrics_reporter_frequency_millis: i64,
    /// One-way `true -> false` on legacy-table-not-found (Java `enabled`
    /// volatile). Lease-table delegate stays `true`.
    enabled: std::sync::atomic::AtomicBool,
}

impl WorkerMetricStatsDAODelegate {
    /// Construct a lease-table delegate (Java `LeaseTableWorkerMetricStatsDAODelegate`).
    pub fn new_lease_table(
        client: Client,
        lease_table_name: impl Into<String>,
        worker_metrics_reporter_frequency_millis: i64,
    ) -> Self {
        Self {
            kind: DelegateKind::LeaseTable,
            client,
            table_name: lease_table_name.into(),
            worker_metrics_reporter_frequency_millis,
            enabled: std::sync::atomic::AtomicBool::new(true),
        }
    }

    /// Construct a legacy-table delegate (Java `LegacyTableWorkerMetricStatsDAODelegate`).
    pub fn new_legacy(
        client: Client,
        table_name: impl Into<String>,
        worker_metrics_reporter_frequency_millis: i64,
    ) -> Self {
        Self {
            kind: DelegateKind::Legacy,
            client,
            table_name: table_name.into(),
            worker_metrics_reporter_frequency_millis,
            enabled: std::sync::atomic::AtomicBool::new(true),
        }
    }

    /// The backing table name.
    pub fn table_name(&self) -> &str {
        &self.table_name
    }

    /// Whether the delegate is enabled (legacy table exists). Always `true` for
    /// the lease-table delegate.
    pub fn is_enabled(&self) -> bool {
        self.enabled.load(std::sync::atomic::Ordering::SeqCst)
    }

    /// Initialize the delegate. Lease table: no-op. Legacy: DescribeTable —
    /// ResourceNotFound => disable; other error => Dependency.
    pub async fn initialize(&self) -> Result<(), LeasingError> {
        match self.kind {
            DelegateKind::LeaseTable => Ok(()),
            DelegateKind::Legacy => {
                let result = self
                    .client
                    .describe_table()
                    .table_name(&self.table_name)
                    .send()
                    .await;
                match result {
                    Ok(_) => {
                        self.enabled
                            .store(true, std::sync::atomic::Ordering::SeqCst);
                        Ok(())
                    }
                    Err(e) => {
                        if e.as_service_error()
                            .map(|s| s.is_resource_not_found_exception())
                            .unwrap_or(false)
                        {
                            self.enabled
                                .store(false, std::sync::atomic::Ordering::SeqCst);
                            Ok(())
                        } else {
                            Err(LeasingError::dependency_caused_by(
                                format!(
                                    "Unable to determine if legacy WorkerMetricStats table {} exists",
                                    self.table_name
                                ),
                                e,
                            ))
                        }
                    }
                }
            }
        }
    }

    fn to_entity(&self, worker_metrics: &WorkerMetricStats) -> WorkerMetricStats {
        // Rebuild in the delegate's own variant (Java toEntity copies all
        // fields into the table-specific subclass; runtime-only fields reset).
        let mut builder = match self.kind {
            DelegateKind::Legacy => WorkerMetricStats::legacy_builder(),
            DelegateKind::LeaseTable => WorkerMetricStats::lease_table_builder(),
        };
        if let Some(w) = worker_metrics.worker_id() {
            builder = builder.worker_id(w);
        }
        if let Some(et) = worker_metrics.entity_type() {
            builder = builder.entity_type(et);
        }
        if let Some(lut) = worker_metrics.last_update_time() {
            builder = builder.last_update_time(lut);
        }
        if let Some(ms) = worker_metrics.metric_stats() {
            builder = builder.metric_stats(ms.clone());
        }
        if let Some(op) = worker_metrics.operating_range() {
            builder = builder.operating_range(op.clone());
        }
        if let Some(props) = worker_metrics.properties() {
            builder = builder.properties(props.clone());
        }
        if let Some(sup) = worker_metrics.support_code() {
            builder = builder.support_code(sup);
        }
        if let Some(slu) = worker_metrics.support_code_update_epoch_seconds() {
            builder = builder.support_code_update_epoch_seconds(slu);
        }
        builder.build()
    }

    /// Validate the worker metrics before writing (Java `validateWorkerMetrics`;
    /// `Preconditions.checkArgument` → panic on violation).
    pub fn validate_worker_metrics(&self, worker_metrics: &WorkerMetricStats) {
        self.validate_worker_metrics_with_now(worker_metrics, chrono::Utc::now().timestamp())
    }

    /// Testable validation with injectable "now" (epoch seconds).
    pub fn validate_worker_metrics_with_now(
        &self,
        worker_metrics: &WorkerMetricStats,
        now_epoch_seconds: i64,
    ) {
        let metric_stats = worker_metrics
            .metric_stats()
            .unwrap_or_else(|| panic!("ResourceMetrics not provided"));

        let entries_without_values: Vec<String> = metric_stats
            .iter()
            .filter(|(_, v)| v.is_empty())
            .map(|(k, _)| k.clone())
            .collect();
        if !entries_without_values.is_empty() {
            panic!(
                "Following metric stats dont have any values {:?}",
                entries_without_values
            );
        }

        let last_update_time = worker_metrics
            .last_update_time()
            .unwrap_or_else(|| panic!("LastUpdateTime field not set"));

        let elapsed_millis = (now_epoch_seconds - last_update_time) * 1000;
        if elapsed_millis >= 2 * self.worker_metrics_reporter_frequency_millis {
            panic!(
                "LastUpdateTime is more than 2x older than workerMetricsReporterFrequencyMillis"
            );
        }
    }

    /// Upsert the worker metrics (Java `updateMetrics`). Legacy: InvalidState if
    /// disabled.
    pub async fn update_metrics(
        &self,
        worker_metrics: &WorkerMetricStats,
    ) -> Result<(), LeasingError> {
        if self.kind == DelegateKind::Legacy && !self.is_enabled() {
            return Err(LeasingError::invalid_state(
                "Legacy WorkerMetricStats table does not exist, cannot update worker metrics",
            ));
        }
        let entity = self.to_entity(worker_metrics);
        self.validate_worker_metrics(worker_metrics);

        let item = ddb_serde::to_dynamo_record(&entity);
        let pk_attr = partition_key_attribute_name(self.kind.partition_variant());
        let key_value = item
            .get(pk_attr)
            .cloned()
            .expect("worker id (partition key) must be present for update");

        // ignoreNulls(true) upsert: PUT each present non-key attribute.
        let mut builder = self
            .client
            .update_item()
            .table_name(&self.table_name)
            .key(pk_attr, key_value);
        for (attr, value) in item {
            if attr == pk_attr {
                continue;
            }
            builder = builder.attribute_updates(
                attr,
                AttributeValueUpdate::builder()
                    .value(value)
                    .action(aws_sdk_dynamodb::types::AttributeAction::Put)
                    .build(),
            );
        }

        match builder.send().await {
            Ok(_) => Ok(()),
            Err(e) => {
                if e.as_service_error()
                    .map(|s| s.is_resource_not_found_exception())
                    .unwrap_or(false)
                {
                    Err(LeasingError::invalid_state(format!(
                        "Cannot update WorkerMetricStats, because table {} does not exist",
                        self.table_name
                    )))
                } else {
                    Err(LeasingError::dependency_caused_by(
                        "update WorkerMetricStats failed",
                        e,
                    ))
                }
            }
        }
    }

    /// Conditional delete gated on unchanged lastUpdateTime (Java
    /// `deleteMetrics`). Returns `false` on conditional-check failure.
    pub async fn delete_metrics(
        &self,
        worker_metrics: &WorkerMetricStats,
    ) -> Result<bool, LeasingError> {
        if self.kind == DelegateKind::Legacy && !self.is_enabled() {
            return Err(LeasingError::invalid_state(
                "Legacy WorkerMetricStats table does not exist, cannot delete worker metrics",
            ));
        }
        let worker_id = worker_metrics
            .worker_id()
            .unwrap_or_else(|| panic!("WorkerID is not provided"))
            .to_string();
        let last_update_time = worker_metrics
            .last_update_time()
            .unwrap_or_else(|| panic!("LastUpdateTime is not provided"));

        let pk_attr = partition_key_attribute_name(self.kind.partition_variant());
        let mut expression_names = HashMap::new();
        expression_names.insert("#key".to_string(), KEY_LAST_UPDATE_TIME.to_string());
        let mut expression_values = HashMap::new();
        expression_values.insert(
            ":value".to_string(),
            AttributeValue::N(last_update_time.to_string()),
        );

        let result = self
            .client
            .delete_item()
            .table_name(&self.table_name)
            .key(pk_attr, AttributeValue::S(worker_id))
            .condition_expression(format!("#key = :value AND attribute_exists ({})", pk_attr))
            .set_expression_attribute_names(Some(expression_names))
            .set_expression_attribute_values(Some(expression_values))
            .send()
            .await;

        match result {
            Ok(_) => Ok(true),
            Err(e) => {
                let svc = e.as_service_error();
                if svc
                    .map(|s| s.is_conditional_check_failed_exception())
                    .unwrap_or(false)
                {
                    tracing::warn!(
                        "Failed to delete WorkerMetricStats due to conditional failure for worker: {:?}",
                        worker_metrics.worker_id()
                    );
                    Ok(false)
                } else if svc
                    .map(|s| s.is_resource_not_found_exception())
                    .unwrap_or(false)
                {
                    Err(LeasingError::invalid_state(format!(
                        "Cannot delete WorkerMetricStats, because table {} does not exist",
                        self.table_name
                    )))
                } else {
                    Err(LeasingError::dependency_caused_by(
                        "delete WorkerMetricStats failed",
                        e,
                    ))
                }
            }
        }
    }

    /// Scan all worker metric stats (Java `getAllWorkerMetricStats`). Lease
    /// table filters by `entityType = WORKER_METRIC_STATS`; legacy scans
    /// unfiltered (returns empty if disabled).
    pub async fn get_all_worker_metric_stats(
        &self,
    ) -> Result<Vec<WorkerMetricStats>, LeasingError> {
        if self.kind == DelegateKind::Legacy && !self.is_enabled() {
            return Ok(Vec::new());
        }

        let mut results = Vec::new();
        let mut exclusive_start_key: Option<HashMap<String, AttributeValue>> = None;
        loop {
            let mut builder = self.client.scan().table_name(&self.table_name);
            if self.kind == DelegateKind::LeaseTable {
                let mut names = HashMap::new();
                names.insert("#et".to_string(), ENTITY_TYPE_ATTRIBUTE_NAME.to_string());
                let mut values = HashMap::new();
                values.insert(
                    ":etVal".to_string(),
                    AttributeValue::S(EntityType::WorkerMetricStats.ddb_value().to_string()),
                );
                builder = builder
                    .filter_expression("#et = :etVal")
                    .set_expression_attribute_names(Some(names))
                    .set_expression_attribute_values(Some(values));
            }
            if let Some(start) = exclusive_start_key.take() {
                builder = builder.set_exclusive_start_key(Some(start));
            }

            let output = match builder.send().await {
                Ok(o) => o,
                Err(e) => {
                    if e.as_service_error()
                        .map(|s| s.is_resource_not_found_exception())
                        .unwrap_or(false)
                    {
                        return Err(LeasingError::invalid_state(format!(
                            "Cannot scan WorkerMetricStats, because table {} does not exist",
                            self.table_name
                        )));
                    }
                    return Err(LeasingError::dependency_caused_by(
                        "scan WorkerMetricStats failed",
                        e,
                    ));
                }
            };

            if let Some(items) = output.items {
                for item in items {
                    results.push(ddb_serde::from_dynamo_record(
                        &item,
                        self.kind.partition_variant(),
                    ));
                }
            }
            match output.last_evaluated_key {
                Some(ref key) if !key.is_empty() => {
                    exclusive_start_key = Some(key.clone());
                }
                _ => break,
            }
        }
        Ok(results)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::worker::metricstats::worker_metric_stats::WorkerMetricStats;

    // A delegate for pure validation tests (no client calls). We build a dummy
    // client that is never invoked.
    fn dummy_delegate(freq_millis: i64) -> WorkerMetricStatsDAODelegate {
        let config = aws_sdk_dynamodb::Config::builder()
            .behavior_version(aws_sdk_dynamodb::config::BehaviorVersion::latest())
            .region(aws_config::Region::new("us-east-1"))
            .build();
        let client = Client::from_conf(config);
        WorkerMetricStatsDAODelegate::new_lease_table(client, "tbl", freq_millis)
    }

    #[test]
    fn validate_ok_for_recent_valid_metrics() {
        let d = dummy_delegate(10_000);
        let now = 1_000_000;
        let stats = WorkerMetricStats::lease_table_builder()
            .worker_id("w")
            .last_update_time(now)
            .metric_stats([("C".to_string(), vec![50.0])].into_iter().collect())
            .build();
        d.validate_worker_metrics_with_now(&stats, now);
    }

    #[test]
    #[should_panic(expected = "ResourceMetrics not provided")]
    fn validate_missing_metric_stats_panics() {
        let d = dummy_delegate(10_000);
        let stats = WorkerMetricStats::lease_table_builder()
            .worker_id("w")
            .last_update_time(100)
            .build();
        d.validate_worker_metrics_with_now(&stats, 100);
    }

    #[test]
    #[should_panic(expected = "dont have any values")]
    fn validate_empty_metric_values_panics() {
        let d = dummy_delegate(10_000);
        let stats = WorkerMetricStats::lease_table_builder()
            .worker_id("w")
            .last_update_time(100)
            .metric_stats([("C".to_string(), vec![])].into_iter().collect())
            .build();
        d.validate_worker_metrics_with_now(&stats, 100);
    }

    #[test]
    #[should_panic(expected = "LastUpdateTime field not set")]
    fn validate_missing_last_update_time_panics() {
        let d = dummy_delegate(10_000);
        let stats = WorkerMetricStats::lease_table_builder()
            .worker_id("w")
            .metric_stats([("C".to_string(), vec![50.0])].into_iter().collect())
            .build();
        d.validate_worker_metrics_with_now(&stats, 100);
    }

    #[test]
    #[should_panic(expected = "more than 2x older")]
    fn validate_stale_last_update_time_panics() {
        let d = dummy_delegate(10_000); // 2x = 20_000ms = 20s
        let now = 1_000_000;
        let stats = WorkerMetricStats::lease_table_builder()
            .worker_id("w")
            .last_update_time(now - 25) // 25s old > 20s
            .metric_stats([("C".to_string(), vec![50.0])].into_iter().collect())
            .build();
        d.validate_worker_metrics_with_now(&stats, now);
    }
}
