use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::EncodedFrame;
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
    // Cursor support
    CursorManager,
    EventBasedHandler,
    EventCallback,
    // Observability
    FpsCounter,
    HandlerError,
    // Security
    HandlerSecuritySettings,
    HandlerStats,
    HealthStatus,
    InstructionSender,
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
    VideoOutput,
    DEFAULT_KEEPALIVE_INTERVAL_SECS,
};
use guacr_protocol::{
    format_instruction, GuacamoleParser, TextProtocolEncoder, STATUS_UPSTREAM_ERROR,
    STATUS_UPSTREAM_NOT_FOUND, STATUS_UPSTREAM_TIMEOUT,
};
use image::RgbaImage;
use log::{debug, error, info, trace, warn};
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::net::TcpStream;
use tokio::sync::mpsc;

// IronRDP imports
use ironrdp::connector::{self, ClientConnector, ConnectionResult, Credentials, DesktopSize};
use ironrdp::pdu::gcc::{ConnectionType, KeyboardType};
use ironrdp::pdu::rdp::capability_sets::{MajorPlatformType, RailSupportLevel};
use ironrdp::session::image::DecodedImage;
use ironrdp::session::{ActiveStage, ActiveStageBuilder, ActiveStageOutput};
use ironrdp_core::WriteBuf;
use ironrdp_pdu::geometry::InclusiveRectangle;
use ironrdp_pdu::input::fast_path::{FastPathInputEvent, KeyboardFlags};
use ironrdp_pdu::input::mouse::PointerFlags;
use ironrdp_pdu::input::MousePdu;
use ironrdp_pdu::rdp::client_info::{PerformanceFlags, TimezoneInfo};
use ironrdp_pdu::rdp::headers::ShareDataPdu;
use ironrdp_pdu::rdp::refresh_rectangle::RefreshRectanglePdu;
use tokio_rustls::TlsConnector;

// DisplayControl for dynamic resize
use ironrdp_displaycontrol::client::DisplayControlClient;
use ironrdp_displaycontrol::pdu::MonitorLayoutEntry;

// Video session recording (fMP4 + AES-256-GCM + WebSocket upload to router)
use guacr_recorder::ZmqVideoSink;

// EGFX passthrough (H.264 from Windows GPU encoder)
use crate::audio_backend::{AudioChunk, GuacrRdpsndBackend};
use crate::clipboard_backend::{create_backend, PendingClipboardData};
use crate::egfx_handler::{EgfxPassthroughHandler, H264Frame};
use crossbeam_queue::ArrayQueue;
use ironrdp::dvc::DrdynvcClient;
use ironrdp_egfx::client::GraphicsPipelineClient;

// Threat detection (optional feature)
#[cfg(feature = "threat-detection")]
use guacr_threat_detection::{ThreatDetector, ThreatDetectorConfig};

type TokioTlsStream = tokio_rustls::client::TlsStream<TcpStream>;

// Re-export supporting modules
use crate::channel_handler::RdpChannelHandler;

// Import shared types from guacr-terminal
use guacr_terminal::{
    FrameBuffer, RdpInputHandler, CLIPBOARD_DEFAULT_SIZE, CLIPBOARD_MAX_SIZE, CLIPBOARD_MIN_SIZE,
};

/// Normalize a GraphicsUpdate rect from IronRDP before encoding.
///
/// IronRDP emits `{0,0,0,0}` for the initial full-frame update (no specific dirty-rect hint)
/// as well as for cursor-move-only no-ops where the image is empty.  Distinguish by checking
/// whether the image has content:
///
/// * `{0,0,0,0}` + image has content  → promote to full-image rect
/// * `{0,0,0,0}` + image is empty     → `None` (skip)
/// * anything else                     → `Some(rect)` unchanged
pub(crate) fn normalize_graphics_rect(
    rect: InclusiveRectangle,
    img_w: u16,
    img_h: u16,
) -> Option<InclusiveRectangle> {
    if rect.left == 0 && rect.top == 0 && rect.right == 0 && rect.bottom == 0 {
        if img_w == 0 || img_h == 0 {
            return None;
        }
        return Some(InclusiveRectangle {
            left: 0,
            top: 0,
            right: img_w - 1,
            bottom: img_h - 1,
        });
    }
    Some(rect)
}

/// Decide whether the software H.264 keepalive submit should fire.
///
/// The encoder must send a frame at least once per second even when the
/// framebuffer has not changed.  Without this, Chrome marks the video track
/// as inactive after ~5-10 s of silence and discards the decoder state,
/// causing a blank screen on the next real frame.
///
/// * `last_submit` — the `Instant` of the most-recent encoder submit, or
///   `None` if the encoder has never submitted a frame.
///
/// Returns `true` when `last_submit` is `Some` and its elapsed time is at
/// least one second.  Returns `false` for `None` (nothing to keep alive yet)
/// or when the submit was recent enough.
pub(crate) fn h264_keepalive_needed(last_submit: Option<std::time::Instant>) -> bool {
    last_submit
        .map(|t| t.elapsed() >= Duration::from_secs(1))
        .unwrap_or(false)
}

/// RDP server type detection for compatibility
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum RdpServerType {
    /// Native Windows RDP server (supports CredSSP, DVC)
    WindowsNative,
    /// xrdp/FreeRDP-based server (no CredSSP, no DVC, needs autologon)
    Xrdp,
    /// Unknown server type (use safe defaults)
    Unknown,
}

/// Map a Guacamole `security` parameter value and server-type heuristic to
/// `(enable_credssp, autologon)` for the IronRDP connector.
///
/// The explicit `security_mode` always wins over the heuristic when it gives
/// a definitive answer.  `"any"` or unknown values fall back to the heuristic.
pub(crate) fn resolve_credssp_settings(
    security_mode: &str,
    server_type: RdpServerType,
) -> (bool, bool) {
    let (heuristic_credssp, heuristic_autologon) = match server_type {
        RdpServerType::WindowsNative => (true, false),
        RdpServerType::Xrdp => (false, true),
        RdpServerType::Unknown => (false, true),
    };
    match security_mode {
        "nla" => (true, false),
        "tls" | "rdp" => (false, heuristic_autologon),
        _ => (heuristic_credssp, heuristic_autologon),
    }
}

/// RDP protocol handler
///
/// Connects to RDP servers and provides remote desktop access via the Guacamole protocol.
///
/// ## Rendering Method
///
/// RDP always uses the H.264 WebRTC video track — the JPEG dirty-rect path has been removed.
/// Requires the caller to supply a `video_tx`; connections without one are rejected at connect
/// time with a clear error message.
///
/// Two H.264 paths:
/// - Windows with EGFX: GPU-encoded frames from `EgfxPassthroughHandler` (zero software encode).
/// - xrdp / non-EGFX: software OpenH264 encode of the full framebuffer at 30fps via `maybe_encode_h264_rdp`.
#[derive(Clone)]
pub struct RdpHandler {
    config: RdpConfig,
}

#[derive(Debug, Clone)]
pub struct RdpConfig {
    pub default_port: u16,
    pub default_width: u32,
    pub default_height: u32,
    pub default_dpi: u32,
    pub security_mode: String,
    /// Clipboard buffer size in bytes (256KB - 50MB)
    pub clipboard_buffer_size: usize,
    /// Whether clipboard copy is disabled
    pub disable_copy: bool,
    /// Whether clipboard paste is disabled
    pub disable_paste: bool,
}

impl Default for RdpConfig {
    fn default() -> Self {
        Self {
            default_port: 3389,
            default_width: 1920,
            default_height: 1080,
            default_dpi: 96, // Standard Windows DPI (matches guacd default)
            security_mode: "nla".to_string(), // Network Level Authentication
            clipboard_buffer_size: CLIPBOARD_DEFAULT_SIZE,
            disable_copy: false,
            disable_paste: false,
        }
    }
}

impl RdpHandler {
    pub fn new(config: RdpConfig) -> Self {
        Self { config }
    }

    pub fn with_defaults() -> Self {
        Self::new(RdpConfig::default())
    }
}

/// Software openh264 cannot sustain 30fps much above ~1080p — measured 2026-08-04 on a
/// Precision 5540 (real code, not a proxy): 19.6fps best case at 3292x1724 even after
/// fixing openh264's slow RGBA->YUV conversion path. The vault sends a *device*
/// resolution (CSS pixels × devicePixelRatio), so a Retina display becomes e.g. 3816×1926,
/// which starves the encoder and freezes the session (RDP's "didn't connect" symptom).
/// This caps the requested desktop to a software-encodable budget, preserving aspect ratio;
/// the browser upscales the video track. Dimensions are forced even (H.264 requirement).
pub(crate) const RDP_MAX_ENCODE_WIDTH: u32 = 1920;
pub(crate) const RDP_MAX_ENCODE_HEIGHT: u32 = 1080;

/// Ceiling used when FFmpeg hardware encode is available (see `hardware_encode_available`).
/// Measured 2026-08-04: NVENC held 32.9fps at 3292x1724, comfortably above 30fps — a
/// generous bound rather than "no cap", since resolution is decided before the RDP
/// connection negotiates desktop size and nothing sanity-checks it downstream.
pub(crate) const RDP_MAX_ENCODE_WIDTH_HW: u32 = 3840;
pub(crate) const RDP_MAX_ENCODE_HEIGHT_HW: u32 = 2160;

/// True if this build has FFmpeg hardware H.264 support compiled in and libavcodec exposes
/// at least one candidate encoder. This — not `EncoderPipeline::backend_kind()` — is the
/// signal available here, because the encode resolution decision happens *before* the RDP
/// connection negotiates desktop size (`clamp_resolution` below shapes the actual RDP
/// session resolution, not a post-capture downscale), so no encoder exists yet to inspect.
/// Probing is cheap (~178µs measured) and does not guarantee a device will actually open —
/// if it later doesn't, `make_encoder` falls back to software at this now-too-high
/// resolution; `h264_pipeline`'s construction site logs a warning when that mismatch is
/// observed via `backend_kind()`, so it's visible rather than a silent freeze.
#[cfg(feature = "ffmpeg")]
fn hardware_encode_available() -> bool {
    guacr_encoder::ffmpeg_backend::probe()
}

#[cfg(not(feature = "ffmpeg"))]
fn hardware_encode_available() -> bool {
    false
}

/// Pure decision logic, factored out so it's testable without depending on the runtime
/// probe result (which varies by build features and host hardware).
pub(crate) fn resolution_cap_defaults(hardware_available: bool) -> (u32, u32) {
    if hardware_available {
        (RDP_MAX_ENCODE_WIDTH_HW, RDP_MAX_ENCODE_HEIGHT_HW)
    } else {
        (RDP_MAX_ENCODE_WIDTH, RDP_MAX_ENCODE_HEIGHT)
    }
}

/// Runtime override for the encode resolution cap, for validating whether a given
/// encoder can sustain higher resolutions without rebuilding the wheel:
/// `GUACR_RDP_MAX_ENCODE_WIDTH` / `GUACR_RDP_MAX_ENCODE_HEIGHT`. Invalid or absent
/// values keep the (hardware-aware) compiled defaults. Zero disables the cap entirely
/// (pass-through).
pub(crate) fn encode_resolution_cap() -> (u32, u32) {
    fn env_u32(name: &str, default: u32) -> u32 {
        match std::env::var(name) {
            Ok(v) => v.trim().parse::<u32>().unwrap_or(default),
            Err(_) => default,
        }
    }
    let (default_w, default_h) = resolution_cap_defaults(hardware_encode_available());
    (
        env_u32("GUACR_RDP_MAX_ENCODE_WIDTH", default_w),
        env_u32("GUACR_RDP_MAX_ENCODE_HEIGHT", default_h),
    )
}

pub(crate) fn clamp_resolution(width: u32, height: u32, max_w: u32, max_h: u32) -> (u32, u32) {
    // A zero budget on either axis means "no cap" — used by the env override to
    // request true pass-through of the client's device resolution.
    if max_w == 0 || max_h == 0 {
        return (width, height);
    }
    if width == 0 || height == 0 || (width <= max_w && height <= max_h) {
        return (width, height);
    }
    // Uniform downscale by the tighter axis ratio to fit the budget, aspect preserved.
    let scale = (max_w as f64 / width as f64).min(max_h as f64 / height as f64);
    let w = (((width as f64 * scale) as u32).max(2)) & !1;
    let h = (((height as f64 * scale) as u32).max(2)) & !1;
    (w, h)
}

#[async_trait]
impl ProtocolHandler for RdpHandler {
    fn name(&self) -> &str {
        "rdp"
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
        info!("[conn={conn_id}] RDP handler starting connection");

        // -- GUID-based viewer join (Phase 6b)
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
            info!("[conn={conn_id}] RDP: viewer mode for session {sid:?}");
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
                    info!("[conn={conn_id}] RDP: registered shared session {sid:?}");
                    handle.set_viewer_input_channel(viewer_input_tx);
                    owner_sender.attach_session(handle);
                }
                Err(e) => {
                    warn!(
                        "[conn={conn_id}] RDP: failed to register session {sid:?}: {e} — continuing as standalone"
                    );
                }
            }
        }

        // Parse RDP settings
        let settings = RdpSettings::from_params(&params, &self.config)
            .map_err(HandlerError::InvalidParameter)?;

        // RDP requires a WebRTC video track. Reject connections without one early so
        // the client receives a clear error rather than a blank screen.
        if video_tx.is_none() {
            let msg =
                "RDP requires a video track. The vault must negotiate H.264 for RDP sessions."
                    .to_string();
            send_error_best_effort(&to_client, &msg, STATUS_UPSTREAM_ERROR).await;
            return Err(HandlerError::ConnectionFailed(msg));
        }

        // Create session
        let mut session = IronRdpSession::new(
            settings.width,
            settings.height,
            settings.dpi,
            settings.clipboard_buffer_size,
            settings.disable_copy,
            settings.disable_paste,
            settings.read_only,
            settings.security.connection_timeout_secs,
            settings.recording_config.clone(),
            owner_sender,
            share_id.clone(),
            &params,
            video_tx,
            conn_id.clone(),
        );
        // Wire viewer input channel so PRIV_CONTROL viewers can send key/mouse events.
        if share_id.is_some() {
            session.viewer_input_rx = Some(viewer_input_rx);
        }

        // Connect and run session.
        // owner_sender is consumed by the session; the session calls
        // owner_sender.owner_disconnect() internally via its share_id field.
        session
            .connect_and_run(
                &settings.hostname,
                settings.port,
                &settings.username,
                &settings.password,
                settings.domain.as_deref(),
                from_client,
                Some(&settings),
            )
            .await
            .map_err(HandlerError::ConnectionFailed)?;

        info!("[conn={conn_id}] RDP handler connection ended");
        Ok(())
    }

    async fn health_check(&self) -> guacr_handlers::Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    async fn stats(&self) -> guacr_handlers::Result<HandlerStats> {
        Ok(HandlerStats::default())
    }
}

