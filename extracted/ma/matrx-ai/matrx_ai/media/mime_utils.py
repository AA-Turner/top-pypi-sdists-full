"""
MIME Type Detection Utilities

Provides auto-detection of MIME types from various sources:
- URLs and file paths
- Base64 data (including data URIs)
- Magic bytes (file signatures)
"""

import base64
import mimetypes

# Fallback extension-to-MIME mappings for types that may not be in system database
EXTENSION_MIME_MAP: dict[str, str] = {
    # Images
    ".webp": "image/webp",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".ico": "image/x-icon",
    ".svg": "image/svg+xml",
    ".avif": "image/avif",
    ".heic": "image/heic",
    ".heif": "image/heif",
    # Audio
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".aac": "audio/aac",
    ".m4a": "audio/mp4",
    ".opus": "audio/opus",
    ".amr": "audio/amr",
    # Video
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".avi": "video/x-msvideo",
    ".mov": "video/quicktime",
    ".mkv": "video/x-matroska",
    # Documents
    ".pdf": "application/pdf",
}


def detect_mime_type(
    url: str | None = None,
    base64_data: str | None = None,
    file_uri: str | None = None,
) -> str | None:
    """
    Auto-detect MIME type from available sources.

    Checks sources in order:
    1. URL
    2. file_uri
    3. base64_data

    Args:
        url: HTTP(S) URL
        base64_data: Base64 encoded data (raw or data URI)
        file_uri: File URI or path

    Returns:
        Detected MIME type or None if unable to detect
    """
    # Try to detect from URL
    if url:
        mime_type = _detect_mime_from_path(url)
        if mime_type:
            return mime_type

    # Try to detect from file_uri
    if file_uri:
        mime_type = _detect_mime_from_path(file_uri)
        if mime_type:
            return mime_type

    # Try to detect from base64_data
    if base64_data:
        return _detect_mime_from_base64(base64_data)

    return None


def _detect_mime_from_path(path: str) -> str | None:
    """Detect MIME type from file path or URL"""
    # Remove query parameters and fragments for better detection
    clean_path = path.split("?")[0].split("#")[0]

    # Use strict=False to include common_types (where .webp lives)
    mime_type, _ = mimetypes.guess_type(clean_path, strict=False)
    if mime_type:
        return mime_type

    # Fallback to explicit extension mapping for any edge cases
    ext = clean_path.rsplit(".", 1)[-1].lower() if "." in clean_path else ""
    if ext:
        return EXTENSION_MIME_MAP.get(f".{ext}")

    return None


def _detect_mime_from_base64(data: str) -> str | None:
    """Detect MIME type from base64 data (data URI or raw base64)"""
    # Check if it's a data URI: data:image/png;base64,iVBORw0KG...
    if data.startswith("data:"):
        try:
            mime_part = data.split(";")[0].split(":")[1]
            return mime_part
        except (IndexError, ValueError):
            pass

    # Try to detect from magic bytes (first few bytes of decoded data)
    try:
        decoded = base64.b64decode(data[:100])  # Only decode first bit for efficiency
        return _detect_mime_from_magic_bytes(decoded)
    except Exception:
        pass

    return None


def _detect_mime_from_magic_bytes(data: bytes) -> str | None:
    """
    Detect MIME type from magic bytes (file signature).

    Supports common media formats used in AI APIs.
    """
    # Images
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    elif data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    elif data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "image/gif"
    elif data.startswith(b"RIFF") and b"WEBP" in data[:12]:
        return "image/webp"
    elif data.startswith(b"BM"):
        return "image/bmp"
    elif data.startswith(b"\x00\x00\x01\x00"):
        return "image/x-icon"

    # Documents
    elif data.startswith(b"%PDF"):
        return "application/pdf"

    # Video
    elif data.startswith(b"\x00\x00\x00\x18ftypmp4") or data.startswith(
        b"\x00\x00\x00\x1cftypisom"
    ):
        return "video/mp4"
    elif data.startswith(b"\x1aE\xdf\xa3"):
        return "video/webm"
    elif data.startswith(b"RIFF") and b"AVI " in data[:12]:
        return "video/x-msvideo"

    # Audio
    elif data.startswith(b"ID3") or data.startswith(b"\xff\xfb"):
        return "audio/mpeg"
    elif data.startswith(b"RIFF") and b"WAVE" in data[:12]:
        return "audio/wav"
    elif data.startswith(b"OggS"):
        return "audio/ogg"
    elif data.startswith(b"fLaC"):
        return "audio/flac"
    elif data.startswith(b"#!AMR"):
        return "audio/amr"

    return None
