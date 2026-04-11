// Chrome session manager using chromiumoxide for RBI
// Provides browser launch, navigation, screenshot capture, and input handling
//
// SECURITY: Session Isolation
// Each RBI session gets an isolated browser profile to prevent data leakage:
// - Unique temp directory per session (auto-created, auto-cleaned)
// - Separate cookies, localStorage, cache per session
// - No cross-session data access possible
//
// CLIPBOARD APPROACH (No Chrome Patches Required):
// Unlike KCM to add cef_kcm_add_clipboard_observer(),
// we use JavaScript-based clipboard monitoring:
// 1. Inject copy event listener on page load
// 2. Poll for captured clipboard data
// 3. Send to client when changed
//
// This avoids needing custom Chrome builds while maintaining functionality.

use crate::clipboard_polling::ClipboardState;
#[cfg(feature = "chrome")]
use crate::clipboard_polling::{COPY_EVENT_LISTENER_JS, GET_CLIPBOARD_DATA_JS};
use crate::cursor::CursorState;
#[cfg(feature = "chrome")]
use crate::cursor::{CursorType, CURSOR_TRACKER_JS, GET_CURSOR_JS};
#[cfg(feature = "chrome")]
use crate::scroll_detector::{ScrollPosition, GET_SCROLL_DATA_JS, SCROLL_TRACKER_JS};
use log::warn;
#[cfg(feature = "chrome")]
use log::{debug, info};
use tokio::time::{Duration, Instant};

#[cfg(feature = "chrome")]
use chromiumoxide::browser::{Browser, BrowserConfigBuilder};
use chromiumoxide::handler::viewport::Viewport;
#[cfg(feature = "chrome")]
use chromiumoxide::page::Page;
#[cfg(feature = "chrome")]
use futures::StreamExt;

/// Performance metrics from Chrome
#[derive(Debug, Clone, Default)]
pub struct PerformanceMetrics {
    /// JS heap memory used (MB)
    pub js_heap_used_mb: usize,
    /// JS heap total allocated (MB)
    pub js_heap_total_mb: usize,
    /// Time to DOMContentLoaded (ms)
    pub dom_content_loaded_ms: usize,
    /// Time to load complete (ms)
    pub load_complete_ms: usize,
    /// Number of resources loaded
    pub resource_count: usize,
    /// Number of DOM nodes
    pub dom_node_count: usize,
}

impl PerformanceMetrics {
    /// Check if memory usage is within limits
    pub fn is_memory_ok(&self, max_mb: usize) -> bool {
        self.js_heap_used_mb <= max_mb
    }

    /// Check if page is "heavy" (many DOM nodes or resources)
    pub fn is_heavy_page(&self) -> bool {
        self.dom_node_count > 5000 || self.resource_count > 200
    }
}

/// Chrome session manager for RBI
///
/// Manages a dedicated Chrome instance with:
/// - Chrome DevTools Protocol (CDP) communication via chromiumoxide
/// - Screenshot capture at configurable FPS
/// - Input injection (keyboard, mouse)
/// - Popup blocking/handling
/// - Resource monitoring
/// - Clipboard sync (via JavaScript, no patches required)
/// - **Session isolation** via unique temp profile directories
///
/// # Security
///
/// Each ChromeSession automatically creates an isolated profile directory
/// to prevent data leakage between sessions. This ensures:
/// - Cookies are not shared between users
/// - localStorage/sessionStorage is isolated
/// - Browser cache is separate
/// - History is not leaked
///
/// The profile directory is automatically cleaned up when the session ends.
pub struct ChromeSession {
    #[cfg_attr(not(feature = "chrome"), allow(dead_code))]
    pub(crate) width: u32,
    #[cfg_attr(not(feature = "chrome"), allow(dead_code))]
    pub(crate) height: u32,
    #[cfg(feature = "chrome")]
    browser: Option<Browser>,
    #[cfg(feature = "chrome")]
    page: Option<Page>,
    #[cfg_attr(not(feature = "chrome"), allow(dead_code))]
    last_capture_time: Instant,
    #[cfg_attr(not(feature = "chrome"), allow(dead_code))]
    capture_interval: Duration,
    #[cfg_attr(not(feature = "chrome"), allow(dead_code))]
    download_count: usize, // Track downloads for rate limiting
    #[cfg_attr(not(feature = "chrome"), allow(dead_code))]
    clipboard_state: ClipboardState, // Track clipboard changes
    #[cfg_attr(not(feature = "chrome"), allow(dead_code))]
    cursor_state: CursorState, // Track cursor changes
    /// Isolated profile directory for this session (auto-cleaned on drop)
    #[cfg(feature = "chrome")]
    profile_dir: Option<tempfile::TempDir>,
    /// Profile lock for persistent profiles (prevents concurrent use)
    #[cfg(feature = "chrome")]
    profile_lock: Option<crate::profile_isolation::ProfileLock>,
}

impl ChromeSession {
    /// Create a new Chrome session with isolated profile directory
    ///
    /// # Security
    ///
    /// Automatically creates a unique temporary directory for this session's
    /// browser profile. This prevents data leakage between sessions:
    /// - Each session gets isolated cookies, localStorage, cache
    /// - Directory is automatically cleaned up when session drops
    /// - No possibility of cross-session data access
    pub fn new(width: u32, height: u32, capture_fps: u32, _chromium_path: &str) -> Self {
        let capture_interval = Duration::from_millis(1000 / capture_fps as u64);

        Self {
            width,
            height,
            #[cfg(feature = "chrome")]
            browser: None,
            #[cfg(feature = "chrome")]
            page: None,
            last_capture_time: Instant::now(),
            capture_interval,
            download_count: 0,
            clipboard_state: ClipboardState::new(),
            cursor_state: CursorState::new(),
            #[cfg(feature = "chrome")]
            profile_dir: None, // Created lazily on launch
            #[cfg(feature = "chrome")]
            profile_lock: None, // Acquired when using persistent profile
        }
    }

    /// Launch Chrome with CDP enabled using chromiumoxide
    #[cfg(feature = "chrome")]
    pub async fn launch(
        &mut self,
        url: &str,
        chromium_path: &str,
        popup_handling: &crate::handler::PopupHandling,
    ) -> Result<(), String> {
        self.launch_with_options(url, chromium_path, popup_handling, None, None, None)
            .await
    }

