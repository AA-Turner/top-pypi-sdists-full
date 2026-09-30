"""Step context manager — wraps a logical test step with reporting + heal context."""
import logging
from contextvars import ContextVar
from contextlib import contextmanager
from dataclasses import dataclass

from testmu_selenium._step_variables import pop_step_variables, reset_step_variables

logger = logging.getLogger(__name__)


@dataclass
class StepInfo:
    description: str
    timeout_ms: int | None = None
    on_failure: str = "fail"  # "fail" | "continue"
    auto_heal: bool = False
    instruction_id: str | None = None  # per-step instruction id for the instance-view timeline


# ContextVar accessible inside step body — for downstream introspection (heal logs etc.)
_current_step: ContextVar[StepInfo | None] = ContextVar("_current_step", default=None)

# Module-level step counter — reset by _session.run() at session start, incremented
# on each step() entry. Logged in `[STEP N] description` form mirroring Playwright's
# LTReporter so HE worker logs read the same across drivers.
_step_counter: int = 0


def _reset_step_counter() -> None:
    """Internal — called by _session.run() so each test starts from STEP 1."""
    global _step_counter
    _step_counter = 0
    # A step-variable buffer left over from a previous run would be attributed
    # to this run's first step.
    reset_step_variables()


def get_step_count() -> int:
    """Return the number of steps completed in the current test."""
    return _step_counter


def _emit_step_hook(verb: str, payload: dict) -> None:
    """Ship a per-step wire hook so the LT hub forwards it to the grid for the instance view.

    No-op off the ``cloud`` run target or before a driver exists; never raises.
    """
    from testmu_selenium import _config
    if _config.run_target != "cloud":
        return
    try:
        import json
        from testmu_selenium._helpers.driver import get_driver
        get_driver().execute_script(f"{verb}=" + json.dumps(payload))
    except Exception as e:  # noqa: BLE001 — never propagate reporter errors
        logger.debug("[testmu] step hook %s skipped: %s", verb, e)


# The step end hook must carry WHY a failed step failed, so HPS can map
# a step to its commands and show the per-step failure disposition. The wire
# vocabulary is the runtime's FailureCondition enum, which each binding names
# differently — map explicitly rather than sending the binding's own token.
_WIRE_FAILURE_CONDITION = {
    "fail": "FAIL_TEST_IMMEDIATELY",
    "continue": "FAIL_BUT_CONTINUE_EXECUTING",
    # Accepted for forward-compatibility with the other bindings' vocabularies;
    # selenium-python's step() only exposes fail/continue today.
    "fail-continue": "FAIL_BUT_CONTINUE_EXECUTING",
    "warn-continue": "WARN_BUT_CONTINUE_EXECUTING",
}


def _wire_failure_condition(on_failure: str) -> str:
    """Map the binding's on_failure token to the runtime's FailureCondition name."""
    return _WIRE_FAILURE_CONDITION.get((on_failure or "").strip().lower(), "")


@contextmanager
def step(description: str, timeout_ms: int | None = None, on_failure: str = "fail",
         instruction_id: str | None = None):
    """Context manager wrapping a logical test step.

    on_failure="continue" suppresses exceptions (logged + step marked failed).
    timeout_ms is recorded but enforced best-effort by the implementer (Phase A: not enforced).
    instruction_id is the per-step id mapping each step back to its instruction in the instance view.
    """
    global _step_counter
    _step_counter += 1
    n = _step_counter
    logger.info("  [STEP %d] %s", n, description)
    info = StepInfo(description=description, timeout_ms=timeout_ms, on_failure=on_failure,
                    instruction_id=instruction_id)
    token = _current_step.set(info)
    status = "passed"
    # Start hook — records the step and takes the pre-step screenshot before its commands run.
    _emit_step_hook(
        "lambda-testCase-start",
        {"name": description, **({"instructionId": instruction_id} if instruction_id else {})},
    )
    try:
        yield info
    except Exception as e:
        status = "failed"
        if on_failure == "continue":
            logger.warning("step %r failed (on_failure=continue): %s", description, e)
            return
        raise
    finally:
        # %r on description so the end-line is unambiguous when the name has spaces
        logger.info(
            "  [STEP %d] end name=%r status=%s auto_heal=%s",
            n, description, status, info.auto_heal,
        )
        # End hook — closes the step with its verdict. name MUST match the start hook.
        # auto_heal: set by the action engine when this step fell to the heal cascade.
        #
        # Report the values this step ran with, not just the names. The
        # buffer is DRAINED unconditionally (even off the cloud run target, where
        # the hook itself is a no-op) so a local run cannot leak one step's reads
        # into the next step's payload.
        step_variables = pop_step_variables()
        payload = {"name": description, "status": status, "auto_heal": info.auto_heal}
        if step_variables:
            payload["variables"] = step_variables
            logger.info("  [STEP %d] variables=%s", n, sorted(step_variables))
        # Only on a failure — the disposition is meaningless for a
        # passing step, and the source omits it there too.
        if status == "failed":
            wire_condition = _wire_failure_condition(on_failure)
            if wire_condition:
                payload["failure_condition"] = wire_condition
        _emit_step_hook("lambda-testCase-end", payload)
        _current_step.reset(token)
