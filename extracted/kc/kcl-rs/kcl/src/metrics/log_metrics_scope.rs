//! Port of `software.amazon.kinesis.metrics.LogMetricsScope` and
//! `LogMetricsFactory`.

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::metrics::scope_chain::{Accumulator, DimensionSet};
use crate::metrics::{MetricsFactory, MetricsLevel, MetricsScope};

/// An accumulating [`MetricsScope`] that logs a formatted report on
/// [`end`](MetricsScope::end).
///
/// Port of `LogMetricsScope extends AccumulateByNameMetricsScope`.
///
/// **Behavioral asymmetry preserved from Java:** `LogMetricsScope.end()` does
/// **not** call `super.end()`, so the ended-guard is *never* activated. `end()`
/// can be called repeatedly, and `add_data`/`add_dimension` after `end` do not
/// panic — unlike every other scope in the accumulating chain. This is
/// preserved deliberately (do not "fix").
#[derive(Debug, Default)]
pub struct LogMetricsScope {
    dimensions: DimensionSet,
    accumulator: Accumulator,
}

impl LogMetricsScope {
    pub fn new() -> Self {
        Self::default()
    }

    /// Builds the multi-line report string (extracted so it can be tested
    /// without capturing log output). Mirrors the Java `end()` formatting.
    fn format_report(&self) -> String {
        let mut output = String::new();
        output.push_str("Metrics:\n");
        output.push_str("Dimensions: ");
        let mut needs_comma = false;
        for dimension in self.dimensions.dimensions() {
            output.push_str(&format!(
                "{}[{}: {}]",
                if needs_comma { ", " } else { "" },
                dimension.name().unwrap_or_default(),
                dimension.value().unwrap_or_default()
            ));
            needs_comma = true;
        }
        output.push('\n');

        for datum in self.accumulator.data().values() {
            let stats = datum.statistic_values().unwrap();
            let (min, max, count, sum) = (
                stats.minimum().unwrap_or(0.0),
                stats.maximum().unwrap_or(0.0),
                stats.sample_count().unwrap_or(0.0),
                stats.sum().unwrap_or(0.0),
            );
            output.push_str(&format!(
                "Name={:>25}\tMin={:.2}\tMax={:.2}\tCount={:.2}\tSum={:.2}\tAvg={:.2}\tUnit={}\n",
                datum.metric_name().unwrap_or_default(),
                min,
                max,
                count,
                sum,
                sum / count,
                datum.unit().map(|u| u.as_str()).unwrap_or_default(),
            ));
        }
        output
    }
}

impl MetricsScope for LogMetricsScope {
    fn add_data(&mut self, name: &str, value: f64, unit: StandardUnit) {
        self.accumulator.add_data(name, value, unit);
    }

    fn add_data_with_level(
        &mut self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        _level: MetricsLevel,
    ) {
        self.accumulator.add_data(name, value, unit);
    }

    fn add_dimension(&mut self, name: &str, value: &str) {
        // super.addDimension: add then throw if ended. But LogMetricsScope never
        // sets the ended flag (its end() skips super.end()), so this never
        // throws in practice.
        self.dimensions.add_dimension(name, value);
        if self.accumulator.is_ended() {
            panic!("Cannot call addDimension after calling IMetricsScope.end()");
        }
    }

    fn end(&mut self) {
        // NOTE: does NOT call the accumulator's end() — the ended-guard is never
        // activated, matching Java's LogMetricsScope.end() which omits
        // super.end().
        let report = self.format_report();
        tracing::info!("{}", report);
    }
}

/// A [`MetricsFactory`] that produces [`LogMetricsScope`]s.
///
/// Port of `LogMetricsFactory`.
#[derive(Debug, Default)]
pub struct LogMetricsFactory;

impl LogMetricsFactory {
    pub fn new() -> Self {
        Self
    }
}

impl MetricsFactory for LogMetricsFactory {
    fn create_metrics(&self) -> Box<dyn MetricsScope + Send> {
        Box::new(LogMetricsScope::new())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn end_does_not_activate_ended_guard() {
        let mut scope = LogMetricsScope::new();
        scope.add_data("foo", 1.0, StandardUnit::Count);
        scope.end();
        // Unlike other scopes, these do NOT panic after end().
        scope.end();
        scope.add_data("foo", 2.0, StandardUnit::Count);
        scope.add_dimension("d", "v");
    }

    #[test]
    fn report_contains_accumulated_metric() {
        let mut scope = LogMetricsScope::new();
        scope.add_dimension("Operation", "Op");
        scope.add_data("Latency", 4.0, StandardUnit::Milliseconds);
        scope.add_data("Latency", 6.0, StandardUnit::Milliseconds);
        let report = scope.format_report();
        assert!(report.contains("Metrics:"));
        assert!(report.contains("[Operation: Op]"));
        assert!(report.contains("Latency"));
        // Avg = sum/count = 10/2 = 5.00
        assert!(report.contains("Avg=5.00"));
        assert!(report.contains("Unit=Milliseconds"));
    }
}
