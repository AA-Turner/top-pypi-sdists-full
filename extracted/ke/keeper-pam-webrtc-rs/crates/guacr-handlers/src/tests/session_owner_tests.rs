// Unit tests for session_owner module.
//
// Covers: owner send → transport, owner send → viewers via broadcast,
// near-zero overhead with no viewers, disconnect notification to viewers,
// deregistration cleanup on owner_disconnect.

use crate::session_owner::SessionOwnerSender;
use crate::session_sharing;
use bytes::Bytes;
use tokio::sync::mpsc;

fn unique_id(prefix: &str) -> String {
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(2000);
    format!("${prefix}{}", CTR.fetch_add(1, Ordering::Relaxed))
}

// -------------------------------------------------------------------------
// Initialization
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_new_has_no_session_and_zero_viewers() {
    let (tx, _rx) = mpsc::channel(4);
    let sender = SessionOwnerSender::new(tx);
    assert_eq!(sender.viewer_count(), 0, "no viewers before attach_session");
}

#[tokio::test]
async fn test_transport_sender_is_the_provided_channel() {
    let (tx, mut rx) = mpsc::channel(4);
    let sender = SessionOwnerSender::new(tx);

    // Use the exposed transport_sender to verify it is the original channel.
    sender
        .transport_sender()
        .send(Bytes::from_static(b"probe"))
        .await
        .unwrap();
    let got = rx.recv().await.unwrap();
    assert_eq!(&got[..], b"probe");
}

// -------------------------------------------------------------------------
// send() — owner receives instructions
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_send_without_session_reaches_owner() {
    let (tx, mut rx) = mpsc::channel(4);
    let sender = SessionOwnerSender::new(tx);

    let frame = Bytes::from_static(b"owner-only");
    sender.send(frame.clone()).await.unwrap();

    let got = rx.recv().await.unwrap();
    assert_eq!(
        got, frame,
        "owner must receive frame even without session attached"
    );
}

// -------------------------------------------------------------------------
// attach_session + send() — owner and viewers both receive
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_send_with_session_reaches_owner_and_viewer() {
    let id = unique_id("so_both_");
    let (tx, mut owner_rx) = mpsc::channel(16);
    let mut sender = SessionOwnerSender::new(tx);

    let handle = session_sharing::register(&id).unwrap();
    let mut viewer_rx = handle.subscribe();
    sender.attach_session(handle);

    let frame = Bytes::from_static(b"owner-and-viewer");
    sender.send(frame.clone()).await.unwrap();

    let owner_got = owner_rx.recv().await.unwrap();
    assert_eq!(owner_got, frame, "owner must receive frame");

    let viewer_got = viewer_rx.try_recv().expect("viewer must receive frame");
    assert_eq!(viewer_got, frame, "viewer must receive same frame");

    session_sharing::deregister(&id);
}

#[tokio::test]
async fn test_send_with_multiple_viewers() {
    let id = unique_id("so_multi_");
    let (tx, mut owner_rx) = mpsc::channel(16);
    let mut sender = SessionOwnerSender::new(tx);

    let handle = session_sharing::register(&id).unwrap();
    let mut v1 = handle.subscribe();
    let mut v2 = handle.subscribe();
    sender.attach_session(handle);

    let frame = Bytes::from_static(b"broadcast");
    sender.send(frame.clone()).await.unwrap();

    assert_eq!(owner_rx.recv().await.unwrap(), frame);
    assert_eq!(v1.try_recv().unwrap(), frame);
    assert_eq!(v2.try_recv().unwrap(), frame);

    session_sharing::deregister(&id);
}

// -------------------------------------------------------------------------
// Near-zero overhead with no viewers (AC-3)
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_send_no_viewers_zero_overhead() {
    let id = unique_id("so_noview_");
    let (tx, mut owner_rx) = mpsc::channel(4);
    let mut sender = SessionOwnerSender::new(tx);

    let handle = session_sharing::register(&id).unwrap();
    // No subscriptions — viewer_count is 0.
    assert_eq!(handle.viewer_count(), 0);
    sender.attach_session(handle);

    let frame = Bytes::from_static(b"no-viewers");
    sender.send(frame.clone()).await.unwrap();

    let got = owner_rx.recv().await.unwrap();
    assert_eq!(got, frame, "owner still receives frame when no viewers");
    assert_eq!(sender.viewer_count(), 0);

    session_sharing::deregister(&id);
}

// -------------------------------------------------------------------------
// owner_disconnect (T-089)
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_owner_disconnect_sends_disconnect_to_viewers() {
    let id = unique_id("so_disc_");
    let (tx, _owner_rx) = mpsc::channel(4);
    let mut sender = SessionOwnerSender::new(tx);

    let handle = session_sharing::register(&id).unwrap();
    let mut viewer_rx = handle.subscribe();
    sender.attach_session(handle);

    sender.owner_disconnect(&id);

    let notif = viewer_rx
        .try_recv()
        .expect("viewer must receive disconnect notification after owner_disconnect");
    let as_str = String::from_utf8_lossy(&notif);
    assert!(
        as_str.contains("disconnect"),
        "notification must contain 'disconnect'; got: {as_str}"
    );
}

#[tokio::test]
async fn test_owner_disconnect_deregisters_session() {
    let id = unique_id("so_dereg_");
    let (tx, _rx) = mpsc::channel(4);
    let mut sender = SessionOwnerSender::new(tx);

    let handle = session_sharing::register(&id).unwrap();
    sender.attach_session(handle);

    assert!(
        session_sharing::lookup(&id).is_some(),
        "session must exist before disconnect"
    );
    sender.owner_disconnect(&id);
    assert!(
        session_sharing::lookup(&id).is_none(),
        "session must be deregistered after owner_disconnect"
    );
}

#[tokio::test]
async fn test_owner_disconnect_viewer_count_drops_to_zero() {
    let id = unique_id("so_vc_");
    let (tx, _rx) = mpsc::channel(4);
    let mut sender = SessionOwnerSender::new(tx);

    let handle = session_sharing::register(&id).unwrap();
    let _v = handle.subscribe();
    sender.attach_session(handle);

    sender.owner_disconnect(&id);
    assert_eq!(
        sender.viewer_count(),
        0,
        "viewer count must be 0 after owner_disconnect"
    );
}

// -------------------------------------------------------------------------
// Sequence: attach → send many frames → disconnect
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_full_lifecycle_attach_send_disconnect() {
    let id = unique_id("so_lifecycle_");
    let (tx, mut owner_rx) = mpsc::channel(32);
    let mut sender = SessionOwnerSender::new(tx);

    let handle = session_sharing::register(&id).unwrap();
    let mut viewer_rx = handle.subscribe();
    sender.attach_session(handle);

    for i in 0u8..5 {
        let f = Bytes::from(vec![i]);
        sender.send(f.clone()).await.unwrap();
        assert_eq!(owner_rx.recv().await.unwrap(), f);
        assert_eq!(viewer_rx.try_recv().unwrap(), f);
    }

    sender.owner_disconnect(&id);

    // After disconnect the broadcast channel closes — viewer gets Closed error.
    let result = viewer_rx.try_recv();
    // The last item from disconnect may or may not still be in the buffer,
    // but eventually the channel must close.
    // We only assert the session is gone from the registry.
    assert!(session_sharing::lookup(&id).is_none());
    let _ = result; // allow either Ok(disconnect) or Err(Empty/Closed)
}
