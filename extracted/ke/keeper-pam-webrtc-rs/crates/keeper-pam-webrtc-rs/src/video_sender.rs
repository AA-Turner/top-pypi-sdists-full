// VideoSender — concrete implementation of VideoOutput for keeper-pam-webrtc-rs.
//
// Wraps an RTCRtpSender + TrackLocalStaticSample pair.  On creation it spawns a
// dedicated task that polls RTCRtpSender::read_rtcp() and feeds REMB estimates
// into BweController (which updates target_bitrate_bps and resolution_scale_pct)
// and sets keyframe_requested on PLI.
//
// The encode loop in the guacr handler reads the shared atomics on each iteration
// without any extra tasks or channels on its side.

use guacr_handlers::{video::VideoOutput, BweController, EncodedFrame, HandlerError, Result};
use log::{debug, info};
use std::sync::atomic::{AtomicBool, AtomicU32, AtomicU64, Ordering};
use std::sync::Arc;
use std::sync::OnceLock;
use std::time::{Duration, Instant};
use tokio::task::AbortHandle;
use webrtc::media::Sample;
use webrtc::rtcp::payload_feedbacks::picture_loss_indication::PictureLossIndication;
use webrtc::rtcp::payload_feedbacks::receiver_estimated_maximum_bitrate::ReceiverEstimatedMaximumBitrate;
use webrtc::rtp::extension::playout_delay_extension::{
    PlayoutDelayExtension, PLAYOUT_DELAY_MAX_VALUE,
};
use webrtc::rtp::extension::HeaderExtension;
use webrtc::rtp_transceiver::rtp_sender::RTCRtpSender;
use webrtc::track::track_local::track_local_static_sample::TrackLocalStaticSample;

/// Minimum interval between keyframe responses to PLI.
const PLI_MIN_INTERVAL: Duration = Duration::from_millis(500);

/// Duration attributed to the first frame, before an interval can be measured.
const FIRST_FRAME_DURATION: Duration = Duration::from_millis(33);

/// Never advance the RTP clock by zero: two frames sharing one timestamp are read
/// by receivers as packets belonging to a single frame, which merges them.
const MIN_FRAME_DURATION: Duration = Duration::from_millis(1);

/// Ceiling on a single frame's timestamp advance. Screen content legitimately idles
/// for long stretches, but an unbounded gap would make one absurd timestamp jump.
const MAX_FRAME_DURATION: Duration = Duration::from_secs(10);

/// URI of the playout-delay RTP header extension. Must be registered on the
/// MediaEngine (see `webrtc_core`) or `write_sample_with_extensions` silently drops it.
pub const PLAYOUT_DELAY_URI: &str = "http://www.webrtc.org/experiments/rtp-hdrext/playout-delay";

/// Default upper bound on receiver playout buffering, in milliseconds.
///
/// Not zero on purpose. Zero tells the receiver to render as soon as a frame
/// arrives, which converts any arrival variance straight into visible stutter —
/// and this stream is measurably jittery (freezes observed with zero packet loss,
/// on a TURN-relayed path). 100ms is well under the ~66ms-and-climbing buffer
/// Chrome picks on its own for camera-tuned content, while still absorbing a
/// couple of late frames. Override with `GUACR_PLAYOUT_DELAY_MAX_MS`.
const DEFAULT_PLAYOUT_DELAY_MAX_MS: u32 = 100;

/// Wire granularity of the playout-delay extension: values are in units of 10ms.
const PLAYOUT_DELAY_UNIT_MS: u32 = 10;

/// The playout-delay extension to stamp on every video sample, resolved once.
///
/// `min_delay` is always 0 — there is never a reason to make a remote-desktop frame
/// wait longer than it must. `max_delay` is the tunable half.
fn playout_delay_extension() -> &'static Option<HeaderExtension> {
    static EXT: OnceLock<Option<HeaderExtension>> = OnceLock::new();
    EXT.get_or_init(|| {
        let max_ms = match std::env::var("GUACR_PLAYOUT_DELAY_MAX_MS") {
            Ok(raw) => match raw.trim().parse::<u32>() {
                Ok(v) => v,
                Err(_) => {
                    debug!(
                        "VideoSender: GUACR_PLAYOUT_DELAY_MAX_MS={raw:?} is not a number, using {}ms",
                        DEFAULT_PLAYOUT_DELAY_MAX_MS
                    );
                    DEFAULT_PLAYOUT_DELAY_MAX_MS
                }
            },
            Err(_) => DEFAULT_PLAYOUT_DELAY_MAX_MS,
        };

        // An explicit 0 disables the hint entirely rather than requesting
        // zero-buffering, which is the stutter-prone setting described above.
        if max_ms == 0 {
            info!("VideoSender: playout-delay hint disabled (GUACR_PLAYOUT_DELAY_MAX_MS=0)");
            return None;
        }

        let max_units = (max_ms / PLAYOUT_DELAY_UNIT_MS).min(PLAYOUT_DELAY_MAX_VALUE as u32) as u16;
        info!(
            "VideoSender: playout-delay hint min=0ms max={}ms",
            max_units as u32 * PLAYOUT_DELAY_UNIT_MS
        );
        Some(HeaderExtension::PlayoutDelay(PlayoutDelayExtension::new(
            0, max_units,
        )))
    })
}

