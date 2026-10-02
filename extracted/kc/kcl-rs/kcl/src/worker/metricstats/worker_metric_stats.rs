//! Port of `software.amazon.kinesis.worker.metricstats.WorkerMetricStats`.
//!
//! Persistent per-worker DDB item capturing the rolling metric-stat history
//! plus derived (runtime-only) EMA averages used by lease assignment.
//!
//! # Porting notes
//! - Java's `@SuperBuilder` with two `@DynamoDbBean` subclasses
//!   (`LegacyWorkerMetricStats` PK `wid`, `LeaseTableWorkerMetricStats` PK
//!   `leaseKey`) is flattened into ONE [`WorkerMetricStats`] struct carrying a
//!   [`PartitionKeyVariant`] that records which table's PK attribute applies.
//!   [`WorkerMetricStats::legacy_builder`] / [`Self::lease_table_builder`]
//!   produce the two variants; [`WorkerMetricStats::builder`] defaults to the
//!   base (no partition variant — used by the entity-type tests).
//! - The `@DynamoDbIgnore` runtime fields (`metricStatsMap` memoization cache,
//!   `emaAlpha`) are excluded from equality and never serialized. The
//!   memoization cache uses a `Mutex<HashMap>` (needs `Send + Sync` as an
//!   `Entity`); [`WorkerMetricStats::get_metric_stat`] takes `&self` and
//!   compute-if-absents into it, preserving Java's stale-cache-by-design.
//! - `isExpired`/`isStale` read `Instant.now()` in Java; the port takes an
//!   injectable `now_epoch_seconds` on the `*_with_now` variants for testability
//!   and provides `is_expired`/`is_stale` calling the real clock.

use std::collections::HashMap;
use std::sync::Mutex;

use crate::leases::entity_dao::Entity;
use crate::leases::EntityType;
use crate::utils::ExponentialMovingAverage;
use crate::worker::metric::WorkerMetricType;

/// Which DDB table's partition-key attribute this record maps to.
///
/// Replaces Java's `LegacyWorkerMetricStats` (PK `wid`) /
/// `LeaseTableWorkerMetricStats` (PK `leaseKey`) subclasses.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum PartitionKeyVariant {
    /// No specific table variant (base `WorkerMetricStats`).
    Base,
    /// Legacy dedicated worker-metrics table (PK attribute `wid`).
    Legacy,
    /// Unified lease table (PK attribute `leaseKey`).
    LeaseTable,
}

/// Feature version list. Add new "breaking" features to the END (chronological
/// order). Java nested `enum Features`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Features {
    ZeroIndexPlaceholder,
    SingleTableMigration,
}

impl Features {
    /// The variants in declared order (Java `Features.values()`).
    pub fn values() -> &'static [Features] {
        &[
            Features::ZeroIndexPlaceholder,
            Features::SingleTableMigration,
        ]
    }

    /// The zero-based ordinal (Java `ordinal()`).
    pub fn ordinal(&self) -> i32 {
        match self {
            Features::ZeroIndexPlaceholder => 0,
            Features::SingleTableMigration => 1,
        }
    }

    /// The feature name string (Java `getName`).
    pub fn name(&self) -> &'static str {
        match self {
            Features::ZeroIndexPlaceholder => "ZERO_INDEX_PLACEHOLDER",
            Features::SingleTableMigration => "SINGLE_TABLE_MIGRATION",
        }
    }
}

/// The highest supported feature ordinal (`Features.values().length - 1`), the
/// support-code heartbeat value (Java `SUPPORT_CODE`).
pub fn support_code() -> i32 {
    Features::values().len() as i32 - 1
}

/// The DDB attribute name for lastUpdateTime (Java `KEY_LAST_UPDATE_TIME`).
pub const KEY_LAST_UPDATE_TIME: &str = "lut";
/// The DDB attribute name for the legacy worker-id PK (Java `KEY_WORKER_ID`).
pub const KEY_WORKER_ID: &str = "wid";
/// The DDB attribute name for the entityType discriminator.
pub const ENTITY_TYPE_ATTRIBUTE_NAME: &str = "entityType";

