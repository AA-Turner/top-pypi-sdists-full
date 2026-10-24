// Python Handler Task - Batched message delivery to Python callbacks
//
// This module implements the background task that receives messages from
// PythonHandler protocol mode channels and delivers them to Python callbacks
// with efficient batching to minimize GIL acquisition overhead.
//
// It also provides an outbound sender task that processes messages queued by
// Python callbacks (via send_handler_data) and sends them to WebRTC. This
// architecture prevents deadlocks by ensuring Python callbacks never block
// waiting for async operations.

use crate::buffer_pool::BufferPool;
use crate::channel::core::{PythonHandlerMessage, PythonHandlerOutbound};
use crate::runtime::RuntimeHandle;
use crate::tube_protocol::{CloseConnectionReason, Frame, MAX_FRAME_LEN};
use crate::tube_registry::REGISTRY;
use log::{debug, error, warn};
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyList};
use std::time::Duration;
use tokio::sync::mpsc;
use tokio::time::timeout;

/// Maximum number of messages to batch before calling Python
const MAX_BATCH_SIZE: usize = 10;

/// Maximum time to wait for more messages before flushing the batch
const BATCH_TIMEOUT_MS: u64 = 1;

/// Set up the Python handler task that receives messages from Rust and delivers to Python
///
/// The task batches messages to minimize GIL acquisition overhead:
/// - Up to MAX_BATCH_SIZE messages per batch
/// - Or BATCH_TIMEOUT_MS timeout, whichever comes first
///
/// # Arguments
/// * `conversation_id` - The conversation ID for this handler
/// * `receiver` - The receiver end of the message channel from Rust
/// * `runtime_handle` - The tokio runtime handle
/// * `callback` - The Python callback function to invoke with batched messages
///
/// The callback receives a list of dicts, each with:
/// - `type`: "data", "connection_opened", or "connection_closed"
/// - `conn_no`: The connection number
/// - `payload`: For data messages, the bytes payload
/// - `reason`: For connection_closed, the close reason code
pub fn setup_python_handler_task(
    conversation_id: String,
    mut receiver: mpsc::Receiver<PythonHandlerMessage>,
    runtime_handle: RuntimeHandle,
    callback: Py<PyAny>,
) {
    let task_conversation_id = conversation_id.clone();
    let runtime = runtime_handle.runtime().clone();

    runtime.spawn(async move {
        debug!(
            "Python handler task started (conversation_id: {})",
            task_conversation_id
        );

        let mut batch: Vec<PythonHandlerMessage> = Vec::with_capacity(MAX_BATCH_SIZE);
        let mut total_messages = 0u64;
        let mut total_batches = 0u64;

        loop {
            // Try to fill the batch
            let should_flush = loop {
                if batch.len() >= MAX_BATCH_SIZE {
                    // Batch is full, flush it
                    break true;
                }

                // Wait for a message with timeout
                match timeout(Duration::from_millis(BATCH_TIMEOUT_MS), receiver.recv()).await {
                    Ok(Some(msg)) => {
                        batch.push(msg);
                        // If batch is full, flush immediately
                        if batch.len() >= MAX_BATCH_SIZE {
                            break true;
                        }
                        // Try to get more messages without blocking
                        while batch.len() < MAX_BATCH_SIZE {
                            match receiver.try_recv() {
                                Ok(msg) => batch.push(msg),
                                Err(_) => break, // No more immediate messages
                            }
                        }
                        // Flush if we have any messages
                        if !batch.is_empty() {
                            break true;
                        }
                    }
                    Ok(None) => {
                        // Channel closed
                        debug!(
                            "Python handler channel closed (conversation_id: {})",
                            task_conversation_id
                        );
                        // Flush any remaining messages
                        break !batch.is_empty();
                    }
                    Err(_) => {
                        // Timeout - flush if we have messages
                        if !batch.is_empty() {
                            break true;
                        }
                        // No messages, continue waiting
                    }
                }
            };

            if should_flush && !batch.is_empty() {
                total_messages += batch.len() as u64;
                total_batches += 1;

                // Deliver batch to Python
                let batch_to_send = std::mem::replace(
                    &mut batch,
                    Vec::with_capacity(MAX_BATCH_SIZE),
                );

                let conv_id = task_conversation_id.clone();

                // Call Python with the batch
                // Note: callback is already owned by this async closure, so we can pass a reference
                if let Err(e) = deliver_batch_to_python(&conv_id, batch_to_send, &callback) {
                    error!(
                        "Error delivering batch to Python handler (conversation_id: {}): {:?}",
                        conv_id, e
                    );
                    // Don't break on error - continue processing
                }
            }

            // Check if channel is closed (receiver returned None)
            if receiver.is_closed() && batch.is_empty() {
                break;
            }
        }

        debug!(
            "Python handler task completed (conversation_id: {}, total_messages: {}, total_batches: {})",
            task_conversation_id, total_messages, total_batches
        );
    });
}

