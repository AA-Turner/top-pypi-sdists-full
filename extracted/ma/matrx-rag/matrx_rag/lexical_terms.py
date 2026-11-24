"""The keyword lane's own notion of a match, in Python: which query words take part and which text
words each one matches — exactly as ``rag.recall_lexical`` (kg_046) builds its tsquery.

The lane recalls a chunk holding ANY term; a caller that needs "every word" (a scan search door, a
highlighter) asks here instead of re-inventing word rules, so it never disagrees with the engine:

- query words are the alphanumeric runs (a trailing ``'s`` dropped), lower-cased, of 2+ characters or
  holding a digit; English stop words are dropped unless every word is one (``english`` config);
- each word ``w`` with English stem ``s`` (Snowball english, as Postgres's ``english_stem``) becomes
  ``w | s:*`` when ``s`` has 4+ letters, else ``w | s``; the chunk side is the ``simple`` config
  (lower-cased words, no stemming, no accent folding), so a text word ``t`` matches when
  ``t == w``, ``t == s``, or (``len(s) >= 4`` and ``t`` starts with ``s``);
- a query with search operators (a quote, or ``-word``) keeps its strict meaning: its plain words,
  each matched as itself.

MIRROR, NOT A CALL: the database does not report which terms a hit matched, so this module mirrors the
SQL. The stemmer below is Porter2 (the Snowball english algorithm Postgres uses) written out here,
because the package carries no stemming library; a word whose stem differs from Postgres's would be
judged differently — the tests pin the words that matter. Change the SQL, change this file.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

#: Postgres ``english.stop`` (the Snowball English stop list).
ENGLISH_STOP_WORDS = frozenset(
    "i me my myself we our ours ourselves you your yours yourself yourselves he him his himself she her hers "
    "herself it its itself they them their theirs themselves what which who whom this that these those am is "
    "are was were be been being have has had having do does did doing a an the and but if or because as until "
    "while of at by for with about against between into through during before after above below to from up "
    "down in out on off over under again further then once here there when where why how all any both each few "
    "more most other some such no nor not only own same so than too very s t can will just don should now".split()
)

_RUN = re.compile(r"[^\W_]+", re.UNICODE)
_POSSESSIVE = re.compile(r"['’]s\b", re.IGNORECASE)
_OPERATORS = re.compile(r'"|(^|\s)-[^\W_]', re.UNICODE)


@dataclass(frozen=True)
class LexicalTerm:
    """One query word as the keyword lane searches for it."""

    word: str
    stem: str | None
    prefix: bool

    def matches(self, token: str) -> bool:
        if token == self.word or (self.stem is not None and token == self.stem):
            return True
        return self.prefix and self.stem is not None and token.startswith(self.stem)


def text_tokens(text: str) -> set[str]:
    """The words the ``simple`` config indexes for ``text``: lower-cased alphanumeric runs."""
    return {t.lower() for t in _RUN.findall(text or "")}


def lexical_terms(query: str) -> list[LexicalTerm]:
    """The query's terms as ``rag.recall_lexical`` builds them (see the module doc)."""
    q = query or ""
    if _OPERATORS.search(q):
        plain = re.sub(r'(^|\s)-[^\s]+', " ", q)
        return [LexicalTerm(w, None, False) for w in dict.fromkeys(t.lower() for t in _RUN.findall(plain))]
    words = list(dict.fromkeys(
        w.lower() for w in _RUN.findall(_POSSESSIVE.sub("", q)) if len(w) >= 2 or any(c.isdigit() for c in w)
    ))
    keep = [w for w in words if w not in ENGLISH_STOP_WORDS] or words
    out = []
    for w in keep:
        stem = None if w in ENGLISH_STOP_WORDS else english_stem(w)
        out.append(LexicalTerm(w, stem, stem is not None and stem != w and len(stem) >= 4))
    return out


def holds_every_term(terms: list[LexicalTerm], text: str) -> bool:
    """True when every term matches some word of ``text`` — the lane's AND stage, over one text."""
    tokens = text_tokens(text)
    return bool(terms) and all(any(term.matches(t) for t in tokens) for term in terms)


# --- Porter2 (Snowball english) --------------------------------------------------------------------------

_VOWELS = frozenset("aeiouy")
_DOUBLES = ("bb", "dd", "ff", "gg", "mm", "nn", "pp", "rr", "tt")
_LI_ENDING = frozenset("cdeghkmnrt")
_EXCEPTIONS = {
    "skis": "ski", "skies": "sky", "dying": "die", "lying": "lie", "tying": "tie", "idly": "idl",
    "gently": "gentl", "ugly": "ugli", "early": "earli", "only": "onli", "singly": "singl",
}
_INVARIANT = frozenset({"sky", "news", "howe", "atlas", "cosmos", "bias", "andes"})
_STEP1A_INVARIANT = frozenset({"inning", "outing", "canning", "herring", "earring", "proceed", "exceed", "succeed"})


def _is_vowel(c: str) -> bool:
    return c in _VOWELS


