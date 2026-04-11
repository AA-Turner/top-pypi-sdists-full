use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    // Connection utilities
    connect_tcp_with_timeout,
    is_mouse_event_allowed_readonly,
    // Recording helpers
    record_client_input as shared_record_client_input,
    send_and_record as shared_send_and_record,
    // Session lifecycle
    send_disconnect,
    send_name,
    send_ready,
    // Adaptive quality (bandwidth-aware quality adjustment, shared with RDP)
    AdaptiveQuality,
    // Cursor support
    CursorManager,
    // Drag detection (shared with RDP)
    DragDetector,
    EncodedFrame,
    EventBasedHandler,
    EventCallback,
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
    StandardCursor,
    // Sync flow control (prevents overwhelming slow clients, shared with RDP)
    SyncFlowControl,
    VideoOutput,
    DEFAULT_KEEPALIVE_INTERVAL_SECS,
};
use guacr_protocol::{format_chunked_blobs, format_img, format_instruction, GuacamoleParser};
use guacr_terminal::{
    CopyDetector, FrameBuffer, ScrollDetector, ScrollDirection, SoftwareH264Encoder,
};
use image::{ImageEncoder, RgbaImage};
use log::{debug, error, info, trace, warn};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;
use tokio::io::{AsyncRead, AsyncReadExt, AsyncWrite};
use tokio::sync::mpsc;

