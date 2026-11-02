"""``data.choose`` — Choose Items: mark, leave out, drop repeats, order and cap a list in ONE step.

"Keep by rules, rank, cap per group and overall, and say why each one missed" is one decision a person
reads as one sentence; before this step it took 4-10 steps (rules → kept filter → left-out filter → dedupe
→ sort → limit → why rows). Design: common-docs/systems/workflows/projects/generic-only/FEWER-STRONGER-STEPS.md
(N2). The stages always run in this order, each one optional:

1. **Rules** — the ``data.rules`` table and evaluator, one decision per item (``inputs['item']``,
   ``inputs['index']``, the whole list as ``inputs['items']``, plus this step's other inputs by name). The deciding row's ``fields`` (and, under
   ``decision_keys``, its label / reason / score) are written onto the item; an item whose label is in
   ``left_out_labels`` is left out with that row's reason.
2. **Repeats** — first of each ``unique_by`` key wins (the ``data.dedupe`` comparison, same ``normalize``).
3. **Order** — ``order_by`` keys, most important first (``data.sort``'s keys: a path, an expression, or a
   position in another input's list).
4. **Per group** — at most ``per_group.max`` of each ``per_group.by`` value; the rest are left out or moved last.
5. **At most** — ``limit`` items, from the top or by turns across groups (``data.limit``'s ``round_robin``).

Every item left out is listed once, in input order, with the stage's reason; ``counts`` says how many each
stage left out. No budget here: ``data.limit`` and ``data.batch`` fit a size budget.
Users: pages to read (kinds first, family cap, max pages); stories to report (score floors, per-source cap,
limit); offerings to ask about (not filed, not dismissed, round robin by product line).
"""

from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_graph.content_ir.model import KindModel
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import render_template_string
from matrx_graph.nodes.data.collections import (
    RoundRobin,
    SortKey,
    _identity,
    _key_of,
    _round_robin_positions,
    dedupe_identity,
    multi_key_order,
)
from matrx_graph.nodes.data.filter import LeftOutEntry, left_out_label, step_id
from matrx_graph.nodes.data.rules import Rule, RulesConfig, RuleThen, _decide, _write_fields
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

#: The stages, in the order they run; also the keys of ``counts``.
STAGES = ("rules", "repeats", "per_group", "limit")


class ChooseInput(BaseModel):
    # extra="allow": the other inputs are readable by rules (inputs['<name>']), by order_by
    # (position_in / inputs['$in'][<name>]) and by reasons ({name}).
    model_config = ConfigDict(extra="allow")
    items: list[JsonValue] = Field(description="The list to choose from.")


class UniqueBy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, description="Path to the value that makes two items the same (e.g. 'url').")
    normalize: Literal["none", "case_space", "text"] = Field(
        default="none",
        description="none: exactly. case_space: ignoring upper/lower case and spacing. text: also punctuation.",
    )
    reason: str = Field(default="", description="Reason on a repeat left out; empty: 'a repeat of item N'.")


class PerGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")

    by: str = Field(min_length=1, description="Path to the value that defines a group (e.g. 'family').")
    max: int = Field(ge=1, le=100_000, description="At most this many items of one group, in the current order.")
    overflow: Literal["left_out", "last"] = Field(
        default="left_out",
        description="left_out: the rest of a group is left out. last: they move after everyone else, in order.",
    )
    reason: str = Field(default="", description="Reason on an item left out; empty: 'more than N of its group'.")


class ChooseConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rules: list[Rule] = Field(
        default_factory=list,
        description=(
            "Stage 1 (optional): the Rules table, decided per item (inputs['item'], inputs['index'], other inputs "
            "by name). The deciding row's fields are written onto the item."
        ),
    )
    mode: Literal["first_match", "all_match"] = Field(default="first_match", description="As on Rules.")
    default: RuleThen | None = Field(default=None, description="The answer when no row matches (as on Rules).")
    left_out_labels: list[str] = Field(
        default_factory=list,
        description="Items whose deciding label is one of these are left out, with that row's reason.",
    )
    decision_keys: dict[Literal["label", "reason", "score"], str] = Field(
        default_factory=dict,
        description="Also write the deciding row's label / reason / score onto each item under these names.",
    )
    unique_by: UniqueBy | None = Field(default=None, description="Stage 2 (optional): first of each key wins.")
    order_by: list[SortKey] = Field(
        default_factory=list, description="Stage 3 (optional): sort keys, most important first (as on Sort)."
    )
    missing: Literal["last", "first"] = Field(
        default="last", description="Where an item with no value for a sort key goes."
    )
    per_group: PerGroup | None = Field(default=None, description="Stage 4 (optional): at most N of each group.")
    limit: int | None = Field(default=None, ge=0, le=100_000, description="Stage 5 (optional): at most this many.")
    round_robin: RoundRobin | None = Field(
        default=None,
        description="With `limit`: pick by turns across groups instead of from the top (as on Limit).",
    )
    limit_reason: str = Field(default="", description="Reason on an item past `limit`; empty: 'past the limit of N'.")
    label_path: str = Field(default="", description="Path to each item's id or label for `left_out` (e.g. 'url').")
    rank_as: str = Field(
        default="", description="Write each chosen item's position (1 = first) under this name (over a field of that name)."
    )

    @model_validator(mode="after")
    def _consistent(self) -> ChooseConfig:
        if (self.left_out_labels or self.decision_keys or self.default) and not self.rules:
            raise ValueError("data.choose: left_out_labels, decision_keys and default belong to `rules`; add rules.")
        if self.round_robin is not None and self.limit is None:
            raise ValueError("data.choose: round_robin picks `limit` items by turns; set `limit` too.")
        if self.missing != "last" and not self.order_by:
            raise ValueError("data.choose: `missing` places items in the order stage; set `order_by` too.")
        if self.limit_reason and self.limit is None:
            raise ValueError("data.choose: `limit_reason` is written on items past `limit`; set `limit` too.")
        if self.mode != "first_match" and not self.rules:
            raise ValueError("data.choose: `mode` is how `rules` decide; add rules.")
        produced = {r.then.label for r in self.rules} | ({self.default.label} if self.default else set())
        unknown = sorted(set(self.left_out_labels) - produced)
        if unknown:
            raise ValueError(f"data.choose: left_out_labels {unknown} — no rule or default gives that label.")
        names = list(self.decision_keys.values()) + ([self.rank_as] if self.rank_as else [])
        if len(set(names)) != len(names):
            raise ValueError("data.choose: decision_keys and rank_as each write a field; give each its own name.")
        if self.rules:
            # The same authoring checks as a Rules step (every predicate through the sandbox check).
            self.rules_config()
        return self

    def rules_config(self) -> RulesConfig:
        return RulesConfig(rules=self.rules, mode=self.mode, default=self.default, items_path="items")


class ChooseOutput(KindModel, kind="chosen_list_result"):
    items: list[JsonValue] = Field(description="The chosen items, in order (rule fields written on).")
    kept: int = Field(description="How many were chosen.")
    dropped: int = Field(description="How many were left out.")
    left_out: list[LeftOutEntry] = Field(
        description="Every item left out, in input order: its position, label, reason and this step's id."
    )
    counts: dict[str, int] = Field(
        description="How many items each stage left out: rules, repeats, per_group, limit."
    )


def _reason(text: str, default: str, item: JsonValue, index: int, others: dict[str, Any]) -> str:
    if not text:
        return default
    fields = item if isinstance(item, dict) else {}
    return render_template_string(text, {**fields, **others, "item": item, "index": index}, whole_key="inputs")[0]


