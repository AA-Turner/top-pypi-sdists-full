"""
Configuration classes for advanced tracker.

This module provides configuration classes for the advanced tracker,
including parameters for tracking algorithms and thresholds.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TrackerConfig:
    """
    Configuration for advanced tracker.
    
    This class contains all the parameters needed to configure the tracking algorithm,
    including thresholds, buffer sizes, and algorithm-specific settings.
    """
    
    # Tracking thresholds
    track_high_thresh: float = 0.7
    track_low_thresh: float = 0.1
    new_track_thresh: float = 0.7
    match_thresh: float = 0.8
    
    # Buffer settings
    track_buffer: int = 600
    max_time_lost: int = 600
    
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
        
        # Calculate max_time_lost if not explicitly set
        if self.max_time_lost == 30:  # Default value
            self.max_time_lost = int(self.frame_rate / 30.0 * self.track_buffer) 