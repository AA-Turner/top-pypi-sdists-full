// Session hooks injected at ProtocolHandler::connect() time.
//
// See crates/guacr/docs/THREAT_DETECTION_HOOKS.md for the full design.
//
// All fields are None by default — passing SessionHooks::default() leaves
// existing handler behaviour completely unchanged.

use bytes::Bytes;
use std::sync::Arc;
use tokio::sync::mpsc;

/// Receives raw outbound bytes from a guacr handler session.
///
/// Called synchronously before each frame is sent to the client.
/// Implementations MUST NOT block — use a channel internally if work
/// is needed (e.g. writing to FrameBus).
pub trait FrameTap: Send + Sync {
    /// Called for every chunk of bytes the handler produces for the client.
    /// `bytes` are raw Guacamole wire-format or binary protocol bytes.
    fn on_frame(&self, bytes: &Bytes);
}

/// Signals sent from the gateway's threat consumer back to a guacr handler.
///
/// Only delivered when `threat-detection.mode=proactive` is set in params
/// (i.e. when `SessionHooks::threat_rx` is `Some`).
#[derive(Debug, Clone)]
pub enum ThreatSignal {
    /// Terminate the session immediately. guacr sends a clean disconnect
    /// instruction and returns from connect().
    Terminate { reason: String },

    /// Block the next user-initiated action pending approval.
    /// guacr buffers the triggering input and waits for Allow or Deny.
    HoldForApproval { context: String },

    /// Release a previously held action. Forwarded to the remote host.
    Allow,

    /// Drop a previously held action. Not forwarded; user sees no-op.
    Deny { reason: String },
}

pub type ThreatSignalTx = mpsc::Sender<ThreatSignal>;
pub type ThreatSignalRx = mpsc::Receiver<ThreatSignal>;

/// Optional gateway hooks injected at session start.
///
/// All fields are None — handlers run unchanged when passed the default.
#[derive(Default)]
pub struct SessionHooks {
    /// Receives raw outbound frames from the handler.
    /// Gateway implements FrameTap; guacr calls it before sending to client.
    pub frame_tap: Option<Arc<dyn FrameTap>>,

    /// Receives threat signals from the gateway's AI consumer.
    /// None = non-blocking mode (default).
    /// Some = guacr checks at user-action boundaries (proactive mode).
    pub threat_rx: Option<ThreatSignalRx>,
}

impl std::fmt::Debug for SessionHooks {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("SessionHooks")
            .field("frame_tap", &self.frame_tap.is_some())
            .field("threat_rx", &self.threat_rx.is_some())
            .finish()
    }
}
