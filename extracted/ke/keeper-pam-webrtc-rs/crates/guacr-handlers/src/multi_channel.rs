// Simple multi-channel sender for WebRTC data channels
//
// Distributes video frames across multiple channels using round-robin.
// Drops oversized frames (video codec handles missing frames gracefully).

use bytes::Bytes;
use log::warn;
use parking_lot::Mutex;
use std::sync::Arc;

/// Simple multi-channel sender for WebRTC data channels
///
/// Distributes video frames across multiple channels using round-robin.
/// Frames are sent whole (no fragmentation) - if a frame is too large, it's dropped.
///
/// This is simpler than fragmentation-based multi-channel because:
/// - No reassembly needed on client
/// - Video codec handles missing frames gracefully
/// - Lower latency (no fragmentation overhead)
pub struct SimpleMultiChannelSender {
    channels: Vec<Arc<dyn WebRTCDataChannel>>,
    current_channel: Arc<Mutex<usize>>,
    max_payload_size: usize,
}

/// Trait for WebRTC data channel (adapt to your actual type)
pub trait WebRTCDataChannel: Send + Sync {
    /// Send data on this channel
    fn send(&self, data: Bytes) -> Result<(), String>;
}

impl SimpleMultiChannelSender {
    /// Create a new simple multi-channel sender
    ///
    /// # Arguments
    ///
    /// * `channels` - Vector of WebRTC data channels
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// use guacr_handlers::{SimpleMultiChannelSender, WebRTCDataChannel};
    /// use bytes::Bytes;
    /// use std::sync::Arc;
    ///
    /// struct MyChannel;
    /// impl WebRTCDataChannel for MyChannel {
    ///     fn send(&self, _data: Bytes) -> Result<(), String> { Ok(()) }
    /// }
    ///
    /// let channels: Vec<Arc<dyn WebRTCDataChannel>> = vec![
    ///     Arc::new(MyChannel),
    ///     Arc::new(MyChannel),
    ///     Arc::new(MyChannel),
    /// ];
    /// let sender = SimpleMultiChannelSender::new(channels);
    /// ```
    pub fn new(channels: Vec<Arc<dyn WebRTCDataChannel>>) -> Self {
        use guacr_protocol::MAX_SAFE_PAYLOAD_SIZE;

        Self {
            channels,
            current_channel: Arc::new(Mutex::new(0)),
            max_payload_size: MAX_SAFE_PAYLOAD_SIZE,
        }
    }

    /// Send a video frame
    ///
    /// # Arguments
    ///
    /// * `frame` - Video frame data (e.g., H.264 NAL units)
    ///
    /// # Returns
    ///
    /// `Ok(())` if frame was sent or dropped (oversized frames are dropped).
    /// `Err(String)` if channel send failed.
    ///
    /// # Behavior
    ///
    /// - Frames within limit: Sent on next channel (round-robin)
    /// - Frames over limit: Dropped with warning (video codec handles missing frames)
    pub fn send_frame(&self, frame: Bytes) -> Result<(), String> {
        // Check payload size (before overhead)
        if frame.len() > self.max_payload_size {
            warn!(
                "Frame payload too large ({} bytes > {} bytes), dropping",
                frame.len(),
                self.max_payload_size
            );
            // Drop frame - video codec handles missing frames
            return Ok(());
        }

        if self.channels.is_empty() {
            return Err("No channels available".to_string());
        }

        // Round-robin to channel
        // Using parking_lot::Mutex which doesn't poison on panic
        let channel_idx = {
            let mut idx = self.current_channel.lock();
            let current = *idx;
            *idx = (*idx + 1) % self.channels.len();
            current
        };

        self.channels[channel_idx].send(frame)
    }

    /// Get the maximum payload size (before protocol overhead)
    pub fn max_payload_size(&self) -> usize {
        self.max_payload_size
    }

    /// Get the number of channels
    pub fn channel_count(&self) -> usize {
        self.channels.len()
    }
}
