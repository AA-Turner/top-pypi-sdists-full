"""``data.spread_rank`` — rank terms by how WIDELY they spread, never by how often they repeat.

Each item has a home (the place it lives: a note, a chat, a page, an outlet), a kind (notes,
chats, files; blog, docs; news, blogs), an optional date and the terms found in it. A term is
scored by the distinct homes it appears in, per kind, and the distinct ISO weeks it spans; many
mentions inside one home count once:

    score = (0.5 + backed_share) x sum over kinds of log(1 + homes in that kind) x log(1 + weeks)

``backed_share`` = homes where the term arrived ``backed`` (named by the source itself — an entity
pass, a tag, a headline) / homes it appears in. When NO item carries a date the weeks factor is 1,
so undated inputs (a site's pages) still rank.

Settings (each one on the step, else the ``workflow.spread_rank`` knob row; ``settings_from`` says
which): ``min_homes`` (relative to the input with ``min_homes_share`` / ``min_homes_floor``), the
filler cap (``filler_home_share`` of all homes, never below ``filler_cap_min_homes``; a term
``backed`` in ``backed_share`` of its homes or ``backed_home_share`` of all homes escapes it),
``longer_phrase_cover`` (a longer phrase covering that share of a shorter one's homes replaces it),
``fold_variants`` (plural spellings and same-head phrase variants of 3+ words — "sensory garden
herbs" / "sensory garden plan" -> "sensory garden" — fold into one term, each variant kept as an
alias; a variant must itself reach ``variant_min_homes``) and ``top_n``. ``filler_terms`` are never
terms. Terms meet on :func:`matrx_graph.text_match.term_key` and plurals on
:func:`matrx_graph.text_match.plural_forms` — the shared matcher's own folding, never a copy.

Pure: the same items and settings always give the same ranking (ties: more homes, then the key).
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from datetime import date, datetime
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph import knobs
from matrx_graph.content_ir.accessor import resolve_path
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.text_match import plural_forms, term_key
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


class SpreadRankInput(KindModel, kind="spread_rank_request"):
    items: list[JsonValue] = Field(
        description=(
            "One record per item: its home, kind, date and terms sit at the step's paths. A term is "
            "a string or {term, backed}."
        )
    )


class SpreadRankConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    home_path: str = Field(
        default="home", min_length=1, description="Where each item's home is (e.g. 'note_id')."
    )
    kind_path: str = Field(
        default="kind", description="Where each item's kind is. Empty: every item is one kind."
    )
    date_path: str = Field(
        default="date", description="Where each item's date is (ISO). Empty: no dates."
    )
    terms_path: str = Field(
        default="terms", min_length=1, description="Where each item's list of terms is."
    )
    filler_terms: list[str] = Field(
        default_factory=list, description="Terms that are never a topic."
    )
    unscored_kinds: list[str] = Field(
        default_factory=list, description="Kinds whose homes count as places but add no score."
    )
    min_homes: int | None = Field(
        default=None, ge=1, le=100_000, description="Fewest homes a term needs."
    )
    min_homes_share: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Fewest homes as a share of all homes (0: fixed min_homes).",
    )
    min_homes_floor: int | None = Field(
        default=None, ge=1, le=100_000, description="The share never asks below this."
    )
    filler_home_share: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="A term in more than this share of all homes is filler.",
    )
    filler_cap_min_homes: int | None = Field(
        default=None,
        ge=0,
        le=10_000_000,
        description="The filler cap never falls below this many homes.",
    )
    backed_share: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Backed in this share of its homes escapes the filler cap.",
    )
    backed_home_share: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Backed in this share of ALL homes escapes the filler cap.",
    )
    longer_phrase_cover: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="A longer phrase covering this share of a shorter one's homes replaces it.",
    )
    fold_variants: bool | None = Field(
        default=None, description="Fold plurals and same-head phrase variants."
    )
    variant_min_homes: int | None = Field(
        default=None, ge=1, le=100_000, description="A variant must reach this many homes to fold."
    )
    top_n: int | None = Field(
        default=None, ge=1, le=100_000, description="How many ranked terms to return."
    )


_SETTING_KEYS = (
    "min_homes",
    "min_homes_share",
    "min_homes_floor",
    "filler_home_share",
    "filler_cap_min_homes",
    "backed_share",
    "backed_home_share",
    "longer_phrase_cover",
    "fold_variants",
    "variant_min_homes",
    "top_n",
)


class SpreadRankSettings(KindSubModel):
    min_homes: int
    min_homes_share: float
    min_homes_floor: int
    filler_home_share: float
    filler_cap_min_homes: int
    backed_share: float
    backed_home_share: float
    longer_phrase_cover: float
    fold_variants: bool
    variant_min_homes: int
    top_n: int


class SpreadTerm(KindSubModel):
    key: str = Field(description="The folded term the spellings meet on.")
    term: str = Field(description="Its most used spelling.")
    homes: int = Field(description="Distinct homes it appears in.")
    by_kind: dict[str, int] = Field(description="Distinct homes per kind.")
    weeks: int = Field(description="Distinct ISO weeks it spans.")
    score: float = Field(description="The spread score, best first.")
    backed_share: float = Field(description="Share of its homes where it arrived backed.")
    aliases: list[str] = Field(description="Variant keys folded into it, most homes first.")
    items: list[int] = Field(description="Positions of the items it appears in.")


class SpreadDropped(KindSubModel):
    filler_terms: int = Field(description="Mentions of a listed filler term.")
    below_min_homes: int = Field(description="Terms in fewer homes than the minimum.")
    filler_cap: int = Field(description="Terms spread so wide they are filler.")
    longer_phrase: int = Field(description="Terms replaced by a longer phrase covering them.")
    past_top_n: int = Field(description="Ranked terms past top_n.")


class SpreadRankOutput(KindModel, kind="spread_ranking"):
    terms: list[SpreadTerm] = Field(description="Ranked terms, best spread first.")
    item_count: int
    home_count: int
    candidate_count: int = Field(description="Distinct terms seen (after folding).")
    min_homes_used: int = Field(description="The minimum homes this input asked of a term.")
    filler_cap_homes: float = Field(description="Above this many homes an unbacked term is filler.")
    dated: bool = Field(description="True when any item carried a date (weeks count).")
    dropped: SpreadDropped
    settings: SpreadRankSettings
    settings_from: dict[str, Literal["step", "knob"]] = Field(
        description="Where each setting came from."
    )


class _Refused(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _one(item: JsonValue, path: str, index: int, what: str) -> Any:
    found = resolve_path(item, path, unwrap_root=False).values
    if not found:
        return None
    if len(found) != 1:
        raise _Refused(
            f"{what}_ambiguous", f"Item {index} has {len(found)} values at '{path}' for its {what}."
        )
    return found[0]


def _week(raw: Any, index: int, path: str) -> tuple[int, int] | None:
    if raw is None or raw == "":
        return None
    if isinstance(raw, datetime | date):
        day = raw
    elif isinstance(raw, str):
        try:
            day = datetime.fromisoformat(raw.strip())
        except ValueError:
            try:
                day = date.fromisoformat(raw.strip()[:10])
            except ValueError:
                raise _Refused(
                    "date_unreadable",
                    f"Item {index}'s date at '{path}' is {raw!r}, not an ISO date.",
                ) from None
    else:
        raise _Refused(
            "date_unreadable", f"Item {index}'s date at '{path}' is {raw!r}, not an ISO date."
        )
    iso = day.isocalendar()
    return (iso[0], iso[1])


def _terms(raw: Any, index: int, path: str) -> list[tuple[str, bool]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise _Refused(
            "terms_not_a_list",
            f"Item {index}'s terms at '{path}' are {type(raw).__name__}, not a list.",
        )
    out: list[tuple[str, bool]] = []
    for n, t in enumerate(raw):
        if isinstance(t, str):
            out.append((t, False))
        elif isinstance(t, dict) and isinstance(t.get("term"), str):
            out.append((t["term"], bool(t.get("backed"))))
        else:
            raise _Refused(
                "term_unreadable",
                f"Item {index}'s term {n} is {t!r}: give a string or {{term, backed}}.",
            )
    return out


def _resolve(
    config: SpreadRankConfig, live: knobs.SpreadRankKnobs
) -> tuple[SpreadRankSettings, dict[str, str]]:
    values: dict[str, Any] = {}
    source: dict[str, str] = {}
    for key in _SETTING_KEYS:
        mine = getattr(config, key)
        values[key], source[key] = (
            (mine, "step") if mine is not None else (getattr(live, key), "knob")
        )
    return SpreadRankSettings(**values), source


class _Pool:
    """Every term's mentions, keyed on the folded term."""

    def __init__(self) -> None:
        self.mentions: dict[str, set[int]] = defaultdict(set)
        self.backed: dict[str, set[int]] = defaultdict(set)
        self.spelling: dict[str, Counter[str]] = defaultdict(Counter)
        self.aliases: dict[str, set[str]] = defaultdict(set)
        #: Homes each folded variant had on its own (orders the aliases).
        self.alias_homes: dict[str, int] = {}

    def fold(self, variant: str, into: str, homes: list[str]) -> None:
        self.alias_homes[variant] = len({homes[i] for i in self.mentions[variant]})
        self.mentions[into] |= self.mentions.pop(variant)
        self.backed[into] |= self.backed.pop(variant, set())
        self.spelling[into].update(self.spelling.pop(variant, Counter()))
        self.aliases[into] |= {variant} | self.aliases.pop(variant, set())