// Event-based handler implementation for zero-copy integration
#[async_trait]
impl EventBasedHandler for RdpHandler {
    fn name(&self) -> &str {
        "rdp"
    }

    async fn connect_with_events(
        &self,
        params: HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> Result<(), HandlerError> {
        let conn_id = params.get("client_id").cloned().unwrap_or_default();
        // RDP sends 3 instructions per frame (img, blob, end) and can have multiple
        // frames in flight, so we need a larger buffer than text-based protocols
        let (to_client, mut handler_rx) = mpsc::channel::<Bytes>(1024);

        let sender = InstructionSender::new(callback);
        let sender_arc = Arc::new(sender);

        let sender_clone = Arc::clone(&sender_arc);
        let forward_handle = tokio::spawn(async move {
            while let Some(msg) = handler_rx.recv().await {
                if let Err(e) = sender_clone.send(msg).await {
                    log::error!("[conn={conn_id}] RDP: Failed to send instruction: {}", e);
                    break;
                }
            }
        });

        let result = self
            .connect(params, to_client, from_client, video_tx, _hooks)
            .await;
        // Abort the forwarding task so it doesn't run orphaned after the session ends.
        forward_handle.abort();
        result?;

        Ok(())
    }
}

// ============================================================================
// RDP Settings - Parameter parsing and validation
// ============================================================================

/// RDP connection settings
#[derive(Debug, Clone)]
pub struct RdpSettings {
    pub hostname: String,
    pub port: u16,
    pub username: String,
    pub password: String,
    pub width: u32,
    pub height: u32,
    pub dpi: u32,
    pub security_mode: String,
    pub clipboard_buffer_size: usize,
    pub disable_copy: bool,
    pub disable_paste: bool,
    /// Read-only mode - blocks keyboard/mouse input
    pub read_only: bool,
    /// Security settings (includes connection timeout)
    pub security: HandlerSecuritySettings,
    pub domain: Option<String>,
    /// Server type hint for compatibility (windows, xrdp, auto)
    pub server_type: Option<String>,
    pub ignore_cert: bool,
    pub cert_fingerprint: Option<String>,
    /// Recording configuration
    pub recording_config: RecordingConfig,
    /// Drive redirection settings
    pub enable_drive: bool,
    pub drive_path: Option<String>,
    pub drive_name: String,
    pub disable_download: bool,
    pub disable_upload: bool,
}

impl RdpSettings {
    pub fn from_params(
        params: &HashMap<String, String>,
        defaults: &RdpConfig,
    ) -> Result<Self, String> {
        let conn = guacr_handlers::ConnectionParameters::from_params(params, defaults.default_port)
            .map_err(|e| e.to_string())?;
        let hostname = conn.hostname;
        let port = conn.port;

        let username = params
            .get("username")
            .ok_or_else(|| "Missing required parameter: username".to_string())?
            .clone();

        let password = params
            .get("password")
            .ok_or_else(|| "Missing required parameter: password".to_string())?
            .clone();

        // Parse width/height/dpi from connection parameters
        // Client sends "size" as "width,height,dpi" (e.g., "1920,1080,96")
        // If not provided, use defaults
        let (width, height, dpi) = if let Some(size_str) = params.get("size") {
            let parts: Vec<&str> = size_str.split(',').collect();
            if parts.len() >= 3 {
                let w = parts[0].parse().unwrap_or(defaults.default_width);
                let h = parts[1].parse().unwrap_or(defaults.default_height);
                let d = parts[2].parse().unwrap_or(defaults.default_dpi);
                (w, h, d)
            } else if parts.len() == 2 {
                let w = parts[0].parse().unwrap_or(defaults.default_width);
                let h = parts[1].parse().unwrap_or(defaults.default_height);
                (w, h, defaults.default_dpi)
            } else {
                (
                    defaults.default_width,
                    defaults.default_height,
                    defaults.default_dpi,
                )
            }
        } else {
            // Fallback to separate width/height/dpi params if size not present
            let w = params
                .get("width")
                .and_then(|w| w.parse().ok())
                .unwrap_or(defaults.default_width);
            let h = params
                .get("height")
                .and_then(|h| h.parse().ok())
                .unwrap_or(defaults.default_height);
            let d = params
                .get("dpi")
                .and_then(|d| d.parse().ok())
                .unwrap_or(defaults.default_dpi);
            (w, h, d)
        };

        // Cap to a software-encodable resolution (see clamp_resolution): the vault sends a
        // Retina *device* resolution that software openh264 can't drive at 30fps, freezing
        // the session. Downscale to fit, preserving aspect; the browser upscales the track.
        let (req_width, req_height) = (width, height);
        let (cap_w, cap_h) = encode_resolution_cap();
        let (width, height) = clamp_resolution(width, height, cap_w, cap_h);

        let conn_id = params.get("client_id").map(|s| s.as_str()).unwrap_or("");
        if (req_width, req_height) != (width, height) {
            info!(
                "[conn={conn_id}] RDP: Capped requested {req_width}x{req_height} -> {width}x{height} for software H.264 encode"
            );
        }
        info!(
            "[conn={conn_id}] RDP: Display settings - {}x{} @ {} DPI",
            width, height, dpi
        );

        let security_mode = params
            .get("security")
            .cloned()
            .unwrap_or_else(|| defaults.security_mode.clone());

        let clipboard_buffer_size = params
            .get("clipboard-buffer-size")
            .and_then(|s| s.parse().ok())
            .unwrap_or(defaults.clipboard_buffer_size);

        let clipboard_buffer_size =
            clipboard_buffer_size.clamp(CLIPBOARD_MIN_SIZE, CLIPBOARD_MAX_SIZE);

        let disable_copy = params
            .get("disable-copy")
            .map(|s| s == "true")
            .unwrap_or(defaults.disable_copy);

        let disable_paste = params
            .get("disable-paste")
            .map(|s| s == "true")
            .unwrap_or(defaults.disable_paste);

        let read_only = params
            .get("read-only")
            .map(|s| s == "true" || s == "1")
            .unwrap_or(false);

        // Parse security settings (includes connection timeout)
        let security = HandlerSecuritySettings::from_params(params);

        // Parse recording configuration
        let recording_config = RecordingConfig::from_params(params);

        let domain = params.get("domain").cloned();
        let server_type = params.get("server-type").cloned();
        let ignore_cert = params
            .get("ignore-cert")
            .map(|s| s == "true")
            .unwrap_or(false);
        let cert_fingerprint = params.get("cert-fingerprint").cloned();

        let enable_drive = params
            .get("enable-drive")
            .map(|v| v == "true")
            .unwrap_or(false);
        let drive_path = params.get("drive-path").cloned();
        let drive_name = params
            .get("drive-name")
            .cloned()
            .unwrap_or_else(|| "KeeperShare".to_string());
        let disable_download = params
            .get("disable-download")
            .map(|v| v == "true")
            .unwrap_or(false);
        let disable_upload = params
            .get("disable-upload")
            .map(|v| v == "true")
            .unwrap_or(false);

        info!(
            "[conn={conn_id}] RDP Settings: {}@{}:{}, {}x{}, security: {}, clipboard: {} bytes, read_only: {}",
            username,
            hostname,
            port,
            width,
            height,
            security_mode,
            clipboard_buffer_size,
            read_only
        );

        if recording_config.is_enabled() {
            info!(
                "[conn={conn_id}] RDP: Recording enabled - ses={}, asciicast={}, typescript={}",
                recording_config.is_ses_enabled(),
                recording_config.is_asciicast_enabled(),
                recording_config.is_typescript_enabled()
            );
        }

        Ok(Self {
            hostname,
            port,
            username,
            password,
            width,
            height,
            dpi,
            security_mode,
            clipboard_buffer_size,
            disable_copy,
            disable_paste,
            read_only,
            security,
            domain,
            server_type,
            ignore_cert,
            cert_fingerprint,
            recording_config,
            enable_drive,
            drive_path,
            drive_name,
            disable_download,
            disable_upload,
        })
    }
}

// ============================================================================
// Helper Functions
// ============================================================================

// ============================================================================
// RDPDR restriction wrapper (drive feature only)
// ============================================================================

/// Wraps any RdpdrBackend and enforces download/upload restrictions by returning
/// ACCESS_DENIED for read (download) or write (upload) I/O requests.
#[cfg(feature = "drive")]
#[derive(Debug)]
struct RestrictedRdpdrBackend {
    inner: Box<dyn ironrdp_rdpdr::RdpdrBackend>,
    disable_download: bool,
    disable_upload: bool,
}

#[cfg(feature = "drive")]
ironrdp_core::impl_as_any!(RestrictedRdpdrBackend);

#[cfg(feature = "drive")]
impl ironrdp_rdpdr::RdpdrBackend for RestrictedRdpdrBackend {
    fn handle_server_device_announce_response(
        &mut self,
        pdu: ironrdp_rdpdr::pdu::efs::ServerDeviceAnnounceResponse,
    ) -> ironrdp_pdu::PduResult<()> {
        self.inner.handle_server_device_announce_response(pdu)
    }

    fn handle_scard_call(
        &mut self,
        req: ironrdp_rdpdr::pdu::efs::DeviceControlRequest<ironrdp_rdpdr::pdu::esc::ScardIoCtlCode>,
        call: ironrdp_rdpdr::pdu::esc::ScardCall,
    ) -> ironrdp_pdu::PduResult<Vec<ironrdp_svc::SvcMessage>> {
        self.inner.handle_scard_call(req, call)
    }

    fn handle_drive_io_request(
        &mut self,
        req: ironrdp_rdpdr::pdu::efs::ServerDriveIoRequest,
    ) -> ironrdp_pdu::PduResult<Vec<ironrdp_svc::SvcMessage>> {
        use ironrdp_rdpdr::pdu::efs::*;
        use ironrdp_rdpdr::pdu::RdpdrPdu;
        use ironrdp_svc::SvcMessage;

        match &req {
            ServerDriveIoRequest::DeviceReadRequest(r) if self.disable_download => {
                Ok(vec![SvcMessage::from(RdpdrPdu::DeviceReadResponse(
                    DeviceReadResponse {
                        device_io_reply: DeviceIoResponse::new(
                            r.device_io_request.clone(),
                            NtStatus::ACCESS_DENIED,
                        ),
                        read_data: Vec::new(),
                    },
                ))])
            }
            ServerDriveIoRequest::DeviceWriteRequest(r) if self.disable_upload => {
                Ok(vec![SvcMessage::from(RdpdrPdu::DeviceWriteResponse(
                    DeviceWriteResponse {
                        device_io_reply: DeviceIoResponse::new(
                            r.device_io_request.clone(),
                            NtStatus::ACCESS_DENIED,
                        ),
                        length: 0,
                    },
                ))])
            }
            _ => self.inner.handle_drive_io_request(req),
        }
    }
}

// ============================================================================
// RDP Session - Complete connection and event loop
// ============================================================================

/// Complete ironrdp session manager
struct IronRdpSession {
    /// Connection ID extracted from params["client_id"] for log correlation.
    conn_id: String,
    framebuffer: FrameBuffer,
    input_handler: RdpInputHandler,
    // Zero-copy buffers for encoding (reused across frames)
    protocol_encoder: TextProtocolEncoder,
    /// Stream ID counter for Guacamole audio/ClearCodec instructions
    stream_id: u32,
    channel_handler: RdpChannelHandler,
    /// True when connected to an xrdp server — used to skip EGFX grace period.
    is_xrdp: bool,
    /// Read-only mode - blocks keyboard/mouse input
    read_only: bool,
    /// Connection timeout in seconds
    connection_timeout_secs: u64,
    /// Active recorder for .guac format session recording
    recorder: Option<MultiFormatRecorder>,
    owner_sender: SessionOwnerSender,
    /// Session share-id if this session is shared; used for owner_disconnect on cleanup.
    share_id: Option<String>,
    width: u32,
    height: u32,
    dpi: u32,
    // Sync flow control (prevents overwhelming slow clients)
    sync_control: guacr_handlers::SyncFlowControl,

    // Tracks when the last sync was sent (for timeout detection in keepalive)
    sync_sent_at: Option<std::time::Instant>,

    // Track if first frame has been sent (skip sync wait on first frame)
    first_frame_sent: bool,

    // Software H.264 path (xrdp / non-EGFX servers).
    // EncoderPipeline runs encoding on a dedicated thread; we submit at 30fps and drain
    // completed NALs to send over the WebRTC video track.
    h264_pipeline: Option<guacr_encoder::pipeline::EncoderPipeline>,
    framebuffer_dirty_for_h264: bool,
    // Last time a frame was submitted to the H.264 encoder (for keepalive).
    h264_last_submit: Option<std::time::Instant>,
    // Last bitrate pushed to the encoder, so BWE updates only reconfigure on change.
    h264_last_bitrate_bps: u32,

    // Cursor manager for client-side cursor rendering (matches KCM behavior)
    cursor_manager: CursorManager,

    // ZMQ address for video recording — passed to ZmqVideoSink at connect time
    video_zmq_addr: Option<String>,
    // Video session recording via ZMQ — Some when video_zmq_addr is set
    video_recorder: Option<ZmqVideoSink>,

