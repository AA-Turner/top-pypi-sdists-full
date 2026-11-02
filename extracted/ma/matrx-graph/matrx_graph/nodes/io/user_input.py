from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.input_surface import (
    EntityTypePicks,
    InputHints,
    UserInputFieldType,
    apply_kind_value_schema,
    apply_picks_schema,
    structured_input_kind,
)
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

# Field kinds the author can pick: ``UserInputFieldType`` (types/input_surface.py),
# shared with declared workflow variables so both doors speak one vocabulary.


class UserInputField(InputHints):
    """One field the person running the workflow fills in. Carries the input
    hints (primary box, Tools reveal, chips…) the run form arranges by."""

    model_config = ConfigDict(extra="forbid")

    label: str = Field(
        default="",
        title="Label",
        description="Human label shown above the field.",
        json_schema_extra=field_extras(
            order=1, placeholder="e.g. Topic", help="Shown above the field"
        ),
    )
    type: UserInputFieldType = Field(
        default="text",
        title="Type",
        description="What kind of value to collect.",
        json_schema_extra=field_extras(order=2, help="The kind of value to collect"),
    )
    required: bool = Field(
        default=False,
        title="Required",
        description="Whether the person must fill this in before the run can start.",
        json_schema_extra=field_extras(order=3, widget="toggle"),
    )
    options: list[str] = Field(
        default_factory=list,
        title="Choices",
        description="Choices for type='choice'.",
        json_schema_extra=field_extras(order=4, help="Used when Type is Choice"),
    )
    key: str = Field(
        min_length=1,
        pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$",
        title="Field ID",
        description="The output key this value is stored under (and routed downstream as).",
        json_schema_extra=field_extras(
            order=5,
            help=("Short id used to connect this value to a step — letters, numbers, underscore"),
        ),
    )
    help: str = Field(
        default="",
        title="Help text",
        description="Helper text shown under the field.",
        json_schema_extra=field_extras(order=6),
    )
    placeholder: str = Field(
        default="",
        title="Placeholder",
        description="Faint example text shown inside the empty field.",
        json_schema_extra=field_extras(order=7),
    )
    default: JsonValue = Field(
        default=None,
        title="Default",
        description="Pre-filled value, if any.",
        json_schema_extra=field_extras(order=8),
    )
    # --- Input-surface declarations (INPUT-SURFACE.md, 2026-08-27) ---------
    kind: str = Field(
        default="",
        title="Kind",
        description=(
            "content_ir kind slug this input carries. Empty = derived from "
            "`type` (text/long_text/choice/file → 'text', number → 'number', "
            "yes_no → 'boolean'). A declared slug passes through to the "
            "compiled surface as-is."
        ),
        json_schema_extra=field_extras(order=9, help="Advanced: the platform kind of this value"),
    )
    sourcing: Literal["", "ask", "require", "optional"] = Field(
        default="",
        title="Sourcing rule",
        description=(
            "How this input is sourced: 'ask' (a human answers every time — "
            "even on a programmatic trigger), 'require' (must be present at "
            "start from any source), 'optional' (never blocks). Empty = "
            "derived from `required` (required → require, else optional)."
        ),
        json_schema_extra=field_extras(order=10, help="When a person must answer"),
    )
    # FILLED FROM MY DATA (W1.1, 2026-10-02). The SAME merge-field declaration an agent
    # variable carries when bound with the agent builder's "From my data" picker
    # (`{"kind": "merge_field", "source": "record", "semantic_type": …, "table_id": …}`).
    # A bound field is not asked for: its value is read from the table at run start by the
    # host's one merge-field resolver (`matrx_graph.input_bindings`).
    binding: dict[str, JsonValue] | None = Field(
        default=None,
        title="Fill from my data",
        description="Read this value from one of your tables when the run starts, instead of asking.",
        json_schema_extra=field_extras(order=12, widget="custom_data_binding"),
    )
    # A LIST and a RECORD PICKER, the same two words a declared variable carries
    # (types/variables.py ``VariableSpec``), so every value a workflow uses can sit on a
    # visible input step instead of a hidden variable (Rule 18, Arman 2026-10-28).
    multiple: bool = Field(
        default=False,
        title="Several values",
        description="The value is a list (several files, organizations, words...).",
        json_schema_extra=field_extras(order=13, widget="toggle"),
    )
    picks: EntityTypePicks | None = Field(
        default=None,
        title="Pick from",
        description="The platform record type(s) this value names (e.g. organization, or [note, file]): a picker instead of a raw id box.",
        json_schema_extra=field_extras(order=14, help="Advanced: a record type, e.g. organization"),
    )
    picks_type_into: str = Field(
        default="",
        title="Picked type goes to",
        description="With several record types: the field that receives the type of the record picked.",
        json_schema_extra=field_extras(order=15, help="Advanced: another field's key"),
    )
    variant: str = Field(
        default="",
        title="Presentation variant",
        description=(
            "Named presentation variant registered ON the kind, selected by "
            "name (never an ad-hoc component). Empty = derived from `type` "
            "(long_text → textarea, choice → dropdown), else the kind's "
            "default component. Every name must be seeded on the kind in the "
            "registry — an unregistered name degrades silently."
        ),
        json_schema_extra=field_extras(order=11, help="Advanced: named variant on the kind"),
    )

    def effective_kind(self) -> str:
        """The kind slug this field carries on the compiled surface."""
        from matrx_graph.types.input_surface import compiled_kind_and_variant

        return compiled_kind_and_variant(self.type, multiple=self.multiple, kind=self.kind)[0]

    def is_bound(self) -> bool:
        """True when this field is filled from table data (a merge-field binding)."""
        return isinstance(self.binding, dict) and self.binding.get("kind") == "merge_field"

    def effective_sourcing(self) -> str:
        """The sourcing rule: explicit wins; else required → require, else optional.

        A field filled from table data is never asked for — the run fills it."""
        if self.is_bound():
            return "optional"
        return self.sourcing or ("require" if self.required else "optional")

    def effective_variant(self) -> str | None:
        """The named presentation variant, or None for the kind's default."""
        from matrx_graph.types.input_surface import compiled_kind_and_variant

        return compiled_kind_and_variant(
            self.type, multiple=self.multiple, kind=self.kind, variant=self.variant
        )[1]


class UserInputConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        default="Your inputs",
        description="Section heading shown in the run form.",
        json_schema_extra=field_extras(help="What this group of inputs is for"),
    )
    description: str = Field(
        default="",
        description="Optional one-line explanation shown under the title.",
    )
    fields: list[UserInputField] = Field(
        default_factory=list,
        description="The fields the user fills in to start the run.",
        # minItems lives as a real JSON Schema keyword (NOT via field_extras —
        # that helper prefixes every extra with ui:). Studio readiness reads it
        # so an empty Collect Inputs shows "Needs setup". Kept out of Pydantic
        # min_length so a freshly dropped / mid-edit draft still validates.
        json_schema_extra={
            **field_extras(
                widget="user_input_fields",
                help="Add one entry per input the user fills in to start the run",
            ),
            "minItems": 1,
        },
    )

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
            prop: dict[str, Any] = {"title": fld.label or fld.key, "ui:order": index}
            if fld.help:
                prop["description"] = fld.help
            if fld.type == "number":
                prop["type"] = "number"
            elif fld.type == "yes_no":
                prop["type"] = "boolean"
            elif fld.type == "choice":
                prop["type"] = "string"
                if fld.options:
                    prop["enum"] = list(fld.options)
                if fld.option_labels:
                    prop["ui:option_labels"] = dict(fld.option_labels)
            else:  # text, long_text, file
                prop["type"] = "string"
            if fld.type == "long_text":
                prop["ui:widget"] = "textarea"
            elif fld.type == "file":
                prop["ui:widget"] = "file"
            if fld.multiple:
                prop["type"] = "array"
                prop["items"] = {"type": "number" if fld.type == "number" else "string"}
                # Each item is one of the choices; an enum on the array would refuse every list.
                if "enum" in prop:
                    prop["items"]["enum"] = prop.pop("enum")
                prop["ui:multiple"] = True
            if fld.picks and fld.type != "file":
                apply_picks_schema(prop, fld.picks, fld.picks_type_into)
            # A field naming a structured kind takes its value contract from the kind (gap 8).
            apply_kind_value_schema(prop, fld.kind, fld.type, multiple=fld.multiple, name=fld.key)
            # A field of kind ``json`` carries any data a caller hands over (a list of records, an
            # object), the same open contract an untyped run variable has; the run form edits it as JSON.
            if fld.kind.strip() == "json":
                for key in ("type", "items", "ui:multiple"):
                    prop.pop(key, None)
                prop["ui:widget"] = "json"
            if fld.placeholder:
                prop["ui:placeholder"] = fld.placeholder
            if fld.default is not None:
                prop["default"] = fld.default
            if fld.is_bound():
                # Filled from table data at run start: never a box on the run form.
                prop["ui:hidden"] = True
                prop["ui:filled_from_data"] = True
            props[fld.key] = prop
            if fld.required and not fld.is_bound():
                required.append(fld.key)
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
        await _fill_bound_fields(ctx, config, payload)
        # A missing required field parks the run on THIS node (recoverable)
        # with a clear message — never silently pass an empty value downstream.
        missing = [
            fld.key for fld in config.fields if fld.required and payload.get(fld.key) in (None, "")
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
            if fld.key in payload:
                continue
            if fld.default is not None:
                payload[fld.key] = fld.default
            elif structured_input_kind(fld.kind, fld.type) is not None:
                # A structured value left blank is no value — never an empty string.
                payload[fld.key] = [] if fld.multiple else None
            elif fld.type == "yes_no":
                payload[fld.key] = False
            elif fld.type == "number":
                payload[fld.key] = None
            else:  # text, long_text, choice, file
                payload[fld.key] = ""
        return success(UserInputOutput(**payload))


async def _fill_bound_fields(
    ctx: NodeExecutionContext, config: UserInputConfig, payload: dict[str, Any]
) -> None:
    """Fill every field bound to table data, through the host's ONE merge-field resolver.

    An absent binding delivers the resolver's named absence as the value and SAYS so in the
    run (a progress line) — never a silent empty. ``missing: "block"`` parks the run here.
    """
    bindings = {fld.key: dict(fld.binding or {}) for fld in config.fields if fld.is_bound()}
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
    labels = {fld.key: (fld.label or fld.key) for fld in config.fields}
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
        slug = structured_input_kind(fld.kind, fld.type)
        if slug is None or await structured_kind_schema(slug) is None:
            continue
        judged.add(fld.key)
        problems.extend(await input_kind_problems(fld.key, values.get(fld.key), slug, multiple=fld.multiple))
    return judged, problems