def _homes(pool: _Pool, key: str, homes: list[str]) -> set[str]:
    return {homes[i] for i in pool.mentions[key]}


def _fold_plurals(pool: _Pool, homes: list[str]) -> None:
    """``garden plans`` folds into ``garden plan`` when both are terms (the matcher's plural rule)."""
    for base in sorted(pool.mentions, key=lambda k: (len(k), k)):
        if base not in pool.mentions:
            continue
        words = base.split()
        for form in plural_forms(words[-1])[1:]:
            variant = " ".join([*words[:-1], form])
            if variant != base and variant in pool.mentions:
                pool.fold(variant, base, homes)


def _fold_heads(
    pool: _Pool, homes: list[str], settings: SpreadRankSettings, filler: set[str]
) -> None:
    """Unbacked phrases of 3+ words differing only in their last word fold into the shared head
    (at least two variants, each in ``variant_min_homes`` homes); longest heads first."""
    by_head: dict[str, list[str]] = defaultdict(list)
    for k in sorted(pool.mentions):
        words = k.split()
        if (
            len(words) < 3
            or pool.backed.get(k)
            or len(_homes(pool, k, homes)) < settings.variant_min_homes
        ):
            continue
        head = " ".join(words[:-1])
        if head not in filler:
            by_head[head].append(k)
    for head in sorted(by_head, key=lambda h: (-len(h.split()), h)):
        variants = [v for v in by_head[head] if v in pool.mentions and v != head]
        if len(variants) < 2:
            continue
        pool.mentions.setdefault(head, set())
        for v in variants:
            pool.fold(v, head, homes)


