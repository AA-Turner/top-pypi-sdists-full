//! Port of the Java test-only `metrics.TestHelper`.
//!
//! Exposed (not `#[cfg(test)]`) so the ported tests across the metrics module
//! files can share it, mirroring how the Java `TestHelper` is shared across the
//! test package.

use aws_sdk_cloudwatch::types::{Dimension, MetricDatum, StandardUnit, StatisticSet};

/// Constructs a [`MetricDatum`] with the given statistic values.
///
/// Port of `TestHelper.constructDatum`.
pub fn construct_datum(
    name: &str,
    unit: StandardUnit,
    maximum: f64,
    minimum: f64,
    sum: f64,
    count: f64,
) -> MetricDatum {
    MetricDatum::builder()
        .metric_name(name)
        .unit(unit)
        .statistic_values(
            StatisticSet::builder()
                .maximum(maximum)
                .minimum(minimum)
                .sum(sum)
                .sample_count(count)
                .build(),
        )
        .build()
}

/// Constructs a [`Dimension`]. Port of `TestHelper.constructDimension`.
pub fn construct_dimension(name: &str, value: &str) -> Dimension {
    Dimension::builder().name(name).value(value).build()
}
