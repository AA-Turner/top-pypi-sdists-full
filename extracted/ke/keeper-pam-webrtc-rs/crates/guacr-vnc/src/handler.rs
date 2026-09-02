use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    // Connection utilities
    connect_tcp_with_timeout,
    is_mouse_event_allowed_readonly,
    // Recording helpers
    record_client_input as shared_record_client_input,
    // Session lifecycle
    send_disconnect,
    send_error_best_effort,
    send_name,
    send_ready,
    session_sharing,
    share_viewer,
    // Adaptive quality (bandwidth-aware quality adjustment, shared with RDP)
    AdaptiveQuality,
    // Cursor support
    CursorManager,
    // Drag detection (shared with RDP)
    DragDetector,
    EncodedFrame,
    EventBasedHandler,
    EventCallback,
    // Observability
    FpsCounter,
    HandlerError,
    // Security
    HandlerSecuritySettings,
    HandlerStats,
    HealthStatus,
    KeepAliveManager,
    MultiFormatRecorder,
    ProtocolHandler,
    // Recording
    RecordingConfig,
    RecordingDirection,
    SessionOwnerSender,
    SessionStats,
    SessionViewer,
    StandardCursor,
    // Sync flow control (prevents overwhelming slow clients, shared with RDP)
    SyncFlowControl,
    VideoOutput,
    DEFAULT_KEEPALIVE_INTERVAL_SECS,
};
use guacr_protocol::{
    format_chunked_blobs, format_img, format_instruction, GuacamoleParser,
    STATUS_UPSTREAM_NOT_FOUND,
};
use guacr_terminal::{CopyDetector, FrameBuffer, ScrollDetector, ScrollDirection};
use image::{ImageEncoder, RgbaImage};
use log::{debug, info, trace, warn};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{AsyncRead, AsyncWrite};
use tokio::sync::mpsc;

use crate::vnc_protocol::VncProtocol;

#[cfg(feature = "threat-detection")]
use guacr_threat_detection::ThreatDetector;

/// How long after submitting a frame to check the encoder pipeline for output when
/// no other render-loop event has occurred. Armed only while an encode is
/// outstanding, so an idle session runs no timer at all. Windows' 15-16ms timer
/// granularity rounds this up, which is fine for a backstop — the opportunistic
/// drain in `maybe_encode_h264` covers the busy case.
const H264_DRAIN_BACKSTOP: std::time::Duration = std::time::Duration::from_millis(5);

/// Bound on backstop re-arms. openh264 with `skip_frames` can legitimately hold a
/// frame back and produce no output, so an unbounded re-arm would spin.
const H264_DRAIN_MAX_ATTEMPTS: u8 = 20;

/// VNC protocol handler
///
/// Connects to VNC servers and provides remote desktop access via the Guacamole protocol.
///
/// ## IMPORTANT: Rendering Method
///
/// VNC MUST use PNG images (NOT Guacamole drawing instructions like rect/cfill).
/// Why:
/// - VNC streams framebuffer data: arbitrary graphics, photos, complex UI
/// - Drawing instructions only work for simple colored rectangles
/// - Cannot represent the visual complexity of VNC sessions
/// - Expected bandwidth: ~50-200KB/frame (acceptable for graphics-rich content)
#[derive(Clone)]
pub struct VncHandler {
    config: VncConfig,
}

#[derive(Debug, Clone)]
pub struct VncConfig {
    pub default_port: u16,
    pub default_width: u32,
    pub default_height: u32,
    /// JPEG quality for image encoding (1-100, default 85)
    /// Higher = better quality but larger files
    /// 85 is optimal balance for RDP-like performance
    pub jpeg_quality: u8,
    /// Use JPEG encoding instead of PNG (default true for bandwidth savings)
    pub use_jpeg: bool,
    /// Client supports WebP format (40% smaller than JPEG)
    pub supports_webp: bool,
    /// Client supports JPEG format
    pub supports_jpeg: bool,
    /// Frame rate limit in FPS (default 30)
    pub frame_rate: u32,
}

impl Default for VncConfig {
    fn default() -> Self {
        Self {
            default_port: 5900,
            default_width: 1920,
            default_height: 1080,
            jpeg_quality: 85,     // Same as RDP for consistency
            use_jpeg: true,       // Enable by default for bandwidth savings
            supports_webp: false, // Will be overridden by client capabilities
            supports_jpeg: false, // Will be overridden by client capabilities
            frame_rate: 30,       // 30 FPS default (can go up to 60)
        }
    }
}

impl VncHandler {
    pub fn new(config: VncConfig) -> Self {
        Self { config }
    }

    pub fn with_defaults() -> Self {
        Self::new(VncConfig::default())
    }
}

#[async_trait]
impl ProtocolHandler for VncHandler {
    fn name(&self) -> &str {
        "vnc"
    }

    fn as_event_based(&self) -> Option<&dyn EventBasedHandler> {
        Some(self)
    }

    async fn connect(
        &self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        mut from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> guacr_handlers::Result<()> {
        let conn_id = params.get("client_id").cloned().unwrap_or_default();
        info!("[conn={}] VNC handler starting connection", conn_id);

        // ── GUID-based viewer join (Phase 6b) ────────────────────────────────
        if params.contains_key("share_guid") {
            return guacr_handlers::share_viewer::check_viewer_join(
                &params,
                &to_client,
                from_client,
                &conn_id,
            )
            .await
            .unwrap_or(Ok(()));
        }

        // ── Session sharing — handle viewer and owner modes ──────────────────
        let share_id = params.get("share-id").cloned();
        let viewer_mode = params
            .get("viewer-mode")
            .map(|v| v == "true" || v == "1")
            .unwrap_or(false);

        if viewer_mode {
            let sid = share_id.as_deref().unwrap_or("");
            info!("[conn={conn_id}] VNC: viewer mode for session {sid:?}");
            let viewer = SessionViewer::join(sid, to_client.clone()).await;
            match viewer {
                Some(v) => {
                    tokio::spawn(async move { while from_client.recv().await.is_some() {} });
                    v.run().await;
                    return Ok(());
                }
                None => {
                    let msg = format!("No active session found for share-id: {sid}");
                    send_error_best_effort(&to_client, &msg, STATUS_UPSTREAM_NOT_FOUND).await;
                    return Err(HandlerError::ConnectionFailed(msg));
                }
            }
        }

        // Owner path: register session if share-id present.
        let mut owner_sender = SessionOwnerSender::new(to_client.clone());
        let (viewer_input_tx, viewer_input_rx) = tokio::sync::mpsc::unbounded_channel::<Bytes>();
        if let Some(ref sid) = share_id {
            match session_sharing::register(sid) {
                Ok(handle) => {
                    info!("[conn={conn_id}] VNC: registered shared session {sid:?}");
                    handle.set_viewer_input_channel(viewer_input_tx);
                    owner_sender.attach_session(handle);
                }
                Err(e) => {
                    warn!(
                        "[conn={conn_id}] VNC: failed to register session {sid:?}: {e} — continuing as standalone"
                    );
                }
            }
        }

        // Parse VNC settings
        let settings = VncSettings::from_params(&params, &self.config)
            .map_err(HandlerError::InvalidParameter)?;

        // Create VNC client
        let mut client = VncClient::new(
            settings.width,
            settings.height,
            conn_id.clone(),
            settings.read_only,
            settings.security.clone(),
            settings.recording_config.clone(),
            settings.jpeg_quality,
            settings.use_jpeg,
            settings.supports_webp,
            settings.supports_jpeg,
            settings.frame_rate,
            owner_sender,
            share_id.clone(),
            &params,
            video_tx,
        );

        // Wire viewer input channel so PRIV_CONTROL viewers can send key/mouse events.
        if share_id.is_some() {
            client.viewer_input_rx = Some(viewer_input_rx);
        }

        // Connect and run session
        client
            .connect(
                &settings.hostname,
                settings.port,
                settings.password.as_deref(),
                from_client,
                #[cfg(feature = "sftp")]
                Some(&settings),
                #[cfg(not(feature = "sftp"))]
                None,
            )
            .await
            .map_err(HandlerError::ConnectionFailed)?;

        info!("[conn={}] VNC handler connection ended", conn_id);
        Ok(())
    }

    async fn health_check(&self) -> guacr_handlers::Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    async fn stats(&self) -> guacr_handlers::Result<HandlerStats> {
        Ok(HandlerStats::default())
    }
}

// Event-based handler implementation
#[async_trait]
impl EventBasedHandler for VncHandler {
    fn name(&self) -> &str {
        "vnc"
    }

