"""``data.apportion`` — share a whole number out across a list, in proportion to weights.

"Make 40 questions across these 6 sections, more where there is more text" — and the
shares must add up to exactly 40. Rounding each part's share on its own drifts (39, 41),
so the split is the shared largest-remainder splitter
(:func:`matrx_utils.splitting.apportion`), the same one ``data.batch``'s ``quota_total``
and the study-kit planners run. Nothing here knows what is being shared.

Optional per-share call split: with ``items_per_call`` each share is cut into calls of at
most that many (``max_calls`` caps how many calls one share may take; the calls then carry
more each), evenly, earlier calls taking the extra one. ``calls`` is one flat row per call
— ``{part, call, of, count}`` — ready for a For Each.
"""

from __future__ import annotations

import math
from typing import ClassVar

from matrx_utils.splitting import apportion
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.accessor import resolve_path
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


class ApportionInput(KindModel, kind="apportion_request"):

    items: list[JsonValue] = Field(
        description=(
            "One entry per part: a number (its weight), or a record whose weight sits at "
            "`weight_path`."
        )
    )
    total: int | None = Field(
        default=None, ge=0, description="The whole number to share out. Wins over the step's own total."
    )
    items_per_call: int | None = Field(
        default=None,
        ge=1,
        description="Cut each share into calls of at most this many. Wins over the step's own setting.",
    )
    min_each: int | None = Field(
        default=None, ge=0, description="Every part gets at least this. Wins over the step's own setting."
    )


class ApportionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total: int | None = Field(default=None, ge=0, le=10_000_000, description="The whole number to share out.")
    weight_path: str = Field(
        default="",
        description="Path to each record's weight (e.g. 'size'). Empty: each entry IS its weight.",
    )
    min_each: int = Field(default=0, ge=0, le=1_000_000, description="Every part gets at least this.")
    items_per_call: int | None = Field(
        default=None,
        ge=1,
        le=1_000_000,
        description="Cut each share into calls of at most this many (the `calls` list). Empty: no calls.",
    )
    max_calls: int | None = Field(
        default=None,
        ge=1,
        le=10_000,
        description="At most this many calls per share; past it each call carries more than items_per_call.",
    )


class ApportionPart(KindSubModel):
    index: int = Field(description="Position of the part in `items`, from 0.")
    weight: float = Field(description="The weight it was shared by.")
    share: int = Field(description="Its whole-number share of the total.")
    calls: int = Field(default=0, description="How many calls its share was cut into (0 without items_per_call).")
    call_counts: list[int] = Field(default_factory=list, description="How many each of its calls carries.")


class ApportionCall(KindSubModel):
    part: int = Field(description="The part this call belongs to (its index).")
    call: int = Field(description="This call's number within its part, from 1.")
    of: int = Field(description="How many calls the part has.")
    count: int = Field(description="How many this call carries.")


class ApportionOutput(KindModel, kind="apportioned_shares"):
    shares: list[int] = Field(description="Each part's share, index-aligned with `items`.")
    total: int = Field(description="The sum of the shares.")
    asked: int = Field(description="The total that was asked for.")
    exact: bool = Field(description="True when the shares sum to exactly what was asked.")
    parts: list[ApportionPart] = Field(description="Per part: weight, share and its call split.")
    calls: list[ApportionCall] = Field(
        default_factory=list, description="One row per call across every part, in order (with items_per_call)."
    )
    notes: list[str] = Field(default_factory=list, description="What could not be done exactly as asked.")


