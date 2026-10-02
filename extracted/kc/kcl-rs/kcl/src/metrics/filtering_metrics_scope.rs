//! Port of `software.amazon.kinesis.metrics.FilteringMetricsScope`
//! (and, by composition, the `DimensionTracking`/`Ending`/`Accumulating`/
//! `AccumulateByName` chain beneath it).

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::metrics::scope_chain::{Accumulator, DimensionSet, FilteringLayer};
use crate::metrics::{MetricsLevel, MetricsScope};

/// A [`MetricsScope`] that filters `add_data` calls below a configured metrics
/// level and drops dimensions outside an allow-list, accumulating the rest by
/// name.
///
/// This is the concrete composition of Java's
/// `FilteringMetricsScope extends AccumulateByNameMetricsScope extends
/// AccumulatingMetricsScope<String> extends EndingMetricsScope extends
/// DimensionTrackingMetricsScope`. It is also the shared base state embedded by
/// [`CloudWatchMetricsScope`](crate::metrics::CloudWatchMetricsScope), which adds
/// publisher enqueue on `end`.
#[derive(Debug)]
pub struct FilteringMetricsScope {
    pub(crate) dimensions: DimensionSet,
    pub(crate) accumulator: Accumulator,
    pub(crate) filter: FilteringLayer,
}

impl Default for FilteringMetricsScope {
    /// Mirrors the no-arg `FilteringMetricsScope()`: `DETAILED` level, all
    /// dimensions enabled.
    fn default() -> Self {
        Self::new(FilteringLayer::default_all())
    }
}

impl FilteringMetricsScope {
    /// Creates a scope with an explicit filtering layer.
    pub fn new(filter: FilteringLayer) -> Self {
        Self {
            dimensions: DimensionSet::new(),
            accumulator: Accumulator::new(),
            filter,
        }
    }

    /// Creates a scope from a metrics level and enabled-dimensions set,
    /// mirroring `FilteringMetricsScope(MetricsLevel, Set<String>)`.
    pub fn with_level_and_dimensions(
        metrics_level: MetricsLevel,
        metrics_enabled_dimensions: Option<Vec<String>>,
    ) -> Self {
        Self::new(FilteringLayer::new(
            metrics_level,
            metrics_enabled_dimensions,
        ))
    }
}

impl MetricsScope for FilteringMetricsScope {
    fn add_data(&mut self, name: &str, value: f64, unit: StandardUnit) {
        // FilteringMetricsScope.addData(name,value,unit) delegates to the
        // level-aware overload at DETAILED.
        self.add_data_with_level(name, value, unit, MetricsLevel::Detailed);
    }

    fn add_data_with_level(
        &mut self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        level: MetricsLevel,
    ) {
        // FilteringMetricsScope.addData(...,level): drop if below enabled level,
        // else delegate to the accumulation path (super.addData(name,value,unit)
        // which resolves to AccumulatingMetricsScope's two-arg accumulate — the
        // `level` is intentionally dropped from that path).
        if self.filter.should_drop_data(level) {
            return;
        }
        self.accumulator.add_data(name, value, unit);
    }

    fn add_dimension(&mut self, name: &str, value: &str) {
        // FilteringMetricsScope.addDimension: drop unless enabled, else call
        // super.addDimension — which is EndingMetricsScope.addDimension: it adds
        // the dimension FIRST, then panics if the scope has ended (the
        // mutate-then-throw quirk we preserve exactly).
        if self.filter.should_drop_dimension(name) {
            return;
        }
        self.dimensions.add_dimension(name, value);
        if self.accumulator.is_ended() {
            panic!("Cannot call addDimension after calling IMetricsScope.end()");
        }
    }

