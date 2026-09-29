"""
Configuration classes for advanced tracker.
This module provides configuration classes for the advanced tracker,
including parameters for tracking algorithms and thresholds.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TrackerConfig:
    """
    Configuration for advanced tracker.

    This class contains all the parameters needed to configure the tracking algorithm,
    including thresholds, buffer sizes, and algorithm-specific settings.

    Threshold Tuning Guide:
    - Lower thresholds = more lenient matching = fewer new track IDs = more stable counts
    - Higher thresholds = stricter matching = more new track IDs = potential count inflation

    Recommended defaults are optimized for count accuracy over precision.
    """

    # Tracking thresholds - OPTIMIZED for count accuracy
    # track_high_thresh: Detections above this use primary (stronger) matching
    # Lower = more detections use strong matching = better track continuity
    track_high_thresh: float = 0.5  # Was 0.7, lowered for better continuity

    # track_low_thresh: Minimum confidence for secondary matching
    track_low_thresh: float = 0.1

    # new_track_thresh: Minimum confidence to create a NEW track
    # Lower = objects with temporarily low confidence keep their ID instead of getting new one
    # CRITICAL for count accuracy when model confidence fluctuates
    new_track_thresh: float = 0.5  # Was 0.7, lowered to prevent ID inflation

    # match_thresh: IoU threshold for matching detections to tracks
    # Lower = more lenient matching = better track continuity during movement
    match_thresh: float = 0.5  # Was 0.8, lowered for better matching

    # Secondary matching thresholds
    # secondary_match_thresh: Used in Step 2 for low-confidence detection recovery
    secondary_match_thresh: float = 0.4  # Was 0.5, lowered for better recovery

    # unconfirmed_match_thresh: Used in Step 3 for matching unconfirmed tracks
    unconfirmed_match_thresh: float = 0.6  # Was 0.7, lowered for better matching

    # Duplicate removal threshold (IoU-based)
    # Higher values = more permissive = fewer false duplicate removals
    duplicate_removal_iou_thresh: float = 0.4  # Was 0.3, increased to reduce false removals

    # Buffer settings — expressed in SECONDS of stream time, not frames.
    #
    # The frame-count forms below carried wall-clock INTENT ("60 seconds at
    # 30fps") but were compared against a frame counter, so they only meant what
    # the comment said when every frame reached the tracker. Under sampling they
    # are wrong by the sampling factor: at 1-GOP-in-3 a 1800-frame grace is 180
    # seconds of wall clock, not 60, so dead tracks linger 3x too long and keep
    # stealing associations from genuinely new objects.
    #
    # ``max_lost_seconds`` / ``track_buffer_seconds`` are the real parameters.
    # The frame-count fields are kept for backward compatibility: when a caller
    # passes one, ``__post_init__`` converts it to seconds via ``reference_fps``
    # (so an existing max_time_lost=1800 keeps meaning 60s exactly). When a
    # caller passes neither, the frame-count fields are back-filled from the
    # seconds fields so anything reading ``config.max_time_lost`` still works.
    max_lost_seconds: float = 60.0  # seconds a lost track survives before removal
    track_buffer_seconds: float = 20.0  # seconds of track buffer (600 frames @30fps)

    # Deprecated frame-count forms. None => derive from the seconds fields above.
    track_buffer: Optional[int] = None
    max_time_lost: Optional[int] = None  # frames; converted via reference_fps

    # Algorithm settings
    fuse_score: bool = True
    enable_gmc: bool = True
    gmc_method: str = "sparseOptFlow"  # "orb", "sift", "ecc", "sparseOptFlow", "none"
    gmc_downscale: int = 2

    # Frame rate (used for max_time_lost calculation)
    frame_rate: int = 30

    # Class aggregation settings
    enable_class_aggregation: bool = False
    class_aggregation_window_size: int = 30

    # Track recovery settings - for re-identifying objects that re-enter after being lost
    enable_track_recovery: bool = True
    track_recovery_iou_thresh: float = 0.3  # IoU threshold to consider same object
    track_recovery_time_window: float = 30.0  # Seconds to keep lost tracks for recovery

    # State persistence settings - for preserving counts across restarts
    enable_state_persistence: bool = True
    state_save_interval: int = 300  # Save state every N frames (~10 seconds at 30fps)
    state_expiry_seconds: float = 3600.0  # 1 hour - state older than this is not restored

    # -------------------------------------------------------------------------
    # CCTVTracker-parity features (all OFF by default -> behavior unchanged).
    # Ported from the legacy CCTVTracker so it can be retired with zero loss.
    # See ADVANCED_TRACKER_IMPROVEMENTS.md.
    # -------------------------------------------------------------------------

    # FPS adaptation: rescale the time-dependent params (Kalman dt, match/
    # new-track thresholds, the grace) to the real frame interval, so a 5-fps and
    # a 30-fps camera both track well. The interval comes from the frame's own
    # timestamp when update(timestamp=...) is given one, and only otherwise from
    # averaged wall-clock update() spacing (the ONLY path that touches the clock).
    #
    # DEFAULT OFF, measured rather than assumed, on two rigs that agree:
    # MOT17-val's published ground truth (scripts/sg24_mot17_rig.py, 7 FRCNN
    # sequences x 3 strides x 2 burst patterns) and the rtsp_exps sampler
    # benchmark (scripts/sg24_rtp_dt_bench.py). Both show the per-frame dt
    # estimator beating the wall-clock average — decisively so under a bursty
    # sampler, +10.6 points of IDF1 recovery, and a tie under a constant stride
    # where the average IS the per-frame interval — yet adaptation of either kind
    # still scoring at or below leaving it off. Two separate causes, separated by
    # the bounded-extrapolation sweep: under a BURST, extrapolating constant
    # velocity across a multi-second gap displaces the predicted box further than
    # the relaxed thresholds recover; under a CONSTANT STRIDE the gaps are far
    # too short for that and the loss comes from the threshold relaxation and
    # grace rescale instead. Bounding the extrapolation (`max_extrapolation_sec`
    # below) was swept over ten ceilings and does not recover either. Numbers and
    # reasoning are in this package's README. Turning this on is a behavioural
    # change for every consumer, bought with a measured regression.
    enable_fps_adaptation: bool = False
    reference_fps: int = 30  # fps at which the base thresholds/dt are calibrated
    # At low fps, thresholds relax toward these floors (objects move more/frame).
    match_thresh_low_fps_floor: float = 0.4
    new_track_thresh_low_fps_floor: float = 0.3
    # Explicit override for the lost-track grace, in seconds. None (default)
    # uses `max_lost_seconds` (itself derived from a caller-supplied
    # max_time_lost when one was given), so adaptation rescales the caller's own
    # grace instead of silently replacing it. Set this to pin the grace in
    # seconds regardless of any frame-count field.
    grace_period_sec: Optional[float] = None
    # Upper bound on the fps that auto-detection may infer. Wall-clock update()
    # spacing is meaningless for batched/offline replay (frames arrive back to
    # back), which would otherwise drive dt -> 0 and max_time_lost -> millions.
    max_detected_fps: float = 120.0
    # Lower bound on the inferred fps, i.e. an upper bound on how long a gap the
    # time base can represent (0.1 fps == a 10 s gap). This used to be hardcoded
    # at 1.0, which silently collapsed every gap longer than one second to
    # "1 fps" — exactly the multi-second bursty gaps a sampler produces and the
    # ones that break association. Raise it to clamp harder.
    min_detected_fps: float = 0.1

    # Bounded extrapolation. Ceiling, in seconds of stream time, on how far ONE
    # Kalman propagation step may carry the constant-velocity term. Only the
    # motion matrix is clamped; the lost-track grace and the relaxed thresholds
    # keep using the true measured interval, so the ageing stays correct.
    #
    # Why a bound is even plausible: `KalmanFilter.predict` scales F's velocity
    # block by dt but does NOT scale the process noise by dt, so a multi-second
    # gap moves the predicted mean by v*dt while leaving the covariance the size
    # it had at 30 fps — the box is confidently in the wrong place, and IoU
    # association sees a miss rather than a widened gate.
    #
    # DEFAULT None = unbounded = pre-existing behaviour. Swept over
    # {0.1, 0.2, 0.33, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0} s on the same MOT17 rig
    # as the flag itself. Result: inert under a constant stride (the gaps are
    # already shorter than any useful ceiling), and on bursts it moves the number
    # around by a few points without reaching a win — adjacent ceilings differ by
    # up to 14 points of recovery, which is noise, and no ceiling is best in more
    # than one sampling pattern. So there is nothing to default it to and
    # `enable_fps_adaptation` stays off. Numbers in the package README.
    max_extrapolation_sec: Optional[float] = None

    # Temporal confirmation (ghost suppression): a track is only EMITTED after it
    # has been hit in >= min_hits of the last `window` frames, suppressing 1-2
    # frame false positives (shadows, reflections). Gates emission + counting,
    # not lifecycle, so recovery/re-ID still see every track.
    enable_temporal_confirmation: bool = False
    confirm_window_sec: float = 0.17  # sliding window length (scaled by effective fps)
    confirm_min_hits_ratio: float = 0.6  # fraction of window frames that must be hits

    # predict() gap-glide: when True, update([]) advances all confirmed tracks one
    # frame via Kalman predict-only (smooth box glide on rendered frames between
    # inference frames). Default False preserves the "empty in -> empty out" contract.
    enable_predict_on_empty: bool = False
    # Hard bound on how long a track may glide without any detection evidence.
    # update([]) cannot distinguish "no inference this frame" from "the detector
    # genuinely saw nothing", so without this a subject leaving the scene would
    # leave a phantom box gliding forever. A track unseen for longer than this is
    # demoted to lost (normal lost/removal machinery then applies) and stops being
    # emitted. Interleaved predict/update streams refresh the timer every real
    # inference frame and never trip it.
    predict_glide_grace_sec: float = 1.0

    def __post_init__(self):
        """Validate configuration parameters."""
        self._normalize_time_budgets()

        if not 0.0 <= self.track_high_thresh <= 1.0:
            raise ValueError(
                f"track_high_thresh must be between 0.0 and 1.0, got {self.track_high_thresh}"
            )

        if not 0.0 <= self.track_low_thresh <= 1.0:
            raise ValueError(
                f"track_low_thresh must be between 0.0 and 1.0, got {self.track_low_thresh}"
            )

        if not 0.0 <= self.new_track_thresh <= 1.0:
            raise ValueError(
                f"new_track_thresh must be between 0.0 and 1.0, got {self.new_track_thresh}"
            )

        if not 0.0 <= self.match_thresh <= 1.0:
            raise ValueError(f"match_thresh must be between 0.0 and 1.0, got {self.match_thresh}")

        if self.track_buffer is not None and self.track_buffer <= 0:
            raise ValueError(f"track_buffer must be positive, got {self.track_buffer}")

        if self.frame_rate <= 0:
            raise ValueError(f"frame_rate must be positive, got {self.frame_rate}")

        if self.gmc_method not in ["orb", "sift", "ecc", "sparseOptFlow", "none"]:
            raise ValueError(f"Invalid gmc_method: {self.gmc_method}")

        if self.class_aggregation_window_size <= 0:
            raise ValueError(
                f"class_aggregation_window_size must be positive, got {self.class_aggregation_window_size}"
            )

        # CCTVTracker-parity feature validation
        if self.reference_fps <= 0:
            raise ValueError(f"reference_fps must be positive, got {self.reference_fps}")

        if not 0.0 <= self.match_thresh_low_fps_floor <= 1.0:
            raise ValueError(
                f"match_thresh_low_fps_floor must be between 0.0 and 1.0, got {self.match_thresh_low_fps_floor}"
            )

        if not 0.0 <= self.new_track_thresh_low_fps_floor <= 1.0:
            raise ValueError(
                f"new_track_thresh_low_fps_floor must be between 0.0 and 1.0, got {self.new_track_thresh_low_fps_floor}"
            )

        if self.grace_period_sec is not None and self.grace_period_sec <= 0:
            raise ValueError(
                f"grace_period_sec must be positive or None, got {self.grace_period_sec}"
            )

        if self.max_detected_fps <= 0:
            raise ValueError(f"max_detected_fps must be positive, got {self.max_detected_fps}")

        if self.min_detected_fps <= 0:
            raise ValueError(f"min_detected_fps must be positive, got {self.min_detected_fps}")

        if self.min_detected_fps > self.max_detected_fps:
            raise ValueError(
                f"min_detected_fps ({self.min_detected_fps}) must not exceed "
                f"max_detected_fps ({self.max_detected_fps})"
            )

        if self.max_extrapolation_sec is not None and self.max_extrapolation_sec <= 0:
            raise ValueError(
                f"max_extrapolation_sec must be positive or None, got {self.max_extrapolation_sec}"
            )

        if self.predict_glide_grace_sec <= 0:
            raise ValueError(
                f"predict_glide_grace_sec must be positive, got {self.predict_glide_grace_sec}"
            )

        if self.confirm_window_sec <= 0:
            raise ValueError(f"confirm_window_sec must be positive, got {self.confirm_window_sec}")

        if not 0.0 <= self.confirm_min_hits_ratio <= 1.0:
            raise ValueError(
                f"confirm_min_hits_ratio must be between 0.0 and 1.0, got {self.confirm_min_hits_ratio}"
            )

    def _normalize_time_budgets(self) -> None:
        """Reconcile the seconds-based budgets with the deprecated frame counts.

        An explicitly supplied frame count wins and is read as
        ``frames / reference_fps`` seconds — the meaning its comment always
        claimed — so every existing caller keeps its configured grace. When no
        frame count is given, the frame-count attributes are back-filled from
        the seconds fields so external readers of ``config.max_time_lost`` /
        ``config.track_buffer`` keep seeing an int.
        """
        ref = float(self.reference_fps) if self.reference_fps > 0 else 30.0

        if self.max_time_lost is not None:
            self.max_time_lost = int(self.max_time_lost)
            if self.max_time_lost <= 0:
                raise ValueError(f"max_time_lost must be positive, got {self.max_time_lost}")
            self.max_lost_seconds = float(self.max_time_lost) / ref
        else:
            if self.max_lost_seconds <= 0:
                raise ValueError(f"max_lost_seconds must be positive, got {self.max_lost_seconds}")
            self.max_lost_seconds = float(self.max_lost_seconds)
            self.max_time_lost = max(1, int(round(self.max_lost_seconds * ref)))

        if self.track_buffer is not None:
            self.track_buffer = int(self.track_buffer)
            if self.track_buffer > 0:
                self.track_buffer_seconds = float(self.track_buffer) / ref
        else:
            if self.track_buffer_seconds <= 0:
                raise ValueError(
                    f"track_buffer_seconds must be positive, got {self.track_buffer_seconds}"
                )
            self.track_buffer_seconds = float(self.track_buffer_seconds)
            self.track_buffer = max(1, int(round(self.track_buffer_seconds * ref)))
