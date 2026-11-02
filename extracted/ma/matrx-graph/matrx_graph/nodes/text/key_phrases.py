"""``text.key_phrases`` — the multi-word phrases each item's own words are built from.

RAKE-style: a phrase is a run of 1-4 content words between stop words and punctuation (a longer
run gives its 2- and 3-word windows); web addresses, file names, ids and snake_case names are
never phrases. Each item gets its distinct phrases written at ``terms_path`` — appended to a list
already there, so an entity pass's names and the mined phrases arrive as one term list for
``data.spread_rank`` (phrases are never ``backed``: the source did not name them itself).

Callers (Rule 3): knowledge buckets (spread candidates), a site's recurring themes across its
pages, a brand's repeated claims across sources, a person's recurring subjects in notes.

Words are lower-cased and a possessive ``'s`` is dropped; plurals are left as written —
``data.spread_rank`` folds them through the shared matcher. The stop-word list is scikit-learn's
English list (BSD-3, copied as data) plus conversational filler; ``extra_stop_words`` adds more.
Pure: the same items and settings always give the same phrases, in first-seen order.
"""

from __future__ import annotations

import re
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.accessor import resolve_path
from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success

_ENGLISH_STOP_WORDS = frozenset(
    """
a about above across after afterwards again against all almost alone along already also although
always am among amongst amoungst amount an and another any anyhow anyone anything anyway anywhere
are around as at back be became because become becomes becoming been before beforehand behind being
below beside besides between beyond bill both bottom but by call can cannot cant co con could
couldnt cry de describe detail do done down due during each eg eight either eleven else elsewhere
empty enough etc even ever every everyone everything everywhere except few fifteen fifty fill find
fire first five for former formerly forty found four from front full further get give go had has
hasnt have he hence her here hereafter hereby herein hereupon hers herself him himself his how
however hundred i ie if in inc indeed interest into is it its itself keep last latter latterly least
less ltd made many may me meanwhile might mill mine more moreover most mostly move much must my
myself name namely neither never nevertheless next nine no nobody none noone nor not nothing now
nowhere of off often on once one only onto or other others otherwise our ours ourselves out over own
part per perhaps please put rather re same see seem seemed seeming seems serious several she should
show side since sincere six sixty so some somehow someone something sometime sometimes somewhere
still such system take ten than that the their them themselves then thence there thereafter thereby
therefore therein thereupon these they thick thin third this those though three through throughout
thru thus to together too top toward towards twelve twenty two un under until up upon us very via
was we well were what whatever when whence whenever where whereafter whereas whereby wherein
whereupon wherever whether which while whither who whoever whole whom whose why will with within
without would yet you your yours yourself yourselves
""".split()
)

#: Conversational filler that is never a subject on its own.
_FILLER_WORDS = frozenset(
    """please want need make like just use using used also would could get got im dont let lets ok okay
yes thanks thank will going know think really thing things way well new sure see look good right now
should may might us our we you your i me my it's that's there's they're what's here's i'm i've you're
we're can't won't doesn't isn't aren't didn't don't let's etc via per vs eg ie one two three first
second next last today tomorrow yesterday time times day days week year years example examples
following follow above below based able actually basically really maybe probably quite pretty lot lots
kind sort bit stuff add added adding create created creating update updated updating change changes
changed fix fixed run running work working try trying make making give show tell say said ask asked
help find found keep put take set call called start started end done""".split()
)

STOP_WORDS = _ENGLISH_STOP_WORDS | _FILLER_WORDS

_SPLIT = re.compile(r"[\n\r\t.,;:!?()\[\]{}<>\"“”|=*#`~^/\\+]+|\s[-–—]\s|\s'|'\s")
_WORD = re.compile(r"^[A-Za-z][A-Za-z0-9&'-]*$")
_NOT_WORDS = re.compile(
    r"(https?://\S+|\S*/\S+|\S+@\S+|\S+\.(?:com|org|net|io|py|ts|tsx|js|json|md|html|css|sql)\b"
    r"|\b[0-9a-f]{8,}\b|\b\w*_\w+\b)"
)


def _word(raw: str) -> str:
    w = raw.lower().strip("'-")
    return w[:-2] if w.endswith("'s") else w


def mine_phrases(
    text: str, *, max_chars: int, min_words: int, max_words: int, stop_words: frozenset[str]
) -> list[str]:
    """The distinct phrases of ``text`` (first ``max_chars``), in first-seen order."""
    t = _NOT_WORDS.sub(" . ", text[:max_chars])
    out: dict[str, None] = {}
    for chunk in _SPLIT.split(t):
        run: list[str] = []
        for raw in [*chunk.split(), "the"]:
            if _WORD.match(raw) and raw.lower() not in stop_words and len(raw) > 1:
                run.append(raw)
                continue
            if 1 <= len(run) <= max_words:
                phrase = " ".join(_word(w) for w in run)
                if len(phrase) >= 4 and len(run) >= min_words:
                    out.setdefault(phrase, None)
            elif len(run) > max_words:
                for n in range(max(2, min_words), min(3, max_words) + 1):
                    for i in range(len(run) - n + 1):
                        out.setdefault(" ".join(_word(w) for w in run[i : i + n]), None)
            run = []
    return list(out)


