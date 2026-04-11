// Shared display constants and utility functions used across all terminal and
// graphical protocol handlers.

use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};

/// Pixel width of one character cell in the shared fontdue renderer.
pub const CHAR_WIDTH: u32 = 9;
/// Pixel height of one character cell in the shared fontdue renderer.
pub const CHAR_HEIGHT: u32 = 18;

/// Default terminal width in columns (standard VT100).
pub const DEFAULT_COLS: u16 = 80;
/// Default terminal height in rows (standard VT100).
pub const DEFAULT_ROWS: u16 = 24;

/// JPEG quality used for terminal and graphical frame encoding.
pub const JPEG_QUALITY: u8 = 85;

/// Target render interval in milliseconds (~30 FPS).
pub const RENDER_INTERVAL_MS: u64 = 33;

/// Returns the current time as milliseconds since the Unix epoch.
///
/// Replaces the 18 inline `SystemTime::now().duration_since(UNIX_EPOCH)...as_millis() as u64`
/// expressions across SSH, Telnet, VNC, RDP, TN3270, and TN5250 handlers.
pub fn current_time_millis() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as u64
}

/// Convert pixel dimensions to terminal character columns and rows.
///
/// Uses the shared `CHAR_WIDTH` × `CHAR_HEIGHT` cell size. Results are
/// clamped to a minimum of `DEFAULT_COLS` × `DEFAULT_ROWS`.
pub fn pixels_to_chars(width: u32, height: u32) -> (u16, u16) {
    let cols = (width / CHAR_WIDTH).max(DEFAULT_COLS as u32) as u16;
    let rows = (height / CHAR_HEIGHT).max(DEFAULT_ROWS as u32) as u16;
    (cols, rows)
}

/// Convert terminal character columns and rows to pixel dimensions.
pub fn chars_to_pixels(cols: u16, rows: u16) -> (u32, u32) {
    (cols as u32 * CHAR_WIDTH, rows as u32 * CHAR_HEIGHT)
}

/// Parse display size from Guacamole connection parameters.
///
/// Reads the `"size"` parameter (format: `"width,height,dpi"`, e.g. `"1024,768,96"`)
/// and returns `(pixel_width, pixel_height, cols, rows)`. Defaults to 1024×768 if
/// the parameter is absent or unparseable.
pub fn parse_display_size(params: &HashMap<String, String>) -> (u32, u32, u16, u16) {
    let size_str = params
        .get("size")
        .map(|s| s.as_str())
        .unwrap_or("1024,768,96");
    let parts: Vec<&str> = size_str.split(',').collect();
    let width: u32 = parts.first().and_then(|s| s.parse().ok()).unwrap_or(1024);
    let height: u32 = parts.get(1).and_then(|s| s.parse().ok()).unwrap_or(768);
    let (cols, rows) = pixels_to_chars(width, height);
    (width, height, cols, rows)
}