/// Immutable snapshot of a worker's support-code info (Java nested
/// `WorkerSupportInfo`).
#[derive(Debug, Clone, PartialEq, Eq, bon::Builder)]
pub struct WorkerSupportInfo {
    /// The support code reported by this worker (None on older versions).
    pub support_code: Option<i32>,
    /// Epoch seconds when the support code was last heartbeated (None if never).
    pub support_code_update_epoch_seconds: Option<i64>,
}

impl WorkerSupportInfo {
    /// Whether the support-code heartbeat is expired (Java
    /// `isSupportCodeExpired`), using `chrono::Utc::now()`.
    pub fn is_support_code_expired(&self, max_age: chrono::Duration) -> bool {
        self.is_support_code_expired_with_now(max_age, chrono::Utc::now().timestamp())
    }

    /// Testable variant of [`Self::is_support_code_expired`] with an injectable
    /// "now" (epoch seconds).
    pub fn is_support_code_expired_with_now(
        &self,
        max_age: chrono::Duration,
        now_epoch_seconds: i64,
    ) -> bool {
        match self.support_code_update_epoch_seconds {
            None => true,
            Some(ts) => {
                let elapsed = chrono::Duration::seconds(now_epoch_seconds - ts);
                elapsed > max_age
            }
        }
    }
}

/// Per-worker rolling metric-stat data model (Java `WorkerMetricStats`, both
/// subclasses folded in via [`PartitionKeyVariant`]).
#[derive(Debug)]
pub struct WorkerMetricStats {
    partition_variant: PartitionKeyVariant,
    worker_id: Option<String>,
    entity_type: Option<EntityType>,
    last_update_time: Option<i64>,
    metric_stats: Option<HashMap<String, Vec<f64>>>,
    operating_range: Option<HashMap<String, Vec<i64>>>,
    properties: Option<HashMap<String, String>>,
    support_code: Option<i32>,
    support_code_update_epoch_seconds: Option<i64>,
    // Runtime-only (@DynamoDbIgnore): memoized EMA averages + alpha.
    metric_stats_map: Mutex<HashMap<String, f64>>,
    ema_alpha: f64,
}

impl Clone for WorkerMetricStats {
    fn clone(&self) -> Self {
        Self {
            partition_variant: self.partition_variant,
            worker_id: self.worker_id.clone(),
            entity_type: self.entity_type,
            last_update_time: self.last_update_time,
            metric_stats: self.metric_stats.clone(),
            operating_range: self.operating_range.clone(),
            properties: self.properties.clone(),
            support_code: self.support_code,
            support_code_update_epoch_seconds: self.support_code_update_epoch_seconds,
            metric_stats_map: Mutex::new(
                self.metric_stats_map
                    .lock()
                    .unwrap_or_else(|e| e.into_inner())
                    .clone(),
            ),
            ema_alpha: self.ema_alpha,
        }
    }
}

impl PartialEq for WorkerMetricStats {
    /// Field equality excluding the runtime `metricStatsMap` / `emaAlpha`
    /// (Java `@EqualsAndHashCode` with `@Exclude` on those two).
    fn eq(&self, other: &Self) -> bool {
        self.worker_id == other.worker_id
            && self.entity_type == other.entity_type
            && self.last_update_time == other.last_update_time
            && self.metric_stats == other.metric_stats
            && self.operating_range == other.operating_range
            && self.properties == other.properties
            && self.support_code == other.support_code
            && self.support_code_update_epoch_seconds == other.support_code_update_epoch_seconds
    }
}

impl WorkerMetricStats {
    fn default_state(partition_variant: PartitionKeyVariant) -> Self {
        Self {
            partition_variant,
            worker_id: None,
            entity_type: Some(EntityType::WorkerMetricStats),
            last_update_time: None,
            metric_stats: None,
            operating_range: None,
            properties: None,
            support_code: None,
            support_code_update_epoch_seconds: None,
            metric_stats_map: Mutex::new(HashMap::new()),
            ema_alpha: 0.2,
        }
    }

    /// Base builder (Java `WorkerMetricStats.builder()` — no PK variant).
    pub fn builder() -> WorkerMetricStatsBuilder {
        WorkerMetricStatsBuilder::new(PartitionKeyVariant::Base)
    }

