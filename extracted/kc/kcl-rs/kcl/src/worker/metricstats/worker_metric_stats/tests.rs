//! Ports of `WorkerMetricsTest` + `WorkerMetricStatsEntityTypeTest`.

use std::collections::HashMap;

use super::super::worker_metric_stats::*;
use crate::leases::entity_dao::Entity;
use crate::leases::EntityType;

fn now_epoch() -> i64 {
    chrono::Utc::now().timestamp()
}

fn map_f64(entries: &[(&str, &[f64])]) -> HashMap<String, Vec<f64>> {
    entries
        .iter()
        .map(|(k, v)| (k.to_string(), v.to_vec()))
        .collect()
}

fn map_i64(entries: &[(&str, &[i64])]) -> HashMap<String, Vec<i64>> {
    entries
        .iter()
        .map(|(k, v)| (k.to_string(), v.to_vec()))
        .collect()
}

// ------------------------------ WorkerMetricsTest ------------------------------

#[test]
fn is_any_worker_metric_failing_with_failing_metric_true() {
    let stats = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("C", &[50.0, -1.0]), ("M", &[20.0, 11.0])]))
        .build();
    assert!(stats.is_any_worker_metric_failing());
}

#[test]
fn is_any_worker_metric_failing_without_failing_metric_false() {
    let stats = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("C", &[50.0, 1.0]), ("M", &[-1.0, 11.0])]))
        .build();
    assert!(!stats.is_any_worker_metric_failing());
}

#[test]
fn is_any_worker_metric_failing_without_any_values_false() {
    let stats = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("C", &[])]))
        .build();
    assert!(!stats.is_any_worker_metric_failing());
}

#[test]
fn is_valid_worker_metrics_sanity() {
    // default worker metric (no maps)
    let default_metric = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .build();
    assert!(default_metric.is_valid_worker_metric());
    assert!(default_metric.is_using_default_worker_metric());

    // empty maps => default
    let empty_maps = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .metric_stats(HashMap::new())
        .operating_range(HashMap::new())
        .last_update_time(now_epoch())
        .build();
    assert!(empty_maps.is_valid_worker_metric());
    assert!(empty_maps.is_using_default_worker_metric());

    // missing operating range
    let missing_op = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("C", &[])]))
        .build();
    assert!(!missing_op.is_valid_worker_metric());

    // missing last update time
    let missing_lut = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .metric_stats(map_f64(&[("C", &[5.0, 5.0])]))
        .operating_range(map_i64(&[("C", &[80, 10])]))
        .build();
    assert!(!missing_lut.is_valid_worker_metric());

    // missing resource metrics (only operating range)
    let missing_metrics = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .operating_range(map_i64(&[("C", &[80, 10])]))
        .build();
    assert!(!missing_metrics.is_valid_worker_metric());

    // mismatch keys
    let mismatch = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("C", &[5.0, 5.0])]))
        .operating_range(map_i64(&[("M", &[80, 10])]))
        .build();
    assert!(!mismatch.is_valid_worker_metric());

    // empty operating range value
    let empty_op_value = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("C", &[5.0, 5.0])]))
        .operating_range(map_i64(&[("C", &[])]))
        .build();
    assert!(!empty_op_value.is_valid_worker_metric());

    // no metric stats (empty map) but operating range present => valid (default)
    let no_metric_stats = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(HashMap::new())
        .operating_range(map_i64(&[("C", &[80, 10])]))
        .build();
    assert!(no_metric_stats.is_valid_worker_metric());

    // null resource metrics (only operating range) => invalid
    let null_metrics = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .operating_range(map_i64(&[("C", &[80, 10])]))
        .build();
    assert!(!null_metrics.is_valid_worker_metric());

    // zero max utilization => invalid
    let zero_max = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("C", &[5.0, 5.0])]))
        .operating_range(map_i64(&[("C", &[0, 10])]))
        .build();
    assert!(!zero_max.is_valid_worker_metric());

    // valid
    let valid = WorkerMetricStats::legacy_builder()
        .worker_id("WorkerId1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("C", &[5.0, 5.0])]))
        .operating_range(map_i64(&[("C", &[80, 10])]))
        .build();
    assert!(valid.is_valid_worker_metric());
}

// ----------------------- WorkerMetricStatsEntityTypeTest -----------------------

#[test]
fn implements_entity_interface() {
    let stats = WorkerMetricStats::builder().worker_id("worker-1").build();
    assert_eq!(stats.get_entity_type(), EntityType::WorkerMetricStats);
}

#[test]
fn get_entity_type_default_builder_returns_entity_type() {
    let stats = WorkerMetricStats::builder().worker_id("worker-1").build();
    assert_eq!(
        stats.entity_type_ddb_value().as_deref(),
        Some("WORKER_METRIC_STATS")
    );
}

#[test]
fn get_entity_type_when_set_explicitly() {
    let stats = WorkerMetricStats::builder()
        .worker_id("worker-1")
        .entity_type(EntityType::WorkerMetricStats)
        .build();
    assert_eq!(stats.entity_type(), Some(EntityType::WorkerMetricStats));
}

#[test]
fn get_entity_type_ddb_value_when_set() {
    let stats = WorkerMetricStats::builder()
        .worker_id("worker-1")
        .entity_type(EntityType::WorkerMetricStats)
        .build();
    assert_eq!(
        stats.entity_type_ddb_value().as_deref(),
        Some("WORKER_METRIC_STATS")
    );
}

