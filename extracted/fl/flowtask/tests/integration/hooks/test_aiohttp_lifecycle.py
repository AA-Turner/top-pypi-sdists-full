"""End-to-end integration tests for the HookService aiohttp lifecycle (TASK-050).

Tests boot a real aiohttp Application with a HookService and a stub trigger,
verifying that:
- on_startup fires through aiohttp's signal dispatcher (not any internal workaround)
- on_shutdown fires through aiohttp's signal dispatcher
- Triggers added via add_hook (post-freeze) receive a start_runtime call
- No "Cannot modify frozen list" appears in logs during normal pre-freeze setup
- DB-backed triggers are instantiated and their signals wired during setup()
"""
import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock, patch

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from flowtask.hooks import HookService
from flowtask.hooks.types.base import BaseTrigger


# ---------------------------------------------------------------------------
# _StubTrigger for integration tests
# (mirrors conftest.py in unit/hooks but is self-contained here)
# ---------------------------------------------------------------------------


class _StubTrigger(BaseTrigger):
    """Records lifecycle calls without touching real I/O."""

    def __init__(self, *args, **kwargs):
        actions = kwargs.pop("actions", [])
        super().__init__(*args, actions=actions, **kwargs)
        self.startup_calls: int = 0
        self.shutdown_calls: int = 0

    async def on_startup(self, app):  # type: ignore[override]
        self.startup_calls += 1

    async def on_shutdown(self, app):  # type: ignore[override]
        self.shutdown_calls += 1


def _make_hookservice(app: web.Application) -> HookService:
    """Build a HookService, stubbing the storage check."""
    mock_store = MagicMock()
    mock_store.path = MagicMock()

    with patch("flowtask.hooks.service.TASK_STORAGES", {"default": mock_store}):
        svc = HookService(app=app)
    return svc


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


async def test_aiohttp_lifecycle_runs_trigger_callbacks():
    """Boot a real aiohttp app with a trigger wired via setup().

    Assert that on_startup fires when the server starts and on_shutdown fires
    when the server closes — both through aiohttp's signal dispatcher.
    """
    app = web.Application()
    svc = _make_hookservice(app)
    trigger = _StubTrigger(name="lifecycle-test")

    # Bypass FS/DB loaders; wire the stub directly as if load_fs_hooks did it.
    async def _noop(a):
        return

    svc.load_fs_hooks = _noop
    svc.load_db_hooks = _noop

    # Pre-freeze: register the trigger's callbacks on app signals.
    trigger.setup(app)
    svc._hooks.append(trigger)

    # Register the teardown hook on app.on_shutdown.
    app.on_shutdown.append(svc._stop_hooks)

    async with TestClient(TestServer(app)):
        # Server is running; aiohttp fired app.on_startup.
        assert (
            trigger.startup_calls == 1
        ), "on_startup must fire exactly once through aiohttp signals"

    # Server is stopped; aiohttp fired app.on_shutdown.
    assert (
        trigger.shutdown_calls == 1
    ), "on_shutdown must fire exactly once through aiohttp signals"


async def test_no_frozen_list_warnings_in_log():
    """Full pre-freeze setup must not emit any 'Cannot modify frozen list' log line."""
    app = web.Application()
    _make_hookservice(app)
    trigger = _StubTrigger(name="no-frozen-test")

    # Pre-freeze: this must succeed silently.
    trigger.setup(app)

    # Capture any log output during setup
    log_records: list[logging.LogRecord] = []

    class _Capture(logging.Handler):
        def emit(self, record):
            log_records.append(record)

    handler = _Capture()
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    try:
        async with TestClient(TestServer(app)):
            pass
    finally:
        root_logger.removeHandler(handler)

    frozen_warnings = [
        r for r in log_records if "Cannot modify frozen list" in r.getMessage()
    ]
    assert (
        frozen_warnings == []
    ), f"Unexpected 'Cannot modify frozen list' log entries: {frozen_warnings}"


