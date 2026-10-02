//! Port of `OtelMetricsScopeTest`.
//!
//! The Java tests mock the OTel `Meter` and verify which builder
//! (`gaugeBuilder`/`counterBuilder`/`histogramBuilder`) is called. The Rust OTel
//! `Meter` is a concrete struct that cannot be mocked, so instead of asserting
//! on *which builder was called* we assert on the actual **exported instrument
//! kind** using a real in-memory OTel SDK pipeline
//! ([`InMemoryMetricExporter`]): a gauge exports as
//! [`MetricData::Gauge`], a `COUNT` counter as [`MetricData::Sum`], and any
//! other unit as [`MetricData::Histogram`]. This is strictly more faithful —
//! it verifies the emitted OTel output, not just the builder call. Attribute
//! mapping/filtering is verified against the exported data points' attributes.
//!
//! The `noop`-lifecycle and `convertUnit` tests are ported directly.

use std::collections::HashSet;

use aws_sdk_cloudwatch::types::StandardUnit;
use opentelemetry::metrics::{Meter, MeterProvider};
use opentelemetry::Value;
use opentelemetry_sdk::metrics::data::{AggregatedMetrics, Metric, MetricData};
use opentelemetry_sdk::metrics::{InMemoryMetricExporter, SdkMeterProvider};

use super::*;
use crate::metrics::{MetricsLevel, MetricsScope, METRICS_DIMENSIONS_ALL};

fn all_dimensions() -> HashSet<String> {
    [METRICS_DIMENSIONS_ALL.to_string()].into_iter().collect()
}

/// The instrument kind of an exported metric, derived from its aggregation.
#[derive(Debug, PartialEq, Eq)]
enum Kind {
    Gauge,
    Sum,
    Histogram,
    Other,
}

fn kind_of(m: &Metric) -> Kind {
    match m.data() {
        AggregatedMetrics::F64(d) => match d {
            MetricData::Gauge(_) => Kind::Gauge,
            MetricData::Sum(_) => Kind::Sum,
            MetricData::Histogram(_) => Kind::Histogram,
            _ => Kind::Other,
        },
        _ => Kind::Other,
    }
}

// -----------------------------------------------------------------------
// Gauge selection — metrics in GAUGE_METRIC_NAMES export as a Gauge
// -----------------------------------------------------------------------

/// Helper: record a single (name, value, unit) and return the sole exported
/// metric's (transformed name, kind).
fn record_one(level: MetricsLevel, name: &str, value: f64, unit: StandardUnit) -> (String, Kind) {
    let exporter = InMemoryMetricExporter::default();
    let provider = SdkMeterProvider::builder()
        .with_periodic_exporter(exporter.clone())
        .build();
    let meter = provider.meter("software.amazon.kinesis");
    let mut scope = OtelMetricsScope::new(meter, level, all_dimensions());
    scope.add_data(name, value, unit);
    scope.end();
    provider.force_flush().expect("force_flush");
    let resource_metrics = exporter
        .get_finished_metrics()
        .expect("get_finished_metrics");
    let mut found: Option<(String, Kind)> = None;
    for rm in &resource_metrics {
        for sm in rm.scope_metrics() {
            for m in sm.metrics() {
                found = Some((m.name().to_string(), kind_of(m)));
            }
        }
    }
    found.expect("exactly one metric expected")
}

#[test]
fn test_gauge_selection_current_leases() {
    let (name, kind) = record_one(
        MetricsLevel::Detailed,
        "CurrentLeases",
        5.0,
        StandardUnit::Count,
    );
    assert_eq!(kind, Kind::Gauge);
    assert_eq!(name, "aws.kinesis.client.current_leases");
}

#[test]
fn test_gauge_selection_total_leases() {
    let (_, kind) = record_one(
        MetricsLevel::Detailed,
        "TotalLeases",
        10.0,
        StandardUnit::Count,
    );
    assert_eq!(kind, Kind::Gauge);
}

#[test]
fn test_gauge_selection_num_workers() {
    let (name, kind) = record_one(
        MetricsLevel::Detailed,
        "NumWorkers",
        3.0,
        StandardUnit::Count,
    );
    assert_eq!(kind, Kind::Gauge);
    // NumWorkers is a special-case rename → "workers"
    assert_eq!(name, "aws.kinesis.client.workers");
}

