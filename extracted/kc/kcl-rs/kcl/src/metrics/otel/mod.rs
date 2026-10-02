//! OpenTelemetry metrics backend — port of the Java `Otel*` metrics classes.
//!
//! Selecting [`MetricsBackend::Otel`](crate::metrics::MetricsBackend::Otel) in
//! [`MetricsConfig`](crate::metrics::MetricsConfig) builds an
//! [`OtelMetricsFactory`], which produces [`OtelMetricsScope`]s that record
//! observations immediately onto OTel [`Meter`](opentelemetry::metrics::Meter)
//! instruments. Metric names are transformed by
//! [`otel_metric_name_transformer::transform_name`].
//!
//! # Java → Rust OTel API mapping
//!
//! * Java `OpenTelemetry` → Rust `Arc<dyn MeterProvider + Send + Sync>` (the
//!   [`MeterProvider`](opentelemetry::metrics::MeterProvider) trait object).
//!   `OpenTelemetry.noop()` → a `NoopMeterProvider`;
//!   `GlobalOpenTelemetry.getOrNoop()` →
//!   [`opentelemetry::global::meter_provider`].
//! * Java `Meter.gaugeBuilder(name).setUnit(u).build()` → `DoubleGauge.set(v, attrs)`
//!   maps to `meter.f64_gauge(name).with_unit(u).build()` → `Gauge<f64>.record(v, attrs)`.
//! * `counterBuilder(name).ofDoubles().setUnit(u).build()` → `DoubleCounter.add(v, attrs)`
//!   maps to `meter.f64_counter(name).with_unit(u).build()` → `Counter<f64>.add(v, attrs)`.
//! * `histogramBuilder(name).setUnit(u).build()` → `DoubleHistogram.record(v, attrs)`
//!   maps to `meter.f64_histogram(name).with_unit(u).build()` → `Histogram<f64>.record(v, attrs)`.
//! * OTel `Attributes` → `Vec<KeyValue>`; `AttributeKey.stringKey(k)` +
//!   `.put(k, v)` → `KeyValue::new(k, v)`.
//!
//! The instrument kinds, metric-name transformation, unit conversion, gauge
//! allow-list, and dimension→attribute mapping are all preserved verbatim, so
//! the emitted OTel output is behaviorally equivalent to the Java backend.

pub mod otel_metric_name_transformer;
pub mod otel_metrics_factory;
pub mod otel_metrics_scope;

pub use otel_metrics_factory::OtelMetricsFactory;
pub use otel_metrics_scope::{
    convert_unit, dimension_to_attribute_map, gauge_metric_names, OtelMetricsScope,
};
