//! Port of `software.amazon.kinesis.metrics.InterceptingMetricsFactory`.

use std::sync::Arc;

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::metrics::{MetricsFactory, MetricsLevel, MetricsScope};

/// The interception hooks, porting the `protected intercept*` methods of the
/// abstract Java `InterceptingMetricsFactory`.
///
/// Java uses subclassing to override the hooks; the Rust port uses a trait with
/// default methods (each defaulting to forwarding to the wrapped scope, matching
/// Java's default implementations). Implement this trait to observe/modify calls
/// and pass it to [`InterceptingMetricsFactory::new`].
pub trait MetricsInterceptor: Send + Sync {
    /// Hook invoked after the delegate creates a scope (Java
    /// `interceptCreateMetrics`; default no-op).
    fn intercept_create_metrics(&self, _scope: &mut dyn MetricsScope) {}

    /// Hook for `addData(name, value, unit)` (default: forward).
    fn intercept_add_data(
        &self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        scope: &mut dyn MetricsScope,
    ) {
        scope.add_data(name, value, unit);
    }

    /// Hook for `addData(name, value, unit, level)` (default: forward).
    fn intercept_add_data_with_level(
        &self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        level: MetricsLevel,
        scope: &mut dyn MetricsScope,
    ) {
        scope.add_data_with_level(name, value, unit, level);
    }

    /// Hook for `addDimension(name, value)` (default: forward).
    fn intercept_add_dimension(&self, name: &str, value: &str, scope: &mut dyn MetricsScope) {
        scope.add_dimension(name, value);
    }

    /// Hook for `end()` (default: forward).
    fn intercept_end(&self, scope: &mut dyn MetricsScope) {
        scope.end();
    }
}

/// A [`MetricsFactory`] decorator that routes every scope call through a
/// [`MetricsInterceptor`]'s hooks before reaching the wrapped scope.
///
/// Port of the abstract `InterceptingMetricsFactory` + its private inner
/// `InterceptingMetricsScope`.
pub struct InterceptingMetricsFactory {
    other: Box<dyn MetricsFactory + Send + Sync>,
    interceptor: Arc<dyn MetricsInterceptor>,
}

impl InterceptingMetricsFactory {
    /// Wraps `other`, routing calls through `interceptor`.
    pub fn new(
        other: Box<dyn MetricsFactory + Send + Sync>,
        interceptor: Arc<dyn MetricsInterceptor>,
    ) -> Self {
        Self { other, interceptor }
    }
}

impl MetricsFactory for InterceptingMetricsFactory {
    fn create_metrics(&self) -> Box<dyn MetricsScope + Send> {
        let mut other_scope = self.other.create_metrics();
        self.interceptor
            .intercept_create_metrics(other_scope.as_mut());
        Box::new(InterceptingMetricsScope {
            other: other_scope,
            interceptor: self.interceptor.clone(),
        })
    }
}

/// The wrapper scope delegating each call through the interceptor hooks.
struct InterceptingMetricsScope {
    other: Box<dyn MetricsScope + Send>,
    interceptor: Arc<dyn MetricsInterceptor>,
}

impl MetricsScope for InterceptingMetricsScope {
    fn add_data(&mut self, name: &str, value: f64, unit: StandardUnit) {
        self.interceptor
            .intercept_add_data(name, value, unit, self.other.as_mut());
    }

    fn add_data_with_level(
        &mut self,
        name: &str,
        value: f64,
        unit: StandardUnit,
        level: MetricsLevel,
    ) {
        self.interceptor.intercept_add_data_with_level(
            name,
            value,
            unit,
            level,
            self.other.as_mut(),
        );
    }

    fn add_dimension(&mut self, name: &str, value: &str) {
        self.interceptor
            .intercept_add_dimension(name, value, self.other.as_mut());
    }

    fn end(&mut self) {
        self.interceptor.intercept_end(self.other.as_mut());
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::NullMetricsFactory;
    use std::sync::atomic::{AtomicUsize, Ordering};

    struct CountingInterceptor {
        create_count: AtomicUsize,
        data_count: AtomicUsize,
        end_count: AtomicUsize,
    }

    impl MetricsInterceptor for CountingInterceptor {
        fn intercept_create_metrics(&self, _scope: &mut dyn MetricsScope) {
            self.create_count.fetch_add(1, Ordering::SeqCst);
        }
        fn intercept_add_data(
            &self,
            name: &str,
            value: f64,
            unit: StandardUnit,
            scope: &mut dyn MetricsScope,
        ) {
            self.data_count.fetch_add(1, Ordering::SeqCst);
            scope.add_data(name, value, unit);
        }
        fn intercept_end(&self, scope: &mut dyn MetricsScope) {
            self.end_count.fetch_add(1, Ordering::SeqCst);
            scope.end();
        }
    }

    #[test]
    fn hooks_are_invoked() {
        let interceptor = Arc::new(CountingInterceptor {
            create_count: AtomicUsize::new(0),
            data_count: AtomicUsize::new(0),
            end_count: AtomicUsize::new(0),
        });
        let factory = InterceptingMetricsFactory::new(
            Box::new(NullMetricsFactory::new()),
            interceptor.clone(),
        );
        let mut scope = factory.create_metrics();
        scope.add_data("x", 1.0, StandardUnit::Count);
        scope.add_dimension("d", "v"); // default forwarding hook
        scope.end();

        assert_eq!(interceptor.create_count.load(Ordering::SeqCst), 1);
        assert_eq!(interceptor.data_count.load(Ordering::SeqCst), 1);
        assert_eq!(interceptor.end_count.load(Ordering::SeqCst), 1);
    }
}
