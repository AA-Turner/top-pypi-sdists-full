"""Collection staples over list payloads — dedupe / sort / limit / batch / aggregate.

The table-stakes list primitives every workflow system ships (n8n's Remove
Duplicates / Sort / Limit / Summarize, Zapier's Formatter line-items). They
compose with kind-filtered edges and ``each``/``all`` fan-out: shape the list
here, then dispatch it.

Key paths use the ONE platform accessor grammar
(``matrx_graph.content_ir.accessor`` — ``a.b`` / ``a[].b``), never a new
dialect. An empty key path means "the item itself". A path that resolves to
nothing on an item is a HOLE: dedupe/sort/aggregate treat it per their
declared ``missing`` posture rather than crashing or silently guessing.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import re
import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, ClassVar, Literal

from matrx_utils.splitting import (
    TokenizerUnavailable,
    apportion,
    fold_plan,
    measure_text,
    opens_a_division,
    pack,
    split_text,
)
from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator

from matrx_graph.content_ir.accessor import resolve_path
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.errors import ExecutionError
from matrx_graph.text_match import fold as _shared_fold
from matrx_graph.nodes._sandbox import bind_item, safe_eval, validate_expression
from matrx_graph.nodes.data.filter import (
    DedupeMatch,
    FilterOutput,
    LeftOutEntry,
    LeftOutOptions,
    left_out_entry,
    step_id,
)
from matrx_graph.safe_regex import UnsafePatternError, compile_safe
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success

_IO_HANDLES = (
    HandleSpec(id="in", direction=HandleDirection.INPUT),
    HandleSpec(id="out", direction=HandleDirection.OUTPUT),
)


def _key_of(item: JsonValue, path: str) -> tuple[Any, bool]:
    """(value, found) for ``path`` on ``item``. Empty path = the item itself."""
    if not path:
        return item, True
    resolution = resolve_path(item, path, unwrap_root=False)
    if not resolution.values:
        return None, False
    return (
        resolution.values[0] if len(resolution.values) == 1 else resolution.values,
        True,
    )


def _identity(value: Any) -> str:
    """Stable hashable identity for arbitrary JSON values."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


# ---------------------------------------------------------------------------
# data.dedupe
# ---------------------------------------------------------------------------


def dedupe_identity(item: JsonValue, key: str, normalize: str) -> str:
    """What an item is compared by when deduping by an exact key (a hole is its own bucket)."""
    key_value, found = _key_of(item, key)
    if found and normalize != "none" and isinstance(key_value, str):
        key_value = _fold_words(key_value) if normalize == "text" else _fold_text(key_value)
    return _identity(key_value) if found else "\x00missing:" + _identity(item)


class DedupeInput(KindModel, kind="dedupe_request"):
    items: list[JsonValue] = Field(description="The list to remove duplicates from.")
    against: list[JsonValue] = Field(
        default_factory=list,
        description=(
            "Entries that already exist (e.g. records already saved). Items matching one by the "
            "same key / normalize / similar rules are dropped and reported in `matches`; these "
            "entries are never in the output."
        ),
    )


class DedupeMerge(BaseModel):
    """How duplicates combine into the surviving copy (2026-10-26).

    Search results found by several engines, contacts found on several pages,
    social accounts found by several sources: keep one row, lose nothing.
    Field names are top-level keys of each item (items must be objects).
    """

    model_config = ConfigDict(extra="forbid")

    combine_lists: list[str] = Field(
        default_factory=list,
        description=(
            "Fields whose values are joined across duplicates — unique, in the "
            "order first seen (e.g. 'engines', 'queries', 'found_on'). A single "
            "value counts as a one-item list; empty values are skipped."
        ),
    )
    keep_lowest: list[str] = Field(
        default_factory=list,
        description=(
            "Number fields that keep the lowest value across duplicates "
            "(e.g. 'rank', 'position'). Non-numbers are ignored."
        ),
    )


    fill_empty: list[str] = Field(
        default_factory=list,
        description=(
            "Fields the surviving copy fills from the others when its own value is "
            "empty (missing, null, blank text, [] or {}): the first non-empty value across "
            "the copies, in list order (e.g. one engine has the description, another "
            "the thumbnail). '*' means every field not named in combine_lists or "
            "keep_lowest."
        ),
    )


def _merge_duplicates(group: list[JsonValue], survivor: JsonValue, merge: DedupeMerge) -> JsonValue:
    """The survivor with ``merge``'s fields combined across every copy in ``group``."""
    if not isinstance(survivor, dict):
        raise ExecutionError(
            "data.dedupe: merge needs each item to be an object with named "
            f"fields, but a duplicate is a {type(survivor).__name__}. Remove "
            "the merge setting, or dedupe a list of objects."
        )
    merged = dict(survivor)
    for name in merge.combine_lists:
        seen: set[str] = set()
        combined: list[JsonValue] = []
        present = False
        for copy in group:
            if not isinstance(copy, dict) or name not in copy:
                continue
            present = True
            value = copy[name]
            for element in value if isinstance(value, list) else [value]:
                if element is None or element == "":
                    continue
                identity = _identity(element)
                if identity not in seen:
                    seen.add(identity)
                    combined.append(element)
        if present:
            merged[name] = combined
    for name in merge.keep_lowest:
        numbers = [
            copy[name]
            for copy in group
            if isinstance(copy, dict)
            and isinstance(copy.get(name), (int, float))
            and not isinstance(copy.get(name), bool)
        ]
        if numbers:
            merged[name] = min(numbers)
    fill = list(merge.fill_empty)
    if "*" in fill:
        named = {*merge.combine_lists, *merge.keep_lowest}
        fill = [n for n in fill if n != "*"]
        for copy in group:
            if isinstance(copy, dict):
                fill.extend(k for k in copy if k not in named and k not in fill)
    for name in fill:
        if not _is_empty(merged.get(name)):
            continue
        for copy in group:
            if isinstance(copy, dict) and not _is_empty(copy.get(name)):
                merged[name] = copy[name]
                break
    return merged


def _is_empty(value: JsonValue) -> bool:
    """Missing, null, blank text, [] or {} — what ``fill_empty`` fills."""
    return value is None or (isinstance(value, str) and not value.strip()) or value == [] or value == {}


#: Small joining words that never make two texts "about the same thing".
#: The ONE default stop list for word matching (data.dedupe ``similar``, data.group).
SIMILAR_STOP_WORDS = frozenset(
    "a an and the of to in for with on at by is are our we your you us it its that this or".split()
)
#: A word: letters/digits, with ' . - + allowed only BETWEEN them ("don't", "e-mail", "3.5");
#: trailing punctuation never sticks ("delivery." is "delivery").
_SIMILAR_WORD = re.compile(r"[^\W_]+(?:['\u2019.\-+][^\W_]+)*")


