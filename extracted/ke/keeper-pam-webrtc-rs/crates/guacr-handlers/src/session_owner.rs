// Session owner channel for multi-viewer session sharing (T-068, T-069)
//
// The SessionOwnerSender wraps a Guacamole `to_client` sender and an optional
// session broadcast handle. When the owner's protocol handler sends outbound
// instructions (screen frames, cursor updates, sync), they are forwarded to:
//   1. The owner's direct transport channel (existing behavior, AC-1)
//   2. The session's broadcast channel (all connected viewers, AC-2)
//
// Display output is cached for late join even when no viewers are subscribed.
//
// Usage:
//   let sender = SessionOwnerSender::new(to_client_tx);
//   // After registering with session registry:
//   let handle = session_sharing::register("$my-session").unwrap();
//   sender.attach_session(handle);
//   // Now every send() also broadcasts to viewers.

use bytes::Bytes;
use tokio::sync::mpsc;

use crate::session_sharing::SessionHandle;

/// An outbound instruction sender that forwards to both the owner's transport
/// channel and the session broadcast channel.
///
/// Implements the owner side of session sharing (T-068, T-069).
pub struct SessionOwnerSender {
    /// Direct channel to the owner's WebRTC/transport layer.
    to_client: mpsc::Sender<Bytes>,
    /// Optional session broadcast handle.
    /// None until attach_session() is called.
    session: Option<SessionHandle>,
}

/// Owner transport credit held through recording and synchronous output acceptance.
pub struct SessionOwnerPermit<'a> {
    permit: mpsc::Permit<'a, Bytes>,
    session: Option<&'a SessionHandle>,
}

impl SessionOwnerPermit<'_> {
    pub fn send(self, bytes: Bytes) {
        if let Some(handle) = self.session {
            let _ = handle.broadcast(bytes.clone());
        }
        self.permit.send(bytes);
    }
}

impl SessionOwnerSender {
    /// Create a new owner sender backed by the given transport channel.
    pub fn new(to_client: mpsc::Sender<Bytes>) -> Self {
        Self {
            to_client,
            session: None,
        }
    }

    /// Attach a session handle. After this call, every send() also broadcasts to viewers.
    pub fn attach_session(&mut self, handle: SessionHandle) {
        self.session = Some(handle);
    }

    /// Send an instruction to the owner and broadcast to all viewers (AC-2).
    ///
    /// A live session caches the display instruction even with no viewers.
    pub async fn send(&self, bytes: Bytes) -> Result<(), mpsc::error::SendError<Bytes>> {
        // AC-2: broadcast to viewers FIRST (before the owner send so viewers
        // can't fall behind if the owner is slow).
        if let Some(ref handle) = self.session {
            // broadcast() returns number of receivers that got the frame.
            // Returns 0 when no viewers are connected or this generation ended.
            let _ = handle.broadcast(bytes.clone());
        }

        // AC-1: send to owner's direct transport channel.
        self.to_client.send(bytes).await
    }

    /// Reserve owner credit without publishing output to viewers or the late-join cache.
    pub fn try_reserve(&self) -> Result<SessionOwnerPermit<'_>, mpsc::error::TrySendError<()>> {
        self.to_client
            .try_reserve()
            .map(|permit| SessionOwnerPermit {
                permit,
                session: self.session.as_ref(),
            })
    }

    /// Non-blocking send; rejected output is neither broadcast nor cached.
    pub fn try_send(&self, bytes: Bytes) -> Result<(), mpsc::error::TrySendError<Bytes>> {
        match self.try_reserve() {
            Ok(permit) => {
                permit.send(bytes);
                Ok(())
            }
            Err(mpsc::error::TrySendError::Full(())) => Err(mpsc::error::TrySendError::Full(bytes)),
            Err(mpsc::error::TrySendError::Closed(())) => {
                Err(mpsc::error::TrySendError::Closed(bytes))
            }
        }
    }

    /// Get a reference to the underlying transport sender.
    pub fn transport_sender(&self) -> &mpsc::Sender<Bytes> {
        &self.to_client
    }

    /// Return the number of currently connected viewers (for metrics).
    pub fn viewer_count(&self) -> usize {
        self.session.as_ref().map_or(0, |h| h.viewer_count())
    }

    /// Called when the owner disconnects (T-089).
    ///
    /// AC-1: Broadcasts a Guacamole disconnect instruction to all viewers.
    /// AC-2: Deregisters the session from the session registry.
    /// AC-3: Explicitly ends this generation, including surviving handle clones.
    /// The disconnect notice is best-effort; blocked viewers exit via cancellation.
    pub fn owner_disconnect(&mut self, session_id: &str) {
        if let Some(handle) = self.session.take() {
            let disconnect = bytes::Bytes::from_static(b"10.disconnect;");
            let _ = handle.broadcast_control(disconnect);
            crate::session_sharing::deregister_owner(session_id, &handle);
        }
    }
}
