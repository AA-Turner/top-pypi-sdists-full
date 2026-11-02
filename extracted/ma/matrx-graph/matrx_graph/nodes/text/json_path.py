"""``text.json_path`` — read a value from a JSON/dict by dotted + indexed path.

Why a dedicated node: ``data.pick`` is single-level per-key; ``data.transform``
can't dig into nested structures because the sandbox allows subscripts but
not the "try each level gracefully" pattern. This fills the gap with a
forgiving reader that never raises — a missing path returns ``default``.

The grammar and the walk live in ``matrx_graph.paths`` — THE ONE source-path
resolver, shared with edge mappings and display steps.

Path grammar:
    ``a.b.c``                 — walk dicts by key
    ``a[0]`` / ``a[-1]``      — index into lists (supports negatives)
    ``a.b[2].c``              — mixed
    ``a\\.b``                 — backslash-escape literal dot in a key
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.paths import resolve_path
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class JsonPathInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: JsonValue = Field(description="JSON-like structure (dict / list / scalar).")


class JsonPathConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(
        min_length=1,
        description="Dotted + indexed path, e.g. ``data.users[0].name``.",
        json_schema_extra=field_extras(widget="text", placeholder="data.items[0].name"),
    )
    default: JsonValue = Field(
        default=None,
        description="Returned as ``value`` when the path doesn't resolve.",
    )


class JsonPathOutput(KindModel, kind="json_path_result"):
    found: bool = Field(
        description="True when the path resolved to a value; false when a segment was missing."
    )
    value: JsonValue = Field(
        default=None,
        description="The value at the path, or the configured default when not found.",
    )


class JsonPathExecutor:
    """Read a value from a nested structure by path. Never raises on miss."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.json_path",
        category=NodeCategory.DATA,
        display_name="Get a Value",
        description="Pull one value out of nested data by its path.",
        input_schema=JsonPathInput,
        input_kind="value",
        output_schema=JsonPathOutput,
        config_schema=JsonPathConfig,
        output_kind="json_path_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="file-search",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: JsonPathInput,
        config: JsonPathConfig,
    ) -> NodeResult[JsonPathOutput]:
        _ = ctx
        found, value = resolve_path(inputs.value, config.path)
        # A miss is DOMAIN data by design ("forgiving reader that never
        # raises") — found=False + default is a Success, not a Failure.
        if not found:
            return success(JsonPathOutput(found=False, value=config.default))
        return success(JsonPathOutput(found=True, value=value))
