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

_current_instruction_id = contextvars.ContextVar("testmu_instruction_id", default="")


def set_instruction_id(value):
    return _current_instruction_id.set(value or "")


def get_instruction_id():
    step = _current_step.get()
    return getattr(step, "instruction_id", "") or _current_instruction_id.get()
# Per-step auto-heal flag: reset at step start, set by the heal cascade, read into the step-end payload (auto_heal).
_step_autoheal = contextvars.ContextVar("testmu_step_autoheal", default=False)


def mark_autoheal():
    """Flag the current step as having auto-healed (called from the heal cascade)."""
    _step_autoheal.set(True)


def get_step_autoheal() -> bool:
    """Whether a heal occurred during the current step (read at step end)."""
    return _step_autoheal.get()


# The step end hook must carry WHY a failed step failed, so HPS can map
# a step to its commands and show the per-step failure disposition. The wire
# vocabulary is the runtime's FailureCondition enum, which each binding names
# differently — map explicitly rather than sending the binding's own token.
#
# A step with no on_failure fails the test immediately, so None maps to
# FAIL_TEST_IMMEDIATELY rather than being omitted.
_WIRE_FAILURE_CONDITION = {
    None: "FAIL_TEST_IMMEDIATELY",
    "": "FAIL_TEST_IMMEDIATELY",
    "fail": "FAIL_TEST_IMMEDIATELY",
    "fail-continue": "FAIL_BUT_CONTINUE_EXECUTING",
    "warn-continue": "WARN_BUT_CONTINUE_EXECUTING",
}


def wire_failure_condition(on_failure) -> str:
    """Map the binding's on_failure token to the runtime's FailureCondition name."""
    if on_failure is None:
        return _WIRE_FAILURE_CONDITION[None]
    return _WIRE_FAILURE_CONDITION.get(str(on_failure).strip().lower(), "")

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
            on_failure=self.on_failure,
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
