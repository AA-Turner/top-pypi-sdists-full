"""Pure, dependency-free structured-output schema rules.

The recursive ``additionalProperties: false`` enforcement is the standard Matrx
baked in: Anthropic 400s without it, OpenAI strict mode requires it. It lives
here — **zero ``matrx_ai`` imports** — so BOTH the provider translators and the
standalone schema linter share ONE implementation, and the linter stays usable
without host DB configuration. Re-deriving this rule anywhere else is forbidden.
"""

from __future__ import annotations

from typing import Any


def is_object_node(node: dict[str, Any]) -> bool:
    """An object schema node: explicit ``type: object`` or property-bearing."""
    return node.get("type") == "object" or isinstance(node.get("properties"), dict)


def is_root_object(schema: dict[str, Any]) -> bool:
    """Every provider requires an object root for structured output."""
    t = schema.get("type")
    return t == "object" or (t is None and isinstance(schema.get("properties"), dict))


def enforce_additional_properties_false(node: Any) -> Any:
    """Return a copy of ``node`` with ``additionalProperties: false`` set on
    every object node, recursively. The input is never mutated — schemas may be
    shared or persisted configs."""
    if isinstance(node, dict):
        new: dict[str, Any] = {
            key: enforce_additional_properties_false(value) for key, value in node.items()
        }
        if new.get("type") == "object" or "properties" in new:
            new["additionalProperties"] = False
        return new
    if isinstance(node, list):
        return [enforce_additional_properties_false(item) for item in node]
    return node


# Validation keywords that grammar-constrained structured-output engines do NOT
# honor. They never shape the constrained-decoding grammar (type / enum /
# required / nesting / $ref do) — so removing them changes NOTHING about the
# ENFORCED output — yet several providers HARD-REJECT them. Cerebras 400s with
# ``wrong_api_format`` ("Invalid fields for schema with types ['array']:
# {'minItems', 'maxItems'}"), and every OpenAI-compatible endpoint that validates
# a restricted json_schema subset (groq / xai / together / generic-openai) fails
# the same way. This is the ``response_format`` analogue of the tool-schema strip
# in ``tools/models.py`` (``_process_nested(strip_unsupported=True)``) — SAME
# class of keyword, SAME reason, kept as one shared list so a fix lands once.
STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS: frozenset[str] = frozenset(
    {
        # array
        "minItems", "maxItems", "uniqueItems", "minContains", "maxContains",
        # string
        "minLength", "maxLength", "pattern", "format",
        # number / integer
        "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf",
        # object
        "minProperties", "maxProperties", "patternProperties", "propertyNames",
        # meta not consumed by constrained decoding
        "default", "$schema", "$comment", "contentEncoding", "contentMediaType",
    }
)

# Under these keys the child dict is a NAME → subschema map — the keys are
# user-chosen names, NOT schema keywords — so recurse the values but NEVER treat
# a name as a keyword to strip (a property literally named "pattern" must
# survive). Everywhere else a dict is itself a schema node.
_SCHEMA_NAME_MAP_KEYS: frozenset[str] = frozenset({"properties", "$defs", "definitions"})


