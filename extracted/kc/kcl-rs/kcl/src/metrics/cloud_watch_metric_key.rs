//! Port of `software.amazon.kinesis.metrics.CloudWatchMetricKey`.

use aws_sdk_cloudwatch::types::MetricDatum;

/// Identity of a CloudWatch metric — its dimensions plus metric name — used as a
/// dedup/aggregation key in [`MetricAccumulatingQueue`](crate::metrics::MetricAccumulatingQueue).
///
/// **Dimension-sorting fix (deviation from Java):** Java stores
/// `datum.dimensions()` as a `List<Dimension>` derived from a `HashSet`, whose
/// iteration order is not stable across scope instances. Two logically-identical
/// dimension sets built via different insertion orders could therefore produce
/// *unequal* keys, silently defeating aggregation. The arch map flags this as a
/// latent Java bug and recommends normalizing. This port **sorts** the
/// dimensions by `(name, value)` when building the key, so aggregation is
/// order-insensitive and correct. The stored dimension pairs are `(String,
/// String)` so the key derives `Eq`/`Hash` (the SDK `Dimension` implements
/// neither).
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct CloudWatchMetricKey {
    /// Sorted `(name, value)` dimension pairs.
    dimensions: Vec<(String, String)>,
    metric_name: Option<String>,
}

impl CloudWatchMetricKey {
    /// Builds a key from a metric datum, extracting and sorting its dimensions
    /// and taking its metric name.
    pub fn new(datum: &MetricDatum) -> Self {
        let mut dimensions: Vec<(String, String)> = datum
            .dimensions()
            .iter()
            .map(|d| {
                (
                    d.name().unwrap_or_default().to_string(),
                    d.value().unwrap_or_default().to_string(),
                )
            })
            .collect();
        dimensions.sort();
        Self {
            dimensions,
            metric_name: datum.metric_name().map(str::to_string),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use aws_sdk_cloudwatch::types::{Dimension, StandardUnit};

    fn datum_with_dims(name: &str, dims: &[(&str, &str)]) -> MetricDatum {
        let dimensions: Vec<Dimension> = dims
            .iter()
            .map(|(n, v)| Dimension::builder().name(*n).value(*v).build())
            .collect();
        MetricDatum::builder()
            .metric_name(name)
            .unit(StandardUnit::Count)
            .set_dimensions(Some(dimensions))
            .build()
    }

    #[test]
    fn equal_for_same_name_and_dimensions() {
        let a = CloudWatchMetricKey::new(&datum_with_dims("m", &[("x", "1"), ("y", "2")]));
        let b = CloudWatchMetricKey::new(&datum_with_dims("m", &[("x", "1"), ("y", "2")]));
        assert_eq!(a, b);
    }

    #[test]
    fn equal_regardless_of_dimension_order() {
        // The sorting fix makes these keys equal even though Java's list-order
        // comparison might not.
        let a = CloudWatchMetricKey::new(&datum_with_dims("m", &[("x", "1"), ("y", "2")]));
        let b = CloudWatchMetricKey::new(&datum_with_dims("m", &[("y", "2"), ("x", "1")]));
        assert_eq!(a, b);
    }

    #[test]
    fn unequal_for_different_name() {
        let a = CloudWatchMetricKey::new(&datum_with_dims("m1", &[("x", "1")]));
        let b = CloudWatchMetricKey::new(&datum_with_dims("m2", &[("x", "1")]));
        assert_ne!(a, b);
    }

    #[test]
    fn unequal_for_different_dimensions() {
        let a = CloudWatchMetricKey::new(&datum_with_dims("m", &[("x", "1")]));
        let b = CloudWatchMetricKey::new(&datum_with_dims("m", &[("x", "2")]));
        assert_ne!(a, b);
    }
}