def _fold_words(value: Any) -> str:
    """``normalize: text`` — the shared fold (``matrx_graph.text_match.fold``: NFKC, casefold,
    invisible characters out), then every run of punctuation/symbols becomes one space and
    spaces collapse: 'What is X?' == 'what is x'. Underscores and accents are kept (the same
    key matrx_seo ``normalize_prompt`` and brand discovery's quote key build)."""
    return " ".join(re.sub(r"[^\w\s]+", " ", _shared_fold(str(value))).split())


def _fold_text(value: Any) -> str:
    """Case-, accent- and whitespace-folded text: 'Fast  Delivery ' == 'fast delivery'."""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.casefold().split())


class DedupeSimilar(BaseModel):
    """Near-duplicate matching: two items are the same when their text shares enough words.

    The words of a text are its lower-cased, accent-folded word SET (``&`` read as
    ``and``; small joining words left out unless ``keep_stop_words``). With A and B
    the two sets: ``jaccard`` = |A∩B| / |A∪B|; ``containment`` = |A∩B| / min(|A|,|B|)
    (a short re-cut of a long text scores 1.0). Two texts match when the score is at
    least ``threshold`` (identical word sets always match).
    """

    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        min_length=1,
        description="Path to the text compared (e.g. 'title' or 'quote').",
    )
    measure: Literal["jaccard", "containment"] = Field(
        default="jaccard",
        description=(
            "jaccard: shared words over all words of both texts. containment: shared "
            "words over the shorter text's words, so a short excerpt of a long text matches."
        ),
    )
    threshold: float = Field(
        default=0.85,
        gt=0.0,
        le=1.0,
        description="The least share of words that makes two items duplicates (0.6 loose, 0.85 close).",
    )
    within: str = Field(
        default="",
        description=(
            "Path to a value; items are only compared with others holding the SAME value "
            "(e.g. 'topic'). Empty compares across the whole list."
        ),
    )
    min_words: int = Field(
        default=3,
        ge=1,
        le=100,
        description="A text with fewer words than this only matches an identical word set.",
    )
    keep_stop_words: bool = Field(
        default=False,
        description="Count small joining words (the, of, and ...) as words too.",
    )
    max_items: int = Field(
        default=5000,
        ge=1,
        le=50_000,
        description=(
            "Most items this step compares. A longer list fails the step with a plain "
            "message (matching is pairwise): dedupe by key or split the list first."
        ),
    )


class DedupeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(
        default="",
        description=(
            "Path to the value that defines 'the same' (e.g. 'url' or "
            "'author.email'). Leave empty to compare whole items."
        ),
    )
    id_path: str = Field(
        default="id",
        description="Path to an item's id; `matches` carries the matched item's id from here (e.g. the saved record's id).",
    )
    normalize: Literal["none", "case_space", "text"] = Field(
        default="none",
        description=(
            "How the key value is compared. none: exactly. case_space: ignoring upper/lower "
            "case, accents and extra spaces, so 'Fast Delivery ' and 'fast  delivery' are one. "
            "text: also ignoring punctuation, so 'What is X?' and 'what is x' are one."
        ),
    )
    similar: DedupeSimilar | None = Field(
        default=None,
        description=(
            "Match near-duplicates by shared words instead of an exact key. Items are "
            "compared with the first item of each kept group (no chains of near-matches). "
            "Set this OR `key`, not both."
        ),
    )
    keep: Literal["first", "last"] = Field(
        default="first",
        description="Which duplicate survives: the first seen, or the last.",
    )
    merge: DedupeMerge | None = Field(
        default=None,
        description=(
            "Merge duplicates instead of dropping their values: the surviving "
            "copy gets the named fields combined across every copy. Leave "
            "empty to simply drop the repeats."
        ),
    )

    @model_validator(mode="after")
    def _one_way_to_match(self) -> DedupeConfig:
        if self.similar is not None and self.key:
            raise ValueError(
                "data.dedupe: set `similar` (matching by shared words) or `key` (exact), not both. "
                "To match within a group, use similar.within."
            )
        if self.similar is not None and self.normalize != "none":
            raise ValueError("data.dedupe: `normalize` applies to an exact `key`; similar already folds case and spaces.")
        return self


#: ``data.dedupe`` and ``data.limit`` produce a kept subset — the SAME contract
#: ``data.filter`` owns. One kind, one model (plan §10d-B2): this was a second
#: class for one registered shape, which is how two nodes drift apart while
#: both claiming to answer with ``filter_result``.
KeptListOutput = FilterOutput


def word_set(
    value: Any,
    *,
    stop_words: frozenset[str] = SIMILAR_STOP_WORDS,
    min_length: int = 1,
) -> frozenset[str]:
    """THE word set of a text, for every "do these say the same thing" match.

    Lower-cased, accent-folded words (``&`` read as ``and``), minus ``stop_words``
    and words shorter than ``min_length``. A non-string value is read as its JSON
    text. Shared by ``data.dedupe`` (``similar``) and ``data.group`` — never a
    second tokenizer.
    """
    text = _fold_text(value if isinstance(value, str) else _identity(value)).replace("&", " and ")
    return frozenset(
        w for w in _SIMILAR_WORD.findall(text) if len(w) >= min_length and w not in stop_words
    )


def word_overlap(
    a: frozenset[str] | set[str], b: frozenset[str] | set[str], measure: Literal["jaccard", "containment"]
) -> tuple[float, int]:
    """(score, shared words) of two word sets. ``jaccard`` = |A∩B| / |A∪B|;
    ``containment`` = |A∩B| / min(|A|,|B|). An empty set scores 0."""
    if not a or not b:
        return 0.0, 0
    shared = len(a & b)
    base = len(a | b) if measure == "jaccard" else min(len(a), len(b))
    return shared / base, shared


def _similar_words(item: JsonValue, similar: DedupeSimilar) -> frozenset[str]:
    value, found = _key_of(item, similar.text)
    if not found or value is None:
        return frozenset()
    return word_set(value, stop_words=frozenset() if similar.keep_stop_words else SIMILAR_STOP_WORDS)


def _is_near(a: frozenset[str], b: frozenset[str], similar: DedupeSimilar) -> bool:
    if a == b:
        return True
    if min(len(a), len(b)) < similar.min_words:
        return False
    return word_overlap(a, b, similar.measure)[0] >= similar.threshold


def _similar_groups(items: list[JsonValue], similar: DedupeSimilar) -> list[list[int]]:
    """Group near-duplicates, in first-seen order.

    Each item joins the first earlier group whose FIRST item it is near (so a long
    chain of slight rewrites does not collapse into one). Cost: an inverted index
    word -> groups means an item is only compared with groups sharing a word with it
    (and, with ``within``, only inside its own scope); the worst case, every item
    sharing a word, is O(items x groups), bounded by ``similar.max_items``.
    An item with no words (hole or empty text) is never a duplicate of anything.
    Returns groups of POSITIONS in ``items``.
    """
    if len(items) > similar.max_items:
        raise ExecutionError(
            f"data.dedupe: similar matching compares items pairwise and is capped at "
            f"{similar.max_items} items, but the list has {len(items)}. Dedupe by an exact "
            "key first, split the list, or raise similar.max_items (up to 50000)."
        )
    groups: list[list[int]] = []
    leaders: list[frozenset[str]] = []
    index: dict[tuple[str, str], list[int]] = {}
    for position, item in enumerate(items):
        words = _similar_words(item, similar)
        scope = ""
        if similar.within:
            scope_value, scope_found = _key_of(item, similar.within)
            scope = _identity(scope_value) if scope_found else "\x00missing"
        home = -1
        if words:
            seen: set[int] = set()
            for word in words:
                for gi in index.get((scope, word), ()):
                    if gi in seen:
                        continue
                    seen.add(gi)
                    if (home < 0 or gi < home) and _is_near(words, leaders[gi], similar):
                        home = gi
        if home >= 0:
            groups[home].append(position)
            continue
        groups.append([position])
        leaders.append(words)
        for word in words:
            index.setdefault((scope, word), []).append(len(groups) - 1)
    return groups


