"""Auto-generated stub for module: codec_detect."""
from typing import Any, Optional

from matrice_streaming.url_redact import redact_url
import logging
import subprocess

# Constants
CODEC_H264: str
CODEC_H265: str
DEFAULT_CODEC: Any
logger: Any

# Functions
def detect_codec_ffprobe(url: str, timeout: float = 10.0) -> Optional[str]: ...
    """
    Detect video codec of an RTSP stream or file using ffprobe.
    
        Runs ffprobe as a subprocess to query the first video stream's codec_name.
        Returns the canonical codec string ("h264" or "h265") or None on failure.
    
        This is the most reliable detection method but requires:
        - ffprobe installed (part of ffmpeg package)
        - Network access to the RTSP URL
        - ~2-5 seconds for RTSP streams (connection + probe)
    
        Args:
            url: RTSP URL or file path to probe
            timeout: Maximum seconds to wait for ffprobe (default: 10s)
    
        Returns:
            "h264", "h265", or None if detection failed
    """
def detect_codec_rtp_payload(payload: Any) -> Optional[str]: ...
    """
    Detect video codec from a raw RTP payload by inspecting NAL unit headers.
    
        Examines the first bytes of an RTP payload to distinguish H.264 from H.265
        based on the NAL unit type encoding:
    
        - H.264: NAL type is bits [4:0] of byte 0 (5 bits, range 1-23 for single NAL)
        - H.265: NAL type is bits [6:1] of byte 0 (6 bits), and byte 1 has layer_id + tid
    
        Heuristic: H.265 NAL units have the forbidden_zero_bit=0 (bit 7 of byte 0)
        AND the temporal_id in byte 1 bits [2:0] must be >= 1 (never 0 in valid H.265).
        H.264 NAL units don't have this byte 1 constraint.
    
        Args:
            payload: Raw RTP payload bytes (after removing 12-byte RTP header)
    
        Returns:
            "h264", "h265", or None if payload is too short or ambiguous
    """
def normalize_codec(codec: Optional[str]) -> str: ...
    """
    Normalize a codec string to canonical form ("h264" or "h265").
    
        Handles case-insensitive matching and common aliases (HEVC, AVC, H.264, etc.).
        Returns DEFAULT_CODEC ("h264") for None, empty, or unrecognized values.
    
        Args:
            codec: Codec string in any case/format, or None
    
        Returns:
            "h264" or "h265"
    """
