"""``data.group`` — put a list's items into groups and pick each group's lead.

The general problem (GAP 11 in the generic-only STEP-CENSUS): "these items are
the same thing — keep one lead, keep the rest as evidence". Articles about one
story, claims an agent says repeat each other, search results found by several
engines, keywords on one topic. Each was a custom Python step. This is the one
primitive for the class.

Ways two items join (any that is set may join them — any-match):

* ``key`` — the same value at a path (a hole never equals another hole).
* ``shared_values`` — paths to lists (``url_keys``, ``articles[].url``); two
  items sharing ANY value join.
* ``token_overlap`` — the words of chosen text paths (case- and accent-folded,
  stop words dropped) overlap by at least ``threshold`` AND share at least
  ``min_shared`` words. ``compare: any_member`` joins an item to a group when
  it matches any member; ``first_member`` only when it matches the group's
  first item (stricter, no chains of near-matches).
* ``ids_from`` — a decision list (``inputs.decisions``) naming ids under a lead
  id, as an agent answers "these say the same thing" (the lead joins even when
  absent from its own ids). NOT transitive: an id already in an earlier
  decision's group is dropped from the later one. Every drop is counted by
  reason in ``dropped`` (unknown_id, id_in_two_groups, group_lead_missing,
  group_not_an_object). The named lead leads unless ``lead_by`` picks another
  (``leads_changed`` counts those).

Joins by key, shared values and words chain: A~C and C~B put A, B, C in one
group (``first_member`` word matching excepted). Groups are ordered by their
first item's position — or by ``inputs.order`` (ids; a member's id stands for
its group) with unnamed groups after, in input order.

Keys are unique: an earlier group's key first, then the lead's id, then
``group-N`` for a lead with no id; a key already taken gets a ``~2``, ``~3``…
suffix (``key_collisions``). Ids compare as text — ``1`` and ``"1"`` are one id;
a repeated item id names its first item, and each later copy is counted
(``dropped.duplicate_item_id``) and stays its own group unless another way joins
it. ``None`` and ``""`` are holes everywhere: they never join and sort last.

After grouping: ``min_overlap`` splits off a member whose words (3+ letters,
case-folded) overlap the lead's less than a threshold (``split_from_groups``),
and ``evidence_field`` puts the lead's other members on a copy of the lead.

``existing`` (``inputs.existing``) holds groups from an earlier run: a group
matching one by shared values, by key, or by words takes its key, so a group
keeps its identity when its lead changes between runs. Two groups matching the
same earlier group are one group.

Key paths use the ONE platform accessor grammar (``a.b`` / ``a[].b``), shared
with ``data.dedupe`` / ``data.sort``. It GROUPS; it never routes or drops
(Rule 9: no edge capability is duplicated here).
"""

from __future__ import annotations

import functools
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_graph.content_ir.accessor import resolve_path
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes.data.collections import SIMILAR_STOP_WORDS, _identity, word_overlap, word_set
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

GroupMode = Literal["key", "shared_values", "token_overlap", "ids_from", "existing"]
_MODE_ORDER: tuple[str, ...] = ("key", "shared_values", "token_overlap", "ids_from", "existing")


class GroupInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[JsonValue] = Field(description="The list to group.")
    existing: list[JsonValue] = Field(
        default_factory=list,
        description="Groups from an earlier run; a group matching one takes its key.",
    )
    decisions: list[JsonValue] = Field(
        default_factory=list,
        description="Decisions by id for `ids_from`: each names a lead id and its member ids.",
    )
    order: list[JsonValue] = Field(
        default_factory=list,
        description="Ids in the order groups should come out; groups not named follow in input order.",
    )


