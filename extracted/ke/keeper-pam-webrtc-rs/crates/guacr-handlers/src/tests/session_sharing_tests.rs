// Unit tests for session_sharing module.
//
// Covers: register/lookup/deregister lifecycle, broadcast, late-join frame cache,
// concurrent access, and '$' prefix enforcement.

use crate::session_sharing::{
    active_session_ids, deregister, lookup, register, SessionHandle, ViewerInput,
    BROADCAST_CHANNEL_CAPACITY,
};
use bytes::Bytes;
use std::sync::Arc;
use uuid::Uuid;

fn unique_id(prefix: &str) -> String {
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(1000);
    format!("${prefix}{}", CTR.fetch_add(1, Ordering::Relaxed))
}

// -------------------------------------------------------------------------
// Registration lifecycle
// -------------------------------------------------------------------------

#[test]
fn test_register_creates_findable_session() {
    let id = unique_id("reg_");
    let _handle = register(&id).expect("register must succeed for new id");
    assert!(lookup(&id).is_some(), "registered session must be findable");
    deregister(&id);
}

#[test]
fn test_register_duplicate_id_returns_err() {
    let id = unique_id("dup_");
    let owner = register(&id).unwrap();
    let (input_tx, mut input_rx) = tokio::sync::mpsc::unbounded_channel();
    owner.set_viewer_input_channel(input_tx);
    assert!(register(&id).is_err());
    let current = lookup(&id).unwrap();
    let mut viewer = current.subscribe();
    let frame = Bytes::from_static(b"original-owner-frame");
    assert_eq!(owner.broadcast(frame.clone()), 1);
    assert_eq!(viewer.try_recv().unwrap(), frame);
    assert!(current.forward_viewer_input(viewer_input(b"4.key,1.1,1.0;", "Viewer")));
    assert_eq!(
        input_rx.try_recv().unwrap().bytes.as_ref(),
        b"4.key,1.1,1.0;"
    );
    deregister(&id);
}

#[test]
fn test_lookup_nonexistent_returns_none() {
    assert!(
        lookup("$nonexistent_sharing_test_xyz").is_none(),
        "lookup of unknown id must return None"
    );
}

#[test]
fn test_deregister_removes_session() {
    let id = unique_id("dereg_");
    register(&id).unwrap();
    deregister(&id);
    assert!(
        lookup(&id).is_none(),
        "deregistered session must not be findable"
    );
}

#[test]
fn test_deregister_nonexistent_does_not_panic() {
    // Must be a no-op, not a panic.
    deregister("$nonexistent_dereg_xyz");
}

// -------------------------------------------------------------------------
// '$' prefix enforcement
// -------------------------------------------------------------------------

#[test]
fn test_session_id_without_dollar_prefix_rejected() {
    let result = register("no-dollar-here");
    assert!(result.is_err(), "missing '$' prefix must be rejected");
}

#[test]
fn test_session_id_with_dollar_prefix_accepted() {
    let id = unique_id("prefix_ok_");
    assert!(register(&id).is_ok(), "'$' prefixed id must be accepted");
    deregister(&id);
}

// -------------------------------------------------------------------------
// Broadcast channel
// -------------------------------------------------------------------------

/// BROADCAST_CHANNEL_CAPACITY is a compile-time constant — verified here so a
/// future change that sets it to zero is caught immediately.
const _: () = {
    assert!(
        BROADCAST_CHANNEL_CAPACITY > 0,
        "broadcast capacity must be positive"
    );
};

#[test]
fn test_broadcast_single_receiver() {
    let id = unique_id("bc_single_");
    let handle = register(&id).unwrap();
    let mut rx = handle.subscribe();

    let frame = Bytes::from_static(b"hello-world");
    let n = handle.broadcast(frame.clone());
    assert_eq!(n, 1, "one receiver must be counted");

    let got = rx.try_recv().expect("receiver must get the frame");
    assert_eq!(got, frame);
    deregister(&id);
}

#[test]
fn test_broadcast_no_receivers_returns_zero() {
    let id = unique_id("bc_none_");
    let handle = register(&id).unwrap();
    // No subscribers.
    let n = handle.broadcast(Bytes::from_static(b"no-one-home"));
    assert_eq!(n, 0, "send with no receivers must return 0");
    deregister(&id);
}

