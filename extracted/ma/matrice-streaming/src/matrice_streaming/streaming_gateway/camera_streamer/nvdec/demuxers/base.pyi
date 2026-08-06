"""Auto-generated stub for module: base."""
from typing import Any, Optional

from __future__ import annotations
from dataclasses import dataclass

# Classes
class DemuxedUnit:
    """
    One demuxed NAL unit with associated timestamps.
    """

    pass
class Demuxer(Protocol):
    """
    Minimal interface every demuxer backend must implement.
    
        The decode loop calls demux() and iterates DemuxedUnit objects.
        All other details (subprocess management, RTCP, PTS) live inside
        the concrete demuxer module.
    """

    def close(self: Any) -> None: ...
        """
        Release resources.
        """

    def demux(self: Any) -> Any: ...
        """
        Yield DemuxedUnit per NAL unit; yield None on empty/stall; raise on hard error.
        """

    def fps(self: Any) -> float: ...

    def height(self: Any) -> int: ...

    def open(self: Any) -> None: ...
        """
        Open / (re-)connect the source.
        """

    def session_id(self: Any) -> str: ...

    def session_start_ns(self: Any) -> int: ...

    def width(self: Any) -> int: ...

