"""text.render_list — render a list into one LLM-ready text block.

The generic bridge between structured lists (search results, page analyses,
gathered agent outputs) and the formatted text an agent variable expects.
Each element is rendered through a per-item template whose ``{dot.path}``
placeholders resolve into the element; items are joined with a separator
under an optional header. Bounded by ``max_items`` / ``max_chars_per_item``
so one oversized list cannot blow an agent's context window.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.nodes._template import render_template_string
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class RenderListInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[JsonValue] = Field(
        default_factory=list,
        description="The list to render — one template pass per element.",
    )


class RenderListOutput(KindModel, kind="rendered_text"):
    text: str = Field(default="", description="The rendered text block.")
    rendered: int = Field(default=0, description="How many elements were rendered.")
    truncated: bool = Field(
        default=False,
        description="True when max_items dropped elements or any per-item "
        "value was cut at max_chars_per_item.",
    )


class RenderListConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_template: str = Field(
        default="{item}",
        min_length=1,
        description=(
            "Per-element template. '{item}' inserts the whole element; "
            "'{<dot.path>}' inserts that path into the element (digit "
            "segments index lists). A missing path renders as '' — "
            "formatting stays best-effort, it never parks a run. Non-string "
            "values are JSON-encoded. '{#path}…{/path}' repeats its text for "
            "each element of a nested list ('{#key_facts}- {item}\\n{/key_facts}'; "
            "inside, '{item}' is the element and '{field}' a field of it); "
            "'{^path}…{/path}' shows its text only when that list is empty."
        ),
        json_schema_extra=field_extras(
            widget="textarea",
            placeholder="- {title} ({url}): {description}",
        ),
    )
    separator: str = Field(
        default="\n\n",
        description="Text placed between rendered elements.",
        json_schema_extra=field_extras(widget="text"),
    )
    header: str = Field(
        default="",
        description="Optional text placed once before the first element.",
        json_schema_extra=field_extras(widget="textarea"),
    )
    empty_text: str = Field(
        default="",
        description="Output when the list is empty (header is NOT emitted).",
        json_schema_extra=field_extras(widget="text"),
    )
    max_items: int | None = Field(
        default=None,
        ge=1,
        description="Render at most this many elements (in input order). None renders all.",
        json_schema_extra=field_extras(widget="number"),
    )
    max_chars_per_item: int | None = Field(
        default=None,
        ge=1,
        description="Cap each interpolated VALUE at this many characters "
        "(appending '…'). Bounds one huge page/summary, not the template "
        "text. None means uncapped.",
        json_schema_extra=field_extras(widget="number"),
    )


class RenderListExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.render_list",
        category=NodeCategory.DATA,
        display_name="Format List as Text",
        description="Turn a list into one readable block of text using a template for each item.",
        input_schema=RenderListInput,
        output_schema=RenderListOutput,
        config_schema=RenderListConfig,
        output_kind="rendered_text",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="text-quote",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: RenderListInput,
        config: RenderListConfig,
    ) -> NodeResult[RenderListOutput]:
        items = inputs.items
        if not items:
            return success(RenderListOutput(text=config.empty_text, rendered=0))

        truncated = False
        if config.max_items is not None and len(items) > config.max_items:
            items = items[: config.max_items]
            truncated = True

        rendered_parts: list[str] = []
        for item in items:
            text, cut = render_template_string(
                config.item_template, item, max_chars=config.max_chars_per_item
            )
            rendered_parts.append(text)
            truncated = truncated or cut

        body = config.separator.join(rendered_parts)
        text = (config.header + body) if config.header else body
        return success(
            RenderListOutput(text=text, rendered=len(rendered_parts), truncated=truncated)
        )