def rank_spread(
    items: list[JsonValue],
    config: SpreadRankConfig,
    settings: SpreadRankSettings,
    settings_from: dict[str, str],
) -> SpreadRankOutput:
    """The pure ranker behind ``data.spread_rank`` (tested without an engine)."""
    filler = {term_key(t) for t in config.filler_terms} - {""}
    unscored = set(config.unscored_kinds)
    homes: list[str] = []
    kinds: list[str] = []
    weeks: list[tuple[int, int] | None] = []
    pool = _Pool()
    filler_hits = 0
    for i, item in enumerate(items):
        home = _one(item, config.home_path, i, "home")
        if home is None or home == "":
            raise _Refused("home_missing", f"Item {i} has no home at '{config.home_path}'.")
        homes.append(str(home))
        kind = _one(item, config.kind_path, i, "kind") if config.kind_path else "all"
        if kind is None or kind == "":
            raise _Refused(
                "kind_missing",
                f"Item {i} has no kind at '{config.kind_path}' (empty the path for one kind).",
            )
        kinds.append(str(kind))
        weeks.append(
            _week(_one(item, config.date_path, i, "date"), i, config.date_path)
            if config.date_path
            else None
        )
        for raw, backed in _terms(_one(item, config.terms_path, i, "terms"), i, config.terms_path):
            k = term_key(raw)
            if not k:
                continue
            if k in filler:
                filler_hits += 1
                continue
            pool.mentions[k].add(i)
            if backed:
                pool.backed[k].add(i)
            pool.spelling[k][raw.strip()] += 1

    if settings.fold_variants:
        _fold_plurals(pool, homes)
        _fold_heads(pool, homes, settings, filler)

    n_homes = len(set(homes))
    min_homes = settings.min_homes
    if settings.min_homes_share > 0:
        min_homes = max(
            settings.min_homes_floor,
            min(settings.min_homes, math.ceil(settings.min_homes_share * n_homes)),
        )
    cap = max(settings.filler_home_share * n_homes, settings.filler_cap_min_homes)
    dated = any(w is not None for w in weeks)
    dropped = Counter[str]()

    rows: list[SpreadTerm] = []
    for k in sorted(pool.mentions):
        idx = pool.mentions[k]
        term_homes = {homes[i] for i in idx}
        if len(term_homes) < min_homes:
            dropped["below_min_homes"] += 1
            continue
        backed_homes = {homes[i] for i in pool.backed.get(k, set())}
        share = len(backed_homes) / len(term_homes)
        if (
            len(term_homes) > cap
            and share < settings.backed_share
            and len(backed_homes) < settings.backed_home_share * n_homes
        ):
            dropped["filler_cap"] += 1
            continue
        by_kind: dict[str, set[str]] = defaultdict(set)
        for i in idx:
            by_kind[kinds[i]].add(homes[i])
        n_weeks = len({weeks[i] for i in idx} - {None})
        spread = sum(math.log(1 + len(v)) for g, v in by_kind.items() if g not in unscored)
        score = (0.5 + share) * spread * (math.log(1 + n_weeks) if dated else 1.0)
        spellings = sorted(pool.spelling[k].items(), key=lambda kv: (-kv[1], kv[0]))
        alias_homes = {a: pool.alias_homes.get(a, 0) for a in pool.aliases.get(k, ())}
        rows.append(
            SpreadTerm(
                key=k,
                term=spellings[0][0] if spellings else k,
                homes=len(term_homes),
                by_kind={g: len(v) for g, v in sorted(by_kind.items())},
                weeks=n_weeks,
                score=round(score, 4),
                backed_share=round(share, 4),
                aliases=sorted(alias_homes, key=lambda a: (-alias_homes[a], a)),
                items=sorted(idx),
            )
        )
    rows.sort(key=lambda r: (-r.score, -r.homes, r.key))
    kept = _keep_longer(rows, settings.longer_phrase_cover)
    dropped["longer_phrase"] = len(rows) - len(kept)
    dropped["past_top_n"] = max(0, len(kept) - settings.top_n)
    return SpreadRankOutput(
        terms=kept[: settings.top_n],
        item_count=len(items),
        home_count=n_homes,
        candidate_count=len(pool.mentions),
        min_homes_used=min_homes,
        filler_cap_homes=round(cap, 4),
        dated=dated,
        dropped=SpreadDropped(
            filler_terms=filler_hits,
            below_min_homes=dropped["below_min_homes"],
            filler_cap=dropped["filler_cap"],
            longer_phrase=dropped["longer_phrase"],
            past_top_n=dropped["past_top_n"],
        ),
        settings=settings,
        settings_from=settings_from,  # type: ignore[arg-type]
    )


