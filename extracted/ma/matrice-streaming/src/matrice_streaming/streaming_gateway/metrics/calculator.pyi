"""Auto-generated stub for module: calculator."""
from typing import Dict, List

from __future__ import annotations

# Classes
class MetricsCalculator:
    """
    Calculate statistical metrics over time windows.
    """

    def calculate_fps(frame_count_start: int, frame_count_end: int, time_elapsed: float) -> float: ...
        """
        Calculate frames per second.
        
                Args:
                    frame_count_start: Starting frame count
                    frame_count_end: Ending frame count
                    time_elapsed: Time elapsed in seconds
        
                Returns:
                    Frames per second
        """

    def calculate_statistics(values: List[float]) -> Dict[str, float]: ...
        """
        Calculate min, max, avg, p0, p50, p100 from a list of values.
        
                Args:
                    values: List of numeric values
        
                Returns:
                    Dictionary with statistical metrics
        """