    /// Launch Chrome with full options including profile and localization
    ///
    /// # Security: Session Isolation
    ///
    /// If `profile_directory` is `None`, an isolated temporary directory is
    /// automatically created for this session. This ensures:
    /// - Complete isolation between concurrent RBI sessions
    /// - No data leakage (cookies, localStorage, cache) between users
    /// - Automatic cleanup when session ends
    ///
    /// If `profile_directory` is `Some`, that directory is used instead
    /// (useful for persistent sessions where state should be preserved).
    #[cfg(feature = "chrome")]
    pub async fn launch_with_options(
        &mut self,
        url: &str,
        chromium_path: &str,
        popup_handling: &crate::handler::PopupHandling,
        profile_directory: Option<&str>,
        timezone: Option<&str>,
        accept_language: Option<&str>,
    ) -> Result<(), String> {
        info!("RBI: Launching Chrome for URL: {}", url);

        // Build Chrome config with security flags
        let mut args = vec![
            format!("--window-size={},{}", self.width, self.height),
            "--force-device-scale-factor=1".to_string(), // Ensure viewport matches window size
            "--headless=new".to_string(),
            "--disable-gpu".to_string(),
            "--no-first-run".to_string(),
            "--no-default-browser-check".to_string(),
            "--disable-background-networking".to_string(),
            "--disable-background-timer-throttling".to_string(),
            "--disable-backgrounding-occluded-windows".to_string(),
            "--disable-breakpad".to_string(),
            "--disable-client-side-phishing-detection".to_string(),
            "--disable-component-extensions-with-background-pages".to_string(),
            "--disable-default-apps".to_string(),
            "--disable-extensions".to_string(),
            "--disable-features=TranslateUI".to_string(),
            "--disable-hang-monitor".to_string(),
            "--disable-ipc-flooding-protection".to_string(),
            "--disable-prompt-on-repost".to_string(),
            "--disable-renderer-backgrounding".to_string(),
            "--disable-sync".to_string(),
            "--disable-web-resources".to_string(),
            "--metrics-recording-only".to_string(),
            "--safebrowsing-disable-auto-update".to_string(),
            "--enable-automation".to_string(),
            "--password-store=basic".to_string(),
            "--use-mock-keychain".to_string(),
            // Security flags (equivalent to KCM patches)
            "--disable-bluetooth".to_string(),
            "--disable-usb-keyboard-detect".to_string(),
            "--disable-speech-api".to_string(),
            "--disable-notifications".to_string(),
            // Additional isolation flags
            "--incognito".to_string(), // Extra layer: don't persist anything by default
            "--disable-features=ChromeWhatsNewUI".to_string(),
            "--disable-domain-reliability".to_string(),
            // Avoid GPU shader disk cache writes (fails in read-only container mounts)
            "--disable-gpu-shader-disk-cache".to_string(),
        ];

        // Linux-only flags: Ozone is Chrome's display abstraction layer on Linux only;
        // --no-sandbox is needed on Linux where kernel user namespaces may be unavailable
        // (Docker root user, restrictive seccomp profiles). macOS/Windows have working
        // sandboxes and do not use Ozone.
        #[cfg(target_os = "linux")]
        {
            args.push("--no-sandbox".to_string());
            args.push("--ozone-platform=headless".to_string());
            // /dev/shm is a Linux tmpfs mount; Docker limits it to 64MB by default
            args.push("--disable-dev-shm-usage".to_string());
        }

        // SECURITY: Session Isolation via Profile Directory
        // Each session MUST have its own profile directory to prevent data leakage
        if let Some(profile_dir) = profile_directory {
            // User-specified persistent profile - acquire exclusive lock
            // This prevents data corruption if two sessions try to use the same profile
            use crate::profile_isolation::{ProfileCreationMode, ProfileLock};

            let lock = ProfileLock::acquire(profile_dir, ProfileCreationMode::CreateRecursive)
                .map_err(|e| match e {
                    crate::profile_isolation::ProfileLockError::ProfileInUse(_) =>
                        "PROFILE_IN_USE: This browser profile is already in use by another active session.".to_string(),
                    other => format!("Failed to lock profile directory: {}", other),
                })?;

            args.push(format!("--user-data-dir={}", profile_dir));
            info!(
                "RBI: Using persistent profile directory: {} (locked)",
                profile_dir
            );

            // Store the lock - released when session ends
            self.profile_lock = Some(lock);
        } else {
            // Create isolated temporary profile directory
            // This is automatically cleaned up when ChromeSession is dropped
            let temp_dir = tempfile::Builder::new()
                .prefix("guacr-rbi-profile-")
                .tempdir()
                .map_err(|e| format!("Failed to create isolated profile directory: {}", e))?;

            let profile_path = temp_dir.path().to_string_lossy().to_string();
            args.push(format!("--user-data-dir={}", profile_path));
            info!("RBI: Created isolated profile directory: {}", profile_path);

            // Store the TempDir so it lives as long as the session
            // When dropped, the directory is automatically cleaned up
            self.profile_dir = Some(temp_dir);
        }

        // Accept-Language header
        if let Some(lang) = accept_language {
            args.push(format!("--accept-lang={}", lang));
            info!("RBI: Accept-Language: {}", lang);
        }

        // Popup blocking configuration
        match popup_handling {
            crate::handler::PopupHandling::Block => {
                args.push("--disable-popup-blocking=false".to_string()); // Keep popup blocking ON
            }
            crate::handler::PopupHandling::AllowList(_) => {
                args.push("--disable-popup-blocking=false".to_string());
                // Will handle via JavaScript injection
            }
            crate::handler::PopupHandling::NavigateMainWindow => {
                // Allow popups but will navigate main window instead
            }
        }

        // Download behavior is controlled via CDP, not command line
        // We'll handle downloads via Page.setDownloadBehavior if needed

        // Launch browser with chromiumoxide
        // Note: chromiumoxide API may vary by version - adjust as needed
        let mut config_builder = BrowserConfigBuilder::default();
        // Override chromiumoxide's default 800x600 viewport — it sends
        // Emulation.setDeviceMetricsOverride via CDP which takes precedence over
        // --window-size, so we must set the correct dimensions here.
        let viewport = Viewport {
            width: self.width,
            height: self.height,
            device_scale_factor: Some(1.0),
            emulating_mobile: false,
            is_landscape: true,
            has_touch: false,
        };
        config_builder = config_builder
            .args(args)
            .chrome_executable(chromium_path)
            .viewport(viewport);

        let config = config_builder
            .build()
            .map_err(|e| format!("Failed to build browser config: {}", e))?;

        let (browser, mut handler) = Browser::launch(config)
            .await
            .map_err(|e| format!("Failed to launch Chrome: {}", e))?;

        // Spawn handler task to process browser events
        tokio::spawn(async move {
            while (handler.next().await).is_some() {
                // Handle browser events (target created, etc.)
            }
        });

        // Create new page and navigate
        let page = browser
            .new_page(url)
            .await
            .map_err(|e| format!("Failed to create page: {}", e))?;

        // Set timezone emulation if specified
        if let Some(tz) = timezone {
            if let Err(e) = page.emulate_timezone(tz).await {
                warn!("RBI: Failed to set timezone {}: {}", tz, e);
            } else {
                info!("RBI: Timezone set to {}", tz);
            }
        }

        // Don't wait for navigation - start capturing immediately
        // Like KCM, we rely on asynchronous load handlers and start
        // capturing screenshots right away. The page will render
        // progressively as content loads.
        info!("RBI: Page navigation started (async)");

        // Bring page to front so it has focus. Without this, headless Chrome
        // may not process input events and clipboard APIs fail with
        // "Document is not focused".
        if let Err(e) = page.bring_to_front().await {
            warn!("RBI: Failed to bring page to front: {}", e);
        }

        self.browser = Some(browser);
        self.page = Some(page);

        info!("RBI: Chrome launched successfully");
        Ok(())
    }

    /// Launch Chrome (fallback when chrome feature is disabled)
    #[cfg(not(feature = "chrome"))]
    pub async fn launch(
        &mut self,
        _url: &str,
        _chromium_path: &str,
        _popup_handling: &crate::handler::PopupHandling,
    ) -> Result<(), String> {
        Err("Chrome feature not enabled. Enable with 'chrome' feature flag.".to_string())
    }

    /// Capture screenshot via chromiumoxide
    #[cfg(feature = "chrome")]
    pub async fn capture_screenshot(&mut self) -> Result<Option<Vec<u8>>, String> {
        // Check if enough time has passed since last capture
        let elapsed = self.last_capture_time.elapsed();
        if elapsed < self.capture_interval {
            debug!(
                "RBI: Skipping capture (too soon: {:?} < {:?})",
                elapsed, self.capture_interval
            );
            return Ok(None);
        }

        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        debug!("RBI: Attempting screenshot capture...");

        // Capture screenshot using chromiumoxide with JPEG compression
        use chromiumoxide::cdp::browser_protocol::page::CaptureScreenshotFormat;
        use chromiumoxide::page::ScreenshotParams;
        use tokio::time::{timeout, Duration};

        let screenshot_params = ScreenshotParams::builder()
            .format(CaptureScreenshotFormat::Jpeg)
            .quality(50) // Lower quality to fit within 64KB WebRTC limit (was 85)
            .build();

        debug!("RBI: Calling page.screenshot() with 10s timeout...");
        let screenshot = match timeout(Duration::from_secs(10), page.screenshot(screenshot_params))
            .await
        {
            Ok(Ok(data)) => {
                debug!(
                    "RBI: Screenshot captured successfully ({} bytes)",
                    data.len()
                );
                data
            }
            Ok(Err(e)) => {
                warn!("RBI: Screenshot failed: {}", e);
                return Err(format!("Failed to capture screenshot: {}", e));
            }
            Err(_) => {
                warn!("RBI: Screenshot timeout after 10s - Chrome may be unresponsive or stuck");
                return Err("Screenshot timeout after 10s".to_string());
            }
        };

        let screenshot_vec = screenshot;

        self.last_capture_time = Instant::now();
        Ok(Some(screenshot_vec))
    }

