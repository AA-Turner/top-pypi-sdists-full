"""Auto-generated stub for module: volume."""
from typing import Any, Dict, Optional, Set

from ..base_processor import BaseMetricProcessor, MetricEntry
from ..geometry import create_counter_from_zone_config, denormalize_zone_config

# Constants
logger: Any

# Classes
class VolumeProcessor:
    # VOLUME category processor for counting-based analytics.
    #
    #     Computes per-frame metrics (entry_count, exit_count, current_occupancy)
    #     and aggregation-time metrics (peak_count, unique_count, turnover_rate).
    #
    #     When geometry (zone_config) is set via ``set_zone_config()``, entry/exit
    #     counts are derived from line-crossing or polygon-based counters. Otherwise,
    #     falls back to simple track-ID counting.
    #
    #     Window-level aggregation mirrors ``AnalyticsPublisher`` semantics:
    #
    #     - **current_counts** = SUM of per-frame ``current_new_counts``
    #       (new arrivals in the 1-min window).
    #     - **total_current_counts** = previous window's last-frame occupancy
    #       + accumulated new arrivals (0 carry on first window).
    #     - **total_counts** = cumulative unique since last full reset.

    def __init__(self: Any, category: str, manifest_config: dict[str, Any], zone_id: str = '') -> None:
        """
        Initialize VolumeProcessor, ignoring ``category`` in favour of "VOLUME".
        
                Args:
                    category: Passed by the engine; always overridden to ``"VOLUME"``.
                    manifest_config: Full parsed manifest dict from the YAML config file.
                    zone_id: Optional zone name when running per-zone analytics.
                        Empty string means global (no zone).
        """
        ...

    def has_geometry(self: Any) -> bool:
        """
        Whether a geometry counter is active.
        """
        ...

    def remove_zone_config(self: Any) -> None:
        """
        Remove geometry config and revert to simple track-ID counting.
        """
        ...

    def reset(self: Any) -> None:
        """
        Full reset including VOLUME-specific state.
        """
        ...

    def set_zone_config(self: Any, zone_config: dict[str, Any], width: int, height: int, method: str = 'abline', in_direction: str = 'A_to_B', use_foot_center: bool = False) -> None:
        """
        Set geometry and create a counting counter for entry/exit analytics.
        
                After calling this, ``_compute_frame_metrics`` will use the geometry
                counter instead of simple track-ID counting.
        
                Args:
                    zone_config: Dict with ``"lines"`` and/or ``"zones"`` in normalized
                        (0-1) coordinates, matching the Matrice post-processing API format.
                    width: Frame width in pixels (for denormalization).
                    height: Frame height in pixels (for denormalization).
                    method: ``"abline"`` (two-line trap zone) or ``"polygon"``
                        (double-polygon hysteresis).
                    in_direction: For abline method -- ``"A_to_B"`` or ``"B_to_A"``.
                    use_foot_center: Use bottom-center of bbox instead of center.
        """
        ...