/// Real elapsed time between two frames, for use as the RTP sample duration.
///
/// `TrackLocalStaticSample::write_sample` converts this straight into the RTP
/// timestamp advance (`samples = duration * clock_rate`), so it must track wall
/// clock or the RTP timeline drifts away from reality. Screen content is
/// inherently irregular — ~20ms while the user interacts, tens of seconds while
/// idle — and a fixed value makes the stream claim a frame rate it is not
/// delivering, which inflates the receiver's jitter buffer.
///
/// `prev_us == 0` means no previous frame has been written yet.
fn rtp_frame_duration(prev_us: u64, now_us: u64) -> Duration {
    if prev_us == 0 {
        return FIRST_FRAME_DURATION;
    }
    Duration::from_micros(now_us.saturating_sub(prev_us))
        .clamp(MIN_FRAME_DURATION, MAX_FRAME_DURATION)
}

struct PliThrottle {
    last_keyframe_at: Instant,
}

impl PliThrottle {
    fn new() -> Self {
        Self {
            last_keyframe_at: Instant::now() - PLI_MIN_INTERVAL,
        }
    }

    fn should_respond(&mut self) -> bool {
        if self.last_keyframe_at.elapsed() >= PLI_MIN_INTERVAL {
            self.last_keyframe_at = Instant::now();
            true
        } else {
            false
        }
    }
}

pub struct VideoSender {
    track: Arc<TrackLocalStaticSample>,
    keyframe_requested: Arc<AtomicBool>,
    target_bitrate_bps: Arc<AtomicU32>,
    resolution_scale_pct: Arc<AtomicU32>,
    /// Monotonic base for measuring real inter-frame intervals.
    start: Instant,
    /// Microseconds since `start` at which the previous frame was written; 0 until
    /// the first frame. Drives `rtp_frame_duration`.
    last_frame_us: AtomicU64,
    _rtcp_task: AbortHandle,
}

impl VideoSender {
    /// Create a VideoSender.
    ///
    /// `resolution_scale_pct` starts at 100 (full natural resolution); `BweController`
    /// lowers it as sustained bandwidth drops. Handlers apply it with
    /// `guacr_handlers::video::scaled_encode_size`.
    pub fn new(track: Arc<TrackLocalStaticSample>, rtp_sender: Arc<RTCRtpSender>) -> Self {
        let keyframe_flag = Arc::new(AtomicBool::new(false));
        let bitrate = Arc::new(AtomicU32::new(0));
        let scale_pct = Arc::new(AtomicU32::new(100));

        let mut bwe = BweController::new(bitrate.clone(), scale_pct.clone(), keyframe_flag.clone());

        let flag_clone = keyframe_flag.clone();

        let handle = tokio::spawn(async move {
            let mut throttle = PliThrottle::new();

            loop {
                match rtp_sender.read_rtcp().await {
                    Ok((packets, _attrs)) => {
                        for pkt in &packets {
                            let pkt_any = pkt.as_any();

                            if pkt_any.downcast_ref::<PictureLossIndication>().is_some() {
                                if throttle.should_respond() {
                                    flag_clone.store(true, Ordering::Release);
                                    debug!("VideoSender: PLI accepted, keyframe requested");
                                } else {
                                    debug!("VideoSender: PLI throttled");
                                }
                            } else if let Some(remb) =
                                pkt_any.downcast_ref::<ReceiverEstimatedMaximumBitrate>()
                            {
                                let bps = remb.bitrate as u32;
                                bwe.update_bwe(bps);
                                debug!(
                                    "VideoSender: REMB {:.1} Mbps → bwe updated",
                                    bps as f32 / 1_000_000.0
                                );
                            }
                        }
                    }
                    Err(e) => {
                        debug!("VideoSender: RTCP read stopped: {}", e);
                        break;
                    }
                }
            }
        })
        .abort_handle();

        Self {
            track,
            keyframe_requested: keyframe_flag,
            target_bitrate_bps: bitrate,
            resolution_scale_pct: scale_pct,
            start: Instant::now(),
            last_frame_us: AtomicU64::new(0),
            _rtcp_task: handle,
        }
    }
}