    /// Legacy-table builder (Java `LegacyWorkerMetricStats.builder()`, PK `wid`).
    pub fn legacy_builder() -> WorkerMetricStatsBuilder {
        WorkerMetricStatsBuilder::new(PartitionKeyVariant::Legacy)
    }

    /// Lease-table builder (Java `LeaseTableWorkerMetricStats.builder()`, PK
    /// `leaseKey`).
    pub fn lease_table_builder() -> WorkerMetricStatsBuilder {
        WorkerMetricStatsBuilder::new(PartitionKeyVariant::LeaseTable)
    }

    /// The partition-key table variant.
    pub fn partition_variant(&self) -> PartitionKeyVariant {
        self.partition_variant
    }

    /// The worker id (Java `getWorkerId`).
    pub fn worker_id(&self) -> Option<&str> {
        self.worker_id.as_deref()
    }

    /// Set the worker id (Java setter).
    pub fn set_worker_id(&mut self, worker_id: impl Into<String>) {
        self.worker_id = Some(worker_id.into());
    }

    /// The entity type (Java `getEntityType`).
    pub fn entity_type(&self) -> Option<EntityType> {
        self.entity_type
    }

    /// The entity-type DDB value (Java `getEntityTypeDdbValue`).
    pub fn entity_type_ddb_value(&self) -> Option<String> {
        self.entity_type.map(|e| e.ddb_value().to_string())
    }

    /// Set the entity type from a DDB value string (Java
    /// `setEntityTypeDdbValue`); unknown/None → `None`.
    pub fn set_entity_type_ddb_value(&mut self, ddb_value: Option<&str>) {
        self.entity_type = ddb_value.and_then(EntityType::from_ddb_value);
    }

    /// The last update time in epoch seconds.
    pub fn last_update_time(&self) -> Option<i64> {
        self.last_update_time
    }

    /// The raw metric-stat history map.
    pub fn metric_stats(&self) -> Option<&HashMap<String, Vec<f64>>> {
        self.metric_stats.as_ref()
    }

    /// The operating-range map.
    pub fn operating_range(&self) -> Option<&HashMap<String, Vec<i64>>> {
        self.operating_range.as_ref()
    }

    /// Java `setEmaAlpha(double)`. Invalidates the memoized per-metric EMA cache
    /// (a subsequent `get_metric_stat` recomputes with the new alpha).
    pub fn set_ema_alpha(&mut self, ema_alpha: f64) {
        self.ema_alpha = ema_alpha;
        self.metric_stats_map
            .lock()
            .unwrap_or_else(|e| e.into_inner())
            .clear();
    }

    /// Java `setMetricStats(Map)`. Invalidates the memoized per-metric EMA cache.
    pub fn set_metric_stats(&mut self, metric_stats: HashMap<String, Vec<f64>>) {
        self.metric_stats = Some(metric_stats);
        self.metric_stats_map
            .lock()
            .unwrap_or_else(|e| e.into_inner())
            .clear();
    }

    /// Java `setOperatingRange(Map)`.
    pub fn set_operating_range(&mut self, operating_range: HashMap<String, Vec<i64>>) {
        self.operating_range = Some(operating_range);
    }

    /// The extensibility properties map.
    pub fn properties(&self) -> Option<&HashMap<String, String>> {
        self.properties.as_ref()
    }

    /// The support code.
    pub fn support_code(&self) -> Option<i32> {
        self.support_code
    }

    /// The support-code update epoch seconds.
    pub fn support_code_update_epoch_seconds(&self) -> Option<i64> {
        self.support_code_update_epoch_seconds
    }

    /// Whether the given metric stat name is present (Java `containsMetricStat`).
    pub fn contains_metric_stat(&self, name: &str) -> bool {
        self.metric_stats
            .as_ref()
            .map(|m| m.contains_key(name))
            .unwrap_or(false)
    }

    /// Memoized EMA average for the metric name (Java `getMetricStat`; computes
    /// once and caches — later raw-list mutations are not reflected).
    pub fn get_metric_stat(&self, name: &str) -> f64 {
        let mut cache = self
            .metric_stats_map
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        if let Some(v) = cache.get(name) {
            return *v;
        }
        let values = self
            .metric_stats
            .as_ref()
            .and_then(|m| m.get(name))
            .cloned()
            .unwrap_or_default();
        let avg = self.compute_average(&values);
        cache.insert(name.to_string(), avg);
        avg
    }

