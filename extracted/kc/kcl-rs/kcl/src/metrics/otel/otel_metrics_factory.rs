//! Port of `software.amazon.kinesis.metrics.OtelMetricsFactory`.

use std::collections::HashSet;
use std::sync::Arc;

use opentelemetry::metrics::{Meter, MeterProvider};

use crate::metrics::otel::OtelMetricsScope;
use crate::metrics::{MetricsFactory, MetricsLevel, MetricsScope};

/// The OTel meter name (Java `openTelemetry.getMeter("software.amazon.kinesis")`).
const METER_NAME: &str = "software.amazon.kinesis";

/// A [`MetricsFactory`] for the OTel backend. Obtains a [`Meter`] named
/// `software.amazon.kinesis` from the supplied [`MeterProvider`] and produces
/// [`OtelMetricsScope`] instances sharing that meter, level, and enabled
/// dimensions.
///
/// Unlike `CloudWatchMetricsFactory`, construction has **no** side effects
/// beyond obtaining the [`Meter`] handle: no background threads, no custom
/// batching. The OTel SDK (configured by the application owner via the
/// [`MeterProvider`]) handles aggregation, batching, and export.
///
/// **Java `OpenTelemetry` → Rust [`MeterProvider`].** The Rust OTel API has no
/// single `OpenTelemetry` facade; the meter-provider trait object plays that
/// role. `OpenTelemetry.noop()` maps to a `NoopMeterProvider`, and
/// `GlobalOpenTelemetry.getOrNoop()` maps to
/// [`opentelemetry::global::meter_provider`].
pub struct OtelMetricsFactory {
    meter: Meter,
    metrics_level: MetricsLevel,
    metrics_enabled_dimensions: HashSet<String>,
}

impl OtelMetricsFactory {
    /// Creates the factory, obtaining a [`Meter`] from `meter_provider`.
    ///
    /// Mirrors the Java constructor
    /// `OtelMetricsFactory(OpenTelemetry, MetricsLevel, Set<String>)`. The
    /// enabled-dimensions set is defensively copied (Java `ImmutableSet.copyOf`).
    pub fn new(
        meter_provider: Arc<dyn MeterProvider + Send + Sync>,
        metrics_level: MetricsLevel,
        metrics_enabled_dimensions: HashSet<String>,
    ) -> Self {
        Self {
            meter: meter_provider.meter(METER_NAME),
            metrics_level,
            metrics_enabled_dimensions,
        }
    }

    /// No-op shutdown. The application owner is responsible for managing the
    /// OTel `MeterProvider` lifecycle (flushing and shutting down exporters).
    ///
    /// Mirrors Java `OtelMetricsFactory.shutdown()`.
    pub fn shutdown(&self) {
        // No-op: application owner manages MeterProvider lifecycle
    }
}

impl MetricsFactory for OtelMetricsFactory {
    fn create_metrics(&self) -> Box<dyn MetricsScope + Send> {
        Box::new(OtelMetricsScope::new(
            self.meter.clone(),
            self.metrics_level,
            self.metrics_enabled_dimensions.clone(),
        ))
    }

    fn as_any(&self) -> &dyn std::any::Any {
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::METRICS_DIMENSIONS_ALL;
    use aws_sdk_cloudwatch::types::StandardUnit;
    use opentelemetry::metrics::noop::NoopMeterProvider;

    fn all_dimensions() -> HashSet<String> {
        [METRICS_DIMENSIONS_ALL.to_string()].into_iter().collect()
    }

    fn noop() -> Arc<dyn MeterProvider + Send + Sync> {
        Arc::new(NoopMeterProvider::new())
    }

    // -----------------------------------------------------------------------
    // createMetrics returns OtelMetricsScope (usable scope)
    // -----------------------------------------------------------------------

    #[test]
    fn test_create_metrics_returns_otel_metrics_scope() {
        let factory = OtelMetricsFactory::new(noop(), MetricsLevel::Detailed, all_dimensions());
        let mut scope = factory.create_metrics();
        // A usable OtelMetricsScope — exercise it without panicking.
        scope.add_data("RecordsProcessed", 1.0, StandardUnit::Count);
        scope.end();
    }

    #[test]
    fn test_create_metrics_multiple_calls_return_distinct_scopes() {
        let factory = OtelMetricsFactory::new(noop(), MetricsLevel::Detailed, all_dimensions());
        let scope1 = factory.create_metrics();
        let scope2 = factory.create_metrics();
        // Distinct heap allocations (Java asserts scope1 != scope2 by identity).
        let p1 = scope1.as_ref() as *const _ as *const ();
        let p2 = scope2.as_ref() as *const _ as *const ();
        assert_ne!(p1, p2, "Each call should return a new scope instance");
    }

    // -----------------------------------------------------------------------
    // shutdown is no-op — completes without error
    // -----------------------------------------------------------------------

    #[test]
    fn test_shutdown_completes_without_error() {
        let factory = OtelMetricsFactory::new(noop(), MetricsLevel::Detailed, all_dimensions());
        factory.shutdown();
    }

    #[test]
    fn test_shutdown_can_be_called_multiple_times() {
        let factory = OtelMetricsFactory::new(noop(), MetricsLevel::Detailed, all_dimensions());
        factory.shutdown();
        factory.shutdown();
    }

    // -----------------------------------------------------------------------
    // Noop MeterProvider — factory works with the noop instance
    // -----------------------------------------------------------------------

    #[test]
    fn test_noop_open_telemetry_create_metrics_works() {
        let factory = OtelMetricsFactory::new(noop(), MetricsLevel::Detailed, all_dimensions());
        let mut scope = factory.create_metrics();
        scope.add_dimension("Operation", "GetRecords");
        scope.add_data("RecordsProcessed", 10.0, StandardUnit::Count);
        scope.end();
    }

    #[test]
    fn test_noop_open_telemetry_with_summary_level() {
        let factory = OtelMetricsFactory::new(noop(), MetricsLevel::Summary, all_dimensions());
        let mut scope = factory.create_metrics();
        // Exercise the scope; SUMMARY-level factory produces a working scope.
        scope.add_data("RecordsProcessed", 1.0, StandardUnit::Count);
        scope.end();
    }

    #[test]
    fn test_noop_open_telemetry_with_empty_dimensions() {
        let empty: HashSet<String> = HashSet::new();
        let factory = OtelMetricsFactory::new(noop(), MetricsLevel::Detailed, empty);
        let mut scope = factory.create_metrics();
        scope.add_data("RecordsProcessed", 1.0, StandardUnit::Count);
        scope.end();
    }

    #[test]
    fn test_noop_open_telemetry_with_none_level() {
        let factory = OtelMetricsFactory::new(noop(), MetricsLevel::None, all_dimensions());
        let mut scope = factory.create_metrics();
        // With NONE level, all data is dropped but no exceptions.
        scope.add_data_with_level(
            "SomeMetric",
            1.0,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.end();
    }

    // -----------------------------------------------------------------------
    // Constructor validation — null arguments
    //
    // The three Java `NullPointerException` tests (nullOpenTelemetry,
    // nullMetricsLevel, nullDimensions) have no Rust analog: `MeterProvider`,
    // `MetricsLevel`, and `HashSet<String>` are non-nullable by type, so the
    // Lombok `@NonNull` checks are enforced statically. Skipped (see final report).
    // -----------------------------------------------------------------------
}
