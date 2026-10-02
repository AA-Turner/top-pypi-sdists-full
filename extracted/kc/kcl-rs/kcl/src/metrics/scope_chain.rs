//! Composable building blocks for the metrics scope inheritance chain.
//!
//! Java composes the CloudWatch scope through a deep inheritance chain:
//! `DimensionTrackingMetricsScope` ← `EndingMetricsScope` ←
//! `AccumulatingMetricsScope<KeyType>` ← `AccumulateByNameMetricsScope` ←
//! `FilteringMetricsScope` ← `CloudWatchMetricsScope`. This Rust port replaces
//! inheritance with **composition**: two small structs — [`DimensionSet`]
//! (dimension storage, from `DimensionTrackingMetricsScope`) and
//! [`Accumulator`] (the ended-guard + min/max/sum/sampleCount `StatisticSet`
//! accumulation by metric name, folding `EndingMetricsScope` +
//! `AccumulatingMetricsScope<String>` + `AccumulateByNameMetricsScope`) — plus a
//! [`FilteringLayer`] (`FilteringMetricsScope`'s level/dimension filtering).
//!
//! The concrete scopes (`FilteringMetricsScope`, `CloudWatchMetricsScope`,
//! `LogMetricsScope`) embed these and preserve the exact override order and
//! mutate-then-throw / check-then-noop quirks documented on each method.

use std::collections::HashMap;

use aws_sdk_cloudwatch::types::{Dimension, MetricDatum, StandardUnit, StatisticSet};

/// Dimension storage, porting `DimensionTrackingMetricsScope`.
///
/// Java uses a `HashSet<Dimension>` keyed by the SDK `Dimension`'s
/// `equals`/`hashCode` (name + value), collapsing duplicates. The Rust SDK
/// `Dimension` does not implement `Eq`/`Hash` (it may carry no fields that
/// hash), so this stores a `Vec<Dimension>` and de-duplicates on insert by
/// comparing `(name, value)` — the same collapsing behavior. Order is *not*
/// contractually meaningful (Java's `HashSet` iteration order is arbitrary), so
/// tests must not rely on it beyond set membership.
#[derive(Debug, Default, Clone)]
pub struct DimensionSet {
    dimensions: Vec<Dimension>,
}

impl DimensionSet {
    pub fn new() -> Self {
        Self::default()
    }

    /// Adds a dimension, collapsing duplicates by `(name, value)`.
    ///
    /// Mirrors `DimensionTrackingMetricsScope.addDimension`, which inserts into
    /// a `HashSet<Dimension>`.
    pub fn add_dimension(&mut self, name: &str, value: &str) {
        let exists = self
            .dimensions
            .iter()
            .any(|d| d.name() == Some(name) && d.value() == Some(value));
        if !exists {
            self.dimensions
                .push(Dimension::builder().name(name).value(value).build());
        }
    }

    /// The set of dimensions (Java `getDimensions`).
    pub fn dimensions(&self) -> &[Dimension] {
        &self.dimensions
    }

    /// Removes a matching dimension by `(name, value)`, returning whether one
    /// was present. Used by the ported `assertDimensions` test helper.
    pub fn remove(&mut self, name: &str, value: &str) -> bool {
        if let Some(idx) = self
            .dimensions
            .iter()
            .position(|d| d.name() == Some(name) && d.value() == Some(value))
        {
            self.dimensions.remove(idx);
            true
        } else {
            false
        }
    }

    pub fn is_empty(&self) -> bool {
        self.dimensions.is_empty()
    }
}

/// The ended-guard plus per-name `StatisticSet` accumulation, porting the
/// `EndingMetricsScope` + `AccumulatingMetricsScope<String>` +
/// `AccumulateByNameMetricsScope` slice of the chain.
///
/// Data is keyed by metric name (`AccumulateByNameMetricsScope.getKey` returns
/// the name). Contract violations panic with the exact Java messages.
#[derive(Debug, Default)]
pub struct Accumulator {
    ended: bool,
    /// Metric name -> accumulated datum. Java uses a plain `HashMap`, whose
    /// iteration order is unspecified.
    data: HashMap<String, MetricDatum>,
}

impl Accumulator {
    pub fn new() -> Self {
        Self::default()
    }

    /// The check performed by `EndingMetricsScope.addData` before any storage:
    /// panics if the scope has ended.
    fn check_add_data(&self) {
        if self.ended {
            panic!("Cannot call addData after calling IMetricsScope.end()");
        }
    }