    fn end(&mut self) {
        self.accumulator.end();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::test_helper;
    use aws_sdk_cloudwatch::types::StandardUnit;

    // Ported from FilteringMetricsScopeTest.assertMetrics: removes each expected
    // datum from the accumulator's map and asserts it matches, then asserts the
    // map is empty.
    fn assert_metrics(
        scope: &mut FilteringMetricsScope,
        expected: &[aws_sdk_cloudwatch::types::MetricDatum],
    ) {
        for exp in expected {
            let name = exp.metric_name().unwrap();
            let actual = scope.accumulator.data_mut().remove(name);
            assert_eq!(actual.as_ref(), Some(exp));
        }
        assert_eq!(
            scope.accumulator.data().len(),
            0,
            "Data should be empty at the end of assertMetrics"
        );
    }

    fn assert_dimensions(scope: &mut FilteringMetricsScope, dims: &[(&str, &str)]) {
        for (name, value) in dims {
            assert!(scope.dimensions.remove(name, value));
        }
        assert!(
            scope.dimensions.is_empty(),
            "Dimensions should be empty at the end of assertDimensions"
        );
    }

    #[test]
    fn test_default_add_all() {
        let mut scope = FilteringMetricsScope::default();
        scope.add_data_with_level(
            "detailedDataName",
            2.0,
            StandardUnit::Count,
            MetricsLevel::Detailed,
        );
        scope.add_data("noLevelDataName", 3.0, StandardUnit::Milliseconds);
        scope.add_dimension("dimensionName", "dimensionValue");

        assert_metrics(
            &mut scope,
            &[
                test_helper::construct_datum(
                    "detailedDataName",
                    StandardUnit::Count,
                    2.0,
                    2.0,
                    2.0,
                    1.0,
                ),
                test_helper::construct_datum(
                    "noLevelDataName",
                    StandardUnit::Milliseconds,
                    3.0,
                    3.0,
                    3.0,
                    1.0,
                ),
            ],
        );
        assert_dimensions(&mut scope, &[("dimensionName", "dimensionValue")]);
    }

    #[test]
    fn test_metrics_level() {
        let mut scope =
            FilteringMetricsScope::with_level_and_dimensions(MetricsLevel::Summary, None);
        scope.add_data_with_level(
            "summaryDataName",
            2.0,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "summaryDataName",
            10.0,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "detailedDataName",
            4.0,
            StandardUnit::Bytes,
            MetricsLevel::Detailed,
        );
        scope.add_data("noLevelDataName", 3.0, StandardUnit::Milliseconds);

        assert_metrics(
            &mut scope,
            &[test_helper::construct_datum(
                "summaryDataName",
                StandardUnit::Count,
                10.0,
                2.0,
                12.0,
                2.0,
            )],
        );
    }

    #[test]
    fn test_metrics_level_none() {
        let mut scope = FilteringMetricsScope::with_level_and_dimensions(MetricsLevel::None, None);
        scope.add_data_with_level(
            "summaryDataName",
            2.0,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "summaryDataName",
            10.0,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.add_data_with_level(
            "detailedDataName",
            4.0,
            StandardUnit::Bytes,
            MetricsLevel::Detailed,
        );
        scope.add_data("noLevelDataName", 3.0, StandardUnit::Milliseconds);

        // No metrics should be emitted.
        assert_metrics(&mut scope, &[]);
    }

    #[test]
    fn test_metrics_dimensions() {
        let mut scope = FilteringMetricsScope::with_level_and_dimensions(
            MetricsLevel::Detailed,
            Some(vec!["ShardId".to_string()]),
        );
        scope.add_dimension("ShardId", "shard-0001");
        scope.add_dimension("Operation", "ProcessRecords");
        scope.add_dimension("ShardId", "shard-0001");
        scope.add_dimension("ShardId", "shard-0002");
        scope.add_dimension("WorkerIdentifier", "testworker");

        assert_dimensions(
            &mut scope,
            &[("ShardId", "shard-0001"), ("ShardId", "shard-0002")],
        );
    }

    #[test]
    fn test_metrics_dimensions_all() {
        let mut scope = FilteringMetricsScope::with_level_and_dimensions(
            MetricsLevel::Detailed,
            Some(vec![
                "ThisDoesNotMatter".to_string(),
                crate::metrics::METRICS_DIMENSIONS_ALL.to_string(),
                "ThisAlsoDoesNotMatter".to_string(),
            ]),
        );
        scope.add_dimension("ShardId", "shard-0001");
        scope.add_dimension("Operation", "ProcessRecords");
        scope.add_dimension("ShardId", "shard-0001");
        scope.add_dimension("ShardId", "shard-0002");
        scope.add_dimension("WorkerIdentifier", "testworker");

        assert_dimensions(
            &mut scope,
            &[
                ("ShardId", "shard-0001"),
                ("ShardId", "shard-0002"),
                ("Operation", "ProcessRecords"),
                ("WorkerIdentifier", "testworker"),
            ],
        );
    }
}