    // H.264 video output — always Some (required for RDP; session is rejected at connect if None)
    video_tx: Option<Arc<dyn VideoOutput>>,
    // EGFX passthrough queue — Some when video_tx is Some; frames queued by EgfxPassthroughHandler
    egfx_frames: Option<Arc<ArrayQueue<H264Frame>>>,
    // ClearCodec decoded frame queue (T-023 to T-027). Drained by the main loop.
    clearcodec_frames: Option<Arc<ArrayQueue<crate::egfx_handler::ClearCodecFrame>>>,
    // CLIPRDR clipboard backend message receiver (T-028 to T-031). UnboundedReceiver is Send.
    cliprdr_rx:
        Option<tokio::sync::mpsc::UnboundedReceiver<ironrdp::cliprdr::backend::ClipboardMessage>>,
    // Shared clipboard state between main loop and CLIPRDR backend.
    cliprdr_data: Option<Arc<parking_lot::Mutex<PendingClipboardData>>>,
    // RDPSND audio chunk queue (T-032 to T-034). Drained by the main loop.
    audio_chunks: Option<Arc<ArrayQueue<AudioChunk>>>,
    // Flipped to true on the first EGFX frame.  Used to gate the software H.264 encoder:
    // when true, the encode_interval tick is skipped and GPU-encoded frames are sent instead.
    egfx_active: Arc<AtomicBool>,

    // Timestamp of the first GDI update received after video_tx was set.
    egfx_grace_start: Option<std::time::Instant>,

    // AI threat detection — Some when threat_detection_baml_endpoint param is provided
    #[cfg(feature = "threat-detection")]
    threat_detector: Option<std::sync::Arc<ThreatDetector>>,
    // Per-session ID for threat detection state tracking
    #[cfg(feature = "threat-detection")]
    threat_session_id: String,
    // Username and hostname captured for threat detection context
    #[cfg(feature = "threat-detection")]
    threat_username: String,
    #[cfg(feature = "threat-detection")]
    threat_hostname: String,

    // Per-session observability counters
    stats: SessionStats,
    fps_counter: FpsCounter,

    // Viewer key/mouse input channel (Phase 6b). Receives bytes forwarded from
    // connected viewers with PRIV_CONTROL via SessionHandle::forward_viewer_input().
    // None for standalone sessions (no share-id).
    viewer_input_rx: Option<tokio::sync::mpsc::UnboundedReceiver<Bytes>>,
}

impl IronRdpSession {
    #[allow(clippy::too_many_arguments)]
    fn new(
        width: u32,
        height: u32,
        dpi: u32,
        clipboard_buffer_size: usize,
        disable_copy: bool,
        disable_paste: bool,
        read_only: bool,
        connection_timeout_secs: u64,
        recording_config: RecordingConfig,
        owner_sender: SessionOwnerSender,
        share_id: Option<String>,
        params: &HashMap<String, String>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        conn_id: String,
    ) -> Self {
        // RDP requires a WebRTC video track.
        //
        //   Windows with EGFX  →  EgfxPassthroughHandler queues GPU-encoded H.264;
        //                          egfx_active flips true on first frame.
        //                          Soft encoder is initialised as a fallback for the window
        //                          between connection and first EGFX frame, then released.
        //
        //   xrdp / non-EGFX   →  EGFX never activates; framebuffer updates set
        //                          framebuffer_dirty_for_h264 = true; the 30fps
        //                          encode_interval drives software H.264 encoding.

        // Parse ZMQ video recording address from params (only relevant when video_tx is Some)
        let video_zmq_addr = if video_tx.is_some() {
            params.get("recording-zmq-addr-video").cloned()
        } else {
            None
        };

        let egfx_active = Arc::new(AtomicBool::new(false));
        let (video_tx, egfx_frames, clearcodec_frames) = if let Some(vtx) = video_tx {
            (
                Some(vtx),
                // EGFX H.264 passthrough frames. Sized to ride out a transient stall
                // in the consumer (a single video-track write has been measured at
                // 261ms) without discarding anything: at 30fps, 16 slots is ~530ms of
                // slack. Deeper would only convert dropped frames into added latency.
                // See PassthroughH264Decoder::decode for the overflow policy.
                Some(Arc::new(ArrayQueue::new(16))),
                Some(Arc::new(ArrayQueue::new(64))),
            )
        } else {
            (None, None, None)
        };
        let protocol_encoder = TextProtocolEncoder::new();

        // Initialize recording if enabled
        let recorder = if recording_config.is_enabled() {
            // RDP doesn't have cols/rows like terminal, use width/height
            match MultiFormatRecorder::new(
                &recording_config,
                params,
                "rdp",
                width as u16,
                height as u16,
            ) {
                Ok(rec) => {
                    info!("[conn={conn_id}] RDP: Session recording initialized");
                    Some(rec)
                }
                Err(e) => {
                    warn!(
                        "[conn={conn_id}] RDP: Failed to initialize recording: {}",
                        e
                    );
                    None
                }
            }
        } else {
            None
        };

        // Initialize threat detection if the feature is enabled and baml endpoint is configured
        #[cfg(feature = "threat-detection")]
        let threat_detector = {
            if let Some(baml_endpoint) = params.get("threat_detection_baml_endpoint") {
                let config = ThreatDetectorConfig {
                    baml_endpoint: baml_endpoint.clone(),
                    baml_api_key: params.get("threat_detection_baml_api_key").cloned(),
                    enabled: true,
                    auto_terminate: params
                        .get("threat_detection_auto_terminate")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    min_log_level: params
                        .get("threat_detection_min_log_level")
                        .and_then(|s| match s.as_str() {
                            "critical" => Some(guacr_threat_detection::ThreatLevel::Critical),
                            "high" => Some(guacr_threat_detection::ThreatLevel::High),
                            "medium" => Some(guacr_threat_detection::ThreatLevel::Medium),
                            "low" => Some(guacr_threat_detection::ThreatLevel::Low),
                            _ => None,
                        })
                        .unwrap_or(guacr_threat_detection::ThreatLevel::Low),
                    command_history_size: params
                        .get("threat_detection_command_history_size")
                        .and_then(|s| s.parse().ok())
                        .unwrap_or(10),
                    timeout_seconds: params
                        .get("threat_detection_timeout_seconds")
                        .and_then(|s| s.parse().ok())
                        .unwrap_or(5),
                    deny_tags: {
                        let (deny, _) = guacr_handlers::parse_threat_detection_risk_levels(params);
                        deny
                    },
                    allow_tags: {
                        let (_, allow) = guacr_handlers::parse_threat_detection_risk_levels(params);
                        allow
                    },
                    enable_tag_checking: true,
                    proactive_mode: params
                        .get("threat_detection_proactive_mode")
                        .map(|s| s == "true")
                        .unwrap_or(false),
                    approval_timeout_ms: params
                        .get("threat_detection_approval_timeout_ms")
                        .and_then(|s| s.parse().ok())
                        .unwrap_or(2000),
                    fail_closed_on_error: params
                        .get("threat_detection_fail_closed_on_error")
                        .map(|s| s == "true")
                        .unwrap_or(false),
                    show_approval_status: params
                        .get("threat_detection_show_approval_status")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    auto_approve_safe_commands: params
                        .get("threat_detection_auto_approve_safe_commands")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    config_allow_ai_session_terminate: params
                        .get("threat_detection_config_allow_ai_session_terminate")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    resource_ai_session_terminate_enabled: params
                        .get("threat_detection_resource_ai_session_terminate_enabled")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    level_terminate_flags: HashMap::new(),
                };

                match ThreatDetector::new(config) {
                    Ok(detector) => {
                        info!(
                            "[conn={conn_id}] RDP: Threat detection enabled with BAML endpoint: {}",
                            baml_endpoint
                        );
                        Some(std::sync::Arc::new(detector))
                    }
                    Err(e) => {
                        warn!(
                            "[conn={conn_id}] RDP: Failed to initialize threat detection: {}",
                            e
                        );
                        None
                    }
                }
            } else {
                None
            }
        };
        #[cfg(feature = "threat-detection")]
        let threat_session_id = uuid::Uuid::new_v4().to_string();

        Self {
            conn_id,
            framebuffer: FrameBuffer::new(width, height),
            input_handler: RdpInputHandler::new(),
            protocol_encoder,
            stream_id: 1,
            is_xrdp: false,
            channel_handler: RdpChannelHandler::new(
                clipboard_buffer_size,
                disable_copy,
                disable_paste,
            ),
            read_only,
            connection_timeout_secs,
            recorder,
            owner_sender,
            share_id: share_id.clone(),
            width,
            height,
            dpi,

            // Initialize sync flow control (15s timeout, 3 strikes - matches guacd)
            sync_control: guacr_handlers::SyncFlowControl::new(),

            // No pending sync initially
            sync_sent_at: None,

            // Track first frame (skip sync wait to avoid blocking initial display)
            first_frame_sent: false,

            h264_pipeline: None,
            framebuffer_dirty_for_h264: false,
            h264_last_submit: None,
            h264_last_bitrate_bps: 0,

            // Initialize cursor manager for client-side cursor rendering
            cursor_manager: CursorManager::new(false, false, 92),

            video_tx,
            egfx_frames,
            clearcodec_frames,
            egfx_active,
            cliprdr_rx: None,
            cliprdr_data: None,
            audio_chunks: None,
            egfx_grace_start: None,
            video_zmq_addr,
            video_recorder: None,
            #[cfg(feature = "threat-detection")]
            threat_detector,
            #[cfg(feature = "threat-detection")]
            threat_session_id,
            // Username and hostname are not yet known at new() time; set in connect_and_run
            #[cfg(feature = "threat-detection")]
            threat_username: String::new(),
            #[cfg(feature = "threat-detection")]
            threat_hostname: String::new(),
            stats: SessionStats::new("rdp"),
            fps_counter: FpsCounter::new(),
            viewer_input_rx: None,
        }
    }

    #[allow(clippy::too_many_arguments)]
    async fn connect_and_run(
        mut self,
        hostname: &str,
        port: u16,
        username: &str,
        password: &str,
        domain: Option<&str>,
        from_client: mpsc::Receiver<Bytes>,
        settings: Option<&RdpSettings>,
    ) -> Result<(), String> {
        // Initialize ZMQ video recorder if recording-zmq-addr-video param was set
        if let Some(addr) = self.video_zmq_addr.take() {
            match ZmqVideoSink::new(&addr, self.width, self.height, false).await {
                Ok(sink) => {
                    self.video_recorder = Some(sink);
                    info!("[conn={}] RDP: ZMQ video recorder initialized ({})", self.conn_id, addr);
                }
                Err(e) => warn!(
                    "[conn={}] RDP: Failed to initialize ZMQ video recorder, recording disabled: {}",
                    self.conn_id, e
                ),
            }
        }

        // Capture hostname and username for threat detection context
        #[cfg(feature = "threat-detection")]
        {
            self.threat_hostname = hostname.to_string();
            self.threat_username = username.to_string();
        }

        info!(
            "[conn={}] RDP: Connecting to {}:{} (timeout: {}s)",
            self.conn_id, hostname, port, self.connection_timeout_secs
        );

        // Build IronRDP connector config
        let settings_ref = settings.ok_or("RDP settings required")?;
        let config = self.build_ironrdp_config(username, password, domain, settings_ref);
        self.is_xrdp = matches!(self.detect_server_type(settings_ref), RdpServerType::Xrdp);

        // Establish TCP connection with timeout (matches guacd behavior)
        let stream =
            match connect_tcp_with_timeout((hostname, port), self.connection_timeout_secs).await {
                Ok(s) => s,
                Err(e) => {
                    let msg = format!("{}", e);
                    send_error_best_effort(
                        self.owner_sender.transport_sender(),
                        &msg,
                        STATUS_UPSTREAM_TIMEOUT,
                    )
                    .await;
                    return Err(msg);
                }
            };

        info!("[conn={}] RDP: TCP connection established", self.conn_id);

        // Perform RDP handshake and authentication
        let drive_args = if settings_ref.enable_drive {
            settings_ref.drive_path.as_deref().map(|p| {
                (
                    p,
                    settings_ref.drive_name.as_str(),
                    settings_ref.disable_download,
                    settings_ref.disable_upload,
                )
            })
        } else {
            None
        };
        // Receive the ClearCodec queue and CLIPRDR state from perform_rdp_handshake.
        let mut handshake_clearcodec_frames: Option<
            Arc<ArrayQueue<crate::egfx_handler::ClearCodecFrame>>,
        > = None;
        let mut handshake_cliprdr_rx: Option<
            tokio::sync::mpsc::UnboundedReceiver<ironrdp::cliprdr::backend::ClipboardMessage>,
        > = None;
        let mut handshake_cliprdr_data: Option<Arc<parking_lot::Mutex<PendingClipboardData>>> =
            None;
        let mut handshake_audio_chunks: Option<Arc<ArrayQueue<AudioChunk>>> = None;
        let (connection_result, framed) = match self
            .perform_rdp_handshake(
                stream,
                config,
                hostname.to_string(),
                settings_ref.ignore_cert,
                settings_ref.cert_fingerprint.clone(),
                drive_args,
                &mut handshake_clearcodec_frames,
                &mut handshake_cliprdr_rx,
                &mut handshake_cliprdr_data,
                &mut handshake_audio_chunks,
            )
            .await
        {
            Ok(result) => result,
            Err(e) => {
                let msg = format!("RDP handshake failed: {}", e);
                send_error_best_effort(
                    self.owner_sender.transport_sender(),
                    &msg,
                    STATUS_UPSTREAM_ERROR,
                )
                .await;
                return Err(msg);
            }
        };
        // Wire the ClearCodec queue for use in the main loop (T-023 to T-027).
        if handshake_clearcodec_frames.is_some() {
            self.clearcodec_frames = handshake_clearcodec_frames;
        }
        // Wire the CLIPRDR receiver and state for clipboard forwarding (T-028 to T-031).
        self.cliprdr_rx = handshake_cliprdr_rx;
        self.cliprdr_data = handshake_cliprdr_data;
        // Wire the audio queue for RDPSND draining (T-032 to T-034).
        self.audio_chunks = handshake_audio_chunks;

        info!(
            "[conn={}] RDP: Connection established - {}x{}",
            self.conn_id,
            connection_result.desktop_size.width,
            connection_result.desktop_size.height
        );

        // Update session dimensions if they differ from requested
        self.width = u32::from(connection_result.desktop_size.width);
        self.height = u32::from(connection_result.desktop_size.height);
        self.framebuffer = FrameBuffer::new(self.width, self.height);

        // Send ready and name instructions to client (matches Apache guacd behavior)
        send_ready(self.owner_sender.transport_sender(), "rdp-ready")
            .await
            .map_err(|e| e.to_string())?;
        send_name(self.owner_sender.transport_sender(), "RDP")
            .await
            .map_err(|e| e.to_string())?;

        // Set initial cursor to pointer (client-side cursor rendering, matches KCM)
        if !self.read_only {
            let cursor_instrs = self
                .cursor_manager
                .send_standard_cursor(StandardCursor::Pointer)
                .map_err(|e| format!("Failed to generate cursor: {}", e))?;
            for instr in cursor_instrs {
                self.send_and_record(&instr).await?;
            }
            info!(
                "[conn={}] RDP: Initial cursor set to pointer (client-side rendering)",
                self.conn_id
            );
        }

        // Send size instruction using the ADJUSTED display dimensions (what xrdp
        // actually uses after rounding to RDP-valid values, e.g. 1724→1728).
        // If we send the client-requested size (1724), Guacamole creates a 1724px
        // canvas. xrdp then sends dirty rects at coordinates up to 1728, which
        // triggers Guacamole's Layer.resize auto-expand → clears the entire canvas
        // on every dirty rect that touches the boundary. Using the adjusted size
        // ensures the canvas starts at the correct size and never needs expanding.
        let (adj_w, adj_h) = MonitorLayoutEntry::adjust_display_size(self.width, self.height);
        self.width = adj_w;
        self.height = adj_h;
        let size_instr = self
            .protocol_encoder
            .format_size_instruction(0, self.width, self.height);
        let size_instr_str = String::from_utf8_lossy(&size_instr).to_string();
        info!(
            "[conn={}] RDP: Sending size instruction (adjusted): {}",
            self.conn_id, size_instr_str
        );
        self.send_and_record(&size_instr_str).await?;

        info!(
            "[conn={}] RDP: Session ready, starting active session",
            self.conn_id
        );

        // Run the active RDP session.
        // owner_disconnect and session deregistration are handled inside run_active_session.
        self.run_active_session(connection_result, framed, from_client)
            .await
    }

