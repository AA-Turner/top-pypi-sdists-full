"""``text.similarity`` — how close a text (or each item) is to each candidate of a list.

Scores are 0–1, computed on the words of :func:`matrx_graph.text_match.words` — the same
folding as ``text.term_scan`` (NFKC + casefold); punctuation, apostrophes included, separates
words, so "don't" and "don’t" are the same words (the AI-visibility reference's rule):

- ``jaccard``: shared words / all distinct words of both.
- ``containment``: shared words / the candidate's words (how much of the candidate the text
  carries — "the question uses the buyer's words").
- ``max_jaccard_containment``: the larger of the two.
- ``char3_cosine``: cosine of character-3-gram counts over the words joined by single spaces
  (padded "  text ") — catches spelling and plural variants word sets miss.

A text or candidate with no words scores 0, and ``best`` is null when no candidate scores above
0. ``pairs`` (items mode) compares every item with every other (only within the same
``group_by`` value when set) and lists the pairs that pass ``threshold`` — or ANY of
``pair_methods`` (e.g. Jaccard 0.6 or char-3 0.85, the reference's rule). A NOMINATION for a
person or a later step; nothing is removed. A pair's score is the larger of its two directions.
"""

from __future__ import annotations

import collections
import json
import math
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.accessor import resolve_path
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.nodes.text.term_scan import text_at_path
from matrx_graph.text_match import words
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success

Method = Literal["jaccard", "containment", "max_jaccard_containment", "char3_cosine"]


class _Text:
    __slots__ = ("words", "grams")

    def __init__(self, text: str) -> None:
        tokens = words(text)
        self.words = frozenset(tokens)
        joined = " ".join(tokens)
        padded = f"  {joined} "
        self.grams = (
            collections.Counter(padded[i : i + 3] for i in range(len(padded) - 2)) if tokens else None
        )


def _score(text: _Text, cand: _Text, method: Method) -> float:
    if method == "char3_cosine":
        a, b = text.grams, cand.grams
        if not a or not b:
            return 0.0
        dot = sum(v * b.get(k, 0) for k, v in a.items())
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb)
    if not text.words or not cand.words:
        return 0.0
    shared = len(text.words & cand.words)
    jaccard = shared / len(text.words | cand.words)
    containment = shared / len(cand.words)
    if method == "jaccard":
        return jaccard
    if method == "containment":
        return containment
    return max(jaccard, containment)


class SimilarityInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str | None = Field(default=None, description="One text to compare. Use this or `items`.")
    items: list[JsonValue] | None = Field(
        default=None, description="A list to compare; each item's text is read at `text_path`."
    )
    candidates: list[JsonValue] = Field(
        default_factory=list, description="What to compare against: strings, or objects (text at `candidate_path`)."
    )


class PairRule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    method: Method = Field(description="How closeness is measured.")
    threshold: float = Field(ge=0, le=1, description="Lowest score that nominates a pair.")


class SimilarityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    method: Method = Field(default="max_jaccard_containment", description="How closeness is measured.")
    threshold: float | None = Field(
        default=None, ge=0, le=1, description="Lowest score that counts as a match. Empty = rank every candidate."
    )
    text_path: str = Field(default="", description="Items mode: where each item's text is. Empty = the item.")
    candidate_path: str = Field(default="", description="Where an object candidate's text is. Empty = the candidate.")
    pairs: bool = Field(default=False, description="Items mode: also list near-duplicate pairs within the list.")
    group_by: str = Field(default="", description="pairs: only compare items with the same value here (e.g. locale).")
    pair_methods: list[PairRule] | None = Field(
        default=None, description="pairs: nominate when ANY of these passes. Empty = `method` at `threshold`."
    )


class SimilarityMatch(KindSubModel):
    index: int = Field(description="Position of the candidate in `candidates`.")
    score: float = Field(description="0–1, rounded to 4 places.")
    candidate: JsonValue = Field(description="The candidate as given.")


class ItemSimilarity(KindSubModel):
    index: int = Field(description="Position of the item in `items`.")
    best: SimilarityMatch | None
    matches: list[SimilarityMatch]


class SimilarPair(KindSubModel):
    a: int = Field(description="Position of the first item.")
    b: int = Field(description="Position of the second item.")
    score: float = Field(description="The highest passing score.")
    scores: dict[str, float] = Field(description="The pair's score for each method checked.")
    nominated_by: list[str] = Field(description="The methods that passed.")


class SimilarityOutput(KindModel, kind="similarity_result"):
    best: SimilarityMatch | None = Field(description="Text mode: the closest candidate (first on a tie).")
    matches: list[SimilarityMatch] = Field(description="Text mode: candidates at or above threshold, closest first.")
    results: list[ItemSimilarity] = Field(description="Items mode: one entry per item, in order.")
    pairs: list[SimilarPair] = Field(description="Items mode with pairs: near-duplicate pairs, closest first.")
    method: Method
    threshold: float | None


