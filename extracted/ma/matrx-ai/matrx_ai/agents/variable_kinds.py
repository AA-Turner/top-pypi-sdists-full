"""THE AGENT-INPUT BRIDGE — ``variable_definitions`` ⇄ Content-IR kind fields.

The forward half of the agent consumer family. Agent OUTPUTS have been bound
for a while (``response_format_for_kind`` + the content contract); an agent's
INPUTS were untyped variables — a bag of strings with authoring metadata that
nothing downstream could validate, form-render, or gate.

This module is the FAITHFUL translator between the two, and it is a twin: the
same conversion exists in TypeScript at matrx-frontend
``features/content-ir/convert/kind-variable-bridge.ts``
(``variableDefinitionsToKindFields`` / ``kindFieldsToVariableDefinitions``).
A twin pinned to someone's READING of the contract drifts silently, so the two
are gated against a generated fixture — ``scripts/generate_variable_kind_fixture.py``
writes what THIS module actually produced and the TS suite asserts against it
(drift gate: ``packages/matrx-ai/tests/parity/test_variable_kind_fixture.py``).

FIDELITY MODEL (the A2 schema-expressivity constructs this depends on) — the
conversion is faithful along two channels, and NEITHER is allowed to swallow
the other:

- **STRUCTURE lives on the field schema.** Option sets with ``allowOther``
  (``enum.open``), defaults (``default``), help text (``description``),
  numeric bounds (``min``/``max``/``step``), multi-select option sets
  (``string[].values`` + ``open``), and ``toggleValues`` (a 2-value enum — the
  LABELS are the wire values).
- **PROVENANCE lives OUT OF BAND, in the sidecar.** Picklist bindings
  (``customComponent.structured_list``), scope-context bindings
  (``VariableDefinition.binding``), and WHICH input component renders the
  value. 🚨 These are NEVER flattened into the schema: a picklist binding in
  the schema would let a caller forge which LIST a value is drawn from, and
  the server resolves that from the agent row alone
  (``AgentVariable.picklist_binding`` / ``scope_binding``).

LOSS DISCIPLINE — a conversion never silently drops semantics. Every value-domain
narrowing that NEITHER the field NOR the sidecar can carry is returned as an
explicit :class:`BridgeLoss`. Authoring residue (``customComponent.stash``) is
uniformly not carried — it is a UI scratchpad, not semantics.

ROUND-TRIP LAW (tested, and cross-language) — for the CLEAN subset (non-nullable
string / number / boolean / enum / enum.open / bounded number / ``string[]`` +
values fields, ``required`` either true or absent, plus any sidecar entries),
fields → variables → fields is the identity with zero losses, and
variables → fields → variables reproduces the variable modulo the documented
normalizations (legacy ``picklist`` key → ``structured_list``, stash dropped,
zero-value defaults omitted).

THE PROMPT DOOR IS NOT TOUCHED. ``matrx_ai.agents.variables`` /
``matrx_ai.config.prompt_values`` remain the one lawful place a ``__kind``
marker is stripped on the way into a prompt (KINDS_EVERYWHERE_PLAN §4.2 door
1). This module never renders a prompt and never sees a runtime value — it
converts DECLARATIONS.

Contract + binding model: ``common-docs/systems/content-ir-system/KINDS_EVERYWHERE_PLAN.md``
§10d-C; ledger: ``aidream/docs/workflow/KIND_AGENT_INPUT_LEDGER.md``.
"""

from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, ConfigDict

#: The system discriminator. Not a field of any kind's field map.
KIND_KEY = "__kind"

#: helpText the FORWARD converter stamps on a scalar-array field flattened to
#: a textarea. Machine-stamped — never read back as a user description.
LIST_HELP_TEXT = "One per line."

_STRUCTURED_HELP_RE = re.compile(r"^Structured JSON \(.*\)\.$")