#[test]
fn test_broadcast_multiple_receivers() {
    let id = unique_id("bc_multi_");
    let handle = register(&id).unwrap();
    let mut rx1 = handle.subscribe();
    let mut rx2 = handle.subscribe();
    let mut rx3 = handle.subscribe();

    let frame = Bytes::from_static(b"multi-rx");
    let n = handle.broadcast(frame.clone());
    assert_eq!(n, 3, "three receivers must all get the frame");

    assert_eq!(rx1.try_recv().unwrap(), frame);
    assert_eq!(rx2.try_recv().unwrap(), frame);
    assert_eq!(rx3.try_recv().unwrap(), frame);
    deregister(&id);
}

// -------------------------------------------------------------------------
// Late-join frame cache (T-087)
// -------------------------------------------------------------------------

#[test]
fn test_last_frame_is_none_before_any_broadcast() {
    let id = unique_id("lf_none_");
    let handle = register(&id).unwrap();
    assert!(
        handle.last_frame().is_none(),
        "last_frame must be None before any broadcast"
    );
    deregister(&id);
}

#[test]
fn test_last_frame_updated_after_broadcast() {
    let id = unique_id("lf_set_");
    let handle = register(&id).unwrap();
    let frame = Bytes::from_static(b"latest-state");
    handle.broadcast(frame.clone());
    let cached = handle
        .last_frame()
        .expect("last_frame must be Some after broadcast");
    assert_eq!(cached, frame, "cached frame must match last broadcast");
    deregister(&id);
}

#[test]
fn test_last_frame_updated_to_most_recent() {
    let id = unique_id("lf_update_");
    let handle = register(&id).unwrap();
    handle.broadcast(Bytes::from_static(b"first-frame"));
    let second = Bytes::from_static(b"second-frame");
    handle.broadcast(second.clone());
    let cached = handle.last_frame().unwrap();
    assert_eq!(cached, second, "last_frame must hold most recent frame");
    deregister(&id);
}

// -------------------------------------------------------------------------
// Viewer count
// -------------------------------------------------------------------------

#[test]
fn test_viewer_count_zero_initially() {
    let id = unique_id("vc_zero_");
    let handle = register(&id).unwrap();
    assert_eq!(handle.viewer_count(), 0);
    deregister(&id);
}

#[test]
fn test_viewer_count_increments_with_subscriptions() {
    let id = unique_id("vc_inc_");
    let handle = register(&id).unwrap();
    let _r1 = handle.subscribe();
    assert_eq!(handle.viewer_count(), 1);
    let _r2 = handle.subscribe();
    assert_eq!(handle.viewer_count(), 2);
    deregister(&id);
}

#[test]
fn test_viewer_count_decrements_when_receiver_dropped() {
    let id = unique_id("vc_dec_");
    let handle = register(&id).unwrap();
    let r1 = handle.subscribe();
    assert_eq!(handle.viewer_count(), 1);
    drop(r1);
    assert_eq!(
        handle.viewer_count(),
        0,
        "dropped receiver must decrement count"
    );
    deregister(&id);
}

// -------------------------------------------------------------------------
// active_session_ids diagnostics
// -------------------------------------------------------------------------

#[test]
fn test_active_session_ids_includes_registered() {
    let id = unique_id("ids_");
    register(&id).unwrap();
    let ids = active_session_ids();
    assert!(
        ids.contains(&id),
        "active_session_ids must include registered id"
    );
    deregister(&id);
}

#[test]
fn test_active_session_ids_excludes_deregistered() {
    let id = unique_id("ids_gone_");
    register(&id).unwrap();
    deregister(&id);
    let ids = active_session_ids();
    assert!(
        !ids.contains(&id),
        "deregistered id must not appear in active_session_ids"
    );
}

// -------------------------------------------------------------------------
// Concurrent access (DashMap must not deadlock or panic)
// -------------------------------------------------------------------------

#[test]
fn test_concurrent_register_lookup_race_free() {
    use std::thread;

    let id = Arc::new(unique_id("conc_"));
    let barrier = Arc::new(std::sync::Barrier::new(8));

    let threads: Vec<_> = (0..8)
        .map(|i| {
            let id = Arc::clone(&id);
            let b = Arc::clone(&barrier);
            thread::spawn(move || {
                b.wait();
                if i == 0 {
                    let _ = register(&id);
                } else {
                    let _ = lookup(&id);
                }
            })
        })
        .collect();

    for t in threads {
        t.join().expect("thread must not panic");
    }
    deregister(&id);
}

// -------------------------------------------------------------------------
// SessionHandle: Default/Clone consistency
// -------------------------------------------------------------------------

