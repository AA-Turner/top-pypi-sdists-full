//! Port of `software.amazon.kinesis.coordinator.GracefulShutdownContext`.

use std::sync::Arc;

use crate::coordinator::graceful_shutdown_coordinator::SchedulerHandle;
use crate::lifecycle::CountDownLatch;

/// Immutable value object carrying the three synchronization latches plus a
/// Scheduler handle between the Scheduler-side shutdown initiation and the
/// `GracefulShutdownCoordinator`'s wait logic. Java `GracefulShutdownContext`
/// (package-private, Lombok `@Data @Builder @Accessors(fluent = true)`).
///
/// The Java `scheduler` back-reference is modeled as an
/// `Option<Arc<dyn SchedulerHandle>>` (a trait breaking the
/// `Scheduler`↔coordinator cycle). `is_record_processor_shutdown_complete()`
/// tests `scheduler == null` faithfully.
#[derive(Clone, Default)]
pub struct GracefulShutdownContext {
    shutdown_complete_latch: Option<Arc<CountDownLatch>>,
    notification_complete_latch: Option<Arc<CountDownLatch>>,
    final_shutdown_latch: Option<Arc<CountDownLatch>>,
    scheduler: Option<Arc<dyn SchedulerHandle>>,
}

impl GracefulShutdownContext {
    /// Full-context builder (Java `builder().shutdownCompleteLatch(..)...build()`).
    pub fn new(
        shutdown_complete_latch: Option<Arc<CountDownLatch>>,
        notification_complete_latch: Option<Arc<CountDownLatch>>,
        final_shutdown_latch: Option<Arc<CountDownLatch>>,
        scheduler: Option<Arc<dyn SchedulerHandle>>,
    ) -> Self {
        Self {
            shutdown_complete_latch,
            notification_complete_latch,
            final_shutdown_latch,
            scheduler,
        }
    }

    pub fn shutdown_complete_latch(&self) -> Option<&Arc<CountDownLatch>> {
        self.shutdown_complete_latch.as_ref()
    }

    pub fn notification_complete_latch(&self) -> Option<&Arc<CountDownLatch>> {
        self.notification_complete_latch.as_ref()
    }

    pub fn final_shutdown_latch(&self) -> Option<&Arc<CountDownLatch>> {
        self.final_shutdown_latch.as_ref()
    }

    /// The Scheduler back-reference (Java `scheduler()`).
    pub fn scheduler(&self) -> Option<&Arc<dyn SchedulerHandle>> {
        self.scheduler.as_ref()
    }

    /// Java `isRecordProcessorShutdownComplete()`: true iff the shutdown-complete
    /// and notification-complete latches and the scheduler are all absent (a
    /// minimal context built with only a `finalShutdownLatch` when the Scheduler
    /// had zero leases at shutdown-request time).
    pub fn is_record_processor_shutdown_complete(&self) -> bool {
        self.shutdown_complete_latch.is_none()
            && self.notification_complete_latch.is_none()
            && self.scheduler.is_none()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_context_is_record_processor_shutdown_complete() {
        let ctx = GracefulShutdownContext::default();
        assert!(ctx.is_record_processor_shutdown_complete());
    }

    #[test]
    fn context_with_latch_is_not_complete() {
        let ctx = GracefulShutdownContext::new(
            Some(Arc::new(CountDownLatch::new())),
            None,
            Some(Arc::new(CountDownLatch::new())),
            None,
        );
        assert!(!ctx.is_record_processor_shutdown_complete());
        assert!(ctx.shutdown_complete_latch().is_some());
        assert!(ctx.final_shutdown_latch().is_some());
    }

    #[test]
    fn final_only_context_is_complete() {
        let ctx =
            GracefulShutdownContext::new(None, None, Some(Arc::new(CountDownLatch::new())), None);
        assert!(ctx.is_record_processor_shutdown_complete());
    }
}