# The component families, mirrored from the TS twin.
_SELECT_FAMILY = frozenset(
    {"select", "radio", "pill-toggle", "selection-list", "buttons"}
)
_MEDIA_COMPONENTS = frozenset({"image", "audio", "video", "youtube", "document"})
_BOOLEAN_COMPONENTS = frozenset({"toggle", "light-switch"})
_NUMBER_COMPONENTS = frozenset({"number", "slider", "percent"})
#: Components whose VALUE is a plain string (textarea-compatible shapes). The
#: select family is included: an optionless / runtime-options select renders as
#: a select whose options hydrate elsewhere — its value is still a string.
_STRING_COMPONENTS = frozenset(
    {
        "textarea",
        "datetime",
        "time",
        "email",
        "url",
        "phone",
        "color",
        "markdown",
        "currency",
        "image",
        "audio",
        "video",
        "youtube",
        "document",
        "select",
        "radio",
        "pill-toggle",
        "selection-list",
        "buttons",
        "checkbox",
    }
)

_DUPLICATE_NAME_REASON = (
    "duplicate name — this definition overwrote an earlier field of the same name"
)


def structured_json_help_text(shape: str) -> str:
    """helpText stamped on a structured field flattened to a JSON textarea."""
    return f"Structured JSON ({shape})."


def is_synthetic_bridge_help_text(help_text: str) -> bool:
    """Is this helpText one the FORWARD converter synthesized for a flattened
    field (one-per-line list / structured-JSON textarea)?

    The reverse converter must not read a machine-stamped authoring hint back
    as a user ``description`` (or its JSON stub back as a user ``default``).
    """
    return help_text == LIST_HELP_TEXT or bool(_STRUCTURED_HELP_RE.match(help_text))


def sanitize_variable_name(value: str) -> str:
    """The variables system's canonical name rule (twin of
    matrx-frontend ``features/agents/utils/variable-utils.ts``).

    Trim → lowercase → spaces/dashes to ``_`` → drop everything outside
    ``[a-z0-9_]`` → collapse runs of ``_`` → strip leading/trailing ``_``.
    """
    lowered = value.strip().lower()
    underscored = re.sub(r"[\s-]+", "_", lowered)
    cleaned = re.sub(r"[^a-z0-9_]", "", underscored)
    return re.sub(r"_+", "_", cleaned).strip("_")


# ---------------------------------------------------------------------------
# Shapes
# ---------------------------------------------------------------------------


class BridgeLoss(BaseModel):
    """ONE recorded semantic narrowing. ``name`` is the variable it applies to."""

    model_config = ConfigDict(frozen=True)

    name: str
    reason: str


class KindFieldsConversion(BaseModel):
    """Result of a variables → kind conversion.

    ``fields`` is the kind's field map (name → field schema, the KindSchema
    ``fields`` shape). ``sidecar`` is the OUT-OF-BAND provenance per field
    (component identity, picklist binding, scope binding, orphaned
    ``allowOther``) — it never enters the schema. ``losses`` names every
    narrowing neither could carry.
    """

    fields: dict[str, dict[str, Any]]
    sidecar: dict[str, dict[str, Any]]
    losses: list[BridgeLoss]


# ---------------------------------------------------------------------------
# 1) VariableDefinitions → kind fields  (THE FORWARD BUILD — this chip)
# ---------------------------------------------------------------------------


def _read_structured_list(cc: dict[str, Any]) -> dict[str, Any] | None:
    """Canonical ``structured_list``; legacy ``picklist`` is a READ-ONLY alias."""
    for key in ("structured_list", "picklist"):
        value = cc.get(key)
        if isinstance(value, dict):
            return value
    return None


def _list_id(structured_list: dict[str, Any]) -> str:
    raw = structured_list.get("listId") or structured_list.get("list_id")
    return raw if isinstance(raw, str) else ""


def _has_scope_binding(entry: dict[str, Any]) -> bool:
    binding = entry.get("binding")
    return isinstance(binding, dict) and bool(
        binding.get("itemKey")
        or binding.get("item_key")
        or binding.get("contextItemId")
        or binding.get("context_item_id")
    )


def _is_zero_default(field: dict[str, Any], value: Any) -> bool:
    """The zero value the FORWARD converter emits for a field shape — an
    omission, never an authored default."""
    ftype = field.get("type")
    if ftype == "number":
        # `False` is not 0 here: a bool default on a number field is authored data.
        return value == "" or (value == 0 and not isinstance(value, bool))
    if ftype == "boolean":
        return value == "" or value is False
    return value == ""


