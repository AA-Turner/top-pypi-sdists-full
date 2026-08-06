"""Auto-generated stub for module: config."""
from typing import Any, Dict, Optional

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import os

# Classes
class DemuxerType(Enum):
    """
    Demuxer backend selection.
    
        NVC: PyNvVideoCodec demuxer - fastest for local files
        GSTREAMER: GStreamer demuxer - provides ABSOLUTE RTP timestamps for RTSP
    """

    GSTREAMER: str
    NVC: str

    pass
class GatewayConfig:
    """
    Configuration for the streaming gateway.
    """

    pass
class StreamState:
    """
    Track state for each logical stream in NVDEC pool.
    """

    pass
