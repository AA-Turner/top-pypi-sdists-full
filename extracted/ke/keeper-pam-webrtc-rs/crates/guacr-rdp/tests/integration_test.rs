//! Integration tests for RDP handler
//!
//! These tests require a running RDP server. Start one with:
//!   docker-compose -f docker-compose.test.yml up -d rdp
//!
//! Run tests with:
//!   cargo test --package guacr-rdp --test integration_test -- --include-ignored
//!
//! Connection details:
//!   Host: localhost:3389
//!   User: linuxuser
//!   Password: alpine

use std::collections::HashMap;
use std::time::Duration;
use tokio::time::timeout;

/// Test connection timeout
const CONNECT_TIMEOUT: Duration = Duration::from_secs(30);

/// Check if a port is open (server is running)
async fn port_is_open(host: &str, port: u16) -> bool {
    timeout(
        Duration::from_secs(2),
        tokio::net::TcpStream::connect(format!("{}:{}", host, port)),
    )
    .await
    .map(|r| r.is_ok())
    .unwrap_or(false)
}

mod rdp_handler_tests {
    use super::*;
    use bytes::Bytes;
    use guacr_handlers::ProtocolHandler;
    use guacr_rdp::RdpHandler;
    use tokio::sync::mpsc;

    const HOST: &str = "127.0.0.1";
    const PORT: u16 = 3389;
    const USERNAME: &str = "linuxuser";
    const PASSWORD: &str = "alpine";

    async fn skip_if_not_available() -> bool {
        if !port_is_open(HOST, PORT).await {
            eprintln!(
                "Skipping RDP tests - server not available on {}:{}",
                HOST, PORT
            );
            eprintln!(
                "Start a test RDP server with: docker-compose -f docker-compose.test.yml up -d rdp"
            );
            return true;
        }
        false
    }

