// Unit tests for session_sharing module.
//
// Covers: register/lookup/deregister lifecycle, broadcast, late-join frame cache,
// concurrent access, and '$' prefix enforcement.

use crate::session_sharing::{
    active_session_ids, deregister, lookup, register, SessionHandle, BROADCAST_CHANNEL_CAPACITY,
};
use bytes::Bytes;
use std::sync::Arc;

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
    let _h = register(&id).unwrap();
    let result = register(&id);
    assert!(result.is_err(), "duplicate register must return Err");
    let msg = result.unwrap_err();
    assert!(
        msg.contains("already registered"),
        "error must mention already-registered; got: {msg}"
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
    let msg = result.unwrap_err();
    assert!(
        msg.contains('$'),
        "error must mention '$' requirement; got: {msg}"
    );
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

/// Prove that a viewer input registered on the handle is delivered to the owner.
///
/// This test FAILS until SessionHandle gains a viewer_input channel:
///   set_viewer_input_channel() / forward_viewer_input()
#[test]
fn test_viewer_input_forwarded_to_owner_channel() {
    use tokio::sync::mpsc;
    let (tx, mut rx) = mpsc::unbounded_channel::<Bytes>();

    let handle = SessionHandle::new();
    handle.set_viewer_input_channel(tx);

    let input = Bytes::from_static(b"4.key,5.65507,1.1;");
    let forwarded = handle.forward_viewer_input(input.clone());
    assert!(
        forwarded,
        "forward_viewer_input must return true when channel is registered"
    );

    let received = rx
        .try_recv()
        .expect("owner channel must receive viewer input");
    assert_eq!(received, input);
}

/// Prove that forward_viewer_input returns false when no channel is registered.
#[test]
fn test_viewer_input_not_forwarded_without_channel() {
    let handle = SessionHandle::new();
    let input = Bytes::from_static(b"4.key,5.65507,1.1;");
    let forwarded = handle.forward_viewer_input(input);
    assert!(
        !forwarded,
        "forward_viewer_input must return false when no channel registered"
    );
}
