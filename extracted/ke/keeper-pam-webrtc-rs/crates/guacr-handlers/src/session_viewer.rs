// Session viewer channel for multi-viewer session sharing (T-080, T-081)
//
// A viewer connection subscribes to the session's broadcast channel and receives
// screen output from the owner session. Viewers are read-only: input from the
// viewer is discarded.
//
// AC-1: A viewer connecting to an active session ID receives screen output.
// AC-2: Input instructions from the viewer are discarded (not forwarded to the handler).
// AC-3: Multiple viewers can subscribe simultaneously.
// AC-4: A slow viewer drops frames rather than causing backpressure to the owner.

use bytes::Bytes;
use log::{info, warn};
use tokio::sync::{broadcast, mpsc};

use crate::session_sharing;

/// A read-only session viewer.
///
/// The viewer subscribes to a session's broadcast channel (via `session_sharing::lookup`)
/// and forwards received frames to its own `to_client` sender. Input from the viewer
/// client is silently discarded (AC-2).
pub struct SessionViewer {
    /// The viewer's transport sender.
    to_client: mpsc::Sender<Bytes>,
    /// Broadcast receiver for the session output.
    rx: broadcast::Receiver<Bytes>,
    /// Session ID this viewer is subscribed to.
    session_id: String,
}

impl SessionViewer {
    /// Subscribe to an active session.
    ///
    /// Returns `None` if the session ID is not found (AC-2 of session-sharing R1:
    /// lookup of nonexistent ID returns "not found").
    ///
    /// T-087 AC-1: If the session has a cached last frame, sends it immediately
    /// so the viewer's display matches the owner's current state.
    pub async fn join(session_id: &str, to_client: mpsc::Sender<Bytes>) -> Option<Self> {
        let handle = session_sharing::lookup(session_id)?;

        // Subscribe BEFORE reading last_frame to avoid a race where a new frame arrives
        // between reading last_frame and subscribing.
        let rx = handle.subscribe();

        // T-087 AC-1: Send the most recent frame immediately so the late-joining
        // viewer's display matches the owner's current display (no blank screen on join).
        if let Some(last) = handle.last_frame() {
            // Best-effort: if the channel is full we still continue.
            let _ = to_client.send(last).await;
        }

        info!(
            "Session viewer joined session {session_id:?} \
             (current viewers: {})",
            handle.viewer_count()
        );
        Some(Self {
            to_client,
            rx,
            session_id: session_id.to_string(),
        })
    }

    /// Run the viewer loop until the session ends or the viewer disconnects.
    ///
    /// AC-1: Receives screen output from the owner and forwards to `to_client`.
    /// AC-4: A lagging viewer gets `RecvError::Lagged` — frames are dropped without
    ///        backpressure to the owner.
    pub async fn run(mut self) {
        loop {
            match self.rx.recv().await {
                Ok(frame) => {
                    // Forward frame to viewer's transport channel.
                    if self.to_client.send(frame).await.is_err() {
                        info!(
                            "Session viewer disconnected (session: {:?})",
                            self.session_id
                        );
                        return;
                    }
                }
                Err(broadcast::error::RecvError::Lagged(n)) => {
                    // AC-4: slow viewer drops frames (no backpressure to owner).
                    warn!(
                        "Session viewer lagging — dropped {n} frames \
                         (session: {:?})",
                        self.session_id
                    );
                }
                Err(broadcast::error::RecvError::Closed) => {
                    // Owner disconnected or session was deregistered.
                    info!("Session ended for viewer (session: {:?})", self.session_id);
                    return;
                }
            }
        }
    }

    /// Discard a viewer input instruction (AC-2).
    ///
    /// Called when the viewer's transport receives an instruction. Viewers are
    /// read-only: no instructions are forwarded to the protocol handler.
    pub fn discard_input(msg: &bytes::Bytes) {
        let _ = msg; // intentionally discarded
                     // Note: in production, log at trace level to avoid log spam.
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::session_sharing;

    // AC-1: viewer receives screen output from owner session.
    #[tokio::test]
    async fn test_viewer_receives_output() {
        let id = "$test_viewer_rx";
        let handle = session_sharing::register(id).unwrap();

        let (viewer_tx, mut viewer_rx) = mpsc::channel(10);
        let viewer = SessionViewer::join(id, viewer_tx)
            .await
            .expect("join must succeed");

        // Spawn viewer loop.
        tokio::spawn(async move { viewer.run().await });

        // Owner broadcasts a frame.
        let frame = Bytes::from_static(b"screen-frame");
        handle.broadcast(frame.clone());

        // Give viewer a moment to process.
        tokio::time::sleep(std::time::Duration::from_millis(10)).await;

        let received = viewer_rx.try_recv().expect("viewer must receive frame");
        assert_eq!(
            received, frame,
            "viewer must receive exact owner output (AC-1)"
        );

        session_sharing::deregister(id);
    }

    // AC-2: input discarded — discard_input is a no-op.
    #[test]
    fn test_discard_input_no_forward() {
        let msg = Bytes::from_static(b"4.key,5.65507,1.1;");
        SessionViewer::discard_input(&msg); // must not panic, not return anything
    }

    // AC-3: multiple viewers subscribe simultaneously.
    #[tokio::test]
    async fn test_multiple_viewers() {
        let id = "$test_multi_viewer";
        let handle = session_sharing::register(id).unwrap();

        let (tx1, mut rx1) = mpsc::channel(10);
        let (tx2, mut rx2) = mpsc::channel(10);
        let v1 = SessionViewer::join(id, tx1).await.unwrap();
        let v2 = SessionViewer::join(id, tx2).await.unwrap();

        tokio::spawn(async move { v1.run().await });
        tokio::spawn(async move { v2.run().await });

        let frame = Bytes::from_static(b"multi-viewer");
        handle.broadcast(frame.clone());

        tokio::time::sleep(std::time::Duration::from_millis(10)).await;

        assert_eq!(
            rx1.try_recv().unwrap(),
            frame,
            "viewer 1 must receive frame"
        );
        assert_eq!(
            rx2.try_recv().unwrap(),
            frame,
            "viewer 2 must receive frame"
        );

        session_sharing::deregister(id);
    }

    // join() returns None for unknown session (AC-2 of session-sharing R1).
    #[tokio::test]
    async fn test_join_unknown_session_returns_none() {
        let (tx, _rx) = mpsc::channel(1);
        let result = SessionViewer::join("$nonexistent_viewer_test", tx).await;
        assert!(
            result.is_none(),
            "join must return None for unknown session"
        );
    }

    // T-087 AC-1: Late-join viewer receives most recent full frame.
    #[tokio::test]
    async fn test_late_join_receives_last_frame() {
        let id = "$test_late_join";
        let handle = session_sharing::register(id).unwrap();

        // Owner broadcasts a frame BEFORE viewer joins.
        let last_frame = Bytes::from_static(b"latest-screen-state");
        handle.broadcast(last_frame.clone());

        // Viewer joins AFTER the frame was broadcast.
        let (viewer_tx, mut viewer_rx) = mpsc::channel(10);
        let viewer = SessionViewer::join(id, viewer_tx).await.unwrap();
        tokio::spawn(async move { viewer.run().await });

        // Give viewer a moment to receive the cached frame.
        tokio::time::sleep(std::time::Duration::from_millis(10)).await;

        // Viewer should have received the cached last frame immediately on join.
        let got = viewer_rx
            .try_recv()
            .expect("late-join viewer must receive cached frame");
        assert_eq!(
            got, last_frame,
            "late-join viewer must get most recent owner frame (AC-1)"
        );

        session_sharing::deregister(id);
    }
}
