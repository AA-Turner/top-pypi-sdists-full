"""GhostPC streaming — MJPEG live screen streaming and optional WebRTC."""

from ghost_pc.streaming.mjpeg_server import MJPEGServer


def is_webrtc_available() -> bool:
    """Check if WebRTC streaming is available (aiortc installed)."""
    try:
        import aiortc  # noqa: F401

        return True
    except ImportError:
        return False


__all__ = ["MJPEGServer", "is_webrtc_available"]