class DedupeExecutor:
    """Remove duplicates by key path (or whole-item identity)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.dedupe",
        category=NodeCategory.DATA,
        display_name="Remove Duplicates",
        description=(
            "Keep one of each — drop repeated items from a list, matched by an exact key "
            "or by shared words (similar matching compares at most 5000 items by default). "
            "Says which kept item (or `against` entry, e.g. an already-saved record) each "
            "dropped item matched, in `matches`."
        ),
        input_schema=DedupeInput,
        input_kind="dedupe_request",
        output_schema=KeptListOutput,
        config_schema=DedupeConfig,
        # Reuse-first: the shape ({items, kept, dropped}) IS filter_result —
        # a dedupe is a filter whose predicate is 'first (or last) of its key'.
        output_kind="filter_result",
        handles=_IO_HANDLES,
        determinism=ActionTier.PURE,
        icon="list-x",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: DedupeInput,
        config: DedupeConfig,
    ) -> NodeResult[KeptListOutput]:
        _ = ctx
        # `against` entries go FIRST in one pool, so an item that matches one joins its
        # group and is dropped; the entry itself is never output. A hole at the key is an
        # absence, never "equal to every other hole" (it is its own bucket).
        against = inputs.against
        pool = [*against, *inputs.items]
        offset = len(against)
        if config.similar is not None:
            index_groups = _similar_groups(pool, config.similar)
        else:
            buckets: dict[str, list[int]] = {}
            for position, item in enumerate(pool):
                buckets.setdefault(dedupe_identity(item, config.key, config.normalize), []).append(position)
            index_groups = list(buckets.values())

        def id_of(item: JsonValue) -> JsonValue:
            value, found = _key_of(item, config.id_path)
            return value if found else None

        items: list[JsonValue] = []
        matches: list[DedupeMatch] = []
        for group in index_groups:
            held = [p for p in group if p < offset]
            mine = [p - offset for p in group if p >= offset]
            if held:
                for p in mine:
                    matches.append(
                        DedupeMatch(index=p, against_index=held[0], survivor_id=id_of(against[held[0]]))
                    )
                continue
            copies = [inputs.items[p] for p in mine]
            survivor_at = mine[0] if config.keep == "first" else mine[-1]
            survivor = inputs.items[survivor_at]
            if config.merge is not None:
                survivor = _merge_duplicates(copies, survivor, config.merge)
            items.append(survivor)
            for p in mine:
                if p != survivor_at:
                    matches.append(
                        DedupeMatch(index=p, survivor_index=survivor_at, survivor_id=id_of(inputs.items[survivor_at]))
                    )
        matches.sort(key=lambda m: m.index)
        return success(
            KeptListOutput(
                items=items, kept=len(items), dropped=len(inputs.items) - len(items), matches=matches
            )
        )


# ---------------------------------------------------------------------------
# data.sort
# ---------------------------------------------------------------------------


class SortInput(BaseModel):
    # extra="allow": `order_by` keys read this step's other inputs — `position_in` names one
    # (a list), and an `expression` reads them as ``inputs['$in'][<name>]``.
    model_config = ConfigDict(extra="allow")
    items: list[JsonValue] = Field(description="The list to sort.")


class SortKey(BaseModel):
    """One sort key: a path, an expression, or a position in another input's list."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(default="", description="Path to the value (e.g. 'score'); empty with `expression` unset = the item itself.")
    expression: str | None = Field(
        default=None,
        description=(
            "Instead of `key`: an expression over the item as `inputs` (other inputs as "
            "``inputs['$in'][<name>]``), e.g. ``url_depth(inputs['url'])`` or ``inputs['kind'] != 'home'`` "
            "(False sorts before True)."
        ),
    )
    position_in: str | None = Field(
        default=None,
        description=(
            "Order by where the value at `key` stands in this input's list (e.g. 'kinds_first'): "
            "listed values first in list order, unlisted ones count as missing."
        ),
    )
    order: Literal["asc", "desc"] = Field(default="asc", description="Ascending (smallest first) or descending.")

    @model_validator(mode="after")
    def _one_source(self) -> SortKey:
        if self.expression is not None and (self.key or self.position_in):
            raise ValueError("A sort key is an `expression`, or a `key` (optionally with `position_in`), not both.")
        if self.expression is not None:
            validate_expression(self.expression)
        return self


class SortConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(
        default="",
        description=(
            "Path to the value to sort by (e.g. 'score' or 'author.name'). "
            "Leave empty to sort the items themselves."
        ),
    )
    order: Literal["asc", "desc"] = Field(
        default="asc", description="Ascending (smallest first) or descending."
    )
    missing: Literal["last", "first"] = Field(
        default="last",
        description="Where items whose sort value is absent should land.",
    )
    order_by: list[SortKey] = Field(
        default_factory=list,
        description=(
            "Several keys, most important first (ties fall to the next key, then the list's order). "
            "When given, `key` and `order` are not used; `missing` applies to every key."
        ),
    )


class SortOutput(KindModel, kind="sorted_list_result"):
    items: list[JsonValue] = Field(description="The sorted list.")
    count: int = Field(description="How many items the list holds.")


def _sort_rank(value: Any) -> tuple[int, Any]:
    """A total order over mixed JSON values: group by type, then compare.

    Comparing 3 with "3" raises in Python; a workflow list is user data and
    may mix types, so rank by type family first — numbers, then strings, then
    everything else by its canonical JSON identity.
    """
    if isinstance(value, bool):
        return (0, int(value))
    if isinstance(value, int | float):
        return (0, float(value))
    if isinstance(value, str):
        return (1, value)
    return (2, _identity(value))


