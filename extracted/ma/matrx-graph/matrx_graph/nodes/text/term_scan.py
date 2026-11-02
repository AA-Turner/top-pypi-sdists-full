"""``text.term_scan`` — does a text (or each item of a list) contain any term of a list.

One generic primitive for every "never say / must flag" list: a brand's never-say list over a
blind brief, a style guide's banned words, privileged terms in documents, names to redact.
Matching is THE shared matcher, :mod:`matrx_graph.text_match` (``data.check_items``
``not_contains`` uses the same one): folded (NFKC + casefold, whole words, run-together names,
symbols kept, web addresses as their host) or exact. A fuzzy near miss is reported under
``fuzzy`` for a person to review — never a hit, never unclean.

A step that cannot really look is never "clean": an item with no text at ``text_path``, or a
term list with no usable term left after the ``classes`` filter, fails the step with a
sentence naming the path or the classes. An EMPTY term list is a real answer (nothing to find)
and passes clean.

A name that is also an everyday word ("Render", "Notion", "Apple") is matched only where it
reads as a proper name when the term says ``match: "proper_name_only"`` or ``everyday_words``
marks it (``auto``: every one-word dictionary-word term; a list: those terms). "Render times got
slow" is clean; "Rendering in Render is slow" is a hit. The rules:
:mod:`matrx_utils.proper_names`.

Positions (``start``/``end``) index the ORIGINAL text, so ``text[start:end]`` is what matched.
"""

from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.accessor import resolve_path
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.text_match import FuzzyRule, Match, TermMatcher, TermMode
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


def text_at_path(item: JsonValue, path: str) -> tuple[str | None, str | None]:
    """(text, problem) for ``path`` on ``item``; empty path = the item itself.

    A missing or null value is ``(None, None)``. A list of strings is joined with spaces.
    Anything else that is not a string or number is a problem.
    """
    if path:
        values = resolve_path(item, path, unwrap_root=False).values
        value: Any = values[0] if len(values) == 1 else (values or None)
    else:
        value = item
    if value is None:
        return None, None
    if isinstance(value, str):
        return value, None
    if isinstance(value, bool) or not isinstance(value, int | float | list):
        return None, f"a {type(value).__name__}, not text"
    if isinstance(value, list):
        if not all(isinstance(v, str) for v in value):
            return None, "a list that is not all text"
        return " ".join(value), None
    return str(value), None


class ScanTerm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    term: str = Field(description="The word or phrase to look for.")
    term_class: str | None = Field(
        default=None,
        validation_alias=AliasChoices("term_class", "class"),
        description="Optional group the term belongs to (e.g. brands). `class` is accepted too.",
    )
    match: TermMode | None = Field(
        default=None,
        description="proper_name_only: count it only where written as a name ('Render vs X', not "
        "'render times'). any: every occurrence. Unset: `everyday_words` decides.",
    )


class TermScanInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str | None = Field(default=None, description="One text to scan. Use this or `items`.")
    items: list[JsonValue] | None = Field(
        default=None, description="A list to scan; each item's text is read at `text_path`."
    )
    terms: list[str | ScanTerm] = Field(
        description="Terms to find: strings, or {term, term_class, match} objects.",
    )


class FuzzySettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = Field(default=False, description="Also report near-miss spellings for review.")
    min_token_length: int = Field(
        default=7, ge=3, le=40, description="Shortest one-word term that is checked for near misses."
    )
    ratio: float = Field(default=0.86, gt=0, le=1, description="How close a spelling must be (0–1).")


class TermScanConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    match: Literal["folded", "exact"] = Field(
        default="folded",
        description="folded: ignore case, width and spacing (accents kept); exact: as written.",
    )
    strip_accents: bool = Field(default=False, description="folded only: also treat é as e.")
    strip_html: bool = Field(default=False, description="folded only: read HTML as its visible text.")
    fuzzy: FuzzySettings = Field(default_factory=FuzzySettings)
    classes: list[str] | None = Field(
        default=None, description="Only use terms of these classes. Empty = every term."
    )
    everyday_words: Literal["auto", "none"] | list[str] = Field(
        default="none",
        description="Terms matched only as a proper name: auto = every one-word term that is a "
        "dictionary word (Render, Apple); a list = these terms; none = only terms that say so.",
    )
    text_path: str = Field(
        default="", description="Items mode: where each item's text is (e.g. brief.text). Empty = the item."
    )


class TermHit(KindSubModel):
    term: str = Field(description="The term as given.")
    term_class: str | None = Field(description="The term's class, when it had one.")
    start: int = Field(description="Where the match starts in the text.")
    end: int = Field(description="Where the match ends in the text.")
    matched_text: str = Field(description="The text that matched.")
    kind: Literal["words", "compact", "symbols", "exact", "fuzzy"] = Field(description="How it matched.")


class FuzzyHit(TermHit):
    ratio: float = Field(description="How close the spelling is (0–1).")


