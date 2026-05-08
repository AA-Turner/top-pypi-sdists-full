"""Unit tests for HookService lifecycle contract (TASK-047).

Covers:
- __init__ does not mutate app.cleanup_ctx
- setup() wires trigger signals before freeze
- setup() registers _stop_hooks exactly once (idempotent)
- add_hook() post-freeze schedules start_runtime and does NOT touch signals
- _stop_hooks() only invokes runtime-added triggers' on_shutdown
- HookHandler._post_response no longer contains print('TG > ') or tg.start()
"""
import asyncio
import inspect
from unittest.mock import MagicMock, patch

import pytest
from aiohttp import web

from flowtask.hooks import HookService
from flowtask.hooks.service import HookHandler


# ---------------------------------------------------------------------------
# Helpers / stubs
# ---------------------------------------------------------------------------


def _make_minimal_hookservice(app: web.Application) -> HookService:
    """Build a HookService, stubbing out the storage check so tests do not
    require a real filesystem-backed task store."""
    mock_store = MagicMock()
    mock_store.path = MagicMock()  # truthy

    with patch("flowtask.hooks.service.TASK_STORAGES", {"default": mock_store}):
        svc = HookService(app=app)
    return svc


# ---------------------------------------------------------------------------
# __init__ contract
# ---------------------------------------------------------------------------


class TestHookServiceInit:
    def test_init_does_not_register_cleanup_ctx(self):
        """Construction alone must leave app.cleanup_ctx empty."""
        app = web.Application()
        _make_minimal_hookservice(app)
        assert len(app.cleanup_ctx) == 0

    def test_init_registers_app_key(self):
        app = web.Application()
        svc = _make_minimal_hookservice(app)
        assert app["HookService"] is svc

    def test_init_starts_with_empty_hooks(self):
        app = web.Application()
        svc = _make_minimal_hookservice(app)
        assert svc._hooks == []
        assert svc._runtime_hooks == []
        assert svc._started is False
        assert svc._teardown_registered is False


# ---------------------------------------------------------------------------
# setup() — wires triggers and registers _stop_hooks
# ---------------------------------------------------------------------------


class TestHookServiceSetup:
    def test_setup_loads_fs_hooks_and_wires_signals(
        self, fresh_app, stub_trigger_factory
    ):
        """After setup(), loaded triggers have on_startup in app.on_startup.

        Uses a dedicated event loop because setup() is a sync method that calls
        loop.run_until_complete() internally when the supplied loop is not
        already running.
        """
        svc = _make_minimal_hookservice(fresh_app)
        stub = stub_trigger_factory()

        # Patch both async loaders to do nothing (no filesystem/DB)
        async def _noop_fs(app):
            # Manually wire the stub trigger as if load_fs_hooks did it
            stub.setup(app)
            svc._hooks.append(stub)

        async def _noop_db(app):
            return

        svc.load_fs_hooks = _noop_fs
        svc.load_db_hooks = _noop_db

        loop = asyncio.new_event_loop()
        try:
            svc.setup(app=fresh_app, loop=loop)
        finally:
            loop.close()

        assert stub.on_startup in list(fresh_app.on_startup)
        assert stub.on_shutdown in list(fresh_app.on_shutdown)

    async def test_setup_with_running_loop_still_wires_signals(
        self, fresh_app, stub_trigger_factory
    ):
        """Navigator calls configure() while its app loop is already running."""
        svc = _make_minimal_hookservice(fresh_app)
        stub = stub_trigger_factory()

        async def _noop_fs(app):
            stub.setup(app)
            svc._hooks.append(stub)

        async def _noop_db(app):
            return

        svc.load_fs_hooks = _noop_fs
        svc.load_db_hooks = _noop_db

        svc.setup(app=fresh_app, loop=asyncio.get_running_loop())

        assert stub.on_startup in list(fresh_app.on_startup)
        assert stub.on_shutdown in list(fresh_app.on_shutdown)
        assert svc._started is True

    def test_setup_registers_stop_hooks_once(self, fresh_app):
        """_stop_hooks appears exactly once in app.on_shutdown even if setup() is called twice.

        Uses a dedicated event loop for the non-running-loop path.
        """
        svc = _make_minimal_hookservice(fresh_app)

        async def _noop(app):
            return

        svc.load_fs_hooks = _noop
        svc.load_db_hooks = _noop

        loop = asyncio.new_event_loop()
        try:
            svc.setup(app=fresh_app, loop=loop)
            svc.setup(app=fresh_app, loop=loop)  # idempotent call
        finally:
            loop.close()

        # Use == (not `is`) because bound method objects are created fresh on
        # each attribute access — `svc._stop_hooks is svc._stop_hooks` is False.
        stop_hooks_count = sum(
            1 for cb in fresh_app.on_shutdown if cb == svc._stop_hooks
        )
        assert stop_hooks_count == 1

    def test_setup_raises_when_app_missing(self):
        """setup() with no app and no self.app raises RuntimeError."""
        app = web.Application()
        svc = _make_minimal_hookservice(app)
        svc.app = None  # force missing

        loop = asyncio.new_event_loop()
        try:
            with pytest.raises(RuntimeError, match="requires an aiohttp Application"):
                svc.setup(app=None, loop=loop)
        finally:
            loop.close()


