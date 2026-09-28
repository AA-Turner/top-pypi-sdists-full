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


def concretize_empty_schemas(node: Any, placeholder_type: str = "string") -> Any:
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
        return [concretize_empty_schemas(item, placeholder_type) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in _SCHEMA_NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {
                name: concretize_empty_schemas(sub, placeholder_type)
                for name, sub in value.items()
            }
        else:
            out[key] = concretize_empty_schemas(value, placeholder_type)
    shaping = {k for k in out if k not in ("title", "description", _NOTES_KEY)}
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
        if isinstance(node.get("items"), list):
            problems.append(f"{path}.items: must be a single schema, not a list")
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
        problems.append(
            f"$defs: circular reference {' -> '.join(cycle)} — recursive schemas are not "
            "supported and cannot be expressed in the accepted subset"
        )
    return problems


def _ref_cycles(schema: Any) -> list[list[str]]:
    """Every self- or mutually-referencing ``$defs`` entry, as a name cycle.
    ``Circular reference detected in schema definitions: N -> N`` is a hard 400
    and no boundary rewrite can remove it, so it is reported, never "fixed"."""
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

    Either explicitly (``["T","null"]`` / ``anyOf [..., null]``) or because it
    constrains nothing at all: a bare ``{"description": "…"}`` is an unconstrained
    schema and ``null`` is a JSON value, so it validates. 68 live schemas are
    exactly that — an optional field with no type — and forcing them into
    ``required`` takes nothing away, which is why they are not a finding."""
    if not isinstance(node, dict):
        return False
    if is_nullable_union(node):
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
    author meant "absent". OpenAI documents exactly this ("emulate an optional
    parameter by using a union type with null"), and it costs one of Anthropic's
    16 union-parameter slots, which is the budget
    :func:`collapse_nullable_unions` then enforces."""
    if not isinstance(node, dict):
        return None
    if admits_null(node):
        return dict(node)
    out = dict(node)
    t = out.get("type")
    if isinstance(t, str):
        out["type"] = [t, "null"]
        if isinstance(out.get("enum"), list) and None not in out["enum"]:
            out["enum"] = [*out["enum"], None]
        return out
    if isinstance(t, list) and t:
        out["type"] = [*t, "null"]
        if isinstance(out.get("enum"), list) and None not in out["enum"]:
            out["enum"] = [*out["enum"], None]
        return out
    for combinator in ("anyOf", "oneOf"):
        branches = out.get(combinator)
        if isinstance(branches, list) and branches:
            out[combinator] = [*branches, {"type": "null"}]
            return out
    if isinstance(out.get("$ref"), str):
        # A `$ref` may carry no sibling constraints, so the union wraps it.
        wrapper: dict[str, Any] = {"anyOf": [{"$ref": out["$ref"]}, {"type": "null"}]}
        for key in ("title", "description"):
            if key in out:
                wrapper[key] = out[key]
        return wrapper
    if isinstance(out.get("enum"), list) and out["enum"]:
        if None not in out["enum"]:
            out["enum"] = [*out["enum"], None]
        return out
    # A node that declares its type only by SHAPE — `properties` with no
    # `"type"`, or `items` with no `"type"` — is still an object / an array, and
    # every rule in this module already reads it that way (`is_object_node`).
    # Naming the implied type is what lets it carry null.
    if isinstance(out.get("properties"), dict):
        out["type"] = ["object", "null"]
        return out
    if "items" in out:
        out["type"] = ["array", "null"]
        return out
    return None


def enforce_all_required(
    node: Any,
    *,
    express_optional_as_nullable: bool = False,
    notes: list[str] | None = None,
    _path: str = "$",
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
            widened = widen_to_nullable(sub)
            if widened is None:
                forced.append(f"{_path}.{name}")
            else:
                props[name] = widened
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
                _path=f"{_path}.{name}",
            )
    items = node.get("items")
    if isinstance(items, dict):
        enforce_all_required(
            items,
            express_optional_as_nullable=express_optional_as_nullable,
            notes=notes,
            _path=f"{_path}[]",
        )
    elif isinstance(items, list):
        for index, item in enumerate(items):
            enforce_all_required(
                item,
                express_optional_as_nullable=express_optional_as_nullable,
                notes=notes,
                _path=f"{_path}[{index}]",
            )
    for comb in ("anyOf", "oneOf", "allOf"):
        arr = node.get(comb)
        if isinstance(arr, list) and not _is_refinement_combinator(node, comb):
            for index, item in enumerate(arr):
                enforce_all_required(
                    item,
                    express_optional_as_nullable=express_optional_as_nullable,
                    notes=notes,
                    _path=f"{_path}.{comb}[{index}]",
                )
    defs = node.get("$defs") or node.get("definitions")
    if isinstance(defs, dict):
        for name, value in defs.items():
            enforce_all_required(
                value,
                express_optional_as_nullable=express_optional_as_nullable,
                notes=notes,
                _path=f"$defs.{name}",
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


def prune_optional_nulls(answer: Any, schema: Any, *, _path: str = "$") -> Any:
    """Return a copy of ``answer`` with every ``null`` REMOVED wherever the
    declared ``schema`` leaves that property optional and non-nullable.

    The reader's half of :func:`enforce_all_required`'s bargain. A provider that
    demands every property in ``required`` is answered with required+nullable, so
    the model says ``null`` where the author meant "absent" — and ``null`` is not
    a valid value under the declared contract. Dropping it restores exactly the
    answer the author's schema describes, so the declared contract can judge the
    answer without the boundary's compromise counting against the model.

    Only a ``null`` at a declared-optional, declared-non-nullable property is
    removed. A ``null`` the author DID allow is kept; a missing key stays missing.
    """
    if not isinstance(schema, dict):
        return answer
    if isinstance(answer, list):
        items = schema.get("items")
        if isinstance(items, dict):
            return [prune_optional_nulls(item, items, _path=f"{_path}[]") for item in answer]
        return answer
    if not isinstance(answer, dict):
        return answer
    props = schema.get("properties")
    if not isinstance(props, dict):
        return answer
    required = set(schema.get("required") or ())
    out: dict[str, Any] = {}
    for key, value in answer.items():
        sub = props.get(key)
        if (
            value is None
            and key not in required
            and isinstance(sub, dict)
            and not admits_null(sub)
        ):
            continue
        out[key] = (
            prune_optional_nulls(value, sub, _path=f"{_path}.{key}")
            if isinstance(sub, dict)
            else value
        )
    return out


__all__ = [
    "admits_null",
    "ANTHROPIC_UNION_PARAM_LIMIT",
    "classify_normalization_notes",
    "COMBINATOR_SAFE_SIBLINGS",
    "collapse_nullable_unions",
    "count_nullable_union_params",
    "count_union_params",
    "dedupe_identical_subtrees",
    "drop_refinement_combinators",
    "is_map_node",
    "is_nullable_union",
    "ref_cycles",
    "unroll_recursive_refs",
    "unresolvable_refs",
    "NORMALIZATION_NOTES_KEY",
    "KIND_KEY",
    "STRUCTURED_OUTPUT_UNSUPPORTED_KEYWORDS",
    "concretize_empty_schemas",
    "count_optional_properties",
    "enforce_additional_properties_false",
    "enforce_all_required",
    "optional_nonnullable_properties",
    "pins_one_value",
    "prune_optional_nulls",
    "widen_to_nullable",
    "flatten_allof",
    "hoist_nested_defs",
    "hoist_discriminator_first",
    "is_object_node",
    "is_root_object",
    "normalize_array_items",
    "normalize_combinator_siblings",
    "prune_unreachable_defs",
    "rewrite_const_as_enum",
    "rewrite_oneof_as_anyof",
    "strip_unsupported_keywords",
    "structured_output_schema_violations",
    "structured_output_size",
    "take_normalization_notes",
    "unsupported_structured_output_keywords",
]