    async fn connect_with_events(
        &self,
        params: HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> Result<(), HandlerError> {
        // Use common event adapter helper (eliminates boilerplate)
        guacr_handlers::connect_with_event_adapter(
            |params, to_client, from_client, video_tx, _hooks| {
                self.connect(params, to_client, from_client, video_tx, _hooks)
            },
            params,
            callback,
            from_client,
            video_tx,
            _hooks,
            4096, // channel capacity
        )
        .await
    }
}

// ============================================================================
// VNC Settings - Parameter parsing and validation
// ============================================================================

/// VNC connection settings
#[derive(Debug, Clone)]
pub struct VncSettings {
    pub hostname: String,
    pub port: u16,
    pub password: Option<String>,
    pub width: u32,
    pub height: u32,
    /// Read-only mode - blocks keyboard/mouse input
    pub read_only: bool,
    /// Security settings
    pub security: HandlerSecuritySettings,
    /// Recording configuration
    pub recording_config: RecordingConfig,
    /// JPEG quality (1-100)
    pub jpeg_quality: u8,
    /// Use JPEG encoding (vs PNG)
    pub use_jpeg: bool,
    /// Client supports WebP format
    pub supports_webp: bool,
    /// Client supports JPEG format
    pub supports_jpeg: bool,
    /// Frame rate limit (FPS)
    pub frame_rate: u32,
}

impl VncSettings {
    pub fn from_params(
        params: &HashMap<String, String>,
        defaults: &VncConfig,
    ) -> Result<Self, String> {
        let conn_id = params.get("client_id").cloned().unwrap_or_default();
        let conn = guacr_handlers::ConnectionParameters::from_params(params, defaults.default_port)
            .map_err(|e| e.to_string())?;
        let hostname = conn.hostname;
        let port = conn.port;
        let password = conn.password;

        // IMPORTANT: Always use DEFAULT size during initialization (like guacd does)
        // The client will send a resize instruction with actual browser dimensions after handshake
        // This prevents "half screen" display issues
        info!(
            "[conn={}] VNC: Using default handshake size - will resize after client connects",
            conn_id
        );
        let width = defaults.default_width;
        let height = defaults.default_height;

        // Parse security settings
        let security = HandlerSecuritySettings::from_params(params);
        let read_only = security.read_only;
        info!(
            "[conn={}] VNC: Security settings - read_only={}, disable_copy={}, disable_paste={}",
            conn_id, security.read_only, security.disable_copy, security.disable_paste
        );

        // Parse recording configuration
        let recording_config = RecordingConfig::from_params(params);
        if recording_config.is_enabled() {
            info!(
                "[conn={}] VNC: Recording enabled - ses={}, asciicast={}, typescript={}",
                conn_id,
                recording_config.is_ses_enabled(),
                recording_config.is_asciicast_enabled(),
                recording_config.is_typescript_enabled()
            );
        }

        // Parse image encoding settings
        let jpeg_quality = params
            .get("jpeg_quality")
            .and_then(|q| q.parse().ok())
            .unwrap_or(defaults.jpeg_quality)
            .clamp(1, 100);

        let use_jpeg = params
            .get("use_jpeg")
            .map(|v| v == "true")
            .unwrap_or(defaults.use_jpeg);

        let frame_rate = params
            .get("frame_rate")
            .and_then(|f| f.parse().ok())
            .unwrap_or(defaults.frame_rate)
            .clamp(1, 60);

        // Parse client image format support
        let (supports_webp, supports_jpeg) = guacr_handlers::parse_image_formats(params, "VNC");

        info!(
            "[conn={}] VNC: Image encoding - use_jpeg={}, quality={}, frame_rate={} FPS",
            conn_id, use_jpeg, jpeg_quality, frame_rate
        );

        info!(
            "[conn={}] VNC Settings: {}:{}, {}x{}, read_only={}",
            conn_id, hostname, port, width, height, read_only
        );

        Ok(Self {
            hostname,
            port,
            password,
            width,
            height,
            read_only,
            security,
            recording_config,
            jpeg_quality,
            use_jpeg,
            supports_webp,
            supports_jpeg,
            frame_rate,
        })
    }
}

// ============================================================================
// VNC Client - Connection and event loop
// ============================================================================

/// VNC client wrapper for VNC connections
pub(crate) struct VncClient {
    /// Decoded framebuffer — updated by read_framebuffer_update on every FBU.
    pub(crate) framebuffer: FrameBuffer,
    /// Stream ID for Guacamole image instructions (wrapping counter).
    stream_id: u32,
    width: u32,
    height: u32,
    /// Connection ID for log correlation
    conn_id: String,
    /// Read-only mode - blocks keyboard/mouse input
    read_only: bool,
    /// Security settings (includes connection timeout)
    security: HandlerSecuritySettings,
    /// Active recorder
    recorder: Option<MultiFormatRecorder>,
    /// Scroll detector for bandwidth optimization (shared with RDP)
    scroll_detector: ScrollDetector,
    /// Drag detector for copy optimization during window moves (shared with RDP)
    drag_detector: DragDetector,
    /// Cell-based copy detector for detecting moved pixel content (shared with RDP)
    /// Currently disabled: tile fragmentation causes visual artifacts during drag.
    #[allow(dead_code)]
    copy_detector: CopyDetector,
    /// Use JPEG encoding (vs PNG)
    use_jpeg: bool,
    /// Client supports WebP format
    supports_webp: bool,
    /// Client supports JPEG format
    supports_jpeg: bool,
    /// Frame rate limit (FPS) - server controls rate for VNC; stored for future use
    _frame_rate: u32,
    #[cfg(feature = "sftp")]
    #[allow(dead_code)]
    sftp_session: Option<russh_sftp::client::SftpSession>,
    /// Cursor manager for client-side cursor rendering (matches KCM behavior)
    cursor_manager: CursorManager,
    /// VNC pixel format (needed for cursor parsing)
    pixel_format: Option<crate::vnc_protocol::VncPixelFormat>,
    /// Per-session ZRLE zlib decompression state (T-013 to T-015).
    /// The zlib stream is continuous across FBU messages within a session.
    zrle_state: crate::encodings::ZrleState,
    /// Adaptive quality manager (bandwidth-aware quality adjustment, shared with RDP)
    adaptive_quality: AdaptiveQuality,
    /// Sync flow control (prevents overwhelming slow clients, shared with RDP)
    sync_control: SyncFlowControl,
    /// Instant at which the most-recent sync was sent; used to drive check_timeout.
    sync_sent_at: Option<std::time::Instant>,
    owner_sender: SessionOwnerSender,
    /// Session share-id for owner_disconnect on session end (None = not shared).
    share_id: Option<String>,
    /// WebRTC video track for H.264 output (None = Guacamole JPEG path)
    video_tx: Option<Arc<dyn VideoOutput>>,
    /// Software H.264 encoder (present when video_tx is Some)
    /// Dedicated-thread encode pipeline (shared with guacr-rdp). Replaces the
    /// former in-loop SoftwareH264Encoder: gives VNC real bitrate adaptation,
    /// BWE resolution tiers, a recycled frame-buffer pool, the hardware-encoder
    /// cascade, and moves encode off this session's async loop.
    h264_pipeline: Option<guacr_encoder::pipeline::EncoderPipeline>,
    /// Last bitrate pushed to the encoder, so BWE updates only reconfigure on change.
    h264_last_bitrate_bps: u32,
    /// When set, the render loop should re-check the pipeline for finished output at
    /// this instant. Armed on submit, cleared once a frame is drained. See
    /// `H264_DRAIN_BACKSTOP`.
    h264_drain_deadline: Option<tokio::time::Instant>,
    /// Backstop re-arms used so far for the outstanding encode.
    h264_drain_attempts: u8,
    /// Per-session observability counters
    stats: SessionStats,
    /// FPS counter (logs FPS every 5 seconds)
    fps_counter: FpsCounter,
    /// AI threat detector for graphical sessions — Some when threat detection is enabled.
    /// Initialized from params; None when the feature is disabled or baml endpoint absent.
    #[cfg(feature = "threat-detection")]
    threat_detector: Option<Arc<ThreatDetector>>,
    /// Per-session ID for threat detection state tracking.
    #[cfg(feature = "threat-detection")]
    threat_session_id: String,
    /// Keystrokes buffered since the last analyze_screenshot trigger.
    /// Cleared after each screenshot analysis call.
    #[cfg(feature = "threat-detection")]
    threat_keystroke_buffer: String,
    /// Viewer key/mouse input channel (Phase 6b). None for standalone sessions.
    viewer_input_rx: Option<tokio::sync::mpsc::UnboundedReceiver<Bytes>>,
}

impl VncClient {
    /// Returns true when the H.264 encoder has been instantiated.
    /// Used by tests to verify encoder activation without a live VNC connection.
    #[cfg(test)]
    pub(crate) fn has_h264_encoder(&self) -> bool {
        self.h264_pipeline.is_some()
    }

    #[allow(clippy::too_many_arguments)]
    pub(crate) fn new(
        width: u32,
        height: u32,
        conn_id: String,
        read_only: bool,
        security: HandlerSecuritySettings,
        recording_config: RecordingConfig,
        jpeg_quality: u8,
        use_jpeg: bool,
        supports_webp: bool,
        supports_jpeg: bool,
        frame_rate: u32,
        owner_sender: SessionOwnerSender,
        share_id: Option<String>,
        params: &HashMap<String, String>,
        video_tx: Option<Arc<dyn VideoOutput>>,
    ) -> Self {
        // Initialize recording if enabled
        let recorder = if recording_config.is_enabled() {
            match MultiFormatRecorder::new(
                &recording_config,
                params,
                "vnc",
                width as u16,
                height as u16,
            ) {
                Ok(rec) => {
                    info!("[conn={}] VNC: Session recording initialized", conn_id);
                    Some(rec)
                }
                Err(e) => {
                    warn!(
                        "[conn={}] VNC: Failed to initialize recording: {}",
                        conn_id, e
                    );
                    None
                }
            }
        } else {
            None
        };

        #[cfg(feature = "threat-detection")]
        let threat_detector = ThreatDetector::from_params(params, "VNC");
        #[cfg(feature = "threat-detection")]
        let threat_session_id = uuid::Uuid::new_v4().to_string();

        Self {
            framebuffer: FrameBuffer::new(width, height),
            stream_id: 1,
            width,
            height,
            conn_id,
            read_only,
            security,
            recorder,
            scroll_detector: ScrollDetector::new(width, height),
            drag_detector: DragDetector::new(width, height),
            copy_detector: CopyDetector::new(width, height),
            use_jpeg,
            supports_webp,
            supports_jpeg,
            _frame_rate: frame_rate,
            #[cfg(feature = "sftp")]
            sftp_session: None,
            cursor_manager: CursorManager::new(supports_jpeg, supports_webp, jpeg_quality),
            pixel_format: None,
            zrle_state: crate::encodings::ZrleState::new(),
            adaptive_quality: AdaptiveQuality::new(jpeg_quality),
            sync_control: SyncFlowControl::new(),
            sync_sent_at: None,
            owner_sender,
            share_id,
            h264_pipeline: None,
            h264_last_bitrate_bps: 0,
            h264_drain_deadline: None,
            h264_drain_attempts: 0,
            video_tx,
            stats: SessionStats::new("vnc"),
            fps_counter: FpsCounter::new(),
            #[cfg(feature = "threat-detection")]
            threat_detector,
            #[cfg(feature = "threat-detection")]
            threat_session_id,
            #[cfg(feature = "threat-detection")]
            threat_keystroke_buffer: String::new(),
            viewer_input_rx: None,
        }
    }

    /// Initialise the H.264 encoder when a video track is available.
    ///
    /// Must be called after the VNC handshake completes so `self.width` and
    /// `self.height` reflect the real server dimensions.  When `video_tx` is
    /// `None` this is a no-op and the session uses the JPEG dirty-rect path.
    pub(crate) fn init_h264_encoder(&mut self) {
        if self.video_tx.is_none() {
            return;
        }
        match guacr_encoder::make_encoder(self.width, self.height) {
            Ok(enc) => {
                info!(
                    "[conn={}] VNC: H.264 encoder initialised ({}x{})",
                    self.conn_id, self.width, self.height
                );
                self.h264_pipeline = Some(guacr_encoder::pipeline::EncoderPipeline::new(enc));
            }
            Err(e) => {
                warn!(
                    "[conn={}] VNC: H.264 encoder init failed, falling back to JPEG: {}",
                    self.conn_id, e
                );
            }
        }
    }

