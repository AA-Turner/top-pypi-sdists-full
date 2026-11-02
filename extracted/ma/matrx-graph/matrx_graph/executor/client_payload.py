"""Folding a CLIENT-authored payload into a node's declared output shape.

Some nodes are resumed with a payload the CLIENT wrote — ``control.human_input``
gets whatever the UI collected from the person. Those keys used to be recorded
at the ROOT of the node's output, which meant the node could never declare an
honest output kind: a kind forbids undeclared fields
(``KindModel``: "a field nobody declared is a silent drift channel"), and the
set of keys was whatever the UI felt like sending.

Arman's ruling, 2026-08-21:

    Extra keys belong in a place where you hold the extra keys — inside an
    object, not at the top level. At the top level nothing can read them,
    because nothing knows what to look for.

So a node that expects client-authored keys DECLARES a map to hold them
(``extras``), and this module puts them there. Nothing is lost and nothing is
renamed — a key moves one level down, keeping its name.

This is strictly OPT-IN: a node whose output model has no ``extras`` field is
returned untouched, so this changes nothing for the nodes that never had the
problem.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

#: The declared home for client-authored keys.
EXTRAS_FIELD = "extras"


def declares_extras(output_model: type[BaseModel] | None) -> bool:
    """Whether this node opted in by declaring an ``extras`` map."""
    if output_model is None or not isinstance(output_model, type):
        return False
    if not issubclass(output_model, BaseModel):
        return False
    return EXTRAS_FIELD in output_model.model_fields


def fold_undeclared_into_extras(
    value: dict[str, Any],
    output_model: type[BaseModel] | None,
    *,
    reserved: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    """Move keys the node never declared into its ``extras`` map.

    ``reserved`` names engine-owned keys that belong at the root whatever the
    model says (the decision-provenance stamp) — they are neither folded nor
    dropped.

    An ``extras`` value the client sent itself is merged, with the client's own
    ``extras`` entries losing to root-level keys of the same name: a root key is
    what the UI actually collected, and silently discarding it is the failure
    this whole change exists to prevent.
    """
    if not isinstance(value, dict) or not declares_extras(output_model):
        return value

    declared = set(output_model.model_fields) | {
        field.alias for field in output_model.model_fields.values() if field.alias
    }

    extras: dict[str, Any] = {}
    client_extras = value.get(EXTRAS_FIELD)
    if isinstance(client_extras, dict):
        extras.update(client_extras)

    folded: dict[str, Any] = {}
    for key, item in value.items():
        if key == EXTRAS_FIELD:
            continue
        if key in reserved or key in declared:
            folded[key] = item
        else:
            extras[key] = item

    folded[EXTRAS_FIELD] = extras
    return folded
