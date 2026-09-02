// Per-connection session statistics.
//
// Tracks frames sent, bytes sent, input events, session duration, and protocol
// name for a single connection. Logged at session end as a structured summary.
//
// Design: single-threaded per session — no atomics needed. Each handler owns
// one SessionStats and updates it in its main loop.
//
// FPS counter (graphical protocols): a companion FpsCounter wraps SessionStats
// and logs a periodic FPS line every 5 seconds using wall-clock measurement.
// Integrate by calling FpsCounter::record_frame() instead of
// SessionStats::record_frame() directly.
//
// TubeDataTap integration note:
// `TubeDataTap` (keeper-pam-webrtc-rs::webrtc_data_tap) fires on raw outbound
// bytes at the WebRTC transport layer, BEFORE Guacamole framing. It is the
// right hook for recording and threat detection but lives in a crate that
// guacr handlers intentionally do not depend on (layer boundary).
//
// The correct wiring point is the caller of ProtocolHandler::connect() inside
// keeper-pam-webrtc-rs (handler_integration.rs). After connect() returns, the
// caller already holds the Tube reference and can call
// `tube.set_outbound_tap(tap)` to observe bytes at the transport level.
//
// SessionStats (this module) is the right layer for application-level stats
// (frame count, byte count, input events). TubeDataTap is the right layer for
// byte-exact transport-level observation (recording, threat detection).
// They are complementary, not competing.

use log::debug;
use std::time::Instant;

/// Per-connection statistics accumulated across the session lifetime.
pub struct SessionStats {
    /// Guacamole protocol name (e.g. "ssh", "rdp", "vnc", "telnet").
    pub protocol: &'static str,
    /// Total Guacamole instructions (frames) sent to the client.
    pub frames_sent: u64,
    /// Total bytes sent to the client (instruction payload bytes).
    pub bytes_sent: u64,
    /// Total input events received from the client (key, mouse, clipboard, etc.).
    pub input_events_received: u64,
    /// Wall-clock time when the session started (used for duration).
    session_start: Instant,
}

impl SessionStats {
    /// Create a new stats counter for the given protocol.
    pub fn new(protocol: &'static str) -> Self {
        Self {
            protocol,
            frames_sent: 0,
            bytes_sent: 0,
            input_events_received: 0,
            session_start: Instant::now(),
        }
    }

    /// Record that a frame (instruction) of `bytes` payload bytes was sent to the client.
    #[inline]
    pub fn record_frame(&mut self, bytes: usize) {
        self.frames_sent += 1;
        self.bytes_sent += bytes as u64;
    }

    /// Record that one input event was received from the client.
    #[inline]
    pub fn record_input(&mut self) {
        self.input_events_received += 1;
    }

    /// Session duration in milliseconds from creation to now.
    pub fn elapsed_ms(&self) -> u64 {
        self.session_start.elapsed().as_millis() as u64
    }

    /// Structured log line for session end.
    ///
    /// Format: `protocol=ssh frames=N bytes=N inputs=N duration_ms=N`
    pub fn summary(&self) -> String {
        format!(
            "protocol={} frames={} bytes={} inputs={} duration_ms={}",
            self.protocol,
            self.frames_sent,
            self.bytes_sent,
            self.input_events_received,
            self.elapsed_ms(),
        )
    }
}

/// Periodic FPS counter for graphical protocols (RDP, VNC, RBI).
///
/// Wraps a `SessionStats` reference and logs an FPS sample every 5 seconds.
/// Use instead of calling `stats.record_frame()` directly from graphical handlers.
///
/// Usage:
/// ```ignore
/// let mut fps = FpsCounter::new();
/// // in the frame send loop:
/// fps.record_frame(&mut stats, bytes, &conn_id);
/// ```
pub struct FpsCounter {
    /// Start of the current 5-second measurement window.
    pub(crate) window_start: Instant,
    /// Frames counted within the current window.
    pub(crate) window_frames: u32,
    /// Duration of each reporting window (5 seconds).
    pub(crate) window_secs: f64,
}

impl FpsCounter {
    /// Create a counter with a 5-second reporting window.
    pub fn new() -> Self {
        Self {
            window_start: Instant::now(),
            window_frames: 0,
            window_secs: 5.0,
        }
    }

    /// Record a frame and update stats. Logs FPS every 5 seconds.
    ///
    /// `bytes` is the instruction payload size (forwarded to SessionStats).
    /// `conn_id` is the connection ID string used in the log line.
    pub fn record_frame(&mut self, stats: &mut SessionStats, bytes: usize, conn_id: &str) {
        stats.record_frame(bytes);
        self.window_frames += 1;

        let elapsed = self.window_start.elapsed().as_secs_f64();
        if elapsed >= self.window_secs {
            let fps = self.window_frames as f64 / elapsed;
            debug!("[conn={}] fps={:.1}", conn_id, fps);
            self.window_frames = 0;
            self.window_start = Instant::now();
        }
    }
}

impl Default for FpsCounter {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_initial_state() {
        let stats = SessionStats::new("ssh");
        assert_eq!(stats.frames_sent, 0);
        assert_eq!(stats.bytes_sent, 0);
        assert_eq!(stats.input_events_received, 0);
        assert_eq!(stats.protocol, "ssh");
    }

    #[test]
    fn test_record_frame() {
        let mut stats = SessionStats::new("rdp");
        stats.record_frame(1024);
        stats.record_frame(512);
        assert_eq!(stats.frames_sent, 2);
        assert_eq!(stats.bytes_sent, 1536);
    }

    #[test]
    fn test_record_input() {
        let mut stats = SessionStats::new("vnc");
        stats.record_input();
        stats.record_input();
        stats.record_input();
        assert_eq!(stats.input_events_received, 3);
    }

    #[test]
    fn test_summary_format() {
        let mut stats = SessionStats::new("telnet");
        stats.record_frame(100);
        stats.record_input();
        let s = stats.summary();
        assert!(
            s.starts_with("protocol=telnet"),
            "summary starts with protocol=telnet: {s}"
        );
        assert!(s.contains("frames=1"), "summary contains frames=1: {s}");
        assert!(s.contains("bytes=100"), "summary contains bytes=100: {s}");
        assert!(s.contains("inputs=1"), "summary contains inputs=1: {s}");
        assert!(
            s.contains("duration_ms="),
            "summary contains duration_ms=: {s}"
        );
    }

    #[test]
    fn test_elapsed_ms_nonnegative() {
        let stats = SessionStats::new("ssh");
        assert!(
            stats.elapsed_ms() < 1000,
            "elapsed_ms should be < 1s for fresh stats"
        );
    }

    #[test]
    fn test_fps_counter_accumulates() {
        let mut fps = FpsCounter::new();
        let mut stats = SessionStats::new("rdp");
        fps.record_frame(&mut stats, 256, "test-conn");
        fps.record_frame(&mut stats, 256, "test-conn");
        assert_eq!(stats.frames_sent, 2);
        assert_eq!(stats.bytes_sent, 512);
        // Window not yet elapsed — no log yet, counter still running
        assert_eq!(fps.window_frames, 2);
    }

    #[test]
    fn test_fps_counter_resets_after_window() {
        let mut fps = FpsCounter {
            window_start: Instant::now() - std::time::Duration::from_secs(6),
            window_frames: 10,
            window_secs: 5.0,
        };
        let mut stats = SessionStats::new("rdp");
        // This frame tips us past the window — window_frames resets to 0 after logging.
        fps.record_frame(&mut stats, 1, "test");
        // After the window elapses, the counter resets to 0; a new window starts fresh.
        assert_eq!(fps.window_frames, 0);
    }
}