    /// Encode RGBA framebuffer data as JPEG
    ///
    /// Converts RGBA pixels to RGB and encodes as JPEG with specified quality.
    /// This provides 5-10x bandwidth reduction compared to PNG encoding.
    ///
    /// # Arguments
    ///
    /// * `data` - RGBA pixel data (4 bytes per pixel)
    /// * `width` - Image width in pixels
    /// * `height` - Image height in pixels
    /// * `quality` - JPEG quality (1-100, higher = better quality)
    ///
    /// # Returns
    ///
    /// JPEG-encoded image data
    fn encode_jpeg(data: &[u8], width: u32, height: u32, quality: u8) -> Result<Vec<u8>, String> {
        let img = RgbaImage::from_raw(width, height, data.to_vec())
            .ok_or_else(|| "Invalid image dimensions".to_string())?;

        let rgb_img = image::DynamicImage::ImageRgba8(img).to_rgb8();

        let mut jpeg_data = Vec::new();
        let encoder = image::codecs::jpeg::JpegEncoder::new_with_quality(&mut jpeg_data, quality);
        encoder
            .write_image(&rgb_img, width, height, image::ExtendedColorType::Rgb8)
            .map_err(|e| format!("JPEG encode failed: {}", e))?;

        Ok(jpeg_data)
    }

    /// Encode RGBA data as WebP (lossy)
    fn encode_webp_lossy(
        data: &[u8],
        width: u32,
        height: u32,
        quality: f32,
    ) -> Result<Vec<u8>, String> {
        use webp::{Encoder, WebPMemory};

        let encoder = Encoder::from_rgba(data, width, height);
        let webp: WebPMemory = encoder.encode(quality);
        Ok(webp.to_vec())
    }

    /// Encode RGBA data as WebP (lossless)
    fn encode_webp_lossless(data: &[u8], width: u32, height: u32) -> Result<Vec<u8>, String> {
        use webp::{Encoder, WebPMemory};

        let encoder = Encoder::from_rgba(data, width, height);
        let webp: WebPMemory = encoder.encode_lossless();
        Ok(webp.to_vec())
    }

    /// Encode a framebuffer region using configured encoding (WebP, JPEG, or PNG)
    ///
    /// Uses WebP by default for 40% bandwidth savings vs JPEG, with fallback.
    /// Returns `(bytes, format)` — format: 0=PNG, 1=JPEG, 2=WebP.
    fn encode_region(&mut self, rect: guacr_terminal::FrameRect) -> Result<(Vec<u8>, u8), String> {
        let total_pixels = self.width * self.height;
        let rect_pixels = rect.width * rect.height;
        let is_large_update = rect_pixels > total_pixels / 10;
        let adaptive_quality = self.adaptive_quality.calculate_quality();

        if self.supports_webp {
            let region_pixels = self.framebuffer.get_region_pixels(rect);
            let bytes = if is_large_update {
                let quality = adaptive_quality as f32 / 100.0;
                Self::encode_webp_lossy(&region_pixels, rect.width, rect.height, quality)?
            } else {
                Self::encode_webp_lossless(&region_pixels, rect.width, rect.height)?
            };
            Ok((bytes, 2))
        } else if self.supports_jpeg && self.use_jpeg {
            let region_pixels = self.framebuffer.get_region_pixels(rect);
            let bytes =
                Self::encode_jpeg(&region_pixels, rect.width, rect.height, adaptive_quality)?;
            Ok((bytes, 1))
        } else {
            let bytes = self
                .framebuffer
                .encode_region(rect)
                .map_err(|e| format!("PNG encoding failed: {}", e))?;
            Ok((bytes, 0))
        }
    }

    /// Send sync instruction for frame timing and flow control
    ///
    /// Helps with session recording playback timing and client-side frame synchronization.
    /// Also enables flow control to prevent overwhelming slow clients.
    /// Send instruction to client and record it (if recording is enabled)
    async fn send_and_record(&mut self, instruction: &str) -> Result<(), String> {
        self.fps_counter
            .record_frame(&mut self.stats, instruction.len(), &self.conn_id);
        let bytes = Bytes::from(instruction.to_string());
        if let Some(ref mut rec) = self.recorder {
            if let Err(e) = rec.record_instruction(RecordingDirection::ServerToClient, &bytes) {
                warn!("Failed to record server instruction: {}", e);
            }
        }
        self.owner_sender
            .send(bytes)
            .await
            .map_err(|e| format!("Send failed: {}", e))
    }

    /// Record client input instruction (if recording is enabled)
    fn record_client_input(&mut self, instruction: &Bytes) {
        self.stats.record_input();
        shared_record_client_input(&mut self.recorder, instruction);
    }

    async fn send_sync(&mut self) -> Result<(), String> {
        let timestamp = guacr_terminal::current_time_millis();

        let sync_instr = format!("4.sync,{}.{};", timestamp.to_string().len(), timestamp);

        self.send_and_record(&sync_instr).await?;

        // Store pending sync for flow control (prevents overwhelming slow clients)
        self.sync_control.set_pending_sync(timestamp);
        self.sync_sent_at = Some(std::time::Instant::now());

        Ok(())
    }

    pub(crate) async fn maybe_encode_h264(&mut self) -> Result<(), String> {
        if self.framebuffer.dirty_rects().is_empty() {
            return Ok(());
        }

        if self.h264_pipeline.is_none() {
            return Ok(());
        }
        let video_tx = match self.video_tx.as_ref() {
            Some(v) => v.clone(),
            None => return Ok(()),
        };
        use std::sync::atomic::Ordering;

        // Submit in a scope so the &EncoderPipeline (not Sync, due to its inner
        // mpsc::Receiver) is dropped before the awaits below — same pattern as
        // guacr-rdp.
        {
            let Some(pipeline) = self.h264_pipeline.as_ref() else {
                return Ok(());
            };

            let force_keyframe = video_tx.keyframe_requested().swap(false, Ordering::AcqRel);

            // Real bitrate adaptation. The former SoftwareH264Encoder::update_bitrate
            // was a no-op, so VNC read the BWE estimate and then discarded it — every
            // session encoded at a fixed 2 Mbps. The pipeline's encoders implement this
            // for real (openh264 via ENCODER_OPTION_BITRATE).
            let bps = video_tx.target_bitrate_bps().load(Ordering::Relaxed);
            if bps > 0 && bps != self.h264_last_bitrate_bps {
                pipeline.set_target_bitrate(bps);
                self.h264_last_bitrate_bps = bps;
                debug!(
                    "[conn={}] VNC: encoder target bitrate -> {:.2} Mbps",
                    self.conn_id,
                    bps as f64 / 1_000_000.0
                );
            }

            // BWE resolution tier (100 -> 75 -> 50 -> 33 % of natural size). The
            // pipeline worker rebuilds the encoder off this loop when geometry changes.
            let scale_pct = video_tx.resolution_scale_pct().load(Ordering::Relaxed);
            let (enc_w, enc_h) =
                guacr_handlers::video::scaled_encode_size(self.width, self.height, scale_pct);

            // Snapshot into a pooled buffer — replaces get_all_pixels(), which
            // allocated a full framebuffer copy on every frame.
            let mut data = pipeline.acquire_frame_buffer();
            let src = self.framebuffer.data();
            if (enc_w, enc_h) == (self.width, self.height) {
                data.extend_from_slice(src);
            } else {
                guacr_encoder::scale_rgba(src, self.width, self.height, &mut data, enc_w, enc_h);
            }

            pipeline.submit(
                guacr_encoder::RgbaFrame {
                    data,
                    width: enc_w,
                    height: enc_h,
                    timestamp_us: guacr_terminal::current_time_millis() * 1000,
                },
                force_keyframe,
            );
        }; // pipeline reference dropped here

        self.framebuffer.clear_dirty();

        // The encode runs on the pipeline's worker thread and is not finished yet.
        // Arm the render loop's backstop drain so the result is delivered even when
        // no further loop event occurs — a static desktop can go tens of seconds
        // between dirty-rect events, and the last frame of an interaction burst has
        // nothing following it at all.
        self.h264_drain_deadline = Some(tokio::time::Instant::now() + H264_DRAIN_BACKSTOP);
        self.h264_drain_attempts = 0;

        // Opportunistic non-blocking drain. In steady state this collects the
        // *previous* frame's output, which is what keeps submit and encode
        // pipelined instead of serialized.
        if self.drain_and_send_h264().await? {
            self.h264_drain_deadline = None;
        }

        Ok(())
    }

    /// Forward any completed H.264 frames to the video track. Never blocks waiting
    /// on the encoder: callers are the render loop's own events and its backstop
    /// timer, so waiting here would stall VNC socket reads and client input.
    ///
    /// Returns whether at least one frame was sent.
    pub(crate) async fn drain_and_send_h264(&mut self) -> Result<bool, String> {
        let video_tx = match self.video_tx.as_ref() {
            Some(v) => v.clone(),
            None => return Ok(false),
        };

        let encoded_frames: Vec<EncodedFrame> = {
            let Some(pipeline) = self.h264_pipeline.as_ref() else {
                return Ok(false);
            };
            pipeline.drain()
        }; // pipeline reference dropped before the awaits below

        if encoded_frames.is_empty() {
            return Ok(false);
        }

        for frame in encoded_frames {
            let frame_len = frame.data.len();
            video_tx
                .send_frame(frame)
                .await
                .map_err(|e| format!("H.264 send_frame failed: {}", e))?;
            debug!(
                "[conn={}] VNC: sent H.264 frame ({} bytes) to video track",
                self.conn_id, frame_len
            );
        }

        // Guacamole.Client (vault JS) only reaches State.CONNECTED on receiving a
        // `sync` instruction — without this, internals.guacClient/rawTunnel never
        // populate client-side and the session times out after 30s even though the
        // H.264 track and RTP transport are working correctly. Mirrors guacr-rdp's
        // EGFX video path, which sends `sync` after every video_tx.send_frame().
        self.send_sync().await?;

        Ok(true)
    }

