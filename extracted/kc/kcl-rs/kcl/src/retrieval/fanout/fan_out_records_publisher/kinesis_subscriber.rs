//! Production [`ShardSubscriber`] driving the AWS SDK `SubscribeToShard` event
//! stream.
//!
//! Each `subscribe` spawns a driver task that calls `kinesis.subscribe_to_shard`,
//! then reads the `EventReceiver`, forwarding `SubscribeToShardEvent`s + terminal
//! signals as [`FlowEvent`]s to the publisher task. Per-flow demand
//! ([`request_next`]) and cancel are relayed over per-flow channels.
//!
//! The SDK event stream is inherently push-based (the `EventReceiver` yields the
//! next event when polled). Java's manual reactive `request(1)` credit maps to a
//! per-flow "pull one more" signal: the driver reads exactly one event per
//! `request_next`, forwards it, then waits for the next `request_next` — preserving
//! the 1-at-a-time flow control.
//!
//! [`request_next`]: super::ShardSubscriber::request_next

use std::collections::HashMap;
use std::sync::Mutex;

use async_trait::async_trait;
use tokio::sync::mpsc;

use crate::common::{InitialPositionInStreamExtended, StreamIdentifier};
use crate::retrieval::iterator_builder;
use crate::retrieval::kpl::ExtendedSequenceNumber;

use super::{FlowError, FlowEvent, ShardSubscriber};

/// Per-flow control channel: carries "pull one more event" and "cancel" signals
/// to the driver task.
enum FlowControl {
    RequestNext,
    Cancel,
}

/// SDK-backed [`ShardSubscriber`].
pub struct KinesisShardSubscriber {
    kinesis: aws_sdk_kinesis::Client,
    shard_id: String,
    consumer_arn: String,
    stream_identifier: StreamIdentifier,
    // Per-flow control senders (to drive request_next/cancel from the publisher task).
    flows: Mutex<HashMap<u64, mpsc::UnboundedSender<FlowControl>>>,
}

impl KinesisShardSubscriber {
    /// Construct over a Kinesis client.
    pub fn new(
        kinesis: aws_sdk_kinesis::Client,
        shard_id: String,
        consumer_arn: String,
        stream_identifier: StreamIdentifier,
    ) -> Self {
        Self {
            kinesis,
            shard_id,
            consumer_arn,
            stream_identifier,
            flows: Mutex::new(HashMap::new()),
        }
    }
}

#[async_trait]
impl ShardSubscriber for KinesisShardSubscriber {
    async fn subscribe(
        &self,
        flow_id: u64,
        sequence_number: ExtendedSequenceNumber,
        is_first_connection: bool,
        initial_position: InitialPositionInStreamExtended,
        events: mpsc::UnboundedSender<FlowEvent>,
    ) {
        let (ctrl_tx, mut ctrl_rx) = mpsc::unbounded_channel::<FlowControl>();
        self.flows.lock().unwrap().insert(flow_id, ctrl_tx);

        // Build the starting position (Java subscribeToShard three-way branch).
        let starting_position = if sequence_number.is_shard_end() {
            iterator_builder::starting_position_request("LATEST", &initial_position)
        } else if is_first_connection {
            iterator_builder::starting_position_request(
                sequence_number.sequence_number(),
                &initial_position,
            )
        } else {
            iterator_builder::starting_position_reconnect_request(
                sequence_number.sequence_number(),
                &initial_position,
            )
        };

        let kinesis = self.kinesis.clone();
        let consumer_arn = self.consumer_arn.clone();
        let shard_id = self.shard_id.clone();
        let _stream_identifier = self.stream_identifier.clone();

        tokio::spawn(async move {
            let output = kinesis
                .subscribe_to_shard()
                .consumer_arn(consumer_arn)
                .shard_id(shard_id)
                .starting_position(starting_position)
                .send()
                .await;

            let mut output = match output {
                Ok(o) => o,
                Err(e) => {
                    let _ = events.send(FlowEvent::Error {
                        flow_id,
                        error: classify_throwable(&e),
                    });
                    return;
                }
            };

            // Signal that the event stream has started.
            let _ = events.send(FlowEvent::Started { flow_id });

            loop {
                // Wait for a pull signal (1-at-a-time credit) or cancel.
                match ctrl_rx.recv().await {
                    Some(FlowControl::RequestNext) => {}
                    Some(FlowControl::Cancel) | None => return,
                }
                // Pull until exactly one record event is forwarded (or the stream
                // terminates). A non-record variant (e.g. a future/unknown event
                // type; Java's Visitor no-op) must not consume the flow credit:
                // the publisher only re-requests per forwarded Records event, so
                // charging the credit here would stall the flow until the
                // health-check restart.
                loop {
                    match output.event_stream.recv().await {
                        Ok(Some(event_stream)) => {
                            if let Ok(event) = event_stream.as_subscribe_to_shard_event() {
                                let _ = events.send(FlowEvent::Records {
                                    flow_id,
                                    event: Box::new(event.clone()),
                                });
                                break;
                            }
                            tracing::debug!(
                                "ignoring non-record SubscribeToShard event-stream variant"
                            );
                        }
                        Ok(None) => {
                            let _ = events.send(FlowEvent::Complete { flow_id });
                            return;
                        }
                        Err(e) => {
                            let _ = events.send(FlowEvent::Error {
                                flow_id,
                                error: classify_throwable(&e),
                            });
                            return;
                        }
                    }
                }
            }
        });
    }

    fn request_next(&self, flow_id: u64) {
        if let Some(tx) = self.flows.lock().unwrap().get(&flow_id) {
            let _ = tx.send(FlowControl::RequestNext);
        }
    }

    fn cancel(&self, flow_id: u64) {
        if let Some(tx) = self.flows.lock().unwrap().remove(&flow_id) {
            let _ = tx.send(FlowControl::Cancel);
        }
    }
}

/// Classify an SDK/transport error into a [`FlowError`] (Java `throwableCategory`).
///
/// Java sniffs the cause chain for message prefix `"Acquire operation"` and a
/// simple-class-name containing `"ReadTimeoutException"`. The Rust SDK/transport
/// stack differs, so this matches the rendered error chain against those markers
/// plus `ResourceNotFoundException`.
pub(super) fn classify_throwable<E: std::error::Error + 'static>(err: &E) -> FlowError {
    let mut chain = String::new();
    let mut cur: Option<&(dyn std::error::Error + 'static)> = Some(err);
    while let Some(e) = cur {
        let msg = e.to_string();
        if msg.starts_with("Acquire operation") {
            return FlowError::AcquireTimeout(msg);
        }
        let type_name = std::any::type_name_of_val(e);
        if type_name.contains("ReadTimeout") || msg.contains("ReadTimeout") {
            return FlowError::ReadTimeout(msg);
        }
        if type_name.contains("ResourceNotFound") || msg.contains("ResourceNotFound") {
            return FlowError::ResourceNotFound(msg);
        }
        chain.push_str(&msg);
        chain.push('/');
        cur = e.source();
    }
    FlowError::Other(chain)
}
