// sync_control.rs - Guacamole sync flow control for all protocol handlers
//
// Implements bidirectional sync acknowledgment to prevent overwhelming slow clients.
// Server sends sync instructions with timestamps, then waits for client to echo back.
// Disconnects after multiple consecutive timeouts.
//
// This prevents frame buffering that causes lag and memory issues on slow connections.

use bytes::Bytes;
use std::time::Duration;
use tokio::sync::mpsc;

/// Manages sync flow control between server and client
///
/// Flow control prevents the server from overwhelming slow clients by:
/// 1. Sending a sync instruction with timestamp after each frame
/// 2. Waiting for client to acknowledge the sync (echo back the timestamp)
/// 3. Timing out after a configurable duration (default 15s)
/// 4. Disconnecting after multiple consecutive timeouts (default 3)
///
/// This matches Apache Guacamole's guacd behavior for compatibility.
pub struct SyncFlowControl {
    pending_sync_timestamp: Option<u64>,
    pub(crate) sync_timeout_count: u32,
    timeout_duration: Duration,
    max_consecutive_timeouts: u32,
}

impl SyncFlowControl {
    /// Create a new sync flow control manager with default settings
    ///
    /// Defaults match Apache Guacamole guacd:
    /// - 15 second timeout
    /// - 3 consecutive timeouts before disconnect
    pub fn new() -> Self {
        Self {
            pending_sync_timestamp: None,
            sync_timeout_count: 0,
            timeout_duration: Duration::from_secs(15),
            max_consecutive_timeouts: 3,
        }
    }

    /// Create with custom timeout settings
    ///
    /// # Arguments
    ///
    /// * `timeout_secs` - Seconds to wait for sync acknowledgment
    /// * `max_timeouts` - Number of consecutive timeouts before disconnect
    pub fn with_timeout(timeout_secs: u64, max_timeouts: u32) -> Self {
        Self {
            pending_sync_timestamp: None,
            sync_timeout_count: 0,
            timeout_duration: Duration::from_secs(timeout_secs),
            max_consecutive_timeouts: max_timeouts,
        }
    }

    /// Record that a sync was sent to the client
    ///
    /// Call this after sending a sync instruction. The timestamp should match
    /// what was sent in the sync instruction.
    ///
    /// # Arguments
    ///
    /// * `timestamp` - The timestamp sent in the sync instruction
    pub fn set_pending_sync(&mut self, timestamp: u64) {
        self.pending_sync_timestamp = Some(timestamp);
    }

    /// Wait for client to acknowledge the sync
    ///
    /// Blocks until:
    /// - Client sends back a sync with matching or newer timestamp (success)
    /// - Timeout expires (may allow retry if under max_consecutive_timeouts)
    /// - Client channel closes (error)
    ///
    /// # Arguments
    ///
    /// * `from_client` - Receiver for client messages
    /// * `sent_timestamp` - The timestamp that was sent (should match set_pending_sync)
    ///
    /// # Returns
    ///
    /// - `Ok(())` - Client acknowledged sync
    /// - `Err(msg)` - Client disconnected or exceeded timeout limit
    pub async fn wait_for_client_sync(
        &mut self,
        from_client: &mut mpsc::Receiver<Bytes>,
        sent_timestamp: u64,
    ) -> Result<(), String> {
        let timeout_result = tokio::time::timeout(self.timeout_duration, async {
            loop {
                match from_client.recv().await {
                    Some(msg) => {
                        // Try to parse as UTF-8 string for sync instruction check
                        if let Ok(msg_str) = std::str::from_utf8(&msg) {
                            if msg_str.starts_with("4.sync,") {
                                if let Some(ts) = self.parse_sync_timestamp(msg_str) {
                                    if ts >= sent_timestamp {
                                        // Client caught up with our sync
                                        self.sync_timeout_count = 0;
                                        return Ok(());
                                    }
                                }
                            }
                        }
                        // Not a matching sync, keep waiting
                    }
                    None => {
                        return Err("Client channel closed while waiting for sync".to_string());
                    }
                }
            }
        })
        .await;

        match timeout_result {
            Ok(Ok(())) => {
                // Client responded in time
                Ok(())
            }
            Ok(Err(e)) => {
                // Client channel closed
                Err(e)
            }
            Err(_) => {
                // Timeout
                self.sync_timeout_count += 1;

                if self.sync_timeout_count >= self.max_consecutive_timeouts {
                    Err(format!(
                        "Client not responding to sync ({} consecutive timeouts)",
                        self.sync_timeout_count
                    ))
                } else {
                    // Allow a few timeouts before giving up
                    log::warn!(
                        "Sync timeout {}/{} - continuing",
                        self.sync_timeout_count,
                        self.max_consecutive_timeouts
                    );
                    Ok(())
                }
            }
        }
    }