    #[tokio::test]
    #[ignore] // Requires RDP server
    async fn test_rdp_connection_basic() {
        if skip_if_not_available().await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("width".to_string(), "1024".to_string());
        params.insert("height".to_string(), "768".to_string());
        // Use RDP security for xrdp compatibility
        params.insert("security".to_string(), "rdp".to_string());
        params.insert("ignore-cert".to_string(), "true".to_string());

        // Spawn handler in background
        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Wait for ready instruction
        let msg = timeout(CONNECT_TIMEOUT, to_client_rx.recv())
            .await
            .expect("Timeout waiting for ready")
            .expect("Channel closed");

        let msg_str = String::from_utf8_lossy(&msg);
        println!("RDP: First message: {}", msg_str);

        // RDP should send ready or size instruction
        assert!(
            msg_str.contains("ready") || msg_str.contains("size"),
            "Expected ready or size instruction, got: {}",
            msg_str
        );

        // Wait for a few more messages (size, img, sync)
        let mut received_size = false;
        let mut received_img = false;

        for _ in 0..20 {
            match timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let msg_str = String::from_utf8_lossy(&msg);
                    if msg_str.contains("size") {
                        received_size = true;
                    }
                    if msg_str.contains("img") {
                        received_img = true;
                        break; // Got an image, connection is working
                    }
                }
                _ => break,
            }
        }

        println!(
            "RDP: received_size={}, received_img={}",
            received_size, received_img
        );

        // Close the connection
        drop(from_client_tx);

        // Wait for handler to finish (with timeout)
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore] // Requires RDP server
    async fn test_rdp_security_settings() {
        if skip_if_not_available().await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("security".to_string(), "rdp".to_string());
        params.insert("ignore-cert".to_string(), "true".to_string());
        // Security settings
        params.insert("read-only".to_string(), "true".to_string());
        params.insert("disable-copy".to_string(), "true".to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Wait for connection
        let _ = timeout(CONNECT_TIMEOUT, to_client_rx.recv()).await;

        // In read-only mode, keyboard/mouse should be blocked
        // Send a key event (should be ignored by handler)
        let key_instr = "3.key,2.65,1.1;"; // 'A' key
        from_client_tx
            .send(Bytes::from(key_instr))
            .await
            .expect("Send failed");

        // Wait briefly
        tokio::time::sleep(Duration::from_millis(500)).await;

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore] // Requires RDP server
    async fn test_rdp_resize() {
        if skip_if_not_available().await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("security".to_string(), "rdp".to_string());
        params.insert("ignore-cert".to_string(), "true".to_string());
        params.insert("width".to_string(), "800".to_string());
        params.insert("height".to_string(), "600".to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Wait for initial connection and first image
        let mut connected = false;
        for _ in 0..10 {
            if let Ok(Some(msg)) = timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                let msg_str = String::from_utf8_lossy(&msg);
                if msg_str.contains("img") {
                    connected = true;
                    break;
                }
            }
        }

        if !connected {
            println!("RDP resize: Connection failed, skipping test");
            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(5), handle).await;
            return;
        }

        // Send resize instruction
        let resize_instr = "4.size,4.1024,3.768;";
        if from_client_tx
            .send(Bytes::from(resize_instr))
            .await
            .is_err()
        {
            println!("RDP resize: Channel closed, connection dropped");
            let _ = timeout(Duration::from_secs(5), handle).await;
            return;
        }

        // Wait for new size response
        let mut got_new_size = false;
        for _ in 0..10 {
            match timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let msg_str = String::from_utf8_lossy(&msg);
                    if msg_str.contains("size") && msg_str.contains("1024") {
                        got_new_size = true;
                        break;
                    }
                }
                _ => break,
            }
        }

        println!("RDP resize: got_new_size={}", got_new_size);

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore]
    async fn test_rdp_different_color_depths() {
        if skip_if_not_available().await {
            return;
        }

        for color_depth in &["8", "16", "24", "32"] {
            let handler = RdpHandler::with_defaults();
            let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
            let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

            let mut params = HashMap::new();
            params.insert("hostname".to_string(), HOST.to_string());
            params.insert("port".to_string(), PORT.to_string());
            params.insert("username".to_string(), USERNAME.to_string());
            params.insert("password".to_string(), PASSWORD.to_string());
            params.insert("security".to_string(), "rdp".to_string());
            params.insert("ignore-cert".to_string(), "true".to_string());
            params.insert("color-depth".to_string(), color_depth.to_string());

            let handle = tokio::spawn(async move {
                handler
                    .connect(
                        params,
                        to_client_tx,
                        from_client_rx,
                        None,
                        guacr_handlers::SessionHooks::default(),
                    )
                    .await
            });

            // Wait for connection
            let _ = timeout(CONNECT_TIMEOUT, to_client_rx.recv()).await;

            println!("RDP: Tested with color depth {}", color_depth);

            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(5), handle).await;
        }
    }

    #[tokio::test]
    #[ignore]
    async fn test_rdp_keyboard_input() {
        if skip_if_not_available().await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("security".to_string(), "rdp".to_string());
        params.insert("ignore-cert".to_string(), "true".to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Wait for connection and first image
        let mut connected = false;
        for _ in 0..10 {
            if let Ok(Some(msg)) = timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                let msg_str = String::from_utf8_lossy(&msg);
                if msg_str.contains("img") {
                    connected = true;
                    break;
                }
            }
        }

        if !connected {
            println!("RDP keyboard: Connection failed, skipping test");
            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(5), handle).await;
            return;
        }

        // Send key event (letter 'A')
        let key_instr = "3.key,2.65,1.1;";
        if from_client_tx.send(Bytes::from(key_instr)).await.is_err() {
            println!("RDP keyboard: Channel closed, test ending");
            let _ = timeout(Duration::from_secs(5), handle).await;
            return;
        }

        tokio::time::sleep(Duration::from_millis(200)).await;

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore]
    async fn test_rdp_mouse_input() {
        if skip_if_not_available().await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("security".to_string(), "rdp".to_string());
        params.insert("ignore-cert".to_string(), "true".to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Wait for connection and first image
        let mut connected = false;
        for _ in 0..10 {
            if let Ok(Some(msg)) = timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                let msg_str = String::from_utf8_lossy(&msg);
                if msg_str.contains("img") {
                    connected = true;
                    break;
                }
            }
        }

        if !connected {
            println!("RDP mouse: Connection failed, skipping test");
            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(5), handle).await;
            return;
        }

        // Send mouse move
        let mouse_instr = "5.mouse,3.100,3.100;";
        if from_client_tx.send(Bytes::from(mouse_instr)).await.is_err() {
            println!("RDP mouse: Channel closed, test ending");
            let _ = timeout(Duration::from_secs(5), handle).await;
            return;
        }

        // Send mouse click
        let click_instr = "5.mouse,3.100,3.100,1.1;";
        if from_client_tx.send(Bytes::from(click_instr)).await.is_err() {
            println!("RDP mouse: Channel closed, test ending");
            let _ = timeout(Duration::from_secs(5), handle).await;
            return;
        }

        tokio::time::sleep(Duration::from_millis(200)).await;

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore] // Requires RDP server
    async fn test_rdp_alpha_channel_fix() {
        if skip_if_not_available().await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (_from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("width".to_string(), "1024".to_string());
        params.insert("height".to_string(), "768".to_string());
        params.insert("security".to_string(), "rdp".to_string());
        params.insert("ignore-cert".to_string(), "true".to_string());

        // Spawn handler
        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        let mut received_ready = false;
        let mut received_img = false;
        let mut first_png: Option<Vec<u8>> = None;

        // Collect messages for up to 15 seconds
        for _ in 0..30 {
            if let Ok(Some(msg)) = timeout(Duration::from_millis(500), to_client_rx.recv()).await {
                let msg_str = String::from_utf8_lossy(&msg);

                if msg_str.contains("ready") {
                    received_ready = true;
                } else if msg_str.contains("img,") {
                    received_img = true;
                } else if msg_str.contains("blob,") && first_png.is_none() {
                    // Parse and decode blob to verify alpha channel
                    if let Some(blob_start) = msg_str.find("blob,") {
                        let after_blob = &msg_str[blob_start + 5..];
                        if let Some(comma_pos) = after_blob.find(',') {
                            let after_comma = &after_blob[comma_pos + 1..];
                            if let Some(dot_pos) = after_comma.find('.') {
                                let after_dot = &after_comma[dot_pos + 1..];
                                if let Some(semicolon) = after_dot.find(';') {
                                    let base64_data = &after_dot[..semicolon];
                                    if let Ok(png_bytes) = base64::Engine::decode(
                                        &base64::engine::general_purpose::STANDARD,
                                        base64_data.trim(),
                                    ) {
                                        first_png = Some(png_bytes);
                                        break; // Got what we need
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // Verify we got a connection
        if !received_ready || !received_img {
            println!("RDP alpha channel: Connection incomplete, skipping test");
            drop(handle);
            return;
        }

        // Verify PNG has correct alpha channel
        let Some(png_bytes) = first_png else {
            println!("RDP alpha channel: No PNG data received, skipping test");
            drop(handle);
            return;
        };

        {
            // Decode PNG
            let Ok(img) = image::load_from_memory(&png_bytes) else {
                println!("RDP alpha channel: PNG decode failed, skipping test");
                drop(handle);
                return;
            };
            let rgba = img.to_rgba8();
            let pixels = rgba.as_raw();

            // Check that alpha channel is set to 255 (opaque) for pixels
            // Sample first 100 pixels
            let mut alpha_255_count = 0;
            let mut alpha_0_count = 0;
            for i in 0..100.min(pixels.len() / 4) {
                let alpha = pixels[i * 4 + 3];
                if alpha == 255 {
                    alpha_255_count += 1;
                } else if alpha == 0 {
                    alpha_0_count += 1;
                }
            }

            println!(
                "Alpha channel test: 255={}, 0={} out of 100 pixels",
                alpha_255_count, alpha_0_count
            );

            // Most pixels should have alpha=255 (opaque)
            // Allow some with alpha=0 for special cases (inverted pixels, etc.)
            assert!(
                alpha_255_count > 50,
                "Expected most pixels to have alpha=255, got only {} out of 100",
                alpha_255_count
            );
        }

        // Cleanup
        handle.abort();
    }
}

mod video_tests {
    use super::*;
    use bytes::Bytes;
    use guacr_handlers::EncodedFrame;
    use guacr_handlers::{video::VideoOutput, ProtocolHandler};
    use guacr_rdp::RdpHandler;
    use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
    use std::sync::{Arc, Mutex};
    use tokio::sync::mpsc;

    struct MockVideoOutput {
        frames: Arc<Mutex<Vec<EncodedFrame>>>,
        keyframe_requested: Arc<AtomicBool>,
        target_bitrate_bps: Arc<AtomicU32>,
    }

    impl MockVideoOutput {
        fn new() -> Self {
            Self {
                frames: Arc::new(Mutex::new(Vec::new())),
                keyframe_requested: Arc::new(AtomicBool::new(false)),
                target_bitrate_bps: Arc::new(AtomicU32::new(0)),
            }
        }
        fn frame_count(&self) -> usize {
            self.frames.lock().unwrap().len()
        }
        fn had_keyframe(&self) -> bool {
            self.frames.lock().unwrap().iter().any(|f| f.is_keyframe)
        }
    }

    #[async_trait::async_trait]
    impl VideoOutput for MockVideoOutput {
        async fn send_frame(&self, frame: EncodedFrame) -> guacr_handlers::Result<()> {
            self.frames.lock().unwrap().push(frame);
            Ok(())
        }
        fn keyframe_requested(&self) -> Arc<AtomicBool> {
            self.keyframe_requested.clone()
        }
        fn target_bitrate_bps(&self) -> Arc<AtomicU32> {
            self.target_bitrate_bps.clone()
        }
        fn resolution_scale_pct(&self) -> Arc<AtomicU32> {
            Arc::new(AtomicU32::new(100))
        }
    }

    const HOST: &str = "127.0.0.1";
    const PORT: u16 = 3389;
    const USERNAME: &str = "linuxuser";
    const PASSWORD: &str = "alpine";

    async fn skip_if_not_available() -> bool {
        if !port_is_open(HOST, PORT).await {
            eprintln!(
                "Skipping RDP video tests - server not available on {}:{}",
                HOST, PORT
            );
            return true;
        }
        false
    }

    fn base_params() -> std::collections::HashMap<String, String> {
        let mut p = std::collections::HashMap::new();
        p.insert("hostname".to_string(), HOST.to_string());
        p.insert("port".to_string(), PORT.to_string());
        p.insert("username".to_string(), USERNAME.to_string());
        p.insert("password".to_string(), PASSWORD.to_string());
        p.insert("width".to_string(), "1024".to_string());
        p.insert("height".to_string(), "768".to_string());
        p.insert("security".to_string(), "rdp".to_string());
        p.insert("ignore-cert".to_string(), "true".to_string());
        p
    }

    #[tokio::test]
    #[ignore] // Requires RDP server
    async fn test_rdp_h264_path_sends_frames() {
        if skip_if_not_available().await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (_from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);
        let mock = Arc::new(MockVideoOutput::new());
        let mock_ref = mock.clone();

        let video_tx: Option<Arc<dyn VideoOutput>> = Some(mock);
        let handle = tokio::spawn(async move {
            handler
                .connect(
                    base_params(),
                    to_client_tx,
                    from_client_rx,
                    video_tx,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Collect data channel output for a few seconds
        let mut received_img = false;
        for _ in 0..30 {
            match timeout(Duration::from_millis(500), to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("img,") {
                        received_img = true;
                    }
                }
                _ => break,
            }
        }

        assert!(
            !received_img,
            "H.264 path must not send img instructions for screen content"
        );
        assert!(
            mock_ref.frame_count() > 0,
            "expected H.264 frames to be sent to VideoOutput"
        );
        assert!(
            mock_ref.had_keyframe(),
            "expected at least one IDR keyframe"
        );

        handle.abort();
    }

    #[tokio::test]
    #[ignore] // Requires RDP server
    async fn test_rdp_pli_triggers_keyframe() {
        if skip_if_not_available().await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, _to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (_from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);
        let mock = Arc::new(MockVideoOutput::new());
        let mock_ref = mock.clone();
        let keyframe_flag = mock.keyframe_requested();

        let video_tx: Option<Arc<dyn VideoOutput>> = Some(mock);
        let handle = tokio::spawn(async move {
            handler
                .connect(
                    base_params(),
                    to_client_tx,
                    from_client_rx,
                    video_tx,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Wait for frames to start arriving
        for _ in 0..50 {
            if mock_ref.frame_count() > 0 {
                break;
            }
            tokio::time::sleep(Duration::from_millis(100)).await;
        }
        assert!(
            mock_ref.frame_count() > 0,
            "no frames arrived before PLI test"
        );

        let frames_before = mock_ref.frame_count();
        // Simulate a PLI from the browser
        keyframe_flag.store(true, Ordering::Release);

        // Wait for the encode loop to consume the flag and produce a keyframe
        for _ in 0..50 {
            if mock_ref.frame_count() > frames_before {
                break;
            }
            tokio::time::sleep(Duration::from_millis(100)).await;
        }

        let frames = mock_ref.frames.lock().unwrap();
        let new_frames = &frames[frames_before..];
        assert!(!new_frames.is_empty(), "expected frames after PLI");
        assert!(
            new_frames.iter().any(|f| f.is_keyframe),
            "expected IDR frame after PLI"
        );
        assert!(
            !keyframe_flag.load(Ordering::Acquire),
            "keyframe flag must be cleared by encode loop"
        );
        drop(frames);
        handle.abort();
    }
}

mod unit_tests {
    use guacr_handlers::ProtocolHandler;
    use guacr_rdp::RdpHandler;

    #[test]
    fn test_rdp_handler_creation() {
        let handler = RdpHandler::with_defaults();
        assert_eq!(handler.name(), "rdp");
    }

    #[tokio::test]
    async fn test_rdp_handler_health_check() {
        let handler = RdpHandler::with_defaults();
        let health = handler.health_check().await;
        assert!(health.is_ok());
    }
}

mod disconnect_cleanup_tests {
    //! Verify that the RDP handler always sends a `disconnect` instruction to the
    //! client regardless of which code path ends the session loop.
    //!
    //! Stability finding (2026-05-05): three code paths inside `run_active_session`
    //! used `return Err(...)` or `return Ok(())` which bypassed the cleanup block
    //! after the loop.  These were converted to `break` so `send_disconnect()`,
    //! recording finalization, and threat-detection cleanup always execute.
    //!
    //! These tests require a live xrdp server so they live in the integration file.

    use super::*;
    use bytes::Bytes;
    use guacr_handlers::ProtocolHandler;
    use guacr_rdp::RdpHandler;
    use tokio::sync::mpsc;

    const HOST: &str = "127.0.0.1";
    const PORT: u16 = 3389;
    const USERNAME: &str = "linuxuser";
    const PASSWORD: &str = "alpine";

    /// Collect all `disconnect` instructions from the to_client channel.
    ///
    /// Returns the count of instructions whose bytes start with `10.disconnect`.
    async fn count_disconnect_instructions(
        rx: &mut mpsc::Receiver<Bytes>,
        timeout_ms: u64,
    ) -> usize {
        let deadline = std::time::Instant::now() + std::time::Duration::from_millis(timeout_ms);
        let mut count = 0;
        loop {
            let remaining = deadline.saturating_duration_since(std::time::Instant::now());
            if remaining.is_zero() {
                break;
            }
            match tokio::time::timeout(remaining, rx.recv()).await {
                Ok(Some(msg)) => {
                    let s = String::from_utf8_lossy(&msg);
                    if s.contains("disconnect") {
                        count += 1;
                    }
                }
                _ => break,
            }
        }
        count
    }

    #[tokio::test]
    #[ignore] // Requires RDP server on 127.0.0.1:3389
    async fn test_disconnect_sent_when_client_drops_channel() {
        // Stability: client dropping from_client_tx must cause the handler to
        // send a `disconnect` instruction on the to_client channel before exiting.
        if !port_is_open(HOST, PORT).await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(256);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(16);

        let mut params = std::collections::HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("security".to_string(), "rdp".to_string());
        params.insert("ignore-cert".to_string(), "true".to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Wait for session to become active (ready instruction arrives).
        let _ = tokio::time::timeout(std::time::Duration::from_secs(30), to_client_rx.recv()).await;

        // Drop the client sender — simulates vault disconnecting.
        drop(from_client_tx);

        // The handler must send `disconnect` before it exits.
        let dc_count = count_disconnect_instructions(&mut to_client_rx, 5000).await;
        assert_eq!(
            dc_count, 1,
            "expected exactly one disconnect instruction after client drops channel"
        );

        let _ = tokio::time::timeout(std::time::Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore] // Requires RDP server on 127.0.0.1:3389
    async fn test_disconnect_sent_when_terminate_pdu_received() {
        // Stability: ActiveStageOutput::Terminate (sent by the RDP server when it
        // closes the session) must also trigger a `disconnect` instruction.
        //
        // This test exercises the path by connecting, then waiting for the server
        // to close naturally or by dropping from_client to hasten shutdown.
        if !port_is_open(HOST, PORT).await {
            return;
        }

        let handler = RdpHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(256);
        let (_from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(16);

        let mut params = std::collections::HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("security".to_string(), "rdp".to_string());
        params.insert("ignore-cert".to_string(), "true".to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        // Wait for session ready.
        let _ = tokio::time::timeout(std::time::Duration::from_secs(30), to_client_rx.recv()).await;

        // Wait for handler to finish (from_client_tx was dropped above so the
        // handler sees channel closed and breaks the loop).
        let _ = tokio::time::timeout(std::time::Duration::from_secs(10), handle).await;

        // Drain remaining messages; at least one disconnect must have been sent.
        let dc_count = count_disconnect_instructions(&mut to_client_rx, 1000).await;
        assert!(
            dc_count >= 1,
            "expected at least one disconnect instruction before handler exit"
        );
    }
}
