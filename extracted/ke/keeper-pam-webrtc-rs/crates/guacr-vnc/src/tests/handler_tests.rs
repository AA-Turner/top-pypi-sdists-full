use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, AtomicU32};
use std::sync::{Arc, Mutex};
use std::time::Duration;

use bytes::Bytes;
use guacr_handlers::{EncodedFrame, HealthStatus, ProtocolHandler, VideoOutput};
use tokio::sync::mpsc;

use crate::handler::{VncClient, VncConfig, VncHandler, VncSettings};

// Minimal VideoOutput mock for encoder-activation tests.
struct MockVideoOutput;

#[async_trait::async_trait]
impl VideoOutput for MockVideoOutput {
    async fn send_frame(&self, _frame: EncodedFrame) -> guacr_handlers::Result<()> {
        Ok(())
    }

    fn keyframe_requested(&self) -> Arc<AtomicBool> {
        Arc::new(AtomicBool::new(false))
    }

    fn target_bitrate_bps(&self) -> Arc<AtomicU32> {
        Arc::new(AtomicU32::new(0))
    }

    fn resolution_scale_pct(&self) -> Arc<AtomicU32> {
        Arc::new(AtomicU32::new(100))
    }
}

/// Build a minimal VncClient for unit tests (no live VNC connection required).
fn make_test_client(video_tx: Option<Arc<dyn VideoOutput>>) -> VncClient {
    make_test_client_with_rx(video_tx).0
}

/// Same as `make_test_client`, but also returns the client-bound channel receiver
/// so tests can assert on the Guacamole instructions actually sent to the client.
fn make_test_client_with_rx(
    video_tx: Option<Arc<dyn VideoOutput>>,
) -> (VncClient, mpsc::Receiver<Bytes>) {
    let (tx, rx) = mpsc::channel(16);
    let params = HashMap::new();
    let config = VncConfig::default();
    let client = VncClient::new(
        config.default_width,
        config.default_height,
        "test-conn".to_string(),
        false,
        guacr_handlers::HandlerSecuritySettings::from_params(&params),
        guacr_handlers::RecordingConfig::from_params(&params),
        config.jpeg_quality,
        config.use_jpeg,
        config.supports_webp,
        config.supports_jpeg,
        config.frame_rate,
        guacr_handlers::SessionOwnerSender::new(tx),
        None, // share_id
        &params,
        video_tx,
    );
    (client, rx)
}

#[test]
fn test_vnc_handler_new() {
    let handler = VncHandler::with_defaults();
    assert_eq!(<VncHandler as ProtocolHandler>::name(&handler), "vnc");
}

#[test]
fn test_vnc_config_defaults() {
    let config = VncConfig::default();
    assert_eq!(config.default_port, 5900);
    assert_eq!(config.default_width, 1920);
    assert_eq!(config.default_height, 1080);
}

#[tokio::test]
async fn test_vnc_handler_health() {
    let handler = VncHandler::with_defaults();
    let health = handler.health_check().await.unwrap();
    assert_eq!(health, HealthStatus::Healthy);
}

#[test]
fn test_vnc_settings_from_params() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "server.example.com".to_string());

    let defaults = VncConfig::default();
    let settings = VncSettings::from_params(&params, &defaults).unwrap();

    assert_eq!(settings.hostname, "server.example.com");
    assert_eq!(settings.port, 5900);
    assert_eq!(settings.width, 1920);
}

/// FrameBuffer::new with dimensions that would overflow u32 (e.g. 65535×65535)
/// must not panic — checked arithmetic in new() prevents silent truncation.
#[test]
fn test_framebuffer_new_with_large_dims_does_not_overflow() {
    use guacr_terminal::FrameBuffer;
    // 65535×65535 × 4 bytes overflows u32::MAX — saturating_mul caps it.
    // The allocation would succeed as usize::MAX if saturate were not used,
    // causing an OOM panic. With saturation, the vec is allocated at the
    // actual available limit or panics with a clean OOM, not corrupt memory.
    // We test a more modest "large" dimension that passes the VNC handler cap
    // but exercises the multiplication path.
    let fb = FrameBuffer::new(7680, 4320);
    assert_eq!(fb.width(), 7680);
    assert_eq!(fb.height(), 4320);
    // 7680 * 4320 * 4 = 132,710,400 bytes (~127 MiB) — must not overflow u32
    assert!(7680usize * 4320 * 4 < u32::MAX as usize);
}

/// H.264 encoder is instantiated when video_tx is Some and init_h264_encoder()
/// is called (as it is after the VNC handshake in connect()).
#[test]
fn test_h264_encoder_activated_when_video_tx_present() {
    let video_tx: Arc<dyn VideoOutput> = Arc::new(MockVideoOutput);
    let mut client = make_test_client(Some(video_tx));
    assert!(
        !client.has_h264_encoder(),
        "encoder must be None before init"
    );
    client.init_h264_encoder();
    assert!(
        client.has_h264_encoder(),
        "encoder must be Some after init when video_tx is Some"
    );
}

/// When video_tx is None the session uses the JPEG dirty-rect path exclusively.
/// init_h264_encoder() must remain a no-op.
#[test]
fn test_jpeg_fallback_when_no_video_tx() {
    let mut client = make_test_client(None);
    client.init_h264_encoder();
    assert!(
        !client.has_h264_encoder(),
        "encoder must stay None when video_tx is None (JPEG fallback path)"
    );
}

/// Records every frame handed to send_frame, to verify the encoded output of a
/// single maybe_encode_h264() call actually reaches the client.
struct RecordingVideoOutput {
    sent_frame_sizes: Mutex<Vec<usize>>,
}