def _keep_longer(rows: list[SpreadTerm], cover: float) -> list[SpreadTerm]:
    """Drop a term when a longer phrase containing it covers at least ``cover`` of its homes."""
    by_word: dict[str, list[SpreadTerm]] = defaultdict(list)
    for r in rows:
        if " " in r.key:
            for w in set(r.key.split()):
                by_word[w].append(r)
    keep: list[SpreadTerm] = []
    for r in rows:
        padded = f" {r.key} "
        if any(
            q.key != r.key
            and len(q.key) > len(r.key)
            and padded in f" {q.key} "
            and q.homes >= cover * r.homes
            for q in by_word.get(r.key.split()[0], ())
        ):
            continue
        keep.append(r)
    return keep


class SpreadRankExecutor:
    """Rank terms by distinct homes per kind and weeks, with a filler cap and variant folding."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.spread_rank",
        category=NodeCategory.DATA,
        display_name="Rank by Spread",
        description=(
            "Rank terms by how many separate places, kinds and weeks they appear in — not how often. "
            "Drops filler, folds plurals and phrase variants."
        ),
        input_schema=SpreadRankInput,
        input_kind="spread_rank_request",
        output_schema=SpreadRankOutput,
        output_kind="spread_ranking",
        config_schema=SpreadRankConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="bar-chart-3",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SpreadRankInput,
        config: SpreadRankConfig,
    ) -> NodeResult[SpreadRankOutput]:
        _ = ctx
        settings, source = _resolve(config, await knobs.spread_rank_knobs())
        try:
            return success(rank_spread(inputs.items, config, settings, source))
        except _Refused as refused:
            return failure(refused.code, f"data.spread_rank: {refused}")


__all__ = [
    "SpreadDropped",
    "SpreadRankConfig",
    "SpreadRankExecutor",
    "SpreadRankInput",
    "SpreadRankOutput",
    "SpreadRankSettings",
    "SpreadTerm",
    "rank_spread",
]
