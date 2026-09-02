/// Unit tests for RfbProxy::synthesize_handshake() and clean disconnect.
///
/// Uses tokio::io::duplex for in-process mock streams.
/// All tests run in CI — no external services required.
use base64::{engine::general_purpose::STANDARD as BASE64, Engine};
use bytes::Bytes;
use tokio::sync::mpsc;

use crate::rfb_proxy::{parse_vnc_input, RfbProxy};
use crate::vnc_protocol::VncPixelFormat;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/// Build a minimal vnc-input Guacamole instruction containing the given raw bytes.
fn make_vnc_input(raw: &[u8]) -> Bytes {
    let b64 = BASE64.encode(raw);
    let msg = format!("9.vnc-input,{}.{};", b64.len(), b64);
    Bytes::from(msg)
}

/// Decode a vnc-data instruction sent by the proxy into the raw bytes.
fn decode_vnc_data(instruction: &Bytes) -> Vec<u8> {
    let s = std::str::from_utf8(instruction).expect("vnc-data must be UTF-8");
    // Format: "8.vnc-data,<len>.<base64>;"
    let after = s
        .split_once("vnc-data,")
        .expect("expected vnc-data instruction")
        .1;
    let after_dot = after.split_once('.').expect("expected length.b64").1;
    let b64 = after_dot.trim_end_matches(';');
    BASE64.decode(b64).expect("valid base64")
}

fn default_pixel_format() -> VncPixelFormat {
    VncPixelFormat::default()
}

// ---------------------------------------------------------------------------
// synthesize_handshake tests
// ---------------------------------------------------------------------------

/// The proxy sends the RFB version banner first.
/// Verify the first vnc-data message is exactly "RFB 003.008\n".
#[tokio::test]
async fn test_synthesize_handshake_sends_rfb_version() {
    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    let (stream, _server_side) = tokio::io::duplex(1024);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        800,
        600,
        default_pixel_format(),
        "test-server".to_string(),
    );

    // Feed the expected client responses asynchronously so the handshake can proceed.
    tokio::spawn(async move {
        // Version response: 12 bytes
        from_client_tx
            .send(make_vnc_input(b"RFB 003.008\n"))
            .await
            .unwrap();
        // Security type choice: 1 byte (choose None = 0x01)
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
        // ClientInit: 1 byte (shared-flag = 1)
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
    });

    proxy
        .synthesize_handshake(&mut from_client_rx)
        .await
        .expect("synthesize_handshake must succeed");

    // First message must be the RFB version banner.
    let first_msg = to_client_rx.recv().await.expect("expected vnc-data");
    let decoded = decode_vnc_data(&first_msg);
    assert_eq!(
        decoded, b"RFB 003.008\n",
        "first vnc-data must be RFB version string"
    );
}

/// The proxy sends security types [0x01, 0x01] as the second message.
/// Verifies the SecurityType=None advertisement.
#[tokio::test]
async fn test_synthesize_handshake_sends_security_none() {
    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    let (stream, _server_side) = tokio::io::duplex(1024);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        800,
        600,
        default_pixel_format(),
        "test-server".to_string(),
    );

    tokio::spawn(async move {
        from_client_tx
            .send(make_vnc_input(b"RFB 003.008\n"))
            .await
            .unwrap();
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
    });

    proxy
        .synthesize_handshake(&mut from_client_rx)
        .await
        .expect("synthesize_handshake must succeed");

    // Drain all messages and find the security-types message [0x01, 0x01].
    let mut found = false;
    while let Ok(msg) = to_client_rx.try_recv() {
        let raw = decode_vnc_data(&msg);
        if raw == [0x01, 0x01] {
            found = true;
            break;
        }
    }
    assert!(found, "security types message [0x01, 0x01] must be sent");
}

/// The security result (OK = [0x00,0x00,0x00,0x00]) is forwarded to the browser.
#[tokio::test]
async fn test_synthesize_handshake_sends_security_result_ok() {
    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    let (stream, _server_side) = tokio::io::duplex(1024);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        1920,
        1080,
        default_pixel_format(),
        "desktop".to_string(),
    );

    tokio::spawn(async move {
        from_client_tx
            .send(make_vnc_input(b"RFB 003.008\n"))
            .await
            .unwrap();
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
    });

    proxy
        .synthesize_handshake(&mut from_client_rx)
        .await
        .expect("synthesize_handshake must succeed");

    let mut found_ok = false;
    while let Ok(msg) = to_client_rx.try_recv() {
        let raw = decode_vnc_data(&msg);
        if raw == [0x00, 0x00, 0x00, 0x00] {
            found_ok = true;
            break;
        }
    }
    assert!(
        found_ok,
        "security result OK ([0x00,0x00,0x00,0x00]) must be sent"
    );
}

