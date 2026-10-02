//! Port of `software.amazon.kinesis.metrics.CloudWatchMetricsPublisher`.

use std::time::Duration;

use aws_sdk_cloudwatch::types::MetricDatum;
use aws_sdk_cloudwatch::Client as CloudWatchClient;

use crate::metrics::{CloudWatchMetricKey, MetricDatumWithKey};
use crate::retrieval::aws_exception_manager::{AwsExceptionManager, BoxError};

/// CloudWatch API limit of 20 `MetricDatum` per `PutMetricData` request. Must be
/// preserved exactly.
const BATCH_SIZE: usize = 20;
/// Per-batch blocking wait (Java `PUT_TIMEOUT_MILLIS`).
const PUT_TIMEOUT: Duration = Duration::from_millis(5000);

/// Publishes lists of [`MetricDatumWithKey`] to CloudWatch via `PutMetricData`,
/// batching into chunks of at most [`BATCH_SIZE`] and awaiting each batch with a
/// timeout.
///
/// **Design intent preserved from Java:** "This needs to be blocking. Making it
/// asynchronous leads to increased throttling." The Java code deliberately
/// blocks on each batch's future to serialize CloudWatch calls. The Rust port
/// preserves this by `.await`ing each batch **sequentially** (never spawning
/// concurrent futures), wrapped in [`tokio::time::timeout`] so a slow call does
/// not stall the publisher task indefinitely. Partial failure is tolerated: a
/// timeout or CloudWatch error on one batch is logged and the loop continues to
/// the next batch.
pub struct CloudWatchMetricsPublisher {
    namespace: String,
    cloud_watch_client: CloudWatchClient,
    exception_manager: AwsExceptionManager,
}

impl std::fmt::Debug for CloudWatchMetricsPublisher {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CloudWatchMetricsPublisher")
            .field("namespace", &self.namespace)
            .finish_non_exhaustive()
    }
}

impl CloudWatchMetricsPublisher {
    /// Creates a publisher for `namespace` using `cloud_watch_client`.
    pub fn new(cloud_watch_client: CloudWatchClient, namespace: impl Into<String>) -> Self {
        // Mirrors the static CW_EXCEPTION_MANAGER registered to pass a
        // CloudWatchException through unchanged (t -> t). Any SDK error is
        // already a boxed error here, so the identity registration is a no-op
        // beyond documenting the dispatch; the default function also passes
        // through. Kept for fidelity with the Java wiring.
        let mut exception_manager = AwsExceptionManager::new();
        exception_manager.add(|_e: &BoxError| true, |e| e);
        Self {
            namespace: namespace.into(),
            cloud_watch_client,
            exception_manager,
        }
    }

    /// Extracts the [`MetricDatum`]s from `data_to_publish` and publishes them in
    /// batches of at most [`BATCH_SIZE`]. Port of `publishMetrics`.
    pub async fn publish_metrics(
        &self,
        data_to_publish: &[MetricDatumWithKey<CloudWatchMetricKey>],
    ) {
        for batch in build_batches(data_to_publish) {
            let count = batch.len();
            let result = self.blocking_execute(batch).await;
            match result {
                Ok(()) => {}
                Err(PublishError::Timeout) => {
                    tracing::warn!(count, "Could not publish datums to CloudWatch (timeout)");
                }
                Err(PublishError::CloudWatch(e)) => {
                    // The exception manager pass-through mirrors the Java
                    // CloudWatchException catch branch (logged, loop continues).
                    let mapped = self.exception_manager.apply(e);
                    tracing::warn!(count, error = %mapped, "Could not publish datums to CloudWatch");
                }
            }
        }
    }

    /// Awaits a single `PutMetricData` call with a timeout. Port of
    /// `blockingExecute`.
    async fn blocking_execute(&self, metric_data: Vec<MetricDatum>) -> Result<(), PublishError> {
        let fut = self
            .cloud_watch_client
            .put_metric_data()
            .namespace(&self.namespace)
            .set_metric_data(Some(metric_data))
            .send();

        match tokio::time::timeout(PUT_TIMEOUT, fut).await {
            Err(_elapsed) => Err(PublishError::Timeout),
            Ok(Ok(_output)) => Ok(()),
            Ok(Err(sdk_err)) => Err(PublishError::CloudWatch(Box::new(sdk_err))),
        }
    }
}

