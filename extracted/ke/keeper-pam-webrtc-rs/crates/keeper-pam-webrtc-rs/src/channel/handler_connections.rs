// Handler-based connection management (zero-copy integration with guacr)
//
// This module provides zero-copy integration with guacr protocol handlers using
// the EventCallback pattern. Falls back to channel-based interface for backwards
// compatibility if handlers don't support EventBasedHandler trait yet.

use async_trait::async_trait;
use guacr_handlers::{
    EventCallback, HandlerError, HandlerEvent, ProtocolHandlerRegistry, VideoOutput,
};

use crate::channel::core::Channel;
use crate::models::ConversationType;
use crate::tube_protocol::{CloseConnectionReason, ControlMessage, Frame};
use crate::unlikely; // Branch prediction optimization
use anyhow::{anyhow, Result};
use bytes::{BufMut, Bytes};
use log::{debug, error, info, trace, warn};
use std::future::Future;
use std::sync::Arc;
use tokio::sync::mpsc;

fn log_handler_failure(error: &HandlerError) {
    let operation = match error {
        HandlerError::ConnectionFailed(_) => "connection",
        HandlerError::AuthenticationFailed(_) => "authentication",
        HandlerError::RecordingFailed(_) => "recording",
        _ => "lifecycle",
    };
    let outcome = if matches!(error, HandlerError::Timeout(_)) {
        "timed_out"
    } else {
        "failed"
    };
    if let HandlerError::IoError(error) = error {
        if let Some(errno) = error.raw_os_error() {
            tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation, outcome, errno, "Handler failed");
        } else {
            tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation, outcome, "Handler IO failed");
        }
    } else {
        tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation, outcome, "Handler failed");
    }
}

fn drain_terminal_batch(
    first: Bytes,
    rx: &mut mpsc::Receiver<Bytes>,
    pending: &mut Option<Bytes>,
) -> Bytes {
    const TERMINAL_DATA_OPCODE: u8 = 0x20;
    const MAX_BATCH_PAYLOAD: usize = guacr_protocol::MAX_SAFE_PAYLOAD_SIZE;

    let mut batch = bytes::BytesMut::with_capacity(first.len());
    batch.extend_from_slice(&first);
    while batch.len() < MAX_BATCH_PAYLOAD {
        match rx.try_recv() {
            Ok(more) if more.first() == Some(&TERMINAL_DATA_OPCODE) => {
                if batch.len() + more.len() > MAX_BATCH_PAYLOAD {
                    *pending = Some(more);
                    break;
                }
                batch.extend_from_slice(&more);
            }
            Ok(other) => {
                *pending = Some(other);
                break;
            }
            Err(_) => break,
        }
    }
    batch.freeze()
}

fn now_ms() -> u64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or(std::time::Duration::ZERO)
        .as_millis() as u64
}

/// Terminal events select a reason; only the dedicated sender closes the wire.
#[derive(Clone, Copy, Default)]
struct HandlerTermination {
    reason: Option<CloseConnectionReason>,
    finished: bool,
    discard_output: bool,
    producer_done: bool,
}

fn request_termination(
    terminal: &tokio::sync::watch::Sender<HandlerTermination>,
    reason: CloseConnectionReason,
    finished: bool,
) {
    terminal.send_modify(|state| {
        // A normal completion must never overwrite an explicit critical event.
        if state.reason != Some(CloseConnectionReason::SecurityThreat)
            && (reason != CloseConnectionReason::Normal || state.reason.is_none())
        {
            state.reason = Some(reason);
        }
        state.finished |= finished;
    });
}

fn finish_termination(
    terminal: &tokio::sync::watch::Sender<HandlerTermination>,
    reason: CloseConnectionReason,
) {
    request_termination(terminal, reason, true);
    terminal.send_modify(|state| state.producer_done = true);
}

#[derive(Clone)]
struct WebRtcEventCallback {
    conn_no: u32,
    channel_id: String,
    conversation_id: String,
    terminal: tokio::sync::watch::Sender<HandlerTermination>,
    send_queue_tx: mpsc::Sender<Bytes>,
    handler_senders: Arc<dashmap::DashMap<u32, mpsc::Sender<Bytes>>>,
}
#[derive(Clone)]
struct HandlerOutput {
    conn_no: u32,
    channel_id: String,
    buffer_pool: crate::buffer_pool::BufferPool,
    channel_close_reason: Arc<tokio::sync::Mutex<Option<CloseConnectionReason>>>,
    conn_closed_tx: mpsc::UnboundedSender<(u32, String)>,
    handler_senders: Arc<dashmap::DashMap<u32, mpsc::Sender<Bytes>>>,
    finalization_deadline: std::time::Duration,
}

