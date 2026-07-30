"""Step context manager for testmu.

Dual-protocol: `with testmu.step(...)` (sync, dormant) and
`async with testmu.step(...)` (async, used by generated code).
Sets a ContextVar the heal patch reads.

on_failure: None | 'fail-continue' | 'warn-continue'.
  - None: exception bubbles.
  - 'fail-continue': suppress + mark verdict failed.
  - 'warn-continue': suppress + log + reporter.warn_step (no verdict mutation).
"""
import contextvars
import logging

from testmu._heal_cache import set_cache, reset_cache, new_cache
from testmu import _test_state

_log = logging.getLogger("testmu")
_current_step = contextvars.ContextVar("testmu_step", default=None)
# Per-step auto-heal flag: reset at step start, set by the heal cascade, read into the step-end payload (auto_heal).
_step_autoheal = contextvars.ContextVar("testmu_step_autoheal", default=False)


def mark_autoheal():
    """Flag the current step as having auto-healed (called from the heal cascade)."""
    _step_autoheal.set(True)


def get_step_autoheal() -> bool:
    """Whether a heal occurred during the current step (read at step end)."""
    return _step_autoheal.get()


class _Step:
    __slots__ = (
        "description",
        "on_failure",
        "instruction_id",
        "_token",
        "_cache_token",
    )

    def __init__(self, description, on_failure=None, instruction_id=None):
        self.description = description
        self.on_failure = on_failure
        self.instruction_id = instruction_id
        self._token = None
        self._cache_token = None

    # ── Sync protocol (dormant) ──

    def __enter__(self):
        self._token = _current_step.set(self)
        self._cache_token = set_cache(new_cache())
        return self

    def __exit__(self, exc_type, exc_val, tb):
        if self._cache_token is not None:
            reset_cache(self._cache_token)
            self._cache_token = None
        if self._token is not None:
            _current_step.reset(self._token)
            self._token = None
        if exc_type is not None and self.on_failure == "fail-continue":
            return True
        return False

    # ── Async protocol ──

    async def __aenter__(self):
        self._token = _current_step.set(self)
        _step_autoheal.set(False)  # reset per step; the heal cascade sets it
        self._cache_token = set_cache(new_cache())
        from testmu._reporter import reporter
        await reporter().begin_step(self.description, instruction_id=self.instruction_id)
        return self

    async def __aexit__(self, exc_type, exc_val, tb):
        from testmu._reporter import reporter
        rep = reporter()

        ok = exc_type is None
        await rep.end_step(
            self.description,
            ok=ok,
            error=exc_val,
            instruction_id=self.instruction_id,
        )
        if self._cache_token is not None:
            reset_cache(self._cache_token)
            self._cache_token = None
        if self._token is not None:
            _current_step.reset(self._token)
            self._token = None
        if exc_type is None:
            return False
        if self.on_failure == "fail-continue":
            _test_state.mark_step_failed(self.description, exc_val)
            return True
        if self.on_failure == "warn-continue":
            _log.warning("[STEP WARN] %s — %s", self.description, exc_val)
            if hasattr(rep, "warn_step"):
                await rep.warn_step(self.description, exc_val)
            return True
        return False


def step(description, on_failure=None, id=None, instruction_id=None):
    return _Step(
        description,
        on_failure=on_failure,
        instruction_id=id if id is not None else instruction_id,
    )
