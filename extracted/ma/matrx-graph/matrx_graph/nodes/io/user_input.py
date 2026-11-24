from __future__ import annotations

from matrx_graph.content_ir.envelope import KIND_KEY

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue, RootModel, field_validator

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.input_declaration import VariableDefinition
from matrx_graph.types.input_surface import (
    apply_kind_value_schema,
    apply_picks_schema,
    check_input_name,
    compiled_kind_and_variant,
    declared_inputs,
    input_binding_dict,
    input_is_bound,
    input_label,
    input_multiple,
    input_option_labels,
    input_options,
    input_picks,
    input_picks_type_into,
    input_type,
    structured_input_kind,
)
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

#: THE INPUT-SOURCE STEP TYPES: every step whose ``config.fields`` compile into the workflow's ONE
#: input surface. ``io.trigger`` (the Trigger step) is a second registration of the SAME executor
#: and config as ``io.user_input`` (Collect Inputs); everything that means "an input source" reads
#: this set, never one of the two names.
TRIGGER_STEP_TYPE = "io.trigger"
INPUT_SOURCE_TYPES: frozenset[str] = frozenset({"io.user_input", TRIGGER_STEP_TYPE})


def input_source_label(spec_type: str, node_id: str) -> str:
    """How an error names an input-source step: the Trigger step or an input node, by id."""
    return f"the Trigger step '{node_id}'" if spec_type == TRIGGER_STEP_TYPE else f"input node '{node_id}'"


# A field is ONE input declaration (``VariableDefinition``, matrx_graph.input_declaration) — the
# same shape a declared workflow variable and an agent variable take. What it means to the engine
# (type, several values, record picks, options, hints) is read through the reader API in
# ``types/input_surface.py``; nothing here re-declares it.


def field_kind_and_variant(d: VariableDefinition) -> tuple[str, str | None]:
    """The (kind, variant) a field compiles to on the input surface."""
    return compiled_kind_and_variant(
        input_type(d) or "text",
        multiple=input_multiple(d),
        kind=d.valueKind or "",
        variant=d.valueVariant or "",
    )


def field_sourcing(d: VariableDefinition) -> str:
    """The sourcing rule: explicit wins; else required -> require, else optional. A field filled
    from table data is never asked for — the run fills it."""
    if input_is_bound(d):
        return "optional"
    return d.sourcing or ("require" if d.required else "optional")


def field_json_schema(d: VariableDefinition, index: int = 0) -> dict[str, Any]:
    """The value contract of one ``io.user_input`` field — the run form renders from it."""
    ftype = input_type(d) or "text"
    multiple = input_multiple(d)
    prop: dict[str, Any] = {"title": input_label(d), "ui:order": index}
    if d.helpText:
        prop["description"] = d.helpText
    if ftype == "number":
        prop["type"] = "number"
    elif ftype == "yes_no":
        prop["type"] = "boolean"
    elif ftype == "choice":
        prop["type"] = "string"
        options = input_options(d)
        if options:
            prop["enum"] = options
        labels = input_option_labels(d)
        if labels:
            prop["ui:option_labels"] = labels
    else:  # text, long_text, file
        prop["type"] = "string"
    if ftype == "long_text":
        prop["ui:widget"] = "textarea"
    elif ftype == "file":
        prop["ui:widget"] = "file"
    if multiple:
        prop["type"] = "array"
        prop["items"] = {"type": "number" if ftype == "number" else "string"}
        # Each item is one of the choices; an enum on the array would refuse every list.
        if "enum" in prop:
            prop["items"]["enum"] = prop.pop("enum")
        prop["ui:multiple"] = True
    picks = input_picks(d)
    if picks and ftype != "file":
        apply_picks_schema(prop, picks, input_picks_type_into(d))
    # A field naming a structured kind takes its value contract from the kind (gap 8).
    apply_kind_value_schema(prop, d.valueKind, ftype, multiple=multiple, name=d.name)
    # A field of kind ``json`` carries any data a caller hands over (a list of records, an
    # object), the same open contract an untyped run variable has; the run form edits it as JSON.
    if (d.valueKind or "").strip() == "json":
        for key in ("type", "items", "ui:multiple"):
            prop.pop(key, None)
        prop["ui:widget"] = "json"
    placeholder = d.hints.placeholder if d.hints is not None else None
    if placeholder:
        prop["ui:placeholder"] = placeholder
    if d.defaultValue is not None:
        prop["default"] = d.defaultValue
    if input_is_bound(d):
        # Filled from table data at run start: never a box on the run form.
        prop["ui:hidden"] = True
        prop["ui:filled_from_data"] = True
    return prop


class UserInputConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        default="Your inputs",
        description="Section heading shown in the run form.",
        # The label says it all: no help icon, one line.
        json_schema_extra=field_extras(help="", single_line=True),
    )
    description: str = Field(
        default="",
        description="Optional one-line explanation shown under the title.",
        json_schema_extra=field_extras(help="", single_line=True),
    )
    fields: list[VariableDefinition] = Field(
        default_factory=list,
        description="The fields the user fills in to start the run.",
        # minItems lives as a real JSON Schema keyword (NOT via field_extras —
        # that helper prefixes every extra with ui:). Studio readiness reads it
        # so an empty Collect Inputs shows "Needs setup". Kept out of Pydantic
        # min_length so a freshly dropped / mid-edit draft still validates.
        json_schema_extra={
            **field_extras(
                widget="user_input_fields",
                help="",
            ),
            "minItems": 1,
        },
    )

    @field_validator("fields", mode="before")
    @classmethod
    def _declared_fields(cls, value: Any) -> Any:
        # Old stored fields (key/type/picks/...) are read ONLY through the converter.
        return declared_inputs(value) if isinstance(value, list | tuple) else value

    @field_validator("fields", mode="after")
    @classmethod
    def _field_names(cls, value: list[VariableDefinition]) -> list[VariableDefinition]:
        for fld in value:
            check_input_name(fld.name)
        return value

    def effective_output_json_schema(self) -> dict[str, Any]:
        """Compile the author-defined fields into a JSON Schema.

        This IS the node's output shape and the form the studio renders (via
        AutoForm) to collect the run's inputs. Read at compile time by
        ``compile.py`` (because ``NodeSpec.dynamic_output`` is True) and stored
        on the CompiledNode for run-form generation + downstream type hints.
        """
        props: dict[str, Any] = {}
        required: list[str] = []
        for index, fld in enumerate(self.fields):
            props[fld.name] = field_json_schema(fld, index)
            if fld.required and not input_is_bound(fld):
                required.append(fld.name)
        schema: dict[str, Any] = {"type": "object", "properties": props}
        if required:
            schema["required"] = required
        return schema


class UserInputInput(BaseModel):
    # Permissive: at run start the scheduler delivers the user's filled values
    # here (one per author-defined field). extra="allow" so any field shape the
    # author defined validates.
    model_config = ConfigDict(extra="allow")


class UserInputOutput(BaseModel):
    # Permissive: the user's values become this node's output and route
    # downstream on normal edges. The *effective* schema is computed from the
    # config (see UserInputConfig.effective_output_json_schema).
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "author-defined field keys; effective schema comes from config.fields"
        },
    )


