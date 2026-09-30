"""Per-step variable buffer reported on the step's end hook.

Every variable the step READS or WRITES between its start and end hook is
recorded here; the LT reporter drains the buffer into the
``lambda-testCase-end`` payload as ``variables`` so the instance view can show
the values the step actually ran with, instead of only the names.

Two deliberate exclusions, both because this buffer is shipped to the hub and
written into the run's artefacts:

* ``{{secrets.x}}`` resolves to a live credential.
* ``{{totp.x}}`` resolves to a one-time code.

Neither is ever recorded — the recording calls live in the other resolution
branches, not in a shared choke point, precisely so this stays true by
construction rather than by a filter someone can forget to update.
"""
import json
import logging
from typing import Any

_log = logging.getLogger("testmu")

_step_variables: dict[str, Any] = {}


def _json_safe(value: Any) -> Any:
    """Coerce to something ``json.dumps`` accepts.

    The buffer is serialized as a whole, so one odd value (a Locator, a
    datetime, a custom object) would otherwise take the entire hook payload
    down with it.
    """
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


def record_read(name: str, value: Any) -> Any:
    """Record a variable this step read and return it unchanged."""
    record_variable(name, value)
    return value


def pop_step_variables() -> dict:
    """Return and clear the variables recorded since the last drain."""
    global _step_variables
    produced = _step_variables
    _step_variables = {}
    return produced


def reset_step_variables() -> None:
    """Internal — clear the buffer at session start so runs never bleed."""
    pop_step_variables()
