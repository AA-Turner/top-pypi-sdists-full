"""Settings dependency for FastAPI injection.

Extracts the ``Settings`` instance from ``request.app.state.settings``
so that settings propagate through the dependency graph without
module-level singleton imports.

Usage::

    @router.get("/example")
    async def example(settings: Settings):
        return {"app": settings.app_name}
"""

from typing import Annotated

from fastapi import Depends
from fastapi.requests import HTTPConnection


def _settings_factory(request: HTTPConnection):
    """Extract application settings from ``request.app.state.settings``."""
    return request.app.state.settings


Settings = Annotated["Settings", Depends(_settings_factory)]

__all__ = ("Settings",)