def _canonical_component_for_field(field: dict[str, Any]) -> str:
    ftype = field.get("type")
    if ftype == "number":
        return "number"
    if ftype == "boolean":
        return "toggle"
    if ftype == "enum":
        return "select"
    if ftype == "string[]":
        return "checkbox" if "values" in field else "textarea"
    return "textarea"


def _convert_variable(
    entry: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any], list[str]]:
    """ONE variable definition → ``(field, sidecar_entry, loss_reasons)``."""
    losses: list[str] = []
    sidecar: dict[str, Any] = {}

    cc_raw = entry.get("customComponent")
    cc: dict[str, Any] = cc_raw if isinstance(cc_raw, dict) else {}
    ctype = cc.get("type") or "textarea"
    help_text = entry.get("helpText")
    synthetic_help = isinstance(help_text, str) and is_synthetic_bridge_help_text(
        help_text
    )

    def finish(core: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
        field = dict(core)
        if entry.get("required"):
            field["required"] = True
        if isinstance(help_text, str) and help_text != "" and not synthetic_help:
            field["description"] = help_text
        default = entry.get("defaultValue")
        if (
            default is not None
            and not _is_zero_default(field, default)
            and not synthetic_help
        ):
            field["default"] = default
        # Record the rendering component only when it deviates from the shape's
        # canonical one (media, slider, radio, …). Scope-bound variables inherit
        # their component from the bound context item — nothing to record.
        if (
            "scopeBinding" not in sidecar
            and cc_raw is not None
            and isinstance(cc_raw, dict)
            and ctype != _canonical_component_for_field(field)
        ):
            sidecar["component"] = ctype
        return field, sidecar, losses

    # PRECEDENCE: scope binding → picklist → component type.
    if _has_scope_binding(entry):
        # Runtime-filled from the active scope. The VALUE structure in kind
        # space is a string; the binding itself is provenance → sidecar.
        sidecar["scopeBinding"] = entry["binding"]
        return finish({"type": "string"})

    structured_list = _read_structured_list(cc)
    if structured_list is not None:
        # Normalized to the canonical key on the way out.
        sidecar["structuredList"] = structured_list
        options = [o for o in (cc.get("options") or []) if isinstance(o, str)]
        multiple = bool(structured_list.get("multiple"))
        if options and not multiple:
            # Cached static options ARE a real value domain — keep them.
            core: dict[str, Any] = {"type": "enum", "values": list(options)}
            if cc.get("allowOther"):
                core["open"] = True
            return finish(core)
        if cc.get("allowOther"):
            sidecar["allowOther"] = True
        losses.append(
            f"structured-list-bound (list {_list_id(structured_list)}) — "
            + ("multi-select, " if multiple else "")
            + "options resolve at run time; string in kind space "
            "(binding carried in the sidecar)"
        )
        return finish({"type": "string"})

    if ctype == "currency":
        losses.append("currency {amount, currency} — serialized string in kind space")
        return finish({"type": "string"})

    if ctype in _NUMBER_COMPONENTS:
        core = {"type": "number"}
        for src, dst in (("min", "min"), ("max", "max"), ("step", "step")):
            value = cc.get(src)
            if value is not None:
                core[dst] = value
        return finish(core)

    if ctype in _BOOLEAN_COMPONENTS:
        toggle_values = cc.get("toggleValues")
        if isinstance(toggle_values, (list, tuple)) and toggle_values:
            # toggleValues emit the LABELS as wire values — a 2-value enum is
            # the faithful structure.
            return finish({"type": "enum", "values": list(toggle_values)})
        return finish({"type": "boolean"})

    if ctype in _SELECT_FAMILY:
        options = [o for o in (cc.get("options") or []) if isinstance(o, str)]
        if not options:
            if cc.get("allowOther"):
                sidecar["allowOther"] = True
            losses.append(f"{ctype} has no static options — string in kind space")
            return finish({"type": "string"})
        core = {"type": "enum", "values": list(options)}
        if cc.get("allowOther"):
            core["open"] = True
        return finish(core)

    if ctype == "checkbox":
        options = [o for o in (cc.get("options") or []) if isinstance(o, str)]
        if options:
            core = {"type": "string[]", "values": list(options)}
            if cc.get("allowOther"):
                core["open"] = True
            return finish(core)
        if cc.get("allowOther"):
            sidecar["allowOther"] = True
        return finish({"type": "string[]"})

    if ctype in _STRING_COMPONENTS or ctype in _MEDIA_COMPONENTS:
        # String-valued components — component identity (when not textarea) is
        # an input-role annotation carried in the sidecar by `finish`.
        return finish({"type": "string"})

    # Unknown / future component type: string is the historical behavior, but
    # never silently — the gap is a loss, not a shrug.
    losses.append(
        f"unknown component type {ctype!r} — string in kind space; extend "
        "matrx_ai.agents.variable_kinds to keep schema fidelity"
    )
    return finish({"type": "string"})


def variable_definitions_to_kind_fields(
    variable_definitions: list[Any] | None,
) -> KindFieldsConversion:
    """Agent ``variable_definitions`` → kind field map + sidecar + losses.

    MAPPING TABLE (precedence: binding → picklist → component type; a variable
    with no ``customComponent`` is a textarea):

    ==========================================  =========================  ==========================
    variable definition                         field                      sidecar
    ==========================================  =========================  ==========================
    binding set (scope context item)            string                     scopeBinding
    picklist + static options + !multiple       enum {values} (+open)      structuredList
    picklist otherwise                          string (+LOSS)             structuredList (+allowOther)
    textarea / no customComponent               string                     —
    number / slider / percent (+min/max/step)   number {min,max,step}      component when not "number"
    toggle / light-switch                       boolean                    component when "light-switch"
    toggle / light-switch + toggleValues [a,b]  enum {values:[a,b]}        component
    select family + options                     enum {values} (+open)      component when not "select"
    select family without options               string (+LOSS)             component (+allowOther)
    checkbox + options                          string[] {values} (+open)  —
    checkbox without options                    string[]                   component (+allowOther)
    datetime/time/email/url/phone/color/…       string                     component
    currency                                    string (+LOSS)             component
    image/audio/video/youtube/document          string                     component
    ==========================================  =========================  ==========================

    Cross-cutting: ``helpText`` → ``description`` (except machine-stamped
    flattening hints); ``defaultValue`` → ``default`` verbatim except the
    shape's zero value; ``required: true`` → ``required: true``, otherwise
    omitted; ``customComponent.stash`` is never carried; duplicate names
    overwrite (last wins) and record a loss.
    """
    fields: dict[str, dict[str, Any]] = {}
    sidecar: dict[str, dict[str, Any]] = {}
    losses: list[BridgeLoss] = []
    for entry in variable_definitions or []:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            continue
        field, sidecar_entry, loss_reasons = _convert_variable(entry)
        losses.extend(BridgeLoss(name=name, reason=reason) for reason in loss_reasons)
        if field is None:
            continue
        if name in fields:
            losses.append(BridgeLoss(name=name, reason=_DUPLICATE_NAME_REASON))
        fields[name] = field
        if sidecar_entry:
            sidecar[name] = sidecar_entry
        else:
            # Last-wins for duplicates: a later entry without a sidecar clears
            # an earlier one, so fields and sidecar can never disagree.
            sidecar.pop(name, None)
    return KindFieldsConversion(fields=fields, sidecar=sidecar, losses=losses)


# ---------------------------------------------------------------------------
# 2) Kind fields → VariableDefinitions  (the twin of the shipped TS direction)
# ---------------------------------------------------------------------------


def _component_for(
    compatible: frozenset[str], canonical: str, sidecar: dict[str, Any]
) -> str:
    component = sidecar.get("component")
    return component if isinstance(component, str) and component in compatible else canonical


def _with_structured_list(
    cc: dict[str, Any], sidecar: dict[str, Any]
) -> dict[str, Any]:
    structured_list = sidecar.get("structuredList")
    if structured_list is None:
        return cc
    return {**cc, "structured_list": structured_list}


def _field_stub_value(field: dict[str, Any]) -> Any:
    """Zero/stub value for a field — used to build the pretty JSON stubs."""
    ftype = field.get("type")
    if ftype == "string":
        return ""
    if ftype == "number":
        return 0
    if ftype == "boolean":
        return False
    if ftype == "enum":
        values = field.get("values") or []
        return values[0] if values else ""
    if ftype in ("string[]", "number[]", "boolean[]", "json[]"):
        return []
    if ftype == "array":
        return [{KIND_KEY: kind} for kind in field.get("itemKinds") or []]
    if ftype == "json":
        return None
    if ftype == "object":
        return {KIND_KEY: field.get("kind")}
    if ftype == "inline_object":
        return {
            key: _field_stub_value(child)
            for key, child in (field.get("fields") or {}).items()
        }
    if ftype == "record":
        return {}
    if ftype == "union":
        scalars = field.get("scalars") or []
        if scalars:
            first = scalars[0]
            return 0 if first == "number" else False if first == "boolean" else ""
        kinds = field.get("kinds") or []
        return {KIND_KEY: kinds[0]} if kinds else ""
    return ""


def _structured_shape_label(field: dict[str, Any]) -> str:
    ftype = field.get("type")
    if ftype == "array":
        return f"array of {' | '.join(field.get('itemKinds') or [])}"
    if ftype == "object":
        return str(field.get("kind") or "")
    if ftype == "inline_object":
        return "inline object"
    if ftype == "record":
        return f"record of {field.get('values')}"
    if ftype == "union":
        parts = list(field.get("scalars") or []) + list(field.get("kinds") or [])
        return " | ".join(parts)
    if ftype == "json":
        return "any JSON value"
    if ftype == "json[]":
        return "array of any JSON values"
    return str(ftype)


def _field_to_variable_definition(
    name: str, field: dict[str, Any], sidecar: dict[str, Any]
) -> dict[str, Any]:
    ftype = field.get("type")
    tail: dict[str, Any] = {}
    if field.get("description") is not None:
        tail["helpText"] = field["description"]
    if field.get("required"):
        tail["required"] = True

    def default_or(zero: Any) -> Any:
        return field["default"] if "default" in field else zero

    # Scope-bound variables carry NO customComponent — it is inherited from the
    # bound context item.
    scope_binding = sidecar.get("scopeBinding")
    if scope_binding is not None:
        return {
            "name": name,
            "defaultValue": default_or(""),
            "binding": scope_binding,
            **tail,
        }

    if ftype == "string":
        component = _component_for(_STRING_COMPONENTS, "textarea", sidecar)
        cc: dict[str, Any] = {"type": component}
        # allowOther could not live on a plain string field — reattach it from
        # the sidecar onto option-bearing components.
        if sidecar.get("allowOther") and (
            component in _SELECT_FAMILY or component == "checkbox"
        ):
            cc["allowOther"] = True
        return {
            "name": name,
            "defaultValue": default_or(""),
            "customComponent": _with_structured_list(cc, sidecar),
            **tail,
        }

    if ftype == "number":
        cc = {"type": _component_for(_NUMBER_COMPONENTS, "number", sidecar)}
        for key in ("min", "max", "step"):
            if field.get(key) is not None:
                cc[key] = field[key]
        return {
            "name": name,
            "defaultValue": default_or(0),
            "customComponent": _with_structured_list(cc, sidecar),
            **tail,
        }

    if ftype == "boolean":
        return {
            "name": name,
            "defaultValue": default_or(False),
            "customComponent": _with_structured_list(
                {"type": _component_for(_BOOLEAN_COMPONENTS, "toggle", sidecar)},
                sidecar,
            ),
            **tail,
        }

    if ftype == "enum":
        values = list(field.get("values") or [])
        component = sidecar.get("component")
        # A 2-value enum whose sidecar names a toggle component came FROM
        # toggleValues — the two labels are the wire values.
        if component in _BOOLEAN_COMPONENTS and len(values) == 2:
            return {
                "name": name,
                "defaultValue": default_or(""),
                "customComponent": _with_structured_list(
                    {"type": component, "toggleValues": values}, sidecar
                ),
                **tail,
            }
        cc = {
            "type": _component_for(_SELECT_FAMILY, "select", sidecar),
            "options": values,
        }
        if field.get("open"):
            cc["allowOther"] = True
        return {
            "name": name,
            "defaultValue": default_or(""),
            "customComponent": _with_structured_list(cc, sidecar),
            **tail,
        }

    if ftype == "string[]":
        if "values" in field:
            cc = {"type": "checkbox", "options": list(field["values"] or [])}
            if field.get("open"):
                cc["allowOther"] = True
            return {
                "name": name,
                "defaultValue": default_or(""),
                "customComponent": _with_structured_list(cc, sidecar),
                **tail,
            }
        if sidecar.get("component") == "checkbox":
            cc = {"type": "checkbox"}
            if sidecar.get("allowOther"):
                cc["allowOther"] = True
            return {
                "name": name,
                "defaultValue": default_or(""),
                "customComponent": _with_structured_list(cc, sidecar),
                **tail,
            }
        # falls through to the one-per-line textarea flattening

    if ftype in ("string[]", "number[]", "boolean[]"):
        description = field.get("description")
        out = {
            "name": name,
            "defaultValue": default_or(""),
            "helpText": LIST_HELP_TEXT if description is None else description,
            "customComponent": {"type": "textarea"},
        }
        if field.get("required"):
            out["required"] = True
        return out

    # array / object / inline_object / record / union / json / json[] — the
    # HONEST flattening: a structured-JSON textarea, never a fake sub-form.
    if "default" not in field:
        stub_default = json.dumps(_field_stub_value(field), indent=2)
    elif isinstance(field["default"], str):
        stub_default = field["default"]
    else:
        stub_default = json.dumps(field["default"], indent=2)
    description = field.get("description")
    out = {
        "name": name,
        "defaultValue": stub_default,
        "helpText": structured_json_help_text(_structured_shape_label(field))
        if description is None
        else description,
        "customComponent": {"type": "textarea"},
    }
    if field.get("required"):
        out["required"] = True
    return out


def kind_fields_to_variable_definitions(
    fields: dict[str, dict[str, Any]],
    *,
    sidecar: dict[str, dict[str, Any]] | None = None,
    sanitize_names: bool = True,
) -> list[dict[str, Any]]:
    """Kind field map (+ sidecar) → agent variable definitions.

    The twin of matrx-frontend's shipped ``kindFieldsToVariableDefinitions``.
    A sidecar entry incompatible with the field's shape is ignored and the
    canonical component used — the field's STRUCTURE is authoritative.
    """
    side = sidecar or {}
    taken: set[str] = set()
    out: list[dict[str, Any]] = []
    for key, field in fields.items():
        name = key
        if sanitize_names:
            sanitized = sanitize_variable_name(key)
            name = key if sanitized == "" else sanitized
        if name in taken:
            n = 2
            while f"{name}_{n}" in taken:
                n += 1
            name = f"{name}_{n}"
        taken.add(name)
        out.append(_field_to_variable_definition(name, field, side.get(key, {})))
    return out


# ---------------------------------------------------------------------------
# 3) Kind fields → the registered JSON Schema
# ---------------------------------------------------------------------------


def _field_json_schema(field: dict[str, Any]) -> dict[str, Any]:
    """ONE field → its JSON Schema node (the flat agent-input subset)."""
    ftype = field.get("type")
    node: dict[str, Any]
    if ftype == "string":
        node = {"type": "string"}
    elif ftype == "number":
        node = {"type": "number"}
        for src, dst in (("min", "minimum"), ("max", "maximum"), ("step", "multipleOf")):
            if field.get(src) is not None:
                node[dst] = field[src]
    elif ftype == "boolean":
        node = {"type": "boolean"}
    elif ftype == "enum":
        values = list(field.get("values") or [])
        if field.get("open"):
            # OPEN enum — "one of these OR any string". anyOf keeps the option
            # set VISIBLE instead of widening to a bare string (the historical
            # information loss this bridge exists to end).
            node = {"anyOf": [{"type": "string", "enum": values}, {"type": "string"}]}
        else:
            node = {"type": "string", "enum": values}
    elif ftype == "string[]":
        if "values" in field:
            values = list(field.get("values") or [])
            items: dict[str, Any] = (
                {"anyOf": [{"type": "string", "enum": values}, {"type": "string"}]}
                if field.get("open")
                else {"type": "string", "enum": values}
            )
        else:
            items = {"type": "string"}
        node = {"type": "array", "items": items}
    elif ftype in ("number[]", "boolean[]"):
        node = {"type": "array", "items": {"type": ftype[:-2]}}
    else:
        # Structural field types cannot arise from a variable contract; a
        # permissive node is honest ("any JSON value") and never a silent lie.
        node = {}
    if field.get("nullable") and "type" in node:
        node["type"] = [node["type"], "null"]
    if field.get("description"):
        node["description"] = field["description"]
    if "default" in field:
        node["default"] = field["default"]
    return node


def agent_input_json_schema(
    fields: dict[str, dict[str, Any]], kind_slug: str | None = None
) -> dict[str, Any]:
    """The whole input contract as ONE JSON Schema.

    Deliberately the same posture as a Provision's derived offer schema
    (``aidream.services.mandates.provisions.derived_offer_schema``): a BARE
    Draft 2020-12 object schema — never the ``{name, schema, strict}``
    response-format wrapper, which is not a validating schema and makes every
    value pass. Required = the fields declared required.

    🚨 ``__kind`` IS ALWAYS DECLARED (THE SCHEMA LAW — KINDS_EVERYWHERE_PLAN
    §4.2a, Arman 2026-08-23). This function used to omit it on the reasoning
    that "an input contract is checked against values that arrive from forms
    and upstream nodes, which do not carry a marker" — but the schema it
    returns is ``additionalProperties: False``, so a value that DID carry one
    was REJECTED, and the omission leaned on the validator stripping the marker
    away. That is the exact class of defect the law exists to end: a schema
    with no place to put an identity is how a payload loses it.

    DECLARED BUT NOT REQUIRED, deliberately. An input value legitimately
    arrives from a human filling a form, and a form has no identity to supply;
    forcing one would make the platform invent identities rather than carry
    them. With ``kind_slug`` the declaration is a ``const`` — a marker that IS
    present must be the RIGHT one — so nothing can smuggle a foreign shape
    through an input contract while an unmarked form value still passes.
    """
    properties: dict[str, Any] = {}
    required: list[str] = []
    for name, field in fields.items():
        properties[name] = _field_json_schema(field)
        if field.get("required"):
            required.append(name)
    marker: dict[str, Any] = {
        "type": "string",
        "description": "The registered kind this payload is an instance of.",
    }
    if kind_slug:
        marker["const"] = kind_slug
    return {
        "type": "object",
        # Marker FIRST — the house convention, and what a streaming reader needs.
        "properties": {"__kind": marker, **properties},
        "required": required,
        "additionalProperties": False,
    }


def variable_definitions_to_kind(
    variable_definitions: list[Any] | None,
) -> tuple[KindFieldsConversion, dict[str, Any]]:
    """The whole bridge in one call: ``(conversion, json_schema)``."""
    conversion = variable_definitions_to_kind_fields(variable_definitions)
    return conversion, agent_input_json_schema(conversion.fields)


def kind_fields_signature(fields: dict[str, dict[str, Any]]) -> str:
    """A stable signature of a field map — two agents whose variable contract
    is genuinely the same shape produce the same string.

    This is what the promote-on-reuse binding model counts (§10d-C): a kind is
    minted only where a variable contract is REUSED, so the platform never ends
    up with 500 one-off names for 500 shapes nobody shares.
    """
    return json.dumps(
        {name: fields[name] for name in sorted(fields)},
        sort_keys=True,
        separators=(",", ":"),
    )


# ---------------------------------------------------------------------------
# 4) String-space → typed-space  (the twin of the FE's value layer)
# ---------------------------------------------------------------------------

#: The free-text channel that rides ALONGSIDE the declared variables in a live
#: `chat.conversation.variables` dict. It is the envelope's human text, not a
#: declared input — the same law Provisions state as "user_input can never be
#: an offered value". It is NEVER part of an input contract, and a checker that
#: forgets that rejects every real payload it sees.
USER_INPUT_VARIABLE_KEY = "__agent_user_input__"

_TRUE_WORDS = frozenset({"true", "yes", "on", "1"})
_FALSE_WORDS = frozenset({"false", "no", "off", "0"})

#: Sentinel for "the caller supplied nothing" — distinct from a `None` value.
OMITTED = object()


def _parse_boolean(text: str) -> bool | None:
    lowered = text.strip().lower()
    if lowered in _TRUE_WORDS:
        return True
    if lowered in _FALSE_WORDS:
        return False
    return None


def _split_lines(raw: str) -> list[str]:
    return [line.strip() for line in raw.split("\n") if line.strip()]


def coerce_to_kind_value(field: dict[str, Any], raw: Any) -> tuple[Any, str | None]:
    """ONE raw variable value → the field's kind-space type.

    Returns ``(value, error)``; ``value is OMITTED`` means the caller supplied
    nothing (blank), which is an OMISSION, not a failure — a required field
    then fails on the schema's own terms, where the error belongs.

    This exists because the agent runtime carries variable VALUES as strings
    everywhere (``AgentVariable.value``), so a real payload says ``"800"`` where
    the contract says ``number``. Checking a live payload against an input kind
    WITHOUT this step reports a fake failure on every numeric and boolean field.
    Twin of matrx-frontend ``features/content-ir/input/kind-input-values.ts``
    ``coerceInputValueToKindValue``.
    """
    if raw is None or (isinstance(raw, str) and raw.strip() == ""):
        return OMITTED, None
    ftype = field.get("type")

    if ftype in ("string", "enum"):
        # Value-domain membership for `enum` is the schema's job, not ours.
        return (raw if isinstance(raw, str) else json.dumps(raw)), None

    if ftype == "number":
        if isinstance(raw, (int, float)) and not isinstance(raw, bool):
            return raw, None
        try:
            text = str(raw).strip()
            return (int(text) if re.fullmatch(r"[+-]?\d+", text) else float(text)), None
        except ValueError:
            return None, f'"{raw}" is not a number'

    if ftype == "boolean":
        if isinstance(raw, bool):
            return raw, None
        parsed = _parse_boolean(str(raw))
        if parsed is None:
            return None, (
                f'"{raw}" is not a boolean (expected one of yes/no, true/false, on/off, 1/0)'
            )
        return parsed, None

    if ftype == "string[]":
        if isinstance(raw, list):
            return [str(item) for item in raw], None
        return _split_lines(str(raw)), None

    if ftype in ("number[]", "boolean[]"):
        lines = raw if isinstance(raw, list) else _split_lines(str(raw))
        out: list[Any] = []
        for index, line in enumerate(lines, start=1):
            if ftype == "number[]":
                try:
                    text = str(line).strip()
                    out.append(int(text) if re.fullmatch(r"[+-]?\d+", text) else float(text))
                except ValueError:
                    return None, f'line {index} ("{line}") is not a number'
            else:
                parsed = _parse_boolean(str(line))
                if parsed is None:
                    return None, f'line {index} ("{line}") is not a boolean'
                out.append(parsed)
        return out, None

    # Every structured field is a JSON textarea on the way out, so the way back
    # in is a JSON parse.
    if not isinstance(raw, str):
        return raw, None
    try:
        return json.loads(raw), None
    except ValueError as exc:
        return None, f"not valid JSON: {exc}"


class CoercedInstance(BaseModel):
    """A live variables dict rendered into the kind's typed space."""

    instance: dict[str, Any]
    coercion_errors: dict[str, str]
    omitted: list[str]
    #: Keys present in the payload that the contract does not declare. The
    #: user-input channel is NOT one of these — it is excluded by law.
    undeclared: list[str]


def coerce_variables_to_instance(
    fields: dict[str, dict[str, Any]], values: dict[str, Any]
) -> CoercedInstance:
    """A live ``{variable: value}`` payload → the kind instance it means.

    The user-input channel is excluded, never reported as undeclared.
    """
    instance: dict[str, Any] = {}
    errors: dict[str, str] = {}
    omitted: list[str] = []
    for name, field in fields.items():
        if name not in values:
            omitted.append(name)
            continue
        value, error = coerce_to_kind_value(field, values[name])
        if error is not None:
            errors[name] = error
        elif value is OMITTED:
            omitted.append(name)
        else:
            instance[name] = value
    undeclared = [
        key
        for key in values
        if key not in fields and key != USER_INPUT_VARIABLE_KEY
    ]
    return CoercedInstance(
        instance=instance,
        coercion_errors=errors,
        omitted=omitted,
        undeclared=undeclared,
    )