    fn detect_server_type(&self, settings: &RdpSettings) -> RdpServerType {
        // Check explicit server-type parameter first
        if let Some(ref server_type_str) = settings.server_type {
            return match server_type_str.to_lowercase().as_str() {
                "windows" => RdpServerType::WindowsNative,
                "xrdp" => RdpServerType::Xrdp,
                _ => RdpServerType::Unknown,
            };
        }

        // Auto-detection heuristics:
        // 1. If domain is set, likely Windows Active Directory
        if settings.domain.is_some() {
            return RdpServerType::WindowsNative;
        }

        // 2. Default to xrdp-compatible mode (works with both xrdp and Windows)
        //    This is the safest default as:
        //    - xrdp requires: CredSSP=false, autologon=true, no DVC
        //    - Windows works with: CredSSP=false, autologon=true (just slower auth)
        RdpServerType::Xrdp
    }

    fn build_ironrdp_config(
        &self,
        username: &str,
        password: &str,
        domain: Option<&str>,
        settings: &RdpSettings,
    ) -> connector::Config {
        // Detect server type, then resolve CredSSP/autologon from explicit security_mode.
        // The explicit parameter always wins over the heuristic when set to nla/tls/rdp.
        let server_type = self.detect_server_type(settings);
        let (enable_credssp, autologon) =
            resolve_credssp_settings(&settings.security_mode, server_type);

        info!(
            "[conn={}] RDP: Detected server type: {:?}, CredSSP: {}, Autologon: {}",
            self.conn_id, server_type, enable_credssp, autologon
        );

        connector::Config {
            credentials: Credentials::UsernamePassword {
                username: username.to_string(),
                password: password.to_string(),
            },
            domain: domain.map(|s| s.to_string()),
            enable_tls: true,
            enable_credssp,
            enable_standard_rdp_security: false,
            keyboard_type: KeyboardType::IBM_ENHANCED,
            keyboard_subtype: 0,
            keyboard_layout: 0,
            keyboard_functional_keys_count: 12,
            connection_type: ConnectionType::Lan,
            ime_file_name: String::new(),
            dig_product_id: String::new(),
            desktop_size: DesktopSize {
                width: self.width as u16,
                height: self.height as u16,
            },
            bitmap: None,
            client_build: 0,
            client_name: "guacr-rdp".to_owned(),
            client_dir: "C:\\\\Windows\\\\System32\\\\mstscax.dll".to_owned(),
            #[cfg(target_os = "macos")]
            platform: MajorPlatformType::MACINTOSH,
            #[cfg(target_os = "linux")]
            platform: MajorPlatformType::UNIX,
            #[cfg(target_os = "windows")]
            platform: MajorPlatformType::WINDOWS,
            #[cfg(not(any(target_os = "macos", target_os = "linux", target_os = "windows")))]
            platform: MajorPlatformType::UNIX,
            enable_server_pointer: true, // Enable pointer events from RDP server (required for cursor)
            request_data: None,
            autologon,
            enable_audio_playback: false,
            pointer_software_rendering: false, // Client-side cursor rendering via PointerBitmap events (matches KCM)
            performance_flags: PerformanceFlags::default()
                | PerformanceFlags::ENABLE_DESKTOP_COMPOSITION,
            desktop_scale_factor: 0,
            hardware_id: None,
            license_cache: None,
            timezone_info: TimezoneInfo::default(),
            alternate_shell: String::new(),
            work_dir: String::new(),
            compression_type: None,
            multitransport_flags: None,
            remote_application_mode: false,
            rail_support_level: RailSupportLevel::empty(),
            monitor_layout: None,
            enable_audio_capture: false,
        }
    }

    #[allow(clippy::too_many_arguments)]
    async fn perform_rdp_handshake(
        &self,
        stream: TcpStream,
        config: connector::Config,
        server_name: String,
        ignore_cert: bool,
        cert_fingerprint: Option<String>,
        _drive_settings: Option<(&str, &str, bool, bool)>,
        clearcodec_frames_out: &mut Option<Arc<ArrayQueue<crate::egfx_handler::ClearCodecFrame>>>,
        cliprdr_rx_out: &mut Option<
            tokio::sync::mpsc::UnboundedReceiver<ironrdp::cliprdr::backend::ClipboardMessage>,
        >,
        cliprdr_data_out: &mut Option<Arc<parking_lot::Mutex<PendingClipboardData>>>,
        audio_chunks_out: &mut Option<Arc<ArrayQueue<AudioChunk>>>,
    ) -> Result<
        (
            ConnectionResult,
            ironrdp_tokio::Framed<ironrdp_tokio::MovableTokioStream<TokioTlsStream>>,
        ),
        String,
    > {
        use ironrdp_tokio::{connect_begin, connect_finalize, mark_as_upgraded, Framed};

        let client_addr = stream
            .local_addr()
            .map_err(|e| format!("Failed to get local address: {}", e))?;

        let mut framed = Framed::<ironrdp_tokio::MovableTokioStream<_>>::new(stream);

        let mut connector = ClientConnector::new(config, client_addr);

        // Register DVC channels.
        // DisplayControlClient enables dynamic resize on Windows servers.
        // EgfxPassthroughHandler intercepts GPU-encoded H.264 frames when video output is active.
        // xrdp silently ignores DVC channels it does not support, so this is safe for all servers.
        {
            let mut drdynvc = DrdynvcClient::new()
                .with_dynamic_channel(DisplayControlClient::new(|_| Ok(Vec::new())));
            if let Some(frames_arc) = self.egfx_frames.clone() {
                let (egfx_handler, egfx_decoder, cc_queue) =
                    EgfxPassthroughHandler::new(frames_arc, self.egfx_active.clone());
                // Return the ClearCodec queue to the caller (connect_and_run) via out-param.
                *clearcodec_frames_out = Some(cc_queue);
                drdynvc = drdynvc.with_dynamic_channel(GraphicsPipelineClient::new(
                    Box::new(egfx_handler),
                    Some(Box::new(egfx_decoder)),
                ));
                info!(
                    "[conn={}] RDP: EGFX GraphicsPipeline DVC registered for H.264 passthrough + ClearCodec",
                    self.conn_id
                );
            }
            connector.attach_static_channel(drdynvc);
        }

        // Register CLIPRDR static virtual channel for clipboard forwarding (T-028 to T-031).
        // AC-4: this is best-effort — if the server doesn't negotiate CLIPRDR, the session
        // continues without clipboard (graceful fallback).
        {
            use ironrdp::cliprdr::CliprdrClient;
            let (backend, cliprdr_rx, cliprdr_data) =
                create_backend(std::env::temp_dir().to_string_lossy().to_string());
            *cliprdr_rx_out = Some(cliprdr_rx);
            *cliprdr_data_out = Some(cliprdr_data);
            let cliprdr = CliprdrClient::new(Box::new(backend));
            connector.attach_static_channel(cliprdr);
            info!(
                "[conn={}] RDP: CLIPRDR static virtual channel registered for clipboard forwarding",
                self.conn_id
            );
        }

        // Register RDPSND static virtual channel for audio output (T-032 to T-034).
        // AC-3: If the server doesn't negotiate audio, wave() is never called — no error.
        {
            use ironrdp::rdpsnd::client::Rdpsnd;
            let audio_queue = Arc::new(ArrayQueue::new(128));
            let backend = GuacrRdpsndBackend::new(Arc::clone(&audio_queue));
            *audio_chunks_out = Some(audio_queue);
            let rdpsnd = Rdpsnd::new(Box::new(backend));
            connector.attach_static_channel(rdpsnd);
            info!(
                "[conn={}] RDP: RDPSND static virtual channel registered for audio output",
                self.conn_id
            );
        }

        // Register RDPDR for drive redirection
        #[cfg(feature = "drive")]
        if let Some((path, name, disable_download, disable_upload)) = _drive_settings {
            use ironrdp_rdpdr::Rdpdr;

            #[cfg(any(target_os = "linux", target_os = "macos"))]
            let platform_backend: Box<dyn ironrdp_rdpdr::RdpdrBackend> = {
                use ironrdp_rdpdr_native::backend::NixRdpdrBackend;
                Box::new(NixRdpdrBackend::new(path.to_string()))
            };

            #[cfg(target_os = "windows")]
            let platform_backend: Box<dyn ironrdp_rdpdr::RdpdrBackend> = {
                use ironrdp_rdpdr_native::{RedirectedDrive, WindowsRdpdrBackendFactory};
                let drive = RedirectedDrive::new(1, name.to_string(), path.to_string(), false)
                    .expect("valid drive configuration");
                Box::new(WindowsRdpdrBackendFactory::new(drive).build())
            };

            let backend: Box<dyn ironrdp_rdpdr::RdpdrBackend> = Box::new(RestrictedRdpdrBackend {
                inner: platform_backend,
                disable_download,
                disable_upload,
            });

            let rdpdr = Rdpdr::new(backend, "KeeperGateway".to_owned())
                .with_drives(Some(vec![(1u32, name.to_string())]));
            connector.attach_static_channel(rdpdr);
            info!(
                "[conn={}] RDP: Drive redirection enabled: path={} name={} disable_download={} disable_upload={}",
                self.conn_id, path, name, disable_download, disable_upload
            );
        }

        // Begin RDP connection (X.224, MCS)
        let should_upgrade = connect_begin(&mut framed, &mut connector)
            .await
            .map_err(|e| format!("RDP connection begin failed: {}", e))?;

        info!(
            "[conn={}] RDP: Initial handshake complete, performing TLS upgrade",
            self.conn_id
        );

        // TLS upgrade
        let initial_stream = framed.into_inner_no_leftover();
        let (upgraded_stream, server_public_key) = self
            .tls_upgrade(
                initial_stream,
                &server_name,
                ignore_cert,
                cert_fingerprint.as_deref(),
            )
            .await
            .map_err(|e| format!("TLS upgrade failed: {}", e))?;

        let upgraded = mark_as_upgraded(should_upgrade, &mut connector);
        let mut upgraded_framed =
            Framed::<ironrdp_tokio::MovableTokioStream<_>>::new(upgraded_stream);

        // Finalize connection (authentication, capability negotiation)
        // PR #1043 changed parameter order and made network_client required
        let mut dummy_network_client = DummyNetworkClient;
        let connection_result = connect_finalize(
            upgraded,
            connector,
            &mut upgraded_framed,
            &mut dummy_network_client,
            server_name.into(),
            server_public_key,
            None, // kerberos_config
        )
        .await
        .map_err(|e| format!("RDP connection finalize failed: {}", e))?;

        info!("[conn={}] RDP: Connection established - client-side cursor rendering enabled (matches KCM)", self.conn_id);
        Ok((connection_result, upgraded_framed))
    }

    async fn tls_upgrade(
        &self,
        stream: TcpStream,
        server_name: &str,
        ignore_cert: bool,
        cert_fingerprint: Option<&str>,
    ) -> Result<(TokioTlsStream, Vec<u8>), String> {
        use tokio_rustls::rustls;

        // Install default crypto provider if not already installed (required for Rustls
        // 0.23+). Use aws-lc-rs to match this crate's declared rustls feature; relying on
        // `ring` only compiled by accident via workspace feature unification and broke when
        // guacr-rdp was built in isolation.
        let _ = rustls::crypto::aws_lc_rs::default_provider().install_default();

        let mut config = if ignore_cert {
            rustls::ClientConfig::builder()
                .dangerous()
                .with_custom_certificate_verifier(std::sync::Arc::new(
                    DangerousNoCertificateVerification,
                ))
                .with_no_client_auth()
        } else {
            let root_store = rustls::RootCertStore {
                roots: webpki_roots::TLS_SERVER_ROOTS.to_vec(),
            };
            rustls::ClientConfig::builder()
                .with_root_certificates(root_store)
                .with_no_client_auth()
        };

        // Disable TLS resumption (not supported by CredSSP)
        config.resumption = rustls::client::Resumption::disabled();

        let connector = TlsConnector::from(std::sync::Arc::new(config));
        let server_name_owned = rustls::pki_types::ServerName::try_from(server_name.to_string())
            .map_err(|e| format!("Invalid server name: {}", e))?;

        let tls_stream = connector
            .connect(server_name_owned, stream)
            .await
            .map_err(|e| format!("TLS connection failed: {}", e))?;

        // Extract server public key
        let (_, session) = tls_stream.get_ref();
        let cert = session
            .peer_certificates()
            .and_then(|certs| certs.first())
            .ok_or_else(|| "No peer certificate found".to_string())?;

        let server_public_key = extract_tls_server_public_key(cert.as_ref())
            .map_err(|e| format!("Failed to extract server public key: {}", e))?;

        // Certificate pinning: if a fingerprint is configured, verify it.
        if let Some(expected_fp) = cert_fingerprint {
            if !cert_fingerprint_matches(cert.as_ref(), expected_fp) {
                return Err(format!(
                    "RDP server certificate fingerprint mismatch — \
                     expected {expected_fp} but got a different certificate. \
                     This may indicate a MITM attack."
                ));
            }
            debug!(
                "[conn={}] RDP: Certificate fingerprint verified",
                self.conn_id
            );
        }

        Ok((tls_stream, server_public_key))
    }

