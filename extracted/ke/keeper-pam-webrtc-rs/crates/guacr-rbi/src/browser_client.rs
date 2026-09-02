// Browser client integration for RBI (Remote Browser Isolation)
// Provides headless browser session management with proper input handling

use crate::adaptive_fps::AdaptiveFps;
use crate::clipboard::RbiClipboard;
use crate::dirty_tracker::RbiDirtyTracker;
use crate::file_upload::{format_upload_dialog_instruction, UploadEngine};
use crate::js_dialog::{JsDialogConfig, JsDialogManager};
use crate::screencast::ScreencastConfig;
use crate::scroll_detector::ScrollDetector;
// Events module provides types used for more complex RBI scenarios
use crate::handler::{RbiBackend, RbiConfig};
use crate::input::{chrome_flags_to_cdp_modifiers, KeyboardShortcut, RbiInputHandler};
use bytes::Bytes;
use guacr_protocol::GuacamoleParser;
use log::{debug, error, info, warn};
use tokio::sync::mpsc;
// Sync flow control (shared with RDP/VNC) and session lifecycle
use guacr_handlers::{
    record_client_input as shared_record_client_input, send_cursor_instructions, send_disconnect,
    send_name, send_ready, AdaptiveQuality, CursorManager, MultiFormatRecorder, RecordingConfig,
    RecordingDirection, StandardCursor, SyncFlowControl,
};
use std::collections::HashMap;

#[cfg(feature = "threat-detection")]
use guacr_threat_detection::ThreatDetector;
#[cfg(feature = "threat-detection")]
use std::sync::Arc;
// `image` is used unconditionally in other parts of this crate (screencast encoding).
// Within the threat-detection feature block we also need it for JPEG decode → RGBA.
// The crate is a direct dep in Cargo.toml so this import is always available.

/// CDP's `Page.startScreencast` has no live quality knob — changing quality means
/// reissuing the command, which briefly disrupts the frame stream. Restarting on every
/// small throughput wobble isn't worth that, so a change only takes effect once it clears
/// this threshold.
const QUALITY_RESTART_THRESHOLD: u8 = 10;

/// Whether a quality recommendation from `AdaptiveQuality` is worth restarting the
/// screencast for. Factored out from the event loop so it's testable without a Chrome
/// session — see `QUALITY_RESTART_THRESHOLD`.
pub(crate) fn should_restart_screencast(current: u8, recommended: u8) -> bool {
    recommended.abs_diff(current) >= QUALITY_RESTART_THRESHOLD
}

/// Browser client for RBI sessions
pub struct BrowserClient {
    stream_id: u32,
    pub(crate) width: u32,
    pub(crate) height: u32,
    config: RbiConfig,
    input_handler: RbiInputHandler,
    clipboard: RbiClipboard,
    upload_engine: UploadEngine,
    dialog_manager: JsDialogManager,
    sync_control: SyncFlowControl,
    cursor_manager: CursorManager,
    recorder: Option<MultiFormatRecorder>,
    /// Profile lock held for the duration of the session (persistent profiles only).
    /// Releasing this field drops the lock, allowing the next session to use the profile.
    profile_lock: Option<crate::profile_isolation::ProfileLock>,
    /// Parsed profile storage configuration (from connection params).
    profile_config: crate::profile_storage::ProfileStorageConfig,
    /// AI threat detector for graphical sessions (RBI screenshots are already JPEG).
    #[cfg(feature = "threat-detection")]
    threat_detector: Option<Arc<ThreatDetector>>,
    /// Per-session ID for threat detection state tracking.
    #[cfg(feature = "threat-detection")]
    threat_session_id: String,
    /// Drives screencast JPEG quality from measured throughput instead of the fixed
    /// quality=30 this used to hardcode (chosen only to keep frames under 2 SCTP
    /// fragments) — same shared infra VNC already uses for its JPEG path.
    adaptive_quality: AdaptiveQuality,
    /// Keystrokes buffered since the last screenshot analysis trigger.
    #[cfg(feature = "threat-detection")]
    threat_keystroke_buffer: String,
}

impl BrowserClient {
    /// Create a new browser client
    pub fn new(
        width: u32,
        height: u32,
        config: RbiConfig,
        recording_config: &RecordingConfig,
        params: &HashMap<String, String>,
    ) -> Result<Self, String> {
        let mut clipboard = RbiClipboard::new(config.clipboard_buffer_size);
        clipboard.set_restrictions(config.disable_copy, config.disable_paste);

        // Use upload config from RbiConfig
        let upload_config = config.upload_config.clone();

        // Setup dialog config
        let dialog_config = JsDialogConfig {
            show_dialogs: true,
            auto_dismiss_alert_ms: Some(10000), // Auto-dismiss alerts after 10s
            allow_beforeunload: false,          // Block beforeunload by default
            ..Default::default()
        };

        // Initialize recording if enabled
        let recorder = if recording_config.is_enabled() {
            match MultiFormatRecorder::new(
                recording_config,
                params,
                "rbi",
                width as u16,
                height as u16,
            ) {
                Ok(rec) => {
                    info!("RBI: Session recording initialized");
                    Some(rec)
                }
                Err(e) => {
                    warn!("RBI: Failed to initialize recording: {}", e);
                    None
                }
            }
        } else {
            None
        };

        // Parse profile storage configuration from connection params.
        // On parse error (e.g. path traversal attempt), log a warning and fall
        // back to the default (no persistent profile, temp dir).
        let profile_config = crate::profile_storage::ProfileStorageConfig::from_params(params)
            .unwrap_or_else(|e| {
                warn!(
                    "RBI: Invalid profile-path parameter ({}), using temp dir",
                    e
                );
                crate::profile_storage::ProfileStorageConfig::default()
            });

        #[cfg(feature = "threat-detection")]
        let threat_detector = ThreatDetector::from_params(params, "RBI");
        #[cfg(feature = "threat-detection")]
        let threat_session_id = uuid::Uuid::new_v4().to_string();

        Ok(Self {
            stream_id: 1,
            width,
            height,
            input_handler: RbiInputHandler::new(),
            clipboard,
            upload_engine: UploadEngine::new(upload_config),
            dialog_manager: JsDialogManager::new(dialog_config),
            sync_control: SyncFlowControl::new(),
            cursor_manager: CursorManager::new(false, false, 85),
            config,
            recorder,
            profile_lock: None,
            profile_config,
            #[cfg(feature = "threat-detection")]
            threat_detector,
            #[cfg(feature = "threat-detection")]
            threat_session_id,
            #[cfg(feature = "threat-detection")]
            threat_keystroke_buffer: String::new(),
            adaptive_quality: AdaptiveQuality::new(80).with_min_quality(20),
        })
    }

    /// Launch browser and navigate to URL
    ///
    /// # Arguments
    ///
    /// * `url` - URL to navigate to
    /// * `to_client` - Channel to send Guacamole instructions
    /// * `from_client` - Channel to receive Guacamole instructions
    pub async fn connect(
        &mut self,
        url: &str,
        to_client: mpsc::Sender<Bytes>,
        from_client: mpsc::Receiver<Bytes>,
    ) -> Result<(), String> {
        info!(
            "RBI: Launching browser for URL: {}",
            rbi_safe_url_for_log(url)
        );

        match self.config.backend {
            RbiBackend::Chrome => {
                self.launch_chrome(url, to_client, from_client).await?;
            }
            RbiBackend::Servo => {
                return Err("Servo backend not yet implemented".to_string());
            }
            RbiBackend::ServoWithFallback => {
                // Servo is not implemented; always fall through to Chrome
                self.launch_chrome(url, to_client, from_client).await?;
            }
        }

        Ok(())
    }