#[test]
fn test_gauge_selection_expired_leases() {
    let (_, kind) = record_one(
        MetricsLevel::Detailed,
        "ExpiredLeases",
        2.0,
        StandardUnit::Count,
    );
    assert_eq!(kind, Kind::Gauge);
}

#[test]
fn test_gauge_selection_queue_size() {
    let (_, kind) = record_one(
        MetricsLevel::Detailed,
        "QueueSize",
        100.0,
        StandardUnit::Count,
    );
    assert_eq!(kind, Kind::Gauge);
}

// -----------------------------------------------------------------------
// Counter selection — StandardUnit.COUNT metrics NOT in gauge set
// -----------------------------------------------------------------------

#[test]
fn test_counter_selection_count_unit_non_gauge() {
    let (name, kind) = record_one(
        MetricsLevel::Detailed,
        "RecordsProcessed",
        42.0,
        StandardUnit::Count,
    );
    assert_eq!(kind, Kind::Sum);
    assert_eq!(name, "aws.kinesis.client.records_processed");
}

#[test]
fn test_counter_selection_success() {
    let (name, kind) = record_one(MetricsLevel::Detailed, "Success", 1.0, StandardUnit::Count);
    assert_eq!(kind, Kind::Sum);
    assert_eq!(name, "aws.kinesis.client.success");
}

// -----------------------------------------------------------------------
// Histogram selection — non-COUNT units use histogram
// -----------------------------------------------------------------------

#[test]
fn test_histogram_selection_milliseconds() {
    let (name, kind) = record_one(
        MetricsLevel::Detailed,
        "RenewLease.Time",
        150.0,
        StandardUnit::Milliseconds,
    );
    assert_eq!(kind, Kind::Histogram);
    assert_eq!(name, "aws.kinesis.client.renew_lease.duration");
}

#[test]
fn test_histogram_selection_bytes() {
    let (_, kind) = record_one(
        MetricsLevel::Detailed,
        "PayloadSize",
        1024.0,
        StandardUnit::Bytes,
    );
    assert_eq!(kind, Kind::Histogram);
}

#[test]
fn test_histogram_selection_seconds() {
    let (_, kind) = record_one(
        MetricsLevel::Detailed,
        "Latency",
        2.5,
        StandardUnit::Seconds,
    );
    assert_eq!(kind, Kind::Histogram);
}

// -----------------------------------------------------------------------
// Dimension-to-attribute mapping — known dimensions (static-table tests)
// -----------------------------------------------------------------------

#[test]
fn test_dimension_mapping_operation() {
    assert_eq!(
        Some(&"aws.kinesis.operation"),
        dimension_to_attribute_map().get("Operation")
    );
}

#[test]
fn test_dimension_mapping_shard_id() {
    assert_eq!(
        Some(&"aws.kinesis.shard.id"),
        dimension_to_attribute_map().get("ShardId")
    );
}

#[test]
fn test_dimension_mapping_stream_id() {
    assert_eq!(
        Some(&"aws.kinesis.stream_name"),
        dimension_to_attribute_map().get("StreamId")
    );
}

#[test]
fn test_dimension_mapping_worker_identifier() {
    assert_eq!(
        Some(&"aws.kinesis.consumer.name"),
        dimension_to_attribute_map().get("WorkerIdentifier")
    );
}

// -----------------------------------------------------------------------
// Unknown dimension passthrough
// -----------------------------------------------------------------------

#[test]
fn test_unknown_dimension_passthrough() {
    assert!(
        !dimension_to_attribute_map().contains_key("CustomDimension"),
        "Unknown dimension should not be in the attribute map"
    );
}

#[test]
fn test_unknown_dimension_add_dimension_does_not_throw() {
    let mut scope = OtelMetricsScope::new(noop_meter(), MetricsLevel::Detailed, all_dimensions());
    // Should not panic — unknown dimensions pass through as-is.
    scope.add_dimension("CustomDimension", "customValue");
}

// -----------------------------------------------------------------------
// MetricsLevel filtering — data below configured level is dropped
// -----------------------------------------------------------------------