def _region(w: str, start: int) -> int:
    for i in range(start + 1, len(w)):
        if not _is_vowel(w[i]) and _is_vowel(w[i - 1]):
            return i + 1
    return len(w)


def _short_syllable_end(w: str) -> bool:
    if len(w) == 2:
        return _is_vowel(w[0]) and not _is_vowel(w[1])
    return (len(w) >= 3 and not _is_vowel(w[-3]) and _is_vowel(w[-2])
            and not _is_vowel(w[-1]) and w[-1] not in "wxY")


def english_stem(word: str) -> str:
    """Porter2 stem of a lower-case ``word`` (the Snowball english stemmer)."""
    w = word.lower()
    if len(w) <= 2 or w in _INVARIANT or not w.isalpha() or not w.isascii():
        return w
    if w in _EXCEPTIONS:
        return _EXCEPTIONS[w]
    w = w.lstrip("'")
    if w.startswith("y"):
        w = "Y" + w[1:]
    w = "".join("Y" if c == "y" and i and _is_vowel(w[i - 1]) else c for i, c in enumerate(w))
    r1 = next((len(p) for p in ("gener", "commun", "arsen") if w.startswith(p)), None)
    if r1 is None:
        r1 = _region(w, 0)
    r2 = _region(w, r1) if r1 < len(w) else len(w)

    for suf in ("'s'", "'s", "'"):
        if w.endswith(suf):
            w = w[: -len(suf)]
            break
    # Step 1a
    if w.endswith("sses"):
        w = w[:-2]
    elif w.endswith(("ied", "ies")):
        w = w[:-2] if len(w) > 4 else w[:-1]
    elif w.endswith(("us", "ss")):
        pass
    elif w.endswith("s") and any(_is_vowel(c) for c in w[:-2]):
        w = w[:-1]
    if w in _STEP1A_INVARIANT:
        return w
    # Step 1b
    for suf in ("eedly", "eed"):
        if w.endswith(suf):
            if len(w) - len(suf) >= r1:
                w = w[: -len(suf)] + "ee"
            break
    else:
        for suf in ("ingly", "edly", "ing", "ed"):
            if w.endswith(suf):
                base = w[: -len(suf)]
                if any(_is_vowel(c) for c in base):
                    w = base
                    if w.endswith(("at", "bl", "iz")):
                        w += "e"
                    elif w.endswith(_DOUBLES):
                        w = w[:-1]
                    elif r1 >= len(w) and _short_syllable_end(w):
                        w += "e"
                break
    # Step 1c
    if len(w) > 2 and w[-1] in "yY" and not _is_vowel(w[-2]):
        w = w[:-1] + "i"
    # Step 2
    step2 = (("ization", "ize"), ("ational", "ate"), ("fulness", "ful"), ("ousness", "ous"), ("iveness", "ive"),
             ("tional", "tion"), ("biliti", "ble"), ("lessli", "less"), ("entli", "ent"), ("ation", "ate"),
             ("alism", "al"), ("aliti", "al"), ("ousli", "ous"), ("iviti", "ive"), ("fulli", "ful"), ("enci", "ence"),
             ("anci", "ance"), ("abli", "able"), ("izer", "ize"), ("ator", "ate"), ("alli", "al"), ("bli", "ble"),
             ("ogi", "og"), ("li", ""))
    for suf, rep in step2:
        if w.endswith(suf):
            if len(w) - len(suf) >= r1:
                if suf == "ogi" and not w[:-3].endswith("l"):
                    break
                if suf == "li" and w[-3:-2] not in _LI_ENDING:
                    break
                w = w[: -len(suf)] + rep
            break
    # Step 3
    step3 = (("ational", "ate"), ("tional", "tion"), ("alize", "al"), ("icate", "ic"), ("iciti", "ic"),
             ("ative", ""), ("ical", "ic"), ("ness", ""), ("ful", ""))
    for suf, rep in step3:
        if w.endswith(suf):
            if len(w) - len(suf) >= r1 and (suf != "ative" or len(w) - len(suf) >= r2):
                w = w[: -len(suf)] + rep
            break
    # Step 4
    step4 = ("ement", "ance", "ence", "able", "ible", "ment", "ant", "ent", "ism", "ate", "iti", "ous", "ive", "ize",
             "ion", "al", "er", "ic")
    for suf in step4:
        if w.endswith(suf):
            if len(w) - len(suf) >= r2 and (suf != "ion" or w[:-3].endswith(("s", "t"))):
                w = w[: -len(suf)]
            break
    # Step 5
    if w.endswith("e"):
        if len(w) - 1 >= r2 or (len(w) - 1 >= r1 and not _short_syllable_end(w[:-1])):
            w = w[:-1]
    elif w.endswith("ll") and len(w) - 1 >= r2:
        w = w[:-1]
    return w.replace("Y", "y")


__all__ = ["ENGLISH_STOP_WORDS", "LexicalTerm", "english_stem", "holds_every_term", "lexical_terms", "text_tokens"]