class ItemScan(KindSubModel):
    index: int = Field(description="Position of the item in `items`.")
    item: JsonValue = Field(description="The item as given.")
    hits: list[TermHit]
    fuzzy: list[FuzzyHit]
    clean: bool = Field(description="True when no term was found.")


class TermScanOutput(KindModel, kind="term_scan_result"):
    hits: list[TermHit] = Field(description="Text mode: every term found.")
    fuzzy: list[FuzzyHit] = Field(description="Text mode: near misses to review (not hits).")
    clean: bool = Field(description="True when no term was found (in any item).")
    needs_review: bool = Field(description="True when any near miss was reported.")
    hit_count: int
    fuzzy_count: int
    term_count: int = Field(description="Terms used after the classes filter.")
    skipped_terms: list[str] = Field(description="Terms with no letters or digits, never matched.")
    results: list[ItemScan] = Field(description="Items mode: one entry per item, in order.")
    clean_items: list[JsonValue] = Field(description="Items mode: items with no term found.")
    flagged_items: list[JsonValue] = Field(description="Items mode: items with a term found.")
    clean_count: int
    flagged_count: int


def _hit(m: Match) -> TermHit:
    return TermHit(
        term=m.term, term_class=m.term_class, start=m.start, end=m.end, matched_text=m.matched_text, kind=m.kind
    )


def _near(m: Match) -> FuzzyHit:
    return FuzzyHit(
        term=m.term, term_class=m.term_class, start=m.start, end=m.end, matched_text=m.matched_text,
        kind=m.kind, ratio=m.ratio or 0.0,
    )


class TermScanExecutor:
    """Find every term of a list in a text or in each item of a list."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.term_scan",
        category=NodeCategory.DATA,
        display_name="Find Terms",
        description="Find words or phrases from a list in a text or in each item.",
        input_schema=TermScanInput,
        output_schema=TermScanOutput,
        output_kind="term_scan_result",
        config_schema=TermScanConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="scan-search",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: TermScanInput,
        config: TermScanConfig,
    ) -> NodeResult[TermScanOutput]:
        _ = ctx
        if (inputs.text is None) == (inputs.items is None):
            return failure(
                "invalid_input",
                "text.term_scan: give either `text` (one text) or `items` (a list), not both and not neither.",
            )
        pairs = [(t, None, None) if isinstance(t, str) else (t.term, t.term_class, t.match) for t in inputs.terms]
        given = [p for p in pairs if p[0].strip()]
        if config.classes:
            wanted = set(config.classes)
            given = [p for p in given if p[1] in wanted]
        fz = config.fuzzy
        matcher = TermMatcher(
            given,
            mode=config.match,
            strip_accents=config.strip_accents,
            strip_html=config.strip_html,
            fuzzy=FuzzyRule(fz.ratio, fz.min_token_length, fz.min_token_length - 1) if fz.enabled else None,
            everyday_words=config.everyday_words,
        )
        if inputs.terms and not matcher.terms:
            why = (
                f"none of the {len(inputs.terms)} terms has a class in {config.classes}"
                if config.classes and not given
                else "no term has a letter or digit in it"
            )
            return failure(
                "invalid_input",
                f"text.term_scan: nothing to look for — {why}, so no text could be checked. "
                "Fix the term list or the classes filter.",
            )
        empty: dict[str, Any] = {
            "hits": [], "fuzzy": [], "results": [], "clean_items": [], "flagged_items": [],
            "clean_count": 0, "flagged_count": 0, "term_count": len(matcher.terms),
            "skipped_terms": matcher.skipped,
        }
        if inputs.text is not None:
            hits, near = matcher.scan(inputs.text)
            return success(TermScanOutput(**{
                **empty, "hits": [_hit(m) for m in hits], "fuzzy": [_near(m) for m in near],
                "clean": not hits, "needs_review": bool(near), "hit_count": len(hits), "fuzzy_count": len(near),
            }))
        results: list[ItemScan] = []
        assert inputs.items is not None
        where = config.text_path or "the item itself"
        for index, item in enumerate(inputs.items):
            text, problem = text_at_path(item, config.text_path)
            if problem is not None or text is None:
                return failure(
                    "invalid_input",
                    f"text.term_scan: item {index} has {problem or 'no text'} at {where!r}, so it "
                    "could not be checked. Point `text_path` at the text.",
                )
            hits, near = matcher.scan(text)
            results.append(ItemScan(
                index=index, item=item, hits=[_hit(m) for m in hits], fuzzy=[_near(m) for m in near], clean=not hits,
            ))
        clean_items = [r.item for r in results if r.clean]
        flagged_items = [r.item for r in results if not r.clean]
        return success(TermScanOutput(**{
            **empty,
            "results": results,
            "clean_items": clean_items,
            "flagged_items": flagged_items,
            "clean_count": len(clean_items),
            "flagged_count": len(flagged_items),
            "clean": not flagged_items,
            "needs_review": any(r.fuzzy for r in results),
            "hit_count": sum(len(r.hits) for r in results),
            "fuzzy_count": sum(len(r.fuzzy) for r in results),
        }))