#[async_trait::async_trait]
impl VideoOutput for VideoSender {
    async fn send_frame(&self, frame: EncodedFrame) -> Result<()> {
        let now_us = self.start.elapsed().as_micros() as u64;
        let prev_us = self.last_frame_us.swap(now_us, Ordering::Relaxed);
        let duration = rtp_frame_duration(prev_us, now_us);

        let sample = Sample {
            data: frame.data,
            duration,
            ..Default::default()
        };

        // The hint has to ride every packet, not just the first: the receiver applies
        // the most recent value it has seen, and it is cheap (3 bytes).
        let extensions: &[HeaderExtension] = match playout_delay_extension() {
            Some(ext) => std::slice::from_ref(ext),
            None => &[],
        };

        self.track
            .write_sample_with_extensions(&sample, extensions)
            .await
            .map_err(|e| {
                HandlerError::ConnectionFailed(format!("video track write_sample failed: {}", e))
            })
    }

    fn keyframe_requested(&self) -> Arc<AtomicBool> {
        self.keyframe_requested.clone()
    }
    fn target_bitrate_bps(&self) -> Arc<AtomicU32> {
        self.target_bitrate_bps.clone()
    }
    fn resolution_scale_pct(&self) -> Arc<AtomicU32> {
        self.resolution_scale_pct.clone()
    }
}

impl Drop for VideoSender {
    fn drop(&mut self) {
        self._rtcp_task.abort();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pli_throttle_first_call_allowed() {
        let mut t = PliThrottle::new();
        assert!(t.should_respond());
    }

    #[test]
    fn test_pli_throttle_second_call_blocked() {
        let mut t = PliThrottle::new();
        assert!(t.should_respond());
        assert!(!t.should_respond());
    }

    #[test]
    fn test_pli_throttle_allowed_after_interval() {
        let mut t = PliThrottle::new();
        assert!(t.should_respond());
        t.last_keyframe_at = Instant::now() - Duration::from_millis(600);
        assert!(t.should_respond());
    }

    // ── RTP sample duration ──────────────────────────────────────────────────
    //
    // webrtc-rs turns Sample::duration directly into the RTP timestamp advance
    // (samples = duration * clock_rate). At the 90kHz video clock, 20ms must
    // advance 1800 ticks; a hardcoded 16ms always advanced 1440 regardless of the
    // real interval, so the RTP timeline drifted from wall clock and Chrome's
    // jitter buffer inflated to compensate.

    #[test]
    fn first_frame_uses_nominal_duration() {
        assert_eq!(rtp_frame_duration(0, 5_000_000), FIRST_FRAME_DURATION);
    }

    #[test]
    fn duration_tracks_real_interval() {
        // 21ms apart -> 21ms, not a fixed 16ms.
        assert_eq!(rtp_frame_duration(1_000, 22_000), Duration::from_millis(21));
    }

    #[test]
    fn identical_timestamps_never_produce_zero_duration() {
        // Two frames in the same microsecond must still advance the RTP clock, or
        // the receiver treats them as packets of one frame and merges them.
        assert_eq!(rtp_frame_duration(7_000, 7_000), MIN_FRAME_DURATION);
    }

    #[test]
    fn long_idle_gap_is_clamped() {
        // A 10-minute idle stretch must not produce a 10-minute timestamp jump.
        let ten_minutes_us = 600_000_000u64;
        assert_eq!(
            rtp_frame_duration(1_000, 1_000 + ten_minutes_us),
            MAX_FRAME_DURATION
        );
    }

    // ── playout-delay hint ───────────────────────────────────────────────────

    #[test]
    fn playout_delay_uri_matches_the_negotiated_extension() {
        // Must match what browsers put in the SDP extmap, or the MediaEngine
        // registration will not line up with the offer and the extension is dropped.
        assert_eq!(
            PLAYOUT_DELAY_URI,
            "http://www.webrtc.org/experiments/rtp-hdrext/playout-delay"
        );
    }

    #[test]
    fn default_max_delay_converts_ms_to_wire_units() {
        // The wire field is in 10ms units, so the 100ms default is 10 units. Getting
        // this wrong by a factor of 10 would silently ask for 1s of buffering.
        assert_eq!(DEFAULT_PLAYOUT_DELAY_MAX_MS / PLAYOUT_DELAY_UNIT_MS, 10);
    }

    #[test]
    fn min_delay_is_always_zero_and_max_is_within_wire_range() {
        // Whatever the env resolves to, the encoded values must be legal: marshal
        // rejects anything above PLAYOUT_DELAY_MAX_VALUE.
        if let Some(HeaderExtension::PlayoutDelay(ext)) = playout_delay_extension() {
            assert_eq!(
                ext.min_delay, 0,
                "a frame should never be held artificially"
            );
            assert!(ext.max_delay <= PLAYOUT_DELAY_MAX_VALUE);
        }
    }

    #[test]
    fn interval_is_not_fixed_across_irregular_frames() {
        // Screen content is bursty: a fast pair then a slow pair must yield
        // different durations, which is exactly what the old hardcoded value lost.
        let fast = rtp_frame_duration(1_000, 21_000);
        let slow = rtp_frame_duration(21_000, 521_000);
        assert_ne!(fast, slow);
        assert_eq!(fast, Duration::from_millis(20));
        assert_eq!(slow, Duration::from_millis(500));
    }
}
