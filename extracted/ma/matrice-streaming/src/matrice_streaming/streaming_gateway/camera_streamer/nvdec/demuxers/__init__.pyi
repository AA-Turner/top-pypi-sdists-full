"""Stub file for streaming_gateway.camera_streamer.nvdec.demuxers directory."""
from typing import Any, Optional

from __future__ import annotations
from dataclasses import dataclass
from matrice_streaming.streaming_gateway.camera_streamer.nvdec.demuxers.base import DemuxedUnit
from matrice_streaming.streaming_gateway.camera_streamer.nvdec.gstreamer_rtp_demuxer import GstRTPDemuxer, RTCPSenderReport
from matrice_streaming.streaming_gateway.camera_streamer.nvdec.gstreamer_subprocess_demuxer import GStreamerSubprocessDemuxer
import PyNvVideoCodec as nvc
import json
import logging
import struct
import sys
import time
import uuid

# Constants
log: Any = ...  # From nvc

# Functions
# From _subprocess_child
def read_json(proc: Any) -> Any: ...
    """
    Read one length-prefixed message and decode as JSON.
    """

# From _subprocess_child
def read_msg(proc: Any) -> Any: ...
    """
    Read one length-prefixed message from proc.stdout.
    
        Returns raw bytes payload. Caller interprets as JSON or binary.
        Raises EOFError on pipe close.
    """

# From _subprocess_child
def write_json(obj: Any) -> None: ...
    """
    Serialize obj to JSON and write as a length-prefixed message.
    """

# From _subprocess_child
def write_msg(data: Any) -> None: ...
    """
    Write length-prefixed message to stdout.
    """

# Classes
# From base
class DemuxedUnit:
    """
    One demuxed NAL unit with associated timestamps.
    """

    pass

# From base
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


# From nvc
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


from . import _subprocess_child, base, gstreamer_inprocess, gstreamer_subprocess, nvc