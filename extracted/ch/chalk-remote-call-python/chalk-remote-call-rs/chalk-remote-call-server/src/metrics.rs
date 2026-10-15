//! Function-call metrics for synchronous gRPC calls and self-consumed queue work.
//!
//! Each completed call goes to the `chalk_metrics` pipeline (the metrics bus feeding
//! TimescaleDB `metrics1`, which the "Function Calls Dequeued" chart reads) and directly
//! to statsd as `chalk.function_call.*`.

use std::env;
use std::future::Future;
use std::sync::Arc;
use std::time::Duration;

use chalk_metrics::metrics::tags::{FunctionName, Mode as BusMode, Status as BusStatus, TagValue};
use chalk_metrics::metrics::well_known_metrics::WellKnownMetricName;
use chalk_metrics::{
    make_pubsub_publisher, BatchConfig, BusPublisher, MetricsPipeline, PublishingMetricsPipeline,
};
use chalk_statsd::datadog::{DatadogConnection, DatadogError};
use chalk_statsd::metrics::MetricsClient;
use tracing::{debug, warn};

const DEQUEUED_METRIC: &str = "chalk.function_call.dequeued";
const PROCESSING_LATENCY_METRIC: &str = "chalk.function_call.processing_latency";

// Batch tuning — chalk_function_queue's defaults (METRICS_BATCH_* ), inlined.
const BATCH_MAX_MESSAGES: usize = 1000;
const BATCH_MAX_BYTES: usize = 10 * 1024 * 1024; // 10 MB
const BATCH_MAX_LATENCY: Duration = Duration::from_millis(100);
const SHUTDOWN_TIMEOUT: Duration = Duration::from_secs(10);

/// Keep the runtime alive until buffered metrics are published, even when the server fails.
pub async fn run_with_metrics<T>(
    metrics: Option<Arc<CallMetrics>>,
    server: impl Future<Output = T>,
) -> T {
    let result = server.await;
    if let Some(pipeline) = metrics.as_ref().and_then(|m| m.pipeline.as_ref()) {
        debug!("Draining function-call metrics pipeline...");
        // Stop drains routers, aggregators and publishers in order. Bound the wait
        // so an unavailable sink cannot hold the process past its termination grace period.
        match pipeline.stop(Some(SHUTDOWN_TIMEOUT)).await {
            Ok(()) => debug!("Function-call metrics pipeline drained"),
            Err(e) => warn!(error = %e, "failed to drain function-call metrics pipeline"),
        }
    }
    result
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Mode {
    Sync,
    Async,
}

impl Mode {
    fn as_str(self) -> &'static str {
        match self {
            Mode::Sync => "sync",
            Mode::Async => "async",
        }
    }

    fn bus_mode(self) -> BusMode {
        match self {
            Mode::Sync => BusMode::Sync,
            Mode::Async => BusMode::Async,
        }
    }
}

pub struct CallMetrics {
    statsd: Option<Arc<MetricsClient>>,
    pipeline: Option<Arc<PublishingMetricsPipeline>>,
}

fn non_empty_env(name: &str) -> Option<String> {
    env::var(name).ok().filter(|v| !v.is_empty())
}

fn init_statsd_client() -> Option<Arc<MetricsClient>> {
    let result = MetricsClient::new_from_default_environment().or_else(|e| {
        let no_connection = matches!(
            e.downcast_ref::<DatadogError>(),
            Some(DatadogError::ConnectionInfoNotFound)
        );
        match non_empty_env("HOST_IP") {
            // Scaling-group pods set HOST_IP but not DD_AGENT_HOST.
            Some(host_ip) if no_connection => {
                let port = non_empty_env("STATSD_PORT").unwrap_or_else(|| "8125".to_string());
                MetricsClient::new_from_datadog_config_unbatched(DatadogConnection::UdpSocket(
                    format!("{host_ip}:{port}"),
                ))
            }
            _ => Err(e),
        }
    });
    match result {
        Ok(client) => Some(Arc::new(client)),
        Err(e) => {
            if !matches!(
                e.downcast_ref::<DatadogError>(),
                Some(DatadogError::ConnectionInfoNotFound)
            ) {
                warn!(error = %e, "failed to init statsd client; statsd function-call metrics disabled");
            }
            None
        }
    }
}

