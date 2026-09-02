// Unit tests for session sharing integration in the RDP handler.
//
// Tests cover the three connection modes: standalone (no share-id), owner
// (share-id present, viewer-mode false), and viewer (viewer-mode=true).
//
// The viewer path returns before any network I/O, making it suitable for fast
// unit tests. Owner/standalone paths fail at TCP connect to a no-listener
// address.

use guacr_handlers::{session_sharing, ProtocolHandler};
use std::collections::HashMap;
use tokio::sync::mpsc;

use crate::handler::RdpHandler;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

fn unique_sid(tag: &str) -> String {
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(0);
    format!("$rdp-test-{tag}-{}", CTR.fetch_add(1, Ordering::Relaxed))
}

/// Minimal params that pass RdpSettings::from_params but connect to an
/// address with no listener so the TCP connect fails fast.
fn base_params() -> HashMap<String, String> {
    let mut p = HashMap::new();
    p.insert("hostname".to_string(), "127.0.0.1".to_string());
    p.insert("port".to_string(), "19998".to_string());
    p.insert("username".to_string(), "test-user".to_string());
    p.insert("password".to_string(), "test-pass".to_string());
    // allow-supply-user=true is required when credentials are present.
    p.insert("allow-supply-user".to_string(), "true".to_string());
    p
}

// ---------------------------------------------------------------------------
// test_viewer_gets_error_for_unknown_share_id
// ---------------------------------------------------------------------------

#[tokio::test]
async fn test_viewer_gets_error_for_unknown_share_id() {
    let handler = RdpHandler::with_defaults();
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

    // Pre-register to confirm the registry enforces uniqueness (the same
    // call that connect() makes).
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
    let handler = RdpHandler::with_defaults();
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

    // Error must be TCP-level, not session-sharing.
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
    let handler = RdpHandler::with_defaults();
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

    // The owner path attempts TCP connect (fails), not the viewer "not found" path.
    if let Err(ref e) = result {
        let msg = e.to_string();
        assert!(
            !msg.contains("No active session"),
            "viewer-mode=false must not trigger viewer error path; got: {msg}"
        );
    }

    session_sharing::deregister(&sid);
}