class SortExecutor:
    """Stable sort by key path, mixed-type safe, holes placed deliberately."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.sort",
        category=NodeCategory.DATA,
        display_name="Sort",
        description="Put a list in order by one of its values.",
        input_schema=SortInput,
        input_kind="items",
        output_schema=SortOutput,
        config_schema=SortConfig,
        output_kind="sorted_list_result",
        handles=_IO_HANDLES,
        determinism=ActionTier.PURE,
        icon="arrow-up-down",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SortInput,
        config: SortConfig,
    ) -> NodeResult[SortOutput]:
        _ = ctx
        if config.order_by:
            items = _multi_key_sort(inputs, config)
            return success(SortOutput(items=items, count=len(items)))
        present: list[tuple[tuple[int, Any], JsonValue]] = []
        holes: list[JsonValue] = []
        for item in inputs.items:
            key_value, found = _key_of(item, config.key)
            if found:
                present.append((_sort_rank(key_value), item))
            else:
                holes.append(item)
        present.sort(key=lambda pair: pair[0], reverse=config.order == "desc")
        ordered = [item for _, item in present]
        items = holes + ordered if config.missing == "first" else ordered + holes
        return success(SortOutput(items=items, count=len(items)))


def _sort_value(item: JsonValue, index: int, sort: SortKey, others: dict[str, Any]) -> tuple[Any, bool]:
    if sort.expression is not None:
        bound = bind_item(sort.expression, item, where=f"data.sort: item {index}")
        if others:
            bound = {**bound, "$in": others}
        try:
            return safe_eval(sort.expression, bound), True
        except KeyError:
            # The item lacks a field the expression reads: a hole, placed per `missing` (as a key path would be).
            return None, False
        except ExecutionError:
            raise
        except Exception as e:  # noqa: BLE001 - name the step, expression and item
            raise ExecutionError(
                f"data.sort: the expression {sort.expression!r} failed on item {index}: {type(e).__name__}: {e}"
            ) from e
    value, found = _key_of(item, sort.key)
    if sort.position_in is None or not found:
        return value, found
    listed = others.get(sort.position_in)
    if not isinstance(listed, list):
        raise ExecutionError(
            f"data.sort: position_in names {sort.position_in!r}, which this step did not receive as a list."
        )
    identities = [_identity(v) for v in listed]
    identity = _identity(value)
    return (identities.index(identity), True) if identity in identities else (None, False)


def _multi_key_sort(inputs: SortInput, config: SortConfig) -> list[JsonValue]:
    others = {k: v for k, v in inputs.model_dump(mode="json").items() if k != "items"}
    return [inputs.items[i] for i in multi_key_order(inputs.items, config.order_by, config.missing, others)]


def multi_key_order(
    items: list[JsonValue], order_by: list[SortKey], missing: str, others: dict[str, Any]
) -> list[int]:
    """The input positions in sorted order: stable sorts from the least to the most important key;
    holes per `missing`, per key."""
    rows = list(enumerate(items))
    for sort in reversed(order_by):
        present: list[tuple[tuple[int, Any], tuple[int, JsonValue]]] = []
        holes: list[tuple[int, JsonValue]] = []
        for index, item in rows:
            value, found = _sort_value(item, index, sort, others)
            if found and value is not None:
                present.append((_sort_rank(value), (index, item)))
            else:
                holes.append((index, item))
        present.sort(key=lambda pair: pair[0], reverse=sort.order == "desc")
        ordered = [row for _, row in present]
        rows = holes + ordered if missing == "first" else ordered + holes
    return [index for index, _ in rows]


# ---------------------------------------------------------------------------
# data.limit
# ---------------------------------------------------------------------------


class LimitInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[JsonValue] = Field(description="The list to take a slice of.")


class RoundRobinSort(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, description="Path to the value that ranks items inside a group (e.g. 'score').")
    order: Literal["asc", "desc"] = Field(default="desc", description="desc: the largest value is best.")


class RoundRobin(BaseModel):
    """Take turns across groups: the best of each group, then the second best of each, and so on."""

    model_config = ConfigDict(extra="forbid")

    by: str = Field(min_length=1, description="Path to the value that defines a group (e.g. 'product_line').")
    order_by: list[RoundRobinSort] = Field(
        default_factory=list,
        description="Best-first order inside each group, most important key first; empty keeps the list's order. Items missing a value come last.",
    )
    group_order: Literal["largest_first", "first_seen", "listed"] = Field(
        default="largest_first",
        description="Who goes first in each round: the biggest groups, the group seen first, or the order in `groups`.",
    )
    groups: list[str] = Field(
        default_factory=list,
        description="For group_order 'listed': group values in turn order; unlisted groups follow, largest first.",
    )
    output_order: Literal["rotation", "original"] = Field(
        default="rotation",
        description="rotation: in the order picked. original: the picked items in the order they had in the list.",
    )

    @model_validator(mode="after")
    def _listed_needs_groups(self) -> RoundRobin:
        if self.group_order == "listed" and not self.groups:
            raise ValueError("round_robin.group_order 'listed' needs `groups`.")
        if len(set(self.groups)) != len(self.groups):
            raise ValueError("round_robin.groups names a group more than once.")
        return self


class LimitConfig(LeftOutOptions):
    model_config = ConfigDict(extra="forbid")

    count: int = Field(
        ge=0,
        le=100_000,
        description="How many items to keep.",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="How many items to skip before keeping (ignored from the end).",
    )
    from_end: bool = Field(
        default=False,
        description="Take the LAST items instead of the first.",
    )
    round_robin: RoundRobin | None = Field(
        default=None,
        description=(
            "Pick the `count` items by turns across groups instead of from the top, so "
            "one big group cannot crowd the others out. Not with offset or from_end."
        ),
    )

    @model_validator(mode="after")
    def _round_robin_alone(self) -> LimitConfig:
        if self.round_robin is not None and (self.offset or self.from_end):
            raise ValueError("data.limit: round_robin picks across groups; it cannot combine with offset or from_end.")
        return self


def _round_robin_pick(items: list[JsonValue], count: int, spec: RoundRobin) -> list[JsonValue]:
    return [item for _, item in _round_robin_positions(items, count, spec)]


def _round_robin_positions(items: list[JsonValue], count: int, spec: RoundRobin) -> list[tuple[int, JsonValue]]:
    buckets: dict[str, list[tuple[int, JsonValue]]] = {}
    labels: dict[str, str] = {}
    for position, item in enumerate(items):
        value, found = _key_of(item, spec.by)
        # A hole and an explicit null are the same thing: no group value.
        identity = _identity(value) if found and value is not None else "\x00missing"
        buckets.setdefault(identity, []).append((position, item))
        # `groups` names are compared as text, so 1 and "1" both answer to "1".
        labels.setdefault(identity, value if isinstance(value, str) else str(value))
    for members in buckets.values():
        # Stable sorts applied from the least to the most important key.
        for sort in reversed(spec.order_by):
            present = [(m, _key_of(m[1], sort.key)) for m in members]
            have = [(m, _sort_rank(v)) for m, (v, ok) in present if ok]
            holes = [m for m, (_, ok) in present if not ok]
            have.sort(key=lambda pair: pair[1], reverse=sort.order == "desc")
            members[:] = [m for m, _ in have] + holes
    first_seen = list(buckets)
    seen_at = {g: n for n, g in enumerate(first_seen)}
    if spec.group_order == "largest_first":
        order = sorted(first_seen, key=lambda g: (-len(buckets[g]), seen_at[g]))
    elif spec.group_order == "listed":
        by_label: dict[str, list[str]] = {}
        for g in first_seen:
            if g != "\x00missing":
                by_label.setdefault(labels[g], []).append(g)
        listed = [g for name in spec.groups for g in by_label.get(name, [])]
        rest = sorted((g for g in first_seen if g not in listed), key=lambda g: (-len(buckets[g]), seen_at[g]))
        order = listed + rest
    else:
        order = first_seen
    picked: list[tuple[int, JsonValue]] = []
    depth = 0
    while len(picked) < count and any(depth < len(buckets[g]) for g in order):
        for g in order:
            if len(picked) >= count:
                break
            if depth < len(buckets[g]):
                picked.append(buckets[g][depth])
        depth += 1
    if spec.output_order == "original":
        picked.sort(key=lambda pair: pair[0])
    return picked


class LimitExecutor:
    """head / tail / offset over a list."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.limit",
        category=NodeCategory.DATA,
        display_name="Limit",
        description="Keep only the first (or last) N items of a list.",
        input_schema=LimitInput,
        input_kind="items",
        output_schema=KeptListOutput,
        config_schema=LimitConfig,
        # Reuse-first: same {items, kept, dropped} shape as data.filter.
        output_kind="filter_result",
        handles=_IO_HANDLES,
        determinism=ActionTier.PURE,
        icon="list-minus",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: LimitInput,
        config: LimitConfig,
    ) -> NodeResult[KeptListOutput]:
        total = len(inputs.items)
        if config.round_robin is not None:
            picked = _round_robin_positions(inputs.items, config.count, config.round_robin)
            positions = {p for p, _ in picked}
            items = [item for _, item in picked]
        elif config.from_end:
            start = max(total - config.count, 0) if config.count else total
            positions = set(range(start, total))
            items = inputs.items[start:]
        else:
            positions = set(range(config.offset, min(config.offset + config.count, total)))
            items = inputs.items[config.offset : config.offset + config.count]
        left_out: list[LeftOutEntry] = []
        if config.left_out:
            reason = f"past the limit of {config.count}"
            if config.from_end and not config.round_robin:
                reason = f"outside the last {config.count} items"
            elif config.offset and not config.round_robin:
                reason = f"outside items {config.offset + 1}-{config.offset + config.count}"
            left_out = [
                left_out_entry(item, index, config, default_reason=reason, others={}, step=step_id(ctx))
                for index, item in enumerate(inputs.items)
                if index not in positions
            ]
        return success(
            KeptListOutput(
                items=items, kept=len(items), dropped=total - len(items), left_out=left_out if config.left_out else None
            )
        )


