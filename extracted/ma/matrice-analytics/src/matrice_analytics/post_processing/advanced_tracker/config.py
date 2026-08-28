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

    # Buffer settings
    track_buffer: int = 600
    max_time_lost: int = 1800  # 60 seconds at 30fps before permanent removal

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

    # FPS adaptation: auto-detect the real detection frame-rate from update()
    # intervals and rescale time-dependent params (Kalman dt, match/new-track
    # thresholds, max_time_lost) so a 5-fps and a 30-fps camera both track well.
    # When enabled and no explicit fps is known, fps is measured from wall-clock
    # update() spacing (the ONLY path that touches the clock; kept off by default
    # to preserve deterministic core processing).
    enable_fps_adaptation: bool = False
    reference_fps: int = 30  # fps at which the base thresholds/dt are calibrated
    # At low fps, thresholds relax toward these floors (objects move more/frame).
    match_thresh_low_fps_floor: float = 0.4
    new_track_thresh_low_fps_floor: float = 0.3
    # Time-based lost grace used in place of a fixed max_time_lost when adapting.
    # None (default) derives it from the CONFIGURED max_time_lost:
    # max_time_lost / reference_fps, so adaptation rescales the caller's own grace
    # instead of silently replacing it (at reference_fps it is an exact no-op).
    # Set an explicit value to pin the grace in seconds regardless of max_time_lost.
    grace_period_sec: Optional[float] = None
    # Upper bound on the fps that auto-detection may infer. Wall-clock update()
    # spacing is meaningless for batched/offline replay (frames arrive back to
    # back), which would otherwise drive dt -> 0 and max_time_lost -> millions.
    max_detected_fps: float = 120.0

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
        if not 0.0 <= self.track_high_thresh <= 1.0:
            raise ValueError(f"track_high_thresh must be between 0.0 and 1.0, got {self.track_high_thresh}")

        if not 0.0 <= self.track_low_thresh <= 1.0:
            raise ValueError(f"track_low_thresh must be between 0.0 and 1.0, got {self.track_low_thresh}")

        if not 0.0 <= self.new_track_thresh <= 1.0:
            raise ValueError(f"new_track_thresh must be between 0.0 and 1.0, got {self.new_track_thresh}")

        if not 0.0 <= self.match_thresh <= 1.0:
            raise ValueError(f"match_thresh must be between 0.0 and 1.0, got {self.match_thresh}")

        if self.track_buffer <= 0:
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
            raise ValueError(f"grace_period_sec must be positive or None, got {self.grace_period_sec}")

        if self.max_detected_fps <= 0:
            raise ValueError(f"max_detected_fps must be positive, got {self.max_detected_fps}")

        if self.predict_glide_grace_sec <= 0:
            raise ValueError(f"predict_glide_grace_sec must be positive, got {self.predict_glide_grace_sec}")

        if self.confirm_window_sec <= 0:
            raise ValueError(f"confirm_window_sec must be positive, got {self.confirm_window_sec}")

        if not 0.0 <= self.confirm_min_hits_ratio <= 1.0:
            raise ValueError(f"confirm_min_hits_ratio must be between 0.0 and 1.0, got {self.confirm_min_hits_ratio}")