    /// Accumulates a data point by name, porting
    /// `AccumulatingMetricsScope.addData(key, name, value, unit)` (with the
    /// `EndingMetricsScope.addData` ended-check performed first).
    ///
    /// The first datum for a name is created with
    /// `StatisticSet{max=min=sum=value, sampleCount=1.0}`. Subsequent data for
    /// the same name must share the same unit or this panics with
    /// `"Cannot add to existing metric with different unit"`; otherwise the
    /// statistics are merged (max/min/sum/sampleCount+1).
    pub fn add_data(&mut self, name: &str, value: f64, unit: StandardUnit) {
        // super.addData(...) in EndingMetricsScope: ended-check only.
        self.check_add_data();

        match self.data.get(name) {
            None => {
                let datum = MetricDatum::builder()
                    .metric_name(name)
                    .unit(unit)
                    .statistic_values(
                        StatisticSet::builder()
                            .maximum(value)
                            .minimum(value)
                            .sample_count(1.0)
                            .sum(value)
                            .build(),
                    )
                    .build();
                self.data.insert(name.to_string(), datum);
            }
            Some(existing) => {
                if existing.unit() != Some(&unit) {
                    panic!("Cannot add to existing metric with different unit");
                }
                let old = existing
                    .statistic_values()
                    .expect("accumulated datum always has statistic values");
                let new_stats = StatisticSet::builder()
                    .maximum(value.max(old.maximum().unwrap_or(value)))
                    .minimum(value.min(old.minimum().unwrap_or(value)))
                    .sample_count(old.sample_count().unwrap_or(0.0) + 1.0)
                    .sum(old.sum().unwrap_or(0.0) + value)
                    .build();
                // Rebuild the datum with merged statistics (SDK models are
                // immutable; Java uses toBuilder()).
                let dimensions = existing.dimensions().to_vec();
                let mut builder = MetricDatum::builder()
                    .metric_name(name)
                    .unit(unit)
                    .statistic_values(new_stats);
                if !dimensions.is_empty() {
                    builder = builder.set_dimensions(Some(dimensions));
                }
                self.data.insert(name.to_string(), builder.build());
            }
        }
    }

    /// The ended guard, porting `EndingMetricsScope.end()`: panics if already
    /// ended, else marks ended.
    pub fn end(&mut self) {
        if self.ended {
            panic!("Cannot call IMetricsScope.end() more than once on the same instance");
        }
        self.ended = true;
    }

    /// Whether `end()` has been called.
    pub fn is_ended(&self) -> bool {
        self.ended
    }

    /// The accumulated data map, keyed by metric name.
    pub fn data(&self) -> &HashMap<String, MetricDatum> {
        &self.data
    }

    /// Mutable access to the accumulated data map (used by ported test helpers
    /// mirroring `data.remove(name)`).
    pub fn data_mut(&mut self) -> &mut HashMap<String, MetricDatum> {
        &mut self.data
    }
}

/// The level/dimension filtering slice, porting `FilteringMetricsScope`'s
/// filtering decisions (independent of the underlying accumulation, which the
/// embedding scope owns).
#[derive(Debug, Clone)]
pub struct FilteringLayer {
    metrics_level: crate::metrics::MetricsLevel,
    metrics_enabled_dimensions: Vec<String>,
    metrics_enabled_dimensions_all: bool,
}

impl FilteringLayer {
    /// Creates a filtering layer that drops data below `metrics_level` and only
    /// allows dimensions in `metrics_enabled_dimensions` (unless the sentinel
    /// [`METRICS_DIMENSIONS_ALL`](crate::metrics::METRICS_DIMENSIONS_ALL) is
    /// present).
    ///
    /// `metrics_enabled_dimensions == None` mirrors Java passing a `null` set:
    /// the "all" flag is false and every named dimension is dropped.
    pub fn new(
        metrics_level: crate::metrics::MetricsLevel,
        metrics_enabled_dimensions: Option<Vec<String>>,
    ) -> Self {
        let all = metrics_enabled_dimensions.as_ref().is_some_and(|s| {
            s.iter()
                .any(|d| d == crate::metrics::METRICS_DIMENSIONS_ALL)
        });
        Self {
            metrics_level,
            metrics_enabled_dimensions: metrics_enabled_dimensions.unwrap_or_default(),
            metrics_enabled_dimensions_all: all,
        }
    }

    /// The default filtering layer: `DETAILED` level, all dimensions enabled.
    ///
    /// Mirrors `new FilteringMetricsScope()`.
    pub fn default_all() -> Self {
        Self::new(
            crate::metrics::MetricsLevel::Detailed,
            Some(vec![crate::metrics::METRICS_DIMENSIONS_ALL.to_string()]),
        )
    }

    /// Whether a datum at `level` should be dropped, porting
    /// `FilteringMetricsScope.addData(...,level)`'s guard: drop if
    /// `level.value() < metricsLevel.value()`.
    pub fn should_drop_data(&self, level: crate::metrics::MetricsLevel) -> bool {
        level.value() < self.metrics_level.value()
    }

    /// Whether a dimension named `name` should be dropped, porting
    /// `FilteringMetricsScope.addDimension`'s guard.
    pub fn should_drop_dimension(&self, name: &str) -> bool {
        !self.metrics_enabled_dimensions_all
            && !self.metrics_enabled_dimensions.iter().any(|d| d == name)
    }
}