    async fn connect(
        &mut self,
        hostname: &str,
        port: u16,
        password: Option<&str>,
        mut from_client: mpsc::Receiver<Bytes>,
        #[cfg(feature = "sftp")] _settings: Option<&VncSettings>,
        #[cfg(not(feature = "sftp"))] _settings: Option<&VncSettings>,
    ) -> Result<(), String> {
        info!(
            "[conn={}] VNC: Connecting to {}:{} (timeout: {}s)",
            self.conn_id, hostname, port, self.security.connection_timeout_secs
        );

        // Connect with timeout (matches guacd behavior)
        let mut stream =
            connect_tcp_with_timeout((hostname, port), self.security.connection_timeout_secs)
                .await
                .map_err(|e| format!("{}", e))?;

        info!("[conn={}] VNC: TCP connection established", self.conn_id);

        let (_version, pixel_format, server_width, server_height, server_name) =
            VncProtocol::handshake(&mut stream, password)
                .await
                .map_err(|e| format!("VNC handshake failed: {}", e))?;

        info!(
            "[conn={}] VNC: Handshake complete - {}x{}, server: {}",
            self.conn_id, server_width, server_height, server_name
        );

        // Cap server dimensions: 65535×65535 would overflow u32 in FrameBuffer::new
        // (width*height*4 exceeds u32::MAX). A 8K framebuffer (7680×4320) is
        // a reasonable maximum for any PAM session.
        const MAX_VNC_DIM: u16 = 7680;
        if server_width > MAX_VNC_DIM || server_height > MAX_VNC_DIM {
            return Err(format!(
                "VNC server dimensions {}×{} exceed maximum {}×{}",
                server_width, server_height, MAX_VNC_DIM, MAX_VNC_DIM
            ));
        }
        self.width = server_width as u32;
        self.height = server_height as u32;
        self.framebuffer = FrameBuffer::new(self.width, self.height);
        self.pixel_format = Some(pixel_format);

        // Instantiate the H.264 encoder when a video track is available.
        // The encoder must be created after the handshake so we have the real server
        // dimensions. When video_tx is None the session falls back to JPEG dirty-rects.
        self.init_h264_encoder();

        // Send ready and name instructions to client
        send_ready(self.owner_sender.transport_sender(), "vnc-ready")
            .await
            .map_err(|e| e.to_string())?;
        send_name(self.owner_sender.transport_sender(), "VNC")
            .await
            .map_err(|e| e.to_string())?;

        let size_instr = format_instruction(
            "size",
            &["0", &self.width.to_string(), &self.height.to_string()],
        );
        self.send_and_record(&size_instr).await?;

        // Set initial cursor to pointer (matches KCM/guacamole behavior)
        if !self.read_only {
            let cursor_instrs = self
                .cursor_manager
                .send_standard_cursor(StandardCursor::Pointer)
                .map_err(|e| format!("Failed to generate cursor: {}", e))?;
            for instr in cursor_instrs {
                self.send_and_record(&instr).await?;
            }
            info!("[conn={}] VNC: Initial cursor set to pointer", self.conn_id);
        }

        // Direct render loop: decode server framebuffer updates and send
        // Guacamole image instructions (or H.264 frames when video_tx is Some).
        // noVNC proxy is no longer used; all RFB framing is handled here.
        info!(
            "[conn={}] VNC: Starting direct render loop (h264={})",
            self.conn_id,
            self.h264_pipeline.is_some()
        );

        // Advertise supported encodings and request the first frame.
        VncProtocol::send_set_encodings(&mut stream, /* enable_cursor= */ !self.read_only)
            .await
            .map_err(|e| format!("SetEncodings failed: {e}"))?;

        VncProtocol::send_framebuffer_update_request(
            &mut stream,
            false, // non-incremental: full screen for first frame
            0,
            0,
            self.width as u16,
            self.height as u16,
        )
        .await
        .map_err(|e| format!("Initial FBU request failed: {e}"))?;

        // Keep-alive, unconditional and on the same 5s cadence as every other protocol
        // handler (RDP, SSH, telnet, serial). VNC was the only handler without one: a
        // viewer that stopped reading was detected solely via the sync timeout, which is
        // only evaluated when a client message arrives - so an idle-but-dead viewer held
        // the session (and any JIT account behind it) open indefinitely.
        let mut keepalive = KeepAliveManager::new(DEFAULT_KEEPALIVE_INTERVAL_SECS);
        let mut keepalive_interval = tokio::time::interval(std::time::Duration::from_secs(
            DEFAULT_KEEPALIVE_INTERVAL_SECS,
        ));
        keepalive_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        // Main loop: interleave server frame reads with client input handling.
        // read_framebuffer_update() consumes the full FBU body and sends the next
        // incremental request when it returns, so we only need to drive client input
        // concurrently; no explicit FBU re-request is needed here.
        loop {
            use tokio::io::AsyncReadExt;

            // Copied out so the select! branch below borrows nothing from self.
            // Instant is Copy, and sleep_until on a fixed deadline is idempotent
            // across select! re-polls (a fresh sleep() would restart every wakeup
            // and could be starved by other branches).
            let drain_deadline = self.h264_drain_deadline;

            tokio::select! {
                // Bias toward server data so client input doesn't starve rendering.
                biased;

                // Read the first byte of the next server message.
                result = stream.read_u8() => {
                    match result {
                        Ok(msg_type) => {
                            match msg_type {
                                // FramebufferUpdate
                                0 => {
                                    if let Err(e) = self.read_framebuffer_update(&mut stream).await {
                                        debug!("[conn={}] VNC: FBU read ended: {}", self.conn_id, e);
                                        break;
                                    }
                                    // Encode updated framebuffer — H.264 path or JPEG fallback.
                                    if self.h264_pipeline.is_some() {
                                        if let Err(e) = self.maybe_encode_h264().await {
                                            warn!(
                                                "[conn={}] VNC: H.264 encode error: {}",
                                                self.conn_id, e
                                            );
                                        }
                                    }
                                    // The JPEG path is handled inside handle_raw_pixels /
                                    // handle_framebuffer_rectangle, which are called by
                                    // read_framebuffer_update. No extra work needed here.
                                }
                                // SetColourMapEntries — skip, uncommon with true-colour
                                1 => {
                                    if let Err(e) =
                                        Self::skip_colour_map_entries(&mut stream).await
                                    {
                                        debug!(
                                            "[conn={}] VNC: colour map skip error: {}",
                                            self.conn_id, e
                                        );
                                        break;
                                    }
                                }
                                // Bell — ignore
                                2 => {}
                                // ServerCutText — skip
                                3 => {
                                    if let Err(e) =
                                        Self::skip_server_cut_text(&mut stream).await
                                    {
                                        debug!(
                                            "[conn={}] VNC: cut text skip error: {}",
                                            self.conn_id, e
                                        );
                                        break;
                                    }
                                }
                                other => {
                                    warn!(
                                        "[conn={}] VNC: Unknown server message type {}, disconnecting",
                                        self.conn_id, other
                                    );
                                    break;
                                }
                            }
                        }
                        Err(e) => {
                            debug!("[conn={}] VNC: Server stream ended: {}", self.conn_id, e);
                            break;
                        }
                    }
                }

                // Keep-alive ping, so a dead viewer is detected even while idle.
                _ = keepalive_interval.tick() => {
                    if let Some(sent_at) = self.sync_sent_at {
                        if self.sync_control.check_timeout(sent_at.elapsed()) {
                            warn!("[conn={}] VNC: Client not responding to sync - disconnecting", self.conn_id);
                            break;
                        }
                        if !self.sync_control.is_waiting_for_sync() {
                            self.sync_sent_at = None;
                        }
                    }

                    if keepalive.check().is_some() && !self.sync_control.is_waiting_for_sync() {
                        trace!("[conn={}] VNC: Sending keep-alive sync", self.conn_id);
                        if self.send_sync().await.is_err() {
                            info!("[conn={}] VNC: Client channel closed, ending session", self.conn_id);
                            break;
                        }
                    }
                }

                // Viewer key/mouse input forwarded from a connected viewer with PRIV_CONTROL.
                viewer_bytes = async {
                    match self.viewer_input_rx {
                        Some(ref mut rx) => rx.recv().await,
                        None => std::future::pending().await,
                    }
                } => {
                    if let Some(bytes) = viewer_bytes {
                        if let Err(e) = self.handle_client_input(&mut stream, &bytes).await {
                            debug!("[conn={}] VNC: viewer input error: {}", self.conn_id, e);
                        }
                    }
                }

                // Process one client input message (keyboard, mouse, resize, clipboard).
                msg = from_client.recv() => {
                    // Check for sync timeout before processing the next message.
                    // This is the natural pace point: we already sent a sync after each frame,
                    // and client messages arrive at human-input frequency.
                    if let Some(sent_at) = self.sync_sent_at {
                        if self.sync_control.check_timeout(sent_at.elapsed()) {
                            warn!("[conn={}] VNC: Client not responding to sync — disconnecting", self.conn_id);
                            break;
                        }
                        if !self.sync_control.is_waiting_for_sync() {
                            self.sync_sent_at = None;
                        }
                    }

                    match msg {
                        Some(bytes) => {
                            if let Err(e) = self.handle_client_input(&mut stream, &bytes).await {
                                debug!(
                                    "[conn={}] VNC: Client input error: {}",
                                    self.conn_id, e
                                );
                                break;
                            }
                        }
                        None => {
                            info!("[conn={}] VNC: Client disconnected", self.conn_id);
                            break;
                        }
                    }
                }

                // Backstop: deliver encoder output when nothing else is pending.
                // Listed last so `biased` keeps server data and client input ahead of
                // it; the busy path is already covered by the opportunistic drain in
                // maybe_encode_h264. Disabled entirely (pending future) when no
                // encode is outstanding.
                _ = async move {
                    match drain_deadline {
                        Some(deadline) => tokio::time::sleep_until(deadline).await,
                        None => std::future::pending::<()>().await,
                    }
                } => {
                    match self.drain_and_send_h264().await {
                        Ok(true) => {
                            self.h264_drain_deadline = None;
                            self.h264_drain_attempts = 0;
                        }
                        Ok(false) => {
                            // Encoder still working (or holding this frame back).
                            if self.h264_drain_attempts < H264_DRAIN_MAX_ATTEMPTS {
                                self.h264_drain_attempts += 1;
                                self.h264_drain_deadline =
                                    Some(tokio::time::Instant::now() + H264_DRAIN_BACKSTOP);
                            } else {
                                self.h264_drain_deadline = None;
                                self.h264_drain_attempts = 0;
                            }
                        }
                        Err(e) => {
                            debug!("[conn={}] VNC: H.264 drain error: {}", self.conn_id, e);
                            break;
                        }
                    }
                }
            }
        }

        // Finalize recording
        if let Some(recorder) = self.recorder.take() {
            if let Err(e) = recorder.finalize() {
                warn!(
                    "[conn={}] VNC: Failed to finalize recording: {}",
                    self.conn_id, e
                );
            } else {
                info!("[conn={}] VNC: Session recording finalized", self.conn_id);
            }
        }

        info!(
            "[conn={}] session complete: {}",
            self.conn_id,
            self.stats.summary()
        );
        // Send disconnect instruction to client (matches Apache guacd behavior)
        send_disconnect(self.owner_sender.transport_sender()).await;

        // Notify viewers and deregister shared session.
        if let Some(ref sid) = self.share_id {
            self.owner_sender.owner_disconnect(sid);
        }

        info!("[conn={}] VNC: Connection ended", self.conn_id);
        Ok(())
    }

