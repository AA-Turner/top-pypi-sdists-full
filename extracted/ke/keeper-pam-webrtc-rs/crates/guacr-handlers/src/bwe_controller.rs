// Bandwidth Estimation Controller — drives encoder bitrate cap and resolution
// step-down in response to REMB/TWCC feedback from the browser.
//
// Lives in guacr-handlers (no WebRTC dependency) so it can be tested in
// isolation. VideoSender in keeper-pam-webrtc-rs owns a BweController and
// calls update_bwe() each time a REMB packet arrives.

use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};

/// Resolution tiers as a PERCENTAGE of the session's natural size, highest first.
///
/// Percentages rather than absolute sizes, because `VideoSender::new` never receives the
/// session's natural resolution and this controller is moved into a spawned RTCP task that
/// handlers cannot reach — so an absolute ladder cannot know what "full resolution" means.
/// It also makes three former defects unrepresentable: no cliff (first step is 100 -> 75,
/// where the old ladder jumped from natural straight to a fixed 1280x720), full resolution
/// is always recoverable (ceiling is 100%, where the old ceiling was a hardcoded 1920x1080),
/// and a window smaller than 1920x1080 can never be upscaled (nothing exceeds 100%).
const TIERS_PCT: &[u32] = &[100, 75, 50, 33];

/// BWE must stay below STEP_DOWN_RATIO * current_bitrate for this long before
/// stepping down one resolution tier.
const STEP_DOWN_RATIO: f64 = 0.50;
const STEP_DOWN_HOLD: Duration = Duration::from_millis(2000);

/// BWE must stay above STEP_UP_RATIO * current_bitrate for this long before
/// stepping up one resolution tier.
const STEP_UP_RATIO: f64 = 0.90;
const STEP_UP_HOLD: Duration = Duration::from_millis(5000);

/// Below this bitrate the encoder is not useful. Signal a keyframe request so
/// the decoder can recover cleanly when bandwidth recovers.
const BITRATE_FLOOR_BPS: u32 = 200_000;

/// Drives encoder bitrate and resolution based on REMB/TWCC bandwidth estimates.
///
/// Call `update_bwe(bps)` each time the WebRTC backend delivers a bandwidth
/// estimate. The controller updates shared atomics that the handler reads on
/// every encode iteration — no channels, no extra tasks.
pub struct BweController {
    target_bitrate_bps: Arc<AtomicU32>,
    resolution_scale_pct: Arc<AtomicU32>,
    keyframe_requested: Arc<AtomicBool>,

    /// Index into TIERS for the current resolution (0 = highest).
    current_tier: usize,
    low_bwe_since: Option<Instant>,
    high_bwe_since: Option<Instant>,
    /// Last bitrate stored (used as the "current" baseline for ratio checks).
    last_bps: u32,
    /// Frozen baseline bps captured when a hold timer starts.
    /// Prevents a sustained BWE drop from readjusting the threshold each sample
    /// and inadvertently resetting the hold timer.
    hold_baseline_bps: u32,
}

impl BweController {
    /// Create a BweController sharing the same atomics as VideoSender / VideoOutput.
    ///
    /// `resolution_scale_pct` starts at 100 (full natural resolution). Handlers apply it
    /// with `crate::video::scaled_encode_size`.
    pub fn new(
        target_bitrate_bps: Arc<AtomicU32>,
        resolution_scale_pct: Arc<AtomicU32>,
        keyframe_requested: Arc<AtomicBool>,
    ) -> Self {
        resolution_scale_pct.store(TIERS_PCT[0], Ordering::Relaxed);
        Self {
            target_bitrate_bps,
            resolution_scale_pct,
            keyframe_requested,
            current_tier: 0, // start at the highest tier (100% of natural)
            low_bwe_since: None,
            high_bwe_since: None,
            last_bps: 0,
            hold_baseline_bps: 0,
        }
    }