class UserInputExecutor:
    """Collect inputs from the person running the workflow — the keystone of
    "build by running".

    The author defines the fields (key / label / type / required / ...); the
    studio renders a form from ``config.fields`` and the user's answers are
    delivered as this node's inputs when the run starts. The node echoes them
    as its output, so ordinary edges carry each value to wherever the author
    wired it.

    Distinct from ``control.human_input``, which PAUSES mid-run to ask. This
    one SEEDS the run: it is a source node (no incoming edges) and the run form
    is generated from it.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="io.user_input",
        category=NodeCategory.IO,
        display_name="Collect Inputs",
        description=(
            "Ask the person running the workflow for information at the START — "
            "these fields become the Run form."
        ),
        input_schema=UserInputInput,
        output_schema=UserInputOutput,
        config_schema=UserInputConfig,
        # Named shape for pickers/labels; the *effective* per-definition schema
        # (config.fields) still gates the run form — dynamic_output stays True.
        output_kind="user_inputs",
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
        is_source=True,
        dynamic_output=True,
        icon="clipboard-pen",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: UserInputInput,
        config: UserInputConfig,
    ) -> NodeResult[UserInputOutput]:
        payload = inputs.model_dump(mode="json")
        # A run started with a KIND-declared input (a ``relation``, a record …) arrives as that
        # kind's instance: its top-level ``__kind`` names the whole run input — which keeps it
        # (``workflow.run.input``) — not a field of this step's output, whose own kind is
        # ``user_inputs``. Carried through, it collided with that kind and failed the run as
        # "something went wrong on our side" (run a02a0b62, 2026-11-02). The fields pass
        # through as they are; a field that IS a kind value keeps its own marker.
        if payload.get(KIND_KEY) not in (None, self.spec.output_kind):
            payload.pop(KIND_KEY)
        await _fill_bound_fields(ctx, config, payload)
        # A missing required field parks the run on THIS node (recoverable)
        # with a clear message — never silently pass an empty value downstream.
        missing = [
            fld.name for fld in config.fields if fld.required and payload.get(fld.name) in (None, "")
        ]
        if missing:
            raise ValueError(
                f"Missing required input(s): {', '.join(missing)}. Fill them in and run again."
            )
        # Every AUTHOR-DEFINED field key must exist on the output, even when the
        # person running the workflow left an optional field blank — otherwise a
        # downstream edge mapped to that key KeyErrors (EdgeRoutingError) instead
        # of resolving to an empty value. The scheduler only delivers keys the
        # user actually touched, so backfill the rest from the field's default.
        for fld in config.fields:
            if fld.name in payload:
                continue
            ftype = input_type(fld) or "text"
            if fld.defaultValue is not None:
                payload[fld.name] = fld.defaultValue
            elif structured_input_kind(fld.valueKind, ftype) is not None:
                # A structured value left blank is no value — never an empty string.
                payload[fld.name] = [] if input_multiple(fld) else None
            elif ftype == "yes_no":
                payload[fld.name] = False
            elif ftype == "number":
                payload[fld.name] = None
            else:  # text, long_text, choice, file
                payload[fld.name] = ""
        # The output model is the spec's: this step's open-keys model, or the Trigger step's typed JSON map.
        return success(self.spec.output_schema.model_validate(payload))


async def _fill_bound_fields(
    ctx: NodeExecutionContext, config: UserInputConfig, payload: dict[str, Any]
) -> None:
    """Fill every field bound to table data, through the host's ONE merge-field resolver.

    An absent binding delivers the resolver's named absence as the value and SAYS so in the
    run (a progress line) — never a silent empty. ``missing: "block"`` parks the run here.
    """
    bindings = {fld.name: input_binding_dict(fld) for fld in config.fields if input_is_bound(fld)}
    if not bindings:
        return
    from matrx_graph.input_bindings import InputBindingBlocked, get_input_binding_resolver

    resolver = get_input_binding_resolver()
    if resolver is None:
        raise ValueError(
            "These inputs are filled from your data, but this server cannot read tables for a "
            f"workflow ({', '.join(sorted(bindings))}). Type the values in instead, or run it on AI Matrx."
        )
    try:
        resolved = await resolver(bindings, ctx.user_id or None, ctx.organization_id)
    except InputBindingBlocked as blocked:
        raise ValueError(blocked.user_message) from blocked
    labels = {fld.name: input_label(fld) for fld in config.fields}
    for key in bindings:
        bound = resolved.get(key)
        if bound is None:
            sentence = f"{labels[key]}: nothing was read from the table."
            payload[key] = f"[not available — {sentence}]"
            await ctx.progress(sentence)
            continue
        supplied = payload.get(key) not in (None, "")
        if supplied and not bound.locks_client:
            continue
        payload[key] = bound.text
        if not bound.present:
            await ctx.progress(f"{labels[key]}: {bound.absent_sentence or 'nothing was found in the table.'}")


async def user_input_kind_problems(
    config: UserInputConfig, values: dict[str, Any]
) -> tuple[set[str], list[str]]:
    """``(field keys judged by their kind, the problems found)`` for the landed run-form values.

    A field naming a structured kind is judged against the kind's registered schema (resolved
    now, so a cold kind cache at compile never decides), one problem per wrong item, each
    naming the field, the item and the kind. A kind whose value is plain is not judged here —
    the compiled plain contract judges it."""
    from matrx_graph.kinds import input_kind_problems, structured_kind_schema

    judged: set[str] = set()
    problems: list[str] = []
    for fld in config.fields:
        slug = structured_input_kind(fld.valueKind, input_type(fld) or "text")
        if slug is None or await structured_kind_schema(slug) is None:
            continue
        judged.add(fld.name)
        problems.extend(
            await input_kind_problems(fld.name, values.get(fld.name), slug, multiple=input_multiple(fld))
        )
    return judged, problems


class TriggerOutput(RootModel[dict[str, JsonValue]]):
    """The Trigger step's output: the fire's values keyed by the author's field names, every value
    typed JSON. A fully declared contract (the keys are author-defined; the values are JSON)."""


class TriggerStepExecutor(UserInputExecutor):
    """THE TRIGGER STEP (``io.trigger``): a workflow's first step when something outside starts it —
    the SAME executor and config as ``io.user_input`` (a second registration, nothing else). Its
    fields are the values a fire fills; the triggers that start the workflow are the host's
    ``workflow.trigger`` rows (this package knows nothing about them). At most one per workflow,
    always a source (``validate_definition``)."""

    spec: ClassVar[NodeSpec] = UserInputExecutor.spec.model_copy(
        update={
            "node_type": TRIGGER_STEP_TYPE,
            "display_name": "Trigger",
            "description": (
                "Start this workflow from outside: a schedule, a web address, a data change or a "
                "connected app. Its fields are what each trigger fills in. Not a mid-run data subscription."
            ),
            "icon": "zap",
            "output_schema": TriggerOutput,
        }
    )

