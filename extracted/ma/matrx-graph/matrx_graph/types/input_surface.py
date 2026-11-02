"""THE workflow input surface — one flat, kind-addressed declaration.

Ruled design (Arman, 2026-08-27 — common-docs
``systems/workflows/INPUT-SURFACE.md``): a workflow's inputs are the union of
all fields across all of its ``io.user_input`` nodes PLUS its declared
variables (``Definition.variables`` FOLD IN — no separate species), compiled
to ONE name-unique surface. The surface — not any node — is what the outside
world addresses:

1. the run form (kind → component, auto-generated),
2. the programmatic API (callers pass name → value),
3. mandate delivery (a consumption map lands name → value into these slots),
4. the tool schema when an agent invokes the workflow as a tool.

Every input is a ``__kind``; every input carries exactly one sourcing rule
(``ask`` / ``require`` / ``optional``); every landed value is provenance-
stamped (``human`` / ``caller`` / ``mandate`` / ``default``). A name collision
across input nodes (or between a field and a declared variable) is a NAMED
compile refusal. A headless run missing a require/ask input parks
(``awaiting_input``), never dies.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, StringConstraints

SourcingRule = Literal["ask", "require", "optional"]

# Provenance sources, strongest first. ``pinned`` is a mandate delivery with
# lock strength (renders read-only); ``human`` may ONLY ever be stamped by the
# human-facing form path — THE source=human INVARIANT, enforced server-side
# where values land, never a convention.
InputSource = Literal["pinned", "human", "caller", "mandate", "default"]

# One precedence order — collisions between sources resolve exactly this way:
# pinned-mandate > human > caller > mandate-default > declared default.
SOURCE_PRECEDENCE: tuple[InputSource, ...] = ("pinned", "human", "caller", "mandate", "default")

# The plain-language value types an author picks from — for an io.user_input
# field AND for a declared workflow variable (one vocabulary, both doors). Each
# maps to a JSON Schema type + an AutoForm widget hint so the run form renders
# the right control.
UserInputFieldType = Literal["text", "long_text", "number", "yes_no", "choice", "file"]

# A PERSON'S DOOR into a reference input: the platform record type(s) — ``platform.entity_types``
# tokens — an id input points at. One type, or several when the input accepts more than one kind
# of record (a note OR a file): the run form offers one search-by-name picker over all of them.
EntityTypeToken = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]*$")]
EntityTypePicks = EntityTypeToken | list[EntityTypeToken]


def apply_picks_schema(schema: dict[str, Any], picks: str | list[str] | None, picks_type_into: str) -> None:
    """A picker over ``picks`` instead of a raw id box. Several types → ``ui:entity_type`` is the
    list; ``picks_type_into`` names the sibling input that receives the PICKED record's type token,
    so a workflow taking a (kind, id) pair is told which kind the person chose."""
    tokens = [picks] if isinstance(picks, str) else list(picks or [])
    if not tokens:
        return
    schema["ui:widget"] = "record_picker"
    schema["ui:entity_type"] = tokens[0] if len(tokens) == 1 else tokens
    if picks_type_into:
        schema["ui:entity_type_field"] = picks_type_into

# Kind slugs for the six legacy UserInputFieldType values. Each is a live
# ``content_ir.kind_definition`` row (verified 2026-08-27). Presentation nuance
# (long_text vs text, choice options, file pickers) is a VARIANT on the kind —
# never a second type system.
FIELD_TYPE_KINDS: dict[str, str] = {
    "text": "text",
    "long_text": "text",
    "number": "number",
    "yes_no": "boolean",
    "choice": "text",
    "file": "text",
}

# Default presentation-variant names for field types whose rendering differs
# from the kind's default component. Named variants live ON the kind in the
# kind registry (INPUT-SURFACE.md § Presentation variants); the input only
# SELECTS one by name.
#
# 🚨 THE REGISTRY IS THE ONE HOME FOR ANYTHING THAT RENDERS, so THIS TABLE
# CONFORMS TO THE REGISTRY — never the reverse. A name that is not a seeded
# variant on the accompanying kind is not "a variant the registry has yet to
# learn"; it is a silent degrade to the kind's default component, which is the
# worst outcome available: the form renders something plausible and wrong (a
# 3-option choice as a free-text box) with nothing logged. Every name below is
# pinned against the seed list by ``tests/test_input_surface_variant_registry``
# — add a name here only after it exists in the registry.
#
# ``file`` deliberately emits NO variant: the compiled kind for a file field is
# ``text`` (see FIELD_TYPE_KINDS) and the registry seeds no file variant on it.
# Emitting an unregistered "file" name bought nothing — the same degrade
# happened either way — while making the surface assert a variant that does not
# exist. File-typed inputs render through their kind's own component; when a
# real file kind is seeded, FIELD_TYPE_KINDS is what changes, not this table.
FIELD_TYPE_VARIANTS: dict[str, str | None] = {
    "text": None,
    "long_text": "textarea",  # kind text
    "number": None,
    "yes_no": None,
    "choice": "dropdown",  # kind text
    "file": None,
}


# THE INPUT HINTS (third-party services lane L6a, 2026-10-16 — common-docs
# ``projects/third-party-services/INPUT-HINTS.md``). How one input sits in the
# Google-simple arrangement: the one box, chips, a Tools-style reveal. Every
# hint is optional and absent means "infer"; the client planner
# (``@ai-matrx/chat/mandates/invoke/simple-box``) owns the inference so every
# client arranges one surface the same way.
ChoiceStyle = Literal["", "chips", "select"]
DetectType = Literal["handle", "url", "domain", "keyword", "email", "person_name", "phone"]


class InputHints(BaseModel):
    """Presentation hints for one input. Additive on every served shape; the
    authoring field (``UserInputField``) and the compiled ``InputSpec`` both
    carry it, so the compiler copies it across with ``hint_values``."""

    primary: bool = Field(default=False, description="This input is THE box (at most one).")
    advanced: bool | None = Field(
        default=None,
        description=(
            "True: behind the Tools reveal; False: always visible; None: inferred "
            "(optional, or required with a default, goes behind Tools)."
        ),
    )
    group: str = Field(default="", description="Tools-bar group label, e.g. 'Location'.")
    order: int | None = Field(default=None, description="Sort key within its zone.")
    choice_style: ChoiceStyle = Field(
        default="", description="Options as chips or a select; empty = chips up to six."
    )
    inline: bool = Field(
        default=False, description="A short choice attached to the primary box as a scope picker."
    )
    example: str = Field(default="", description="One realistic value; never a default.")
    option_labels: dict[str, str] = Field(
        default_factory=dict, description="Friendly words for machine option values."
    )
    detect: list[DetectType] = Field(
        default_factory=list, description="What the primary box accepts; drives smart detection."
    )
    required_in_form: bool = Field(
        default=False,
        description=(
            "A person must fill this in on the run form; callers (API, mandate, schedule) "
            "may still leave it empty. The form enforces it; the engine never does."
        ),
    )


# A LIST OF WORDS (review gap B2, 2026-10-29): a text input that takes several values is the
# registered ``string_list`` kind with its ``lines`` variant ("one per line"), so nobody has
# to name a kind to get a list. Both names are seeded in the registry (fixture pinned by
# ``tests/test_input_surface_variant_registry``).
LIST_KIND = "string_list"
LIST_VARIANT = "lines"
_LISTABLE_TYPES: frozenset[str] = frozenset({"text", "long_text"})


def compiled_kind_and_variant(
    field_type: str | None, *, multiple: bool = False, kind: str = "", variant: str = ""
) -> tuple[str, str | None]:
    """The (kind, variant) an input compiles to. A declared kind/variant wins; a several-values
    text input is a ``string_list`` with ``lines``; otherwise the field type's own pair."""
    declared_kind = (kind or "").strip()
    declared_variant = (variant or "").strip() or None
    if declared_kind:
        return declared_kind, declared_variant or (FIELD_TYPE_VARIANTS.get(field_type) if field_type else None)
    if multiple and (field_type or "text") in _LISTABLE_TYPES:
        return LIST_KIND, declared_variant or LIST_VARIANT
    if field_type is None:
        return "text", declared_variant
    return FIELD_TYPE_KINDS.get(field_type, "text"), declared_variant or FIELD_TYPE_VARIANTS.get(field_type)


