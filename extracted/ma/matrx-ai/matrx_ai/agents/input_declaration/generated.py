# ruff: noqa
# AUTO-GENERATED — DO NOT EDIT.
# Source: packages/matrx-ai/matrx_ai/agents/input_declaration/schema/*.schema.json (JSON Schema
#   2020-12, the one input declaration) → datamodel-codegen 0.83.0 → scripts/generate_input_declaration.py.
# Regenerate: uv run python scripts/generate_input_declaration.py
# Check:      uv run python scripts/generate_input_declaration.py --check
#             (and scripts/check_one_input_declaration.py, which also refuses any hand-written copy)

from __future__ import annotations

from typing import Annotated, Any, Literal

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind

from matrx_ai.agents.input_declaration.source import source_schema

from pydantic import BaseModel, ConfigDict, Field, RootModel


class Control(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    key: Annotated[
        str,
        Field(
            description="Canonical control key from the model's catalog record.",
            min_length=1,
        ),
    ]


class Hints(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    primary: Annotated[
        bool | None, Field(description='This input is THE box (at most one per form).')
    ] = None
    advanced: Annotated[
        bool | None,
        Field(
            description='true: behind the Tools reveal; false: always visible; absent: inferred.'
        ),
    ] = None
    group: Annotated[
        str | None, Field(description='Tools-bar group label, e.g. Location.')
    ] = None
    order: Annotated[int | None, Field(description='Sort key within its zone.')] = None
    inline: Annotated[
        bool | None,
        Field(
            description='A short choice attached to the primary box as a scope picker.'
        ),
    ] = None
    placeholder: Annotated[
        str | None, Field(description='Faint example text inside the empty field.')
    ] = None
    example: Annotated[
        str | None, Field(description='One realistic value; never a default.')
    ] = None
    detect: Annotated[
        list[Literal['handle', 'url', 'domain', 'keyword', 'email', 'person_name', 'phone']] | None,
        Field(description='What the primary box accepts; drives smart detection.'),
    ] = None
    requiredInForm: Annotated[
        bool | None,
        Field(
            description='A person must fill it in on the run form; callers (API, Mandate, schedule) may leave it empty. The form enforces it, the engine never does.'
        ),
    ] = None


@kind(
    'variable_context_binding',
    disposition='envelope',
    family='input_declaration',
    maturity='distilled',
    example=source_schema('variable_context_binding')['examples'][0],
)
class VariableContextBinding(KindModel):
    @classmethod
    def model_json_schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        # The registry row stores the source file byte for byte (rule 2: emitted, never hand-patched).
        return source_schema('variable_context_binding')

    model_config = ConfigDict(
        extra='forbid',
    )
    kind: Annotated[
        Literal['context_item'] | None,
        Field(
            description='Optional discriminant. Older rows carry none; a binding without kind is a context-item binding.'
        ),
    ] = None
    contextItemId: Annotated[
        str, Field(description='ctx_context_items.id of the exact item.')
    ]
    scopeTypeId: Annotated[
        str,
        Field(description='ctx_scope_types.id whose active scope supplies the value.'),
    ]
    itemKey: Annotated[
        str,
        Field(
            description="The item's machine key, resolved against the active scope's items."
        ),
    ]
    onMissing: Annotated[
        Literal['empty', 'skip', 'error'] | None,
        Field(
            description='What happens when no active scope supplies the value. Absent means empty.'
        ),
    ] = None


class Sort(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    field: Annotated[str, Field(description='Field key to order by.')]
    dir: Literal['asc', 'desc'] | None = None


class Transform(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: Annotated[
        str, Field(description='list | currency | number | date | upper | title.')
    ]
    template: Annotated[
        str | None,
        Field(
            description='list: per-row render with {field_key} / {field.name} / {field.id} placeholders.'
        ),
    ] = None
    join: Annotated[str | None, Field(description='list: text between rows.')] = None
    max: Annotated[
        int | None, Field(description='list: rows shown; the rest are announced.')
    ] = None
    header: Annotated[
        str | None, Field(description='list: a line placed before the rows.')
    ] = None


@kind(
    'variable_record_binding',
    disposition='envelope',
    family='input_declaration',
    maturity='distilled',
    example=source_schema('variable_record_binding')['examples'][0],
)
class VariableRecordBinding(KindModel):
    @classmethod
    def model_json_schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        # The registry row stores the source file byte for byte (rule 2: emitted, never hand-patched).
        return source_schema('variable_record_binding')

    model_config = ConfigDict(
        extra='forbid',
    )
    kind: Annotated[
        Literal['merge_field'],
        Field(description='Discriminant of a merge-field binding.'),
    ]
    source: Annotated[
        Literal['record'], Field(description='Where the value comes from.')
    ]
    semantic_type: Annotated[
        Literal['collection', 'reference', 'value'],
        Field(description='What it resolves into.'),
    ]
    table_id: Annotated[str, Field(description='The Table the value is read from.')]
    record_id: Annotated[
        str | None, Field(description='One record of that Table (reference, value).')
    ] = None
    field_key: Annotated[
        str | None, Field(description='With record_id: the one field (value).')
    ] = None
    match: Annotated[
        dict[str, Any] | None,
        Field(description='Exact-equality filter {field_key: value} for a collection.'),
    ] = None
    sort: Annotated[Sort | None, Field(description='Collection row order.')] = None
    limit: Annotated[
        int | None,
        Field(description='Collection row cap (default 40); truncation is announced.'),
    ] = None
    transform: Annotated[
        Transform | None, Field(description='How the resolved value reads.')
    ] = None
    missing: Annotated[
        Literal['absent', 'block'] | None,
        Field(
            description='absent: a named absence in the prompt (default). block: the run refuses.'
        ),
    ] = None
    override_policy: Annotated[
        Literal['must_supply', 'shown_overridable', 'shown_locked', 'server_fixed', 'derived'] | None,
        Field(
            description="How a caller-sent value is treated. Default shown_locked (the caller's value is discarded)."
        ),
    ] = None


class PickList(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    listId: Annotated[str, Field(description="The pick list's id.")]
    groupName: Annotated[
        str | None,
        Field(
            description='Only this group; otherwise every group renders as a section.'
        ),
    ] = None
    multiple: Annotated[bool | None, Field(description='Several items may be picked.')] = (
        None
    )


class Assignment(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    random: Annotated[
        bool | None,
        Field(description='A caller may ask the server to pick one option at random.'),
    ] = None


class PromoteItem(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    representation: str
    max_chars: int | None = None


class ResourceContext(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    promote: Annotated[
        list[PromoteItem] | None,
        Field(description='Bounded representations placed directly in context.'),
    ] = None
    exclude: Annotated[
        list[str] | None,
        Field(description='Representations hidden for this reference.'),
    ] = None


class Token(RootModel[str]):
    root: Annotated[str, Field(pattern='^[a-z][a-z0-9_]*$')]


class Stash(KindSubModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    options: Annotated[
        list[str] | None, Field(description='The choices (choice types).')
    ] = None
    allowOther: Annotated[
        bool | None,
        Field(description="Allow a free-text 'Other' entry beside the choices."),
    ] = None
    optionLabels: Annotated[
        dict[str, Any] | None,
        Field(description='Friendly words for machine option values: {value: label}.'),
    ] = None
    toggleValues: Annotated[
        list[str] | None,
        Field(description='[off, on] labels.', max_length=2, min_length=2),
    ] = None
    min: Annotated[float | None, Field(description='Lowest value.')] = None
    max: Annotated[float | None, Field(description='Highest value.')] = None
    step: Annotated[float | None, Field(description='Step between values.')] = None
    unit: Annotated[
        str | None, Field(description='Unit shown after the value (display only).')
    ] = None
    accept: Annotated[
        str | None,
        Field(
            description='Which files are taken, as an accept list (image/* lets a phone take a photo). Empty means any.'
        ),
    ] = None
    multiple: Annotated[
        bool | None,
        Field(
            description='The value is a list: several lines of text, several files, several records.'
        ),
    ] = None
    tokens: Annotated[
        list[Token] | None,
        Field(
            description='Entity type tokens (platform.entity_types) a record may be. Empty means any reference-pickable type.'
        ),
    ] = None


@kind(
    'variable_component',
    disposition='envelope',
    family='input_declaration',
    maturity='distilled',
    example=source_schema('variable_component')['examples'][0],
)
class VariableComponent(KindModel):
    @classmethod
    def model_json_schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        # The registry row stores the source file byte for byte (rule 2: emitted, never hand-patched).
        return source_schema('variable_component')

    model_config = ConfigDict(
        extra='forbid',
    )
    type: Annotated[
        Literal['textarea', 'text', 'toggle', 'light-switch', 'radio', 'pill-toggle', 'selection-list', 'buttons', 'checkbox', 'select', 'number', 'slider', 'datetime', 'time', 'email', 'url', 'phone', 'percent', 'color', 'markdown', 'currency', 'image', 'audio', 'video', 'youtube', 'document', 'table', 'tables', 'record'],
        Field(
            description='The control. One value per distinct component; there is no separate variant.'
        ),
    ]
    options: Annotated[
        list[str] | None, Field(description='The choices (choice types).')
    ] = None
    allowOther: Annotated[
        bool | None,
        Field(description="Allow a free-text 'Other' entry beside the choices."),
    ] = None
    optionLabels: Annotated[
        dict[str, Any] | None,
        Field(description='Friendly words for machine option values: {value: label}.'),
    ] = None
    pick_list: Annotated[
        PickList | None,
        Field(
            description='Options come from a pick list (a Table of choices); the value is a ```matrx reference fence. Read only by choice types, but allowed on every type: it stays outside stash so it survives type switches.'
        ),
    ] = None
    assignment: Annotated[
        Assignment | None,
        Field(description='Automatic-assignment strategies the author enabled.'),
    ] = None
    toggleValues: Annotated[
        list[str] | None,
        Field(description='[off, on] labels.', max_length=2, min_length=2),
    ] = None
    min: Annotated[float | None, Field(description='Lowest value.')] = None
    max: Annotated[float | None, Field(description='Highest value.')] = None
    step: Annotated[float | None, Field(description='Step between values.')] = None
    unit: Annotated[
        str | None, Field(description='Unit shown after the value (display only).')
    ] = None
    resource_context: Annotated[
        ResourceContext | None,
        Field(
            description='How a media value is presented in model context. Absent means the whole resource family. Never requests generation.'
        ),
    ] = None
    imageRole: Annotated[
        Literal['subject', 'character', 'style', 'mask', 'edit_target', 'composition_control', 'first_frame', 'last_frame', 'asset', 'extend', 'restyle', 'lip_sync'] | None,
        Field(
            description='The reference role this media input fills (image, video or audio roles).'
        ),
    ] = None
    accept: Annotated[
        str | None,
        Field(
            description='Which files are taken, as an accept list (image/* lets a phone take a photo). Empty means any.'
        ),
    ] = None
    multiple: Annotated[
        bool | None,
        Field(
            description='The value is a list: several lines of text, several files, several records.'
        ),
    ] = None
    tokens: Annotated[
        list[Token] | None,
        Field(
            description='Entity type tokens (platform.entity_types) a record may be. Empty means any reference-pickable type.'
        ),
    ] = None
    stash: Annotated[
        Stash | None,
        Field(
            description='Settings kept for other component types while this one is shown, so switching type and back loses nothing. Never read for rendering.'
        ),
    ] = None


@kind(
    'variable_definition',
    disposition='envelope',
    family='input_declaration',
    maturity='distilled',
    example=source_schema('variable_definition')['examples'][0],
)
class VariableDefinition(KindModel):
    @classmethod
    def model_json_schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        # The registry row stores the source file byte for byte (rule 2: emitted, never hand-patched).
        return source_schema('variable_definition')

    model_config = ConfigDict(
        extra='forbid',
    )
    name: Annotated[
        str,
        Field(
            description='The key messages use as {{name}} and the value is stored under: letters, digits, underscore.',
            min_length=1,
        ),
    ]
    label: Annotated[
        str | None,
        Field(
            description='What the person called it ("Normal Text"); every screen shows it. Absent means the humanized name.'
        ),
    ] = None
    defaultValue: Annotated[
        Any | None,
        Field(
            description='The value used when no one supplies one. Any JSON; its shape follows customComponent.type (see x-valueShapes). For record it is a relation or a list of relations.'
        ),
    ] = None
    helpText: Annotated[str | None, Field(description='Help shown under the field.')] = (
        None
    )
    purpose: Annotated[
        str | None,
        Field(
            description='What the value is for, in one line, for callers (API, Mandates, agents). Shown when helpText is empty.'
        ),
    ] = None
    required: Annotated[
        bool | None,
        Field(description='Must be supplied before the run starts, from any source.'),
    ] = None
    sourcing: Annotated[
        Literal['', 'ask', 'require', 'optional'] | None,
        Field(
            description='Who supplies it: ask (a person answers every time, even on a programmatic start), require (must be present from any source), optional (never blocks). Empty means derived from required.'
        ),
    ] = None
    customComponent: Annotated[
        VariableComponent | None,
        Field(
            description='The control this input renders as. Absent means a textarea. Ignored while binding is set (a context item supplies its own).'
        ),
    ] = None
    binding: Annotated[
        VariableContextBinding | VariableRecordBinding | None,
        Field(
            description="When set, the value is filled at run time: from a scope context item, or from the author's own data (a merge field)."
        ),
    ] = None
    control: Annotated[
        Control | None,
        Field(
            description="When set, this input is a model control (aspect_ratio, quality, tts_voice...): its value is sent as that control and defaultValue is the agent's value."
        ),
    ] = None
    valueKind: Annotated[
        str | None,
        Field(
            description='The registered kind slug the value is (json, search_request, string_list...). Empty means derived from customComponent.type. A structured kind gives the value its contract and the form a structured editor.',
            pattern='^$|^[a-z][a-z0-9_]*$',
        ),
    ] = None
    valueVariant: Annotated[
        str | None,
        Field(
            description="A presentation variant registered on valueKind, selected by name. Empty means the kind's default component."
        ),
    ] = None
    hints: Annotated[
        Hints | None,
        Field(
            description='How the input sits on a simple run form (the one box, chips, a Tools reveal). Every hint is optional; absent means inferred.'
        ),
    ] = None


__all__ = [
    'Assignment',
    'Control',
    'Hints',
    'PickList',
    'PromoteItem',
    'ResourceContext',
    'Sort',
    'Stash',
    'Token',
    'Transform',
    'VariableComponent',
    'VariableContextBinding',
    'VariableDefinition',
    'VariableRecordBinding',
]