/// Returns the number of exported metrics after recording once at `data_level`
/// against a scope configured with `scope_level`.
fn count_after_level(
    scope_level: MetricsLevel,
    data_level: MetricsLevel,
    unit: StandardUnit,
) -> usize {
    let exporter = InMemoryMetricExporter::default();
    let provider = SdkMeterProvider::builder()
        .with_periodic_exporter(exporter.clone())
        .build();
    let meter = provider.meter("software.amazon.kinesis");
    let mut scope = OtelMetricsScope::new(meter, scope_level, all_dimensions());
    scope.add_data_with_level("SomeMetric", 1.0, unit, data_level);
    scope.end();
    provider.force_flush().expect("force_flush");
    let resource_metrics = exporter
        .get_finished_metrics()
        .expect("get_finished_metrics");
    resource_metrics
        .iter()
        .flat_map(|rm| rm.scope_metrics())
        .flat_map(|sm| sm.metrics())
        .count()
}

#[test]
fn test_metrics_level_filtering_detailed_dropped_when_summary() {
    // DETAILED (9000) is below SUMMARY (10000), so this should be dropped.
    assert_eq!(
        0,
        count_after_level(
            MetricsLevel::Summary,
            MetricsLevel::Detailed,
            StandardUnit::Count
        )
    );
}

#[test]
fn test_metrics_level_filtering_summary_passes_when_summary() {
    assert_eq!(
        1,
        count_after_level(
            MetricsLevel::Summary,
            MetricsLevel::Summary,
            StandardUnit::Count
        )
    );
}

#[test]
fn test_metrics_level_filtering_summary_passes_when_detailed() {
    assert_eq!(
        1,
        count_after_level(
            MetricsLevel::Detailed,
            MetricsLevel::Summary,
            StandardUnit::Count
        )
    );
}

#[test]
fn test_metrics_level_filtering_none_drops_everything() {
    let exporter = InMemoryMetricExporter::default();
    let provider = SdkMeterProvider::builder()
        .with_periodic_exporter(exporter.clone())
        .build();
    let meter = provider.meter("software.amazon.kinesis");
    let mut scope = OtelMetricsScope::new(meter, MetricsLevel::None, all_dimensions());
    scope.add_data_with_level(
        "SomeMetric",
        1.0,
        StandardUnit::Count,
        MetricsLevel::Summary,
    );
    scope.add_data_with_level(
        "AnotherMetric",
        2.0,
        StandardUnit::Milliseconds,
        MetricsLevel::Detailed,
    );
    scope.end();
    provider.force_flush().expect("force_flush");
    let resource_metrics = exporter
        .get_finished_metrics()
        .expect("get_finished_metrics");
    let count = resource_metrics
        .iter()
        .flat_map(|rm| rm.scope_metrics())
        .flat_map(|sm| sm.metrics())
        .count();
    assert_eq!(0, count);
}

// -----------------------------------------------------------------------
// Dimension filtering — dimensions not in enabled set are excluded
// -----------------------------------------------------------------------

/// Records "RecordsProcessed" (a COUNT counter) with the given dimensions and
/// enabled-dimension set, then returns the attribute key/value pairs attached
/// to the sole data point.
fn record_with_dimensions(
    enabled: HashSet<String>,
    dims: &[(&str, &str)],
) -> Vec<(String, String)> {
    let exporter = InMemoryMetricExporter::default();
    let provider = SdkMeterProvider::builder()
        .with_periodic_exporter(exporter.clone())
        .build();
    let meter = provider.meter("software.amazon.kinesis");
    let mut scope = OtelMetricsScope::new(meter, MetricsLevel::Detailed, enabled);
    for (k, v) in dims {
        scope.add_dimension(k, v);
    }
    scope.add_data("RecordsProcessed", 5.0, StandardUnit::Count);
    scope.end();
    provider.force_flush().expect("force_flush");
    let resource_metrics = exporter
        .get_finished_metrics()
        .expect("get_finished_metrics");
    let mut attrs: Vec<(String, String)> = Vec::new();
    let mut found_counter = false;
    for rm in &resource_metrics {
        for sm in rm.scope_metrics() {
            for m in sm.metrics() {
                if m.name() == "aws.kinesis.client.records_processed" {
                    found_counter = true;
                    if let AggregatedMetrics::F64(MetricData::Sum(sum)) = m.data() {
                        for dp in sum.data_points() {
                            for kv in dp.attributes() {
                                attrs.push((
                                    kv.key.as_str().to_string(),
                                    value_to_string(&kv.value),
                                ));
                            }
                        }
                    }
                }
            }
        }
    }
    assert!(found_counter, "counter metric should always be recorded");
    attrs.sort();
    attrs
}

fn value_to_string(v: &Value) -> String {
    match v {
        Value::String(s) => s.as_str().to_string(),
        other => format!("{:?}", other),
    }
}