    /// Process a new bandwidth estimate from REMB or TWCC.
    ///
    /// Always updates `target_bitrate_bps` immediately.
    /// Applies resolution step-down / step-up after the hysteresis thresholds
    /// are met.
    ///
    /// Keyframe behaviour:
    /// - Step-DOWN: no keyframe — IDR would spike bandwidth at exactly the wrong
    ///   moment. The encoder just starts producing smaller frames.
    /// - Step-UP: keyframe requested — the higher-resolution render needs a clean
    ///   IDR to look right. Rate-limited by PliThrottle in VideoSender.
    /// - Below floor: keyframe requested so the decoder recovers when bandwidth
    ///   returns.
    pub fn update_bwe(&mut self, bps: u32) {
        self.target_bitrate_bps.store(bps, Ordering::Relaxed);

        if bps < BITRATE_FLOOR_BPS {
            // Signal keyframe so decoder recovers cleanly when bandwidth returns.
            self.keyframe_requested.store(true, Ordering::Release);
            self.low_bwe_since = None;
            self.high_bwe_since = None;
            self.hold_baseline_bps = 0;
            self.last_bps = bps;
            return;
        }

        // Use a frozen baseline while a hold timer is running so that a sustained
        // BWE drop (5M → 1M → 1M → 1M) does not readjust the threshold each sample
        // and inadvertently reset the timer before STEP_DOWN_HOLD elapses.
        let effective_baseline = if (self.low_bwe_since.is_some() || self.high_bwe_since.is_some())
            && self.hold_baseline_bps > 0
        {
            self.hold_baseline_bps
        } else if self.last_bps == 0 {
            bps
        } else {
            self.last_bps
        };
        self.last_bps = bps;

        let low_threshold = (effective_baseline as f64 * STEP_DOWN_RATIO) as u32;
        let high_threshold = (effective_baseline as f64 * STEP_UP_RATIO) as u32;

        if bps < low_threshold {
            // Sustained low BWE → consider stepping down
            self.high_bwe_since = None;
            if self.low_bwe_since.is_none() {
                self.hold_baseline_bps = effective_baseline;
                self.low_bwe_since = Some(Instant::now());
            }
            if let Some(since) = self.low_bwe_since {
                if since.elapsed() >= STEP_DOWN_HOLD {
                    self.step_down();
                    self.low_bwe_since = None;
                    self.hold_baseline_bps = 0;
                }
            }
        } else if bps > high_threshold {
            // Sustained high BWE → consider stepping up
            self.low_bwe_since = None;
            if self.high_bwe_since.is_none() {
                self.hold_baseline_bps = effective_baseline;
                self.high_bwe_since = Some(Instant::now());
            }
            if let Some(since) = self.high_bwe_since {
                if since.elapsed() >= STEP_UP_HOLD {
                    self.step_up();
                    self.high_bwe_since = None;
                    self.hold_baseline_bps = 0;
                }
            }
        } else {
            self.low_bwe_since = None;
            self.high_bwe_since = None;
            self.hold_baseline_bps = 0;
        }
    }

    fn step_down(&mut self) {
        let next = self.current_tier + 1;
        if next < TIERS_PCT.len() {
            self.current_tier = next;
            self.resolution_scale_pct
                .store(TIERS_PCT[next], Ordering::Relaxed);
            // No keyframe on step-down — avoids spiking bandwidth when congested.
        }
    }

    fn step_up(&mut self) {
        if self.current_tier > 0 {
            self.current_tier -= 1;
            self.resolution_scale_pct
                .store(TIERS_PCT[self.current_tier], Ordering::Relaxed);
            // Keyframe on step-up so the higher-resolution render is clean.
            self.keyframe_requested.store(true, Ordering::Release);
        }
    }

