"""Auto-generated stub for module: sink."""
from typing import Any, Dict, List, Optional

from __future__ import annotations
from dataclasses import dataclass, field
import logging

# Constants
log: Any

# Classes
class CudaIpcRingBufferSink:
    """
    Wraps matrice_common CudaIpcRingBuffer for use as a FrameSink.
    
        The ring_buffer object is created lazily per camera on first publish
        via the factory callable: factory(camera_id) → ring_buffer object.
    """

    def __init__(self: Any, ring_buffer_factory: Any) -> None: ...

    def commit_round(self: Any) -> None: ...

    def publish(self: Any, camera_id: str, frame: Any, timestamp_ns: int, rtp_timestamp: int, src_w: int, src_h: int, session_id: str = '', session_start_ns: int = 0) -> None: ...

class FrameSink(Protocol):
    """
    Write-side of the CUDA IPC ring buffer (or any alternative output).
    """

    def commit_round(self: Any) -> None: ...
        """
        Flush/sync after a round of publishes (batched CUDA sync).
        """

    def publish(self: Any, camera_id: str, frame: Any, timestamp_ns: int, rtp_timestamp: int, src_w: int, src_h: int, session_id: str = '', session_start_ns: int = 0) -> None: ...
        """
        Publish one decoded NV12 frame.
        """

class InMemoryFrameSink:
    """
    Accumulates published frames in memory — no GPU required.
    
        Use in unit tests and local CPU decode:
            sink = InMemoryFrameSink()
            # ... run decode loop ...
            assert len(sink.frames) == expected_count
    """

    def __init__(self: Any) -> None: ...

    def commit_round(self: Any) -> None: ...

    def publish(self: Any, camera_id: str, frame: Any, timestamp_ns: int, rtp_timestamp: int, src_w: int, src_h: int, session_id: str = '', session_start_ns: int = 0) -> None: ...

    def reset(self: Any) -> None: ...

