"""``data.flatten`` — one flat list out of a list of lists.

The primitive a fan-in has always needed and never had. When ``control.map``
fans a node and a downstream node joins the results, each delivery arrives
wrapped as ``{"error": ..., "value": <the mapped fragment>}`` and the joined
input is a LIST of those envelopes. Every per-item node downstream (``data.filter``,
``data.sort``, ``data.dedupe``) then sees envelopes where the author meant to
see the items inside them — which is exactly how the Masterwork ``generate``
shape died for four days on ``KeyError: 'rule_id'`` (2026-08-21): its citation
gate filtered five fan envelopes as if they were five audit verdicts.

``path`` is the dot-path to the list inside each element (``"value.items"`` for
the fan envelope above); leave it empty when the elements are already lists.
A missing path or a non-list at the end of it is a LOUD failure, never a
silent skip — a flatten that quietly drops a source is how a load-bearing gate
gets to pass on data it never saw.

``carry`` unnests WITHOUT losing the parent: ``{child_field: parent_path}`` copies
each parent's value (a missing one is null) onto every child it held, so "which
group is this item in" or "which query found this result" survives the flatten.
``source_index_as`` / ``index_as`` stamp the parent's and the child's positions.
Two review flags keep it honest: ``flatten.carry_overwrote`` when a stamped field
replaced a child's own value, ``flatten.carry_missing`` when a carry path found
nothing in any parent (a typo reads as a whole null column otherwise). Names must
be distinct and non-empty; carrying onto a child that is not an object is refused
unless ``value_as`` names the field a plain child (text, number, yes/no, list) is
wrapped under first — ``{"engines": ["brave", "google"]}`` with ``path: engines``,
``value_as: engine`` and ``carry: {query: query}`` gives one ``{engine, query}`` per
engine, so a search set expands into one call per engine with no copied arm.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_graph.content_ir.model import KindModel
from matrx_graph.errors import ExecutionError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class FlattenInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[JsonValue] = Field(description="The list of lists (or of wrappers) to flatten.")


class FlattenConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(
        default="",
        description=(
            "Dot-path to the list inside each element. Empty means the element "
            "IS the list. For a fanned join use 'value.items'."
        ),
        json_schema_extra=field_extras(placeholder="value.items"),
    )
    carry: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Keep fields of the item each child came from: {child field: path in that item}, "
            "e.g. {'territory': 'territory'}. A missing value is null; the parent's value wins "
            "over a child field of the same name (raised as a review flag)."
        ),
    )
    source_index_as: str = Field(
        default="", description="Also write the position of the item each child came from under this field."
    )
    index_as: str = Field(default="", description="Also write each child's position inside its item under this field.")
    value_as: str = Field(
        default="",
        description=(
            "With carry/index settings: a child that is not an object (text, number, list) becomes "
            "{this field: the child} so fields can be carried onto it, e.g. 'engine' for a list of engine names. "
            "Empty: such a child is refused."
        ),
    )

    @model_validator(mode="after")
    def _carry_needs_a_path(self) -> FlattenConfig:
        if self.value_as and not (self.carry or self.source_index_as or self.index_as):
            raise ValueError(
                "data.flatten: value_as wraps a plain child so fields can be carried onto it — set carry, "
                "source_index_as or index_as too (without them a plain list flattens as it is)."
            )
        if (self.carry or self.source_index_as or self.index_as) and not self.path:
            raise ValueError(
                "data.flatten: carry, source_index_as and index_as need 'path' — they copy fields of the item "
                "that holds each list, and with no path the item IS the list."
            )
        if any(not k.strip() or not v.strip() for k, v in self.carry.items()):
            raise ValueError("data.flatten: every carry entry needs a field name and a path in the parent item.")
        names = [*self.carry, *(n for n in (self.source_index_as, self.index_as, self.value_as) if n)]
        repeated = sorted({n for n in names if names.count(n) > 1})
        if repeated:
            raise ValueError(
                f"data.flatten: {', '.join(repeated)} is named more than once across carry, source_index_as, "
                "index_as and value_as — each would silently overwrite the other. Give each its own field name."
            )
        return self


class FlattenOutput(KindModel, kind="flattened_list_result"):
    items: list[JsonValue] = Field(description="Every inner element, in source order.")
    count: int = Field(description="How many elements the flat list holds.")
    sources: int = Field(description="How many input elements were flattened.")


def _dig(element: JsonValue, path: str, index: int) -> JsonValue:
    """Walk ``path`` on one element, naming what was actually there on a miss."""
    current: JsonValue = element
    walked: list[str] = []
    for part in path.split("."):
        walked.append(part)
        if not isinstance(current, dict):
            raise ExecutionError(
                f"data.flatten: item {index} has no '{'.'.join(walked)}' — "
                f"'{'.'.join(walked[:-1]) or 'the item'}' is a "
                f"{type(current).__name__}, not an object."
            )
        if part not in current:
            raise ExecutionError(
                f"data.flatten: item {index} has no '{'.'.join(walked)}'. "
                f"Its keys are {sorted(current)}."
            )
        current = current[part]
    return current


class FlattenExecutor:
    """Concatenate the inner lists into one, in order."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.flatten",
        category=NodeCategory.DATA,
        display_name="Flatten",
        description="Turn a list of lists into one flat list.",
        input_schema=FlattenInput,
        input_kind="items",
        output_schema=FlattenOutput,
        config_schema=FlattenConfig,
        output_kind="flattened_list_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="list-collapse",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: FlattenInput,
        config: FlattenConfig,
    ) -> NodeResult[FlattenOutput]:
        flat: list[JsonValue] = []
        overwritten: dict[str, int] = {}
        found: set[str] = set()
        stamping = bool(config.carry or config.source_index_as or config.index_as)
        for index, element in enumerate(inputs.items):
            inner = _dig(element, config.path, index) if config.path else element
            if not isinstance(inner, list):
                where = f"'{config.path}' of item {index}" if config.path else f"item {index}"
                raise ExecutionError(
                    f"data.flatten: {where} is a {type(inner).__name__}, not a list. "
                    "Every element must carry a list to flatten."
                )
            if not stamping:
                flat.extend(inner)
                continue
            stamp: dict[str, JsonValue] = {}
            for name, src in config.carry.items():
                value, hit = _parent_value(element, src)
                stamp[name] = value
                if hit:
                    found.add(name)
            if config.source_index_as:
                stamp[config.source_index_as] = index
            for position, child in enumerate(inner):
                if not isinstance(child, dict) and config.value_as:
                    child = {config.value_as: child}
                if not isinstance(child, dict):
                    raise ExecutionError(
                        f"data.flatten: child {position} of item {index} is a {type(child).__name__}, not an "
                        "object, so fields cannot be carried onto it. Set value_as to wrap it (e.g. 'engine'), "
                        "remove carry/index settings, or flatten a list of objects."
                    )
                row = dict(child)
                if config.index_as:
                    stamp[config.index_as] = position
                for k in stamp:
                    if k in row:
                        overwritten[k] = overwritten.get(k, 0) + 1
                row.update(stamp)
                flat.append(row)
        if ctx is not None and overwritten:
            total = sum(overwritten.values())
            await ctx.flag_for_review(
                "flatten.carry_overwrote",
                f"{total} child field value(s) were replaced by a stamped value "
                f"({', '.join(f'{k}: {n}' for k, n in sorted(overwritten.items()))}).",
                category="unexpected_path",
                payload={"overwritten": total, "fields": dict(sorted(overwritten.items()))},
            )
        missing = sorted(set(config.carry) - found) if inputs.items else []
        if ctx is not None and missing:
            await ctx.flag_for_review(
                "flatten.carry_missing",
                f"carry path(s) found nothing in any item, so the field is null on every child: "
                f"{', '.join(f'{n} <- {config.carry[n]}' for n in missing)}.",
                category="unexpected_path",
                payload={"fields": {n: config.carry[n] for n in missing}},
            )
        return success(FlattenOutput(items=flat, count=len(flat), sources=len(inputs.items)))


def _parent_value(element: JsonValue, path: str) -> tuple[JsonValue, bool]:
    """(value, found) at a dotted ``path`` on the parent item — a digit step indexes a list; a missing step is
    (None, False): a hole, not a refusal (the step flags a path that found nothing in any parent)."""
    current: JsonValue = element
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return None, False
    return current, True
