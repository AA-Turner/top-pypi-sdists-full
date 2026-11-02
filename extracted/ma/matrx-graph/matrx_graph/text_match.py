"""THE one term matcher: does a text contain any term of a list (2026-10-27).

Used by ``text.term_scan`` (a fuzzy near miss is for REVIEW) and ``data.check_items``
``not_contains`` (a fuzzy near miss DROPS the item) — the callers decide what a near miss
means; this module only finds hits and near misses, separately. The similarity step splits
words with :func:`words` so both steps see the same words.

Folding (``folded`` mode), done on the WHOLE text so positions still point into the original:
- Unicode NFKC (decomposed "Café" == composed; fullwidth == plain) and casefold;
- every Default_Ignorable_Code_Point removed (zero-width space / joiner, soft hyphen, combining
  grapheme joiner, variation selectors, …) — the Unicode property, not a hand list;
- the dotted-capital-I artifact of casefolding ("İ" -> "i" + dot above) folded to "i";
- accents are KEPT unless ``strip_accents`` ("Cafe" is not "Café" by default);
- with ``strip_html``: inline formatting tags join the words around them (``<b>sh</b>red`` is
  "shred"), any other tag is a break, and entities read as their character (``&amp;`` is "&").

Words: letters and digits; an underscore, a space or punctuation separates words, a change
of case inside a written word does too ("AcmeCorp" is "acme" + "corp", "AI_Matrx" is "ai" +
"matrx"), and in scripts written without spaces (Han, kana, Thai, Lao, Khmer, Myanmar) every
character is a word, so "北京" is found inside "我爱北京". A word that MIXES Latin with
Cyrillic/Greek lookalikes ("Аcme" with a Cyrillic А), or is made only of such lookalikes, is
read through a Unicode TR39-style confusables skeleton; a real Russian or Greek word is not.

A term matches in one of these ways (``kind`` on every hit):
- ``words``: its words appear as a whole-word sequence ("art" never hits "party"); the last
  word may carry a plural "s"/"es" ("Acmes");
- ``compact``: a term of 4+ letters written run-together or split differently — "AIMatrx",
  "AI Matrx", "A.I. Matrx", "Coca-Cola"/"CocaCola", "O'Reilly"/"OReilly" — or any term of 2+
  letters spelled out one letter at a time ("I.B.M.", "A c m e"). Only WHOLE adjacent text
  words whose letters join to exactly the term's letters count, and only when the text's
  separator breaks fall on the term's own word breaks or the text splits at every one of them
  (so "aim at rx" is never "AI Matrx", "the academy" never "Acme") — or a ONE-word term is
  written as exactly two adjacent words that join to it ("Brew lio", "Brew-lio" for "Brewlio";
  "brew list" never, it joins to something else);
- ``symbols``: a term with symbols in it ("C++", "C#", "AT&T") must match WITH its symbols;
- domains: a term that is a web address ("https://www.example.com/", "www.example.com") is
  matched as its bare host ("example.com"), which also hits inside any URL on that host;
- ``exact`` mode: the term exactly as written (outer spaces trimmed), case-sensitive, as a
  WHOLE WORD ("Acme" never hits "Acmes") — not a plain substring.

Proper-name terms (per term, ``proper_name_only``): a name that is also an everyday word
("Render", "Notion", "Apple") counts only where the text writes it as a name — capitalised and
mid-sentence, or opening a sentence/line/list item WITH a naming cue ("Render vs …", "Render's",
"Render.com", "- Render", "Render offers a managed hosting platform"). The rules are THE shared
ones, :func:`matrx_utils.proper_names.reads_as_proper_name` (each rule documented there); the
other terms of the list are its ``co_terms``. ``everyday_words="auto"`` marks every one-word term
that is a dictionary word (:func:`matrx_utils.proper_names.everyday_word_terms`) this way; a list
marks the terms in it; a term given ``"any"`` is never marked. Near misses of a proper-name term
are not reported (a misspelt everyday word is not a name).

Fuzzy (opt-in): a one-word term of at least ``min_term_length`` letters with no hit is compared
with each text word of at least ``min_word_length`` letters; a spelling ratio at or above
``ratio`` is a near miss (``kind="fuzzy"``, with ``ratio``).
"""

