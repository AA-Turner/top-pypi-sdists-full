"""
Trace collection utilities.
"""
from typing import Any, Dict, List


class TraceCollector:
    """
    Trace collector.
    """

    def __init__(self):
        self.traces: List[Dict[str, Any]] = []

    def add_trace(self, trace: Dict[str, Any]):
        """Add a trace."""
        self.traces.append(trace)

    def get_traces(self) -> List[Dict[str, Any]]:
        """Get all traces."""
        return self.traces

    def clear(self):
        """Clear traces."""
        self.traces.clear()


__all__ = ["TraceCollector"]