/// Deliver a batch of messages to the Python callback
fn deliver_batch_to_python(
    conversation_id: &str,
    batch: Vec<PythonHandlerMessage>,
    callback: &Py<PyAny>,
) -> PyResult<()> {
    Python::attach(|py| {
        let py_list = PyList::empty(py);

        for msg in batch {
            let py_dict = PyDict::new(py);

            match msg {
                PythonHandlerMessage::ConnectionOpened { conn_no } => {
                    py_dict.set_item("type", "connection_opened")?;
                    py_dict.set_item("conn_no", conn_no)?;
                    py_dict.set_item("conversation_id", conversation_id)?;
                }
                PythonHandlerMessage::Data { conn_no, payload } => {
                    py_dict.set_item("type", "data")?;
                    py_dict.set_item("conn_no", conn_no)?;
                    py_dict.set_item("conversation_id", conversation_id)?;
                    // Convert Bytes to PyBytes
                    let py_bytes = PyBytes::new(py, &payload);
                    py_dict.set_item("payload", py_bytes)?;
                }
                PythonHandlerMessage::ConnectionClosed { conn_no, reason } => {
                    py_dict.set_item("type", "connection_closed")?;
                    py_dict.set_item("conn_no", conn_no)?;
                    py_dict.set_item("conversation_id", conversation_id)?;
                    py_dict.set_item("reason", reason as u16)?;
                }
            }

            py_list.append(py_dict)?;
        }

        // Call the Python callback with the list of messages
        callback.call1(py, (py_list,)).map_err(|e| {
            // Log and convert the Python error
            warn!(
                "Python handler callback error (conversation_id: {}): {:?}",
                conversation_id, e
            );
            PyRuntimeError::new_err(format!("Handler callback failed: {e}"))
        })?;

        Ok(())
    })
}

/// Create a channel pair for Python handler communication
/// Returns (sender, receiver) where:
/// - sender: Used by the Channel to send messages to Python
/// - receiver: Used by the handler task to receive messages
pub fn create_handler_channel() -> (
    mpsc::Sender<PythonHandlerMessage>,
    mpsc::Receiver<PythonHandlerMessage>,
) {
    // Use a bounded channel to provide backpressure
    // 1000 messages should be plenty for most use cases
    mpsc::channel(1000)
}

/// Create an outbound channel for Python handler to send data back to WebRTC
/// Returns (sender, receiver) where:
/// - sender: Stored globally and used by send_handler_data() to queue messages
/// - receiver: Used by the outbound sender task to process messages
pub fn create_outbound_channel() -> (
    mpsc::Sender<PythonHandlerOutbound>,
    mpsc::Receiver<PythonHandlerOutbound>,
) {
    // Use a bounded channel for backpressure
    // 1000 messages should be plenty - sync responses are small
    mpsc::channel(1000)
}

/// Set up the outbound sender task that processes messages from Python callbacks
/// and sends them to WebRTC.
///
/// This task runs independently and processes the outbound queue, ensuring
/// Python callbacks never block waiting for async WebRTC operations.
///
/// # Arguments
/// * `conversation_id` - The conversation ID for logging
/// * `receiver` - The receiver end of the outbound message channel
/// * `runtime_handle` - The tokio runtime handle
pub fn setup_outbound_sender_task(
    conversation_id: String,
    receiver: mpsc::Receiver<PythonHandlerOutbound>,
    runtime_handle: RuntimeHandle,
) {
    runtime_handle
        .runtime()
        .spawn(run_outbound_sender(conversation_id, receiver, |id| {
            REGISTRY.get_by_conversation_id(id)
        }));
}

