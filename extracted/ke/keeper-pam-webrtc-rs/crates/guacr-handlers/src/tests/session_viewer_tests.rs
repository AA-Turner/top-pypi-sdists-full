// Unit tests for session_viewer module.
//
// Covers: join active session, reject unknown session, late-join frame sync,
// multiple simultaneous viewers, viewer disconnect, input discard.

use crate::session_owner::SessionOwnerSender;
use crate::session_sharing;
use crate::session_viewer::SessionViewer;
use bytes::Bytes;
use std::future::Future;
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

    let got = viewer_rx
        .recv()
        .await
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

    for i in 0u8..4 {
        let got = viewer_rx.recv().await.expect("viewer must get each frame");
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

    let got = viewer_rx
        .recv()
        .await
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

    assert_eq!(
        rx1.recv().await.unwrap(),
        frame,
        "viewer 1 must receive frame"
    );
    assert_eq!(
        rx2.recv().await.unwrap(),
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

    for (i, rx) in rxs.iter_mut().enumerate() {
        let got = rx
            .recv()
            .await
            .unwrap_or_else(|| panic!("viewer {i} must receive frame"));
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
    session_sharing::register(&id).unwrap();

    // Start two viewers.
    let (tx1, rx1) = mpsc::channel(4);
    let (tx2, rx2) = mpsc::channel(4);
    let v1 = SessionViewer::join(&id, tx1).await.unwrap();
    let v2 = SessionViewer::join(&id, tx2).await.unwrap();
    let t1 = tokio::spawn(async move { v1.run().await });
    let t2 = tokio::spawn(async move { v2.run().await });

    drop(rx1);
    drop(rx2);
    tokio::time::timeout(std::time::Duration::from_secs(1), t1)
        .await
        .unwrap()
        .unwrap();
    tokio::time::timeout(std::time::Duration::from_secs(1), t2)
        .await
        .unwrap()
        .unwrap();

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

    for i in 0u8..3 {
        let viewer_got = viewer_rx
            .recv()
            .await
            .unwrap_or_else(|| panic!("viewer must receive frame {i}"));
        assert_eq!(&viewer_got[..], &[i]);
    }

    // Owner disconnects; viewer's run() should exit.
    owner.owner_disconnect(&id);
    assert!(session_sharing::lookup(&id).is_none());
}
#[cfg(test)]
mod share_control_tests {
    use crate::share_registry::{get_share_session, remove_share_session, ParticipantStatus};
    use crate::share_viewer::*;
    use base64::{engine::general_purpose::STANDARD as B64, Engine};
    use tokio::sync::mpsc;
    use uuid::Uuid;

    fn unique_id() -> String {
        use std::sync::atomic::{AtomicU64, Ordering};
        static CTR: AtomicU64 = AtomicU64::new(0);
        format!("$test-viewer-{}", CTR.fetch_add(1, Ordering::Relaxed))
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_create() {
        let id = unique_id();
        let (tx, mut rx) = mpsc::channel(8);

        let pt = B64.encode(b"passthrough-data");
        let args = ["Alice", "03", pt.as_str()];
        let handled = handle_owner_share_control(&id, "share_create", &args, &tx).await;
        assert!(handled);

        // Should have sent share_created back
        let msg = rx.try_recv().expect("share_created not sent");
        let instruction = guacr_protocol::GuacamoleParser::parse_instruction(&msg).unwrap();
        assert_eq!(instruction.opcode, "share_created");
        assert_eq!(
            B64.decode(instruction.args[1]).unwrap(),
            b"passthrough-data"
        );

        // Registry should now have Alice as Pending
        let share = get_share_session(&id).expect("share session missing");
        let participants = share.participant_list();
        // owner (Connected) + Alice (Pending)
        assert_eq!(participants.len(), 2);
        let alice = participants
            .iter()
            .find(|p| p.display_name == "Alice")
            .expect("Alice not found");
        assert_eq!(alice.status, ParticipantStatus::Pending);
        assert_eq!(alice.privileges, 0x03);
        assert_eq!(Uuid::parse_str(instruction.args[0]).unwrap(), alice.guid);

        remove_share_session(&id);
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_revoke() {
        let id = unique_id();
        ensure_share_session(&id, "Owner");
        let share = get_share_session(&id).unwrap();
        let guid = share.add_invitation("Bob".into(), 0x01, vec![]);

        let (tx, _rx) = mpsc::channel(8);
        let handled =
            handle_owner_share_control(&id, "share_revoke", &[guid.to_string().as_str()], &tx)
                .await;
        assert!(handled);

        // Bob should be gone
        assert!(share.accept_join(guid).is_err());
        remove_share_session(&id);
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_privilege_change() {
        let id = unique_id();
        ensure_share_session(&id, "Owner");
        let share = get_share_session(&id).unwrap();
        let guid = share.add_invitation("Carol".into(), 0x01, vec![]);

        let (tx, _rx) = mpsc::channel(8);
        let handled = handle_owner_share_control(
            &id,
            "privilege_change",
            &[guid.to_string().as_str(), "07"],
            &tx,
        )
        .await;
        assert!(handled);

        let carol = share
            .participant_list()
            .into_iter()
            .find(|p| p.guid == guid)
            .unwrap();
        assert_eq!(carol.privileges, 0x07);
        remove_share_session(&id);
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_unknown_opcode() {
        let id = unique_id();
        let (tx, _rx) = mpsc::channel(8);
        let handled = handle_owner_share_control(&id, "key", &["65507", "1"], &tx).await;
        assert!(
            !handled,
            "key opcode should not be handled as share control"
        );
    }

    #[tokio::test]
    async fn test_handle_owner_share_control_admin_takeover() {
        let id = unique_id();
        ensure_share_session(&id, "Owner");
        let share = get_share_session(&id).unwrap();
        let owner_guid = share.owner_guid;

        let (tx, _rx) = mpsc::channel(8);
        let handled =
            handle_owner_share_control(&id, "admin_takeover", &["Admin", "07", "01"], &tx).await;
        assert!(handled);

        // Owner should be demoted to view-only
        let owner = share
            .participant_list()
            .into_iter()
            .find(|p| p.guid == owner_guid)
            .unwrap();
        assert_eq!(owner.privileges, 0x01);

        // Admin slot should exist as Pending
        let admin = share
            .participant_list()
            .into_iter()
            .find(|p| p.display_name == "Admin")
            .unwrap();
        assert_eq!(admin.privileges, 0x07);
        assert_eq!(admin.status, ParticipantStatus::Pending);

        remove_share_session(&id);
    }
}

// Drive to a real awaited-channel boundary without scheduling sleeps.
fn poll_pending<F: Future>(future: std::pin::Pin<&mut F>) {
    let mut context = std::task::Context::from_waker(std::task::Waker::noop());
    assert!(future.poll(&mut context).is_pending());
}

#[tokio::test]
async fn test_raw_viewer_terminal_close_interrupts_blocked_snapshot_and_output() {
    for snapshot in [true, false] {
        let id = unique_id("raw_blocked_close_");
        let owner = session_sharing::register(&id).unwrap();
        let survivor = owner.clone();
        let (tx, mut rx) = mpsc::channel(1);
        if snapshot {
            owner.broadcast(Bytes::from_static(b"snapshot"));
            tx.try_send(Bytes::from_static(b"occupied")).unwrap();
            let join = SessionViewer::join(&id, tx);
            tokio::pin!(join);
            poll_pending(join.as_mut());
            session_sharing::deregister(&id);
            assert!(
                tokio::time::timeout(std::time::Duration::from_secs(1), join)
                    .await
                    .unwrap()
                    .is_none()
            );
        } else {
            let viewer = SessionViewer::join(&id, tx.clone()).await.unwrap();
            tx.try_send(Bytes::from_static(b"occupied")).unwrap();
            owner.broadcast(Bytes::from_static(b"ordinary-output"));
            drop(tx); // Only the viewer owns a transport sender during run.
            let run = viewer.run();
            tokio::pin!(run);
            poll_pending(run.as_mut());
            session_sharing::deregister(&id);
            tokio::time::timeout(std::time::Duration::from_secs(1), run)
                .await
                .unwrap();
        }
        assert_eq!(rx.try_recv().unwrap().as_ref(), b"occupied");
        assert!(matches!(
            rx.try_recv(),
            Err(tokio::sync::mpsc::error::TryRecvError::Disconnected)
        ));
        assert!(survivor.last_frame().is_none());
    }
}

#[tokio::test]
async fn test_raw_viewer_lag_terminates_incomplete_delta_stream() {
    let id = unique_id("raw_lag_failure_");
    let owner = session_sharing::register(&id).unwrap();
    let (tx, mut rx) = mpsc::channel(4);
    let viewer = SessionViewer::join(&id, tx).await.unwrap();
    for _ in 0..=session_sharing::BROADCAST_CHANNEL_CAPACITY {
        owner.broadcast(Bytes::from_static(b"delta"));
    }
    tokio::time::timeout(std::time::Duration::from_secs(1), viewer.run())
        .await
        .unwrap();
    assert!(rx.recv().await.is_none());
    session_sharing::deregister(&id);
}

#[derive(Clone, Copy)]
enum ViewerStop {
    FrameEnd,
    OwnerEnd,
    ShareEnd,
    Revoke,
    ViewLoss,
}

#[derive(Clone, Copy)]
enum BlockedViewerStage {
    Accepted,
    Snapshot,
    Output,
}

#[tokio::test]
async fn test_guid_viewer_cancellation_interrupts_every_blocked_send() {
    use crate::share_registry::{
        create_share_session, remove_share_session, ParticipantStatus, PRIV_CONTROL, PRIV_VIEW,
    };
    use crate::share_viewer::check_viewer_join;
    for stop in [
        ViewerStop::FrameEnd,
        ViewerStop::OwnerEnd,
        ViewerStop::ShareEnd,
        ViewerStop::Revoke,
        ViewerStop::ViewLoss,
    ] {
        for stage in [
            BlockedViewerStage::Accepted,
            BlockedViewerStage::Snapshot,
            BlockedViewerStage::Output,
        ] {
            let id = unique_id("guid_blocked_close_");
            let frame = session_sharing::register(&id).unwrap();
            let survivor = frame.clone();
            let (owner_tx, _owner_rx) = mpsc::channel(4);
            let mut owner = SessionOwnerSender::new(owner_tx);
            owner.attach_session(frame.clone());
            let (share, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW | PRIV_CONTROL);
            let guid = share.add_invitation("Viewer".into(), PRIV_VIEW | PRIV_CONTROL, vec![]);
            let params = std::collections::HashMap::from([("share_guid".into(), guid.to_string())]);
            let (tx, mut rx) = mpsc::channel(1);
            let (from_tx, from_rx) = mpsc::channel(4);
            match stage {
                BlockedViewerStage::Accepted => {
                    tx.try_send(Bytes::from_static(b"occupied")).unwrap()
                }
                BlockedViewerStage::Snapshot => {
                    frame.broadcast(Bytes::from_static(b"snapshot"));
                }
                BlockedViewerStage::Output => {}
            }
            let viewer = check_viewer_join(&params, &tx, from_rx, "viewer-transport");
            tokio::pin!(viewer);
            poll_pending(viewer.as_mut());
            if matches!(stage, BlockedViewerStage::Output) {
                let accepted = rx.try_recv().unwrap();
                assert_eq!(
                    guacr_protocol::GuacamoleParser::parse_instruction(&accepted)
                        .unwrap()
                        .opcode,
                    "share_join_accepted"
                );
                tx.try_send(Bytes::from_static(b"occupied")).unwrap();
                frame.broadcast(Bytes::from_static(b"ordinary-output"));
                poll_pending(viewer.as_mut());
            }
            match stop {
                ViewerStop::FrameEnd => session_sharing::deregister(&id),
                ViewerStop::OwnerEnd => owner.owner_disconnect(&id),
                ViewerStop::ShareEnd => remove_share_session(&id),
                ViewerStop::Revoke => share.revoke(guid),
                ViewerStop::ViewLoss => {
                    assert!(share.set_privileges(guid, PRIV_CONTROL));
                    // Restoration must not undo a view-loss termination already signalled.
                    assert!(share.set_privileges(guid, PRIV_VIEW | PRIV_CONTROL));
                }
            }
            let result = tokio::time::timeout(std::time::Duration::from_secs(1), viewer)
                .await
                .unwrap();
            assert!(result.unwrap().is_ok());
            assert!(
                from_tx.is_closed(),
                "exit must release input without requiring sender drop"
            );
            assert!(share
                .participant_list()
                .iter()
                .filter(|p| p.guid == guid)
                .all(|p| p.status == ParticipantStatus::Disconnected));
            let queued = rx.try_recv().unwrap();
            if matches!(stage, BlockedViewerStage::Snapshot) {
                assert_eq!(
                    guacr_protocol::GuacamoleParser::parse_instruction(&queued)
                        .unwrap()
                        .opcode,
                    "share_join_accepted"
                );
            } else {
                assert_eq!(queued.as_ref(), b"occupied");
            }
            assert!(matches!(
                rx.try_recv(),
                Err(tokio::sync::mpsc::error::TryRecvError::Empty)
            ));
            assert_eq!(survivor.viewer_count(), 0);
            session_sharing::deregister(&id);
            remove_share_session(&id);
        }
    }
}

#[tokio::test]
async fn test_guid_viewer_lag_is_explicit_failure() {
    use crate::share_registry::{
        create_share_session, remove_share_session, ParticipantStatus, PRIV_VIEW,
    };
    let id = unique_id("guid_lag_failure_");
    let frame = session_sharing::register(&id).unwrap();
    let (share, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
    let guid = share.add_invitation("Viewer".into(), PRIV_VIEW, vec![]);
    let params = std::collections::HashMap::from([("share_guid".into(), guid.to_string())]);
    let (tx, _rx) = mpsc::channel(8);
    let (from_tx, from_rx) = mpsc::channel(4);
    let viewer = crate::share_viewer::check_viewer_join(&params, &tx, from_rx, "viewer-transport");
    tokio::pin!(viewer);
    poll_pending(viewer.as_mut());
    for _ in 0..=session_sharing::BROADCAST_CHANNEL_CAPACITY {
        frame.broadcast(Bytes::from_static(b"delta"));
    }
    assert!(
        tokio::time::timeout(std::time::Duration::from_secs(1), viewer)
            .await
            .unwrap()
            .unwrap()
            .is_err()
    );
    assert!(from_tx.is_closed());
    assert_eq!(
        share
            .participant_list()
            .iter()
            .find(|p| p.guid == guid)
            .unwrap()
            .status,
        ParticipantStatus::Disconnected
    );
    session_sharing::deregister(&id);
    remove_share_session(&id);
}

#[tokio::test]
async fn test_guid_viewer_preserves_bytes_actor_and_original_generation() {
    use crate::session_sharing::ViewerInput;
    use crate::share_registry::{
        create_share_session, remove_share_session, PRIV_CONTROL, PRIV_VIEW,
    };
    let id = unique_id("guid_actor_generation_");
    let frame = session_sharing::register(&id).unwrap();
    let (input_tx, mut input_rx) = mpsc::unbounded_channel::<ViewerInput>();
    frame.set_viewer_input_channel(input_tx);
    let (share, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW | PRIV_CONTROL);
    let guid = share.add_invitation("Viewer Actor".into(), PRIV_VIEW | PRIV_CONTROL, vec![]);
    let params = std::collections::HashMap::from([("share_guid".into(), guid.to_string())]);
    let (tx, mut rx) = mpsc::channel(8);
    let (from_tx, from_rx) = mpsc::channel(4);
    let viewer = crate::share_viewer::check_viewer_join(&params, &tx, from_rx, "viewer-transport");
    tokio::pin!(viewer);
    let accepted = tokio::select! {
        result = viewer.as_mut() => panic!("viewer ended before join confirmation: {result:?}"),
        accepted = tokio::time::timeout(std::time::Duration::from_secs(1), rx.recv()) => accepted.unwrap().unwrap(),
    };
    let accepted = guacr_protocol::GuacamoleParser::parse_instruction(&accepted).unwrap();
    assert_eq!(accepted.opcode, "share_join_accepted");
    assert_eq!(accepted.args, vec!["03"]);
    let bytes = Bytes::from_static(b"3.key,5.65507,1.1;");
    from_tx.try_send(bytes.clone()).unwrap();
    let input = tokio::select! {
        result = viewer.as_mut() => panic!("viewer ended before attributed input: {result:?}"),
        input = tokio::time::timeout(std::time::Duration::from_secs(1), input_rx.recv()) => input.unwrap().unwrap(),
    };
    assert_eq!(input.bytes, bytes);
    assert_eq!(input.guid, guid);
    assert_eq!(input.display_name, "Viewer Actor");
    assert!(share.set_privileges(guid, PRIV_VIEW));
    from_tx
        .try_send(Bytes::from_static(b"3.key,5.65507,1.0;"))
        .unwrap();
    // Wait until the input queue has consumed this event under its current privileges.
    // Polling once does not promise progress when Tokio's cooperative budget is spent.
    tokio::select! {
        result = viewer.as_mut() => panic!("viewer ended while draining denied input: {result:?}"),
        permits = tokio::time::timeout(std::time::Duration::from_secs(1), from_tx.reserve_many(4)) => drop(permits.unwrap().unwrap()),
    }
    assert!(matches!(
        input_rx.try_recv(),
        Err(tokio::sync::mpsc::error::TryRecvError::Empty)
    ));
    let output = Bytes::from_static(b"4.sync,1.7;");
    frame.broadcast(output.clone());
    let delivered = tokio::select! {
        result = viewer.as_mut() => panic!("viewer ended before ordinary output: {result:?}"),
        output = tokio::time::timeout(std::time::Duration::from_secs(1), rx.recv()) => output.unwrap().unwrap(),
    };
    assert_eq!(delivered, output);
    session_sharing::deregister(&id);
    let replacement = session_sharing::register(&id).unwrap();
    let mut replacement_viewer = replacement.subscribe();
    let (replacement_input_tx, mut replacement_input_rx) = mpsc::unbounded_channel::<ViewerInput>();
    replacement.set_viewer_input_channel(replacement_input_tx);
    assert!(share.set_privileges(guid, PRIV_VIEW | PRIV_CONTROL));
    from_tx
        .try_send(Bytes::from_static(b"3.key,1.1,1.1;"))
        .unwrap();
    assert!(
        tokio::time::timeout(std::time::Duration::from_secs(1), viewer)
            .await
            .unwrap()
            .unwrap()
            .is_ok()
    );
    assert!(matches!(
        replacement_input_rx.try_recv(),
        Err(tokio::sync::mpsc::error::TryRecvError::Empty)
    ));
    // Old-viewer cleanup must not broadcast a participant update into the replacement.
    assert!(matches!(
        replacement_viewer.try_recv(),
        Err(tokio::sync::broadcast::error::TryRecvError::Empty)
    ));
    let output = Bytes::from_static(b"replacement-output");
    assert_eq!(replacement.broadcast(output.clone()), 1);
    assert_eq!(replacement_viewer.try_recv().unwrap(), output);
    session_sharing::deregister(&id);
    remove_share_session(&id);
}

#[tokio::test]
async fn test_guid_viewer_view_loss_broadcasts_disconnected_without_transport_capacity() {
    use crate::share_registry::{create_share_session, remove_share_session, PRIV_VIEW};
    let id = unique_id("guid_cleanup_update_");
    let frame = session_sharing::register(&id).unwrap();
    let mut observer = frame.subscribe();
    let cached = Bytes::from_static(b"cached-display");
    frame.broadcast(cached.clone());
    assert_eq!(observer.try_recv().unwrap(), cached);
    let (share, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
    let guid = share.add_invitation("Viewer".into(), PRIV_VIEW, vec![]);
    let params = std::collections::HashMap::from([("share_guid".into(), guid.to_string())]);
    let (tx, _rx) = mpsc::channel(1);
    tx.try_send(Bytes::from_static(b"occupied")).unwrap();
    let (from_tx, from_rx) = mpsc::channel(4);
    let viewer = crate::share_viewer::check_viewer_join(&params, &tx, from_rx, "viewer-transport");
    tokio::pin!(viewer);
    poll_pending(viewer.as_mut());
    observer.try_recv().unwrap(); // Connected participant update before subscription.
    assert!(share.set_privileges(guid, 0));
    assert!(
        tokio::time::timeout(std::time::Duration::from_secs(1), viewer)
            .await
            .unwrap()
            .unwrap()
            .is_ok()
    );
    assert!(from_tx.is_closed());
    let update = observer.try_recv().unwrap();
    let update = guacr_protocol::GuacamoleParser::parse_instruction(&update).unwrap();
    assert_eq!(update.opcode, "participant_update");
    let payload: serde_json::Value = serde_json::from_str(update.args[0]).unwrap();
    let viewer = payload["participants"]
        .as_array()
        .unwrap()
        .iter()
        .find(|p| p["display_name"] == "Viewer")
        .unwrap();
    assert_eq!(viewer["status"], "disconnected");
    assert_eq!(frame.last_frame(), Some(cached));
    session_sharing::deregister(&id);
    remove_share_session(&id);
}

#[tokio::test]
async fn test_old_guid_cannot_join_replacement_and_old_teardown_preserves_fresh_share() {
    use crate::share_registry::{
        create_share_session, find_session_by_guid, get_share_session, remove_share_session,
        PRIV_VIEW,
    };
    for owner_end in [false, true] {
        let id = unique_id("guid_replacement_admission_");
        let old_frame = session_sharing::register(&id).unwrap();
        let (owner_tx, _owner_rx) = mpsc::channel(4);
        let mut old_owner = SessionOwnerSender::new(owner_tx);
        old_owner.attach_session(old_frame.clone());
        let (old_share, _) = create_share_session(&id, "Old Owner".into(), PRIV_VIEW);
        let old_guid = old_share.add_invitation("Old Viewer".into(), PRIV_VIEW, vec![]);
        if owner_end {
            old_owner.owner_disconnect(&id);
        } else {
            session_sharing::deregister(&id);
        }
        assert!(find_session_by_guid(old_guid).is_none());
        assert!(old_share.accept_join(old_guid).is_err());
        let fresh_frame = session_sharing::register(&id).unwrap();
        let (fresh_share, _) = create_share_session(&id, "Fresh Owner".into(), PRIV_VIEW);
        let fresh_guid = fresh_share.add_invitation("Fresh Viewer".into(), PRIV_VIEW, vec![]);
        let old_params =
            std::collections::HashMap::from([("share_guid".into(), old_guid.to_string())]);
        let (old_tx, mut old_rx) = mpsc::channel(8);
        let (_old_input_tx, old_input_rx) = mpsc::channel(4);
        let old_result = tokio::time::timeout(
            std::time::Duration::from_secs(1),
            crate::share_viewer::check_viewer_join(
                &old_params,
                &old_tx,
                old_input_rx,
                "old-viewer-transport",
            ),
        )
        .await
        .unwrap()
        .unwrap();
        assert!(old_result.is_err());
        let rejection = old_rx.try_recv().unwrap();
        assert_eq!(
            guacr_protocol::GuacamoleParser::parse_instruction(&rejection)
                .unwrap()
                .opcode,
            "share_join_rejected"
        );
        old_owner.owner_disconnect(&id);
        assert!(std::sync::Arc::ptr_eq(
            &get_share_session(&id).unwrap(),
            &fresh_share
        ));
        let params =
            std::collections::HashMap::from([("share_guid".into(), fresh_guid.to_string())]);
        let (tx, mut rx) = mpsc::channel(8);
        let (input_tx, input_rx) = mpsc::channel(4);
        let viewer = crate::share_viewer::check_viewer_join(
            &params,
            &tx,
            input_rx,
            "fresh-viewer-transport",
        );
        tokio::pin!(viewer);
        let accepted = tokio::select! {
            result = viewer.as_mut() => panic!("fresh viewer failed to join: {result:?}"),
            accepted = tokio::time::timeout(std::time::Duration::from_secs(1), rx.recv()) => accepted.unwrap().unwrap(),
        };
        assert_eq!(
            guacr_protocol::GuacamoleParser::parse_instruction(&accepted)
                .unwrap()
                .opcode,
            "share_join_accepted"
        );
        let output = Bytes::from_static(b"fresh-owner-output");
        fresh_frame.broadcast(output.clone());
        let delivered = tokio::select! {
            result = viewer.as_mut() => panic!("fresh viewer ended before output: {result:?}"),
            delivered = tokio::time::timeout(std::time::Duration::from_secs(1), rx.recv()) => delivered.unwrap().unwrap(),
        };
        assert_eq!(delivered, output);
        session_sharing::deregister(&id);
        assert!(
            tokio::time::timeout(std::time::Duration::from_secs(1), viewer)
                .await
                .unwrap()
                .unwrap()
                .is_ok()
        );
        assert!(input_tx.is_closed());
        remove_share_session(&id);
    }
}