    /// Read and process one complete FramebufferUpdate message (type byte already consumed).
    /// Uses read_exact for every field so TCP fragmentation never misaligns the stream.
    async fn read_framebuffer_update<S>(&mut self, stream: &mut S) -> Result<(), String>
    where
        S: AsyncRead + AsyncWrite + Unpin,
    {
        use tokio::io::AsyncReadExt;

        // Remaining FBU header after the type byte: pad(1) + num_rects(2)
        let mut hdr = [0u8; 3];
        stream
            .read_exact(&mut hdr)
            .await
            .map_err(|e| format!("FBU header read: {e}"))?;
        let num_rects = u16::from_be_bytes([hdr[1], hdr[2]]) as usize;

        let bpp = self
            .pixel_format
            .as_ref()
            .map(|pf| (pf.bits_per_pixel / 8) as usize)
            .unwrap_or(4);

        for _ in 0..num_rects {
            // Each rectangle header: x(2) y(2) w(2) h(2) enc(4) = 12 bytes
            let mut rh = [0u8; 12];
            stream
                .read_exact(&mut rh)
                .await
                .map_err(|e| format!("rect header read: {e}"))?;
            let x = u16::from_be_bytes([rh[0], rh[1]]);
            let y = u16::from_be_bytes([rh[2], rh[3]]);
            let w = u16::from_be_bytes([rh[4], rh[5]]);
            let h = u16::from_be_bytes([rh[6], rh[7]]);
            let enc = i32::from_be_bytes([rh[8], rh[9], rh[10], rh[11]]);

            match enc {
                // Raw: bpp bytes per pixel
                0 => {
                    // SEC-VNC-01: use checked arithmetic — w*h*bpp can overflow for
                    // adversarial dimensions (e.g. 65535×65535×4 ≈ 17 GB on 64-bit;
                    // wraps to a small number on 32-bit causing silent OOB writes).
                    let n = (w as usize)
                        .checked_mul(h as usize)
                        .and_then(|n| n.checked_mul(bpp))
                        .ok_or_else(|| {
                            format!("VNC Raw: dimension overflow ({w}x{h} bpp={bpp})")
                        })?;
                    let mut raw = vec![0u8; n];
                    stream
                        .read_exact(&mut raw)
                        .await
                        .map_err(|e| format!("Raw read: {e}"))?;
                    let rgb = self.raw_pixels_to_rgb(&raw, bpp);
                    let rect = crate::vnc_protocol::VncRectangle {
                        x,
                        y,
                        width: w,
                        height: h,
                        encoding: 0,
                        src_x: 0,
                        src_y: 0,
                        pixels: rgb,
                        pixel_data: crate::vnc_protocol::VncPixelData::Empty,
                    };
                    self.handle_framebuffer_rectangle(rect).await?;
                }
                // CopyRect: src_x(2) src_y(2)
                1 => {
                    let mut src = [0u8; 4];
                    stream
                        .read_exact(&mut src)
                        .await
                        .map_err(|e| format!("CopyRect read: {e}"))?;
                    let src_x = u16::from_be_bytes([src[0], src[1]]);
                    let src_y = u16::from_be_bytes([src[2], src[3]]);
                    let rect = crate::vnc_protocol::VncRectangle {
                        x,
                        y,
                        width: w,
                        height: h,
                        encoding: 1,
                        src_x,
                        src_y,
                        pixels: vec![],
                        pixel_data: crate::vnc_protocol::VncPixelData::Empty,
                    };
                    self.handle_framebuffer_rectangle(rect).await?;
                }
                // ZRLE: compressed_length(4) + compressed_data
                16 => {
                    let mut lb = [0u8; 4];
                    stream
                        .read_exact(&mut lb)
                        .await
                        .map_err(|e| format!("ZRLE len read: {e}"))?;
                    let clen = u32::from_be_bytes(lb) as usize;
                    let mut compressed = vec![0u8; clen];
                    stream
                        .read_exact(&mut compressed)
                        .await
                        .map_err(|e| format!("ZRLE data read: {e}"))?;
                    let rect = crate::vnc_protocol::VncRectangle {
                        x,
                        y,
                        width: w,
                        height: h,
                        encoding: 16,
                        src_x: 0,
                        src_y: 0,
                        pixels: vec![],
                        pixel_data: crate::vnc_protocol::VncPixelData::ZrleCompressed(compressed),
                    };
                    self.handle_framebuffer_rectangle(rect).await?;
                }
                // RichCursor: img(w*h*bpp) + mask(ceil(w/8)*h)
                -239 => {
                    // SEC-VNC-02: use checked arithmetic — img_n and mask_n can
                    // overflow for adversarial cursor dimensions (e.g. 65535×65535).
                    let img_n = (w as usize)
                        .checked_mul(h as usize)
                        .and_then(|n| n.checked_mul(bpp))
                        .ok_or_else(|| {
                            format!("VNC RichCursor: img dimension overflow ({w}x{h} bpp={bpp})")
                        })?;
                    let mask_stride = (w as usize).div_ceil(8);
                    let mask_n = mask_stride.checked_mul(h as usize).ok_or_else(|| {
                        format!("VNC RichCursor: mask dimension overflow ({w}x{h})")
                    })?;
                    let mut img = vec![0u8; img_n];
                    let mut mask = vec![0u8; mask_n];
                    stream
                        .read_exact(&mut img)
                        .await
                        .map_err(|e| format!("Cursor img read: {e}"))?;
                    stream
                        .read_exact(&mut mask)
                        .await
                        .map_err(|e| format!("Cursor mask read: {e}"))?;
                    // Build RGBA cursor from server pixel format
                    let rgba = self
                        .cursor_pixels_to_rgba(&img, &mask, w, h, bpp)
                        .map_err(|e| format!("Cursor RGBA conversion failed: {e}"))?;
                    let rect = crate::vnc_protocol::VncRectangle {
                        x,
                        y,
                        width: w,
                        height: h,
                        encoding: -239,
                        src_x: 0,
                        src_y: 0,
                        pixels: rgba,
                        pixel_data: crate::vnc_protocol::VncPixelData::Empty,
                    };
                    self.handle_framebuffer_rectangle(rect).await?;
                }
                // XCursor: 6 bytes fore+back RGB triplets + mask + mask
                -240 => {
                    if w > 0 && h > 0 {
                        // SEC-VNC-03: use checked arithmetic — mask_n can overflow for
                        // adversarial cursor dimensions (e.g. 65535×65535 → ~1 GB buf).
                        let mask_stride = (w as usize).div_ceil(8);
                        let mask_n = mask_stride.checked_mul(h as usize).ok_or_else(|| {
                            format!("VNC XCursor: mask dimension overflow ({w}x{h})")
                        })?;
                        let buf_size = (2usize)
                            .checked_mul(mask_n)
                            .and_then(|n| n.checked_add(6))
                            .ok_or_else(|| "VNC XCursor: buffer size overflow".to_string())?;
                        let mut buf = vec![0u8; buf_size];
                        stream
                            .read_exact(&mut buf)
                            .await
                            .map_err(|e| format!("XCursor read: {e}"))?;
                    }
                    // Skip — use RichCursor (-239) when available
                }
                // DesktopSize: new dimensions are w × h, no body
                -223 => {
                    // SEC-VNC-06: apply the same MAX_VNC_DIM cap as the initial handshake.
                    // Without this, a malicious server can send DesktopSize with
                    // 65535×65535 after the handshake, bypassing the connect() check
                    // and triggering a ~17 GB FrameBuffer allocation (DoS / OOM).
                    const MAX_VNC_DIM: u16 = 7680;
                    if w > MAX_VNC_DIM || h > MAX_VNC_DIM {
                        return Err(format!(
                            "VNC DesktopSize {}×{} exceeds maximum {}×{} — disconnecting",
                            w, h, MAX_VNC_DIM, MAX_VNC_DIM
                        ));
                    }
                    let size_instr = guacr_protocol::format_instruction(
                        "size",
                        &["0", &(w as u32).to_string(), &(h as u32).to_string()],
                    );
                    self.send_and_record(&size_instr).await?;
                    self.width = w as u32;
                    self.height = h as u32;
                    self.framebuffer = FrameBuffer::new(self.width, self.height);
                }
                // LastRect: no body, no more rectangles in this FBU
                -224 => break,
                enc => {
                    // Unknown pseudo-encodings (negative) carry only w/h metadata — no body.
                    // Unknown positive encodings have an unknown body size; we cannot recover
                    // stream alignment, so log and terminate.
                    if enc < 0 {
                        debug!(
                            "VNC: Ignoring unrecognized pseudo-encoding {} at ({},{}) {}x{}",
                            enc, x, y, w, h
                        );
                    } else {
                        warn!("[conn={}] VNC: Unknown positive encoding {} — cannot determine body size, disconnecting", self.conn_id, enc);
                        return Err(format!("unknown encoding {enc}"));
                    }
                }
            }
        }

        // Request next incremental update
        VncProtocol::send_framebuffer_update_request(
            stream,
            true,
            0,
            0,
            self.width as u16,
            self.height as u16,
        )
        .await
        .map_err(|e| format!("FBU request: {e}"))?;

        Ok(())
    }