# AN INPUT THAT NAMES A STRUCTURED KIND (gap 8, 2026-10-29): a field or variable whose declared
# kind is an object (a company candidate, an address) takes its value contract FROM THE KIND —
# the kind's schema, or a list of it when ``multiple`` — so the run form draws a structured
# editor and a real object is accepted instead of refused as "not of type 'string'".
#
# 🚨 A kind that is really a plain value never becomes an object. The kinds a field type
# already compiles to (``text`` is registered as ``{text: …}``, yet a text input's value is a
# string), ``json`` (no shape), a non-object schema, and a one-scalar wrapper (``markdown``,
# ``slug_result``…) keep the field type's plain contract. Only a text-typed declaration may
# take a kind's shape: a number, yes/no, choice or file says what its value is.
PLAIN_VALUE_KINDS: frozenset[str] = frozenset({*FIELD_TYPE_KINDS.values(), LIST_KIND, "json"})
_SCALAR_TYPES: frozenset[str] = frozenset({"string", "number", "integer", "boolean"})
KIND_SCHEMA_UNRESOLVED = "x-kind-schema-unresolved"


def structured_input_kind(kind: str | None, field_type: str | None) -> str | None:
    """The declared kind slug when it may give the input a structured value; else None."""
    slug = (kind or "").strip()
    if not slug or slug in PLAIN_VALUE_KINDS or (field_type or "text") not in _LISTABLE_TYPES:
        return None
    return slug


