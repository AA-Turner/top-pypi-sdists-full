"""aiohttp request handlers for the Maintenance service.

Plain aiohttp handlers (no Navigator/auth dependency) so the status and
changelog pages stay publicly reachable, mirroring the ``attach_routes`` style
already used by :mod:`flowtask.handlers.component`.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import orjson
from aiohttp import web

from .models import MaintenanceWindow
from .templates import render_status

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .service import MaintenanceService


def _json(data: Any, status: int = 200) -> web.Response:
    """Serialize ``data`` to a JSON response using orjson."""
    return web.Response(
        body=orjson.dumps(data),
        status=status,
        content_type="application/json",
    )


class MaintenanceHandlers:
    """Bundle of handlers bound to a :class:`MaintenanceService`."""

    def __init__(self, service: "MaintenanceService") -> None:
        self.service = service

    # -- status ------------------------------------------------------------
    async def status_html(self, request: web.Request) -> web.Response:
        """``GET /status`` — human-readable HTML status page."""
        report = await self.service.build_report(request.app)
        return web.Response(text=render_status(report), content_type="text/html")

    async def status_json(self, request: web.Request) -> web.Response:
        """``GET /api/v2/maintenance/status`` — machine-readable status.

        Returns HTTP 503 when the server is not fully operational so external
        monitors (load balancers, uptime checks) can act on it.
        """
        report = await self.service.build_report(request.app)
        payload = report.model_dump(mode="json")
        payload["overall"] = report.overall.value
        payload["uptime_seconds"] = report.uptime_seconds
        payload["healthy"] = report.healthy
        status = 200 if report.healthy else 503
        return _json(payload, status=status)

    async def failures_json(self, request: web.Request) -> web.Response:
        """``GET /api/v2/maintenance/failures`` — recent recorded failures."""
        try:
            limit = int(request.query.get("limit", "50"))
        except ValueError:
            limit = 50
        failures = await self.service.store.recent_failures(limit=limit)
        return _json(
            {
                "failures": [f.model_dump(mode="json") for f in failures],
                "count": len(failures),
                "degraded_store": self.service.store.degraded,
            }
        )

    # -- changelog ---------------------------------------------------------
    async def changelog_html(self, request: web.Request) -> web.Response:
        """``GET /changelog`` — the "What's New" HTML page."""
        html = await self.service.get_changelog_html()
        return web.Response(text=html, content_type="text/html")

    async def changelog_json(self, request: web.Request) -> web.Response:
        """``GET /api/v2/maintenance/changelog`` — changelog as JSON."""
        entries = await self.service.get_changelog_entries()
        return _json(
            {
                "entries": [e.model_dump(mode="json") for e in entries],
                "count": len(entries),
            }
        )

    # -- maintenance windows ----------------------------------------------
    async def windows_list(self, request: web.Request) -> web.Response:
        """``GET /api/v2/maintenance/windows`` — list windows.

        ``?upcoming=true`` filters to active/future windows only.
        """
        upcoming_only = request.query.get("upcoming", "").lower() in ("1", "true", "yes")
        manager = self.service.windows
        windows = await (manager.upcoming() if upcoming_only else manager.all_windows())
        return _json(
            {
                "windows": [w.model_dump(mode="json") for w in windows],
                "count": len(windows),
            }
        )

    async def windows_register(self, request: web.Request) -> web.Response:
        """``POST /api/v2/maintenance/windows`` — register a window.

        Body (JSON): ``title``, ``day`` (``YYYY-MM-DD``), ``start_time`` and
        ``end_time`` (``HH:MM``), optional ``description`` and ``notify``.
        """
        try:
            body = await request.json(loads=orjson.loads)
        except Exception:
            return _json({"error": "invalid JSON body"}, status=400)
        if not isinstance(body, dict):
            return _json({"error": "expected a JSON object"}, status=400)
        try:
            window = MaintenanceWindow(**body)
        except Exception as err:  # pydantic ValidationError or type errors
            return _json({"error": "invalid maintenance window", "detail": str(err)}, status=422)
        window = await self.service.windows.register(window)
        return _json(window.model_dump(mode="json"), status=201)

    async def windows_delete(self, request: web.Request) -> web.Response:
        """``DELETE /api/v2/maintenance/windows/{identifier}`` — remove a window."""
        identifier = request.match_info["identifier"]
        removed = await self.service.windows.remove(identifier)
        if not removed:
            return _json({"error": f"window '{identifier}' not found"}, status=404)
        return _json({"deleted": identifier})