# ---------------------------------------------------------------------------
# data.batch
# ---------------------------------------------------------------------------

BatchMeasure = Literal["count", "chars", "tokens"]


class BatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[JsonValue] = Field(description="The list to split into chunks.")


class BatchConfig(BaseModel):
    """How to split. Only ``size`` is required: by default ``size`` items per batch."""

    model_config = ConfigDict(extra="forbid")

    size: int = Field(
        ge=1,
        le=50_000_000,
        description=(
            "The budget per batch, in the unit `measure` names: items (count), "
            "characters (chars) or tokens (tokens). The last batch may be smaller."
        ),
    )
    measure: BatchMeasure = Field(
        default="count",
        description=(
            "What `size` counts: items, characters, or real tokens (the cl100k "
            "tokenizer). Characters and tokens are read from `text_path`."
        ),
    )
    text_path: str = Field(
        default="",
        description=(
            "Path to the text to measure on each item (e.g. 'content'). Empty: a "
            "text item is measured as itself, any other item as its JSON."
        ),
    )
    overlap: int = Field(
        default=0,
        ge=0,
        le=10_000,
        description="Items repeated from the end of one batch at the start of the next.",
    )
    split_oversized: bool = Field(
        default=True,
        description=(
            "When measuring chars or tokens, an item larger than `size` is cut at "
            "its paragraphs, lines, sentences or words into pieces that fit."
        ),
    )
    never_cross: list[str] = Field(
        default_factory=list,
        description=(
            "Paths that may never change inside a batch (e.g. 'source_id'): a new "
            "value always starts a new batch."
        ),
    )
    prefer_cut_on: list[str] = Field(
        default_factory=list,
        description=(
            "Paths whose change marks a natural cut (e.g. 'section_title'): a batch "
            "that must end is cut back to the last one when it stays `min_fill` full."
        ),
    )
    prefer_cut_at_headings: bool = Field(
        default=False,
        description=(
            "Treat an item whose text opens with a heading, chapter or page line as "
            "a natural cut."
        ),
    )
    prefer_cut_pattern: str | None = Field(
        default=None,
        description="A regular expression: an item whose text opens with a match is a natural cut.",
    )
    continues_path: str = Field(
        default="",
        description=(
            "Path to a true/false flag (e.g. 'is_continuation'): a true item belongs "
            "with the one before it even when a `never_cross` or `prefer_cut_on` value changed."
        ),
    )
    min_fill: float = Field(
        default=0.5,
        gt=0,
        le=1,
        description="How full a batch must stay for a natural cut to be taken.",
    )
    max_batches: int | None = Field(
        default=None,
        ge=1,
        le=10_000,
        description=(
            "At most this many batches: neighbours are merged evenly, never across "
            "a `never_cross` change."
        ),
    )
    quota_total: int | None = Field(
        default=None,
        ge=1,
        le=1_000_000,
        description=(
            "Share this many items to produce across the batches in proportion to "
            "their size (each batch's `quota`)."
        ),
    )
    quota_min_each: int = Field(
        default=1,
        ge=0,
        le=10_000,
        description="Every batch's quota is at least this.",
    )
    label_path: str = Field(
        default="",
        description="Path to a label on each item (e.g. 'section_title'); a batch is named first – last.",
    )
    id_path: str = Field(
        default="",
        description="Path to each item's stable id; batch ids are derived from them (else from the items).",
    )

    fit: Literal["in_order", "first_fit"] = Field(
        default="in_order",
        description=(
            "How a batch fills. in_order: items go in as they come and a batch closes at the "
            "first item that does not fit. first_fit: an item that does not fit the room left is "
            "passed over and later, smaller items still fill the batch; the passed-over items "
            "start the next batch, in their order. (With measure 'count' every item is 1, so both act the same.)"
        ),
    )
    overflow: Literal["next_batch", "left_out"] = Field(
        default="next_batch",
        description=(
            "What happens to items that do not fit. next_batch: they go into later batches. "
            "left_out: ONE batch is made (a single budget) and the rest are listed in `left_out` "
            "with their size, e.g. a reading budget."
        ),
    )

    @model_validator(mode="after")
    def _fit_stands_alone(self) -> BatchConfig:
        if self.fit == "in_order" and self.overflow == "next_batch":
            return self
        clashes = [
            name
            for name, on in (
                ("overlap", self.overlap),
                ("never_cross", self.never_cross),
                ("prefer_cut_on", self.prefer_cut_on),
                ("prefer_cut_at_headings", self.prefer_cut_at_headings),
                ("prefer_cut_pattern", self.prefer_cut_pattern),
                ("continues_path", self.continues_path),
            )
            if on
        ]
        if self.overflow == "left_out" and self.max_batches is not None:
            clashes.append("max_batches")
        if clashes:
            raise ValueError(
                "data.batch: fit 'first_fit' / overflow 'left_out' fill by room alone, so they "
                f"cannot combine with {', '.join(clashes)}. Remove those settings or use fit 'in_order'."
            )
        return self

    @field_validator("prefer_cut_pattern")
    @classmethod
    def _pattern_compiles(cls, value: str | None) -> str | None:
        if value:
            try:
                compile_safe(value, level="exponential")
            except UnsafePatternError as exc:
                raise ValueError(f"prefer_cut_pattern: {exc}") from exc
        return value or None


