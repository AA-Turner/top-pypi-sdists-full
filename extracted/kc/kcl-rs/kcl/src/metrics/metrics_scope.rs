//! Port of `software.amazon.kinesis.metrics.MetricsScope` and `MetricsFactory`.

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::metrics::MetricsLevel;

/// Value that signifies that all dimensions are allowed for the metrics scope.
///
/// Port of `MetricsScope.METRICS_DIMENSIONS_ALL`.
pub const METRICS_DIMENSIONS_ALL: &str = "ALL";

/// A set of metric data points sharing a set of dimensions; the core
/// abstraction for all metrics emission in KCL.
///
/// Ported as a **synchronous** trait. Scope methods mutate accumulation state,
/// so they take `&mut self`. Contract violations (adding data/dimensions after
/// [`end`](MetricsScope::end), calling `end` twice, or accumulating with a
/// mismatched unit) `panic!` with the exact Java message, matching Java's
/// `void`-returning methods that throw `IllegalArgumentException` — none of
/// which KCL catches in this subsystem.
///
/// **Ordering contract** (preserved from Java): all
/// [`add_dimension`](MetricsScope::add_dimension) calls should precede
/// [`add_data`](MetricsScope::add_data) calls.
pub trait MetricsScope {
    /// Adds a data point. Multiple calls with the same `name` accumulate.
    ///
    /// Mirrors Java `addData(name, value, unit)`.
    fn add_data(&mut self, name: &str, value: f64, unit: StandardUnit);

    /// Adds a data point if the given metrics `level` is enabled. Multiple calls
    /// with the same `name` accumulate.
    ///
    /// Mirrors Java `addData(name, value, unit, level)`.
    fn add_data_with_level(
        &mut self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        level: MetricsLevel,
    );

    /// Adds a dimension that applies to all metrics in this scope.
    ///
    /// Mirrors Java `addDimension(name, value)`.
    fn add_dimension(&mut self, name: &str, value: &str);

    /// Flushes this scope and causes future `add_data`/`add_dimension` calls to
    /// fail (for scopes that enforce the ended guard).
    ///
    /// Mirrors Java `end()`.
    fn end(&mut self);
}

/// Factory for [`MetricsScope`] objects. Port of
/// `software.amazon.kinesis.metrics.MetricsFactory`.
pub trait MetricsFactory {
    /// Returns a new metrics scope of the type constructed by this factory.
    ///
    /// Mirrors Java `createMetrics()`. The returned scope is `Send` so it can be
    /// moved across the async runtime.
    fn create_metrics(&self) -> Box<dyn MetricsScope + Send>;

    /// Returns this factory as [`std::any::Any`] for downcasting to a concrete
    /// factory type. Enables the Java `instanceof` checks (e.g. verifying that
    /// [`MetricsConfig`](crate::metrics::MetricsConfig) selected the CloudWatch
    /// vs. OTel factory) that have no direct Rust analog. The default panics;
    /// concrete factories override it to return `self`.
    fn as_any(&self) -> &dyn std::any::Any {
        unimplemented!("as_any is not implemented for this MetricsFactory")
    }
}
