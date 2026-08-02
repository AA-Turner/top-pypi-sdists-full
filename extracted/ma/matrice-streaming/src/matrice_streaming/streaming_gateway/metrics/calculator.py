"""Statistical metrics calculator."""

from __future__ import annotations

from typing import Dict, List


class MetricsCalculator:
    """Calculate statistical metrics over time windows."""

    @staticmethod
    def calculate_statistics(values: List[float]) -> Dict[str, float]:
        """Calculate min, max, avg, p0, p50, p100 from a list of values.

        Args:
            values: List of numeric values

        Returns:
            Dictionary with statistical metrics
        """
        if not values:
            return {
                "min": 0.0,
                "max": 0.0,
                "avg": 0.0,
                "p0": 0.0,
                "p50": 0.0,
                "p100": 0.0,
            }

        sorted_values = sorted(values)
        count = len(sorted_values)

        return {
            "min": sorted_values[0],
            "max": sorted_values[-1],
            "avg": sum(values) / count,
            "p0": sorted_values[0],  # Minimum
            "p50": sorted_values[count // 2],  # Median
            "p100": sorted_values[-1],  # Maximum
        }

    @staticmethod
    def calculate_fps(frame_count_start: int, frame_count_end: int, time_elapsed: float) -> float:
        """Calculate frames per second.

        Args:
            frame_count_start: Starting frame count
            frame_count_end: Ending frame count
            time_elapsed: Time elapsed in seconds

        Returns:
            Frames per second
        """
        if time_elapsed <= 0:
            return 0.0

        frame_diff = frame_count_end - frame_count_start
        return frame_diff / time_elapsed
