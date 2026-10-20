"""Required agent inputs: a run missing one is refused before any model call.

A variable declared ``required: true`` must reach the run with a non-empty value after the
whole ladder (explicit caller value > binding > saved default). With enforcement on, a run
missing any of them raises :class:`RequiredVariablesMissing` naming every missing input, so a
screen can highlight them and nothing is paid for. With enforcement off (the default), a
required flag changes nothing at run time, exactly as before.

Whether enforcement is on is the host's platform knob (aidream:
``agents.variable_binding.required_inputs_enforced``). The package cannot read it, so the host
injects a zero-argument reader through :func:`configure_required_variable_enforcement`. Unwired,
enforcement is off.
"""

from __future__ import annotations

import sys

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

_enforcement_reader: Callable[[], bool] | None = None


def configure_required_variable_enforcement(reader: Callable[[], bool] | None) -> None:
    """Install (or clear, with ``None``) the host's reader for the enforcement switch."""
    global _enforcement_reader
    _enforcement_reader = reader


_announced_unreadable = False


def required_variables_enforced() -> bool:
    """True when the host switched enforcement on. A reader that cannot answer (a process that
    runs agents before priming its knobs) is announced once and falls to the package posture: off.
    """
    global _announced_unreadable
    if _enforcement_reader is None:
        return False
    try:
        return bool(_enforcement_reader())
    except Exception as exc:  # noqa: BLE001 — announced, then the package posture (off)
        if not _announced_unreadable:
            _announced_unreadable = True
            print(
                "[matrx_ai.required_variables] enforcement switch unreadable; required inputs are "
                f"NOT enforced in this process until it is: {exc!r}",
                file=sys.stderr,
            )
        return False


@dataclass(frozen=True)
class _RequiredMissingInfo:
    """What ``create_streaming_response`` / the API error handler read off ``exc.error_info``."""

    error_type: str
    code: str
    message: str
    user_message: str
    details: dict[str, Any] = field(default_factory=dict)
    status_code: int = 422


class RequiredVariablesMissing(ValueError):
    """The run did not start: required inputs have no value. Retrying without them cannot help."""

    def __init__(self, missing: list[str], *, agent_name: str | None = None) -> None:
        self.missing = list(missing)
        names = ", ".join(self.missing)
        who = f"'{agent_name}'" if agent_name else "This agent"
        message = f"{who} was not run: required input(s) missing: {names}"
        super().__init__(message)
        self.error_info = _RequiredMissingInfo(
            error_type="required_variables_missing",
            code="required_variables_missing",
            message=message,
            user_message=f"Fill in {names} to run this agent.",
            details={"missing": self.missing, "retryable": False},
        )


def _is_required(declared: Any) -> bool:
    if isinstance(declared, Mapping):
        required, binding = declared.get("required"), declared.get("binding")
    else:
        required, binding = getattr(declared, "required", False), getattr(declared, "binding", None)
    # A bound variable (scope context item, custom data / merge field) is filled by the server
    # from its binding and is never a caller requirement: the same exemption the client's
    # selectMissingRequiredVariables applies. An on_missing='error' binding refuses on its own.
    if isinstance(binding, Mapping) and binding:
        return False
    return required is True


def missing_required_variables(
    definitions: Mapping[str, Any] | None, values: Mapping[str, Any] | None
) -> list[str]:
    """Declared-required names whose final value is empty (None, blank text, empty list/dict)."""
    from matrx_ai.config.template_substitution import is_empty_value

    values = values or {}
    return [
        name
        for name, declared in (definitions or {}).items()
        if _is_required(declared) and is_empty_value(values.get(name))
    ]


def enforce_required_variables(
    definitions: Mapping[str, Any] | None,
    values: Mapping[str, Any] | None,
    *,
    agent_name: str | None = None,
    pinned_version: bool = False,
) -> None:
    """Raise :class:`RequiredVariablesMissing` when enforcement is on and an input is missing.

    Only a run of the agent's CURRENT definition is enforced. A run of a pinned version (a
    shortcut or binding that pins ``agent_version_id``) keeps the flags that version was saved
    with, which predate the reset of every required flag (2026-10-17), so it is skipped and the
    skip is said out loud once per run.
    """
    if not definitions or not required_variables_enforced():
        return
    missing = missing_required_variables(definitions, values)
    if not missing:
        return
    if pinned_version:
        print(
            f"[matrx_ai.required_variables] pinned-version run of {agent_name or 'an agent'}: "
            f"required input(s) {', '.join(missing)} not enforced (enforcement covers current "
            "definitions only)",
            file=sys.stderr,
        )
        return
    raise RequiredVariablesMissing(missing, agent_name=agent_name)
