"""``data.merge`` — shallow merge of two dicts.

For combining payloads from multiple upstream nodes into a single record
without writing a `data.transform` expression. `base` is the starting point;
`overlay` keys win on collision.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success


class MergeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Base record. Keys not present in `overlay` pass through.",
    )
    overlay: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Overlay record. Keys here win on collision.",
    )


class MergeOutput(KindModel, kind="record_result"):
    """THE ``record_result`` kind — one model for every node that answers with
    a single reshaped record (``data.merge``, ``data.pick``, ``data.omit``)."""

    result: dict[str, JsonValue] = Field(description="The resulting record.")


class MergeExecutor:
    """Shallow dict merge — `{**base, **overlay}` semantics."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.merge",
        category=NodeCategory.DATA,
        display_name="Merge",
        description="Combine two records into one; the second wins where they overlap.",
        input_schema=MergeInput,
        output_schema=MergeOutput,
        output_kind="record_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="merge",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: MergeInput,
        config: BaseModel,
    ) -> NodeResult[MergeOutput]:
        _ = ctx, config
        return success(MergeOutput(result={**inputs.base, **inputs.overlay}))
