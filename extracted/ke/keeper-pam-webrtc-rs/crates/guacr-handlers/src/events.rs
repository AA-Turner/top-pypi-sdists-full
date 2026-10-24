// Event-based protocol handler interface
// Zero-copy integration with keeper-pam-webrtc-rs

use bytes::Bytes;
use std::future::Future;
use std::sync::Arc;

use crate::video::VideoOutput;

/// Protocol handler events (zero-copy)
///
/// Events are sent from protocol handlers to the WebRTC layer.
/// Uses Bytes for zero-copy data transfer.
#[derive(Debug, Clone)]
pub enum HandlerEvent {
    /// Send instruction to client (zero-copy Bytes)
    Instruction(Bytes),

    /// Error occurred - terminate connection
    Error { message: String, code: Option<i32> },

    /// Disconnect request
    Disconnect { reason: String },

    /// Threat detected - terminate session
    ThreatDetected { level: String, description: String },

    /// Connection ready
    Ready { connection_id: String },

    /// Size change (backwards compatibility, not needed with threat detection)
    Size { width: u32, height: u32 },
}

/// Event callback trait for WebRTC integration
///
/// This allows keeper-pam-webrtc-rs to register callbacks for events
/// instead of parsing all instructions. Only critical events (error,
/// disconnect, threat) need to be handled by WebRTC layer.
#[async_trait::async_trait]
pub trait EventCallback: Send + Sync {
    /// Handle a protocol handler event
    fn on_event(&self, event: HandlerEvent);

    /// Send instruction to client (zero-copy with backpressure)
    ///
    /// This is the hot path - Bytes is reference-counted, so no copying happens.
    /// The WebRTC layer should send the Bytes directly to the client.
    ///
    /// Async to allow proper backpressure - if WebRTC is backed up, this will await
    /// rather than dropping frames (critical for RDP/VNC/database protocols).
    ///
    /// # Returns
    /// * `Ok(())` - Instruction sent successfully
    /// * `Err(HandlerError)` - Failed to send (channel closed, backpressure timeout, etc.)
    async fn send_instruction(&self, instruction: Bytes) -> Result<(), crate::error::HandlerError>;
}

/// Protocol handler with event-based interface
///
/// This is an alternative to the channel-based interface that allows
/// zero-copy integration with keeper-pam-webrtc-rs.
///
/// For bidirectional communication, the handler receives a channel receiver
/// for client messages (keyboard, mouse, etc.) as a parameter.
#[async_trait::async_trait]
pub trait EventBasedHandler: Send + Sync {
    /// Protocol name
    fn name(&self) -> &str;

    /// Connect with event callback and client message receiver
    ///
    /// # Arguments
    ///
    /// * `params` - Connection parameters (hostname, port, username, etc.)
    /// * `callback` - Callback for sending instructions to client (handler → WebRTC)
    /// * `from_client` - Channel receiver for client messages (WebRTC → handler)
    ///
    /// The handler calls the callback to send instructions to the client (zero-copy).
    /// The handler receives client messages (keyboard, mouse, etc.) from the channel.
    async fn connect_with_events(
        &self,
        params: std::collections::HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: tokio::sync::mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        hooks: crate::hooks::SessionHooks,
    ) -> Result<(), crate::error::HandlerError>;
}

/// Zero-copy instruction sender
///
/// Allows handlers to send instructions directly without copying.
pub struct InstructionSender {
    callback: Arc<dyn EventCallback>,
}

impl InstructionSender {
    pub fn new(callback: Arc<dyn EventCallback>) -> Self {
        Self { callback }
    }

    /// Send instruction (zero-copy with backpressure)
    ///
    /// Bytes is reference-counted, so this is zero-copy.
    /// Async to propagate backpressure from WebRTC layer.
    ///
    /// # Returns
    /// * `Ok(())` - Instruction sent successfully
    /// * `Err(HandlerError)` - Failed to send (channel closed, backpressure timeout, etc.)
    pub async fn send(&self, instruction: Bytes) -> Result<(), crate::error::HandlerError> {
        self.callback.send_instruction(instruction).await
    }

    /// Send error event
    pub fn send_error(&self, message: String, code: Option<i32>) {
        self.callback
            .on_event(HandlerEvent::Error { message, code });
    }

    /// Send disconnect event
    pub fn send_disconnect(&self, reason: String) {
        self.callback.on_event(HandlerEvent::Disconnect { reason });
    }

    /// Send threat detected event
    pub fn send_threat(&self, level: String, description: String) {
        self.callback
            .on_event(HandlerEvent::ThreatDetected { level, description });
    }

    /// Send ready event
    pub fn send_ready(&self, connection_id: String) {
        self.callback
            .on_event(HandlerEvent::Ready { connection_id });
    }

    /// Send size event (backwards compatibility)
    pub fn send_size(&self, width: u32, height: u32) {
        self.callback.on_event(HandlerEvent::Size { width, height });
    }
}