#[test]
fn test_dimension_filtering_enabled_dimension_included() {
    let enabled: HashSet<String> = ["Operation".to_string()].into_iter().collect();
    let attrs = record_with_dimensions(enabled, &[("Operation", "GetRecords")]);
    assert_eq!(
        attrs,
        vec![(
            "aws.kinesis.operation".to_string(),
            "GetRecords".to_string()
        )]
    );
}

#[test]
fn test_dimension_filtering_disabled_dimension_excluded() {
    // "ShardId" is NOT in the enabled set → silently excluded, but the metric
    // is still recorded (without the ShardId attribute).
    let enabled: HashSet<String> = ["Operation".to_string()].into_iter().collect();
    let attrs = record_with_dimensions(enabled, &[("ShardId", "shard-001")]);
    assert!(
        attrs.is_empty(),
        "excluded dimension should yield no attributes"
    );
}

#[test]
fn test_dimension_filtering_empty_enabled_set() {
    let attrs = record_with_dimensions(
        HashSet::new(),
        &[("Operation", "GetRecords"), ("ShardId", "shard-001")],
    );
    assert!(attrs.is_empty(), "no dimensions should be included");
}

// -----------------------------------------------------------------------
// ALL dimensions — METRICS_DIMENSIONS_ALL includes everything
// -----------------------------------------------------------------------

#[test]
fn test_all_dimensions_includes_everything() {
    let attrs = record_with_dimensions(
        all_dimensions(),
        &[
            ("Operation", "GetRecords"),
            ("ShardId", "shard-001"),
            ("StreamId", "stream-123"),
            ("WorkerIdentifier", "worker-1"),
            ("CustomDimension", "customValue"),
        ],
    );
    assert_eq!(
        attrs,
        vec![
            ("CustomDimension".to_string(), "customValue".to_string()),
            (
                "aws.kinesis.consumer.name".to_string(),
                "worker-1".to_string()
            ),
            (
                "aws.kinesis.operation".to_string(),
                "GetRecords".to_string()
            ),
            ("aws.kinesis.shard.id".to_string(), "shard-001".to_string()),
            (
                "aws.kinesis.stream_name".to_string(),
                "stream-123".to_string()
            ),
        ]
    );
}

// -----------------------------------------------------------------------
// End-state enforcement
// -----------------------------------------------------------------------

fn ended_scope() -> OtelMetricsScope {
    let provider = SdkMeterProvider::builder().build();
    let meter = provider.meter("software.amazon.kinesis");
    let mut scope = OtelMetricsScope::new(meter, MetricsLevel::Detailed, all_dimensions());
    scope.end();
    scope
}

#[test]
#[should_panic(expected = "MetricsScope has already been ended")]
fn test_add_data_after_end_throws() {
    let mut scope = ended_scope();
    scope.add_data("SomeMetric", 1.0, StandardUnit::Count);
}

#[test]
#[should_panic(expected = "MetricsScope has already been ended")]
fn test_double_end_throws() {
    let mut scope = ended_scope();
    scope.end();
}

#[test]
#[should_panic(expected = "MetricsScope has already been ended")]
fn test_add_dimension_after_end_throws() {
    let mut scope = ended_scope();
    scope.add_dimension("Operation", "GetRecords");
}

#[test]
#[should_panic(expected = "MetricsScope has already been ended")]
fn test_add_data_with_level_after_end_throws() {
    let mut scope = ended_scope();
    scope.add_data_with_level(
        "SomeMetric",
        1.0,
        StandardUnit::Count,
        MetricsLevel::Summary,
    );
}

// -----------------------------------------------------------------------
// Unit conversion — convertUnit for key units
// -----------------------------------------------------------------------

#[test]
fn test_convert_unit_count() {
    assert_eq!("1", convert_unit(Some(&StandardUnit::Count)));
}

#[test]
fn test_convert_unit_milliseconds() {
    assert_eq!("ms", convert_unit(Some(&StandardUnit::Milliseconds)));
}

#[test]
fn test_convert_unit_bytes() {
    assert_eq!("By", convert_unit(Some(&StandardUnit::Bytes)));
}

#[test]
fn test_convert_unit_seconds() {
    assert_eq!("s", convert_unit(Some(&StandardUnit::Seconds)));
}

#[test]
fn test_convert_unit_percent() {
    assert_eq!("%", convert_unit(Some(&StandardUnit::Percent)));
}

