"""Dashboard API routes — added to the existing MJPEG server's aiohttp app."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from aiohttp import WSMsgType, web

from ghost_pc.web import get_web_root

if TYPE_CHECKING:
    from ghost_pc.agent.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


def register_dashboard_routes(app: web.Application, orchestrator: Orchestrator) -> None:
    """Add dashboard routes to an existing aiohttp application.

    Called from ``MJPEGServer.run()`` when an orchestrator is provided.
    """
    handler = _DashboardHandler(orchestrator)

    app.router.add_get("/dashboard", handler.handle_page)
    app.router.add_get("/api/status", handler.handle_status)
    app.router.add_get("/api/logs", handler.handle_logs)
    app.router.add_get("/api/cost", handler.handle_cost)
    app.router.add_post("/api/control/pause", handler.handle_pause)
    app.router.add_post("/api/control/resume", handler.handle_resume)
    app.router.add_post("/api/control/stop", handler.handle_stop)
    app.router.add_get("/ws/dashboard", handler.handle_ws)

    # Static files for dashboard (CSS/JS/images)
    app.router.add_get("/static/{path:.*}", handler.handle_static)


class _DashboardHandler:
    """Encapsulates all dashboard route handlers."""

    def __init__(self, orchestrator: Orchestrator) -> None:
        self._orch = orchestrator

    async def handle_page(self, request: web.Request) -> web.Response:
        """Serve the dashboard HTML."""
        template = get_web_root() / "templates" / "dashboard.html"
        html = template.read_text(encoding="utf-8")
        return web.Response(text=html, content_type="text/html")

    async def handle_static(self, request: web.Request) -> web.FileResponse:
        """Serve static files."""
        rel_path = request.match_info["path"]
        file_path = get_web_root() / "static" / rel_path
        if not file_path.is_file():
            raise web.HTTPNotFound()
        return web.FileResponse(file_path)

    async def handle_status(self, request: web.Request) -> web.Response:
        """Return agent status JSON."""
        status = self._orch.get_status()
        return web.json_response(status)

    async def handle_logs(self, request: web.Request) -> web.Response:
        """Return recent log entries."""
        count = int(request.query.get("count", "50"))
        handler = self._orch.dashboard_log_handler
        if handler is None:
            return web.json_response({"logs": []})
        logs = handler.get_recent(count)
        return web.json_response({"logs": logs})

    async def handle_cost(self, request: web.Request) -> web.Response:
        """Return token usage and cost estimate."""
        summary = self._orch.get_cost_summary()
        return web.json_response(summary)

    async def handle_pause(self, request: web.Request) -> web.Response:
        """Pause the agent."""
        self._orch.pause()
        return web.json_response({"ok": True, "paused": True})

    async def handle_resume(self, request: web.Request) -> web.Response:
        """Resume the agent."""
        self._orch.resume()
        return web.json_response({"ok": True, "paused": False})

    async def handle_stop(self, request: web.Request) -> web.Response:
        """Graceful shutdown."""
        asyncio.ensure_future(self._orch.shutdown())
        return web.json_response({"ok": True})

    async def handle_ws(self, request: web.Request) -> web.WebSocketResponse:
        """WebSocket for real-time status + log push."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        handler = self._orch.dashboard_log_handler
        log_queue = handler.subscribe() if handler else None

        try:
            # Push status + logs every 2 seconds, interleaved with log queue
            while not ws.closed:
                # Send status update
                status = self._orch.get_status()
                await ws.send_json({"type": "status", "data": status})

                # Drain log queue
                if log_queue:
                    logs: list[dict[str, Any]] = []
                    while not log_queue.empty():
                        try:
                            logs.append(log_queue.get_nowait())
                        except asyncio.QueueEmpty:
                            break
                    if logs:
                        await ws.send_json({"type": "logs", "data": logs})

                # Wait 2 seconds or until a WS message arrives
                try:
                    msg = await asyncio.wait_for(ws.receive(), timeout=2.0)
                    if msg.type in (WSMsgType.ERROR, WSMsgType.CLOSE, WSMsgType.CLOSED):
                        break
                except TimeoutError:
                    pass
        except (ConnectionResetError, RuntimeError):
            pass
        finally:
            if handler and log_queue:
                handler.unsubscribe(log_queue)

        return ws
