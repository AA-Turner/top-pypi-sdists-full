"""The one name matcher: a name that is also an everyday word counts only as a proper name.

Every place that asks "does this text name the company or a competitor?" goes through here —
the blinding check (``ai_visibility_design.scan_text``), answer mentions
(``providers.dataforseo.ai_answers.answer_mentions_target``) and coverage
(``coverage.term_hits``). "Stream", "Workers", "Render", "Remote", "Square" are names only when
written as names; the ordinary word is never a mention and never a leak.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from collections.abc import Callable, Iterable
from typing import Any

logger = logging.getLogger(__name__)

_COMMON_WORDS: frozenset[str] | None = None


def common_english_words() -> frozenset[str]:
    """Lower-case English words (Webster's 2nd, public domain; ``data/``), loaded once."""
    global _COMMON_WORDS
    if _COMMON_WORDS is None:
        import gzip
        from importlib import resources

        raw = resources.files("matrx_seo").joinpath("data/common_english_words.txt.gz")
        with raw.open("rb") as fh:
            _COMMON_WORDS = frozenset(gzip.decompress(fh.read()).decode("utf-8").split())
    return _COMMON_WORDS


def common_word_names(terms: Iterable[Any]) -> list[str]:
    """The names that are also an everyday word: one alphabetic token whose lower-case form is an
    English word ("Render", "Remote", "Workers", "Stream")."""
    words = common_english_words()
    out: list[str] = []
    for term in terms:
        text = str(term).strip()
        if re.fullmatch(r"[^\W\d_]+", text) and is_word(text.casefold(), words):
            if text not in out:
                out.append(text)
    return out


def is_word(word: str, words: frozenset[str]) -> bool:
    """``word`` or its singular is an English word (the list holds singulars: "workers")."""
    if word in words:
        return True
    singulars = []
    if word.endswith("ies"):
        singulars.append(word[:-3] + "y")
    if word.endswith("es"):
        singulars.append(word[:-2])
    if word.endswith("s"):
        singulars.append(word[:-1])
    return any(len(w) >= 3 and w in words for w in singulars)


#: Verbs that, right after a capitalised everyday word opening a sentence or list item, mark it as
#: a name ("Render offers …", "Acme is one option"). The SEED of platform.feature_knob
#: "seo.name_matching" "name_verb_cues" (aidream migration 1530). The live list is the knob row,
#: handed in by the host through :func:`configure_name_verb_cues`; see :func:`name_verb_cues`.
NAME_VERB_CUES: tuple[str, ...] = (
    "is", "are", "was", "were", "has", "have", "had", "offers", "offered", "provides", "provided",
    "lets", "gives", "supports", "includes", "features", "makes", "allows", "enables", "helps",
    "charges", "costs", "uses", "runs", "hosts", "sells", "ships", "focuses", "specializes",
    "specialises", "stands", "remains", "delivers", "excels", "leads", "integrates", "works",
)

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
NAME_PRODUCT_CONTEXT_WORDS: tuple[str, ...] = (
    "alternative", "alternatives", "api", "app", "apps", "brand", "cdn", "cloud", "companies", "company",
    "competitor", "competitors", "crm", "customers", "dashboard", "database", "deploy", "deploys",
    "deployment", "enterprise", "eor", "feature", "features", "hosted", "hosting", "integration",
    "integrations", "managed", "option", "options", "payroll", "plan", "plans", "platform", "platforms",
    "price", "priced", "pricing", "product", "products", "provider", "providers", "saas", "sdk",
    "service", "services", "software", "solution", "solutions", "startup", "subscription", "tier",
    "tool", "tools", "vendor", "vendors",
)

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


#: Words that put a capitalised everyday word in a naming context when it opens a sentence.
NAME_CONTEXT = re.compile(
    r"^\s*(?:/|,|&|\+|\(|\)|'s\b|\.(?:com|io|co|app|dev|net|org)\b|vs\.?\b|versus\b|or\b|and\b"
    r"|alternatives?\b|pricing\b|review"
    # "Render: good", "Render — managed hosting", "Render - fast", "**Render**:"
    r"|\**\s*:|\**\s+[-\u2013\u2014]\s|\**\s*[\u2013\u2014])",
    re.IGNORECASE,
)
NAME_CONTEXT_BEFORE = re.compile(r"(?:/|,|&|\+|\bvs\.?|\bversus|\bor|\band|\blike)\s*$", re.I)
#: A list marker opening the line: "1. ", "2) ", "- ", "* ", "• ", optionally bold ("- **").
LIST_MARKER_BEFORE = re.compile(r"(?:^|\n)[ \t]*(?:\d{1,3}[.)]|[-*\u2022+])[ \t]+\**$")


def _verb_cue(after: str, verbs: Iterable[str]) -> bool:
    m = re.match(r"\**\s+([^\W\d_]+)\b", after)
    return m is not None and m.group(1).casefold() in {v.casefold() for v in verbs}


def _second_signal(
    name: str, text: str, after: str, context_words: Iterable[str], co_terms: Iterable[str]
) -> bool:
    """What a verb cue needs beside it before an everyday word counts as the name: a product word
    in the same sentence, the name written as a domain anywhere, or another tracked name in the text."""
    sentence = re.split(r"[.!?\n]", after, maxsplit=1)[0]
    words = {w.casefold() for w in re.findall(r"[^\W\d_]+", sentence)}
    if words & {w.casefold() for w in context_words}:
        return True
    if re.search(r"(?<![\w.])" + re.escape(name) + r"\.(?:com|io|co|app|dev|net|org|ai)\b", text, re.IGNORECASE):
        return True
    for other in co_terms:
        other = unicodedata.normalize("NFKC", str(other)).strip()
        if not other or other.casefold() == name.casefold():
            continue
        if re.search(r"(?<!\w)" + re.escape(other) + r"(?!\w)", text):
            return True
    return False


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
        found = m.group(0)
        if not found[:1].isupper():
            continue
        before = folded[: m.start()]
        opens = not before.strip() or re.search(r"[.!?:\n\"“(\[*-]\s*$", before) is not None
        if not opens:
            return found
        after = folded[m.end() :]
        if re.search(r"[\"“'\[]\s*$", before) and re.match(r"\s*[\"”'\]]", after):
            return found  # the whole value of a quoted or listed item: a name, not a word
        if NAME_CONTEXT.match(after) or NAME_CONTEXT_BEFORE.search(before):
            return found
        if _verb_cue(after, cues) and _second_signal(name, folded, after, context, co_terms):
            return found
        if LIST_MARKER_BEFORE.search(before) and re.match(r"\**[ \t]*(?:\n|$|\()", after):
            return found  # a list item that is the name alone
    return None


def is_flagged(term: str, common_word_terms: Iterable[str] | None = None) -> bool:
    """``term`` is a name that is also an everyday word: in the given flag list (a register's,
    possibly edited by a person), or — with no list — by the dictionary rule."""
    if common_word_terms is not None:
        return term.strip().casefold() in {str(t).strip().casefold() for t in common_word_terms}
    return bool(common_word_names([term]))