/// The sole owner of output ordering and connection retirement. Closing the
/// receiver seals admission but preserves every queued instruction and permit.
async fn send_handler_output<S, Fut>(
    mut rx: mpsc::Receiver<Bytes>,
    terminal: tokio::sync::watch::Sender<HandlerTermination>,
    output: HandlerOutput,
    mut send: S,
) -> Result<(), HandlerError>
where
    S: FnMut(Bytes) -> Fut,
    Fut: Future<Output = Result<(), String>>,
{
    let mut changes = terminal.subscribe();
    let mut pending = None;
    let mut failure = None;
    loop {
        if changes.borrow().discard_output {
            rx.close();
            while rx.try_recv().is_ok() {}
            break;
        }
        if changes.borrow().finished {
            // Producers can retain cloned senders in auxiliary tasks. Completion,
            // not every clone drop, seals admission after queued output drains.
            rx.close();
        }
        let first = match pending.take() {
            Some(first) => first,
            None => tokio::select! {
                biased;
                _ = changes.changed() => continue,
                next = rx.recv() => match next {
                    Some(first) => first,
                    None if changes.borrow().finished => break,
                    None => {
                        // An early drop of the callback is not handler completion:
                        // recording finalization may still be running.
                        let _ = changes.changed().await;
                        continue;
                    }
                },
            },
        };
        let payload = if first.first() == Some(&0x20) {
            drain_terminal_batch(first, &mut rx, &mut pending)
        } else {
            first
        };
        let frame = Frame {
            connection_no: output.conn_no,
            timestamp_ms: now_ms(),
            payload,
        };
        if send(frame.encode_with_pool(&output.buffer_pool))
            .await
            .is_err()
        {
            tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation = "send", outcome = "failed", "Handler instruction send failed");
            rx.close();
            terminal.send_modify(|state| state.discard_output = true);
            request_termination(&terminal, CloseConnectionReason::HandlerError, true);
            failure = Some(HandlerError::ChannelError(
                "Instruction send failed".to_string(),
            ));
            break;
        }
    }
    let reason = terminal
        .borrow()
        .reason
        .unwrap_or(CloseConnectionReason::Normal);
    let wait_for_producer_before_close = reason != CloseConnectionReason::SecurityThreat;
    if wait_for_producer_before_close {
        // A normal or error terminal frame follows final admitted output and
        // required producer cleanup.
        while !changes.borrow().producer_done {
            let _ = changes.changed().await;
        }
    }
    if reason != CloseConnectionReason::Normal {
        let mut stored = output.channel_close_reason.lock().await;
        if *stored != Some(CloseConnectionReason::SecurityThreat) {
            *stored = Some(reason);
        }
    }
    let mut payload = output.buffer_pool.acquire();
    payload.extend_from_slice(&output.conn_no.to_be_bytes());
    payload.put_u8(reason as u8);
    let frame = Frame::new_control_with_pool(
        ControlMessage::CloseConnection,
        &payload,
        &output.buffer_pool,
    );
    if send(frame.encode_with_pool(&output.buffer_pool))
        .await
        .is_err()
    {
        tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation = "close", outcome = "failed", "Handler close send failed");
        failure.get_or_insert_with(|| HandlerError::ChannelError("Close send failed".to_string()));
    }
    if !wait_for_producer_before_close {
        // Threat policy closes the wire and input route immediately, but local
        // retirement still waits for producer cleanup or its backstop.
        while !changes.borrow().producer_done {
            let _ = changes.changed().await;
        }
    }
    output.handler_senders.remove(&output.conn_no);
    let _ = output
        .conn_closed_tx
        .send((output.conn_no, output.channel_id));
    match failure {
        Some(error) => Err(error),
        None => Ok(()),
    }
}

