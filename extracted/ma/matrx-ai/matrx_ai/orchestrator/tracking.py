from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCallUsage:
    """Tracks tool call information for a single request iteration."""

    iteration: int
    tool_calls_count: int
    """Number of tool calls made in this iteration"""

    tool_calls_details: list[dict[str, Any]]
    """List of tool call details (name, success, etc.)"""

    @staticmethod
    def aggregate(tool_call_list: list[ToolCallUsage]) -> dict[str, Any]:
        """Aggregate tool call statistics from a list of iteration tool calls.

        Returns a dictionary with comprehensive tool call analysis including:
        - Total tool calls across all iterations
        - Breakdown by tool name
        - Success/failure counts
        """
        if not tool_call_list:
            return {
                "total_tool_calls": 0,
                "iterations_with_tools": 0,
                "by_tool": {},
            }

        total_calls = sum(tc.tool_calls_count for tc in tool_call_list)
        iterations_with_tools = len(
            [tc for tc in tool_call_list if tc.tool_calls_count > 0]
        )

        # Aggregate by tool name
        by_tool: dict[str, dict[str, int]] = {}

        for tc in tool_call_list:
            for detail in tc.tool_calls_details:
                tool_name = detail.get("name", "unknown")
                if tool_name not in by_tool:
                    by_tool[tool_name] = {
                        "count": 0,
                        "success": 0,
                        "error": 0,
                    }

                by_tool[tool_name]["count"] += 1

                # Track success/error if available
                if detail.get("success", True):  # Default to True if not specified
                    by_tool[tool_name]["success"] += 1
                else:
                    by_tool[tool_name]["error"] += 1

        return {
            "total_tool_calls": total_calls,
            "iterations_with_tools": iterations_with_tools,
            "by_tool": by_tool,
        }


@dataclass
class TimingUsage:
    """Tracks timing information for a single request iteration."""

    start_time: float
    end_time: float | None = None

    # Component timings
    api_call_duration: float = 0.0
    tool_execution_duration: float = 0.0

    # Context
    model: str = ""
    iteration: int = 0

    @property
    def total_duration(self) -> float:
        """Total duration of this iteration in seconds."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return 0.0

    @property
    def processing_duration(self) -> float:
        """Time spent processing logic outside of API and Tools."""
        return max(
            0.0,
            self.total_duration - self.api_call_duration - self.tool_execution_duration,
        )

    @staticmethod
    def aggregate(timings: list[TimingUsage]) -> dict[str, Any]:
        """Aggregate timing statistics from a list of iteration timings.

        Returns a dictionary with comprehensive timing analysis including:
        - Total wall-clock duration
        - Total time spent in API calls
        - Total time spent executing tools
        - Average times for each component
        """
        if not timings:
            return {
                "total_duration": 0.0,
                "api_duration": 0.0,
                "tool_duration": 0.0,
                "processing_duration": 0.0,
            }

        valid_timings = [t for t in timings if t.end_time is not None]
        if not valid_timings:
            return {
                "total_duration": 0.0,
                "api_duration": 0.0,
                "tool_duration": 0.0,
                "processing_duration": 0.0,
            }

        # Calculate totals
        total_api = sum(t.api_call_duration for t in valid_timings)
        total_tool = sum(t.tool_execution_duration for t in valid_timings)
        total_sum_duration = sum(t.total_duration for t in valid_timings)

        # Calculate wall clock duration (from start of first to end of last)
        # Sort just in case they aren't in order (though they should be)
        sorted_timings = sorted(valid_timings, key=lambda t: t.start_time)
        wall_clock_start = sorted_timings[0].start_time
        last_end_time = sorted_timings[-1].end_time
        assert last_end_time is not None  # guaranteed by valid_timings filter above
        wall_clock_duration = last_end_time - wall_clock_start

        return {
            "total_duration": wall_clock_duration,
            "sum_duration": total_sum_duration,
            "api_duration": total_api,
            "tool_duration": total_tool,
            "processing_duration": max(
                0.0, wall_clock_duration - total_api - total_tool
            ),
            "iterations": len(valid_timings),
            "avg_iteration_duration": wall_clock_duration / len(valid_timings)
            if valid_timings
            else 0,
        }
