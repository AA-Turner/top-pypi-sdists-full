"""Dashboard themes API — server-side theme persistence.

The active dashboard theme is persisted in ``~/.cvc/dashboard.json`` so it
survives page refresh and is shared across the user's CVC instances on
the same host.

Endpoints
---------
* ``GET  /api/dashboard/theme``      — current theme info
* ``POST /api/dashboard/theme``      — set active theme (body: ``{"theme_id": "..."}``)
* ``GET  /api/dashboard/themes``     — list known theme ids
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

_DASHBOARD_FILE = Path.home() / ".cvc" / "dashboard.json"
_DEFAULT_THEME = "cvc-red"

# Known theme catalog (must stay in sync with frontend src/themes/themes.ts).
# Keeping a server-side list lets the dashboard validate POST requests and
# gives a single source for "what themes exist" without bundling the full
# theme definitions on the backend.
_KNOWN_THEMES: List[str] = [
    "cvc-red",
    "cvc-dark",
    "cvc-light",
    "cvc-blue",
    "cvc-green",
    "cvc-purple",
    "cvc-amber",
    "cvc-rose",
    "cvc-slate",
    "cvc-mono",
]


class ThemeUpdate(BaseModel):
    theme_id: str


def _read_dashboard() -> Dict[str, Any]:
    if not _DASHBOARD_FILE.exists():
        return {}
    try:
        return json.loads(_DASHBOARD_FILE.read_text(encoding="utf-8") or "{}") or {}
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed reading %s: %s", _DASHBOARD_FILE, exc)
        return {}


def _write_dashboard(data: Dict[str, Any]) -> None:
    _DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    _DASHBOARD_FILE.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )


def get_active_theme() -> str:
    data = _read_dashboard()
    val = data.get("active_theme")
    return str(val) if val else _DEFAULT_THEME


def set_active_theme(theme_id: str) -> None:
    data = _read_dashboard()
    data["active_theme"] = theme_id
    _write_dashboard(data)


def register_themes_routes(app: FastAPI) -> None:
    """Mount /api/dashboard/theme* routes."""

    @app.get("/api/dashboard/theme")
    async def get_theme() -> Dict[str, Any]:
        return {
            "active_theme": get_active_theme(),
            "default_theme": _DEFAULT_THEME,
        }

    @app.post("/api/dashboard/theme")
    async def post_theme(body: ThemeUpdate) -> Dict[str, Any]:
        tid = (body.theme_id or "").strip()
        if not tid:
            raise HTTPException(400, "Missing theme_id")
        if tid not in _KNOWN_THEMES:
            # Allow unknown ids but log — themes can be added on the
            # frontend ahead of the backend catalog.
            logger.info("Setting unknown theme id: %s", tid)
        set_active_theme(tid)
        return {"active_theme": tid}

    @app.get("/api/dashboard/themes")
    async def list_themes() -> Dict[str, Any]:
        return {"themes": _KNOWN_THEMES, "count": len(_KNOWN_THEMES)}