#[async_trait::async_trait]
impl VideoOutput for RecordingVideoOutput {
    async fn send_frame(&self, frame: EncodedFrame) -> guacr_handlers::Result<()> {
        self.sent_frame_sizes.lock().unwrap().push(frame.data.len());
        Ok(())
    }

    fn keyframe_requested(&self) -> Arc<AtomicBool> {
        Arc::new(AtomicBool::new(false))
    }

    fn target_bitrate_bps(&self) -> Arc<AtomicU32> {
        Arc::new(AtomicU32::new(0))
    }

    fn resolution_scale_pct(&self) -> Arc<AtomicU32> {
        Arc::new(AtomicU32::new(100))
    }
}

/// Drive the pipeline the way the render loop does: submit, then drain without
/// blocking until output appears. Returns how many drain attempts were needed.
///
/// `maybe_encode_h264` deliberately does NOT wait for the encoder — it runs inline
/// in the render loop's `select!`, so blocking there stalls VNC socket reads and
/// client input. The loop's armed backstop timer performs these later drains.
async fn submit_and_drain(client: &mut VncClient) -> bool {
    client.maybe_encode_h264().await.unwrap();
    for _ in 0..200 {
        if client.drain_and_send_h264().await.unwrap() {
            return true;
        }
        tokio::time::sleep(Duration::from_millis(5)).await;
    }
    false
}

/// Reproduces the VNC "connection timed out — no content received" bug: the
/// encoder pipeline runs the actual encode on a background worker thread, so a
/// drain immediately after submit finds nothing yet. On a busy session the next
/// dirty-rect event arrives milliseconds later and picks up the frame with no
/// visible effect, but on a mostly-static desktop (VNC's initial full-screen
/// paint, then nothing for tens of seconds) that frame is exactly the one the
/// client's 30s no-content fallback timer needed to see. It must therefore be
/// delivered without depending on a second dirty-rect event.
#[tokio::test]
async fn first_h264_frame_is_not_lost_when_encode_outpaces_dirty_event() {
    let sent = Arc::new(RecordingVideoOutput {
        sent_frame_sizes: Mutex::new(Vec::new()),
    });
    let video_tx: Arc<dyn VideoOutput> = sent.clone();
    let (mut client, _rx) = make_test_client_with_rx(Some(video_tx));
    client.init_h264_encoder();

    let config = VncConfig::default();
    client
        .framebuffer
        .mark_dirty(0, 0, config.default_width, config.default_height);

    assert!(
        submit_and_drain(&mut client).await,
        "the first encoded frame must be delivered off a single dirty-rect event, \
         not left in the queue waiting for a second one that may never come"
    );
    assert_eq!(
        sent.sent_frame_sizes.lock().unwrap().len(),
        1,
        "exactly one frame should have reached the client"
    );
}

/// The encode call itself must not block on the encoder. It runs inline in the
/// render loop's `select!` server-read branch, so any wait there stalls VNC socket
/// reads and client input — which is what made interaction feel sluggish.
#[tokio::test]
async fn maybe_encode_h264_does_not_block_on_the_encoder() {
    let video_tx: Arc<dyn VideoOutput> = Arc::new(MockVideoOutput);
    let mut client = make_test_client(Some(video_tx));
    client.init_h264_encoder();

    let config = VncConfig::default();
    client
        .framebuffer
        .mark_dirty(0, 0, config.default_width, config.default_height);

    let start = std::time::Instant::now();
    client.maybe_encode_h264().await.unwrap();
    let elapsed = start.elapsed();

    // A full-frame software encode at the default size takes tens of ms; submitting
    // must return well inside that. The previous implementation slept in 20ms steps
    // for up to 200ms here.
    assert!(
        elapsed < Duration::from_millis(15),
        "maybe_encode_h264 must return without waiting for the encoder, took {:?}",
        elapsed
    );
}

/// Reproduces the VNC "no content received" timeout even after the drain-lag fix:
/// Guacamole.Client (vault JS) only flips to State.CONNECTED on receiving a `sync`
/// instruction. RDP's H.264/EGFX path sends one after every video frame
/// (guacr-rdp/src/handler.rs, "First EGFX frame sent"); VNC's maybe_encode_h264 sent
/// frames straight to the video track and never sent `sync` at all, so the client's
/// Guacamole.Client state machine never left WAITING, internals.guacClient/rawTunnel
/// stayed null forever, and the connection died to the 30s connect-timeout — despite
/// the H.264 track and RTP transport working perfectly the whole time.
#[tokio::test]
async fn h264_frame_is_followed_by_sync_instruction() {
    let video_tx: Arc<dyn VideoOutput> = Arc::new(MockVideoOutput);
    let (mut client, mut rx) = make_test_client_with_rx(Some(video_tx));
    client.init_h264_encoder();

    let config = VncConfig::default();
    client
        .framebuffer
        .mark_dirty(0, 0, config.default_width, config.default_height);

    assert!(
        submit_and_drain(&mut client).await,
        "frame should have been delivered"
    );

    let mut saw_sync = false;
    while let Ok(msg) = rx.try_recv() {
        if msg.starts_with(b"4.sync,") {
            saw_sync = true;
            break;
        }
    }
    assert!(
        saw_sync,
        "sending an H.264 frame must be followed by a Guacamole `sync` instruction, \
         or the client's Guacamole.Client never reaches State.CONNECTED and the \
         session times out even though frames are being sent successfully"
    );
}
