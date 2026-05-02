"""MJPEG live screen streaming server with integrated chat.

Serves the desktop screen as a live MJPEG stream that any mobile browser can display.
Also provides a WebSocket chat endpoint so users can control the PC directly
from the viewer page without switching back to WhatsApp.

MJPEG works in ALL mobile browsers (iOS Safari, Android Chrome) without
WebRTC, JavaScript, or any special setup. Just an <img> tag.
"""

from __future__ import annotations

import asyncio
import json
import logging
import secrets
import time
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from aiohttp import WSMsgType, web

if TYPE_CHECKING:
    from ghost_pc.agent.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


class _InputRateLimiter:
    """Dual-tier token-bucket rate limiter.

    Mouse move events get 60/sec, discrete actions get 30/sec.
    """

    def __init__(
        self,
        move_per_second: float = 60.0,
        action_per_second: float = 30.0,
    ) -> None:
        self._move_max = move_per_second
        self._move_allowance = move_per_second
        self._move_last = time.monotonic()
        self._action_max = action_per_second
        self._action_allowance = action_per_second
        self._action_last = time.monotonic()

    def allow(self, *, is_move: bool = False) -> bool:
        """Return True if the event should be processed, False to drop it."""
        now = time.monotonic()
        if is_move:
            elapsed = now - self._move_last
            self._move_last = now
            self._move_allowance = min(
                self._move_max, self._move_allowance + elapsed * self._move_max
            )
            if self._move_allowance < 1.0:
                return False
            self._move_allowance -= 1.0
            return True
        else:
            elapsed = now - self._action_last
            self._action_last = now
            self._action_allowance = min(
                self._action_max,
                self._action_allowance + elapsed * self._action_max,
            )
            if self._action_allowance < 1.0:
                return False
            self._action_allowance -= 1.0
            return True


