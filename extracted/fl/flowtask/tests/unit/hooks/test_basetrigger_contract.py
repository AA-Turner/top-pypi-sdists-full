"""Unit tests for BaseTrigger.setup and BaseTrigger.start_runtime contracts.

Covers TASK-046 acceptance criteria:
- setup() appends callbacks to app signals (pre-freeze)
- setup() propagates RuntimeError when signals are frozen
- setup() is a no-op for triggers with no lifecycle methods
- setup() assigns self.app
- start_runtime() invokes on_startup exactly once
- start_runtime() does NOT mutate app.on_startup / app.on_shutdown
- start_runtime() is a no-op (apart from self.app = app) when on_startup is None
"""
import pytest
from flowtask.hooks.types.base import BaseTrigger


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _NoCallbackTrigger(BaseTrigger):
    """Trigger that does NOT override on_startup / on_shutdown (inherits None)."""

    def __init__(self, *args, **kwargs):
        actions = kwargs.pop("actions", [])
        super().__init__(*args, actions=actions, **kwargs)


# Use the shared _StubTrigger from conftest (imported via pytest fixture)


# ---------------------------------------------------------------------------
# setup() — pre-freeze
# ---------------------------------------------------------------------------


class TestBaseTriggerSetupPreFreeze:
    def test_setup_appends_callbacks_when_unfrozen(
        self, fresh_app, stub_trigger_factory
    ):
        trigger = stub_trigger_factory()
        trigger.setup(fresh_app)
        assert trigger.on_startup in list(fresh_app.on_startup)
        assert trigger.on_shutdown in list(fresh_app.on_shutdown)

    def test_setup_sets_self_app(self, fresh_app, stub_trigger_factory):
        trigger = stub_trigger_factory()
        trigger.setup(fresh_app)
        assert trigger.app is fresh_app

    def test_setup_skips_none_callbacks(self, fresh_app):
        """A trigger with no on_startup/on_shutdown overrides → no signals appended.

        Newer versions of aiohttp pre-populate app.on_startup with internal
        callbacks (e.g. CleanupContext._on_startup), so we record baseline
        lengths before calling setup() and assert no new items were added.
        """
        trigger = _NoCallbackTrigger(name="no-cb")
        # BaseTrigger class attributes are None — not callable
        assert not callable(trigger.on_startup)
        assert not callable(trigger.on_shutdown)

        startup_before = len(list(fresh_app.on_startup))
        shutdown_before = len(list(fresh_app.on_shutdown))

        trigger.setup(fresh_app)  # must not raise

        assert trigger.app is fresh_app
        # Signal lists must not have grown — trigger added nothing.
        assert len(list(fresh_app.on_startup)) == startup_before
        assert len(list(fresh_app.on_shutdown)) == shutdown_before


# ---------------------------------------------------------------------------
# setup() — post-freeze (RuntimeError propagation)
# ---------------------------------------------------------------------------


class TestBaseTriggerSetupFrozen:
    def test_setup_raises_runtimeerror_when_signals_frozen(
        self, fresh_app, stub_trigger_factory
    ):
        fresh_app.freeze()
        trigger = stub_trigger_factory()
        with pytest.raises(RuntimeError):
            trigger.setup(fresh_app)

    def test_setup_no_silent_swallow(self, fresh_app, stub_trigger_factory):
        """Ensure the broad try/except is gone — no return value from a frozen call."""
        fresh_app.freeze()
        trigger = stub_trigger_factory()
        raised = False
        try:
            trigger.setup(fresh_app)
            # If we reach here it means no exception — that's a failure
        except RuntimeError:
            raised = True
        assert raised, "setup() must raise RuntimeError on a frozen app, not swallow it"


# ---------------------------------------------------------------------------
# start_runtime() — post-freeze path
# ---------------------------------------------------------------------------


class TestBaseTriggerStartRuntime:
    async def test_start_runtime_invokes_on_startup_once(
        self, fresh_app, stub_trigger_factory
    ):
        trigger = stub_trigger_factory()
        await trigger.start_runtime(fresh_app)
        assert trigger.startup_calls == 1

    async def test_start_runtime_does_not_mutate_signals(
        self, fresh_app, stub_trigger_factory
    ):
        """start_runtime must NOT append to app.on_startup / app.on_shutdown."""
        before_startup = list(fresh_app.on_startup)
        before_shutdown = list(fresh_app.on_shutdown)
        trigger = stub_trigger_factory()
        await trigger.start_runtime(fresh_app)
        assert list(fresh_app.on_startup) == before_startup
        assert list(fresh_app.on_shutdown) == before_shutdown

    async def test_start_runtime_sets_self_app(
        self, fresh_app, stub_trigger_factory
    ):
        trigger = stub_trigger_factory()
        await trigger.start_runtime(fresh_app)
        assert trigger.app is fresh_app

    async def test_start_runtime_skips_when_on_startup_none(self, fresh_app):
        """start_runtime with no on_startup override does not raise; sets self.app."""
        trigger = _NoCallbackTrigger(name="no-cb-rt")
        await trigger.start_runtime(fresh_app)
        assert trigger.app is fresh_app

    async def test_start_runtime_propagates_on_startup_exception(self, fresh_app):
        """If on_startup raises, start_runtime propagates the exception."""

        class _FailingTrigger(BaseTrigger):
            def __init__(self):
                super().__init__(actions=[])

            async def on_startup(self, app):  # type: ignore[override]
                raise ValueError("startup boom")

        trigger = _FailingTrigger()
        with pytest.raises(ValueError, match="startup boom"):
            await trigger.start_runtime(fresh_app)