#[test]
fn test_session_handle_default_has_no_last_frame() {
    let h = SessionHandle::default();
    assert!(h.last_frame().is_none());
    assert_eq!(h.viewer_count(), 0);
}

#[test]
fn test_session_handle_clone_shares_broadcast_channel() {
    // Two clones of the same handle must share the same broadcast channel.
    let h1 = SessionHandle::new();
    let h2 = h1.clone();
    let mut rx = h2.subscribe();

    let frame = Bytes::from_static(b"shared-channel");
    h1.broadcast(frame.clone());

    let got = rx
        .try_recv()
        .expect("clone must receive frame broadcast via original");
    assert_eq!(got, frame);
}

// -------------------------------------------------------------------------
// Viewer input forwarding (PRIV_CONTROL — Phase 6b)
// -------------------------------------------------------------------------

fn viewer_input(bytes: &'static [u8], display_name: &str) -> ViewerInput {
    ViewerInput {
        bytes: Bytes::from_static(bytes),
        guid: Uuid::nil(),
        display_name: display_name.to_string(),
    }
}

/// Prove that a viewer input registered on the handle is delivered to the owner.
///
/// This test FAILS until SessionHandle gains a viewer_input channel:
///   set_viewer_input_channel() / forward_viewer_input()
#[test]
fn test_viewer_input_forwarded_to_owner_channel() {
    use tokio::sync::mpsc;
    let (tx, mut rx) = mpsc::unbounded_channel::<ViewerInput>();

    let handle = SessionHandle::new();
    handle.set_viewer_input_channel(tx);

    let forwarded = handle.forward_viewer_input(viewer_input(b"4.key,5.65507,1.1;", "Alice"));
    assert!(
        forwarded,
        "forward_viewer_input must return true when channel is registered"
    );

    let received = rx
        .try_recv()
        .expect("owner channel must receive viewer input");
    assert_eq!(received.bytes, Bytes::from_static(b"4.key,5.65507,1.1;"));
}

/// Prove that forward_viewer_input returns false when no channel is registered.
#[test]
fn test_viewer_input_not_forwarded_without_channel() {
    let handle = SessionHandle::new();
    let forwarded = handle.forward_viewer_input(viewer_input(b"4.key,5.65507,1.1;", "Alice"));
    assert!(
        !forwarded,
        "forward_viewer_input must return false when no channel registered"
    );
}

/// The forwarded input must name its sender, or the owner's handler cannot tell a
/// viewer's keystroke from the owner's own and records both as the owner's.
#[test]
fn test_forwarded_input_carries_sender_identity() {
    use tokio::sync::mpsc;
    let (tx, mut rx) = mpsc::unbounded_channel::<ViewerInput>();

    let handle = SessionHandle::new();
    handle.set_viewer_input_channel(tx);

    let guid = Uuid::new_v4();
    handle.forward_viewer_input(ViewerInput {
        bytes: Bytes::from_static(b"4.key,5.65507,1.1;"),
        guid,
        display_name: "Bob".into(),
    });

    let received = rx.try_recv().expect("input must arrive");
    assert_eq!(received.display_name, "Bob");
    assert_eq!(received.guid, guid, "guid must survive the hand-off");
}

// -------------------------------------------------------------------------
// Late-join frame cache vs. control traffic
// -------------------------------------------------------------------------

/// A late-joining viewer's state sync replays `last_frame`. Control traffic is not
/// screen state, so caching it hands the next joiner a participant-list update
/// where a picture belongs.
#[test]
fn test_broadcast_control_does_not_disturb_frame_cache() {
    let handle = SessionHandle::new();
    let frame = Bytes::from_static(b"4.img,1.0;");
    handle.broadcast(frame.clone());

    handle.broadcast_control(Bytes::from_static(b"18.participant_update,2.{};"));

    assert_eq!(
        handle.last_frame(),
        Some(frame),
        "control traffic must not overwrite the cached frame"
    );
}

/// Control traffic must still reach every connected viewer — only the cache is skipped.
#[test]
fn test_broadcast_control_still_reaches_viewers() {
    let handle = SessionHandle::new();
    let mut rx = handle.subscribe();

    let notice = Bytes::from_static(b"18.participant_update,2.{};");
    assert_eq!(handle.broadcast_control(notice.clone()), 1);
    assert_eq!(rx.try_recv().expect("viewer must receive it"), notice);
}

