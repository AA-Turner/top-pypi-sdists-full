//! Port of `software.amazon.kinesis.metrics`.
//!
//! The metrics subsystem defines the [`MetricsScope`]/[`MetricsFactory`]
//! abstractions and the CloudWatch, log, null, and (deferred) OpenTelemetry
//! backends, plus the [`MetricsUtil`](metrics_util)-style helpers used
//! throughout KCL for recording latency, success, and counts.
//!
//! # Design
//!
//! Java composes the CloudWatch scope through a deep inheritance chain
//! (`DimensionTracking` ← `Ending` ← `Accumulating` ← `AccumulateByName` ←
//! `Filtering` ← `CloudWatch`). This port replaces inheritance with
//! **composition**: small building blocks in [`scope_chain`] ([`DimensionSet`],
//! [`scope_chain::Accumulator`], [`scope_chain::FilteringLayer`]) are embedded by
//! the concrete scopes ([`FilteringMetricsScope`], [`CloudWatchMetricsScope`],
//! [`LogMetricsScope`], …). The exact combined behavior is preserved, including
//! the ended-guard quirks, the min/max/sum/sampleCount `StatisticSet` merging,
//! and the unit-mismatch check.
//!
//! [`MetricsScope`]/[`MetricsFactory`] are **synchronous, infallible** traits;
//! contract violations `panic!` with the exact Java message. The CloudWatch
//! background publisher is a spawned tokio task (see
//! [`cloud_watch_publisher_runnable`]).
//!
//! The OpenTelemetry backend ([`otel`]) is fully ported:
//! [`MetricsBackend::Otel`] builds an
//! [`OtelMetricsFactory`](otel::OtelMetricsFactory) in [`MetricsConfig`], which
//! produces [`OtelMetricsScope`](otel::OtelMetricsScope)s recording directly
//! onto OTel `Meter` instruments.
//!
//! # Deferrals
//!
//! * [`MetricsCollectingTaskDecorator`](metrics_collecting_task_decorator) wraps
//!   a `lifecycle::ConsumerTask`, timing its `call()` and recording
//!   success/latency at `SUMMARY` (ported in the lifecycle 7a wave).

pub mod accumulate_by_name_metrics_scope;
pub mod cloud_watch_metric_key;
pub mod cloud_watch_metrics_factory;
pub mod cloud_watch_metrics_publisher;
pub mod cloud_watch_metrics_scope;
pub mod cloud_watch_publisher_runnable;
pub mod filtering_metrics_scope;
pub mod intercepting_metrics_factory;
pub mod log_metrics_scope;
pub mod metric_accumulating_queue;
pub mod metric_datum_with_key;
pub mod metrics_backend;
pub mod metrics_collecting_task_decorator;
pub mod metrics_config;
pub mod metrics_level;
pub mod metrics_scope;
pub mod metrics_util;
pub mod null_metrics_scope;
pub mod otel;
pub mod scope_chain;
pub mod test_helper;
pub mod thread_safe_metrics_delegating_scope;

// --- Core traits, enums, constants ---
pub use metrics_backend::MetricsBackend;
pub use metrics_level::MetricsLevel;
pub use metrics_scope::{MetricsFactory, MetricsScope, METRICS_DIMENSIONS_ALL};

// --- Scope chain building blocks ---
pub use scope_chain::DimensionSet;

// --- Concrete scopes / factories ---
pub use accumulate_by_name_metrics_scope::{AccumulateByNameMetricsScope, EndingMetricsScope};
pub use cloud_watch_metric_key::CloudWatchMetricKey;
pub use cloud_watch_metrics_factory::CloudWatchMetricsFactory;
pub use cloud_watch_metrics_publisher::CloudWatchMetricsPublisher;
pub use cloud_watch_metrics_scope::CloudWatchMetricsScope;
pub use cloud_watch_publisher_runnable::{
    CloudWatchPublisherRunnable, MetricsPublisher, PublisherHandle,
};
pub use filtering_metrics_scope::FilteringMetricsScope;
pub use intercepting_metrics_factory::{InterceptingMetricsFactory, MetricsInterceptor};
pub use log_metrics_scope::{LogMetricsFactory, LogMetricsScope};
pub use metric_accumulating_queue::MetricAccumulatingQueue;
pub use metric_datum_with_key::MetricDatumWithKey;
pub use metrics_collecting_task_decorator::MetricsCollectingTaskDecorator;
pub use metrics_config::MetricsConfig;
pub use null_metrics_scope::{NullMetricsFactory, NullMetricsScope};
pub use otel::{OtelMetricsFactory, OtelMetricsScope};
pub use thread_safe_metrics_delegating_scope::{
    ThreadSafeMetricsDelegatingFactory, ThreadSafeMetricsDelegatingScope,
};

// --- MetricsUtil free functions + dimension-name constants ---
pub use metrics_util::{
    add_count, add_latency, add_latency_with_now, add_operation, add_shard_id, add_stream_id,
    add_success, add_success_and_latency, add_success_and_latency_with_dimension,
    add_worker_identifier, create_metrics, create_metrics_with_operation, current_time_millis,
    end_scope, OPERATION_DIMENSION_NAME, SHARD_ID_DIMENSION_NAME, STREAM_IDENTIFIER,
};
