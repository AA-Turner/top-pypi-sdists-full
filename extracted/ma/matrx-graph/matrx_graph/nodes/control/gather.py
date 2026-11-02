"""control.gather — fan-in shaper: reassemble fanned items into one payload.

Two modes:

* **Engine-fed aggregated dispatch (ENGINE_SPEC §4.4, preferred).** When the
  node is edge-wired from a fanned chain (``control.map`` → worker → gather),
  the engine delivers ONE logical upstream payload
  ``{"items": [{item_index, status, value, error, reused}, ...]}`` — index-ordered,
  gaps impossible, holes explicit. Gather shapes it: ``values`` in index
  order, ``skipped_indexes`` + ``holes`` reporting every non-succeeded item
  explicitly (never silent absence, never duplication), ``reused_indexes``
  naming the items whose step reused a saved result (run once per key). For AI items it also
  projects ``structured_outputs`` and ``final_texts`` — index-aligned
  collections a merge step can be pointed at, so an edge never has to carry
  whole agent results (messages, usage, metadata) into the next prompt.
  With ``items_from`` (the name of an input carrying the list the For Each
  fanned out — wire that same list into the gather), every hole and every
  entry of ``pairs`` carries its dispatched ``item`` beside it, so naming a
  failed item or joining a value back to what was sent needs no index step.
* **Channel drain (legacy).** Upstream nodes write partial results to a
  shared channel (``append`` / ``topic_map`` reducer); gather drains it.
  Retained for existing definitions — used only when no engine-fed ``items``
  input is present and ``config.channel`` is set.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.errors import ExecutionError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class GatherInput(BaseModel):
    model_config = ConfigDict(extra="allow")


# ``KindSubModel``, not a bare ``BaseModel``: a nested sub-structure must ACCEPT
# the ``__kind`` marker (declared, optional, excluded from every dump). While
# this was ``BaseModel`` + ``extra="forbid"`` the emitted ``$defs.GatherHole``
# had no ``__kind`` property while the LIVE registry row's did — the schema-law
# campaign patched it there — so the publisher's backward-compatibility gate
# read the model as REMOVING a field and refused EVERY republish of
# ``gather_result`` as breaking. That is why the three AI-projection fields
# added 2026-09-12 could not reach the registry down the honest path, and why
# the Newsroom Desk run died at ``n_gather``. (Docstrings on a KindModel or a
# KindSubModel become the registry row's `description` — keep the incident story
# in comments like this one, never in the docstring.)
class GatherHole(KindSubModel):
    """One non-succeeded fan-out item, reported explicitly (§4.4)."""

    item_index: int = Field(description="The item's position within its dispatch.")
    status: str = Field(description="Why the item is a hole: 'skipped' or 'pruned'.")
    item: JsonValue = Field(
        default=None,
        description="The dispatched item this hole stands for (only with `items_from`).",
    )
    error: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Structured error carried with the hole when available. A "
            "user-skip clears the failed attempt's error, so this is "
            "usually None."
        ),
    )


class GatherPair(KindSubModel):
    """One succeeded fan-out item beside what was dispatched for it."""

    item_index: int = Field(description="The item's position within its dispatch.")
    item: JsonValue = Field(default=None, description="The dispatched item.")
    value: JsonValue = Field(default=None, description="That item's result.")


class GatherOutput(KindModel, kind="gather_result"):
    values: list[JsonValue] = Field(
        default_factory=list,
        description="THE RAW per-item results, in item-index order (engine "
        "mode) or channel order (legacy mode) — every field the step emitted, "
        "an AI step's whole `messages` history included. Map an edge at this "
        "key only when the next step genuinely needs the raw objects; for AI "
        "items prefer `structured_outputs` / `final_texts` below.",
    )
    structured_outputs: list[JsonValue] = Field(
        default_factory=list,
        description="For AI items: each gathered result's `structured_output`, "
        "index-aligned with `values` (null where an item has none). This is "
        "what a merge step almost always wants — passing `values` instead "
        "carries every message, usage and metadata blob into the next prompt.",
    )
    final_texts: list[str] = Field(
        default_factory=list,
        description="For AI items: each gathered result's `final_text`, "
        "index-aligned with `values` (empty string where an item has none).",
    )
    ai_item_count: int = Field(
        default=0,
        description="How many gathered values looked like an AI step result "
        "(carried `final_text` or `structured_output`). 0 means the two "
        "collections above are all-empty by construction, not by loss.",
    )
    item_indexes: list[int] = Field(
        default_factory=list,
        description="For each entry of `values`, the position of the dispatched item it "
        "came from — so a hole never shifts what a value pairs with in the list that "
        "was fanned out.",
    )
    count: int = Field(default=0, description="How many values were gathered.")
    skipped_indexes: list[int] = Field(
        default_factory=list,
        description="Item indexes the user skipped (engine mode only).",
    )
    reused_indexes: list[int] = Field(
        default_factory=list,
        description="Item indexes whose step reused a saved result instead of running "
        "(run once per key) — each also appears in `item_indexes`. Engine mode only.",
    )
    holes: list[GatherHole] = Field(
        default_factory=list,
        description="Explicit per-item hole report for every non-succeeded "
        "item — never silent absence (ENGINE_SPEC §4.4).",
    )
    expected: int | None = Field(
        default=None,
        description="Total items the dispatch fanned out (engine mode only).",
    )
    pairs: list[GatherPair] = Field(
        default_factory=list,
        description="With `items_from`: each succeeded item's dispatched `item` beside its "
        "`value`, in item-index order. Empty otherwise.",
    )


class GatherConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel: str | None = Field(
        default=None,
        description=(
            "Legacy channel-drain mode: name of the channel to drain. Leave "
            "unset when the gather is edge-wired from a fanned chain — the "
            "engine feeds the aggregated items directly (ENGINE_SPEC §4.4)."
        ),
        json_schema_extra=field_extras(widget="channel_picker"),
    )
    only_successful: bool = Field(
        default=True,
        description=(
            "Channel mode only: skip entries shaped like `{error: ...}` — "
            "useful for gather-after-map patterns where some children fail "
            "gracefully. Engine mode reports holes explicitly instead."
        ),
        json_schema_extra=field_extras(widget="toggle"),
    )
    items_from: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Engine mode: the input holding the list the For Each fanned out (connect "
            "that same list into this step under this name). Each hole and each entry of "
            "`pairs` then carries its dispatched `item`."
        ),
        json_schema_extra=field_extras(widget="text"),
    )


def _is_engine_items(raw: Any) -> bool:
    # An EMPTY list is engine-fed too: the scheduler delivers ``items: []``
    # when the For Each this gather closes fanned out zero items (§4.4a), and
    # the gather reports zero values instead of refusing.
    return isinstance(raw, list) and all(
        isinstance(e, dict) and "item_index" in e and "status" in e for e in raw
    )


def _unwrap_value(value: Any) -> Any:
    # A non-dict item payload travels as {"value": X} through edge mapping
    # (`_map_edge_payload`); unwrap that single-key envelope so gather emits
    # the item itself, symmetric with how it was wrapped.
    if isinstance(value, dict) and set(value) == {"value"}:
        return value["value"]
    return value


def _ai_projection(values: list[Any]) -> tuple[list[Any], list[str], int]:
    """(structured_outputs, final_texts, ai_item_count) for gathered values.

    Index-aligned with ``values`` — a non-AI item contributes ``None`` / ``""``
    so position N always means item N. Values are copied VERBATIM (``__kind``
    markers and all — never stripped, KINDS_EVERYWHERE §4.2a).
    """
    structured: list[Any] = []
    texts: list[str] = []
    ai_count = 0
    for value in values:
        if not isinstance(value, dict):
            structured.append(None)
            texts.append("")
            continue
        has_text = "final_text" in value
        has_structured = "structured_output" in value
        if has_text or has_structured:
            ai_count += 1
        structured.append(value.get("structured_output") if has_structured else None)
        raw_text = value.get("final_text")
        texts.append(raw_text if isinstance(raw_text, str) else "")
    return structured, texts, ai_count


def _dispatched_list(dump: dict[str, Any], name: str | None) -> list[Any] | None:
    if name is None:
        return None
    raw = dump.get(name)
    if isinstance(raw, dict) and set(raw) == {"value"}:
        raw = raw["value"]
    if not isinstance(raw, list):
        raise ExecutionError(
            f"control.gather: items_from names the input {name!r}, but "
            + ("nothing arrived under it" if raw is None else f"it holds a {type(raw).__name__}")
            + ". Connect the list the For Each fanned out into this step under that name."
        )
    return raw


def _dispatched_item(dispatched: list[Any] | None, idx: int, name: str | None, expected: int) -> Any:
    if dispatched is None:
        return None
    if len(dispatched) != expected:
        raise ExecutionError(
            f"control.gather: items_from {name!r} holds {len(dispatched)} items but the For Each "
            f"fanned out {expected}. Connect the same list the For Each was given."
        )
    return dispatched[idx]


class GatherExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="control.gather",
        category=NodeCategory.CONTROL,
        display_name="Gather",
        description="Collect the results of parallel steps back into one list.",
        input_schema=GatherInput,
        output_schema=GatherOutput,
        config_schema=GatherConfig,
        output_kind="gather_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="layers",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: GatherInput,
        config: GatherConfig,
    ) -> NodeResult[GatherOutput]:
        dump = inputs.model_dump(mode="json")
        engine_items = dump.get("items")
        # 🚨 An EXPLICIT config.channel WINS over engine-aggregated inbound
        # items. A gather triggered from a multi-fire source (a work-queue's
        # 'done' handle — the queue self-Sends per wave, so its emission
        # arrives in the §4.4 aggregated-dispatch shape) would otherwise
        # match _is_engine_items and silently gather the TRIGGER payload
        # instead of the channel it was configured to drain. Found live
        # 2026-08-19: W7's gather returned the queue's done tally while two
        # rendered images sat unread in the channel.
        if _is_engine_items(engine_items) and not config.channel:
            ordered = sorted(engine_items, key=lambda e: int(e.get("item_index", 0)))
            values: list[JsonValue] = []
            item_indexes: list[int] = []
            skipped_indexes: list[int] = []
            reused_indexes: list[int] = []
            holes: list[GatherHole] = []
            pairs: list[GatherPair] = []
            dispatched = _dispatched_list(dump, config.items_from)
            for entry in ordered:
                idx = int(entry["item_index"])
                status = str(entry["status"])
                sent = _dispatched_item(dispatched, idx, config.items_from, len(ordered))
                if status == "succeeded":
                    values.append(_unwrap_value(entry.get("value")))
                    item_indexes.append(idx)
                    if dispatched is not None:
                        pairs.append(GatherPair(item_index=idx, item=sent, value=values[-1]))
                    if entry.get("reused") is True:
                        reused_indexes.append(idx)
                    continue
                holes.append(
                    GatherHole(item_index=idx, status=status, error=entry.get("error"), item=sent)
                )
                if status == "skipped":
                    skipped_indexes.append(idx)
            structured, texts, ai_count = _ai_projection(values)
            return success(
                GatherOutput(
                    values=values,
                    structured_outputs=structured,
                    final_texts=texts,
                    ai_item_count=ai_count,
                    item_indexes=item_indexes,
                    count=len(values),
                    skipped_indexes=skipped_indexes,
                    reused_indexes=reused_indexes,
                    holes=holes,
                    expected=len(ordered),
                    pairs=pairs,
                )
            )

        if not config.channel:
            raise ExecutionError(
                "control.gather: no engine-aggregated 'items' input arrived "
                "and no config.channel is set — nothing to gather. Edge-wire "
                "this node from the fanned chain (ENGINE_SPEC §4.4) or "
                "configure the channel to drain."
            )

        raw = ctx.channels.get(config.channel, [])
        items: list[Any]
        if isinstance(raw, list):
            items = list(raw)
        elif isinstance(raw, dict):
            # topic_map reducer stores {topic: [entries]}; flatten to entries
            items = [e for entries in raw.values() if isinstance(entries, list) for e in entries]
        else:
            items = [raw]

        # item_indexes on this path too: each kept value's position in the
        # drained channel (the order its entries were written), so a pairing
        # step downstream never meets a silently empty index list.
        positions = list(range(len(items)))
        if config.only_successful:
            kept = [
                (i, v) for i, v in zip(positions, items, strict=True)
                if not (isinstance(v, dict) and v.get("error") is not None)
            ]
            positions = [i for i, _ in kept]
            items = [v for _, v in kept]
        structured, texts, ai_count = _ai_projection(items)
        return success(
            GatherOutput(
                values=items,
                structured_outputs=structured,
                final_texts=texts,
                ai_item_count=ai_count,
                item_indexes=positions,
                count=len(items),
            )
        )
