//! Function-call metrics for synchronous gRPC calls and self-consumed queue work.
//! A shared `chalk_metrics` publishing pipeline emits call counts and
//! processing latency, independently of whether Redis queue consumption is enabled.
//!
//! The External Function "Function Calls Dequeued" chart reads TimescaleDB
//! `metrics1`, which is fed only by the chalk_metrics PubSub bus (statsd goes to
//! Datadog, not `metrics1`). So the bus publisher is what makes the chart move;
//! statsd is attached too, matching the cc, for Datadog parity.

use std::sync::Arc;
use std::time::Duration;

use chalk_metrics::metrics::tags::{FunctionName, Mode, Status as MetricStatus, TagValue};
use chalk_metrics::metrics::well_known_metrics::WellKnownMetricName;
use chalk_metrics::{
    make_pubsub_publisher, BatchConfig, BusPublisher, MetricsPipeline, PublishingMetricsPipeline,
};
use chalk_statsd::datadog::DatadogError;
use chalk_statsd::metrics::MetricsClient;
use tracing::{debug, warn};

// Batch tuning — chalk_function_queue's defaults (METRICS_BATCH_* ), inlined.
const BATCH_MAX_MESSAGES: usize = 1000;
const BATCH_MAX_BYTES: usize = 10 * 1024 * 1024; // 10 MB
const BATCH_MAX_LATENCY: Duration = Duration::from_millis(100);

/// Build and start the metrics pipeline from the environment, mirroring the
/// fnq-server / catalog-consumer init. Returns `None` if startup fails.
///
/// The bus publisher is what reaches the metrics store (and thus the dashboard);
/// StatsD and the bus are optional sinks. Missing configuration is quiet;
/// failures initializing a configured sink remain warnings.
pub async fn init_pipeline() -> Option<Arc<PublishingMetricsPipeline>> {
    let environment_id = std::env::var("CHALK_ENVIRONMENT_ID").unwrap_or_default();

    let statsd = Arc::new(
        MetricsClient::new_from_default_environment().unwrap_or_else(|e| {
            if !matches!(
                e.downcast_ref::<DatadogError>(),
                Some(DatadogError::ConnectionInfoNotFound)
            ) {
                warn!(error = %e, "failed to init statsd client; statsd metrics disabled");
            }
            MetricsClient::new_null()
        }),
    );

    let publishers: Vec<Arc<dyn BusPublisher>> = build_bus_publisher().await.into_iter().collect();

    let metrics_pipeline: Arc<PublishingMetricsPipeline> =
        Arc::new(PublishingMetricsPipeline::new_with_env_var_defaults(
            environment_id,
            String::new(),
            publishers,
            Some(statsd),
        ));
    if let Err(e) = metrics_pipeline.start().await {
        warn!(error = %e, "failed to start metrics pipeline; metrics disabled");
        return None;
    }
    debug!("function-call metrics pipeline started");
    Some(metrics_pipeline)
}

/// Build the metrics bus publisher for the configured backend, mirroring
/// `chalk_function_queue::config::Config::get_bus_publisher`. Empty
/// `METRICS_BUS_TOPIC` ⇒ no publisher (statsd-only). Only PubSub is wired here
/// (the dataplane uses `BUS_BACKEND=PUBSUB`); other backends fall back to no bus.
async fn build_bus_publisher() -> Option<Arc<dyn BusPublisher>> {
    let topic = std::env::var("METRICS_BUS_TOPIC").unwrap_or_default();
    if topic.is_empty() {
        return None;
    }
    let backend = std::env::var("BUS_BACKEND").unwrap_or_else(|_| "PUBSUB".to_string());
    let batch = BatchConfig {
        max_messages: BATCH_MAX_MESSAGES,
        max_bytes: BATCH_MAX_BYTES,
        max_latency: BATCH_MAX_LATENCY,
    };

    match backend.to_ascii_uppercase().as_str() {
        "PUBSUB" => {
            let project_id = std::env::var("GCP_PROJECT_ID")
                .ok()
                .or_else(|| std::env::var("GOOGLE_CLOUD_PROJECT").ok());
            let Some(project_id) = project_id else {
                warn!(
                    "BUS_BACKEND=PUBSUB but GCP_PROJECT_ID / GOOGLE_CLOUD_PROJECT is unset; metrics bus disabled"
                );
                return None;
            };
            match make_pubsub_publisher(project_id, topic, Some(batch)).await {
                Ok(publisher) => Some(publisher),
                Err(e) => {
                    warn!(error = %e, "failed to build pubsub metrics publisher; metrics bus disabled");
                    None
                }
            }
        }
        other => {
            warn!(
                backend = %other,
                "unsupported BUS_BACKEND for shim metrics; metrics bus disabled (set BUS_BACKEND=PUBSUB)"
            );
            None
        }
    }
}

/// Emit completed-call metrics tagged with function name and success/failure.
///
/// `FunctionCallProcessingLatency` is defined as a sketch in metrics.cue, which
/// is emitted through the histogram API in chalk_metrics. The shim does not
/// carry the scaling-group revision tag used by the legacy catalog consumer;
/// the dashboard filters by function name.
pub fn record_completed_call(
    pipeline: &Arc<PublishingMetricsPipeline>,
    function_name: &str,
    success: bool,
    elapsed: Duration,
    mode: Mode,
) {
    let queue_name = std::env::var("CHALK_FNQ_FUNCTION_NAME")
        .ok()
        .filter(|name| !name.is_empty());
    let function_name = queue_name.as_deref().unwrap_or(function_name);
    let status = if success {
        MetricStatus::Success
    } else {
        MetricStatus::Failure
    };
    let tags = vec![
        TagValue::FunctionName(FunctionName(function_name.to_string())),
        TagValue::Status(status.clone()),
        TagValue::Mode(mode.clone()),
    ];

    if let Err(e) = pipeline.count(WellKnownMetricName::FunctionCallDequeued, 1.0, tags.clone()) {
        warn!(error = %e, function = %function_name, "failed to emit FunctionCallDequeued metric");
    }

    if let Err(e) = pipeline.histogram(
        WellKnownMetricName::FunctionCallProcessingLatency,
        elapsed.as_secs_f64() * 1000.0,
        tags,
    ) {
        warn!(error = %e, function = %function_name, "failed to emit FunctionCallProcessingLatency metric");
    }
}
