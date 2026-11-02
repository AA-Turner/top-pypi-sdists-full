"""Run variables — declared workflow inputs substituted into node inputs.

The one generic channel for getting RUN-TIME values (the studio Start
sheet's ``initial_variables``, an API caller's ``initial_variables``) into
ANY node's inputs, on ANY workflow:

1. The Definition DECLARES its variables (``Definition.variables`` — name,
   description, optional default).
2. A node's authored static inputs REFERENCE a variable with
   ``{"$var": "topic"}`` (optionally ``{"$var": "topic", "default": ...}``),
   anywhere in the value tree — top level, nested dict, inside a list.
3. Compile / validate FAILS LOUDLY on a reference to an undeclared variable
   (CompilationError / ValidationIssue) — never a silent empty string.
4. At input-resolution time the scheduler substitutes each reference:
   run value → per-reference default → declared default → loud
   UnresolvedVariableError parking the run on that node.

Edge-routed payloads are DATA, not authored refs — they are never scanned
for ``$var``; only the node's ``static_inputs`` side is resolved, and an
edge value overriding the same key still wins (last-writer-wins merge).
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import ConfigDict, Field

from matrx_graph.types.input_surface import (
    EntityTypePicks,
    InputHints,
    UserInputFieldType,
    apply_kind_value_schema,
    apply_picks_schema,
)

logger = logging.getLogger(__name__)

# The LEGACY reference marker key — deprecated, replaced by ``$input``
# (INPUT-SURFACE.md, ruled 2026-08-27). Kept functional for stored
# definitions until the $var → $input definition migration runs
# (scripts/migrate_var_to_input.py); new compiles refuse authoring NEW
# ``$var`` markers. A dict is a variable reference iff it has this key (a
# string value) and no keys other than this + "default".
VAR_REF_KEY = "$var"
_ALLOWED_REF_KEYS = {VAR_REF_KEY, "default"}

# THE one reference namespace of the input surface: ``{"$input": name}``
# resolves against the workflow's compiled input surface. Same structural
# rules as $var (this key + optional "default", nothing else).
INPUT_REF_KEY = "$input"
_ALLOWED_INPUT_REF_KEYS = {INPUT_REF_KEY, "default"}

# ``{"$run": "id" | "workflow_id" | "step_id" | "organization_id" | "user_id"}`` — the RUN's
# own identity in a step's authored inputs (and, through ``substitute_template``, inside a
# template): a record a run writes can say which run, step, organization and person wrote it
# (a kit outline's ``built_by_run_id``, provenance and audit stamps, an org-scoped key)
# without a step that exists only to echo it. Resolved by the scheduler from the run it is
# executing (``NodeExecutionContext.run_facts`` — the organization and user are the run's
# CARRIED request context, never resolved from a default); never from the payload.
# ``step_id`` is the id of the step that reads it.
RUN_REF_KEY = "$run"
RUN_REF_FIELDS = frozenset({"id", "workflow_id", "step_id", "organization_id", "user_id"})


def is_run_ref(value: Any) -> bool:
    """True when ``value`` is a ``{"$run": field}`` reference dict."""
    return isinstance(value, dict) and set(value.keys()) == {RUN_REF_KEY} and isinstance(value[RUN_REF_KEY], str)

# Loud-patches law: the $var compatibility pass is a stand-in that dies with
# the definition migration, so every resolution SCREAMS — counted, throttled
# to once per (variable name) per process so a hot loop doesn't drown logs.
_VAR_DEPRECATION_SEEN: set[str] = set()
_VAR_DEPRECATION_COUNT = 0


def _scream_var_deprecation(name: str, node_id: str) -> None:
    global _VAR_DEPRECATION_COUNT
    _VAR_DEPRECATION_COUNT += 1
    if name in _VAR_DEPRECATION_SEEN:
        return
    _VAR_DEPRECATION_SEEN.add(name)
    logger.warning(
        "DEPRECATED $var MARKER (occurrence #%d this process): node '%s' "
        "references {'$var': '%s'}. The $var namespace is replaced by "
        "{'$input': '%s'} (INPUT-SURFACE.md); this compatibility pass dies "
        "with the definition migration (scripts/migrate_var_to_input.py).",
        _VAR_DEPRECATION_COUNT,
        node_id,
        name,
        name,
    )


class VariableSpec(InputHints):
    """One declared run variable on a Definition.

    ``default=None`` means "no default" — a reference to this variable with
    no per-reference default MUST be supplied at run time or the run fails
    loudly at that node. (A literal None default would be useless anyway:
    node input schemas want real values.)
    """

    model_config = ConfigDict(extra="ignore")

    name: str = Field(min_length=1, pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$")
    description: str = ""
    default: Any = None  # api-any-ok: user-defined variable value, any JSON shape
    # The value type, in the SAME plain-language vocabulary an io.user_input
    # field uses. None = read it from ``default`` (3 → number, false → yes_no);
    # a variable with neither is text. Without this every variable reached the
    # run form as a text box — a number typed as "2", a yes/no as "true".
    type: UserInputFieldType | None = None
    options: list[str] = Field(default_factory=list)  # choices for type="choice"
    # A PERSON'S DOOR into a reference input (generic-only VISION, "Every workflow takes a
    # person's input too", Arman 2026-10-27). ``picks`` names the platform record type
    # (``platform.entity_types`` token) an id input points at — or a list of them when it
    # accepts several kinds of record — so the run form offers a search-by-name picker instead of
    # a raw id box; ``picks_type_into`` names the input that receives the picked record's type. ``multiple``/``accept`` shape a
    # ``file`` input: several files at once, and which (``image/*`` lets a phone take a
    # photo). A file input's value is the stored file's id (file_id is identity), or a list.
    picks: EntityTypePicks | None = None
    picks_type_into: str = ""
    multiple: bool = False
    accept: str = ""
    # WHAT A PERSON READS (review gap A1/B1, 2026-10-29). A declared variable carries the same
    # presentation an input step's field does — a label, help, a placeholder, a kind, and the
    # input hints it inherits (example, advanced, group, order, detect, primary,
    # required_in_form) — and ``_build_input_surface`` copies them. Empty label = the run form
    # shows the name in words, never snake_case. ``help`` empty = ``description``.
    label: str = ""
    help: str = ""
    placeholder: str = ""
    kind: str = Field(default="", pattern=r"^$|^[a-z][a-z0-9_]*$")

    def effective_type(self) -> UserInputFieldType | None:
        """The declared type, else the one ``default`` shows; None = free-form JSON."""
        if self.type is not None:
            return self.type
        if self.options:
            return "choice"
        value = self.default
        if isinstance(value, bool):
            return "yes_no"
        if isinstance(value, int | float):
            return "number"
        if isinstance(value, dict | list):
            return None
        return "text"


def variable_json_schema(var: VariableSpec) -> dict[str, Any]:
    """The value contract of one declared variable — the run form renders from it."""
    # The title is what a person reads: the label when the author wrote one (as a field's is).
    schema: dict[str, Any] = {"title": var.label or var.name}
    if var.description:
        schema["description"] = var.description
    kind = var.effective_type()
    if kind is None:
        schema["type"] = "array" if isinstance(var.default, list) else "object"
    elif kind == "number":
        # A whole-number default (3) asks for a whole number; 0.5 asks for any.
        whole = isinstance(var.default, int) and not isinstance(var.default, bool)
        schema["type"] = "integer" if whole else "number"
    elif kind == "yes_no":
        schema["type"] = "boolean"
    else:
        schema["type"] = "string"
        if kind == "choice" and var.options:
            schema["enum"] = list(var.options)
        if kind == "long_text":
            schema["ui:widget"] = "textarea"
        elif kind == "file":
            schema["ui:widget"] = "file"
            if var.accept:
                schema["ui:accept"] = var.accept
            if var.multiple:
                schema["type"] = "array"
                schema["items"] = {"type": "string"}
                schema["ui:multiple"] = True
        if var.multiple and kind in ("text", "long_text"):
            # Several words, one per line: a list of strings (kind string_list, variant lines).
            schema.pop("ui:widget", None)
            schema["type"] = "array"
            schema["items"] = {"type": "string"}
            schema["ui:multiple"] = True
        if var.picks and kind != "file":
            apply_picks_schema(schema, var.picks, var.picks_type_into)
    if var.kind and (kind is None or kind in ("text", "long_text")):
        # A variable naming a structured kind takes its value contract from the kind (gap 8).
        apply_kind_value_schema(schema, var.kind, kind, multiple=var.multiple, name=var.name)
    if var.default is not None:
        schema["default"] = var.default
    return schema


def is_var_ref(value: Any) -> bool:
    """True when ``value`` is a ``{"$var": name}`` reference dict."""
    return (
        isinstance(value, dict)
        and isinstance(value.get(VAR_REF_KEY), str)
        and bool(value.get(VAR_REF_KEY))
        and set(value.keys()) <= _ALLOWED_REF_KEYS
    )


def is_input_ref(value: Any) -> bool:
    """True when ``value`` is a ``{"$input": name}`` reference dict."""
    return (
        isinstance(value, dict)
        and isinstance(value.get(INPUT_REF_KEY), str)
        and bool(value.get(INPUT_REF_KEY))
        and set(value.keys()) <= _ALLOWED_INPUT_REF_KEYS
    )


def iter_input_refs(obj: Any, _path: str = "") -> list[tuple[str, str]]:
    """Every ``(path, input_name)`` referenced anywhere inside ``obj``."""
    refs: list[tuple[str, str]] = []
    if is_input_ref(obj):
        refs.append((_path or "<root>", obj[INPUT_REF_KEY]))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            refs.extend(iter_input_refs(value, f"{_path}.{key}" if _path else str(key)))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            refs.extend(iter_input_refs(value, f"{_path}[{index}]" if _path else f"[{index}]"))
    return refs


def iter_var_refs(obj: Any, _path: str = "") -> list[tuple[str, str]]:
    """Every ``(path, variable_name)`` referenced anywhere inside ``obj``."""
    refs: list[tuple[str, str]] = []
    if is_var_ref(obj):
        refs.append((_path or "<root>", obj[VAR_REF_KEY]))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            refs.extend(iter_var_refs(value, f"{_path}.{key}" if _path else str(key)))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            refs.extend(iter_var_refs(value, f"{_path}[{index}]" if _path else f"[{index}]"))
    return refs


def resolve_var_refs(
    obj: Any,
    *,
    run_variables: dict[str, Any],
    declared: dict[str, VariableSpec],
    node_id: str,
    strict: bool = True,
    run_inputs: dict[str, Any] | None = None,
    input_surface: dict[str, Any] | None = None,
    run_facts: dict[str, Any] | None = None,
) -> Any:
    """Substitute every ``{"$input": name}`` and legacy ``{"$var": name}``
    reference inside ``obj``, and every ``{"$run": <RUN_REF_FIELDS>}`` from
    ``run_facts`` (strict: an unknown field, or no run to read it from, fails loudly).

    ``$input`` (the one namespace, INPUT-SURFACE.md) resolves against the
    run's landed surface values (``run_inputs``) → per-reference ``default``
    → the surface entry's declared default → **UnresolvedInputError** (strict)
    or ``None`` (lenient). An UNDECLARED name — one not on the compiled
    surface — is a loud failure in strict mode even when a value happens to
    be lying around: the surface, not the payload, is the contract.

    ``$var`` (legacy, dies with the definition migration): run value (key
    present and not None) → per-reference ``default`` → declared default →
    **UnresolvedVariableError** (strict — parks the run on this node) or
    ``None`` (lenient, for pre-execution introspection). Every $var
    resolution screams a counted deprecation warning (loud-patches law).

    Edge-routed payloads are DATA and are never scanned — callers only pass
    authored ``static_inputs`` here. Returns a new structure; never mutates
    ``obj``.
    """
    from matrx_graph.errors import UnresolvedInputError, UnresolvedVariableError

    inputs = run_inputs or {}
    surface = input_surface or {}

    if is_run_ref(obj):
        field = obj[RUN_REF_KEY]
        if field not in RUN_REF_FIELDS:
            raise UnresolvedInputError(
                f"Node '{node_id}' reads '$run': '{field}', which a run does not offer. "
                f"Use one of: {sorted(RUN_REF_FIELDS)}."
            )
        value = (run_facts or {}).get(field)
        if value:
            return str(value)
        if strict:
            raise UnresolvedInputError(
                f"Node '{node_id}' reads '$run': '{field}' but this step is not running "
                "inside a run that has one."
            )
        return None
    if isinstance(obj, dict) and RUN_REF_KEY in obj:
        raise UnresolvedInputError(
            f"Node '{node_id}' writes '$run' with {sorted(obj)}: a run reference is the name "
            'alone, {"$run": "id"} — no "default" or other key beside it (a made-up run id '
            "would stamp records as if a run wrote them)."
        )
    if is_input_ref(obj):
        name = obj[INPUT_REF_KEY]
        spec = surface.get(name)
        if spec is None and strict:
            raise UnresolvedInputError(
                f"Node '{node_id}' references workflow input '{name}', which is "
                f"not on this workflow's input surface. Declare it on an input "
                f"node (or as a workflow variable) — the surface is the only "
                f"thing '$input' can address."
            )
        run_value = inputs.get(name)
        if name in inputs and run_value is not None:
            return run_value
        if "default" in obj and obj["default"] is not None:
            return obj["default"]
        declared_default = getattr(spec, "default", None)
        if declared_default is not None:
            return declared_default
        if strict:
            raise UnresolvedInputError(
                f"Node '{node_id}' references workflow input '{name}' but no "
                f"value landed for this run and it has no default. Supply "
                f"inputs['{name}'] when starting the run, or declare a default "
                f"for it on the input."
            )
        return None
    if is_var_ref(obj):
        name = obj[VAR_REF_KEY]
        _scream_var_deprecation(name, node_id)
        run_value = run_variables.get(name)
        if name in run_variables and run_value is not None:
            return run_value
        if "default" in obj and obj["default"] is not None:
            return obj["default"]
        spec = declared.get(name)
        if spec is not None and spec.default is not None:
            return spec.default
        # The surface folds declared variables in, so a landed surface value
        # for this name also satisfies a legacy $var reference (compat until
        # the marker migration runs).
        if name in inputs and inputs.get(name) is not None:
            return inputs[name]
        if strict:
            raise UnresolvedVariableError(
                f"Node '{node_id}' references run variable '{name}' but no value "
                f"was provided for this run and it has no default. Supply "
                f"initial_variables['{name}'] when starting the run, or declare "
                f"a default for it on the workflow."
            )
        return None
    if isinstance(obj, dict):
        return {
            key: resolve_var_refs(
                value,
                run_variables=run_variables,
                declared=declared,
                node_id=node_id,
                strict=strict,
                run_inputs=run_inputs,
                input_surface=input_surface,
                run_facts=run_facts,
            )
            for key, value in obj.items()
        }
    if isinstance(obj, list):
        return [
            resolve_var_refs(
                value,
                run_variables=run_variables,
                declared=declared,
                node_id=node_id,
                strict=strict,
                run_inputs=run_inputs,
                input_surface=input_surface,
                run_facts=run_facts,
            )
            for value in obj
        ]
    return obj


def var_ref(name: str, default: Any = None) -> dict[str, Any]:  # api-any-ok: authoring helper
    """DEPRECATED authoring helper: build a ``{"$var": name}`` reference dict.

    New authoring uses :func:`input_ref` — the compiler refuses NEW $var
    markers (validation error naming ``$input``); this survives only for the
    stored-definition compatibility window.
    """
    ref: dict[str, Any] = {VAR_REF_KEY: name}
    if default is not None:
        ref["default"] = default
    return ref


def input_ref(name: str, default: Any = None) -> dict[str, Any]:  # api-any-ok: authoring helper
    """Authoring helper: build a ``{"$input": name}`` surface reference dict."""
    ref: dict[str, Any] = {INPUT_REF_KEY: name}
    if default is not None:
        ref["default"] = default
    return ref