/// Normal/error completion waits for handler finalization. A broken sender seals
/// output, lets the handler finalize within its deadline, and aborts only as a
/// last resort. Threats close the wire immediately while retaining local cleanup.
async fn run_handler_session<H, S, Fut>(
    handler: H,
    rx: mpsc::Receiver<Bytes>,
    terminal: tokio::sync::watch::Sender<HandlerTermination>,
    output: HandlerOutput,
    send: S,
) -> Result<(), HandlerError>
where
    H: Future<Output = Result<(), HandlerError>> + Send + 'static,
    S: FnMut(Bytes) -> Fut,
    Fut: Future<Output = Result<(), String>>,
{
    let mut changes = terminal.subscribe();
    let mut producer = tokio::task::JoinSet::new();
    producer.spawn(handler);
    let sender = send_handler_output(rx, terminal.clone(), output.clone(), send);
    tokio::pin!(sender);
    let mut deadline = Box::pin(tokio::time::sleep(std::time::Duration::MAX));
    let mut deadline_armed = false;
    let producer_result = loop {
        tokio::select! {
            biased;
            result = producer.join_next() => {
                let result = match result {
                    Some(Ok(result)) => result,
                    _ => Err(HandlerError::ChannelError("Handler task failed".to_string())),
                };
                let requested_reason = match &result {
                    Err(HandlerError::SecurityViolation(_)) => CloseConnectionReason::SecurityThreat,
                    Err(_) => CloseConnectionReason::HandlerError,
                    Ok(()) => CloseConnectionReason::Normal,
                };
                finish_termination(&terminal, requested_reason);
                let reason = terminal
                    .borrow()
                    .reason
                    .unwrap_or(CloseConnectionReason::HandlerError);
                if reason == CloseConnectionReason::SecurityThreat {
                    break Err(HandlerError::SecurityViolation("Handler threat policy terminated session".to_string()));
                }
                break result;
            }
            _ = changes.changed() => {
                if changes.borrow().reason.is_some() && !deadline_armed {
                    deadline.as_mut().reset(tokio::time::Instant::now() + output.finalization_deadline);
                    deadline_armed = true;
                }
            }
            _ = &mut deadline, if deadline_armed => {
                let reason = terminal.borrow().reason.unwrap_or(CloseConnectionReason::HandlerError);
                tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation = "finalize", outcome = "timed_out", "Handler finalization exceeded deadline");
                producer.abort_all();
                let _ = producer.join_next().await;
                finish_termination(&terminal, reason);
                break Err(HandlerError::ChannelError("Handler finalization exceeded deadline".to_string()));
            }
            result = &mut sender => {
                // The sender cannot finish before producer_done is acknowledged.
                // Keep polling it here to propagate backpressure/send failures.
                return result;
            }
        }
    };
    let sender_result = sender.await;
    producer_result.and(sender_result)
}

#[async_trait]
impl EventCallback for WebRtcEventCallback {
    /// Handle critical events from protocol handler
    ///
    /// This is called for errors, disconnects, and threats. Regular instructions
    /// bypass this method and go directly through send_instruction() for zero-copy.
    fn on_event(&self, event: HandlerEvent) {
        match event {
            HandlerEvent::Error { message: _, code } => {
                if let Some(code) = code {
                    tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation = "lifecycle", outcome = "failed", error_code = i64::from(code), "Handler error");
                } else {
                    tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation = "lifecycle", outcome = "failed", "Handler error");
                }

                request_termination(&self.terminal, CloseConnectionReason::HandlerError, false);
            }

            HandlerEvent::Disconnect { reason: _ } => {
                info!(
                    "Handler disconnect (channel: {}, conversation_id: {}, conn: {})",
                    self.channel_id, self.conversation_id, self.conn_no
                );

                request_termination(&self.terminal, CloseConnectionReason::Normal, false);
            }

            HandlerEvent::ThreatDetected {
                level: _,
                description: _,
            } => {
                self.handler_senders.remove(&self.conn_no);
                self.terminal
                    .send_modify(|state| state.discard_output = true);
                request_termination(&self.terminal, CloseConnectionReason::SecurityThreat, true);
            }

            HandlerEvent::Ready { connection_id } => {
                debug!(
                    "Handler ready (channel: {}, conversation_id: {}, conn: {}, connection_id: {})",
                    self.channel_id, self.conversation_id, self.conn_no, connection_id
                );
            }