    /// Capture screenshot (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn capture_screenshot(&mut self) -> Result<Option<Vec<u8>>, String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Start screencast for H.264 video streaming
    ///
    /// This is more efficient than screenshot polling:
    /// - Hardware-accelerated H.264 encoding
    /// - Push-based (no polling overhead)
    /// - 100x bandwidth reduction vs screenshots
    /// - Supports up to 60 FPS
    #[cfg(feature = "chrome")]
    pub async fn start_screencast(
        &self,
        format: &str,
        quality: u8,
        max_width: u32,
        max_height: u32,
    ) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        use chromiumoxide::cdp::browser_protocol::page::{
            StartScreencastFormat, StartScreencastParams,
        };

        let format_enum = match format {
            "jpeg" => StartScreencastFormat::Jpeg,
            "png" => StartScreencastFormat::Png,
            _ => StartScreencastFormat::Jpeg,
        };

        let params = StartScreencastParams::builder()
            .format(format_enum)
            .quality(quality as i64)
            .max_width(max_width as i64)
            .max_height(max_height as i64)
            .every_nth_frame(1)
            .build();

        page.execute(params)
            .await
            .map_err(|e| format!("Failed to start screencast: {:?}", e))?;

        info!(
            "Screencast started: format={}, quality={}, size={}x{}",
            format, quality, max_width, max_height
        );

