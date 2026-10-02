//! Port of `software.amazon.kinesis.retrieval.polling.BlockingRecordsPublisher`.
//!
//! A minimal, non-prefetching publisher: each [`get_next_result`] drives one
//! `getRecordsAdapter` call and returns the [`ProcessRecordsInput`] directly.
//! Legacy/simple pull path — `restart_from` is unsupported and `subscribe` only
//! stores the sink (never delivers), faithfully matching Java's partial
//! `Publisher` contract.

use std::sync::{Arc, Mutex};

use async_trait::async_trait;

use crate::common::request_details::RequestDetails;
use crate::common::InitialPositionInStreamExtended;
use crate::exceptions::BoxError;
use crate::lifecycle::events::process_records_input::ProcessRecordsInput;
use crate::retrieval::get_records_retrieval_strategy::GetRecordsRetrievalStrategy;
use crate::retrieval::kpl::ExtendedSequenceNumber;
use crate::retrieval::polling::data_fetcher::FetchError;
use crate::retrieval::records_publisher::{
    new_subscription, RecordsPublisher, RecordsPublisherSubscription,
};
use crate::retrieval::records_retrieved::RecordsRetrieved;

/// A minimal synchronous single-call publisher.
///
/// Port of the Java `BlockingRecordsPublisher`.
pub struct BlockingRecordsPublisher {
    max_records_per_call: i32,
    strategy: Arc<dyn GetRecordsRetrievalStrategy>,
    last_successful_request_details: Mutex<RequestDetails>,
}

impl BlockingRecordsPublisher {
    /// Construct with the per-call max records and the retrieval strategy.
    pub fn new(max_records_per_call: i32, strategy: Arc<dyn GetRecordsRetrievalStrategy>) -> Self {
        Self {
            max_records_per_call,
            strategy,
            last_successful_request_details: Mutex::new(RequestDetails::empty()),
        }
    }

    /// Drive one `getRecordsAdapter` call and return the resulting
    /// [`ProcessRecordsInput`]. Port of the extra public `getNextResult()`.
    ///
    /// Returns a [`FetchError`] if the retrieval fails (Java propagates the SDK
    /// exception).
    pub async fn get_next_result(&self) -> Result<ProcessRecordsInput, FetchError> {
        let adapter = self
            .strategy
            .get_records_adapter(self.max_records_per_call)
            .await?;
        if let Some(req_id) = adapter.request_id() {
            *self.last_successful_request_details.lock().unwrap() =
                RequestDetails::new(req_id, chrono::Utc::now().to_rfc3339());
        }
        Ok(adapter.to_process_records_input())
    }
}

#[async_trait]
impl RecordsPublisher for BlockingRecordsPublisher {
    async fn start(
        &self,
        _extended_sequence_number: ExtendedSequenceNumber,
        _initial_position_in_stream_extended: InitialPositionInStreamExtended,
    ) -> Result<(), BoxError> {
        // Nothing to do here (Java no-op).
        Ok(())
    }

    async fn restart_from(&self, _records_retrieved: Arc<dyn RecordsRetrieved>) {
        panic!("BlockingRecordsPublisher does not support restartFrom");
    }

    async fn shutdown(&self) {
        self.strategy.shutdown();
    }

    fn last_successful_request_details(&self) -> RequestDetails {
        self.last_successful_request_details.lock().unwrap().clone()
    }

    fn subscribe(&self) -> RecordsPublisherSubscription {
        // Java merely stores the subscriber reference and never calls onSubscribe/
        // onNext; the returned subscription's delivery channel therefore never
        // yields (matching the partial Publisher contract). We mint and drop the
        // sink so the subscription's channel exists but is never fed.
        let (subscription, _sink) = new_subscription();
        subscription
    }
}