            HandlerEvent::Size { width, height } => {
                trace!(
                    "Handler size change (channel: {}, conversation_id: {}, conn: {}): {}x{}",
                    self.channel_id,
                    self.conversation_id,
                    self.conn_no,
                    width,
                    height
                );
            }

            HandlerEvent::Instruction(bytes) => {
                // This shouldn't happen in normal flow - send_instruction is the hot path
                warn!(
                    "Received Instruction event (should use send_instruction): {} bytes (channel: {}, conversation_id: {}, conn: {})",
                    bytes.len(), self.channel_id, self.conversation_id, self.conn_no
                );
                // The synchronous compatibility path cannot await backpressure.
                // Failed admission is terminal, never detached or silently dropped.
                if self.send_queue_tx.try_send(bytes).is_err() {
                    tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation = "send", outcome = "failed", "Handler instruction admission failed");
                    request_termination(&self.terminal, CloseConnectionReason::HandlerError, true);
                }
            }
        }
    }

    /// Send instruction to WebRTC client (ZERO-COPY HOT PATH WITH BACKPRESSURE)
    ///
    /// This is the performance-critical path. Bytes is reference-counted (Arc internally),
    /// so no copying occurs. The instruction is queued for sending by a dedicated sender task.
    ///
    /// Uses blocking send().await to provide proper backpressure. If the WebRTC send queue
    /// is full, this awaits here (blocking the handler's forwarding task) rather than:
    /// - Dropping frames (unacceptable for RDP/VNC/database protocols)
    /// - Spawning tasks (which caused the original "one char behind" latency)
    ///
    /// The channel capacity (256) gives image protocols headroom while Guacamole
    /// sync/ACK flow control in terminal handlers prevents unbounded queuing.
    async fn send_instruction(&self, instruction: Bytes) -> Result<(), HandlerError> {
        if self.terminal.borrow().discard_output {
            return Err(HandlerError::ChannelError("Send queue closed".to_string()));
        }
        // Send to dedicated sender task with backpressure (blocks if queue full)
        // This is the RIGHT behavior: better to slow down the handler than drop frames
        if self.send_queue_tx.send(instruction).await.is_err() {
            return Err(HandlerError::ChannelError("Send queue closed".to_string()));
        }
        Ok(())
    }
}

