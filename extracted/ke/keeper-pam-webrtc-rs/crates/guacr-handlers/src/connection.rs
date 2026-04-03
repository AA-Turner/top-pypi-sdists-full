// Connection utilities for protocol handlers
//
// Provides timeout-wrapped connection helpers and keep-alive mechanisms
// matching Apache guacd's behavior.

use bytes::Bytes;
use std::time::Duration;
use tokio::net::TcpStream;
use tokio::sync::mpsc;
use tokio::time::{interval, timeout, Instant};

use crate::HandlerError;

/// Default connection timeout in seconds
///
/// Matches keeper-pam-webrtc-rs `tube_creation_timeout()` (15 seconds).
/// This is the maximum time to wait for TCP + protocol handshake.
pub const DEFAULT_CONNECTION_TIMEOUT_SECS: u64 = 15;

/// Default keep-alive interval in seconds
pub const DEFAULT_KEEPALIVE_INTERVAL_SECS: u64 = 5;

/// Connect to a TCP endpoint with timeout
///
/// Wraps `TcpStream::connect` with a configurable timeout, matching
/// guacd's `timeout` parameter behavior for SSH/RDP/VNC connections.
///
/// # Arguments
/// * `addr` - The address to connect to (hostname:port or (hostname, port))
/// * `timeout_secs` - Connection timeout in seconds (0 = no timeout, uses OS default)
///
/// # Returns
/// * `Ok(TcpStream)` - Connected stream with TCP_NODELAY enabled
/// * `Err(HandlerError)` - Connection failed or timed out
pub async fn connect_tcp_with_timeout<A: tokio::net::ToSocketAddrs>(
    addr: A,
    timeout_secs: u64,
) -> Result<TcpStream, HandlerError> {
    let stream = if timeout_secs > 0 {
        timeout(Duration::from_secs(timeout_secs), TcpStream::connect(&addr))
            .await
            .map_err(|_| {
                HandlerError::ConnectionFailed(format!(
                    "Connection timed out after {} seconds",
                    timeout_secs
                ))
            })?
            .map_err(|e| HandlerError::ConnectionFailed(e.to_string()))?
    } else {
        // No timeout - use OS default (typically 75-120 seconds)
        TcpStream::connect(&addr)
            .await
            .map_err(|e| HandlerError::ConnectionFailed(e.to_string()))?
    };

    // Enable TCP_NODELAY for low-latency interactive sessions
    if let Err(e) = stream.set_nodelay(true) {
        log::warn!("Failed to set TCP_NODELAY: {}", e);
    }

    Ok(stream)
}

/// Keep-alive manager for Guacamole connections
///
/// Sends periodic "sync" instructions to detect dead connections,
/// matching guacd's `guac_socket_require_keep_alive()` behavior.
///
/// The sync instruction format is: `4.sync,TIMESTAMP_LEN.TIMESTAMP,1.FRAME;`
/// where TIMESTAMP is milliseconds since connection start.
pub struct KeepAliveManager {
    interval: Duration,
    start_time: Instant,
    last_sync: Instant,
    frame_counter: u32,
}

impl KeepAliveManager {
    /// Create a new keep-alive manager
    ///
    /// # Arguments
    /// * `interval_secs` - Interval between keep-alive pings (0 = disabled)
    pub fn new(interval_secs: u64) -> Self {
        let now = Instant::now();
        Self {
            interval: Duration::from_secs(interval_secs),
            start_time: now,
            last_sync: now,
            frame_counter: 0,
        }
    }

    /// Check if a keep-alive ping is due
    ///
    /// Returns `Some(sync_instruction)` if it's time to send a ping,
    /// `None` otherwise.
    pub fn check(&mut self) -> Option<Bytes> {
        if self.interval.is_zero() {
            return None;
        }

        if self.last_sync.elapsed() >= self.interval {
            self.last_sync = Instant::now();
            Some(self.generate_sync())
        } else {
            None
        }
    }

    /// Generate a sync instruction
    ///
    /// Format: `4.sync,TIMESTAMP_LEN.TIMESTAMP,1.FRAME;`
    pub fn generate_sync(&mut self) -> Bytes {
        let timestamp = self.start_time.elapsed().as_millis() as u64;
        self.frame_counter = self.frame_counter.wrapping_add(1);

        let timestamp_str = timestamp.to_string();
        let frame_str = self.frame_counter.to_string();

        Bytes::from(format!(
            "4.sync,{}.{},{}.{};",
            timestamp_str.len(),
            timestamp_str,
            frame_str.len(),
            frame_str
        ))
    }

    /// Get the current timestamp (milliseconds since start)
    pub fn timestamp_ms(&self) -> u64 {
        self.start_time.elapsed().as_millis() as u64
    }

    /// Reset the keep-alive timer (call after receiving client activity)
    pub fn reset(&mut self) {
        self.last_sync = Instant::now();
    }
}

/// Spawn a keep-alive task that sends periodic sync instructions
///
/// This runs in the background and sends sync instructions at the specified
/// interval. The task stops when the sender is dropped or the receiver closes.
///
/// # Arguments
/// * `to_client` - Channel to send sync instructions to
/// * `interval_secs` - Interval between pings (0 = disabled, returns immediately)
///
/// # Returns
/// A handle that can be used to stop the keep-alive task
pub fn spawn_keepalive_task(
    to_client: mpsc::Sender<Bytes>,
    interval_secs: u64,
) -> Option<tokio::task::JoinHandle<()>> {
    if interval_secs == 0 {
        return None;
    }

    let handle = tokio::spawn(async move {
        let mut manager = KeepAliveManager::new(interval_secs);
        let mut ticker = interval(Duration::from_secs(interval_secs));

        loop {
            ticker.tick().await;

            if let Some(sync_instr) = manager.check() {
                if to_client.send(sync_instr).await.is_err() {
                    // Channel closed, stop the task
                    log::debug!("Keep-alive task stopping: channel closed");
                    break;
                }
                log::trace!("Keep-alive sync sent (frame {})", manager.frame_counter);
            }
        }
    });

    Some(handle)
}

/// Connection options for protocol handlers
#[derive(Debug, Clone)]
pub struct ConnectionOptions {
    /// Connection timeout in seconds (0 = OS default)
    pub connection_timeout_secs: u64,
    /// Keep-alive interval in seconds (0 = disabled)
    pub keepalive_interval_secs: u64,
}

impl Default for ConnectionOptions {
    fn default() -> Self {
        Self {
            connection_timeout_secs: DEFAULT_CONNECTION_TIMEOUT_SECS,
            keepalive_interval_secs: DEFAULT_KEEPALIVE_INTERVAL_SECS,
        }
    }
}

impl ConnectionOptions {
    /// Create from handler security settings
    pub fn from_security_settings(settings: &crate::HandlerSecuritySettings) -> Self {
        Self {
            connection_timeout_secs: settings.connection_timeout_secs,
            // Use default keepalive unless explicitly configured
            keepalive_interval_secs: DEFAULT_KEEPALIVE_INTERVAL_SECS,
        }
    }
}