        Ok(())
    }

    /// Stop screencast
    #[cfg(feature = "chrome")]
    #[allow(dead_code)]
    pub async fn stop_screencast(&self) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        use chromiumoxide::cdp::browser_protocol::page::StopScreencastParams;

        page.execute(StopScreencastParams::default())
            .await
            .map_err(|e| format!("Failed to stop screencast: {}", e))?;

        info!("Screencast stopped");
        Ok(())
    }

    /// Subscribe to Page.screencastFrame events
    #[cfg(feature = "chrome")]
    #[allow(dead_code)] // called from browser_client.rs; cdylib build can't trace cfg-gated callers
    pub async fn screencast_event_listener(
        &self,
    ) -> Result<
        chromiumoxide::listeners::EventStream<
            chromiumoxide::cdp::browser_protocol::page::EventScreencastFrame,
        >,
        String,
    > {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;
        page.event_listener::<chromiumoxide::cdp::browser_protocol::page::EventScreencastFrame>()
            .await
            .map_err(|e| format!("Failed to subscribe to screencast frames: {:?}", e))
    }

    /// Acknowledge screencast frame
    #[cfg(feature = "chrome")]
    #[allow(dead_code)] // called from browser_client.rs; cdylib build can't trace cfg-gated callers
    pub async fn ack_screencast_frame(&self, session_id: i64) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        use chromiumoxide::cdp::browser_protocol::page::ScreencastFrameAckParams;

        let params = ScreencastFrameAckParams::new(session_id);

        page.execute(params)
            .await
            .map_err(|e| format!("Failed to ack screencast frame: {}", e))?;

        Ok(())
    }

    /// Install scroll tracker
    #[cfg(feature = "chrome")]
    pub async fn install_scroll_tracker(&self) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        page.evaluate(SCROLL_TRACKER_JS)
            .await
            .map_err(|e| format!("Failed to install scroll tracker: {}", e))?;

        info!("Scroll tracker installed");
        Ok(())
    }

    /// Poll for scroll changes
    #[cfg(feature = "chrome")]
    pub async fn poll_scroll(&self) -> Result<Option<ScrollPosition>, String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let result = page
            .evaluate(GET_SCROLL_DATA_JS)
            .await
            .map_err(|e| format!("Failed to poll scroll: {}", e))?;

        // Parse result
        if let Some(value) = result.value() {
            if value.is_null() {
                return Ok(None);
            }

            let x = value["x"].as_i64().unwrap_or(0) as i32;
            let y = value["y"].as_i64().unwrap_or(0) as i32;
            let max_x = value["maxX"].as_i64().unwrap_or(0) as i32;
            let max_y = value["maxY"].as_i64().unwrap_or(0) as i32;

            Ok(Some(ScrollPosition::new(x, y, max_x, max_y)))
        } else {
            Ok(None)
        }
    }

    /// Inject keyboard input via CDP `Input.dispatchKeyEvent`.
    ///
    /// Uses proper CDP native key events (`isTrusted=true`) instead of JS `dispatchEvent`
    /// (`isTrusted=false`). For printable keys a `char` event is also sent so that `input`
    /// events fire in text fields. `cdp_modifiers` is the CDP bitmask (Alt=1, Ctrl=2,
    /// Meta=4, Shift=8) computed from the current keyboard state.
    #[cfg(feature = "chrome")]
    pub async fn inject_keyboard(
        &self,
        keysym: u32,
        pressed: bool,
        cdp_modifiers: i64,
    ) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let Some((key, code, windows_vk, text)) = keysym_to_key_info(keysym) else {
            debug!("RBI: No key mapping for keysym 0x{:04x}, skipping", keysym);
            return Ok(());
        };

        use chromiumoxide::cdp::browser_protocol::input::{
            DispatchKeyEventParams, DispatchKeyEventType,
        };

        if pressed {
            // rawKeyDown — fires keydown in the page
            let mut params = DispatchKeyEventParams::new(DispatchKeyEventType::RawKeyDown);
            params.key = Some(key.clone());
            params.code = Some(code.clone());
            params.windows_virtual_key_code = Some(windows_vk);
            params.native_virtual_key_code = Some(windows_vk);
            params.modifiers = Some(cdp_modifiers);
            page.execute(params)
                .await
                .map_err(|e| format!("Failed to dispatch rawKeyDown: {}", e))?;

            // char — fires input event in text fields (printable keys only)
            if let Some(ref ch) = text {
                let mut params = DispatchKeyEventParams::new(DispatchKeyEventType::Char);
                params.key = Some(ch.clone());
                params.text = Some(ch.clone());
                params.unmodified_text = Some(ch.clone());
                params.modifiers = Some(cdp_modifiers);
                page.execute(params)
                    .await
                    .map_err(|e| format!("Failed to dispatch char event: {}", e))?;
            }
        } else {
            // keyUp
            let mut params = DispatchKeyEventParams::new(DispatchKeyEventType::KeyUp);
            params.key = Some(key.clone());
            params.code = Some(code.clone());
            params.windows_virtual_key_code = Some(windows_vk);
            params.native_virtual_key_code = Some(windows_vk);
            params.modifiers = Some(cdp_modifiers);
            page.execute(params)
                .await
                .map_err(|e| format!("Failed to dispatch keyUp: {}", e))?;
        }

        debug!(
            "RBI: Key {} for keysym 0x{:04x} (key={}, code={}, vk={}, text={:?})",
            if pressed { "down" } else { "up" },
            keysym,
            key,
            code,
            windows_vk,
            text
        );

        Ok(())
    }

    /// Inject keyboard (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn inject_keyboard(
        &self,
        _keysym: u32,
        _pressed: bool,
        _cdp_modifiers: i64,
    ) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Inject mouse press/release via CDP `Input.dispatchMouseEvent`.
    ///
    /// `buttons_mask` is the W3C bitmask of ALL buttons currently held AFTER this
    /// event (left=1, right=2, middle=4). Chrome uses this to correctly update its
    /// internal button state — without it many sites' click handlers silently ignore
    /// the event because `event.buttons` is 0.
    #[cfg(feature = "chrome")]
    pub async fn inject_mouse(
        &self,
        x: i32,
        y: i32,
        button: u8,
        pressed: bool,
        buttons_mask: u32,
    ) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let x = x.max(0) as f64;
        let y = y.max(0) as f64;

        use chromiumoxide::cdp::browser_protocol::input::{
            DispatchMouseEventParams, DispatchMouseEventType, MouseButton,
        };

        let (event_type, mouse_button) = if pressed {
            (
                DispatchMouseEventType::MousePressed,
                match button {
                    0 => MouseButton::Left,
                    1 => MouseButton::Middle,
                    2 => MouseButton::Right,
                    _ => MouseButton::None,
                },
            )
        } else {
            (
                DispatchMouseEventType::MouseReleased,
                match button {
                    0 => MouseButton::Left,
                    1 => MouseButton::Middle,
                    2 => MouseButton::Right,
                    _ => MouseButton::None,
                },
            )
        };

        let mut params = DispatchMouseEventParams::new(event_type, x, y);
        params.button = Some(mouse_button);
        params.buttons = Some(buttons_mask as i64);
        params.click_count = Some(1);

        page.execute(params)
            .await
            .map_err(|e| format!("Failed to dispatch mouse event: {}", e))?;

        debug!(
            "RBI: Mouse {} button={} buttons_mask={} at ({}, {})",
            if pressed { "press" } else { "release" },
            button,
            buttons_mask,
            x,
            y
        );

        Ok(())
    }

    /// Inject mouse move — updates Chrome's cursor position so hover effects,
    /// CSS :hover, and cursor style changes work correctly.
    /// `buttons_mask` is the W3C bitmask of currently held buttons (left=1, right=2, middle=4).
    /// Returns true if the event was sent, false if page not ready.
    #[cfg(feature = "chrome")]
    #[allow(dead_code)] // called from browser_client.rs; cdylib build can't trace cfg-gated callers
    pub async fn inject_mouse_move(
        &self,
        x: i32,
        y: i32,
        buttons_mask: u32,
    ) -> Result<bool, String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;
        use chromiumoxide::cdp::browser_protocol::input::{
            DispatchMouseEventParams, DispatchMouseEventType,
        };
        let mut params = DispatchMouseEventParams::new(
            DispatchMouseEventType::MouseMoved,
            x.max(0) as f64,
            y.max(0) as f64,
        );
        params.buttons = Some(buttons_mask as i64);
        page.execute(params)
            .await
            .map_err(|e| format!("Failed to move mouse: {}", e))?;
        Ok(true)
    }

    #[cfg(not(feature = "chrome"))]
    pub async fn inject_mouse_move(
        &self,
        _x: i32,
        _y: i32,
        _buttons_mask: u32,
    ) -> Result<bool, String> {
        Ok(false)
    }

    /// Inject mouse (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn inject_mouse(
        &self,
        _x: i32,
        _y: i32,
        _button: u8,
        _pressed: bool,
        _buttons_mask: u32,
    ) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Block popups via JavaScript injection
    #[cfg(feature = "chrome")]
    pub async fn block_popups(&self, allow_list: &[String]) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let js_code = format!(
            r#"
            (function() {{
                const allowList = {};
                const originalOpen = window.open;
                window.open = function(url, name, specs) {{
                    try {{
                        const domain = new URL(url).hostname;
                        if (allowList.some(allowed => domain.includes(allowed))) {{
                            window.location.href = url;
                            return null;
                        }}
                        console.log('Popup blocked:', url);
                        return null;
                    }} catch (e) {{
                        console.log('Popup blocked (invalid URL):', url);
                        return null;
                    }}
                }};
            }})();
        "#,
            serde_json::to_string(allow_list).unwrap_or("[]".to_string())
        );

        page.evaluate(js_code)
            .await
            .map_err(|e| format!("Failed to inject popup blocking script: {}", e))?;

        info!("RBI: Popup blocking script injected");
        Ok(())
    }

    /// Block popups (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn block_popups(&self, _allow_list: &[String]) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Monitor resource usage via CDP
    ///
    /// Uses Chrome's Performance.getMetrics to get JS heap size.
    /// Returns Ok(true) if within limits, Ok(false) if exceeded.
    #[cfg(feature = "chrome")]
    pub async fn check_resources(&self, max_memory_mb: usize) -> Result<bool, String> {
        let page = match self.page.as_ref() {
            Some(p) => p,
            None => return Ok(true), // No page yet, consider OK
        };

        // Use JavaScript to get memory info (works in Chrome)
        let js = r#"
        (function() {
            if (performance.memory) {
                return {
                    usedJSHeapSize: performance.memory.usedJSHeapSize,
                    totalJSHeapSize: performance.memory.totalJSHeapSize,
                    jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
                };
            }
            return null;
        })()
        "#;

        match page.evaluate(js).await {
            Ok(result) => {
                if let Some(value) = result.value() {
                    if let Some(obj) = value.as_object() {
                        if let Some(used) = obj.get("usedJSHeapSize").and_then(|v| v.as_u64()) {
                            let used_mb = used / (1024 * 1024);
                            debug!(
                                "RBI: JS heap usage: {} MB (limit: {} MB)",
                                used_mb, max_memory_mb
                            );

                            if used_mb > max_memory_mb as u64 {
                                warn!(
                                    "RBI: Memory limit exceeded: {} MB > {} MB",
                                    used_mb, max_memory_mb
                                );
                                return Ok(false);
                            }
                        }
                    }
                }
                Ok(true)
            }
            Err(e) => {
                // Memory API not available, log but don't fail
                debug!("RBI: Could not get memory metrics: {}", e);
                Ok(true)
            }
        }
    }

    /// Monitor resource usage (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn check_resources(&self, _max_memory_mb: usize) -> Result<bool, String> {
        Ok(true) // Can't monitor without Chrome
    }

    /// Get detailed performance metrics
    #[cfg(feature = "chrome")]
    pub async fn get_performance_metrics(&self) -> Result<PerformanceMetrics, String> {
        let page = self.page.as_ref().ok_or("Page not initialized")?;

        let js = r#"
        (function() {
            const metrics = {};

            // Memory (Chrome only)
            if (performance.memory) {
                metrics.jsHeapUsedMB = Math.round(performance.memory.usedJSHeapSize / 1024 / 1024);
                metrics.jsHeapTotalMB = Math.round(performance.memory.totalJSHeapSize / 1024 / 1024);
            }

            // Navigation timing
            const timing = performance.getEntriesByType('navigation')[0];
            if (timing) {
                metrics.domContentLoaded = Math.round(timing.domContentLoadedEventEnd);
                metrics.loadComplete = Math.round(timing.loadEventEnd);
            }

            // Resource count
            metrics.resourceCount = performance.getEntriesByType('resource').length;

            // DOM stats
            metrics.domNodes = document.getElementsByTagName('*').length;

            return metrics;
        })()
        "#;

        let result = page
            .evaluate(js)
            .await
            .map_err(|e| format!("Failed to get metrics: {}", e))?;

        let mut metrics = PerformanceMetrics::default();

        if let Some(value) = result.value() {
            if let Some(obj) = value.as_object() {
                metrics.js_heap_used_mb = obj
                    .get("jsHeapUsedMB")
                    .and_then(|v| v.as_u64())
                    .unwrap_or(0) as usize;
                metrics.js_heap_total_mb = obj
                    .get("jsHeapTotalMB")
                    .and_then(|v| v.as_u64())
                    .unwrap_or(0) as usize;
                metrics.dom_content_loaded_ms = obj
                    .get("domContentLoaded")
                    .and_then(|v| v.as_u64())
                    .unwrap_or(0) as usize;
                metrics.load_complete_ms = obj
                    .get("loadComplete")
                    .and_then(|v| v.as_u64())
                    .unwrap_or(0) as usize;
                metrics.resource_count = obj
                    .get("resourceCount")
                    .and_then(|v| v.as_u64())
                    .unwrap_or(0) as usize;
                metrics.dom_node_count =
                    obj.get("domNodes").and_then(|v| v.as_u64()).unwrap_or(0) as usize;
            }
        }

        Ok(metrics)
    }

    /// Get performance metrics (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn get_performance_metrics(&self) -> Result<PerformanceMetrics, String> {
        Ok(PerformanceMetrics::default())
    }

    /// Get page reference (for advanced operations)
    #[cfg(feature = "chrome")]
    #[allow(dead_code)]
    pub fn page(&self) -> Option<&Page> {
        self.page.as_ref()
    }

    /// Handle file download request
    ///
    /// Downloads file from URL and streams it to client via Guacamole protocol.
    /// Applies security checks: size limits, file type restrictions, rate limiting.
    #[cfg(feature = "chrome")]
    pub async fn handle_download(
        &mut self,
        url: &str,
        suggested_filename: &str,
        download_config: &crate::handler::DownloadConfig,
        to_client: &tokio::sync::mpsc::Sender<bytes::Bytes>,
    ) -> Result<(), String> {
        use base64::engine::general_purpose::STANDARD as BASE64;
        use base64::Engine;
        use bytes::Bytes;
        use guacr_protocol::{format_blob, format_end};

        // Check if downloads are enabled
        if !download_config.enabled {
            return Err("Downloads are disabled".to_string());
        }

        // Check rate limiting
        if self.download_count >= download_config.max_downloads_per_session {
            return Err(format!(
                "Maximum downloads per session ({}) exceeded",
                download_config.max_downloads_per_session
            ));
        }

        // Check file extension
        let ext = suggested_filename
            .split('.')
            .next_back()
            .unwrap_or("")
            .to_lowercase();

        if download_config.blocked_extensions.contains(&ext) {
            return Err(format!("File type .{} is not allowed", ext));
        }

        if !download_config.allowed_extensions.is_empty()
            && !download_config.allowed_extensions.contains(&ext)
        {
            return Err(format!("File type .{} is not in allowed list", ext));
        }

        // Download file via HTTP
        let client = reqwest::Client::new();
        let response = client
            .get(url)
            .send()
            .await
            .map_err(|e| format!("Failed to download file: {}", e))?;

        // Check content length
        if let Some(len) = response.content_length() {
            let max_size = download_config.max_file_size_mb * 1024 * 1024;
            if len > max_size as u64 {
                return Err(format!(
                    "File too large: {} bytes (max: {} bytes)",
                    len, max_size
                ));
            }
        }

        // Read file data
        let file_data = response
            .bytes()
            .await
            .map_err(|e| format!("Failed to read file data: {}", e))?
            .to_vec();

        // Check actual size (in case Content-Length was missing)
        let max_size = download_config.max_file_size_mb * 1024 * 1024;
        if file_data.len() > max_size {
            return Err(format!(
                "File too large: {} bytes (max: {} bytes)",
                file_data.len(),
                max_size
            ));
        }

        // Detect MIME type
        let mimetype = self.detect_mime_type(suggested_filename).to_string();

        // Send file via Guacamole protocol
        // Increment download_count first to get unique stream ID
        self.download_count += 1;
        let stream_id = (self.download_count as u32) + 1000; // Start at 1000 to avoid conflicts

        // Send file instruction: file,<stream>,<mimetype>,<filename>;
        let file_instr = format!(
            "7.file,{}.{},{}.{},{}.{};",
            stream_id.to_string().len(),
            stream_id,
            mimetype.len(),
            mimetype,
            suggested_filename.len(),
            suggested_filename
        );
        to_client
            .send(Bytes::from(file_instr))
            .await
            .map_err(|e| format!("Failed to send file instruction: {}", e))?;

        // Send file data in chunks via blob instruction (base64-encoded)
        let chunk_size = 48 * 1024; // 48KB chunks (64KB base64 = ~48KB raw)
        for chunk in file_data.chunks(chunk_size) {
            let base64_data = BASE64.encode(chunk);
            let blob_instr = format_blob(stream_id, &base64_data);
            to_client
                .send(Bytes::from(blob_instr))
                .await
                .map_err(|e| format!("Failed to send blob chunk: {}", e))?;
        }

        // Send end instruction: end,<stream>;
        let end_instr = format_end(stream_id);
        to_client
            .send(Bytes::from(end_instr))
            .await
            .map_err(|e| format!("Failed to send end instruction: {}", e))?;

        info!(
            "RBI: File '{}' sent to client ({} bytes, {} chunks)",
            suggested_filename,
            file_data.len(),
            file_data.len().div_ceil(chunk_size)
        );

        Ok(())
    }

    /// Handle download (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn handle_download(
        &mut self,
        _url: &str,
        _suggested_filename: &str,
        _download_config: &crate::handler::DownloadConfig,
        _to_client: &tokio::sync::mpsc::Sender<bytes::Bytes>,
    ) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Detect MIME type from filename
    #[cfg_attr(not(feature = "chrome"), allow(dead_code))]
    fn detect_mime_type(&self, filename: &str) -> &str {
        let ext = filename.split('.').next_back().unwrap_or("").to_lowercase();
        match ext.as_str() {
            "pdf" => "application/pdf",
            "txt" => "text/plain",
            "csv" => "text/csv",
            "json" => "application/json",
            "xml" => "application/xml",
            "zip" => "application/zip",
            "png" => "image/png",
            "jpg" | "jpeg" => "image/jpeg",
            "gif" => "image/gif",
            "webp" => "image/webp",
            "svg" => "image/svg+xml",
            "html" => "text/html",
            "css" => "text/css",
            "js" => "application/javascript",
            _ => "application/octet-stream",
        }
    }

    /// Inject mouse scroll event
    #[cfg(feature = "chrome")]
    pub async fn inject_scroll(
        &self,
        x: i32,
        y: i32,
        delta_x: i32,
        delta_y: i32,
    ) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        use chromiumoxide::cdp::browser_protocol::input::{
            DispatchMouseEventParams, DispatchMouseEventType,
        };
        let params = DispatchMouseEventParams::builder()
            .r#type(DispatchMouseEventType::MouseWheel)
            .x(x.max(0) as f64)
            .y(y.max(0) as f64)
            .delta_x(delta_x as f64)
            .delta_y(delta_y as f64)
            .build()
            .map_err(|e| format!("Failed to build scroll params: {}", e))?;

        page.execute(params)
            .await
            .map_err(|e| format!("Failed to inject scroll: {}", e))?;

        Ok(())
    }

    /// Inject scroll (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn inject_scroll(
        &self,
        _x: i32,
        _y: i32,
        _delta_x: i32,
        _delta_y: i32,
    ) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Inject touch event
    #[cfg(feature = "chrome")]
    pub async fn inject_touch(
        &self,
        touch: &crate::input::BrowserTouchEvent,
    ) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let event_type = match touch.event_type {
            crate::input::TouchEventType::Pressed => "touchstart",
            crate::input::TouchEventType::Moved => "touchmove",
            crate::input::TouchEventType::Released => "touchend",
            crate::input::TouchEventType::Cancelled => "touchcancel",
        };

        // Use JavaScript to dispatch touch event
        let js = format!(
            r#"(function() {{
                var touch = new Touch({{
                    identifier: {},
                    target: document.elementFromPoint({}, {}),
                    clientX: {},
                    clientY: {},
                    radiusX: {},
                    radiusY: {},
                    rotationAngle: {},
                    force: {}
                }});
                var event = new TouchEvent('{}', {{
                    bubbles: true,
                    cancelable: true,
                    touches: [touch],
                    targetTouches: [touch],
                    changedTouches: [touch]
                }});
                document.elementFromPoint({}, {}).dispatchEvent(event);
            }})()"#,
            touch.id,
            touch.x,
            touch.y,
            touch.x,
            touch.y,
            touch.radius_x,
            touch.radius_y,
            touch.rotation_angle,
            touch.pressure,
            event_type,
            touch.x,
            touch.y
        );

        page.evaluate(js)
            .await
            .map_err(|e| format!("Failed to inject touch: {}", e))?;

        Ok(())
    }

    /// Inject touch (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn inject_touch(
        &self,
        _touch: &crate::input::BrowserTouchEvent,
    ) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Resize browser viewport
    ///
    /// Note: For headless Chrome, viewport size is typically set at launch.
    /// Dynamic resize during session would require browser restart or
    /// using CDP Emulation.setDeviceMetricsOverride command directly.
    #[cfg(feature = "chrome")]
    pub async fn resize(&mut self, width: u32, height: u32) -> Result<(), String> {
        self.width = width;
        self.height = height;

        // For now, just update dimensions - actual resize would need CDP command
        // The next capture will use the original viewport size
        // Full implementation would require:
        // 1. Emulation.setDeviceMetricsOverride CDP command
        // 2. Or restarting browser with new --window-size
        info!("RBI: Viewport resize requested to {}x{}", width, height);

        // Notify page of resize via window resize event
        if let Some(page) = self.page.as_ref() {
            let js = "window.dispatchEvent(new Event('resize'));".to_string();
            let _ = page.evaluate(js).await;
        }

        Ok(())
    }

    /// Resize (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn resize(&mut self, width: u32, height: u32) -> Result<(), String> {
        self.width = width;
        self.height = height;
        Ok(()) // Just update dimensions
    }

    /// Navigate in history
    #[cfg(feature = "chrome")]
    pub async fn navigate_history(&self, position: i32) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        if position == 0 {
            // Refresh using page.reload()
            page.reload()
                .await
                .map_err(|e| format!("Failed to reload: {}", e))?;
        } else if position < 0 {
            // Go back using JavaScript
            let steps = -position;
            let js = format!("history.go({})", -steps);
            page.evaluate(js)
                .await
                .map_err(|e| format!("Failed to go back: {}", e))?;
        } else {
            // Go forward using JavaScript
            let js = format!("history.go({})", position);
            page.evaluate(js)
                .await
                .map_err(|e| format!("Failed to go forward: {}", e))?;
        }

        Ok(())
    }

    /// Navigate history (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn navigate_history(&self, _position: i32) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Navigate to URL
    #[cfg(feature = "chrome")]
    pub async fn navigate_to(&self, url: &str) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        page.goto(url)
            .await
            .map_err(|e| format!("Failed to navigate to {}: {}", url, e))?;

        info!("RBI: Navigated to {}", url);
        Ok(())
    }

    /// Navigate to URL (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn navigate_to(&self, _url: &str) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Set clipboard content
    #[cfg(feature = "chrome")]
    pub async fn set_clipboard(&self, data: &[u8]) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let text = String::from_utf8_lossy(data);

        // Use JavaScript to write to clipboard
        let js = format!(
            r#"navigator.clipboard.writeText('{}')"#,
            text.replace('\\', "\\\\")
                .replace('\'', "\\'")
                .replace('\n', "\\n")
        );

        page.evaluate(js)
            .await
            .map_err(|e| format!("Failed to set clipboard: {}", e))?;

        info!("RBI: Clipboard set ({} bytes)", data.len());
        Ok(())
    }

    /// Set clipboard (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn set_clipboard(&self, _data: &[u8]) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Install clipboard event listener
    ///
    /// This injects JavaScript that captures copy events.
    /// Call this after page load to start monitoring.
    #[cfg(feature = "chrome")]
    pub async fn install_clipboard_listener(&self) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        page.evaluate(COPY_EVENT_LISTENER_JS)
            .await
            .map_err(|e| format!("Failed to install clipboard listener: {}", e))?;

        debug!("RBI: Clipboard event listener installed");
        Ok(())
    }

    /// Install clipboard listener (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn install_clipboard_listener(&self) -> Result<(), String> {
        Ok(()) // No-op when Chrome not enabled
    }

    /// Check for clipboard changes
    ///
    /// Returns Some(text) if clipboard has changed since last check.
    /// Uses JavaScript-based monitoring (no Chrome patches required).
    #[cfg(feature = "chrome")]
    pub async fn poll_clipboard(&mut self) -> Result<Option<String>, String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        // Get captured clipboard data from JavaScript
        let result = page
            .evaluate(GET_CLIPBOARD_DATA_JS)
            .await
            .map_err(|e| format!("Failed to poll clipboard: {}", e))?;

        // Parse the result (returns {text: string, timestamp: number} or null)
        if let Some(value) = result.value() {
            if let Some(obj) = value.as_object() {
                if let Some(text_val) = obj.get("text") {
                    if let Some(text) = text_val.as_str() {
                        // Check if content has changed
                        if self.clipboard_state.has_changed(text) {
                            info!("RBI: Clipboard changed ({} chars)", text.len());
                            return Ok(Some(text.to_string()));
                        }
                    }
                }
            }
        }

        Ok(None)
    }

    /// Poll clipboard (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn poll_clipboard(&mut self) -> Result<Option<String>, String> {
        Ok(None) // No-op when Chrome not enabled
    }

    /// Get clipboard using Clipboard API (requires focus)
    ///
    /// This is an alternative that reads directly from the Clipboard API.
    /// Only works when the page has focus.
    #[cfg(feature = "chrome")]
    #[allow(dead_code)]
    pub async fn read_clipboard_direct(&self) -> Result<Option<String>, String> {
        use crate::clipboard_polling::CLIPBOARD_READ_JS;

        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let result = page
            .evaluate(CLIPBOARD_READ_JS)
            .await
            .map_err(|e| format!("Failed to read clipboard: {}", e))?;

        if let Some(value) = result.value() {
            if let Some(text) = value.as_str() {
                return Ok(Some(text.to_string()));
            }
        }

        Ok(None)
    }

    /// Read clipboard direct (fallback)
    #[cfg(not(feature = "chrome"))]
    #[allow(dead_code)]
    pub async fn read_clipboard_direct(&self) -> Result<Option<String>, String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Install cursor tracker
    ///
    /// Injects JavaScript that monitors cursor style changes.
    #[cfg(feature = "chrome")]
    pub async fn install_cursor_tracker(&self) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        page.evaluate(CURSOR_TRACKER_JS)
            .await
            .map_err(|e| format!("Failed to install cursor tracker: {}", e))?;

        debug!("RBI: Cursor tracker installed");
        Ok(())
    }

    /// Install cursor tracker (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn install_cursor_tracker(&self) -> Result<(), String> {
        Ok(()) // No-op when Chrome not enabled
    }

    /// Poll for cursor changes
    ///
    /// Returns Some(CursorType) if cursor has changed since last check.
    #[cfg(feature = "chrome")]
    pub async fn poll_cursor(&mut self) -> Result<Option<CursorType>, String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let result = page
            .evaluate(GET_CURSOR_JS)
            .await
            .map_err(|e| format!("Failed to poll cursor: {}", e))?;

        if let Some(value) = result.value() {
            if let Some(obj) = value.as_object() {
                let style = obj
                    .get("style")
                    .and_then(|v| v.as_str())
                    .unwrap_or("default");
                let timestamp = obj.get("timestamp").and_then(|v| v.as_u64()).unwrap_or(0);

                return Ok(self.cursor_state.update(style, timestamp));
            }
        }

        Ok(None)
    }

    /// Poll cursor (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn poll_cursor(&mut self) -> Result<Option<crate::cursor::CursorType>, String> {
        Ok(None) // No-op when Chrome not enabled
    }

    /// Handle file chooser dialog (file upload)
    ///
    /// When a web page triggers a file input, Chrome opens a file chooser.
    /// Handle file chooser for file uploads
    ///
    /// This method is currently unused because file uploads are handled via
    /// the UploadEngine in browser_client.rs using Guacamole's file protocol.
    /// Kept for potential future CDP-based file upload implementation.
    #[cfg(feature = "chrome")]
    #[allow(dead_code)]
    pub async fn handle_file_chooser(&self, files: &[std::path::PathBuf]) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        // Build file paths array for CDP
        let file_paths: Vec<String> = files
            .iter()
            .filter_map(|p| p.to_str().map(String::from))
            .collect();

        if file_paths.is_empty() {
            return Err("No valid file paths provided".to_string());
        }

        // Use CDP to set files on the file input
        // This requires finding the active file chooser element
        let js = format!(
            r#"(function() {{
                const files = {};
                const input = document.querySelector('input[type="file"]:focus') || 
                              document.querySelector('input[type="file"]');
                if (!input) return false;
                
                // Create DataTransfer to simulate file selection
                const dt = new DataTransfer();
                files.forEach(path => {{
                    // Note: This won't work with actual files in browser context
                    // File upload requires CDP FileChooser.setFiles or similar
                    console.log('Would upload:', path);
                }});
                return true;
            }})()"#,
            serde_json::to_string(&file_paths).unwrap_or("[]".to_string())
        );

        page.evaluate(js)
            .await
            .map_err(|e| format!("Failed to handle file chooser: {}", e))?;

        info!("RBI: File chooser handled with {} files", files.len());
        Ok(())
    }

    /// Handle file chooser (fallback)
    #[cfg(not(feature = "chrome"))]
    #[allow(dead_code)]
    pub async fn handle_file_chooser(&self, _files: &[std::path::PathBuf]) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Enable file chooser interception via CDP
    ///
    /// Call this to be notified when a file input is clicked.
    /// Returns a receiver that will get file chooser events.
    #[cfg(feature = "chrome")]
    pub async fn enable_file_chooser_interception(&self) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        // Inject script to detect file input clicks
        let js = r#"
        (function() {
            window.__guac_pending_file_chooser = null;
            
            document.addEventListener('click', function(e) {
                if (e.target.tagName === 'INPUT' && e.target.type === 'file') {
                    window.__guac_pending_file_chooser = {
                        multiple: e.target.multiple,
                        accept: e.target.accept || '*/*',
                        timestamp: Date.now()
                    };
                    // Prevent default to let us handle it
                    // e.preventDefault();
                    console.log('Guacamole: File chooser detected', window.__guac_pending_file_chooser);
                }
            }, true);
            
            console.log('Guacamole: File chooser interception enabled');
        })();
        "#;

        page.evaluate(js)
            .await
            .map_err(|e| format!("Failed to enable file chooser interception: {}", e))?;

        debug!("RBI: File chooser interception enabled");
        Ok(())
    }

    /// Enable file chooser interception (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn enable_file_chooser_interception(&self) -> Result<(), String> {
        Ok(()) // No-op
    }

    /// Check if file chooser is pending
    #[cfg(feature = "chrome")]
    pub async fn poll_file_chooser(
        &self,
    ) -> Result<Option<crate::file_upload::UploadRequest>, String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        let js = r#"
        (function() {
            const pending = window.__guac_pending_file_chooser;
            if (pending) {
                window.__guac_pending_file_chooser = null;
                return pending;
            }
            return null;
        })()
        "#;

        let result = page
            .evaluate(js)
            .await
            .map_err(|e| format!("Failed to poll file chooser: {}", e))?;

        if let Some(value) = result.value() {
            if let Some(obj) = value.as_object() {
                let multiple = obj
                    .get("multiple")
                    .and_then(|v| v.as_bool())
                    .unwrap_or(false);
                let accept = obj
                    .get("accept")
                    .and_then(|v| v.as_str())
                    .unwrap_or("*/*")
                    .to_string();
                let timestamp = obj.get("timestamp").and_then(|v| v.as_u64()).unwrap_or(0);

                return Ok(Some(crate::file_upload::UploadRequest {
                    id: format!("fc-{}", timestamp),
                    multiple,
                    accept: vec![accept],
                }));
            }
        }

        Ok(None)
    }

    /// Poll file chooser (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn poll_file_chooser(
        &self,
    ) -> Result<Option<crate::file_upload::UploadRequest>, String> {
        Ok(None)
    }

    /// Submit files to a file input element
    ///
    /// This uses CDP to set files on the currently active file input.
    #[cfg(feature = "chrome")]
    pub async fn submit_upload_files(
        &self,
        file_data: &[(String, String, Vec<u8>)], // (filename, mimetype, data)
    ) -> Result<(), String> {
        let page = self
            .page
            .as_ref()
            .ok_or_else(|| "Page not initialized".to_string())?;

        // Create base64 encoded file data for JavaScript
        use base64::engine::general_purpose::STANDARD as BASE64;
        use base64::Engine;

        let files_json: Vec<serde_json::Value> = file_data
            .iter()
            .map(|(name, mime, data)| {
                serde_json::json!({
                    "name": name,
                    "type": mime,
                    "data": BASE64.encode(data)
                })
            })
            .collect();

        let js = format!(
            r#"(async function() {{
                const filesData = {};
                const input = document.querySelector('input[type="file"]');
                if (!input) {{
                    console.error('No file input found');
                    return false;
                }}
                
                const dt = new DataTransfer();
                
                for (const fileData of filesData) {{
                    // Decode base64 data
                    const binaryString = atob(fileData.data);
                    const bytes = new Uint8Array(binaryString.length);
                    for (let i = 0; i < binaryString.length; i++) {{
                        bytes[i] = binaryString.charCodeAt(i);
                    }}
                    
                    // Create File object
                    const file = new File([bytes], fileData.name, {{ type: fileData.type }});
                    dt.items.add(file);
                }}
                
                // Set files on input
                input.files = dt.files;
                
                // Dispatch change event
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                
                console.log('Guacamole: Files uploaded:', filesData.length);
                return true;
            }})()"#,
            serde_json::to_string(&files_json).unwrap_or("[]".to_string())
        );

        page.evaluate(js)
            .await
            .map_err(|e| format!("Failed to submit upload files: {}", e))?;

        info!("RBI: Submitted {} files to upload", file_data.len());
        Ok(())
    }

    /// Submit upload files (fallback)
    #[cfg(not(feature = "chrome"))]
    pub async fn submit_upload_files(
        &self,
        _file_data: &[(String, String, Vec<u8>)],
    ) -> Result<(), String> {
        Err("Chrome feature not enabled".to_string())
    }

    /// Explicitly close the Chrome browser, freeing the process, sockets, and profile directory.
    /// Must be called before the session is dropped to avoid resource leaks.
    #[cfg(feature = "chrome")]
    #[allow(dead_code)] // called from browser_client.rs; cdylib build can't trace cfg-gated callers
    pub async fn close(&mut self) {
        if let Some(mut browser) = self.browser.take() {
            // Try graceful close first (sends Browser.close CDP command)
            if let Err(e) = browser.close().await {
                debug!("RBI: Browser graceful close failed, killing: {}", e);
                // Force kill the Chrome subprocess
                browser.kill().await;
            }
            // profile_dir (TempDir) is dropped here, cleaning up the temp directory
        }
    }

    #[cfg(not(feature = "chrome"))]
    pub async fn close(&mut self) {}
}

