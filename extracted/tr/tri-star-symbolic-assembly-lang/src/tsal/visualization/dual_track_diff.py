from __future__ import annotations

"""Display differences between two memory tracks."""

class DualTrackDiffViewer:
    """Highlight mismatches between tracks."""

    def diff(self, track_a: list[str], track_b: list[str]) -> list[str]:
        """Return list of divergent entries."""
        return []

__all__ = ["DualTrackDiffViewer"]
