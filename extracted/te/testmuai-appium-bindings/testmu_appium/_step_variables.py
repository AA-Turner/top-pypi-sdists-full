"""Per-step variable buffer for the step-end hook; secrets/totp are never recorded (it ships to the hub)."""
import json
import logging
from typing import Any

_log = logging.getLogger(__name__)

_step_variables: dict[str, Any] = {}


def _json_safe(value: Any) -> Any:
    """Coerce to something ``json.dumps`` accepts so one odd value cannot break the payload."""
    try:
        json.dumps(value)
        return value
    except Exception:  # noqa: BLE001 — any unserializable value degrades to its repr
        return str(value)


def record_variable(name: str, value: Any) -> None:
    """Record a variable this step read or wrote. Never raises."""
    if not name:
        return
    try:
        _step_variables[name] = _json_safe(value)
    except Exception as e:  # noqa: BLE001 — reporting must never fail a step
        _log.debug("[testmu] step-variable record skipped for %r: %s", name, e)


def pop_step_variables() -> dict:
    """Return and clear the variables recorded since the last drain."""
    global _step_variables
    produced = _step_variables
    _step_variables = {}
    return produced


def reset_step_variables() -> None:
    pop_step_variables()
