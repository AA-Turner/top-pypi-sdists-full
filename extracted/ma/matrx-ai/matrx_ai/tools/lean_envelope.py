"""A lean dispatcher row built from a flat one, and the ``guide`` every lean row answers.

A tool whose provider definition is the flattened union of every action's arguments pays
for all of them on every run that carries it. The lean shape (``records``, 2026-10-02) shows
the provider ``action`` + one ``args`` object; each action's arguments are served on demand
by ``{"action": "guide", "args": {"topic": "<action>"}}``.

Two pieces live here, ONCE, so any dispatcher row can go lean without code of its own:

* :func:`envelope_parameters` turns a flat row's ``parameters`` into the lean shape. The
  per-action contract (``$variants``) keeps every argument, type, enum, default and bound
  exactly; it only GAINS text: each argument's root-map description when its variant
  entry had none, and each action's own description. The drift gate, the executor's
  validation and the delegated pre-check read ``$variants``, so nothing they enforce moves.
* :func:`row_guide` answers ``guide`` from the row itself. A tool whose code union has its
  own ``guide`` action (``records``) keeps answering it; for every other lean row the
  executor answers it here, before validation and before delegation (a delegated client
  has no ``guide`` of its own), so the tool's code and its clients are untouched.
"""

from __future__ import annotations

import copy
from typing import Any

#: The action a lean row answers from its own ``$variants``.
GUIDE_ACTION = "guide"

#: The object a lean row's calls carry their arguments in.
ENVELOPE = "args"


def _is_schema_object(spec: Any) -> bool:
    return isinstance(spec, dict) and isinstance(spec.get("properties"), dict)


def _as_schema_object(spec: dict[str, Any]) -> dict[str, Any]:
    """A property-map variant (``{arg: {type, required: true}}``) as a JSON-Schema object.

    The two shapes are the same contract to ``canon_db_params``; only the object shape has
    a place for the action's own description (in a property map, ``description`` would be
    an argument of that name).
    """
    if _is_schema_object(spec):
        return copy.deepcopy(spec)
    properties: dict[str, Any] = {}
    required: list[str] = []
    for name, prop in spec.items():
        entry = copy.deepcopy(prop) if isinstance(prop, dict) else {"type": prop}
        if entry.pop("required", False) is True:
            required.append(name)
        properties[name] = entry
    return {"type": "object", "required": required, "properties": properties}


def envelope_parameters(
    parameters: dict[str, Any],
    *,
    action_how: dict[str, str],
    action_description: str = "What to do; each action is listed above.",
    envelope_description: str | None = None,
    discriminator: str = "action",
) -> dict[str, Any]:
    """The lean ``parameters`` of a flat dispatcher row: ``action`` + ``args`` + ``$variants``.

    ``action_how`` is each action's own text, stored as ``$variants.<action>.description``
    and served by ``guide`` (a missing entry keeps the variant's existing description).
    The advertised ``action`` enum is the row's enum plus ``guide``.
    """
    from matrx_ai.tools.models import ARGS_ENVELOPE_KEY

    variants = parameters.get("$variants")
    root_disc = parameters.get(discriminator)
    if not isinstance(variants, dict) or not variants or not isinstance(root_disc, dict):
        raise ValueError("a lean row is built from a dispatcher row with $variants and an action enum")
    unknown = set(action_how) - set(variants)
    if unknown:
        raise ValueError(f"action_how names actions the row does not have: {sorted(unknown)}")

    lean_variants: dict[str, Any] = {}
    for action, spec in variants.items():
        if not isinstance(spec, dict):
            raise ValueError(f"$variants.{action} is not an object")
        out = _as_schema_object(spec)
        for name, prop in out["properties"].items():
            root = parameters.get(name)
            if (
                isinstance(prop, dict)
                and "description" not in prop
                and isinstance(root, dict)
                and isinstance(root.get("description"), str)
            ):
                prop["description"] = root["description"]
        how = action_how.get(action)
        if how:
            out["description"] = how
        lean_variants[action] = out

    enum = [a for a in (root_disc.get("enum") or list(variants)) if a != GUIDE_ACTION]
    return {
        discriminator: {
            "type": "string",
            "enum": [*enum, GUIDE_ACTION],
            "required": True,
            "description": action_description,
        },
        ENVELOPE: {
            "type": "object",
            "description": envelope_description
            or (
                "That action's arguments. "
                f'{{"{discriminator}": "{GUIDE_ACTION}", "{ENVELOPE}": {{"topic": "<action>"}}}} '
                "lists them."
            ),
        },
        ARGS_ENVELOPE_KEY: ENVELOPE,
        "$variants": lean_variants,
    }


def serves_row_guide(tool_def: Any, arguments: Any, *, discriminator: str = "action") -> bool:
    """True when this call is a lean row's ``guide`` that the ROW answers (no code guide)."""
    if not isinstance(arguments, dict) or arguments.get(discriminator) != GUIDE_ACTION:
        return False
    if getattr(tool_def, "args_envelope", None) is None:
        return False
    variants = (getattr(tool_def, "parameters", None) or {}).get("$variants")
    return isinstance(variants, dict) and GUIDE_ACTION not in variants


def _argument_entry(prop: Any, *, required: bool) -> dict[str, Any]:
    entry = {k: v for k, v in (prop if isinstance(prop, dict) else {"type": prop}).items() if k != "title"}
    entry.pop("required", None)
    if required:
        entry["required"] = True
    return entry


def row_guide(tool_def: Any, topic: Any) -> dict[str, Any]:
    """What ``guide`` answers: one action's rules and every argument, read from the row.

    No topic, or a name that is not an action, answers the list of actions with each
    one's text, so a guessed name is corrected rather than refused.
    """
    variants = (getattr(tool_def, "parameters", None) or {}).get("$variants") or {}
    name = topic.strip() if isinstance(topic, str) else ""
    spec = variants.get(name) if name != GUIDE_ACTION else None
    if not isinstance(spec, dict):
        actions = {}
        for action, entry in variants.items():
            text = entry.get("description") if _is_schema_object(entry) else None
            actions[action] = text if isinstance(text, str) else ""
        return {
            "topic": None,
            "note": (f"{name!r} is not an action of this tool. " if name else "")
            + f'Call {{"action": "{GUIDE_ACTION}", "{ENVELOPE}": {{"topic": "<action>"}}}} '
            "with one of these for its arguments.",
            "actions": actions,
        }
    obj = _as_schema_object(spec)
    required = set(obj.get("required") or [])
    return {
        "topic": name,
        "how": obj.get("description"),
        "arguments": {
            arg: _argument_entry(prop, required=arg in required)
            for arg, prop in obj["properties"].items()
        },
        "send": f'{{"action": "{name}", "{ENVELOPE}": {{...these arguments}}}}',
    }


__all__ = [
    "ENVELOPE",
    "GUIDE_ACTION",
    "envelope_parameters",
    "row_guide",
    "serves_row_guide",
]
