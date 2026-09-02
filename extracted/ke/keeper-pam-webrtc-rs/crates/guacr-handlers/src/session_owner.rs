// Session owner channel for multi-viewer session sharing (T-068, T-069)
//
// The SessionOwnerSender wraps a Guacamole `to_client` sender and an optional
// session broadcast handle. When the owner's protocol handler sends outbound
// instructions (screen frames, cursor updates, sync), they are forwarded to:
//   1. The owner's direct transport channel (existing behavior, AC-1)
//   2. The session's broadcast channel (all connected viewers, AC-2)
//
// When no viewers are connected, the broadcast call is a no-op at near-zero cost
// (checking a receiver count via AtomicUsize, AC-3).
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
    /// AC-3: If no viewers are connected, `broadcast()` returns 0 at near-zero cost
    /// (no allocation, no channel operations).
    pub async fn send(&self, bytes: Bytes) -> Result<(), mpsc::error::SendError<Bytes>> {
        // AC-2: broadcast to viewers FIRST (before the owner send so viewers
        // can't fall behind if the owner is slow).
        if let Some(ref handle) = self.session {
            // broadcast() returns number of receivers that got the frame.
            // Returns 0 when no viewers are connected (AC-3: near-zero overhead).
            let _ = handle.broadcast(bytes.clone());
        }

        // AC-1: send to owner's direct transport channel.
        self.to_client.send(bytes).await
    }

    /// Non-blocking send. Broadcasts to viewers then attempts to deliver to the
    /// owner's transport channel without waiting. Returns Err if the channel is
    /// full. Callers that can tolerate a dropped frame (e.g. high-rate terminal
    /// output where the next frame will supersede this one) should use this
    /// instead of `send` to prevent the select! loop from stalling.
    pub fn try_send(&self, bytes: Bytes) -> Result<(), mpsc::error::TrySendError<Bytes>> {
        if let Some(ref handle) = self.session {
            let _ = handle.broadcast(bytes.clone());
        }
        self.to_client.try_send(bytes)
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
    /// AC-3: No resources leak — the SessionHandle (and its broadcast channel)
    ///        is dropped when this method completes and all viewer receivers
    ///        will receive RecvError::Closed.
    pub fn owner_disconnect(&mut self, session_id: &str) {
        // AC-1: Send disconnect to all viewers.
        if let Some(ref handle) = self.session {
            // Guacamole disconnect instruction.
            let disconnect = bytes::Bytes::from_static(b"10.disconnect;");
            let _ = handle.broadcast(disconnect);
        }
        // AC-2: Remove from registry.
        crate::session_sharing::deregister(session_id);
        // AC-3: Drop our reference to the handle (broadcast channel closes when
        // all senders are dropped; viewers get RecvError::Closed).
        self.session = None;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::session_sharing;

    // AC-2: outbound instructions sent to both owner and broadcast.
    #[tokio::test]
    async fn test_send_reaches_owner_and_viewer() {
        let (owner_tx, mut owner_rx) = mpsc::channel(10);
        let sender = SessionOwnerSender::new(owner_tx);

        // Register a session and attach it.
        let id = "$test_owner_broadcast";
        let handle = session_sharing::register(id).unwrap();
        let mut viewer_rx = handle.subscribe();

        let mut sender = sender;
        sender.attach_session(handle);

        // Send an instruction.
        let frame = Bytes::from_static(b"test-frame");
        sender.send(frame.clone()).await.unwrap();

        // AC-1: owner receives it.
        let owner_got = owner_rx.recv().await.unwrap();
        assert_eq!(owner_got, frame);

        // AC-2: viewer receives it.
        let viewer_got = viewer_rx.try_recv().unwrap();
        assert_eq!(viewer_got, frame);

        session_sharing::deregister(id);
    }

    // T-089/T-090: Owner disconnect sends viewer disconnect notification.
    #[tokio::test]
    async fn test_owner_disconnect_notifies_viewers() {
        let (owner_tx, _owner_rx) = mpsc::channel(10);
        let mut sender = SessionOwnerSender::new(owner_tx);

        let id = "$test_owner_disconnect";
        let handle = session_sharing::register(id).unwrap();
        let mut viewer_rx = handle.subscribe();
        sender.attach_session(handle);

        // Owner disconnects.
        sender.owner_disconnect(id);

        // Viewer receives the disconnect instruction (AC-1).
        let notif = viewer_rx
            .try_recv()
            .expect("viewer must receive disconnect notification");
        assert!(
            notif.windows(10).any(|w| w == b"disconnect"),
            "notification must contain 'disconnect'"
        );

        // Session ID removed from registry (AC-2).
        assert!(
            session_sharing::lookup(id).is_none(),
            "session must be deregistered after owner disconnect"
        );
    }

    // T-091: No resource leak after session cleanup.
    #[tokio::test]
    async fn test_no_resource_leak_after_cleanup() {
        let (owner_tx, _owner_rx) = mpsc::channel(10);
        let mut sender = SessionOwnerSender::new(owner_tx);

        let id = "$test_no_leak";
        let handle = session_sharing::register(id).unwrap();
        sender.attach_session(handle);
        sender.owner_disconnect(id);

        // After cleanup: session not found, no panic.
        assert!(
            session_sharing::lookup(id).is_none(),
            "registry must be clean"
        );
        // Viewer count drops to 0 (sender dropped, no open channels).
        assert_eq!(
            sender.viewer_count(),
            0,
            "viewer count must be 0 after cleanup"
        );
    }

    // AC-3: zero viewers means no measurable overhead — send still succeeds.
    #[tokio::test]
    async fn test_send_no_viewers_no_overhead() {
        let (owner_tx, mut owner_rx) = mpsc::channel(10);
        let mut sender = SessionOwnerSender::new(owner_tx);

        // Attach session with no subscribers yet.
        let id = "$test_no_viewers";
        let handle = session_sharing::register(id).unwrap();
        sender.attach_session(handle);

        let frame = Bytes::from_static(b"frame-data");
        sender.send(frame.clone()).await.unwrap();

        let got = owner_rx.recv().await.unwrap();
        assert_eq!(got, frame, "owner must still receive frame when no viewers");
        assert_eq!(sender.viewer_count(), 0, "viewer count must be 0");

        session_sharing::deregister(id);
    }
}