    /// Current resolution tier index (0 = highest). Exposed for testing.
    #[cfg(test)]
    pub fn current_tier(&self) -> usize {
        self.current_tier
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn make_controller() -> BweController {
        BweController::new(
            Arc::new(AtomicU32::new(0)),
            Arc::new(AtomicU32::new(0)),
            Arc::new(AtomicBool::new(false)),
        )
    }

    #[test]
    fn test_initial_tier_is_highest() {
        let c = make_controller();
        assert_eq!(c.current_tier(), 0);
    }

    // ---------------------------------------------------------------------
    // Tier ladder — regression cover for three defects that the old absolute
    // ladder [(1920,1080),(1280,720),(960,540),(640,480)] exhibited and that
    // percentage tiers make unrepresentable. Written as failing tests against the
    // old design on 2026-08-03, then rewritten here to lock in the fix.
    // ---------------------------------------------------------------------

    /// FIXED (was: cliff). The old ladder jumped from natural straight to a fixed
    /// 1280x720 — a ~4.6x pixel drop for a 3292x1724 session. Now the first step is
    /// 100% -> 75%, which is 56% of the pixels: a real step, not a cliff.
    #[test]
    fn first_step_down_is_a_gentle_tier_not_a_cliff() {
        let pct = Arc::new(AtomicU32::new(0));
        let mut c = BweController::new(
            Arc::new(AtomicU32::new(0)),
            pct.clone(),
            Arc::new(AtomicBool::new(false)),
        );
        assert_eq!(
            pct.load(Ordering::Relaxed),
            100,
            "starts at full resolution"
        );

        c.step_down();
        assert_eq!(pct.load(Ordering::Relaxed), 75);

        // Pixel ratio is what matters, and it must stay well clear of the old cliff.
        let area_ratio = (75.0 * 75.0) / (100.0 * 100.0);
        assert!(
            area_ratio > 0.5,
            "one step should retain >50% of pixels, got {area_ratio:.2}"
        );
    }

    /// FIXED (was: native unrecoverable). The old ceiling was a hardcoded 1920x1080, so a
    /// Retina session could never climb back to its own resolution. The ceiling is now 100%.
    #[test]
    fn step_up_returns_all_the_way_to_full_resolution() {
        let pct = Arc::new(AtomicU32::new(0));
        let mut c = BweController::new(
            Arc::new(AtomicU32::new(0)),
            pct.clone(),
            Arc::new(AtomicBool::new(false)),
        );
        c.step_down();
        c.step_down();
        assert!(pct.load(Ordering::Relaxed) < 100);

        for _ in 0..8 {
            c.step_up();
        }
        assert_eq!(c.current_tier(), 0);
        assert_eq!(
            pct.load(Ordering::Relaxed),
            100,
            "full natural resolution must be recoverable"
        );
    }

    /// FIXED (was: upscaling small windows). The old ladder wrote absolute 1920x1080 on
    /// step-up, exceeding a 1024x768 session. A percentage can never exceed natural size.
    #[test]
    fn no_tier_ever_exceeds_the_sessions_natural_size() {
        for &t in TIERS_PCT {
            assert!(t <= 100, "tier {t}% would upscale");
        }
        // And the same holds once applied to a small session.
        let (natural_w, natural_h) = (1024u32, 768u32);
        for &t in TIERS_PCT {
            let (w, h) = crate::video::scaled_encode_size(natural_w, natural_h, t);
            assert!(
                w <= natural_w && h <= natural_h,
                "tier {t}% -> {w}x{h} exceeds {natural_w}x{natural_h}"
            );
        }
    }

    /// Tiers must descend strictly, or step_down/step_up would not change anything.
    #[test]
    fn tiers_are_strictly_descending() {
        for pair in TIERS_PCT.windows(2) {
            assert!(pair[0] > pair[1], "tiers must descend: {pair:?}");
        }
    }

    #[test]
    fn test_bwe_updates_target_bitrate_immediately() {
        let bps_atom = Arc::new(AtomicU32::new(0));
        let mut c = BweController::new(
            bps_atom.clone(),
            Arc::new(AtomicU32::new(0)),
            Arc::new(AtomicBool::new(false)),
        );
        c.update_bwe(5_000_000);
        assert_eq!(bps_atom.load(Ordering::Relaxed), 5_000_000);
    }

    #[test]
    fn test_no_step_down_before_hold_period() {
        let mut c = make_controller();
        c.last_bps = 5_000_000;
        // Low BWE but instant — should NOT step down yet
        c.update_bwe(1_000_000); // 20% of 5Mbps
        assert_eq!(
            c.current_tier(),
            0,
            "should not step down before hold period"
        );
    }

    #[test]
    fn test_step_down_after_hold_period() {
        let mut c = make_controller();
        c.last_bps = 5_000_000;
        // Manually set low_bwe_since to past the hold period
        c.low_bwe_since = Some(Instant::now() - STEP_DOWN_HOLD - Duration::from_millis(100));
        c.update_bwe(1_000_000);
        assert_eq!(c.current_tier(), 1, "should step down to 720p");
    }

    #[test]
    fn test_step_up_after_hold_period() {
        let mut c = make_controller();
        c.current_tier = 2; // start at 960×540
        c.last_bps = 2_000_000;
        c.high_bwe_since = Some(Instant::now() - STEP_UP_HOLD - Duration::from_millis(100));
        c.update_bwe(2_000_000); // same as current → above 90%
        assert_eq!(c.current_tier(), 1, "should step up to 720p");
    }

    #[test]
    fn test_no_step_below_floor_requests_keyframe() {
        let keyframe = Arc::new(AtomicBool::new(false));
        let mut c = BweController::new(
            Arc::new(AtomicU32::new(0)),
            Arc::new(AtomicU32::new(0)),
            keyframe.clone(),
        );
        c.update_bwe(100_000); // below 200 kbps floor
        assert!(
            keyframe.load(Ordering::Relaxed),
            "keyframe should be requested below floor"
        );
    }

    #[test]
    fn test_step_down_does_not_request_keyframe() {
        let keyframe = Arc::new(AtomicBool::new(false));
        let mut c = BweController::new(
            Arc::new(AtomicU32::new(0)),
            Arc::new(AtomicU32::new(0)),
            keyframe.clone(),
        );
        c.last_bps = 5_000_000;
        c.low_bwe_since = Some(Instant::now() - STEP_DOWN_HOLD - Duration::from_millis(100));
        c.update_bwe(1_000_000);
        assert_eq!(c.current_tier(), 1);
        assert!(
            !keyframe.load(Ordering::Relaxed),
            "step-down must not request keyframe"
        );
    }

    #[test]
    fn test_step_up_requests_keyframe() {
        let keyframe = Arc::new(AtomicBool::new(false));
        let mut c = BweController::new(
            Arc::new(AtomicU32::new(0)),
            Arc::new(AtomicU32::new(0)),
            keyframe.clone(),
        );
        c.current_tier = 1;
        c.last_bps = 3_000_000;
        c.high_bwe_since = Some(Instant::now() - STEP_UP_HOLD - Duration::from_millis(100));
        c.update_bwe(3_000_000);
        assert_eq!(c.current_tier(), 0);
        assert!(
            keyframe.load(Ordering::Relaxed),
            "step-up must request keyframe"
        );
    }

    // Regression: sustained low BWE must not reset the hold timer each sample.
    // Previously last_bps was updated before the threshold check, so after a
    // 5M→1M drop the next call at 1M saw baseline=1M, threshold=500K, and
    // 1M > 500K cleared low_bwe_since — the timer never accumulated.
    #[test]
    fn test_sustained_low_bwe_does_not_reset_hold_timer() {
        let mut c = make_controller();
        c.last_bps = 5_000_000;

        // Call 1: 5M→1M starts the timer.
        c.update_bwe(1_000_000);
        assert!(
            c.low_bwe_since.is_some(),
            "hold timer must start on first low sample"
        );
        let t0 = c.low_bwe_since.unwrap();

        std::thread::sleep(Duration::from_millis(5));

        // Calls 2-3: sustained 1M — timer must NOT reset.
        c.update_bwe(1_000_000);
        c.update_bwe(1_000_000);
        assert!(
            c.low_bwe_since.is_some(),
            "hold timer must survive repeated low samples"
        );
        let t1 = c.low_bwe_since.unwrap();
        assert!(
            t1.duration_since(t0) < Duration::from_millis(2),
            "hold timer must not have been reset (t0={t0:?}, t1={t1:?})"
        );
        assert_eq!(
            c.current_tier(),
            0,
            "must not step down before hold period elapses"
        );
    }

    // Sustained high BWE must similarly not reset the step-up timer.
    #[test]
    fn test_sustained_high_bwe_does_not_reset_hold_timer() {
        let mut c = make_controller();
        c.current_tier = 2; // start below maximum
        c.last_bps = 1_000_000;

        // Call 1: 1M→5M starts the step-up timer.
        c.update_bwe(5_000_000);
        assert!(c.high_bwe_since.is_some(), "step-up timer must start");
        let t0 = c.high_bwe_since.unwrap();

        std::thread::sleep(Duration::from_millis(5));

        c.update_bwe(5_000_000);
        c.update_bwe(5_000_000);
        assert!(
            c.high_bwe_since.is_some(),
            "step-up timer must survive repeated high samples"
        );
        let t1 = c.high_bwe_since.unwrap();
        assert!(
            t1.duration_since(t0) < Duration::from_millis(2),
            "step-up timer must not have been reset (t0={t0:?}, t1={t1:?})"
        );
    }
}