    fn compute_average(&self, values: &[f64]) -> f64 {
        if values.is_empty() {
            return 0.0;
        }
        let mut ema = ExponentialMovingAverage::new(self.ema_alpha);
        for &v in values {
            // Skip -1 (metric-capture failure sentinel).
            if v != -1.0 {
                ema.add(v);
            }
        }
        ema.value()
    }

    /// Extrapolate one metric's value (Java private `extrapolateMetricsValue`).
    fn extrapolate_metrics_value(
        &self,
        metric_name: &str,
        fleet_level_metric_average: f64,
        average_throughput: f64,
        increase_throughput: f64,
        average_lease_count: f64,
        cache: &HashMap<String, f64>,
    ) -> f64 {
        let current = *cache.get(metric_name).unwrap_or(&0.0);
        if average_throughput > 0.0 {
            current + increase_throughput * fleet_level_metric_average / average_throughput
        } else {
            current + fleet_level_metric_average / average_lease_count
        }
    }

    /// Increase all metric-stat map values by the added-throughput extrapolation
    /// (Java `extrapolateMetricStatValuesForAddedThroughput`).
    pub fn extrapolate_metric_stat_values_for_added_throughput(
        &self,
        worker_metrics_to_fleet_level_average: &HashMap<String, f64>,
        average_throughput: f64,
        increase_throughput: f64,
        average_lease_count: f64,
    ) {
        let mut cache = self
            .metric_stats_map
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        let snapshot = cache.clone();
        for (key, slot) in cache.iter_mut() {
            let fleet = *worker_metrics_to_fleet_level_average
                .get(key)
                .unwrap_or(&0.0);
            *slot = self.extrapolate_metrics_value(
                key,
                fleet,
                average_throughput,
                increase_throughput,
                average_lease_count,
                &snapshot,
            );
        }
    }

    /// Whether any metric stat would exceed the fleet average or operating range
    /// after the added-throughput extrapolation (Java
    /// `willAnyMetricStatsGoAboveAverageUtilizationOrOperatingRange`).
    pub fn will_any_metric_stats_go_above_average_utilization_or_operating_range(
        &self,
        worker_metrics_to_fleet_level_average: &HashMap<String, f64>,
        average_throughput: f64,
        increase_throughput: f64,
        average_lease_count: f64,
    ) -> bool {
        let cache = self
            .metric_stats_map
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        let metric_stats = match &self.metric_stats {
            Some(m) => m,
            None => return false,
        };
        for metric_stat_name in metric_stats.keys() {
            let fleet = *worker_metrics_to_fleet_level_average
                .get(metric_stat_name)
                .unwrap_or(&0.0);
            let updated = self.extrapolate_metrics_value(
                metric_stat_name,
                fleet,
                average_throughput,
                increase_throughput,
                average_lease_count,
                &cache,
            );
            let op_first = self
                .operating_range
                .as_ref()
                .and_then(|o| o.get(metric_stat_name))
                .and_then(|v| v.first())
                .copied()
                .unwrap_or(0);
            if updated > fleet || updated > op_first as f64 {
                return true;
            }
        }
        false
    }

    /// Increase metric-stat map values for one added lease (Java
    /// `extrapolateMetricStatValuesForAddedLease`).
    pub fn extrapolate_metric_stat_values_for_added_lease(
        &self,
        worker_metric_to_fleet_level_average: &HashMap<String, f64>,
        average_lease_count: i32,
    ) {
        let mut cache = self
            .metric_stats_map
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        let keys: Vec<String> = cache.keys().cloned().collect();
        for key in keys {
            let current = *cache.get(&key).unwrap_or(&0.0);
            let fleet = *worker_metric_to_fleet_level_average
                .get(&key)
                .unwrap_or(&0.0);
            let updated = current + fleet / average_lease_count as f64;
            cache.insert(key, updated);
        }
    }

