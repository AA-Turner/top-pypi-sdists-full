//! Port of `software.amazon.kinesis.metrics.MetricsUtil`.

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::common::StreamIdentifier;
use crate::metrics::{MetricsFactory, MetricsLevel, MetricsScope};

/// Dimension name for the operation being timed.
pub const OPERATION_DIMENSION_NAME: &str = "Operation";
/// Dimension name for a shard id.
pub const SHARD_ID_DIMENSION_NAME: &str = "ShardId";
/// Dimension name for a stream identifier.
pub const STREAM_IDENTIFIER: &str = "StreamId";
const WORKER_IDENTIFIER_DIMENSION: &str = "WorkerIdentifier";
const TIME_METRIC: &str = "Time";
const SUCCESS_METRIC: &str = "Success";

/// Current wall-clock milliseconds since the Unix epoch (Java
/// `System.currentTimeMillis()`).
pub fn current_time_millis() -> i64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

/// Creates a metrics scope with no operation dimension. Port of `createMetrics`.
pub fn create_metrics(
    metrics_factory: &(dyn MetricsFactory + Send + Sync),
) -> Box<dyn MetricsScope + Send> {
    create_metric_scope(metrics_factory, None)
}

/// Creates a metrics scope with an `Operation` dimension. Port of
/// `createMetricsWithOperation`.
pub fn create_metrics_with_operation(
    metrics_factory: &(dyn MetricsFactory + Send + Sync),
    operation: &str,
) -> Box<dyn MetricsScope + Send> {
    create_metric_scope(metrics_factory, Some(operation))
}

fn create_metric_scope(
    metrics_factory: &(dyn MetricsFactory + Send + Sync),
    operation: Option<&str>,
) -> Box<dyn MetricsScope + Send> {
    let mut scope = metrics_factory.create_metrics();
    if let Some(op) = operation {
        // StringUtils.isNotEmpty(operation)
        if !op.is_empty() {
            scope.add_dimension(OPERATION_DIMENSION_NAME, op);
        }
    }
    scope
}

/// Adds a `ShardId` dimension. Port of `addShardId`.
pub fn add_shard_id(scope: &mut dyn MetricsScope, shard_id: &str) {
    add_operation(scope, SHARD_ID_DIMENSION_NAME, shard_id);
}

/// Adds a `StreamId` dimension, but only if the identifier carries an account id
/// (Java `addStreamId` guards on `accountIdOptional().isPresent()`).
pub fn add_stream_id(scope: &mut dyn MetricsScope, stream_id: &StreamIdentifier) {
    if stream_id.account_id_optional().is_some() {
        add_operation(scope, STREAM_IDENTIFIER, &stream_id.serialize());
    }
}

/// Adds a `WorkerIdentifier` dimension. Port of `addWorkerIdentifier`.
pub fn add_worker_identifier(scope: &mut dyn MetricsScope, worker_identifier: &str) {
    add_operation(scope, WORKER_IDENTIFIER_DIMENSION, worker_identifier);
}

/// Adds a dimension. Port of `addOperation`.
pub fn add_operation(scope: &mut dyn MetricsScope, dimension: &str, value: &str) {
    scope.add_dimension(dimension, value);
}

/// Records success and latency (no dimension prefix). Port of the 4-arg
/// `addSuccessAndLatency`.
pub fn add_success_and_latency(
    scope: &mut dyn MetricsScope,
    success: bool,
    start_time: i64,
    metrics_level: MetricsLevel,
) {
    add_success_and_latency_with_dimension(scope, None, success, start_time, metrics_level);
}

/// Records success and latency with an optional dimension name prefix. Port of
/// the 5-arg `addSuccessAndLatency`.
pub fn add_success_and_latency_with_dimension(
    scope: &mut dyn MetricsScope,
    dimension: Option<&str>,
    success: bool,
    start_time: i64,
    metrics_level: MetricsLevel,
) {
    add_success(scope, dimension, success, metrics_level);
    add_latency(scope, dimension, start_time, metrics_level);
}

