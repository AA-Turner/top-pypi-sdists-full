//! Port of `software.amazon.kinesis.metrics.MetricsBackend`.

/// The available metrics publishing backends for the KCL.
///
/// Port of the Java `enum`. The `Otel` backend is deferred in this port (see
/// the `otel` stub module and `MetricsConfig`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum MetricsBackend {
    /// Publish metrics via the CloudWatch `PutMetricData` API.
    CloudWatch,
    /// Native OpenTelemetry library instrumentation backend.
    ///
    /// **Deferred in this port** — see [`crate::metrics::otel`].
    Otel,
}
