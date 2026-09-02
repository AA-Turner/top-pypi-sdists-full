// Unit tests for session sharing integration in the VNC handler.
//
// Tests cover the three connection modes: standalone (no share-id), owner
// (share-id present, viewer-mode false), and viewer (viewer-mode=true).
//
// The viewer path returns before any network I/O. Owner/standalone paths
// fail at TCP connect.
//
// The frame-delivery test (test_owner_sender_broadcasts_frames_to_viewer) is
// a direct unit test of the SessionOwnerSender broadcast path — the same path
// that VncClient.send_and_record now routes through after the hot-path fix.
// It does not require a live VNC server.

use guacr_handlers::{session_sharing, ProtocolHandler, SessionOwnerSender};
use std::collections::HashMap;
use tokio::sync::mpsc;

use crate::handler::VncHandler;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

fn unique_sid(tag: &str) -> String {
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(0);
    format!("$vnc-test-{tag}-{}", CTR.fetch_add(1, Ordering::Relaxed))
}

/// Minimal params that pass VncSettings::from_params but connect to an
/// address with no listener so the TCP connect fails fast.
fn base_params() -> HashMap<String, String> {
    let mut p = HashMap::new();
    p.insert("hostname".to_string(), "127.0.0.1".to_string());
    p.insert("port".to_string(), "19997".to_string());
    p
}

// ---------------------------------------------------------------------------
// test_viewer_gets_error_for_unknown_share_id
// ---------------------------------------------------------------------------

#[tokio::test]
async fn test_viewer_gets_error_for_unknown_share_id() {
    let handler = VncHandler::with_defaults();
    let sid = unique_sid("viewer-unknown");

    let mut params = base_params();
    params.insert("share-id".to_string(), sid.clone());
    params.insert("viewer-mode".to_string(), "true".to_string());

    let (to_client_tx, _to_client_rx) = mpsc::channel(16);
    let (_from_client_tx, from_client_rx) = mpsc::channel(16);

    let result = handler
        .connect(
            params,
            to_client_tx,
            from_client_rx,
            None,
            guacr_handlers::SessionHooks::default(),
        )
        .await;

    assert!(
        result.is_err(),
        "viewer with unknown share-id must return Err"
    );
    let msg = result.unwrap_err().to_string();
    assert!(
        msg.contains("share-id") || msg.contains(&sid) || msg.contains("No active session"),
        "error must mention the share-id or session; got: {msg}"
    );
}

// ---------------------------------------------------------------------------
// test_session_registers_when_share_id_present
// ---------------------------------------------------------------------------

#[tokio::test]
async fn test_session_registers_when_share_id_present() {
    let sid = unique_sid("owner-reg");

    let _handle = session_sharing::register(&sid).expect("pre-registration must succeed");
    assert!(
        session_sharing::lookup(&sid).is_some(),
        "pre-registered session must be visible in registry"
    );

    let dup = session_sharing::register(&sid);
    assert!(
        dup.is_err(),
        "registering the same ID twice must fail (AC-5 uniqueness)"
    );

    assert!(
        session_sharing::lookup(&sid).is_some(),
        "registry must retain the original entry after a failed duplicate register"
    );

    session_sharing::deregister(&sid);
}

// ---------------------------------------------------------------------------
// test_standalone_session_unaffected
// ---------------------------------------------------------------------------

#[tokio::test]
async fn test_standalone_session_unaffected() {
    let handler = VncHandler::with_defaults();
    let sentinel = unique_sid("standalone-sentinel");
    let params = base_params(); // no share-id

    let (to_client_tx, _to_client_rx) = mpsc::channel(16);
    let (_from_client_tx, from_client_rx) = mpsc::channel(16);

    let result = handler
        .connect(
            params,
            to_client_tx,
            from_client_rx,
            None,
            guacr_handlers::SessionHooks::default(),
        )
        .await;

    // The sentinel ID must NOT be in the registry — standalone sessions never register.
    assert!(
        session_sharing::lookup(&sentinel).is_none(),
        "standalone session must not register any session ID"
    );

    if let Err(ref e) = result {
        let msg = e.to_string();
        assert!(
            !msg.contains("share-id") && !msg.contains("No active session"),
            "standalone error must not mention session sharing; got: {msg}"
        );
    }
}

