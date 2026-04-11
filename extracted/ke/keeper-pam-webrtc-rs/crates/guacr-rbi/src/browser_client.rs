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
    send_name, send_ready, CursorManager, MultiFormatRecorder, RecordingConfig, RecordingDirection,
    StandardCursor, SyncFlowControl,
};
use std::collections::HashMap;
use std::sync::Arc;

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
}

impl BrowserClient {
    /// Create a new browser client
    pub fn new(
        width: u32,
        height: u32,
        config: RbiConfig,
        recording_config: &RecordingConfig,
        params: &HashMap<String, String>,
        _video_tx: Option<Arc<dyn guacr_handlers::VideoOutput>>,
    ) -> Self {
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

        Self {
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
        }
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
        info!("RBI: Launching browser for URL: {}", url);

        // TODO: Implement browser launch based on backend
        //
        // For Chrome backend:
        // 1. Launch headless Chrome with security flags
        // 2. Navigate to URL
        // 3. Capture screenshots periodically
        // 4. Handle input events (mouse, keyboard)
        //
        // For Servo backend (future):
        // 1. Launch Servo engine
        // 2. Navigate to URL
        // 3. Capture screenshots
        // 4. Handle input events

        match self.config.backend {
            RbiBackend::Chrome => {
                self.launch_chrome(url, to_client, from_client).await?;
            }
            RbiBackend::Servo => {
                return Err("Servo backend not yet implemented".to_string());
            }
            RbiBackend::ServoWithFallback => {
                // Try Servo first, fallback to Chrome
                if self.is_servo_compatible(url) {
                    return Err("Servo backend not yet implemented".to_string());
                } else {
                    self.launch_chrome(url, to_client, from_client).await?;
                }
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

        info!("RBI: Launching Chrome browser for URL: {}", url);

        // Launch Chrome with chromiumoxide
        let mut chrome_session = ChromeSession::new(
            self.width,
            self.height,
            self.config.capture_fps,
            &self.config.chromium_path,
        );

        // 30-second timeout prevents the session from hanging indefinitely if the
        // chromium subprocess fails to start or never opens its DevTools port.
        tokio::time::timeout(
            Duration::from_secs(30),
            chrome_session.launch(url, &self.config.chromium_path, &self.config.popup_handling),
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

        // Post-click screenshot fallback: tracks whether we need a screenshot
        // 150ms after a left-click (in case Chrome's screencast doesn't push a frame).
        let mut post_click_capture = false;
        let mut prev_mouse_mask: u32 = 0;

        // Screencast mode (use if enabled in config, otherwise fall back to screenshots)
        let mut use_screencast = self.config.use_screencast.unwrap_or(true);
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

            // Start screencast using actual session dimensions to avoid downscaling
            let screencast_config = ScreencastConfig {
                max_width: self.width,
                max_height: self.height,
                quality: 85,
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
        // leaving the user staring at a blank screen until they interact. This primes
        // the display regardless of which capture mode is active.
        #[cfg(feature = "chrome")]
        {
            match chrome_session.capture_screenshot().await {
                Ok(Some(screenshot)) => {
                    if let Err(e) = self.send_screenshot(&screenshot, &to_client).await {
                        warn!("RBI: Failed to send initial screenshot: {}", e);
                    } else {
                        debug!("RBI: Initial screenshot sent ({} bytes)", screenshot.len());
                        // Seed the dirty tracker so subsequent identical frames are skipped.
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

        loop {
            tokio::select! {
                biased; // Check arms in order: input first, then frames, then timers.
                        // Ensures clicks/keyboard/scroll are never starved by a
                        // high-frequency screencast stream.

                // Client input has highest priority — process immediately when ready.
                // Listed first so biased select always drains input before rendering.
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("RBI: Client disconnected");
                        break;
                    };
                    self.record_client_input(&msg);
                    if let Ok(msg_str) = std::str::from_utf8(&msg) {
                        if msg_str.starts_with("4.sync,") {
                            if let Some(ts) = self.sync_control.pending_timestamp() {
                                self.sync_control.clear_pending();
                                debug!("RBI: Client acknowledged sync (ts={})", ts);
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
                    if let Err(e) = self.handle_client_input(&mut chrome_session, &msg, &to_client, &mut last_mouse_move).await {
                        warn!("RBI: Error handling input: {}", e);
                    }

                    // Detect left-button release to schedule a post-click fallback screenshot.
                    if let Ok(instr) = guacr_protocol::GuacamoleParser::parse_instruction(&msg) {
                        if instr.opcode == "mouse" && instr.args.len() >= 3 {
                            if let Ok(mask) = instr.args[2].parse::<u32>() {
                                if (prev_mouse_mask & 1) != 0 && (mask & 1) == 0 {
                                    post_click_capture = true;
                                }
                                prev_mouse_mask = mask;
                            }
                        }
                    }
                }

                // Post-click screenshot fallback: fires 150ms after left-click release if
                // Chrome's screencast hasn't pushed a new frame (common in headless mode).
                _ = tokio::time::sleep(tokio::time::Duration::from_millis(150)), if post_click_capture => {
                    post_click_capture = false;
                    match chrome_session.capture_screenshot().await {
                        Ok(Some(screenshot)) => {
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
                }, if use_screencast => {
                    #[cfg(feature = "chrome")]
                    {
                        match screencast_frame {
                            Some(frame) => {
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

                                        // Send sync instruction for flow control
                                        let timestamp = std::time::SystemTime::now()
                                            .duration_since(std::time::UNIX_EPOCH)
                                            .unwrap()
                                            .as_millis() as u64;
                                        let sync_instr = format!("4.sync,{}.{};", timestamp.to_string().len(), timestamp);
                                        let sync_bytes = Bytes::from(sync_instr);
                                        self.record_server_instruction(&sync_bytes);
                                        if let Err(e) = to_client.send(sync_bytes).await {
                                            warn!("RBI: Failed to send sync: {}", e);
                                            break;
                                        }
                                        self.sync_control.set_pending_sync(timestamp);

                                        // Ack immediately so Chrome can prepare the next frame.
                                        // Input starvation is prevented by biased select (input arm first).
                                        chrome_session.ack_screencast_frame(frame.session_id).await.ok();

                                        // Content is changing — stay at active FPS
                                        adaptive_fps.boost_fps();
                                    }
                                    Err(e) => {
                                        warn!("RBI: Screencast frame base64 decode failed: {}", e);
                                    }
                                }
                            }
                            None => {
                                // Stream ended — fall back to screenshot mode
                                warn!("RBI: Screencast stream ended, falling back to screenshots");
                                screencast_stream = None;
                                use_screencast = false;
                            }
                        }
                    }
                    #[cfg(not(feature = "chrome"))]
                    {
                        // use_screencast is always false without chrome feature; this arm never fires
                        let _ = screencast_frame;
                    }
                }

                // Capture screenshots at adaptive FPS with dirty tracking (fallback when not in screencast mode)
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
                                    .unwrap()
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
                            error!("RBI: Memory limit exceeded ({}MB max)", self.config.resource_limits.max_memory_mb);
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
                    debug!("RBI: Connection closed");
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
                    } else if !self.is_url_allowed(url) {
                        warn!("RBI: URL not in allowlist: {}", url);
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

        for pattern in &self.config.allowed_url_patterns {
            if let Some(suffix) = pattern.strip_prefix('*') {
                // Wildcard pattern - must match as domain suffix
                // e.g., "*.example.com" should match "sub.example.com" but not "malicious-example.com"
                if url.ends_with(suffix) || url.contains(&format!("/{}", suffix)) {
                    return true;
                }
            } else if url.contains(pattern) {
                return true;
            }
        }

        false
    }

    /// Check if URL is compatible with Servo
    fn is_servo_compatible(&self, url: &str) -> bool {
        // Check against allowlist
        for allowed in &self.config.servo_allowlist {
            if url.contains(allowed) {
                return true;
            }
        }
        false
    }

    /// Send screenshot to client using chunked blob protocol
    ///
    /// This uses the shared chunking logic from guacr-protocol, matching RDP/SSH/Terminal.
    /// Pattern: img instruction + chunked blobs (6KB each) + end instruction.
    async fn send_screenshot(
        &mut self,
        screenshot: &[u8],
        to_client: &mpsc::Sender<Bytes>,
    ) -> Result<(), String> {
        use base64::{engine::general_purpose::STANDARD as BASE64, Engine};
        use guacr_protocol::{format_chunked_blobs, TextProtocolEncoder};

        // Detect image format from header
        // JPEG: starts with 0xFF 0xD8
        // PNG: starts with 0x89 0x50 0x4E 0x47
        let mimetype = if screenshot.len() >= 2 && screenshot[0] == 0xFF && screenshot[1] == 0xD8 {
            "image/jpeg"
        } else {
            "image/png"
        };

        // Base64 encode the screenshot
        let base64_data = BASE64.encode(screenshot);
        let base64_len = base64_data.len();

        debug!(
            "RBI: Sending screenshot ({} KB, {})",
            base64_len / 1024,
            mimetype
        );

        // Send img instruction with metadata
        // CRITICAL: x=0, y=0 means top-left corner. If client shows image in wrong position,
        // check that the size instruction matches the screenshot dimensions.
        let mut text_encoder = TextProtocolEncoder::new();
        let img_instr = text_encoder.format_img_instruction(
            self.stream_id,
            0, // layer
            0, // x (top-left)
            0, // y (top-left)
            mimetype,
        );

        debug!(
            "RBI: Sending img instruction - stream: {}, layer: 0, pos: (0,0), type: {}",
            self.stream_id, mimetype
        );

        let img_bytes = img_instr.freeze();
        self.record_server_instruction(&img_bytes);
        to_client
            .send(img_bytes)
            .await
            .map_err(|e| format!("Failed to send img instruction: {}", e))?;

        // Send blob data in 6KB chunks + end instruction (shared logic from guacr-protocol)
        let blob_instructions = format_chunked_blobs(self.stream_id, &base64_data, None);

        debug!(
            "RBI: Sending {} blob chunks + end instruction",
            blob_instructions.len() - 1 // -1 for end instruction
        );

        for (idx, instr) in blob_instructions.iter().enumerate() {
            let bytes = Bytes::from(instr.clone());
            self.record_server_instruction(&bytes);
            to_client
                .send(bytes)
                .await
                .map_err(|e| format!("Failed to send instruction {}: {}", idx, e))?;
        }

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