/// With nothing but control traffic sent, the cache stays empty rather than
/// offering a control message as a first frame.
#[test]
fn test_control_only_session_has_no_cached_frame() {
    let handle = SessionHandle::new();
    handle.broadcast_control(Bytes::from_static(b"18.participant_update,2.{};"));
    assert!(
        handle.last_frame().is_none(),
        "a session that has sent no frames must have no cached frame"
    );
}
#[cfg(test)]
mod share_registry_tests {
    use crate::share_registry::*;
    use uuid::Uuid;

    fn session_id() -> String {
        use std::sync::atomic::{AtomicU64, Ordering};
        static CTR: AtomicU64 = AtomicU64::new(0);
        format!("$test-share-{}", CTR.fetch_add(1, Ordering::Relaxed))
    }

    #[test]
    fn test_create_and_get() {
        let id = session_id();
        let (session, _owner) = create_share_session(&id, "Alice".into(), PRIV_VIEW | PRIV_CONTROL);
        assert_eq!(session.participant_list().len(), 1);
        assert!(get_share_session(&id).is_some());
        remove_share_session(&id);
        assert!(get_share_session(&id).is_none());
    }

    #[test]
    fn test_invitation_lifecycle() {
        let id = session_id();
        let (session, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW | PRIV_CONTROL);

        let guid = session.add_invitation("Bob".into(), PRIV_VIEW, vec![]);
        assert_eq!(session.participant_list().len(), 2);

        // Accept
        let p = session.accept_join(guid).unwrap();
        assert_eq!(p.status, ParticipantStatus::Connected);

        // Can't join twice
        assert!(session.accept_join(guid).is_err());

        remove_share_session(&id);
    }

