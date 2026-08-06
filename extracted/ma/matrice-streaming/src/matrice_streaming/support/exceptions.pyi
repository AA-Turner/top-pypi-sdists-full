"""Auto-generated stub for module: exceptions."""
from typing import Any, Optional

from __future__ import annotations

# Classes
class ControlPlaneError(StreamingError):
    """
    Raised when Kafka/RPC/API control-plane calls fail.
    """

    pass
class DecodeError(StreamingError):
    """
    Raised when NVDEC or software decode fails.
    """

    pass
class DemuxerError(StreamingError):
    """
    Raised when demuxer (GStreamer/NVC) fails.
    """

    pass
class SinkError(StreamingError):
    """
    Raised when writing to FrameSink (SHM/DataBus) fails.
    """

    pass
class StreamingError(RuntimeError):
    def __init__(self: Any, message: str, camera_id: Optional[str] = None) -> None: ...

    pass
