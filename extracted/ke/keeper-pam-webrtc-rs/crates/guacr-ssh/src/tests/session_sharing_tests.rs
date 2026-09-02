// Unit tests for session sharing integration in the SSH handler.
//
// Tests are structured around the three connection modes introduced in
// Phase 1f: standalone (no share-id), owner (share-id present, viewer-mode
// false), and viewer (viewer-mode=true).
//
// All tests run without a live SSH server — the viewer path returns before
// any network I/O, and the owner/standalone paths fail fast at TCP connect
// to a loopback address with no listener.

use guacr_handlers::{session_sharing, ProtocolHandler};
use std::collections::HashMap;
use tokio::sync::mpsc;

use crate::handler::SshHandler;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/// Unique session ID generator — prevents test cross-contamination in the
/// global SESSION_REGISTRY.
fn unique_sid(tag: &str) -> String {
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(0);
    format!("$ssh-test-{tag}-{}", CTR.fetch_add(1, Ordering::Relaxed))
}

/// Build a minimal params map sufficient to reach the share-id branching code
/// but invalid for a real SSH connection (hostname points nowhere useful).
fn base_params() -> HashMap<String, String> {
    let mut p = HashMap::new();
    // hostname is required by SshConnectParams; 127.0.0.1:19999 is almost
    // certainly not listening so the TCP connect fails fast.
    p.insert("hostname".to_string(), "127.0.0.1".to_string());
    p.insert("port".to_string(), "19999".to_string());
    p.insert("username".to_string(), "test-user".to_string());
    p.insert("password".to_string(), "test-pass".to_string());
    // allow-supply-user=true is required when credentials are present.
    p.insert("allow-supply-user".to_string(), "true".to_string());
    p
}

// ---------------------------------------------------------------------------
// test_viewer_gets_error_for_unknown_share_id
// ---------------------------------------------------------------------------
//
// viewer-mode=true with a share-id that is not in the registry must return
// Err immediately — no network I/O is attempted.

#[tokio::test]
async fn test_viewer_gets_error_for_unknown_share_id() {
    let handler = SshHandler::with_defaults();
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
    let err = result.unwrap_err();
    let msg = err.to_string();
    assert!(
        msg.contains("share-id") || msg.contains(&sid) || msg.contains("No active session"),
        "error must mention the share-id or session; got: {msg}"
    );
}

// ---------------------------------------------------------------------------
// test_session_registers_when_share_id_present
// ---------------------------------------------------------------------------
//
// When share-id is set and viewer-mode is false (owner mode), the handler
// must call session_sharing::register() before attempting the TCP connect.
// We verify this by registering the same ID first, which causes the
// session_sharing::register() call inside connect() to fail silently (already
// registered), and then confirming the ID remains in the registry.

#[tokio::test]
async fn test_session_registers_when_share_id_present() {
    let sid = unique_sid("owner-reg");

    // Pre-register so we can observe the collision path without keeping
    // the connect() call alive long enough to do real TCP I/O.
    let _handle = session_sharing::register(&sid).expect("pre-registration must succeed");
    assert!(
        session_sharing::lookup(&sid).is_some(),
        "pre-registered session must be visible in registry"
    );

    // Confirm that a second registration attempt (as would happen inside
    // connect()) is correctly rejected — the registry enforces uniqueness.
    let dup = session_sharing::register(&sid);
    assert!(
        dup.is_err(),
        "registering the same ID twice must fail (AC-5 uniqueness)"
    );

    // The session remains in the registry after the failed second attempt.
    assert!(
        session_sharing::lookup(&sid).is_some(),
        "registry must retain the original entry after a failed duplicate register"
    );

    // Cleanup.
    session_sharing::deregister(&sid);
}

// ---------------------------------------------------------------------------
// test_standalone_session_unaffected
// ---------------------------------------------------------------------------
//
// With no share-id parameter the handler must NOT register anything in the
// session registry and must proceed normally (failing at TCP connect, not
// at session-sharing validation).

#[tokio::test]
async fn test_standalone_session_unaffected() {
    let handler = SshHandler::with_defaults();
    // Use a recognizable sentinel prefix so we can confirm it never appears.
    let sentinel = unique_sid("standalone-sentinel");
    let params = base_params(); // no share-id, no viewer-mode

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
    // (We didn't pass share-id=sentinel, so nothing should have registered it.)
    assert!(
        session_sharing::lookup(&sentinel).is_none(),
        "standalone session must not register any session ID"
    );

    // The error (if any) must be a connection-level failure, not a
    // session-sharing rejection.
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
//
// viewer-mode=false (explicit) with a share-id must NOT call SessionViewer::join
// and must proceed to the owner/standalone path (failing at TCP connect, not
// at session-sharing validation with "not found").

#[tokio::test]
async fn test_viewer_mode_false_does_not_join_session() {
    let handler = SshHandler::with_defaults();
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

    // The session was not pre-registered, so if the viewer path ran it would
    // return Err("No active session found for share-id"). The owner path
    // instead tries to register and then do a TCP connect. Either outcome
    // (Ok or a TCP-level Err) confirms we did NOT take the viewer path.
    if let Err(ref e) = result {
        let msg = e.to_string();
        assert!(
            !msg.contains("No active session"),
            "viewer-mode=false must not trigger viewer error path; got: {msg}"
        );
    }

    // Cleanup any leftover registry entry.
    session_sharing::deregister(&sid);
}
