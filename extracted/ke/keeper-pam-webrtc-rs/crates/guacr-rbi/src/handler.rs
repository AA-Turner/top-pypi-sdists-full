use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    // Error helpers
    send_error_best_effort,
    EventBasedHandler,
    EventCallback,
    HandlerError,
    HandlerStats,
    HealthStatus,
    ProtocolHandler,
    // Security
    RbiSecuritySettings,
    // Recording
    RecordingConfig,
    VideoOutput,
};
use guacr_protocol::STATUS_RESOURCE_CONFLICT;
use log::info;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;

/// Remote Browser Isolation (RBI) handler
///
/// Provides isolated browser sessions using headless Chrome/Chromium.
/// Screen is captured and sent as images over WebRTC.
///
/// ## CRITICAL: Pixel-Perfect Dimension Alignment
///
/// To avoid blurry rendering from browser scaling:
/// 1. Browser sends size request: width_px, height_px
/// 2. Set browser viewport: browser.set_window_size(width_px, height_px)
/// 3. Send `size` instruction with SAME dimensions: size,0,width_px,height_px;
/// 4. Capture screenshot at SAME dimensions: screenshot(width_px, height_px)
/// 5. Result: PNG size = layer size = no scaling = crisp
///
/// NEVER use mismatched dimensions - causes browser to scale and blur the image.
pub struct RbiHandler {
    config: RbiConfig,
}

#[derive(Debug, Clone, PartialEq)]
pub enum RbiBackend {
    Chrome,            // Production: Full compatibility, 200-500MB
    Servo,             // Experimental: Rust-native, 50-100MB, limited sites
    ServoWithFallback, // Try Servo first, fallback to Chrome if broken
}

#[derive(Debug, Clone)]
pub struct RbiConfig {
    pub backend: RbiBackend,
    pub default_width: u32,
    pub default_height: u32,
    pub chromium_path: String,
    pub popup_handling: PopupHandling,
    pub resource_limits: ResourceLimits,
    pub capture_fps: u32,
    pub use_screencast: Option<bool>, // Use Page.startScreencast instead of screenshots
    pub servo_allowlist: Vec<String>, // Domains known to work with Servo
    pub download_config: DownloadConfig,
    pub upload_config: crate::file_upload::UploadConfig,
    // Security settings
    pub allowed_url_patterns: Vec<String>, // URL whitelist patterns
    pub allowed_resource_patterns: Vec<String>, // Resource URL whitelist
    pub disable_copy: bool,                // Block copy from browser
    pub disable_paste: bool,               // Block paste to browser
    pub clipboard_buffer_size: usize,      // Clipboard buffer size (256KB-50MB)
    // Navigation settings
    pub allow_url_manipulation: bool, // Allow user to change URL
    pub ignore_ssl_errors: bool,      // Ignore SSL cert errors for initial URL
    // Localization settings
    pub timezone: Option<String>, // Timezone (e.g., "America/New_York")
    pub accept_language: Option<String>, // Accept-Language header (e.g., "en-US,en;q=0.9")
    // Audio settings
    pub audio_config: crate::audio::AudioConfig,
    // Autofill settings
    pub autofill_rules: Vec<crate::autofill::AutofillRule>,
    pub autofill_credentials: Option<crate::autofill::AutofillCredentials>,
    // Profile settings
    pub profile_storage_directory: Option<String>, // Persist browser profile
    pub create_profile_directory: bool,            // Create directory if missing
}

#[derive(Debug, Clone)]
pub struct DownloadConfig {
    pub enabled: bool,           // Enable downloads (default: false for security)
    pub max_file_size_mb: usize, // Maximum file size (default: 10MB)
    pub allowed_extensions: Vec<String>, // Allowed file extensions (e.g., ["pdf", "txt"])
    pub blocked_extensions: Vec<String>, // Blocked file extensions (e.g., ["exe", "bat"])
    pub require_approval: bool,  // Require user approval (future)
    pub max_downloads_per_session: usize, // Rate limiting (default: 5)
}

#[derive(Debug, Clone, PartialEq)]
pub enum PopupHandling {
    Block,                  // Block all popups (default, most secure)
    AllowList(Vec<String>), // Only allow specific domains (e.g., OAuth)
    NavigateMainWindow,     // Navigate main window to popup URL
}

#[derive(Debug, Clone)]
pub struct ResourceLimits {
    pub max_memory_mb: usize, // Kill browser if exceeds (default: 500MB)
    pub max_cpu_percent: u32, // Throttle if exceeds (default: 80%)
    pub timeout_seconds: u64, // Max session duration (default: 3600 = 1 hour)
}

