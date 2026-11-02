"""data.map_template — reshape every element of a list with a template.

Written when the sandbox behind ``data.transform`` had no loops (it has list
loops since 2026-10-27, which also filter and total). This node applies
one ``$item`` / ``$in`` template (same mini-language as ``control.map``'s
``payload_template``, shared in ``nodes/_template.py``) to every element and
returns the new list. Typical uses: project search results down to URLs,
shape scraped pages into agent variables, attach an upstream constant to
every element before a fan-out.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.nodes._template import run_facts_of, substitute_template
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class MapTemplateInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[JsonValue] = Field(
        default_factory=list,
        description="The list to reshape — the template is applied to each element.",
    )
    limit: int | None = Field(
        default=None,
        ge=0,
        description=(
            "Optional cap on how many elements are processed (after "
            "require-path filtering). Mappable from an upstream value — e.g. "
            "a user-chosen depth — or set statically. None processes all."
        ),
    )


class MapTemplateOutput(KindModel, kind="mapped_list_result"):
    values: list[JsonValue] = Field(
        default_factory=list,
        description="The reshaped elements, in input order.",
    )
    count: int = Field(default=0, description="How many elements were produced.")
    dropped: int = Field(
        default=0,
        description="How many input elements were filtered out by `require_path` "
        "or the `limit` cap.",
    )


class MapTemplateConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template: JsonValue = Field(
        default="$item",
        description=(
            "Per-element output shape. Every string value '$item' is replaced "
            "by the element, '$item.<dot.path>' by that path into the element "
            "(digit segments index lists), and '$in' / '$in.<dot.path>' by this "
            "node's OTHER inputs (everything delivered on its edges besides "
            "`items` and `limit`) — so upstream values can be attached to every "
            "element. '$index' is the element's 0-based position, and "
            "{'$cycle': [a, b, c]} round-robins a literal pool across the list "
            "(element i gets pool[i % len(pool)]) — how a fan-out rotates "
            "Mandates or any other per-item setting. Non-ref values pass "
            "through literally, recursing into nested dicts/lists. A path that "
            "does not resolve FAILS the node (parks, recoverable)."
        ),
        json_schema_extra=field_extras(
            widget="json",
            placeholder='{"url": "$item.url", "topic": "$in.topic"}',
        ),
    )
    require_path: str | None = Field(
        default=None,
        description=(
            "Optional dot-path into each element; elements where the path is "
            "missing or falsy (None, '', 0, false, empty list) are dropped "
            "before the template is applied. Use to keep only usable rows, "
            "e.g. 'text' to drop scrapes with no content."
        ),
        json_schema_extra=field_extras(widget="text", placeholder="text"),
    )


def _path_truthy(item: JsonValue, path: str) -> bool:
    val: JsonValue = item
    for part in path.split("."):
        if isinstance(val, list):
            try:
                val = val[int(part)]
            except (IndexError, ValueError):
                return False
        elif isinstance(val, dict):
            if part not in val:
                return False
            val = val[part]
        else:
            return False
    return bool(val)


class MapTemplateExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.map_template",
        category=NodeCategory.DATA,
        display_name="Reshape List",
        description="Change each item in a list (pick, rename, and adjust fields) without code.",
        input_schema=MapTemplateInput,
        output_schema=MapTemplateOutput,
        config_schema=MapTemplateConfig,
        output_kind="mapped_list_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="list-tree",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: MapTemplateInput,
        config: MapTemplateConfig,
    ) -> NodeResult[MapTemplateOutput]:
        extra = {
            k: v for k, v in inputs.model_dump(mode="json").items() if k not in ("items", "limit")
        }
        kept = [
            item
            for item in inputs.items
            if config.require_path is None or _path_truthy(item, config.require_path)
        ]
        capped = kept if inputs.limit is None else kept[: inputs.limit]
        values = [
            substitute_template(config.template, item, index=i, extra=extra, run=run_facts_of(ctx))
            for i, item in enumerate(capped)
        ]
        return success(
            MapTemplateOutput(
                values=values,
                count=len(values),
                dropped=len(inputs.items) - len(values),
            )
        )
