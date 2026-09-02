"""Faithful ``variable_definitions`` → tool-parameter conversion (W3-A).

Replaces the lossy ``_variable_definitions_to_parameters`` in
``matrx_ai.tools.agent_projection`` (everything → bare string) with the same
semantics as matrx-frontend's kind-variable bridge
(``features/content-ir/convert/kind-variable-bridge.ts``): option sets,
open-enum (``allowOther``) semantics, defaults, descriptions, numeric
bounds, and multi-select items enums all survive into the projected tool
schema the calling model sees.

Output notation: the ``ToolDefinition.parameters`` internal ``key → property
dict`` shape consumed by ``ToolDefinition._build_json_schema`` (see
tools/models.py). Constructs used: ``type`` / ``description`` / ``required``
(bool) / ``default`` / ``enum`` / ``minimum`` / ``maximum`` / ``multipleOf``
/ ``items`` / ``anyOf`` (open enums — ``anyOf: [{enum…}, {string}]``).

WIRE COMPATIBILITY — the agent runtime treats variable VALUES as strings
everywhere (``AgentVariable.value: str``). Non-string args are safe because
dispatch (``agent_tool._merge_projected_variables``) ``json.dumps``-es any
non-string value before it becomes a variable ("5" for numbers,
"true"/"false" for booleans, a JSON array string for checkbox lists) — so
this module changes SCHEMA fidelity only, never runtime value handling.
Where a component's wire value is itself a string artifact (picklist
reference fences, media URL/file_id, toggleValues labels), the parameter
stays string-typed and says so in its description.

PROVENANCE STAYS OUT-OF-BAND: picklist bindings
(``customComponent.structured_list``/legacy ``picklist``) and scope bindings
(``binding``) are resolved server-side from the agent row
(``AgentVariable.picklist_binding`` / ``scope_binding``) — they shape the
parameter's description, never a schema construct the caller could forge.
"""

from __future__ import annotations

from typing import Any

# The select-family components — an option set the user picks ONE value from.
_SELECT_FAMILY = {"select", "radio", "pill-toggle", "selection-list", "buttons"}

# Media components — the wire value is a string reference (URL / file_id).
_MEDIA_COMPONENTS = {"image", "audio", "video", "youtube", "document"}

# String-shaped scalar input components (value is a plain string).
_STRING_COMPONENTS = {
    "textarea",
    "markdown",
    "datetime",
    "time",
    "email",
    "url",
    "phone",
    "color",
    "currency",
}


def _base_parameter(entry: dict[str, Any]) -> dict[str, Any]:
    """description / required / default — shared by every component mapping.

    ``defaultValue`` is carried verbatim when non-empty; the FE's zero values
    ("" / 0 / False) are omissions, not authored defaults.
    """
    param: dict[str, Any] = {
        "description": entry.get("helpText") or "",
        "required": bool(entry.get("required", False)),
    }
    default = entry.get("defaultValue")
    if default not in (None, "", 0, False):
        param["default"] = default
    return param


def _with_note(param: dict[str, Any], note: str) -> dict[str, Any]:
    """Append a runtime note to the parameter description."""
    desc = str(param.get("description") or "")
    param["description"] = f"{desc} {note}".strip() if desc else note
    return param