class BatchPart(KindSubModel):
    """What a consumer needs beside one batch's items (``batches[index]``) — the items
    are never stored twice. A fan-out maps over ``batches`` and reads this batch's
    quota/label with ``$in.parts.{$index}.quota``."""

    id: str = Field(description="Stable id: the same items in the same order give the same id.")
    index: int = Field(description="Position of this batch, from 0.")
    item_count: int = Field(description="How many items this batch holds.")
    size: int = Field(description="Measured size, in the unit `measure` names.")
    first_item: int = Field(description="Input position of the first item.")
    last_item: int = Field(description="Input position of the last item.")
    overlap_count: int = Field(
        default=0, description="How many leading items repeat the previous batch's end."
    )
    split_items: list[int] = Field(
        default_factory=list,
        description="Input positions of items that were too large and were cut into pieces here.",
    )
    label: str = Field(default="", description="First – last label, or 'Part N'.")
    quota: int | None = Field(default=None, description="This batch's share of `quota_total`.")
    ended_by: str = Field(
        default="end",
        description="Why it ended: budget, natural (a preferred cut), forced (a never_cross change), or end.",
    )


class BatchLeftOut(LeftOutEntry):
    """An item the single budget had no room for (``overflow: left_out``): the shared
    left-out entry (position, label, reason, step) plus its measured size."""

    item: int = Field(description="Input position of the item (or of the piece's source item).")
    size: int = Field(description="Its measured size, in the unit `measure` names.")


class BatchOutput(KindModel, kind="batched_list_result"):
    batches: list[list[JsonValue]] = Field(description="The list split into chunks, in order.")
    count: int = Field(description="How many batches were produced.")
    total_items: int = Field(description="How many items went in.")
    size: int = Field(description="The requested batch size.")
    measure: str = Field(default="count", description="What `size` counted: count, chars or tokens.")
    parts: list[BatchPart] = Field(
        default_factory=list,
        description=(
            "Per batch, index-aligned with `batches`: id, size, positions, label and quota "
            "(a fan-out over `batches` reads `$in.parts.{$index}.quota`)."
        ),
    )
    quota_total: int | None = Field(
        default=None, description="The sum of the batches' quotas, when a quota was asked for."
    )
    left_out: list[BatchLeftOut] | None = Field(
        default=None,
        description="With overflow 'left_out': the items that did not fit the one budget, with their size. Absent (null) otherwise, as live kind batched_list_result v14 declares.",
    )
    notes: list[str] = Field(
        default_factory=list,
        description="What the split could not do exactly as asked, in plain words.",
    )


@dataclass
class _BatchUnit:
    source_index: int
    item: JsonValue
    text: str
    size: int
    piece: bool = False


def _batch_text(item: JsonValue, text_path: str) -> str | None:
    value, found = _key_of(item, text_path)
    if not found:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _with_text(item: JsonValue, text_path: str, text: str) -> JsonValue | None:
    """``item`` with the value at a plain dotted ``text_path`` replaced, or None when
    the path is not a plain dict path."""
    if not text_path:
        return text if isinstance(item, str) else None
    if not isinstance(item, dict) or "[" in text_path:
        return None
    clone: dict[str, Any] = json.loads(json.dumps(item))
    node: Any = clone
    keys = text_path.split(".")
    for key in keys[:-1]:
        node = node.get(key) if isinstance(node, dict) else None
        if not isinstance(node, dict):
            return None
    if not isinstance(node, dict) or keys[-1] not in node:
        return None
    node[keys[-1]] = text
    return clone


def _value_identity(item: JsonValue, path: str) -> str:
    value, found = _key_of(item, path)
    return _identity(value) if found else "\x00missing"