    /// Launch Chrome browser using chromiumoxide
    async fn launch_chrome(
        &mut self,
        url: &str,
        to_client: mpsc::Sender<Bytes>,
        mut from_client: mpsc::Receiver<Bytes>,
    ) -> Result<(), String> {
        use crate::chrome_session::ChromeSession;
        use tokio::time::{interval, Duration};

        info!(
            "RBI: Launching Chrome browser for URL: {}",
            rbi_safe_url_for_log(url)
        );

        // Launch Chrome with chromiumoxide
        let mut chrome_session = ChromeSession::new(
            self.width,
            self.height,
            self.config.capture_fps,
            &self.config.chromium_path,
        );

        // Resolve the profile directory and acquire the exclusive lock.
        //
        // For sessions without a configured profile-path, validate_and_prepare
        // returns a UUID-named temp path that Chrome will create on first launch.
        // No lock is needed in that case — acquire_lock returns None.
        //
        // For persistent profiles the lock is held in self.profile_lock for the
        // entire session duration; dropping it releases the lock so the next
        // session can use the same profile.
        let profile_dir_str = self
            .profile_config
            .validate_and_prepare()
            .map_err(|e| format!("Profile directory error: {}", e))?
            .to_string_lossy()
            .into_owned();

        let lock = crate::profile_storage::acquire_lock(
            &self.profile_config,
            std::path::Path::new(&profile_dir_str),
        )?;
        self.profile_lock = lock;

        // 30-second timeout prevents the session from hanging indefinitely if the
        // chromium subprocess fails to start or never opens its DevTools port.
        //
        // Use launch_with_prepared_profile so the session uses our validated
        // profile directory.  The lock is already held in self.profile_lock;
        // chrome_session must NOT re-lock (skip_lock=true path).
        tokio::time::timeout(
            Duration::from_secs(30),
            chrome_session.launch_with_prepared_profile(
                url,
                &self.config.chromium_path,
                &self.config.popup_handling,
                &profile_dir_str,
                self.config.timezone.as_deref(),
                self.config.accept_language.as_deref(),
            ),
        )
        .await
        .map_err(|_| "Chrome launch timed out after 30s".to_string())?
        .map_err(|e| format!("Chrome launch failed: {}", e))?;

        // Block popups if configured
        match &self.config.popup_handling {
            crate::handler::PopupHandling::Block => {
                chrome_session.block_popups(&[]).await?;
            }
            crate::handler::PopupHandling::AllowList(allowed) => {
                chrome_session.block_popups(allowed).await?;
            }
            crate::handler::PopupHandling::NavigateMainWindow => {
                // Allow popups but will navigate main window instead
            }
        }

        // Send ready and name instructions (client needs ready to start sending instructions)
        // The client will send a size instruction after receiving ready, which we'll handle
        // in the main event loop to dynamically resize Chrome
        send_ready(&to_client, "rbi-ready")
            .await
            .map_err(|e| e.to_string())?;
        send_name(&to_client, "RBI")
            .await
            .map_err(|e| e.to_string())?;

        // Send initial pointer cursor using embedded bitmap (drawn on buffer layer -1)
        let cursor_instrs = self
            .cursor_manager
            .send_standard_cursor(StandardCursor::Pointer)
            .map_err(|e| format!("Failed to generate cursor: {}", e))?;
        info!("RBI: Sending initial cursor instruction (pointer)");
        send_cursor_instructions(cursor_instrs, &to_client)
            .await
            .map_err(|e| format!("Failed to send cursor: {}", e))?;

        // Send size instruction using TEXT protocol (must match ready instruction format)
        // Format: size,<layer>,<width>,<height>;
        // CRITICAL: This must match the screenshot dimensions or the client will scale/position incorrectly
        use guacr_protocol::format_instruction;
        let size_instr = format_instruction(
            "size",
            &["0", &self.width.to_string(), &self.height.to_string()],
        );
        info!(
            "RBI: Sending size instruction: {}x{} (must match screenshot size)",
            self.width, self.height
        );
        info!("RBI: Size instruction bytes: {}", size_instr);
        to_client
            .send(Bytes::from(size_instr))
            .await
            .map_err(|e| format!("Failed to send size: {}", e))?;

        info!("RBI: Chrome browser launched, starting capture loop");

        // Setup download interception if enabled
        #[cfg(feature = "chrome")]
        if self.config.download_config.enabled {
            info!(
                "RBI: Downloads enabled with config: max_size={}MB, allowed={:?}, blocked={:?}",
                self.config.download_config.max_file_size_mb,
                self.config.download_config.allowed_extensions,
                self.config.download_config.blocked_extensions
            );
        } else {
            info!("RBI: Downloads disabled (default for security)");
        }

        // Install clipboard event listener (no Chrome patches needed)
        if !self.config.disable_copy {
            if let Err(e) = chrome_session.install_clipboard_listener().await {
                warn!("RBI: Failed to install clipboard listener: {}", e);
            }
        }

        // Install cursor tracker
        if let Err(e) = chrome_session.install_cursor_tracker().await {
            warn!("RBI: Failed to install cursor tracker: {}", e);
        }

        // Install scroll tracker
        if let Err(e) = chrome_session.install_scroll_tracker().await {
            warn!("RBI: Failed to install scroll tracker: {}", e);
        }

        // Enable file chooser interception if uploads are enabled
        if self.upload_engine.manager().is_enabled() {
            if let Err(e) = chrome_session.enable_file_chooser_interception().await {
                warn!("RBI: Failed to enable file chooser interception: {}", e);
            } else {
                info!("RBI: File upload support enabled");
            }
        }

        // Performance optimizations
        let mut dirty_tracker = RbiDirtyTracker::new();
        let mut adaptive_fps = AdaptiveFps::new(5, self.config.capture_fps);
        let mut scroll_detector = ScrollDetector::new();

        // Post-input screenshot fallback: deadline-based so it survives rapid input
        // bursts. A bare `tokio::time::sleep(150ms)` in a biased select gets recreated
        // every loop iteration when from_client fires continuously, so it never fires.
        // Storing the absolute deadline fixes that.
        let mut post_input_deadline: Option<tokio::time::Instant> = None;

        // Screencast mode (use if enabled in config, otherwise fall back to screenshots)
        let mut use_screencast = self.config.use_screencast.unwrap_or(true);
        // The quality currently configured on Chrome's screencast (0 = not started yet).
        // Compared against `adaptive_quality.calculate_quality()` on each frame to decide
        // whether it's worth restarting the screencast with a new value.
        #[cfg(feature = "chrome")]
        let mut current_screencast_quality: u8 = 0;
        // screencast_stream is Some when screencast mode is active (chrome feature only)
        #[cfg(feature = "chrome")]
        let mut screencast_stream: Option<
            chromiumoxide::listeners::EventStream<
                chromiumoxide::cdp::browser_protocol::page::EventScreencastFrame,
            >,
        > = None;

        #[cfg(feature = "chrome")]
        if use_screencast {
            info!("RBI: Screencast mode enabled - JPEG video streaming");

            // Start screencast using actual session dimensions to avoid downscaling.
            // Quality is driven by AdaptiveQuality (throughput-fed, same shared infra VNC's
            // JPEG path already uses) instead of a fixed value — it starts at max_quality
            // (matching VNC's own start-high-then-back-off pattern) and adapts from there.
            // The old fixed quality=30 existed to keep frames under 2 SCTP fragments,
            // avoiding ICE keepalive starvation on a reassembler that couldn't handle more;
            // that reassembler is fixed now (2026-08-04), so this constraint no longer holds.
            let screencast_config = ScreencastConfig {
                max_width: self.width,
                max_height: self.height,
                quality: self.adaptive_quality.calculate_quality(),
                ..ScreencastConfig::default()
            };
            if let Err(e) = chrome_session
                .start_screencast(
                    screencast_config.format.as_str(),
                    screencast_config.quality,
                    screencast_config.max_width,
                    screencast_config.max_height,
                )
                .await
            {
                warn!(
                    "RBI: Failed to start screencast, falling back to screenshots: {}",
                    e
                );
                use_screencast = false;
            } else {
                current_screencast_quality = screencast_config.quality;
                // Subscribe to screencast frame events
                match chrome_session.screencast_event_listener().await {
                    Ok(stream) => {
                        info!("RBI: Screencast event listener subscribed successfully");
                        screencast_stream = Some(stream);
                    }
                    Err(e) => {
                        warn!(
                            "RBI: Failed to subscribe to screencast events, falling back to screenshots: {}",
                            e
                        );
                        use_screencast = false;
                    }
                }
            }
        }

        // Take an initial screenshot immediately so the user sees the page right away.
        // Chrome's screencast often doesn't push a first frame until content changes,
        // leaving the user staring at a blank screen until they interact.
        #[cfg(feature = "chrome")]
        {
            match chrome_session.capture_screenshot().await {
                Ok(Some(screenshot)) => {
                    if let Err(e) = self.send_screenshot(&screenshot, &to_client).await {
                        warn!("RBI: Failed to send initial screenshot: {}", e);
                    } else {
                        debug!("RBI: Initial screenshot sent ({} bytes)", screenshot.len());
                        let _ = dirty_tracker.has_changed(&screenshot);
                    }
                }
                Ok(None) => debug!("RBI: Initial screenshot returned no data"),
                Err(e) => warn!("RBI: Initial screenshot failed: {}", e),
            }
        }

        #[cfg(feature = "chrome")]
        if !use_screencast {
            info!(
                "RBI: Screenshot mode - adaptive FPS (5-{}), dirty tracking",
                self.config.capture_fps
            );
        }
        #[cfg(not(feature = "chrome"))]
        {
            use_screencast = false;
            info!(
                "RBI: Screenshot mode - adaptive FPS (5-{}), dirty tracking",
                self.config.capture_fps
            );
        }

        info!(
            "RBI: Entering main event loop (use_screencast={})",
            use_screencast
        );
        // Main event loop
        let mut capture_interval =
            interval(Duration::from_millis(1000 / self.config.capture_fps as u64));

        // Clipboard polling interval (every 500ms)
        let mut clipboard_interval = interval(Duration::from_millis(500));

        // Resource monitoring interval (every 5 seconds)
        let mut resource_interval = interval(Duration::from_secs(5));
        let mut resource_check_count = 0u32;

        // Throttle MouseMoved CDP calls — track last time we sent one (capped at 30fps)
        let mut last_mouse_move: Option<std::time::Instant> = None;

        // Sliding window: allow up to 3 screencast frames in flight before blocking.
        // 1-frame-strict gate → ~2fps (400ms sync RTT). 3-frame window → ~6fps with
        // same backpressure protection against SCTP flooding ICE keepalives.
        let mut frames_in_flight: u32 = 0;

        loop {
            tokio::select! {
                biased; // Check arms in order: input first, then frames, then timers.
                        // Ensures clicks/keyboard/scroll are never starved by a
                        // high-frequency screencast stream.

                // Client input has highest priority — process immediately when ready.
                // Listed first so biased select always drains input before rendering.
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("RBI: Client disconnected (from_client channel closed)");
                        break;
                    };
                    self.record_client_input(&msg);
                    if let Ok(msg_str) = std::str::from_utf8(&msg) {
                        if msg_str.starts_with("4.sync,") {
                            if let Some(ts) = self.sync_control.pending_timestamp() {
                                self.sync_control.clear_pending();
                                frames_in_flight = frames_in_flight.saturating_sub(1);
                                debug!("RBI: Client acknowledged sync (ts={}, in_flight={})", ts, frames_in_flight);
                            }
                            continue;
                        }
                        if msg_str.starts_with("4.size,") {
                            let parts: Vec<&str> = msg_str.split(',').collect();
                            if parts.len() >= 3 {
                                if let Some(width_part) = parts.get(2) {
                                    if let Some(height_part) = parts.get(3) {
                                        if let Some(w_str) = width_part.split('.').nth(1) {
                                            if let Some(h_str) = height_part
                                                .split('.')
                                                .nth(1)
                                                .and_then(|s| s.strip_suffix(';'))
                                            {
                                                if let (Ok(w), Ok(h)) =
                                                    (w_str.parse::<u32>(), h_str.parse::<u32>())
                                                {
                                                    info!(
                                                        "RBI: Client requested size change: {}x{} (was {}x{})",
                                                        w, h, self.width, self.height
                                                    );
                                                    self.width = w;
                                                    self.height = h;
                                                    if let Err(e) = chrome_session.resize(w, h).await {
                                                        warn!("RBI: Failed to resize Chrome: {}", e);
                                                    } else {
                                                        use guacr_protocol::format_instruction;
                                                        let size_instr = format_instruction(
                                                            "size",
                                                            &["0", &w.to_string(), &h.to_string()],
                                                        );
                                                        let size_bytes = Bytes::from(size_instr);
                                                        self.record_server_instruction(&size_bytes);
                                                        if let Err(e) = to_client.send(size_bytes).await {
                                                            warn!("RBI: Failed to send size confirmation: {}", e);
                                                        }
                                                    }
                                                    continue;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    // Read button state BEFORE processing (to detect releases).
                    // Must use input_handler directly: vault sends binary protocol which
                    // GuacamoleParser::parse_instruction (text-only) cannot parse.
                    let left_was_pressed = (self.input_handler.mouse_buttons_mask() & 1) != 0;

                    if let Err(e) = self.handle_client_input(&mut chrome_session, &msg, &to_client, &mut last_mouse_move).await {
                        warn!("RBI: Error handling input: {}", e);
                    }

                    // Detect left-button release OR scroll — both need a post-capture.
                    let left_now_pressed = (self.input_handler.mouse_buttons_mask() & 1) != 0;
                    let had_scroll = msg.len() > 1 && {
                        // scroll bits: 0x08 (up) or 0x10 (down) in text mask arg,
                        // or binary Mouse opcode 0x02 with button_mask scroll bits
                        let is_scroll_text = GuacamoleParser::parse_instruction(&msg.clone())
                            .ok()
                            .and_then(|i| if i.opcode == "mouse" { i.args.get(2).and_then(|m| m.parse::<u32>().ok()) } else { None })
                            .map(|m| m & 0x18 != 0)
                            .unwrap_or(false);
                        let is_scroll_binary = !msg.is_empty() && msg[0] == 0x02 && msg.len() >= 14
                            && (msg[12] & 0x18 != 0); // button_mask byte in binary mouse
                        is_scroll_text || is_scroll_binary
                    };
                    if (left_was_pressed && !left_now_pressed) || had_scroll {
                        // Set deadline only on the first input event; don't push it out
                        // on subsequent rapid events (that's the bug we're fixing).
                        if post_input_deadline.is_none() {
                            post_input_deadline = Some(
                                tokio::time::Instant::now()
                                    + tokio::time::Duration::from_millis(200),
                            );
                        }
                    }
                }

                // Post-input screenshot fallback: fires 200ms after the first click/scroll
                // if Chrome's screencast hasn't pushed a new frame. Uses sleep_until with
                // a stored deadline so rapid input bursts don't keep resetting the timer.
                _ = async {
                    match post_input_deadline {
                        Some(d) => tokio::time::sleep_until(d).await,
                        None => std::future::pending().await,
                    }
                }, if post_input_deadline.is_some() => {
                    post_input_deadline = None;
                    match chrome_session.capture_screenshot().await {
                        Ok(Some(screenshot)) => {
                            // Threat detection stub: analyze the post-click screenshot.
                            // RBI screenshots are already JPEG — convert to grayscale before
                            // sending to the BAML vision endpoint (smaller payload, color not
                            // needed for content analysis).
                            #[cfg(feature = "threat-detection")]
                            if let Some(ref detector) = self.threat_detector {
                                // Decode JPEG → RGBA → grayscale JPEG for the detector.
                                if let Ok(img) = image::load_from_memory(&screenshot) {
                                    let rgba = img.to_rgba8();
                                    let (w, h) = (rgba.width(), rgba.height());
                                    if let Ok(gray_jpeg) =
                                        guacr_threat_detection::rgba_to_grayscale_jpeg(
                                            rgba.as_raw(),
                                            w,
                                            h,
                                            75,
                                        )
                                    {
                                        let keystrokes =
                                            std::mem::take(&mut self.threat_keystroke_buffer);
                                        let sid = self.threat_session_id.clone();
                                        let det = Arc::clone(detector);
                                        tokio::spawn(async move {
                                            if let Ok(analysis) = det
                                                .analyze_screenshot(&gray_jpeg, &keystrokes, &sid)
                                                .await
                                            {
                                                if analysis.result.level
                                                    >= guacr_threat_detection::ThreatLevel::Medium
                                                {
                                                    warn!(
                                                        "[conn={}] RBI: screenshot threat: {} (level={:?})",
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

                            if dirty_tracker.has_changed(&screenshot) {
                                if let Err(e) = self.send_screenshot(&screenshot, &to_client).await {
                                    warn!("RBI: Failed to send post-click frame: {}", e);
                                }
                            }
                        }
                        Ok(None) => {}
                        Err(e) => debug!("RBI: Post-click screenshot error: {}", e),
                    }
                }

                // Screencast frame events (active when screencast mode is running)
                // Always present in the select to avoid cfg-in-select issues;
                // guarded by `if use_screencast` which is always false without the chrome feature.
                screencast_frame = async {
                    #[cfg(feature = "chrome")]
                    {
                        match screencast_stream.as_mut() {
                            Some(s) => {
                                use futures::StreamExt as _;
                                s.next().await
                            }
                            None => std::future::pending().await,
                        }
                    }
                    #[cfg(not(feature = "chrome"))]
                    {
                        std::future::pending::<Option<()>>().await
                    }
                // Sliding-window gate: process a new screencast frame only while fewer than
                // 3 frames are in flight. This keeps SCTP traffic bounded (prevents ICE
                // keepalive starvation) while allowing ~6fps at 400ms sync RTT instead of ~2fps.
                }, if use_screencast && frames_in_flight < 3 => {
                    #[cfg(feature = "chrome")]
                    {
                        match screencast_frame {
                            Some(frame) => {
                                // Screencast frame arrived — cancel any pending input-screenshot.
                                post_input_deadline = None;

                                // Ack BEFORE sending the encoded frame so Chrome renders the next
                                // frame in parallel while we transmit this one over WebRTC.
                                chrome_session.ack_screencast_frame(frame.session_id).await.ok();

                                // frame.data is chromiumoxide_types::Binary, base64-encoded JPEG
                                // Binary implements AsRef<str> returning the raw base64 string
                                use base64::{engine::general_purpose::STANDARD as BASE64, Engine};
                                match BASE64.decode(frame.data.as_ref() as &str) {
                                    Ok(frame_bytes) => {
                                        let send_result = self.send_screenshot(&frame_bytes, &to_client).await;
                                        if let Err(e) = send_result {
                                            warn!("RBI: Failed to send screencast frame: {}", e);
                                            break;
                                        }

                                        // Send sync and count in-flight frames
                                        let timestamp = std::time::SystemTime::now()
                                            .duration_since(std::time::UNIX_EPOCH)
                                            .unwrap_or_default()
                                            .as_millis() as u64;
                                        let sync_instr = format!("4.sync,{}.{};", timestamp.to_string().len(), timestamp);
                                        let sync_bytes = Bytes::from(sync_instr);
                                        self.record_server_instruction(&sync_bytes);
                                        if let Err(e) = to_client.send(sync_bytes).await {
                                            warn!("RBI: Failed to send sync: {}", e);
                                            break;
                                        }
                                        self.sync_control.set_pending_sync(timestamp);
                                        frames_in_flight = frames_in_flight.saturating_add(1);

                                        // Content is changing — stay at active FPS
                                        adaptive_fps.boost_fps();

                                        // Feed throughput and, if it moved quality enough to be
                                        // worth the disruption, restart the screencast at the new
                                        // value. CDP's startScreencast has no live quality knob —
                                        // changing it means reissuing the command, which is why
                                        // this is threshold-gated rather than applied every frame.
                                        self.adaptive_quality.track_frame_sent(frame_bytes.len());
                                        let recommended = self.adaptive_quality.calculate_quality();
                                        if should_restart_screencast(
                                            current_screencast_quality,
                                            recommended,
                                        ) {
                                            match chrome_session
                                                .start_screencast(
                                                    "jpeg", // ScreencastConfig::default()'s format; never varied
                                                    recommended,
                                                    self.width,
                                                    self.height,
                                                )
                                                .await
                                            {
                                                Ok(()) => {
                                                    debug!(
                                                        "RBI: screencast quality adjusted {} -> {}",
                                                        current_screencast_quality, recommended
                                                    );
                                                    current_screencast_quality = recommended;
                                                }
                                                Err(e) => warn!(
                                                    "RBI: failed to restart screencast at new quality: {}",
                                                    e
                                                ),
                                            }
                                        }
                                    }
                                    Err(e) => {
                                        warn!("RBI: Screencast frame base64 decode failed: {}", e);
                                    }
                                }
                            }
                            None => {
                                // Stream ended = Chrome CDP connection died (chromiumoxide
                                // handler crashed on an unrecognized CDP event). Exit cleanly
                                // rather than falling back to screenshots that will hang for 10s each.
                                info!("RBI: Screencast stream ended — Chrome connection closed, exiting");
                                break;
                            }
                        }
                    }
                    #[cfg(not(feature = "chrome"))]
                    {
                        // use_screencast is always false without chrome feature; this arm never fires
                        let _ = screencast_frame;
                    }
                }

                // Capture screenshots at adaptive FPS with dirty tracking.
                _ = capture_interval.tick(), if !use_screencast => {
                    debug!("RBI: Capture interval tick - calling capture_screenshot()");
                    match chrome_session.capture_screenshot().await {
                        Ok(Some(screenshot)) => {
                            // Check if frame has changed (dirty tracking)
                            let frame_changed = dirty_tracker.has_changed(&screenshot);

                            if frame_changed {
                                let send_result = self.send_screenshot(&screenshot, &to_client).await;
                                if let Err(e) = send_result {
                                    warn!("RBI: Failed to send frame: {}", e);
                                    break;
                                }

                                // Send sync instruction for flow control (prevents overwhelming slow clients)
                                let timestamp = std::time::SystemTime::now()
                                    .duration_since(std::time::UNIX_EPOCH)
                                    .unwrap_or_default()
                                    .as_millis() as u64;
                                let sync_instr = format!("4.sync,{}.{};", timestamp.to_string().len(), timestamp);
                                let sync_bytes = Bytes::from(sync_instr);
                                self.record_server_instruction(&sync_bytes);

                                if let Err(e) = to_client.send(sync_bytes).await {
                                    warn!("RBI: Failed to send sync: {}", e);
                                    break;
                                }

                                self.sync_control.set_pending_sync(timestamp);
                            }

                            // Boost FPS if actively scrolling
                            if scroll_detector.is_scrolling() {
                                adaptive_fps.boost_fps();
                            }

                            // Update capture interval based on activity (adaptive FPS)
                            let new_interval = adaptive_fps.update(frame_changed);
                            capture_interval = interval(new_interval);

                            // Log FPS changes for monitoring
                            if frame_changed && adaptive_fps.is_active() {
                                debug!("RBI: Activity detected, FPS={}", adaptive_fps.current_fps());
                            } else if !frame_changed && adaptive_fps.is_idle() {
                                debug!("RBI: Static content, FPS={}", adaptive_fps.current_fps());
                            } else if scroll_detector.is_scrolling() {
                                debug!("RBI: Scrolling active, FPS={}", adaptive_fps.current_fps());
                            }
                        }
                        Ok(None) => {
                            // Not time to capture yet
                        }
                        Err(e) => {
                            warn!("RBI: Screenshot capture error: {}", e);
                        }
                    }
                }

                // Resource monitoring (every 5 seconds)
                _ = resource_interval.tick() => {
                    resource_check_count = resource_check_count.wrapping_add(1);

                    // Quick memory check
                    match chrome_session.check_resources(self.config.resource_limits.max_memory_mb).await {
                        Ok(false) => {
                            error!("RBI: Memory limit exceeded ({}MB max) — breaking loop", self.config.resource_limits.max_memory_mb);
                            break;
                        }
                        Err(e) => {
                            debug!("RBI: Resource check error: {}", e);
                        }
                        Ok(true) => {}
                    }

                    // Detailed metrics every 30 seconds (6 checks)
                    if resource_check_count.is_multiple_of(6) {
                        // Chrome performance metrics
                        match chrome_session.get_performance_metrics().await {
                            Ok(metrics) => {
                                info!(
                                    "RBI: Performance - heap={}MB, dom_nodes={}, resources={}",
                                    metrics.js_heap_used_mb,
                                    metrics.dom_node_count,
                                    metrics.resource_count
                                );

                                if metrics.is_heavy_page() {
                                    warn!(
                                        "RBI: Heavy page detected - {} DOM nodes, {} resources",
                                        metrics.dom_node_count,
                                        metrics.resource_count
                                    );
                                }
                            }
                            Err(e) => {
                                debug!("RBI: Performance metrics unavailable: {}", e);
                            }
                        }

                        // Optimization metrics
                        let dirty_stats = dirty_tracker.stats();
                        let fps_stats = adaptive_fps.stats();
                        let scroll_stats = scroll_detector.stats();

                        info!(
                            "RBI: Optimization stats - FPS={} ({}%), frames: captured={}, sent={}, skipped={} ({}% compression)",
                            fps_stats.current_fps,
                            (fps_stats.current_fps * 100) / fps_stats.max_fps,
                            dirty_stats.frames_captured,
                            dirty_stats.frames_sent,
                            dirty_stats.frames_skipped,
                            dirty_stats.compression_ratio as u32
                        );

                        if scroll_stats.scroll_events > 0 {
                            let (avg_x, avg_y) = scroll_stats.avg_distance_per_scroll();
                            info!(
                                "RBI: Scroll stats - events={}, avg_distance=({:.0}, {:.0})",
                                scroll_stats.scroll_events,
                                avg_x,
                                avg_y
                            );
                        }

                        // Reset stats for next period
                        dirty_tracker.reset_stats();
                        scroll_detector.reset_stats();
                    }
                }

                // Poll for clipboard changes (browser → client)
                _ = clipboard_interval.tick() => {
                    if !self.config.disable_copy {
                        match chrome_session.poll_clipboard().await {
                            Ok(Some(text)) => {
                                // Send clipboard to client
                                if let Some(instr) = self.clipboard.handle_browser_clipboard(
                                    text.as_bytes(), "text/plain"
                                ).ok().flatten() {
                                    self.record_server_instruction(&instr);
                                    if let Err(e) = to_client.send(instr).await {
                                        warn!("RBI: Failed to send clipboard: {}", e);
                                    }
                                }
                            }
                            Ok(None) => {
                                // No clipboard change
                            }
                            Err(e) => {
                                debug!("RBI: Clipboard poll error: {}", e);
                            }
                        }
                    }

                    // Also poll for cursor changes
                    match chrome_session.poll_cursor().await {
                        Ok(Some(cursor_type)) => {
                            use crate::cursor::CursorType;
                            // Map RBI CursorType to shared StandardCursor for bitmap rendering
                            let std_cursor = match cursor_type {
                                CursorType::Text => StandardCursor::IBeam,
                                CursorType::None => StandardCursor::None,
                                _ => StandardCursor::Pointer, // Default/Pointer/Wait/etc -> pointer
                            };
                            match self.cursor_manager.send_standard_cursor(std_cursor) {
                                Ok(instrs) => {
                                    if let Err(e) = send_cursor_instructions(instrs, &to_client).await {
                                        warn!("RBI: Failed to send cursor: {}", e);
                                    }
                                }
                                Err(e) => warn!("RBI: Failed to generate cursor: {}", e),
                            }
                        }
                        Ok(None) => {
                            // No cursor change
                        }
                        Err(e) => {
                            debug!("RBI: Cursor poll error: {}", e);
                        }
                    }

                    // Poll for scroll changes
                    match chrome_session.poll_scroll().await {
                        Ok(Some(position)) => {
                            if let Some((delta_x, delta_y)) = scroll_detector.update(position) {
                                // Scroll detected - boost FPS and capture immediately
                                adaptive_fps.boost_fps();

                                // Determine scroll significance
                                let viewport_height = self.height as i32;
                                let is_significant = scroll_detector.is_significant_scroll(delta_y, viewport_height);
                                let is_page_scroll = scroll_detector.is_page_scroll(delta_y, viewport_height);
                                let velocity = scroll_detector.velocity();

                                debug!(
                                    "RBI: Scroll detected: delta=({}, {}), velocity={:.0}px/s, significant={}, page_scroll={}",
                                    delta_x, delta_y, velocity, is_significant, is_page_scroll
                                );

                                // Immediate frame capture for smooth scrolling
                                if is_significant {
                                    match chrome_session.capture_screenshot().await {
                                        Ok(Some(screenshot)) => {
                                            if dirty_tracker.has_changed(&screenshot) {
                                                let send_result = self.send_screenshot(&screenshot, &to_client).await;
                                                if let Err(e) = send_result {
                                                    warn!("RBI: Failed to send scroll frame: {}", e);
                                                } else {
                                                    debug!("RBI: Sent immediate scroll frame");
                                                }
                                            }
                                        }
                                        Ok(None) => {}
                                        Err(e) => {
                                            debug!("RBI: Scroll frame capture error: {}", e);
                                        }
                                    }
                                }
                            }
                        }
                        Ok(None) => {
                            // No scroll change
                        }
                        Err(e) => {
                            debug!("RBI: Scroll poll error: {}", e);
                        }
                    }

                    // Poll for file chooser (upload) requests
                    if self.upload_engine.manager().is_enabled() {
                        match chrome_session.poll_file_chooser().await {
                            Ok(Some(request)) => {
                                info!("RBI: File chooser opened - multiple={}", request.multiple);
                                // Send upload dialog request to client
                                let instr = format_upload_dialog_instruction(&request);
                                self.record_server_instruction(&instr);
                                if let Err(e) = to_client.send(instr).await {
                                    warn!("RBI: Failed to send upload dialog: {}", e);
                                }
                                // Track the pending request
                                self.upload_engine.manager_mut().handle_dialog_request(
                                    request.multiple,
                                    request.accept,
                                );
                            }
                            Ok(None) => {}
                            Err(e) => {
                                debug!("RBI: File chooser poll error: {}", e);
                            }
                        }
                    }

                    // Check for dialog timeouts
                    if let Some(response) = self.dialog_manager.check_timeout() {
                        debug!("RBI: Dialog timed out - id={}", response.id);
                        // Dialog was auto-dismissed, no need to send anything
                    }
                }


                else => {
                    info!("RBI: select else branch — all arms disabled, exiting loop");
                    break;
                }
            }
        }

        // Close Chrome explicitly before anything else — frees the subprocess,
        // all its sockets, and the temp profile directory.
        chrome_session.close().await;

        // Finalize recording
        if let Some(recorder) = self.recorder.take() {
            if let Err(e) = recorder.finalize() {
                warn!("RBI: Failed to finalize recording: {}", e);
            } else {
                info!("RBI: Session recording finalized");
            }
        }

        send_disconnect(&to_client).await;
        info!("RBI: Chrome session ended");
        Ok(())
    }

    /// Handle client input (keyboard, mouse, touch, navigation, clipboard)
    async fn handle_client_input(
        &mut self,
        chrome_session: &mut crate::chrome_session::ChromeSession,
        msg: &Bytes,
        to_client: &mpsc::Sender<Bytes>,
        last_mouse_move: &mut Option<std::time::Instant>,
    ) -> Result<(), String> {
        // Dispatch binary protocol messages (vault sends binary when binaryProtocolActive=true).
        // Binary messages start with opcode byte < 0x30; text starts with ASCII digit 0x30-0x39.
        // Header: opcode(1) + flags(1) + reserved(2) + length(4) = 8 bytes.
        if !msg.is_empty() && msg[0] < 0x30 {
            use guacr_protocol::Opcode;
            if msg.len() >= 9 {
                let opcode = msg[0];
                let payload = &msg[8..]; // skip 8-byte header
                if opcode == Opcode::Mouse as u8 && payload.len() >= 6 {
                    let x = u16::from_le_bytes([payload[0], payload[1]]) as i32;
                    let y = u16::from_le_bytes([payload[2], payload[3]]) as i32;
                    let buttons = payload[4] as u32;
                    // Inject directly into Chrome — same path as text mouse handler below
                    let mouse_event = self.input_handler.handle_mouse(x, y, buttons);
                    for button in &mouse_event.buttons_pressed {
                        let n = match button {
                            crate::input::MouseButton::Left => 0,
                            crate::input::MouseButton::Middle => 1,
                            crate::input::MouseButton::Right => 2,
                        };
                        chrome_session
                            .inject_mouse(x, y, n, true, self.input_handler.mouse_buttons_mask())
                            .await?;
                    }
                    for button in &mouse_event.buttons_released {
                        let n = match button {
                            crate::input::MouseButton::Left => 0,
                            crate::input::MouseButton::Middle => 1,
                            crate::input::MouseButton::Right => 2,
                        };
                        chrome_session
                            .inject_mouse(x, y, n, false, self.input_handler.mouse_buttons_mask())
                            .await?;
                    }
                    if let Some(delta_y) = mouse_event.scroll_delta_y {
                        chrome_session.inject_scroll(x, y, 0, delta_y).await?;
                    }
                } else if opcode == Opcode::MouseDelta as u8 && payload.len() >= 4 {
                    // Delta-encoded mouse: dx(i8), dy(i8), button_mask(u8), scroll_delta(i8)
                    let dx = payload[0] as i8;
                    let dy = payload[1] as i8;
                    let buttons = payload[2] as u32;
                    let scroll = payload[3] as i8;
                    let (abs_x, abs_y) = self.input_handler.mouse_position();
                    let x = (abs_x + dx as i32).clamp(0, self.width as i32 - 1);
                    let y = (abs_y + dy as i32).clamp(0, self.height as i32 - 1);
                    let mouse_event = self.input_handler.handle_mouse(x, y, buttons);
                    for button in &mouse_event.buttons_pressed {
                        let n = match button {
                            crate::input::MouseButton::Left => 0,
                            crate::input::MouseButton::Middle => 1,
                            crate::input::MouseButton::Right => 2,
                        };
                        chrome_session
                            .inject_mouse(x, y, n, true, self.input_handler.mouse_buttons_mask())
                            .await?;
                    }
                    for button in &mouse_event.buttons_released {
                        let n = match button {
                            crate::input::MouseButton::Left => 0,
                            crate::input::MouseButton::Middle => 1,
                            crate::input::MouseButton::Right => 2,
                        };
                        chrome_session
                            .inject_mouse(x, y, n, false, self.input_handler.mouse_buttons_mask())
                            .await?;
                    }
                    let now = std::time::Instant::now();
                    let should_move = last_mouse_move
                        .map(|t| now.duration_since(t).as_millis() >= 33)
                        .unwrap_or(true);
                    if should_move
                        && chrome_session
                            .inject_mouse_move(x, y, self.input_handler.mouse_buttons_mask())
                            .await
                            .unwrap_or(false)
                    {
                        *last_mouse_move = Some(now);
                    }
                    if scroll != 0 {
                        chrome_session.inject_scroll(x, y, 0, scroll as i32).await?;
                    }
                } else if opcode == Opcode::Key as u8 && payload.len() >= 6 {
                    let keysym =
                        u32::from_le_bytes([payload[0], payload[1], payload[2], payload[3]]);
                    let pressed = payload[4] == 1;
                    let key_event = self.input_handler.handle_keyboard(keysym, pressed);
                    let cdp_mods = chrome_flags_to_cdp_modifiers(key_event.modifiers);
                    chrome_session
                        .inject_keyboard(keysym, pressed, cdp_mods)
                        .await
                        .unwrap_or_default();
                }
            }
            return Ok(()); // binary opcode handled (or unknown — ignore)
        }

        let instr = GuacamoleParser::parse_instruction(msg)
            .map_err(|e| format!("Failed to parse instruction: {}", e))?;

        match instr.opcode {
            "key" => {
                if instr.args.len() >= 2 {
                    if let (Ok(keysym), Ok(pressed)) =
                        (instr.args[0].parse::<u32>(), instr.args[1].parse::<u8>())
                    {
                        let pressed = pressed == 1;

                        // Use the new input handler for proper state tracking
                        let key_event = self.input_handler.handle_keyboard(keysym, pressed);
                        let cdp_mods = chrome_flags_to_cdp_modifiers(key_event.modifiers);

                        // Check for keyboard shortcuts (Ctrl+C, Ctrl+V, etc.)
                        if let Some(shortcut) = self.input_handler.check_shortcut(keysym, pressed) {
                            match shortcut {
                                KeyboardShortcut::Copy => {
                                    info!("RBI: Copy shortcut detected");
                                    // Browser handles copy internally
                                }
                                KeyboardShortcut::Paste => {
                                    info!("RBI: Paste shortcut detected");
                                    // Browser handles paste internally
                                }
                                KeyboardShortcut::Cut => {
                                    info!("RBI: Cut shortcut detected");
                                }
                                KeyboardShortcut::SelectAll => {
                                    info!("RBI: Select All shortcut detected");
                                }
                            }
                            // Let the browser handle the shortcut
                        }

                        // Buffer printable keystrokes for threat detection context.
                        #[cfg(feature = "threat-detection")]
                        if pressed && self.threat_detector.is_some() && keysym < 0x100 {
                            if let Some(c) = char::from_u32(keysym) {
                                if c.is_ascii_graphic() || c == ' ' {
                                    self.threat_keystroke_buffer.push(c);
                                }
                            }
                        }

                        // Inject the key event into browser via CDP (isTrusted=true)
                        chrome_session
                            .inject_keyboard(keysym, pressed, cdp_mods)
                            .await?;
                    }
                }
            }
            "mouse" => {
                if instr.args.len() >= 3 {
                    if let (Ok(x), Ok(y), Ok(mask)) = (
                        instr.args[0].parse::<i32>(),
                        instr.args[1].parse::<i32>(),
                        instr.args[2].parse::<u32>(),
                    ) {
                        // Clamp coordinates
                        let x = x.max(0).min(self.width as i32 - 1);
                        let y = y.max(0).min(self.height as i32 - 1);

                        // Throttle MouseMoved CDP calls to ~30fps to avoid flooding
                        // the CDP channel and starving click/scroll/screenshot calls.
                        let now = std::time::Instant::now();
                        let should_send_move = last_mouse_move
                            .map(|t: std::time::Instant| now.duration_since(t).as_millis() >= 33)
                            .unwrap_or(true);
                        // Pass current buttons mask so Chrome tracks hover state correctly.
                        let pre_buttons = self.input_handler.mouse_buttons_mask();
                        if should_send_move
                            && chrome_session
                                .inject_mouse_move(x, y, pre_buttons)
                                .await
                                .unwrap_or(false)
                        {
                            *last_mouse_move = Some(now);
                        }

                        // Update button state — must happen before reading post-event mask.
                        let mouse_event = self.input_handler.handle_mouse(x, y, mask);

                        // Handle button presses (post-event mask: pressed button is now held)
                        for button in &mouse_event.buttons_pressed {
                            let button_num = match button {
                                crate::input::MouseButton::Left => 0,
                                crate::input::MouseButton::Middle => 1,
                                crate::input::MouseButton::Right => 2,
                            };
                            let post_buttons = self.input_handler.mouse_buttons_mask();
                            chrome_session
                                .inject_mouse(x, y, button_num, true, post_buttons)
                                .await?;
                        }

                        // Handle button releases (post-event mask: released button no longer held)
                        for button in &mouse_event.buttons_released {
                            let button_num = match button {
                                crate::input::MouseButton::Left => 0,
                                crate::input::MouseButton::Middle => 1,
                                crate::input::MouseButton::Right => 2,
                            };
                            let post_buttons = self.input_handler.mouse_buttons_mask();
                            chrome_session
                                .inject_mouse(x, y, button_num, false, post_buttons)
                                .await?;
                        }

                        // Handle scroll
                        if let Some(delta_y) = mouse_event.scroll_delta_y {
                            chrome_session.inject_scroll(x, y, 0, delta_y).await?;
                        }
                    }
                }
            }
            "touch" => {
                // Touch event: touch,<id>,<x>,<y>,<radius_x>,<radius_y>,<angle>,<force>;
                if instr.args.len() >= 7 {
                    if let (
                        Ok(id),
                        Ok(x),
                        Ok(y),
                        Ok(radius_x),
                        Ok(radius_y),
                        Ok(angle),
                        Ok(force),
                    ) = (
                        instr.args[0].parse::<i32>(),
                        instr.args[1].parse::<i32>(),
                        instr.args[2].parse::<i32>(),
                        instr.args[3].parse::<i32>(),
                        instr.args[4].parse::<i32>(),
                        instr.args[5].parse::<f64>(),
                        instr.args[6].parse::<f64>(),
                    ) {
                        if let Some(touch_event) = self
                            .input_handler
                            .handle_touch(id, x, y, radius_x, radius_y, angle, force)
                        {
                            chrome_session.inject_touch(&touch_event).await?;
                        }
                    }
                }
            }
            "size" => {
                // Client size instruction format: size,<layer>,<width>,<height>;
                // We ignore the layer (args[0]) and use width/height (args[1], args[2])
                if instr.args.len() >= 3 {
                    if let (Ok(w), Ok(h)) =
                        (instr.args[1].parse::<u32>(), instr.args[2].parse::<u32>())
                    {
                        info!(
                            "RBI: Resize requested: {}x{} (layer: {})",
                            w, h, instr.args[0]
                        );
                        self.width = w;
                        self.height = h;
                        chrome_session.resize(w, h).await?;
                    }
                }
            }
            "clipboard" => {
                // Clipboard instruction: clipboard,<mimetype>;
                // Followed by blob instructions with data
                if let Some(mimetype) = instr.args.first() {
                    debug!("RBI: Clipboard stream started, mimetype: {}", mimetype);
                    // Clipboard data will come in blob instructions
                }
            }
            "blob" => {
                // Blob instruction: blob,<stream_id>,<base64_data>;
                if instr.args.len() >= 2 {
                    let data = instr.args[1];
                    use base64::Engine;
                    if let Ok(decoded) = base64::engine::general_purpose::STANDARD.decode(data) {
                        // Handle clipboard data
                        if let Some(browser_data) = self
                            .clipboard
                            .handle_client_clipboard(&decoded, "text/plain")?
                        {
                            chrome_session.set_clipboard(&browser_data).await?;
                        }
                    }
                }
            }
            "navigate" => {
                // Navigation: navigate,<position>;
                // position: -1 = back, 0 = refresh, 1 = forward
                if let Some(pos_str) = instr.args.first() {
                    if let Ok(position) = pos_str.parse::<i32>() {
                        if !self.config.allow_url_manipulation && position != 0 {
                            warn!("RBI: URL manipulation disabled, blocking navigation");
                        } else {
                            chrome_session.navigate_history(position).await?;
                        }
                    }
                }
            }
            "goto" => {
                // Go to URL: goto,<url>;
                if let Some(url) = instr.args.first() {
                    if !self.config.allow_url_manipulation {
                        warn!("RBI: URL manipulation disabled, blocking goto");
                    } else if let Err(e) = validate_navigate_scheme(url) {
                        warn!("RBI: goto blocked — {}", e);
                    } else if !self.is_url_allowed(url) {
                        warn!("RBI: URL not in allowlist");
                    } else {
                        chrome_session.navigate_to(url).await?;
                    }
                }
            }
            "download" => {
                // Handle download request: download,<url>,<filename>;
                if instr.args.len() >= 2 {
                    let url = &instr.args[0];
                    let filename = &instr.args[1];
                    if let Err(e) = chrome_session
                        .handle_download(url, filename, &self.config.download_config, to_client)
                        .await
                    {
                        warn!("RBI: Download failed: {}", e);
                    }
                }
            }
            "file" => {
                // Start file upload: file,<stream_id>,<mimetype>,<filename>;
                if instr.args.len() >= 3 {
                    let stream_id = &instr.args[0];
                    let mimetype = &instr.args[1];
                    let filename = &instr.args[2];

                    // Size will come from ack or be determined from blob data
                    // For now, use 0 and track actual size from blobs
                    match self
                        .upload_engine
                        .start_upload(stream_id, filename, mimetype, 0)
                    {
                        Ok(upload_id) => {
                            info!("RBI: Upload started - id={}, file={}", upload_id, filename);
                        }
                        Err(e) => {
                            warn!("RBI: Upload rejected: {}", e);
                            // Send error ack
                            let ack = format!(
                                "3.ack,{}.{},6.UPLOAD,5.error;",
                                stream_id.len(),
                                stream_id
                            );
                            let ack_bytes = Bytes::from(ack);
                            self.record_server_instruction(&ack_bytes);
                            let _ = to_client.send(ack_bytes).await;
                        }
                    }
                }
            }
            "upload-blob" => {
                // Upload data chunk: upload-blob,<upload_id>,<base64_data>;
                if instr.args.len() >= 2 {
                    let upload_id = &instr.args[0];
                    let data = instr.args[1];

                    use base64::Engine;
                    if let Ok(decoded) = base64::engine::general_purpose::STANDARD.decode(data) {
                        match self.upload_engine.handle_chunk(upload_id, &decoded) {
                            Ok(progress) => {
                                debug!(
                                    "RBI: Upload progress - id={}, {}%",
                                    upload_id, progress as u32
                                );
                            }
                            Err(e) => {
                                warn!("RBI: Upload chunk error: {}", e);
                            }
                        }
                    }
                }
            }
            "upload-end" => {
                // End file upload: upload-end,<upload_id>;
                if let Some(upload_id) = instr.args.first() {
                    match self.upload_engine.complete_upload(upload_id) {
                        Ok((info, data)) => {
                            info!(
                                "RBI: Upload complete - file={}, size={}",
                                info.filename,
                                data.len()
                            );

                            // Submit file to browser
                            let file_data =
                                vec![(info.filename.clone(), info.mimetype.clone(), data)];
                            if let Err(e) = chrome_session.submit_upload_files(&file_data).await {
                                warn!("RBI: Failed to submit upload to browser: {}", e);
                            }
                        }
                        Err(e) => {
                            warn!("RBI: Upload completion error: {}", e);
                        }
                    }
                }
            }
            "upload-cancel" => {
                // Cancel file upload: upload-cancel,<upload_id>;
                if let Some(upload_id) = instr.args.first() {
                    if let Err(e) = self.upload_engine.cancel_upload(upload_id) {
                        warn!("RBI: Upload cancel error: {}", e);
                    } else {
                        info!("RBI: Upload cancelled - id={}", upload_id);
                    }
                }
            }
            "dialog-response" => {
                // Response to JS dialog: dialog-response,<id>,<confirmed>,<input>;
                if instr.args.len() >= 2 {
                    let id = instr.args[0].to_string();
                    let confirmed = instr.args[1] == "1" || instr.args[1] == "true";
                    let input = instr.args.get(2).map(|s| s.to_string());

                    let response = crate::js_dialog::JsDialogResponse {
                        id,
                        confirmed,
                        input,
                    };

                    if let Err(e) = self.dialog_manager.handle_response(response) {
                        warn!("RBI: Dialog response error: {}", e);
                    }
                }
            }
            _ => {
                debug!("RBI: Unknown instruction: {}", instr.opcode);
            }
        }

        Ok(())
    }

    /// Check if URL is allowed by patterns
    fn is_url_allowed(&self, url: &str) -> bool {
        if self.config.allowed_url_patterns.is_empty() {
            return true; // No restrictions
        }
        is_url_allowed_for_patterns(url, &self.config.allowed_url_patterns)
    }
}

/// Check if a URL is allowed by the given patterns.
///
/// Uses host-based matching to prevent path-confusion bypasses where
/// `url.contains("example.com")` would accept `evil.com/example.com`.
///
/// Patterns without `*` must match the URL's host exactly or as a suffix.
/// Patterns with `*.` prefix match any subdomain of the given domain.
pub(crate) fn is_url_allowed_for_patterns(url: &str, patterns: &[String]) -> bool {
    // Extract the host from the URL without using the url crate
    // to avoid pulling in an extra dep. Simple string parsing suffices
    // since we only need to isolate the host portion.
    let host = extract_url_host(url);

    for pattern in patterns {
        if let Some(domain) = pattern.strip_prefix("*.") {
            // Wildcard: match exact domain or any subdomain
            if host == domain || host.ends_with(&format!(".{}", domain)) {
                return true;
            }
        } else {
            // Exact or subdomain match — host must equal pattern or end with ".pattern"
            let pat = pattern
                .trim_start_matches("https://")
                .trim_start_matches("http://");
            let pat = pat.split('/').next().unwrap_or(pat); // strip any path component
            if host == pat || host.ends_with(&format!(".{}", pat)) {
                return true;
            }
        }
    }
    false
}

/// Return a redacted form of a URL safe for logging (scheme + host only).
///
/// Full URLs must not be logged at info! level because query parameters and path
/// components may contain session tokens, credentials, or sensitive resource names.
pub(crate) fn rbi_safe_url_for_log(url: &str) -> String {
    if let Some(scheme_end) = url.find("://") {
        let scheme = &url[..scheme_end];
        let rest = &url[scheme_end + 3..];
        let host = rest.split(['/', '?', '#']).next().unwrap_or(rest);
        format!("{}://{}", scheme, host)
    } else {
        let prefix_len = url.len().min(16);
        format!("{}...", &url[..prefix_len])
    }
}

/// Validate that a URL scheme is safe to navigate Chrome to.
///
/// Only http:// and https:// are allowed. All other schemes (javascript:, data:,
/// file://, about:, chrome://, etc.) must be rejected before the URL reaches Chrome
/// to prevent scheme-based code execution or local file access.
///
/// Returns Ok(()) if the scheme is safe, Err with a description if not.
pub fn validate_navigate_scheme(url: &str) -> Result<(), String> {
    let lower = url.to_lowercase();
    if lower.starts_with("https://") || lower.starts_with("http://") {
        return Ok(());
    }
    // Extract scheme for the error message
    let scheme = lower.split("://").next().unwrap_or(url);
    Err(format!(
        "scheme '{}' is not allowed for navigation; only http and https are permitted",
        scheme
    ))
}

/// Extract the host (without port) from a URL string without the url crate.
fn extract_url_host(url: &str) -> &str {
    // Strip scheme
    let after_scheme = if let Some(rest) = url.strip_prefix("https://") {
        rest
    } else if let Some(rest) = url.strip_prefix("http://") {
        rest
    } else {
        url
    };
    // Take everything up to the first / or ?
    let host_with_port = after_scheme
        .split(['/', '?', '#'])
        .next()
        .unwrap_or(after_scheme);
    // Strip port
    if host_with_port.starts_with('[') {
        // IPv6
        host_with_port
    } else {
        host_with_port.split(':').next().unwrap_or(host_with_port)
    }
}

impl BrowserClient {
    /// Send screenshot to client using chunked blob protocol
    ///
    /// This uses the shared chunking logic from guacr-protocol, matching RDP/SSH/Terminal.
    /// Pattern: img instruction + chunked blobs (6KB each) + end instruction.
    async fn send_screenshot(
        &mut self,
        screenshot: &[u8],
        to_client: &mpsc::Sender<Bytes>,
    ) -> Result<(), String> {
        use guacr_protocol::{BinaryEncoder, ImageFormat};

        // Send JPEG bytes as binary IMAGE opcode 0x10.
        // The vault's BinaryProtocolParser routes 0x10 to BinaryRenderer → onBinaryActive
        // → markConnected(). No base64, no re-encoding — raw JPEG from Chrome CDP.
        // (TextProtocolEncoder was wrong here: text `img` starts with byte 0x33 which the
        //  vault routes to the Guacamole text parser, never reaching the BinaryRenderer.)
        let format = if screenshot.len() >= 2 && screenshot[0] == 0xFF && screenshot[1] == 0xD8 {
            ImageFormat::Jpeg as u8
        } else {
            ImageFormat::Png as u8
        };

        // Build IMAGE payload: x(u16) y(u16) w(u16) h(u16) format(u8) compression(u8) pad(u16) + data
        let mut payload = Vec::with_capacity(12 + screenshot.len());
        payload.extend_from_slice(&(0u16).to_le_bytes()); // x
        payload.extend_from_slice(&(0u16).to_le_bytes()); // y
        payload.extend_from_slice(&(self.width as u16).to_le_bytes());
        payload.extend_from_slice(&(self.height as u16).to_le_bytes());
        payload.push(format);
        payload.push(0); // compression: none
        payload.extend_from_slice(&(0u16).to_le_bytes()); // padding
        payload.extend_from_slice(screenshot);

        // Fragment if > 60 KB — data channel max safe payload size.
        let mut enc = BinaryEncoder::new();
        let frames = enc.fragment_message(guacr_protocol::Opcode::Image, 0, &payload);

        debug!(
            "RBI: Sending binary IMAGE ({} KB, {} fragment(s))",
            payload.len() / 1024,
            frames.len()
        );

        for frame in frames {
            self.record_server_instruction(&frame);
            to_client
                .send(frame)
                .await
                .map_err(|e| format!("Failed to send binary IMAGE fragment: {}", e))?;
            // Yield between fragments so the ICE keepalive task can run.
            // Without this, 4 back-to-back 60KB sends saturate the SCTP send buffer
            // and starve the ICE ping task, causing spurious ICE disconnects.
            tokio::task::yield_now().await;
        }

        self.stream_id = self.stream_id.wrapping_add(1);
        Ok(())
    }

    /// Record a server-to-client instruction (if recording is enabled)
    fn record_server_instruction(&mut self, instruction: &Bytes) {
        if let Some(ref mut recorder) = self.recorder {
            if let Err(e) =
                recorder.record_instruction(RecordingDirection::ServerToClient, instruction)
            {
                warn!("RBI: Failed to record instruction: {}", e);
            }
        }
    }

    /// Record a client-to-server instruction (if recording is enabled)
    fn record_client_input(&mut self, instruction: &Bytes) {
        shared_record_client_input(&mut self.recorder, instruction);
    }
}