    async fn run_active_session(
        mut self,
        connection_result: ConnectionResult,
        mut framed: ironrdp_tokio::Framed<ironrdp_tokio::MovableTokioStream<TokioTlsStream>>,
        mut from_client: mpsc::Receiver<Bytes>,
    ) -> Result<(), String> {
        use ironrdp_tokio::FramedWrite;

        // ActiveStage::new(ConnectionResult) was removed upstream (ironrdp-session no longer
        // depends on ironrdp-connector); build from the ConnectionResult fields instead.
        let mut active_stage = ActiveStageBuilder {
            static_channels: connection_result.static_channels,
            user_channel_id: connection_result.user_channel_id,
            io_channel_id: connection_result.io_channel_id,
            message_channel_id: connection_result.message_channel_id,
            share_id: connection_result.share_id,
            compression_type: connection_result.compression_type,
            enable_server_pointer: connection_result.enable_server_pointer,
            pointer_software_rendering: connection_result.pointer_software_rendering,
        }
        .build();
        let mut image = DecodedImage::new(
            ironrdp::graphics::image_processing::PixelFormat::RgbA32,
            self.width as u16,
            self.height as u16,
        );

        // Keep-alive manager (matches guacd's guac_socket_require_keep_alive behavior)
        let mut keepalive = KeepAliveManager::new(DEFAULT_KEEPALIVE_INTERVAL_SECS);
        let mut keepalive_interval =
            tokio::time::interval(Duration::from_secs(DEFAULT_KEEPALIVE_INTERVAL_SECS));
        keepalive_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        // 60fps encode loop (16ms). EGFX sessions (Windows RDP) skip this branch entirely
        // when egfx_active=true, so the faster tick only affects xrdp/GDI sessions.
        let mut encode_interval = tokio::time::interval(Duration::from_millis(16));
        encode_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        info!("[conn={}] RDP: Active session started", self.conn_id);

        // xrdp won't repaint on reconnect unless the client explicitly requests it.
        // Send RefreshRect immediately so every session start gets a full repaint.
        if let Some(bytes) = self.encode_refresh_rect(&active_stage) {
            framed
                .write_all(&bytes)
                .await
                .map_err(|e| format!("RDP: Failed to send initial RefreshRect: {}", e))?;
            debug!(
                "[conn={}] RDP: Sent initial RefreshRect for {}x{}",
                self.conn_id, self.width, self.height
            );
        }

        // When the loop exits via a non-clean path (server error, fatal recording
        // failure, etc.) we store the error here so the cleanup block below always
        // runs before we propagate it to the caller.
        let mut exit_error: Option<String> = None;

        'event_loop: loop {
            tokio::select! {
                biased;

                // Handle client input — always first so keystrokes are never blocked by encoding
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("[conn={}] RDP: Client disconnected", self.conn_id);
                        break;
                    };
                    match self.handle_client_input_ironrdp(&mut framed, &msg, &mut active_stage, &mut image).await {
                        Ok(()) => {}
                        Err(ref e) if e.starts_with("TERMINATE:") => {
                            info!("[conn={}] RDP: Session terminated: {}", self.conn_id, &e["TERMINATE:".len()..]);
                            break;
                        }
                        Err(e) => {
                            warn!("[conn={}] RDP: Error handling client input: {}", self.conn_id, e);
                        }
                    }
                }

                // Viewer key/mouse input forwarded from a connected viewer with PRIV_CONTROL.
                viewer_msg = async {
                    match self.viewer_input_rx {
                        Some(ref mut rx) => rx.recv().await,
                        None => std::future::pending().await,
                    }
                } => {
                    if let Some(msg) = viewer_msg {
                        if let Err(e) = self.handle_client_input_ironrdp(&mut framed, &msg, &mut active_stage, &mut image).await {
                            if !e.starts_with("TERMINATE:") {
                                debug!("[conn={}] RDP: viewer input error: {}", self.conn_id, e);
                            }
                        }
                    }
                }

                // Keep-alive ping to detect dead connections
                _ = keepalive_interval.tick() => {
                    // Check for sync timeout (client not responding)
                    if let Some(sent_at) = self.sync_sent_at {
                        if self.sync_control.check_timeout(sent_at.elapsed()) {
                            error!("[conn={}] RDP: Client not responding to sync - disconnecting", self.conn_id);
                            break;
                        }
                        if !self.sync_control.is_waiting_for_sync() {
                            self.sync_sent_at = None;
                        }
                    }

                    if let Some(sync_instr) = keepalive.check() {
                        trace!("[conn={}] RDP: Sending keep-alive sync", self.conn_id);
                        if self.owner_sender.send(sync_instr).await.is_err() {
                            info!("[conn={}] RDP: Client channel closed, ending session", self.conn_id);
                            break;
                        }
                    }
                }

                // Software H.264 encode tick (30fps, xrdp / non-EGFX path).
                _ = encode_interval.tick(),
                    if self.video_tx.is_some()
                        && !self.egfx_active.load(Ordering::Acquire) =>
                {
                    if let Err(e) = self.maybe_encode_h264_rdp().await {
                        warn!("[conn={}] RDP: Software H.264 encode error: {}", self.conn_id, e);
                    }
                }

                // Handle incoming RDP frames
                result = framed.read_pdu() => {
                    match result {
                        Ok((action, payload)) => {
                            trace!("[conn={}] RDP: Received frame - action: {:?}, {} bytes", self.conn_id, action, payload.len());

                            let outputs = active_stage
                                .process(&mut image, action, &payload)
                                .map_err(|e| format!("Failed to process RDP frame: {}", e))?;

                            if outputs.is_empty() && payload.len() > 1000
                                && !self.egfx_active.load(Ordering::Relaxed)
                            {
                                debug!("[conn={}] RDP: Large frame ({} bytes) produced 0 outputs (EGFX PDU or channel data)", self.conn_id, payload.len());
                            }

                            trace!("[conn={}] RDP: ActiveStage returned {} outputs", self.conn_id, outputs.len());
                            for (idx, output) in outputs.iter().enumerate() {
                                trace!("[conn={}] RDP: Output {}: {:?}", self.conn_id, idx, output);
                            }

                            for output in outputs {
                                match output {
                                    ActiveStageOutput::ResponseFrame(frame) => {
                                        framed
                                            .write_all(&frame)
                                            .await
                                            .map_err(|e| format!("Failed to write response: {}", e))?;
                                    }
                                    ActiveStageOutput::GraphicsUpdate(rect) => {
                                        // Send graphics update to client
                                        debug!("[conn={}] RDP: GraphicsUpdate received - rect: {:?}, image size: {}x{}",
                                            self.conn_id, rect, image.width(), image.height());

                                        if let Some(effective) = normalize_graphics_rect(
                                            rect, image.width(), image.height(),
                                        ) {
                                            if self.egfx_active.load(Ordering::Acquire) {
                                                // EGFX passthrough: GPU-encoded H.264 frames are queued
                                                // by EgfxPassthroughHandler and drained after this loop.
                                            } else {
                                                // Non-EGFX (xrdp / pre-EGFX grace period): update the
                                                // framebuffer and mark it dirty for the software H.264
                                                // encoder. The 30fps encode_interval drives submission.
                                                let x = effective.left as u32;
                                                let y = effective.top as u32;
                                                let w = (effective.right - effective.left + 1) as u32;
                                                let h = (effective.bottom - effective.top + 1) as u32;
                                                self.framebuffer.update_region_from_fullscreen(
                                                    x, y, w, h, image.data(), self.width,
                                                );
                                                self.framebuffer_dirty_for_h264 = true;

                                                if self.egfx_grace_start.is_none() {
                                                    self.egfx_grace_start = Some(std::time::Instant::now());
                                                    debug!(
                                                        "[conn={}] RDP: First GDI update received, starting EGFX grace period",
                                                        self.conn_id
                                                    );
                                                }
                                            }
                                        } else {
                                            trace!("[conn={}] RDP: Skipping zero-size rect (cursor-only update)", self.conn_id);
                                        }

                                        if !self.first_frame_sent {
                                            self.first_frame_sent = true;
                                            debug!("[conn={}] RDP: First frame sent", self.conn_id);
                                        }
                                    }
                                    ActiveStageOutput::PointerDefault => {
                                        trace!("[conn={}] RDP: Pointer set to default", self.conn_id);
                                        if !self.read_only {
                                            match self.cursor_manager.send_standard_cursor(StandardCursor::Pointer) {
                                                Ok(instrs) => {
                                                    for instr in instrs {
                                                        if let Err(e) = self.send_and_record(&instr).await {
                                                            warn!("[conn={}] RDP: Failed to send default cursor: {}", self.conn_id, e);
                                                            break;
                                                        }
                                                    }
                                                }
                                                Err(e) => warn!("[conn={}] RDP: Failed to generate default cursor: {}", self.conn_id, e),
                                            }
                                        }
                                    }
                                    ActiveStageOutput::PointerHidden => {
                                        trace!("[conn={}] RDP: Pointer hidden", self.conn_id);
                                        if !self.read_only {
                                            match self.cursor_manager.send_standard_cursor(StandardCursor::None) {
                                                Ok(instrs) => {
                                                    for instr in instrs {
                                                        if let Err(e) = self.send_and_record(&instr).await {
                                                            warn!("[conn={}] RDP: Failed to hide cursor: {}", self.conn_id, e);
                                                            break;
                                                        }
                                                    }
                                                }
                                                Err(e) => warn!("[conn={}] RDP: Failed to generate hidden cursor: {}", self.conn_id, e),
                                            }
                                        }
                                    }
                                    ActiveStageOutput::PointerPosition { x, y } => {
                                        trace!("[conn={}] RDP: Pointer moved to ({}, {}) - client handles cursor locally", self.conn_id, x, y);
                                        // Client-side cursor position is handled by the browser automatically
                                        // No need to send position updates (cursor layer follows mouse)
                                    }
                                    ActiveStageOutput::PointerBitmap(pointer) => {
                                        debug!("[conn={}] RDP: Custom pointer bitmap received: {}x{} at hotspot ({}, {})",
                                            self.conn_id, pointer.width, pointer.height, pointer.hotspot_x, pointer.hotspot_y);

                                        // Send custom cursor to client using shared cursor manager
                                        if let Err(e) = self.send_custom_cursor(&pointer).await {
                                            warn!("[conn={}] RDP: Failed to send custom cursor: {}", self.conn_id, e);
                                        }
                                    }
                                    ActiveStageOutput::Terminate(reason) => {
                                        info!("[conn={}] RDP: Session terminated: {:?}", self.conn_id, reason);
                                        break 'event_loop;
                                    }
                                    other => {
                                        debug!("[conn={}] RDP: Unhandled ActiveStageOutput variant: {:?}", self.conn_id, other);
                                    }
                                }
                            }

                            // Drain H.264 frames queued by the EGFX handler during active_stage.process().
                            // Each call to process() may push one or more frames; we send all of them
                            // and follow with a single Guacamole sync to keep the client clock aligned.
                            if let (Some(ref frames), Some(ref video_tx)) =
                                (&self.egfx_frames, &self.video_tx)
                            {
                                let mut last_timestamp_us = 0u64;
                                let mut sent_any = false;
                                while let Some(frame) = frames.pop() {
                                    // Each frame gets its own timestamp so batched frames have
                                    // monotonically increasing PTS (rare but possible).
                                    let timestamp_us = std::time::SystemTime::now()
                                        .duration_since(std::time::UNIX_EPOCH)
                                        .unwrap_or_default()
                                        .as_micros() as u64;
                                    let pts = timestamp_us * 9 / 100; // microseconds → 90 kHz RTP clock
                                    last_timestamp_us = timestamp_us;
                                    let encoded = EncodedFrame {
                                        data: bytes::Bytes::from(frame.data),
                                        is_keyframe: frame.is_keyframe,
                                        pts,
                                    };
                                    // Tee to video recorder before sending to WebRTC
                                    if let Some(ref mut recorder) = self.video_recorder {
                                        if let Err(e) = recorder.write_video_frame(&encoded).await {
                                            warn!("[conn={}] RDP: Video recording error: {}", self.conn_id, e);
                                            exit_error = Some(format!("Recording failed: {}", e));
                                            break;
                                        }
                                    }
                                    video_tx
                                        .send_frame(encoded)
                                        .await
                                        .map_err(|e| format!("EGFX send_frame failed: {}", e))?;
                                    sent_any = true;
                                }
                                // Propagate a fatal recording failure to the outer loop.
                                if exit_error.is_some() {
                                    break;
                                }
                                if sent_any {
                                    if !self.first_frame_sent {
                                        self.first_frame_sent = true;
                                        debug!("[conn={}] RDP: First EGFX frame sent", self.conn_id);
                                    }
                                    let ts_ms = last_timestamp_us / 1000;
                                    let sync_instr =
                                        format_instruction("sync", &[&ts_ms.to_string()]);
                                    self.owner_sender
                                        .send(bytes::Bytes::from(sync_instr))
                                        .await
                                        .map_err(|_| {
                                            "client channel closed during EGFX video sync"
                                                .to_string()
                                        })?;
                                }
                            }

                            // T-028 to T-031: Process pending CLIPRDR clipboard messages.
                            // The backend sends ClipboardMessage events via mpsc; we drain them here
                            // and dispatch through the active_stage CLIPRDR SVC channel.
                            if let Some(ref mut rx) = self.cliprdr_rx {
                                use ironrdp::cliprdr::backend::ClipboardMessage;
                                use ironrdp::cliprdr::CliprdrClient;
                                while let Ok(msg) = rx.try_recv() {
                                    match msg {
                                        ClipboardMessage::SendInitiateCopy(formats) => {
                                            // Advertise our clipboard formats to the server (AC-3).
                                            if let Some(cliprdr) = active_stage.get_svc_processor_mut::<CliprdrClient>() {
                                                match cliprdr.initiate_copy(&formats) {
                                                    Ok(svc_msgs) => {
                                                        match active_stage.process_svc_processor_messages::<CliprdrClient>(svc_msgs) {
                                                            Ok(bytes) => {
                                                                framed.write_all(&bytes).await
                                                                    .map_err(|e| format!("CLIPRDR write error: {e}"))?;
                                                                debug!("[conn={}] RDP: CLIPRDR format list advertised to server", self.conn_id);
                                                            }
                                                            Err(e) => warn!("[conn={}] RDP: CLIPRDR initiate_copy encode error: {e}", self.conn_id),
                                                        }
                                                    }
                                                    Err(e) => warn!("[conn={}] RDP: CLIPRDR initiate_copy failed: {e}", self.conn_id),
                                                }
                                            }
                                        }
                                        ClipboardMessage::SendFormatData(response) => {
                                            // Respond to server's format data request (AC-3).
                                            if let Some(cliprdr) = active_stage.get_svc_processor_mut::<CliprdrClient>() {
                                                match cliprdr.submit_format_data(response) {
                                                    Ok(svc_msgs) => {
                                                        match active_stage.process_svc_processor_messages::<CliprdrClient>(svc_msgs) {
                                                            Ok(bytes) => {
                                                                framed.write_all(&bytes).await
                                                                    .map_err(|e| format!("CLIPRDR write error: {e}"))?;
                                                                info!("[conn={}] RDP: CLIPRDR format data sent to server (AC-1)", self.conn_id);
                                                            }
                                                            Err(e) => warn!("[conn={}] RDP: CLIPRDR submit encode error: {e}", self.conn_id),
                                                        }
                                                    }
                                                    Err(e) => warn!("[conn={}] RDP: CLIPRDR submit_format_data failed: {e}", self.conn_id),
                                                }
                                            }
                                        }
                                        ClipboardMessage::SendInitiatePaste(format_id) => {
                                            if let Some(cliprdr) = active_stage.get_svc_processor_mut::<CliprdrClient>() {
                                                match cliprdr.initiate_paste(format_id) {
                                                    Ok(svc_msgs) => {
                                                        match active_stage.process_svc_processor_messages::<CliprdrClient>(svc_msgs) {
                                                            Ok(bytes) => {
                                                                framed.write_all(&bytes).await
                                                                    .map_err(|e| format!("CLIPRDR write error: {e}"))?;
                                                            }
                                                            Err(e) => warn!("[conn={}] RDP: CLIPRDR paste encode error: {e}", self.conn_id),
                                                        }
                                                    }
                                                    Err(e) => warn!("[conn={}] RDP: CLIPRDR initiate_paste failed: {e}", self.conn_id),
                                                }
                                            }
                                        }
                                        _ => {
                                            debug!("[conn={}] RDP: Unhandled clipboard message variant", self.conn_id);
                                        }
                                    }
                                }
                            }

                            // T-023 to T-027 / T-074 AC-1+AC-2: Drain ClearCodec decoded frames
                            // and send as Guacamole image instructions (crisp bitmaps for text/UI).
                            // These co-render with H.264 on the same EGFX surface (AC-2).
                            let cc_queue = self.clearcodec_frames.clone();
                            if let Some(ref cc_frames) = cc_queue {
                                while let Some(cc) = cc_frames.pop() {
                                    if let Err(e) = self.send_clearcodec_frame(&cc).await {
                                        warn!("[conn={}] RDP: ClearCodec frame send error: {e}", self.conn_id);
                                    }
                                }
                            }

                            // T-032 to T-034: Drain RDPSND audio chunks and send as Guacamole
                            // audio stream instructions (AC-1, AC-2).
                            let audio_q = self.audio_chunks.clone();
                            if let Some(ref aq) = audio_q {
                                while let Some(chunk) = aq.pop() {
                                    if let Err(e) = self.send_audio_chunk(&chunk).await {
                                        warn!("[conn={}] RDP: Audio chunk send error: {e}", self.conn_id);
                                    }
                                }
                            }
                        }
                        Err(e) => {
                            error!("[conn={}] RDP: Read error: {}", self.conn_id, e);
                            // Store error so cleanup block runs before returning.
                            exit_error = Some(format!("RDP read error: {}", e));
                            break;
                        }
                    }
                }

