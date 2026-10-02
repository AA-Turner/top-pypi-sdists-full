//! Port of `software.amazon.kinesis.metrics.CloudWatchMetricsScope`.

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::metrics::cloud_watch_publisher_runnable::PublisherHandle;
use crate::metrics::scope_chain::FilteringLayer;
use crate::metrics::{
    CloudWatchMetricKey, FilteringMetricsScope, MetricDatumWithKey, MetricsLevel, MetricsScope,
};

/// The concrete CloudWatch [`MetricsScope`]. Extends the filtering/accumulating
/// chain (via an embedded [`FilteringMetricsScope`]) and, on
/// [`end`](MetricsScope::end), attaches the scope's dimensions to each
/// accumulated datum and enqueues the results to the publisher.
///
/// Port of `CloudWatchMetricsScope extends FilteringMetricsScope`.
pub struct CloudWatchMetricsScope {
    inner: FilteringMetricsScope,
    publisher: PublisherHandle,
}

impl CloudWatchMetricsScope {
    /// Creates a CloudWatch scope. Port of the Java constructor.
    pub fn new(
        publisher: PublisherHandle,
        metrics_level: MetricsLevel,
        metrics_enabled_dimensions: Option<Vec<String>>,
    ) -> Self {
        Self {
            inner: FilteringMetricsScope::new(FilteringLayer::new(
                metrics_level,
                metrics_enabled_dimensions,
            )),
            publisher,
        }
    }
}

impl MetricsScope for CloudWatchMetricsScope {
    fn add_data(&mut self, name: &str, value: f64, unit: StandardUnit) {
        self.inner.add_data(name, value, unit);
    }

    fn add_data_with_level(
        &mut self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        level: MetricsLevel,
    ) {
        self.inner.add_data_with_level(name, value, unit, level);
    }

    fn add_dimension(&mut self, name: &str, value: &str) {
        self.inner.add_dimension(name, value);
    }

    fn end(&mut self) {
        // super.end() runs the ended-guard from the accumulating chain.
        self.inner.end();

        // For each accumulated datum, attach the scope's dimensions, wrap in a
        // CloudWatchMetricKey + MetricDatumWithKey, and enqueue. Java iterates
        // `data.values()` (HashMap order, non-deterministic).
        let dimensions = self.inner.dimensions.dimensions().to_vec();
        let data_with_keys: Vec<MetricDatumWithKey<CloudWatchMetricKey>> = self
            .inner
            .accumulator
            .data()
            .values()
            .map(|datum| {
                // Rebuild datum with the scope dimensions (SDK models are
                // immutable; Java uses metricDatum.toBuilder().dimensions(...)).
                let mut builder = aws_sdk_cloudwatch::types::MetricDatum::builder();
                if let Some(n) = datum.metric_name() {
                    builder = builder.metric_name(n);
                }
                if let Some(u) = datum.unit() {
                    builder = builder.unit(u.clone());
                }
                if let Some(s) = datum.statistic_values() {
                    builder = builder.statistic_values(s.clone());
                }
                if !dimensions.is_empty() {
                    builder = builder.set_dimensions(Some(dimensions.clone()));
                }
                let datum = builder.build();
                MetricDatumWithKey::new(CloudWatchMetricKey::new(&datum), datum)
            })
            .collect();

        self.publisher.enqueue(data_with_keys);
    }
}