/// Helper function to adapt a channel-based handler to event-based interface
///
/// This eliminates boilerplate code in protocol implementations by providing
/// a common adapter pattern. All protocols that implement both ProtocolHandler
/// and EventBasedHandler can use this helper.
///
/// # Arguments
/// * `connect_fn` - The channel-based connect function to wrap
/// * `params` - Connection parameters
/// * `callback` - Event callback for sending instructions
/// * `from_client` - Channel receiver for client messages
/// * `channel_capacity` - Capacity for the internal forwarding channel (typically 128 or 4096)
///
/// Completion joins the forwarding task: admitted instructions are forwarded
/// before returning. A failed forwarder seals output and gives the producer a
/// bounded interval to finalize before its task is cancelled.
/// # Example
/// ```no_run
/// # use guacr_handlers::{connect_with_event_adapter, EventCallback, HandlerEvent, Result, SessionHooks, VideoOutput};
/// # use std::collections::HashMap;
/// # use std::sync::Arc;
/// # use tokio::sync::mpsc;
/// # use bytes::Bytes;
/// # async fn example(
/// #     params: HashMap<String, String>,
/// #     callback: Arc<dyn EventCallback>,
/// #     from_client: mpsc::Receiver<Bytes>,
/// #     video_tx: Option<Arc<dyn VideoOutput>>,
/// #     hooks: SessionHooks,
/// # ) -> Result<()> {
/// connect_with_event_adapter(
///     |p, tx, rx, vtx, hooks| async move {
///         // Your channel-based connect implementation
///         Ok(())
///     },
///     params,
///     callback,
///     from_client,
///     video_tx,
///     hooks,
///     128,  // channel capacity
/// ).await
/// # }
/// ```
pub async fn connect_with_event_adapter<F, Fut>(
    connect_fn: F,
    params: std::collections::HashMap<String, String>,
    callback: Arc<dyn EventCallback>,
    from_client: tokio::sync::mpsc::Receiver<Bytes>,
    video_tx: Option<Arc<dyn VideoOutput>>,
    hooks: crate::hooks::SessionHooks,
    channel_capacity: usize,
) -> Result<(), crate::error::HandlerError>
where
    F: FnOnce(
        std::collections::HashMap<String, String>,
        tokio::sync::mpsc::Sender<Bytes>,
        tokio::sync::mpsc::Receiver<Bytes>,
        Option<Arc<dyn VideoOutput>>,
        crate::hooks::SessionHooks,
    ) -> Fut,
    Fut: Future<Output = Result<(), crate::error::HandlerError>>,
{
    let finalization_deadline = hooks.handler_finalization_timeout;
    // Create channel for handler → callback forwarding
    let (to_client, mut handler_rx) = tokio::sync::mpsc::channel::<Bytes>(channel_capacity);
    let (finished_tx, finished_rx) = tokio::sync::oneshot::channel();

    let mut forwarder = tokio::task::JoinSet::new();
    forwarder.spawn(async move {
        tokio::pin!(finished_rx);
        let mut finished = false;
        loop {
            let msg = tokio::select! {
                biased;
                _ = &mut finished_rx, if !finished => {
                    finished = true;
                    handler_rx.close();
                    continue;
                }
                msg = handler_rx.recv() => match msg {
                    Some(msg) => msg,
                    None => break,
                },
            };
            callback.send_instruction(msg).await?;
        }
        Ok(())
    });

    let producer = connect_fn(params, to_client, from_client, video_tx, hooks);
    tokio::pin!(producer);
    tokio::select! {
        biased;
        producer_result = &mut producer => {
            let _ = finished_tx.send(());
            let forwarding_result = forwarding_result(forwarder.join_next().await);
            producer_result.and(forwarding_result)
        }
        result = forwarder.join_next() => {
            let forwarding_result = forwarding_result(result);
            if forwarding_result.is_err() {
                // Reject new output and discard queued frames. The producer observes
                // the closed sender and retains the configured deadline for async
                // finalization. Dropping it after expiry is the cancellation backstop.
                match tokio::time::timeout(finalization_deadline, &mut producer).await {
                    Ok(producer_result) => return producer_result.and(forwarding_result),
                    Err(_) => {
                        tracing::error!(target: "guacr_handlers::events", operation = "finalize", outcome = "timed_out", "Handler finalization exceeded deadline");
                        return forwarding_result;
                    }
                }
            }
            producer.await
        }
    }
}

fn forwarding_result(
    result: Option<Result<Result<(), crate::error::HandlerError>, tokio::task::JoinError>>,
) -> Result<(), crate::error::HandlerError> {
    match result {
        Some(Ok(result)) => result,
        Some(Err(_)) | None => Err(crate::error::HandlerError::ChannelError(
            "Instruction forwarding task failed".to_string(),
        )),
    }
}