def variable_definition_to_parameter(entry: dict[str, Any]) -> dict[str, Any]:
    """One ``variable_definitions`` JSONB entry → one internal parameter dict.

    Mirrors the frontend bridge's structure channel exactly:

    ==============================================  =================================
    variable definition                             parameter
    ==============================================  =================================
    binding set (scope context item)                string (+resolved-at-runtime note)
    picklist-bound (structured_list / picklist)     string enum from cached options
                                                    when static + single-select
                                                    (anyOf-open with allowOther),
                                                    else string + runtime note
    select family + options, no allowOther          {"type": "string", "enum": […]}
    select family + options + allowOther            {"anyOf": [{enum…}, {string}]}
    select family without options                   string
    checkbox + options                              array, items string enum
                                                    (items anyOf-open on allowOther)
    checkbox without options                        array of strings
    toggle / light-switch + toggleValues [a, b]     {"type": "string", "enum": [a, b]}
                                                    — the labels ARE the wire values
    toggle / light-switch plain                     boolean (dispatch json.dumps →
                                                    "true"/"false" on the wire)
    number / slider (+min/max/step)                 number + minimum/maximum/multipleOf
    percent                                         number, 0–100
    media (image/audio/video/youtube/document)      string (URL / file_id note)
    textarea / typed string components / currency   string
    ==============================================  =================================
    """
    param = _base_parameter(entry)

    binding = entry.get("binding")
    if isinstance(binding, dict) and (
        binding.get("itemKey")
        or binding.get("item_key")
        or binding.get("contextItemId")
        or binding.get("context_item_id")
    ):
        # Scope-context binding — the server usually fills this from the
        # active scope; a caller-supplied value participates per resolution
        # rules. String on the wire either way.
        param["type"] = "string"
        return _with_note(
            param,
            "(Usually auto-filled from the active scope context; provide only to override.)",
        )

    cc = entry.get("customComponent")
    cc = cc if isinstance(cc, dict) else {}
    ctype = cc.get("type") or "textarea"
    options = [o for o in (cc.get("options") or []) if isinstance(o, str)]
    allow_other = bool(cc.get("allowOther"))

    structured_list = cc.get("structured_list") or cc.get("picklist")
    if isinstance(structured_list, dict) and structured_list.get("listId"):
        multiple = bool(structured_list.get("multiple"))
        if options and not multiple:
            # Cached static options are a real value domain.
            if allow_other:
                param["anyOf"] = [
                    {"type": "string", "enum": list(options)},
                    {"type": "string"},
                ]
            else:
                param["type"] = "string"
                param["enum"] = list(options)
            return param
        param["type"] = "string"
        return _with_note(
            param,
            "(Options resolve from a bound list at run time"
            + ("; multiple selections allowed" if multiple else "")
            + ".)",
        )

    if ctype in _SELECT_FAMILY:
        if not options:
            param["type"] = "string"
            return param
        if allow_other:
            # OPEN enum — "one of these options OR any string". anyOf keeps
            # the option set visible to the provider instead of widening to
            # a bare string (the historical information loss this module
            # exists to fix).
            param["anyOf"] = [
                {"type": "string", "enum": list(options)},
                {"type": "string"},
            ]
            return param
        param["type"] = "string"
        param["enum"] = list(options)
        return param

    if ctype == "checkbox":
        # Multi-select. A list arg is json.dumps-ed into the variable by
        # dispatch — schema-typed here, string on the wire (see module doc).
        param["type"] = "array"
        if options and allow_other:
            param["items"] = {
                "anyOf": [
                    {"type": "string", "enum": list(options)},
                    {"type": "string"},
                ]
            }
        elif options:
            param["items"] = {"type": "string", "enum": list(options)}
        else:
            param["items"] = {"type": "string"}
        return param

    if ctype in ("toggle", "light-switch"):
        toggle_values = cc.get("toggleValues")
        if (
            isinstance(toggle_values, (list, tuple))
            and len(toggle_values) == 2
            and all(isinstance(v, str) for v in toggle_values)
        ):
            # toggleValues LABELS are the wire values — a 2-value string
            # enum, never a boolean.
            param["type"] = "string"
            param["enum"] = list(toggle_values)
            return param
        # Plain boolean toggle. WIRE-COMPAT: dispatch json.dumps a boolean
        # arg to "true"/"false" before it becomes the (string) variable.
        param["type"] = "boolean"
        return param

    if ctype in ("number", "slider", "percent"):
        # WIRE-COMPAT: dispatch json.dumps a numeric arg to its decimal
        # string before it becomes the (string) variable.
        param["type"] = "number"
        min_v = 0 if ctype == "percent" else cc.get("min")
        max_v = 100 if ctype == "percent" else cc.get("max")
        step_v = cc.get("step")
        if isinstance(min_v, (int, float)) and not isinstance(min_v, bool):
            param["minimum"] = min_v
        if isinstance(max_v, (int, float)) and not isinstance(max_v, bool):
            param["maximum"] = max_v
        if isinstance(step_v, (int, float)) and not isinstance(step_v, bool):
            param["multipleOf"] = step_v
        return param

    if ctype in _MEDIA_COMPONENTS:
        param["type"] = "string"
        return _with_note(param, f"(A {ctype} reference — URL or file id.)")

    # textarea, typed string scalars, currency, and anything unrecognized:
    # a plain string parameter (the system default input).
    if ctype not in _STRING_COMPONENTS and ctype != "textarea":
        # Unknown / future component types stay string — the historical
        # behavior — but never silently: surface the gap in server logs.
        from matrx_utils import vcprint

        vcprint(
            f"[variable_schema] Unknown variable component type {ctype!r} "
            f"on variable {entry.get('name')!r} — projected as string. "
            "Extend variable_definition_to_parameter to keep schema fidelity.",
            color="yellow",
        )
    param["type"] = "string"
    return param


def variable_definitions_to_parameters(
    variable_definitions: list | None,
    *,
    auto_input_description: str,
) -> dict[str, Any]:
    """Translate an agent's ``variable_definitions`` JSONB into the internal
    ``parameters`` dict for a projected agent tool, with full schema fidelity
    per :func:`variable_definition_to_parameter`.

    Every projected agent accepts a free-text task alongside its declared
    variables (``auto_input_description`` is the exact constant dispatch uses
    to tell the auto param from an author-declared variable named "input" —
    see ``agent_projection.AUTO_INPUT_DESCRIPTION``). A declared variable
    literally named "input" wins.
    """
    params: dict[str, Any] = {
        "input": {
            "type": "string",
            "description": auto_input_description,
            "required": False,
        }
    }
    for entry in variable_definitions or []:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        if not name:
            continue
        params[name] = variable_definition_to_parameter(entry)
    return params
