"""Auto-generated stub for module: gstreamer_rtp_demuxer."""
from typing import Any, List, Optional, Tuple

from __future__ import annotations
from codec_detect import normalize_codec
from dataclasses import dataclass
from enum import Enum
from gi.repository import GLib, Gst, GstRtp
from rtp_correlation import DEFAULT_MAX_ENTRIES
from rtp_correlation import RtpPtsCorrelator
import argparse
import gi
import importlib.util as _ilu
import importlib.util as _ilu
import logging
import os
import os as _os
import os as _os
import re
import sys
import threading
import time
import uuid

# Constants
RTP_CLOCK_RATE: int
logger: Any

# Classes
class DemuxerType(Enum):
    """
    Demuxer backend selection.
    """

    GSTREAMER: str
    NVC: str

    pass
class GstRTPDemuxer:
    """
    GStreamer H264 demuxer with ABSOLUTE RTP timestamp capture.
    
        For RTSP streams:
        - Captures RAW 32-bit RTP timestamps via pad probe BEFORE depayloading
        - These are the ACTUAL timestamps from the RTP packet header
        - NOT normalized like PyAV (which starts near 0 each session)
        - Timestamps persist across reconnections (monotonically increasing from source)
        - Automatically converts localhost to 127.0.0.1 to avoid IPv6 issues
        - Uses TCP by default to avoid UDP IPv6 socket issues
    
        For files:
        - Uses container PTS (presentation timestamp)
        - No RTP timestamps available
    
        Outputs H264 NAL units for external decoder (e.g., PyNvVideoCodec).
    
        Args:
            source: RTSP URL or file path
            use_tcp: Use TCP for RTSP transport (default: True, more reliable)
            loop: Loop file playback (default: False)
    """

    def __init__(self: Any, source: str, use_tcp: bool = True, loop: bool = False, codec: str = 'h264') -> None: ...

    MAX_RETRIES: int
    RETRY_DELAYS: List[Any]

    def close(self: Any) -> Any: ...
        """
        Close demuxer and release resources.
        """

    def demux(self: Any) -> Any: ...
        """
        Demux H264/H265 NAL units with timestamps.
        
                Yields:
                    (nal_bytes, timestamp, timestamp_ns, absolute_time_ns)
        
                    For RTSP:
                    - nal_bytes: H264/H265 NAL unit as bytes
                    - timestamp: RAW 32-bit RTP timestamp (ABSOLUTE, NOT normalized)
                    - timestamp_ns: RTP timestamp converted to nanoseconds (at 90kHz)
                    - absolute_time_ns: Unix time if RTCP SR available, None otherwise
        
                    For files:
                    - nal_bytes: H264/H265 NAL unit as bytes
                    - timestamp: Container PTS
                    - timestamp_ns: PTS in nanoseconds
                    - absolute_time_ns: None
        """

    def first_rtp_timestamp(self: Any) -> Optional[int]: ...
        """
        First ABSOLUTE RTP timestamp captured (RTSP only).
        """

    def fps(self: Any) -> float: ...
        """
        Video frame rate.
        """

    def frames_demuxed(self: Any) -> int: ...
        """
        Number of frames demuxed in this session.
        """

    def has_rtcp_sr(self: Any) -> bool: ...
        """
        Whether RTCP Sender Report is available for absolute time mapping.
        """

    def height(self: Any) -> int: ...
        """
        Video frame height.
        """

    def is_eof(self: Any) -> bool: ...
        """
        Whether end-of-stream has been reached.
        """

    def is_rtsp(self: Any) -> bool: ...
        """
        Whether source is RTSP stream.
        """

    def latest_rtcp_sr(self: Any) -> Optional[RTCPSenderReport]: ...
        """
        Most recent RTCP Sender Report.
        """

    def open(self: Any, quiet: bool = False) -> Any: ...
        """
        Open source and initialize demuxer pipeline with retry logic.
        
                For RTSP streams, automatically retries with TCP if UDP fails,
                and converts localhost to 127.0.0.1 to avoid IPv6 issues.
        
                Args:
                    quiet: Suppress info logging
        
                Returns:
                    self (for chaining)
        
                Raises:
                    RuntimeError: If pipeline creation fails after all retries
        """

    def rtp_correlation_stats(self: Any) -> Tuple[int, int]: ...
        """
        ``(hits, misses)`` for PTS -> RTP correlation. Diagnostics only.
        """

    def session_id(self: Any) -> str: ...
        """
        Unique session identifier.
        """

    def session_start_ns(self: Any) -> int: ...
        """
        Session start time in nanoseconds.
        """

    def width(self: Any) -> int: ...
        """
        Video frame width.
        """

class RTCPSenderReport:
    """
    Parsed RTCP Sender Report for RTP-to-NTP time mapping.
    
        Attributes:
            ssrc: Synchronization source identifier
            ntp_timestamp: 64-bit NTP timestamp from RTCP SR
            rtp_timestamp: 32-bit RTP timestamp at SR time
            unix_time: NTP timestamp converted to Unix time
            received_at_ns: Local time when SR was received (nanoseconds)
    """

    pass
class RTCPTracker:
    """
    Tracks RTCP Sender Reports for RTP-to-absolute-time mapping.
    
        RTCP Sender Reports provide the mapping between RTP timestamps (at 90kHz)
        and absolute wall-clock time (NTP). This allows converting any RTP timestamp
        to Unix time for cross-camera synchronization.
    """

    def __init__(self: Any, clock_rate: int = RTP_CLOCK_RATE) -> None: ...

    NTP_UNIX_EPOCH_DIFF: int

    def has_sender_report(self: Any) -> bool: ...
        """
        Check if at least one RTCP Sender Report has been received.
        """

    def latest_sr(self: Any) -> Optional[RTCPSenderReport]: ...
        """
        Get the most recent RTCP Sender Report.
        """

    def rtp_to_unix_ns(self: Any, rtp_timestamp: int) -> Optional[int]: ...
        """
        Convert RTP timestamp to absolute Unix time in nanoseconds.
        
                Uses the most recent RTCP Sender Report to map RTP timestamps to
                absolute wall-clock time. Handles 32-bit RTP timestamp rollover.
        
                Args:
                    rtp_timestamp: 32-bit RTP timestamp to convert
        
                Returns:
                    Unix time in nanoseconds, or None if no SR available
        """

    def update_from_session_stats(self: Any, stats_str: str, ssrc: int) -> Optional[RTCPSenderReport]: ...
        """
        Parse RTCP SR from GStreamer session stats.
        
                Args:
                    stats_str: GStreamer stats structure as string
                    ssrc: Source SSRC identifier
        
                Returns:
                    RTCPSenderReport if valid SR found, None otherwise
        """

