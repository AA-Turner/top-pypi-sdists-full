"""Kinds for the text-utility tool results.

Ledger rows (KIND_TOOL_LEDGER, agent ``lead-w2b``): ``text_analyze``
(``text_regex_extract`` is in the same file but REUSES the registered
``regex_extract_result`` kind — its model is matrx-graph's
``RegexExtractOutput``, so nothing is declared for it here; near-duplicate
slugs are a defect, NOMENCLATURE.md).

THE ANALYSIS MODES ARE ONE SHAPE, NOT FOUR. ``text_analyze`` has four modes
(summary / keywords / entities / language) that each emit a different subset of
keys, plus a ``message`` branch for an unknown mode. A KindModel is
``additionalProperties: false``, so the honest declaration is the UNION across
branches with every branch-only field optional (the ``fs_*`` union rule).
``analysis_type`` is always present and says which projection this is —
splitting the modes into four kinds would make one tool four identities.

All PLACEHOLDER tier: the counts and entity lists capture the tool's own
computation completely; nothing richer is being flattened away.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "word_frequency",
    label="Word Frequency",
    family="text_tools",
    example={"word": "platform", "count": 7},
    maturity="placeholder",
)
class WordFrequency(KindModel):
    """One word and how many times it appeared."""

    word: str = ""
    count: int = 0


@kind(
    "text_analysis",
    label="Text Analysis",
    family="text_tools",
    example={
        "analysis_type": "summary",
        "word_count": 120,
        "char_count": 741,
        "sentence_count": 9,
        "paragraph_count": 3,
    },
    maturity="placeholder",
)
class TextAnalysis(KindModel):
    """The result of one ``text_analyze`` call — a mode-specific projection.

    ``analysis_type`` names the mode; every other field is optional because it
    belongs to exactly one mode's branch:

    * ``summary`` — word/char/sentence/paragraph counts
    * ``keywords`` — ``keywords`` (top-20 stop-word-filtered frequencies)
    * ``entities`` — ``emails`` / ``urls`` / ``phones`` / ``dates``
    * ``language`` — char/word counts, ``unique_words``, ``avg_word_length``
    * unknown mode — ``message`` explains what is supported
    """

    analysis_type: str = ""
    # summary + language
    word_count: int | None = None
    char_count: int | None = None
    # summary only
    sentence_count: int | None = None
    paragraph_count: int | None = None
    # keywords only
    keywords: list[WordFrequency] | None = None
    # entities only — de-duplicated pattern hits, in no particular order.
    emails: list[str] | None = None
    urls: list[str] | None = None
    phones: list[str] | None = None
    dates: list[str] | None = None
    # language only
    unique_words: int | None = None
    avg_word_length: float | None = None
    # unknown-mode branch only
    message: str | None = None