class KeyPhrasesInput(KindModel, kind="key_phrases_request"):
    items: list[JsonValue] = Field(
        description="The items to read: plain texts, or records whose text sits at the step's paths."
    )


class KeyPhrasesConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text_paths: list[str] = Field(
        default_factory=lambda: ["text"],
        min_length=1,
        description="Where each record's text is (several: title and body are both read).",
    )
    terms_path: str = Field(
        default="terms",
        min_length=1,
        description="The field each record's phrases are written to (added to a list already there).",
    )
    max_chars: int = Field(
        default=40_000, ge=100, le=1_000_000, description="How much of each text is read."
    )
    min_words: int = Field(default=2, ge=1, le=4, description="Fewest words in a phrase.")
    max_words: int = Field(default=4, ge=1, le=4, description="Most words in a phrase.")
    extra_stop_words: list[str] = Field(
        default_factory=list, description="More words that never start, end or sit in a phrase."
    )
    ignore_phrases: list[str] = Field(
        default_factory=list, description="Phrases never returned (matched lower-cased)."
    )


class KeyPhrasesOutput(KindModel, kind="key_phrases_result"):
    items: list[JsonValue] = Field(
        description="Every item in order; a record carries its phrases at terms_path, a plain text becomes {text, terms}."
    )
    item_count: int = Field(description="Items read.")
    phrase_count: int = Field(description="Distinct phrases across all items.")
    empty_items: list[int] = Field(description="Positions of items with no text at any path.")


class KeyPhrasesExecutor:
    """Mine each item's multi-word phrases."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.key_phrases",
        category=NodeCategory.DATA,
        display_name="Find Key Phrases",
        description="Find the multi-word phrases each item is written in and add them to its terms.",
        input_schema=KeyPhrasesInput,
        input_kind="key_phrases_request",
        output_schema=KeyPhrasesOutput,
        config_schema=KeyPhrasesConfig,
        output_kind="key_phrases_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="quote",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: KeyPhrasesInput,
        config: KeyPhrasesConfig,
    ) -> NodeResult[KeyPhrasesOutput]:
        if config.min_words > config.max_words:
            return failure(
                "invalid_config",
                f"min_words ({config.min_words}) is more than max_words ({config.max_words}).",
            )
        if "." in config.terms_path or "[" in config.terms_path:
            return failure(
                "invalid_config",
                f"terms_path '{config.terms_path}' must be one field name, not a path.",
            )
        stop = STOP_WORDS | {w.lower() for w in config.extra_stop_words}
        ignore = {p.strip().lower() for p in config.ignore_phrases}
        out_items: list[JsonValue] = []
        empty: list[int] = []
        distinct: set[str] = set()
        for position, item in enumerate(inputs.items):
            if isinstance(item, str):
                texts = [item]
            elif isinstance(item, dict):
                texts = []
                for path in config.text_paths:
                    for value in resolve_path(item, path).values:
                        if isinstance(value, str):
                            texts.append(value)
                        elif value is not None:
                            return failure(
                                "text_not_a_string",
                                f"Item {position} has a '{path}' that is not text.",
                            )
            elif item is None:
                texts = []
            else:
                return failure(
                    "item_not_text", f"Item {position} is neither text nor a record."
                )
            if not any(t.strip() for t in texts):
                empty.append(position)
            phrases: dict[str, None] = {}
            for text in texts:
                for p in mine_phrases(
                    text,
                    max_chars=config.max_chars,
                    min_words=config.min_words,
                    max_words=config.max_words,
                    stop_words=stop,
                ):
                    if p not in ignore:
                        phrases.setdefault(p, None)
            distinct.update(phrases)
            if isinstance(item, dict):
                before = item.get(config.terms_path)
                if before is not None and not isinstance(before, list):
                    return failure(
                        "terms_not_a_list",
                        f"Item {position} has a '{config.terms_path}' that is not a list.",
                    )
                out_items.append({**item, config.terms_path: [*(before or []), *phrases]})
            else:
                out_items.append({"text": item or "", config.terms_path: list(phrases)})
        return success(
            KeyPhrasesOutput(
                items=out_items,
                item_count=len(inputs.items),
                phrase_count=len(distinct),
                empty_items=empty,
            )
        )
