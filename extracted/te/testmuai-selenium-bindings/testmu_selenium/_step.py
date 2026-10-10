"""Step context manager — wraps a logical test step with reporting + heal context."""
import logging
import re
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
    # The label BEFORE variable substitution. get_step_intent() gates on this: a label
    # that was templated cannot be trusted as a locate intent, because whether its
    # variables actually resolved depends on the environment (see get_step_intent).
    raw_description: str | None = None


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


_TEMPLATE_TOKEN_RE = re.compile(r"\{\{(.+?)\}\}|\$\{(.+?)\}")


def get_step_intent():
    """The active step's label — the authored instruction — or None.

    The heal payload's locate intent. V2 sends the authored sentence to
    /v2/locate/desktop (UIActions._try_locate_element_web reads
    meta['operation_intent']) and automind's locate prompt extracts TARGET from it,
    so the cascade sends the instruction rather than the bare element phrase.

    Returns None — so callers fall back to the element description — when there is no
    active step, and ALSO whenever the AUTHORED label carried a {{...}}/${...}
    template. A label only resolves when the producing step ran in the same process:
    true of an exported script (set_var is emitted ahead of it), false in a live
    auteur session, which executes one instruction at a time.

    Gating on the authored label rather than the resolved one is deliberate — the two
    bindings fail differently and neither failure is detectable afterwards. Selenium
    leaves the token in place ("Click {{item}} button"); playwright BLANKS it ("Click
    button"), which is indistinguishable from a variable that legitimately resolved to
    "". Either way automind gets something worse than the element phrase it replaced,
    so a templated label simply never becomes the intent.
    """
    active = _current_step.get(None)
    if active is None:
        return None
    label = getattr(active, "description", None)
    if not isinstance(label, str) or not label:
        return None
    raw = getattr(active, "raw_description", None) or label
    if _TEMPLATE_TOKEN_RE.search(raw):
        return None
    return label


def _resolve_label(description):
    """Resolve {{name}} / ${name} in a step label against the live variable store.

    The label is the authored instruction, so it still carries templates
    ("Type \'parth\' in {{search}} field"). Without this the [STEP N] logs and both
    lambda-testCase-* hooks ship raw mustaches to the dashboard. Mirrors V2, which
    resolves inside the hook itself (UIActions.lambda_hooks -> get_variable_value).

    str()-guarded: var() returns the NATIVE value when the whole string is one
    template, and a non-str label would break the logger and json.dumps downstream.
    Never raises — a reporting label must not fail the step.
    """
    if not isinstance(description, str):
        return description
    try:
        from testmu_selenium._vars import var
        return str(var(description))
    except Exception as e:  # noqa: BLE001 — label resolution is best-effort
        logger.debug("[testmu] step label resolve skipped: %s", e)
        return description


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
    raw_description = description
    description = _resolve_label(description)
    logger.info("  [STEP %d] %s", n, description)
    info = StepInfo(description=description, timeout_ms=timeout_ms, on_failure=on_failure,
                    instruction_id=instruction_id, raw_description=raw_description)
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
