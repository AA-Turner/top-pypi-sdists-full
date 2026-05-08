"""Shared fixtures for HookService lifecycle unit tests (TASK-050).

Provides a _StubTrigger that records on_startup/on_shutdown calls without
touching real I/O, and standard fixtures for fresh aiohttp Applications.
"""
import pytest
from aiohttp import web
from flowtask.hooks.types.base import BaseTrigger


class _StubTrigger(BaseTrigger):
    """Records lifecycle calls without touching real I/O."""

    def __init__(self, *args, **kwargs):
        actions = kwargs.pop("actions", [])
        super().__init__(*args, actions=actions, **kwargs)
        self.startup_calls: int = 0
        self.shutdown_calls: int = 0

    async def on_startup(self, app):  # type: ignore[override]
        """Record startup invocation."""
        self.startup_calls += 1

    async def on_shutdown(self, app):  # type: ignore[override]
        """Record shutdown invocation."""
        self.shutdown_calls += 1


@pytest.fixture
def fresh_app() -> web.Application:
    """An aiohttp Application with mutable signal lists."""
    return web.Application()


@pytest.fixture
def stub_trigger_factory():
    """Factory callable that returns a _StubTrigger instance with counters."""
    return lambda **kw: _StubTrigger(name=kw.pop("name", "stub"), **kw)
