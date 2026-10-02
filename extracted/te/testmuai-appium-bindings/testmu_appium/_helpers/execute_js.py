"""VALUE-returning execute_js verb — run a recorded JavaScript snippet.

A native session has no DOM to evaluate against, so the snippet runs through
the LambdaTest grid hook ("lambda-kane-ai" / executeScript) — the same channel
the legacy V2 exported runtime uses (auteur models/appium_uiActions.py::
execute_script_action). That mobile call site's payload shape is this
verb's contract; keep the two in lockstep.

Cloud-only: a local Appium session has no lambda hook endpoint, so a local
run raises instead of silently returning nothing.
"""
import json
import logging

from testmu_appium import _config
from testmu_appium import _vars

_log = logging.getLogger("testmu_appium")


def _json_safe_variables() -> dict:
    """The variable store, filtered to JSON-serialisable entries.

    The hook payload travels as JSON; a non-serialisable value would fail the
    whole call rather than just its own injection.
    """
    safe = {}
    for name, value in _vars._variable_store.items():
        try:
            json.dumps(value)
        except (TypeError, ValueError):
            continue
        safe[name] = value
    return safe


def execute_js(driver, *, script: str, timeout_sec: int = 10,
               output_variable: str = "", description: str = ""):
    """Execute a JavaScript snippet via the LambdaTest grid hook.

    Args:
        driver: Live Appium webdriver session (cloud run target).
        script: The snippet exactly as recorded ("return ...;" style).
        timeout_sec: Hook-side execution deadline.
        output_variable: When set, the result is also stored via set_var.
        description: Optional human-readable label for the INFO log line.

    Returns:
        The snippet's return value.

    Raises:
        RuntimeError: local run target (no hook available), an invalid hook
            response, or a JavaScript error/timeout reported by the hook.
    """
    if _config.run_target != "cloud":
        raise RuntimeError(
            "execute_js runs through the LambdaTest grid hook and needs "
            "run_target='cloud'"
        )

    args = {
        "command": "executeScript",
        "driverSessionId": driver.session_id,
        "testId": _config.get("test_id") or driver.session_id,
        "commitId": _config.get("commit_id"),
        "org_id": int(_config.get("org_id") or 0),
        "payload": {
            "is_mobile": True,
            "mobile_browser": False,
            "code_snippet": script,
            "script_type": "javascript",
            "variables": _json_safe_variables(),
            "timeout_sec": timeout_sec,
        },
    }
    response = driver.execute_script("lambda-kane-ai", args)

    if not response or not isinstance(response, dict):
        raise RuntimeError(f"invalid response from lambda hook: {response!r}")
    if response.get("timed_out"):
        raise RuntimeError(f"JavaScript execution timed out after {timeout_sec}s")
    if response.get("error"):
        line = response.get("line")
        at_line = f" at line {line}" if line is not None else ""
        raise RuntimeError(f"JavaScript error{at_line}: {response['error']}")

    value = response.get("value")
    suffix = f" — {description}" if description else ""
    _log.info("execute_js: ok%s", suffix)
    if output_variable:
        _vars.set_var(output_variable, value)
    return value