    /// Percentage of load to reach the fleet mean (Java
    /// `computePercentageToReachAverage`).
    pub fn compute_percentage_to_reach_average(
        &self,
        worker_metric_to_fleet_level_average: &HashMap<String, f64>,
    ) -> f64 {
        let mut min_difference_percentage = f64::MAX;
        let metric_stats = match &self.metric_stats {
            Some(m) => m,
            None => return min_difference_percentage,
        };
        for worker_metric_name in metric_stats.keys() {
            let metric_stat_value = self.get_metric_stat(worker_metric_name);
            let difference_ratio = if metric_stat_value == 0.0 {
                1.0
            } else {
                (*worker_metric_to_fleet_level_average
                    .get(worker_metric_name)
                    .unwrap_or(&0.0)
                    - metric_stat_value)
                    / metric_stat_value
            };
            min_difference_percentage = min_difference_percentage.min(difference_ratio);
        }
        min_difference_percentage
    }

    /// Whether any metric-stat list has `-1.0` as its last element (Java
    /// `isAnyWorkerMetricFailing`). Returns false when using the default metric.
    pub fn is_any_worker_metric_failing(&self) -> bool {
        if self.is_using_default_worker_metric() {
            return false;
        }
        let metric_stats = match &self.metric_stats {
            Some(m) => m,
            None => return false,
        };
        let mut response = false;
        for values in metric_stats.values() {
            if values.is_empty() {
                continue;
            }
            let last = values[values.len() - 1];
            if last == -1.0 {
                response = true;
                break;
            }
        }
        if response {
            tracing::warn!(
                "WorkerStats: {:?} has a WorkerMetric which is failing.",
                self
            );
        }
        response
    }

    /// Whether this entry is a valid worker metric (Java `isValidWorkerMetric`).
    pub fn is_valid_worker_metric(&self) -> bool {
        if self.last_update_time.is_none() {
            return false;
        }
        if self.is_using_default_worker_metric() {
            return true;
        }
        let metric_stats = match &self.metric_stats {
            Some(m) => m,
            None => return false,
        };
        let operating_range = match &self.operating_range {
            Some(o) => o,
            None => return false,
        };
        for key in metric_stats.keys() {
            if !operating_range.contains_key(key) {
                return false;
            }
        }
        for values in operating_range.values() {
            if values.is_empty() || values[0] == 0 {
                return false;
            }
        }
        true
    }

    /// Whether any metric stat is above the fleet average or operating range
    /// (Java `isAnyWorkerMetricAboveAverageUtilizationOrOperatingRange`).
    pub fn is_any_worker_metric_above_average_utilization_or_operating_range(
        &self,
        worker_metric_to_fleet_level_average: &HashMap<String, f64>,
    ) -> bool {
        if let Some(metric_stats) = &self.metric_stats {
            for worker_metric_name in metric_stats.keys() {
                let value = self.get_metric_stat(worker_metric_name);
                if value
                    > *worker_metric_to_fleet_level_average
                        .get(worker_metric_name)
                        .unwrap_or(&0.0)
                {
                    return true;
                }
            }
        }
        worker_metric_to_fleet_level_average
            .keys()
            .any(|k| self.is_worker_metric_above_operating_range(k))
    }

    /// Whether the worker uses the default (throughput fallback) metric (Java
    /// `isUsingDefaultWorkerMetric`).
    pub fn is_using_default_worker_metric(&self) -> bool {
        let metric_stats_empty = self
            .metric_stats
            .as_ref()
            .map(|m| m.is_empty())
            .unwrap_or(true);
        let operating_range_empty = self
            .operating_range
            .as_ref()
            .map(|o| o.is_empty())
            .unwrap_or(true);
        if metric_stats_empty && operating_range_empty {
            return true;
        }
        if let Some(metric_stats) = &self.metric_stats {
            return metric_stats
                .keys()
                .any(|k| k == WorkerMetricType::Throughput.name());
        }
        false
    }

    /// Whether the memoized metric stat exceeds the operating range for `name`
    /// (Java `isWorkerMetricAboveOperatingRange`).
    pub fn is_worker_metric_above_operating_range(&self, name: &str) -> bool {
        let cache = self
            .metric_stats_map
            .lock()
            .unwrap_or_else(|e| e.into_inner());
        match cache.get(name) {
            None => false,
            Some(&v) => {
                let op_first = self
                    .operating_range
                    .as_ref()
                    .and_then(|o| o.get(name))
                    .and_then(|l| l.first())
                    .copied()
                    .unwrap_or(0);
                v > op_first as f64
            }
        }
    }

