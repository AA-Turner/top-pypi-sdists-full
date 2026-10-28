"""The one name matcher: a name that is also an everyday word counts only as a proper name.

Every place that asks "does this text name the company or a competitor?" goes through here —
the blinding check (``ai_visibility_design.scan_text``), answer mentions
(``providers.dataforseo.ai_answers.answer_mentions_target``) and coverage
(``coverage.term_hits``). "Stream", "Workers", "Render", "Remote", "Square" are names only when
written as names; the ordinary word is never a mention and never a leak.

The dictionary and the cue rules live ONCE in :mod:`matrx_utils.proper_names` (also used by
``matrx_graph.text_match``); this module feeds them the live knob lists.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from collections.abc import Callable, Iterable
from typing import Any

# A module import (not ``from``): the floor guard reads ``from`` imports against PUBLISHED tags, and
# proper_names ships in the next matrx-utils release, whose bump refreshes this package's floor.
import matrx_utils.proper_names as _shared

LIST_MARKER_BEFORE = _shared.LIST_MARKER_BEFORE
NAME_CONTEXT = _shared.NAME_CONTEXT
NAME_CONTEXT_BEFORE = _shared.NAME_CONTEXT_BEFORE
common_english_words = _shared.common_english_words
everyday_word_terms = _shared.everyday_word_terms
is_word = _shared.is_word
reads_as_proper_name = _shared.reads_as_proper_name

__all__ = [
    "LIST_MARKER_BEFORE",
    "NAME_CONTEXT",
    "NAME_CONTEXT_BEFORE",
    "NAME_PRODUCT_CONTEXT_WORDS",
    "NAME_VERB_CUES",
    "common_english_words",
    "common_word_names",
    "configure_name_context_words",
    "configure_name_verb_cues",
    "is_flagged",
    "is_word",
    "name_context_words",
    "name_verb_cues",
    "proper_name_match",
]

logger = logging.getLogger(__name__)


def common_word_names(terms: Iterable[Any]) -> list[str]:
    """The names that are also an everyday word ("Render", "Remote", "Workers", "Stream") — THE
    shared rule, :func:`matrx_utils.proper_names.everyday_word_terms`."""
    return everyday_word_terms(terms)


#: Verbs that, right after a capitalised everyday word opening a sentence or list item, mark it as
#: a name ("Render offers …", "Acme is one option"). The SEED of platform.feature_knob
#: "seo.name_matching" "name_verb_cues" (aidream migration 1530). The live list is the knob row,
#: handed in by the host through :func:`configure_name_verb_cues`; see :func:`name_verb_cues`.
NAME_VERB_CUES: tuple[str, ...] = _shared.NAME_VERB_CUES

#: The host's live source for the verb cues (a synchronous read of the knob row from its process
#: cache). Unset — a standalone install, or a test — means the seed above, announced once.
_verb_cue_source: Callable[[], Iterable[str]] | None = None
_announced: set[str] = set()


def configure_name_verb_cues(source: Callable[[], Iterable[str]] | None) -> None:
    """Install the host's live reader of the ``seo.name_matching.name_verb_cues`` knob (None clears)."""
    global _verb_cue_source
    _verb_cue_source = source
    _announced.clear()


def _announce(kind: str, message: str) -> None:
    if kind not in _announced:
        _announced.add(kind)
        logger.warning(message)


def name_verb_cues() -> tuple[str, ...]:
    """The verb cues in force now: the host's knob row, or — announced — the seed.

    The host source answers from memory (no I/O), so a caller may ask per call; a failing source
    never stops matching: the seed answers and the failure is logged once until it reads again.
    """
    if _verb_cue_source is None:
        _announce(
            "unconfigured",
            "matrx_seo.name_matching: no host verb-cue source configured — matching with the seed "
            "list (knob seo.name_matching.name_verb_cues is not being read)",
        )
        return NAME_VERB_CUES
    try:
        cues = tuple(str(v) for v in _verb_cue_source() if str(v).strip())
    except Exception as exc:  # noqa: BLE001 — announced, never silent
        _announce(
            f"failed:{type(exc).__name__}",
            f"matrx_seo.name_matching: the verb-cue knob could not be read ({exc!r}) — matching "
            "with the seed list until it reads",
        )
        return NAME_VERB_CUES
    _announced.discard("unconfigured")
    return cues