    #[test]
    fn test_revoke_pending() {
        let id = session_id();
        let (session, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
        let guid = session.add_invitation("Viewer".into(), PRIV_VIEW, vec![]);
        session.revoke(guid);
        assert!(session.accept_join(guid).is_err());
        remove_share_session(&id);
    }

    #[test]
    fn test_privilege_change() {
        let id = session_id();
        let (session, owner_guid) =
            create_share_session(&id, "Owner".into(), PRIV_VIEW | PRIV_CONTROL);
        session.set_privileges(owner_guid, PRIV_VIEW);
        let p = session
            .participant_list()
            .into_iter()
            .find(|p| p.guid == owner_guid)
            .unwrap();
        assert_eq!(p.privileges, PRIV_VIEW);
        assert!(!p.has_privilege(PRIV_CONTROL));
        remove_share_session(&id);
    }

    #[test]
    fn test_find_by_guid() {
        let id = session_id();
        let (session, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
        let guid = session.add_invitation("Viewer".into(), PRIV_VIEW, vec![]);

        let found = find_session_by_guid(guid);
        assert!(found.is_some());
        assert_eq!(found.unwrap().session_id, id);

        let not_found = find_session_by_guid(Uuid::new_v4());
        assert!(not_found.is_none());

        remove_share_session(&id);
    }

    #[test]
    fn test_get_privileges_reflects_revocation() {
        let id = session_id();
        let (session, _owner) = create_share_session(&id, "Owner".into(), PRIV_VIEW | PRIV_CONTROL);
        let guid = session.add_invitation("Viewer".into(), PRIV_VIEW | PRIV_CONTROL, vec![]);
        session.accept_join(guid).unwrap();
        assert_eq!(session.get_privileges(guid), Some(PRIV_VIEW | PRIV_CONTROL));
        assert!(session.set_privileges(guid, PRIV_VIEW));
        let privs = session
            .get_privileges(guid)
            .expect("participant still present");
        assert_eq!(
            privs & PRIV_CONTROL,
            0,
            "PRIV_CONTROL must be gone after revoke"
        );
        assert_eq!(privs & PRIV_VIEW, PRIV_VIEW, "PRIV_VIEW retained");
        remove_share_session(&id);
    }

    #[test]
    fn test_get_privileges_none_after_full_revoke() {
        let id = session_id();
        let (session, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
        let guid = session.add_invitation("Viewer".into(), PRIV_VIEW | PRIV_CONTROL, vec![]);
        session.accept_join(guid).unwrap();
        session.revoke(guid);
        assert_eq!(session.get_privileges(guid), None);
        remove_share_session(&id);
    }

    // Regression: forward_viewer_input() must return false if the owner's handler
    // never registered a viewer_input channel. Without registering the channel,
    // viewers with PRIV_CONTROL can send key/mouse events but they are silently
    // dropped. The owner's select! loop never receives them.
    //
    // This test proves the current buggy state (forward returns false before wiring)
    // and validates the fix (forward returns true and delivers bytes after wiring).
    #[test]
    fn test_viewer_input_forwarding_requires_channel_registration() {
        use crate::session_sharing::{self, ViewerInput};
        use bytes::Bytes;

        let id = session_id();
        // Register as if we're the owner handler calling session_sharing::register().
        let handle = session_sharing::register(&id).unwrap();

        let input = || ViewerInput {
            bytes: Bytes::from_static(b"4.key,1.1,1.0;"),
            guid: uuid::Uuid::nil(),
            display_name: "Viewer".into(),
        };

        // Before set_viewer_input_channel: forward_viewer_input returns false.
        let dropped = !handle.forward_viewer_input(input());
        assert!(
            dropped,
            "input must be dropped when no channel is registered"
        );

        // Wire the channel (what the owner handler must do at session start).
        let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel::<ViewerInput>();
        handle.set_viewer_input_channel(tx);

        // After wiring: forward_viewer_input returns true and the bytes arrive.
        let delivered = handle.forward_viewer_input(input());
        assert!(
            delivered,
            "input must be delivered after channel is registered"
        );
        let received = rx.try_recv().expect("bytes must arrive on channel");
        assert_eq!(received.bytes.as_ref(), b"4.key,1.1,1.0;");

        session_sharing::deregister(&id);
    }
}

#[test]
fn test_terminal_close_retires_surviving_handle_capabilities() {
    let id = unique_id("terminal_capabilities_");
    let owner = register(&id).unwrap();
    let survivor = owner.clone();
    let mut viewer = survivor.subscribe();
    let (tx, mut input_rx) = tokio::sync::mpsc::unbounded_channel();
    owner.set_viewer_input_channel(tx);
    owner.broadcast(Bytes::from_static(b"cached-display"));
    assert_eq!(viewer.try_recv().unwrap().as_ref(), b"cached-display");
    deregister(&id);
    assert!(survivor.last_frame().is_none());
    assert!(matches!(
        viewer.try_recv(),
        Err(tokio::sync::broadcast::error::TryRecvError::Closed)
    ));
    assert_eq!(survivor.broadcast(Bytes::from_static(b"after-close")), 0);
    assert_eq!(
        survivor.broadcast_control(Bytes::from_static(b"after-close-control")),
        0
    );
    assert!(!survivor.forward_viewer_input(viewer_input(b"4.key,1.1,1.0;", "Viewer")));
    assert!(matches!(
        input_rx.try_recv(),
        Err(tokio::sync::mpsc::error::TryRecvError::Disconnected)
    ));
    let (new_tx, mut new_rx) = tokio::sync::mpsc::unbounded_channel();
    survivor.set_viewer_input_channel(new_tx);
    assert!(matches!(
        new_rx.try_recv(),
        Err(tokio::sync::mpsc::error::TryRecvError::Disconnected)
    ));
    assert!(survivor.subscribe_viewer().is_none());
}

#[tokio::test]
async fn test_share_remove_invalidates_surviving_invitation_and_lifetime() {
    use crate::share_registry::{
        create_share_session, remove_share_session, ParticipantStatus, PRIV_VIEW,
    };
    let id = unique_id("terminal_share_");
    let (share, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
    let guid = share.add_invitation("Viewer".into(), PRIV_VIEW, vec![]);
    remove_share_session(&id);
    assert!(share.accept_join(guid).is_err());
    assert!(share.get_privileges(guid).is_none());
    assert!(share
        .participant_list()
        .iter()
        .all(|p| p.status == ParticipantStatus::Disconnected));
    let mut ended = share.cancellation();
    tokio::time::timeout(std::time::Duration::from_secs(1), ended.cancelled())
        .await
        .unwrap();
}

#[tokio::test]
async fn test_view_loss_before_subscription_remains_terminal_after_restore() {
    use crate::share_registry::{
        create_share_session, remove_share_session, PRIV_CONTROL, PRIV_VIEW,
    };
    let id = unique_id("sticky_view_loss_");
    let (share, _) = create_share_session(&id, "Owner".into(), PRIV_VIEW);
    let guid = share.add_invitation("Viewer".into(), PRIV_VIEW, vec![]);
    share.accept_join(guid).unwrap();
    assert!(share.set_privileges(guid, PRIV_CONTROL));
    assert!(share.set_privileges(guid, PRIV_VIEW));
    let mut ended = share.participant_cancellation(guid).unwrap();
    tokio::time::timeout(std::time::Duration::from_secs(1), ended.cancelled())
        .await
        .unwrap();
    remove_share_session(&id);
}