/// ServerInit is the last message: dimensions match what was passed to RfbProxy::new().
#[tokio::test]
async fn test_synthesize_handshake_server_init_dimensions() {
    let width: u16 = 1280;
    let height: u16 = 720;
    let server_name = "my-vnc-box";

    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    let (stream, _server_side) = tokio::io::duplex(1024);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        width,
        height,
        default_pixel_format(),
        server_name.to_string(),
    );

    tokio::spawn(async move {
        from_client_tx
            .send(make_vnc_input(b"RFB 003.008\n"))
            .await
            .unwrap();
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
    });

    proxy
        .synthesize_handshake(&mut from_client_rx)
        .await
        .expect("synthesize_handshake must succeed");

    // Collect all messages; ServerInit is the last one.
    // ServerInit: 2(w)+2(h)+16(pf)+4(name_len)+name bytes
    let expected_len = 24 + server_name.len();
    let mut last: Option<Vec<u8>> = None;
    while let Ok(msg) = to_client_rx.try_recv() {
        last = Some(decode_vnc_data(&msg));
    }
    let server_init = last.expect("ServerInit must be the last vnc-data message");

    assert_eq!(
        server_init.len(),
        expected_len,
        "ServerInit length must be 24 + server_name.len()"
    );

    // First 2 bytes = width, next 2 = height (big-endian)
    let w = u16::from_be_bytes([server_init[0], server_init[1]]);
    let h = u16::from_be_bytes([server_init[2], server_init[3]]);
    assert_eq!(w, width, "ServerInit width must match");
    assert_eq!(h, height, "ServerInit height must match");
}

/// If the browser disconnects mid-handshake (channel closed), synthesize_handshake
/// returns an Err — it does NOT panic.
#[tokio::test]
async fn test_synthesize_handshake_browser_disconnect_returns_err() {
    let (to_client_tx, _to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    let (stream, _server_side) = tokio::io::duplex(1024);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        800,
        600,
        default_pixel_format(),
        "server".to_string(),
    );

    // Close the channel immediately — browser "disconnected" before handshake.
    drop(from_client_tx);

    let result = proxy.synthesize_handshake(&mut from_client_rx).await;
    assert!(
        result.is_err(),
        "synthesize_handshake must return Err on browser disconnect"
    );
    let err = result.unwrap_err();
    assert!(
        err.contains("disconnected"),
        "error message must mention 'disconnected', got: {}",
        err
    );
}

/// ClientInit byte value of 0 (non-shared) must not panic — the handshake continues normally.
/// The proxy does not interpret ClientInit; it just consumes the byte.
#[tokio::test]
async fn test_synthesize_handshake_non_shared_client_init_no_panic() {
    let (to_client_tx, _to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    let (stream, _server_side) = tokio::io::duplex(1024);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        800,
        600,
        default_pixel_format(),
        "srv".to_string(),
    );

    tokio::spawn(async move {
        from_client_tx
            .send(make_vnc_input(b"RFB 003.008\n"))
            .await
            .unwrap();
        from_client_tx.send(make_vnc_input(&[0x01])).await.unwrap();
        // ClientInit with shared=0 (non-shared session)
        from_client_tx.send(make_vnc_input(&[0x00])).await.unwrap();
    });

    // Must not panic — ClientInit value is not validated.
    let result = proxy.synthesize_handshake(&mut from_client_rx).await;
    assert!(
        result.is_ok(),
        "non-shared ClientInit (0x00) must not cause an error: {:?}",
        result
    );
}

// ---------------------------------------------------------------------------
// Clean disconnect tests
// ---------------------------------------------------------------------------

/// Client disconnect (from_client channel dropped) causes run() to exit cleanly.
/// The proxy must return Ok(()) and do so promptly (within the test timeout).
#[tokio::test]
async fn test_run_exits_on_client_disconnect() {
    let (to_client_tx, _to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    // duplex stream: server_side is unused (server never writes)
    let (stream, _server_side) = tokio::io::duplex(4096);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        800,
        600,
        default_pixel_format(),
        "server".to_string(),
    );

    // Drop the sender immediately — simulates browser disconnecting.
    drop(from_client_tx);

    // run() must return promptly with Ok(()) because from_client is closed.
    let result = tokio::time::timeout(
        std::time::Duration::from_secs(2),
        proxy.run(&mut from_client_rx),
    )
    .await
    .expect("run() must exit within 2 seconds when client disconnects");

    assert!(
        result.is_ok(),
        "run() must return Ok(()) on client disconnect, got: {:?}",
        result
    );
}

/// Server-side TCP EOF causes run() to exit cleanly with Ok(()).
#[tokio::test]
async fn test_run_exits_on_server_eof() {
    let (to_client_tx, _to_client_rx) = mpsc::channel::<Bytes>(64);
    let (_from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    // duplex: drop server_side immediately to cause EOF on client reads
    let (stream, server_side) = tokio::io::duplex(4096);
    // Close server side — reads on stream will return EOF
    drop(server_side);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        800,
        600,
        default_pixel_format(),
        "server".to_string(),
    );

    let result = tokio::time::timeout(
        std::time::Duration::from_secs(2),
        proxy.run(&mut from_client_rx),
    )
    .await
    .expect("run() must exit within 2 seconds on server EOF");

    assert!(
        result.is_ok(),
        "run() must return Ok(()) on server EOF, got: {:?}",
        result
    );
}