    /// Convert raw server pixels (bpp bytes each) to 24-bit RGB.
    fn raw_pixels_to_rgb(&self, raw: &[u8], bpp: usize) -> Vec<u8> {
        if bpp == 3 {
            return raw.to_vec();
        }
        let pf = self.pixel_format.as_ref();
        let (rs, gs, bs) = pf
            .map(|p| (p.red_shift, p.green_shift, p.blue_shift))
            .unwrap_or((16, 8, 0));
        let pixel_count = raw.len() / bpp;
        let mut rgb = vec![0u8; pixel_count * 3];
        for i in 0..pixel_count {
            let p = &raw[i * bpp..(i + 1) * bpp];
            // Reconstruct u32 from bytes (little-endian is most common for 32bpp)
            let val = match bpp {
                4 => u32::from_le_bytes([p[0], p[1], p[2], p[3]]),
                _ => p[0] as u32,
            };
            rgb[i * 3] = ((val >> rs) & 0xFF) as u8;
            rgb[i * 3 + 1] = ((val >> gs) & 0xFF) as u8;
            rgb[i * 3 + 2] = ((val >> bs) & 0xFF) as u8;
        }
        rgb
    }

    /// Convert cursor image (server pixel format) + 1-bit mask to RGBA.
    fn cursor_pixels_to_rgba(
        &self,
        img: &[u8],
        mask: &[u8],
        w: u16,
        h: u16,
        bpp: usize,
    ) -> Result<Vec<u8>, String> {
        let (rs, gs, bs) = self
            .pixel_format
            .as_ref()
            .map(|p| (p.red_shift, p.green_shift, p.blue_shift))
            .unwrap_or((16, 8, 0));
        // SEC-VNC-05: use checked arithmetic — w*h*4 can overflow for adversarial
        // cursor dimensions even if w*h*bpp passed the check in the caller,
        // because bpp may be as low as 1 while RGBA always uses 4 bytes/pixel.
        let pixel_count = (w as usize)
            .checked_mul(h as usize)
            .ok_or_else(|| format!("VNC cursor_pixels_to_rgba: dimension overflow ({w}x{h})"))?;
        let rgba_size = pixel_count
            .checked_mul(4)
            .ok_or_else(|| "VNC cursor_pixels_to_rgba: RGBA allocation overflow".to_string())?;
        let mut rgba = vec![0u8; rgba_size];
        let stride = (w as usize).div_ceil(8);
        for row in 0..(h as usize) {
            for col in 0..(w as usize) {
                let i = row * (w as usize) + col;
                let p = &img[i * bpp..(i + 1) * bpp.min(img.len())];
                let val = match bpp {
                    4 => u32::from_le_bytes([
                        p.first().copied().unwrap_or(0),
                        p.get(1).copied().unwrap_or(0),
                        p.get(2).copied().unwrap_or(0),
                        p.get(3).copied().unwrap_or(0),
                    ]),
                    _ => p.first().copied().unwrap_or(0) as u32,
                };
                let alpha = if mask.len() > row * stride + col / 8 {
                    if (mask[row * stride + col / 8] >> (7 - col % 8)) & 1 != 0 {
                        255
                    } else {
                        0
                    }
                } else {
                    0
                };
                rgba[i * 4] = ((val >> rs) & 0xFF) as u8;
                rgba[i * 4 + 1] = ((val >> gs) & 0xFF) as u8;
                rgba[i * 4 + 2] = ((val >> bs) & 0xFF) as u8;
                rgba[i * 4 + 3] = alpha;
            }
        }
        Ok(rgba)
    }

    async fn skip_colour_map_entries<S>(stream: &mut S) -> Result<(), String>
    where
        S: AsyncRead + Unpin,
    {
        use tokio::io::AsyncReadExt;
        let mut hdr = [0u8; 5]; // pad(1) + first-colour(2) + num-colours(2)
        stream
            .read_exact(&mut hdr)
            .await
            .map_err(|e| format!("colour map hdr: {e}"))?;
        let num_colours = u16::from_be_bytes([hdr[3], hdr[4]]) as usize;
        let mut buf = vec![0u8; num_colours * 6];
        stream
            .read_exact(&mut buf)
            .await
            .map_err(|e| format!("colour map data: {e}"))?;
        Ok(())
    }

    async fn skip_server_cut_text<S>(stream: &mut S) -> Result<(), String>
    where
        S: AsyncRead + Unpin,
    {
        use tokio::io::AsyncReadExt;
        let mut hdr = [0u8; 7]; // pad(3) + length(4)
        stream
            .read_exact(&mut hdr)
            .await
            .map_err(|e| format!("cut text hdr: {e}"))?;
        let length = u32::from_be_bytes([hdr[3], hdr[4], hdr[5], hdr[6]]) as usize;
        let mut buf = vec![0u8; length];
        stream
            .read_exact(&mut buf)
            .await
            .map_err(|e| format!("cut text data: {e}"))?;
        Ok(())
    }

    async fn handle_client_input<S>(&mut self, stream: &mut S, msg: &Bytes) -> Result<(), String>
    where
        S: AsyncWrite + Unpin,
    {
        // Record client input (if recording is enabled)
        self.record_client_input(msg);

        let instr = GuacamoleParser::parse_instruction(msg)
            .map_err(|e| format!("Failed to parse instruction: {}", e))?;

        match instr.opcode {
            "key" => {
                // Security: Check read-only mode
                if self.read_only {
                    trace!("VNC: Keyboard input blocked (read-only mode)");
                    return Ok(());
                }

                if instr.args.len() >= 2 {
                    if let (Ok(keysym), Ok(pressed)) =
                        (instr.args[0].parse::<u32>(), instr.args[1].parse::<u8>())
                    {
                        // Buffer printable keystrokes for threat detection context.
                        // Enter (0xFF0D) is a trigger event — analyze screenshot then clear buffer.
                        // Buffer printable ASCII keystrokes for threat detection context.
                        // Enter (0xFF0D) is a trigger event — analyze screenshot then clear buffer.
                        #[cfg(feature = "threat-detection")]
                        if pressed == 1 {
                            const KEYSYM_RETURN: u32 = 0xFF0D;
                            if keysym == KEYSYM_RETURN {
                                // Trigger: analyze screenshot on Enter key press.
                                if let Some(ref detector) = self.threat_detector {
                                    let rgba = self.framebuffer.data();
                                    match guacr_threat_detection::rgba_to_grayscale_jpeg(
                                        rgba,
                                        self.width,
                                        self.height,
                                        75,
                                    ) {
                                        Ok(jpeg) => {
                                            let keystrokes =
                                                std::mem::take(&mut self.threat_keystroke_buffer);
                                            let sid = self.threat_session_id.clone();
                                            let det = Arc::clone(detector);
                                            // Spawn non-blocking so the session loop is not
                                            // stalled by the BAML HTTP round-trip.
                                            tokio::spawn(async move {
                                                match det
                                                    .analyze_screenshot(&jpeg, &keystrokes, &sid)
                                                    .await
                                                {
                                                    Ok(analysis) => {
                                                        if analysis.result.level
                                                            >= guacr_threat_detection::ThreatLevel::Medium
                                                        {
                                                            warn!(
                                                                "[conn={}] VNC: screenshot threat: {} (level={:?})",
                                                                sid,
                                                                analysis.result.description,
                                                                analysis.result.level
                                                            );
                                                        }
                                                    }
                                                    Err(e) => {
                                                        debug!(
                                                            "[conn={}] VNC: screenshot analysis error: {}",
                                                            sid, e
                                                        );
                                                    }
                                                }
                                            });
                                        }
                                        Err(e) => {
                                            debug!(
                                                "[conn={}] VNC: grayscale JPEG capture failed: {}",
                                                self.conn_id, e
                                            );
                                        }
                                    }
                                }
                            } else if keysym < 0x100 {
                                // Buffer printable ASCII keystrokes for context.
                                if let Some(c) = char::from_u32(keysym) {
                                    if c.is_ascii_graphic() || c == ' ' {
                                        self.threat_keystroke_buffer.push(c);
                                    }
                                }
                            }
                        }

                        VncProtocol::send_key_event(stream, keysym, pressed == 1).await?;
                    }
                }
            }
            "mouse" if instr.args.len() >= 3 => {
                // Protocol order: x, y, mask (per Guacamole protocol spec)
                if let (Ok(x), Ok(y), Ok(mask)) = (
                    instr.args[0].parse::<i32>(),
                    instr.args[1].parse::<i32>(),
                    instr.args[2].parse::<u8>(),
                ) {
                    // Security: Check read-only mode for mouse clicks
                    if self.read_only && !is_mouse_event_allowed_readonly(mask as u32) {
                        trace!("VNC: Mouse click blocked (read-only mode)");
                        return Ok(());
                    }

                    // Mouse click is a threat detection trigger for VNC.
                    #[cfg(feature = "threat-detection")]
                    if mask & 0x07 != 0 {
                        if let Some(ref detector) = self.threat_detector {
                            let rgba = self.framebuffer.data();
                            if let Ok(jpeg) = guacr_threat_detection::rgba_to_grayscale_jpeg(
                                rgba,
                                self.width,
                                self.height,
                                75,
                            ) {
                                let keystrokes = std::mem::take(&mut self.threat_keystroke_buffer);
                                let sid = self.threat_session_id.clone();
                                let det = Arc::clone(detector);
                                tokio::spawn(async move {
                                    if let Ok(analysis) =
                                        det.analyze_screenshot(&jpeg, &keystrokes, &sid).await
                                    {
                                        if analysis.result.level
                                            >= guacr_threat_detection::ThreatLevel::Medium
                                        {
                                            warn!(
                                                "[conn={}] VNC: screenshot threat (click): {} (level={:?})",
                                                sid,
                                                analysis.result.description,
                                                analysis.result.level
                                            );
                                        }
                                    }
                                });
                            }
                        }
                    }

                    // Feed mouse state to drag detector
                    self.drag_detector.notify_mouse_event(x, y, mask);

                    let x = x.max(0).min(self.width as i32 - 1) as u16;
                    let y = y.max(0).min(self.height as i32 - 1) as u16;

                    VncProtocol::send_pointer_event(stream, x, y, mask).await?;
                }
            }
            "size" => {
                // Client size instruction format: size,<layer>,<width>,<height>;
                // We ignore the layer (args[0]) and use width/height (args[1], args[2])
                if let Some(width_str) = instr.args.get(1) {
                    if let Some(height_str) = instr.args.get(2) {
                        if let (Ok(w), Ok(h)) =
                            (width_str.parse::<u32>(), height_str.parse::<u32>())
                        {
                            info!(
                                "[conn={}] VNC: Resize requested: {}x{} (layer: {})",
                                self.conn_id,
                                w,
                                h,
                                instr.args.first().unwrap_or(&"0")
                            );

                            // Reset scroll detector for new dimensions
                            self.scroll_detector.reset(w, h);
                            self.width = w;
                            self.height = h;

                            VncProtocol::send_framebuffer_update_request(
                                stream, false, 0, 0, w as u16, h as u16,
                            )
                            .await?;
                        }
                    }
                }
            }
            "sync" => {
                // Client is acknowledging a sync instruction (flow control)
                if let Some(ts_str) = instr.args.first() {
                    if let Ok(client_ts) = ts_str.parse::<u64>() {
                        if let Some(pending_ts) = self.sync_control.pending_timestamp() {
                            if client_ts >= pending_ts {
                                self.sync_control.clear_pending();
                                self.sync_control.reset_timeout_count();
                                self.sync_sent_at = None;
                                trace!("VNC: Client acknowledged sync (ts={})", client_ts);
                            }
                        }
                    }
                }
            }
            #[cfg(feature = "sftp")]
            "file" => {
                if let Some(ref mut sftp) = self.sftp_session {
                    if let Err(e) = crate::sftp_integration::handle_sftp_file_request(
                        sftp,
                        &instr.args.iter().map(|s| s.to_string()).collect::<Vec<_>>(),
                        self.owner_sender.transport_sender(),
                    )
                    .await
                    {
                        warn!(
                            "[conn={}] VNC: SFTP file operation failed: {}",
                            self.conn_id, e
                        );
                    }
                } else {
                    warn!(
                        "[conn={}] VNC: File transfer requested but SFTP not enabled",
                        self.conn_id
                    );
                }
            }
            _ => {
                let handled = if let Some(session_id) = self.share_id.as_deref() {
                    share_viewer::handle_owner_share_control(
                        session_id,
                        instr.opcode,
                        &instr.args,
                        self.owner_sender.transport_sender(),
                    )
                    .await
                } else {
                    false
                };
                if !handled {
                    debug!("VNC: Unhandled instruction: {}", instr.opcode);
                }
            }
        }

        Ok(())
    }

