//! Port of `software.amazon.kinesis.worker.metric.WorkerMetric` (the interface
//! plus the nested `WorkerMetricValue` model class).

use crate::worker::metric::{OperatingRange, WorkerMetricType};

/// A normalized 0-100 percentage value captured by a [`WorkerMetric`].
///
/// Port of the nested `WorkerMetric.WorkerMetricValue`. Java's Lombok `@Builder`
/// invokes a private constructor that validates `0 <= value <= 100`. The port
/// enforces the same invariant in [`WorkerMetricValue::new`] /
/// [`WorkerMetricValue::builder`], **panicking** (Java
/// `IllegalArgumentException`) with the exact message
/// `"{value} is either less than 0 or greater than 100"` on an out-of-range value.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct WorkerMetricValue {
    value: f64,
}

impl WorkerMetricValue {
    /// Construct a validated worker-metric value.
    ///
    /// # Panics
    /// Panics if `value` is `< 0` or `> 100` (Java `IllegalArgumentException`),
    /// with the same message format as Java.
    pub fn new(value: f64) -> Self {
        if !(0.0..=100.0).contains(&value) {
            panic!("{} is either less than 0 or greater than 100", value);
        }
        Self { value }
    }

    /// A builder mirroring Java `WorkerMetricValue.builder()`. `build()` runs
    /// the same range validation as [`WorkerMetricValue::new`].
    pub fn builder() -> WorkerMetricValueBuilder {
        WorkerMetricValueBuilder::default()
    }

    /// The normalized value (Java `getValue`).
    pub fn value(&self) -> f64 {
        self.value
    }
}

/// Builder for [`WorkerMetricValue`], mirroring the Lombok `@Builder`.
#[derive(Debug, Default)]
pub struct WorkerMetricValueBuilder {
    value: Option<f64>,
}

impl WorkerMetricValueBuilder {
    /// Set the value.
    pub fn value(mut self, v: f64) -> Self {
        self.value = Some(v);
        self
    }

    /// Build the [`WorkerMetricValue`], validating the range (panics on
    /// failure). Panics with `"value is marked non-null but is null"` if unset
    /// (Java Lombok `@NonNull` null-check).
    pub fn build(self) -> WorkerMetricValue {
        let value = self.value.expect("value is marked non-null but is null");
        WorkerMetricValue::new(value)
    }
}

/// Contract for a pluggable worker resource metric (CPU, memory, network, ...)
/// that can be captured as a normalized 0-100 percentage value.
///
/// Port of the Java `WorkerMetric` interface. `capture()` is synchronous (Java's
/// CPU/network implementations read `/proc`/cgroup files synchronously; the ECS
/// implementation performs blocking HTTP in Java — see [`EcsCpuWorkerMetric`]).
///
/// [`EcsCpuWorkerMetric`]: crate::worker::metric::EcsCpuWorkerMetric
pub trait WorkerMetric: Send + Sync + std::fmt::Debug {
    /// Short name used as the attribute name in storage (Java `getShortName`).
    fn short_name(&self) -> String;

    /// Capture the current normalized value (Java `capture`).
    fn capture(&self) -> WorkerMetricValue;

    /// The operating range for this metric (Java `getOperatingRange`).
    fn operating_range(&self) -> OperatingRange;

    /// The type of this metric (Java `getWorkerMetricType`).
    fn worker_metric_type(&self) -> WorkerMetricType;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn build_valid_cases() {
        // build does not panic => valid
        WorkerMetricValue::builder().value(0.0).build();
        WorkerMetricValue::builder().value(0.000001).build();
        WorkerMetricValue::builder().value(50.0).build();
        WorkerMetricValue::builder().value(100.0).build();
        WorkerMetricValue::builder().value(99.00001).build();
    }

    #[test]
    #[should_panic(expected = "less than 0 or greater than 100")]
    fn build_negative_panics() {
        WorkerMetricValue::builder().value(-1.0).build();
    }

    #[test]
    #[should_panic(expected = "less than 0 or greater than 100")]
    fn build_over_hundred_panics() {
        WorkerMetricValue::builder().value(100.00001).build();
    }
}