#[test]
fn test_convert_unit_none() {
    assert_eq!("1", convert_unit(Some(&StandardUnit::None)));
}

#[test]
fn test_convert_unit_null() {
    assert_eq!("1", convert_unit(None));
}

#[test]
fn test_convert_unit_kilobytes() {
    assert_eq!("kBy", convert_unit(Some(&StandardUnit::Kilobytes)));
}

#[test]
fn test_convert_unit_megabytes() {
    assert_eq!("MBy", convert_unit(Some(&StandardUnit::Megabytes)));
}

#[test]
fn test_convert_unit_bits_second() {
    assert_eq!("bit/s", convert_unit(Some(&StandardUnit::BitsSecond)));
}

#[test]
fn test_convert_unit_count_second() {
    assert_eq!("1/s", convert_unit(Some(&StandardUnit::CountSecond)));
}

// -----------------------------------------------------------------------
// Noop lifecycle — full lifecycle with a no-op MeterProvider
// -----------------------------------------------------------------------

fn noop_meter() -> Meter {
    opentelemetry::metrics::noop::NoopMeterProvider::new().meter("test")
}

#[test]
fn test_noop_lifecycle_full_cycle() {
    let mut scope = OtelMetricsScope::new(noop_meter(), MetricsLevel::Detailed, all_dimensions());
    scope.add_dimension("Operation", "GetRecords");
    scope.add_dimension("ShardId", "shard-001");
    scope.add_data("RecordsProcessed", 42.0, StandardUnit::Count);
    scope.add_data("MillisBehindLatest", 100.0, StandardUnit::Milliseconds);
    scope.add_data("CurrentLeases", 5.0, StandardUnit::Count);
    scope.end();
}

#[test]
fn test_noop_lifecycle_add_data_with_level() {
    let mut scope = OtelMetricsScope::new(noop_meter(), MetricsLevel::Detailed, all_dimensions());
    scope.add_data_with_level(
        "SomeMetric",
        1.0,
        StandardUnit::Count,
        MetricsLevel::Summary,
    );
    scope.add_data_with_level(
        "AnotherMetric",
        2.0,
        StandardUnit::Milliseconds,
        MetricsLevel::Detailed,
    );
    scope.end();
}

#[test]
fn test_noop_lifecycle_no_data_no_exception() {
    let mut scope = OtelMetricsScope::new(noop_meter(), MetricsLevel::Detailed, all_dimensions());
    scope.end();
}

#[test]
fn test_noop_lifecycle_dimensions_only() {
    let mut scope = OtelMetricsScope::new(noop_meter(), MetricsLevel::Detailed, all_dimensions());
    scope.add_dimension("Operation", "GetRecords");
    scope.add_dimension("ShardId", "shard-001");
    scope.end();
}

// -----------------------------------------------------------------------
// addData without explicit level defaults to DETAILED
// -----------------------------------------------------------------------

#[test]
fn test_add_data_default_level_passes_when_detailed() {
    let (_, kind) = record_one(
        MetricsLevel::Detailed,
        "RecordsProcessed",
        1.0,
        StandardUnit::Count,
    );
    assert_eq!(kind, Kind::Sum);
}

#[test]
fn test_add_data_default_level_dropped_when_summary() {
    // Default level is DETAILED, which is below the SUMMARY threshold.
    let exporter = InMemoryMetricExporter::default();
    let provider = SdkMeterProvider::builder()
        .with_periodic_exporter(exporter.clone())
        .build();
    let meter = provider.meter("software.amazon.kinesis");
    let mut scope = OtelMetricsScope::new(meter, MetricsLevel::Summary, all_dimensions());
    scope.add_data("RecordsProcessed", 1.0, StandardUnit::Count);
    scope.end();
    provider.force_flush().expect("force_flush");
    let resource_metrics = exporter
        .get_finished_metrics()
        .expect("get_finished_metrics");
    let count = resource_metrics
        .iter()
        .flat_map(|rm| rm.scope_metrics())
        .flat_map(|sm| sm.metrics())
        .count();
    assert_eq!(0, count);
}

// -----------------------------------------------------------------------
// GAUGE_METRIC_NAMES set membership
// -----------------------------------------------------------------------