    /// Handle cursor update from VNC server (client-side cursor rendering)
    ///
    /// rect.pixels contains RGBA data already converted by the FBU loop
    /// (cursor_pixels_to_rgba was called before this point for -239, and -240 is skipped).
    async fn handle_cursor_update(
        &mut self,
        rect: crate::vnc_protocol::VncRectangle,
    ) -> Result<(), String> {
        if self.read_only {
            return Ok(());
        }

        // 0×0 cursor means the server wants the cursor hidden.
        // Send a 1×1 fully-transparent cursor so the client cursor disappears.
        if rect.width == 0 || rect.height == 0 {
            let instructions =
                self.cursor_manager
                    .send_custom_cursor(&[0u8, 0u8, 0u8, 0u8], 1, 1, 0, 0)?;
            for instr in instructions {
                self.send_and_record(&instr).await?;
            }
            return Ok(());
        }

        // rect.pixels is RGBA (4 bytes/pixel) already — cursor_pixels_to_rgba ran upstream.
        // Do not call parse_cursor_data here: that function expects raw VNC cursor format
        // (pixel data in server format + bitmask), not RGBA.
        let instructions = self.cursor_manager.send_custom_cursor(
            &rect.pixels,
            rect.width as u32,
            rect.height as u32,
            rect.x as i32,
            rect.y as i32,
        )?;

        for instr in instructions {
            self.send_and_record(&instr).await?;
        }

        debug!(
            "VNC: Sent cursor update {}x{} with hotspot ({}, {})",
            rect.width, rect.height, rect.x, rect.y
        );

        Ok(())
    }

    /// Encode a framebuffer region and send it as a Guacamole image instruction.
    async fn encode_and_send_region(
        &mut self,
        frect: guacr_terminal::FrameRect,
    ) -> Result<(), String> {
        use base64::Engine;
        let (encoded, fmt) = self.encode_region(frect)?;
        self.adaptive_quality.track_frame_sent(encoded.len());
        let mimetype = match fmt {
            1 => "image/jpeg",
            2 => "image/webp",
            _ => "image/png",
        };
        let b64 = base64::engine::general_purpose::STANDARD.encode(&encoded);
        let img_instr = format_img(
            self.stream_id,
            14,
            0,
            mimetype,
            frect.x as i32,
            frect.y as i32,
        );
        self.send_and_record(&img_instr).await?;
        for chunk in format_chunked_blobs(self.stream_id, &b64, None) {
            self.send_and_record(&chunk).await?;
        }
        self.stream_id = self.stream_id.wrapping_add(1);
        Ok(())
    }

    /// Handle CopyRect encoding: copy pixels within the framebuffer and emit a
    /// Guacamole copy instruction instead of encoding image data.
    async fn handle_copyrect(
        &mut self,
        rect: &crate::vnc_protocol::VncRectangle,
    ) -> Result<(), String> {
        let src_x = rect.src_x as u32;
        let src_y = rect.src_y as u32;
        let dst_x = rect.x as u32;
        let dst_y = rect.y as u32;
        let width = rect.width as u32;
        let height = rect.height as u32;

        // Update the local framebuffer so future operations have correct pixel state
        self.framebuffer
            .copy_region(src_x, src_y, dst_x, dst_y, width, height);

        // Notify drag detector of update size (same as other paths)
        self.drag_detector.notify_graphics_update(width, height);

        // Emit Guacamole copy instruction (no image encoding needed)
        let copy_instr =
            guacr_protocol::format_copy(0, src_x, src_y, width, height, 12, 0, dst_x, dst_y);
        self.send_and_record(&copy_instr).await?;
        self.send_sync().await?;

        self.framebuffer.clear_dirty();
        Ok(())
    }

    /// Handle Tight JPEG subtype: forward the server's JPEG bytes directly.
    /// Zero re-encoding overhead — the server already compressed the pixels.
    async fn handle_tight_jpeg(
        &mut self,
        rect: &crate::vnc_protocol::VncRectangle,
    ) -> Result<(), String> {
        let jpeg_bytes = match &rect.pixel_data {
            crate::vnc_protocol::VncPixelData::TightJpeg(b) => b.clone(),
            _ => return Ok(()),
        };

        // Decode JPEG to update local framebuffer (for scroll/drag detection)
        match image::load_from_memory(&jpeg_bytes) {
            Ok(img) => {
                let rgba = img.to_rgba8();
                self.framebuffer.update_region(
                    rect.x as u32,
                    rect.y as u32,
                    rect.width as u32,
                    rect.height as u32,
                    &rgba,
                );
            }
            Err(e) => warn!(
                "[conn={}] VNC: Failed to decode Tight JPEG for framebuffer: {}",
                self.conn_id, e
            ),
        }
        self.adaptive_quality.track_frame_sent(jpeg_bytes.len());
        self.drag_detector
            .notify_graphics_update(rect.width as u32, rect.height as u32);
        use base64::Engine;
        let b64 = base64::engine::general_purpose::STANDARD.encode(&jpeg_bytes);
        let img_instr = format_img(
            self.stream_id,
            14,
            0,
            "image/jpeg",
            rect.x as i32,
            rect.y as i32,
        );
        self.send_and_record(&img_instr).await?;
        for chunk in format_chunked_blobs(self.stream_id, &b64, None) {
            self.send_and_record(&chunk).await?;
        }
        self.stream_id = self.stream_id.wrapping_add(1);
        self.send_sync().await?;
        self.framebuffer.clear_dirty();
        Ok(())
    }

    /// Handle Tight FillRect: update framebuffer and encode the solid-color region.
    async fn handle_tight_fill(
        &mut self,
        rect: &crate::vnc_protocol::VncRectangle,
        r: u8,
        g: u8,
        b: u8,
    ) -> Result<(), String> {
        // SEC-VNC-04: use checked arithmetic — pixel_count*4 can overflow for
        // adversarial Tight FillRect dimensions (e.g. 65535×65535 → ~17 GB).
        let pixel_count = (rect.width as usize)
            .checked_mul(rect.height as usize)
            .ok_or_else(|| {
                format!(
                    "VNC Tight FillRect: dimension overflow ({}x{})",
                    rect.width, rect.height
                )
            })?;
        let rgba_size = pixel_count
            .checked_mul(4)
            .ok_or_else(|| "VNC Tight FillRect: RGBA allocation overflow".to_string())?;
        let mut rgba_fill = vec![0u8; rgba_size];
        for i in 0..pixel_count {
            rgba_fill[i * 4] = r;
            rgba_fill[i * 4 + 1] = g;
            rgba_fill[i * 4 + 2] = b;
            rgba_fill[i * 4 + 3] = 255;
        }
        if let Some(img) =
            image::RgbaImage::from_raw(rect.width as u32, rect.height as u32, rgba_fill)
        {
            self.framebuffer.update_region(
                rect.x as u32,
                rect.y as u32,
                rect.width as u32,
                rect.height as u32,
                &img,
            );
        }
        self.drag_detector
            .notify_graphics_update(rect.width as u32, rect.height as u32);
        let frect = guacr_terminal::FrameRect {
            x: rect.x as u32,
            y: rect.y as u32,
            width: rect.width as u32,
            height: rect.height as u32,
        };
        self.encode_and_send_region(frect).await?;
        self.send_sync().await?;
        self.framebuffer.clear_dirty();
        Ok(())
    }

    /// Handle active drag: emit a copy instruction for the dragged region and encode
    /// the exposed edge strips. Returns `Ok(true)` if the drag was handled (caller
    /// should return), `Ok(false)` if no actionable drag delta was present.
    async fn handle_drag_copy(&mut self, dx: i32, dy: i32) -> Result<bool, String> {
        if dx == 0 && dy == 0 {
            return Ok(false);
        }

        debug!("VNC: Drag detected - sending copy delta ({}, {})", dx, dy);

        let src_x = dx.max(0) as u32;
        let src_y = dy.max(0) as u32;
        let dst_x = (-dx).max(0) as u32;
        let dst_y = (-dy).max(0) as u32;
        let copy_w = self.width.saturating_sub(dx.unsigned_abs());
        let copy_h = self.height.saturating_sub(dy.unsigned_abs());

        if copy_w > 0 && copy_h > 0 {
            let copy_instr = guacr_protocol::format_copy(
                0, src_x, src_y, copy_w, copy_h, 12, // GUAC_COMP_SRC
                0, dst_x, dst_y,
            );
            self.send_and_record(&copy_instr).await?;
        }

        // Encode exposed edge strips
        if dx.unsigned_abs() > 0 {
            let strip_x = if dx > 0 {
                self.width.saturating_sub(dx as u32)
            } else {
                0
            };
            let strip_w = dx.unsigned_abs().min(self.width);
            self.encode_and_send_region(guacr_terminal::FrameRect {
                x: strip_x,
                y: 0,
                width: strip_w,
                height: self.height,
            })
            .await?;
        }

        if dy.unsigned_abs() > 0 {
            let strip_y = if dy > 0 {
                self.height.saturating_sub(dy as u32)
            } else {
                0
            };
            let strip_h = dy.unsigned_abs().min(self.height);
            self.encode_and_send_region(guacr_terminal::FrameRect {
                x: 0,
                y: strip_y,
                width: self.width,
                height: strip_h,
            })
            .await?;
        }

        self.send_sync().await?;
        self.framebuffer.clear_dirty();
        Ok(true)
    }

