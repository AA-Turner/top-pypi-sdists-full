//! Port of `software.amazon.kinesis.metrics.OtelMetricsScope`.
//!
//! OTel-native [`MetricsScope`] that records observations **immediately** onto
//! OTel [`Meter`] instruments (a [`Histogram`](opentelemetry::metrics::Histogram)
//! by default, a [`Counter`](opentelemetry::metrics::Counter) for
//! `StandardUnit::Count`, a [`Gauge`](opentelemetry::metrics::Gauge) for the
//! gauge allow-list), tagging each observation with an attribute set built from
//! [`add_dimension`](MetricsScope::add_dimension) calls made so far.

use std::collections::{HashMap, HashSet};
use std::sync::OnceLock;

use aws_sdk_cloudwatch::types::StandardUnit;
use opentelemetry::metrics::Meter;
use opentelemetry::KeyValue;

use crate::metrics::otel::otel_metric_name_transformer;
use crate::metrics::{MetricsLevel, MetricsScope, METRICS_DIMENSIONS_ALL};

/// Mapping of KCL dimension names to OTel semantic-convention attribute keys.
///
/// Port of `OtelMetricsScope.DIMENSION_TO_ATTRIBUTE_MAP`, copied verbatim.
pub fn dimension_to_attribute_map() -> &'static HashMap<&'static str, &'static str> {
    static MAP: OnceLock<HashMap<&'static str, &'static str>> = OnceLock::new();
    MAP.get_or_init(|| {
        let mut map = HashMap::new();
        // MetricsUtil.OPERATION_DIMENSION_NAME
        map.insert("Operation", "aws.kinesis.operation");
        // MetricsUtil.SHARD_ID_DIMENSION_NAME
        map.insert("ShardId", "aws.kinesis.shard.id");
        // MetricsUtil.STREAM_IDENTIFIER
        map.insert("StreamId", "aws.kinesis.stream_name");
        map.insert("WorkerIdentifier", "aws.kinesis.consumer.name");
        map
    })
}

/// KCL metric names (original, pre-transformation) recorded as gauges rather
/// than counters or histograms.
///
/// Port of `OtelMetricsScope.GAUGE_METRIC_NAMES`, copied verbatim — including
/// the unusual casing of `"GsiReadyStatus"` (lowercase `s`).
pub fn gauge_metric_names() -> &'static HashSet<&'static str> {
    static SET: OnceLock<HashSet<&'static str>> = OnceLock::new();
    SET.get_or_init(|| {
        [
            "CurrentLeases",
            "TotalLeases",
            "NumWorkers",
            "ExpiredLeases",
            "VeryOldLeases",
            "ActiveStreams.Count",
            "StreamsPendingDeletion.Count",
            "QueueSize",
            "NumStreamsToSync",
            "NumWorkersWithInvalidEntry",
            "NumWorkersWithFailingWorkerMetric",
            "GsiReadyStatus",
            "WorkerMetricsReadyStatus",
            "CurrentState:3xWorker",
            "CurrentState:2xCompatibleWorker",
        ]
        .into_iter()
        .collect()
    })
}

/// Mapping of CloudWatch `StandardUnit` to OTel UCUM unit strings.
///
/// Port of `OtelMetricsScope.UNIT_MAP`, copied verbatim.
fn unit_map(unit: &StandardUnit) -> Option<&'static str> {
    Some(match unit {
        StandardUnit::Seconds => "s",
        StandardUnit::Microseconds => "us",
        StandardUnit::Milliseconds => "ms",
        StandardUnit::Bytes => "By",
        StandardUnit::Kilobytes => "kBy",
        StandardUnit::Megabytes => "MBy",
        StandardUnit::Gigabytes => "GBy",
        StandardUnit::Terabytes => "TBy",
        StandardUnit::Bits => "bit",
        StandardUnit::Kilobits => "kbit",
        StandardUnit::Megabits => "Mbit",
        StandardUnit::Gigabits => "Gbit",
        StandardUnit::Terabits => "Tbit",
        StandardUnit::Percent => "%",
        StandardUnit::Count => "1",
        StandardUnit::BytesSecond => "By/s",
        StandardUnit::KilobytesSecond => "kBy/s",
        StandardUnit::MegabytesSecond => "MBy/s",
        StandardUnit::GigabytesSecond => "GBy/s",
        StandardUnit::TerabytesSecond => "TBy/s",
        StandardUnit::BitsSecond => "bit/s",
        StandardUnit::KilobitsSecond => "kbit/s",
        StandardUnit::MegabitsSecond => "Mbit/s",
        StandardUnit::GigabitsSecond => "Gbit/s",
        StandardUnit::TerabitsSecond => "Tbit/s",
        StandardUnit::CountSecond => "1/s",
        StandardUnit::None => "1",
        _ => return None,
    })
}