/// Server-side write succeeds: bytes from the VNC server are forwarded to to_client
/// as vnc-data instructions.
#[tokio::test]
async fn test_run_forwards_server_bytes_to_client() {
    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(64);
    let (_from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(8);
    let (stream, mut server_side) = tokio::io::duplex(4096);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        800,
        600,
        default_pixel_format(),
        "server".to_string(),
    );

    let test_payload = vec![0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x02];
    let payload_clone = test_payload.clone();

    tokio::spawn(async move {
        use tokio::io::AsyncWriteExt;
        server_side
            .write_all(&payload_clone)
            .await
            .expect("server write must succeed");
        // Close server side to terminate the proxy loop after forwarding.
        drop(server_side);
    });

    tokio::time::timeout(
        std::time::Duration::from_secs(2),
        proxy.run(&mut from_client_rx),
    )
    .await
    .expect("run() must exit within 2 seconds")
    .expect("run() must return Ok(())");

    // Collect all received messages and reassemble the raw bytes.
    let mut received: Vec<u8> = Vec::new();
    while let Ok(msg) = to_client_rx.try_recv() {
        received.extend_from_slice(&decode_vnc_data(&msg));
    }
    // The test payload must appear in the forwarded bytes.
    assert!(
        received
            .windows(test_payload.len())
            .any(|w| w == test_payload.as_slice()),
        "server bytes must be forwarded to to_client as vnc-data; got {:?}",
        received
    );
}

/// Client bytes (vnc-input) are forwarded to the VNC server as raw RFB bytes.
#[tokio::test]
async fn test_run_forwards_client_input_to_server() {
    let (to_client_tx, _to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, mut from_client_rx) = mpsc::channel::<Bytes>(64);
    let (stream, mut server_side) = tokio::io::duplex(4096);

    let mut proxy = RfbProxy::new(
        stream,
        to_client_tx,
        800,
        600,
        default_pixel_format(),
        "server".to_string(),
    );

    let input_bytes = vec![0xAA, 0xBB, 0xCC];
    let input_vnc_msg = make_vnc_input(&input_bytes);

    tokio::spawn(async move {
        // Send one vnc-input message, then drop the sender to end the session.
        from_client_tx
            .send(input_vnc_msg)
            .await
            .expect("send must succeed");
        drop(from_client_tx);
    });

    // Read bytes on server side concurrently with running the proxy.
    let read_task = tokio::spawn(async move {
        use tokio::io::AsyncReadExt;
        let mut buf = vec![0u8; 256];
        let mut received = Vec::new();
        loop {
            match server_side.read(&mut buf).await {
                Ok(0) => break,
                Ok(n) => received.extend_from_slice(&buf[..n]),
                Err(_) => break,
            }
        }
        received
    });

    tokio::time::timeout(
        std::time::Duration::from_secs(2),
        proxy.run(&mut from_client_rx),
    )
    .await
    .expect("run() must exit within 2 seconds")
    .expect("run() must return Ok(())");

    // Drop proxy to close stream, which will unblock the read_task.
    drop(proxy);

    let server_received = tokio::time::timeout(std::time::Duration::from_secs(2), read_task)
        .await
        .expect("read_task must complete")
        .expect("read_task must not panic");

    assert!(
        server_received
            .windows(input_bytes.len())
            .any(|w| w == input_bytes.as_slice()),
        "client vnc-input bytes must reach the VNC server; server got {:?}",
        server_received
    );
}

// ---------------------------------------------------------------------------
// parse_vnc_input edge cases (supplement existing tests in rfb_proxy.rs)
// ---------------------------------------------------------------------------

/// vnc-input with multiple instructions in one message: only the first is decoded.
/// This tests the split_once behavior — it stops at the first vnc-input.
#[test]
fn test_parse_vnc_input_empty_payload() {
    // Empty base64 = empty payload — should decode to empty Vec, not None.
    let b64 = BASE64.encode(b"");
    let instr = format!("9.vnc-input,{}.{};", b64.len(), b64);
    let result = parse_vnc_input(instr.as_bytes());
    assert_eq!(
        result,
        Some(vec![]),
        "empty payload must decode to empty vec"
    );
}

/// Binary content in vnc-input round-trips correctly.
#[test]
fn test_parse_vnc_input_binary_content() {
    let payload: Vec<u8> = (0u8..=255).collect();
    let b64 = BASE64.encode(&payload);
    let instr = format!("9.vnc-input,{}.{};", b64.len(), b64);
    let result = parse_vnc_input(instr.as_bytes()).expect("must parse");
    assert_eq!(
        result, payload,
        "binary payload must round-trip through vnc-input"
    );
}