from __future__ import annotations

import difflib
import html
import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Literal

__all__ = [
    "FuzzyRule", "Match", "TermMatcher", "TermMode", "fold", "fold_with_spans", "plural_forms", "term_key", "words",
]

_WORD = re.compile(r"[^\W_]+")

#: Unicode Default_Ignorable_Code_Point (DerivedCoreProperties.txt, Unicode 15.1). The stdlib
#: exposes no accessor for the property, so its ranges are the property's own definition.
_IGNORABLE = (
    (0x00AD, 0x00AD), (0x034F, 0x034F), (0x061C, 0x061C), (0x115F, 0x1160), (0x17B4, 0x17B5),
    (0x180B, 0x180F), (0x200B, 0x200F), (0x202A, 0x202E), (0x2060, 0x206F), (0x3164, 0x3164),
    (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF), (0xFFA0, 0xFFA0), (0xFFF0, 0xFFF8), (0x1BCA0, 0x1BCA3),
    (0x1D173, 0x1D17A), (0xE0000, 0xE0FFF),
)

#: Scripts written without spaces between words: every character is its own word.
_NO_SPACE = (
    (0x0E00, 0x0EFF), (0x1000, 0x109F), (0x1780, 0x17FF), (0x3040, 0x30FF), (0x31F0, 0x31FF),
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0xFF66, 0xFF9F), (0x20000, 0x323AF),
)

#: TR39-style confusables skeleton for the Cyrillic and Greek letters that look Latin (lower
#: case: folding runs first). Applied only to a word that mixes them with Latin letters or is
#: made only of them.
_SKELETON = str.maketrans({
    "а": "a", "в": "b", "е": "e", "к": "k", "м": "m", "н": "h", "о": "o", "р": "p", "с": "c",
    "т": "t", "у": "y", "х": "x", "і": "i", "ј": "j", "ѕ": "s", "һ": "h", "ԁ": "d", "ԛ": "q",
    "ԝ": "w", "ӏ": "l", "ѵ": "v", "ү": "y",
    "α": "a", "β": "b", "ε": "e", "ζ": "z", "η": "n", "ι": "i", "κ": "k", "μ": "u", "ν": "v",
    "ο": "o", "ρ": "p", "τ": "t", "υ": "u", "χ": "x", "ϲ": "c", "ϳ": "j",
})