class TokenOverlap(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fields: list[str] = Field(
        min_length=1,
        description="Paths to the text compared (e.g. 'title'); several are read as one text.",
    )
    threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Shared words over the shorter text's words (or over all words, for jaccard).",
    )
    min_shared: int = Field(default=2, ge=1, description="At least this many shared words.")
    measure: Literal["containment", "jaccard"] = Field(
        default="containment",
        description="containment: shared / smaller set (one long text does not dilute it). jaccard: shared / union.",
    )
    min_word_length: int = Field(default=2, ge=1, description="Shorter words are ignored.")
    compare: Literal["any_member", "first_member"] = Field(
        default="any_member",
        description="Join a group when matching any member, or only its first item.",
    )
    stop_words: list[str] | None = Field(
        default=None,
        description="Words ignored. Unset = the shared small joining-word list; [] = ignore none.",
    )


class IdsFrom(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lead_path: str = Field(default="lead_id", description="Path to the lead id in each decision.")
    ids_path: str = Field(
        default="member_ids",
        description="Path to the ids in each decision (the lead may or may not be among them).",
    )


class ExistingMatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key_path: str = Field(default="key", description="Path to an earlier group's key.")
    values_path: str | None = Field(
        default=None,
        description="Path to an earlier group's values, matched against the `shared_values` of the group.",
    )
    key_value_path: str | None = Field(
        default=None,
        description="Path to an earlier group's value matched against the `key` of the group's items.",
    )
    text_paths: list[str] = Field(
        default_factory=list,
        description="Paths to an earlier group's text, matched by the `token_overlap` settings.",
    )


class LeadSort(BaseModel):
    """One lead sort. Also written as a string: ``"priority"`` (desc), ``"id asc"``,
    ``"longest(text)"`` / ``"longest:text"`` or ``"shortest(text)"``."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1, description="Path to the value to sort by (e.g. 'priority').")
    order: Literal["asc", "desc"] = Field(default="desc", description="desc: largest (or longest) leads.")
    measure: Literal["value", "length"] = Field(
        default="value", description="value: compare the values. length: compare the text's length."
    )

    @model_validator(mode="before")
    @classmethod
    def _from_text(cls, data: Any) -> Any:
        if not isinstance(data, str):
            return data
        text = data.strip()
        for word, order in (("longest", "desc"), ("shortest", "asc")):
            if text.startswith(word + ":"):
                return {"path": text[len(word) + 1:].strip(), "order": order, "measure": "length"}
            if text.startswith(word + "(") and text.endswith(")"):
                return {"path": text[len(word) + 1:-1].strip(), "order": order, "measure": "length"}
        path, _, order = text.partition(" ")
        return {"path": path, "order": order.strip() or "desc"}


class MinOverlap(BaseModel):
    model_config = ConfigDict(extra="forbid")

    threshold: float = Field(ge=0.0, le=1.0, description="The least word overlap with the lead (0.3 = 30%).")
    fields: list[str] = Field(min_length=1, description="Paths to the text compared (e.g. 'text').")
    measure: Literal["jaccard", "containment"] = Field(
        default="jaccard",
        description="jaccard: shared / all distinct words of the pair. containment: shared / the smaller set.",
    )
    min_word_length: int = Field(default=3, ge=1, description="Shorter words are ignored.")
    stop_words: list[str] = Field(default_factory=list, description="Words ignored (none by default).")


class GroupConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id_path: str = Field(default="id", description="Path to each item's id (used for keys and decisions).")
    key: str | None = Field(default=None, description="Items with the same value here join.")
    shared_values: list[str] = Field(
        default_factory=list,
        description="Paths to lists; items sharing any value join (e.g. 'url_keys').",
    )
    token_overlap: TokenOverlap | None = Field(
        default=None, description="Items whose chosen text shares enough words join."
    )
    ids_from: IdsFrom | None = Field(
        default=None, description="Join items as `inputs.decisions` says (lead id + member ids)."
    )
    existing: ExistingMatch | None = Field(
        default=None, description="How groups match `inputs.existing` to keep an earlier key."
    )
    lead_by: list[LeadSort] = Field(
        default_factory=list,
        description="Ordered sorts that pick each group's lead. Missing values sort last; then a decision's lead, then input order.",
    )
    union: list[str] = Field(
        default_factory=list,
        description="Paths whose values are combined across a group's members (unique, in order).",
    )
    evidence_field: str | None = Field(
        default=None,
        min_length=1,
        description="When set, the lead carries its other members (all fields) under this field (e.g. 'evidence').",
    )
    min_overlap: MinOverlap | None = Field(
        default=None,
        description="A member whose words overlap the lead's less than this is split off as its own group.",
    )
    write_key: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Also return `keyed_items`: every item (an object) in input order with its group key written "
            "at this field, its place in the group at `<field>_rank` (1 = first in input order) and the "
            "group's size at `<field>_size` (e.g. 'family')."
        ),
    )

    @model_validator(mode="after")
    def _has_a_way_to_join(self) -> GroupConfig:
        if not (self.key or self.shared_values or self.token_overlap or self.ids_from):
            raise ValueError(
                "data.group needs at least one way to join items: key, shared_values, "
                "token_overlap or ids_from."
            )
        if self.existing and self.existing.text_paths and self.token_overlap is None:
            raise ValueError("existing.text_paths compares words, so token_overlap must be set.")
        return self


class ItemGroup(KindSubModel):
    key: str = Field(description="The group's identity: an earlier group's key, else the lead's id.")
    lead: JsonValue = Field(description="The item chosen to represent the group.")
    members: list[JsonValue] = Field(description="Every item in the group (the lead included), in input order.")
    member_ids: list[JsonValue] = Field(description="The members' ids, in input order.")
    count: int = Field(description="How many items the group holds.")
    union: dict[str, list[JsonValue]] = Field(
        default_factory=dict, description="Per `union` path: the values combined across members."
    )
    matched_existing: str | None = Field(
        default=None, description="The earlier group's key this group continues; null when new."
    )
    matched_by: list[GroupMode] = Field(
        default_factory=list, description="Which ways joined this group's members (empty for one item)."
    )


class GroupOutput(KindModel, kind="grouped_list_result"):
    groups: list[ItemGroup] = Field(description="The groups, ordered by their first item's position.")
    group_count: int = Field(description="How many groups.")
    item_count: int = Field(description="How many items went in.")
    ungrouped: int = Field(description="Groups of one item.")
    item_keys: list[str] = Field(description="Each input item's group key, in input order.")
    matched_existing_count: int = Field(default=0, description="Groups that kept an earlier key.")
    key_collisions: int = Field(
        default=0, description="Groups whose key was already taken and got a ~2, ~3… suffix."
    )
    unknown_ids: list[str] = Field(
        default_factory=list, description="Ids in the decisions (or `order`) that are not items' ids."
    )
    dropped: dict[str, int] = Field(
        default_factory=dict,
        description=(
            "What `ids_from` dropped, by reason: unknown_id, id_in_two_groups, group_lead_missing, "
            "group_not_an_object, duplicate_item_id. Empty without ids_from."
        ),
    )
    leads_changed: int = Field(
        default=0, description="Groups whose lead `lead_by` chose over the decision's named lead."
    )
    split_from_groups: int = Field(
        default=0, description="Members split off into their own group by `min_overlap`."
    )
    keyed_items: list[JsonValue] | None = Field(
        default=None,
        description="With `write_key`: every item in input order, carrying its group key, rank in group and group size.",
    )


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _values(item: Any, path: str) -> list[Any]:
    """Every value at ``path``, lists flattened one level, empties skipped."""
    out: list[Any] = []
    for value in resolve_path(item, path, unwrap_root=False).values:
        for element in value if isinstance(value, list) else [value]:
            if element is not None and element != "":
                out.append(element)
    return out


def _first(item: Any, path: str) -> tuple[Any, bool]:
    """The first value at ``path``; None and "" are holes (absent), as in ``_values``."""
    values = resolve_path(item, path, unwrap_root=False).values
    if not values or values[0] is None or values[0] == "":
        return None, False
    return values[0], True


def _text_words(item: Any, fields: list[str], stop: frozenset[str], min_length: int) -> frozenset[str]:
    """The shared word set (``collections.word_set``) of the text at ``fields``, read as one text."""
    text = " ".join(str(v) for path in fields for v in _values(item, path) if isinstance(v, (str, int, float)))
    return word_set(text, stop_words=stop, min_length=min_length)


def _similar(a: frozenset[str], b: frozenset[str], spec: TokenOverlap) -> bool:
    score, shared = word_overlap(a, b, spec.measure)
    return shared >= spec.min_shared and score >= spec.threshold


def _overlap(a: frozenset[str], b: frozenset[str], spec: MinOverlap) -> bool:
    """True when ``b`` overlaps ``a`` at least ``spec.threshold`` (two empty texts never split)."""
    if not a and not b:
        return True
    return word_overlap(a, b, spec.measure)[0] >= spec.threshold


def _id_text(value: Any) -> str:
    return value if isinstance(value, str) else _identity(value)


def _unique_keys(built: list[tuple[list[int], int, str | None, set[str]]], ids: list[Any]) -> tuple[list[str], int]:
    """One key per group, never repeated. Claims go in three passes, each in output order:
    earlier-group keys, then lead ids, then ``group-N`` for a lead with no id. A key already
    claimed gets the smallest free ``~2``, ``~3``… suffix, counted as a collision."""
    taken: set[str] = set()
    keys: list[str | None] = [None] * len(built)
    collisions = 0
    wanted: list[tuple[int, int, str]] = []
    for index, (_members, lead, existing_key, _modes) in enumerate(built):
        if existing_key is not None:
            wanted.append((0, index, existing_key))
        elif ids[lead] is not None:
            wanted.append((1, index, _id_text(ids[lead])))
        else:
            wanted.append((2, index, f"group-{index + 1}"))
    for _pass, index, base in sorted(wanted):
        key = base
        if key in taken:
            collisions += 1
            suffix = 2
            while f"{base}~{suffix}" in taken:
                suffix += 1
            key = f"{base}~{suffix}"
        taken.add(key)
        keys[index] = key
    return [k or "" for k in keys], collisions


def _compare_values(a: Any, b: Any) -> int:
    """Natural order for like types (numbers, strings, booleans), else by type then identity."""
    numeric = (int, float)
    if isinstance(a, numeric) and isinstance(b, numeric) and not isinstance(a, bool) and not isinstance(b, bool):
        return (a > b) - (a < b)
    if type(a) is type(b) and isinstance(a, (str, bool)):
        return (a > b) - (a < b)
    ka, kb = (type(a).__name__, _identity(a)), (type(b).__name__, _identity(b))
    return (ka > kb) - (ka < kb)


class _Components:
    """Union-find over item positions; the root is always the smallest position (the first item)."""

    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.modes: dict[int, set[str]] = {}

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def join(self, a: int, b: int, mode: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            keep, gone = min(ra, rb), max(ra, rb)
            self.parent[gone] = keep
            self.modes.setdefault(keep, set()).update(self.modes.pop(gone, set()))
        self.modes.setdefault(self.find(a), set()).add(mode)


# ---------------------------------------------------------------------------
# executor
# ---------------------------------------------------------------------------


class GroupExecutor:
    """Group a list by key, shared values, word overlap or decisions by id; pick a lead per group."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.group",
        category=NodeCategory.DATA,
        display_name="Group Items",
        description="Put items that are the same thing into groups, each with a lead and its members.",
        input_schema=GroupInput,
        output_schema=GroupOutput,
        config_schema=GroupConfig,
        output_kind="grouped_list_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="group",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: GroupInput,
        config: GroupConfig,
    ) -> NodeResult[GroupOutput]:
        _ = ctx
        items = inputs.items
        n = len(items)
        comps = _Components(n)

        ids: list[Any] = [_first(item, config.id_path)[0] for item in items]
        keys: list[str | None] = []
        for item in items:
            value, found = _first(item, config.key) if config.key else (None, False)
            keys.append(_identity(value) if found else None)
        shared: list[set[str]] = [
            {_identity(v) for path in config.shared_values for v in _values(item, path)} for item in items
        ]
        spec = config.token_overlap
        stop = (
            SIMILAR_STOP_WORDS
            if spec is None or spec.stop_words is None
            else frozenset(w.casefold() for w in spec.stop_words)
        )
        toks: list[frozenset[str]] = [
            _text_words(item, spec.fields, stop, spec.min_word_length) if spec else frozenset() for item in items
        ]

        # ids_from: decisions become joins between the items they name. NOT transitive: an id
        # already in an earlier decision's group is dropped from the later one and counted.
        unknown: set[str] = set()
        decision_leads: set[int] = set()
        dropped: dict[str, int] = {}
        if config.ids_from is not None:
            dropped = dict.fromkeys(
                (
                    "unknown_id", "id_in_two_groups", "group_lead_missing", "group_not_an_object",
                    "duplicate_item_id",
                ),
                0,
            )
            # Ids compare as text (1 and "1" are one id). A repeated item id names its FIRST
            # item; later items with that id cannot be named by a decision, stay their own
            # groups (unless another way joins them), and are counted.
            position = {}
            for i, v in enumerate(ids):
                if v is None:
                    continue
                if _id_text(v) in position:
                    dropped["duplicate_item_id"] += 1
                else:
                    position[_id_text(v)] = i
            claimed: set[int] = set()
            for decision in inputs.decisions:
                if not isinstance(decision, dict):
                    dropped["group_not_an_object"] += 1
                    continue
                lead_vals = _values(decision, config.ids_from.lead_path)
                if not lead_vals:
                    dropped["group_lead_missing"] += 1
                    continue
                lead_text = _id_text(lead_vals[0])
                named: list[str] = []
                for raw in [lead_vals[0], *_values(decision, config.ids_from.ids_path)]:
                    text = _id_text(raw)
                    if text not in named:  # the lead may be among its own ids
                        named.append(text)
                known: list[int] = []
                for text in named:
                    if text not in position:
                        unknown.add(text)
                        dropped["unknown_id"] += 1
                    elif position[text] in claimed:
                        dropped["id_in_two_groups"] += 1
                    else:
                        claimed.add(position[text])
                        known.append(position[text])
                        if text == lead_text:
                            decision_leads.add(position[text])
                for other in known[1:]:
                    comps.join(known[0], other, "ids_from")

        # key / shared values: index each value to the first item that carries it.
        first_with_key: dict[str, int] = {}
        first_with_value: dict[str, int] = {}
        word_index: dict[str, list[int]] = {}
        for i in range(n):
            if keys[i] is not None:
                if keys[i] in first_with_key:
                    comps.join(first_with_key[keys[i]], i, "key")
                else:
                    first_with_key[keys[i]] = i
            for value in shared[i]:
                if value in first_with_value:
                    comps.join(first_with_value[value], i, "shared_values")
                else:
                    first_with_value[value] = i
            if spec is not None and toks[i]:
                counts: dict[int, int] = {}
                for word in toks[i]:
                    for j in word_index.get(word, ()):
                        counts[j] = counts.get(j, 0) + 1
                for j in sorted(counts):
                    if counts[j] < spec.min_shared:
                        continue
                    if spec.compare == "first_member" and comps.find(j) != j:
                        continue
                    if comps.find(j) == comps.find(i) and spec.compare == "any_member":
                        continue
                    if _similar(toks[i], toks[j], spec):
                        comps.join(j, i, "token_overlap")
                for word in toks[i]:
                    word_index.setdefault(word, []).append(i)

        # existing: a group matching an earlier one takes its key; groups matching the same one merge.
        matched: dict[int, str] = {}
        if config.existing is not None and inputs.existing:
            matched = self._match_existing(config, inputs.existing, comps, n, keys, shared, toks, stop)

        roots: dict[int, list[int]] = {}
        for i in range(n):
            roots.setdefault(comps.find(i), []).append(i)

        lead_cmp = functools.cmp_to_key(self._lead_comparator(config, items, decision_leads))
        # (members, lead, existing key, modes) per group; split-off members become groups of one.
        built: list[tuple[list[int], int, str | None, set[str]]] = []
        leads_changed = 0
        split = 0
        overlap = config.min_overlap
        for root, members in roots.items():
            lead = min(members, key=lead_cmp)
            if any(m in decision_leads for m in members) and lead not in decision_leads:
                leads_changed += 1
            if overlap is not None and len(members) > 1:
                split_stop = frozenset(w.casefold() for w in overlap.stop_words)
                lead_words = _text_words(items[lead], overlap.fields, split_stop, overlap.min_word_length)
                kept = [
                    m
                    for m in members
                    if m == lead
                    or _overlap(
                        lead_words,
                        _text_words(items[m], overlap.fields, split_stop, overlap.min_word_length),
                        overlap,
                    )
                ]
                for m in members:
                    if m not in kept:
                        split += 1
                        built.append(([m], m, None, set()))
                members = kept
            existing_key = matched.get(root)
            modes = set(comps.modes.get(root, set())) if len(members) > 1 else set()
            if existing_key is not None:
                modes.add("existing")
            built.append((members, lead, existing_key, modes))
        built.sort(key=lambda g: g[0][0])

        if inputs.order:
            group_of = {m: index for index, g in enumerate(built) for m in g[0]}
            position = {_id_text(v): i for i, v in reversed(list(enumerate(ids))) if v is not None}
            rank: dict[int, int] = {}
            for raw in inputs.order:
                text = _id_text(raw)
                if text not in position:
                    unknown.add(text)
                    continue
                rank.setdefault(group_of[position[text]], len(rank))
            ranked = sorted((g for g in range(len(built)) if g in rank), key=rank.__getitem__)
            built = [built[g] for g in ranked] + [b for g, b in enumerate(built) if g not in rank]

        keys_out, collisions = _unique_keys(built, ids)
        groups: list[ItemGroup] = []
        item_keys: list[str] = [""] * n
        for index, (members, lead, existing_key, modes) in enumerate(built):
            key = keys_out[index]
            union: dict[str, list[JsonValue]] = {}
            for path in config.union:
                seen: set[str] = set()
                combined: list[JsonValue] = []
                for m in members:
                    for value in _values(items[m], path):
                        identity = _identity(value)
                        if identity not in seen:
                            seen.add(identity)
                            combined.append(value)
                union[path] = combined
            lead_item = items[lead]
            if config.evidence_field is not None:
                if not isinstance(lead_item, dict):
                    raise ExecutionError(
                        f"data.group: evidence_field puts members on the lead, but a lead is a "
                        f"{type(lead_item).__name__}, not an object. Remove evidence_field or group objects."
                    )
                lead_item = {**lead_item, config.evidence_field: [items[m] for m in members if m != lead]}
            for m in members:
                item_keys[m] = key
            groups.append(
                ItemGroup(
                    key=key,
                    lead=lead_item,
                    members=[items[m] for m in members],
                    member_ids=[ids[m] for m in members],
                    count=len(members),
                    union=union,
                    matched_existing=existing_key,
                    matched_by=[m for m in _MODE_ORDER if m in modes],  # type: ignore[misc]
                )
            )
        keyed_items: list[JsonValue] | None = None
        if config.write_key is not None:
            field = config.write_key
            rank_of: dict[int, tuple[int, int]] = {}
            for members, _lead, _existing, _modes in built:
                for place, m in enumerate(sorted(members), start=1):
                    rank_of[m] = (place, len(members))
            keyed_items = []
            for index, item in enumerate(items):
                if not isinstance(item, dict):
                    raise ExecutionError(
                        f"data.group: write_key writes onto objects, but item {index} is a "
                        f"{type(item).__name__}. Remove write_key or group objects."
                    )
                place, size = rank_of[index]
                keyed_items.append(
                    {**item, field: item_keys[index], f"{field}_rank": place, f"{field}_size": size}
                )
        return success(
            GroupOutput(
                keyed_items=keyed_items,
                groups=groups,
                group_count=len(groups),
                item_count=n,
                ungrouped=sum(1 for g in groups if g.count == 1),
                item_keys=item_keys,
                matched_existing_count=sum(1 for g in groups if g.matched_existing is not None),
                key_collisions=collisions,
                unknown_ids=sorted(unknown),
                dropped=dropped,
                leads_changed=leads_changed,
                split_from_groups=split,
            )
        )

    @staticmethod
    def _match_existing(
        config: GroupConfig,
        existing: list[JsonValue],
        comps: _Components,
        n: int,
        keys: list[str | None],
        shared: list[set[str]],
        toks: list[frozenset[str]],
        stop: frozenset[str],
    ) -> dict[int, str]:
        rule = config.existing
        assert rule is not None
        prior: list[tuple[str, set[str], set[str], frozenset[str]]] = []
        for record in existing:
            key_value, found = _first(record, rule.key_path)
            if not found:
                continue
            values = {_identity(v) for v in _values(record, rule.values_path)} if rule.values_path else set()
            key_values = (
                {_identity(v) for v in _values(record, rule.key_value_path)} if rule.key_value_path else set()
            )
            words = (
                _text_words(record, rule.text_paths, stop, config.token_overlap.min_word_length)
                if rule.text_paths and config.token_overlap is not None
                else frozenset()
            )
            prior.append((_id_text(key_value), values, key_values, words))

        members: dict[int, list[int]] = {}
        for i in range(n):
            members.setdefault(comps.find(i), []).append(i)

        best: dict[int, str] = {}
        for root, group in members.items():
            g_values = set().union(*(shared[i] for i in group))
            g_keys = {keys[i] for i in group if keys[i] is not None}
            candidates: list[tuple[int, str]] = []
            for key, values, key_values, words in prior:
                if values and g_values & values:
                    candidates.append((0, key))
                elif key_values and g_keys & key_values:
                    candidates.append((1, key))
                elif words and config.token_overlap is not None and any(
                    _similar(toks[i], words, config.token_overlap) for i in group
                ):
                    candidates.append((2, key))
            if candidates:
                best[root] = min(candidates)[1]

        first_root: dict[str, int] = {}
        for root in sorted(best):
            key = best[root]
            if key in first_root:
                comps.join(first_root[key], root, "existing")
            else:
                first_root[key] = root
        return {comps.find(root): key for key, root in first_root.items()}

    @staticmethod
    def _lead_comparator(config: GroupConfig, items: list[JsonValue], decision_leads: set[int]):
        def compare(a: int, b: int) -> int:
            for sort in config.lead_by:
                va, fa = _first(items[a], sort.path)
                vb, fb = _first(items[b], sort.path)
                if fa != fb:
                    return -1 if fa else 1  # a missing value sorts last, whatever the order
                if fa and fb:
                    if sort.measure == "length":
                        va, vb = len(_id_text(va)), len(_id_text(vb))
                    result = _compare_values(va, vb)
                    if result:
                        return -result if sort.order == "desc" else result
            if (a in decision_leads) != (b in decision_leads):
                return -1 if a in decision_leads else 1
            return (a > b) - (a < b)

        return compare
