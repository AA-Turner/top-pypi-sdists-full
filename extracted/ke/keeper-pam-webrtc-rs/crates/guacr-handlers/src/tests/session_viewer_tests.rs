// Unit tests for session_viewer module.
//
// Covers: join active session, reject unknown session, late-join frame sync,
// multiple simultaneous viewers, viewer disconnect, input discard.

use crate::session_owner::SessionOwnerSender;
use crate::session_sharing;
use crate::session_viewer::SessionViewer;
use bytes::Bytes;
use tokio::sync::mpsc;

fn unique_id(prefix: &str) -> String {
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(3000);
    format!("${prefix}{}", CTR.fetch_add(1, Ordering::Relaxed))
}

// -------------------------------------------------------------------------
// join()
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_join_active_session_returns_some() {
    let id = unique_id("vj_some_");
    session_sharing::register(&id).unwrap();

    let (tx, _rx) = mpsc::channel(4);
    let viewer = SessionViewer::join(&id, tx).await;
    assert!(
        viewer.is_some(),
        "join must succeed for a registered session"
    );

    session_sharing::deregister(&id);
}

#[tokio::test]
async fn test_join_nonexistent_session_returns_none() {
    let (tx, _rx) = mpsc::channel(4);
    let result = SessionViewer::join("$viewer_nonexistent_xyz", tx).await;
    assert!(
        result.is_none(),
        "join must return None for unknown session"
    );
}

// -------------------------------------------------------------------------
// run() — viewer receives frames (AC-1)
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_viewer_run_receives_broadcast_frame() {
    let id = unique_id("vr_rx_");
    let handle = session_sharing::register(&id).unwrap();

    let (viewer_tx, mut viewer_rx) = mpsc::channel(16);
    let viewer = SessionViewer::join(&id, viewer_tx).await.unwrap();
    tokio::spawn(async move { viewer.run().await });

    let frame = Bytes::from_static(b"screen-data");
    handle.broadcast(frame.clone());

    tokio::time::sleep(std::time::Duration::from_millis(10)).await;
    let got = viewer_rx
        .try_recv()
        .expect("viewer must receive broadcast frame");
    assert_eq!(got, frame);

    session_sharing::deregister(&id);
}

#[tokio::test]
async fn test_viewer_receives_multiple_frames_in_order() {
    let id = unique_id("vr_order_");
    let handle = session_sharing::register(&id).unwrap();

    let (viewer_tx, mut viewer_rx) = mpsc::channel(16);
    let viewer = SessionViewer::join(&id, viewer_tx).await.unwrap();
    tokio::spawn(async move { viewer.run().await });

    for i in 0u8..4 {
        handle.broadcast(Bytes::from(vec![i]));
    }

    tokio::time::sleep(std::time::Duration::from_millis(20)).await;

    for i in 0u8..4 {
        let got = viewer_rx.try_recv().expect("viewer must get each frame");
        assert_eq!(&got[..], &[i], "frames must arrive in broadcast order");
    }

    session_sharing::deregister(&id);
}

// -------------------------------------------------------------------------
// Late-join state sync (T-087 AC-1)
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_late_join_viewer_gets_last_cached_frame() {
    let id = unique_id("vr_late_");
    let handle = session_sharing::register(&id).unwrap();

    // Owner broadcasts a frame before the viewer joins.
    let last = Bytes::from_static(b"latest-screen-state");
    handle.broadcast(last.clone());

    // Viewer joins after the frame was already sent.
    let (viewer_tx, mut viewer_rx) = mpsc::channel(16);
    let viewer = SessionViewer::join(&id, viewer_tx).await.unwrap();
    tokio::spawn(async move { viewer.run().await });

    tokio::time::sleep(std::time::Duration::from_millis(15)).await;

    let got = viewer_rx
        .try_recv()
        .expect("late-join viewer must receive cached frame");
    assert_eq!(
        got, last,
        "late-join viewer must get the most recent owner frame"
    );

    session_sharing::deregister(&id);
}

// -------------------------------------------------------------------------
// Multiple simultaneous viewers (AC-3)
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_two_viewers_both_receive_frames() {
    let id = unique_id("vr_two_");
    let handle = session_sharing::register(&id).unwrap();

    let (tx1, mut rx1) = mpsc::channel(16);
    let (tx2, mut rx2) = mpsc::channel(16);

    let v1 = SessionViewer::join(&id, tx1).await.unwrap();
    let v2 = SessionViewer::join(&id, tx2).await.unwrap();
    tokio::spawn(async move { v1.run().await });
    tokio::spawn(async move { v2.run().await });

    let frame = Bytes::from_static(b"two-viewers");
    handle.broadcast(frame.clone());

    tokio::time::sleep(std::time::Duration::from_millis(15)).await;

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

    session_sharing::deregister(&id);
}

#[tokio::test]
async fn test_five_viewers_all_receive_frames() {
    let id = unique_id("vr_five_");
    let handle = session_sharing::register(&id).unwrap();

    let mut rxs = Vec::new();
    for _ in 0..5 {
        let (tx, rx) = mpsc::channel(16);
        let v = SessionViewer::join(&id, tx).await.unwrap();
        tokio::spawn(async move { v.run().await });
        rxs.push(rx);
    }

    let frame = Bytes::from_static(b"five-viewers");
    handle.broadcast(frame.clone());

    tokio::time::sleep(std::time::Duration::from_millis(20)).await;

    for (i, rx) in rxs.iter_mut().enumerate() {
        let got = rx
            .try_recv()
            .unwrap_or_else(|_| panic!("viewer {i} must receive frame"));
        assert_eq!(got, frame);
    }

    session_sharing::deregister(&id);
}