impl RbiConfig {
    /// Auto-detect Chromium/Chrome installation path
    fn find_chromium_path() -> String {
        // Allow explicit override via environment variable
        if let Ok(path) = std::env::var("CHROMIUM_PATH") {
            if !path.is_empty() && std::path::Path::new(&path).exists() {
                return path;
            }
        }

        // Platform-specific candidate paths
        #[cfg(target_os = "windows")]
        let candidates: &[&str] = &[
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Chromium\Application\chrome.exe",
            r"C:\Program Files (x86)\Chromium\Application\chrome.exe",
        ];
        // IMPORTANT: Rocky/RHEL use chromium-browser, check it BEFORE chromium
        #[cfg(not(target_os = "windows"))]
        let candidates: &[&str] = &[
            "/usr/bin/chromium-browser", // Rocky/RHEL/CentOS (CHECKED FIRST)
            "/usr/lib64/chromium-browser/chromium-browser", // Rocky/RHEL alternate
            "/usr/bin/chromium",         // Debian/Ubuntu
            "/usr/bin/google-chrome",    // Google Chrome
            "/usr/bin/google-chrome-stable", // Google Chrome stable
            "/snap/bin/chromium",        // Snap package
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", // macOS
            "/Applications/Chromium.app/Contents/MacOS/Chromium", // macOS Chromium
        ];

        for &path in candidates {
            if std::path::Path::new(path).exists() {
                return path.to_string();
            }
        }

        // Fallback: search PATH using the `which` crate (works on Linux, macOS, and Windows;
        // no subprocess spawned — avoids PATH injection and works in sandboxed environments).
        #[cfg(target_os = "windows")]
        let fallback_names: &[&str] = &["chrome", "chromium"];
        #[cfg(not(target_os = "windows"))]
        let fallback_names: &[&str] = &["chromium-browser", "chromium", "google-chrome"];

        for name in fallback_names {
            if let Ok(path) = which::which(name) {
                return path.to_string_lossy().into_owned();
            }
        }

        // Last resort: platform default
        #[cfg(target_os = "windows")]
        let default = "chrome.exe";
        #[cfg(not(target_os = "windows"))]
        let default = "/usr/bin/chromium-browser";
        default.to_string()
    }
}

impl Default for RbiConfig {
    fn default() -> Self {
        // Auto-detect Chromium path
        let chromium_path = Self::find_chromium_path();

        Self {
            backend: RbiBackend::Chrome, // Chrome is the only implemented backend
            default_width: 1920,
            default_height: 1080,
            chromium_path,
            popup_handling: PopupHandling::Block,
            resource_limits: ResourceLimits {
                max_memory_mb: 500,
                max_cpu_percent: 80,
                timeout_seconds: 3600,
            },
            capture_fps: 30, // Max FPS for adaptive screenshot fallback. Must be >= 5 (AdaptiveFps min).
            use_screencast: Some(true), // Prefer JPEG screencast (Chrome pushes frames on change);
            // falls back to screenshot polling if setup fails.
            servo_allowlist: vec![
                "docs.rs".to_string(),
                "github.com".to_string(),
                "stackoverflow.com".to_string(),
                "wikipedia.org".to_string(),
                "rust-lang.org".to_string(),
            ],
            download_config: DownloadConfig::default(),
            upload_config: crate::file_upload::UploadConfig::default(),
            // Security settings - open by default (can be restricted per-connection)
            allowed_url_patterns: Vec::new(), // Empty = allow all
            allowed_resource_patterns: Vec::new(),
            disable_copy: false,
            disable_paste: false,
            clipboard_buffer_size: 256 * 1024, // 256KB default
            // Navigation settings
            allow_url_manipulation: true,
            ignore_ssl_errors: false,
            // Localization settings
            timezone: None,        // Use browser default
            accept_language: None, // Use browser default
            // Audio settings
            audio_config: crate::audio::AudioConfig::default(),
            // Autofill settings
            autofill_rules: Vec::new(),
            autofill_credentials: None,
            // Profile settings
            profile_storage_directory: None, // Don't persist by default
            create_profile_directory: false,
        }
    }
}

impl Default for DownloadConfig {
    fn default() -> Self {
        Self {
            enabled: false, // Block by default (like KCM)
            max_file_size_mb: 10,
            allowed_extensions: vec![
                "pdf".to_string(),
                "txt".to_string(),
                "csv".to_string(),
                "json".to_string(),
                "xml".to_string(),
                "png".to_string(),
                "jpg".to_string(),
                "jpeg".to_string(),
                "gif".to_string(),
            ],
            blocked_extensions: vec![
                "exe".to_string(),
                "bat".to_string(),
                "sh".to_string(),
                "dmg".to_string(),
                "msi".to_string(),
                "app".to_string(),
                "deb".to_string(),
                "rpm".to_string(),
                "zip".to_string(), // Can contain executables
            ],
            require_approval: true,
            max_downloads_per_session: 5,
        }
    }
}

