"""Workflow settings — named, labelled, typed behaviour knobs a person changes without touching steps.

A setting is NOT a new store. It is a declared workflow input (``Definition.variables``, the one input
declaration) placed in the run form's ``Settings`` group (``hints.group == SETTINGS_GROUP``). That one
choice gives it everything the engine already does for an input, and nothing else is built:

- **declared**: name, label, type (number · text · choice · yes/no · list of text), default, one-line help;
- **read by steps** with ``{"$input": name}`` in a step's inputs or settings (INPUT-SURFACE.md);
- **versioned with the workflow**: it lives in the definition, so every saved version carries its values;
- **visible on the run**: the landed value and its provenance are stamped on the run row like any input;
- **overridable per run**: a caller (API, schedule, Mandate, run form) passes ``name → value``.

What this module adds is the part an input does not promise: a setting ALWAYS has a value (it never asks
and never blocks), its type is one of five plain ones, and both its default and a run's override are
checked against that type — the definition at save/validate, the override at run start (the run parks
naming the problem, never a step failing later on a wrong value). ``set_workflow_setting`` changes a
setting's default by name (``patch.py``).
"""

from __future__ import annotations

from typing import Any

from matrx_graph.input_declaration import VariableDefinition

#: The run-form group a declared input is placed in to be a workflow setting.
SETTINGS_GROUP = "Settings"

#: The plain types a setting may have: ``types.input_surface.input_type`` names, plus ``list`` (a list of
#: text: a setting whose default is a list, declared with no control; see :func:`setting_type`).
SETTING_TYPES: tuple[str, ...] = ("number", "text", "choice", "yes_no", "list")


def setting_type(var: VariableDefinition) -> str | None:
    """The setting's plain type. A list of text has no control of its own in the input declaration
    (``input_type`` reads it as free-form JSON), so it is read from its default: a list is a ``list``."""
    from matrx_graph.types.input_surface import input_type

    kind = input_type(var)
    if kind is None and isinstance(var.defaultValue, list):
        return "list"
    return kind


def is_setting(var: VariableDefinition) -> bool:
    """True when this declared input is a workflow setting."""
    hints = var.hints
    return bool(hints is not None and (hints.group or "").strip() == SETTINGS_GROUP)


def declared_settings(variables: list[VariableDefinition]) -> list[VariableDefinition]:
    """The workflow's settings, in declared order."""
    return [v for v in variables if is_setting(v)]


def setting_value_problem(var: VariableDefinition, value: Any) -> str | None:
    """Why ``value`` cannot be this setting's value, in a person's words; None when it fits."""
    from matrx_graph.types.input_surface import input_options

    label = var.label or var.name
    kind = setting_type(var)
    if kind not in SETTING_TYPES:
        return f"Setting '{label}' must be a number, text, a choice, yes/no or a list of text."
    if kind == "number":
        if isinstance(value, bool) or not isinstance(value, int | float):
            return f"Setting '{label}' takes a number, and {value!r} is not one."
        return None
    if kind == "yes_no":
        return None if isinstance(value, bool) else f"Setting '{label}' takes yes or no, and {value!r} is neither."
    if kind == "list":
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            return f"Setting '{label}' takes a list of text, and {value!r} is not one."
        return None
    if not isinstance(value, str):
        return f"Setting '{label}' takes text, and {value!r} is not text."
    if kind == "choice":
        options = input_options(var)
        if options and value not in options:
            return f"Setting '{label}' is one of {', '.join(options)}; {value!r} is not."
    return None


def definition_setting_problems(variables: list[VariableDefinition]) -> list[tuple[str, str]]:
    """``(name, problem)`` for each setting the definition declares wrongly: no default, a default that
    does not fit its type, or a sourcing that would ask or block (a setting always has its value)."""
    problems: list[tuple[str, str]] = []
    for var in declared_settings(variables):
        label = var.label or var.name
        if var.defaultValue is None:
            problems.append((var.name, f"Setting '{label}' needs a default value."))
            continue
        if var.sourcing in ("ask", "require") or var.required:
            problems.append((var.name, f"Setting '{label}' always has its default, so it cannot be asked for or required."))
        problem = setting_value_problem(var, var.defaultValue)
        if problem:
            problems.append((var.name, problem))
    return problems


def coerce_setting_text(var: VariableDefinition, text: str) -> Any:
    """A setting's value from the text a patch op carries (``set_workflow_setting`` values are strings):
    ``"3"`` → 3, ``"true"`` → True, ``'["a", "b"]'`` or ``"a, b"`` → ["a", "b"] for their types; anything
    that does not read stays the text (and is then refused by :func:`setting_value_problem`)."""
    import json

    kind = setting_type(var)
    raw = text.strip()
    if kind == "list":
        if raw.startswith("["):
            try:
                return json.loads(raw)
            except ValueError:
                return text
        return [item.strip() for item in raw.replace("\n", ",").split(",") if item.strip()]
    if kind == "number":
        try:
            number = float(raw)
        except ValueError:
            return text
        return int(number) if number.is_integer() and "." not in raw and "e" not in raw.lower() else number
    if kind == "yes_no":
        lowered = raw.lower()
        if lowered in ("true", "yes", "on", "1"):
            return True
        if lowered in ("false", "no", "off", "0"):
            return False
    return text