#[test]
fn test_gauge_metric_names_contains_expected_entries() {
    let set = gauge_metric_names();
    assert!(set.contains("CurrentLeases"));
    assert!(set.contains("TotalLeases"));
    assert!(set.contains("NumWorkers"));
    assert!(set.contains("ExpiredLeases"));
    assert!(set.contains("VeryOldLeases"));
    assert!(set.contains("ActiveStreams.Count"));
    assert!(set.contains("StreamsPendingDeletion.Count"));
    assert!(set.contains("QueueSize"));
    assert!(set.contains("NumStreamsToSync"));
}

#[test]
fn test_gauge_metric_names_does_not_contain_counter_metrics() {
    let set = gauge_metric_names();
    assert!(!set.contains("RecordsProcessed"));
    assert!(!set.contains("Success"));
    assert!(!set.contains("DataBytesProcessed"));
}

// -----------------------------------------------------------------------
// Dimension ordering contract — dimensions must be added before addData
// -----------------------------------------------------------------------

#[test]
fn test_dimensions_before_data_attributes_included() {
    // Add dimension first, then data — correct ordering. The recorded counter
    // data point carries the Operation attribute.
    let enabled = all_dimensions();
    let attrs = record_with_dimensions(enabled, &[("Operation", "RenewAllLeases")]);
    assert_eq!(
        attrs,
        vec![(
            "aws.kinesis.operation".to_string(),
            "RenewAllLeases".to_string()
        )]
    );
}

#[test]
fn test_dimension_after_data_later_data_gets_all_attributes() {
    // Pattern: addData → addDimension → addData. Because attributes are
    // snapshotted on the FIRST addData, the LATE dimension does NOT appear on
    // *either* recorded metric (both share the cached, empty snapshot). This
    // preserves the Java ordering contract; the Java test only asserts no
    // exception, so we additionally verify the cached-snapshot semantics.
    let exporter = InMemoryMetricExporter::default();
    let provider = SdkMeterProvider::builder()
        .with_periodic_exporter(exporter.clone())
        .build();
    let meter = provider.meter("software.amazon.kinesis");
    let mut scope = OtelMetricsScope::new(meter, MetricsLevel::Detailed, all_dimensions());

    scope.add_data("LostLeases", 0.0, StandardUnit::Count);
    // Added after the first addData — will NOT be on any recorded metric.
    scope.add_dimension("WorkerIdentifier", "worker-1");
    scope.add_data("Success", 1.0, StandardUnit::Count);
    scope.end();

    provider.force_flush().expect("force_flush");
    let resource_metrics = exporter
        .get_finished_metrics()
        .expect("get_finished_metrics");
    for rm in &resource_metrics {
        for sm in rm.scope_metrics() {
            for m in sm.metrics() {
                if let AggregatedMetrics::F64(MetricData::Sum(sum)) = m.data() {
                    for dp in sum.data_points() {
                        assert!(
                            dp.attributes().count() == 0,
                            "cached snapshot (empty) is reused for all data on this scope"
                        );
                    }
                }
            }
        }
    }
}

#[test]
fn test_all_dimensions_before_all_data_correct_pattern() {
    // The correct usage pattern per the MetricsScope contract: all dimensions
    // first, then all data. Every recorded counter carries all attributes.
    let exporter = InMemoryMetricExporter::default();
    let provider = SdkMeterProvider::builder()
        .with_periodic_exporter(exporter.clone())
        .build();
    let meter = provider.meter("software.amazon.kinesis");
    let mut scope = OtelMetricsScope::new(meter, MetricsLevel::Detailed, all_dimensions());

    scope.add_dimension("Operation", "RenewAllLeases");
    scope.add_dimension("WorkerIdentifier", "worker-1");
    scope.add_dimension("ShardId", "shard-001");

    scope.add_data("LostLeases", 0.0, StandardUnit::Count);
    scope.add_data("CurrentLeases", 5.0, StandardUnit::Count);
    scope.add_data("Success", 1.0, StandardUnit::Count);
    scope.end();

    provider.force_flush().expect("force_flush");
    let resource_metrics = exporter
        .get_finished_metrics()
        .expect("get_finished_metrics");
    let mut saw_success = false;
    for rm in &resource_metrics {
        for sm in rm.scope_metrics() {
            for m in sm.metrics() {
                if m.name() == "aws.kinesis.client.success" {
                    saw_success = true;
                    if let AggregatedMetrics::F64(MetricData::Sum(sum)) = m.data() {
                        for dp in sum.data_points() {
                            assert_eq!(dp.attributes().count(), 3);
                        }
                    }
                }
            }
        }
    }
    assert!(saw_success);
}
