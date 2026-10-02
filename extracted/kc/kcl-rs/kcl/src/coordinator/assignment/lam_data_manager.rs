//! Port of `software.amazon.kinesis.coordinator.assignment.LAMDataManager`.
//!
//! Abstraction over loading + validating + cleaning leases and worker-metric
//! data for one [`LeaseAssignmentManager`](super::LeaseAssignmentManager)
//! assignment cycle. Hides DynamoDB table topology + migration state from LAM.

use async_trait::async_trait;

use super::lam_data_snapshot::LamDataSnapshot;
use crate::leases::exceptions::LeasingError;
use crate::metrics::MetricsScope;

/// Manages data loading, validation, and cleanup for LAM. Java `LAMDataManager`.
#[async_trait]
pub trait LamDataManager: Send + Sync {
    /// Java `loadData(MetricsScope)`: load + validate + clean leases and worker
    /// metrics for a single LAM cycle. Java blocks synchronously; the Rust port
    /// is `async` (I/O via `EntityDAO`/`WorkerMetricStatsDAO`).
    async fn load_data(
        &self,
        metrics_scope: &mut (dyn MetricsScope + Send),
    ) -> Result<LamDataSnapshot, LeasingError>;

    /// Java `shutdown()`: release internal resources.
    async fn shutdown(&self);
}

#[cfg(test)]
pub use mock::MockLamDataManager;

// NOTE(port): `mockall::automock` cannot generate a mock for this trait because
// `async_trait` rewrites `load_data`'s `&mut (dyn MetricsScope + Send)` argument
// into a form whose elided lifetime bounds no longer match the trait method
// (rustc E0195). A `#[mockall::concretize]` workaround also fails under
// `async_trait` (E0261 undeclared lifetime). We therefore hand-write a
// mockall-compatible `MockLamDataManager` exposing the subset of the mockall
// builder API the tests use: `new()`, `expect_load_data()` with
// `.returning(..)` / `.times(n)` / `.never()`, and `expect_shutdown()`. Call
// counts are verified on drop, matching mockall semantics.
#[cfg(test)]
mod mock {
    use std::sync::Mutex;

    use super::*;

    type LoadDataFn =
        dyn FnMut(&mut (dyn MetricsScope + Send)) -> Result<LamDataSnapshot, LeasingError> + Send;

    /// A panicking `.returning(..)` closure is a supported use (the LAM
    /// panic-containment tests), so tolerate the poisoned mutex it leaves
    /// behind — the expectation state stays consistent (the call is recorded
    /// before the closure runs).
    fn lock_ignore_poison<T>(m: &Mutex<T>) -> std::sync::MutexGuard<'_, T> {
        m.lock().unwrap_or_else(std::sync::PoisonError::into_inner)
    }

    /// Mockall-style expectation for a single mocked method: an optional return
    /// closure plus a min/max call-count range verified on drop.
    struct Expectation<F: ?Sized> {
        func: Option<Box<F>>,
        calls: usize,
        min: usize,
        max: usize,
    }

    impl<F: ?Sized> Default for Expectation<F> {
        fn default() -> Self {
            Self {
                func: None,
                calls: 0,
                min: 0,
                max: usize::MAX,
            }
        }
    }

    impl<F: ?Sized> Expectation<F> {
        fn record_call(&mut self) {
            self.calls += 1;
        }

        fn verify(&self, method: &str) {
            assert!(
                self.calls >= self.min && self.calls <= self.max,
                "MockLamDataManager::{method}: expected call count in [{}, {}], got {}",
                self.min,
                self.max,
                self.calls,
            );
        }
    }

    /// Builder handle returned by `expect_load_data`, mirroring the subset of
    /// mockall's `Expectation` builder used by the tests.
    pub struct LoadDataExpectationBuilder<'a> {
        exp: &'a Mutex<Expectation<LoadDataFn>>,
    }

    impl<'a> LoadDataExpectationBuilder<'a> {
        /// Mockall `.returning(f)`.
        pub fn returning<F>(self, f: F) -> Self
        where
            F: FnMut(&mut (dyn MetricsScope + Send)) -> Result<LamDataSnapshot, LeasingError>
                + Send
                + 'static,
        {
            self.exp.lock().unwrap().func = Some(Box::new(f));
            self
        }

        /// Mockall `.times(n)`.
        pub fn times(self, n: usize) -> Self {
            let mut guard = self.exp.lock().unwrap();
            guard.min = n;
            guard.max = n;
            self
        }

        /// Mockall `.never()`.
        pub fn never(self) -> Self {
            let mut guard = self.exp.lock().unwrap();
            guard.min = 0;
            guard.max = 0;
            self
        }
    }

    /// Hand-written stand-in for `mockall::automock`'s generated
    /// `MockLamDataManager` (see module NOTE for why automock cannot be used).
    #[derive(Default)]
    pub struct MockLamDataManager {
        load_data: Mutex<Expectation<LoadDataFn>>,
        shutdown_calls: Mutex<usize>,
    }

    impl MockLamDataManager {
        pub fn new() -> Self {
            Self::default()
        }

        pub fn expect_load_data(&mut self) -> LoadDataExpectationBuilder<'_> {
            LoadDataExpectationBuilder {
                exp: &self.load_data,
            }
        }
    }

    #[async_trait]
    impl LamDataManager for MockLamDataManager {
        async fn load_data(
            &self,
            metrics_scope: &mut (dyn MetricsScope + Send),
        ) -> Result<LamDataSnapshot, LeasingError> {
            let mut guard = lock_ignore_poison(&self.load_data);
            guard.record_call();
            match guard.func.as_mut() {
                Some(f) => f(metrics_scope),
                None => panic!(
                    "MockLamDataManager::load_data called without a `.returning(..)` expectation"
                ),
            }
        }

        async fn shutdown(&self) {
            *self.shutdown_calls.lock().unwrap() += 1;
        }
    }

    impl Drop for MockLamDataManager {
        fn drop(&mut self) {
            // Skip verification while unwinding to avoid a double-panic.
            if std::thread::panicking() {
                return;
            }
            lock_ignore_poison(&self.load_data).verify("load_data");
        }
    }
}
