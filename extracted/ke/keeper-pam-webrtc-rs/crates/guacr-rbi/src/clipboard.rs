// RBI clipboard handling
// Uses shared terminal clipboard resources with RBI-specific extensions

use bytes::Bytes;
use log::{debug, info, warn};
use std::sync::{Arc, Mutex};

// Re-export clipboard constants from guacr-terminal
pub use guacr_terminal::{CLIPBOARD_DEFAULT_SIZE, CLIPBOARD_MAX_SIZE, CLIPBOARD_MIN_SIZE};

/// RBI clipboard handler
///
/// Manages bidirectional clipboard synchronization between the Guacamole client
/// and the browser. Supports configurable buffer sizes (256KB - 50MB).
pub struct RbiClipboard {
    /// Clipboard buffer
    buffer: Arc<Mutex<Vec<u8>>>,
    /// Current buffer size
    buffer_size: usize,
    /// Current mimetype
    mimetype: String,
    /// Current data length
    length: usize,
    /// Whether copy (browser → client) is disabled
    disable_copy: bool,
    /// Whether paste (client → browser) is disabled
    disable_paste: bool,
}

impl RbiClipboard {
    /// Create a new RBI clipboard with configurable buffer size
    pub fn new(buffer_size: usize) -> Self {
        // Validate and clamp buffer size
        let validated_size = buffer_size.clamp(CLIPBOARD_MIN_SIZE, CLIPBOARD_MAX_SIZE);

        if validated_size != buffer_size {
            warn!(
                "RBI: Clipboard buffer size {} adjusted to {}",
                buffer_size, validated_size
            );
        }

        Self {
            buffer: Arc::new(Mutex::new(vec![0u8; validated_size])),
            buffer_size: validated_size,
            mimetype: String::new(),
            length: 0,
            disable_copy: false,
            disable_paste: false,
        }
    }

    /// Create with default settings
    pub fn with_defaults() -> Self {
        Self::new(CLIPBOARD_DEFAULT_SIZE)
    }

    /// Set copy/paste restrictions
    pub fn set_restrictions(&mut self, disable_copy: bool, disable_paste: bool) {
        self.disable_copy = disable_copy;
        self.disable_paste = disable_paste;
        info!(
            "RBI: Clipboard restrictions - copy: {}, paste: {}",
            if disable_copy { "disabled" } else { "enabled" },
            if disable_paste { "disabled" } else { "enabled" }
        );
    }

    /// Get the configured buffer size
    pub fn buffer_size(&self) -> usize {
        self.buffer_size
    }

    /// Handle clipboard data from browser (copy operation)
    ///
    /// Called when the browser's clipboard content changes.
    /// Returns Guacamole clipboard instruction to send to client.
    pub fn handle_browser_clipboard(
        &mut self,
        data: &[u8],
        mimetype: &str,
    ) -> Result<Option<Bytes>, String> {
        if self.disable_copy {
            debug!("RBI: Copy disabled, ignoring browser clipboard");
            return Ok(None);
        }

        // Truncate if too large
        let length = data.len().min(self.buffer_size);
        if length < data.len() {
            warn!(
                "RBI: Browser clipboard truncated from {} to {} bytes",
                data.len(),
                length
            );
        }

        // Store clipboard data
        {
            let mut buffer = self
                .buffer
                .lock()
                .map_err(|e| format!("Lock error: {}", e))?;
            buffer[..length].copy_from_slice(&data[..length]);
        }
        self.length = length;
        self.mimetype = mimetype.to_string();

        info!(
            "RBI: Browser clipboard updated - {} bytes, type: {}",
            length, mimetype
        );

        // Format as Guacamole clipboard instruction
        Ok(Some(self.format_clipboard_instruction()?))
    }

    /// Handle clipboard data from client (paste operation)
    ///
    /// Called when the client sends clipboard data.
    /// Returns the data to inject into the browser.
    pub fn handle_client_clipboard(
        &mut self,
        data: &[u8],
        mimetype: &str,
    ) -> Result<Option<Vec<u8>>, String> {
        if self.disable_paste {
            debug!("RBI: Paste disabled, ignoring client clipboard");
            return Ok(None);
        }

        // Truncate if too large
        let length = data.len().min(self.buffer_size);
        if length < data.len() {
            warn!(
                "RBI: Client clipboard truncated from {} to {} bytes",
                data.len(),
                length
            );
        }

        // Store clipboard data
        {
            let mut buffer = self
                .buffer
                .lock()
                .map_err(|e| format!("Lock error: {}", e))?;
            buffer[..length].copy_from_slice(&data[..length]);
        }
        self.length = length;
        self.mimetype = mimetype.to_string();

        info!(
            "RBI: Client clipboard received - {} bytes, type: {}",
            length, mimetype
        );

        // Return data for browser injection
        let buffer = self
            .buffer
            .lock()
            .map_err(|e| format!("Lock error: {}", e))?;
        Ok(Some(buffer[..length].to_vec()))
    }

    /// Get current clipboard data
    pub fn get_data(&self) -> Result<Vec<u8>, String> {
        let buffer = self
            .buffer
            .lock()
            .map_err(|e| format!("Lock error: {}", e))?;
        Ok(buffer[..self.length].to_vec())
    }

    /// Get current mimetype
    pub fn mimetype(&self) -> &str {
        &self.mimetype
    }

    /// Format clipboard data as Guacamole instruction
    fn format_clipboard_instruction(&self) -> Result<Bytes, String> {
        let buffer = self
            .buffer
            .lock()
            .map_err(|e| format!("Lock error: {}", e))?;
        let data = &buffer[..self.length];

        let stream_id = 10; // Fixed stream ID for clipboard
        let instrs = guacr_protocol::format_clipboard(stream_id, &self.mimetype, data);
        Ok(Bytes::from(instrs.join("")))
    }

    /// Reset clipboard state
    pub fn reset(&mut self) {
        self.length = 0;
        self.mimetype.clear();
        debug!("RBI: Clipboard reset");
    }
}

impl Default for RbiClipboard {
    fn default() -> Self {
        Self::with_defaults()
    }
}