/// Internal outcome of a single batch publish, mirroring the Java catch arms
/// (`CloudWatchException | TimeoutException` vs other).
enum PublishError {
    Timeout,
    CloudWatch(BoxError),
}

/// Splits the data into batches of at most [`BATCH_SIZE`] datums, in order,
/// extracting each entry's [`MetricDatum`]. This is the batching half of
/// `publishMetrics`, factored out so it can be unit-tested without a live
/// CloudWatch client.
fn build_batches(
    data_to_publish: &[MetricDatumWithKey<CloudWatchMetricKey>],
) -> Vec<Vec<MetricDatum>> {
    let mut batches = Vec::new();
    let mut start = 0;
    while start < data_to_publish.len() {
        let end = data_to_publish.len().min(start + BATCH_SIZE);
        batches.push(
            data_to_publish[start..end]
                .iter()
                .map(|d| d.datum.clone())
                .collect(),
        );
        start += BATCH_SIZE;
    }
    batches
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::test_helper::construct_datum;
    use aws_sdk_cloudwatch::types::StandardUnit;
    use std::collections::HashMap;

    // Ported from CloudWatchMetricsPublisherTest. The Java test mocks the async
    // client and verifies that 25 datums are published as ceil(25/20) = 2
    // PutMetricData requests (20 + 5), each request carrying the expected
    // datums keyed by metric name. Here we verify the batching directly (the
    // client `.send()` path is exercised in the runnable's integration).

    fn construct_metric_datum_with_key_list(
        count: usize,
    ) -> Vec<MetricDatumWithKey<CloudWatchMetricKey>> {
        let mut data = Vec::new();
        for i in 1..=count {
            let datum = construct_datum(
                &format!("datum{}", i),
                StandardUnit::Count,
                i as f64,
                i as f64,
                i as f64,
                1.0,
            );
            data.push(MetricDatumWithKey::new(
                CloudWatchMetricKey::new(&datum),
                datum,
            ));
        }
        data
    }

    // Mirrors constructMetricDatumListMap: expected data grouped into batches of
    // 20, keyed by metric name.
    fn construct_metric_datum_list_map(
        data: &[MetricDatumWithKey<CloudWatchMetricKey>],
    ) -> Vec<HashMap<String, MetricDatum>> {
        let batch_size = 20;
        let expected_request_count = data.len().div_ceil(20);
        let mut data_list: Vec<HashMap<String, MetricDatum>> = (0..expected_request_count)
            .map(|_| HashMap::new())
            .collect();

        let mut batch_index = 1;
        let mut list_index = 0;
        for datum_with_key in data {
            if batch_index > batch_size {
                batch_index = 1;
                list_index += 1;
            }
            batch_index += 1;
            data_list[list_index].insert(
                datum_with_key.datum.metric_name().unwrap().to_string(),
                datum_with_key.datum.clone(),
            );
        }
        data_list
    }

    fn assert_metric_data(expected: &HashMap<String, MetricDatum>, actual: &[MetricDatum]) {
        let mut expected = expected.clone();
        for actual_datum in actual {
            let name = actual_datum.metric_name().unwrap();
            let exp = expected.get(name);
            assert!(exp.is_some(), "unexpected datum {}", name);
            assert_eq!(exp.unwrap(), actual_datum);
            expected.remove(name);
        }
        assert!(expected.is_empty());
    }

    #[test]
    fn test_metrics_publisher_batching() {
        let data_to_publish = construct_metric_datum_with_key_list(25);
        let expected_data = construct_metric_datum_list_map(&data_to_publish);

        let batches = build_batches(&data_to_publish);
        assert_eq!(expected_data.len(), batches.len());
        assert_eq!(batches.len(), 2);
        assert_eq!(batches[0].len(), 20);
        assert_eq!(batches[1].len(), 5);

        for (expected, actual) in expected_data.iter().zip(batches.iter()) {
            assert_metric_data(expected, actual);
        }
    }
}
