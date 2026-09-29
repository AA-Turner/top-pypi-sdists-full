"""Pure, dependency-free structured-output schema rules.

🚨 WHAT "the answer is checked against the stored schema" MEANS HERE (2026-09-27).
Several rules below give a constraint up because no constrained decoder compiles
it, and say the stored schema still holds it. Until 2026-09-27 they said
"platform-side validation still enforces it" and NOTHING did: an independent
review found the package's only ``jsonschema`` uses were design-time
(``schema/lint.py``, which validates the declared SAMPLE) and tool arguments
(``tools/executor.py``), while the agent path had ``extract_json(text, schema=…)``
— a candidate SELECTOR that checks ``type`` + ``required`` at DEPTH 1 and never
raises. The check those sentences describe now exists, once, at
``matrx_ai.schema.answer_contract.verify_answer_and_record``, called by the one
dispatch seam every provider passes through. If that call is ever removed, every
sentence below becomes a lie again — they are load-bearing on it.

The recursive ``additionalProperties: false`` enforcement is the standard Matrx
baked in: Anthropic 400s without it, OpenAI strict mode requires it. It lives
here — **zero ``matrx_ai`` imports** — so BOTH the provider translators and the
standalone schema linter share ONE implementation, and the linter stays usable
without host DB configuration. Re-deriving this rule anywhere else is forbidden.
"""

from __future__ import annotations

import copy
from typing import Any


def is_object_node(node: dict[str, Any]) -> bool:
    """An object schema node: explicit ``type: object`` or property-bearing."""
    return node.get("type") == "object" or isinstance(node.get("properties"), dict)


def is_root_object(schema: dict[str, Any]) -> bool:
    """Every provider requires an object root for structured output."""
    t = schema.get("type")
    return t == "object" or (t is None and isinstance(schema.get("properties"), dict))


def _declares_object(node: dict[str, Any]) -> bool:
    """``type: "object"``, a type ARRAY that includes ``"object"`` (the nullable
    ``["object", "null"]`` form), or a property-bearing node."""
    t = node.get("type")
    return t == "object" or (isinstance(t, list) and "object" in t) or "properties" in node


def is_map_node(node: Any) -> bool:
    """A DYNAMIC-KEY object (``dict[str, X]``): its keys are data, declared only
    through ``additionalProperties`` (a schema or ``true``), with no fixed
    ``properties``. No grammar-constrained provider can express one — Anthropic
    400s ("For 'object' type, 'additionalProperties: object' is not supported")
    and OpenAI strict demands ``additionalProperties: false``."""
    if not isinstance(node, dict) or not _declares_object(node):
        return False
    extra = node.get("additionalProperties")
    return (isinstance(extra, dict) or extra is True) and not node.get("properties")


def enforce_additional_properties_false(
    node: Any, *, maps: str = "narrow", notes: list[str] | None = None, _path: str = "$"
) -> Any:
    """Return a copy of ``node`` with ``additionalProperties: false`` set on
    every object node, recursively. The input is never mutated — schemas may be
    shared or persisted configs.

    A nullable object (``"type": ["object", "null"]``) is an object node too —
    missing it is what let ``Research Setup Suggest Agent``'s ``keyword_goals``
    reach Anthropic as ``additionalProperties: {…}`` and 400 (2026-08-24).

    ``maps`` decides what happens to a DYNAMIC-KEY object (:func:`is_map_node`):

    * ``"narrow"`` (the strict providers' boundary): forced to
      ``additionalProperties: false``. That is the only shape the provider
      compiles, and it NARROWS the field to ``{}`` — every answer is still valid
      under the declared contract, but the model can no longer fill the map. It
      is never silent: the field is named in ``notes``.
    * ``"keep"`` (the platform's own portable contract, which is also what the
      answer is checked against): the map is left exactly as declared, so a
      provider that CAN express it (Gemini) keeps it, and the check keeps
      accepting a filled map.
    """
    if isinstance(node, dict):
        new: dict[str, Any] = {}
        for key, value in node.items():
            if _is_refinement_combinator(node, key):
                # Validation logic about the PARENT's properties, not a shape:
                # stamping `additionalProperties: false` onto a branch that names
                # one property makes it reject every document carrying another —
                # the plan node specialist's oneOf became unsatisfiable that way.
                new[key] = value
                continue
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                new[key] = {
                    name: enforce_additional_properties_false(
                        sub, maps=maps, notes=notes, _path=f"{_path}.{key}.{name}"
                    )
                    for name, sub in value.items()
                }
            elif key == "additionalProperties" and isinstance(value, dict):
                new[key] = enforce_additional_properties_false(
                    value, maps=maps, notes=notes, _path=f"{_path}.additionalProperties"
                )
            else:
                new[key] = enforce_additional_properties_false(
                    value, maps=maps, notes=notes, _path=f"{_path}.{key}"
                )
        if _declares_object(new):
            if is_map_node(node) and maps == "keep":
                return new
            if is_map_node(node) and notes is not None:
                notes.append(
                    f"{_path}: dynamic-key map (additionalProperties="
                    f"{'true' if node.get('additionalProperties') is True else 'schema'}) "
                    "narrowed to an empty object — the provider cannot express keys that are "
                    "data; declare the entries as an array of {key, value} objects instead"
                )
            new["additionalProperties"] = False
            if maps == "narrow" and not isinstance(new.get("properties"), dict):
                # A property-less object must SAY so: OpenAI strict ignores an
                # object with no `properties` key and then refuses its name in the
                # parent's `required` ("Extra required key 'm' supplied"),
                # measured on gpt-4o-mini 2026-09-27.
                new["properties"] = {}
                new.setdefault("required", [])
        return new
    if isinstance(node, list):
        return [
            enforce_additional_properties_false(item, maps=maps, notes=notes, _path=f"{_path}[{i}]")
            for i, item in enumerate(node)
        ]
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
        "contains", "prefixItems", "unevaluatedItems",
        # string
        "minLength", "maxLength", "pattern", "format",
        # number / integer
        "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf",
        # object
        "minProperties", "maxProperties", "patternProperties", "propertyNames",
        "dependentRequired", "dependentSchemas", "unevaluatedProperties",
        # applicators no constrained decoder compiles
        "not", "if", "then", "else",
        # meta not consumed by constrained decoding
        "default", "$schema", "$comment", "contentEncoding", "contentMediaType",
    }
)

# Under these keys the child dict is a NAME → subschema map — the keys are
# user-chosen names, NOT schema keywords — so recurse the values but NEVER treat
# a name as a keyword to strip (a property literally named "pattern" must
# survive). Everywhere else a dict is itself a schema node.
_SCHEMA_NAME_MAP_KEYS: frozenset[str] = frozenset({"properties", "$defs", "definitions"})

# Where a normalization records what it had to give up. It is stripped from the
# schema by :func:`take_normalization_notes` immediately before the send, so it
# never reaches a provider — it exists so a lossy rewrite ANNOUNCES itself.
NORMALIZATION_NOTES_KEY = "x-matrx-normalization-notes"
_NOTES_KEY = NORMALIZATION_NOTES_KEY


#: The JSON Schema EXTENSION prefix (RFC-style ``x-`` vendor keywords). A
#: constrained decoder refuses an unknown property on a schema node outright —
#: Anthropic, verbatim: ``For 'object' type, property 'x-contract-dynamic' is not
#: supported`` — and an extension is by definition not in any enumeration we could
#: keep, so it is stripped by PREFIX. Found on live schemas (``x-contract-dynamic``,
#: ``x-kind``) by probing the 50 largest of them against the real provider, 2026-09-27;
#: enumerating keywords would never have caught the next one.
STRUCTURED_OUTPUT_EXTENSION_PREFIX = "x-"


