"""Auto-generated stub for module: gstreamer_subprocess_demuxer."""
from typing import Any, Optional, Tuple

from __future__ import annotations
from codec_detect import normalize_codec
import json
import logging
import os
import site
import struct
import subprocess
import sys
import tempfile
import time
import uuid

# Constants
logger: Any

# Classes
class GStreamerSubprocessDemuxer:
    """
    GStreamer demuxer that runs in a subprocess to avoid FFmpeg conflicts.
    
        Drop-in replacement for GstRTPDemuxer with the same interface:
        - open() / close()
        - demux() generator yielding (nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns)
        - Properties: width, height, fps, session_id, first_rtp_timestamp
    """

    def __init__(self: Any, video_path: str, use_tcp: bool = True, codec: str = 'h264') -> None: ...

    def close(self: Any) -> None: ...
        """
        Stop the subprocess and clean up all resources.
        """

    def demux(self: Any) -> Any: ...
        """
        Yield (nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns) from subprocess.
        """

    def open(self: Any, quiet: bool = True) -> None: ...
        """
        Start the GStreamer subprocess and wait for metadata.
        
                Retries up to 5 times with exponential backoff to handle transient
                RTSP source unavailability (e.g., video storage restart).
        """

    def restart(self: Any) -> None: ...
        """
        Restart the demuxer (reconnect to RTSP).
        """

