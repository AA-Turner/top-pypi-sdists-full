//! Test-only helpers shared across the lifecycle task tests.

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

use async_trait::async_trait;

use crate::common::{InitialPositionInStreamExtended, RequestDetails};
use crate::exceptions::BoxError;
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::{
    new_subscription, RecordsDeliveryAck, RecordsPublisher, RecordsPublisherSubscription,
    RecordsRetrieved,
};

/// A no-op [`RecordsPublisher`] for task tests: records how often `start` and
/// `shutdown` were called and otherwise does nothing.
///
/// `start` can be made to fail a fixed number of times via
/// [`fail_start_times`](Self::fail_start_times) — used to exercise the
/// `InitializeTask`/`ShardConsumer` failure-then-retry path (2026-07-14 fix: a
/// failed `RecordsPublisher::start` now fails the task instead of being
/// silently ignored).
#[derive(Default)]
pub struct RecordingRecordsPublisher {
    start_calls: AtomicUsize,
    shutdown_calls: AtomicUsize,
    fail_start_times: AtomicUsize,
}

impl RecordingRecordsPublisher {
    pub fn new() -> Self {
        Self::default()
    }

    /// Make the next `n` calls to `start` return `Err` instead of succeeding;
    /// every call after those `n` succeeds.
    pub fn fail_start_times(self, n: usize) -> Self {
        self.fail_start_times.store(n, Ordering::SeqCst);
        self
    }

    pub fn start_calls(&self) -> usize {
        self.start_calls.load(Ordering::SeqCst)
    }

    pub fn shutdown_calls(&self) -> usize {
        self.shutdown_calls.load(Ordering::SeqCst)
    }
}

#[async_trait]
impl RecordsPublisher for RecordingRecordsPublisher {
    async fn start(
        &self,
        _extended_sequence_number: ExtendedSequenceNumber,
        _initial_position_in_stream_extended: InitialPositionInStreamExtended,
    ) -> Result<(), BoxError> {
        self.start_calls.fetch_add(1, Ordering::SeqCst);
        // Decrement-while-positive so exactly the configured number of calls fail.
        let mut remaining = self.fail_start_times.load(Ordering::SeqCst);
        while remaining > 0 {
            match self.fail_start_times.compare_exchange(
                remaining,
                remaining - 1,
                Ordering::SeqCst,
                Ordering::SeqCst,
            ) {
                Ok(_) => {
                    return Err(Box::<dyn std::error::Error + Send + Sync>::from(
                        "RecordingRecordsPublisher: injected start failure",
                    ))
                }
                Err(actual) => remaining = actual,
            }
        }
        Ok(())
    }

    async fn restart_from(&self, _records_retrieved: Arc<dyn RecordsRetrieved>) {}

    async fn shutdown(&self) {
        self.shutdown_calls.fetch_add(1, Ordering::SeqCst);
    }

    fn last_successful_request_details(&self) -> RequestDetails {
        RequestDetails::empty()
    }

    async fn notify(&self, _ack: Box<dyn RecordsDeliveryAck>) {}

    fn subscribe(&self) -> RecordsPublisherSubscription {
        let (subscription, _sink) = new_subscription();
        subscription
    }
}