/// Build and start the metrics pipeline from the environment, mirroring the
/// fnq-server / catalog-consumer init. Returns `None` if startup fails.
///
/// The bus publisher is optional; the pipeline starts regardless, since it also owns the
/// customer statsd sink.
async fn init_pipeline(
    statsd: Option<Arc<MetricsClient>>,
) -> Option<Arc<PublishingMetricsPipeline>> {
    let publishers: Vec<Arc<dyn BusPublisher>> = build_bus_publisher().await.into_iter().collect();
    let environment_id = env::var("CHALK_ENVIRONMENT_ID").unwrap_or_default();
    let pipeline = Arc::new(PublishingMetricsPipeline::new_with_env_var_defaults(
        environment_id,
        String::new(),
        publishers,
        statsd,
    ));
    if let Err(e) = pipeline.start().await {
        warn!(error = %e, "failed to start metrics pipeline; metrics disabled");
        return None;
    }
    debug!("function-call metrics pipeline started");
    Some(pipeline)
}

/// Build the metrics bus publisher for the configured backend, mirroring
/// `chalk_function_queue::config::Config::get_bus_publisher`. Empty
/// `METRICS_BUS_TOPIC` ⇒ no publisher (statsd-only). Only PubSub is wired here
/// (the dataplane uses `BUS_BACKEND=PUBSUB`); other backends fall back to no bus.
async fn build_bus_publisher() -> Option<Arc<dyn BusPublisher>> {
    let topic = non_empty_env("METRICS_BUS_TOPIC")?;
    let backend = env::var("BUS_BACKEND").unwrap_or_else(|_| "PUBSUB".to_string());
    let batch = BatchConfig {
        max_messages: BATCH_MAX_MESSAGES,
        max_bytes: BATCH_MAX_BYTES,
        max_latency: BATCH_MAX_LATENCY,
    };

    match backend.to_ascii_uppercase().as_str() {
        "PUBSUB" => {
            let project_id =
                non_empty_env("GCP_PROJECT_ID").or_else(|| non_empty_env("GOOGLE_CLOUD_PROJECT"));
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

pub async fn init() -> Option<Arc<CallMetrics>> {
    let statsd = init_statsd_client();
    let pipeline = init_pipeline(statsd.clone()).await;
    if statsd.is_none() && pipeline.is_none() {
        return None;
    }
    Some(Arc::new(CallMetrics { statsd, pipeline }))
}

fn metric_function_name(function_name: &str) -> String {
    non_empty_env("CHALK_FNQ_FUNCTION_NAME").unwrap_or_else(|| function_name.to_string())
}

fn call_tags(function_name: &str, success: bool, mode: Mode) -> [String; 3] {
    [
        format!("function_name:{function_name}"),
        format!("status:{}", if success { "success" } else { "failure" }),
        format!("mode:{}", mode.as_str()),
    ]
}

/// Emit completed-call metrics tagged with function name and success/failure.
///
/// `FunctionCallProcessingLatency` is defined as a sketch in metrics.cue, which
/// is emitted through the histogram API in chalk_metrics. The shim does not
/// carry the scaling-group revision tag used by the legacy catalog consumer;
/// the dashboard filters by function name.
pub fn record_completed_call(
    metrics: &CallMetrics,
    function_name: &str,
    success: bool,
    elapsed: Duration,
    mode: Mode,
) {
    let function_name = metric_function_name(function_name);
    let elapsed_ms = elapsed.as_secs_f64() * 1000.0;

    if let Some(statsd) = &metrics.statsd {
        let tags = call_tags(&function_name, success, mode);
        statsd.publish_count_eager(DEQUEUED_METRIC, 1, &tags);
        statsd.publish_distribution_eager(PROCESSING_LATENCY_METRIC, elapsed_ms, &tags);
    }

    if let Some(pipeline) = &metrics.pipeline {
        let status = if success {
            BusStatus::Success
        } else {
            BusStatus::Failure
        };
        let tags = vec![
            TagValue::FunctionName(FunctionName(function_name.clone())),
            TagValue::Status(status),
            TagValue::Mode(mode.bus_mode()),
        ];
        if let Err(e) = pipeline.count(WellKnownMetricName::FunctionCallDequeued, 1.0, tags.clone())
        {
            warn!(error = %e, function = %function_name, "failed to emit FunctionCallDequeued metric");
        }
        if let Err(e) = pipeline.histogram(
            WellKnownMetricName::FunctionCallProcessingLatency,
            elapsed_ms,
            tags,
        ) {
            warn!(error = %e, function = %function_name, "failed to emit FunctionCallProcessingLatency metric");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use async_trait::async_trait;
    use chalk_metrics::{PublishError, Publisher};
    use std::collections::HashMap;
    use std::net::UdpSocket;
    use std::sync::Mutex;

    struct RecordingPublisher {
        messages: Mutex<Vec<Vec<u8>>>,
        stalled: bool,
    }

    #[async_trait]
    impl Publisher for RecordingPublisher {
        async fn publish(
            &self,
            msg: Vec<u8>,
            _metadata: HashMap<String, String>,
        ) -> Result<String, PublishError> {
            if self.stalled {
                std::future::pending::<()>().await;
            }
            self.messages.lock().unwrap().push(msg);
            Ok("test-message".to_string())
        }
    }

    #[async_trait]
    impl BusPublisher for RecordingPublisher {
        fn name(&self) -> &str {
            "recording"
        }

        fn uri(&self) -> &str {
            "test://recording"
        }

        fn max_payload_size(&self) -> usize {
            1024 * 1024
        }

        async fn publish_with_key(
            &self,
            msg: Vec<u8>,
            metadata: HashMap<String, String>,
            _partition_key: Option<String>,
        ) -> Result<String, PublishError> {
            self.publish(msg, metadata).await
        }
    }

    #[test]
    fn emits_count_and_latency_over_udp() {
        let sink = UdpSocket::bind("127.0.0.1:0").unwrap();
        sink.set_read_timeout(Some(Duration::from_secs(5))).unwrap();
        let metrics = CallMetrics {
            statsd: Some(Arc::new(
                MetricsClient::new_from_datadog_config_unbatched(DatadogConnection::UdpSocket(
                    sink.local_addr().unwrap().to_string(),
                ))
                .unwrap(),
            )),
            pipeline: None,
        };

        record_completed_call(
            &metrics,
            "fn_a",
            true,
            Duration::from_millis(250),
            Mode::Sync,
        );

        let mut seen = String::new();
        let mut buf = [0u8; 2048];
        while !(seen.contains(DEQUEUED_METRIC) && seen.contains(PROCESSING_LATENCY_METRIC)) {
            let n = sink.recv(&mut buf).expect("statsd packet");
            seen.push_str(&String::from_utf8_lossy(&buf[..n]));
        }
        assert!(seen.contains("chalk.function_call.dequeued:1|c"), "{seen}");
        assert!(
            seen.contains("chalk.function_call.processing_latency:250|d"),
            "{seen}"
        );
        assert!(seen.contains("function_name:fn_a"), "{seen}");
        assert!(seen.contains("status:success"), "{seen}");
        assert!(seen.contains("mode:sync"), "{seen}");
    }

    fn call_metrics(pipeline: &Arc<PublishingMetricsPipeline>) -> Arc<CallMetrics> {
        Arc::new(CallMetrics {
            statsd: None,
            pipeline: Some(pipeline.clone()),
        })
    }

    async fn make_pipeline(
        stalled: bool,
    ) -> (Arc<PublishingMetricsPipeline>, Arc<RecordingPublisher>) {
        let publisher = Arc::new(RecordingPublisher {
            messages: Mutex::new(Vec::new()),
            stalled,
        });
        let pipeline = Arc::new(PublishingMetricsPipeline::new(
            "test-env".to_string(),
            String::new(),
            None,
            vec![publisher.clone()],
            None,
            None,
            &[],
            &[],
            100,
            2,
            1,
            Duration::from_secs(30),
            1000,
            0.1,
        ));
        pipeline.start().await.unwrap();
        (pipeline, publisher)
    }

    async fn assert_drained(server_result: Result<(), &str>) {
        let (pipeline, publisher) = make_pipeline(false).await;
        let metrics = call_metrics(&pipeline);
        let started = tokio::time::Instant::now();
        let result = run_with_metrics(Some(metrics.clone()), async {
            for mode in [Mode::Sync, Mode::Async] {
                record_completed_call(
                    &metrics,
                    "test-function",
                    true,
                    Duration::from_millis(5),
                    mode,
                );
            }
            assert!(publisher.messages.lock().unwrap().is_empty());
            server_result
        })
        .await;

        assert_eq!(result, server_result);
        assert!(!pipeline.is_running());
        assert!(!publisher.messages.lock().unwrap().is_empty());
        assert!(started.elapsed() < SHUTDOWN_TIMEOUT);
    }

    #[tokio::test]
    async fn shutdown_publishes_buffered_calls_before_periodic_flush() {
        assert_drained(Ok(())).await;
    }

    #[tokio::test]
    async fn server_error_also_drains_metrics_and_preserves_error() {
        assert_drained(Err("server failed")).await;
    }

    #[tokio::test(start_paused = true)]
    async fn stalled_publisher_bounds_shutdown_and_preserves_server_result() {
        let (pipeline, _) = make_pipeline(true).await;
        let metrics = call_metrics(&pipeline);
        let started = tokio::time::Instant::now();
        let result = run_with_metrics(Some(metrics.clone()), async {
            record_completed_call(
                &metrics,
                "test-function",
                true,
                Duration::from_millis(5),
                Mode::Sync,
            );
            Err::<(), _>("server failed")
        })
        .await;

        assert_eq!(result, Err("server failed"));
        assert_eq!(started.elapsed(), SHUTDOWN_TIMEOUT);
    }
}