class MJPEGServer:
    """HTTP server that streams desktop screenshots as MJPEG + WebSocket chat."""

    def __init__(
        self,
        port: int = 8443,
        fps: int = 10,
        jpeg_quality: int = 70,
        on_chat_message: Callable[[str, str], Awaitable[str]] | None = None,
        orchestrator: Orchestrator | None = None,
    ):
        self.port = port
        self.fps = fps
        self.jpeg_quality = jpeg_quality
        self.on_chat_message = on_chat_message  # (session_id, message) -> response
        self.orchestrator = orchestrator
        self.session_token = secrets.token_urlsafe(32)
        self._app: web.Application | None = None
        self._runner: web.AppRunner | None = None
        self._input_limiters: dict[str, _InputRateLimiter] = {}

    async def run(self) -> None:
        """Start the HTTP server."""
        self._app = web.Application()
        self._app.router.add_get("/view", self._handle_viewer)
        self._app.router.add_get("/stream", self._handle_stream)
        self._app.router.add_get("/ws", self._handle_websocket)
        self._app.router.add_get("/health", self._handle_health)

        # Register dashboard routes if orchestrator is provided
        if self.orchestrator is not None:
            try:
                from ghost_pc.web.dashboard_routes import register_dashboard_routes

                register_dashboard_routes(self._app, self.orchestrator)
                logger.info("Dashboard enabled at /dashboard")
            except Exception as exc:
                logger.warning("Failed to register dashboard routes: %s", exc)

        # Register WebRTC routes if aiortc is available
        try:
            from ghost_pc.streaming.webrtc_server import is_webrtc_available, register_webrtc_routes

            if is_webrtc_available():
                register_webrtc_routes(self._app)
                logger.info("WebRTC streaming enabled (LAN low-latency)")
        except ImportError:
            pass

        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, "0.0.0.0", self.port)
        await site.start()

        logger.info("MJPEG stream server running on http://0.0.0.0:%d", self.port)
        logger.info("Viewer URL: %s", self.get_viewer_url())

        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            await self._runner.cleanup()

    def get_viewer_url(self) -> str:
        """Get the URL to share with the user (uses LAN IP so phones can reach it)."""
        from ghost_pc.streaming.tunnel import get_local_ip

        ip = get_local_ip()
        return f"http://{ip}:{self.port}/view?token={self.session_token}"

    async def _handle_health(self, request: web.Request) -> web.Response:
        """Deep health check — verifies core subsystems are functional."""
        checks: dict[str, object] = {"status": "ok"}

        # Check screen capture
        try:
            frame = self._capture_frame()
            checks["screen_capture"] = "ok" if frame else "failed"
        except Exception:
            checks["screen_capture"] = "failed"

        # Check orchestrator status if available
        if self.orchestrator and hasattr(self.orchestrator, "get_status"):
            try:
                status = self.orchestrator.get_status()
                checks["agent_paused"] = status.get("paused", False)
                checks["whatsapp_connected"] = status.get("whatsapp_connected", False)
            except Exception:
                checks["orchestrator"] = "failed"

        # Check Gemini API reachability (lightweight — just check env var is set)
        import os

        checks["gemini_api_key_set"] = bool(os.environ.get("GOOGLE_API_KEY"))

        # Overall status
        if checks.get("screen_capture") == "failed":
            checks["status"] = "degraded"

        return web.json_response(checks)

    async def _handle_viewer(self, request: web.Request) -> web.Response:
        """Serve the HTML viewer page with live screen + chat."""
        token = request.query.get("token", "")
        if token != self.session_token:
            return web.Response(status=403, text="Invalid session token")

        html = VIEWER_HTML.replace("{{TOKEN}}", self.session_token)
        return web.Response(text=html, content_type="text/html")

    async def _handle_stream(self, request: web.Request) -> web.StreamResponse:
        """MJPEG stream endpoint — sends continuous JPEG frames."""
        token = request.query.get("token", "")
        if token != self.session_token:
            return web.Response(status=403, text="Invalid session token")

        response = web.StreamResponse()
        response.content_type = "multipart/x-mixed-replace; boundary=frame"
        await response.prepare(request)

        interval = 1.0 / self.fps
        last_frame: bytes | None = None

        try:
            while True:
                start = time.monotonic()

                frame = self._capture_frame()
                if frame is None:
                    frame = last_frame
                else:
                    last_frame = frame

                if frame:
                    await response.write(
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n"
                        b"Content-Length: " + str(len(frame)).encode() + b"\r\n"
                        b"\r\n" + frame + b"\r\n"
                    )

                elapsed = time.monotonic() - start
                sleep_time = max(0, interval - elapsed)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

        except (ConnectionResetError, asyncio.CancelledError):
            logger.info("Stream client disconnected")
        except Exception as e:
            logger.error("Stream error: %s", e)

        return response

    async def _handle_websocket(self, request: web.Request) -> web.WebSocketResponse | web.Response:
        """WebSocket endpoint for viewer chat and remote input.

        Handles two message types:
          - {"type": "input", ...}  → mouse/keyboard input from viewer overlay
          - {"message": "..."}     → chat message to agent (existing behavior)
        """
        token = request.query.get("token", "")
        if token != self.session_token:
            return web.Response(status=403, text="Invalid session token")

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        chat_session_id = secrets.token_hex(8)
        self._input_limiters[chat_session_id] = _InputRateLimiter()
        logger.info("Viewer chat connected: %s", chat_session_id)

        # Send welcome message
        await ws.send_json(
            {
                "type": "system",
                "content": "Connected to GhostPC. Type commands to control your PC.",
            }
        )

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                    except json.JSONDecodeError:
                        data = {"message": msg.data.strip()}

                    # ── Remote input events (click, key, scroll, mouse) ──
                    if data.get("type") == "input":
                        limiter = self._input_limiters.get(chat_session_id)
                        is_move = data.get("action") == "mousemove"
                        if limiter and not limiter.allow(is_move=is_move):
                            continue  # Drop event — rate limited
                        await self._handle_input_event(data)
                        continue

                    # ── Chat messages ──
                    user_message = data.get("message", "").strip()
                    if not user_message:
                        continue

                    # Send "thinking" indicator
                    await ws.send_json({"type": "thinking"})

                    # Route to agent
                    if self.on_chat_message:
                        response_text = await self.on_chat_message(chat_session_id, user_message)
                    else:
                        response_text = "Chat not connected to agent."

                    await ws.send_json(
                        {
                            "type": "response",
                            "content": response_text,
                        }
                    )

                elif msg.type in (WSMsgType.ERROR, WSMsgType.CLOSE):
                    break

        except Exception as e:
            logger.error("WebSocket error: %s", e)
        finally:
            self._input_limiters.pop(chat_session_id, None)
            logger.info("Viewer chat disconnected: %s", chat_session_id)

        return ws

    async def _handle_input_event(self, data: dict) -> None:
        """Handle mouse/keyboard input from the viewer overlay.

        Coordinates arrive as normalized 0.0-1.0 values. These are converted
        to absolute screen pixels for injection via the desktop input module.

        Supported actions:
          - click:        {"type":"input","action":"click","x":0.5,"y":0.3,"button":0}
          - double_click: {"type":"input","action":"double_click","x":0.5,"y":0.3}
          - right_click:  {"type":"input","action":"right_click","x":0.5,"y":0.3}
          - mousemove:    {"type":"input","action":"mousemove","x":0.5,"y":0.3}
          - mousedown:    {"type":"input","action":"mousedown","x":0.5,"y":0.3,"button":0}
          - mouseup:      {"type":"input","action":"mouseup","x":0.5,"y":0.3,"button":0}
          - scroll:       {"type":"input","action":"scroll","x":0.5,"y":0.3,
                          "direction":"down","amount":3}
          - key:          {"type":"input","action":"key","key":"a",
                          "ctrl":false,"alt":false,"shift":false}
        """
        action = data.get("action")

        if action in ("click", "double_click", "right_click"):
            from ghost_pc.desktop.capture import get_screen_dimensions
            from ghost_pc.desktop.input import click, double_click

            screen_w, screen_h = get_screen_dimensions()
            x = int(float(data.get("x", 0)) * screen_w)
            y = int(float(data.get("y", 0)) * screen_h)

            # Clamp to screen bounds
            x = max(0, min(x, screen_w - 1))
            y = max(0, min(y, screen_h - 1))

            if action == "click":
                button = "right" if data.get("button") == 2 else "left"
                await asyncio.to_thread(click, x, y, button)
            elif action == "double_click":
                await asyncio.to_thread(double_click, x, y)
            elif action == "right_click":
                await asyncio.to_thread(click, x, y, "right")

            logger.debug("Input: %s at (%d, %d)", action, x, y)

        elif action == "mousemove":
            from ghost_pc.desktop.capture import get_screen_dimensions
            from ghost_pc.desktop.input import move_mouse

            screen_w, screen_h = get_screen_dimensions()
            x = max(0, min(int(float(data.get("x", 0)) * screen_w), screen_w - 1))
            y = max(0, min(int(float(data.get("y", 0)) * screen_h), screen_h - 1))
            await asyncio.to_thread(move_mouse, x, y)

        elif action == "mousedown":
            from ghost_pc.desktop.capture import get_screen_dimensions
            from ghost_pc.desktop.input import mouse_down

            screen_w, screen_h = get_screen_dimensions()
            x = max(0, min(int(float(data.get("x", 0)) * screen_w), screen_w - 1))
            y = max(0, min(int(float(data.get("y", 0)) * screen_h), screen_h - 1))
            button = "right" if data.get("button") == 2 else "left"
            await asyncio.to_thread(mouse_down, x, y, button)

        elif action == "mouseup":
            from ghost_pc.desktop.capture import get_screen_dimensions
            from ghost_pc.desktop.input import mouse_up

            screen_w, screen_h = get_screen_dimensions()
            x = max(0, min(int(float(data.get("x", 0)) * screen_w), screen_w - 1))
            y = max(0, min(int(float(data.get("y", 0)) * screen_h), screen_h - 1))
            button = "right" if data.get("button") == 2 else "left"
            await asyncio.to_thread(mouse_up, x, y, button)

        elif action == "scroll":
            from ghost_pc.desktop.capture import get_screen_dimensions
            from ghost_pc.desktop.input import scroll

            screen_w, screen_h = get_screen_dimensions()
            x = int(float(data.get("x", 0.5)) * screen_w)
            y = int(float(data.get("y", 0.5)) * screen_h)
            direction = data.get("direction", "down")
            amount = int(data.get("amount", 3))
            await asyncio.to_thread(scroll, x, y, direction, amount)

        elif action == "key":
            from ghost_pc.desktop.input import hotkey, press_key, type_text

            key: str = data.get("key", "")
            if not key:
                return

            # Build modifier list
            modifiers: list[str] = []
            if data.get("ctrl"):
                modifiers.append("ctrl")
            if data.get("alt"):
                modifiers.append("alt")
            if data.get("shift"):
                modifiers.append("shift")

            # Normalize JS key names → input.py names
            # e.g. "ArrowUp" → "up", "Control" → "ctrl"
            js_key_map = {
                "ArrowUp": "up", "ArrowDown": "down",
                "ArrowLeft": "left", "ArrowRight": "right",
                "Control": "ctrl", "Meta": "win",
                " ": "space",
            }
            norm_key = js_key_map.get(key, key)

            if modifiers:
                # Key combo: ctrl+c, alt+tab, ctrl+shift+t, etc.
                # For single chars with modifiers, use lowercase
                combo_key = norm_key.lower() if len(norm_key) == 1 else norm_key.lower()
                await asyncio.to_thread(hotkey, *modifiers, combo_key)
            elif len(norm_key) == 1:
                # Single character — type it (preserves case)
                await asyncio.to_thread(type_text, norm_key)
            else:
                # Special key: Enter, Backspace, Tab, Escape, arrows, etc.
                await asyncio.to_thread(press_key, norm_key.lower())

    _capture_warned: bool = False

    def _capture_frame(self) -> bytes | None:
        """Capture screen and return JPEG bytes."""
        try:
            from ghost_pc.desktop.capture import grab_and_encode

            return grab_and_encode(quality=self.jpeg_quality)
        except Exception as e:
            if not self._capture_warned:
                logger.warning("Screen capture failed (%s): %s", type(e).__name__, e, exc_info=True)
                self._capture_warned = True
            return None