                else => {
                    info!("[conn={}] RDP: Event loop ended", self.conn_id);
                    break;
                }
            }
        }

        info!(
            "[conn={}] session complete: {}",
            self.conn_id,
            self.stats.summary()
        );
        // Send disconnect instruction to client (matches Apache guacd behavior)
        send_disconnect(self.owner_sender.transport_sender()).await;

        // Finalize Guacamole .ses recording
        if let Some(recorder) = self.recorder.take() {
            if let Err(e) = recorder.finalize() {
                warn!(
                    "[conn={}] RDP: Failed to finalize recording: {}",
                    self.conn_id, e
                );
            } else {
                info!("[conn={}] RDP: Session recording finalized", self.conn_id);
            }
        }

        // Finalize ZMQ video recorder (closes socket → signals end-of-recording to Python)
        if let Some(recorder) = self.video_recorder.take() {
            if let Err(e) = recorder.finalize().await {
                warn!(
                    "[conn={}] RDP: Failed to finalize video recorder: {}",
                    self.conn_id, e
                );
            } else {
                info!("[conn={}] RDP: Video recording finalized", self.conn_id);
            }
        }

        // Clean up threat detection session state to prevent memory leak
        #[cfg(feature = "threat-detection")]
        if let Some(ref detector) = self.threat_detector {
            detector.cleanup_session(&self.threat_session_id);
        }

        // Notify viewers and deregister shared session.
        if let Some(ref sid) = self.share_id {
            self.owner_sender.owner_disconnect(sid);
        }

        // Propagate any error that caused the loop to exit early.
        if let Some(e) = exit_error {
            return Err(e);
        }

        Ok(())
    }

    /// Send custom RDP cursor to client via shared cursor manager
    async fn send_custom_cursor(
        &mut self,
        pointer: &ironrdp::graphics::pointer::DecodedPointer,
    ) -> Result<(), String> {
        if self.read_only {
            return Ok(());
        }

        let cursor_data = &pointer.bitmap_data;
        let width = pointer.width as u32;
        let height = pointer.height as u32;

        // Convert BGRA to RGBA (IronRDP uses BGRA format)
        let mut rgba_data = Vec::with_capacity((width * height * 4) as usize);
        for chunk in cursor_data.chunks(4) {
            if chunk.len() == 4 {
                rgba_data.push(chunk[2]); // R
                rgba_data.push(chunk[1]); // G
                rgba_data.push(chunk[0]); // B
                rgba_data.push(chunk[3]); // A
            }
        }

        // Use shared cursor manager (handles encoding and instruction generation)
        let instructions = self.cursor_manager.send_custom_cursor(
            &rgba_data,
            width,
            height,
            pointer.hotspot_x as i32,
            pointer.hotspot_y as i32,
        )?;

        // Send all cursor instructions
        for instr in instructions {
            self.send_and_record(&instr).await?;
        }

        debug!(
            "[conn={}] RDP: Sent custom cursor {}x{} with hotspot ({}, {})",
            self.conn_id, width, height, pointer.hotspot_x, pointer.hotspot_y
        );

        Ok(())
    }

    async fn handle_client_input_ironrdp(
        &mut self,
        framed: &mut ironrdp_tokio::Framed<ironrdp_tokio::MovableTokioStream<TokioTlsStream>>,
        msg: &Bytes,
        active_stage: &mut ActiveStage,
        image: &mut DecodedImage,
    ) -> Result<(), String> {
        use ironrdp_tokio::FramedWrite;

        // Debug: Log raw instruction
        trace!(
            "[conn={}] RDP: Raw client instruction: {}",
            self.conn_id,
            String::from_utf8_lossy(msg)
        );

        let instr = GuacamoleParser::parse_instruction(msg)
            .map_err(|e| format!("Failed to parse instruction: {}", e))?;

        // Record client input (if recording is enabled and includes keys/mouse)
        self.record_client_input(msg);

        // Tee key/mouse instructions to the video recorder's embedded data track
        // and to the threat detector (one intercept, two consumers)
        if matches!(instr.opcode, "key" | "mouse") {
            let ts_ms = guacr_terminal::current_time_millis();
            let instr_str = String::from_utf8_lossy(msg).into_owned();

            if let Some(ref mut recorder) = self.video_recorder {
                if let Err(e) = recorder.write_input_event(&instr_str, ts_ms).await {
                    warn!(
                        "[conn={}] RDP: Failed to record input event: {}",
                        self.conn_id, e
                    );
                }
            }

            // Threat detection: analyze key/mouse instructions for threats
            #[cfg(feature = "threat-detection")]
            if let Some(ref detector) = self.threat_detector {
                if detector.should_analyze("rdp", instr.opcode) {
                    match detector
                        .analyze_keystroke_sequence(
                            &self.threat_session_id,
                            &instr_str,
                            &self.threat_username,
                            &self.threat_hostname,
                            "rdp",
                        )
                        .await
                    {
                        Ok(threat) => {
                            if threat.should_terminate() {
                                error!(
                                    "[conn={}] RDP: TERMINATING SESSION due to threat in input: {}",
                                    self.conn_id, threat.description
                                );
                                let msg_text =
                                    format!("Session terminated: {}", threat.description);
                                send_error_best_effort(
                                    self.owner_sender.transport_sender(),
                                    &msg_text,
                                    517, // RESOURCE_CLOSED
                                )
                                .await;
                                return Err(format!("TERMINATE:{}", threat.description));
                            }
                        }
                        Err(e) => {
                            debug!(
                                "[conn={}] RDP: Threat detection error (non-fatal): {}",
                                self.conn_id, e
                            );
                        }
                    }

                    // Screenshot analysis stub — vision path for graphical threats.
                    // Triggered at the same events as keystroke analysis (Enter, click, Escape).
                    // DecodedImage::data() returns BGRA pixel data; convert to grayscale JPEG
                    // before sending to the BAML vision endpoint.
                    let img_data = image.data();
                    let (img_w, img_h) = (image.width(), image.height());
                    if img_w > 0 && img_h > 0 && img_data.len() >= (img_w * img_h * 4) as usize {
                        // DecodedImage is BGRA — build a pseudo-RGBA slice by swapping channels
                        // in a temporary buffer so rgba_to_grayscale_jpeg sees the right layout.
                        // Luminance is channel-order-independent for grayscale conversion
                        // (Y = 0.2126R + 0.7152G + 0.0722B — same formula regardless of order).
                        // We can reuse the BGRA data directly: just reinterpret channels.
                        // The luminance formula with BGRA layout: Y = 0.0722B + 0.7152G + 0.2126R
                        // (same components, different positional order — handled inside the helper).
                        match guacr_threat_detection::rgba_to_grayscale_jpeg(
                            img_data,
                            img_w as u32,
                            img_h as u32,
                            75,
                        ) {
                            Ok(gray_jpeg) => {
                                let sid = self.threat_session_id.clone();
                                let det = std::sync::Arc::clone(detector);
                                tokio::spawn(async move {
                                    if let Ok(analysis) =
                                        det.analyze_screenshot(&gray_jpeg, "", &sid).await
                                    {
                                        if analysis.result.level
                                            >= guacr_threat_detection::ThreatLevel::Medium
                                        {
                                            warn!(
                                                "[conn={}] RDP: screenshot threat: {} (level={:?})",
                                                sid,
                                                analysis.result.description,
                                                analysis.result.level
                                            );
                                        }
                                    }
                                });
                            }
                            Err(e) => {
                                debug!(
                                    "[conn={}] RDP: grayscale JPEG capture failed: {}",
                                    self.conn_id, e
                                );
                            }
                        }
                    }
                }
            }
        }

        match instr.opcode {
            "sync" => {
                // Client is acknowledging a sync instruction (flow control)
                if let Some(ts_str) = instr.args.first() {
                    if let Ok(client_ts) = ts_str.parse::<u64>() {
                        if let Some(pending_ts) = self.sync_control.pending_timestamp() {
                            if client_ts >= pending_ts {
                                // Client caught up with our sync
                                self.sync_control.clear_pending();
                                self.sync_control.reset_timeout_count();
                                self.sync_sent_at = None;
                                trace!(
                                    "[conn={}] RDP: Client acknowledged sync (ts={})",
                                    self.conn_id,
                                    client_ts
                                );
                            }
                        }
                    }
                }
                // Sync acks are not processed further
                return Ok(());
            }
            "key" => {
                if instr.args.len() >= 2 {
                    let keysym: u32 = instr.args[0].parse().map_err(|_| "Invalid keysym")?;
                    let pressed = instr.args[1] == "1";

                    // Security: Check read-only mode
                    // In graphical mode, allow Ctrl+C/Ctrl+Insert for copy
                    if self.read_only {
                        // TODO: Track modifier state for Ctrl detection
                        // For now, block all keyboard input in read-only mode
                        trace!(
                            "[conn={}] RDP: Keyboard input blocked (read-only mode)",
                            self.conn_id
                        );
                        return Ok(());
                    }

                    let key_event = match self.input_handler.handle_keyboard(keysym, pressed) {
                        Ok(ev) => ev,
                        Err(_) => {
                            // Unknown keysym - skip silently (already logged by handle_keyboard)
                            return Ok(());
                        }
                    };

                    // Convert to IronRDP FastPathInputEvent
                    let mut flags = if pressed {
                        KeyboardFlags::empty()
                    } else {
                        KeyboardFlags::RELEASE
                    };
                    if key_event.extended {
                        flags |= KeyboardFlags::EXTENDED;
                    }

                    let event = FastPathInputEvent::KeyboardEvent(flags, key_event.scancode);
                    let outputs = active_stage
                        .process_fastpath_input(image, &[event])
                        .map_err(|e| format!("Failed to process keyboard input: {}", e))?;

                    // Send response frames to RDP server
                    for output in outputs {
                        if let ActiveStageOutput::ResponseFrame(frame) = output {
                            framed
                                .write_all(&frame)
                                .await
                                .map_err(|e| format!("Failed to write keyboard response: {}", e))?;
                        }
                    }

                    debug!(
                        "[conn={}] RDP: Keyboard event sent - scancode: 0x{:02x}, pressed: {}",
                        self.conn_id, key_event.scancode, pressed
                    );
                }
            }
            "mouse" => {
                if instr.args.len() >= 3 {
                    // Parse coordinates as integers (per Guacamole protocol spec)
                    // Protocol order: x, y, mask (NOT mask, x, y!)
                    let x: i32 = instr.args[0]
                        .parse()
                        .map_err(|e| format!("Invalid x '{}': {}", instr.args[0], e))?;
                    let y: i32 = instr.args[1]
                        .parse()
                        .map_err(|e| format!("Invalid y '{}': {}", instr.args[1], e))?;
                    let mask: u8 = instr.args[2]
                        .parse()
                        .map_err(|e| format!("Invalid mouse mask '{}': {}", instr.args[2], e))?;

                    debug!(
                        "[conn={}] RDP: mouse x={} y={} mask=0x{:02x}",
                        self.conn_id, x, y, mask
                    );

                    // Security: Check read-only mode for mouse clicks
                    if self.read_only && !is_mouse_event_allowed_readonly(mask as u32) {
                        trace!(
                            "[conn={}] RDP: Mouse click blocked (read-only mode)",
                            self.conn_id
                        );
                        return Ok(());
                    }

                    // Feed mouse state to drag detector
                    let pointer_event = self.input_handler.handle_mouse(mask, x, y)?;

                    // Convert Guacamole mouse mask to RDP PointerFlags
                    // Guacamole mask: bit 0=left, bit 1=middle, bit 2=right, bit 3=scroll up, bit 4=scroll down
                    let mut flags = PointerFlags::empty();
                    let mut wheel_units: i16 = 0;

                    // Handle button state changes
                    // RDP protocol: DOWN flag means "button just pressed", no DOWN means "button released"
                    if pointer_event.left_down {
                        flags |= PointerFlags::LEFT_BUTTON | PointerFlags::DOWN;
                    } else if pointer_event.left_up {
                        flags |= PointerFlags::LEFT_BUTTON; // No DOWN flag = release
                    } else if pointer_event.left_button {
                        // Button held while moving
                        flags |=
                            PointerFlags::LEFT_BUTTON | PointerFlags::DOWN | PointerFlags::MOVE;
                    } else {
                        // Just moving, no button
                        flags |= PointerFlags::MOVE;
                    }

                    if pointer_event.middle_down {
                        flags |= PointerFlags::MIDDLE_BUTTON_OR_WHEEL | PointerFlags::DOWN;
                    } else if pointer_event.middle_up {
                        flags |= PointerFlags::MIDDLE_BUTTON_OR_WHEEL;
                    } else if pointer_event.middle_button {
                        flags |= PointerFlags::MIDDLE_BUTTON_OR_WHEEL
                            | PointerFlags::DOWN
                            | PointerFlags::MOVE;
                    }

                    if pointer_event.right_down {
                        flags |= PointerFlags::RIGHT_BUTTON | PointerFlags::DOWN;
                    } else if pointer_event.right_up {
                        flags |= PointerFlags::RIGHT_BUTTON;
                    } else if pointer_event.right_button {
                        flags |=
                            PointerFlags::RIGHT_BUTTON | PointerFlags::DOWN | PointerFlags::MOVE;
                    }

                    if pointer_event.scroll_up {
                        flags |= PointerFlags::VERTICAL_WHEEL;
                        wheel_units = 120; // Standard wheel delta
                    }
                    if pointer_event.scroll_down {
                        flags |= PointerFlags::VERTICAL_WHEEL | PointerFlags::WHEEL_NEGATIVE;
                        wheel_units = -120;
                    }

                    let mouse_pdu = MousePdu {
                        flags,
                        number_of_wheel_rotation_units: wheel_units,
                        x_position: pointer_event.x as u16,
                        y_position: pointer_event.y as u16,
                    };

                    let event = FastPathInputEvent::MouseEvent(mouse_pdu);
                    let outputs = active_stage
                        .process_fastpath_input(image, &[event])
                        .map_err(|e| format!("Failed to process mouse input: {}", e))?;

                    // Only send ResponseFrame back to the server.
                    // GraphicsUpdate from process_fastpath_input is IronRDP's internal
                    // pointer compositing into the framebuffer. Real screen updates from
                    // mouse actions (drag, click effects) arrive via read_pdu() in the
                    // main event loop. Sending these here causes full-screen redraws on
                    // every mouse move and cursor ghost artifacts.
                    for output in outputs {
                        if let ActiveStageOutput::ResponseFrame(frame) = output {
                            framed
                                .write_all(&frame)
                                .await
                                .map_err(|e| format!("Failed to write mouse response: {}", e))?;
                        }
                    }

                    debug!(
                        "[conn={}] RDP: Mouse event sent - x: {}, y: {}, flags: {:?}",
                        self.conn_id, pointer_event.x, pointer_event.y, flags
                    );
                }
            }
            "clipboard" => {
                match self.channel_handler.handle_client_clipboard(msg) {
                    Ok(Some(cliprdr_data)) => {
                        info!(
                            "[conn={}] RDP: Clipboard data ready for server: {} bytes (AC-1)",
                            self.conn_id,
                            cliprdr_data.data.len()
                        );
                        // T-028/T-029: Forward clipboard text to the CLIPRDR backend.
                        // The backend will advertise it to the server via ClipboardMessage::SendInitiateCopy.
                        if let Some(ref data_arc) = self.cliprdr_data {
                            // Convert from UTF-8 bytes to String (Guacamole sends UTF-8).
                            if let Ok(text) = String::from_utf8(cliprdr_data.data) {
                                data_arc.lock().client_text = Some(text);
                                // Trigger format list advertisement by notifying the backend.
                                // The backend holds an mpsc sender; send a trigger via the rx poll.
                                debug!(
                                    "[conn={}] RDP: Clipboard text stored for CLIPRDR forwarding",
                                    self.conn_id
                                );
                            }
                        }
                    }
                    Ok(None) => {}
                    Err(e) => warn!("[conn={}] RDP: Clipboard error: {}", self.conn_id, e),
                }
            }
            "size" => {
                // Client size instruction format: size,<layer>,<width>,<height>;
                // We ignore the layer (args[0]) and use width/height (args[1], args[2])
                if instr.args.len() >= 3 {
                    let width: u32 = instr.args[1].parse().map_err(|_| "Invalid width")?;
                    let height: u32 = instr.args[2].parse().map_err(|_| "Invalid height")?;

                    // Standard guacd: DPI is set via connection parameters only, not dynamically updated
                    // Use the DPI value established during session initialization
                    info!(
                        "[conn={}] RDP: Client resize request: {}x{} @ {} DPI (layer: {}, current: {}x{} @ {} DPI)",
                        self.conn_id, width, height, self.dpi, instr.args[0], self.width, self.height, self.dpi
                    );

                    let old_width = self.width;
                    let old_height = self.height;

                    // Compute adjusted dimensions before the resize so we can
                    // compare against what xrdp will actually use.
                    let (adj_w, adj_h) = MonitorLayoutEntry::adjust_display_size(width, height);
                    // Try server-side resize via DisplayControl DVC
                    match self.send_display_resize(active_stage, width, height).await {
                        Ok(_) => {
                            info!(
                                "[conn={}] RDP: DisplayControl resize sent successfully",
                                self.conn_id
                            );
                            // Compare adjusted sizes: self.width/height already stores the
                            // adjusted value from either the initial connect or a prior resize.
                            let size_changed = adj_w != old_width || adj_h != old_height;
                            self.width = adj_w;
                            self.height = adj_h;
                            // Only rebuild framebuffer and notify the client when dimensions
                            // actually changed. Using adjusted sizes means a repeated request
                            // for 1724×1256 (adj→1728×1280) won't resend 'size' and trigger
                            // Layer.resize, which would clear the canvas unnecessarily.
                            if size_changed {
                                self.framebuffer = FrameBuffer::new(adj_w, adj_h);
                                // Send adjusted size so canvas matches xrdp's actual
                                // resolution — prevents Guacamole auto-expand clears.
                                let size_instr = self.protocol_encoder.format_size_instruction(
                                    0,
                                    self.width,  // already adj_w
                                    self.height, // already adj_h
                                );
                                let size_str = String::from_utf8_lossy(&size_instr).to_string();
                                if let Err(e) = self.send_and_record(&size_str).await {
                                    warn!(
                                        "[conn={}] RDP: Failed to send size confirmation: {}",
                                        self.conn_id, e
                                    );
                                }
                                // After clearing the canvas via Layer.resize, force xrdp
                                // to repaint the full viewport (wallpaper, static regions).
                                if let Some(bytes) = self.encode_refresh_rect(active_stage) {
                                    use ironrdp_tokio::FramedWrite;
                                    if let Err(e) = framed.write_all(&bytes).await {
                                        warn!(
                                            "[conn={}] RDP: Failed to send RefreshRect: {}",
                                            self.conn_id, e
                                        );
                                    } else {
                                        debug!(
                                            "RDP: Sent RefreshRect for {}x{}",
                                            self.width, self.height
                                        );
                                    }
                                }
                            }
                        }
                        Err(e) => {
                            debug!(
                                "RDP: DisplayControl resize failed: {} - keeping {}x{} (no canvas clear)",
                                e, old_width, old_height
                            );
                            // Do NOT send size(oldW, oldH) back — the client canvas is
                            // already at the correct dimensions. Sending it would trigger
                            // a Guacamole layer.resize() which clears the canvas, causing
                            // the black-flash on every resize attempt with xrdp (which
                            // doesn't support DisplayControl DVC).
                        }
                    }
                }
            }
            "nop" => {
                self.send_and_record("3.nop;").await?;
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
                    debug!("RDP: Unhandled instruction: {}", instr.opcode);
                }
            }
        }

        Ok(())
    }

    /// Software H.264 encode tick — runs every 33 ms for non-EGFX servers (xrdp, VNC, etc.)
    async fn maybe_encode_h264_rdp(&mut self) -> Result<(), String> {
        // Wait until we have a framebuffer with content before initialising the encoder.
        if !self.first_frame_sent {
            return Ok(());
        }

        // For Windows RDP, give EGFX 2 s to activate before starting software encoding.
        // For xrdp, EGFX never activates so skip the wait entirely.
        if !self.is_xrdp {
            if let Some(grace_start) = self.egfx_grace_start {
                if grace_start.elapsed() < Duration::from_secs(2) {
                    return Ok(());
                }
                self.egfx_grace_start = None;
            }
        }

        let video_tx = match self.video_tx.clone() {
            Some(tx) => tx,
            None => return Ok(()),
        };

        // Initialise the software H.264 encoder pipeline once.
        if self.h264_pipeline.is_none() {
            match guacr_encoder::make_encoder(self.width, self.height) {
                Ok(encoder) => {
                    let pipeline = guacr_encoder::pipeline::EncoderPipeline::new(encoder);
                    // Resolution was chosen (see `encode_resolution_cap`) assuming hardware
                    // encode based on a compile-time probe, since no encoder exists yet at
                    // that point. If the probe was right but the device didn't actually
                    // open, this session is now running software encode at a resolution it
                    // can't hold in real time — surface that loudly instead of silently
                    // freezing (see `hardware_encode_available` doc comment).
                    if hardware_encode_available()
                        && pipeline.backend_kind() == guacr_encoder::EncoderBackendKind::Software
                    {
                        warn!(
                            "[conn={}] RDP: hardware encode was expected but software is running at {}x{} — likely too slow for real-time; hardware device may have failed to open",
                            self.conn_id, self.width, self.height
                        );
                    }
                    self.h264_pipeline = Some(pipeline);
                    info!(
                        "[conn={}] RDP: H.264 encoder ready ({}x{})",
                        self.conn_id, self.width, self.height
                    );
                }
                Err(e) => {
                    warn!(
                        "[conn={}] RDP: H.264 encoder unavailable ({}), video_tx disabled — session will appear blank",
                        self.conn_id, e
                    );
                    self.video_tx = None;
                    return Ok(());
                }
            }
        }

        // Submit and drain in a scope so the &EncoderPipeline (which is not Sync due to
        // its inner std::sync::mpsc::Receiver) is dropped before any .await below.
        let encoded_frames: Vec<_> = {
            let Some(pipeline) = self.h264_pipeline.as_ref() else {
                return Ok(());
            };

            let force_keyframe = video_tx.keyframe_requested().swap(false, Ordering::AcqRel);
            let need_keepalive = h264_keepalive_needed(self.h264_last_submit);

            // Feed the BweController's bandwidth estimate to the encoder. The controller
            // (guacr_handlers::BweController, driven from RTCP REMB/TWCC in video_sender)
            // has always written this atomic for RDP sessions; RDP simply never read it,
            // so every session encoded at a fixed 3 Mbps regardless of measured capacity.
            // Mirrors guacr-vnc/src/handler.rs. The resolution tier (resolution_scale_pct)
            // is consumed below at frame-submit time.
            // Only reacts on change, so this is not a hot-path log and needs no verbose gate.
            let bps = video_tx.target_bitrate_bps().load(Ordering::Relaxed);
            if bps > 0 && bps != self.h264_last_bitrate_bps {
                pipeline.set_target_bitrate(bps);
                self.h264_last_bitrate_bps = bps;
                debug!(
                    "[conn={}] RDP: encoder target bitrate -> {:.2} Mbps",
                    self.conn_id,
                    bps as f64 / 1_000_000.0
                );
            }

            if self.framebuffer_dirty_for_h264 || need_keepalive || force_keyframe {
                self.framebuffer_dirty_for_h264 = false;
                self.h264_last_submit = Some(std::time::Instant::now());
                // BWE resolution tier: under sustained congestion the controller lowers
                // resolution_scale_pct (100 -> 75 -> 50 -> 33 of natural size) and this
                // frame is encoded smaller. The pipeline worker rebuilds the encoder off
                // this select loop when the submitted geometry changes.
                let scale_pct = video_tx.resolution_scale_pct().load(Ordering::Relaxed);
                let (enc_w, enc_h) =
                    guacr_handlers::video::scaled_encode_size(self.width, self.height, scale_pct);

                // Snapshot the framebuffer into a pooled buffer. The copy itself is
                // required (the framebuffer keeps mutating while the worker encodes),
                // but the allocation is not: this was a fresh ~8.3 MB Vec per tick on
                // the session's select loop. After warm-up the pool recycles the same
                // buffers and this path allocates nothing.
                let mut data = pipeline.acquire_frame_buffer();
                if (enc_w, enc_h) == (self.width, self.height) {
                    data.extend_from_slice(self.framebuffer.data());
                } else {
                    guacr_encoder::scale_rgba(
                        self.framebuffer.data(),
                        self.width,
                        self.height,
                        &mut data,
                        enc_w,
                        enc_h,
                    );
                }
                let frame = guacr_encoder::RgbaFrame {
                    data,
                    width: enc_w,
                    height: enc_h,
                    timestamp_us: guacr_terminal::current_time_millis() * 1000,
                };
                pipeline.submit(frame, force_keyframe);
            }

            pipeline.drain()
        }; // pipeline reference dropped here

        for encoded_frame in encoded_frames {
            video_tx
                .send_frame(encoded_frame)
                .await
                .map_err(|e| format!("RDP: H.264 video send failed: {}", e))?;
        }

        Ok(())
    }

    /// Send instruction to client and record it (if recording is enabled)
    /// Encode a decoded ClearCodec bitmap as JPEG and send as a Guacamole image instruction.
    ///
    /// AC-1 (T-074): renders crisp bitmaps as Guacamole img instructions.
    /// AC-3 (T-076): this path is taken instead of on_unhandled_pdu.
    async fn send_clearcodec_frame(
        &mut self,
        frame: &crate::egfx_handler::ClearCodecFrame,
    ) -> Result<(), String> {
        use base64::Engine;
        use guacr_protocol::{format_chunked_blobs, format_img};
        use image::codecs::jpeg::JpegEncoder;
        use image::{ColorType, ImageEncoder};

        let rgba = &frame.rgba;
        let width = frame.width;
        let height = frame.height;

        if rgba.is_empty() || width == 0 || height == 0 {
            return Ok(());
        }

        // Encode RGBA → JPEG at high quality (ClearCodec carries text; use high quality).
        let mut jpeg_buf = Vec::new();
        let enc = JpegEncoder::new_with_quality(&mut jpeg_buf, 95);
        enc.write_image(rgba, width, height, ColorType::Rgba8.into())
            .map_err(|e| format!("ClearCodec JPEG encode: {e}"))?;

        // Base64-encode for Guacamole blob transport.
        let b64 = base64::engine::general_purpose::STANDARD.encode(&jpeg_buf);

        // Send as Guacamole img + blob + end + sync on layer 0 (main display).
        let stream_id = self.stream_id;
        self.stream_id += 1;
        let img_instr = format_img(
            stream_id,
            14u32, // GUAC_COMP_OVER (0x0E)
            0i32,  // layer 0 = main display
            "image/jpeg",
            frame.x as i32,
            frame.y as i32,
        );
        self.send_and_record(&img_instr).await?;

        let blob_instrs = format_chunked_blobs(stream_id, &b64, None);
        for blob_instr in &blob_instrs {
            self.send_and_record(blob_instr).await?;
        }

        let ts = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis() as u64;
        let sync_instr = format_instruction("sync", &[&ts.to_string()]);
        self.send_and_record(&sync_instr).await?;

        Ok(())
    }

    /// Send a decoded PCM audio chunk to the Guacamole client as audio stream instructions.
    ///
    /// AC-1 (T-032): server audio output reaches the client.
    /// AC-2 (T-033): L16 PCM stream start signaled; AC-4 audio lifecycle.
    async fn send_audio_chunk(
        &mut self,
        chunk: &crate::audio_backend::AudioChunk,
    ) -> Result<(), String> {
        use base64::Engine;
        use guacr_protocol::{format_chunked_blobs, format_instruction};

        if chunk.data.is_empty() {
            return Ok(());
        }

        let stream_id = self.stream_id;
        self.stream_id += 1;

        // AC-2: L16 PCM = raw 16-bit little-endian PCM samples.
        // Guacamole audio format string: "audio/L16;rate=44100,channels=2"
        let mimetype = format!(
            "audio/L16;rate={},channels={}",
            chunk.sample_rate, chunk.channels
        );

        // AC-4: signal stream open (audio instruction = stream start).
        let audio_instr = format_instruction("audio", &[&stream_id.to_string(), &mimetype]);
        self.send_and_record(&audio_instr).await?;

        // Send PCM data as base64-encoded blobs.
        let b64 = base64::engine::general_purpose::STANDARD.encode(&chunk.data);
        let blob_instrs = format_chunked_blobs(stream_id, &b64, None);
        for instr in &blob_instrs {
            self.send_and_record(instr).await?;
        }

        // AC-4: signal stream close (end instruction).
        let end_instr = format_instruction("end", &[&stream_id.to_string()]);
        self.send_and_record(&end_instr).await?;

        Ok(())
    }

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

    /// Send a Refresh Rect PDU covering the full current display.
    /// Forces xrdp to resend dirty rects for the entire viewport — needed after
    /// the Guacamole canvas is cleared by Layer.resize so that xrdp repaints
    /// static regions (wallpaper, etc.) that it considers "unchanged".
    /// Returns the encoded Refresh Rect PDU bytes or None on error.
    /// Encoding is synchronous; the caller does the async write to avoid
    /// holding a &ActiveStage across an await (ActiveStage is not Sync).
    fn encode_refresh_rect(&self, active_stage: &ActiveStage) -> Option<Vec<u8>> {
        let pdu = RefreshRectanglePdu {
            areas_to_refresh: vec![InclusiveRectangle {
                left: 0,
                top: 0,
                right: (self.width.saturating_sub(1)) as u16,
                bottom: (self.height.saturating_sub(1)) as u16,
            }],
        };
        let mut buf = WriteBuf::new();
        match active_stage.encode_static(&mut buf, ShareDataPdu::RefreshRectangle(pdu)) {
            Ok(_) => Some(buf.filled().to_vec()),
            Err(e) => {
                warn!(
                    "[conn={}] RDP: Failed to encode RefreshRect: {}",
                    self.conn_id, e
                );
                None
            }
        }
    }

    async fn send_display_resize(
        &self,
        active_stage: &mut ActiveStage,
        width: u32,
        height: u32,
    ) -> Result<(), String> {
        // Get DisplayControl DVC
        let dvc = active_stage
            .get_dvc::<DisplayControlClient>()
            .ok_or_else(|| "DisplayControl DVC not available".to_string())?;

        let channel_id = dvc.channel_id();

        // Get DisplayControl client processor
        let display_control = dvc.processor();

        // Check if DisplayControl is ready (capabilities received)
        if !display_control.ready() {
            return Err("DisplayControl not ready (capabilities not received)".to_string());
        }

        // Adjust display size to meet RDP requirements
        // Width must be >= 200, <= 8192, and even
        // Height must be >= 200, <= 8192
        let (adjusted_width, adjusted_height) =
            MonitorLayoutEntry::adjust_display_size(width, height);

        if adjusted_width != width || adjusted_height != height {
            info!(
                "[conn={}] RDP: Adjusted display size from {}x{} to {}x{}",
                self.conn_id, width, height, adjusted_width, adjusted_height
            );
        }

        // Encode monitor layout message
        let messages = display_control
            .encode_single_primary_monitor(
                channel_id,
                adjusted_width,
                adjusted_height,
                None, // scale_factor
                None, // physical_dims
            )
            .map_err(|e| format!("Failed to encode monitor layout: {}", e))?;

        // Send via ActiveStage
        let _encoded = active_stage
            .encode_dvc_messages(messages)
            .map_err(|e| format!("Failed to encode DVC messages: {}", e))?;

        info!(
            "[conn={}] RDP: Sent DisplayControl resize to server: {}x{}",
            self.conn_id, adjusted_width, adjusted_height
        );

        Ok(())
    }
}