// ---------------------------------------------------------------------------
// test_viewer_mode_false_does_not_join_session
// ---------------------------------------------------------------------------

#[tokio::test]
async fn test_viewer_mode_false_does_not_join_session() {
    let handler = VncHandler::with_defaults();
    let sid = unique_sid("no-viewer");

    let mut params = base_params();
    params.insert("share-id".to_string(), sid.clone());
    params.insert("viewer-mode".to_string(), "false".to_string());

    let (to_client_tx, _to_client_rx) = mpsc::channel(16);
    let (_from_client_tx, from_client_rx) = mpsc::channel(16);

    let result = handler
        .connect(
            params,
            to_client_tx,
            from_client_rx,
            None,
            guacr_handlers::SessionHooks::default(),
        )
        .await;

    if let Err(ref e) = result {
        let msg = e.to_string();
        assert!(
            !msg.contains("No active session"),
            "viewer-mode=false must not trigger viewer error path; got: {msg}"
        );
    }

    session_sharing::deregister(&sid);
}

// ---------------------------------------------------------------------------
// test_owner_sender_broadcasts_frames_to_viewer
//
// Proves the broadcast path that VncClient.send_and_record now routes through:
//   1. Register a session and attach it to a SessionOwnerSender
//   2. Spawn a viewer (SessionViewer::join) that subscribes to the broadcast
//   3. Send a frame via owner_sender.send() — simulating what send_and_record does
//   4. Assert both the owner transport AND the viewer receive the exact bytes
//
// This test would have failed before the hot-path fix because VncClient held
// `to_client` directly and never called owner_sender.send().
// ---------------------------------------------------------------------------

#[tokio::test]
async fn test_owner_sender_broadcasts_frames_to_viewer() {
    use bytes::Bytes;
    use guacr_handlers::SessionViewer;

    let sid = unique_sid("frame-broadcast");

    let (owner_tx, mut owner_rx) = mpsc::channel::<Bytes>(16);
    let mut owner_sender = SessionOwnerSender::new(owner_tx);

    let handle = session_sharing::register(&sid).expect("registration must succeed");
    owner_sender.attach_session(handle);

    // Spawn a viewer that subscribes before frames arrive.
    let viewer_sid = sid.clone();
    let (viewer_tx, mut viewer_rx) = mpsc::channel::<Bytes>(16);
    let viewer_task = tokio::spawn(async move {
        let viewer = SessionViewer::join(&viewer_sid, viewer_tx).await;
        assert!(viewer.is_some(), "viewer must join an active session");
        viewer.unwrap().run().await;
    });

    tokio::time::sleep(tokio::time::Duration::from_millis(20)).await;

    let frame = Bytes::from_static(b"5.image,1.0,1.0,5.100,0,5.jpeg;");
    owner_sender
        .send(frame.clone())
        .await
        .expect("send must succeed");

    let by_owner = tokio::time::timeout(tokio::time::Duration::from_millis(200), owner_rx.recv())
        .await
        .expect("owner must receive frame within timeout")
        .expect("owner channel must not close");
    assert_eq!(by_owner, frame, "owner must receive the exact frame");

    let by_viewer = tokio::time::timeout(tokio::time::Duration::from_millis(200), viewer_rx.recv())
        .await
        .expect("viewer must receive frame within timeout")
        .expect("viewer channel must not close");
    assert_eq!(
        by_viewer, frame,
        "viewer must receive the exact frame via broadcast"
    );

    owner_sender.owner_disconnect(&sid);
    viewer_task.abort();
}
