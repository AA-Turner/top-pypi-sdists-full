// VideoOutput trait — the interface between guacr protocol handlers and the WebRTC video track.
//
// Defined here (in guacr-handlers, a leaf crate) so all handler crates can depend on it
// without depending on keeper-pam-webrtc-rs.  The concrete VideoSender implementation that
// wraps TrackLocalStaticSample lives in keeper-pam-webrtc-rs and implements this trait.

use bytes::Bytes;
use std::sync::atomic::{AtomicBool, AtomicU32};
use std::sync::Arc;

/// A single encoded H.264 frame in Annex B format.
///
/// IDR frames are always in the form [SPS NALU][PPS NALU][IDR NALU].
/// P-frames contain one or more slice NALUs.
/// All NALUs use 4-byte Annex B start codes (0x00000001).
pub struct EncodedFrame {
    /// Complete Annex B bitstream. Ready to hand directly to webrtc-rs write_sample.
    pub data: Bytes,
    pub is_keyframe: bool,
    /// Presentation timestamp in 90 kHz RTP clock units.
    pub pts: u64,
}

/// Sends encoded H.264 frames to the browser over RTCRtpSender.
///
/// Handlers receive an `Option<Arc<dyn VideoOutput>>` via `ProtocolHandler::connect`.
/// `None` means the session is GuacamoleOnly (terminal protocols, old vault clients,
/// guacd proxy sessions, encoder initialisation failure) — the handler falls back to
/// JPEG dirty-rect encoding as normal.
#[async_trait::async_trait]
pub trait VideoOutput: Send + Sync {
    /// Send one encoded H.264 frame to the browser.
    ///
    /// The frame's `data` field must be a valid Annex B bitstream.
    /// IDR frames must be in the form \[SPS\]\[PPS\]\[IDR NALU\].
    async fn send_frame(&self, frame: EncodedFrame) -> crate::error::Result<()>;

    /// Returns the keyframe-request flag.
    ///
    /// Set to `true` by VideoSender's internal RTCP task when a PLI arrives from the browser
    /// (already rate-limited to at most once per 500 ms).  The encode loop must swap it to
    /// `false` with `Ordering::Acquire` before calling `encoder.request_keyframe()`.
    fn keyframe_requested(&self) -> Arc<AtomicBool>;

    /// Returns the current REMB target bitrate in bits per second.
    ///
    /// Updated by VideoSender's internal RTCP task when a REMB packet arrives.
    /// Zero means no feedback received yet — keep the current encoder bitrate.
    fn target_bitrate_bps(&self) -> Arc<AtomicU32>;
}