/// Invoke a built-in protocol handler with zero-copy integration
///
/// This function uses the EventCallback pattern for zero-copy data sharing.
/// Falls back to channel-based interface if handlers don't implement
/// EventBasedHandler yet (backwards compatible).
///
/// # Zero-Copy Architecture
///
/// Handler -> EventCallback::send_instruction(Bytes) -> Frame -> WebRTC
///                            |
///                            v
///                      No copying (Bytes is Arc)
///
/// # RAII Safety
///
/// - All tasks are spawned with proper cleanup
/// - handler_senders are removed on completion
/// - No resource leaks (compiler enforced)
pub async fn invoke_builtin_handler(
    channel: &Channel,
    conversation_type: &ConversationType,
    registry: &Arc<ProtocolHandlerRegistry>,
    conn_no: u32,
    spawned_task_completion_tx: Arc<tokio::sync::mpsc::UnboundedSender<()>>,
) -> Result<()> {
    let protocol_name = conversation_type.to_string();

    info!(
        "Channel({}): Invoking built-in handler for protocol '{}' (conversation_id: {}, conn_no: {})",
        channel.channel_id, protocol_name, channel.conversation_id, conn_no
    );

    // Get handler from registry
    let handler = registry
        .get(&protocol_name)
        .ok_or_else(|| anyhow!("No handler registered for protocol: {}", protocol_name))?;

    debug!(
        "Channel({}): Found handler for protocol: {} (conversation_id: {})",
        channel.channel_id, protocol_name, channel.conversation_id
    );

    // Get connection parameters
    let params = channel.guacd_params.lock().await.clone();

    debug!(
        "Channel({}): Handler params: {:?} (conversation_id: {})",
        channel.channel_id,
        params.keys().collect::<Vec<_>>(),
        channel.conversation_id
    );

    // Check if handler supports event-based interface (zero-copy path)
    if handler.as_event_based().is_some() {
        info!(
            "Channel({}): Using event-based zero-copy interface for protocol: {} (conversation_id: {})",
            channel.channel_id, protocol_name, channel.conversation_id
        );

        let handler_arc = Arc::clone(&handler);
        let (send_queue_tx, send_queue_rx) = mpsc::channel::<Bytes>(256);
        let (terminal, _) = tokio::sync::watch::channel(HandlerTermination::default());
        let callback = Arc::new(WebRtcEventCallback {
            conn_no,
            channel_id: channel.channel_id.clone(),
            conversation_id: channel.conversation_id.clone(),
            terminal: terminal.clone(),
            send_queue_tx,
            handler_senders: channel.handler_senders.clone(),
        });
        let output = HandlerOutput {
            conn_no,
            channel_id: channel.channel_id.clone(),
            buffer_pool: channel.buffer_pool.clone(),
            channel_close_reason: channel.channel_close_reason.clone(),
            conn_closed_tx: channel.conn_closed_tx.clone(),
            handler_senders: channel.handler_senders.clone(),
            finalization_deadline: channel.timeouts.handler_finalization,
        };
        let handler_finalization_timeout = output.finalization_deadline;
        let webrtc = channel.webrtc.clone();

        // Create channel for bidirectional communication (WebRTC → Handler)
        // The handler receives client messages (keyboard, mouse, etc.) through this channel
        let (webrtc_tx, from_client_rx) = mpsc::channel::<Bytes>(128);

        // Store sender so incoming frames can be forwarded to handler
        channel.handler_senders.insert(conn_no, webrtc_tx.clone());

        // Spawn handler task with event callback
        let protocol_for_task = protocol_name.clone();
        let channel_id_clone = channel.channel_id.clone();
        let conversation_id_clone = channel.conversation_id.clone();
        // Clone video_output before the spawn — channel is a borrow, can't cross spawn boundary
        let video_tx_for_handler: Option<Arc<dyn VideoOutput>> = channel.video_output.clone();
        let handler_handle = tokio::spawn(async move {
            debug!(
                "Event-based handler task started for protocol: {} (channel: {}, conversation_id: {})",
                protocol_for_task, channel_id_clone, conversation_id_clone
            );

            let producer = async move {
                let event_handler = handler_arc.as_event_based().ok_or_else(|| {
                    HandlerError::Unsupported("Event interface unavailable".to_string())
                })?;
                event_handler
                    .connect_with_events(
                        params,
                        callback,
                        from_client_rx,
                        video_tx_for_handler,
                        guacr_handlers::SessionHooks {
                            handler_finalization_timeout,
                            ..Default::default()
                        },
                    )
                    .await
            };
            let result =
                run_handler_session(producer, send_queue_rx, terminal, output, move |encoded| {
                    let webrtc = webrtc.clone();
                    async move { webrtc.send(encoded).await }
                })
                .await;
            if let Err(error) = result {
                log_handler_failure(&error);
            }

            info!(
                "Event-based handler session ended for protocol: {} (channel: {}, conversation_id: {})",
                protocol_for_task, channel_id_clone, conversation_id_clone
            );
        });

        // Spawn monitor task to track event-based handler task completion
        let handler_completion_tx = Arc::clone(&spawned_task_completion_tx);
        let handler_monitor_channel_id = channel.channel_id.clone();
        let handler_monitor_conversation_id = channel.conversation_id.clone();
        tokio::spawn(async move {
            match handler_handle.await {
                Ok(()) => {
                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!("Event-based handler task completed normally (channel: {}, conversation_id: {})", handler_monitor_channel_id, handler_monitor_conversation_id);
                    }
                }
                Err(e) => {
                    tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation = "lifecycle", outcome = if e.is_cancelled() { "cancelled" } else { "failed" }, "Event-based handler task ended abnormally");
                }
            }
            let _ = handler_completion_tx.send(());
        });

        return Ok(());
    }

    // Fallback to channel-based interface (for handlers that don't implement EventBasedHandler yet)
    info!(
        "Channel({}): Using channel-based interface (fallback) for protocol: {} (conversation_id: {})",
        channel.channel_id, protocol_name, channel.conversation_id
    );

    // Create channels for bidirectional communication
    // Handler → WebRTC (handler sends messages to client)
    let (handler_to_webrtc, mut handler_rx) = mpsc::channel::<Bytes>(128);

    // WebRTC → Handler (client sends messages to handler)
    let (webrtc_tx, handler_from_webrtc) = mpsc::channel::<Bytes>(128);

    // Store sender so incoming frames can be forwarded to handler
    channel.handler_senders.insert(conn_no, webrtc_tx.clone());

    let protocol_for_handler = protocol_name.clone();
    let protocol_for_outbound = protocol_name.clone();
    let channel_id_for_handler_task = channel.channel_id.clone();
    let conversation_id_for_handler_task = channel.conversation_id.clone();
    // Clone before spawn — channel is a borrow, can't cross spawn boundary
    let video_tx_for_handler: Option<Arc<dyn VideoOutput>> = channel.video_output.clone();

    // Spawn protocol handler task
    let handler_task = tokio::spawn(async move {
        debug!(
            "Channel-based handler task started for protocol: {} (channel: {}, conversation_id: {})",
            protocol_for_handler, channel_id_for_handler_task, conversation_id_for_handler_task
        );

        match handler
            .connect(
                params,
                handler_to_webrtc,
                handler_from_webrtc,
                video_tx_for_handler,
                guacr_handlers::SessionHooks::default(),
            )
            .await
        {
            Ok(()) => {
                info!(
                    "Channel-based handler completed successfully: {} (channel: {}, conversation_id: {})",
                    protocol_for_handler, channel_id_for_handler_task, conversation_id_for_handler_task
                );
                Ok(())
            }
            Err(e) => {
                log_handler_failure(&e);
                Err(anyhow!("Handler error: {}", e))
            }
        }
    });

    // Clone needed fields for forwarding tasks
    let dc = channel.webrtc.clone();
    let channel_id_for_outbound = channel.channel_id.clone();
    let conversation_id_for_outbound = channel.conversation_id.clone();
    let conn_closed_tx = channel.conn_closed_tx.clone();
    let buffer_pool = channel.buffer_pool.clone();

    // Task 1: Handler → WebRTC (outbound)
    // Read messages from handler and send to WebRTC data channel
    let outbound_task = tokio::spawn(async move {
        debug!(
            "Handler outbound task started (channel: {}, conversation_id: {}, protocol: {})",
            channel_id_for_outbound, conversation_id_for_outbound, protocol_for_outbound
        );

        let mut message_count = 0u64;
        let mut total_bytes = 0u64;

        while let Some(msg) = handler_rx.recv().await {
            message_count += 1;
            let msg_len = msg.len();
            total_bytes += msg_len as u64;

            // Log first 60 chars of message for debugging
            if crate::logger::is_verbose_logging() {
                let msg_preview = String::from_utf8_lossy(&msg[..msg.len().min(60)]);
                trace!(
                    "Handler → WebRTC: message #{} ({} bytes): {}... (channel: {}, conversation_id: {})",
                    message_count,
                    msg_len,
                    msg_preview,
                    channel_id_for_outbound,
                    conversation_id_for_outbound
                );
            }

            // Wrap handler output in Frame with connection number
            let frame = Frame {
                connection_no: conn_no,
                timestamp_ms: now_ms(),
                payload: msg,
            };

            // Encode frame
            let encoded = frame.encode_with_pool(&buffer_pool);

            // Send to WebRTC data channel
            match dc.send(encoded).await {
                Ok(_) => {
                    if crate::logger::is_verbose_logging() {
                        debug!(
                            "Handler message #{} sent to WebRTC successfully (channel: {}, conversation_id: {})",
                            message_count, channel_id_for_outbound, conversation_id_for_outbound
                        );
                    }
                }
                Err(e) => {
                    error!(
                        "Failed to send handler message #{} to WebRTC: {} (channel: {}, conversation_id: {})",
                        message_count, e, channel_id_for_outbound, conversation_id_for_outbound
                    );
                    break;
                }
            }
        }

        info!(
            "Handler outbound task ended (total messages: {}, total bytes: {}, channel: {}, conversation_id: {})",
            message_count, total_bytes, channel_id_for_outbound, conversation_id_for_outbound
        );

        // Notify that connection closed
        conn_closed_tx.send((conn_no, channel_id_for_outbound)).ok();
    });

    // Task 2: WebRTC → Handler (inbound)
    // This is already wired through handler_senders in frame_handling.rs
    debug!(
        "Handler inbound path ready (conn_no: {}, channel: {}, conversation_id: {})",
        conn_no, channel.channel_id, channel.conversation_id
    );

    // Spawn cleanup task that waits for handler completion (RAII)
    let protocol_for_cleanup = protocol_name.clone();
    let handler_senders = channel.handler_senders.clone();
    let channel_id_for_cleanup = channel.channel_id.clone();
    let conversation_id_for_cleanup = channel.conversation_id.clone();
    let cleanup_handle = tokio::spawn(async move {
        // Wait for handler to complete
        let _ = handler_task.await;
        let _ = outbound_task.await;

        // Cleanup: Remove handler sender
        handler_senders.remove(&conn_no);

        info!(
            "Channel-based handler session ended for protocol: {} (channel: {}, conversation_id: {})",
            protocol_for_cleanup, channel_id_for_cleanup, conversation_id_for_cleanup
        );
    });

    // Spawn monitor task to track channel-based handler cleanup task completion
    // This ensures both handler_task and outbound_task are tracked
    let cleanup_completion_tx = Arc::clone(&spawned_task_completion_tx);
    let cleanup_monitor_channel_id = channel.channel_id.clone();
    let cleanup_monitor_conversation_id = channel.conversation_id.clone();
    tokio::spawn(async move {
        match cleanup_handle.await {
            Ok(()) => {
                if unlikely!(crate::logger::is_verbose_logging()) {
                    debug!("Channel-based handler cleanup task completed normally (channel: {}, conversation_id: {})", cleanup_monitor_channel_id, cleanup_monitor_conversation_id);
                }
            }
            Err(e) => {
                tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections", operation = "cleanup", outcome = if e.is_cancelled() { "cancelled" } else { "failed" }, "Handler cleanup task ended abnormally");
            }
        }
        let _ = cleanup_completion_tx.send(());
    });

    // Return immediately to allow ConnectionOpened to be sent
    debug!(
        "Handler spawned successfully for protocol: {}, conn_no: {} (channel: {}, conversation_id: {})",
        protocol_name, conn_no, channel.channel_id, channel.conversation_id
    );
    Ok(())
}