# Full viewer page with live screen + chat panel + interactive overlay + WebRTC
VIEWER_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
  <title>GhostPC - Live Screen</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #0a0a0a;
      --surface: #1a1a1a;
      --border: #333;
      --text: #e0e0e0;
      --text-dim: #888;
      --accent: #00d26a;
      --accent-dim: rgba(0, 210, 106, 0.15);
      --user-bg: #1e3a2f;
      --bot-bg: #1a1a2e;
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
    }

    /* Layout: screen on top, chat on bottom (mobile) or side-by-side (desktop) */
    .container {
      display: flex;
      flex-direction: column;
      height: 100%;
    }
    @media (min-width: 768px) {
      .container { flex-direction: row; }
    }

    /* Live screen section */
    .screen-section {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #000;
      position: relative;
      min-height: 40vh;
    }
    @media (min-width: 768px) {
      .screen-section { min-height: unset; flex: 2; }
    }
    .screen-section img,
    .screen-section video {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    /* Interactive overlay — sits on top of the screen for click-to-control */
    .input-overlay {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      z-index: 5;
      cursor: crosshair;
      /* Transparent until control mode is active */
      display: none;
    }
    .input-overlay.active {
      display: block;
    }
    /* Click ripple effect */
    .click-ripple {
      position: absolute;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 2px solid var(--accent);
      pointer-events: none;
      animation: ripple 0.4s ease-out forwards;
    }
    @keyframes ripple {
      0% { transform: translate(-50%,-50%) scale(0.5); opacity: 1; }
      100% { transform: translate(-50%,-50%) scale(2.5); opacity: 0; }
    }
    /* Remote cursor indicator dot */
    .cursor-indicator {
      position: absolute;
      width: 12px; height: 12px;
      margin-left: -6px; margin-top: -6px;
      border-radius: 50%;
      background: rgba(0, 210, 106, 0.8);
      border: 2px solid rgba(255, 255, 255, 0.9);
      pointer-events: none;
      z-index: 6;
      display: none;
      transition: left 0.03s linear, top 0.03s linear;
      box-shadow: 0 0 6px rgba(0, 210, 106, 0.5);
    }
    .cursor-indicator.active { display: block; }
    .cursor-indicator.dragging {
      background: rgba(255, 165, 0, 0.8);
      box-shadow: 0 0 10px rgba(255, 165, 0, 0.6);
    }

    /* Toolbar above the screen */
    .toolbar {
      position: absolute;
      top: 8px;
      left: 8px;
      z-index: 10;
      display: flex;
      gap: 6px;
    }
    .toolbar button {
      background: rgba(0,0,0,0.7);
      color: var(--text-dim);
      border: 1px solid transparent;
      font: bold 11px -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      padding: 5px 10px;
      border-radius: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s;
    }
    .toolbar button:hover {
      color: var(--text);
      background: rgba(0,0,0,0.85);
    }
    .toolbar button.active {
      color: var(--accent);
      border-color: var(--accent);
      background: rgba(0,210,106,0.1);
    }

    .status-badge {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(0,0,0,0.7);
      color: var(--accent);
      font: bold 11px monospace;
      padding: 4px 10px;
      border-radius: 12px;
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent);
      animation: pulse 2s infinite;
    }
    .loading-overlay {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      z-index: 2;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #000;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }

    /* Chat section */
    .chat-section {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: var(--surface);
      border-top: 1px solid var(--border);
      max-height: 60vh;
    }
    @media (min-width: 768px) {
      .chat-section {
        display: flex !important;
        position: static;
        max-height: unset;
        border-top: none;
        border-left: 1px solid var(--border);
        max-width: 400px;
        min-width: 320px;
        animation: none;
        border-radius: 0;
      }
    }

    .chat-header {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .chat-header .icon { font-size: 16px; }

    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .msg {
      padding: 8px 12px;
      border-radius: 12px;
      font-size: 14px;
      line-height: 1.4;
      max-width: 90%;
      word-break: break-word;
      white-space: pre-wrap;
    }
    .msg.user {
      background: var(--user-bg);
      align-self: flex-end;
      border-bottom-right-radius: 4px;
    }
    .msg.bot {
      background: var(--bot-bg);
      align-self: flex-start;
      border-bottom-left-radius: 4px;
    }
    .msg.system {
      color: var(--text-dim);
      font-size: 12px;
      text-align: center;
      align-self: center;
      background: none;
    }
    .msg.thinking {
      color: var(--text-dim);
      font-size: 12px;
      align-self: flex-start;
      background: none;
      padding: 4px 0;
    }
    .msg.thinking::after {
      content: '';
      animation: dots 1.5s infinite;
    }
    @keyframes dots {
      0% { content: '.'; }
      33% { content: '..'; }
      66% { content: '...'; }
    }

    .chat-input-area {
      padding: 12px;
      border-top: 1px solid var(--border);
      display: flex;
      gap: 8px;
    }
    .chat-input-area input {
      flex: 1;
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 10px 14px;
      border-radius: 20px;
      font-size: 14px;
      outline: none;
    }
    .chat-input-area input:focus {
      border-color: var(--accent);
    }
    .chat-input-area input::placeholder {
      color: var(--text-dim);
    }
    .chat-input-area button {
      background: var(--accent);
      color: #000;
      border: none;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .chat-input-area button:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }
    .chat-input-area button:hover:not(:disabled) {
      filter: brightness(1.1);
    }

    /* ── Fullscreen mode ── */
    .screen-section:fullscreen,
    .screen-section:-webkit-full-screen {
      width: 100vw;
      height: 100vh;
      min-height: unset;
    }
    .screen-section:fullscreen .toolbar,
    .screen-section:-webkit-full-screen .toolbar {
      opacity: 0;
      transition: opacity 0.3s;
    }
    .screen-section:fullscreen:hover .toolbar,
    .screen-section:-webkit-full-screen:hover .toolbar,
    .screen-section:fullscreen .toolbar:focus-within,
    .screen-section:-webkit-full-screen .toolbar:focus-within {
      opacity: 1;
    }
    /* On touch devices in fullscreen, keep toolbar visible briefly */
    .screen-section:fullscreen .toolbar.touch-visible {
      opacity: 1;
    }

    /* ── Hidden keyboard input for mobile ── */
    .mobile-kb-input {
      position: fixed;
      left: -9999px;
      top: 0;
      width: 1px;
      height: 1px;
      opacity: 0;
      font-size: 16px; /* prevents iOS zoom on focus */
    }

    /* ── Mobile: collapsible chat as overlay ── */
    @media (max-width: 767px) {
      .container { flex-direction: column; }
      .screen-section {
        flex: 1;
        min-height: unset;
        height: 100%;
      }
      .chat-section {
        display: none;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        max-height: 60vh;
        height: 60vh;
        z-index: 50;
        border-top: 1px solid var(--border);
        border-radius: 16px 16px 0 0;
        animation: slideUp 0.25s ease-out;
      }
      .chat-section.open { display: flex; }
      @keyframes slideUp {
        from { transform: translateY(100%); }
        to { transform: translateY(0); }
      }
      .chat-header {
        cursor: pointer;
        user-select: none;
        -webkit-user-select: none;
      }
      /* Floating chat toggle button */
      .chat-fab {
        position: fixed;
        bottom: 16px;
        right: 16px;
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: var(--accent);
        color: #000;
        border: none;
        font-size: 22px;
        cursor: pointer;
        z-index: 40;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        transition: transform 0.15s;
      }
      .chat-fab:active { transform: scale(0.9); }
      .chat-fab.hidden { display: none; }
      /* Unread badge on FAB */
      .chat-fab .badge {
        position: absolute;
        top: -2px;
        right: -2px;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #f44;
        color: #fff;
        font-size: 11px;
        font-weight: bold;
        display: none;
        align-items: center;
        justify-content: center;
      }
      .chat-fab .badge.show { display: flex; }
    }
    /* Desktop: hide FAB, show chat normally */
    @media (min-width: 768px) {
      .chat-fab { display: none !important; }
    }

    /* ── Touch-friendly toolbar buttons ── */
    @media (max-width: 767px) {
      .toolbar button {
        padding: 8px 12px;
        font-size: 12px;
        min-height: 36px;
        border-radius: 18px;
      }
    }

    /* ── Landscape on mobile: maximize screen, side chat ── */
    @media (max-height: 500px) and (orientation: landscape) {
      .screen-section {
        min-height: unset;
        height: 100vh;
        height: 100dvh;
      }
      .chat-section {
        max-height: 80vh;
        height: 80vh;
        right: 0;
        left: auto;
        width: 320px;
        bottom: 0;
        border-radius: 16px 0 0 0;
        animation: slideLeft 0.25s ease-out;
      }
      @keyframes slideLeft {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
      }
      .chat-fab {
        bottom: 12px;
        right: 12px;
        width: 44px;
        height: 44px;
        font-size: 18px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Live Screen -->
    <div class="screen-section" id="screenSection">
      <!-- Toolbar: control mode + keyboard + fullscreen toggles -->
      <div class="toolbar" id="toolbar">
        <button id="controlBtn" onclick="toggleControl()" title="Toggle remote control">
          &#9995; Control
        </button>
        <button id="kbBtn" onclick="toggleKeyboard()" title="Capture keyboard input">
          &#9000; Keyboard
        </button>
        <button id="fsBtn" onclick="toggleFullscreen()" title="Toggle fullscreen">
          &#x26F6; Fullscreen
        </button>
      </div>

      <div class="status-badge" id="status">
        <span class="status-dot"></span>
        <span id="streamMode">MJPEG</span>
      </div>

      <!-- Loading overlay — visible until first frame arrives -->
      <div id="loadingOverlay" class="loading-overlay">
        <div style="text-align:center;">
          <div style="color:#888;font-size:15px;margin-bottom:6px;">Connecting to screen...</div>
          <div id="loadingSubtext" style="color:#555;font-size:12px;">Initializing capture</div>
        </div>
      </div>

      <!-- MJPEG fallback image (visible by default) -->
      <img
        id="mjpegImg"
        alt="Live Screen"
        onerror="onStreamError()"
      >
      <!-- WebRTC video (hidden until negotiation succeeds) -->
      <video id="webrtcVideo" autoplay playsinline style="display:none"></video>

      <!-- Transparent overlay for mouse/touch input -->
      <div class="input-overlay" id="overlay"></div>
      <!-- Remote cursor indicator -->
      <div class="cursor-indicator" id="cursorDot"></div>
    </div>

    <!-- Hidden input for mobile on-screen keyboard -->
    <input type="text" id="mobileKbInput" class="mobile-kb-input"
           autocomplete="off" autocapitalize="off" autocorrect="off"
           spellcheck="false" inputmode="text">

    <!-- Floating chat toggle (mobile only) -->
    <button class="chat-fab" id="chatFab" onclick="toggleChat()">
      &#x1F4AC;
      <span class="badge" id="chatBadge">0</span>
    </button>

    <!-- Chat Panel -->
    <div class="chat-section" id="chatSection">
      <div class="chat-header" onclick="closeChatMobile()">
        <span class="icon">G</span>
        GhostPC Chat
        <span style="margin-left:auto;font-size:18px;display:none;" id="chatClose">&#x2715;</span>
      </div>
      <div class="chat-messages" id="messages"></div>
      <div class="chat-input-area">
        <input
          type="text"
          id="chatInput"
          placeholder="Type a command..."
          autocomplete="off"
        >
        <button id="sendBtn" onclick="sendMessage()">&#8593;</button>
      </div>
    </div>
  </div>

  <script>
    // ── Config — token injected server-side, URLs built client-side ──
    const TOKEN = '{{TOKEN}}';
    const STREAM_URL = '/stream?token=' + TOKEN;
    const WS_PROTO = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const WS_URL = WS_PROTO + '//' + location.host + '/ws?token=' + TOKEN;

    // ── DOM refs ──
    const messagesEl = document.getElementById('messages');
    const inputEl = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const overlay = document.getElementById('overlay');
    const mjpegImg = document.getElementById('mjpegImg');
    const webrtcVideo = document.getElementById('webrtcVideo');
    const controlBtn = document.getElementById('controlBtn');
    const kbBtn = document.getElementById('kbBtn');
    const fsBtn = document.getElementById('fsBtn');
    const screenSection = document.getElementById('screenSection');
    const chatSection = document.getElementById('chatSection');
    const chatFab = document.getElementById('chatFab');
    const chatBadge = document.getElementById('chatBadge');
    const chatClose = document.getElementById('chatClose');
    const mobileKbInput = document.getElementById('mobileKbInput');
    const toolbarEl = document.getElementById('toolbar');
    const streamModeEl = document.getElementById('streamMode');
    const loadingOverlay = document.getElementById('loadingOverlay');

    let ws = null;
    let thinking = null;
    let controlMode = false;
    let kbCapture = false;
    let lastClickTime = 0;
    let rtcPc = null;
    let screenLoaded = false;
    let chatOpen = false;
    let unreadCount = 0;
    const isMobile = window.matchMedia('(max-width: 767px)').matches
      || ('ontouchstart' in window);

    // Drag / cursor state
    let isDragging = false;
    let mouseIsDown = false;
    let mouseDownPos = null;
    let lastMoveTime = 0;
    const MOVE_THROTTLE_MS = 16;   // ~60fps
    const CLICK_THRESHOLD = 5;     // px — below = click, above = drag
    const TOUCH_CLICK_THRESHOLD = 10;
    const cursorDot = document.getElementById('cursorDot');

    // ── Loading overlay — hide on first frame, show error after timeout ──

    mjpegImg.onload = function() {
      if (!screenLoaded) {
        screenLoaded = true;
        loadingOverlay.style.display = 'none';
      }
    };
    setTimeout(function() {
      if (!screenLoaded) {
        document.getElementById('loadingSubtext').textContent =
          'Screen capture may have failed — check the GhostPC terminal';
        document.getElementById('loadingSubtext').style.color = '#f44';
      }
    }, 15000);

    // Start MJPEG stream
    mjpegImg.src = STREAM_URL;

    // ── WebSocket (chat + input) ──

    let wsRetries = 0;
    const MAX_WS_RETRIES = 5;

    function connect() {
      if (wsRetries >= MAX_WS_RETRIES) {
        addMessage('Connection lost. Refresh the page to reconnect.', 'system');
        return;
      }
      ws = new WebSocket(WS_URL);

      ws.onopen = () => { wsRetries = 0; console.log('WebSocket connected'); };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (thinking) { thinking.remove(); thinking = null; }

        if (data.type === 'system') {
          addMessage(data.content, 'system');
        } else if (data.type === 'thinking') {
          thinking = addMessage('Thinking', 'thinking');
        } else if (data.type === 'response') {
          addMessage(data.content, 'bot');
          inputEl.disabled = false;
          sendBtn.disabled = false;
          inputEl.focus();
        } else if (data.type === 'error') {
          addMessage('Error: ' + data.content, 'system');
          inputEl.disabled = false;
          sendBtn.disabled = false;
        }
      };

      ws.onclose = () => {
        wsRetries++;
        addMessage('Disconnected. Reconnecting (' +
          wsRetries + '/' + MAX_WS_RETRIES + ')...', 'system');
        setTimeout(connect, 3000);
      };

      ws.onerror = () => console.error('WebSocket error');
    }

    function wsSend(obj) {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(obj));
      }
    }

    // ── Chat ──

    function addMessage(text, type) {
      const el = document.createElement('div');
      el.className = 'msg ' + type;
      el.textContent = text;
      messagesEl.appendChild(el);
      messagesEl.scrollTop = messagesEl.scrollHeight;
      // Update unread badge on mobile when chat is closed
      if (isMobile && !chatOpen && type === 'bot') {
        unreadCount++;
        chatBadge.textContent = unreadCount > 9 ? '9+' : String(unreadCount);
        chatBadge.classList.add('show');
      }
      return el;
    }

    function sendMessage() {
      const text = inputEl.value.trim();
      if (!text || !ws || ws.readyState !== WebSocket.OPEN) return;
      addMessage(text, 'user');
      ws.send(JSON.stringify({ message: text }));
      inputEl.value = '';
      inputEl.disabled = true;
      sendBtn.disabled = true;
    }

    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    // ── Control mode toggle ──

    function toggleControl() {
      controlMode = !controlMode;
      controlBtn.classList.toggle('active', controlMode);
      overlay.classList.toggle('active', controlMode);
      if (controlMode) {
        cursorDot.classList.add('active');
      } else {
        cursorDot.classList.remove('active', 'dragging');
        // Release button if held when disabling control
        if (mouseIsDown) {
          wsSend({ type: 'input', action: 'mouseup', x: 0.5, y: 0.5, button: 0 });
          mouseIsDown = false;
          isDragging = false;
          mouseDownPos = null;
        }
      }
    }

    // ── Keyboard capture toggle ──

    function toggleKeyboard() {
      kbCapture = !kbCapture;
      kbBtn.classList.toggle('active', kbCapture);
      // On mobile, focus a hidden input to trigger the on-screen keyboard
      if (kbCapture && isMobile) {
        mobileKbInput.focus();
      } else if (!kbCapture) {
        mobileKbInput.blur();
      }
    }

    // ── Mobile keyboard input handling ──
    // Captures input from the on-screen keyboard via the hidden input field

    mobileKbInput.addEventListener('input', (e) => {
      if (!kbCapture) return;
      const val = e.data || mobileKbInput.value;
      if (val) {
        // Send each character as a key event
        for (const ch of val) {
          wsSend({
            type: 'input', action: 'key', key: ch,
            ctrl: false, alt: false, shift: false,
          });
        }
      }
      mobileKbInput.value = '';
    });

    mobileKbInput.addEventListener('keydown', (e) => {
      if (!kbCapture) return;
      // Handle special keys that don't trigger 'input' event
      const specialKeys = ['Backspace', 'Enter', 'Tab', 'Escape',
        'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'];
      if (specialKeys.includes(e.key)) {
        e.preventDefault();
        wsSend({
          type: 'input', action: 'key', key: e.key,
          ctrl: e.ctrlKey, alt: e.altKey, shift: e.shiftKey,
        });
      }
    });

    // Keep mobile input focused when keyboard capture is on
    mobileKbInput.addEventListener('blur', () => {
      if (kbCapture && isMobile) {
        // Small delay to allow intentional blur (e.g., toggling off)
        setTimeout(() => {
          if (kbCapture) mobileKbInput.focus();
        }, 300);
      }
    });

    // ── Fullscreen toggle ──

    function toggleFullscreen() {
      if (document.fullscreenElement || document.webkitFullscreenElement) {
        (document.exitFullscreen || document.webkitExitFullscreen).call(document);
      } else {
        const fn = screenSection.requestFullscreen
          || screenSection.webkitRequestFullscreen;
        fn.call(screenSection);
      }
    }

    // Update button state on fullscreen change
    document.addEventListener('fullscreenchange', onFsChange);
    document.addEventListener('webkitfullscreenchange', onFsChange);
    function onFsChange() {
      const isFs = !!(document.fullscreenElement || document.webkitFullscreenElement);
      fsBtn.classList.toggle('active', isFs);
      fsBtn.innerHTML = isFs ? '&#x2716; Exit' : '&#x26F6; Fullscreen';
    }

    // On touch devices in fullscreen, briefly show toolbar on tap
    screenSection.addEventListener('touchstart', () => {
      if (document.fullscreenElement || document.webkitFullscreenElement) {
        toolbarEl.classList.add('touch-visible');
        clearTimeout(screenSection._toolbarTimer);
        screenSection._toolbarTimer = setTimeout(() => {
          toolbarEl.classList.remove('touch-visible');
        }, 3000);
      }
    }, { passive: true });

    // ── Mobile chat toggle ──

    function toggleChat() {
      chatOpen = !chatOpen;
      chatSection.classList.toggle('open', chatOpen);
      if (chatOpen) {
        unreadCount = 0;
        chatBadge.classList.remove('show');
        chatBadge.textContent = '0';
        inputEl.focus();
      }
    }

    function closeChatMobile() {
      if (isMobile && chatOpen) {
        chatOpen = false;
        chatSection.classList.remove('open');
      }
    }

    // Init: on mobile show close button in chat header, on desktop show chat by default
    if (isMobile) {
      chatClose.style.display = 'inline';
    } else {
      chatSection.classList.add('open');
      chatSection.style.display = 'flex';
    }

    // ── Compute normalized coords relative to the visible screen area ──

    function getScreenCoords(clientX, clientY) {
      // Use the currently visible media element (video or img)
      const el = webrtcVideo.style.display !== 'none' ? webrtcVideo : mjpegImg;
      const rect = el.getBoundingClientRect();

      // object-fit: contain leaves black bars — compute the actual rendered area
      const elAspect = el.videoWidth
        ? el.videoWidth / el.videoHeight
        : (el.naturalWidth || rect.width) / (el.naturalHeight || rect.height);
      const boxAspect = rect.width / rect.height;

      let renderW, renderH, offsetX, offsetY;
      if (elAspect > boxAspect) {
        // Pillarboxed (black bars top/bottom)
        renderW = rect.width;
        renderH = rect.width / elAspect;
        offsetX = 0;
        offsetY = (rect.height - renderH) / 2;
      } else {
        // Letterboxed (black bars left/right)
        renderH = rect.height;
        renderW = rect.height * elAspect;
        offsetX = (rect.width - renderW) / 2;
        offsetY = 0;
      }

      const localX = clientX - rect.left - offsetX;
      const localY = clientY - rect.top - offsetY;

      // Clamp to [0, 1]
      const nx = Math.max(0, Math.min(1, localX / renderW));
      const ny = Math.max(0, Math.min(1, localY / renderH));
      return { x: nx, y: ny };
    }

    // ── Click ripple visual feedback ──

    function showRipple(clientX, clientY) {
      const section = document.getElementById('screenSection');
      const rect = section.getBoundingClientRect();
      const ripple = document.createElement('div');
      ripple.className = 'click-ripple';
      ripple.style.left = (clientX - rect.left) + 'px';
      ripple.style.top = (clientY - rect.top) + 'px';
      section.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove());
    }

    // ── Cursor indicator position helper ──

    function updateCursorIndicator(normX, normY) {
      const el = webrtcVideo.style.display !== 'none' ? webrtcVideo : mjpegImg;
      const rect = el.getBoundingClientRect();
      const section = document.getElementById('screenSection');
      const sRect = section.getBoundingClientRect();

      const elAspect = el.videoWidth
        ? el.videoWidth / el.videoHeight
        : (el.naturalWidth || rect.width) / (el.naturalHeight || rect.height);
      const boxAspect = rect.width / rect.height;

      let renderW, renderH, offsetX, offsetY;
      if (elAspect > boxAspect) {
        renderW = rect.width;
        renderH = rect.width / elAspect;
        offsetX = 0;
        offsetY = (rect.height - renderH) / 2;
      } else {
        renderH = rect.height;
        renderW = rect.height * elAspect;
        offsetX = (rect.width - renderW) / 2;
        offsetY = 0;
      }

      const px = (rect.left - sRect.left) + offsetX + normX * renderW;
      const py = (rect.top - sRect.top) + offsetY + normY * renderH;
      cursorDot.style.left = px + 'px';
      cursorDot.style.top = py + 'px';
    }

    // ── Mouse events on overlay ──

    overlay.addEventListener('mousedown', (e) => {
      if (e.button === 2) return; // right-click handled by contextmenu
      e.preventDefault();
      const { x, y } = getScreenCoords(e.clientX, e.clientY);
      mouseIsDown = true;
      isDragging = false;
      mouseDownPos = { cx: e.clientX, cy: e.clientY, x, y };
      wsSend({ type: 'input', action: 'mousedown', x, y, button: e.button });
    });

    overlay.addEventListener('mousemove', (e) => {
      const { x, y } = getScreenCoords(e.clientX, e.clientY);
      updateCursorIndicator(x, y);

      const now = Date.now();
      if (now - lastMoveTime < MOVE_THROTTLE_MS) return;
      lastMoveTime = now;

      // Detect drag threshold
      if (mouseIsDown && !isDragging && mouseDownPos) {
        const dx = e.clientX - mouseDownPos.cx;
        const dy = e.clientY - mouseDownPos.cy;
        if (Math.sqrt(dx * dx + dy * dy) > CLICK_THRESHOLD) {
          isDragging = true;
          cursorDot.classList.add('dragging');
        }
      }

      wsSend({ type: 'input', action: 'mousemove', x, y });
    });

    overlay.addEventListener('mouseup', (e) => {
      if (e.button === 2) return;
      e.preventDefault();
      const { x, y } = getScreenCoords(e.clientX, e.clientY);
      wsSend({ type: 'input', action: 'mouseup', x, y, button: e.button });

      if (!isDragging) {
        // Treat as click — check for double-click
        const now = Date.now();
        if (now - lastClickTime < 300) {
          wsSend({ type: 'input', action: 'double_click', x, y });
        }
        lastClickTime = now;
        showRipple(e.clientX, e.clientY);
      }

      mouseIsDown = false;
      isDragging = false;
      mouseDownPos = null;
      cursorDot.classList.remove('dragging');
    });

    overlay.addEventListener('mouseleave', (e) => {
      if (mouseIsDown) {
        const { x, y } = getScreenCoords(e.clientX, e.clientY);
        wsSend({ type: 'input', action: 'mouseup', x, y, button: 0 });
        mouseIsDown = false;
        isDragging = false;
        mouseDownPos = null;
        cursorDot.classList.remove('dragging');
      }
    });

    overlay.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      const { x, y } = getScreenCoords(e.clientX, e.clientY);
      wsSend({ type: 'input', action: 'right_click', x, y });
      showRipple(e.clientX, e.clientY);
    });

    overlay.addEventListener('wheel', (e) => {
      e.preventDefault();
      const { x, y } = getScreenCoords(e.clientX, e.clientY);
      const direction = e.deltaY > 0 ? 'down' : 'up';
      const amount = Math.max(1, Math.round(Math.abs(e.deltaY) / 40));
      wsSend({ type: 'input', action: 'scroll', x, y, direction, amount });
    }, { passive: false });

    // ── Touch events on overlay (mobile) ──

    let touchDownPos = null;
    let touchIsDragging = false;

    overlay.addEventListener('touchstart', (e) => {
      if (e.touches.length === 0) return;
      e.preventDefault();
      const touch = e.touches[0];
      const { x, y } = getScreenCoords(touch.clientX, touch.clientY);
      touchDownPos = { cx: touch.clientX, cy: touch.clientY, x, y };
      touchIsDragging = false;
      mouseIsDown = true;
      wsSend({ type: 'input', action: 'mousedown', x, y, button: 0 });
      updateCursorIndicator(x, y);
    }, { passive: false });

    overlay.addEventListener('touchmove', (e) => {
      if (e.touches.length === 0) return;
      e.preventDefault();
      const touch = e.touches[0];
      const { x, y } = getScreenCoords(touch.clientX, touch.clientY);
      updateCursorIndicator(x, y);

      const now = Date.now();
      if (now - lastMoveTime < MOVE_THROTTLE_MS) return;
      lastMoveTime = now;

      if (!touchIsDragging && touchDownPos) {
        const dx = touch.clientX - touchDownPos.cx;
        const dy = touch.clientY - touchDownPos.cy;
        if (Math.sqrt(dx * dx + dy * dy) > TOUCH_CLICK_THRESHOLD) {
          touchIsDragging = true;
          cursorDot.classList.add('dragging');
        }
      }

      wsSend({ type: 'input', action: 'mousemove', x, y });
    }, { passive: false });

    overlay.addEventListener('touchend', (e) => {
      if (e.changedTouches.length === 0) return;
      e.preventDefault();
      const touch = e.changedTouches[0];
      const { x, y } = getScreenCoords(touch.clientX, touch.clientY);
      wsSend({ type: 'input', action: 'mouseup', x, y, button: 0 });

      if (!touchIsDragging) {
        showRipple(touch.clientX, touch.clientY);
      }

      mouseIsDown = false;
      touchIsDragging = false;
      touchDownPos = null;
      cursorDot.classList.remove('dragging');
    });

    overlay.addEventListener('touchcancel', () => {
      if (mouseIsDown) {
        wsSend({ type: 'input', action: 'mouseup', x: 0.5, y: 0.5, button: 0 });
        mouseIsDown = false;
        touchIsDragging = false;
        touchDownPos = null;
        cursorDot.classList.remove('dragging');
      }
    });

    // ── Keyboard capture ──

    document.addEventListener('keydown', (e) => {
      if (!kbCapture) return;
      // Don't capture when chat input or mobile kb input is focused
      if (document.activeElement === inputEl) return;
      if (document.activeElement === mobileKbInput) return;

      // Skip modifier-only keys (they're sent as part of combos)
      if (['Control', 'Alt', 'Shift', 'Meta'].includes(e.key)) return;

      e.preventDefault();
      e.stopPropagation();

      wsSend({
        type: 'input',
        action: 'key',
        key: e.key,
        ctrl: e.ctrlKey,
        alt: e.altKey,
        shift: e.shiftKey,
      });
    });

    // ── WebRTC upgrade (try first, fall back to MJPEG) ──

    async function tryWebRTC() {
      try {
        const res = await fetch('/webrtc/status');
        const info = await res.json();
        if (!info.available) return;

        const pc = new RTCPeerConnection();
        rtcPc = pc;

        pc.addTransceiver('video', { direction: 'recvonly' });

        pc.ontrack = (event) => {
          webrtcVideo.srcObject = event.streams[0];
          webrtcVideo.style.display = '';
          mjpegImg.style.display = 'none';
          streamModeEl.textContent = 'WebRTC';
          screenLoaded = true;
          loadingOverlay.style.display = 'none';
          console.log('WebRTC stream active');
        };

        pc.oniceconnectionstatechange = () => {
          if (pc.iceConnectionState === 'failed' || pc.iceConnectionState === 'disconnected') {
            console.warn('WebRTC connection lost, falling back to MJPEG');
            fallbackToMJPEG();
          }
        };

        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        const sdpRes = await fetch('/webrtc/offer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sdp: offer.sdp, type: offer.type }),
        });

        if (!sdpRes.ok) {
          console.warn('WebRTC offer rejected, staying on MJPEG');
          pc.close();
          rtcPc = null;
          return;
        }

        const answer = await sdpRes.json();
        await pc.setRemoteDescription(new RTCSessionDescription(answer));
      } catch (err) {
        console.warn('WebRTC setup failed:', err.message);
        fallbackToMJPEG();
      }
    }

    function fallbackToMJPEG() {
      if (rtcPc) { rtcPc.close(); rtcPc = null; }
      webrtcVideo.style.display = 'none';
      mjpegImg.style.display = '';
      streamModeEl.textContent = 'MJPEG';
    }

    function onStreamError() {
      document.getElementById('status').querySelector('.status-dot').style.background = '#f44';
      streamModeEl.textContent = 'OFFLINE';
      // Show error in loading overlay if screen never loaded
      if (!screenLoaded) {
        document.getElementById('loadingSubtext').textContent =
          'Stream connection failed — check the GhostPC terminal';
        document.getElementById('loadingSubtext').style.color = '#f44';
      }
    }

    // ── Init ──

    connect();
    tryWebRTC();
  </script>
</body>
</html>
"""