class BatchExecutor:
    """Split a list into batches by count, characters or tokens — pairs with fan-out.

    The packing is the shared splitter (:mod:`matrx_utils.splitting`), the same one
    the RAG parent chunker, page extraction and the study-kit planners run, so any
    material — pages, transcript windows, scraped sections, table rows, ingested
    chunks — splits the same way inside a workflow as in code.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.batch",
        category=NodeCategory.DATA,
        display_name="Split into Batches",
        description=(
            "Split a long list into smaller groups — N items, or a character or "
            "token budget cut at natural breaks — to process a group at a time."
        ),
        input_schema=BatchInput,
        input_kind="items",
        output_schema=BatchOutput,
        config_schema=BatchConfig,
        output_kind="batched_list_result",
        handles=_IO_HANDLES,
        determinism=ActionTier.PURE,
        icon="layers",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: BatchInput,
        config: BatchConfig,
    ) -> NodeResult[BatchOutput]:
        try:
            # Off the event loop: measuring 200k items by tokens is seconds of CPU, and
            # one step must never stall every other run on this process.
            planned = await asyncio.to_thread(plan_batches, inputs.items, config)
            for entry in planned.left_out or ():
                entry.step = step_id(ctx)
            return success(planned)
        except _BatchRefused as refused:
            return failure(refused.code, str(refused), details=refused.details)


class _BatchRefused(Exception):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.details = details or {}


def plan_batches(items: list[JsonValue], config: BatchConfig) -> BatchOutput:
    """The pure planner behind ``data.batch`` (tested without an engine)."""
    measure = config.measure
    notes: list[str] = []
    pattern = re.compile(config.prefer_cut_pattern) if config.prefer_cut_pattern else None

    def measure_of(text: str) -> int:
        try:
            return measure_text(text, measure)
        except TokenizerUnavailable as exc:
            raise _BatchRefused("tokenizer_unavailable", str(exc)) from exc

    def units() -> Iterator[_BatchUnit]:
        for index, item in enumerate(items):
            if measure == "count":
                yield _BatchUnit(index, item, _batch_text(item, config.text_path) or "", 1)
                continue
            text = _batch_text(item, config.text_path)
            if text is None:
                raise _BatchRefused(
                    "batch_text_missing",
                    f"Item {index} has no value at text_path '{config.text_path}', so its "
                    f"size in {measure} cannot be measured.",
                    {"item": index, "text_path": config.text_path},
                )
            size = measure_of(text)
            if size > config.size and config.split_oversized:
                pieces = split_text(text, config.size, measure=measure)
                rebuilt = [_with_text(item, config.text_path, p) for p in pieces]
                if pieces and all(r is not None for r in rebuilt):
                    for piece, piece_item in zip(pieces, rebuilt, strict=True):
                        yield _BatchUnit(index, piece_item, piece, measure_of(piece), piece=True)
                    continue
                notes.append(
                    f"Item {index} is larger than the budget but is not text at a plain "
                    "path, so it was kept whole in a batch of its own."
                )
            yield _BatchUnit(index, item, text, size)

    def key_changed(prev: _BatchUnit, unit: _BatchUnit, paths: list[str]) -> bool:
        if not paths:
            return False
        if config.continues_path:
            flag, found = _key_of(unit.item, config.continues_path)
            if found and flag is True:
                return False
        return any(
            _value_identity(prev.item, p) != _value_identity(unit.item, p) for p in paths
        )

    def must_cut(prev: _BatchUnit, unit: _BatchUnit) -> bool:
        return key_changed(prev, unit, config.never_cross)

    def prefers_cut(prev: _BatchUnit, unit: _BatchUnit) -> bool:
        if key_changed(prev, unit, config.prefer_cut_on):
            return True
        if config.prefer_cut_at_headings and opens_a_division(unit.text):
            return True
        return bool(pattern is not None and opens_a_division(unit.text, pattern=pattern))

    has_prefer = bool(config.prefer_cut_on or config.prefer_cut_at_headings or pattern)
    left_out_units: list[_BatchUnit] = []
    if config.fit == "first_fit" or config.overflow == "left_out":
        packed, left_out_units = _fit_by_room(list(units()), config)
    else:
        packed = list(
            pack(
                units(),
                budget=config.size,
                size_of=lambda u: u.size,
                must_cut=must_cut if config.never_cross else None,
                prefers_cut=prefers_cut if has_prefer else None,
                min_fill=config.min_fill,
                overlap=config.overlap,
            )
        )

    groups: list[list[tuple[list[_BatchUnit], int, str]]] = []
    for i, part in enumerate(packed):
        entry = (part.items, part.overlap_count, part.ended_by)
        if i == 0 or packed[i - 1].ended_by == "forced":
            groups.append([entry])
        else:
            groups[-1].append(entry)

    if config.max_batches is not None and len(packed) > config.max_batches:
        groups, fold_note = _fold_groups(groups, config.max_batches)
        if fold_note:
            notes.append(fold_note)

    merged: list[tuple[list[_BatchUnit], int, str]] = [e for g in groups for e in g]
    over = sum(1 for units_, _, _ in merged if len(units_) > 1 and sum(u.size for u in units_) > config.size)
    if config.max_batches is not None and over:
        notes.append(
            f"max_batches={config.max_batches} merged neighbouring batches, so {over} "
            f"batch(es) are over the size budget of {config.size} {measure}."
        )
    sizes = [sum(u.size for u in units_[ov:]) for units_, ov, _ in merged]
    quotas: list[int | None] = [None] * len(merged)
    quota_sum: int | None = None
    if config.quota_total is not None and merged:
        # A batch with no new material (empty sections, only repeated overlap) gets no
        # quota: the floor is for batches that have something to cover.
        live = [i for i, size in enumerate(sizes) if size > 0] or list(range(len(sizes)))
        shares = apportion(
            [sizes[i] for i in live], config.quota_total, min_each=config.quota_min_each
        )
        quotas = [0] * len(merged)
        for i, share in zip(live, shares, strict=True):
            quotas[i] = share
        quota_sum = sum(shares)
        if quota_sum != config.quota_total:
            notes.append(
                f"{len(live)} batches each need at least {config.quota_min_each}, so the "
                f"quota is {quota_sum}, not the {config.quota_total} asked for. Set "
                f"max_batches to {max(1, config.quota_total // max(1, config.quota_min_each))} "
                "to keep it."
            )

    if config.id_path:
        missing = sum(
            1
            for units_, _, _ in merged
            for u in units_
            if not _key_of(u.item, config.id_path)[1]
        )
        if missing:
            notes.append(
                f"{missing} item(s) have no value at id_path '{config.id_path}', so their "
                "batch ids come from where they sit, not from an id; set id_path to a "
                "field every item has."
            )
    parts: list[BatchPart] = []
    seen_ids: dict[str, int] = {}
    for index, (units_, overlap_count, ended_by) in enumerate(merged):
        identity = "|".join(
            _value_identity(u.item, config.id_path) if config.id_path else _identity(u.item)
            for u in units_
        )
        base = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
        nth = seen_ids.get(base, 0)
        seen_ids[base] = nth + 1
        parts.append(
            BatchPart(
                id=f"b_{base}" if nth == 0 else f"b_{base}_{nth}",
                index=index,
                item_count=len(units_),
                size=sum(u.size for u in units_),
                first_item=units_[0].source_index,
                last_item=units_[-1].source_index,
                overlap_count=overlap_count,
                split_items=sorted({u.source_index for u in units_ if u.piece}),
                label=_batch_label(units_, config.label_path, index),
                quota=quotas[index],
                ended_by=ended_by,
            )
        )
    left_out = [
        BatchLeftOut(
            item=u.source_index,
            size=u.size,
            label=_left_out_label(u, config.label_path),
            reason=f"did not fit the budget of {config.size} {measure}",
        )
        for u in left_out_units
    ]
    if left_out:
        notes.append(
            f"{len(left_out)} item(s) did not fit the budget of {config.size} {measure} and are "
            "listed in left_out."
        )
    return BatchOutput(
        batches=[[u.item for u in units_] for units_, _, _ in merged],
        count=len(parts),
        total_items=len(items),
        size=config.size,
        measure=measure,
        parts=parts,
        quota_total=quota_sum,
        # One left_out contract (filter, limit, dedupe, rules, batch, repeated lines): null when off.
        left_out=left_out if config.overflow == "left_out" else None,
        notes=list(dict.fromkeys(notes)),
    )


@dataclass
class _RoomBatch:
    """The shape ``plan_batches`` reads from the shared packer's parts."""

    items: list[_BatchUnit]
    overlap_count: int = 0
    ended_by: str = "end"


def _fit_by_room(
    units_: list[_BatchUnit], config: BatchConfig
) -> tuple[list[_RoomBatch], list[_BatchUnit]]:
    """Fill batches by room alone. ``first_fit`` passes over an item that does not fit and
    keeps filling with later, smaller ones; ``in_order`` closes at the first misfit.
    ``overflow: left_out`` makes one batch and returns the rest; otherwise the passed-over
    items fill the next batch, in order. An item over the whole budget (it could not be cut)
    takes a batch of its own, or is left out."""
    budget = config.size
    first_fit = config.fit == "first_fit"
    if config.overflow == "left_out":
        kept: list[_BatchUnit] = []
        out: list[_BatchUnit] = []
        room = budget
        closed = False
        for unit in units_:
            if not closed and unit.size <= room:
                kept.append(unit)
                room -= unit.size
                continue
            out.append(unit)
            closed = closed or not first_fit
        return ([_RoomBatch(kept)] if kept else []), out
    batches: list[_RoomBatch] = []
    remaining = units_
    while remaining:
        batch: list[_BatchUnit] = []
        rest: list[_BatchUnit] = []
        room = budget
        for unit in remaining:
            if not batch and unit.size > budget:
                batch.append(unit)
                room = 0
            elif unit.size <= room:
                batch.append(unit)
                room -= unit.size
            else:
                rest.append(unit)
        batches.append(_RoomBatch(batch, ended_by="budget" if rest else "end"))
        remaining = rest
    return batches, []


