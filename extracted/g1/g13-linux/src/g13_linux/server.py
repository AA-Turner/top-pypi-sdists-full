"""
G13 WebSocket/HTTP Server

Provides remote control API for the G13 daemon.
Supports WebSocket for real-time updates and REST API for CRUD operations.
"""

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING

from aiohttp import web

from ._paths import get_static_dir

if TYPE_CHECKING:
    from .daemon import G13Daemon

logger = logging.getLogger(__name__)

# Default path to web GUI build output
DEFAULT_STATIC_DIR = get_static_dir()


class G13Server:
    """
    WebSocket and HTTP API server for G13 daemon.

    WebSocket: ws://host:port/ws
    REST API: http://host:port/api/...
    """

    def __init__(
        self,
        daemon: "G13Daemon",
        host: str = "127.0.0.1",
        port: int = 8765,
        static_dir: str | Path | None = None,
    ):
        """
        Initialize server.

        Args:
            daemon: G13Daemon instance to control
            host: Host to bind to
            port: Port to listen on
            static_dir: Directory containing static web files (default: gui-web/dist)
        """
        self.daemon = daemon
        self.host = host
        self.port = port
        self._app: web.Application | None = None
        self._runner: web.AppRunner | None = None
        self._site: web.TCPSite | None = None
        self._clients: set[web.WebSocketResponse] = set()

        # Static file serving
        if static_dir is None:
            self._static_dir = DEFAULT_STATIC_DIR
        else:
            self._static_dir = Path(static_dir)
        self._serve_static = self._static_dir.exists() and self._static_dir.is_dir()

    async def start(self):
        """Start the server."""
        self._app = web.Application()
        self._setup_routes()

        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, self.host, self.port)
        await self._site.start()

        logger.info(f"G13 server started at http://{self.host}:{self.port}")
        if self._serve_static:
            logger.info(f"Serving web GUI from {self._static_dir}")

    async def stop(self):
        """Stop the server."""
        # Close all WebSocket connections
        for ws in list(self._clients):
            await ws.close()
        self._clients.clear()

        if self._site:
            await self._site.stop()
        if self._runner:
            await self._runner.cleanup()

        logger.info("G13 server stopped")

    def _setup_routes(self):
        """Setup HTTP and WebSocket routes."""
        app = self._app

        # WebSocket endpoint
        app.router.add_get("/ws", self._handle_websocket)

        # REST API endpoints
        app.router.add_get("/api/status", self._api_get_status)
        app.router.add_get("/api/profiles", self._api_list_profiles)
        app.router.add_get("/api/profiles/{name}", self._api_get_profile)
        app.router.add_post("/api/profiles/{name}", self._api_save_profile)
        app.router.add_delete("/api/profiles/{name}", self._api_delete_profile)
        app.router.add_post("/api/profiles/{name}/activate", self._api_activate_profile)
        app.router.add_get("/api/macros", self._api_list_macros)
        app.router.add_get("/api/macros/{id}", self._api_get_macro)
        app.router.add_post("/api/macros", self._api_create_macro)
        app.router.add_put("/api/macros/{id}", self._api_update_macro)
        app.router.add_delete("/api/macros/{id}", self._api_delete_macro)

        # CORS headers for development
        app.router.add_route("OPTIONS", "/{path:.*}", self._handle_options)

        # Static file serving (web GUI)
        if self._serve_static:
            # Serve assets directory
            app.router.add_static("/assets", self._static_dir / "assets", show_index=False)
            # Serve root files (favicon, etc.)
            app.router.add_get("/vite.svg", self._serve_static_file)
            # SPA fallback - serve index.html for all other GET requests
            app.router.add_get("/", self._serve_index)
            app.router.add_get("/{path:.*}", self._serve_spa_fallback)

    def _add_cors_headers(self, response: web.Response) -> web.Response:
        """Add CORS headers to response."""
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    async def _handle_options(self, request: web.Request) -> web.Response:
        """Handle CORS preflight requests."""
        return self._add_cors_headers(web.Response())

    # Static file serving

    async def _serve_index(self, request: web.Request) -> web.Response:
        """Serve index.html for root path."""
        return await self._serve_html_file("index.html")

    async def _serve_static_file(self, request: web.Request) -> web.Response:
        """Serve a static file from the static directory."""
        filename = request.path.lstrip("/")
        file_path = self._static_dir / filename

        if not file_path.exists() or not file_path.is_file():
            raise web.HTTPNotFound()

        return web.FileResponse(file_path)

    async def _serve_spa_fallback(self, request: web.Request) -> web.Response:
        """
        SPA fallback handler.

        For paths that don't match API routes, serve index.html
        to allow client-side routing to handle the path.
        """
        path = request.match_info.get("path", "")

        # Don't intercept API or WebSocket paths
        if path.startswith("api/") or path == "ws":
            raise web.HTTPNotFound()

        # Try to serve as static file first
        file_path = self._static_dir / path
        if file_path.exists() and file_path.is_file():
            return web.FileResponse(file_path)

        # Fall back to index.html for SPA routing
        return await self._serve_html_file("index.html")

    async def _serve_html_file(self, filename: str) -> web.Response:
        """Serve an HTML file with proper content type."""
        file_path = self._static_dir / filename

        if not file_path.exists():
            raise web.HTTPNotFound()

        return web.FileResponse(file_path, headers={"Content-Type": "text/html"})

    # WebSocket handling

    async def _handle_websocket(self, request: web.Request) -> web.WebSocketResponse:
        """Handle WebSocket connections."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        self._clients.add(ws)
        logger.info(f"WebSocket client connected ({len(self._clients)} total)")

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    await self._handle_ws_message(ws, msg.data)
                elif msg.type == web.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
        finally:
            self._clients.discard(ws)
            logger.info(f"WebSocket client disconnected ({len(self._clients)} total)")

        return ws

    async def _ws_set_mode(self, ws, message):
        """Handle set_mode message."""
        mode = message.get("mode", "M1")
        self.daemon.set_mode(mode)
        # Broadcast is handled by daemon.set_mode()

    async def _ws_set_mapping(self, ws, message):
        """Handle set_mapping message."""
        button = message.get("button")
        key = message.get("key")
        if button and key:
            success = self.daemon.set_button_mapping(button, key)
            if success:
                await self._broadcast({"type": "mapping_changed", "button": button, "key": key})
                logger.info(f"Set mapping: {button} -> {key}")
            else:
                await ws.send_json({"type": "error", "message": "Failed to update mapping"})
        else:
            await ws.send_json({"type": "error", "message": "Missing button or key parameter"})

    async def _ws_simulate_press(self, ws, message):
        """Handle simulate_press message."""
        await self._broadcast({"type": "button_pressed", "button": message.get("button")})

    async def _ws_simulate_release(self, ws, message):
        """Handle simulate_release message."""
        await self._broadcast({"type": "button_released", "button": message.get("button")})

    async def _ws_set_backlight(self, ws, message):
        """Handle set_backlight message."""
        color = message.get("color", "#ffffff")
        brightness = message.get("brightness", 100)
        self._set_backlight(color, brightness)
        await self._broadcast(
            {
                "type": "backlight_changed",
                "backlight": {"color": color, "brightness": brightness},
            }
        )

    async def _ws_handle_play_macro(self, ws, message):
        """Handle play_macro message."""
        await self._ws_play_macro(ws, message.get("macro_id"))

    async def _ws_handle_stop_macro(self, ws, message):
        """Handle stop_macro message."""
        await self._ws_stop_macro(ws)

    async def _ws_handle_get_macros(self, ws, message):
        """Handle get_macros message."""
        await self._ws_send_macros(ws)

    async def _ws_handle_get_state(self, ws, message):
        """Handle get_state message."""
        await self._ws_send_state(ws)

    async def _handle_ws_message(self, ws: web.WebSocketResponse, data: str):
        """
        Handle incoming WebSocket message.

        Args:
            ws: WebSocket connection
            data: JSON message string
        """
        handlers = {
            "get_state": self._ws_handle_get_state,
            "set_mode": self._ws_set_mode,
            "set_mapping": self._ws_set_mapping,
            "simulate_press": self._ws_simulate_press,
            "simulate_release": self._ws_simulate_release,
            "set_backlight": self._ws_set_backlight,
            "play_macro": self._ws_handle_play_macro,
            "stop_macro": self._ws_handle_stop_macro,
            "get_macros": self._ws_handle_get_macros,
        }

        try:
            message = json.loads(data)
            msg_type = message.get("type")
            handler = handlers.get(msg_type)
            if handler:
                await handler(ws, message)
            else:
                logger.warning(f"Unknown WebSocket message type: {msg_type}")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in WebSocket message: {data}")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")

    async def _ws_send_state(self, ws: web.WebSocketResponse):
        """Send current state to a WebSocket client."""
        state = self._get_state()
        await ws.send_json({"type": "state", "data": state})

    async def _ws_send_macros(self, ws: web.WebSocketResponse):
        """Send macro list to a WebSocket client."""
        mm = self.daemon.macro_manager
        macros = mm.list_macro_summaries()
        await ws.send_json({"type": "macros", "data": macros})

    async def _ws_play_macro(self, ws: web.WebSocketResponse, macro_id: str):
        """Play a macro by ID."""
        if not macro_id:
            await ws.send_json({"type": "error", "message": "No macro_id provided"})
            return

        mm = self.daemon.macro_manager

        try:
            macro = mm.load_macro(macro_id)
            # Notify clients that playback is starting
            await self._broadcast(
                {"type": "macro_playback_started", "macro_id": macro_id, "name": macro.name}
            )

            # Execute macro steps (simplified - no UInput for daemon mode)
            # Full playback with key injection would require the GUI player
            logger.info(f"Playing macro: {macro.name} ({len(macro.steps)} steps)")

            for i, step in enumerate(macro.steps):
                # Broadcast each step for visualization
                await self._broadcast(
                    {
                        "type": "macro_step",
                        "step_index": i,
                        "total_steps": len(macro.steps),
                        "step": step.to_dict(),
                    }
                )

            await self._broadcast({"type": "macro_playback_complete", "macro_id": macro_id})

        except FileNotFoundError:
            await ws.send_json({"type": "error", "message": f"Macro '{macro_id}' not found"})
        except Exception as e:
            await ws.send_json({"type": "error", "message": str(e)})

    async def _ws_stop_macro(self, ws: web.WebSocketResponse):
        """Stop current macro playback."""
        # For now, just broadcast stop - full implementation would track playback state
        await self._broadcast({"type": "macro_playback_stopped"})
        logger.info("Macro playback stop requested")

    async def _broadcast(self, message: dict):
        """Broadcast message to all connected WebSocket clients."""
        if not self._clients:
            return

        data = json.dumps(message)
        for ws in list(self._clients):
            try:
                await ws.send_str(data)
            except Exception:
                self._clients.discard(ws)

    def _get_state(self) -> dict:
        """Get current G13 state."""
        profile_name = None
        if self.daemon.profile_manager and self.daemon.profile_manager.current_name:
            profile_name = self.daemon.profile_manager.current_name

        backlight_color = "#ff6b00"
        backlight_brightness = 100
        if self.daemon._led_controller:
            color = self.daemon._led_controller.current_color
            backlight_color = color.to_hex()
            backlight_brightness = self.daemon._led_controller.brightness

        # Get pressed keys from event decoder
        pressed_keys = []
        if self.daemon._event_decoder and self.daemon._event_decoder.last_state:
            pressed_keys = self.daemon._event_decoder.get_pressed_buttons()

        # Get joystick position
        joystick_x, joystick_y = self.daemon._last_joystick

        return {
            "connected": self.daemon._device is not None,
            "active_profile": profile_name,
            "active_mode": self.daemon._current_mode,
            "pressed_keys": pressed_keys,
            "joystick": {"x": joystick_x, "y": joystick_y},
            "backlight": {
                "color": backlight_color,
                "brightness": backlight_brightness,
            },
        }

    def _set_backlight(self, color: str, brightness: int):
        """Set backlight color and brightness."""
        if not self.daemon._led_controller:
            return

        # Parse hex color
        if color.startswith("#") and len(color) == 7:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            self.daemon._led_controller.set_color(r, g, b)

        if brightness is not None:
            self.daemon._led_controller.set_brightness(brightness)

    # Broadcast helpers for daemon events

    async def broadcast_button_pressed(self, button: str):
        """Broadcast button press event."""
        await self._broadcast({"type": "button_pressed", "button": button})

    async def broadcast_button_released(self, button: str):
        """Broadcast button release event."""
        await self._broadcast({"type": "button_released", "button": button})

    async def broadcast_profile_activated(self, name: str):
        """Broadcast profile activation event."""
        await self._broadcast({"type": "profile_activated", "name": name})

    async def broadcast_device_connected(self):
        """Broadcast device connected event."""
        await self._broadcast({"type": "device_connected"})

    async def broadcast_device_disconnected(self):
        """Broadcast device disconnected event."""
        await self._broadcast({"type": "device_disconnected"})

    # REST API handlers

    async def _api_get_status(self, request: web.Request) -> web.Response:
        """GET /api/status - Get device status."""
        state = self._get_state()
        response = web.json_response(
            {
                "connected": state["connected"],
                "active_profile": state["active_profile"],
                "active_mode": state["active_mode"],
            }
        )
        return self._add_cors_headers(response)

    async def _api_list_profiles(self, request: web.Request) -> web.Response:
        """GET /api/profiles - List available profiles."""
        pm = self.daemon.profile_manager
        profiles = []

        for name in pm.list_profiles():
            try:
                profile = pm.load_profile(name)
                profiles.append(
                    {
                        "name": name,
                        "filename": f"{name}.json",
                        "description": profile.description or "",
                    }
                )
            except Exception:
                profiles.append(
                    {
                        "name": name,
                        "filename": f"{name}.json",
                        "description": "",
                    }
                )

        response = web.json_response({"profiles": profiles})
        return self._add_cors_headers(response)

    async def _api_get_profile(self, request: web.Request) -> web.Response:
        """GET /api/profiles/{name} - Get profile details."""
        name = request.match_info["name"]
        pm = self.daemon.profile_manager

        try:
            profile = pm.load_profile(name)
            response = web.json_response(asdict(profile))
        except FileNotFoundError:
            response = web.json_response({"error": "Profile not found"}, status=404)

        return self._add_cors_headers(response)

    async def _api_save_profile(self, request: web.Request) -> web.Response:
        """POST /api/profiles/{name} - Save profile."""
        name = request.match_info["name"]
        pm = self.daemon.profile_manager

        try:
            data = await request.json()

            # Create or update profile
            if pm.profile_exists(name):
                profile = pm.load_profile(name)
            else:
                profile = pm.create_profile(name)

            # Update fields
            if "name" in data:
                profile.name = data["name"]
            if "description" in data:
                profile.description = data["description"]
            if "mappings" in data:
                profile.mappings = data["mappings"]
            if "backlight" in data:
                profile.backlight = data["backlight"]

            pm.save_profile(profile, name)
            response = web.json_response({"status": "saved"})

        except Exception as e:
            response = web.json_response({"error": str(e)}, status=400)

        return self._add_cors_headers(response)

    async def _api_delete_profile(self, request: web.Request) -> web.Response:
        """DELETE /api/profiles/{name} - Delete profile."""
        name = request.match_info["name"]
        pm = self.daemon.profile_manager

        try:
            pm.delete_profile(name)
            response = web.json_response({"status": "deleted"})
        except FileNotFoundError:
            response = web.json_response({"error": "Profile not found"}, status=404)

        return self._add_cors_headers(response)

    async def _api_activate_profile(self, request: web.Request) -> web.Response:
        """POST /api/profiles/{name}/activate - Activate profile."""
        name = request.match_info["name"]

        try:
            if self.daemon.load_profile(name):
                await self._broadcast({"type": "profile_activated", "name": name})
                response = web.json_response({"status": "activated"})
            else:
                response = web.json_response({"error": "Failed to activate"}, status=400)
        except Exception as e:
            response = web.json_response({"error": str(e)}, status=400)

        return self._add_cors_headers(response)

    async def _api_list_macros(self, request: web.Request) -> web.Response:
        """GET /api/macros - List available macros."""
        mm = self.daemon.macro_manager
        macros = mm.list_macro_summaries()
        response = web.json_response({"macros": macros})
        return self._add_cors_headers(response)

    async def _api_get_macro(self, request: web.Request) -> web.Response:
        """GET /api/macros/{id} - Get macro details."""
        macro_id = request.match_info["id"]
        mm = self.daemon.macro_manager

        try:
            macro = mm.load_macro(macro_id)
            response = web.json_response(macro.to_dict())
        except FileNotFoundError:
            response = web.json_response({"error": "Macro not found"}, status=404)

        return self._add_cors_headers(response)

    def _update_macro_fields(self, macro, data: dict):
        """Update macro fields from request data."""
        from .gui.models.macro_types import MacroStep, PlaybackMode

        simple_fields = [
            "name",
            "description",
            "speed_multiplier",
            "repeat_count",
            "repeat_delay_ms",
            "fixed_delay_ms",
            "assigned_button",
            "global_hotkey",
        ]
        for field in simple_fields:
            if field in data:
                setattr(macro, field, data[field])

        if "steps" in data:
            macro.steps = [MacroStep.from_dict(s) for s in data["steps"]]
        if "playback_mode" in data:
            macro.playback_mode = PlaybackMode(data["playback_mode"])

    async def _api_create_macro(self, request: web.Request) -> web.Response:
        """POST /api/macros - Create new macro."""
        mm = self.daemon.macro_manager

        try:
            data = await request.json()
            macro = mm.create_macro(data.get("name", "New Macro"))
            self._update_macro_fields(macro, data)
            mm.save_macro(macro)
            response = web.json_response({"status": "created", "id": macro.id})
        except Exception as e:
            response = web.json_response({"error": str(e)}, status=400)

        return self._add_cors_headers(response)

    async def _api_update_macro(self, request: web.Request) -> web.Response:
        """PUT /api/macros/{id} - Update existing macro."""
        macro_id = request.match_info["id"]
        mm = self.daemon.macro_manager

        try:
            data = await request.json()
            macro = mm.load_macro(macro_id)
            self._update_macro_fields(macro, data)
            mm.save_macro(macro)
            response = web.json_response({"status": "updated"})
        except FileNotFoundError:
            response = web.json_response({"error": "Macro not found"}, status=404)
        except Exception as e:
            response = web.json_response({"error": str(e)}, status=400)

        return self._add_cors_headers(response)

    async def _api_delete_macro(self, request: web.Request) -> web.Response:
        """DELETE /api/macros/{id} - Delete macro."""
        macro_id = request.match_info["id"]
        mm = self.daemon.macro_manager

        try:
            mm.delete_macro(macro_id)
            response = web.json_response({"status": "deleted"})
        except FileNotFoundError:
            response = web.json_response({"error": "Macro not found"}, status=404)

        return self._add_cors_headers(response)