async def test_runtime_trigger_starts_immediately():
    """Trigger added via add_hook (post-freeze) starts via start_runtime.

    After add_hook, start_runtime is scheduled with ensure_future. We give
    the event loop a chance to run the coroutine by awaiting a short sleep.

    NOTE: HTTP layer omitted — this test calls svc.add_hook() directly instead
    of issuing a POST /api/v1/triggers/. That path requires a live DB and a
    running auth stack; HookHandler._post_response is separately tested in
    the unit tests (tests/unit/hooks/test_hookservice_lifecycle.py).

    NOTE: setup() coverage lives in the unit tests. This integration test wires
    the service directly so it can focus on post-freeze runtime registration.
    """
    app = web.Application()
    svc = _make_hookservice(app)

    async def _noop(a):
        return

    svc.load_fs_hooks = _noop
    svc.load_db_hooks = _noop

    # Wire teardown and run loaders directly (equivalent to what setup() does).
    await svc.start_hooks(app)
    app.on_shutdown.append(svc._stop_hooks)
    svc._teardown_registered = True

    # Server is now running (on_startup signals are frozen).
    # Add a new trigger at runtime.
    runtime_trigger = _StubTrigger(name="runtime-post-freeze")

    async with TestClient(TestServer(app)):
        # After server starts, add the trigger at runtime.
        svc.add_hook(runtime_trigger)
        # Let the event loop process the scheduled ensure_future coroutine.
        await asyncio.sleep(0.05)
        assert (
            runtime_trigger.startup_calls == 1
        ), "start_runtime must invoke on_startup for runtime-added triggers"


async def test_setup_inside_running_loop_registers_aiohttp_lifecycle():
    """setup() must work when configure() runs inside Navigator's active loop."""
    app = web.Application()
    svc = _make_hookservice(app)
    trigger = _StubTrigger(name="running-loop-setup")

    async def _load_fs_hooks(a):
        trigger.setup(a)
        svc._hooks.append(trigger)

    async def _load_db_hooks(a):
        return

    svc.load_fs_hooks = _load_fs_hooks
    svc.load_db_hooks = _load_db_hooks

    svc.setup(app=app, loop=asyncio.get_running_loop())

    async with TestClient(TestServer(app)):
        assert (
            trigger.startup_calls == 1
        ), "setup() must wire on_startup before aiohttp freezes signals"

    assert (
        trigger.shutdown_calls == 1
    ), "setup() must wire on_shutdown before aiohttp freezes signals"


async def test_db_hooks_loaded_during_setup():
    """DB-backed triggers are instantiated and their signals wired during setup().

    Mocks HookObject.all() so the test does not require a live Postgres
    instance. Asserts that each returned HookObject produces a trigger with
    its on_startup callback registered on app.on_startup.

    NOTE: start_hooks() is awaited directly so this test can isolate DB-backed
    hook loading without also exercising setup()'s sync bridge.
    """
    from flowtask.hooks.models import HookObject

    app = web.Application()
    svc = _make_hookservice(app)

    # A stub trigger that records calls, identical to _StubTrigger.
    db_trigger = _StubTrigger(name="db-backed-trigger")

    # Fake HookObject returned from the database query.
    mock_hook_obj = MagicMock(spec=HookObject)
    mock_hook_obj.definition = {"When": {}, "Then": {}}

    # Fake Hook that yields our db_trigger.
    mock_hook = MagicMock()
    mock_hook.triggers = [db_trigger]

    async def _noop_fs(a):
        return

    svc.load_fs_hooks = _noop_fs

    with patch(
        "flowtask.hooks.service.HookObject.all",
        new=AsyncMock(return_value=[mock_hook_obj]),
    ), patch(
        "flowtask.hooks.service.Hook",
        return_value=mock_hook,
    ), patch(
        "flowtask.hooks.service.AsyncDB",
    ) as mock_asyncdb:
        # Make AsyncDB context manager work without a real DB connection.
        mock_conn = AsyncMock()
        mock_asyncdb.return_value.connection = AsyncMock(return_value=mock_conn)
        mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_conn.__aexit__ = AsyncMock(return_value=False)

        await svc.start_hooks(app)

    # The db_trigger's on_startup must have been appended to app.on_startup.
    assert (
        db_trigger in svc._hooks
    ), "DB-backed trigger must be tracked in svc._hooks after setup()"
    assert db_trigger.on_startup in list(
        app.on_startup
    ), "DB-backed trigger's on_startup must be wired into app.on_startup"
