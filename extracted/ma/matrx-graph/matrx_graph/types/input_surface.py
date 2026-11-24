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

import re
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, StringConstraints

from matrx_graph.input_declaration import VariableDefinition
from matrx_graph.input_declaration.upgrade import DEFINITION_KIND, KIND_KEY, upgrade_workflow_input

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


ChoiceStyle = Literal["", "chips", "select"]
DetectType = Literal["handle", "url", "domain", "keyword", "email", "person_name", "phone"]


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


class InputSpec(BaseModel):
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
    # EVERYTHING A PERSON READS (label, help, placeholder, options, hints, choice style, the
    # component) lives ONLY here — the one input declaration; read it through the reader API
    # above (``input_hint``, ``input_options``…), never copy a field of it onto this model.
    declaration: VariableDefinition


# ---------------------------------------------------------------------------
# THE READER API over the one input declaration (``VariableDefinition``).
#
# Every engine behaviour that once read the old per-door copies (a workflow variable, a step
# form field, its hint block) reads the declaration through these functions — nothing else
# interprets ``customComponent`` / ``hints``. Old stored shapes enter ONLY through
# ``upgrade_workflow_input`` (``declared_input``).
# ---------------------------------------------------------------------------

_TEXT_COMPONENTS = frozenset({"text", "markdown", "email", "url", "phone", "record"})
_NUMBER_COMPONENTS = frozenset({"number", "slider", "percent", "currency"})
_YES_NO_COMPONENTS = frozenset({"toggle", "light-switch"})
_CHOICE_COMPONENTS = frozenset({"select", "pill-toggle", "checkbox", "radio", "selection-list", "buttons"})
_FILE_COMPONENTS = frozenset({"document", "image", "audio", "video", "youtube"})

_HINT_DEFAULTS: dict[str, Any] = {
    "primary": False,
    "advanced": None,
    "group": "",
    "order": None,
    "inline": False,
    "example": "",
    "detect": [],
    "required_in_form": False,
    "placeholder": "",
    "written_with": "",
}
_HINT_KEYS: dict[str, str] = {"required_in_form": "requiredInForm", "written_with": "writtenWith"}


def _flatten_tokens(tokens: Any) -> list[str]:
    out: list[str] = []
    for token in tokens or []:
        token = getattr(token, "root", token)
        if isinstance(token, list | tuple):
            out.extend(_flatten_tokens(token))
        elif token:
            out.append(str(token))
    return out


def declared_input(raw: Any) -> VariableDefinition:
    """One stored input in ANY shape -> the declaration. A ``VariableDefinition`` is itself; a dict
    already carrying ``__kind == "variable_definition"`` is validated as is; any other dict is an
    old-shape workflow variable or ``io.user_input`` field and is read ONLY through
    ``upgrade_workflow_input``."""
    if isinstance(raw, VariableDefinition):
        return raw
    if not isinstance(raw, dict):
        raise TypeError(f"an input declaration is a dict or VariableDefinition, got {type(raw).__name__}")
    data = raw if raw.get(KIND_KEY) == DEFINITION_KIND else upgrade_workflow_input(raw)
    component = data.get("customComponent")
    if isinstance(component, dict) and isinstance(component.get("tokens"), list):
        # The converter nests a list ``picks`` one level too deep; the schema takes flat tokens.
        flat = _flatten_tokens(component["tokens"])
        data = {**data, "customComponent": {**component, "tokens": flat}}
    return VariableDefinition.model_validate(data)


def declared_inputs(raw_list: Any) -> list[VariableDefinition]:
    return [declared_input(item) for item in (raw_list or [])]


_INPUT_NAME = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def check_input_name(name: str) -> str:
    """An input's name is a short id: letters, digits, underscore, not starting with a digit."""
    if not _INPUT_NAME.match(name or ""):
        raise ValueError(
            f"input name '{name}' must be letters, digits and underscore, not starting with a digit"
        )
    return name


def _component(d: VariableDefinition) -> Any:
    return d.customComponent