    /// Whether the entry is expired (Java `isExpired`), using `chrono::Utc::now()`.
    pub fn is_expired(&self, max_age: chrono::Duration) -> bool {
        self.is_expired_with_now(max_age, chrono::Utc::now().timestamp())
    }

    /// Testable variant of [`Self::is_expired`] with an injectable "now".
    pub fn is_expired_with_now(&self, max_age: chrono::Duration, now_epoch_seconds: i64) -> bool {
        match self.last_update_time {
            None => true,
            Some(ts) => chrono::Duration::seconds(now_epoch_seconds - ts) > max_age,
        }
    }

    /// Whether the entry is stale (Java `isStale`), using `chrono::Utc::now()`.
    pub fn is_stale(&self, stale_cleanup_threshold: chrono::Duration) -> bool {
        self.is_stale_with_now(stale_cleanup_threshold, chrono::Utc::now().timestamp())
    }

    /// Testable variant of [`Self::is_stale`] with an injectable "now".
    pub fn is_stale_with_now(
        &self,
        stale_cleanup_threshold: chrono::Duration,
        now_epoch_seconds: i64,
    ) -> bool {
        match self.last_update_time {
            None => true,
            Some(ts) => chrono::Duration::seconds(now_epoch_seconds - ts) > stale_cleanup_threshold,
        }
    }
}

impl Entity for WorkerMetricStats {
    fn get_entity_type(&self) -> EntityType {
        // Always WORKER_METRIC_STATS (Java `implements EntityDAO.Entity`).
        EntityType::WorkerMetricStats
    }
    fn into_any(self: Box<Self>) -> Box<dyn std::any::Any> {
        self
    }
}

/// Builder for [`WorkerMetricStats`], mirroring the Lombok `@SuperBuilder`.
#[derive(Debug)]
pub struct WorkerMetricStatsBuilder {
    stats: WorkerMetricStats,
    // Track whether entityType was set explicitly (default builder leaves the
    // WORKER_METRIC_STATS default; matching Java `@Builder.Default`).
}

impl WorkerMetricStatsBuilder {
    fn new(partition_variant: PartitionKeyVariant) -> Self {
        Self {
            stats: WorkerMetricStats::default_state(partition_variant),
        }
    }

    /// Set the worker id.
    pub fn worker_id(mut self, v: impl Into<String>) -> Self {
        self.stats.worker_id = Some(v.into());
        self
    }
    /// Set the entity type.
    pub fn entity_type(mut self, v: EntityType) -> Self {
        self.stats.entity_type = Some(v);
        self
    }
    /// Set the last update time (epoch seconds).
    pub fn last_update_time(mut self, v: i64) -> Self {
        self.stats.last_update_time = Some(v);
        self
    }
    /// Set the raw metric-stats map.
    pub fn metric_stats(mut self, v: HashMap<String, Vec<f64>>) -> Self {
        self.stats.metric_stats = Some(v);
        self
    }
    /// Set the operating-range map.
    pub fn operating_range(mut self, v: HashMap<String, Vec<i64>>) -> Self {
        self.stats.operating_range = Some(v);
        self
    }
    /// Set the properties map.
    pub fn properties(mut self, v: HashMap<String, String>) -> Self {
        self.stats.properties = Some(v);
        self
    }
    /// Set the support code.
    pub fn support_code(mut self, v: i32) -> Self {
        self.stats.support_code = Some(v);
        self
    }
    /// Set the support-code update epoch seconds.
    pub fn support_code_update_epoch_seconds(mut self, v: i64) -> Self {
        self.stats.support_code_update_epoch_seconds = Some(v);
        self
    }
    /// Set the EMA alpha (defaults to 0.2).
    pub fn ema_alpha(mut self, v: f64) -> Self {
        self.stats.ema_alpha = v;
        self
    }
    /// Build the [`WorkerMetricStats`].
    pub fn build(self) -> WorkerMetricStats {
        self.stats
    }
}

#[cfg(test)]
mod tests;