async fn run_outbound_sender(
    conversation_id: String,
    mut receiver: mpsc::Receiver<PythonHandlerOutbound>,
    lookup_tube: impl Fn(&str) -> Option<std::sync::Arc<crate::Tube>>,
) {
    debug!(
        "Outbound sender task started (conversation_id: {})",
        conversation_id
    );
    let buffer_pool = BufferPool::default();

    while let Some(msg) = receiver.recv().await {
        let Some(tube) = lookup_tube(&msg.conversation_id) else {
            warn!("Outbound sender: route disappeared");
            continue;
        };

        // Retirement makes later queued frames inadmissible without affecting
        // other virtual connections sharing this channel or outbound queue.
        if tube
            .check_handler_send_admission(&msg.conversation_id, msg.conn_no)
            .is_err()
        {
            debug!("Outbound sender: route retired");
            retire_failed_handler_connection(&tube, &msg).await;
            continue;
        }

        let Some(channel) = tube.resolve_handler_channel(&msg.conversation_id).await else {
            error!("Outbound sender: route resolution failed");
            retire_failed_handler_connection(&tube, &msg).await;
            continue;
        };
        // The nonblocking admission probe can be inconclusive while its route
        // lock is busy. Recheck the shared terminal marker after async lookup.
        if channel.failed_connections.contains(&msg.conn_no) {
            continue;
        }

        let frame = Frame::new_data_with_pool(msg.conn_no, &msg.data, &buffer_pool);
        let encoded = frame.encode_with_pool(&buffer_pool);
        if channel.send(encoded).await.is_err() {
            // Do not log transport error text: it can contain session data.
            error!("Outbound sender: native send failed");
            retire_failed_handler_connection(&tube, &msg).await;
        }
    }

    debug!(
        "Outbound sender task completed (conversation_id: {})",
        conversation_id
    );
}

async fn retire_failed_handler_connection(tube: &crate::Tube, msg: &PythonHandlerOutbound) {
    if tube
        .retire_handler_connection(
            &msg.conversation_id,
            msg.conn_no,
            CloseConnectionReason::Error,
        )
        .await
        .is_err()
    {
        error!("Outbound sender: connection retirement failed");
    }
}

/// Global outbound sender for Python handler mode
/// This is set up when a PythonHandler tube is created
static OUTBOUND_SENDER: std::sync::OnceLock<mpsc::Sender<PythonHandlerOutbound>> =
    std::sync::OnceLock::new();

/// Initialize the global outbound sender
/// Called when setting up a PythonHandler tube
pub fn init_outbound_sender(sender: mpsc::Sender<PythonHandlerOutbound>) {
    // Try to set. If already set, that's OK - we use the existing one
    let _ = OUTBOUND_SENDER.set(sender);
}

/// Reject a predictable framing failure before copying or queueing Python data.
pub(crate) fn validate_handler_payload_len(len: usize) -> Result<(), &'static str> {
    if len > MAX_FRAME_LEN {
        Err("Handler payload exceeds maximum frame length")
    } else {
        Ok(())
    }
}

/// Queue a message to be sent to WebRTC (non-blocking)
/// Called by send_handler_data() from within Python callbacks
///
/// Returns Ok(()) if the message was queued successfully
/// Returns Err for an oversized payload, a disappeared/closed route, or an
/// uninitialized/full/closed outbound queue.
pub fn queue_outbound_message(msg: PythonHandlerOutbound) -> Result<(), String> {
    validate_handler_payload_len(msg.data.len()).map_err(str::to_owned)?;
    let tube = REGISTRY
        .get_by_conversation_id(&msg.conversation_id)
        .ok_or_else(|| "Handler route not found".to_string())?;
    tube.check_handler_send_admission(&msg.conversation_id, msg.conn_no)?;
    let sender = OUTBOUND_SENDER
        .get()
        .ok_or_else(|| "Outbound sender not initialized".to_string())?;

    try_queue_outbound_message(sender, msg)
}