def structured_value_schema(kind_schema: Any) -> dict[str, Any] | None:
    """The value contract a structured kind gives one input value, or None when the kind's
    value is plain (see ``PLAIN_VALUE_KINDS``). The ``__kind`` marker is never required of a
    value a person or caller types."""
    if not isinstance(kind_schema, dict) or kind_schema.get("type") != "object":
        return None
    props = kind_schema.get("properties")
    names = [n for n in (props if isinstance(props, dict) else {}) if n != "__kind"]
    # A map kind (names → values, ``key_value_map``) declares no field of its own but a typed
    # ``additionalProperties``: its value is an object too. An object with neither has no shape.
    extra = kind_schema.get("additionalProperties")
    if not names and not (isinstance(extra, dict) and extra):
        return None
    if len(names) == 1 and isinstance(props[names[0]], dict) and props[names[0]].get("type") in _SCALAR_TYPES:
        return None
    schema = {k: v for k, v in kind_schema.items() if k not in ("title", "description", "$schema", "$id")}
    if isinstance(schema.get("required"), list):
        schema["required"] = [n for n in schema["required"] if n != "__kind"]
        if not schema["required"]:
            schema.pop("required")
    return schema


def kind_value_schema(
    kind: str | None, field_type: str | None, *, multiple: bool, name: str
) -> tuple[dict[str, Any] | None, bool]:
    """``(value schema, known)`` for an input declaring ``kind``. Synchronous: reads only the
    kind cache (``kinds.cached_kind_schema``). ``(None, True)`` = a plain value; ``(None,
    False)`` = a structured-looking kind this process has not resolved yet — the caller keeps
    the plain contract and flags it (``warm_input_kinds`` before compiling avoids it; the run
    judges the value against the kind either way)."""
    slug = structured_input_kind(kind, field_type)
    if slug is None:
        return None, True
    from matrx_graph.kinds import cached_kind_schema

    value = structured_value_schema(cached_kind_schema(slug))
    if value is None:
        return None, cached_kind_schema(slug) is not None
    # Each fragment is its own schema resource, so the kind's ``#/$defs/…`` references resolve
    # inside it — served alone (the run form) or embedded in a step's whole output schema.
    defs = value.pop("$defs", None)
    shaped: dict[str, Any] = {"type": "array", "items": value} if multiple else value
    if defs is not None:
        shaped["$defs"] = defs
    shaped["$id"] = f"urn:matrx:input:{name}"
    return shaped, True


def apply_kind_value_schema(
    prop: dict[str, Any], kind: str | None, field_type: str | None, *, multiple: bool, name: str
) -> dict[str, Any]:
    """``prop`` (one input's plain contract) with its value shape taken from a structured kind;
    an unresolved one stays plain and carries ``KIND_SCHEMA_UNRESOLVED`` naming the kind."""
    shaped, known = kind_value_schema(kind, field_type, multiple=multiple, name=name)
    if shaped is not None:
        for key in ("type", "items", "enum", "ui:widget"):
            prop.pop(key, None)
        prop.update(shaped)
    elif not known:
        slug = (kind or "").strip()
        prop[KIND_SCHEMA_UNRESOLVED] = slug
        _warn_unresolved(slug, name)
    return prop


