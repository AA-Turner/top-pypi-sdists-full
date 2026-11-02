"""``data.filter`` — keep list items that satisfy a sandboxed predicate.

The predicate is evaluated in the same restricted-Python sandbox as
``data.transform``. Each item is bound to the name ``inputs`` (same name as
elsewhere, for consistency with the rest of the sandbox). Return truthy
to keep. The step's other inputs (everything besides ``items``) are under
``inputs['$in']`` — compare an item against another step's list. No function calls, no attribute access, only the safe subset.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import bind_item, safe_eval
from matrx_graph.nodes._template import render_template_string
from matrx_graph.content_ir.accessor import resolve_path as _resolve_accessor
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class FilterInput(BaseModel):
    # extra="allow": every OTHER value delivered on this step's edges (a list of
    # links already looked up, articles already seen) is readable by the
    # predicate as ``inputs['$in'][<name>]`` — the same ``$in`` namespace
    # control.map's payload_template uses.
    model_config = ConfigDict(extra="allow")
    items: list[JsonValue] = Field(description="The list to filter.")


# ---------------------------------------------------------------------------
# Left out, with a reason — ONE shape for every step that narrows a list
# (data.filter, data.limit, data.rules, data.batch, text.remove_repeated_lines).
# Opt-in: off by default and ABSENT (`left_out` is None, not []) unless asked for, as on
# data.rules and text.remove_repeated_lines, so no existing definition's output changes. Each entry
# is a REFERENCE (input position + id/label), never the whole item: the item is
# still in the list the step received. Three unrelated users: pages skipped and
# why (Choose pages to read), stories withheld and why (Pick stories),
# recipients not notified and why (Notify people once).
# ---------------------------------------------------------------------------


class LeftOutEntry(KindSubModel):
    """One item a step left out: where it was, what it is called, why, and which step."""

    item: int = Field(description="Input position of the item.")
    label: str = Field(default="", description="Its id or label (from `left_out_label_path`), else 'Item N'.")
    reason: str = Field(default="", description="Why it was left out, in plain words.")
    step: str = Field(default="", description="The id of the step that left it out.")


class LeftOutOptions(BaseModel):
    """The three settings every narrowing step shares (mixed into its config)."""

    left_out: bool = Field(
        default=False,
        description="Also return `left_out`: every item this step dropped, by position and label, with a reason.",
        json_schema_extra=field_extras(widget="toggle"),
    )
    left_out_reason: str = Field(
        default="",
        description=(
            "The reason written on each left-out item. ``{item.path}`` reads the item, ``{name}`` "
            "another input of this step, else a field of the item. Empty: the step's own reason."
        ),
    )
    left_out_label_path: str = Field(
        default="",
        description="Path to each item's id or label (e.g. 'url'); empty labels items 'Item N'.",
    )


def left_out_label(item: JsonValue, index: int, label_path: str) -> str:
    if label_path:
        values = _resolve_accessor(item, label_path, unwrap_root=False).values
        if values and values[0] not in (None, ""):
            value = values[0]
            return value if isinstance(value, str) else str(value)
    return f"Item {index}"


def left_out_entry(
    item: JsonValue,
    index: int,
    options: LeftOutOptions,
    *,
    default_reason: str,
    others: dict[str, JsonValue],
    step: str,
) -> LeftOutEntry:
    """The left-out entry for one dropped item; ``left_out_reason`` overrides the step's own."""
    reason = default_reason
    if options.left_out_reason:
        # `{name}`: another input of the step, else a field of the item itself.
        fields = item if isinstance(item, dict) else {}
        reason, _ = render_template_string(
            options.left_out_reason, {**fields, **others, "item": item, "index": index}, whole_key="inputs"
        )
    return LeftOutEntry(
        item=index, label=left_out_label(item, index, options.left_out_label_path), reason=reason, step=step
    )


def step_id(ctx: object) -> str:
    return str(getattr(ctx, "node_id", "") or "")


#: The key under which the predicate reads this step's other inputs.
OTHER_INPUTS_KEY = "$in"


class FilterConfig(LeftOutOptions):
    model_config = ConfigDict(extra="forbid")

    predicate: str = Field(
        min_length=1,
        description=(
            "Predicate expression. Each list element is bound to `inputs`. "
            "Example: ``inputs['score'] > 0.5``. Items where the expression "
            "is truthy are kept. A list of plain values (strings, numbers) "
            "binds each element as ``{'value': <element>}``, so compare it as "
            "``inputs['value']`` — e.g. ``inputs['value'] not in ['a', 'b']``. "
            "Bare `inputs` over such a list is REFUSED at run time: it would "
            "test the wrapper instead of the element and answer the same for "
            "every item. "
            "Everything else delivered to this step (besides `items`) is "
            "readable as ``inputs['$in'][<name>]`` — e.g. "
            "``inputs['url'] not in inputs['$in']['seen']`` keeps only the "
            "items whose url is not in the list delivered as `seen`."
        ),
        json_schema_extra=field_extras(
            widget="code",
            code_language="python",
            placeholder="inputs['score'] > 0.5",
        ),
    )
    id_key: str | None = Field(
        default=None,
        description=(
            "For a flat tree (each item names its parent): the field holding an item's own id. "
            "Set with `parent_key`; a kept item whose parent was dropped moves to its nearest "
            "kept ancestor, or to the top level when none is left."
        ),
    )
    parent_key: str | None = Field(
        default=None,
        description="For a flat tree: the field naming an item's parent's id. Set with `id_key`.",
    )

    @model_validator(mode="after")
    def _tree_keys_together(self) -> FilterConfig:
        if (self.id_key is None) != (self.parent_key is None):
            raise ValueError("id_key and parent_key are set together (a flat tree needs both) or not at all.")
        return self


