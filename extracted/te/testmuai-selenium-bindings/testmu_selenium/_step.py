"""Step context manager — wraps a logical test step with reporting + heal context."""
import logging
from contextvars import ContextVar
from contextlib import contextmanager
from dataclasses import dataclass

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
        _emit_step_hook(
            "lambda-testCase-end",
            {"name": description, "status": status, "auto_heal": info.auto_heal},
        )
        _current_step.reset(token)
