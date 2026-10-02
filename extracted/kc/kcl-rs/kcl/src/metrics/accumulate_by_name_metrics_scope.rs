//! Port of `software.amazon.kinesis.metrics.AccumulateByNameMetricsScope`,
//! `AccumulatingMetricsScope`, and `EndingMetricsScope`.
//!
//! Java models these as abstract classes in an inheritance chain. Because the
//! Rust port uses composition (see [`scope_chain`](crate::metrics::scope_chain)),
//! these become two concrete structs that embed the shared building blocks:
//! [`EndingMetricsScope`] (dimension storage + ended guard, no accumulation) and
//! [`AccumulateByNameMetricsScope`] (adds by-name statistic accumulation). They
//! exist primarily so the corresponding Java unit tests can be ported directly,
//! and to document the exact per-layer behavior.

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::metrics::scope_chain::{Accumulator, DimensionSet};
use crate::metrics::{MetricsLevel, MetricsScope};

/// The `EndingMetricsScope` layer as a standalone scope: dimension tracking plus
/// the one-shot ended guard, but **no** data storage.
///
/// Mirrors Java `EndingMetricsScope` exactly, including the two quirks:
/// * `add_data` (both overloads) only checks the ended flag and stores nothing
///   (subclasses do storage);
/// * `add_dimension` adds the dimension **first**, then panics if ended
///   (mutate-then-throw).
#[derive(Debug, Default)]
pub struct EndingMetricsScope {
    dimensions: DimensionSet,
    ended: bool,
}

impl EndingMetricsScope {
    pub fn new() -> Self {
        Self::default()
    }
}

impl MetricsScope for EndingMetricsScope {
    fn add_data(&mut self, _name: &str, _value: f64, _unit: StandardUnit) {
        if self.ended {
            panic!("Cannot call addData after calling IMetricsScope.end()");
        }
    }

    fn add_data_with_level(
        &mut self,
        _name: &str,
        _value: f64,
        _unit: StandardUnit,
        _level: MetricsLevel,
    ) {
        if self.ended {
            panic!("Cannot call addData after calling IMetricsScope.end()");
        }
    }

    fn add_dimension(&mut self, name: &str, value: &str) {
        self.dimensions.add_dimension(name, value);
        if self.ended {
            panic!("Cannot call addDimension after calling IMetricsScope.end()");
        }
    }

    fn end(&mut self) {
        if self.ended {
            panic!("Cannot call IMetricsScope.end() more than once on the same instance");
        }
        self.ended = true;
    }
}

/// The `AccumulateByNameMetricsScope` layer as a standalone scope: dimension
/// tracking, the ended guard, and by-name statistic accumulation — but **no**
/// level/dimension filtering.
///
/// Mirrors Java `AccumulateByNameMetricsScope`, whose `addData(...,level)`
/// overload ignores the level entirely (accumulates unconditionally).
#[derive(Debug, Default)]
pub struct AccumulateByNameMetricsScope {
    pub(crate) dimensions: DimensionSet,
    pub(crate) accumulator: Accumulator,
}

impl AccumulateByNameMetricsScope {
    pub fn new() -> Self {
        Self::default()
    }
}

impl MetricsScope for AccumulateByNameMetricsScope {
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
        // AccumulatingMetricsScope.addData(...,level) delegates to the two-arg
        // accumulate, ignoring the level (no filtering at this layer).
        self.accumulator.add_data(name, value, unit);
    }

    fn add_dimension(&mut self, name: &str, value: &str) {
        // super.addDimension (EndingMetricsScope): add then throw if ended.
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
mod ending_tests {
    use super::*;

    // Ported from EndingMetricsScopeTest.

    #[test]
    fn test_add_data_not_ended() {
        let mut scope = EndingMetricsScope::new();
        scope.add_data("foo", 1.0, StandardUnit::Count);
    }

    #[test]
    fn test_add_dimension_not_ended() {
        let mut scope = EndingMetricsScope::new();
        scope.add_dimension("foo", "bar");
    }

    #[test]
    #[should_panic(expected = "Cannot call addData after calling IMetricsScope.end()")]
    fn test_add_data_ended() {
        let mut scope = EndingMetricsScope::new();
        scope.end();
        scope.add_data("foo", 1.0, StandardUnit::Count);
    }

    #[test]
    #[should_panic(expected = "Cannot call addDimension after calling IMetricsScope.end()")]
    fn test_add_dimension_ended() {
        let mut scope = EndingMetricsScope::new();
        scope.end();
        scope.add_dimension("foo", "bar");
    }

    #[test]
    #[should_panic(
        expected = "Cannot call IMetricsScope.end() more than once on the same instance"
    )]
    fn test_double_end() {
        let mut scope = EndingMetricsScope::new();
        scope.end();
        scope.end();
    }

    // Locks in the documented mutate-then-throw quirk: add_dimension after end()
    // adds the dimension to the underlying set BEFORE panicking. We catch the
    // panic and then inspect state.
    #[test]
    fn add_dimension_after_end_mutates_then_panics() {
        let mut scope = EndingMetricsScope::new();
        scope.end();
        let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            scope.add_dimension("foo", "bar");
        }));
        assert!(result.is_err(), "add_dimension after end must panic");
        // The dimension was nonetheless added (Java's super.addDimension runs
        // before the throw).
        assert!(scope.dimensions.remove("foo", "bar"));
    }
}

#[cfg(test)]
mod accumulating_tests {
    use super::*;
    use crate::metrics::test_helper;

    // Ported from AccumulatingMetricsScopeTest. The Java TestScope extends
    // AccumulateByNameMetricsScope and asserts by removing from `data`.
    fn assert_metrics(
        scope: &mut AccumulateByNameMetricsScope,
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

    #[test]
    fn test_single_add() {
        let mut scope = AccumulateByNameMetricsScope::new();
        scope.add_data("name", 2.0, StandardUnit::Count);
        assert_metrics(
            &mut scope,
            &[test_helper::construct_datum(
                "name",
                StandardUnit::Count,
                2.0,
                2.0,
                2.0,
                1.0,
            )],
        );
    }

    #[test]
    fn test_accumulate() {
        let mut scope = AccumulateByNameMetricsScope::new();
        scope.add_data("name", 2.0, StandardUnit::Count);
        scope.add_data("name", 3.0, StandardUnit::Count);
        assert_metrics(
            &mut scope,
            &[test_helper::construct_datum(
                "name",
                StandardUnit::Count,
                3.0,
                2.0,
                5.0,
                2.0,
            )],
        );
    }

    #[test]
    #[should_panic(expected = "Cannot add to existing metric with different unit")]
    fn test_accumulate_wrong_unit() {
        let mut scope = AccumulateByNameMetricsScope::new();
        scope.add_data("name", 2.0, StandardUnit::Count);
        scope.add_data("name", 3.0, StandardUnit::Megabits);
    }
}