def _left_out_label(unit: _BatchUnit, label_path: str) -> str:
    if label_path:
        value, found = _key_of(unit.item, label_path)
        if found and value not in (None, ""):
            return str(value)
    return f"Item {unit.source_index}"


def _batch_label(units_: list[_BatchUnit], label_path: str, index: int) -> str:
    if label_path:
        labels = []
        for u in units_:
            value, found = _key_of(u.item, label_path)
            if found and value not in (None, ""):
                labels.append(str(value))
        if labels:
            first, last = labels[0], labels[-1]
            return first if first == last else f"{first} – {last}"
    return f"Part {index + 1}"


def _fold_groups(
    groups: list[list[tuple[list[_BatchUnit], int, str]]], ceiling: int
) -> tuple[list[list[tuple[list[_BatchUnit], int, str]]], str | None]:
    """Merge neighbouring batches so at most ``ceiling`` remain, never across a
    ``never_cross`` change. Each group gets a share of the ceiling by size."""
    note = None
    if len(groups) > ceiling:
        note = (
            f"{len(groups)} groups may not be merged across (never_cross), more than "
            f"max_batches={ceiling}; each group became one batch."
        )
        budgets = [1] * len(groups)
    else:
        group_sizes = [sum(u.size for units_, ov, _ in g for u in units_[ov:]) for g in groups]
        budgets = apportion(group_sizes, ceiling, min_each=1)
    folded: list[list[tuple[list[_BatchUnit], int, str]]] = []
    for group, budget in zip(groups, budgets, strict=True):
        out: list[tuple[list[_BatchUnit], int, str]] = []
        member_sizes = [sum(u.size for u in units_[ov:]) for units_, ov, _ in group]
        for span in fold_plan(len(group), min(len(group), budget), sizes=member_sizes):
            members = [group[i] for i in span]
            units_: list[_BatchUnit] = list(members[0][0])
            for member_units, member_overlap, _ in members[1:]:
                units_.extend(member_units[member_overlap:])
            out.append((units_, members[0][1], members[-1][2]))
        folded.append(out)
    return folded, note


# ---------------------------------------------------------------------------
# data.aggregate
# ---------------------------------------------------------------------------

AggregateOperation = Literal["count", "sum", "avg", "min", "max"]


class AggregateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[JsonValue] = Field(description="The list to summarize.")


class AggregateConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation: AggregateOperation = Field(
        description="What to compute: count, sum, avg, min, or max."
    )
    value_key: str = Field(
        default="",
        description=(
            "Path to the number to aggregate (e.g. 'score'). Leave empty to "
            "use the item itself. Ignored for 'count'."
        ),
    )
    group_by: str = Field(
        default="",
        description=(
            "Optional path to group by (e.g. 'category') — one result per "
            "distinct value instead of one overall result."
        ),
    )


class AggregateGroup(KindModel, kind="aggregate_group"):
    """One group's aggregate — a kind of its own, NESTED (the §4.4 law).

    ``data.aggregate`` can return many of these, and a repeated nested
    structure inside a kind is minted rather than smeared across the parent:
    a renderer lays out a self-describing row without knowing what produced
    it, and an edge can carry a single group as a value in its own right.
    """

    key: JsonValue = Field(description="The group's value at the group_by path.")
    result: JsonValue = Field(description="The aggregate for this group.")
    count: int = Field(description="How many items landed in this group.")


class AggregateOutput(KindModel, kind="aggregate_result"):
    operation: str = Field(description="The operation that was computed.")
    result: JsonValue = Field(
        default=None,
        description="The overall result (null when grouped — read groups instead).",
    )
    count: int = Field(description="How many items were considered.")
    skipped: int = Field(
        description="Items skipped because the value path was absent or not a number."
    )
    groups: list[AggregateGroup] = Field(
        default_factory=list,
        description="Per-group results when group_by is set (insertion order).",
    )


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    return None


def _compute(operation: str, values: list[float], total: int) -> JsonValue:
    if operation == "count":
        return total
    if not values:
        return None
    if operation == "sum":
        return sum(values)
    if operation == "avg":
        return sum(values) / len(values)
    if operation == "min":
        return min(values)
    return max(values)


class AggregateExecutor:
    """count / sum / avg / min / max over a key path, optionally grouped."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.aggregate",
        category=NodeCategory.DATA,
        display_name="Count & Total",
        description=(
            "Boil a list down to numbers — count items, or sum/average/"
            "min/max one of their values, overall or per group."
        ),
        input_schema=AggregateInput,
        input_kind="items",
        output_schema=AggregateOutput,
        config_schema=AggregateConfig,
        output_kind="aggregate_result",
        handles=_IO_HANDLES,
        determinism=ActionTier.PURE,
        icon="sigma",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: AggregateInput,
        config: AggregateConfig,
    ) -> NodeResult[AggregateOutput]:
        _ = ctx
        needs_values = config.operation != "count"
        skipped = 0

        if not config.group_by:
            values: list[float] = []
            considered = 0
            for item in inputs.items:
                if not needs_values:
                    considered += 1
                    continue
                raw, found = _key_of(item, config.value_key)
                number = _numeric(raw) if found else None
                if number is None:
                    skipped += 1
                    continue
                considered += 1
                values.append(number)
            return success(
                AggregateOutput(
                    operation=config.operation,
                    result=_compute(config.operation, values, considered),
                    count=considered,
                    skipped=skipped,
                )
            )

        grouped: dict[str, dict[str, Any]] = {}
        for item in inputs.items:
            group_raw, group_found = _key_of(item, config.group_by)
            if not group_found:
                skipped += 1
                continue
            number: float | None = None
            if needs_values:
                raw, found = _key_of(item, config.value_key)
                number = _numeric(raw) if found else None
                if number is None:
                    skipped += 1
                    continue
            bucket = grouped.setdefault(
                _identity(group_raw), {"key": group_raw, "values": [], "count": 0}
            )
            bucket["count"] += 1
            if number is not None:
                bucket["values"].append(number)

        groups = [
            AggregateGroup(
                key=bucket["key"],
                result=_compute(config.operation, bucket["values"], bucket["count"]),
                count=bucket["count"],
            )
            for bucket in grouped.values()
        ]
        considered = sum(g.count for g in groups)
        return success(
            AggregateOutput(
                operation=config.operation,
                result=None,
                count=considered,
                skipped=skipped,
                groups=groups,
            )
        )
