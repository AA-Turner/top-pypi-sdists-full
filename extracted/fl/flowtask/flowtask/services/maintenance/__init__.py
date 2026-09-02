"""Flowtask Maintenance service (SOC2 CC8 change-management surfaces).

Exposes a status page, an end-user changelog ("What's New") page and a
maintenance-window registration API for Flowtask running in aiohttp server
mode.

The heavy orchestrator (:class:`MaintenanceService`) is imported lazily so that
importing lightweight pieces (models, store, changelog parsing) does not drag in
the full Flowtask configuration/notify stack.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .models import (
    ChangelogEntry,
    FailureRecord,
    HealthCheck,
    MaintenanceWindow,
    ServiceState,
    StatusReport,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .service import MaintenanceService

__all__ = [
    "MaintenanceService",
    "MAINTENANCE_APP_KEY",
    "StatusReport",
    "HealthCheck",
    "ServiceState",
    "MaintenanceWindow",
    "FailureRecord",
    "ChangelogEntry",
]


def __getattr__(name: str):
    """Lazily resolve the orchestrator symbols to avoid heavy imports."""
    if name in ("MaintenanceService", "MAINTENANCE_APP_KEY"):
        from . import service

        return getattr(service, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
