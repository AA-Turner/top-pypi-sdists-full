"""``data.pick`` + ``data.omit`` — key projection over a dict.

Pick keeps the listed keys and drops everything else. Omit is the inverse.
Both accept dotted paths for nested access (``user.address.street``) but only
at the top level of the record — nested dicts are returned as-is once reached.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.nodes.data.merge import MergeOutput
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class _PickOmitInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    record: dict[str, JsonValue] = Field(description="The source record.")


class _PickOmitConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    keys: tuple[str, ...] = Field(
        min_length=1,
        description=(
            "Top-level keys to project. Dotted paths (``a.b.c``) dig into "
            "nested dicts; the resolved leaf lands at the leaf key in output."
        ),
        json_schema_extra=field_extras(widget="tag_input"),
    )


#: Pick and Omit both answer with one reshaped record — the SAME contract
#: ``data.merge`` owns as ``record_result``. One kind, one model (§10d-B2).
_PickOmitOutput = MergeOutput


def _get_path(record: dict[str, Any], path: str) -> tuple[bool, Any]:
    """Walk `record` by dotted path. Returns (found, value)."""
    current: Any = record
    parts = path.split(".")
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


class PickExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.pick",
        category=NodeCategory.DATA,
        display_name="Pick Fields",
        description="Keep only the fields you choose from a record.",
        input_schema=_PickOmitInput,
        output_schema=_PickOmitOutput,
        config_schema=_PickOmitConfig,
        output_kind="record_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="filter",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: _PickOmitInput,
        config: _PickOmitConfig,
    ) -> NodeResult[_PickOmitOutput]:
        _ = ctx
        out: dict[str, Any] = {}
        for key in config.keys:
            found, value = _get_path(inputs.record, key)
            if found:
                leaf = key.split(".")[-1]
                out[leaf] = value
        return success(_PickOmitOutput(result=out))


class OmitExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.omit",
        category=NodeCategory.DATA,
        display_name="Remove Fields",
        description="Remove the fields you choose from a record.",
        input_schema=_PickOmitInput,
        output_schema=_PickOmitOutput,
        config_schema=_PickOmitConfig,
        output_kind="record_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="filter-x",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: _PickOmitInput,
        config: _PickOmitConfig,
    ) -> NodeResult[_PickOmitOutput]:
        _ = ctx
        # For omit, only top-level key stripping is supported (dotted paths
        # would require a deep-copy to avoid mutating nested structures).
        drop_top = {k.split(".")[0] for k in config.keys if "." not in k}
        return success(
            _PickOmitOutput(result={k: v for k, v in inputs.record.items() if k not in drop_top})
        )
