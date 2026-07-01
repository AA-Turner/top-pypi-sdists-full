"""Driver-level wait helpers — encapsulates timing/condition logic for codegen.

Maps to AST nodes:
- WaitNode (timeout_ms field) → wait()
- WaitUntilNode (query, timeout fields) → wait_until()
- WaitForLoadNode (state field: 'load' | 'domcontentloaded' | 'networkidle') → wait_for_load()

Codegen reference:
- wait emits time.sleep(N)
- wait_until emits time.sleep(N) — current stub
- wait_for_load emits JS document.readyState polling
- check_until_condition emits checkUntilCondition(get_driver(...), "<condition>")
  and evaluates generated Selenium-Python condition expressions locally.
"""
from __future__ import annotations

import logging
import time

from selenium.webdriver.support.ui import WebDriverWait

from testmu_selenium._errors import ConditionEvaluationError
from testmu_selenium._vars import get_variable_value
from testmu_selenium.condition import (
    Assertion,
    Condition,
    Mathmatic,
    PossibleCondition,
    ResolvedCondition,
)

_LOAD_TIMEOUT_S = 30


def wait(driver, *, milliseconds: int | None = None) -> None:
    """Sleep for the given milliseconds.

    No-op if `milliseconds` is None.
    """
    if milliseconds is None:
        return
    time.sleep(milliseconds / 1000)


def wait_until(driver, query: str, *, timeout: int = 30000) -> None:
    """Wait up to ``timeout`` ms for ``query`` to hold.

    Intentionally a fixed ``time.sleep(timeout/1000)`` today: the Selenium code
    generator emits a static sleep for WaitUntilNode and never calls this helper
    with a pollable condition, so there is no condition to poll here. Turning
    this into real condition polling belongs in the code-gen layer (emit a
    polling loop) and is tracked as a follow-up; the binding deliberately
    mirrors current codegen output rather than inventing an unused contract.
    """
    time.sleep(timeout / 1000)


def wait_for_load(driver, *, state: str = 'load') -> None:
    """Wait until document.readyState matches ``state``.

    - state='load': polls until readyState == 'complete'
    - state='domcontentloaded': polls until readyState != 'loading'
    - state='networkidle': Selenium WebDriver has no native network-idle
      primitive (unlike Playwright's ``page.wait_for_load_state('networkidle')``),
      so this is intentionally treated the same as 'load' — readyState complete.
    """
    if state == 'domcontentloaded':
        WebDriverWait(driver, _LOAD_TIMEOUT_S).until(
            lambda d: d.execute_script("return document.readyState") != 'loading'
        )
    else:
        # state in ('load', 'networkidle'); 'networkidle' falls back to 'load'
        # because Selenium has no native network-idle wait.
        WebDriverWait(driver, _LOAD_TIMEOUT_S).until(
            lambda d: d.execute_script("return document.readyState") == 'complete'
        )


_until_log = logging.getLogger("testmu_selenium.check_until_condition")


def check_until_condition(driver, condition: str) -> bool:
    """Evaluate a generated Selenium until-condition expression locally.

    ``condition`` is a Python expression produced by code generation, e.g.
    ``Condition(...).evaluate({}, get_variable_value)[0]``. It is evaluated
    against the runtime variable store and the bundled condition runtime
    classes, and the boolean result is returned.

    The Selenium export must NOT call the V16 visual wait/check API. A condition
    that cannot be evaluated as a Python expression — natural language, a syntax
    error, or an unknown name — raises ConditionEvaluationError rather than
    returning False, so a never-evaluable condition fails loudly instead of
    silently exhausting the caller's retry budget.
    """
    _until_log.info("    [check_until_condition] condition=%s", condition[:80])
    allowed_names = {
        "Assertion": Assertion,
        "Condition": Condition,
        "Mathmatic": Mathmatic,
        "PossibleCondition": PossibleCondition,
        "ResolvedCondition": ResolvedCondition,
        "get_variable_value": get_variable_value,
    }
    try:
        met = bool(eval(condition, {"__builtins__": {}}, allowed_names))
    except Exception as exc:
        _until_log.warning(
            "    [check_until_condition] could not evaluate condition %r: %s",
            condition[:120], exc,
        )
        raise ConditionEvaluationError(condition, exc) from exc
    _until_log.info("    [check_until_condition] met=%s", met)
    return met


__all__ = ["wait", "wait_until", "wait_for_load", "check_until_condition"]