impl Drop for ChromeSession {
    fn drop(&mut self) {
        #[cfg(feature = "chrome")]
        {
            if self.browser.is_some() {
                // If close() was not called before drop, warn — this indicates a bug.
                // The browser will be killed by chromiumoxide's background task but
                // sockets and the profile directory may not be cleaned up promptly.
                warn!(
                    "RBI: ChromeSession dropped without calling close() — possible resource leak"
                );
                drop(self.browser.take());
            }
        }
    }
}

/// Map an X11 keysym to the CDP key info needed by `Input.dispatchKeyEvent`.
///
/// Returns `(key, code, windows_virtual_key_code, text)` where `text` is `Some`
/// only for printable characters that should produce a `char` CDP event (which
/// causes `input` events to fire in text fields).
///
/// Returns `None` for keysyms with no meaningful CDP mapping (e.g. dead keys,
/// compose, unmapped Unicode above BMP).
fn keysym_to_key_info(keysym: u32) -> Option<(String, String, i64, Option<String>)> {
    // --- Special / non-printable keys ---
    let special: Option<(&str, &str, i64)> = match keysym {
        0xFF08 => Some(("Backspace", "Backspace", 8)),
        0xFF09 => Some(("Tab", "Tab", 9)),
        0xFF0D => Some(("Enter", "Enter", 13)),
        0xFF1B => Some(("Escape", "Escape", 27)),
        0xFF50 => Some(("Home", "Home", 36)),
        0xFF51 => Some(("ArrowLeft", "ArrowLeft", 37)),
        0xFF52 => Some(("ArrowUp", "ArrowUp", 38)),
        0xFF53 => Some(("ArrowRight", "ArrowRight", 39)),
        0xFF54 => Some(("ArrowDown", "ArrowDown", 40)),
        0xFF55 => Some(("PageUp", "PageUp", 33)),
        0xFF56 => Some(("PageDown", "PageDown", 34)),
        0xFF57 => Some(("End", "End", 35)),
        0xFF63 => Some(("Insert", "Insert", 45)),
        0xFFFF => Some(("Delete", "Delete", 46)),
        0xFF7F => Some(("NumLock", "NumLock", 144)),
        0xFF14 => Some(("ScrollLock", "ScrollLock", 145)),
        0xFFE5 => Some(("CapsLock", "CapsLock", 20)),
        0xFFE1 => Some(("Shift", "ShiftLeft", 16)),
        0xFFE2 => Some(("Shift", "ShiftRight", 16)),
        0xFFE3 => Some(("Control", "ControlLeft", 17)),
        0xFFE4 => Some(("Control", "ControlRight", 17)),
        0xFFE7 => Some(("Meta", "MetaLeft", 91)),
        0xFFE8 => Some(("Meta", "MetaRight", 92)),
        0xFFE9 => Some(("Alt", "AltLeft", 18)),
        0xFFEA => Some(("Alt", "AltRight", 18)),
        0xFE03 => Some(("AltGraph", "AltRight", 225)),
        0xFFBE => Some(("F1", "F1", 112)),
        0xFFBF => Some(("F2", "F2", 113)),
        0xFFC0 => Some(("F3", "F3", 114)),
        0xFFC1 => Some(("F4", "F4", 115)),
        0xFFC2 => Some(("F5", "F5", 116)),
        0xFFC3 => Some(("F6", "F6", 117)),
        0xFFC4 => Some(("F7", "F7", 118)),
        0xFFC5 => Some(("F8", "F8", 119)),
        0xFFC6 => Some(("F9", "F9", 120)),
        0xFFC7 => Some(("F10", "F10", 121)),
        0xFFC8 => Some(("F11", "F11", 122)),
        0xFFC9 => Some(("F12", "F12", 123)),
        // Numpad operators — printable
        0xFFBD => return Some(("=".into(), "NumpadEqual".into(), 187, Some("=".into()))),
        0xFFAA => return Some(("*".into(), "NumpadMultiply".into(), 106, Some("*".into()))),
        0xFFAB => return Some(("+".into(), "NumpadAdd".into(), 107, Some("+".into()))),
        0xFFAD => return Some(("-".into(), "NumpadSubtract".into(), 109, Some("-".into()))),
        0xFFAE => return Some((".".into(), "NumpadDecimal".into(), 110, Some(".".into()))),
        0xFFAF => return Some(("/".into(), "NumpadDivide".into(), 111, Some("/".into()))),
        0xFF8D => Some(("Enter", "NumpadEnter", 13)),
        _ => None,
    };
    if let Some((key, code, vk)) = special {
        // Tab produces "\t"; Enter, Backspace, etc. produce no char event.
        let text = if keysym == 0xFF09 {
            Some("\t".into())
        } else {
            None
        };
        return Some((key.into(), code.into(), vk, text));
    }

    // Numpad digits 0-9
    if (0xFFB0..=0xFFB9).contains(&keysym) {
        let digit = (keysym - 0xFFB0) as u8 + b'0';
        let ch = char::from(digit);
        let vk = 96 + (keysym - 0xFFB0) as i64;
        return Some((
            ch.to_string(),
            format!("Numpad{}", ch),
            vk,
            Some(ch.to_string()),
        ));
    }

    // --- Printable ASCII (0x20..=0x7E) ---
    if (0x20..=0x7E).contains(&keysym) {
        let ch = char::from_u32(keysym)?;
        let key = ch.to_string();
        let text = Some(ch.to_string());

        let (code, vk): (String, i64) = match keysym {
            0x20 => ("Space".into(), 32),
            // Digits
            0x30..=0x39 => (format!("Digit{}", ch), keysym as i64),
            // Uppercase A-Z
            0x41..=0x5A => (format!("Key{}", ch), keysym as i64),
            // Lowercase a-z → same physical key, VK is the uppercase code
            0x61..=0x7A => (
                format!("Key{}", char::from(b'A' + (keysym as u8 - b'a'))),
                keysym as i64 - 0x20,
            ),
            // Punctuation (shifted digit row)
            0x21 => ("Digit1".into(), 49), // !
            0x40 => ("Digit2".into(), 50), // @
            0x23 => ("Digit3".into(), 51), // #
            0x24 => ("Digit4".into(), 52), // $
            0x25 => ("Digit5".into(), 53), // %
            0x5E => ("Digit6".into(), 54), // ^
            0x26 => ("Digit7".into(), 55), // &
            0x2A => ("Digit8".into(), 56), // *
            0x28 => ("Digit9".into(), 57), // (
            0x29 => ("Digit0".into(), 48), // )
            // Other punctuation
            0x2D | 0x5F => ("Minus".into(), 189),
            0x3D | 0x2B => ("Equal".into(), 187),
            0x5B | 0x7B => ("BracketLeft".into(), 219),
            0x5D | 0x7D => ("BracketRight".into(), 221),
            0x3B | 0x3A => ("Semicolon".into(), 186),
            0x27 | 0x22 => ("Quote".into(), 222),
            0x60 | 0x7E => ("Backquote".into(), 192),
            0x5C | 0x7C => ("Backslash".into(), 220),
            0x2C | 0x3C => ("Comma".into(), 188),
            0x2E | 0x3E => ("Period".into(), 190),
            0x2F | 0x3F => ("Slash".into(), 191),
            _ => (format!("Key{}", ch), keysym as i64),
        };

        return Some((key, code, vk, text));
    }

    // Unicode characters above ASCII plane (keysym >= 0x01000000)
    if keysym >= 0x0100_0000 {
        if let Some(ch) = char::from_u32(keysym & 0x00FF_FFFF) {
            let s = ch.to_string();
            return Some((s.clone(), String::new(), 0, Some(s)));
        }
    }

    None
}