class _Refused(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _weight(item: JsonValue, path: str, index: int) -> float:
    value: object = item
    if path:
        found = resolve_path(item, path, unwrap_root=False).values
        if len(found) != 1:
            raise _Refused(
                "weight_missing",
                f"Item {index} has no single weight at '{path}' (found {len(found)} values).",
            )
        value = found[0]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        where = f" at '{path}'" if path else ""
        raise _Refused(
            "weight_not_a_number",
            f"Item {index}'s weight{where} is {value!r}, not a number.",
        )
    if value < 0 or math.isnan(value) or math.isinf(value):
        raise _Refused("weight_negative", f"Item {index}'s weight is {value}; weights are 0 or more.")
    return float(value)


def split_evenly(share: int, calls: int) -> list[int]:
    """``share`` across ``calls`` as evenly as whole numbers allow, earlier calls taking the extra."""
    return apportion([1] * calls, share, min_each=0) if calls > 0 else []


def plan_apportion(
    items: list[JsonValue],
    total: int,
    *,
    weight_path: str = "",
    min_each: int = 0,
    items_per_call: int | None = None,
    max_calls: int | None = None,
) -> ApportionOutput:
    """The pure planner behind ``data.apportion`` (tested without an engine)."""
    weights = [_weight(item, weight_path, i) for i, item in enumerate(items)]
    notes: list[str] = []
    shares = apportion(weights, total, min_each=min_each, floor_weight=0)
    if weights and not any(weights) and total > len(weights) * min_each:
        notes.append("Every weight is 0, so the total was shared evenly.")
    if sum(shares) != total and weights:
        notes.append(
            f"{len(weights)} parts each get at least {min_each}, so the shares sum to {sum(shares)}, "
            f"not the {total} asked for."
        )
    if not weights and total:
        notes.append(f"No parts were given, so none of the {total} was shared.")
    parts: list[ApportionPart] = []
    calls: list[ApportionCall] = []
    capped = 0
    for index, (weight, share) in enumerate(zip(weights, shares, strict=True)):
        counts: list[int] = []
        if items_per_call is not None and share > 0:
            n = -(-share // items_per_call)
            if max_calls is not None and n > max_calls:
                n, capped = max_calls, capped + 1
            counts = split_evenly(share, n)
            calls.extend(
                ApportionCall(part=index, call=k + 1, of=n, count=c) for k, c in enumerate(counts)
            )
        parts.append(
            ApportionPart(index=index, weight=weight, share=share, calls=len(counts), call_counts=counts)
        )
    if capped:
        notes.append(
            f"{capped} part(s) hit max_calls={max_calls}, so their calls carry more than "
            f"items_per_call={items_per_call} each."
        )
    return ApportionOutput(
        shares=shares,
        total=sum(shares),
        asked=total,
        exact=sum(shares) == total,
        parts=parts,
        calls=calls,
        notes=notes,
    )


class ApportionExecutor:
    """Share a whole number across a list by weight — exact sum, optional per-call split."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.apportion",
        category=NodeCategory.DATA,
        display_name="Split a Total",
        description=(
            "Share a number across a list in proportion to each entry's weight; the shares "
            "always add up to the total. Optionally cut each share into calls of N."
        ),
        input_schema=ApportionInput,
        input_kind="apportion_request",
        output_schema=ApportionOutput,
        config_schema=ApportionConfig,
        output_kind="apportioned_shares",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="pie-chart",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ApportionInput,
        config: ApportionConfig,
    ) -> NodeResult[ApportionOutput]:
        _ = ctx
        total = inputs.total if inputs.total is not None else config.total
        if total is None:
            return failure(
                "missing_total",
                "data.apportion needs a total — set one on the step or feed `total` in on an edge.",
            )
        try:
            return success(
                plan_apportion(
                    inputs.items,
                    total,
                    weight_path=config.weight_path,
                    min_each=inputs.min_each if inputs.min_each is not None else config.min_each,
                    items_per_call=(
                        inputs.items_per_call if inputs.items_per_call is not None else config.items_per_call
                    ),
                    max_calls=config.max_calls,
                )
            )
        except _Refused as refused:
            return failure(refused.code, str(refused))


__all__ = [
    "ApportionCall",
    "ApportionConfig",
    "ApportionExecutor",
    "ApportionInput",
    "ApportionOutput",
    "ApportionPart",
    "plan_apportion",
    "split_evenly",
]
