"""``data.join`` — match the items of one list to the items of another by key.

The general problem (generic-only, 2026-10-27, approved by Arman for Smart Add
unit 7 "Is this a match?"): an agent answers about candidates by short id and
the answers must go back onto the candidates; a triage row must find its story;
a profile photo must find its account's decision; an enrichment row must find
its CRM contact. Without a join, workflows zip by position (fragile) or build
rules + sort + ``items.0`` per item. This is the one primitive for the class.

``items`` is the list kept (left); ``other`` is the list looked up (right).
Each left item gets the right item(s) sharing its key — nested under ``as``
or merged onto it. Left items with no match are kept (``keep_unmatched``) or
dropped; right items no left item asked for come back in ``other_unmatched``
(e.g. answers about ids that were never sent). A key path that resolves to
nothing never matches (a hole is an absence, never "equal to another hole").

Users: Smart Add "Is this a match?" (answers → candidates, photo → its
account's decision), news monitor (triage rows / angle sets → stories, batch
answers → their jobs), CRM enrichment rows → contacts.
"""

from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes.data.collections import _fold_text, _identity, _key_of
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success


class JoinInput(KindModel, kind="join_request"):
    """Kind ``join_request``, registered in ``aidream/kinds/data_ops.py`` (ships with this code)."""

    model_config = ConfigDict(extra="forbid")

    items: list[JsonValue] = Field(description="The list kept: each item looks up its match in `other`.")
    other: list[JsonValue] = Field(
        default_factory=list,
        description="The list looked up (answers, decisions, enrichment rows …).",
    )


class JoinConfig(BaseModel):
    key: str = Field(
        default="",
        description="Dot path of the key on each `items` entry ('' = the item itself), e.g. 'id' or 'account.key'.",
    )
    other_key: str | None = Field(
        default=None,
        description="Dot path of the key on each `other` entry. Empty = the same path as `key`.",
    )
    normalize: Literal["none", "case_space"] = Field(
        default="none",
        description="case_space: keys compare ignoring case, accents and extra spaces.",
    )
    mode: Literal["nest", "merge"] = Field(
        default="nest",
        description=(
            "nest: the match goes under the field named by `as`. merge: the match's top-level "
            "fields are copied onto the item (both must be objects)."
        ),
    )
    as_: str = Field(
        default="match",
        alias="as",
        description="Field the match is nested under (mode nest). Null when there is no match.",
    )
    many: Literal["first", "last", "all"] = Field(
        default="first",
        description=(
            "When several `other` entries share a key: first / last uses one; all nests a list "
            "(mode nest only)."
        ),
    )
    prefer: Literal["items", "other"] = Field(
        default="items",
        description="mode merge: whose value wins when both have the same field.",
    )
    keep_unmatched: bool = Field(
        default=True,
        description="Keep `items` entries with no match (nested match null, or unchanged when merging).",
    )
    unmatched_fill: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "mode merge: fields given to a kept item that found NO match, so every item carries the "
            "same fields (e.g. {status: 'not_read', good: false}). The item's own fields win."
        ),
    )

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class JoinOutput(KindModel, kind="joined_list_result"):
    """Kind ``joined_list_result``, registered in ``aidream/kinds/data_ops.py`` (ships with this code)."""

    items: list[JsonValue] = Field(description="The `items` entries, each with its match.")
    matched: int = Field(description="How many `items` entries found a match.")
    unmatched: int = Field(description="How many `items` entries found none (kept or dropped per keep_unmatched).")
    unmatched_indexes: list[int] = Field(
        default_factory=list, description="Positions in `items` of the entries that found no match."
    )
    other_unmatched: list[JsonValue] = Field(
        default_factory=list,
        description="`other` entries no item matched (e.g. answers about ids never sent), in their order.",
    )


class DataJoinExecutor:
    """Match items of one list to another by key; nest or merge the match."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.join",
        category=NodeCategory.DATA,
        display_name="Join Two Lists",
        description=(
            "Match each item of a list to the item(s) of another list with the same key, and "
            "nest or merge the match. Keeps or drops items with no match; reports the other "
            "list's entries nobody matched."
        ),
        input_schema=JoinInput,
        input_kind="join_request",
        output_schema=JoinOutput,
        config_schema=JoinConfig,
        output_kind="joined_list_result",
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
        inputs: JoinInput,
        config: JoinConfig,
    ) -> NodeResult[JoinOutput]:
        _ = ctx
        if config.mode == "merge" and config.many == "all":
            raise ExecutionError("data.join: many=all nests a list; use mode nest, or many first / last to merge.")
        other_path = config.other_key if config.other_key else config.key

        def identity(item: JsonValue, path: str) -> str | None:
            value, found = _key_of(item, path)
            if not found or value is None:
                return None
            if config.normalize == "case_space" and isinstance(value, str):
                value = _fold_text(value)
            return _identity(value)

        index: dict[str, list[int]] = {}
        for position, entry in enumerate(inputs.other):
            key = identity(entry, other_path)
            if key is not None:
                index.setdefault(key, []).append(position)

        used: set[int] = set()
        items: list[JsonValue] = []
        unmatched_indexes: list[int] = []
        matched = 0
        for position, item in enumerate(inputs.items):
            key = identity(item, config.key)
            hits = index.get(key, []) if key is not None else []
            if not hits:
                unmatched_indexes.append(position)
                if not config.keep_unmatched:
                    continue
                if config.mode == "nest":
                    items.append(_nest(item, config.as_, [] if config.many == "all" else None, position))
                elif config.unmatched_fill and isinstance(item, dict):
                    items.append({**config.unmatched_fill, **item})
                else:
                    items.append(item)
                continue
            matched += 1
            used.update(hits)
            if config.many == "all":
                items.append(_nest(item, config.as_, [inputs.other[h] for h in hits], position))
                continue
            match = inputs.other[hits[0] if config.many == "first" else hits[-1]]
            if config.mode == "nest":
                items.append(_nest(item, config.as_, match, position))
            else:
                items.append(_merge(item, match, config.prefer, position))
        return success(
            JoinOutput(
                items=items,
                matched=matched,
                unmatched=len(unmatched_indexes),
                unmatched_indexes=unmatched_indexes,
                other_unmatched=[e for p, e in enumerate(inputs.other) if p not in used],
            )
        )


def _nest(item: JsonValue, field: str, match: Any, position: int) -> JsonValue:
    if not isinstance(item, dict):
        raise ExecutionError(
            f"data.join: item {position} is a {type(item).__name__}, so the match cannot be nested "
            f"under '{field}'. Join a list of objects."
        )
    return {**item, field: match}


def _merge(item: JsonValue, match: JsonValue, prefer: str, position: int) -> JsonValue:
    if not isinstance(item, dict) or not isinstance(match, dict):
        raise ExecutionError(
            f"data.join: mode merge needs objects on both sides, but item {position} or its match "
            "is not one. Use mode nest."
        )
    return {**item, **match} if prefer == "other" else {**match, **item}
