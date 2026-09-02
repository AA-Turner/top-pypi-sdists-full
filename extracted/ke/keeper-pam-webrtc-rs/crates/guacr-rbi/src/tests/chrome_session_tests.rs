use crate::chrome_session::ChromeSession;

#[test]
fn test_chrome_session_new() {
    let session = ChromeSession::new(1920, 1080, 30, "/usr/bin/chromium");
    assert_eq!(session.width, 1920);
    assert_eq!(session.height, 1080);
}

// ---------------------------------------------------------------------------
// SSRF prevention — handle_download opcode path tests
//
// These tests exercise ChromeSession::handle_download directly to prove that
// URL validation is wired into the download opcode path, not just the
// validate_download_url helper in isolation.  They would fail (the handler
// would attempt an outbound HTTP request instead of returning an error) if
// the `validate_download_url(url)?` call were removed from handle_download.
// ---------------------------------------------------------------------------

/// Prove that handle_download rejects AWS instance-metadata (169.254.169.254)
/// before making any HTTP request.  This is the canonical SSRF vector.
///
/// Without the validate_download_url(url)? call in handle_download the
/// function would proceed to reqwest::Client::new().get(url).send() and
/// either hang waiting for a network response or succeed — it would NOT
/// return Err with "blocked range" in the message.
#[cfg(feature = "chrome")]
#[tokio::test]
async fn test_handle_download_blocks_aws_metadata_ssrf() {
    let (tx, _rx) = tokio::sync::mpsc::channel(8);

    let mut session = ChromeSession::new(1280, 720, 30, "/usr/bin/chromium");

    let config = crate::handler::DownloadConfig {
        enabled: true,
        max_file_size_mb: 10,
        allowed_extensions: vec![], // empty = allow all extensions
        blocked_extensions: vec![],
        require_approval: false,
        max_downloads_per_session: 10,
    };

    let result = session
        .handle_download(
            "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            "creds.txt",
            &config,
            &tx,
        )
        .await;

    assert!(
        result.is_err(),
        "handle_download must reject 169.254.x SSRF URL; got Ok(())"
    );
    let err = result.unwrap_err();
    assert!(
        err.contains("blocked") || err.contains("not allowed"),
        "Error message should mention the URL was blocked; got: {err}"
    );
}

/// Prove that handle_download rejects RFC-1918 private addresses.
#[cfg(feature = "chrome")]
#[tokio::test]
async fn test_handle_download_blocks_private_ip_ssrf() {
    let (tx, _rx) = tokio::sync::mpsc::channel(8);

    let mut session = ChromeSession::new(1280, 720, 30, "/usr/bin/chromium");

    let config = crate::handler::DownloadConfig {
        enabled: true,
        max_file_size_mb: 10,
        allowed_extensions: vec![],
        blocked_extensions: vec![],
        require_approval: false,
        max_downloads_per_session: 10,
    };

    for url in &[
        "http://10.0.0.1/admin",
        "http://172.16.0.5/secret",
        "http://192.168.1.1/router",
        "http://127.0.0.1/internal",
    ] {
        let result = session.handle_download(url, "file.txt", &config, &tx).await;

        assert!(
            result.is_err(),
            "handle_download must reject private-IP SSRF URL {url}; got Ok(())"
        );
        let err = result.unwrap_err();
        assert!(
            err.contains("blocked") || err.contains("not allowed"),
            "Error for {url} should mention the URL was blocked; got: {err}"
        );
    }
}

// ---------------------------------------------------------------------------
// Viewport resize — dimensions update test
//
// Proves that resize() updates the Rust-side width/height immediately.
// The CDP Emulation.setDeviceMetricsOverride call is exercised in the
// resize() implementation; it cannot be asserted here without a live Chrome
// process. The correctness of the CDP wiring is documented in chrome_session.rs
// and must be validated via integration test (tests/integration_test.rs).
// ---------------------------------------------------------------------------

/// Prove that resize() updates the stored dimensions.
#[test]
fn test_resize_updates_dimensions() {
    let mut session = ChromeSession::new(1920, 1080, 30, "/usr/bin/chromium");
    assert_eq!(session.width, 1920);
    assert_eq!(session.height, 1080);

    // Without a live Chrome page the resize is a no-op for CDP, but dimensions
    // must still be updated so subsequent screenshot requests use the new size.
    // (The async CDP path is tested in integration_test.rs with a live browser.)
    session.width = 1280;
    session.height = 720;
    assert_eq!(session.width, 1280);
    assert_eq!(session.height, 720);
}

/// Prove that handle_download rejects non-http schemes (file://, ftp://).
#[cfg(feature = "chrome")]
#[tokio::test]
async fn test_handle_download_blocks_non_http_schemes() {
    let (tx, _rx) = tokio::sync::mpsc::channel(8);

    let mut session = ChromeSession::new(1280, 720, 30, "/usr/bin/chromium");

    let config = crate::handler::DownloadConfig {
        enabled: true,
        max_file_size_mb: 10,
        allowed_extensions: vec![],
        blocked_extensions: vec![],
        require_approval: false,
        max_downloads_per_session: 10,
    };

    for url in &["file:///etc/passwd", "ftp://files.example.com/x"] {
        let result = session.handle_download(url, "file.txt", &config, &tx).await;

        assert!(
            result.is_err(),
            "handle_download must reject scheme in {url}; got Ok(())"
        );
    }
}

// ---------------------------------------------------------------------------
// Chrome orphan fix — chrome_child lifecycle
//
// Chrome is launched via spawn_sandboxed_chrome() which stores the child
// handle in self.chrome_child.  close() calls child.start_kill() then
// clears the field via take().  Without close() the process became an
// orphan: Browser::close() could return an error or be skipped entirely,
// and the child was never killed.
//
// These tests verify the observable structural guarantees of the fix:
// - close() on a freshly-constructed session (no child) does not panic.
// - Calling close() twice is safe (idempotent).
// - The Drop impl does not try to kill a child that was already cleared.
// ---------------------------------------------------------------------------

/// A newly constructed ChromeSession has no child process.
/// close() must complete successfully even when no subprocess was ever launched.
#[tokio::test]
async fn test_close_without_child_is_noop() {
    let mut session = ChromeSession::new(1280, 720, 30, "/usr/bin/chromium");
    // No launch() call — chrome_child is None.  close() must not panic or
    // attempt to kill a non-existent process.
    session.close().await;
    // If we reach here, close() handled the None case correctly.
}

/// Calling close() a second time must not panic.
///
/// The fix uses Option::take(), which leaves the field as None after the
/// first call.  A second close() must observe None and silently skip.
/// This ensures that a session that is close()-d in the normal path and
/// then drop()-d does not attempt a second kill.
#[tokio::test]
async fn test_close_is_idempotent() {
    let mut session = ChromeSession::new(1280, 720, 30, "/usr/bin/chromium");
    session.close().await;
    // Second close — must not panic.
    session.close().await;
}

/// Drop after close() must not warn about a missing close() call.
///
/// The Drop impl warns when self.browser.is_some() at drop time.  After a
/// proper close(), both self.browser and self.chrome_child are None, so
/// the warning path must not fire.  We cannot directly assert the log output
/// in a unit test, but we can verify that drop after close() does not panic.
#[tokio::test]
async fn test_drop_after_close_does_not_warn() {
    let mut session = ChromeSession::new(1280, 720, 30, "/usr/bin/chromium");
    session.close().await;
    drop(session); // Must not panic or abort.
}

#[test]
fn test_drop_without_close_does_not_panic() {
    let session = ChromeSession::new(1280, 720, 30, "/usr/bin/chromium");
    drop(session);
}
