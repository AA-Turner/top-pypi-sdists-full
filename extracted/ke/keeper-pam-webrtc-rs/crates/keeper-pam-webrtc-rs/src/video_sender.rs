// VideoSender — concrete implementation of VideoOutput for keeper-pam-webrtc-rs.
//
// Wraps an RTCRtpSender + TrackLocalStaticSample pair.  On creation it spawns a dedicated
// task that polls RTCRtpSender::read_rtcp() and writes PLI/REMB results into shared
// atomics.  The encode loop in the guacr handler reads those atomics on each iteration
// without any extra tasks or channels on its side.

use guacr_handlers::EncodedFrame;
use guacr_handlers::{video::VideoOutput, HandlerError, Result};
use log::debug;
use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::task::AbortHandle;
use webrtc::media::Sample;
use webrtc::rtcp::payload_feedbacks::picture_loss_indication::PictureLossIndication;
use webrtc::rtcp::payload_feedbacks::receiver_estimated_maximum_bitrate::ReceiverEstimatedMaximumBitrate;
use webrtc::rtp_transceiver::rtp_sender::RTCRtpSender;
use webrtc::track::track_local::track_local_static_sample::TrackLocalStaticSample;

/// Minimum interval between keyframe responses to PLI.
/// Prevents a burst of PLIs from flooding the link with large IDR frames.
const PLI_MIN_INTERVAL: Duration = Duration::from_millis(500);

/// Rate-limits PLI responses so that a burst of PLIs cannot flood the link with IDR frames.
///
/// At most one keyframe is allowed per `PLI_MIN_INTERVAL`. Tested inline in the `#[cfg(test)]`
/// module; access the `last_keyframe_at` field from within the same module.
struct PliThrottle {
    last_keyframe_at: Instant,
}

impl PliThrottle {
    fn new() -> Self {
        // Set last_keyframe_at far enough in the past so the first PLI is always accepted.
        Self {
            last_keyframe_at: Instant::now() - PLI_MIN_INTERVAL,
        }
    }

    /// Returns `true` if enough time has elapsed since the last accepted PLI.
    ///
    /// When this returns `true` the caller should set the keyframe flag and update
    /// `last_keyframe_at` to `Instant::now()`.
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
    /// Set by the RTCP task when a PLI arrives and the throttle allows it.
    /// The encode loop swaps this to `false` (Acquire) before calling request_keyframe().
    keyframe_requested: Arc<AtomicBool>,
    /// Updated by the RTCP task when a REMB packet arrives.
    /// Value is bits/sec.  Zero = no feedback received yet.
    target_bitrate_bps: Arc<AtomicU32>,
    /// Aborts the RTCP reader task when this VideoSender is dropped.
    _rtcp_task: AbortHandle,
}

impl VideoSender {
    /// Create a VideoSender from the track and its associated RTCRtpSender.
    ///
    /// `rtp_sender` is the value returned by `RTCPeerConnection::add_track()`.
    /// It must stay alive for the duration of the session — keep it in the same
    /// struct that owns `VideoSender`.
    pub fn new(track: Arc<TrackLocalStaticSample>, rtp_sender: Arc<RTCRtpSender>) -> Self {
        let keyframe_flag = Arc::new(AtomicBool::new(false));
        let bitrate = Arc::new(AtomicU32::new(0));

        let flag_clone = keyframe_flag.clone();
        let bitrate_clone = bitrate.clone();

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
                                    debug!("VideoSender: PLI throttled (too soon)");
                                }
                            } else if let Some(remb) =
                                pkt_any.downcast_ref::<ReceiverEstimatedMaximumBitrate>()
                            {
                                let bps = remb.bitrate as u32;
                                bitrate_clone.store(bps, Ordering::Relaxed);
                                debug!("VideoSender: REMB target = {} bps", bps);
                            }
                        }
                    }
                    Err(e) => {
                        // read_rtcp errors when the sender is stopped — normal on teardown
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
            _rtcp_task: handle,
        }
    }
}

#[async_trait::async_trait]
impl VideoOutput for VideoSender {
    async fn send_frame(&self, frame: EncodedFrame) -> Result<()> {
        self.track
            .write_sample(&Sample {
                data: frame.data,
                duration: Duration::from_millis(16), // nominal 60fps frame duration
                ..Default::default()
            })
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
}

impl Drop for VideoSender {
    fn drop(&mut self) {
        // Abort the RTCP reader task so it doesn't outlive the sender.
        self._rtcp_task.abort();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pli_min_interval_is_500ms() {
        assert_eq!(PLI_MIN_INTERVAL, Duration::from_millis(500));
    }

    #[test]
    fn test_pli_throttle_first_call_allowed() {
        let mut t = PliThrottle::new();
        assert!(t.should_respond(), "first call must be allowed");
    }

    #[test]
    fn test_pli_throttle_second_call_blocked() {
        let mut t = PliThrottle::new();
        assert!(t.should_respond());
        assert!(!t.should_respond(), "immediate second call must be blocked");
    }

    #[test]
    fn test_pli_throttle_allowed_after_interval() {
        let mut t = PliThrottle::new();
        assert!(t.should_respond());
        // Wind the clock back past the minimum interval.
        t.last_keyframe_at = Instant::now() - Duration::from_millis(600);
        assert!(t.should_respond(), "call after 600ms must be allowed");
    }
}