impl RbiHandler {
    pub fn new(config: RbiConfig) -> Self {
        Self { config }
    }

    pub fn with_defaults() -> Self {
        Self::new(RbiConfig::default())
    }
}

#[async_trait]
impl ProtocolHandler for RbiHandler {
    fn name(&self) -> &str {
        "http"
    }

    fn as_event_based(&self) -> Option<&dyn EventBasedHandler> {
        Some(self)
    }

    #[allow(unused_variables)]
    async fn connect(
        &self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> guacr_handlers::Result<()> {
        info!("RBI handler starting");

        // ── GUID-based viewer join (Phase 6b) ────────────────────────────────
        if params.contains_key("share_guid") {
            return guacr_handlers::share_viewer::check_viewer_join(
                &params,
                &to_client,
                from_client,
                "",
            )
            .await
            .unwrap_or(Ok(()));
        }

        // Parse RBI-specific security settings
        let security = RbiSecuritySettings::from_params(&params);
        info!(
            "RBI: Security - read_only={}, download={}, upload={}, print={}, allowlist_len={}",
            security.base.read_only,
            security.is_download_allowed(),
            security.is_upload_allowed(),
            security.is_print_allowed(),
            security.url_allowlist.len()
        );

        // Parse recording configuration
        let recording_config = RecordingConfig::from_params(&params);
        if recording_config.is_enabled() {
            info!(
                "RBI: Recording enabled - ses={}, asciicast={}, typescript={}",
                recording_config.is_ses_enabled(),
                recording_config.is_asciicast_enabled(),
                recording_config.is_typescript_enabled()
            );
        }

        let url = params
            .get("url")
            .ok_or_else(|| HandlerError::MissingParameter("url".to_string()))?;

        // Security: Validate URL scheme before any other check. Only http/https are allowed.
        crate::browser_client::validate_navigate_scheme(url)
            .map_err(HandlerError::SecurityViolation)?;

        // Security: Check URL against allowlist/blocklist
        if !security.is_url_allowed(url) {
            return Err(HandlerError::SecurityViolation(
                "URL not allowed".to_string(),
            ));
        }

        // AC-1/AC-2 (T-007, T-008): Check for network namespace isolation BEFORE launching any
        // browser process. If the check fails, return an error — no browser is spawned.
        crate::network_isolation::check_network_isolation()
            .map_err(HandlerError::SecurityViolation)?;

        {
            let safe_url = crate::browser_client::rbi_safe_url_for_log(url);
            info!("RBI launching browser for URL: {}", safe_url);
        }

        // Parse width/height from connection parameters
        // Client sends "size" as "width,height,dpi" (e.g., "2102,1536,192")
        // If not provided, use defaults (1920x1080)
        let (width, height) = if let Some(size_str) = params.get("size") {
            let parts: Vec<&str> = size_str.split(',').collect();
            if parts.len() >= 2 {
                let w = parts[0].parse().unwrap_or(self.config.default_width);
                let h = parts[1].parse().unwrap_or(self.config.default_height);
                (w, h)
            } else {
                (self.config.default_width, self.config.default_height)
            }
        } else {
            // Fallback to separate width/height params if size not present
            let w = params
                .get("width")
                .and_then(|w| w.parse().ok())
                .unwrap_or(self.config.default_width);
            let h = params
                .get("height")
                .and_then(|h| h.parse().ok())
                .unwrap_or(self.config.default_height);
            (w, h)
        };

        info!(
            "RBI: Using initial size {}x{} (from params or default)",
            width, height
        );

        // Use the appropriate backend
        #[cfg(feature = "chrome")]
        {
            use crate::browser_client::BrowserClient;
            let mut browser_client = BrowserClient::new(
                width,
                height,
                self.config.clone(),
                &recording_config,
                &params,
            )
            .map_err(HandlerError::ConnectionFailed)?;

            // Connect and handle session
            // Clone sender so we can send an error message if the session fails to start
            let error_sender = to_client.clone();
            let connect_result = browser_client.connect(url, to_client, from_client).await;

            if let Err(ref e) = connect_result {
                if e.starts_with("PROFILE_IN_USE:") {
                    send_error_best_effort(
                        &error_sender,
                        "This browser profile is already in use by another active session. \
                         Please try again later, or ask your administrator to configure \
                         'By User' persistence to allow concurrent access.",
                        STATUS_RESOURCE_CONFLICT,
                    )
                    .await;
                }
            }

            connect_result.map_err(HandlerError::ConnectionFailed)?;

            info!("RBI handler ended (Chrome/CDP)");
            Ok(())
        }
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
impl EventBasedHandler for RbiHandler {
    fn name(&self) -> &str {
        "http"
    }

    async fn connect_with_events(
        &self,
        params: HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> Result<(), HandlerError> {
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
