// guacr-rbi: Remote Browser Isolation handler
//
// Provides isolated browser sessions using Chrome via DevTools Protocol (CDP).
//
// ## Features
//
// - Comprehensive keyboard/mouse/touch input handling
// - Audio streaming via Web Audio API
// - Clipboard synchronization (256KB - 50MB configurable)
// - Dirty rect optimization for display updates
// - Navigation history (back/forward/refresh)
// - URL pattern whitelisting
// - Popup blocking with allowlists
// - Resource limits (memory, CPU, session duration)

mod audio;
mod autofill;
mod browser_client;
mod chrome_session;
mod clipboard;
mod clipboard_polling;
mod cursor;
mod events;

// Performance optimizations
pub mod adaptive_fps;
pub mod dirty_tracker;
mod file_upload;
mod handler;
mod input;
mod js_dialog;
mod profile_isolation;
pub mod screencast;
pub mod scroll_detector;
mod tabs;

// Re-export public API

pub use chrome_session::PerformanceMetrics;

pub use audio::{
    float_to_pcm, AudioConfig, AudioPacket, AudioStream, AUDIO_PACKET_SIZE, GET_AUDIO_STATE_JS,
    WEB_AUDIO_MONITOR_JS,
};
pub use autofill::{
    generate_autofill_js, generate_totp, AutofillCredentials, AutofillManager, AutofillRule,
    TotpAlgorithm, TotpConfig,
};
pub use browser_client::BrowserClient;
pub use clipboard::{RbiClipboard, CLIPBOARD_DEFAULT_SIZE, CLIPBOARD_MAX_SIZE, CLIPBOARD_MIN_SIZE};
pub use clipboard_polling::{
    ClipboardPollingConfig, ClipboardState, CLIPBOARD_READ_JS, CLIPBOARD_WRITE_JS,
    COPY_EVENT_LISTENER_JS, GET_CLIPBOARD_DATA_JS, SELECTION_COPY_JS,
};
pub use cursor::{
    format_cursor_instruction, format_standard_cursor, CursorState, CursorType, CURSOR_TRACKER_JS,
    GET_CURSOR_JS,
};
pub use events::{
    BrowserState, ClipboardDetails, DisplayEvent, DisplayEventType, DisplayRect, DisplaySurface,
    InputEvent, KeyboardEventDetails, MouseEventDetails, NavigateHistoryDetails,
    NavigateUrlDetails, ResizeEventDetails, TouchEventDetails, UrlPattern, MAX_CLIPBOARD_LENGTH,
    MAX_HEIGHT, MAX_NAVIGATIONS, MAX_URL_LENGTH, MAX_URL_PATTERNS, MAX_WIDTH,
};
pub use file_upload::{
    detect_mime_type, format_upload_dialog_instruction, validate_mime_type, ActiveUpload,
    UploadConfig, UploadEngine, UploadInfo, UploadManager, UploadRequest, UploadState,
    MAX_CONCURRENT_UPLOADS, MAX_UPLOAD_SIZE,
};
pub use handler::{
    DownloadConfig, PopupHandling, RbiBackend, RbiConfig, RbiHandler, ResourceLimits,
};
pub use input::{
    is_printable,
    keysym_to_js_keycode,
    keysym_to_unicode,
    BrowserKeyEvent,
    BrowserMouseEvent,
    BrowserTouchEvent,
    ChromeEventFlags,
    InputState,
    KeyMapping,
    KeyboardShortcut,
    KeyboardState,
    MouseButton,
    MouseState,
    RbiInputHandler,
    TouchEventType,
    TouchState,
    KEYSYM_ALTGR,
    // Constants
    KEYSYM_ALT_LEFT,
    KEYSYM_ALT_RIGHT,
    KEYSYM_CTRL_LEFT,
    KEYSYM_CTRL_RIGHT,
    KEYSYM_META_LEFT,
    KEYSYM_META_RIGHT,
    KEYSYM_SHIFT_LEFT,
    KEYSYM_SHIFT_RIGHT,
    KEY_MAPPINGS,
    MAX_TOUCH_EVENTS,
    MOUSE_BUTTON_LEFT,
    MOUSE_BUTTON_MIDDLE,
    MOUSE_BUTTON_RIGHT,
    MOUSE_SCROLL_DISTANCE,
    MOUSE_SCROLL_DOWN,
    MOUSE_SCROLL_UP,
};
pub use js_dialog::{
    format_dialog_instruction, JsDialogConfig, JsDialogManager, JsDialogRequest, JsDialogResponse,
    JsDialogType, DIALOG_INTERCEPTOR_JS, DIALOG_TIMEOUT_SECS, MAX_MESSAGE_LENGTH,
};
pub use profile_isolation::{DbusIsolation, ProfileCreationMode, ProfileLock, ProfileLockError};
pub use tabs::{TabInfo, TabManager, MAX_TABS, TAB_ID_INVALID, TAB_ID_PENDING};

use thiserror::Error;

#[derive(Error, Debug)]
pub enum RbiError {
    #[error("Browser launch failed: {0}")]
    BrowserLaunchFailed(String),

    #[error("Navigation failed: {0}")]
    NavigationFailed(String),

    #[error("Input error: {0}")]
    InputError(String),

    #[error("Clipboard error: {0}")]
    ClipboardError(String),

    #[error("Display error: {0}")]
    DisplayError(String),

    #[error("URL not allowed: {0}")]
    UrlNotAllowed(String),

    #[error("Resource limit exceeded: {0}")]
    ResourceLimitExceeded(String),

    #[error("Handler error: {0}")]
    HandlerError(#[from] guacr_handlers::HandlerError),

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, RbiError>;

/// Check if a URL is allowed based on patterns
pub fn check_url_allowed(url: &str, patterns: &[UrlPattern]) -> bool {
    if patterns.is_empty() {
        return true; // No restrictions
    }
    patterns.iter().any(|p| p.matches(url))
}

#[cfg(test)]
mod tests;