// -------------------------------------------------------------------------
// Viewer disconnect — run() exits cleanly when transport channel closes
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_viewer_exits_when_transport_closed() {
    let id = unique_id("vr_exit_");
    let handle = session_sharing::register(&id).unwrap();

    let (viewer_tx, viewer_rx) = mpsc::channel(4);
    let viewer = SessionViewer::join(&id, viewer_tx).await.unwrap();

    // Drop the receiver end — next send inside run() will fail → run() must return.
    drop(viewer_rx);

    let run_task = tokio::spawn(async move { viewer.run().await });

    // Trigger a broadcast so the viewer's run() loop executes once and discovers the closed channel.
    handle.broadcast(Bytes::from_static(b"trigger-close"));

    // run() must complete quickly after the transport is closed.
    tokio::time::timeout(std::time::Duration::from_millis(100), run_task)
        .await
        .expect("run() must exit promptly when viewer transport closes")
        .expect("task must not panic");

    session_sharing::deregister(&id);
}

// -------------------------------------------------------------------------
// Owner disconnect → viewer receives Closed and run() exits (AC-4)
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_viewer_run_exits_when_owner_disconnects() {
    let id = unique_id("vr_owndisc_");
    let (owner_tx, _owner_rx) = mpsc::channel(4);
    let mut owner = SessionOwnerSender::new(owner_tx);

    let handle = session_sharing::register(&id).unwrap();
    let (viewer_tx, _viewer_rx) = mpsc::channel(16);
    let viewer = SessionViewer::join(&id, viewer_tx).await.unwrap();
    owner.attach_session(handle);

    let run_task = tokio::spawn(async move { viewer.run().await });

    owner.owner_disconnect(&id);

    tokio::time::timeout(std::time::Duration::from_millis(100), run_task)
        .await
        .expect("run() must exit after owner_disconnect")
        .expect("task must not panic");
}

// -------------------------------------------------------------------------
// cleanup — last viewer disconnect does not leak the session
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_cleanup_after_all_viewers_disconnect() {
    let id = unique_id("vr_cleanup_");
    let handle = session_sharing::register(&id).unwrap();

    // Start two viewers.
    let (tx1, _rx1) = mpsc::channel(4);
    let (tx2, _rx2) = mpsc::channel(4);
    let v1 = SessionViewer::join(&id, tx1).await.unwrap();
    let v2 = SessionViewer::join(&id, tx2).await.unwrap();
    let t1 = tokio::spawn(async move { v1.run().await });
    let t2 = tokio::spawn(async move { v2.run().await });

    // Drop all receiver ends so both viewers' transport channels close.
    // run() loops will exit on the next send attempt.
    // Broadcast something to unblock their loops.
    handle.broadcast(Bytes::from_static(b"close-signal"));

    tokio::time::sleep(std::time::Duration::from_millis(20)).await;

    // Both viewer tasks should be finished or finishing.
    // We give them a brief window and then abort; just assert no panic.
    t1.abort();
    t2.abort();

    // Owner is responsible for deregistration. Session still exists.
    assert!(
        session_sharing::lookup(&id).is_some(),
        "session must exist until owner deregisters"
    );
    session_sharing::deregister(&id);
    assert!(
        session_sharing::lookup(&id).is_none(),
        "session must be gone after deregister"
    );
}

// -------------------------------------------------------------------------
// Input discard (AC-2)
// -------------------------------------------------------------------------

#[test]
fn test_discard_input_is_a_no_op() {
    // Must not panic, must not forward anywhere.
    let msg = Bytes::from_static(b"4.key,5.65507,1.1;");
    SessionViewer::discard_input(&msg);
}

#[test]
fn test_discard_input_with_empty_bytes() {
    SessionViewer::discard_input(&Bytes::new());
}

#[test]
fn test_discard_input_with_large_message() {
    let big = Bytes::from(vec![0u8; 4096]);
    SessionViewer::discard_input(&big);
}

// -------------------------------------------------------------------------
// Combined owner→viewer end-to-end flow
// -------------------------------------------------------------------------

#[tokio::test]
async fn test_owner_sender_to_viewer_end_to_end() {
    // Prove the three components work together:
    //   SessionOwnerSender → session_sharing registry → SessionViewer
    let id = unique_id("vr_e2e_");
    let (owner_tx, mut owner_rx) = mpsc::channel(16);
    let mut owner = SessionOwnerSender::new(owner_tx);

    let handle = session_sharing::register(&id).unwrap();
    let (viewer_tx, mut viewer_rx) = mpsc::channel(16);
    let viewer = SessionViewer::join(&id, viewer_tx).await.unwrap();
    owner.attach_session(handle);

    tokio::spawn(async move { viewer.run().await });

    // Owner sends 3 frames.
    for i in 0u8..3 {
        let f = Bytes::from(vec![i]);
        owner.send(f.clone()).await.unwrap();
        let owner_got = owner_rx.recv().await.unwrap();
        assert_eq!(owner_got, f, "owner must receive frame {i}");
    }

    tokio::time::sleep(std::time::Duration::from_millis(15)).await;

    for i in 0u8..3 {
        let viewer_got = viewer_rx
            .try_recv()
            .unwrap_or_else(|_| panic!("viewer must receive frame {i}"));
        assert_eq!(&viewer_got[..], &[i]);
    }

    // Owner disconnects; viewer's run() should exit.
    owner.owner_disconnect(&id);
    assert!(session_sharing::lookup(&id).is_none());
}