class ChooseExecutor:
    """Rules → repeats → order → per group → at most N, every left-out item with its reason."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.choose",
        category=NodeCategory.DATA,
        display_name="Choose Items",
        description="Leave out by rules, drop repeats, order, cap per group and overall; say why each was left out.",
        input_schema=ChooseInput,
        input_kind="items",
        output_schema=ChooseOutput,
        config_schema=ChooseConfig,
        output_kind="chosen_list_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="list-filter",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ChooseInput,
        config: ChooseConfig,
    ) -> NodeResult[ChooseOutput]:
        payload = inputs.model_dump(mode="json")
        source: list[JsonValue] = payload.pop("items")
        others = payload
        step = step_id(ctx)
        counts = {stage: 0 for stage in STAGES}
        dropped: dict[int, LeftOutEntry] = {}

        def leave(index: int, _item: JsonValue, stage: str, reason: str) -> None:
            counts[stage] += 1
            dropped[index] = LeftOutEntry(  # labelled from the item as it came in, as every narrowing step does
                item=index, label=left_out_label(source[index], index, config.label_path), reason=reason, step=step
            )

        # rows: (input position, item as it stands now)
        rows: list[tuple[int, JsonValue]] = list(enumerate(source))

        if config.rules:
            clash = sorted(k for k in ("item", "index") if k in others)
            if clash:
                raise ExecutionError(
                    f"data.choose: rules read each item as inputs['item'] and inputs['index'], but this step also "
                    f"receives inputs named {clash}. Rename that input."
                )
            rules = config.rules_config()
            dropping = set(config.left_out_labels)
            kept: list[tuple[int, JsonValue]] = []
            for index, item in rows:
                decision = _decide(
                    rules, {**others, "items": source, "item": item, "index": index}, where=f" on item {index}"
                )
                writes = decision.then is not None and (
                    config.decision_keys or set(decision.then) - {"label", "reason", "score"}
                )
                if writes:  # an item that is not an object is refused there, by name
                    item = _write_fields(item, decision, index, config.decision_keys)
                if dropping and decision.label in dropping:
                    leave(index, item, "rules", decision.reason or decision.label or "")
                else:
                    kept.append((index, item))
            rows = kept

        if config.unique_by is not None:
            first_at: dict[str, int] = {}
            kept = []
            for index, item in rows:
                identity = dedupe_identity(item, config.unique_by.key, config.unique_by.normalize)
                if identity in first_at:
                    leave(index, item, "repeats",
                          _reason(config.unique_by.reason, f"a repeat of item {first_at[identity]}", item, index, others))
                else:
                    first_at[identity] = index
                    kept.append((index, item))
            rows = kept

        if config.order_by:
            try:
                order = multi_key_order([item for _, item in rows], config.order_by, config.missing, others)
            except ExecutionError as e:
                raise ExecutionError(f"data.choose (order stage, item numbers after the earlier stages): {e}") from e
            rows = [rows[i] for i in order]

        if config.per_group is not None:
            group = config.per_group
            seen: dict[str, int] = {}
            kept, moved = [], []
            for index, item in rows:
                value, found = _key_of(item, group.by)
                identity = _identity(value) if found and value is not None else "\x00missing"
                seen[identity] = seen.get(identity, 0) + 1
                if seen[identity] <= group.max:
                    kept.append((index, item))
                elif group.overflow == "last":
                    moved.append((index, item))
                else:
                    leave(index, item, "per_group",
                          _reason(group.reason, f"more than {group.max} of its group", item, index, others))
            rows = kept + moved

        if config.limit is not None:
            if config.round_robin is not None:
                picked = _round_robin_positions([item for _, item in rows], config.limit, config.round_robin)
                chosen = [rows[p] for p, _ in picked]
            else:
                chosen = rows[: config.limit]
            taken = {index for index, _ in chosen}
            for index, item in rows:
                if index not in taken:
                    leave(index, item, "limit",
                          _reason(config.limit_reason, f"past the limit of {config.limit}", item, index, others))
            rows = chosen

        items = [item for _, item in rows]
        if config.rank_as:
            flat = [n for n, item in enumerate(items) if not isinstance(item, dict)]
            if flat:
                raise ExecutionError(
                    f"data.choose: rank_as writes the position onto objects, but chosen item {flat[0]} is not one. "
                    "Leave rank_as empty, or choose from a list of objects."
                )
            items = [{**item, config.rank_as: n} for n, item in enumerate(items, 1)]  # type: ignore[dict-item]
        left_out = [dropped[i] for i in sorted(dropped)]
        return success(
            ChooseOutput(items=items, kept=len(items), dropped=len(left_out), left_out=left_out, counts=counts)
        )
