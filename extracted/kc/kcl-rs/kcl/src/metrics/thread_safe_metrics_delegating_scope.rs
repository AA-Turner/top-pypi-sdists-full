//! Port of `software.amazon.kinesis.metrics.ThreadSafeMetricsDelegatingScope`
//! and `ThreadSafeMetricsDelegatingFactory`.

use std::sync::Mutex;

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::metrics::{MetricsFactory, MetricsLevel, MetricsScope};

/// A [`MetricsScope`] that serializes all access to a delegate scope so it can
/// be shared safely across threads.
///
/// Port of `ThreadSafeMetricsDelegatingScope`, whose Java methods are all
/// `synchronized` on the wrapper instance. The Rust analog wraps the delegate in
/// a [`std::sync::Mutex`] and locks for the duration of each call (Java monitors
/// are reentrant but this class never re-enters itself, so a non-reentrant mutex
/// suffices).
pub struct ThreadSafeMetricsDelegatingScope {
    delegate: Mutex<Box<dyn MetricsScope + Send>>,
}

impl ThreadSafeMetricsDelegatingScope {
    /// Wraps `delegate`.
    pub fn new(delegate: Box<dyn MetricsScope + Send>) -> Self {
        Self {
            delegate: Mutex::new(delegate),
        }
    }
}

impl MetricsScope for ThreadSafeMetricsDelegatingScope {
    fn add_data(&mut self, name: &str, value: f64, unit: StandardUnit) {
        self.delegate.lock().unwrap().add_data(name, value, unit);
    }

    fn add_data_with_level(
        &mut self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        level: MetricsLevel,
    ) {
        self.delegate
            .lock()
            .unwrap()
            .add_data_with_level(name, value, unit, level);
    }

    fn add_dimension(&mut self, name: &str, value: &str) {
        self.delegate.lock().unwrap().add_dimension(name, value);
    }

    fn end(&mut self) {
        self.delegate.lock().unwrap().end();
    }
}

/// A [`MetricsFactory`] that wraps each created scope in a
/// [`ThreadSafeMetricsDelegatingScope`].
///
/// Port of `ThreadSafeMetricsDelegatingFactory`.
pub struct ThreadSafeMetricsDelegatingFactory {
    delegate: Box<dyn MetricsFactory + Send + Sync>,
}

impl ThreadSafeMetricsDelegatingFactory {
    /// Wraps `delegate`.
    pub fn new(delegate: Box<dyn MetricsFactory + Send + Sync>) -> Self {
        Self { delegate }
    }
}

impl MetricsFactory for ThreadSafeMetricsDelegatingFactory {
    fn create_metrics(&self) -> Box<dyn MetricsScope + Send> {
        Box::new(ThreadSafeMetricsDelegatingScope::new(
            self.delegate.create_metrics(),
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::{LogMetricsFactory, NullMetricsFactory};

    #[test]
    fn delegates_and_serializes() {
        let factory = ThreadSafeMetricsDelegatingFactory::new(Box::new(NullMetricsFactory::new()));
        let mut scope = factory.create_metrics();
        scope.add_dimension("d", "v");
        scope.add_data("x", 1.0, StandardUnit::Count);
        scope.end();
    }

    #[test]
    fn wraps_log_factory() {
        let factory = ThreadSafeMetricsDelegatingFactory::new(Box::new(LogMetricsFactory::new()));
        let mut scope = factory.create_metrics();
        scope.add_data("x", 1.0, StandardUnit::Count);
        scope.end();
    }
}