def strip_unsupported_keywords(
    node: Any, unsupported: frozenset[str] = STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS
) -> Any:
    """Return a deep copy of ``node`` (a JSON Schema) with every keyword in
    ``unsupported`` removed at every level (inside ``$defs``, ``items``,
    ``anyOf``/``oneOf``/``allOf``, nested objects — everywhere). The input is
    never mutated (schemas may be shared or persisted configs). Property / defs
    NAMES are preserved verbatim — only schema *keywords* are stripped, so a
    property whose name happens to match a stripped keyword is left untouched."""
    if isinstance(node, list):
        return [strip_unsupported_keywords(item, unsupported) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in unsupported:
            continue
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {
                name: strip_unsupported_keywords(subschema, unsupported)
                for name, subschema in value.items()
            }
        else:
            out[key] = strip_unsupported_keywords(value, unsupported)
    return out


# Per-provider refinement of the strip. The default stays conservative for
# strict / grammar-constrained engines and OpenAI-compatible endpoints. Standard
# OpenAI models now accept several bounds in this set, while fine-tuned OpenAI
# models still reject them; until capability routing distinguishes those model
# classes, OpenAI keeps the conservative default so either route remains valid.
# Google is the one demonstrated exception: Gemini's ``response_json_schema``
# accepts minItems/maxItems/pattern verbatim (the exact shape that 400s Cerebras
# and Anthropic runs CLEAN on Gemini), so it strips NOTHING — the platform
# enforces the richest schema each provider actually supports rather than
# levelling everyone down to the strictest. Relax a provider here the moment it
# is verified to honor more.
_PROVIDER_STRUCTURED_OUTPUT_UNSUPPORTED: dict[str, frozenset[str]] = {
    "google": frozenset(),
}


def unsupported_structured_output_keywords(provider: str) -> frozenset[str]:
    """The JSON-Schema keywords a given provider's structured-output engine does
    NOT accept — pass to :func:`strip_unsupported_keywords` at that provider's
    request boundary. Defaults to the full advisory set for strict/constrained
    engines; per-provider entries relax it where a provider honors more."""
    return _PROVIDER_STRUCTURED_OUTPUT_UNSUPPORTED.get(
        provider, STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS
    )


def rewrite_const_as_enum(node: Any) -> Any:
    """Return a deep copy with every ``const: X`` rewritten to ``enum: [X]``.

    The two are semantically IDENTICAL in JSON Schema, but they are not
    equivalent to a provider's constrained decoder. Measured live against
    ``gemini-3.6-flash`` on 2026-08-11, 12 runs per cell, asking for the same
    single-valued discriminator:

        const: "topic_ideas"             ->  1/12 emitted the right value
        const + Google Search grounding  ->  0/12
        enum: ["topic_ideas"]            -> 12/12

    With ``const`` the model invents a value (``PodcastTopicIdeas``,
    ``podcast_ideas_response``, ``TopicIdeasResult``, ...). For a ``__kind``
    discriminator that is worse than emitting nothing: the frontend prefers the
    model's ``__kind`` over the caller's expected kind, so an invented value
    routes to a kind that does not exist and renders through the generic viewer.

    This is a REQUEST-BOUNDARY rewrite, deliberately NOT a change to the stored
    schema -- same doctrine as :func:`strip_unsupported_keywords` (spelled out
    in ``schema/lint.py``): the platform persists the richest, most precise
    schema and each provider's boundary massages it into what that provider
    actually honors. ``const`` stays the canonical keyword; only Gemini's
    request sees ``enum``.

    An existing ``enum`` on the same node wins and ``const`` is dropped (the two
    together are a contradiction a provider should never have to resolve).
    Property / ``$defs`` NAMES are preserved verbatim, so a property literally
    named ``const`` survives untouched.
    """
    if isinstance(node, list):
        return [rewrite_const_as_enum(item) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key == "const":
            continue  # re-emitted below, unless an explicit enum already exists
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {
                name: rewrite_const_as_enum(subschema)
                for name, subschema in value.items()
            }
        else:
            out[key] = rewrite_const_as_enum(value)
    if "const" in node and "enum" not in node:
        out["enum"] = [node["const"]]
    return out


KIND_KEY = "__kind"


def hoist_discriminator_first(node: Any, key: str = KIND_KEY) -> Any:
    """Return a deep copy in which every object node's ``properties`` map lists
    ``key`` (default ``__kind``) FIRST. The input is never mutated.

    WHY THIS EXISTS — measured live 2026-08-18 on the flashcard generator.
    A grammar-constrained model emits an object's keys in the order the
    schema's ``properties`` map declares them (proven on gemini-3.7-flash:
    swap ``properties`` order and the wire order swaps with it; swapping
    ``required`` changes nothing). So the position of the discriminator in the
    schema IS its position on the wire — and the live window cannot route a
    streaming payload until ``__kind`` has arrived.

    The platform declares ``__kind`` first everywhere. It does not SURVIVE:
    ``content_ir.kind_definition.emitted_json_schema`` is a **jsonb** column,
    and jsonb sorts object keys by (length, bytewise). The flashcard set's
    authored ``["__kind", "title", "cards"]`` came back out of the registry as
    ``["cards", "title", "__kind"]`` and the model dutifully emitted
    ``__kind`` as the LAST key of a 15-second, 10-card payload — so
    ``selectKindEnvelope`` resolved only after the run was over and the
    "cards appear one by one" preview showed a spinner for the whole run.

    Re-hoisting at the structured-output boundary fixes every kind-routed
    agent at once and needs no data migration: any jsonb round-trip anywhere
    in the platform is repaired on the way to the provider. It is a
    REQUEST-BOUNDARY normalization in the same family as
    :func:`strip_unsupported_keywords` and :func:`rewrite_const_as_enum` — the
    stored schema is left exactly as authored.

    Only the ``properties`` MAP is reordered; ``required`` and every other
    keyword are untouched (order there does not reach the decoder). Property /
    ``$defs`` names are preserved verbatim, so a property literally named
    ``$defs`` is never treated as a schema map.
    """
    if isinstance(node, list):
        return [hoist_discriminator_first(item, key) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for name, value in node.items():
        if name in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            children = {
                child: hoist_discriminator_first(subschema, key)
                for child, subschema in value.items()
            }
            if name == "properties" and key in children:
                children = {key: children[key], **{k: v for k, v in children.items() if k != key}}
            out[name] = children
        else:
            out[name] = hoist_discriminator_first(value, key)
    return out


def rewrite_oneof_as_anyof(node: Any) -> Any:
    """Return a deep copy of ``node`` with every ``oneOf`` keyword rewritten to
    ``anyOf``, recursively (property/defs NAMES preserved verbatim — only the
    schema keyword is rewritten; a node that already carries ``anyOf`` gets the
    branches merged).

    Anthropic's structured-output engine accepts ``anyOf`` but 400s on
    ``oneOf`` ("Schema type 'oneOf' is not supported" — proven live by the plan
    node recommender, whose either/or refinement killed every `recommend` call
    on an Anthropic model, 2026-08-23). The rewrite relaxes exactly-one to
    at-least-one, which is acceptable for OUTPUT GUIDANCE: the stored schema
    keeps ``oneOf`` and platform-side validation still enforces it."""
    if isinstance(node, list):
        return [rewrite_oneof_as_anyof(item) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {name: rewrite_oneof_as_anyof(sub) for name, sub in value.items()}
        elif key == "oneOf" and isinstance(value, list):
            branches = [rewrite_oneof_as_anyof(item) for item in value]
            existing = out.get("anyOf")
            out["anyOf"] = (existing + branches) if isinstance(existing, list) else branches
        elif key == "anyOf" and isinstance(value, list) and isinstance(out.get("anyOf"), list):
            out["anyOf"] = out["anyOf"] + [rewrite_oneof_as_anyof(item) for item in value]
        else:
            out[key] = rewrite_oneof_as_anyof(value)
    return out


def enforce_all_required(node: Any) -> None:
    """In place: set ``required`` to ALL property keys on every object node.
    OpenAI strict + Anthropic require every property listed in ``required``."""
    if isinstance(node, dict):
        props = node.get("properties")
        if isinstance(props, dict):
            node["required"] = list(props.keys())
            for value in props.values():
                enforce_all_required(value)
        items = node.get("items")
        if isinstance(items, dict):
            enforce_all_required(items)
        elif isinstance(items, list):
            for item in items:
                enforce_all_required(item)
        for comb in ("anyOf", "oneOf", "allOf"):
            arr = node.get(comb)
            if isinstance(arr, list):
                for item in arr:
                    enforce_all_required(item)
        defs = node.get("$defs") or node.get("definitions")
        if isinstance(defs, dict):
            for value in defs.values():
                enforce_all_required(value)


__all__ = [
    "KIND_KEY",
    "STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS",
    "enforce_additional_properties_false",
    "enforce_all_required",
    "hoist_discriminator_first",
    "is_object_node",
    "is_root_object",
    "rewrite_const_as_enum",
    "rewrite_oneof_as_anyof",
    "strip_unsupported_keywords",
    "unsupported_structured_output_keywords",
]