/// Records latency as `now - start_time` milliseconds. Port of `addLatency`.
///
/// When `dimension` is non-empty the metric name is `"<dimension>.Time"`, else
/// `"Time"`. Uses the wall clock; see
/// [`add_latency_with_now`] for a deterministic variant.
pub fn add_latency(
    scope: &mut dyn MetricsScope,
    dimension: Option<&str>,
    start_time: i64,
    metrics_level: MetricsLevel,
) {
    add_latency_with_now(
        scope,
        dimension,
        start_time,
        metrics_level,
        current_time_millis(),
    );
}

/// Deterministic variant of [`add_latency`] taking an explicit `now` (Java's
/// `getTime()` is not injectable here, so this is the test seam).
pub fn add_latency_with_now(
    scope: &mut dyn MetricsScope,
    dimension: Option<&str>,
    start_time: i64,
    metrics_level: MetricsLevel,
    now: i64,
) {
    let metric_name = match dimension {
        Some(d) if !d.is_empty() => format!("{}.{}", d, TIME_METRIC),
        _ => TIME_METRIC.to_string(),
    };
    scope.add_data_with_level(
        &metric_name,
        (now - start_time) as f64,
        StandardUnit::Milliseconds,
        metrics_level,
    );
}

/// Records success as `1.0`/`0.0` (`COUNT`). Port of `addSuccess`.
pub fn add_success(
    scope: &mut dyn MetricsScope,
    dimension: Option<&str>,
    success: bool,
    metrics_level: MetricsLevel,
) {
    let metric_name = match dimension {
        Some(d) if !d.is_empty() => format!("{}.{}", d, SUCCESS_METRIC),
        _ => SUCCESS_METRIC.to_string(),
    };
    scope.add_data_with_level(
        &metric_name,
        if success { 1.0 } else { 0.0 },
        StandardUnit::Count,
        metrics_level,
    );
}

/// Records a count metric named `dimension`. Port of `addCount`.
pub fn add_count(
    scope: &mut dyn MetricsScope,
    dimension: &str,
    count: i64,
    metrics_level: MetricsLevel,
) {
    scope.add_data_with_level(dimension, count as f64, StandardUnit::Count, metrics_level);
}

/// Ends the scope. Port of `endScope`.
pub fn end_scope(scope: &mut dyn MetricsScope) {
    scope.end();
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::accumulate_by_name_metrics_scope::AccumulateByNameMetricsScope;

    #[test]
    fn latency_uses_dimension_prefix() {
        let mut scope = AccumulateByNameMetricsScope::new();
        add_latency_with_now(&mut scope, Some("Foo"), 100, MetricsLevel::Summary, 150);
        // metric name should be "Foo.Time" with value 50.
        let data = scope.accumulator.data();
        let datum = data.get("Foo.Time").expect("Foo.Time present");
        assert_eq!(datum.unit(), Some(&StandardUnit::Milliseconds));
        assert_eq!(datum.statistic_values().unwrap().sum(), Some(50.0));
    }

    #[test]
    fn latency_without_dimension_is_time() {
        let mut scope = AccumulateByNameMetricsScope::new();
        add_latency_with_now(&mut scope, None, 100, MetricsLevel::Summary, 130);
        assert!(scope.accumulator.data().contains_key("Time"));
    }

    #[test]
    fn success_emits_count() {
        let mut scope = AccumulateByNameMetricsScope::new();
        add_success(&mut scope, Some("Op"), true, MetricsLevel::Summary);
        add_success(&mut scope, None, false, MetricsLevel::Summary);
        let data = scope.accumulator.data();
        assert_eq!(
            data.get("Op.Success")
                .unwrap()
                .statistic_values()
                .unwrap()
                .sum(),
            Some(1.0)
        );
        assert_eq!(
            data.get("Success")
                .unwrap()
                .statistic_values()
                .unwrap()
                .sum(),
            Some(0.0)
        );
    }

    #[test]
    fn create_metrics_with_operation_adds_dimension() {
        use crate::metrics::LogMetricsFactory;
        let factory = LogMetricsFactory::new();
        let scope = create_metrics_with_operation(&factory, "MyOp");
        // Log scope accumulates dimensions internally; just ensure no panic and
        // the scope is usable.
        drop(scope);
    }
}
