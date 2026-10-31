"""Bring a stored input up to the one input declaration — THE named normalizations.

Two doors, one target shape (``schema/variable_definition.schema.json``):

* ``upgrade_agent_variable(raw)`` — an element of ``agent.definition(.version)/template
  .variable_definitions`` as stored before the kind existed.
* ``upgrade_workflow_input(raw)`` — a workflow ``VariableSpec`` (``workflow.definition(.version)
  .variables``) or an ``io.user_input`` ``UserInputField`` (node ``data.config.fields``).

Pure functions on dicts: they never drop information the schema can hold, never invent a value,
and return a NEW dict. The data lane's backfill and every tolerant reader call these — nothing
else restates a mapping. The field-by-field table lives in ``FEATURE.md`` beside this file.
"""

from __future__ import annotations

import copy
from typing import Any

KIND_KEY = "__kind"
DEFINITION_KIND = "variable_definition"
COMPONENT_KIND = "variable_component"
CONTEXT_BINDING_KIND = "variable_context_binding"
RECORD_BINDING_KIND = "variable_record_binding"

CHOICE_TYPES = frozenset({"radio", "pill-toggle", "selection-list", "buttons", "checkbox", "select"})
TOGGLE_TYPES = frozenset({"toggle", "light-switch"})
NUMERIC_TYPES = frozenset({"number", "slider", "percent", "currency"})
TEXT_TYPES = frozenset({"textarea", "text", "markdown", "email", "url", "phone"})
MEDIA_TYPES = frozenset({"image", "audio", "video", "youtube", "document"})

#: Which component types may carry each setting (mirrors the schema's allOf; the schema test pins
#: the two together so they cannot drift). ``pick_list`` is on every type by design: it is kept
#: outside ``stash`` so it survives type switches.
SETTING_TYPES: dict[str, frozenset[str]] = {
    "options": CHOICE_TYPES,
    "allowOther": CHOICE_TYPES,
    "optionLabels": CHOICE_TYPES,
    "assignment": CHOICE_TYPES,
    "toggleValues": TOGGLE_TYPES,
    "min": NUMERIC_TYPES,
    "max": NUMERIC_TYPES,
    "step": NUMERIC_TYPES,
    "unit": NUMERIC_TYPES,
    "resource_context": MEDIA_TYPES,
    "imageRole": MEDIA_TYPES,
    "accept": MEDIA_TYPES,
    "multiple": TEXT_TYPES | MEDIA_TYPES | {"record"},
    "tokens": frozenset({"record"}),
}
STASHABLE = ("options", "allowOther", "optionLabels", "toggleValues", "min", "max", "step", "unit",
             "accept", "multiple", "tokens")
_LEGACY_PICK_LIST_KEYS = ("structured_list", "picklist")
_HINT_KEYS = {  # workflow InputHints / UserInputField key -> hints key
    "primary": "primary", "advanced": "advanced", "group": "group", "order": "order",
    "inline": "inline", "placeholder": "placeholder", "example": "example", "detect": "detect",
    "required_in_form": "requiredInForm",
}


def _empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def stamp_binding(binding: Any) -> Any:
    """Stamp a binding's ``__kind`` from its own discriminant (merge_field -> record binding)."""
    if not isinstance(binding, dict):
        return binding
    out = dict(binding)
    slug = RECORD_BINDING_KIND if out.get("kind") == "merge_field" else CONTEXT_BINDING_KIND
    return {KIND_KEY: slug, **{k: v for k, v in out.items() if k != KIND_KEY}}


def normalize_component(component: Any) -> Any:
    """Stamp ``__kind``, fold legacy pick-list keys, and park off-type settings in ``stash``."""
    if not isinstance(component, dict):
        return component
    cc = {k: v for k, v in component.items() if k != KIND_KEY}
    for legacy in _LEGACY_PICK_LIST_KEYS:
        value = cc.pop(legacy, None)
        if isinstance(value, dict) and not isinstance(cc.get("pick_list"), dict):
            cc["pick_list"] = value
    if cc.get("type") == "pick_list":
        cc["type"] = "select"
    ctype = cc.get("type")
    stash = dict(cc["stash"]) if isinstance(cc.get("stash"), dict) else {}
    for key, allowed in SETTING_TYPES.items():
        if key in cc and ctype not in allowed and cc[key] is not None:
            value = cc.pop(key)
            if key in STASHABLE and not _empty(value):
                stash.setdefault(key, value)
            elif key not in STASHABLE and not _empty(value):
                # Not stashable and set on a type that cannot use it: keep it where it is so the
                # schema names it; dropping configuration silently is never a normalization.
                cc[key] = value
    if stash:
        stash.pop(KIND_KEY, None)
        cc["stash"] = stash
    return {KIND_KEY: COMPONENT_KIND, **cc}