def strip_unsupported_keywords(
    node: Any, unsupported: frozenset[str] = STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS
) -> Any:
    """Return a deep copy of ``node`` (a JSON Schema) with every keyword in
    ``unsupported`` removed at every level (inside ``$defs``, ``items``,
    ``anyOf``/``oneOf``/``allOf``, nested objects — everywhere). The input is
    never mutated (schemas may be shared or persisted configs). Property / defs
    NAMES are preserved verbatim — only schema *keywords* are stripped, so a
    property whose name happens to match a stripped keyword is left untouched.

    Every ``x-`` EXTENSION keyword goes too, by prefix
    (:data:`STRUCTURED_OUTPUT_EXTENSION_PREFIX`): a constrained decoder refuses an
    unknown property on a node outright, and an extension is by definition not in
    any enumeration we could keep ahead of it."""
    if isinstance(node, list):
        return [strip_unsupported_keywords(item, unsupported) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in unsupported or key.startswith(STRUCTURED_OUTPUT_EXTENSION_PREFIX):
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
    keeps ``oneOf`` and the stored schema keeps it and the answer is CHECKED against the stored schema when the call ends (``matrx_ai.schema.answer_contract.verify_answer_and_record``, which lands an ``answer_off_contract`` finding when the answer misses it)."""
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


# The ONLY keys a grammar-constrained engine tolerates BESIDE a combinator.
# Measured live against ``claude-opus-5-5`` on 2026-09-27, one probe request per
# keyword: ``title`` / ``description`` / ``default`` / ``enum`` / ``const`` beside
# ``anyOf`` are accepted; ``type``, ``additionalProperties``, ``properties``,
# ``required``, ``discriminator`` and ``$ref`` each answer 400 by name —
# ``output_config.format.schema: For 'anyOf', '<keys>' is not supported``. The
# message always says ``anyOf`` even when the offending keyword sits beside
# ``allOf``, which is why "just drop ``discriminator``" only moved the failure.
COMBINATOR_SAFE_SIBLINGS: frozenset[str] = frozenset(
    {"anyOf", "oneOf", "title", "description", "default", "enum", "const"}
)

_COMBINATOR_KEYS: tuple[str, ...] = ("anyOf", "oneOf", "allOf")


def _resolve_local_ref(ref: Any, root: dict[str, Any]) -> dict[str, Any] | None:
    """Resolve an INTERNAL ``#/$defs/Name`` / ``#/definitions/Name`` pointer
    against ``root``. External and non-trivial pointers return ``None`` — the
    caller then treats the branch as unmergeable rather than guessing."""
    if not isinstance(ref, str) or not ref.startswith("#/"):
        return None
    cursor: Any = root
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(cursor, dict) or token not in cursor:
            return None
        cursor = cursor[token]
    return cursor if isinstance(cursor, dict) else None


def flatten_allof(node: Any, root: dict[str, Any] | None = None) -> Any:
    """Return a deep copy of ``node`` with every ``allOf`` MERGED INTO the node
    that carries it, recursively. The input is never mutated.

    WHY THIS EXISTS. Anthropic's structured-output engine rejects a combinator
    that has structural siblings, and Pydantic emits exactly that shape for a
    model whose ``json_schema_extra`` adds a cross-field constraint: the class
    keeps its own ``type`` / ``properties`` / ``required`` and gains an
    ``allOf`` carrying the extra. Four such nodes in the agent factory's own
    wire contract (``AudioMediaPart``, ``DocumentMediaPart``,
    ``ImageMediaPart``, ``VideoMediaPart``) made the whole schema answer
    ``output_config.format.schema: For 'anyOf', 'additionalProperties,
    properties, required, type' is not supported`` — the SIBLING failure that
    survived the 2026-09-27 ``discriminator`` fix. Anthropic also documents
    ``allOf`` with ``$ref`` as unsupported outright, so an ``allOf`` can never
    be passed through; it has to be resolved here.

    ``allOf`` is an intersection, so merging a branch into its parent is exact:
    ``properties`` and ``required`` are UNIONED (the parent wins a key clash,
    because the parent is the authored class and the branch is the refinement)
    and any keyword the parent does not already carry is adopted. A ``$ref``
    branch is inlined from ``root`` first.

    A branch that CANNOT be merged — it carries a combinator of its own, so
    merging would create the very illegal shape this function exists to remove —
    is dropped, and the drop is reported through the returned
    :func:`combinator_normalization_notes` channel so nothing fails silently.
    That is the same doctrine as :func:`strip_unsupported_keywords`: the stored
    schema keeps the refinement and the stored schema keeps it and the answer is CHECKED against the stored schema when the call ends (``matrx_ai.schema.answer_contract.verify_answer_and_record``, which lands an ``answer_off_contract`` finding when the answer misses it);
    only the provider's copy is reduced to what its decoder compiles.
    """
    if root is None and isinstance(node, dict):
        root = node
    if isinstance(node, list):
        return [flatten_allof(item, root) for item in node]
    if not isinstance(node, dict):
        return node

    out: dict[str, Any] = {}
    for key, value in node.items():
        if key == "allOf":
            continue
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {name: flatten_allof(sub, root) for name, sub in value.items()}
        else:
            out[key] = flatten_allof(value, root)

    branches = node.get("allOf")
    if not isinstance(branches, list):
        return out

    dropped: list[dict[str, Any]] = []
    for branch in branches:
        if not isinstance(branch, dict):
            continue
        if set(branch) == {"$ref"}:
            resolved = _resolve_local_ref(branch["$ref"], root or {})
            branch = resolved if isinstance(resolved, dict) else branch
        if any(key in branch for key in _COMBINATOR_KEYS) or "$ref" in branch:
            dropped.append(branch)
            continue
        merged = flatten_allof(branch, root)
        for key, value in merged.items():
            if key in ("properties", "$defs", "definitions") and isinstance(value, dict):
                existing = out.get(key)
                out[key] = {**value, **existing} if isinstance(existing, dict) else dict(value)
            elif key == "required" and isinstance(value, list):
                existing = out.get("required")
                base = list(existing) if isinstance(existing, list) else []
                out["required"] = base + [item for item in value if item not in base]
            elif key not in out:
                out[key] = value
    if dropped:
        out.setdefault(_NOTES_KEY, []).extend(
            f"allOf branch dropped (carries its own combinator or $ref, which cannot "
            f"be merged into a parent that already has structure): {sorted(branch)}"
            for branch in dropped
        )
    return out


def normalize_combinator_siblings(node: Any) -> Any:
    """Return a deep copy of ``node`` in which no combinator has a sibling the
    provider rejects, recursively. Property and ``$defs`` NAMES are preserved
    verbatim — a property literally named ``discriminator`` or ``type`` is
    untouched, because only schema KEYWORDS are normalised.

    This is the general form of the rule the 2026-09-27 ``discriminator`` fix
    got one instance of. Everything outside :data:`COMBINATOR_SAFE_SIBLINGS` is
    removed from a node that carries ``anyOf`` / ``oneOf``:

    * ``discriminator`` is pure OpenAPI routing metadata — ``anyOf`` alone
      validates the same documents, so it is dropped outright.
    * ``type`` beside a union is redundant: every branch declares its own.
    * ``properties`` / ``required`` / ``additionalProperties`` / ``items`` are
      DISTRIBUTED into every branch that can hold them (an ``anyOf`` with an
      outer constraint means "one of these, AND this", which the branches can
      express) and dropped from the union node itself. A branch that cannot hold
      them — a ``$ref``, a scalar, a nested union — is left alone, and the drop
      is recorded in the notes channel.

    The stored schema is untouched; this is a REQUEST-BOUNDARY normalization in
    the same family as :func:`rewrite_oneof_as_anyof`.
    """
    if isinstance(node, list):
        return [normalize_combinator_siblings(item) for item in node]
    if not isinstance(node, dict):
        return node

    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {name: normalize_combinator_siblings(sub) for name, sub in value.items()}
        else:
            out[key] = normalize_combinator_siblings(value)

    if not any(isinstance(out.get(key), list) for key in ("anyOf", "oneOf")):
        return out

    offending = [
        key
        for key in out
        if key not in COMBINATOR_SAFE_SIBLINGS and key != _NOTES_KEY
    ]
    if not offending:
        return out

    distributable = {
        key: out[key]
        for key in ("properties", "required", "additionalProperties", "items")
        if key in offending
    }
    notes: list[str] = []
    for key in offending:
        out.pop(key, None)
    if distributable:
        placed = False
        for combinator in ("anyOf", "oneOf"):
            branches = out.get(combinator)
            if not isinstance(branches, list):
                continue
            new_branches = []
            for branch in branches:
                if (
                    isinstance(branch, dict)
                    and "$ref" not in branch
                    and not any(k in branch for k in _COMBINATOR_KEYS)
                ):
                    merged = dict(branch)
                    for key, value in distributable.items():
                        if key == "properties" and isinstance(value, dict):
                            existing = merged.get("properties")
                            merged["properties"] = (
                                {**value, **existing} if isinstance(existing, dict) else dict(value)
                            )
                        elif key == "required" and isinstance(value, list):
                            existing = merged.get("required")
                            base = list(existing) if isinstance(existing, list) else []
                            merged["required"] = base + [i for i in value if i not in base]
                        else:
                            merged.setdefault(key, value)
                    new_branches.append(merged)
                    placed = True
                else:
                    new_branches.append(branch)
            out[combinator] = new_branches
        if not placed:
            notes.append(
                "union constraints "
                f"{sorted(distributable)} dropped: no branch could hold them "
                "(every branch is a $ref, a scalar or a nested union)"
            )
    dropped_only = sorted(set(offending) - set(distributable))
    if dropped_only:
        notes.append(f"union siblings dropped (provider rejects them beside a union): {dropped_only}")
    if notes:
        out.setdefault(_NOTES_KEY, []).extend(notes)
    return out


def split_enum_from_type_union(node: Any) -> Any:
    """Return a copy in which no ``enum`` sits beside a type ARRAY — the union
    becomes ``anyOf`` branches instead. The input is never mutated.

    Anthropic refuses an enum beside a type array OUTRIGHT, measured live
    2026-09-27 on ``claude-sonnet-5`` and quoted verbatim:

        ``{"type": ["string","null"], "enum": ["a","b", null]}``
            -> ``Invalid schema: Enum value 'a' does not match declared type
               '['string', 'null']'``
        ``{"type": ["string","null"], "enum": ["a","b"]}``  (no null in the enum)
            -> the SAME refusal, so it is the type ARRAY it objects to, not the
               null member
        ``{"anyOf": [{"type":"string","enum":["a","b"]}, {"type":"null"}]}``
            -> **200**

    This is not a shape only this boundary creates. ``Optional[SomeEnum]`` in
    Pydantic emits exactly ``{"type": ["string","null"], "enum": [...]}``, so every
    live contract with a nullable enum has been refused by Anthropic all along —
    ``research_page_analysis`` (``page_type``, ``analysis_status``,
    ``recommended_use``) is one. Fixing it where the shape is translated fixes the
    class for anything that can produce it.

    LOSSLESS: the branches admit exactly the same documents the union did. The
    rewritten node still counts as ONE union parameter
    (:func:`is_union_param` reads ``anyOf`` and a type array alike), so the
    provider's 16-parameter budget is unaffected, and
    :func:`collapse_nullable_unions` narrows the ``anyOf`` form as readily as the
    type-array form.
    """
    if isinstance(node, list):
        return [split_enum_from_type_union(item) for item in node]
    if not isinstance(node, dict):
        return node

    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {name: split_enum_from_type_union(sub) for name, sub in value.items()}
        elif key in ("enum", "const", "required", _NOTES_KEY):
            out[key] = value
        else:
            out[key] = split_enum_from_type_union(value)

    types = out.get("type")
    enum = out.get("enum")
    if not (isinstance(enum, list) and enum):
        return out
    if isinstance(types, str) and types != "null" and None in enum:
        # SIBLING (2026-09-28): a null MEMBER beside a scalar type. ``type:
        # "string"`` already refuses null, so that member admits nothing and the
        # validator names it ("Enum value None does not match declared type").
        # Dropping it is the identical constraint; widening to null instead would
        # let the model answer a value the author's own schema then refuses.
        values = [v for v in enum if v is not None]
        if not values:
            return {k: v for k, v in out.items() if k != "enum"} | {"type": "null"}
        return {**out, "enum": values}
    if not isinstance(types, list):
        return out

    concrete = [t for t in types if t != "null"]
    nullable = "null" in types or None in enum
    values = [v for v in enum if v is not None]
    if not concrete or not values:
        # Nothing but null left to say — the enum carried no real value.
        return {k: v for k, v in out.items() if k != "enum"} | {"type": "null"}

    # Annotations stay on the union; EVERY other keyword (minLength, format, …)
    # travels on the value branch, so nothing the author constrained is lost —
    # and the enum is NOT repeated beside the union: carrying the original
    # null-bearing enum up there kept the very member the validator names.
    annotations = {k: v for k, v in out.items() if k in _NULLABLE_ANNOTATION_KEYS}
    branch: dict[str, Any] = {
        k: v for k, v in out.items() if k not in _NULLABLE_ANNOTATION_KEYS
    }
    branch["type"] = concrete[0] if len(concrete) == 1 else concrete
    branch["enum"] = values
    if not nullable:
        # A multi-type enum with no null: the type array is still the problem.
        return {**annotations, **branch}
    return {**annotations, "anyOf": [branch, {"type": "null"}]}


#: What stays on the union node when a nullable value is split into ``anyOf``
#: branches — annotations only; the value's constraints belong to its branch.
_NULLABLE_ANNOTATION_KEYS: frozenset[str] = frozenset({"title", "description", "default"})


def nullable_enum_violations(node: Any, path: str = "#") -> list[str]:
    """Every node where an ``enum``/``const`` sits beside a type ARRAY, or holds a
    ``null`` member its scalar ``type`` refuses — the shapes Anthropic rejects
    ("Enum value 'victim' does not match declared type '['string', 'null']'",
    live 2026-09-28) and :func:`split_enum_from_type_union` rewrites. Paths are
    JSON-pointer style, rooted at ``path``."""
    found: list[str] = []
    if isinstance(node, list):
        for index, item in enumerate(node):
            found.extend(nullable_enum_violations(item, f"{path}/{index}"))
        return found
    if not isinstance(node, dict):
        return found
    types = node.get("type")
    members = node.get("enum") if isinstance(node.get("enum"), list) else None
    if members is None and "const" in node:
        members = [node["const"]]
    if members:
        if isinstance(types, list) or (
            isinstance(types, str) and types != "null" and None in members
        ):
            found.append(path)
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            for name, sub in value.items():
                found.extend(nullable_enum_violations(sub, f"{path}/{key}/{name}"))
        elif key not in ("enum", "const", "required", _NOTES_KEY):
            found.extend(nullable_enum_violations(value, f"{path}/{key}"))
    return found


#: What an ``items`` the author left UNSPECIFIED becomes at a provider that refuses
#: the empty schema: the widest shape a strict decoder compiles without recursion
#: — every JSON scalar and null. An object or array element cannot be expressed
#: openly there (a strict object must name its properties), so this is still a
#: NARROWING and is recorded as one; it is simply the smallest one available,
#: where ``{"type": "string"}`` used to throw away numbers, booleans and null too.
#: Measured live 2026-09-28 (SCHEMA-TRANSLATION.md §15): accepted by OpenAI strict
#: and by Anthropic on every live wire that carries an unspecified array item.
OPEN_SCALAR_ITEM_SCHEMA: dict[str, Any] = {
    "anyOf": [
        {"type": "string"},
        {"type": "number"},
        {"type": "boolean"},
        {"type": "null"},
    ]
}


_ARRAY_ONLY_KEYS: frozenset[str] = frozenset(
    {"minItems", "maxItems", "uniqueItems", "contains", "minContains", "maxContains"}
)


def _includes_array(node: dict[str, Any]) -> bool:
    kind = node.get("type")
    return kind == "array" or (isinstance(kind, list) and "array" in kind)


def make_array_items_explicit(node: Any) -> Any:
    """Return a deep copy in which every node that admits an ARRAY and names no
    item schema says so explicitly: ``items: {}``.

    Lossless — in JSON Schema an absent ``items`` and ``items: {}`` admit exactly
    the same documents (any element) — which is why it can run in the step every
    provider shares. It exists because the absence is not portable: OpenAI strict
    refuses it by name (``array schema missing items``, 5 live kind contracts
    refused on 2026-09-28, the ``__kind`` fix having already cleared their other
    refusal), while the permissive providers accept the explicit ``{}``. Once the
    element schema is EXPLICIT, each provider's own rules decide what it becomes:
    the permissive ones keep ``{}`` (nothing given up); the strict ones replace it
    through :func:`concretize_empty_schemas` with their widest accepted shape and
    record that narrowing, naming the unspecified item type.

    Adds no notes on purpose: this runs before every translator, including Google,
    whose pipeline does not strip normalization notes, and it gives nothing up.
    """
    if isinstance(node, list):
        return [make_array_items_explicit(item) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {name: make_array_items_explicit(sub) for name, sub in value.items()}
        elif key in ("enum", "const", "required"):
            out[key] = value
        else:
            out[key] = make_array_items_explicit(value)
    if not _includes_array(out) or "items" in out or "prefixItems" in out:
        return out
    kind = out.get("type")
    if kind == "array" or kind == ["array"]:
        out["items"] = {}
        return out
    if any(k in out for k in ("anyOf", "oneOf", "allOf", "$ref")):
        # Not a live shape (census 2026-09-28: 0 of 133); a combinator here would
        # need a merge this rule does not own. Say it explicitly and leave it.
        out["items"] = {}
        return out
    # A type LIST that also admits an array (`["string", ..., "array", "null"]`,
    # a bare `Any` spelled out): `items` beside it is read by a strict provider as
    # a keyword of EVERY listed type — Anthropic, live: "For 'object' type,
    # property 'items' is not supported". The same documents, split so the item
    # schema belongs to the array alone: the array branch takes the array-only
    # keywords, the other branch the rest, and annotations stay on the parent.
    others = [t for t in kind if t != "array"]
    array_branch: dict[str, Any] = {"type": "array", "items": {}}
    other_branch: dict[str, Any] = {"type": others[0] if len(others) == 1 else others}
    parent: dict[str, Any] = {}
    for key, value in out.items():
        if key == "type":
            continue
        if key in _ANNOTATION_ONLY_KEYS:
            parent[key] = value
        elif key in _ARRAY_ONLY_KEYS:
            array_branch[key] = value
        else:
            other_branch[key] = value
    return {**parent, "anyOf": [other_branch, array_branch]}


def concretize_empty_schemas(
    node: Any,
    placeholder_type: str = "string",
    *,
    item_placeholder: dict[str, Any] | None = None,
    _is_item: bool = False,
) -> Any:
    """Return a deep copy in which no subschema is the EMPTY schema.

    ``output_config.format.schema: Empty schema ({}) that accepts any JSON value
    is not supported. Please specify a concrete type.`` — and Pydantic emits
    ``{}`` for every bare ``Any`` field, so one ``Any`` anywhere in a contract
    makes the whole request unsendable. A node with nothing but annotations
    (``title`` / ``description``) is the same thing to the validator.

    There is no way to say "any JSON value" in the accepted subset, so this is a
    genuine NARROWING, not a lossless rewrite: the field becomes
    ``placeholder_type``. It is recorded in the notes channel so the caller
    announces it rather than shipping a silently different contract.
    """
    if isinstance(node, list):
        return [
            concretize_empty_schemas(item, placeholder_type, item_placeholder=item_placeholder)
            for item in node
        ]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {
                name: concretize_empty_schemas(
                    sub, placeholder_type, item_placeholder=item_placeholder
                )
                for name, sub in value.items()
            }
        else:
            out[key] = concretize_empty_schemas(
                value,
                placeholder_type,
                item_placeholder=item_placeholder,
                _is_item=key == "items" and isinstance(value, dict),
            )
    shaping = {k for k in out if k not in ("title", "description", _NOTES_KEY)}
    if not shaping and _is_item:
        # The author said "an array" and never said of WHAT. The provider refuses
        # an element schema that accepts any JSON value, so the element becomes
        # the widest shape it does compile — named, never silent.
        placeholder = copy.deepcopy(item_placeholder) if item_placeholder else {
            "type": placeholder_type
        }
        described = (
            "any JSON scalar or null"
            if placeholder == OPEN_SCALAR_ITEM_SCHEMA
            else f"type={placeholder.get('type')!r}"
        )
        out.update(placeholder)
        out.setdefault(_NOTES_KEY, []).append(
            "array item type left UNSPECIFIED by the author — the element schema was "
            f"narrowed to {described}: the provider rejects an item schema that accepts "
            "any JSON value, so an object or array element can no longer be answered here"
        )
        return out
    if not shaping:
        out["type"] = placeholder_type
        out.setdefault(_NOTES_KEY, []).append(
            "empty schema ({} — a bare `Any`) narrowed to "
            f"type={placeholder_type!r}: the provider rejects a schema that accepts any JSON value"
        )
    return out


def normalize_array_items(node: Any) -> Any:
    """Return a deep copy in which no ``items`` is a LIST.

    ``Invalid schema: Array types must be specified with a single object schema
    for 'items'.`` Draft-4 tuple validation (``items: [A, B]``) is the shape
    ``tuple[...]`` produces; the accepted subset takes one schema, so the first
    entry is kept and the narrowing is recorded."""
    if isinstance(node, list):
        return [normalize_array_items(item) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {name: normalize_array_items(sub) for name, sub in value.items()}
        elif key == "items" and isinstance(value, list):
            kept = next((v for v in value if isinstance(v, dict)), {"type": "string"})
            out["items"] = normalize_array_items(kept)
            out.setdefault(_NOTES_KEY, []).append(
                f"tuple `items` ({len(value)} positional schemas) reduced to the first: "
                "the provider takes a single schema for `items`"
            )
        else:
            out[key] = normalize_array_items(value)
    return out


# Keys a "refinement-only" combinator branch may carry: constraints on the
# PARENT's properties, never a shape of its own. Pydantic / hand-written schemas
# use this for "either the list is non-empty, or gap_description is set" rules
# (the plan node specialist, 2026-08-23).
_REFINEMENT_KEYS: frozenset[str] = frozenset(
    {"properties", "required", "title", "description", "not", "dependentRequired"}
    | STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS
)
_SHAPE_KEYS: frozenset[str] = frozenset(
    {"type", "$ref", "enum", "const", "items", "anyOf", "oneOf", "allOf", "additionalProperties"}
)


def _is_refinement_branch(branch: Any) -> bool:
    """A combinator branch that only REFINES its parent: no type of its own, and
    every property it names is itself constraint-only (``{"minItems": 1}``)."""
    if not isinstance(branch, dict):
        return False
    if not branch:
        return True  # a branch whose constraints were all stripped refines nothing
    # `additionalProperties: false` (and a `required` list) are what the portable
    # step stamps onto every property-bearing node — the branch included — so
    # they do not make a refinement into a shape.
    keys = set(branch) - ({"additionalProperties"} if branch.get("additionalProperties") is False else set())
    if keys - _REFINEMENT_KEYS or _SHAPE_KEYS & keys:
        return False
    props = branch.get("properties")
    if props is None:
        return True
    return isinstance(props, dict) and all(
        isinstance(sub, dict) and not (_SHAPE_KEYS | {"properties"}) & set(sub)
        for sub in props.values()
    )


def _is_refinement_combinator(node: dict[str, Any], key: str) -> bool:
    """``node[key]`` is a oneOf/anyOf/allOf whose every branch only refines a
    parent that has structure of its own (see :func:`_is_refinement_branch`)."""
    if key not in ("oneOf", "anyOf", "allOf"):
        return False
    branches = node.get(key)
    has_shape = "type" in node or isinstance(node.get("properties"), dict)
    return (
        has_shape
        and isinstance(branches, list)
        and bool(branches)
        and all(_is_refinement_branch(b) for b in branches)
    )


def drop_refinement_combinators(node: Any, notes: list[str] | None = None, _path: str = "$") -> Any:
    """Return a copy in which a ``oneOf`` / ``anyOf`` / ``allOf`` whose EVERY
    branch only refines the parent (see :func:`_is_refinement_branch`) is removed
    from a node that carries its own structure.

    Such a combinator is validation logic, not shape: ``{"type": "object",
    "properties": {...}, "oneOf": [{"properties": {"recommendations":
    {"minItems": 1}}}, {"required": ["gap_description"]}]}``. No constrained
    decoder compiles it — Anthropic answered "Schema type 'oneOf' is not
    supported", and after the generic union normalisation it answered "Schema
    type is missing", because distributing the parent into constraint-only
    branches manufactures type-less objects. The parent's structure is exact on
    its own; the refinement is RELAXED (named in ``notes``) and the platform's
    own check of the answer against the stored contract catches a branch the
    model actually violated (``schema.answer_contract``).
    """
    if isinstance(node, list):
        return [drop_refinement_combinators(item, notes, f"{_path}[{i}]") for i, item in enumerate(node)]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {
                name: drop_refinement_combinators(sub, notes, f"{_path}.{key}.{name}")
                for name, sub in value.items()
            }
        else:
            out[key] = drop_refinement_combinators(value, notes, f"{_path}.{key}")
    has_shape = "type" in out or isinstance(out.get("properties"), dict)
    if has_shape:
        for combinator in ("oneOf", "anyOf", "allOf"):
            branches = out.get(combinator)
            if isinstance(branches, list) and branches and all(
                _is_refinement_branch(b) for b in branches
            ):
                out.pop(combinator)
                if notes is not None:
                    notes.append(
                        f"{_path}: `{combinator}` of {len(branches)} refinement-only branches "
                        "RELAXED (validation logic, not shape — no constrained decoder "
                        "compiles it; the stored schema keeps it and the answer is checked "
                        "against the stored schema when the call ends)"
                    )
    return out


def ref_cycles(schema: Any) -> list[list[str]]:
    """Public alias of the cycle finder — every self/mutually-referencing
    ``$defs`` entry as a name cycle."""
    return _ref_cycles(schema)


def unroll_recursive_refs(
    schema: Any, depth: int = 4, notes: list[str] | None = None
) -> Any:
    """Return a copy of ``schema`` in which every recursive ``$defs`` reference is
    UNROLLED to ``depth`` levels, so no definition refers to itself.

    Anthropic refuses a recursive schema outright ("Circular reference detected
    in schema definitions: MapTopicNode -> MapTopicNode", the topical map author,
    2026-09-17) and so did every run bound to it. A tree of bounded depth is the
    closest shape it compiles: level ``k`` is a copy of the definition whose
    recursive references point at level ``k+1``. At the LAST level a recursive
    reference becomes ``{"type": "null"}`` — the property stays (so every node
    still carries its declared keys) but can hold nothing: ``children`` at the
    deepest level can only be ``[]``. Up to ``depth`` levels the tree is enforced
    exactly; a deeper tree cannot be expressed, which is a RELAXATION named in
    ``notes`` (measured live 2026-09-27: removing the property instead made
    every deepest node miss a required key, so the answer failed validation).
    OpenAI and Gemini accept recursion and never call this.
    """
    if not isinstance(schema, dict):
        return schema
    defs_key = "$defs" if isinstance(schema.get("$defs"), dict) else (
        "definitions" if isinstance(schema.get("definitions"), dict) else None
    )
    cycles = _ref_cycles(schema)
    if defs_key is None or not cycles:
        return schema
    recursive = {name for cycle in cycles for name in cycle}
    defs: dict[str, Any] = schema[defs_key]
    prefix = f"#/{defs_key}/"

    def target(ref: Any) -> str | None:
        if isinstance(ref, str) and ref.startswith(prefix):
            name = ref[len(prefix):]
            return name if name in recursive else None
        return None

    def level_name(name: str, level: int) -> str:
        return name if level == 0 else f"{name}__L{level}"

    def rewrite(node: Any, level: int) -> Any:
        if isinstance(node, list):
            return [rewrite(item, level) for item in node]
        if not isinstance(node, dict):
            return node
        name = target(node.get("$ref"))
        if name is not None:
            if level + 1 >= depth:
                return {"type": "null"}
            return {**node, "$ref": prefix + level_name(name, level + 1)}
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                out[key] = {child: rewrite(sub, level) for child, sub in value.items()}
            elif key in ("anyOf", "oneOf") and isinstance(value, list):
                branches: list[Any] = []
                for branch in (rewrite(b, level) for b in value):
                    if branch not in branches:  # a cut ref + an existing null branch
                        branches.append(branch)
                out[key] = branches
            elif key in ("enum", "const", "required"):
                out[key] = value
            else:
                out[key] = rewrite(value, level)
        return out

    new_defs: dict[str, Any] = {}
    for name, body in defs.items():
        if name not in recursive:
            new_defs[name] = rewrite(body, 0)
            continue
        for level in range(depth):
            new_defs[level_name(name, level)] = rewrite(body, level)
    out = {k: v for k, v in schema.items() if k != defs_key}
    # The root is ABOVE level 0: its references point at level 0 itself.
    out = rewrite(out, -1)
    out[defs_key] = new_defs
    if notes is not None:
        cycles_txt = "; ".join(" -> ".join(c) for c in cycles)
        notes.append(
            f"recursive definitions ({cycles_txt}) unrolled to {depth} levels — the provider "
            f"refuses recursion; a tree deeper than {depth} levels cannot be expressed (the "
            "recursive field of the deepest level can only be empty)"
        )
    return out


def ref_cycle_members(schema: Any) -> set[str]:
    """Every ``$defs`` entry that takes part in a ``$ref`` cycle."""
    return {name for cycle in _ref_cycles(schema) for name in cycle}


def _references_any(node: Any, names: set[str]) -> bool:
    """Does this subtree ``$ref`` one of ``names`` (at any depth)?"""
    if isinstance(node, list):
        return any(_references_any(item, names) for item in node)
    if not isinstance(node, dict):
        return False
    ref = node.get("$ref")
    if isinstance(ref, str) and ref.rsplit("/", 1)[-1] in names:
        return True
    return any(
        _references_any(value, names) for key, value in node.items() if key not in ("$ref", "enum", "const")
    )


def express_nullable_as_anyof(node: dict[str, Any]) -> dict[str, Any]:
    """``{"type": ["T","null"], …}`` → ``{"anyOf": [{"type":"T", …}, {"type":"null"}]}``.

    Same documents, different spelling. Gemini's ref-loop check recognises the
    ``anyOf`` spelling as nullable and the type-ARRAY spelling as NOT nullable
    (measured live, see :func:`open_ref_loops`), so the spelling is the whole fix.
    """
    types = node.get("type")
    if not (isinstance(types, list) and "null" in types):
        return dict(node)
    concrete = [t for t in types if t != "null"]
    if not concrete:
        return dict(node)
    # enum/const belong to the value branch ONLY — carrying them beside the union
    # too repeated the null-bearing enum the validator refuses.
    carried = {
        k: v
        for k, v in node.items()
        if k in COMBINATOR_SAFE_SIBLINGS and k not in ("enum", "const")
    }
    branch = {
        k: v
        for k, v in node.items()
        if k not in COMBINATOR_SAFE_SIBLINGS or k in ("enum", "const")
    }
    if isinstance(branch.get("enum"), list):
        branch["enum"] = [v for v in branch["enum"] if v is not None]
    branch["type"] = concrete[0] if len(concrete) == 1 else concrete
    return {**carried, "anyOf": [branch, {"type": "null"}]}


#: Keywords that stop an array from being POTENTIALLY ZERO-LENGTH, which is one of
#: the three escapes Gemini's ref-loop rule accepts.
_MIN_LENGTH_KEYS: tuple[str, ...] = ("minItems", "minContains")


def open_ref_loops(
    schema: Any, *, narrowed: list[str] | None = None, relaxed: list[str] | None = None
) -> Any:
    """Make every ``$ref`` cycle expressible, for a provider that accepts a cycle
    only when the loop can TERMINATE. The input is never mutated.

    Gemini states the rule in its own refusal, verbatim:

        ``ref loops are only supported if they include optional or nullable
        property values, or a potentially-zero-length array items, but a ref loop
        of required fields was found at $defs.MapTopicNode.properties.children.items``

    Measured live on ``gemini-3.8-flash``, 2026-09-27, one request per form —
    because "nullable" does not mean what it looks like:

    | loop-carrying property | Gemini |
    |---|---|
    | required + plain array (no ``minItems``) | **200** |
    | required + ``type: ["array","null"]``    | **400** |
    | required + ``anyOf: [array, null]``      | **200** |
    | optional (out of ``required``)           | **200** |
    | required + array with ``minItems: 1``    | **400** |
    | unrolled, no cycle at all                | **200** |

    So a type-ARRAY nullable does NOT satisfy it and an `anyOf` nullable does.
    That is why ``seo.map_author``'s topic map was refused: the author left
    ``children`` optional — which Gemini accepts — and the platform's own portable
    step listed every property in ``required``, closing the only escape the cycle
    had. **Our transformation created the refusal**, which under Arman's ruling of
    2026-09-27 makes it our translator's bug, not a rule of Gemini's and not
    something the kind's author has to work around.

    The ladder, most faithful first:

    1. a loop carrier that is nullable as a type ARRAY is re-spelled as ``anyOf``
       — lossless, nothing but the spelling changes;
    2. a loop carrier that is an ARRAY has its minimum-length floor removed so the
       recursion can terminate — a RELAXATION, named in ``relaxed``;
    3. a loop that still cannot terminate is UNROLLED to a bounded depth by
       :func:`unroll_recursive_refs` — a NARROWING, named in ``narrowed``. A
       required, non-nullable, non-array self-reference describes an INFINITE
       document that no answer could ever satisfy, so a bounded reading is the
       only expressible one.
    """
    if not isinstance(schema, dict):
        return schema
    members = ref_cycle_members(schema)
    if not members:
        return schema

    def walk(node: Any, path: str) -> Any:
        if isinstance(node, list):
            return [walk(item, f"{path}[{index}]") for index, item in enumerate(node)]
        if not isinstance(node, dict):
            return node
        out: dict[str, Any] = {}
        released: set[str] = set()
        for key, value in node.items():
            if key == "properties" and isinstance(value, dict):
                required = set(node.get("required") or ())
                props: dict[str, Any] = {}
                for name, sub in value.items():
                    where = f"{path}.{name}"
                    if isinstance(sub, dict) and name in required and _references_any(sub, members):
                        sub = _open_carrier(sub, where)
                        if _is_anyof_nullable(sub) and not _array_escape(sub):
                            # (3) An OBJECT loop carrier escapes only by being
                            # optional — `anyOf: [{$ref}, null]` does NOT satisfy
                            # the provider (measured 2026-09-28, gemini-3.8-flash:
                            # required + anyOf-nullable ref 400, optional 200,
                            # both through `#` and through `$defs`). The author's
                            # schema almost always left it optional — the portable
                            # step listed it — so releasing it restores the
                            # author's shape; the nullable spelling stays. A
                            # REQUIRED, NON-nullable carrier is the author's own
                            # infinite document and is unrolled below instead.
                            released.add(name)
                            if relaxed is not None:
                                relaxed.append(
                                    f"{where}: listed as optional again so the $ref cycle "
                                    "through it can terminate — the provider accepts a cycle "
                                    "only through an optional property or a potentially-"
                                    "zero-length array (nullable is not enough)"
                                )
                    props[name] = walk(sub, where)
                out[key] = props
            elif key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                out[key] = {n: walk(s, f"{path}.{key}.{n}") for n, s in value.items()}
            elif key in ("required", "enum", "const", _NOTES_KEY):
                out[key] = value
            else:
                out[key] = walk(value, f"{path}.{key}")
        if released and isinstance(out.get("required"), list):
            out["required"] = [name for name in out["required"] if name not in released]
        return out

    def _open_carrier(sub: dict[str, Any], where: str) -> dict[str, Any]:
        # (1) re-spell a type-ARRAY nullable as anyOf — lossless.
        if isinstance(sub.get("type"), list) and "null" in sub["type"]:
            return express_nullable_as_anyof(sub)
        if _is_anyof_nullable(sub):
            return sub  # already the spelling the provider recognises
        # (2) an array only has to be able to be EMPTY.
        types = sub.get("type")
        is_array = types == "array" or (isinstance(types, list) and "array" in types)
        if is_array:
            floors = [key for key in _MIN_LENGTH_KEYS if key in sub]
            if floors:
                if relaxed is not None:
                    relaxed.append(
                        f"{where}: {', '.join(floors)} dropped so the $ref cycle through this "
                        "array can terminate — the provider accepts a cycle only through a "
                        "potentially-zero-length array"
                    )
                return {k: v for k, v in sub.items() if k not in _MIN_LENGTH_KEYS}
            return sub
        return sub

    opened = walk(schema, "$")
    # (3) whatever still cannot terminate gets a bounded depth instead of a cycle.
    if gemini_ref_loop_violations(opened):
        notes: list[str] = []
        opened = unroll_recursive_refs(opened, depth=4, notes=notes)
        if narrowed is not None:
            narrowed.extend(notes)
            narrowed.append(
                "a $ref cycle with no optional, nullable or zero-length-able property to "
                "terminate on was unrolled to 4 levels — the provider cannot express an "
                "unbounded cycle, and a required non-nullable self-reference describes an "
                "infinite document no answer could satisfy"
            )
    return opened


def _is_anyof_nullable(node: Any) -> bool:
    """Nullable spelled ``anyOf`` with a ``{"type": "null"}`` branch.

    NOT, on its own, an escape for a cycle: measured 2026-09-28 on
    ``gemini-3.8-flash``, a REQUIRED ``anyOf: [{$ref}, null]`` carrier is refused
    ("a ref loop of required fields was found at properties.no.anyOf.0"); the
    2026-09-27 measurement that looked like a nullable escape was an ARRAY branch,
    which escapes by being able to be empty (:func:`_array_escape`).
    Original note: nullable in the ONE spelling the provider's cycle check recognises:
    ``anyOf`` with a ``{"type": "null"}`` branch. A type ARRAY carrying ``"null"``
    is NOT recognised (measured live on ``gemini-3.8-flash``, 2026-09-27)."""
    if not isinstance(node, dict):
        return False
    branches = node.get("anyOf")
    return isinstance(branches, list) and any(
        isinstance(b, dict) and b.get("type") == "null" for b in branches
    )


def _array_escape(node: Any) -> bool:
    """Can a cycle through ``node`` stop because it is an array that may be
    EMPTY? A plain array with no minimum length, or an ``anyOf`` with such an
    array branch (required + ``anyOf: [array, null]`` measured 200)."""
    if not isinstance(node, dict):
        return False
    if node.get("type") == "array" and not any(key in node for key in _MIN_LENGTH_KEYS):
        return True
    branches = node.get("anyOf")
    return isinstance(branches, list) and any(_array_escape(b) for b in branches)


ROOT_DEF_NAME = "__root__"


def hoist_root_recursion(schema: Any) -> Any:
    """``{"$ref": "#"}`` — a schema that recurses through its own ROOT — rewritten
    as the same cycle through a ``$defs`` entry. LOSSLESS: the root keeps its
    body and every ``#`` pointer names an identical copy of it.

    Every cycle rule here reads cycles between ``$defs`` entries, so a root
    self-reference was invisible to all of them: the live ``decision_node`` and
    ``decision_tree`` kinds (``yes``/``no`` → ``#``) went to Gemini with their
    required recursion untouched and were refused on every call
    (SCHEMA-TRANSLATION-VERIFY.md, R7).
    """
    if not isinstance(schema, dict):
        return schema

    def has_root_ref(node: Any) -> bool:
        if isinstance(node, list):
            return any(has_root_ref(item) for item in node)
        if not isinstance(node, dict):
            return False
        if node.get("$ref") == "#":
            return True
        return any(has_root_ref(v) for k, v in node.items() if k not in ("enum", "const"))

    if not has_root_ref(schema):
        return schema
    pointer = f"#/$defs/{ROOT_DEF_NAME}"

    def repoint(node: Any) -> Any:
        if isinstance(node, list):
            return [repoint(item) for item in node]
        if not isinstance(node, dict):
            return node
        return {
            key: (pointer if key == "$ref" and value == "#" else repoint(value))
            for key, value in node.items()
        }

    repointed = repoint(schema)
    body = {k: v for k, v in repointed.items() if k not in ("$defs", "definitions")}
    defs = dict(repointed.get("$defs") or {})
    defs[ROOT_DEF_NAME] = copy.deepcopy(body)
    out = dict(repointed)
    out["$defs"] = defs
    return out


def gemini_ref_loop_violations(schema: Any) -> list[str]:
    """Every ``$ref`` cycle in ``schema`` that the provider will refuse because the
    loop cannot terminate — the forcing function for :func:`open_ref_loops`.

    A cycle is expressible when EVERY path around it passes through at least one
    escape: a property outside ``required``, an ``anyOf``-nullable property, or an
    array with no minimum length. This reports a cycle where some member offers no
    escape at all, which is exactly the shape whose 400 is quoted in
    :func:`open_ref_loops`.
    """
    if not isinstance(schema, dict):
        return []
    members = ref_cycle_members(schema)
    if not members:
        return []
    defs = schema.get("$defs") or schema.get("definitions") or {}
    problems: list[str] = []

    def escapes(node: Any, path: str) -> bool:
        """Is there at least ONE way for the cycle through this node to stop?"""
        if isinstance(node, list):
            return any(escapes(item, path) for item in node)
        if not isinstance(node, dict):
            return False
        props = node.get("properties")
        if isinstance(props, dict):
            required = set(node.get("required") or ())
            for name, sub in props.items():
                if not isinstance(sub, dict) or not _references_any(sub, members):
                    continue
                # NULLABLE means the `anyOf` spelling ONLY. A type-ARRAY nullable
                # (`["array","null"]`) is refused — measured, and the whole reason
                # this check exists rather than trusting `is_nullable_union`.
                if name not in required or _array_escape(sub):
                    return True
                # A PLAIN array only. `["array","null"]` does not escape either —
                # adding "null" to the type array breaks the zero-length escape as
                # well as failing the nullable test (measured: plain array 200,
                # ["array","null"] 400, both required).
                if sub.get("type") == "array" and not any(
                    key in sub for key in _MIN_LENGTH_KEYS
                ):
                    return True
                if escapes(sub, f"{path}.{name}"):
                    return True
            return False
        for key, value in node.items():
            if key in ("required", "enum", "const", _NOTES_KEY, "$ref"):
                continue
            if escapes(value, f"{path}.{key}"):
                return True
        return False

    for name in sorted(members):
        body = defs.get(name)
        if isinstance(body, dict) and not escapes(body, f"$defs.{name}"):
            problems.append(
                f"$defs.{name}: a `$ref` cycle through this definition can never terminate — "
                "the provider supports a cycle only through an optional property, an "
                "`anyOf`-nullable property, or a potentially-zero-length array "
                "(open_ref_loops)"
            )
    return problems


def is_nullable_union(node: Any) -> bool:
    """``["T", "null"]`` or ``anyOf: [..., {"type": "null"}]``."""
    if not isinstance(node, dict):
        return False
    t = node.get("type")
    if isinstance(t, list) and "null" in t and len(t) > 1:
        return True
    branches = node.get("anyOf")
    return isinstance(branches, list) and len(branches) > 1 and any(
        isinstance(b, dict) and b.get("type") == "null" for b in branches
    )


def is_union_param(node: Any) -> bool:
    """What Anthropic counts toward its union-parameter ceiling: a property
    whose schema is an ``anyOf`` or a type ARRAY."""
    return isinstance(node, dict) and (
        isinstance(node.get("anyOf"), list) or isinstance(node.get("type"), list)
    )


def count_nullable_union_params(node: Any) -> int:
    """Nullable union PROPERTIES (``[T, null]`` / ``anyOf [..., null]``) across the
    schema — the part of :func:`count_union_params` that narrowing can remove."""
    total = 0
    if isinstance(node, list):
        return sum(count_nullable_union_params(item) for item in node)
    if not isinstance(node, dict):
        return 0
    props = node.get("properties")
    if isinstance(props, dict):
        total += sum(1 for sub in props.values() if is_nullable_union(sub))
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            total += sum(count_nullable_union_params(sub) for sub in value.values())
        elif key not in ("required", "enum", "const"):
            total += count_nullable_union_params(value)
    return total


def count_union_params(node: Any) -> int:
    """Union-typed PROPERTIES across the whole schema (every ``$defs`` entry
    counted once), the unit Anthropic caps at :data:`ANTHROPIC_UNION_PARAM_LIMIT`."""
    total = 0
    if isinstance(node, list):
        return sum(count_union_params(item) for item in node)
    if not isinstance(node, dict):
        return 0
    props = node.get("properties")
    if isinstance(props, dict):
        total += sum(1 for sub in props.values() if is_union_param(sub))
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            total += sum(count_union_params(sub) for sub in value.values())
        elif key not in ("required", "enum", "const"):
            total += count_union_params(value)
    return total


def _without_null(node: dict[str, Any]) -> dict[str, Any]:
    out = dict(node)
    t = out.get("type")
    if isinstance(t, list) and "null" in t:
        rest = [x for x in t if x != "null"]
        # A node whose ONLY type was null has nothing left to narrow to. Emitting
        # `"type": []` is a hard 400 ("[] is not valid under any of the given
        # schemas"); the honest result is the null it already was.
        if not rest:
            return out if t == ["null"] else {**out, "type": "null"}
        out["type"] = rest[0] if len(rest) == 1 else rest
        if isinstance(out.get("enum"), list):
            out["enum"] = [v for v in out["enum"] if v is not None]
    branches = out.get("anyOf")
    if isinstance(branches, list):
        kept = [b for b in branches if not (isinstance(b, dict) and b.get("type") == "null")]
        if len(kept) == 1 and isinstance(kept[0], dict):
            out.pop("anyOf")
            merged = dict(kept[0])
            for key in ("title", "description", "default"):
                if key in out and key not in merged:
                    merged[key] = out[key]
            out = merged
        elif kept:
            out["anyOf"] = kept
    return out


def collapse_nullable_unions(
    node: Any, keep: int = 0, notes: list[str] | None = None, reason: str = ""
) -> Any:
    """Return a copy in which nullable union PROPERTIES beyond the first ``keep``
    (document order) are NARROWED to their non-null branch.

    This is a narrowing, never a relaxation: every answer the narrowed schema
    admits is also admitted by the declared one (``T`` ⊂ ``T | null``), so the
    platform's check of the answer against the stored contract keeps passing.
    What is given up is the model's ability to answer ``null`` for those fields —
    named in ``notes``, which the translators hand to the findings channel. Anthropic caps a request at 16 union parameters and its
    compiled-grammar ceiling charges unions heavily; this is the lever that
    brought the agent factory's envelope and the Study Pack flashcards node
    (with a tool attached) under it, measured live 2026-09-27."""
    seen = 0
    narrowed: list[str] = []

    def walk(current: Any, path: str) -> Any:
        nonlocal seen
        if isinstance(current, list):
            return [walk(item, f"{path}[{i}]") for i, item in enumerate(current)]
        if not isinstance(current, dict):
            return current
        out: dict[str, Any] = {}
        for key, value in current.items():
            if key == "properties" and isinstance(value, dict):
                props: dict[str, Any] = {}
                for name, sub in value.items():
                    if is_nullable_union(sub):
                        seen += 1
                        if seen > keep:
                            sub = _without_null(sub)
                            narrowed.append(f"{path}.{name}")
                    props[name] = walk(sub, f"{path}.{name}")
                out[key] = props
            elif key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                out[key] = {n: walk(s, f"{path}.{key}.{n}") for n, s in value.items()}
            elif key in ("enum", "const", "required"):
                out[key] = value
            else:
                out[key] = walk(value, f"{path}.{key}")
        return out

    result = walk(node, "$")
    if narrowed and notes is not None:
        shown = ", ".join(narrowed[:12]) + (f" (+{len(narrowed) - 12} more)" if len(narrowed) > 12 else "")
        notes.append(
            f"{len(narrowed)} nullable field(s) NARROWED to non-null{(' — ' + reason) if reason else ''}: "
            f"{shown}. Answers stay valid under the declared contract; the model can no "
            "longer answer null there"
        )
    return result


#: Keywords that only ANNOTATE a node (they constrain nothing), so a
#: single-branch combinator may absorb them without changing what it admits.
_ANNOTATION_ONLY_KEYS: frozenset[str] = frozenset(
    {"title", "description", "default", "examples", "$comment", "readOnly", "writeOnly", "deprecated"}
)

def _without_normalization_notes(node: Any) -> Any:
    """``node`` with every :data:`NORMALIZATION_NOTES_KEY` removed at every depth —
    the shape the provider will actually see, used to compare two branches."""
    if isinstance(node, list):
        return [_without_normalization_notes(item) for item in node]
    if not isinstance(node, dict):
        return node
    return {
        key: (
            value
            if key in ("enum", "const", "required")
            else _without_normalization_notes(value)
        )
        for key, value in node.items()
        if key != _NOTES_KEY
    }


def _all_normalization_notes(node: Any) -> list[str]:
    """Every normalization note anywhere inside ``node``, in document order."""
    found: list[str] = []
    if isinstance(node, list):
        for item in node:
            found.extend(_all_normalization_notes(item))
        return found
    if not isinstance(node, dict):
        return found
    for key, value in node.items():
        if key == _NOTES_KEY:
            if isinstance(value, list):
                found.extend(str(entry) for entry in value)
        elif key not in ("enum", "const", "required"):
            found.extend(_all_normalization_notes(value))
    return found


def dedupe_combinator_branches(node: Any) -> Any:
    """Return a copy in which every ``anyOf`` / ``oneOf`` / ``allOf`` list keeps
    only the FIRST of each set of byte-identical branches, and a union left with
    exactly one branch collapses into that branch.

    Purely lossless — ``A | A`` admits exactly what ``A`` admits, and an
    intersection of a branch with itself is that branch — but it is a real
    provider-budget lever, because a union is the most expensive thing in a
    constrained decoder's grammar and every provider counts the DEGENERATE ones
    too. Measured live 2026-09-28 (SCHEMA-TRANSLATION-VERIFY.md, F7): 3 live
    schemas reached Anthropic's wire with 24 / 21 / 18 union parameters over its
    documented 16-union cap and were refused; the surplus was
    ``{"anyOf": [{"type": "string"}, {"type": "string"}]}`` — an author's
    generator emitting the same branch twice — and dropping the duplicate takes
    them to 13 / 11 / 9.

    This is a REQUEST-BOUNDARY normalization in the same family as
    :func:`strip_unsupported_keywords`, :func:`rewrite_const_as_enum` and
    :func:`hoist_discriminator_first`: the stored schema keeps exactly what the
    author wrote.

    A single-branch union collapses only when nothing would be lost — the
    parent's remaining keys are annotations, or absent from the branch, or
    byte-equal to the branch's. Anything else keeps the one-branch combinator
    rather than resolving a conflict the author never declared. ``allOf`` is
    deduplicated but never collapsed here: :func:`flatten_allof` owns that merge
    and knows how to intersect the constraints.

    🚨 Two branches are compared with :data:`NORMALIZATION_NOTES_KEY` REMOVED at
    every depth, and the notes of every dropped duplicate are carried onto the
    branch that is kept. That key is Matrx bookkeeping which
    :func:`take_normalization_notes` strips before the wire, so two branches that
    differ only in it are the SAME schema to the provider — and that is the live
    shape: the Docker-Hub tool's ``digest`` arrives as
    ``anyOf: [ anyOf: [ {"not": {}}, {"type": "string"} ], {"type": "null"} ]``,
    :func:`concretize_empty_schemas` turns the emptied refinement branch into
    ``{"type": "string"}`` **plus a note**, and only the note kept the two
    branches apart. Comparing them with the note in place is what let the
    degenerate union survive to the wire, and what left a union parameter behind
    after :func:`collapse_nullable_unions` had narrowed the nullable away. Nothing
    goes quiet: the note still reaches the findings channel from the kept branch.
    """
    import json

    if isinstance(node, list):
        return [dedupe_combinator_branches(item) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {
                name: dedupe_combinator_branches(sub) for name, sub in value.items()
            }
        elif key in ("enum", "const", "required"):
            out[key] = value
        else:
            out[key] = dedupe_combinator_branches(value)
    for combinator in _COMBINATOR_KEYS:
        branches = out.get(combinator)
        if not isinstance(branches, list) or len(branches) < 2:
            continue
        first_at: dict[str, int] = {}
        kept: list[Any] = []
        for branch in branches:
            fingerprint = json.dumps(
                _without_normalization_notes(branch),
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            )
            if fingerprint in first_at:
                # Identical schema, different bookkeeping: keep the note.
                position = first_at[fingerprint]
                carried = _all_normalization_notes(branch)
                if carried and isinstance(kept[position], dict):
                    existing = list(kept[position].get(_NOTES_KEY) or [])
                    merged = existing + [n for n in carried if n not in existing]
                    kept[position] = {**kept[position], _NOTES_KEY: merged}
                continue
            first_at[fingerprint] = len(kept)
            kept.append(branch)
        if len(kept) == len(branches):
            continue
        out[combinator] = kept
    for combinator in ("anyOf", "oneOf"):
        branches = out.get(combinator)
        if not (isinstance(branches, list) and len(branches) == 1):
            continue
        branch = branches[0]
        if not isinstance(branch, dict):
            continue
        siblings = {k: v for k, v in out.items() if k != combinator}
        blocked = [
            k
            for k, v in siblings.items()
            if k in branch and k not in _ANNOTATION_ONLY_KEYS and branch[k] != v
        ]
        if blocked:
            continue
        merged = dict(branch)
        for k, v in siblings.items():
            merged.setdefault(k, v)
        out = merged
        break
    return out


def dedupe_identical_subtrees(schema: Any) -> Any:
    """Return a copy of ``schema`` in which every object subtree that appears
    two or more times, byte-identical, is hoisted into ONE ``$defs`` entry and
    referenced. Purely lossless — the documents it admits are unchanged.

    Measured live 2026-09-27 on claude-sonnet-5: nine arrays of the SAME
    six-property object inline are refused as "compiled grammar too large",
    while twenty arrays referencing that object through one ``$def`` compile —
    the compiler builds a shared definition once and an inline copy every time.
    (Moving DISTINCT objects into ``$defs`` buys nothing, also measured.)"""
    if not isinstance(schema, dict):
        return schema
    import hashlib
    import json

    defs_key = "definitions" if isinstance(schema.get("definitions"), dict) and "$defs" not in schema else "$defs"

    def canon(node: Any) -> str:
        return json.dumps(node, sort_keys=True, separators=(",", ":"), default=str)

    def is_candidate(node: Any) -> bool:
        return isinstance(node, dict) and isinstance(node.get("properties"), dict) and bool(node["properties"])

    counts: dict[str, int] = {}

    def count(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                count(item)
            return
        if not isinstance(node, dict):
            return
        for key, value in node.items():
            if key in ("enum", "const", "required"):
                continue
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                for sub in value.values():
                    if is_candidate(sub):
                        k = canon(sub)
                        counts[k] = counts.get(k, 0) + 1
                    count(sub)
            else:
                if is_candidate(value):
                    k = canon(value)
                    counts[k] = counts.get(k, 0) + 1
                count(value)

    body = {k: v for k, v in schema.items() if k != defs_key}
    count(body)
    for sub in (schema.get(defs_key) or {}).values():
        count(sub)
    shared = {k for k, n in counts.items() if n >= 2}
    if not shared:
        return schema

    existing: dict[str, Any] = dict(schema.get(defs_key) or {})
    by_canon = {canon(v): name for name, v in existing.items()}
    new_defs: dict[str, Any] = {}

    def name_for(k: str) -> str:
        if k in by_canon:
            return by_canon[k]
        name = "Shared_" + hashlib.sha1(k.encode()).hexdigest()[:10]
        by_canon[k] = name
        new_defs[name] = json.loads(k)
        return name

    def rewrite(node: Any, allow_self: bool = False) -> Any:
        if isinstance(node, list):
            return [rewrite(item) for item in node]
        if not isinstance(node, dict):
            return node
        if not allow_self and is_candidate(node) and canon(node) in shared:
            return {"$ref": f"#/{defs_key}/{name_for(canon(node))}"}
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key in ("enum", "const", "required"):
                out[key] = value
            elif key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                out[key] = {n: rewrite(s) for n, s in value.items()}
            else:
                out[key] = rewrite(value)
        return out

    out = rewrite(body, allow_self=True)
    defs_out = {name: rewrite(sub, allow_self=True) for name, sub in existing.items()}
    # A freshly hoisted definition can itself contain another shared subtree.
    pending = dict(new_defs)
    while pending:
        new_defs.clear()
        for name, sub in pending.items():
            defs_out[name] = rewrite(sub, allow_self=True)
        pending = {k: v for k, v in new_defs.items() if k not in defs_out}
    out[defs_key] = defs_out
    return out


def classify_normalization_notes(notes: list[str]) -> tuple[list[str], list[str]]:
    """Split the combinator rules' notes into ``(narrowed, relaxed)``, dropping
    the lossless ones.

    * NARROWED — the provider copy admits a SUBSET of the declared documents
      (an empty ``{}`` given a concrete type, a tuple reduced to its first item).
    * RELAXED — a constraint the provider no longer enforces (an ``allOf``
      branch or a union's outer constraint dropped).
    * lossless — ``discriminator`` (routing metadata) or a ``type`` restated by
      every branch of a union: nothing is given up, nothing is reported.
    """
    import re

    narrowed: list[str] = []
    relaxed: list[str] = []
    for note in notes:
        if note.startswith("union siblings dropped"):
            match = re.search(r"\[([^\]]*)\]", note)
            listed = {
                part.strip().strip("'\"") for part in (match.group(1).split(",") if match else [])
            }
            if listed and listed <= {"discriminator", "type"}:
                continue
        if "narrowed to" in note or "reduced to the first" in note:
            narrowed.append(note)
        else:
            relaxed.append(note)
    return narrowed, relaxed


def structured_output_size(schema: Any) -> dict[str, int]:
    """The dimensions Anthropic's compiled-grammar budget responds to, counted
    over DISTINCT definitions (a ``$def`` referenced many times counts once):
    properties, union parameters, optional parameters, objects, arrays.

    Measured 2026-09-27: roughly 70 properties per request compile (67 pass /
    73 fail on claude-sonnet-5, 72 / 76 on claude-opus-5-5), 16 union
    parameters, and ~12 optional ones. Reported on every budget finding so the
    schema's owner knows how far over the line the shape is."""
    size = {"properties": 0, "union_params": 0, "optional": 0, "objects": 0, "arrays": 0}

    def walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return
        props = node.get("properties")
        if isinstance(props, dict):
            size["objects"] += 1
            size["properties"] += len(props)
            required = set(node.get("required") or ())
            size["optional"] += sum(1 for name in props if name not in required)
            size["union_params"] += sum(1 for sub in props.values() if is_union_param(sub))
        if node.get("type") == "array" or "items" in node:
            size["arrays"] += 1
        for key, value in node.items():
            if key in ("enum", "const", "required"):
                continue
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                for sub in value.values():
                    walk(sub)
            else:
                walk(value)

    walk(schema)
    return size


#: Anthropic's documented ceiling on union-typed parameters per request (anyOf
#: or a type array), measured exact on 2026-09-27: 16 compiles, 17 answers
#: "Schemas contains too many parameters with union types". One tool on the
#: request spends one of them (15 compiles with a tool, 16 does not). This is a
#: PROVIDER fact, not a platform opinion — it is not a knob.
ANTHROPIC_UNION_PARAM_LIMIT = 16


def anthropic_grammar_cost(schema: Any) -> float:
    """What a wire schema costs against Anthropic's compiled-grammar budget —
    a MEASURED model, not a guess.

    Fitted on 1,838 distinct bodies probed against ``claude-sonnet-5`` on
    2026-09-28 (the full live sweep's baseline, pre-fix and post-fix bodies; 224
    of them refused "The compiled grammar is too large"):
    ``properties + 1.5 × union parameters + 3 × arrays + 0.3 × enum members``,
    each ``$defs`` entry counted ONCE (identical subtrees shared through
    ``$defs`` compile once — grammar_budget.py). Over 2,700 probed bodies the
    lowest refusal scores 72.0 and the next 81.0. Two earlier fits with unions,
    arrays and enum members weighted lower each put a refused body under their
    ceiling (65.5 / 66, then 72.0 — an io_contract with 36 properties, 8 arrays
    and 45 enum members that three added nullable unions tipped over). It is an
    estimate with a measured floor, not the provider's formula, which is why the
    Anthropic translator's ceiling sits well below that floor. Byte size was
    measured and is not the metric.
    """
    totals = {"props": 0, "unions": 0, "arrays": 0, "enum_members": 0}

    def walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return
        props = node.get("properties")
        if isinstance(props, dict):
            totals["props"] += len(props)
        if is_union_param(node):
            totals["unions"] += 1
        if node.get("type") == "array" or "items" in node:
            totals["arrays"] += 1
        enum = node.get("enum")
        if isinstance(enum, list):
            totals["enum_members"] += len(enum)
        for key, value in node.items():
            if key in ("required", "enum", "const", "default", "examples"):
                continue
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                for sub in value.values():
                    walk(sub)
            else:
                walk(value)

    walk(schema)
    return (
        totals["props"]
        + 1.5 * totals["unions"]
        + 3 * totals["arrays"]
        + 0.3 * totals["enum_members"]
    )


def take_normalization_notes(node: Any) -> tuple[Any, list[str]]:
    """Split a normalized schema into ``(clean_schema, notes)``: every
    :data:`_NOTES_KEY` entry is collected and removed at every depth, so the
    schema that reaches the provider carries no Matrx bookkeeping and the caller
    holds the list of everything a normalization had to give up."""
    notes: list[str] = []

    def walk(current: Any) -> Any:
        if isinstance(current, list):
            return [walk(item) for item in current]
        if not isinstance(current, dict):
            return current
        out: dict[str, Any] = {}
        for key, value in current.items():
            if key == _NOTES_KEY:
                if isinstance(value, list):
                    notes.extend(str(item) for item in value)
                continue
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                out[key] = {name: walk(sub) for name, sub in value.items()}
            else:
                out[key] = walk(value)
        return out

    return walk(node), notes



def hoist_nested_defs(schema: Any) -> Any:
    """Lift every NESTED ``$defs`` / ``definitions`` map to the document root and
    rewrite the pointers, so every ``$ref`` resolves. The input is never mutated.

    A ``$ref`` in JSON Schema is resolved from the document ROOT: ``#/$defs/X``
    means "the entry ``X`` of the root's ``$defs``", and nothing else. Embedding a
    self-contained schema whole under a parent's ``properties`` therefore breaks
    it — the child brings its own ``$defs`` down with it while its internal
    pointers keep naming the root — and the provider answers, verbatim:

        Anthropic: ``output_config.format.schema: Invalid schema: Reference to
                   non-existent definition: #/$defs/plan_draft_section``
        OpenAI:    ``reference to component '#/$defs/plan_draft_section' which was
                   not found``

    That is how 17 live registered kinds (measured 2026-09-27 over every
    ``content_ir.kind_definition`` row: the ``news.*``, ``commerce_intake.*``,
    ``masterwork.*``, ``seo.*`` and ``content_plan.page_review`` offers) hard-400
    on BOTH providers. It is the composition pattern the kind registry is built
    on, so the boundary owns it — per Arman's 2026-09-27 ruling a provider
    refusing our request is OUR translator's bug, never the schema author's.

    Purely LOSSLESS: nothing but the LOCATION of a definition changes. A nested
    entry whose name is already taken at the root by an IDENTICAL body collapses
    onto it; one taken by a DIFFERENT body is renamed (``Name__2``) and the
    pointers inside the subtree that owned it are rewritten to the new name, so
    two unrelated ``Name`` definitions cannot be confused for each other.
    """
    if not isinstance(schema, dict):
        return schema

    root_key = "definitions" if (
        isinstance(schema.get("definitions"), dict) and not isinstance(schema.get("$defs"), dict)
    ) else "$defs"
    root_defs: dict[str, Any] = {}

    def rewrite_refs(node: Any, rename: dict[str, str]) -> Any:
        """Point every local ``$ref`` naming a renamed definition at its new name."""
        if isinstance(node, list):
            return [rewrite_refs(item, rename) for item in node]
        if not isinstance(node, dict):
            return node
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.startswith("#"):
                name = value.rsplit("/", 1)[-1]
                out[key] = f"#/{root_key}/{rename[name]}" if name in rename else value
            elif key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                out[key] = {n: rewrite_refs(sub, rename) for n, sub in value.items()}
            else:
                out[key] = rewrite_refs(value, rename)
        return out

    def walk(node: Any, *, at_root: bool) -> Any:
        if isinstance(node, list):
            return [walk(item, at_root=False) for item in node]
        if not isinstance(node, dict):
            return node

        local: dict[str, Any] = {}
        for defs_key in ("$defs", "definitions"):
            value = node.get(defs_key)
            if isinstance(value, dict):
                # A later key wins only when the earlier one did not define it —
                # a document carrying both maps is malformed either way.
                for name, body in value.items():
                    local.setdefault(name, body)

        if at_root:
            # RESERVE the root's own names BEFORE anything else is walked, or a
            # nested definition sharing a name is hoisted into the free slot and
            # the root's own body is the one that disappears.
            for name, body in local.items():
                root_defs[name] = body

        # Every other key next: a nested definition may itself carry nested defs.
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key in ("$defs", "definitions"):
                continue
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                out[key] = {n: walk(sub, at_root=False) for n, sub in value.items()}
            else:
                out[key] = walk(value, at_root=False)

        if at_root:
            # The root's OWN defs stay at the root; only their insides are walked.
            for name, body in local.items():
                root_defs[name] = walk(body, at_root=False)
            return out

        if not local:
            return out

        bodies = {name: walk(body, at_root=False) for name, body in local.items()}
        rename: dict[str, str] = {}
        for name in list(bodies):
            target = name
            suffix = 2
            while target in root_defs and root_defs[target] != bodies[name]:
                target = f"{name}__{suffix}"
                suffix += 1
            if target != name:
                rename[name] = target
        if rename:
            bodies = {
                rename.get(name, name): rewrite_refs(body, rename)
                for name, body in bodies.items()
            }
            out = rewrite_refs(out, rename)
        for name, body in bodies.items():
            root_defs.setdefault(name, body)
        return out

    hoisted = walk(schema, at_root=True)
    if not root_defs:
        return hoisted
    if not isinstance(hoisted, dict):  # pragma: no cover — root is a dict above
        return hoisted
    result = dict(hoisted)
    result.pop("$defs", None)
    result.pop("definitions", None)
    result[root_key] = root_defs
    return result


def unresolvable_refs(schema: Any) -> list[str]:
    """Every local ``$ref`` in ``schema`` that does NOT resolve from the document
    root, as ``"<path>: <ref>"``.

    A pointer that names nothing is a hard 400 on both grammar-constrained
    providers, and it is the ONE malformation no other rule here can see: every
    other rule reads a node's own keywords, while this one reads the whole
    document. It is the check whose absence let 17 live kinds walk through every
    rule AND through :func:`structured_output_schema_violations` to a provider
    refusal (2026-09-27). Remote (``http``) refs are a different problem and are
    not reported here.
    """
    if not isinstance(schema, dict):
        return []
    bad: list[str] = []

    def resolves(ref: str) -> bool:
        node: Any = schema
        for raw in [part for part in ref.lstrip("#").split("/") if part]:
            part = raw.replace("~1", "/").replace("~0", "~")
            if isinstance(node, dict) and part in node:
                node = node[part]
            elif isinstance(node, list) and part.isdigit() and int(part) < len(node):
                node = node[int(part)]
            else:
                return False
        return True

    def walk(node: Any, path: str) -> None:
        if isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{path}[{index}]")
            return
        if not isinstance(node, dict):
            return
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#") and not resolves(ref):
            bad.append(f"{path}: {ref}")
        for key, value in node.items():
            if key == "$ref":
                continue
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                for name, sub in value.items():
                    walk(sub, f"{path}.{key}.{name}")
            elif key not in ("required", "enum", "const", _NOTES_KEY):
                walk(value, f"{path}.{key}")

    walk(schema, "$")
    return bad


def prune_unreachable_defs(schema: Any) -> Any:
    """Return a copy of ``schema`` whose ``$defs`` / ``definitions`` map holds only
    the entries something actually ``$ref``s, transitively. The input is never
    mutated.

    Purely lossless — an unreferenced definition cannot affect validation — and
    it is not cosmetic: a structured-output engine COMPILES a grammar from the
    whole document, so a definition no property points at still spends capacity
    against Anthropic's compiled-grammar ceiling ("The compiled grammar is too
    large, which would cause performance issues"). Pydantic leaves such entries
    behind whenever a model is narrowed or a branch removed, so this runs at the
    boundary for every provider rather than being remembered per contract."""
    if not isinstance(schema, dict):
        return schema
    defs_key = "$defs" if isinstance(schema.get("$defs"), dict) else (
        "definitions" if isinstance(schema.get("definitions"), dict) else None
    )
    if defs_key is None:
        return schema
    defs: dict[str, Any] = schema[defs_key]

    def names_in(node: Any) -> set[str]:
        found: set[str] = set()
        if isinstance(node, list):
            for item in node:
                found |= names_in(item)
        elif isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref" and isinstance(value, str):
                    found.add(value.rsplit("/", 1)[-1])
                else:
                    found |= names_in(value)
        return found

    reachable = names_in({k: v for k, v in schema.items() if k != defs_key})
    frontier = set(reachable)
    while frontier:
        nxt: set[str] = set()
        for name in frontier:
            if name in defs:
                nxt |= names_in(defs[name]) - reachable
        reachable |= nxt
        frontier = nxt
    kept = {name: body for name, body in defs.items() if name in reachable}
    if len(kept) == len(defs):
        return schema
    out = dict(schema)
    out[defs_key] = kept
    return out


def structured_output_schema_violations(schema: Any) -> list[str]:
    """Return every reason the provider's structured-output validator would 400
    on ``schema`` — empty list means "no known violation left".

    THE FORCING FUNCTION. Every rule above removes ONE shape; this reads the
    FINAL wire schema and says whether anything the subset forbids survived, so
    a new Pydantic shape shows up as a named, actionable line in our own logs
    instead of an opaque 400 from the provider. The checks are exactly the ones
    measured live against ``claude-opus-5-5`` on 2026-09-27 (one request per
    keyword); add a row here the moment a new refusal is observed.
    """
    problems: list[str] = []

    def object_node(node: dict[str, Any]) -> bool:
        return node.get("type") == "object" or isinstance(node.get("properties"), dict)

    def walk(node: Any, path: str) -> None:
        if isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{path}[{index}]")
            return
        if not isinstance(node, dict):
            return
        if "allOf" in node:
            problems.append(f"{path}: `allOf` is not compiled — flatten it into the parent")
        if any(isinstance(node.get(k), list) for k in ("anyOf", "oneOf")):
            bad = sorted(k for k in node if k not in COMBINATOR_SAFE_SIBLINGS and k != _NOTES_KEY)
            if bad:
                problems.append(f"{path}: {bad} sit beside a union; only {sorted(COMBINATOR_SAFE_SIBLINGS)} may")
        if isinstance(node.get("oneOf"), list):
            problems.append(f"{path}: `oneOf` is not supported — rewrite to `anyOf`")
        for combinator in _COMBINATOR_KEYS:
            if isinstance(node.get(combinator), list) and not node[combinator]:
                problems.append(f"{path}.{combinator}: must be a non-empty array")
        for keyword in sorted(STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS - {"default", "$schema", "$comment"}):
            if keyword in node:
                problems.append(f"{path}: `{keyword}` is not supported by the constrained decoder")
        for extension in sorted(
            k for k in node if k.startswith(STRUCTURED_OUTPUT_EXTENSION_PREFIX)
        ):
            # "For 'object' type, property 'x-contract-dynamic' is not supported" —
            # measured live on the largest live schemas, 2026-09-27.
            problems.append(
                f"{path}: `{extension}` is a schema EXTENSION; the constrained decoder "
                "refuses an unknown property on a node"
            )
        if isinstance(node.get("items"), list):
            problems.append(f"{path}.items: must be a single schema, not a list")
        if isinstance(node.get("type"), list) and isinstance(node.get("enum"), list):
            # "Enum value 'a' does not match declared type '['string', 'null']'" —
            # measured live 2026-09-27, and it fires even when the enum holds no
            # null, so it is the type ARRAY the validator objects to. An
            # `Optional[SomeEnum]` in Pydantic is exactly this shape.
            problems.append(
                f"{path}: an `enum` may not sit beside a type ARRAY — rewrite as "
                "`anyOf` branches (split_enum_from_type_union)"
            )
        if (object_node(node) or _declares_object(node)) and node.get("additionalProperties") is not False:
            problems.append(f"{path}: object nodes must set `additionalProperties: false`")
        if "$ref" in node and (set(node) - {"$ref", "title", "description", "default"}):
            problems.append(
                f"{path}: `$ref` cannot carry sibling constraint keys "
                f"{sorted(set(node) - {'$ref', 'title', 'description', 'default'})}"
            )
        if not {k for k in node if k not in ("title", "description", _NOTES_KEY)}:
            problems.append(f"{path}: empty schema — the provider requires a concrete type")
        for key, value in node.items():
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                for name, sub in value.items():
                    walk(sub, f"{path}.{key}.{name}")
            elif key not in ("required", "enum", "const", _NOTES_KEY):
                walk(value, f"{path}.{key}")

    walk(schema, "$")
    # A pointer that resolves to nothing is a hard 400 on both grammar-constrained
    # providers ("Reference to non-existent definition: #/$defs/X"), and no
    # per-node rule can see it — it is a whole-document fact. Its absence is why
    # 17 live kinds with a NESTED `$defs` walked through every rule here to a
    # provider refusal (2026-09-27); `hoist_nested_defs` is the fix, this is the
    # forcing function that will not let the class return silently.
    for dangling in unresolvable_refs(schema):
        problems.append(
            f"{dangling} does not resolve from the document root — hoist the nested "
            "`$defs` to the root (hoist_nested_defs) or remove the pointer"
        )
    unions = count_union_params(schema)
    if unions > ANTHROPIC_UNION_PARAM_LIMIT:
        problems.append(
            f"$: {unions} union-typed parameters — the provider compiles at most "
            f"{ANTHROPIC_UNION_PARAM_LIMIT} (narrow with collapse_nullable_unions)"
        )
    for cycle in _ref_cycles(schema):
        # Reaching this line is a TRANSLATOR gap, not an inexpressible schema: the
        # boundary owns recursion and has two ways to handle it
        # (`unroll_recursive_refs` for a decoder that refuses any cycle,
        # `open_ref_loops` for one that accepts a terminating cycle). Say which,
        # so the finding is actionable instead of a shrug.
        problems.append(
            f"$defs: circular reference {' -> '.join(cycle)} survived translation — "
            "this decoder compiles no cycle at all, so the boundary must unroll it to a "
            "bounded depth (unroll_recursive_refs); reaching here means the translator "
            "did not run that rule"
        )
    return problems


def _ref_cycles(schema: Any) -> list[list[str]]:
    """Every self- or mutually-referencing ``$defs`` entry, as a name cycle.

    🚨 This used to say ``Circular reference detected in schema definitions:
    N -> N`` was a hard 400 that "no boundary rewrite can remove, so it is
    reported, never fixed". That was untrue when it was written and is untrue now:
    :func:`unroll_recursive_refs` removes the cycle (the Anthropic translator has
    called it since 2026-09-27) and :func:`open_ref_loops` makes one EXPRESSIBLE
    for a provider that supports a terminating cycle. FINDING a cycle is all this
    function does; what to do about it belongs to those two, and "the provider
    refuses it" is never the end of the sentence (Arman, 2026-09-27: fix it at the
    core, no workarounds)."""
    if not isinstance(schema, dict):
        return []
    defs = schema.get("$defs") or schema.get("definitions")
    if not isinstance(defs, dict):
        return []

    def refs_in(node: Any) -> set[str]:
        found: set[str] = set()
        if isinstance(node, list):
            for item in node:
                found |= refs_in(item)
        elif isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref" and isinstance(value, str):
                    found.add(value.rsplit("/", 1)[-1])
                else:
                    found |= refs_in(value)
        return found

    edges = {name: refs_in(body) & set(defs) for name, body in defs.items()}
    cycles: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()

    def visit(name: str, stack: list[str]) -> None:
        if name in stack:
            cycle = stack[stack.index(name):] + [name]
            if tuple(sorted(set(cycle))) not in seen:
                seen.add(tuple(sorted(set(cycle))))
                cycles.append(cycle)
            return
        for child in sorted(edges.get(name, ())):
            visit(child, stack + [name])

    for name in sorted(edges):
        visit(name, [])
    return cycles


def count_optional_properties(node: Any) -> int:
    """How many properties across the whole schema are NOT in their object's
    ``required`` list. Anthropic caps a request at 24 of them and then refuses
    the compiled grammar without naming a keyword, so the boundary counts them to
    say what it changed instead of reporting an opaque provider error."""
    total = 0
    if isinstance(node, list):
        return sum(count_optional_properties(item) for item in node)
    if not isinstance(node, dict):
        return 0
    props = node.get("properties")
    if isinstance(props, dict):
        required = set(node.get("required") or ())
        total += len([name for name in props if name not in required])
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            total += sum(count_optional_properties(sub) for sub in value.values())
        elif key not in ("required", "enum", "const"):
            total += count_optional_properties(value)
    return total


_SHAPE_CONSTRAINT_KEYS: frozenset[str] = frozenset(
    {"type", "enum", "const", "$ref", "anyOf", "oneOf", "allOf", "properties", "items"}
)


def admits_null(node: Any) -> bool:
    """Does this declared node already accept ``null``?

    Three ways: explicitly (``["T","null"]`` / ``anyOf [..., null]``); because the
    node IS null (``{"type": "null"}`` — which is what
    :func:`unroll_recursive_refs` puts at its depth floor); or because it
    constrains nothing at all — a bare ``{"description": "…"}`` is an
    unconstrained schema and ``null`` is a JSON value, so it validates. 68 live
    schemas are exactly that, an optional field with no type, and forcing them
    into ``required`` takes nothing away, which is why they are not a finding.

    The null-only case is load-bearing: without it, widening produced
    ``{"type": ["null", "null"]}``, which the union collapse then reduced to
    ``{"type": []}`` — and Anthropic refuses BOTH by name ("[] is not valid under
    any of the given schemas", measured live 2026-09-27). ``decision_tree``, whose
    recursive ``yes``/``no`` branches land on that floor, went from 200 to 400.
    """
    if not isinstance(node, dict):
        return False
    if is_nullable_union(node):
        return True
    t = node.get("type")
    if t == "null" or (isinstance(t, list) and set(t) == {"null"}):
        return True
    return not (_SHAPE_CONSTRAINT_KEYS & set(node))


def pins_one_value(node: Any) -> bool:
    """A property the model cannot invent anything for: a ``const``, or an
    ``enum`` with a single member. Listing it in ``required`` takes nothing away —
    the value is already determined — which is why ``__kind`` is not a finding."""
    if not isinstance(node, dict):
        return False
    if "const" in node:
        return True
    enum = node.get("enum")
    return isinstance(enum, list) and len(enum) == 1


def widen_to_nullable(node: Any) -> Any:
    """Return a copy of ``node`` that also admits ``null``, or ``None`` when the
    node's shape cannot express it.

    This is how an OPTIONAL property survives a provider that demands every
    property in ``required``: required + nullable, answered ``null`` when the
    author meant "absent". :func:`prune_optional_nulls` is the reader's half.

    🚨 THE SPELLING IS ``anyOf``, NOT A TYPE ARRAY, and that is a measured
    decision, not a style. ``{"type": ["T","null"]}`` reads like the obvious form
    and every provider I probed refuses some part of it, each in its own way
    (2026-09-27, one live request per shape):

    * **Anthropic** refuses it beside an ``enum``, even an enum with no null in it:
      ``Enum value 'a' does not match declared type '['string', 'null']'``. Every
      Pydantic ``Optional[SomeEnum]`` is that shape.
    * **Gemini** does not count it as nullable when deciding whether a ``$ref``
      cycle can terminate, and adding ``"null"`` to the type array ALSO breaks the
      zero-length-array escape, so a recursive contract goes from 200 to 400 by
      being made nullable.
    * **OpenAI strict** refuses some combinations of it outright with no context at
      all — ``Invalid schema for response_format 'response'. Please ensure it is a
      valid JSON Schema.`` Bisected to a single node on three live
      ``commerce_intake.*`` kinds; the same node in a small schema is accepted, so
      nothing in the error or the docs predicts it.

    ``{"anyOf": [X, {"type": "null"}]}`` was accepted by all three, every time. One
    spelling, measured, so the class cannot come back per provider. It still counts
    as exactly ONE union parameter (:func:`is_union_param` reads ``anyOf`` and a
    type array alike), so Anthropic's 16-parameter budget is unaffected, and
    :func:`collapse_nullable_unions` narrows this form as readily as the other.
    """
    if not isinstance(node, dict):
        return None
    if admits_null(node):
        return dict(node)

    out = dict(node)
    # Already a union of shapes: add the null branch to it rather than nesting.
    for combinator in ("anyOf", "oneOf"):
        branches = out.get(combinator)
        if isinstance(branches, list) and branches:
            out[combinator] = [*branches, {"type": "null"}]
            return out

    # Name the type the node only implied by its shape, so the branch stands alone.
    if "type" not in out:
        if isinstance(out.get("properties"), dict):
            out["type"] = "object"
        elif "items" in out:
            out["type"] = "array"
        elif not ({"$ref", "enum", "const"} & out.keys()):
            return None

    carried = {k: v for k, v in out.items() if k in ("title", "description")}
    branch = {k: v for k, v in out.items() if k not in ("title", "description")}
    if not branch:
        return None
    return {**carried, "anyOf": [branch, {"type": "null"}]}


def disambiguate_unions_for_strict_validators(schema: Any) -> Any:
    """Respell, LOSSLESSLY, the three union shapes a strict schema validator
    refuses although they mean exactly what the author wrote.

    Measured live on groq (``openai/gpt-oss-20b``, 2026-09-28), one request each:

    * ``{"type": "object", "properties": {}, "required": []}`` → "'required'
      present but 'properties' is missing". An empty ``required`` says nothing,
      and an empty ``properties`` says nothing either: both are removed.
    * ``anyOf: [{"$ref": "#/$defs/J"}, {"type": "null"}]`` where ``J`` is a
      string or an enum → "anyOf branches must be disambiguated via a required
      discriminator"; the same branch INLINED is accepted, and a ``$ref`` to an
      object is accepted as is. So a non-object, non-recursive ``$ref`` branch
      is inlined.
    * two branches that both admit ``null`` → "multiple branches accept null".
      The explicit ``{"type": "null"}`` branch is redundant there and is dropped.

    These were 135 live schemas groq accepted with the optional field forced and
    refused once it was widened (SCHEMA-TRANSLATION-VERIFY.md, R6).
    """
    if not isinstance(schema, dict):
        return schema
    root = schema
    cycle_members = ref_cycle_members(schema)

    def inline_target(branch: Any) -> Any:
        if not (isinstance(branch, dict) and set(branch) <= {"$ref", "description", "title"}):
            return branch
        ref = branch.get("$ref")
        if not isinstance(ref, str):
            return branch
        name = ref.rsplit("/", 1)[-1]
        if name in cycle_members:
            return branch
        target = _resolve_local_ref(ref, root)
        if not isinstance(target, dict) or is_object_node(target) or "$ref" in target:
            return branch
        return {**copy.deepcopy(target), **{k: v for k, v in branch.items() if k != "$ref"}}

    def walk(node: Any) -> Any:
        if isinstance(node, list):
            return [walk(item) for item in node]
        if not isinstance(node, dict):
            return node
        out = {key: walk(value) for key, value in node.items()}
        props = out.get("properties")
        if isinstance(props, dict) and not props:
            out.pop("properties", None)
            if not out.get("required"):
                out.pop("required", None)
        elif "required" in out and not isinstance(props, dict) and not out.get("required"):
            out.pop("required", None)
        branches = out.get("anyOf")
        if isinstance(branches, list) and len(branches) > 1:
            has_null_branch = any(
                isinstance(b, dict) and b.get("type") == "null" for b in branches
            )
            if has_null_branch:
                branches = [inline_target(b) for b in branches]
                others_admit_null = any(
                    isinstance(b, dict) and b.get("type") != "null" and admits_null(b)
                    and (_SHAPE_CONSTRAINT_KEYS & set(b))
                    for b in branches
                )
                if others_admit_null:
                    branches = [
                        b for b in branches if not (isinstance(b, dict) and b.get("type") == "null")
                    ]
                out["anyOf"] = branches
                if len(branches) == 1 and isinstance(branches[0], dict):
                    only = out.pop("anyOf")[0]
                    out = {**only, **out}
        return out

    return walk(schema)


class WideningBudget:
    """Which OPTIONAL properties a provider boundary may express as
    required-and-nullable, and which it must force.

    Widening is lossless for the contract but it is not free on the wire: every
    widened field is one more union the provider's decoder has to compile. On
    most providers that costs nothing measurable; on Anthropic it spends the
    compiled-grammar budget (29 live schemas it accepted with the field forced
    were refused once widened — SCHEMA-TRANSLATION-VERIFY.md, R5), and Groq's
    validator refuses some union spellings outright (R6). So the decision is the
    TRANSLATOR's, per provider, and this object carries it:

    * ``limit`` — widen at most this many optional fields (in document order);
      the rest are forced and NAMED in the notes. ``None`` = no limit.
    * ``can_widen`` — a per-node veto for a shape the provider refuses as a
      union. A vetoed field is forced and named, exactly as over-budget ones are.

    A third lever, for a provider that UNROLLS a bounded array:

    * ``unroll_budget`` — a widening inside ``{"maxItems": 40}`` is paid 40 times
      by such a provider, so it spends 40 of this budget; one at the root spends
      nothing. ``None`` = unmetered, which is every provider but Google.

      Measured live against ``gemini-2.5-flash``, 2026-09-28: the identical item
      schema is ACCEPTED under ``maxItems: 40`` and REFUSED under ``maxItems:
      100``; 5 nullable item fields are accepted at ``maxItems: 40`` and 6 are
      refused; and 80 nullable fields at the ROOT of a flat object are accepted,
      so width on its own costs nothing measurable. That is the whole of Google's
      F1 refusal: ONE extra nullable union inside a ``maxItems: 40`` array turned
      a live schema Gemini accepts into one it refuses
      (SCHEMA-TRANSLATION-VERIFY.md, F1). The spend is not Gemini's formula — the
      frontier also moves with the rest of the schema — so the translator sets the
      budget at the lowest ACCEPTED spend it measured, never the highest.

    ``widened`` / ``forced`` count what happened, so a caller searching for the
    largest budget that fits can read it back.
    """

    __slots__ = (
        "limit",
        "can_widen",
        "widened",
        "forced",
        "candidates",
        "unroll_budget",
        "spent_unroll",
    )

    def __init__(
        self,
        limit: int | None = None,
        can_widen: Any = None,
        unroll_budget: float | None = None,
    ) -> None:
        self.limit = limit
        self.can_widen = can_widen
        self.unroll_budget = unroll_budget
        self.widened = 0
        self.forced = 0
        self.candidates = 0
        self.spent_unroll = 0.0

    def allow(self, node: Any, unroll: float = 1.0) -> bool:
        """May this optional field be widened? ``unroll`` is how many times the
        provider pays for it — the product of the ``maxItems`` of every bounded
        array it sits inside."""
        self.candidates += 1
        if self.can_widen is not None and not self.can_widen(node):
            return False
        if self.limit is not None and self.widened >= self.limit:
            return False
        if self.unroll_budget is not None and unroll > 1:
            if self.spent_unroll + unroll > self.unroll_budget:
                return False
            self.spent_unroll += unroll
        return True


def enforce_all_required(
    node: Any,
    *,
    express_optional_as_nullable: bool = False,
    notes: list[str] | None = None,
    budget: WideningBudget | None = None,
    _path: str = "$",
    _unroll: float = 1.0,
) -> None:
    """In place: set ``required`` to ALL property keys on every object node.
    OpenAI strict + Anthropic require every property listed in ``required``.

    🚨 **Listing a property in ``required`` without making it nullable NARROWS the
    contract**, and that narrowing is invisible to the author. Measured over
    4,000 live schemas on 2026-09-27: **2,865** force a real business field the
    author left optional — ``plan_node_specialist``'s ``gap_description`` exists
    to be set *only when there is a gap*, and forcing it makes the model invent
    one on every call (``Resell Research Agent``: ``product_images``,
    ``market_listings``; ``Brand Coverage Analyst``: ``key_quote``,
    ``published_date``). An answer that legitimately OMITS such a field is
    admitted by the declared contract and refused by the forced one.

    ``express_optional_as_nullable=True`` is therefore the default posture at
    every boundary that has a choice: an optional property becomes
    **required AND nullable**, so ``null`` carries "absent" and the set of
    answers the wire contract admits matches the declared one exactly — LOSSLESS
    instead of narrowing. The reader's half of that bargain is
    :func:`prune_optional_nulls`, which turns those nulls back into absence
    before the answer is judged against the declared schema.

    A property that :func:`pins_one_value` (a ``const``, a one-member ``enum`` —
    ``__kind``) is forced and NOT made nullable: the value is already determined,
    so nothing is taken away, and 653 of the live schemas are this case alone.
    Anything else that cannot be widened is forced and NAMED in ``notes``, which
    the translators pass to the findings channel as a ``narrowed`` finding
    carrying the agent, the schema and the field names.

    Anthropic caps a request at 16 union parameters, so the translator widens
    first and lets :func:`collapse_nullable_unions` take the excess back to the
    budget — the fields it narrows are named there, in the same channel.
    """
    if not isinstance(node, dict):
        return
    props = node.get("properties")
    if isinstance(props, dict):
        optional = [name for name in props if name not in set(node.get("required") or ())]
        forced: list[str] = []
        for name in optional:
            sub = props[name]
            if not express_optional_as_nullable or pins_one_value(sub):
                if not pins_one_value(sub):
                    forced.append(f"{_path}.{name}")
                continue
            if admits_null(sub):
                # Already says "absent" (explicitly nullable, the null node, or an
                # unconstrained schema): listing it in `required` takes nothing away.
                continue
            if budget is not None and not budget.allow(sub, _unroll):
                budget.forced += 1
                forced.append(f"{_path}.{name}")
                continue
            widened = widen_to_nullable(sub)
            if widened is None:
                forced.append(f"{_path}.{name}")
            else:
                props[name] = widened
                if budget is not None:
                    budget.widened += 1
        if forced and notes is not None:
            shown = ", ".join(forced[:12]) + (
                f" (+{len(forced) - 12} more)" if len(forced) > 12 else ""
            )
            notes.append(
                f"{len(forced)} optional field(s) made REQUIRED and not nullable — the "
                f"provider lists every property and this shape cannot express null: {shown}. "
                "The model must now supply a value the author allowed it to omit"
            )
        node["required"] = list(props.keys())
        for name, value in props.items():
            enforce_all_required(
                value,
                express_optional_as_nullable=express_optional_as_nullable,
                notes=notes,
                budget=budget,
                _path=f"{_path}.{name}",
                _unroll=_unroll,
            )
    items = node.get("items")
    # A BOUNDED array multiplies everything under it for a provider that unrolls
    # it (Google): `maxItems: 40` means the item schema — and every widening
    # inside it — is compiled 40 times. An UNBOUNDED array is a loop and costs
    # once, which is why the multiplier only moves when `maxItems` is a real
    # positive integer.
    raw_max = node.get("maxItems")
    item_unroll = (
        _unroll * min(int(raw_max), 256) if isinstance(raw_max, int) and raw_max > 0 else _unroll
    )
    if isinstance(items, dict):
        enforce_all_required(
            items,
            express_optional_as_nullable=express_optional_as_nullable,
            notes=notes,
            budget=budget,
            _path=f"{_path}[]",
            _unroll=item_unroll,
        )
    elif isinstance(items, list):
        for index, item in enumerate(items):
            enforce_all_required(
                item,
                express_optional_as_nullable=express_optional_as_nullable,
                notes=notes,
                budget=budget,
                _path=f"{_path}[{index}]",
                _unroll=item_unroll,
            )
    for comb in ("anyOf", "oneOf", "allOf"):
        arr = node.get(comb)
        if isinstance(arr, list) and not _is_refinement_combinator(node, comb):
            for index, item in enumerate(arr):
                enforce_all_required(
                    item,
                    express_optional_as_nullable=express_optional_as_nullable,
                    notes=notes,
                    budget=budget,
                    _path=f"{_path}.{comb}[{index}]",
                    _unroll=_unroll,
                )
    defs = node.get("$defs") or node.get("definitions")
    if isinstance(defs, dict):
        for name, value in defs.items():
            enforce_all_required(
                value,
                express_optional_as_nullable=express_optional_as_nullable,
                notes=notes,
                budget=budget,
                _path=f"$defs.{name}",
                # A `$defs` entry has no single position, so it carries no array
                # multiplier of its own. It is reached by `$ref` from wherever it
                # is used; a widening inside one that is referenced from a bounded
                # array is therefore NOT metered here, and is the known limit of
                # this measure.
                _unroll=_unroll,
            )


def optional_nonnullable_properties(schema: Any) -> set[str]:
    """Every property in ``schema`` (by JSON-pointer-ish path) that the DECLARED
    contract leaves optional and does not allow to be ``null``.

    These are exactly the properties a provider boundary had to force, so these
    are exactly the ones whose ``null`` in an answer means "the author's absent".
    """
    found: set[str] = set()

    def walk(node: Any, path: str) -> None:
        if isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{path}[{index}]")
            return
        if not isinstance(node, dict):
            return
        props = node.get("properties")
        if isinstance(props, dict):
            required = set(node.get("required") or ())
            for name, sub in props.items():
                if name not in required and not admits_null(sub):
                    found.add(f"{path}.{name}")
        for key, value in node.items():
            if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
                for name, sub in value.items():
                    walk(sub, f"{path}.{name}" if key == "properties" else f"{path}.{key}.{name}")
            elif key not in ("required", "enum", "const", _NOTES_KEY):
                walk(value, f"{path}.{key}" if key != "items" else f"{path}[]")

    walk(schema, "$")
    return found


_MAX_PRUNE_DEPTH = 64


def _deref(node: Any, root: Any, *, limit: int = 32) -> Any:
    """Follow a chain of internal ``$ref`` pointers from ``node`` to the schema it
    names. A pointer that does not resolve leaves the node as it is — the caller
    then reads no ``properties`` from it and prunes nothing, which is the honest
    outcome for a contract it cannot read."""
    seen = 0
    while isinstance(node, dict) and "$ref" in node and seen < limit:
        target = _resolve_local_ref(node.get("$ref"), root) if isinstance(root, dict) else None
        if target is None:
            return node
        siblings = {k: v for k, v in node.items() if k != "$ref"}
        node = {**target, **siblings} if siblings else target
        seen += 1
    return node


def admits_null_in(node: Any, root: Any, *, _depth: int = 0) -> bool:
    """:func:`admits_null`, reading THROUGH ``$ref`` and combinators.

    ``{"$ref": "#/$defs/JsonValue"}`` admits ``null`` exactly when ``JsonValue``
    does; an ``anyOf``/``oneOf`` admits it when any branch does; an ``allOf`` only
    when every member does. The bare :func:`admits_null` reads one node and must
    stay that way for the boundary rewrites, which have no root to resolve
    against — the ANSWER side always has the whole document."""
    if not isinstance(node, dict) or _depth > _MAX_PRUNE_DEPTH:
        return False
    node = _deref(node, root)
    if not isinstance(node, dict):
        return False
    if admits_null(node) and "$ref" not in node:
        return True
    for combinator in ("anyOf", "oneOf"):
        branches = node.get(combinator)
        if isinstance(branches, list) and any(
            admits_null_in(branch, root, _depth=_depth + 1) for branch in branches
        ):
            return True
    members = node.get("allOf")
    if isinstance(members, list) and members:
        return all(admits_null_in(member, root, _depth=_depth + 1) for member in members)
    return False


def _branch_validates(value: Any, branch: Any, root: Any) -> bool:
    try:
        import jsonschema
    except ImportError:  # pragma: no cover — jsonschema is a hard dependency
        return False
    if not isinstance(branch, dict):
        return False
    defs = (
        {k: v for k, v in root.items() if k in ("$defs", "definitions")}
        if isinstance(root, dict)
        else {}
    )
    candidate = {**defs, **branch}
    try:
        validator = jsonschema.validators.validator_for(candidate)(candidate)
        return next(iter(validator.iter_errors(value)), None) is None
    except Exception:  # noqa: BLE001 — an unreadable branch simply does not match
        return False


_JSON_TYPE_OF: tuple[tuple[type, str], ...] = (
    (bool, "boolean"),
    (int, "integer"),
    (float, "number"),
    (str, "string"),
    (list, "array"),
    (dict, "object"),
)


def _type_can_hold(branch: dict[str, Any], value: Any) -> bool:
    """Could ``branch`` accept a value of ``value``'s JSON type at all? Read from
    ``type`` or from the shape keywords that imply one; an unconstrained or
    combinator branch says yes."""
    if value is None:
        kind = "null"
    else:
        kind = next((name for py, name in _JSON_TYPE_OF if isinstance(value, py)), "")
    declared = branch.get("type")
    if declared is None:
        if isinstance(branch.get("properties"), dict):
            declared = "object"
        elif "items" in branch or "prefixItems" in branch:
            declared = "array"
        elif "enum" in branch and isinstance(branch["enum"], list):
            return value in branch["enum"]
        elif "const" in branch:
            return value == branch["const"]
        else:
            return True
    names = set(declared) if isinstance(declared, list) else {declared}
    if kind == "integer" and "number" in names:
        return True
    return kind in names


def _prune_under_combinator(
    answer: Any, branches: list[Any], root: Any, depth: int
) -> Any:
    """Prune ``answer`` under the ``anyOf``/``oneOf`` branch it actually answers.

    The branch is chosen by the AUTHOR's contract, not guessed: the first branch
    the pruned answer satisfies wins; failing that, the object branch that
    declares the most of the answer's keys. An answer that fits no branch at all
    is returned with only the branch-independent pruning applied — the contract
    check reports it."""
    resolved = [_deref(branch, root) for branch in branches if isinstance(branch, dict)]
    fitting = [branch for branch in resolved if _type_can_hold(branch, answer)]
    if len(fitting) == 1:
        # The overwhelmingly common case — `anyOf: [X, null]` answered with an X.
        return _prune(answer, fitting[0], root, depth + 1)
    if fitting:
        resolved = fitting
    pruned_by_branch = [
        (branch, _prune(answer, branch, root, depth + 1)) for branch in resolved
    ]
    for branch, pruned in pruned_by_branch:
        if _branch_validates(pruned, branch, root):
            return pruned
    if isinstance(answer, dict):
        keys = set(answer)
        best = max(
            pruned_by_branch,
            key=lambda pair: len(keys & set((pair[0].get("properties") or {}).keys())),
            default=None,
        )
        if best is not None and isinstance(best[0].get("properties"), dict):
            return best[1]
    return answer


def _prune(answer: Any, schema: Any, root: Any, depth: int) -> Any:
    if not isinstance(schema, dict) or depth > _MAX_PRUNE_DEPTH or answer is None:
        return answer
    schema = _deref(schema, root)
    if not isinstance(schema, dict):
        return answer

    if isinstance(answer, list):
        items = schema.get("items")
        prefix = schema.get("prefixItems")
        if isinstance(prefix, list) or isinstance(items, list):
            positional = prefix if isinstance(prefix, list) else items
            rest = items if isinstance(prefix, list) and isinstance(items, dict) else None
            out: list[Any] = []
            for index, item in enumerate(answer):
                sub = positional[index] if index < len(positional) else rest
                out.append(_prune(item, sub, root, depth + 1) if isinstance(sub, dict) else item)
            answer = out
        elif isinstance(items, dict):
            answer = [_prune(item, items, root, depth + 1) for item in answer]

    elif isinstance(answer, dict):
        props = schema.get("properties")
        if isinstance(props, dict):
            required = set(schema.get("required") or ())
            extra = schema.get("additionalProperties")
            out_obj: dict[str, Any] = {}
            for key, value in answer.items():
                sub = props.get(key)
                if (
                    value is None
                    and key not in required
                    and isinstance(sub, dict)
                    and not admits_null_in(sub, root)
                ):
                    continue
                if isinstance(sub, dict):
                    out_obj[key] = _prune(value, sub, root, depth + 1)
                elif isinstance(extra, dict):
                    # A map entry: never removed (a map's keys are the model's to
                    # choose), only its value pruned.
                    out_obj[key] = _prune(value, extra, root, depth + 1)
                else:
                    out_obj[key] = value
            answer = out_obj
        elif isinstance(schema.get("additionalProperties"), dict):
            extra = schema["additionalProperties"]
            answer = {key: _prune(value, extra, root, depth + 1) for key, value in answer.items()}

        members = schema.get("allOf")
        if isinstance(members, list) and members and isinstance(answer, dict):
            resolved = [_deref(member, root) for member in members if isinstance(member, dict)]
            required_somewhere: set[str] = set()
            for member in resolved:
                required_somewhere |= set(member.get("required") or ())
            out_all: dict[str, Any] = {}
            for key, value in answer.items():
                declaring = [
                    member["properties"][key]
                    for member in resolved
                    if isinstance(member.get("properties"), dict)
                    and isinstance(member["properties"].get(key), dict)
                ]
                if (
                    value is None
                    and declaring
                    and key not in required_somewhere
                    and any(not admits_null_in(sub, root) for sub in declaring)
                ):
                    continue
                out_all[key] = _prune(value, declaring[0], root, depth + 1) if declaring else value
            answer = out_all

    for combinator in ("anyOf", "oneOf"):
        branches = schema.get(combinator)
        if isinstance(branches, list) and branches:
            answer = _prune_under_combinator(answer, branches, root, depth)
            break
    return answer


def prune_optional_nulls(answer: Any, schema: Any, *, root: Any = None) -> Any:
    """Return a copy of ``answer`` with every ``null`` REMOVED wherever the
    declared ``schema`` leaves that property optional and does not allow ``null``.

    The reader's half of :func:`enforce_all_required`'s bargain. A provider that
    demands every property in ``required`` is answered with required+nullable, so
    the model says ``null`` where the author meant "absent" — and ``null`` is not
    a valid value under the declared contract. Dropping it restores exactly the
    answer the author's schema describes.

    It reads the WHOLE contract: through ``$ref`` (every nested Pydantic model is
    one), into ``anyOf``/``oneOf`` (under the branch the answer actually answers),
    across ``allOf`` members, into array items and map values. Until 2026-09-28 it
    walked ``properties`` and ``items`` only, so an optional field inside any
    ``$defs`` object kept its ``null`` and a valid answer was reported off
    contract (SCHEMA-TRANSLATION-VERIFY.md, R4).

    Only a ``null`` at a declared-optional, declared-non-nullable property is
    removed. A ``null`` the author DID allow is kept; a missing key stays missing.
    """
    if not isinstance(schema, dict):
        return answer
    return _prune(answer, schema, schema if root is None else root, 0)


__all__ = [
    "admits_null",
    "admits_null_in",
    "ANTHROPIC_UNION_PARAM_LIMIT",
    "anthropic_grammar_cost",
    "classify_normalization_notes",
    "COMBINATOR_SAFE_SIBLINGS",
    "collapse_nullable_unions",
    "count_nullable_union_params",
    "count_union_params",
    "OPEN_SCALAR_ITEM_SCHEMA",
    "dedupe_combinator_branches",
    "make_array_items_explicit",
    "dedupe_identical_subtrees",
    "disambiguate_unions_for_strict_validators",
    "drop_refinement_combinators",
    "is_map_node",
    "is_nullable_union",
    "ref_cycles",
    "ref_cycle_members",
    "open_ref_loops",
    "gemini_ref_loop_violations",
    "express_nullable_as_anyof",
    "unroll_recursive_refs",
    "unresolvable_refs",
    "NORMALIZATION_NOTES_KEY",
    "KIND_KEY",
    "STRUCTURED_OUTPUT_EXTENSION_PREFIX",
    "STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS",
    "concretize_empty_schemas",
    "count_optional_properties",
    "enforce_additional_properties_false",
    "enforce_all_required",
    "optional_nonnullable_properties",
    "pins_one_value",
    "prune_optional_nulls",
    "widen_to_nullable",
    "WideningBudget",
    "flatten_allof",
    "hoist_nested_defs",
    "hoist_root_recursion",
    "hoist_discriminator_first",
    "is_object_node",
    "is_root_object",
    "normalize_array_items",
    "normalize_combinator_siblings",
    "prune_unreachable_defs",
    "rewrite_const_as_enum",
    "rewrite_oneof_as_anyof",
    "split_enum_from_type_union",
    "strip_unsupported_keywords",
    "structured_output_schema_violations",
    "structured_output_size",
    "take_normalization_notes",
    "unsupported_structured_output_keywords",
]