def _rank(text: _Text, cands: list[tuple[JsonValue, _Text]], config: SimilarityConfig):
    scored = [(i, _score(text, c, config.method), raw) for i, (raw, c) in enumerate(cands)]
    best = None
    for i, s, raw in scored:
        if s > 0 and (best is None or s > best[1]):
            best = (i, s, raw)
    matches = sorted(
        (t for t in scored if config.threshold is None or t[1] >= config.threshold),
        key=lambda t: (-t[1], t[0]),
    )

    def as_match(t: tuple[int, float, JsonValue]) -> SimilarityMatch:
        return SimilarityMatch(index=t[0], score=round(t[1], 4), candidate=t[2])

    return (as_match(best) if best is not None else None), [as_match(t) for t in matches]


class SimilarityExecutor:
    """Score a text (or each item) against a list of candidates."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.similarity",
        category=NodeCategory.DATA,
        display_name="Compare Wording",
        description="Score how close a text is to each item of a list.",
        input_schema=SimilarityInput,
        output_schema=SimilarityOutput,
        output_kind="similarity_result",
        config_schema=SimilarityConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="git-compare",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SimilarityInput,
        config: SimilarityConfig,
    ) -> NodeResult[SimilarityOutput]:
        _ = ctx
        if (inputs.text is None) == (inputs.items is None):
            return failure(
                "invalid_input",
                "text.similarity: give either `text` (one text) or `items` (a list), not both and not neither.",
            )
        if config.pairs and inputs.items is None:
            return failure("invalid_config", "text.similarity: `pairs` compares items with each other; give `items`.")
        if config.pairs and config.threshold is None and not config.pair_methods:
            return failure(
                "invalid_config",
                "text.similarity: `pairs` needs a `threshold` (or `pair_methods`): the lowest score to list.",
            )

        def read(value: JsonValue, path: str, what: str, index: int) -> _Text | str:
            # A plain string is its own text even when a path is set for objects.
            text, problem = (value, None) if isinstance(value, str) else text_at_path(value, path)
            if problem is not None:
                return f"text.similarity: {what} {index} has {problem} at {path or 'the value itself'!r}."
            return _Text(text or "")

        cands: list[tuple[JsonValue, _Text]] = []
        for i, raw in enumerate(inputs.candidates):
            parsed = read(raw, config.candidate_path, "candidate", i)
            if isinstance(parsed, str):
                return failure("invalid_input", parsed)
            cands.append((raw, parsed))

        if inputs.text is not None:
            best, matches = _rank(_Text(inputs.text), cands, config)
            return success(SimilarityOutput(
                best=best, matches=matches, results=[], pairs=[], method=config.method, threshold=config.threshold,
            ))

        assert inputs.items is not None
        texts: list[_Text] = []
        for i, raw in enumerate(inputs.items):
            parsed = read(raw, config.text_path, "item", i)
            if isinstance(parsed, str):
                return failure("invalid_input", parsed)
            texts.append(parsed)
        results = []
        for i, text in enumerate(texts):
            best, matches = _rank(text, cands, config)
            results.append(ItemSimilarity(index=i, best=best, matches=matches))
        pairs: list[SimilarPair] = []
        if config.pairs:
            rules = config.pair_methods or [PairRule(method=config.method, threshold=config.threshold or 0.0)]
            groups: dict[str, list[int]] = {}
            for i, raw in enumerate(inputs.items):
                key = ""
                if config.group_by:
                    found = resolve_path(raw, config.group_by, unwrap_root=False).values
                    key = json.dumps(found, sort_keys=True, default=str)
                groups.setdefault(key, []).append(i)
            for members in groups.values():
                for xi, x in enumerate(members):
                    for y in members[xi + 1 :]:
                        scores: dict[str, float] = {}
                        passed: list[str] = []
                        best_pass = 0.0
                        for rule in rules:
                            s = max(_score(texts[x], texts[y], rule.method), _score(texts[y], texts[x], rule.method))
                            scores[rule.method] = round(s, 4)
                            if s >= rule.threshold:
                                passed.append(rule.method)
                                best_pass = max(best_pass, s)
                        if passed:
                            pairs.append(SimilarPair(
                                a=x, b=y, score=round(best_pass, 4), scores=scores, nominated_by=passed,
                            ))
            pairs.sort(key=lambda p: (-p.score, p.a, p.b))
        return success(SimilarityOutput(
            best=None, matches=[], results=results, pairs=pairs, method=config.method, threshold=config.threshold,
        ))
