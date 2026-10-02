"""Step context manager — reporting, on_failure routing, per-step heal state.

Sync throughout. Lifecycle:

    enter  → step counter++ → set the step ContextVar → install a fresh per-step
             heal cache → reporter.begin_step
    exit   → reporter.end_step(ok=exc is None, is_autohealed=<from step state>, ...)
             BEFORE the contextvars are reset, so a reporter reading step state during
             end_step still sees it
    then   → route on_failure

on_failure vocabulary is playwright's: None → re-raise; "fail-continue" →
suppress and mark the pending verdict failure; "warn-continue" → suppress and warn.
Anything else fails closed — an unrecognised value must never silently swallow.
"""
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Optional

from testmu_appium._reporter import reporter
from testmu_appium._test_state import mark_step_failed

_log = logging.getLogger("testmu_appium")

FAIL_CONTINUE = "fail-continue"
WARN_CONTINUE = "warn-continue"
_KNOWN_ON_FAILURE = frozenset({FAIL_CONTINUE, WARN_CONTINUE})


@dataclass
class StepInfo:
    description: str
    instruction_id: Optional[str] = None
    on_failure: Optional[str] = None
    is_autohealed: bool = False
    autoheal_source: str = ""
    interacted_element: Optional[dict] = None
    heal_cache: dict = field(default_factory=dict)


_current_step: ContextVar[Optional[StepInfo]] = ContextVar("_current_step", default=None)

_current_instruction_id: ContextVar[str] = ContextVar("_current_instruction_id", default="")


def set_instruction_id(value: Optional[str]):
    return _current_instruction_id.set(value or "")


def get_instruction_id() -> str:
    step = _current_step.get(None)
    return getattr(step, "instruction_id", "") or _current_instruction_id.get()

# Module-level step counter — reset by run() at session start.
_step_counter: int = 0


def _reset_step_counter() -> None:
    global _step_counter
    _step_counter = 0


def get_step_count() -> int:
    """The number of steps entered in the current test."""
    return _step_counter


def current_step() -> Optional[StepInfo]:
    """The active StepInfo, or None outside a step."""
    return _current_step.get(None)


def get_heal_cache() -> Optional[dict]:
    """The active step's heal remap cache, or None outside a step.

    Heal only ever runs inside a step, so `None` here is also the signal that a heal
    attempt has no business starting.
    """
    info = current_step()
    return info.heal_cache if info is not None else None


def mark_autohealed(source: str = "") -> None:
    """Record that this step's target was relocated by autoheal.

    Read by end_step as `is_autohealed` / `autoheal_source` — the mobile telemetry
    contract that replay-diff consumes. No-op outside a step.
    """
    info = current_step()
    if info is None:
        return
    info.is_autohealed = True
    if source:
        info.autoheal_source = source


def record_interacted_element(payload: dict) -> None:
    """Record the interacted-element payload (original locator, bounds, center).

    Follows the legacy runtime's contract: the payload rides on the step-end hook.
    No-op outside a step.
    """
    info = current_step()
    if info is None:
        return
    info.interacted_element = payload


@contextmanager
def step(
    description: str,
    on_failure: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002 — public kwarg name emitted by codegen
    instruction_id: Optional[str] = None,
) -> Any:
    """Wrap a logical test step with reporting, heal scope and failure routing."""
    global _step_counter
    _step_counter += 1

    if on_failure is not None and on_failure not in _KNOWN_ON_FAILURE:
        raise ValueError(
            f"unknown on_failure {on_failure!r}; expected one of {sorted(_KNOWN_ON_FAILURE)}"
        )

    info = StepInfo(
        description=description,
        instruction_id=instruction_id or id,
        on_failure=on_failure,
    )
    token = _current_step.set(info)
    rep = reporter()
    rep.begin_step(description, instruction_id=info.instruction_id)

    error: Optional[BaseException] = None
    try:
        yield info
    except BaseException as e:  # noqa: BLE001 — see below; it is re-raised, not swallowed
        # BaseException, not Exception, so a Ctrl-C, a pytest.fail, a SystemExit or a
        # GeneratorExit inside the body is reported as ok=False rather than escaping
        # this handler and leaving the finally below to report a pass.
        error = e
    finally:
        rep.end_step(
            description,
            ok=error is None,
            error=error,
            instruction_id=info.instruction_id,
            is_autohealed=info.is_autohealed,
            autoheal_source=info.autoheal_source,
            interacted_element=info.interacted_element,
        )
        _current_step.reset(token)

    if error is None:
        return
    # on_failure routes ORDINARY failures only. A KeyboardInterrupt or a SystemExit is
    # not a step outcome to continue past — swallowing one on a fail-continue step
    # would make the suite unstoppable.
    if isinstance(error, Exception):
        if on_failure == FAIL_CONTINUE:
            mark_step_failed(description, error)
            return
        if on_failure == WARN_CONTINUE:
            _log.warning(
                "step %r failed (on_failure=warn-continue): %s", description, error
            )
            rep.warn_step(description, error)
            return
    raise error
