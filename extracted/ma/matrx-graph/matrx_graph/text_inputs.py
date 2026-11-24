"""A text-only input handed a whole record or list — ONE rule for the save check and the run.

Live, release 36eaeafb684 (2026-11-03): Company Setup built "Send pickup reminders" with a For
each whose payload was ``{"prompt": "$item"}`` over ``table.row.list`` rows, so each whole Row
landed on ``ai.llm.chat``'s text ``prompt`` and every run stopped with ``string_type``.

* At SAVE, ``validation._text_input_fed_object_issues`` warns wherever the declared shapes prove it
  (offers, never blocks), naming the ``$format`` fix.
* At RUN, :func:`render_whole_values_as_text` turns such a value into JSON text — exactly what
  ``{"$format": "{item}"}`` would send — and returns what it rendered, so the scheduler announces
  it on the step (``engine.sent_whole_value_as_text`` review flag). Never silent.

Only a TOP-LEVEL input whose schema accepts nothing but text (``str`` / ``str | None``) and whose
value is a dict or list is rendered; every other mismatch still fails at the input gate.
"""

from __future__ import annotations

from typing import Any

__all__ = ["text_only", "render_whole_values_as_text", "RENDERED_NOTE", "text_scalars_as_text", "SCALAR_NOTE"]

#: The note a step carries when a number / yes-no value was written as text for a text input.
SCALAR_NOTE = "sent the {shape} value as the text '{text}' for '{field}', which is declared as text"

#: The note a step carries when the run rendered a whole value as text for it.
RENDERED_NOTE = "sent the whole {shape} as text for '{field}'; pick fields for a tighter prompt"


def _resolve(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    ref = schema.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/$defs/"):
        target = (root.get("$defs") or {}).get(ref[len("#/$defs/"):])
        if isinstance(target, dict):
            return target
    return schema


def text_only(schema: Any, root: dict[str, Any]) -> bool:
    """True when an input schema accepts ONLY text (``str`` or ``str | None``)."""
    if not isinstance(schema, dict):
        return False
    schema = _resolve(schema, root)
    branches = schema.get("anyOf") or schema.get("oneOf")
    if isinstance(branches, list):
        kinds = [_resolve(b, root).get("type") for b in branches if isinstance(b, dict)]
        return "string" in kinds and all(k in ("string", "null") for k in kinds)
    return schema.get("type") == "string"


def render_whole_values_as_text(
    inputs: dict[str, Any], schema_json: dict[str, Any]
) -> tuple[dict[str, Any], list[tuple[str, str]]]:
    """Render each dict/list given to a text-only input as JSON text.

    Returns the new inputs and ``[(field, "record" | "list"), ...]`` for every value rendered.
    """
    from matrx_graph.nodes._template import _stringify  # the one $format renderer

    props = schema_json.get("properties")
    if not isinstance(props, dict):
        return inputs, []
    rendered: list[tuple[str, str]] = []
    out = inputs
    for key, value in inputs.items():
        if isinstance(value, (dict, list)) and text_only(props.get(key), schema_json):
            if out is inputs:
                out = dict(inputs)
            out[key] = _stringify(value)
            rendered.append((key, "record" if isinstance(value, dict) else "list"))
    return out, rendered


def text_scalars_as_text(
    inputs: dict[str, Any], schema_json: dict[str, Any]
) -> tuple[dict[str, Any], list[tuple[str, str, str]]]:
    """Write a lossless scalar (yes/no or number) given to a text-only input as its canonical text.

    ``True`` -> ``"true"``, ``False`` -> ``"false"``, ``3`` -> ``"3"``. Returns the new inputs and
    ``[(field, "yes/no" | "number", text), ...]`` so the caller announces it. Validation offers,
    never blocks: a lossless scalar is converted; objects, lists and unrelated types still fail
    the input gate with their per-field message."""
    props = schema_json.get("properties")
    if not isinstance(props, dict):
        return inputs, []
    done: list[tuple[str, str, str]] = []
    out = inputs
    for key, value in inputs.items():
        if isinstance(value, (bool, int, float)) and text_only(props.get(key), schema_json):
            if isinstance(value, bool):
                text, shape = ("true" if value else "false"), "yes/no"
            else:
                text, shape = (str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)), "number"
            if out is inputs:
                out = dict(inputs)
            out[key] = text
            done.append((key, shape, text))
    return out, done