    /// Handle a detected scroll operation: emit transfer + new-region image instructions.
    async fn handle_scroll(
        &mut self,
        scroll_op: guacr_terminal::ScrollOperation,
    ) -> Result<(), String> {
        trace!(
            "VNC: Detected scroll {:?} by {} pixels",
            scroll_op.direction,
            scroll_op.pixels
        );

        match scroll_op.direction {
            ScrollDirection::Up => {
                let copy_instr = guacr_protocol::format_transfer(
                    0,
                    0,
                    scroll_op.pixels,
                    self.width,
                    self.height - scroll_op.pixels,
                    12,
                    0,
                    0,
                    0,
                );
                self.send_and_record(&copy_instr).await?;

                let new_region_y = self.height - scroll_op.pixels;
                self.encode_and_send_region(guacr_terminal::FrameRect {
                    x: 0,
                    y: new_region_y,
                    width: self.width,
                    height: scroll_op.pixels,
                })
                .await?;
                self.send_sync().await?;
            }
            ScrollDirection::Down => {
                let copy_instr = guacr_protocol::format_transfer(
                    0,
                    0,
                    0,
                    self.width,
                    self.height - scroll_op.pixels,
                    12,
                    0,
                    0,
                    scroll_op.pixels,
                );
                self.send_and_record(&copy_instr).await?;

                self.encode_and_send_region(guacr_terminal::FrameRect {
                    x: 0,
                    y: 0,
                    width: self.width,
                    height: scroll_op.pixels,
                })
                .await?;
                self.send_sync().await?;
            }
        }

        self.framebuffer.clear_dirty();
        Ok(())
    }

    /// Handle raw pixel data: convert RGB→RGBA, update the framebuffer, run
    /// drag/scroll optimizations, and encode dirty rects as Guacamole images.
    async fn handle_raw_pixels(
        &mut self,
        rect: &crate::vnc_protocol::VncRectangle,
    ) -> Result<(), String> {
        // AC-5: use checked arithmetic for RGBA allocation.
        let pixel_count = (rect.width as usize)
            .checked_mul(rect.height as usize)
            .ok_or_else(|| {
                format!(
                    "VNC raw pixels: dimension overflow ({}x{})",
                    rect.width, rect.height
                )
            })?;
        let rgba_size = pixel_count
            .checked_mul(4)
            .ok_or_else(|| "VNC raw pixels: RGBA allocation overflow".to_string())?;
        let mut rgba_vec = vec![0u8; rgba_size];

        for i in 0..pixel_count {
            let src_idx = i * 3;
            let dst_idx = i * 4;

            if src_idx + 2 < rect.pixels.len() && dst_idx + 3 < rgba_vec.len() {
                rgba_vec[dst_idx] = rect.pixels[src_idx];
                rgba_vec[dst_idx + 1] = rect.pixels[src_idx + 1];
                rgba_vec[dst_idx + 2] = rect.pixels[src_idx + 2];
                rgba_vec[dst_idx + 3] = 255;
            }
        }

        self.framebuffer.update_region(
            rect.x as u32,
            rect.y as u32,
            rect.width as u32,
            rect.height as u32,
            &rgba_vec,
        );

        // Notify drag detector of update size
        let update_w = rect.width as u32;
        let update_h = rect.height as u32;
        self.drag_detector
            .notify_graphics_update(update_w, update_h);

        self.framebuffer.optimize_dirty_rects();
        let dirty_rects: Vec<_> = self.framebuffer.dirty_rects().to_vec();
        if dirty_rects.is_empty() {
            return Ok(());
        }

        // When the H.264 encoder is active, leave dirty rects for the encode timer.
        // video_tx alone is not sufficient — VNC always uses JPEG/Guacamole path
        // because VncViewer has no video element to receive H.264 frames.
        if self.h264_pipeline.is_some() {
            return Ok(());
        }

        // Check for active drag (copy-based optimization, shared with RDP)
        if self.drag_detector.is_dragging() {
            let (dx, dy) = self.drag_detector.drag_delta();
            if self.handle_drag_copy(dx, dy).await? {
                return Ok(());
            }
        }

        // If drag just ended, force full re-render (fall through to normal path)
        if self.drag_detector.drag_ended() {
            debug!("VNC: Drag ended - forcing full re-render");
        }

        // Check for scroll operation (shared with RDP)
        if let Some(scroll_op) = self.scroll_detector.detect_scroll(self.framebuffer.data()) {
            self.handle_scroll(scroll_op).await?;
            return Ok(());
        }

        // Encode dirty regions directly as images.
        // CopyDetector cell-based tiling is disabled: it fragments large updates
        // into hundreds of small tiles, causing visual artifacts during drag
        // and overwhelming the client with instruction volume.
        use base64::Engine;
        let mut total_bytes = 0;
        for dirty in &dirty_rects {
            let (encoded_data, fmt) = self.encode_region(*dirty)?;
            total_bytes += encoded_data.len();
            let mimetype = match fmt {
                1 => "image/jpeg",
                2 => "image/webp",
                _ => "image/png",
            };
            let b64 = base64::engine::general_purpose::STANDARD.encode(&encoded_data);
            let img_instr = format_img(
                self.stream_id,
                14,
                0,
                mimetype,
                dirty.x as i32,
                dirty.y as i32,
            );
            self.send_and_record(&img_instr).await?;
            for chunk in format_chunked_blobs(self.stream_id, &b64, None) {
                self.send_and_record(&chunk).await?;
            }
            self.stream_id = self.stream_id.wrapping_add(1);
        }

        if total_bytes > 0 {
            self.adaptive_quality.track_frame_sent(total_bytes);
        }
        self.send_sync().await?;
        self.framebuffer.clear_dirty();

        Ok(())
    }

    async fn handle_framebuffer_rectangle(
        &mut self,
        rect: crate::vnc_protocol::VncRectangle,
    ) -> Result<(), String> {
        // AC-2/AC-3 (protocol-security R2): reject rectangles that extend beyond
        // the negotiated framebuffer bounds. Check before any pixel data is written.
        // Pseudo-encodings (cursor, DesktopSize) carry position data in x/y fields
        // with a different meaning, so skip the bounds check for them.
        let is_pseudo = rect.encoding == crate::vnc_protocol::encodings::CURSOR
            || rect.encoding == crate::vnc_protocol::encodings::X_CURSOR
            || rect.encoding == crate::vnc_protocol::encodings::DESKTOP_SIZE;
        if !is_pseudo {
            let right = (rect.x as u32)
                .checked_add(rect.width as u32)
                .ok_or_else(|| {
                    format!(
                        "VNC: rectangle x+width overflows u32 (x={}, width={})",
                        rect.x, rect.width
                    )
                })?;
            let bottom = (rect.y as u32)
                .checked_add(rect.height as u32)
                .ok_or_else(|| {
                    format!(
                        "VNC: rectangle y+height overflows u32 (y={}, height={})",
                        rect.y, rect.height
                    )
                })?;
            if right > self.width {
                return Err(format!(
                    "VNC: rectangle right edge {} exceeds framebuffer width {}",
                    right, self.width
                ));
            }
            if bottom > self.height {
                return Err(format!(
                    "VNC: rectangle bottom edge {} exceeds framebuffer height {}",
                    bottom, self.height
                ));
            }
        }

        // Check for cursor pseudo-encoding (-239 = Rich Cursor, -240 = X Cursor)
        if rect.encoding == crate::vnc_protocol::encodings::CURSOR
            || rect.encoding == crate::vnc_protocol::encodings::X_CURSOR
        {
            return self.handle_cursor_update(rect).await;
        }

        // CopyRect encoding
        if rect.encoding == crate::vnc_protocol::encodings::COPYRECT {
            return self.handle_copyrect(&rect).await;
        }

        // Tight JPEG subtype: forward the server's JPEG bytes directly
        if let crate::vnc_protocol::VncPixelData::TightJpeg(ref jpeg_bytes) = rect.pixel_data {
            if !jpeg_bytes.is_empty() {
                return self.handle_tight_jpeg(&rect).await;
            }
        }

        // Tight FillRect: solid-color region
        if let crate::vnc_protocol::VncPixelData::Fill(r, g, b) = rect.pixel_data {
            return self.handle_tight_fill(&rect, r, g, b).await;
        }

        // ZRLE (T-013 to T-015): decompress using per-session zlib state, then
        // treat the decoded pixels as a Raw rectangle.
        if let crate::vnc_protocol::VncPixelData::ZrleCompressed(ref compressed) = rect.pixel_data {
            let compressed = compressed.clone();
            match crate::encodings::decode_zrle(
                &compressed,
                rect.width,
                rect.height,
                &mut self.zrle_state,
            ) {
                Ok(rgb_pixels) => {
                    let decoded_rect = crate::vnc_protocol::VncRectangle {
                        pixels: rgb_pixels,
                        pixel_data: crate::vnc_protocol::VncPixelData::Empty,
                        ..rect
                    };
                    return self.handle_raw_pixels(&decoded_rect).await;
                }
                Err(e) => {
                    // AC-5 (T-015): on ZRLE decode error, stream position is already
                    // consistent (we consumed the full compressed payload). Terminate.
                    return Err(format!("VNC: ZRLE decode error: {e}"));
                }
            }
        }

        // Empty pixel data — nothing to do
        if rect.pixels.is_empty() {
            return Ok(());
        }

        // Raw pixels path
        self.handle_raw_pixels(&rect).await
    }
}
