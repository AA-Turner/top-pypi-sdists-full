"""WebRTC live screen streaming — optional low-latency upgrade over MJPEG.

Requires: pip install ghost-pc[webrtc]
Falls back to MJPEG automatically if aiortc is not installed.

Architecture:
  Browser ←→ WebRTC (UDP) → 50-100ms latency, H264
  Only works on LAN — no STUN/TURN servers configured.
  Remote users (via Cloudflare tunnel) automatically get MJPEG instead.

Key components:
  - ScreenCaptureTrack: Feeds BetterCam BGRA frames as VideoStreamTrack
  - handle_webrtc_offer(): POST /webrtc/offer — SDP offer/answer exchange
  - handle_webrtc_status(): GET /webrtc/status — availability check
  - register_webrtc_routes(app): adds routes to existing aiohttp app
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aiohttp import web

logger = logging.getLogger(__name__)

# Active peer connections for cleanup
_peer_connections: set[Any] = set()


def is_webrtc_available() -> bool:
    """Check if aiortc is installed and WebRTC can be used."""
    try:
        import aiortc  # noqa: F401

        return True
    except ImportError:
        return False


def _create_capture_track(fps: int = 30) -> Any:
    """Create a ScreenCaptureTrack that feeds BetterCam frames.

    Returns a VideoStreamTrack subclass instance. All aiortc imports
    are deferred to avoid ImportError when aiortc is not installed.
    """
    import av
    from aiortc import VideoStreamTrack

    class ScreenCaptureTrack(VideoStreamTrack):
        """VideoStreamTrack that captures the desktop screen via BetterCam."""

        kind = "video"

        def __init__(self, target_fps: int = 30) -> None:
            super().__init__()
            self._fps = target_fps

        async def recv(self) -> av.VideoFrame:
            """Capture one screen frame and return as VideoFrame."""
            # Use VideoStreamTrack's built-in timestamp pacing
            pts, time_base = await self.next_timestamp()

            # Capture BGRA frame from BetterCam
            frame_data = await asyncio.to_thread(self._grab_frame)
            if frame_data is not None:
                frame = av.VideoFrame.from_ndarray(frame_data, format="bgra")
            else:
                # Black frame fallback if capture fails
                import numpy as np

                black = np.zeros((720, 1280, 4), dtype=np.uint8)
                frame = av.VideoFrame.from_ndarray(black, format="bgra")

            frame.pts = pts
            frame.time_base = time_base
            return frame

        def _grab_frame(self) -> Any:
            """Grab a raw BGRA numpy frame from BetterCam."""
            try:
                from ghost_pc.desktop.capture import grab_screenshot

                return grab_screenshot()
            except Exception:
                return None

    return ScreenCaptureTrack(target_fps=fps)


async def handle_webrtc_status(request: web.Request) -> web.Response:
    """GET /webrtc/status — check if WebRTC is available."""
    from aiohttp import web as aio_web

    return aio_web.json_response(
        {
            "available": is_webrtc_available(),
            "active_connections": len(_peer_connections),
        }
    )


async def handle_webrtc_offer(request: web.Request) -> web.Response:
    """POST /webrtc/offer — WebRTC SDP offer/answer exchange.

    The browser sends an SDP offer, we create a peer connection with a
    screen capture video track, and return the SDP answer.
    """
    from aiohttp import web as aio_web

    if not is_webrtc_available():
        return aio_web.json_response(
            {"error": "WebRTC not available"},
            status=503,
        )

    from aiortc import RTCPeerConnection, RTCSessionDescription

    body = await request.json()
    offer = RTCSessionDescription(sdp=body["sdp"], type=body["type"])

    # Create peer connection — no STUN/TURN for LAN-only
    pc = RTCPeerConnection()
    _peer_connections.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange() -> None:
        state = pc.connectionState
        logger.info("WebRTC connection state: %s", state)
        if state in ("failed", "closed", "disconnected"):
            await pc.close()
            _peer_connections.discard(pc)

    # Add screen capture video track
    video_track = _create_capture_track(fps=30)
    pc.addTrack(video_track)

    # Set remote description and create answer
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return aio_web.json_response(
        {
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type,
        }
    )


async def cleanup_peer_connections() -> None:
    """Close all active peer connections (called during shutdown)."""
    coros = [pc.close() for pc in _peer_connections]
    await asyncio.gather(*coros, return_exceptions=True)
    _peer_connections.clear()


def register_webrtc_routes(app: web.Application) -> None:
    """Register WebRTC routes on an existing aiohttp application.

    Called from MJPEGServer.run() when aiortc is available.
    """
    app.router.add_get("/webrtc/status", handle_webrtc_status)
    app.router.add_post("/webrtc/offer", handle_webrtc_offer)

    # Register cleanup on app shutdown
    async def _on_shutdown(app: web.Application) -> None:
        await cleanup_peer_connections()

    app.on_shutdown.append(_on_shutdown)

    logger.info("WebRTC routes registered (/webrtc/status, /webrtc/offer)")