/// Converts a CloudWatch `StandardUnit` to an OTel UCUM unit string, falling
/// back to `"1"` for an unknown unit.
///
/// Mirrors Java `OtelMetricsScope.convertUnit`. `None` (Java `null`) → `"1"`.
pub fn convert_unit(unit: Option<&StandardUnit>) -> &'static str {
    match unit {
        None => "1",
        Some(u) => unit_map(u).unwrap_or("1"),
    }
}

/// OTel-native metrics scope implementing [`MetricsScope`] directly.
///
/// Records raw observations immediately on the shared [`Meter`]. The OTel SDK
/// (configured by the application owner) handles aggregation, batching, and
/// export. Enforces its own ended-guard; contract violations `panic!` with the
/// exact Java message (Java throws `IllegalArgumentException`).
pub struct OtelMetricsScope {
    meter: Meter,
    metrics_level: MetricsLevel,
    metrics_enabled_dimensions: HashSet<String>,
    all_dimensions_enabled: bool,

    /// Attribute set accumulated from `add_dimension` calls.
    attributes: Vec<KeyValue>,
    /// Immutable snapshot of `attributes`, built once on the first `add_data`
    /// call and reused for all subsequent recordings (the ordering contract:
    /// dimensions added after the first `add_data` are dropped from future
    /// recorded metrics).
    cached_attributes: Option<Vec<KeyValue>>,
    ended: bool,
}

impl OtelMetricsScope {
    /// Creates an OTel-native metrics scope.
    ///
    /// Mirrors the Java constructor
    /// `OtelMetricsScope(Meter, MetricsLevel, Set<String>)`.
    pub fn new(
        meter: Meter,
        metrics_level: MetricsLevel,
        metrics_enabled_dimensions: HashSet<String>,
    ) -> Self {
        let all_dimensions_enabled = metrics_enabled_dimensions.contains(METRICS_DIMENSIONS_ALL);
        Self {
            meter,
            metrics_level,
            metrics_enabled_dimensions,
            all_dimensions_enabled,
            attributes: Vec::new(),
            cached_attributes: None,
            ended: false,
        }
    }

    fn record_observation_impl(
        meter: &Meter,
        name: &str,
        value: f64,
        unit: StandardUnit,
        attrs: &[KeyValue],
    ) {
        let is_gauge = gauge_metric_names().contains(name);
        let otel_name = otel_metric_name_transformer::transform_name(name);
        let otel_unit = convert_unit(Some(&unit));

        if is_gauge {
            let gauge = meter.f64_gauge(otel_name).with_unit(otel_unit).build();
            gauge.record(value, attrs);
        } else if unit == StandardUnit::Count {
            let counter = meter.f64_counter(otel_name).with_unit(otel_unit).build();
            counter.add(value, attrs);
        } else {
            let histogram = meter.f64_histogram(otel_name).with_unit(otel_unit).build();
            histogram.record(value, attrs);
        }
    }

    fn check_not_ended(&self) {
        if self.ended {
            panic!("MetricsScope has already been ended");
        }
    }
}

impl MetricsScope for OtelMetricsScope {
    fn add_data(&mut self, name: &str, value: f64, unit: StandardUnit) {
        self.add_data_with_level(name, value, unit, MetricsLevel::Detailed);
    }

    fn add_data_with_level(
        &mut self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        level: MetricsLevel,
    ) {
        self.check_not_ended();
        if level.value() < self.metrics_level.value() {
            return;
        }
        if self.cached_attributes.is_none() {
            self.cached_attributes = Some(self.attributes.clone());
        }
        // Both borrows are shared (record_observation takes &self and the
        // attributes slice by shared ref), so no clone is needed.
        let attrs = self.cached_attributes.as_ref().unwrap();
        Self::record_observation_impl(&self.meter, name, value, unit, attrs);
    }

    fn add_dimension(&mut self, name: &str, value: &str) {
        self.check_not_ended();
        if !self.all_dimensions_enabled && !self.metrics_enabled_dimensions.contains(name) {
            return;
        }
        let attr_key = dimension_to_attribute_map()
            .get(name)
            .copied()
            .unwrap_or(name)
            .to_string();
        self.attributes
            .push(KeyValue::new(attr_key, value.to_string()));
    }

    fn end(&mut self) {
        self.check_not_ended();
        self.ended = true;
    }
}

#[cfg(test)]
mod tests;
