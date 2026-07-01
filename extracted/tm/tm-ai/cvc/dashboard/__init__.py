"""
cvc.dashboard — Web dashboard for the CVC Gateway.

Provides:
  - ``mount_dashboard(app)`` — attach dashboard routes + static files to a FastAPI app
  - Dashboard API router (imported from routes.py)
"""

from __future__ import annotations

from pathlib import Path

STATIC_DIR = Path(__file__).parent / "static"


def mount_dashboard(app) -> None:
    """Mount dashboard static files and routes onto a FastAPI app."""
    from fastapi.staticfiles import StaticFiles

    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="dashboard-static")
