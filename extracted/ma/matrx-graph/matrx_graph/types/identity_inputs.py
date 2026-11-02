"""Identity inputs — the input fields an edge BROADCAST must never fill.

THE CLASS THIS CLOSES (live defect, 2026-09-12)
-----------------------------------------------
A step's output payload flows down a plain ``data`` edge with no explicit
``mappings``, so the whole dict is merged into the next node's inputs
(:meth:`Scheduler._map_edge_payload`). That default is right for ordinary
data — and catastrophic for one narrow family of fields: the ones that name
a **durable resource somebody else owns**. An ``ai.agent.start`` step's
result carries ``conversation_id``; broadcast into a downstream agent step
it silently became that step's ``conversation_id``, so the second agent
tried to CONTINUE the first agent's conversation with its own variables and
the conversation binding guard refused the whole run with a 409
(``conversation_binding_mismatch``). The author never asked for that — an
edge they drew to pass data along re-pointed the step's identity.

THE RULE
--------
A field marked :func:`identity_input` binds ONLY from something the author
declared for that step: the node's own ``static_inputs`` (a literal or a
``{"$var": ...}`` reference), or an edge mapping that names it explicitly
(``mappings: {"conversation_id": "conversation_id"}``). It NEVER binds
because an upstream payload happened to carry a key with that name.

Dropping is announced, never silent (law 4): the scheduler logs which keys
it withheld, from which edge, and what to do instead.

Marking a field costs one line::

    conversation_id: str | None = Field(
        default=None,
        json_schema_extra=identity_input(),
        description="Continue an existing conversation. Leave blank for a fresh thread.",
    )

It is deliberately opt-in: only the node type knows which of its fields name
a resource with an owner. Everything else keeps the broadcast default.

A step that REFUSES an identity it no longer takes (Run Agent and its family
lost ``conversation_id`` / ``is_new`` on 2026-10-29: continuing a conversation
is the Chat steps' job) names those keys in a class attribute instead of a
field, so an upstream broadcast carrying them is still withheld — announced —
while an author who maps or sets one reaches the step's own refusal::

    __identity_inputs__: ClassVar[frozenset[str]] = frozenset({"conversation_id", "is_new"})
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import BaseModel

#: JSON-Schema extra key carrying the mark. Lives in the exported schema so a
#: studio / validator can read it too, alongside the ``ui:*`` vocabulary.
IDENTITY_INPUT_KEY = "x-identity-input"

#: Class attribute naming identity keys a step declares WITHOUT a field (see module docstring).
IDENTITY_INPUTS_ATTR = "__identity_inputs__"


def identity_input(**extra: Any) -> dict[str, Any]:
    """``json_schema_extra`` marking a field as a resource identity.

    Extra keys are passed through verbatim so a field can carry both this
    mark and other schema extras.
    """
    return {IDENTITY_INPUT_KEY: True, **extra}


@lru_cache(maxsize=512)
def identity_input_fields(model: type[BaseModel]) -> frozenset[str]:
    """Names of ``model``'s fields marked :func:`identity_input`.

    Returns the wire names (alias when one is set) so the result can be
    matched straight against an edge payload's keys.
    """
    names: set[str] = set()
    for field_name, field in model.model_fields.items():
        extra = field.json_schema_extra
        if isinstance(extra, dict) and extra.get(IDENTITY_INPUT_KEY) is True:
            names.add(field.alias or field_name)
    names.update(getattr(model, IDENTITY_INPUTS_ATTR, None) or ())
    return frozenset(names)
