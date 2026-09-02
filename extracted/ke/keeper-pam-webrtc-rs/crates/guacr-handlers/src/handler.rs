use async_trait::async_trait;
use bytes::Bytes;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;

use crate::error::Result;
use crate::events::EventBasedHandler;
use crate::video::VideoOutput;

/// Health status of a protocol handler
#[derive(Debug, Clone, PartialEq)]
pub enum HealthStatus {
    Healthy,
    Degraded { reason: String },
    Unhealthy { reason: String },
}

/// Statistics for a protocol handler
#[derive(Debug, Clone, Default)]
pub struct HandlerStats {
    pub active_connections: usize,
    pub total_connections: u64,
    pub bytes_sent: u64,
    pub bytes_received: u64,
    pub errors: u64,
}

/// Protocol handler trait
///
/// All remote desktop protocol implementations (SSH, RDP, VNC, Database, RBI)
/// must implement this trait. Handlers receive connection parameters and
/// bidirectional message channels for communicating with the client via WebRTC.
///
/// # Message Format
///
/// Messages are Guacamole protocol instructions in raw bytes format.
/// Use the GuacdParser from keeper-webrtc for parsing and formatting.
///
/// # Example
///
/// ```no_run
/// use guacr_handlers::{ProtocolHandler, Result, HealthStatus, VideoOutput, SessionHooks};
/// use async_trait::async_trait;
/// use std::collections::HashMap;
/// use std::sync::Arc;
/// use tokio::sync::mpsc;
/// use bytes::Bytes;
///
/// struct MyHandler;
///
/// #[async_trait]
/// impl ProtocolHandler for MyHandler {
///     fn name(&self) -> &str {
///         "my-protocol"
///     }
///
///     async fn connect(
///         &self,
///         params: HashMap<String, String>,
///         to_client: mpsc::Sender<Bytes>,
///         from_client: mpsc::Receiver<Bytes>,
///         _video_tx: Option<Arc<dyn VideoOutput>>,
///         _hooks: SessionHooks,
///     ) -> Result<()> {
///         // Implementation here
///         Ok(())
///     }
/// }
/// ```
#[async_trait]
pub trait ProtocolHandler: Send + Sync {
    /// Protocol name (e.g., "ssh", "rdp", "vnc", "mysql", "http")
    ///
    /// This should match the ConversationType string from the WebRTC settings.
    fn name(&self) -> &str;

    /// Connect to the remote host and handle the session
    ///
    /// # Arguments
    ///
    /// * `params` - Connection parameters (hostname, port, username, etc.)
    /// * `to_client` - Channel to send Guacamole protocol messages to client
    /// * `from_client` - Channel to receive Guacamole protocol messages from client
    ///
    /// # Message Format
    ///
    /// Messages are raw bytes containing Guacamole protocol instructions.
    /// Parse with GuacdParser::parse_instruction() from keeper-webrtc crate.
    ///
    /// Common opcodes to handle:
    /// - "key" - Keyboard input
    /// - "mouse" - Mouse movement/clicks
    /// - "clipboard" - Clipboard data
    /// - "size" - Screen size change
    ///
    /// Common opcodes to send:
    /// - "img" - Image data (PNG encoded)
    /// - "sync" - Frame synchronization
    /// - "audio" - Audio data
    /// - "clipboard" - Clipboard data
    ///
    /// # Errors
    ///
    /// Returns an error if connection fails, authentication fails, or the
    /// session encounters an unrecoverable error.
    ///
    /// # Cancellation
    ///
    /// The handler should gracefully exit when from_client channel closes.
    async fn connect(
        &self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        from_client: mpsc::Receiver<Bytes>,
        // `Some` for graphical protocols (RDP, VNC, RBI) when H.264 transport is active.
        // `None` for terminal protocols, guacd sessions, old vault clients, and encoder
        // initialisation failures — the handler falls back to JPEG dirty-rect in those cases.
        video_tx: Option<Arc<dyn VideoOutput>>,
        // Optional gateway hooks. Default (all None) leaves behaviour unchanged.
        // See crates/guacr/docs/THREAT_DETECTION_HOOKS.md.
        hooks: crate::hooks::SessionHooks,
    ) -> Result<()>;

    /// Graceful disconnect (optional, cleanup on drop)
    async fn disconnect(&self) -> Result<()> {
        Ok(())
    }

    /// Health check for this handler
    async fn health_check(&self) -> Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    /// Get handler statistics
    async fn stats(&self) -> Result<HandlerStats> {
        Ok(HandlerStats::default())
    }

    /// Initialize handler with configuration (optional)
    async fn initialize(&self, _config: HashMap<String, String>) -> Result<()> {
        Ok(())
    }

    /// Get as event-based handler if supported
    ///
    /// Returns a reference to the EventBasedHandler trait if this handler
    /// implements it, allowing zero-copy integration with keeper-pam-webrtc-rs.
    /// Returns None if the handler only supports the channel-based interface.
    fn as_event_based(&self) -> Option<&dyn EventBasedHandler> {
        None
    }
}
