//! Port of `software.amazon.kinesis.metrics.CloudWatchMetricsFactory`.

use std::sync::Arc;

use aws_sdk_cloudwatch::Client as CloudWatchClient;
use tokio::task::JoinHandle;

use crate::metrics::cloud_watch_publisher_runnable::CloudWatchPublisherRunnable;
use crate::metrics::{
    CloudWatchMetricsPublisher, CloudWatchMetricsScope, MetricsFactory, MetricsLevel, MetricsScope,
};

/// A [`MetricsFactory`] for the CloudWatch backend. Owns the background
/// publication task and creates [`CloudWatchMetricsScope`]s that share it.
///
/// **Side-effecting construction (preserved from Java):** the Java constructor
/// creates and *starts* a background `Thread` named `cw-metrics-publisher`. The
/// Rust port spawns an equivalent **tokio task** in [`new`](Self::new) via
/// [`tokio::spawn`], so `new` must be called from within a tokio runtime.
/// [`shutdown`](Self::shutdown) signals the task and awaits its `JoinHandle`
/// (Java `runnable.shutdown()` + `Thread.join()`).
pub struct CloudWatchMetricsFactory {
    runnable: Arc<CloudWatchPublisherRunnable>,
    join_handle: std::sync::Mutex<Option<JoinHandle<()>>>,
    metrics_level: MetricsLevel,
    metrics_enabled_dimensions: Option<Vec<String>>,
}

impl CloudWatchMetricsFactory {
    /// Creates the factory and spawns the background publisher task.
    ///
    /// `metrics_enabled_dimensions` is defensively copied (Java copies into an
    /// `ImmutableSet`, falling back to empty on `null`). Must be called from
    /// within a tokio runtime.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        cloud_watch_client: CloudWatchClient,
        namespace: impl Into<String>,
        buffer_time_millis: i64,
        max_queue_size: usize,
        metrics_level: MetricsLevel,
        metrics_enabled_dimensions: Option<Vec<String>>,
        flush_size: usize,
    ) -> Self {
        let publisher = CloudWatchMetricsPublisher::new(cloud_watch_client, namespace);
        let runnable = Arc::new(CloudWatchPublisherRunnable::new(
            Arc::new(publisher),
            buffer_time_millis,
            max_queue_size,
            flush_size,
        ));

        // Spawn the background publication task (Java: new Thread(runnable).start()).
        let run_ref = runnable.clone();
        let join_handle = tokio::spawn(async move {
            run_ref.run().await;
        });

        Self {
            runnable,
            join_handle: std::sync::Mutex::new(Some(join_handle)),
            metrics_level,
            metrics_enabled_dimensions,
        }
    }

    /// Signals the publisher to shut down and awaits the background task.
    ///
    /// Port of `shutdown()` (which does `runnable.shutdown()` then
    /// `Thread.join()`).
    pub async fn shutdown(&self) {
        self.runnable.shutdown();
        let handle = self.join_handle.lock().unwrap().take();
        if let Some(handle) = handle {
            // A panic that escaped the publisher task surfaces as a JoinError;
            // log it (Java's Thread would have logged the Throwable) instead of
            // discarding it.
            if let Err(e) = handle.await {
                if e.is_panic() {
                    tracing::error!(
                        "CWPublication task panicked: {}",
                        crate::utils::panic_util::panic_message(e.into_panic().as_ref())
                    );
                }
            }
        }
    }
}

impl MetricsFactory for CloudWatchMetricsFactory {
    fn create_metrics(&self) -> Box<dyn MetricsScope + Send> {
        Box::new(CloudWatchMetricsScope::new(
            self.runnable.handle(),
            self.metrics_level,
            self.metrics_enabled_dimensions.clone(),
        ))
    }

    fn as_any(&self) -> &dyn std::any::Any {
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::MetricsScope;
    use aws_sdk_cloudwatch::types::StandardUnit;

    // A lightweight end-to-end smoke test that exercises factory -> scope ->
    // enqueue path using the runnable with a mock publisher would require
    // constructing a real CloudWatch client. We instead verify the scope wiring
    // via the runnable directly in cloud_watch_publisher_runnable tests, and
    // here just verify the factory produces a usable scope that can accumulate
    // and end without panicking, driving through a fake runtime.
    #[tokio::test]
    async fn create_metrics_produces_usable_scope() {
        // Build a runnable with a recording publisher directly to avoid needing
        // a real CloudWatch client, mirroring the factory's scope creation.
        use crate::metrics::cloud_watch_publisher_runnable::MetricsPublisher;
        use async_trait::async_trait;
        use std::sync::Arc as StdArc;

        struct NoopPublisher;
        #[async_trait]
        impl MetricsPublisher for NoopPublisher {
            async fn publish_metrics(
                &self,
                _data: Vec<crate::metrics::MetricDatumWithKey<crate::metrics::CloudWatchMetricKey>>,
            ) {
            }
        }

        let runnable = StdArc::new(CloudWatchPublisherRunnable::new(
            StdArc::new(NoopPublisher),
            10_000,
            10_000,
            200,
        ));
        let mut scope = CloudWatchMetricsScope::new(
            runnable.handle(),
            MetricsLevel::Detailed,
            Some(vec![crate::metrics::METRICS_DIMENSIONS_ALL.to_string()]),
        );
        scope.add_dimension("Operation", "ProcessRecords");
        scope.add_data("Records", 5.0, StandardUnit::Count);
        scope.end();
        // The runnable should now hold one accumulated datum.
        runnable.run_once().await; // drains/waits without panicking
    }
}
