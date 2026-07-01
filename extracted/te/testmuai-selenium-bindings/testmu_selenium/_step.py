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


@contextmanager
def step(description: str, timeout_ms: int | None = None, on_failure: str = "fail"):
    """Context manager wrapping a logical test step.

    on_failure="continue" suppresses exceptions (logged + step marked failed).
    timeout_ms is recorded but enforced best-effort by the implementer (Phase A: not enforced).
    """
    global _step_counter
    _step_counter += 1
    n = _step_counter
    logger.info("  [STEP %d] %s", n, description)
    info = StepInfo(description=description, timeout_ms=timeout_ms, on_failure=on_failure)
    token = _current_step.set(info)
    status = "passed"
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
        _current_step.reset(token)
