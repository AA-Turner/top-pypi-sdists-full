//! Port of `software.amazon.kinesis.metrics.MetricDatumWithKey`.

use aws_sdk_cloudwatch::types::MetricDatum;

/// A pair of an arbitrary key and an AWS SDK [`MetricDatum`], used throughout the
/// accumulation queue.
///
/// Port of the Lombok `@AllArgsConstructor @Setter @Accessors(fluent=true)`
/// class. In Java the fields are public and code reads/mutates them directly
/// (e.g. `metricDatumWithKey.datum(newDatum)`); in Rust they are `pub` fields
/// updated in place. `PartialEq` derives from both fields (the SDK `MetricDatum`
/// implements `PartialEq`).
#[derive(Debug, Clone, PartialEq)]
pub struct MetricDatumWithKey<K> {
    /// Key storing information about the datum (used for aggregation identity).
    pub key: K,
    /// The data point.
    pub datum: MetricDatum,
}

impl<K> MetricDatumWithKey<K> {
    /// Mirrors the Java `@AllArgsConstructor`.
    pub fn new(key: K, datum: MetricDatum) -> Self {
        Self { key, datum }
    }
}