_UNRESOLVED_WARNED: set[str] = set()


def _warn_unresolved(slug: str, name: str) -> None:
    if slug in _UNRESOLVED_WARNED:
        return
    _UNRESOLVED_WARNED.add(slug)
    import logging

    logging.getLogger(__name__).warning(
        "input '%s' declares kind '%s', which this process has not resolved: its compiled "
        "contract stays the plain type (flagged %s) until the kind is warmed "
        "(matrx_graph.warm_input_kinds); the run still judges the value against the kind.",
        name,
        slug,
        KIND_SCHEMA_UNRESOLVED,
    )


HINT_FIELDS: tuple[str, ...] = tuple(InputHints.model_fields)


def hint_values(source: Any) -> dict[str, Any]:
    """The hint fields of any model carrying them, for copying onto a served shape."""
    return {name: getattr(source, name) for name in HINT_FIELDS if hasattr(source, name)}


class InputSpec(InputHints):
    """One entry of the compiled workflow input surface."""

    model_config = ConfigDict(frozen=True)

    name: str
    kind: str = Field(description="content_ir kind slug — every input IS a kind.")
    sourcing: SourcingRule = "optional"
    variant: str | None = Field(
        default=None,
        description=(
            "Named presentation variant registered ON the kind, selected by "
            "name. Never an ad-hoc component on the input."
        ),
    )
    default: JsonValue = None
    label: str = ""
    help: str = ""
    placeholder: str = ""
    options: list[str] = Field(default_factory=list)
    # Where the input came from: an io.user_input node field ("field") or a
    # folded Definition.variables declaration ("variable"). Compat plumbing —
    # dies with the $var migration.
    origin: Literal["field", "variable"] = "field"
    # The declaring io.user_input node + its field key (origin="field") so the
    # engine can seed the node's payload from surface values. None for folded
    # variables (they resolve through the substitution pass, not node seeds).
    node_id: str | None = None
    field_key: str | None = None
    json_schema: dict[str, Any] = Field(  # api-any-ok: per-input JSON Schema fragment
        default_factory=dict,
        description="The value-contract fragment (from the node's effective schema).",
    )
    # Park-gate qualifiers, computed at compile time so the gate never
    # blocks a run that would have satisfied the input another way:
    # ``referenced`` is False for a folded variable no marker references
    # (nothing consumes it, so its absence cannot break the run);
    # ``edge_fed`` is True for a field whose declaring input node has an
    # inbound routable edge (the value can arrive mid-run over the edge).
    referenced: bool = True
    edge_fed: bool = False


def missing_value(value: Any) -> bool:
    """The one definition of 'no value landed' for sourcing-rule checks.

    ``None`` and ``""`` are missing (matches the io.user_input executor's
    required-field posture); ``False``, ``0``, ``[]`` are real values.
    """
    return value is None or value == ""


def unsatisfied_inputs(
    surface: dict[str, InputSpec],
    values: dict[str, Any],
    provenance: dict[str, str] | None = None,
) -> list[InputSpec]:
    """The surface entries that BLOCK a start, per their sourcing rules.

    - ``require``: satisfied by a value from ANY source, including a declared
      default (defaults are the weakest precedence rung, but they count).
    - ``ask``: a human answers every time — satisfied ONLY by a value whose
      provenance stamp is ``human``. A default or caller value never
      satisfies an ask.
    - ``optional``: never blocks.
    """
    prov = provenance or {}
    gaps: list[InputSpec] = []
    for name, spec in surface.items():
        if spec.sourcing == "optional":
            continue
        if spec.edge_fed or (spec.origin == "variable" and not spec.referenced):
            continue
        value = values.get(name)
        if missing_value(value) and not missing_value(spec.default):
            value = spec.default
        if spec.sourcing == "require":
            if missing_value(value):
                gaps.append(spec)
        elif spec.sourcing == "ask":
            if missing_value(values.get(name)) or prov.get(name) != "human":
                gaps.append(spec)
    return gaps