def upgrade_agent_variable(raw: dict[str, Any]) -> dict[str, Any]:
    """An agent variable element as stored -> the declared shape (see module doc)."""
    v = copy.deepcopy(raw)
    v.pop(KIND_KEY, None)
    if "default_value" in v:
        legacy = v.pop("default_value")
        v.setdefault("defaultValue", legacy)
    if "componentType" in v:
        legacy_type = v.pop("componentType")
        cc = v.get("customComponent")
        if not isinstance(cc, dict):
            v["customComponent"] = {"type": legacy_type}
        elif not cc.get("type"):
            cc["type"] = legacy_type
    if "title" in v:
        title = v.pop("title")
        if _empty(v.get("label")):
            v["label"] = title
    if "description" in v:
        description = v.pop("description")
        if _empty(v.get("helpText")):
            v["helpText"] = description
        elif description and description != v.get("helpText"):
            v.setdefault("purpose", description)
    if isinstance(v.get("customComponent"), dict):
        v["customComponent"] = normalize_component(v["customComponent"])
    if isinstance(v.get("binding"), dict):
        v["binding"] = stamp_binding(v["binding"])
    return {KIND_KEY: DEFINITION_KIND, **v}


def _choice_type(raw: dict[str, Any], options: list[Any]) -> str:
    if raw.get("multiple"):
        return "checkbox"
    style = raw.get("choice_style") or ""
    if style == "select":
        return "select"
    if style == "chips":
        return "pill-toggle"
    # "" = the simple-box planner's inference: chips up to six options, else a select.
    return "pill-toggle" if 0 < len(options) <= 6 else "select"


def upgrade_workflow_input(raw: dict[str, Any]) -> dict[str, Any]:
    """A workflow VariableSpec or io.user_input UserInputField -> the declared shape."""
    src = copy.deepcopy(raw)
    out: dict[str, Any] = {KIND_KEY: DEFINITION_KIND, "name": src.get("name") or src.get("key") or ""}
    if src.get("label"):
        out["label"] = src["label"]
    if "default" in src:
        out["defaultValue"] = src["default"]
    help_text, description = src.get("help") or "", src.get("description") or ""
    if help_text:
        out["helpText"] = help_text
        if description and description != help_text:
            out["purpose"] = description
    elif description:
        out["helpText"] = description
    if "required" in src:
        out["required"] = bool(src["required"])
    if src.get("sourcing"):
        out["sourcing"] = src["sourcing"]
    if src.get("kind"):
        out["valueKind"] = src["kind"]
    if src.get("variant"):
        out["valueVariant"] = src["variant"]

    ftype = src.get("type")
    options = list(src.get("options") or [])
    default = src.get("default")
    if ftype is None and "key" not in src:  # VariableSpec.effective_type()
        if options:
            ftype = "choice"
        elif isinstance(default, bool):
            ftype = "yes_no"
        elif isinstance(default, int | float):
            ftype = "number"
        elif isinstance(default, dict | list):
            ftype = "json"
        else:
            ftype = "text"
    ftype = ftype or "text"
    cc: dict[str, Any] = {}
    multiple = bool(src.get("multiple"))
    if src.get("picks"):
        cc = {"type": "record", "tokens": [src["picks"]], "multiple": multiple}
    elif ftype in ("text", "short_text"):
        cc = {"type": "text"}
    elif ftype in ("long_text", "textarea"):
        cc = {"type": "textarea"}
    elif ftype == "number":
        cc = {"type": "number"}
    elif ftype == "yes_no":
        cc = {"type": "toggle"}
    elif ftype in ("choice", "select"):
        cc = {"type": _choice_type(src, options) if ftype == "choice" else "select", "options": options}
        if src.get("option_labels"):
            cc["optionLabels"] = src["option_labels"]
    elif ftype == "file":
        cc = {"type": "document"}
        if src.get("accept"):
            cc["accept"] = src["accept"]
    elif ftype == "json":
        out.setdefault("valueKind", "json")
    if multiple and cc.get("type") in SETTING_TYPES["multiple"]:
        cc["multiple"] = True
    if cc.get("type") == "record" and out.get("defaultValue") == "":
        # An empty string was the "no value" of a raw id box; a record input's empty is null.
        out["defaultValue"] = None
    if cc:
        out["customComponent"] = normalize_component(cc)

    hints = {dst: src[key] for key, dst in _HINT_KEYS.items() if key in src and not _empty(src[key])}
    if hints:
        out["hints"] = hints
    if isinstance(src.get("binding"), dict):
        out["binding"] = stamp_binding(src["binding"])
    return out
