"""Auto-generated stub for module: nvc."""
from typing import Any, Optional

from __future__ import annotations
from matrice_streaming.streaming_gateway.camera_streamer.nvdec.demuxers.base import DemuxedUnit
import PyNvVideoCodec as nvc
import logging
import time
import uuid

# Constants
log: Any

# Classes
class NvcDemuxer:
    """
    Thin Demuxer-Protocol wrapper around PyNvVideoCodec demuxer.
    
        Implements the Demuxer Protocol defined in demuxers/base.py.
    """

    def __init__(self: Any, video_path: str, gpu_id: int = 0) -> None: ...

    def close(self: Any) -> None: ...

    def demux(self: Any) -> Any: ...
        """
        Yield DemuxedUnit per NAL; yields None on empty packets.
        """

    def fps(self: Any) -> float: ...

    def height(self: Any) -> int: ...

    def open(self: Any) -> None: ...

    def session_id(self: Any) -> str: ...

    def session_start_ns(self: Any) -> int: ...

    def width(self: Any) -> int: ...

