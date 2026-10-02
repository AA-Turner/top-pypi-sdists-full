//! Port of `software.amazon.kinesis.metrics.MetricsCollectingTaskDecorator`.
//!
//! Decorates a [`ConsumerTask`], reporting metrics about its timing and
//! success/failure.

use std::sync::Arc;

use async_trait::async_trait;

use crate::lifecycle::{ConsumerTask, TaskResult, TaskType};
use crate::metrics::{self, MetricsFactory, MetricsLevel};

/// Wraps a [`ConsumerTask`], timing its `call()` and recording success/latency
/// at `SUMMARY` level before ending the scope (a finally-equivalent, so metrics
/// are recorded on every path).
///
/// The operation dimension is the wrapped task's name (Java's
/// `other.getClass().getSimpleName()` → the explicit
/// [`ConsumerTask::task_name`]).
pub struct MetricsCollectingTaskDecorator {
    other: Box<dyn ConsumerTask>,
    factory: Arc<dyn MetricsFactory + Send + Sync>,
}

impl MetricsCollectingTaskDecorator {
    /// Wrap `other`, reporting metrics via `factory`.
    pub fn new(
        other: Box<dyn ConsumerTask>,
        factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Self {
        Self { other, factory }
    }

    /// The wrapped task (Java `getOther()`).
    pub fn other(&self) -> &dyn ConsumerTask {
        self.other.as_ref()
    }
}

#[async_trait]
impl ConsumerTask for MetricsCollectingTaskDecorator {
    async fn call(&self) -> TaskResult {
        let mut scope =
            metrics::create_metrics_with_operation(self.factory.as_ref(), self.other.task_name());
        let start_time_millis = metrics::current_time_millis();
        let result = self.other.call().await;
        metrics::add_success_and_latency(
            scope.as_mut(),
            result.exception().is_none(),
            start_time_millis,
            MetricsLevel::Summary,
        );
        metrics::end_scope(scope.as_mut());
        result
    }

    fn task_type(&self) -> TaskType {
        self.other.task_type()
    }

    fn task_name(&self) -> &'static str {
        self.other.task_name()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::NullMetricsFactory;
    use std::sync::atomic::{AtomicUsize, Ordering};

    struct RecordingTask {
        calls: Arc<AtomicUsize>,
        exception: bool,
    }

    #[async_trait]
    impl ConsumerTask for RecordingTask {
        async fn call(&self) -> TaskResult {
            self.calls.fetch_add(1, Ordering::SeqCst);
            if self.exception {
                TaskResult::new(Some(Box::<dyn std::error::Error + Send + Sync>::from(
                    "boom",
                )))
            } else {
                TaskResult::new(None)
            }
        }
        fn task_type(&self) -> TaskType {
            TaskType::Process
        }
        fn task_name(&self) -> &'static str {
            "ProcessTask"
        }
    }

    #[tokio::test]
    async fn decorator_calls_inner_and_forwards_result() {
        let calls = Arc::new(AtomicUsize::new(0));
        let task = RecordingTask {
            calls: calls.clone(),
            exception: false,
        };
        let decorator =
            MetricsCollectingTaskDecorator::new(Box::new(task), Arc::new(NullMetricsFactory));
        assert_eq!(decorator.task_type(), TaskType::Process);
        assert_eq!(decorator.task_name(), "ProcessTask");
        let result = decorator.call().await;
        assert!(result.exception().is_none());
        assert_eq!(calls.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn decorator_forwards_exception_result() {
        let calls = Arc::new(AtomicUsize::new(0));
        let task = RecordingTask {
            calls,
            exception: true,
        };
        let decorator =
            MetricsCollectingTaskDecorator::new(Box::new(task), Arc::new(NullMetricsFactory));
        let result = decorator.call().await;
        assert!(result.exception().is_some());
    }
}