fn try_queue_outbound_message(
    sender: &mpsc::Sender<PythonHandlerOutbound>,
    msg: PythonHandlerOutbound,
) -> Result<(), String> {
    validate_handler_payload_len(msg.data.len()).map_err(str::to_owned)?;
    sender.try_send(msg).map_err(|e| match e {
        mpsc::error::TrySendError::Full(_) => "Outbound queue full".to_string(),
        mpsc::error::TrySendError::Closed(_) => "Outbound channel closed".to_string(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use bytes::Bytes;

    fn outbound(conn_no: u32, data: Bytes) -> PythonHandlerOutbound {
        PythonHandlerOutbound {
            conversation_id: "handler-send-regression".to_string(),
            conn_no,
            data,
        }
    }

    #[test]
    fn over_cap_payload_is_rejected_before_enqueue() {
        let (sender, mut receiver) = mpsc::channel(1);
        let error = try_queue_outbound_message(
            &sender,
            outbound(1, Bytes::from(vec![0; MAX_FRAME_LEN + 1])),
        )
        .unwrap_err();
        assert_eq!(error, "Handler payload exceeds maximum frame length");
        assert_eq!(sender.capacity(), 1);
        assert!(matches!(
            receiver.try_recv(),
            Err(mpsc::error::TryRecvError::Empty)
        ));
        assert!(validate_handler_payload_len(MAX_FRAME_LEN).is_ok());

        try_queue_outbound_message(&sender, outbound(2, Bytes::from_static(b"live"))).unwrap();
        assert_eq!(receiver.try_recv().unwrap().conn_no, 2);
    }

    #[test]
    fn oversized_payload_precedes_queue_and_route_errors() {
        let error = queue_outbound_message(outbound(1, Bytes::from(vec![0; MAX_FRAME_LEN + 1])))
            .unwrap_err();
        assert_eq!(error, "Handler payload exceeds maximum frame length");
    }

    #[tokio::test]
    async fn native_send_failure_retires_once_and_preserves_other_connections() {
        use crate::channel::core::{Channel, ChannelParams, ProtocolLogicState};
        use crate::tube_protocol::{try_parse_frame, Capabilities, ControlMessage};
        use crate::webrtc_data_channel::WebRTCDataChannel;
        use bytes::BytesMut;
        use std::collections::HashMap;
        use std::sync::atomic::{AtomicUsize, Ordering};
        use std::sync::Arc;
        use webrtc::api::APIBuilder;
        use webrtc::peer_connection::configuration::RTCConfiguration;

        let peer = APIBuilder::new()
            .build()
            .new_peer_connection(RTCConfiguration::default())
            .await
            .unwrap();
        let transport =
            WebRTCDataChannel::new(peer.create_data_channel("control", None).await.unwrap());
        let failed_attempts = Arc::new(AtomicUsize::new(0));
        let observed_attempts = failed_attempts.clone();
        crate::webrtc_data_tap::set(
            &transport.outbound_tap,
            Arc::new(crate::webrtc_data_tap::FnTap::new(
                move |_: &str, _: &Bytes| {
                    observed_attempts.fetch_add(1, Ordering::Relaxed);
                },
            )),
        );
        let healthy_peer = APIBuilder::new()
            .build()
            .new_peer_connection(RTCConfiguration::default())
            .await
            .unwrap();
        let healthy_remote = APIBuilder::new()
            .build()
            .new_peer_connection(RTCConfiguration::default())
            .await
            .unwrap();
        let (healthy_tx, mut healthy_rx) = mpsc::unbounded_channel();
        healthy_remote.on_data_channel(Box::new(move |data_channel| {
            let healthy_tx = healthy_tx.clone();
            data_channel.on_message(Box::new(move |message| {
                let healthy_tx = healthy_tx.clone();
                Box::pin(async move {
                    healthy_tx.send(message.data).unwrap();
                })
            }));
            Box::pin(async {})
        }));
        let healthy = WebRTCDataChannel::new(
            healthy_peer
                .create_data_channel("healthy-handler-route", None)
                .await
                .unwrap(),
        );
        let mut offer_gathered = healthy_peer.gathering_complete_promise().await;
        healthy_peer
            .set_local_description(healthy_peer.create_offer(None).await.unwrap())
            .await
            .unwrap();
        timeout(Duration::from_secs(10), offer_gathered.recv())
            .await
            .unwrap();
        healthy_remote
            .set_remote_description(healthy_peer.local_description().await.unwrap())
            .await
            .unwrap();
        let mut answer_gathered = healthy_remote.gathering_complete_promise().await;
        healthy_remote
            .set_local_description(healthy_remote.create_answer(None).await.unwrap())
            .await
            .unwrap();
        timeout(Duration::from_secs(10), answer_gathered.recv())
            .await
            .unwrap();
        healthy_peer
            .set_remote_description(healthy_remote.local_description().await.unwrap())
            .await
            .unwrap();
        assert!(healthy
            .wait_for_channel_open(Some(Duration::from_secs(10)))
            .await
            .unwrap());
        let (input_tx, input_rx) = mpsc::unbounded_channel();
        *transport.local_input.lock() = Some(input_tx);
        let (callback_tx, mut callback_rx) = create_handler_channel();
        let mut channel = Channel::new(ChannelParams {
            webrtc: transport.clone(),
            rx_from_dc: input_rx,
            tx_from_dc: transport.local_input.clone(),
            channel_id: "control".to_string(),
            conversation_id: "handler-send-regression".to_string(),
            timeouts: None,
            protocol_settings: HashMap::from([(
                "conversationType".to_string(),
                serde_json::json!("python_handler"),
            )]),
            server_mode: false,
            shutdown_notify: Arc::new(tokio::sync::Notify::new()),
            callback_token: None,
            ksm_config: None,
            client_version: String::new(),
            capabilities: Capabilities::NONE,
            python_handler_tx: Some(callback_tx),
            handler_registry: None,
            spawned_task_completion_tx: Arc::new(mpsc::unbounded_channel().0),
            video_output: None,
        })
        .await
        .unwrap();
        if let ProtocolLogicState::PythonHandler(state) = &mut channel.protocol_state {
            state.active_connections.extend([1, 2]);
        } else {
            panic!("expected PythonHandler protocol");
        }

        let tube = crate::Tube::new(
            false,
            Some("handler-send-regression".to_string()),
            None,
            None,
            Capabilities::NONE,
            None,
        )
        .unwrap();
        tube.data_channels
            .write()
            .await
            .insert("control".to_string(), transport.clone());
        tube.data_channels
            .write()
            .await
            .insert("healthy-handler-route".to_string(), healthy);
        assert!(tube
            .check_handler_send_admission("handler-send-regression", 1)
            .is_ok());

        let (sender, receiver) = mpsc::channel(3);
        for _ in 0..2 {
            try_queue_outbound_message(&sender, outbound(1, Bytes::from_static(b"data"))).unwrap();
        }
        try_queue_outbound_message(
            &sender,
            PythonHandlerOutbound {
                conversation_id: "healthy-handler-route".to_string(),
                conn_no: 2,
                data: Bytes::from_static(b"unrelated data"),
            },
        )
        .unwrap();
        drop(sender);
        run_outbound_sender("handler-send-regression".to_string(), receiver, |_| {
            Some(tube.clone())
        })
        .await;

        let healthy_received = timeout(Duration::from_secs(10), healthy_rx.recv())
            .await
            .unwrap()
            .unwrap();
        let mut healthy_frame = BytesMut::from(healthy_received.as_ref());
        let healthy_frame = try_parse_frame(&mut healthy_frame).unwrap().unwrap();
        assert_eq!(healthy_frame.connection_no, 2);
        assert_eq!(healthy_frame.payload, Bytes::from_static(b"unrelated data"));
        assert!(matches!(
            healthy_rx.try_recv(),
            Err(mpsc::error::TryRecvError::Empty)
        ));

        assert!(tube
            .check_handler_send_admission("handler-send-regression", 1)
            .is_err());
        assert_eq!(
            failed_attempts.load(Ordering::Relaxed),
            1,
            "stale frames must not retry the failed native send"
        );
        assert!(tube
            .check_handler_send_admission("handler-send-regression", 2)
            .is_ok());
        assert!(tube
            .check_handler_send_admission("healthy-handler-route", 2)
            .is_ok());
        assert_eq!(transport.failed_connections.len(), 1);

        let mut close = BytesMut::from(channel.rx_from_dc.try_recv().unwrap().as_ref());
        let frame = try_parse_frame(&mut close).unwrap().unwrap();
        assert_eq!(frame.connection_no, 0);
        assert_eq!(
            &frame.payload[..2],
            &(ControlMessage::CloseConnection as u16).to_be_bytes()
        );
        channel
            .process_control_message(ControlMessage::CloseConnection, &frame.payload[2..])
            .await
            .unwrap();
        // A duplicate remote close must not produce a second typed callback.
        channel
            .process_control_message(ControlMessage::CloseConnection, &frame.payload[2..])
            .await
            .unwrap();
        assert!(matches!(
            callback_rx.try_recv().unwrap(),
            PythonHandlerMessage::ConnectionClosed {
                conn_no: 1,
                reason: CloseConnectionReason::Error,
            }
        ));
        assert!(matches!(
            callback_rx.try_recv(),
            Err(mpsc::error::TryRecvError::Empty)
        ));
        assert!(matches!(
            channel.rx_from_dc.try_recv(),
            Err(mpsc::error::TryRecvError::Empty)
        ));
        if let ProtocolLogicState::PythonHandler(state) = &channel.protocol_state {
            assert!(!state.active_connections.contains(&1));
            assert!(state.active_connections.contains(&2));
        }
        // Failure before confirmation must still produce a typed close.
        tube.retire_handler_connection("handler-send-regression", 3, CloseConnectionReason::Error)
            .await
            .unwrap();
        let frame = try_parse_frame(&mut BytesMut::from(
            channel.rx_from_dc.try_recv().unwrap().as_ref(),
        ))
        .unwrap()
        .unwrap();
        channel
            .process_control_message(ControlMessage::CloseConnection, &frame.payload[2..])
            .await
            .unwrap();
        assert!(matches!(
            callback_rx.try_recv().unwrap(),
            PythonHandlerMessage::ConnectionClosed {
                conn_no: 3,
                reason: CloseConnectionReason::Error
            }
        ));
        // A new confirmed lifetime clears terminal markers; a lost receive task
        // still delivers the local failure through the existing callback channel.
        channel
            .process_control_message(ControlMessage::ConnectionOpened, &1u32.to_be_bytes())
            .await
            .unwrap();
        assert!(matches!(
            callback_rx.try_recv().unwrap(),
            PythonHandlerMessage::ConnectionOpened { conn_no: 1 }
        ));
        assert!(tube
            .check_handler_send_admission("handler-send-regression", 1)
            .is_ok());
        transport.local_input.lock().take();
        *tube.python_handler_tx.write().await = channel.python_handler_tx.clone();
        tube.retire_handler_connection("handler-send-regression", 1, CloseConnectionReason::Error)
            .await
            .unwrap();
        tube.retire_handler_connection("handler-send-regression", 1, CloseConnectionReason::Error)
            .await
            .unwrap();
        assert!(matches!(
            callback_rx.try_recv().unwrap(),
            PythonHandlerMessage::ConnectionClosed {
                conn_no: 1,
                reason: CloseConnectionReason::Error
            }
        ));
        assert!(callback_rx.try_recv().is_err());
        peer.close().await.unwrap();
        healthy_peer.close().await.unwrap();
        healthy_remote.close().await.unwrap();
    }

    #[test]
    fn disappeared_route_is_rejected_before_queue_admission() {
        let error = queue_outbound_message(PythonHandlerOutbound {
            conversation_id: format!("missing-handler-route-{}", uuid::Uuid::new_v4()),
            conn_no: 1,
            data: Bytes::from_static(b"data"),
        })
        .unwrap_err();
        assert_eq!(error, "Handler route not found");
    }
}
