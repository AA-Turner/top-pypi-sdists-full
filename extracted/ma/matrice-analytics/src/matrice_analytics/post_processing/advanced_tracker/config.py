"""
Configuration classes for advanced tracker.
This module provides configuration classes for the advanced tracker,
including parameters for tracking algorithms and thresholds.
"""

from dataclasses import dataclass


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

    # Output format settings
    output_format: str = "tracking"  # "tracking" or "detection"

    # Additional settings
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5

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

        if self.output_format not in ["tracking", "detection"]:
            raise ValueError(f"Invalid output_format: {self.output_format}")

        if self.class_aggregation_window_size <= 0:
            raise ValueError(
                f"class_aggregation_window_size must be positive, got {self.class_aggregation_window_size}"
            )