#: Words that, in the same sentence as a verb-cued everyday-word name, show it is a product or a
#: company ("Acme is one OPTION", "Render is a hosting PLATFORM", "Render offers MANAGED Postgres") —
#: the second signal a verb cue needs ("Monday is the best day to post", "Signal has to be strong",
#: "Linear is fine" have none). The SEED of platform.feature_knob "seo.name_matching"
#: "name_product_context_words" (aidream migration 1536), handed in through
#: :func:`configure_name_context_words`; see :func:`name_context_words`.
NAME_PRODUCT_CONTEXT_WORDS: tuple[str, ...] = _shared.NAME_PRODUCT_CONTEXT_WORDS

_context_source: Callable[[], Iterable[str]] | None = None


def configure_name_context_words(source: Callable[[], Iterable[str]] | None) -> None:
    """Install the host's live reader of ``seo.name_matching.name_product_context_words`` (None clears)."""
    global _context_source
    _context_source = source
    _announced.discard("context_unconfigured")


def name_context_words() -> tuple[str, ...]:
    """The product context words in force now: the host's knob row, or — announced — the seed."""
    if _context_source is None:
        _announce(
            "context_unconfigured",
            "matrx_seo.name_matching: no host product-context source configured — matching with the "
            "seed list (knob seo.name_matching.name_product_context_words is not being read)",
        )
        return NAME_PRODUCT_CONTEXT_WORDS
    try:
        return tuple(str(v) for v in _context_source() if str(v).strip())
    except Exception as exc:  # noqa: BLE001 — announced, never silent
        _announce(
            f"context_failed:{type(exc).__name__}",
            f"matrx_seo.name_matching: the product-context knob could not be read ({exc!r}) — matching "
            "with the seed list until it reads",
        )
        return NAME_PRODUCT_CONTEXT_WORDS


def proper_name_match(
    term: str,
    text: str,
    *,
    verbs: Iterable[str] | None = None,
    context_words: Iterable[str] | None = None,
    co_terms: Iterable[str] = (),
) -> str | None:
    """``term`` used as a proper name in ``text``: written capitalised as a whole word, and —
    when it opens a sentence, line or list item, where every word is capitalised — with a naming
    cue next to it ("Render vs …", "… or Render", "Render.com", "Render's", "Render: …",
    "Render — …", or a list item that is the name alone).

    A verb cue ("Render offers …") is not enough alone — "Monday is the best day to post" opens
    with an everyday word and a verb too. It counts with a second signal: a product context word
    in the same sentence, the name as a domain, or one of ``co_terms`` (the other names being
    tracked, such as competitors) in the text."""
    folded = unicodedata.normalize("NFKC", text)
    name = unicodedata.normalize("NFKC", term)
    cues = name_verb_cues() if verbs is None else tuple(verbs)
    context = name_context_words() if context_words is None else tuple(context_words)
    co_terms = tuple(co_terms)
    for m in re.finditer(r"(?<!\w)" + re.escape(name) + r"(?!\w)", folded, flags=re.IGNORECASE):
        if reads_as_proper_name(
            folded, m.start(), m.end(),
            name=name, verbs=cues, context_words=context, co_terms=co_terms,
        ):
            return m.group(0)
    return None


def is_flagged(term: str, common_word_terms: Iterable[str] | None = None) -> bool:
    """``term`` is a name that is also an everyday word: in the given flag list (a register's,
    possibly edited by a person), or — with no list — by the dictionary rule."""
    if common_word_terms is not None:
        return term.strip().casefold() in {str(t).strip().casefold() for t in common_word_terms}
    return bool(common_word_names([term]))