class DedupeMatch(KindSubModel):
    """Which kept (or already-saved) item a dropped item matched — ``data.dedupe`` only."""

    index: int = Field(description="Input position of the dropped item.")
    survivor_index: int | None = Field(
        default=None, description="Input position of the kept item it matched; null when it matched an `against` entry."
    )
    against_index: int | None = Field(
        default=None, description="Position in `against` of the existing entry it matched; null otherwise."
    )
    survivor_id: JsonValue = Field(
        default=None, description="The matched item's id (the `id_path` value), null when it has none."
    )


class FilterOutput(KindModel, kind="filter_result"):
    """THE ``filter_result`` kind — one model for every node that answers with
    a kept subset (``data.filter``, ``data.dedupe``, ``data.limit``).

    The descriptions are deliberately written for all three: this is ONE
    registered contract, so a per-node wording would either lie about the
    other producers or push each of them into minting a near-duplicate kind.
    """

    items: list[JsonValue] = Field(description="The elements that were kept.")
    kept: int = Field(description="How many elements were kept.")
    dropped: int = Field(description="How many elements were dropped.")
    matches: list[DedupeMatch] = Field(
        default_factory=list,
        description="data.dedupe only: for each dropped item, the kept item or `against` entry it matched.",
    )
    left_out: list[LeftOutEntry] | None = Field(
        default=None,
        description="Only with `left_out` on (absent otherwise): each dropped item by input position and label, with the reason and step.",
    )


class FilterExecutor:
    """Sandbox-eval predicate per item; keep truthy."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.filter",
        category=NodeCategory.DATA,
        display_name="Filter",
        description="Keep only the list items that pass a test.",
        input_schema=FilterInput,
        input_kind="items",
        output_schema=FilterOutput,
        config_schema=FilterConfig,
        output_kind="filter_result",
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
        inputs: FilterInput,
        config: FilterConfig,
    ) -> NodeResult[FilterOutput]:
        kept: list[JsonValue] = []
        left_out: list[LeftOutEntry] = []
        others = {
            k: v for k, v in inputs.model_dump(mode="json").items() if k != "items"
        }
        for index, item in enumerate(inputs.items):
            # The sandbox exposes only the name `inputs`; bind the current
            # element there so the predicate UX matches data.transform.
            # `bind_item` refuses a bare-`inputs` predicate over a wrapped
            # scalar — the inert-predicate class (W58), which silently kept
            # all 14 ids of a citation gate whose own list contained them.
            bound = bind_item(
                config.predicate,
                item,
                where=f"data.filter: item {index} of {len(inputs.items)}",
            )
            if others:
                # Added only when other inputs exist, so a predicate over a
                # step with just `items` sees exactly the item, as always.
                if OTHER_INPUTS_KEY in bound:
                    raise ExecutionError(
                        f"data.filter: item {index} has its own {OTHER_INPUTS_KEY!r} "
                        "key, which would hide this step's other inputs. Rename "
                        "that field upstream."
                    )
                bound = {**bound, OTHER_INPUTS_KEY: others}
            try:
                passed = safe_eval(config.predicate, bound)
            except KeyError as e:
                # A bare `KeyError: 'rule_id'` names neither the node, the
                # predicate, nor what the item actually was — four days of the
                # Masterwork generate shape were lost to exactly that message
                # (2026-08-21). The mismatch is still fatal; it is now legible.
                raise ExecutionError(
                    f"data.filter: the predicate {config.predicate!r} asked for "
                    f"{e.args[0]!r}, which item {index} of {len(inputs.items)} "
                    f"does not have. That item's keys are {sorted(bound)}. "
                    "Either the predicate names the wrong field, or the list is "
                    "one level off — a fan-in delivers wrappers "
                    "({'error', 'value'}), so put a data.flatten in front."
                ) from e
            if passed:
                kept.append(item)
            elif config.left_out:
                left_out.append(
                    left_out_entry(
                        item, index, config, default_reason="did not pass the filter", others=others, step=step_id(ctx)
                    )
                )
        if config.id_key and config.parent_key:
            kept = _lift_orphans(inputs.items, kept, config.id_key, config.parent_key)
        return success(
            FilterOutput(
                items=kept,
                kept=len(kept),
                dropped=len(inputs.items) - len(kept),
                left_out=left_out if config.left_out else None,
            )
        )


def _lift_orphans(
    every: list[JsonValue], kept: list[JsonValue], id_key: str, parent_key: str
) -> list[JsonValue]:
    """Re-point each kept node whose parent was dropped at its nearest kept ancestor.

    A parent outside the list is left alone (it may live elsewhere); a node with no kept
    ancestor loses its ``parent_key`` (top level). Cycles stop at the first repeat.
    """
    parent_of = {
        n[id_key]: n.get(parent_key) for n in every if isinstance(n, dict) and n.get(id_key) is not None
    }
    kept_ids = {n[id_key] for n in kept if isinstance(n, dict) and n.get(id_key) is not None}
    dropped = set(parent_of) - kept_ids
    out: list[JsonValue] = []
    for node in kept:
        if not isinstance(node, dict) or node.get(parent_key) not in dropped:
            out.append(node)
            continue
        parent = node.get(parent_key)
        seen: set[JsonValue] = set()
        while parent in dropped and parent not in seen:
            seen.add(parent)
            parent = parent_of.get(parent)
        moved = dict(node)
        if parent is None or parent in seen:
            moved.pop(parent_key, None)
        else:
            moved[parent_key] = parent
        out.append(moved)
    return out