// ============================================================================
// TLS Helper Functions
// ============================================================================

/// Dangerous certificate verifier that accepts all certificates
/// (Required for RDP servers with self-signed certificates)
#[derive(Debug)]
struct DangerousNoCertificateVerification;

impl tokio_rustls::rustls::client::danger::ServerCertVerifier
    for DangerousNoCertificateVerification
{
    fn verify_server_cert(
        &self,
        _end_entity: &tokio_rustls::rustls::pki_types::CertificateDer<'_>,
        _intermediates: &[tokio_rustls::rustls::pki_types::CertificateDer<'_>],
        _server_name: &tokio_rustls::rustls::pki_types::ServerName<'_>,
        _ocsp_response: &[u8],
        _now: tokio_rustls::rustls::pki_types::UnixTime,
    ) -> Result<tokio_rustls::rustls::client::danger::ServerCertVerified, tokio_rustls::rustls::Error>
    {
        Ok(tokio_rustls::rustls::client::danger::ServerCertVerified::assertion())
    }

    fn verify_tls12_signature(
        &self,
        _message: &[u8],
        _cert: &tokio_rustls::rustls::pki_types::CertificateDer<'_>,
        _dss: &tokio_rustls::rustls::DigitallySignedStruct,
    ) -> Result<
        tokio_rustls::rustls::client::danger::HandshakeSignatureValid,
        tokio_rustls::rustls::Error,
    > {
        Ok(tokio_rustls::rustls::client::danger::HandshakeSignatureValid::assertion())
    }

    fn verify_tls13_signature(
        &self,
        _message: &[u8],
        _cert: &tokio_rustls::rustls::pki_types::CertificateDer<'_>,
        _dss: &tokio_rustls::rustls::DigitallySignedStruct,
    ) -> Result<
        tokio_rustls::rustls::client::danger::HandshakeSignatureValid,
        tokio_rustls::rustls::Error,
    > {
        Ok(tokio_rustls::rustls::client::danger::HandshakeSignatureValid::assertion())
    }

    fn supported_verify_schemes(&self) -> Vec<tokio_rustls::rustls::SignatureScheme> {
        vec![
            tokio_rustls::rustls::SignatureScheme::RSA_PKCS1_SHA1,
            tokio_rustls::rustls::SignatureScheme::ECDSA_SHA1_Legacy,
            tokio_rustls::rustls::SignatureScheme::RSA_PKCS1_SHA256,
            tokio_rustls::rustls::SignatureScheme::ECDSA_NISTP256_SHA256,
            tokio_rustls::rustls::SignatureScheme::RSA_PKCS1_SHA384,
            tokio_rustls::rustls::SignatureScheme::ECDSA_NISTP384_SHA384,
            tokio_rustls::rustls::SignatureScheme::RSA_PKCS1_SHA512,
            tokio_rustls::rustls::SignatureScheme::ECDSA_NISTP521_SHA512,
            tokio_rustls::rustls::SignatureScheme::RSA_PSS_SHA256,
            tokio_rustls::rustls::SignatureScheme::RSA_PSS_SHA384,
            tokio_rustls::rustls::SignatureScheme::RSA_PSS_SHA512,
            tokio_rustls::rustls::SignatureScheme::ED25519,
            tokio_rustls::rustls::SignatureScheme::ED448,
        ]
    }
}

/// Compare a server certificate's SHA256 fingerprint against an expected value.
/// Encode an RGBA pixel buffer as JPEG.
///
/// Accepts ownership of the pixel buffer — callers produced the buffer
/// exclusively for this encode call, so no clone is needed.
/// Exposed as `pub(crate)` so unit tests can exercise the encode path directly.
#[allow(dead_code)]
pub(crate) fn encode_jpeg(
    data: Vec<u8>,
    width: u32,
    height: u32,
    quality: u8,
) -> Result<Vec<u8>, String> {
    let img = RgbaImage::from_raw(width, height, data)
        .ok_or_else(|| "Invalid image dimensions".to_string())?;
    use image::ImageEncoder;
    let rgb_img = image::DynamicImage::ImageRgba8(img).to_rgb8();
    let mut jpeg_data = Vec::new();
    let encoder = image::codecs::jpeg::JpegEncoder::new_with_quality(&mut jpeg_data, quality);
    encoder
        .write_image(&rgb_img, width, height, image::ExtendedColorType::Rgb8)
        .map_err(|e| format!("JPEG encode failed: {}", e))?;
    Ok(jpeg_data)
}

/// The expected fingerprint can be a lowercase hex string (64 chars) or
/// a colon-separated hex string (e.g. "aa:bb:cc:…").
/// Returns true if the actual SHA256 of `cert_der` matches `expected`.
pub(crate) fn cert_fingerprint_matches(cert_der: &[u8], expected: &str) -> bool {
    use sha2::{Digest, Sha256};
    let actual = Sha256::digest(cert_der);
    let actual_hex = format!("{:x}", actual);
    // Normalize expected: strip colons and lowercase
    let expected_clean: String = expected
        .to_ascii_lowercase()
        .chars()
        .filter(|c| c.is_ascii_hexdigit())
        .collect();
    actual_hex == expected_clean
}

/// Extract the server's public key from a TLS certificate
fn extract_tls_server_public_key(cert_der: &[u8]) -> Result<Vec<u8>, String> {
    use x509_cert::der::Decode;

    let cert = x509_cert::Certificate::from_der(cert_der)
        .map_err(|e| format!("Failed to parse certificate: {}", e))?;

    debug!(
        "RDP: Server certificate subject: {}",
        cert.tbs_certificate.subject
    );

    let server_public_key = cert
        .tbs_certificate
        .subject_public_key_info
        .subject_public_key
        .as_bytes()
        .ok_or_else(|| "Subject public key BIT STRING is not aligned".to_string())?
        .to_owned();

    Ok(server_public_key)
}

/// Dummy network client for CredSSP
///
/// We don't actually use network client functionality (it's for fetching auth tokens
/// from external services like KDC proxy), but the API requires one.
///
/// See: https://github.com/Devolutions/IronRDP/pull/1043
struct DummyNetworkClient;

impl ironrdp_async::NetworkClient for DummyNetworkClient {
    async fn send(
        &mut self,
        _request: &ironrdp::connector::sspi::generator::NetworkRequest,
    ) -> ironrdp::connector::ConnectorResult<Vec<u8>> {
        Err(ironrdp::connector::general_err!(
            "Network client not implemented"
        ))
    }
}