def _component_type(d: VariableDefinition) -> str:
    component = _component(d)
    return (component.type or "") if component is not None else ""


def input_type(d: VariableDefinition) -> UserInputFieldType | None:
    """The engine's plain-language type, from ``customComponent.type``; None = free-form JSON."""
    ctype = _component_type(d)
    if ctype in _TEXT_COMPONENTS:
        return "text"
    if ctype == "textarea":
        return "long_text"
    if ctype in _NUMBER_COMPONENTS:
        return "number"
    if ctype in _YES_NO_COMPONENTS:
        return "yes_no"
    if ctype in _CHOICE_COMPONENTS:
        return "choice"
    if ctype in _FILE_COMPONENTS:
        return "file"
    if ctype:
        return "text"
    if (d.valueKind or "") == "json":
        return None
    value = d.defaultValue
    if isinstance(value, bool):
        return "yes_no"
    if isinstance(value, int | float):
        return "number"
    if isinstance(value, dict | list):
        return None
    return "text"


def input_multiple(d: VariableDefinition) -> bool:
    component = _component(d)
    if component is None:
        return False
    return bool(component.multiple) or component.type == "checkbox"


def input_picks(d: VariableDefinition) -> str | list[str] | None:
    """The record type tokens a ``record`` input points at: one -> a string, several -> a list."""
    component = _component(d)
    if component is None or component.type != "record":
        return None
    tokens = _flatten_tokens(component.tokens)
    if not tokens:
        return None
    return tokens[0] if len(tokens) == 1 else tokens


def input_picks_type_into(d: VariableDefinition) -> str:
    component = _component(d)
    return str(getattr(component, "picksTypeInto", None) or "") if component is not None else ""


def input_options(d: VariableDefinition) -> list[str]:
    component = _component(d)
    return list(component.options or []) if component is not None else []


def input_option_labels(d: VariableDefinition) -> dict[str, str]:
    component = _component(d)
    labels = (component.optionLabels or {}) if component is not None else {}
    return {str(k): str(v) for k, v in labels.items()}


def input_accept(d: VariableDefinition) -> str:
    component = _component(d)
    return (component.accept or "") if component is not None else ""


def input_choice_style(d: VariableDefinition) -> ChoiceStyle:
    ctype = _component_type(d)
    return "chips" if ctype == "pill-toggle" else "select" if ctype == "select" else ""


def input_hint(d: VariableDefinition, key: str) -> Any:  # api-any-ok: one hint, typed by its key
    """One presentation hint by the OLD snake_case key; the old default when unset."""
    if key not in _HINT_DEFAULTS:
        raise KeyError(f"no input hint named '{key}'")
    hints = d.hints
    value = getattr(hints, _HINT_KEYS.get(key, key), None) if hints is not None else None
    if value is None:
        default = _HINT_DEFAULTS[key]
        return list(default) if isinstance(default, list) else default
    return list(value) if isinstance(value, list) else value


def input_is_bound(d: VariableDefinition) -> bool:
    """True when the value is filled from table data (a merge-field binding)."""
    binding = d.binding
    return binding is not None and getattr(binding, "kind", None) == "merge_field"


def input_binding_dict(d: VariableDefinition) -> dict[str, Any]:  # api-any-ok: the resolver's binding payload
    """The merge-field binding as the plain dict the host's one resolver takes ({} when unbound)."""
    if not input_is_bound(d) or d.binding is None:
        return {}
    dumped = d.binding.model_dump(mode="json", exclude_none=True)
    dumped.pop(KIND_KEY, None)
    return dumped


def variable_sourcing(d: VariableDefinition) -> str:
    """A declared variable's sourcing: explicit wins; then ``required``; else a variable with no
    default must be supplied (require) and one with a default never blocks (optional)."""
    if d.sourcing:
        return d.sourcing
    if d.required is not None:
        return "require" if d.required else "optional"
    return "require" if d.defaultValue is None else "optional"


def input_label(d: VariableDefinition) -> str:
    """What a person reads: the label, else the name."""
    return d.label or d.name


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