def _in(cp: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    return any(lo <= cp <= hi for lo, hi in ranges)


def _ignorable(ch: str) -> bool:
    return _in(ord(ch), _IGNORABLE)


def _no_space(ch: str) -> bool:
    return _in(ord(ch), _NO_SPACE)
#: Characters between words that never make a term "symbol-bearing" (they only separate words).
_SEPARATORS = frozenset(".-'’‘ʼ_/:,;!?\"“”()[]")
_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*://")
_HOST = re.compile(r"^(?:[\w-]+\.)+[^\W\d_]{2,}$")

#: Inline formatting tags join the words around them; any other tag is a break.
INLINE_TAG = re.compile(r"</?(?:strong|b|em|i|u|mark|span|a|small|sup|sub|code|font)\b[^<>]*>", re.I)
ANY_TAG = re.compile(r"</?[A-Za-z][^<>]*>")
_ENTITY = re.compile(r"&(?:#\d+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);")

MatchKind = Literal["words", "compact", "symbols", "exact", "fuzzy"]
#: How one term may match: ``any`` occurrence, or only where it reads as a proper name.
TermMode = Literal["any", "proper_name_only"]


def _fold_cluster(cluster: str, strip_accents: bool) -> str:
    s = unicodedata.normalize("NFKC", cluster).casefold().replace("i̇", "i")
    if strip_accents:
        s = "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))
    return unicodedata.normalize("NFKC", s)


def _html_marks(text: str) -> dict[int, tuple[int, str]]:
    """start -> (end, replacement) for every tag and entity in ``text``."""
    marks: dict[int, tuple[int, str]] = {}
    for m in ANY_TAG.finditer(text):
        marks[m.start()] = (m.end(), "" if INLINE_TAG.fullmatch(m.group()) else " ")
    for m in _ENTITY.finditer(text):
        if not any(s <= m.start() < e for s, (e, _) in marks.items()):
            marks[m.start()] = (m.end(), html.unescape(m.group()))
    return marks


def fold_with_spans(
    text: str, *, strip_accents: bool = False, strip_html: bool = False
) -> tuple[str, list[int], list[int]]:
    """(folded text, start, end) — ``start[k]``/``end[k]`` is the span in ``text`` of the
    character cluster folded character ``k`` came from. A base character and the combining
    marks after it fold together, which is what whole-text NFKC does."""
    out: list[str] = []
    starts: list[int] = []
    ends: list[int] = []
    marks = _html_marks(text) if strip_html and ("<" in text or "&" in text) else {}
    i, n = 0, len(text)
    while i < n:
        if i in marks:
            end, piece = marks[i]
            for ch in _fold_cluster(piece, strip_accents) if piece.strip() else piece:
                out.append(ch)
                starts.append(i)
                ends.append(end)
            i = end
            continue
        j = i + 1
        while j < n and unicodedata.combining(text[j]):
            j += 1
        cluster = "".join(c for c in text[i:j] if not _ignorable(c))
        if not cluster:
            i = j
            continue
        if cluster.isascii():
            piece = cluster.lower()
        else:
            piece = _fold_cluster(cluster, strip_accents)
        for ch in piece:
            out.append(ch)
            starts.append(i)
            ends.append(j)
        i = j
    return "".join(out), starts, ends


def fold(text: str, *, strip_accents: bool = False, strip_html: bool = False) -> str:
    """The folded form of ``text`` (see the module docstring)."""
    return fold_with_spans(text, strip_accents=strip_accents, strip_html=strip_html)[0]


def _skeleton(word: str) -> str:
    mapped = word.translate(_SKELETON)
    if mapped == word:
        return word
    has_latin = any("a" <= c <= "z" for c in word)
    only_lookalikes = all(c.isascii() or c != m for c, m in zip(word, mapped, strict=True))
    return mapped if has_latin or only_lookalikes else word


def _case_cuts(original: str) -> list[int]:
    """Where a written word's own capitals break it ("AcmeCorp" -> 4, "OReilly" -> 1)."""
    cuts = []
    for k in range(1, len(original)):
        a, b = original[k - 1], original[k]
        if (a.islower() and b.isupper()) or (
            a.isupper() and b.isupper() and k + 1 < len(original) and original[k + 1].islower()
        ):
            cuts.append(k)
    return cuts


def _tokens(raw: str, folded: str, starts: list[int], ends: list[int]) -> list[tuple[str, int, int, bool]]:
    """(word, folded start, folded end, soft) — ``soft`` when the break before the word is
    inside one written word (a change of case, or a character of a script without spaces)."""
    out: list[tuple[str, int, int, bool]] = []
    for m in _WORD.finditer(folded):
        s, e = m.start(), m.end()
        word = m.group()
        if word.isascii():
            # Fast path: no script without spaces, no lookalike; split only on mixed case.
            original = raw[starts[s] : ends[e - 1]]
            if len(original) == e - s and original != original.lower() and original != original.upper():
                cuts = _case_cuts(original)
                if cuts:
                    for n, (a, b) in enumerate(zip([0, *cuts], [*cuts, e - s], strict=True)):
                        out.append((word[a:b], s + a, s + b, n > 0))
                    continue
            out.append((word, s, e, False))
            continue
        pieces: list[tuple[int, int]] = []
        k = s
        while k < e:
            if _no_space(folded[k]):
                pieces.append((k, k + 1))
                k += 1
                continue
            r = k
            while r < e and not _no_space(folded[r]):
                r += 1
            original = raw[starts[k] : ends[r - 1]]
            cut_at = [k + c for c in _case_cuts(original)] if len(original) == r - k else []
            for a, b in zip([k, *cut_at], [*cut_at, r], strict=True):
                pieces.append((a, b))
            k = r
        for n, (a, b) in enumerate(pieces):
            out.append((_skeleton(folded[a:b]), a, b, n > 0))
    return out


def words(text: str, *, strip_accents: bool = False) -> list[str]:
    """The folded words of ``text`` (see the module docstring) — punctuation, apostrophes and
    underscores separate words, so "don't" and "don’t" are both ``["don", "t"]``. The one word
    splitter of the text steps."""
    folded, starts, ends = fold_with_spans(text, strip_accents=strip_accents)
    return [w for w, _, _, _ in _tokens(text, folded, starts, ends)]


def term_key(text: str, *, strip_accents: bool = False) -> str:
    """The key two spellings of one term meet on: its folded :func:`words` joined by single spaces
    ("AI-Matrx", "ai matrx" and "AiMatrx" are all ``"ai matrx"``). ``data.spread_rank`` folds terms on it."""
    return " ".join(words(text, strip_accents=strip_accents))


def plural_forms(word: str) -> tuple[str, ...]:
    """The spellings a term's LAST word may take and still be the term: itself, plus "s" / "es" when it
    has 3+ letters ("acme" -> acme, acmes, acmees; "ai" -> ai). THE one plural rule — the matcher's
    ``words`` hits and ``data.spread_rank``'s variant folding both read it."""
    return (word, word + "s", word + "es") if len(word) >= 3 else (word,)


@dataclass(frozen=True, slots=True)
class FuzzyRule:
    ratio: float = 0.86
    min_term_length: int = 7
    min_word_length: int = 6


@dataclass(slots=True)
class Match:
    term_index: int
    term: str
    term_class: str | None
    start: int
    end: int
    matched_text: str
    kind: MatchKind
    ratio: float | None = None


@dataclass(slots=True)
class _Term:
    index: int
    term: str
    term_class: str | None
    key: str
    words: list[str] = field(default_factory=list)
    compact: str = ""
    breaks: frozenset[int] = frozenset()
    pattern: re.Pattern[str] | None = None
    proper_name_only: bool = False


def _term_words(term: str, strip_accents: bool, strip_html: bool) -> tuple[list[str], frozenset[int]]:
    """The term's words and every break between them, as offsets into its joined letters."""
    folded, starts, ends = fold_with_spans(term, strip_accents=strip_accents, strip_html=strip_html)
    toks = [w for w, _, _, _ in _tokens(term, folded, starts, ends)]
    breaks, total = set(), 0
    for w in toks[:-1]:
        total += len(w)
        breaks.add(total)
    return toks, frozenset(breaks)


def _as_host(folded_term: str) -> str | None:
    s = _SCHEME.sub("", folded_term.strip())
    if s.startswith("www."):
        s = s[4:]
    s = re.split(r"[/?#]", s, maxsplit=1)[0]
    return s if " " not in s and _HOST.match(s) else None


class _Text:
    __slots__ = ("raw", "folded", "starts", "ends", "toks", "first", "by_len")

    def __init__(self, raw: str, strip_accents: bool, strip_html: bool = False) -> None:
        self.raw = raw
        self.folded, self.starts, self.ends = fold_with_spans(
            raw, strip_accents=strip_accents, strip_html=strip_html
        )
        self.toks = _tokens(raw, self.folded, self.starts, self.ends)
        self.first: dict[str, list[int]] = {}
        for p, (w, _, _, _) in enumerate(self.toks):
            self.first.setdefault(w, []).append(p)
        self.by_len: dict[int, set[str]] | None = None

    def span(self, fs: int, fe: int) -> tuple[int, int]:
        return self.starts[fs], self.ends[fe - 1]


class TermMatcher:
    """Compile a term list once; :meth:`scan` any number of texts.

    ``terms`` is ``(term, term_class)`` pairs or ``(term, term_class, mode)`` triples (mode
    ``None`` = not stated). Terms are kept distinct by their folded text (symbols included) and
    class; a blank term is ignored and a term with no letters or digits is listed in
    :attr:`skipped`. ``everyday_words``: ``"auto"`` makes every dictionary-word term with no
    stated mode ``proper_name_only``; a list does that for the terms in it (any case);
    ``"none"`` (default) leaves modes as stated.
    """

    def __init__(
        self,
        terms: Iterable[tuple[str, str | None]],
        *,
        mode: Literal["folded", "exact"] = "folded",
        strip_accents: bool = False,
        strip_html: bool = False,
        fuzzy: FuzzyRule | None = None,
        everyday_words: Literal["auto", "none"] | Iterable[str] = "none",
    ) -> None:
        self.mode = mode
        self.strip_accents = strip_accents
        self.strip_html = strip_html
        self.fuzzy = fuzzy
        self.terms: list[_Term] = []
        self.skipped: list[str] = []
        self._ratios: dict[tuple[str, str], float] = {}
        seen: set[tuple[str, str | None]] = set()
        given = [(t[0], t[1], t[2] if len(t) > 2 else None) for t in terms]  # type: ignore[misc]
        everyday: set[str] = set()
        if everyday_words == "auto":
            from matrx_utils.proper_names import everyday_word_terms

            everyday = {w.casefold() for w in everyday_word_terms(t for t, _, m in given if m is None and t)}
        elif everyday_words != "none":
            everyday = {str(w).strip().casefold() for w in everyday_words}
        for term, term_class, term_mode in given:
            if not term or not term.strip():
                continue
            if mode == "exact":
                term = term.strip()
                key = term
            else:
                key = " ".join(fold(term, strip_accents=strip_accents, strip_html=strip_html).split())
            if (key, term_class) in seen:
                continue
            seen.add((key, term_class))
            t = _Term(index=len(self.terms), term=term, term_class=term_class, key=key)
            t.proper_name_only = term_mode == "proper_name_only" or (
                term_mode is None and term.strip().casefold() in everyday
            )
            if mode == "exact":
                t.pattern = re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)")
                t.words = _WORD.findall(term)
            else:
                host = _as_host(key)
                target = host or key
                if host is None and any(
                    not c.isalnum() and not c.isspace() and c != "_" and c not in _SEPARATORS for c in key
                ):
                    t.pattern = re.compile(
                        r"(?<!\w)" + r"\s+".join(re.escape(p) for p in key.split()) + r"(?!\w)"
                    )
                t.words, t.breaks = _term_words(
                    target if host else term, strip_accents, strip_html and not host
                )
                t.compact = "".join(t.words)
            if not t.words:
                self.skipped.append(term)
                continue
            self.terms.append(t)

    def scan(self, text: str) -> tuple[list[Match], list[Match]]:
        """(hits, near misses) in ``text``, each in text order; positions index ``text``."""
        if not self.terms or not text:
            return [], []
        hits: list[Match] = []
        near: list[Match] = []
        tx = _Text(text, self.strip_accents, self.strip_html) if self.mode == "folded" else None
        for t in self.terms:
            found = self._exact(t, text) if self.mode == "exact" else self._folded(t, tx)
            if t.proper_name_only:
                found = [m for m in found if self._reads_as_name(t, text, m)]
                hits.extend(found)
                continue
            hits.extend(found)
            if not found and self.fuzzy is not None:
                if tx is None:
                    tx = _Text(text, self.strip_accents, self.strip_html)
                near.extend(self._near(t, tx))
        hits.sort(key=lambda m: (m.start, m.term_index))
        near.sort(key=lambda m: (m.start, m.term_index))
        return hits, near

    def _reads_as_name(self, t: _Term, text: str, m: Match) -> bool:
        """THE shared proper-name rules on this occurrence; the list's other terms are co-terms."""
        from matrx_utils.proper_names import reads_as_proper_name

        before = unicodedata.normalize("NFKC", text[: m.start])
        found = unicodedata.normalize("NFKC", text[m.start : m.end])
        whole = before + found + unicodedata.normalize("NFKC", text[m.end :])
        co_terms = [o.term for o in self.terms if o is not t]
        return reads_as_proper_name(
            whole, len(before), len(before) + len(found), name=t.term.strip(), co_terms=co_terms
        )

    def _match(self, t: _Term, start: int, end: int, raw: str, kind: MatchKind, ratio: float | None = None) -> Match:
        return Match(t.index, t.term, t.term_class, start, end, raw[start:end], kind, ratio)

    def _exact(self, t: _Term, text: str) -> list[Match]:
        assert t.pattern is not None
        return [self._match(t, m.start(), m.end(), text, "exact") for m in t.pattern.finditer(text)]

    def _folded(self, t: _Term, tx: _Text) -> list[Match]:
        if t.pattern is not None:
            out = []
            for m in t.pattern.finditer(tx.folded):
                s, e = tx.span(m.start(), m.end())
                out.append(self._match(t, s, e, tx.raw, "symbols"))
            return out
        toks, n = tx.toks, len(t.words)
        spans: list[tuple[int, int, MatchKind]] = []
        last_word = t.words[-1]
        plurals = plural_forms(last_word)
        firsts = plurals if n == 1 else (t.words[0],)
        for first in firsts:
            for p in tx.first.get(first, ()):
                got = [w for w, _, _, _ in toks[p : p + n]]
                if len(got) == n and got[:-1] == t.words[:-1] and got[-1] in plurals:
                    spans.append((p, p + n - 1, "words"))
        if len(t.compact) >= 2:
            for k in range(1, len(t.compact) + 1):
                for p in tx.first.get(t.compact[:k], ()):
                    joined, j = toks[p][0], p
                    cuts: set[int] = set()
                    hard: set[int] = set()
                    while len(joined) < len(t.compact) and j + 1 < len(toks):
                        j += 1
                        cuts.add(len(joined))
                        if not toks[j][3]:
                            hard.add(len(joined))
                        joined += toks[j][0]
                        if not t.compact.startswith(joined):
                            break
                    if joined != t.compact or (j == p and n == 1):
                        continue
                    # The text's separators fall on the term's own breaks (it joins or keeps the
                    # term's words), the text splits at every break the term has, or it spells
                    # the term out letter by letter.
                    spelled = j > p and all(len(w) == 1 for w, _, _, _ in toks[p : j + 1])
                    if len(t.compact) < 4 and not spelled:
                        continue
                    split_once = n == 1 and j == p + 1
                    if not (hard <= t.breaks or (t.breaks and t.breaks <= cuts) or spelled or split_once):
                        continue
                    spans.append((p, j, "compact"))
        spans.sort()
        out: list[Match] = []
        last = -1
        for p, j, kind in spans:
            if p <= last:
                continue
            last = j
            s, e = tx.span(toks[p][1], toks[j][2])
            out.append(self._match(t, s, e, tx.raw, kind))
        return out

    def _near(self, t: _Term, tx: _Text) -> list[Match]:
        rule = self.fuzzy
        assert rule is not None
        if len(t.words) != 1 or t.pattern is not None:
            return []
        needle = t.words[0] if self.mode == "folded" else words(t.words[0], strip_accents=self.strip_accents)[0]
        la = len(needle)
        if la < rule.min_term_length:
            return []
        if tx.by_len is None:
            tx.by_len = {}
            for w in tx.first:
                tx.by_len.setdefault(len(w), set()).add(w)
        out: list[Match] = []
        # ratio = 2M / (la + lb) <= 2 min(la, lb) / (la + lb): skip lengths that cannot reach it.
        for lb, bucket in tx.by_len.items():
            if lb < rule.min_word_length or 2 * min(la, lb) / (la + lb) < rule.ratio:
                continue
            for w in bucket:
                if w == needle:
                    continue
                key = (needle, w)
                r = self._ratios.get(key)
                if r is None:
                    sm = difflib.SequenceMatcher(None, w, needle)
                    r = sm.ratio() if sm.quick_ratio() >= rule.ratio else 0.0
                    self._ratios[key] = r
                if r >= rule.ratio:
                    for p in tx.first[w]:
                        s, e = tx.span(tx.toks[p][1], tx.toks[p][2])
                        out.append(self._match(t, s, e, tx.raw, "fuzzy", round(r, 4)))
        return out