# ---------------------------------------------------------------------------
# add_hook() — runtime (post-freeze) path
# ---------------------------------------------------------------------------


class TestHookServiceAddHook:
    async def test_add_hook_post_freeze_uses_runtime_path(
        self, fresh_app, stub_trigger_factory, monkeypatch
    ):
        """Post-freeze add_hook must NOT append to signals; must schedule start_runtime."""
        svc = _make_minimal_hookservice(fresh_app)
        fresh_app.freeze()

        stub = stub_trigger_factory()
        scheduled_coros = []

        def fake_ensure_future(coro, **kwargs):
            scheduled_coros.append(coro)
            # Return a future-like object so asyncio does not complain
            fut = asyncio.get_event_loop().create_task(coro)
            return fut

        monkeypatch.setattr(asyncio, "ensure_future", fake_ensure_future)

        before_startup = list(fresh_app.on_startup)
        before_shutdown = list(fresh_app.on_shutdown)

        svc.add_hook(stub)

        assert stub in svc._hooks
        assert stub in svc._runtime_hooks
        # Signal lists must be untouched
        assert list(fresh_app.on_startup) == before_startup
        assert list(fresh_app.on_shutdown) == before_shutdown
        # start_runtime must have been scheduled
        assert len(scheduled_coros) == 1

    def test_add_hook_pre_freeze_wires_signals(self, fresh_app, stub_trigger_factory):
        """Pre-freeze add_hook wires signals via hook.setup(app); NOT in _runtime_hooks."""
        svc = _make_minimal_hookservice(fresh_app)
        stub = stub_trigger_factory()

        svc.add_hook(stub)

        assert stub in svc._hooks
        # Pre-freeze path: signals are wired, runtime list is not populated.
        assert stub not in svc._runtime_hooks
        assert stub.on_startup in list(fresh_app.on_startup)
        assert stub.on_shutdown in list(fresh_app.on_shutdown)


# ---------------------------------------------------------------------------
# _stop_hooks — housekeeping only
# ---------------------------------------------------------------------------


class TestHookServiceStopHooks:
    async def test_stop_hooks_only_invokes_runtime_hooks(
        self, fresh_app, stub_trigger_factory
    ):
        """Boot-time triggers (in _hooks but NOT in _runtime_hooks) must NOT
        have on_shutdown re-invoked by _stop_hooks."""
        svc = _make_minimal_hookservice(fresh_app)

        boot_trigger = stub_trigger_factory(name="boot")
        runtime_trigger = stub_trigger_factory(name="runtime")

        # Simulate boot-time trigger (registered via setup, not via add_hook)
        svc._hooks.append(boot_trigger)
        # Simulate runtime trigger (registered via add_hook)
        svc._hooks.append(runtime_trigger)
        svc._runtime_hooks.append(runtime_trigger)

        await svc._stop_hooks(fresh_app)

        assert (
            boot_trigger.shutdown_calls == 0
        ), "Boot-time trigger must NOT be re-invoked"
        assert runtime_trigger.shutdown_calls == 1, "Runtime trigger MUST be invoked"
        assert svc._hooks == []
        assert svc._runtime_hooks == []
        assert svc._started is False

    async def test_stop_hooks_clears_all_lists(self, fresh_app, stub_trigger_factory):
        svc = _make_minimal_hookservice(fresh_app)
        stub = stub_trigger_factory()
        svc._hooks.append(stub)
        svc._runtime_hooks.append(stub)
        svc._started = True

        await svc._stop_hooks(fresh_app)

        assert svc._hooks == []
        assert svc._runtime_hooks == []
        assert svc._started is False


# ---------------------------------------------------------------------------
# Source-code inspection: _post_response no longer has print / tg.start
# ---------------------------------------------------------------------------


class TestHookHandlerPostResponseClean:
    def test_post_response_no_print_debug(self):
        """The runtime API path must not contain the old print('TG > ', ...) debug line."""
        src = inspect.getsource(HookHandler._post_response)
        assert "print('TG > '" not in src
        assert 'print("TG > "' not in src

    def test_post_response_no_tg_start(self):
        """The runtime API path must not contain `await tg.start()`."""
        src = inspect.getsource(HookHandler._post_response)
        assert "await tg.start()" not in src
        assert ".start()" not in src

    def test_post_response_no_trigger_reinstantiation(self):
        """The `tg = trigger()` latent bug must be gone."""
        src = inspect.getsource(HookHandler._post_response)
        assert "tg = trigger()" not in src
