//! Port of `software.amazon.kinesis.metrics.NullMetricsScope` and
//! `NullMetricsFactory`.

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::metrics::{MetricsFactory, MetricsLevel, MetricsScope};

/// A no-op [`MetricsScope`] used when metrics are disabled. All methods do
/// nothing and never panic — it does not implement the accumulating chain's
/// ended-guard at all.
///
/// Port of `NullMetricsScope`.
#[derive(Debug, Default, Clone, Copy)]
pub struct NullMetricsScope;

impl NullMetricsScope {
    pub fn new() -> Self {
        Self
    }
}

impl MetricsScope for NullMetricsScope {
    fn add_data(&mut self, _name: &str, _value: f64, _unit: StandardUnit) {}
    fn add_data_with_level(
        &mut self,
        _name: &str,
        _value: f64,
        _unit: StandardUnit,
        _level: MetricsLevel,
    ) {
    }
    fn add_dimension(&mut self, _name: &str, _value: &str) {}
    fn end(&mut self) {}
}

/// A [`MetricsFactory`] that returns no-op scopes.
///
/// Port of `NullMetricsFactory`. Java returns a shared singleton
/// `NullMetricsScope`; because [`NullMetricsScope`] is a zero-sized, stateless
/// value, returning a fresh one per call is behaviorally identical (and required
/// by the `Box<dyn ... + Send>` return type).
#[derive(Debug, Default)]
pub struct NullMetricsFactory;

impl NullMetricsFactory {
    pub fn new() -> Self {
        Self
    }
}

impl MetricsFactory for NullMetricsFactory {
    fn create_metrics(&self) -> Box<dyn MetricsScope + Send> {
        Box::new(NullMetricsScope::new())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn null_scope_never_panics() {
        let mut scope = NullMetricsScope::new();
        scope.add_dimension("d", "v");
        scope.add_data("x", 1.0, StandardUnit::Count);
        scope.add_data_with_level("x", 1.0, StandardUnit::Count, MetricsLevel::Detailed);
        scope.end();
        // No ended-guard — everything is permitted after end().
        scope.end();
        scope.add_data("x", 2.0, StandardUnit::Count);
    }
}
