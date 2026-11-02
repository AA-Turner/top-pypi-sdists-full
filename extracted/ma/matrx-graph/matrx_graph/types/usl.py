from __future__ import annotations

from typing import Any, Literal, TypedDict

from pydantic import BaseModel


class USLFieldHints(TypedDict, total=False):
    """Recommended json_schema_extra keys for Pydantic Field metadata.

    These keys end up in the exported JSON Schema under the matching property,
    where the Studio UI reads them to pick widgets, ordering, grouping,
    show/hide rules, and cross-field dependencies.

    Keep this vocabulary small and stable. New widgets should be added to the
    Literal where possible so adoption is type-checked at authoring time.
    """

    widget: Literal[
        "text",
        "textarea",
        "number",
        "slider",
        "toggle",
        "select",
        "radio",
        "multiselect",
        "tag_input",
        "code",
        "json",
        "color",
        "file",
        "user_picker",
        "model_picker",
        "tool_picker",
        "action_picker",
        "channel_picker",
        "secret",
    ]
    order: int
    group: str
    placeholder: str
    help: str
    readonly: bool
    hidden: bool
    visible_if: str
    enabled_if: str
    multiline_rows: int
    monospace: bool
    format: str
    min_items: int
    max_items: int
    #: On a ``model_picker`` field: the sibling key its chosen CLASS (an
    #: ai.offering id) is saved under — the picker writes both together.
    class_field: str
    #: On that sibling: the model field it is the class of.
    model_class_of: str


def field_extras(
    *,
    widget: str | None = None,
    order: int | None = None,
    group: str | None = None,
    placeholder: str | None = None,
    help: str | None = None,
    readonly: bool | None = None,
    hidden: bool | None = None,
    visible_if: str | None = None,
    enabled_if: str | None = None,
    renders_template: bool | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """Construct a json_schema_extra dict for a Pydantic Field.

    ``renders_template=True`` declares that the step FILLS ``{{placeholders}}`` in this one
    input (a message body, a send-once key) — the save gate then accepts them there and
    still refuses them in every other input of the step (``RENDERS_TEMPLATE_KEY``).

    Usage::

        class MyConfig(BaseModel):
            prompt: str = Field(
                description="The prompt to send to the model",
                json_schema_extra=field_extras(widget="textarea", multiline_rows=6),
            )

    Only non-None hints are emitted so the resulting JSON Schema stays terse.
    """
    out: dict[str, Any] = {}
    if widget is not None:
        out["ui:widget"] = widget
    if order is not None:
        out["ui:order"] = order
    if group is not None:
        out["ui:group"] = group
    if placeholder is not None:
        out["ui:placeholder"] = placeholder
    if help is not None:
        out["ui:help"] = help
    if readonly is not None:
        out["ui:readonly"] = readonly
    if hidden is not None:
        out["ui:hidden"] = hidden
    if visible_if is not None:
        out["ui:visible_if"] = visible_if
    if enabled_if is not None:
        out["ui:enabled_if"] = enabled_if
    if renders_template:
        out[RENDERS_TEMPLATE_KEY] = True
    for k, v in extra.items():
        out[f"ui:{k}"] = v
    return out


#: JSON-schema mark on ONE input property: the step renders placeholders in it.
RENDERS_TEMPLATE_KEY = "x-renders-template"


def model_usl_descriptor(model: type[BaseModel]) -> dict[str, Any]:
    """Return the JSON Schema for a Pydantic model with USL hints preserved.

    Pydantic already emits `json_schema_extra` into the exported schema, so this
    is a thin wrapper today. Kept as a seam so Phase 3+ can add cross-field
    validation descriptors, conditional branches, and eventually codegen without
    touching callers.
    """
    return model.model_json_schema()