#[test]
fn set_entity_type_ddb_value_sets_from_string() {
    let mut stats = WorkerMetricStats::builder().worker_id("worker-1").build();
    stats.set_entity_type_ddb_value(Some("WORKER_METRIC_STATS"));
    assert_eq!(stats.entity_type(), Some(EntityType::WorkerMetricStats));
}

#[test]
fn set_entity_type_ddb_value_unknown_sets_none() {
    let mut stats = WorkerMetricStats::builder()
        .worker_id("worker-1")
        .entity_type(EntityType::WorkerMetricStats)
        .build();
    stats.set_entity_type_ddb_value(Some("UNKNOWN_TYPE"));
    assert_eq!(stats.entity_type(), None);
}

#[test]
fn set_entity_type_ddb_value_null_sets_none() {
    let mut stats = WorkerMetricStats::builder()
        .worker_id("worker-1")
        .entity_type(EntityType::WorkerMetricStats)
        .build();
    stats.set_entity_type_ddb_value(None);
    assert_eq!(stats.entity_type(), None);
}

#[test]
fn is_expired_with_null_last_update_true() {
    let stats = WorkerMetricStats::builder().worker_id("worker-1").build();
    assert!(stats.is_expired(chrono::Duration::minutes(5)));
}

#[test]
fn is_expired_with_recent_update_false() {
    let stats = WorkerMetricStats::builder()
        .worker_id("worker-1")
        .last_update_time(now_epoch())
        .build();
    assert!(!stats.is_expired(chrono::Duration::minutes(5)));
}

#[test]
fn is_expired_with_old_update_true() {
    let ten_minutes_ago = now_epoch() - 10 * 60;
    let stats = WorkerMetricStats::builder()
        .worker_id("worker-1")
        .last_update_time(ten_minutes_ago)
        .build();
    assert!(stats.is_expired(chrono::Duration::minutes(5)));
}

#[test]
fn is_stale_with_null_last_update_true() {
    let stats = WorkerMetricStats::builder().worker_id("worker-1").build();
    assert!(stats.is_stale(chrono::Duration::hours(1)));
}

#[test]
fn is_stale_with_recent_update_false() {
    let stats = WorkerMetricStats::builder()
        .worker_id("worker-1")
        .last_update_time(now_epoch())
        .build();
    assert!(!stats.is_stale(chrono::Duration::hours(1)));
}

#[test]
fn is_stale_with_very_old_update_true() {
    let two_hours_ago = now_epoch() - 2 * 60 * 60;
    let stats = WorkerMetricStats::builder()
        .worker_id("worker-1")
        .last_update_time(two_hours_ago)
        .build();
    assert!(stats.is_stale(chrono::Duration::hours(1)));
}

#[test]
fn worker_support_info_expired_with_null_timestamp_true() {
    let info = WorkerSupportInfo::builder()
        .support_code(1)
        .maybe_support_code_update_epoch_seconds(None)
        .build();
    assert!(info.is_support_code_expired(chrono::Duration::minutes(5)));
}

#[test]
fn worker_support_info_expired_with_recent_timestamp_false() {
    let info = WorkerSupportInfo::builder()
        .support_code(1)
        .support_code_update_epoch_seconds(now_epoch())
        .build();
    assert!(!info.is_support_code_expired(chrono::Duration::minutes(5)));
}

#[test]
fn worker_support_info_expired_with_stale_timestamp_true() {
    let twenty_minutes_ago = now_epoch() - 20 * 60;
    let info = WorkerSupportInfo::builder()
        .support_code(1)
        .support_code_update_epoch_seconds(twenty_minutes_ago)
        .build();
    assert!(info.is_support_code_expired(chrono::Duration::minutes(5)));
}

#[test]
fn support_code_constant_matches_features_length() {
    assert_eq!(Features::values().len() as i32 - 1, support_code());
}

#[test]
fn features_enum_has_expected_values() {
    assert_eq!(Features::ZeroIndexPlaceholder.ordinal(), 0);
    assert_eq!(Features::SingleTableMigration.ordinal(), 1);
    assert_eq!(
        Features::ZeroIndexPlaceholder.name(),
        "ZERO_INDEX_PLACEHOLDER"
    );
    assert_eq!(
        Features::SingleTableMigration.name(),
        "SINGLE_TABLE_MIGRATION"
    );
}

#[test]
fn legacy_worker_metric_stats_get_worker_id() {
    let stats = WorkerMetricStats::legacy_builder()
        .worker_id("legacy-worker-1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("CPU", &[50.0])]))
        .build();
    assert_eq!(stats.worker_id(), Some("legacy-worker-1"));
    assert_eq!(stats.partition_variant(), PartitionKeyVariant::Legacy);
}

#[test]
fn lease_table_worker_metric_stats_get_worker_id() {
    let stats = WorkerMetricStats::lease_table_builder()
        .worker_id("lease-table-worker-1")
        .last_update_time(now_epoch())
        .metric_stats(map_f64(&[("CPU", &[50.0])]))
        .build();
    assert_eq!(stats.worker_id(), Some("lease-table-worker-1"));
    assert_eq!(stats.partition_variant(), PartitionKeyVariant::LeaseTable);
}

#[test]
fn lease_table_worker_metric_stats_implements_entity() {
    let mut stats = WorkerMetricStats::lease_table_builder().build();
    stats.set_worker_id("worker-1");
    assert_eq!(stats.get_entity_type(), EntityType::WorkerMetricStats);
}