    /// Parse timestamp from sync instruction
    ///
    /// Sync instruction format: "4.sync,<len>.<timestamp>;"
    /// Example: "4.sync,13.1234567890123;"
    ///
    /// Uses zero-copy string slicing for efficiency.
    pub(crate) fn parse_sync_timestamp(&self, sync_instr: &str) -> Option<u64> {
        // Find the dot that separates length from timestamp
        let after_sync = sync_instr.strip_prefix("4.sync,")?;
        let dot_pos = after_sync.find('.')?;

        // Extract timestamp (between dot and semicolon)
        let timestamp_part = &after_sync[dot_pos + 1..];
        let semicolon_pos = timestamp_part.find(';')?;
        let timestamp_str = &timestamp_part[..semicolon_pos];

        timestamp_str.parse::<u64>().ok()
    }

    /// Check if currently waiting for a sync acknowledgment
    pub fn is_waiting_for_sync(&self) -> bool {
        self.pending_sync_timestamp.is_some()
    }

    /// Get the pending sync timestamp if any
    pub fn pending_timestamp(&self) -> Option<u64> {
        self.pending_sync_timestamp
    }

    /// Clear pending sync (e.g., after successful acknowledgment)
    pub fn clear_pending(&mut self) {
        self.pending_sync_timestamp = None;
    }

    /// Get the current timeout count
    pub fn timeout_count(&self) -> u32 {
        self.sync_timeout_count
    }

    /// Reset timeout count (e.g., after successful sync)
    pub fn reset_timeout_count(&mut self) {
        self.sync_timeout_count = 0;
    }

    /// Check if a sync timeout occurred and should disconnect
    ///
    /// Call this periodically (e.g., every second) to check if the pending sync has timed out.
    /// Returns true if the connection should be closed due to too many consecutive timeouts.
    pub fn check_timeout(&mut self, elapsed_since_sync: Duration) -> bool {
        if self.pending_sync_timestamp.is_none() {
            return false; // No pending sync
        }

        if elapsed_since_sync >= self.timeout_duration {
            // Timeout occurred
            self.sync_timeout_count += 1;
            self.pending_sync_timestamp = None; // Clear pending so we don't count it again

            if self.sync_timeout_count >= self.max_consecutive_timeouts {
                log::error!(
                    "Client not responding to sync ({} consecutive timeouts) - disconnecting",
                    self.sync_timeout_count
                );
                return true; // Should disconnect
            } else {
                log::warn!(
                    "Sync timeout {}/{} - continuing",
                    self.sync_timeout_count,
                    self.max_consecutive_timeouts
                );
            }
        }

        false // Continue
    }
}

impl Default for SyncFlowControl {
    fn default() -> Self {
        Self::new()
    }
}

/// Lossless, chunked output buffer for terminal handlers (SSH/Telnet/TN3270/TN5250).
///
/// Terminal output is a **stateful byte stream** — escape sequences span multiple
/// bytes and the client's emulator (xterm.js) tracks cursor/mode state across them.
/// Dropping bytes mid-stream corrupts that state and produces visual glitches or a
/// wedged terminal. Unlike image protocols (RDP/VNC), where a dropped frame is healed
/// by the next full frame, terminal bytes must **never** be dropped.
///
/// This buffer accumulates all output losslessly and hands it back in size-bounded
/// frames. Backpressure is applied to the *source* (stop reading the SSH channel when
/// [`len`](Self::len) exceeds a high-water mark) rather than by discarding bytes.
#[derive(Default)]
pub struct TerminalOutputBuffer {
    buf: std::collections::VecDeque<u8>,
}

impl TerminalOutputBuffer {
    pub fn new() -> Self {
        Self {
            buf: std::collections::VecDeque::new(),
        }
    }

    /// Append server output. Never drops.
    pub fn push(&mut self, data: &[u8]) {
        self.buf.extend(data.iter().copied());
    }

    /// Drain up to `max` bytes from the front to send as one frame. Returns `None`
    /// when empty. Any remainder is retained (in order) for the next frame.
    pub fn take_frame(&mut self, max: usize) -> Option<Vec<u8>> {
        if max == 0 || self.buf.is_empty() {
            return None;
        }
        let n = self.buf.len().min(max);
        Some(self.buf.drain(..n).collect())
    }

    /// Return an unsent frame to the front (e.g. when the send queue was full), so no
    /// bytes are lost and ordering is preserved for the next flush attempt.
    pub fn requeue_front(&mut self, frame: Vec<u8>) {
        for b in frame.into_iter().rev() {
            self.buf.push_front(b);
        }
    }

    pub fn len(&self) -> usize {
        self.buf.len()
    }

    pub fn is_empty(&self) -> bool {
        self.buf.is_empty()
    }
}