use crate::vnc_protocol::VncProtocol;

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
        from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
    ) -> guacr_handlers::Result<()> {
        info!("VNC handler starting connection");

        // Parse VNC settings
        let settings = VncSettings::from_params(&params, &self.config)
            .map_err(HandlerError::InvalidParameter)?;

        // Create VNC client
        let mut client = VncClient::new(
            settings.width,
            settings.height,
            settings.read_only,
            settings.security.clone(),
            settings.recording_config.clone(),
            settings.jpeg_quality,
            settings.use_jpeg,
            settings.supports_webp,
            settings.supports_jpeg,
            settings.frame_rate,
            to_client,
            &params,
            video_tx,
        );

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

        info!("VNC handler connection ended");
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
    ) -> Result<(), HandlerError> {
        // Use common event adapter helper (eliminates boilerplate)
        guacr_handlers::connect_with_event_adapter(
            |params, to_client, from_client, video_tx| {
                self.connect(params, to_client, from_client, video_tx)
            },
            params,
            callback,
            from_client,
            video_tx,
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
    #[cfg(feature = "sftp")]
    pub enable_sftp: bool,
    #[cfg(feature = "sftp")]
    pub sftp_hostname: Option<String>,
    #[cfg(feature = "sftp")]
    pub sftp_username: Option<String>,
    #[cfg(feature = "sftp")]
    pub sftp_password: Option<String>,
    #[cfg(feature = "sftp")]
    pub sftp_private_key: Option<String>,
    #[cfg(feature = "sftp")]
    pub sftp_private_key_passphrase: Option<String>,
    #[cfg(feature = "sftp")]
    pub sftp_port: u16,
}

impl VncSettings {
    pub fn from_params(
        params: &HashMap<String, String>,
        defaults: &VncConfig,
    ) -> Result<Self, String> {
        let conn = guacr_handlers::ConnectionParameters::from_params(params, defaults.default_port)
            .map_err(|e| e.to_string())?;
        let hostname = conn.hostname;
        let port = conn.port;
        let password = conn.password;

        // IMPORTANT: Always use DEFAULT size during initialization (like guacd does)
        // The client will send a resize instruction with actual browser dimensions after handshake
        // This prevents "half screen" display issues
        info!("VNC: Using default handshake size - will resize after client connects");
        let width = defaults.default_width;
        let height = defaults.default_height;

        // Parse security settings
        let security = HandlerSecuritySettings::from_params(params);
        let read_only = security.read_only;
        info!(
            "VNC: Security settings - read_only={}, disable_copy={}, disable_paste={}",
            security.read_only, security.disable_copy, security.disable_paste
        );

        // Parse recording configuration
        let recording_config = RecordingConfig::from_params(params);
        if recording_config.is_enabled() {
            info!(
                "VNC: Recording enabled - ses={}, asciicast={}, typescript={}",
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
            "VNC: Image encoding - use_jpeg={}, quality={}, frame_rate={} FPS",
            use_jpeg, jpeg_quality, frame_rate
        );

        #[cfg(feature = "sftp")]
        let (
            enable_sftp,
            sftp_hostname,
            sftp_username,
            sftp_password,
            sftp_private_key,
            sftp_private_key_passphrase,
            sftp_port,
        ) = guacr_handlers::parse_sftp_config(params).map_err(|e| e.to_string())?;

        info!(
            "VNC Settings: {}:{}, {}x{}, read_only={}",
            hostname, port, width, height, read_only
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
            #[cfg(feature = "sftp")]
            enable_sftp,
            #[cfg(feature = "sftp")]
            sftp_hostname,
            #[cfg(feature = "sftp")]
            sftp_username,
            #[cfg(feature = "sftp")]
            sftp_password,
            #[cfg(feature = "sftp")]
            sftp_private_key,
            #[cfg(feature = "sftp")]
            sftp_private_key_passphrase,
            #[cfg(feature = "sftp")]
            sftp_port,
        })
    }
}

// ============================================================================
// VNC Client - Connection and event loop
// ============================================================================

/// VNC client wrapper for VNC connections
struct VncClient {
    framebuffer: FrameBuffer,
    stream_id: u32,
    width: u32,
    height: u32,
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
    /// JPEG quality (1-100) - max quality for adaptive quality manager
    #[allow(dead_code)] // Used only to initialize adaptive_quality
    jpeg_quality: u8,
    /// Use JPEG encoding (vs PNG)
    use_jpeg: bool,
    /// Client supports WebP format
    supports_webp: bool,
    /// Client supports JPEG format
    supports_jpeg: bool,
    /// Frame rate limit (FPS) - currently unused for VNC (server controls rate)
    #[allow(dead_code)]
    frame_rate: u32,
    #[cfg(feature = "sftp")]
    sftp_session: Option<russh_sftp::client::SftpSession>,
    /// Cursor manager for client-side cursor rendering (matches KCM behavior)
    cursor_manager: CursorManager,
    /// VNC pixel format (needed for cursor parsing)
    pixel_format: Option<crate::vnc_protocol::VncPixelFormat>,
    /// Adaptive quality manager (bandwidth-aware quality adjustment, shared with RDP)
    adaptive_quality: AdaptiveQuality,
    /// Sync flow control (prevents overwhelming slow clients, shared with RDP)
    sync_control: SyncFlowControl,
    to_client: mpsc::Sender<Bytes>,
    /// WebRTC video track for H.264 output (None = Guacamole JPEG path)
    video_tx: Option<Arc<dyn VideoOutput>>,
    /// Software H.264 encoder (present when video_tx is Some)
    h264_encoder: Option<SoftwareH264Encoder>,
}

impl VncClient {
    #[allow(clippy::too_many_arguments)]
    fn new(
        width: u32,
        height: u32,
        read_only: bool,
        security: HandlerSecuritySettings,
        recording_config: RecordingConfig,
        jpeg_quality: u8,
        use_jpeg: bool,
        supports_webp: bool,
        supports_jpeg: bool,
        frame_rate: u32,
        to_client: mpsc::Sender<Bytes>,
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
                    info!("VNC: Session recording initialized");
                    Some(rec)
                }
                Err(e) => {
                    warn!("VNC: Failed to initialize recording: {}", e);
                    None
                }
            }
        } else {
            None
        };

        Self {
            framebuffer: FrameBuffer::new(width, height),
            stream_id: 1,
            width,
            height,
            read_only,
            security,
            recorder,
            scroll_detector: ScrollDetector::new(width, height),
            drag_detector: DragDetector::new(width, height),
            copy_detector: CopyDetector::new(width, height),
            jpeg_quality,
            use_jpeg,
            supports_webp,
            supports_jpeg,
            frame_rate,
            #[cfg(feature = "sftp")]
            sftp_session: None,
            cursor_manager: CursorManager::new(supports_jpeg, supports_webp, jpeg_quality),
            pixel_format: None,
            adaptive_quality: AdaptiveQuality::new(jpeg_quality),
            sync_control: SyncFlowControl::new(),
            to_client,
            h264_encoder: None,
            video_tx,
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
        shared_send_and_record(
            &self.to_client,
            &mut self.recorder,
            Bytes::from(instruction.to_string()),
        )
        .await
    }

    /// Record client input instruction (if recording is enabled)
    fn record_client_input(&mut self, instruction: &Bytes) {
        shared_record_client_input(&mut self.recorder, instruction);
    }

    async fn send_sync(&mut self) -> Result<(), String> {
        let timestamp = guacr_terminal::current_time_millis();

        let sync_instr = format!("4.sync,{}.{};", timestamp.to_string().len(), timestamp);

        self.send_and_record(&sync_instr).await?;

        // Store pending sync for flow control (prevents overwhelming slow clients)
        self.sync_control.set_pending_sync(timestamp);

        Ok(())
    }

    async fn maybe_encode_h264(&mut self) -> Result<(), String> {
        if self.framebuffer.dirty_rects().is_empty() {
            return Ok(());
        }

        let encoder = match self.h264_encoder.as_mut() {
            Some(e) => e,
            None => return Ok(()),
        };
        let video_tx = match self.video_tx.as_ref() {
            Some(v) => v.clone(),
            None => return Ok(()),
        };

        let force_keyframe = video_tx
            .keyframe_requested()
            .swap(false, std::sync::atomic::Ordering::AcqRel);

        let bps = video_tx
            .target_bitrate_bps()
            .load(std::sync::atomic::Ordering::Relaxed);
        if bps > 0 {
            encoder.update_bitrate(bps);
        }

        let pixels = self.framebuffer.get_all_pixels();
        let (data, is_keyframe) = encoder
            .encode_rgba(&pixels, force_keyframe)
            .map_err(|e| format!("H.264 encode failed: {}", e))?;

        let pts = encoder.frame_count().saturating_sub(1) * 3000;

        video_tx
            .send_frame(EncodedFrame {
                data,
                is_keyframe,
                pts,
            })
            .await
            .map_err(|e| format!("H.264 send_frame failed: {}", e))?;

        self.framebuffer.clear_dirty();

        Ok(())
    }

    async fn connect(
        &mut self,
        hostname: &str,
        port: u16,
        password: Option<&str>,
        mut from_client: mpsc::Receiver<Bytes>,
        #[cfg(feature = "sftp")] settings: Option<&VncSettings>,
        #[cfg(not(feature = "sftp"))] _settings: Option<&VncSettings>,
    ) -> Result<(), String> {
        info!(
            "VNC: Connecting to {}:{} (timeout: {}s)",
            hostname, port, self.security.connection_timeout_secs
        );

        // Connect with timeout (matches guacd behavior)
        let mut stream =
            connect_tcp_with_timeout((hostname, port), self.security.connection_timeout_secs)
                .await
                .map_err(|e| format!("{}", e))?;

        info!("VNC: TCP connection established");

        let (_version, pixel_format, server_width, server_height, server_name) =
            VncProtocol::handshake(&mut stream, password)
                .await
                .map_err(|e| format!("VNC handshake failed: {}", e))?;

        info!(
            "VNC: Handshake complete - {}x{}, server: {}",
            server_width, server_height, server_name
        );

        self.width = server_width as u32;
        self.height = server_height as u32;
        self.framebuffer = FrameBuffer::new(self.width, self.height);
        self.pixel_format = Some(pixel_format);

        if self.video_tx.is_some() {
            match SoftwareH264Encoder::new(self.width, self.height) {
                Ok(enc) => {
                    self.h264_encoder = Some(enc);
                    info!(
                        "VNC: H.264 software encoder initialized ({}x{})",
                        self.width, self.height
                    );
                }
                Err(e) => {
                    warn!(
                        "VNC: Failed to initialize H.264 encoder, falling back to JPEG: {}",
                        e
                    );
                }
            }
        }

        // Send ready and name instructions to client
        send_ready(&self.to_client, "vnc-ready")
            .await
            .map_err(|e| e.to_string())?;
        send_name(&self.to_client, "VNC")
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
            info!("VNC: Initial cursor set to pointer");
        }

        // Enable cursor pseudo-encoding for client-side cursor rendering (matches KCM)
        VncProtocol::send_set_encodings(&mut stream, !self.read_only)
            .await
            .map_err(|e| format!("Failed to send encodings: {}", e))?;

        #[cfg(feature = "sftp")]
        if let Some(settings) = settings {
            if settings.enable_sftp {
                let sftp_hostname = settings
                    .sftp_hostname
                    .as_ref()
                    .ok_or_else(|| "SFTP enabled but sftp_hostname missing".to_string())?;
                let sftp_username = settings
                    .sftp_username
                    .as_ref()
                    .ok_or_else(|| "SFTP enabled but sftp_username missing".to_string())?;
                match crate::sftp_integration::establish_sftp_session(
                    sftp_hostname,
                    settings.sftp_port,
                    sftp_username,
                    settings.sftp_password.as_deref(),
                    settings.sftp_private_key.as_deref(),
                    settings.sftp_private_key_passphrase.as_deref(),
                )
                .await
                {
                    Ok(sftp) => {
                        self.sftp_session = Some(sftp);
                        info!("VNC: SFTP session established");
                    }
                    Err(e) => {
                        warn!("VNC: Failed to establish SFTP session: {}", e);
                    }
                }
            }
        }

        VncProtocol::send_framebuffer_update_request(
            &mut stream,
            false,
            0,
            0,
            server_width,
            server_height,
        )
        .await
        .map_err(|e| format!("Failed to request framebuffer update: {}", e))?;

        info!("VNC: Connection established, waiting for framebuffer updates");

        let mut read_buf = vec![0u8; 65536];

        // Keep-alive manager (matches guacd's guac_socket_require_keep_alive behavior)
        let mut keepalive = KeepAliveManager::new(DEFAULT_KEEPALIVE_INTERVAL_SECS);
        let mut keepalive_interval =
            tokio::time::interval(Duration::from_secs(DEFAULT_KEEPALIVE_INTERVAL_SECS));
        keepalive_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        let mut encode_interval = tokio::time::interval(Duration::from_millis(33));
        encode_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        loop {
            tokio::select! {
                _ = encode_interval.tick(), if self.h264_encoder.is_some() => {
                    if let Err(e) = self.maybe_encode_h264().await {
                        warn!("VNC: H.264 encode error: {}", e);
                    }
                }

                // Keep-alive ping to detect dead connections
                _ = keepalive_interval.tick() => {
                    if let Some(sync_instr) = keepalive.check() {
                        trace!("VNC: Sending keep-alive sync");
                        if shared_send_and_record(&self.to_client, &mut self.recorder, sync_instr).await.is_err() {
                            info!("VNC: Client channel closed, ending session");
                            break;
                        }
                    }
                }

                result = stream.read(&mut read_buf) => {
                    match result {
                        Ok(0) => {
                            info!("VNC: Connection closed by server");
                            break;
                        }
                        Ok(n) => {
                            if let Err(e) = self.process_vnc_messages(&mut stream, &read_buf[..n]).await {
                                error!("VNC: Error processing messages: {}", e);
                                break;
                            }

                            // Wait for client sync acknowledgment if pending (flow control)
                            if let Some(ts) = self.sync_control.pending_timestamp() {
                                if let Err(e) = self.sync_control.wait_for_client_sync(&mut from_client, ts).await {
                                    warn!("VNC: Sync flow control error: {}", e);
                                    break;
                                }
                                self.sync_control.clear_pending();
                                trace!("VNC: Client acknowledged sync, ready for next frame");
                            }
                        }
                        Err(e) => {
                            error!("VNC: Read error: {}", e);
                            break;
                        }
                    }
                }

                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("VNC: Client disconnected");
                        break;
                    };
                    if let Err(e) = self.handle_client_input(&mut stream, &msg).await {
                        warn!("VNC: Error handling client input: {}", e);
                    }
                }

                else => {
                    debug!("VNC: Connection closed");
                    break;
                }
            }
        }

        // Finalize recording
        if let Some(recorder) = self.recorder.take() {
            if let Err(e) = recorder.finalize() {
                warn!("VNC: Failed to finalize recording: {}", e);
            } else {
                info!("VNC: Session recording finalized");
            }
        }

        // Send disconnect instruction to client (matches Apache guacd behavior)
        send_disconnect(&self.to_client).await;

        info!("VNC: Connection ended");
        Ok(())
    }

    async fn process_vnc_messages<S>(&mut self, stream: &mut S, data: &[u8]) -> Result<(), String>
    where
        S: AsyncRead + AsyncWrite + Unpin,
    {
        if data.len() >= 4 && data[0] == 0 {
            match VncProtocol::parse_framebuffer_update_from_buffer(data) {
                Ok((rectangles, _bytes_consumed)) => {
                    for rect in rectangles {
                        self.handle_framebuffer_rectangle(rect).await?;
                    }

                    VncProtocol::send_framebuffer_update_request(
                        stream,
                        true,
                        0,
                        0,
                        self.width as u16,
                        self.height as u16,
                    )
                    .await?;
                }
                Err(e) => {
                    warn!("VNC: Failed to parse FramebufferUpdate: {}", e);
                }
            }
        }

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
                        VncProtocol::send_key_event(stream, keysym, pressed == 1).await?;
                    }
                }
            }
            "mouse" => {
                if instr.args.len() >= 3 {
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

                        // Feed mouse state to drag detector
                        self.drag_detector.notify_mouse_event(x, y, mask);

                        let x = x.max(0).min(self.width as i32 - 1) as u16;
                        let y = y.max(0).min(self.height as i32 - 1) as u16;

                        VncProtocol::send_pointer_event(stream, x, y, mask).await?;
                    }
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
                                "VNC: Resize requested: {}x{} (layer: {})",
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
            #[cfg(feature = "sftp")]
            "file" => {
                if let Some(ref mut sftp) = self.sftp_session {
                    if let Err(e) = crate::sftp_integration::handle_sftp_file_request(
                        sftp,
                        &instr.args.iter().map(|s| s.to_string()).collect::<Vec<_>>(),
                        &self.to_client,
                    )
                    .await
                    {
                        warn!("VNC: SFTP file operation failed: {}", e);
                    }
                } else {
                    warn!("VNC: File transfer requested but SFTP not enabled");
                }
            }
            _ => {}
        }

        Ok(())
    }

    /// Handle cursor update from VNC server (client-side cursor rendering)
    async fn handle_cursor_update(
        &mut self,
        rect: crate::vnc_protocol::VncRectangle,
    ) -> Result<(), String> {
        if self.read_only {
            // Don't send cursor updates in read-only mode
            return Ok(());
        }

        // Parse cursor data from VNC
        let pixel_format = self
            .pixel_format
            .as_ref()
            .ok_or_else(|| "Pixel format not set".to_string())?;

        let cursor = crate::vnc_protocol::VncProtocol::parse_cursor_data(
            rect.x,
            rect.y,
            rect.width,
            rect.height,
            &rect.pixels,
            pixel_format,
        )?;

        // Send cursor to client using shared cursor manager
        let instructions = self.cursor_manager.send_custom_cursor(
            &cursor.rgba_data,
            cursor.width as u32,
            cursor.height as u32,
            cursor.hotspot_x as i32,
            cursor.hotspot_y as i32,
        )?;

        for instr in instructions {
            self.send_and_record(&instr).await?;
        }

        debug!(
            "VNC: Sent cursor update {}x{} with hotspot ({}, {})",
            cursor.width, cursor.height, cursor.hotspot_x, cursor.hotspot_y
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
            Err(e) => warn!("VNC: Failed to decode Tight JPEG for framebuffer: {}", e),
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
        let pixel_count = rect.width as usize * rect.height as usize;
        let mut rgba_fill = vec![0u8; pixel_count * 4];
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
        let mut rgba_vec = vec![0u8; (rect.width as u32 * rect.height as u32 * 4) as usize];

        for i in 0..(rect.width as usize * rect.height as usize) {
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

        // When a video track is active, leave dirty rects set so the H.264 encode
        // timer can read them. Skip all Guacamole image instructions.
        if self.video_tx.is_some() {
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
        let framebuffer_pixels = self.framebuffer.get_all_pixels();
        if let Some(scroll_op) = self.scroll_detector.detect_scroll(&framebuffer_pixels) {
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

        // Empty pixel data — nothing to do
        if rect.pixels.is_empty() {
            return Ok(());
        }

        // Raw pixels path
        self.handle_raw_pixels(&rect).await
    }
}
