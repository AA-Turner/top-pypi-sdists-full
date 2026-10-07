"""The one name matcher: a name that is also an everyday word counts only as a proper name.

Every place that asks "does this text name the company or a competitor?" goes through here —
the blinding check (``ai_visibility_design.scan_text``), answer mentions
(``providers.dataforseo.ai_answers.answer_mentions_target``) and coverage
(``coverage.term_hits``). "Stream", "Workers", "Render", "Remote", "Square" are names only when
written as names; the ordinary word is never a mention and never a leak.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from typing import Any

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


#: Words that put a capitalised everyday word in a naming context when it opens a sentence.
NAME_CONTEXT = re.compile(
    r"^\s*(?:/|,|&|\+|\(|\)|'s\b|\.(?:com|io|co|app|dev|net|org)\b|vs\.?\b|versus\b|or\b|and\b"
    r"|alternatives?\b|pricing\b|review)",
    re.IGNORECASE,
)
NAME_CONTEXT_BEFORE = re.compile(r"(?:/|,|&|\+|\bvs\.?|\bversus|\bor|\band|\blike)\s*$", re.I)


def proper_name_match(term: str, text: str) -> str | None:
    """``term`` used as a proper name in ``text``: written capitalised as a whole word, and —
    when it opens a sentence or line, where every word is capitalised — with a naming cue next to
    it ("Render vs …", "… or Render", "Render.com", "Render's")."""
    folded = unicodedata.normalize("NFKC", text)
    name = unicodedata.normalize("NFKC", term)
    for m in re.finditer(r"(?<!\w)" + re.escape(name) + r"(?!\w)", folded, flags=re.IGNORECASE):
        found = m.group(0)
        if not found[:1].isupper():
            continue
        before = folded[: m.start()]
        opens = not before.strip() or re.search(r"[.!?:\n\"“(\[-]\s*$", before) is not None
        if not opens:
            return found
        after = folded[m.end() :]
        if re.search(r"[\"“'\[]\s*$", before) and re.match(r"\s*[\"”'\]]", after):
            return found  # the whole value of a quoted or listed item: a name, not a word
        if NAME_CONTEXT.match(folded[m.end() :]) or NAME_CONTEXT_BEFORE.search(before):
            return found
    return None


def is_flagged(term: str, common_word_terms: Iterable[str] | None = None) -> bool:
    """``term`` is a name that is also an everyday word: in the given flag list (a register's,
    possibly edited by a person), or — with no list — by the dictionary rule."""
    if common_word_terms is not None:
        return term.strip().casefold() in {str(t).strip().casefold() for t in common_word_terms}
    return bool(common_word_names([term]))
