"""Codec detection utilities for RTSP streams and video files.

Provides two detection methods:
1. detect_codec_ffprobe() - Uses ffprobe to query stream codec (reliable, requires ffprobe)
2. detect_codec_rtp_payload() - Inspects raw RTP payload NAL headers (lightweight, no deps)

Usage:
    from .codec_detect import detect_codec_ffprobe, detect_codec_rtp_payload, normalize_codec

    # Detect codec from RTSP URL (blocking, ~2-5s)
    codec = detect_codec_ffprobe("rtsp://admin:pass@192.168.1.10:554/stream")
    # Returns: "h264", "h265", or None on failure

    # Detect codec from raw RTP payload bytes (non-blocking)
    codec = detect_codec_rtp_payload(rtp_payload_bytes)
    # Returns: "h264", "h265", or None if ambiguous

    # Normalize any codec string to canonical form
    normalize_codec("H265")   # -> "h265"
    normalize_codec("HEVC")   # -> "h265"
    normalize_codec("H.264")  # -> "h264"
    normalize_codec("junk")   # -> "h264" (default)
"""

import logging
import subprocess
from typing import Optional

from matrice_streaming.url_redact import redact_url

logger = logging.getLogger(__name__)

# Canonical codec names used throughout the pipeline
CODEC_H264 = "h264"
CODEC_H265 = "h265"

# NOTE: Default codec is h264 — this matches the majority of deployed cameras.
# Most RTSP cameras (Hikvision, Dahua, Axis) default to H.264 on their primary
# stream. H.265 is typically only on sub-streams or explicitly configured.
DEFAULT_CODEC = CODEC_H264

# Aliases that all map to the canonical names
_CODEC_ALIASES = {
    # H.264 aliases
    "h264": CODEC_H264,
    "h.264": CODEC_H264,
    "avc": CODEC_H264,
    "avc1": CODEC_H264,
    "x264": CODEC_H264,
    # H.265 aliases
    "h265": CODEC_H265,
    "h.265": CODEC_H265,
    "hevc": CODEC_H265,
    "hev1": CODEC_H265,
    "x265": CODEC_H265,
}


def normalize_codec(codec: Optional[str]) -> str:
    """Normalize a codec string to canonical form ("h264" or "h265").

    Handles case-insensitive matching and common aliases (HEVC, AVC, H.264, etc.).
    Returns DEFAULT_CODEC ("h264") for None, empty, or unrecognized values.

    Args:
        codec: Codec string in any case/format, or None

    Returns:
        "h264" or "h265"
    """
    if not codec:
        return DEFAULT_CODEC
    normalized = _CODEC_ALIASES.get(codec.strip().lower())
    if normalized is None:
        logger.warning(f"Unrecognized codec '{codec}', defaulting to {DEFAULT_CODEC}")
        return DEFAULT_CODEC
    return normalized


def detect_codec_ffprobe(
    url: str,
    timeout: float = 10.0,
) -> Optional[str]:
    """Detect video codec of an RTSP stream or file using ffprobe.

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
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-rtsp_transport",
        "tcp",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        url,
    ]

    try:
        result = subprocess.run(  # nosec B603
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        safe_url = redact_url(url)
        if result.returncode != 0:
            stderr_snippet = (result.stderr or "")[:200]
            logger.warning(f"ffprobe failed for {safe_url}: exit={result.returncode}, stderr={stderr_snippet}")
            return None

        codec_name = result.stdout.strip().lower()
        if not codec_name:
            logger.warning(f"ffprobe returned empty codec for {safe_url}")
            return None

        normalized = _CODEC_ALIASES.get(codec_name)
        if normalized:
            logger.info(f"ffprobe detected codec '{codec_name}' -> '{normalized}' for {safe_url}")
            return normalized

        logger.warning(f"ffprobe returned unsupported codec '{codec_name}' for {safe_url}")
        return None

    except FileNotFoundError:
        logger.warning("ffprobe not found — install ffmpeg to enable codec auto-detection")
        return None
    except subprocess.TimeoutExpired:
        logger.warning(f"ffprobe timed out after {timeout}s for {redact_url(url)}")
        return None
    except Exception as e:
        logger.warning(f"ffprobe error for {redact_url(url)}: {e}")
        return None


def detect_codec_rtp_payload(payload: bytes) -> Optional[str]:
    """Detect video codec from a raw RTP payload by inspecting NAL unit headers.

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
    if not payload or len(payload) < 2:
        return None

    byte0 = payload[0]
    byte1 = payload[1]

    # Forbidden zero bit must be 0 for both H.264 and H.265
    if byte0 & 0x80:
        return None

    # H.265 check: NAL type in bits [6:1], temporal_id in byte1 bits [2:0] >= 1
    h265_nal_type = (byte0 >> 1) & 0x3F
    h265_tid = byte1 & 0x07

    # H.264 check: NAL type in bits [4:0]
    h264_nal_type = byte0 & 0x1F

    # H.265 RTP uses NAL types 0-47 for actual NAL units, 48-49 for aggregation/fragmentation
    # The temporal_id field (byte1 bits [2:0]) is ALWAYS >= 1 in valid H.265
    if h265_tid >= 1 and h265_nal_type <= 49:
        # Could be H.265 — check if H.264 interpretation also makes sense
        # H.264 single NAL types are 1-23, aggregation is 24-31
        if h264_nal_type in (24, 25, 26, 27, 28, 29):
            # H.264 STAP-A/B, MTAP16/24, FU-A/B — these are RTP packetization types
            # In H.264, FU-A (28) is very common. For FU-A, byte1 has S/E/R bits + NAL type.
            # In H.265, type 49 (FU) has byte1 with S/E + NAL type.
            # Disambiguate: H.264 FU-A (type 28) byte1 bit 7 = Start, bit 6 = End
            # H.265 FU (type 49) byte1 bit 7 = Start, bit 6 = End
            if h264_nal_type == 28:
                # H.264 FU-A is extremely common — favor H.264 interpretation
                return CODEC_H264

        # H.265 type 48 = AP (aggregation packet), type 49 = FU (fragmentation unit)
        if h265_nal_type in (48, 49):
            return CODEC_H265

        # Single NAL unit: H.265 types 0-47
        # VPS (32), SPS (33), PPS (34) are strong H.265 indicators
        if h265_nal_type in (32, 33, 34):
            return CODEC_H265

        # IDR_W_RADL (19), IDR_N_LP (20), CRA (21) — H.265 key frame types
        if h265_nal_type in (19, 20, 21):
            return CODEC_H265

    # H.264 single NAL types 1-23
    if 1 <= h264_nal_type <= 23:
        # SPS (7), PPS (8), IDR (5) are strong H.264 indicators
        if h264_nal_type in (5, 7, 8):
            return CODEC_H264
        return CODEC_H264

    # H.264 packetization types (STAP-A=24, FU-A=28, FU-B=29)
    if h264_nal_type in (24, 28, 29):
        return CODEC_H264

    return None
