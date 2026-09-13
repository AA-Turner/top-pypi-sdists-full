"""THE ONE RULE for "may this output carry a ceiling below the model's maximum?"

One predicate, three consumers — the agent birth path
(``aidream/services/agent_factory/directive.py``), the workflow LLM step
(``matrx_ai/graph_nodes/llm_action.py``) and the release-health audit
(``scripts/check_agent_output_ceilings.py``) — so an authoring path, a run path
and a sweep can never disagree about what counts as a document.

THE RULING (Arman, 2026-09-12, after W41)
-----------------------------------------
An output may carry an explicit ``max_output_tokens`` BELOW its model's real
``ai.model_definition.max_tokens`` **only when the declared schema bounds the
answer's own size** — every leaf an ``enum``, a ``const``, a boolean, a number,
or a string with an explicit ``maxLength``. Then the smaller number is a
knowable fact rather than a guess.

Everything else is a DOCUMENT and gets the model's real maximum:

* a schema carrying an ``array`` — the item COUNT is decided by the input,
  never by the schema;
* a schema carrying a free-form string — a rule statement, a rationale, an
  HTML body;
* free prose with nowhere to continue — a workflow step, a batch job, any
  call whose reply nobody can ask to go on.

WHY IT IS SAFE TO RECONCILE UPWARD RATHER THAN REFUSE. You are billed for
tokens GENERATED, not for tokens PERMITTED (``agent_factory/guards.py`` §
``REASONING_OUTPUT_FLOORS``: *"Raising a CEILING is free"*). An unused cap
costs nothing; a too-small one destroys the whole paid run. The asymmetry is
total, so this reconciles and screams — it never raises.

THE LIVE INCIDENT THIS CLOSES (workflow run
``2cf711eb-1a15-49ed-baf7-ddb166dba129``, 2026-09-12 14:46Z, the Masterwork
Conductor's "Montessori Parenting Adviser — Diagnostic Consultation"). TWO
steps of one run died of the same cause:

* ``ask_questions`` — free prose, authored at ``max_tokens: 1200``. Montessori
  asked seven questions; the parent saw four, followed by *"Ask me to continue
  and I'll pick up where it cut off"* — inside a workflow run, where there is
  nothing to ask.
* ``read_case`` — a declared structured output (arrays of rule ids, free-text
  rationales), authored at ``max_tokens: 2500``. It produced exactly 2,500
  tokens, so the JSON never closed and the whole run errored.

Neither number could have been right: both outputs are a function of the
parent's story. THE PROSE CASE IS THE ONE W41 LEFT OPEN — its census
deliberately exempted prose holders as a "legitimate cost knob", which is true
of a chat assistant a person can prompt again and FALSE of a workflow step.
``continuable`` is that distinction, and it is the caller's to declare.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "as_int",
    "schema_body",
    "unbounded_reason",
    "document_output_reason",
    "enforce_document_ceiling",
]

#: How deep the schema walk goes before it gives up and stays silent.
_MAX_SCHEMA_DEPTH = 24


def as_int(value: Any) -> int | None:
    """A ceiling expressed as ``"4000"`` or ``4000.0`` is still a ceiling.
    Anything that is not a positive whole number declares none."""
    if isinstance(value, bool) or not isinstance(value, int | float | str):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def schema_body(schema: Any) -> Any:
    """Unwrap the ``{"name": …, "schema": {...}}`` json_schema envelope when the
    row stores one; a bare JSON Schema passes straight through."""
    if isinstance(schema, dict) and isinstance(schema.get("schema"), dict):
        return schema["schema"]
    return schema


def unbounded_reason(schema: Any) -> str | None:
    """``None`` when the schema BOUNDS its own answer size; otherwise the word
    naming why it cannot — ``"array"`` or ``"free-text"``.

    Bounded leaves: ``enum``, ``const``, boolean, number/integer, ``null``, and
    a string carrying an explicit ``maxLength``.

    Pure, and total on garbage: an unreadable schema is treated as free-text
    (the safe direction — it gets the model's real maximum).
    """
    body = schema_body(schema)
    if not isinstance(body, dict):
        return "free-text"

    found: set[str] = set()

    def walk(node: Any, depth: int) -> None:
        if depth > _MAX_SCHEMA_DEPTH or not isinstance(node, dict):
            return
        if isinstance(node.get("enum"), list) or "const" in node:
            return  # a fixed menu bounds itself, whatever its declared type
        for combinator in ("anyOf", "oneOf", "allOf"):
            for branch in node.get(combinator) or []:
                walk(branch, depth + 1)
        declared = node.get("type")
        types = declared if isinstance(declared, list) else [declared]
        types = [t for t in types if isinstance(t, str)]
        if "array" in types:
            found.add("array")
            walk(node.get("items"), depth + 1)
        if "string" in types and as_int(node.get("maxLength")) is None:
            found.add("free-text")
        for child in (node.get("properties") or {}).values():
            walk(child, depth + 1)
        extra = node.get("additionalProperties")
        if isinstance(extra, dict):
            walk(extra, depth + 1)
        if isinstance(node.get("items"), dict) and "array" not in types:
            walk(node["items"], depth + 1)

    walk(body, 0)
    if "array" in found:
        return "array"
    if "free-text" in found:
        return "free-text"
    return None


def document_output_reason(
    *,
    output_schema: Any = None,
    continuable: bool = False,
) -> str | None:
    """Is this output a DOCUMENT — something whose length the input decides?

    Returns the reason word (``"array"``, ``"free-text"``, ``"prose"``) or
    ``None`` when a ceiling below the model's maximum is a legitimate knob.

    ``continuable`` says whether the caller sits somewhere a person can say
    "keep going" — a conversation. Free prose in a conversation keeps its cost
    knob, because a truncated reply there is a pause, not a loss. Free prose
    anywhere else (a workflow step, a batch job, an agent minted to produce a
    deliverable) is a document: nobody can ask it to continue, so the cut is
    final and the whole step is wrong.
    """
    schema = schema_body(output_schema)
    if isinstance(schema, dict) and schema:
        return unbounded_reason(output_schema)
    return None if continuable else "prose"


def enforce_document_ceiling(
    settings: Any,
    *,
    model_max: Any,
    output_schema: Any = None,
    continuable: bool = False,
    key: str = "max_output_tokens",
    label: str = "",
) -> list[str]:
    """Raise a document's ceiling to the model's real maximum, in place.

    RECONCILES and screams; never raises. Returns one human-readable line per
    repair (what it did and why), empty when nothing was wrong — the same
    contract as ``agent_factory.guards.enforce_reasoning_output_budget``, so
    both birth-path guards log alike.

    ``settings`` may be a plain settings dict (the agent row's ``settings``) or
    any object carrying ``key`` as an attribute (a live ``UnifiedConfig``); both
    are mutated where they stand, so the caller keeps holding the same object.

    An ABSENT ceiling is not this defect: the offering default (already the
    model's maximum since 2026-09-11) applies, and inventing a number where the
    author chose none would be the silent default the platform forbids. Only an
    explicit, too-low ceiling is repaired.
    """
    is_mapping = isinstance(settings, dict)
    if not is_mapping and not hasattr(settings, key):
        return []
    declared = as_int(settings.get(key) if is_mapping else getattr(settings, key, None))
    ceiling = as_int(model_max)
    if declared is None or ceiling is None or declared >= ceiling:
        return []
    reason = document_output_reason(output_schema=output_schema, continuable=continuable)
    if reason is None:
        return []
    if is_mapping:
        settings[key] = ceiling
    else:
        setattr(settings, key, ceiling)
    who = f" for {label}" if label else ""
    why = {
        "array": (
            "its output schema carries an ARRAY, so the item count is decided by the "
            "input and no ceiling can be right; JSON cut mid-object does not parse, so "
            "the whole paid run is destroyed"
        ),
        "free-text": (
            "its output schema carries a FREE-FORM string, so the answer's length is a "
            "function of the input; JSON cut mid-string does not parse, so the whole "
            "paid run is destroyed"
        ),
        "prose": (
            "it writes free prose with nowhere to continue — no conversation to ask "
            "'keep going' in — so a cut is final and the reader silently loses the rest"
        ),
    }[reason]
    return [
        f"{key}{who} raised {declared} -> {ceiling} ({reason}): {why}. "
        "Raising a ceiling is free — you are billed for tokens generated, not permitted."
    ]
