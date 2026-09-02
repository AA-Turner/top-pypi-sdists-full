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

    /// Returns the BWE-recommended encode resolution as a percentage of the session's
    /// natural size. 100 means "encode at full natural resolution".
    ///
    /// Updated by `BweController` as sustained bandwidth changes step the resolution tier.
    /// Handlers multiply their own natural dimensions by this and round to even (H.264
    /// requires even dimensions) — see `guacr_handlers::scaled_encode_size`.
    ///
    /// This is a percentage rather than absolute pixels on purpose. `VideoSender::new`
    /// never receives the session's natural size and the controller is moved into a
    /// spawned RTCP task that handlers cannot reach, so an absolute ladder could not know
    /// what "full resolution" meant. Expressing it relatively also makes three former
    /// defects unrepresentable: there is no cliff (the first step is 100 -> 75 rather than
    /// a jump to a fixed 720p), full resolution is always recoverable (the ceiling is 100%
    /// rather than a hardcoded 1920x1080), and a small window can never be upscaled
    /// (nothing exceeds 100%).
    fn resolution_scale_pct(&self) -> Arc<AtomicU32>;
}

/// Apply a BWE resolution scale percentage to a session's natural size.
///
/// Lives here so every handler rounds and bounds identically. H.264 requires even
/// dimensions, and a zero-sized frame would be rejected by the encoder, so both axes are
/// floored at 2. A `pct` of 0 (no recommendation yet) or >= 100 means full natural size.
pub fn scaled_encode_size(natural_w: u32, natural_h: u32, pct: u32) -> (u32, u32) {
    if natural_w == 0 || natural_h == 0 {
        return (natural_w, natural_h);
    }
    if pct == 0 || pct >= 100 {
        // Natural size still has to satisfy the even-dimension requirement.
        return (natural_w & !1, natural_h & !1);
    }
    let scale = |v: u32| -> u32 {
        let scaled = (v as u64 * pct as u64 / 100) as u32;
        (scaled.max(2)) & !1
    };
    (scale(natural_w), scale(natural_h))
}