#[cfg(test)]
mod terminal_batch_tests {
    use super::*;

    #[test]
    fn full_terminal_frame_and_next_frame_stay_in_separate_vault_messages() {
        // Given one maximum-size binary terminal frame followed by another frame.
        let (tx, mut rx) = mpsc::channel(2);
        let first = vec![0x20; guacr_protocol::MAX_SAFE_PAYLOAD_SIZE];
        tx.try_send(Bytes::from_static(b"\x20nextdata")).unwrap();
        let mut pending = None;

        // When the first frame fills the batch, then the next frame remains queued.
        let batch = drain_terminal_batch(Bytes::from(first), &mut rx, &mut pending);
        assert_eq!(batch.len(), guacr_protocol::MAX_SAFE_PAYLOAD_SIZE);
        assert!(batch.len() + guacr_protocol::FRAME_PROTOCOL_OVERHEAD <= (16 * 1024 - 17) * 2);
        assert!(pending.is_none());
        assert_eq!(rx.try_recv().unwrap(), Bytes::from_static(b"\x20nextdata"));
    }

    #[test]
    fn near_full_terminal_batch_defers_next_frame_without_losing_it() {
        // Given two terminal frames that fit the old budget but exceed the Vault budget together.
        let (tx, mut rx) = mpsc::channel(2);
        let first = Bytes::from(vec![0x20; guacr_protocol::MAX_SAFE_PAYLOAD_SIZE - 8]);
        let second = Bytes::from(vec![0x20; 16]);
        tx.try_send(second.clone()).unwrap();
        let mut pending = None;

        // When batched, then both ordered messages remain within Vault's frame limit.
        let batch = drain_terminal_batch(first.clone(), &mut rx, &mut pending);
        assert_eq!(batch, first);
        assert!(batch.len() + guacr_protocol::FRAME_PROTOCOL_OVERHEAD <= (16 * 1024 - 17) * 2);
        assert_eq!(pending.as_ref(), Some(&second));
        let next = drain_terminal_batch(pending.take().unwrap(), &mut rx, &mut pending);
        assert_eq!(next, second);
    }
}

#[cfg(test)]
#[path = "../tests/handler_lifecycle_tests.rs"]
mod handler_lifecycle_tests;
