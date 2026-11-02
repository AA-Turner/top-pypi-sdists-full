"""Safe regular expressions — refuse, before they run, the patterns that can hang the engine.

Python's ``re`` has no match timeout, and matrx-graph does not depend on a
timeout-bounded engine, so a pattern a person (or an agent) writes into a step
is judged BEFORE it runs. Backtracking blows up when the engine has many ways
to split the same text; the judge refuses the shapes that give it that choice.

Every caller (``exponential`` level — ``text.regex_extract`` /
``text.regex_replace``, ``data.batch`` ``prefer_cut_pattern``):

* a repeated group (any ``{m,n}`` with n > 1, ``+``, ``*``) whose body can vary
  in length and where one round's end is not fixed: its growing tail can run into
  the next round's start — ``(a+)+``, ``(a{1,3})+``, ``(\\d\\d?)*``,
  ``(\\w+\\s?)*`` — or a growing piece can swallow the character that ends the
  round — ``(?:\\w+x)+``. ``(?:[^,]*,)*`` and ``(?:a\\s*)+`` stay allowed (each
  round ends in a character nothing before it can take);
* alternatives inside such a repeat that can start with the same character
  (or be empty) — ``(a|ab)*``, ``(?:aa|a)+``;
* a repeat of something that can match nothing — ``(a*)*``.

Strict level (``data.check_items`` ``pattern`` checks) adds:

* two growing pieces side by side that can take the same characters —
  ``\\w+\\w*``, ``.*\\d+``;
* two or more unbounded "match anything" pieces (``.*``, ``.+``, ``[\\s\\S]*``,
  ``[^x]*``) in a pattern not anchored at its start (``^`` / ``\\A``) — ``.*a.*b``
  is cubic on hostile text even at the cap; ``^.*award.*$`` is allowed;
* back-references.

Other polynomial shapes (``\\w+-?\\w+-?\\w+``, ``.*a.*b``) are NOT refused — they
are common in safe patterns (``^.*award.*$``, ``\\b\\w+(?:\\s+\\w+){0,3}\\s+award``);
the text cap bounds them.

A group repeated with disjoint edges stays allowed — ``(?:\\S+\\s+){0,6}`` (each
round ends in a space and starts with a non-space) — as does
``\\d{1,3}(?:,\\d{3})*``. No judge removes the ordinary cost of searching (a
single growing piece is still read from every start), so strict callers also cap
the text a pattern reads (``data.check_items`` ``max_text_chars``).

Character sets are compared over the characters the pattern names, every
whitespace character, ASCII and Latin, plus three stand-ins for "any other
letter / digit / symbol", so ``[б-я]`` meets ``б`` and ``\\w`` meets any letter
outside the sample. Unknown shapes count as overlapping (the judge errs toward
refusing).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

try:  # Python 3.11+: the parser moved under ``re``.
    from re import _constants as _c  # type: ignore[attr-defined]
    from re import _parser as _p  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover - older interpreters
    import sre_constants as _c  # type: ignore[no-redef]
    import sre_parse as _p  # type: ignore[no-redef]

#: The longest pattern a strict caller accepts (characters).
MAX_PATTERN_LENGTH = 500

Level = Literal["strict", "exponential"]

#: A set missing at most this many real characters counts as "match anything" (``[^x]``, ``.``).
_NEAR_UNIVERSAL_MISSING = 3

#: Stand-ins for characters outside the enumerated alphabet (never real characters: two+ chars long).
_OTHER_WORD, _OTHER_DIGIT, _OTHER_SYMBOL = "<word>", "<digit>", "<symbol>"
_OTHERS = frozenset({_OTHER_WORD, _OTHER_DIGIT, _OTHER_SYMBOL})
_SPACES: tuple[str, ...] = tuple(chr(c) for c in range(0x3001) if chr(c).isspace())
_SAMPLE: tuple[str, ...] = tuple(chr(c) for c in range(0x250)) + _SPACES + tuple(
    "–—‘’“”…"
)
_CATEGORY: dict[str, tuple[re.Pattern[str], frozenset[str]]] = {
    "CATEGORY_DIGIT": (re.compile(r"\d"), frozenset({_OTHER_DIGIT})),
    "CATEGORY_NOT_DIGIT": (re.compile(r"\D"), frozenset({_OTHER_WORD, _OTHER_SYMBOL})),
    "CATEGORY_SPACE": (re.compile(r"\s"), frozenset()),
    "CATEGORY_NOT_SPACE": (re.compile(r"\S"), _OTHERS),
    "CATEGORY_WORD": (re.compile(r"\w"), frozenset({_OTHER_WORD, _OTHER_DIGIT})),
    "CATEGORY_NOT_WORD": (re.compile(r"\W"), frozenset({_OTHER_SYMBOL})),
    "CATEGORY_LINEBREAK": (re.compile(r"\n"), frozenset()),
    "CATEGORY_NOT_LINEBREAK": (re.compile(r"[^\n]"), _OTHERS),
}


class UnsafePatternError(ValueError):
    """A pattern that is invalid, too long, or could backtrack catastrophically."""


@dataclass(frozen=True)
class _Info:
    first: frozenset[str]
    last: frozenset[str]
    chars: frozenset[str]
    nullable: bool
    elastic: bool
    zero_width: bool = False
    #: The top-level pieces of a sequence (empty for a single piece), for the round-end rule.
    parts: tuple[_Info, ...] = ()


_EMPTY: frozenset[str] = frozenset()
_ZERO = _Info(_EMPTY, _EMPTY, _EMPTY, True, False, zero_width=True)


def _pattern_chars(items: Iterable) -> set[str]:
    """Every character a parsed pattern names (literals, range ends), so the alphabet holds them."""
    out: set[str] = set()
    for op, av in items:
        name = str(op)
        if name in ("LITERAL", "NOT_LITERAL"):
            out.add(chr(av))
        elif name == "IN":
            for iop, iav in av:
                if str(iop) == "LITERAL":
                    out.add(chr(iav))
                elif str(iop) == "RANGE":
                    out.update({chr(iav[0]), chr(iav[1])})
        elif name == "SUBPATTERN":
            out |= _pattern_chars(av[-1])
        elif name in ("MAX_REPEAT", "MIN_REPEAT", "POSSESSIVE_REPEAT"):
            out |= _pattern_chars(av[2])
        elif name == "BRANCH":
            for b in av[1]:
                out |= _pattern_chars(b)
        elif name in ("ASSERT", "ASSERT_NOT"):
            out |= _pattern_chars(av[1])
        elif name == "ATOMIC_GROUP":
            out |= _pattern_chars(av)
    return out


class _Judge:
    def __init__(self, pattern: str, ic: bool, level: Level, named: set[str]) -> None:
        self.pattern = pattern
        self.ic = ic
        self.strict = level == "strict"
        cased = {v for c in named for v in (c, c.lower(), c.upper()) if len(v) == 1}
        self.alphabet: tuple[str, ...] = tuple(sorted(set(_SAMPLE) | cased))
        self.everything = frozenset(self.alphabet) | _OTHERS
        #: Unbounded "match anything" pieces seen (``.*``, ``[^x]+``) — strict refuses two unanchored.
        self.anything_runs = 0

    # -- character sets -------------------------------------------------- #
    def _where(self, pred) -> frozenset[str]:
        return frozenset(c for c in self.alphabet if pred(c))

    def _either_case(self, s: frozenset[str]) -> frozenset[str]:
        real = {c for c in s if len(c) == 1}
        return s | self._where(lambda c: c.lower() in real or c.upper() in real or c.casefold() in real)

    def _literal(self, code: int) -> frozenset[str]:
        s = frozenset({chr(code)})
        return self._either_case(s) if self.ic else s

    def _class(self, items: list) -> frozenset[str]:
        negate = False
        out: set[str] = set()
        for op, av in items:
            name = str(op)
            if name == "NEGATE":
                negate = True
            elif name == "LITERAL":
                out.add(chr(av))
            elif name == "RANGE":
                lo, hi = av
                inside = self._where(lambda c, lo=lo, hi=hi: lo <= ord(c) <= hi)
                out |= inside
                if len(inside) < hi - lo + 1:  # the range reaches characters the alphabet does not list
                    out |= _OTHERS
            elif name == "CATEGORY":
                rx, others = _CATEGORY.get(str(av), (None, _OTHERS))
                out |= (self._where(lambda c, rx=rx: bool(rx.match(c))) if rx else frozenset(self.alphabet))
                out |= others
            else:  # an unfamiliar set member: it may be anything
                out |= self.everything
        got = self._either_case(frozenset(out)) if self.ic else frozenset(out)
        return frozenset(self.everything - got) if negate else got

    # -- the judge ------------------------------------------------------- #
    def refuse(self, why: str) -> UnsafePatternError:
        return UnsafePatternError(f"Pattern '{self.pattern[:80]}' could take too long to run: {why}.")

    def seq(self, items, in_repeat: bool) -> _Info:
        infos = [self.node(op, av, in_repeat) for op, av in items]
        solid = [i for i in infos if not i.zero_width]
        if self.strict:
            for a, b in zip(solid, solid[1:], strict=False):
                if a.elastic and b.elastic and a.last & b.first:
                    raise self.refuse(
                        "two growing pieces side by side can take the same characters (like \\w+\\w* "
                        "or .*\\d+) — make the edge between them a character only one of them takes"
                    )
        first: set[str] = set()
        for i in solid:
            first |= i.first
            if not i.nullable:
                break
        last: set[str] = set()
        for i in reversed(solid):
            last |= i.last
            if not i.nullable:
                break
        chars: set[str] = set()
        for i in solid:
            chars |= i.chars
        return _Info(
            first=frozenset(first), last=frozenset(last), chars=frozenset(chars),
            nullable=all(i.nullable for i in solid),
            elastic=any(i.elastic for i in solid),
            zero_width=not solid,
            parts=tuple(solid),
        )

    def _round_end_is_ambiguous(self, body: _Info) -> bool:
        """A repeated body's round can end in more than one place: its growing tail can run into
        the next round's start, or a growing piece can swallow the fixed character that ends it."""
        parts = body.parts or (body,)
        while len(parts) == 1 and parts[0].parts:
            parts = parts[0].parts
        tail: set[str] = set()
        end: _Info | None = None
        at = len(parts)
        for at in range(len(parts) - 1, -1, -1):
            p = parts[at]
            if p.elastic:
                tail |= p.last
                if not p.nullable:
                    break
            else:
                end = p
                break
        if tail & body.first:
            return True
        if end is not None:
            swallowing: set[str] = set()
            for p in parts[:at]:
                if p.elastic:
                    swallowing |= p.chars
            return bool(swallowing & end.chars)
        return False

    def node(self, op, av, in_repeat: bool) -> _Info:
        name = str(op)
        if name in ("LITERAL", "NOT_LITERAL", "ANY", "IN"):
            if name == "LITERAL":
                s = self._literal(av)
            elif name == "NOT_LITERAL":
                s = frozenset(self.everything - self._literal(av))
            elif name == "ANY":
                s = self.everything
            else:
                s = self._class(av)
            return _Info(s, s, s, False, False)
        if name == "AT":
            return _ZERO
        if name in ("ASSERT", "ASSERT_NOT"):
            self.seq(av[1], False)
            return _ZERO
        if name == "SUBPATTERN":
            return self.seq(av[-1], in_repeat)
        if name == "ATOMIC_GROUP":
            info = self.seq(av, False)  # an atomic group never backtracks into itself
            return _Info(info.first, info.last, info.chars, info.nullable, info.elastic)
        if name == "BRANCH":
            branches = [self.seq(b, in_repeat) for b in av[1]]
            if in_repeat:
                for x in range(len(branches)):
                    for y in range(x + 1, len(branches)):
                        if branches[x].first & branches[y].first or branches[x].nullable or branches[y].nullable:
                            raise self.refuse(
                                "alternatives inside a repeat can start the same way (like (a|ab)* or "
                                "(?:aa|a)+) — give each alternative a different first character"
                            )
            union = frozenset().union
            return _Info(
                union(*(b.first for b in branches)), union(*(b.last for b in branches)),
                union(*(b.chars for b in branches)),
                any(b.nullable for b in branches),
                any(b.elastic for b in branches) or len({b.nullable for b in branches}) > 1,
            )
        if name in ("MAX_REPEAT", "MIN_REPEAT", "POSSESSIVE_REPEAT"):
            lo, hi, body_items = av
            varies = hi != lo
            repeats = hi > 1 or hi == _c.MAXREPEAT
            if name == "POSSESSIVE_REPEAT":
                body = self.seq(body_items, False)  # possessive: never gives back, no ambiguity
                return _Info(body.first, body.last, body.chars, lo == 0 or body.nullable, varies or body.elastic)
            body = self.seq(body_items, in_repeat or repeats)
            if (
                hi == _c.MAXREPEAT and not body.elastic and body.first == body.chars
                and _OTHERS <= body.chars and len(self.everything - body.chars) <= _NEAR_UNIVERSAL_MISSING
            ):
                self.anything_runs += 1
            if repeats and body.nullable:
                raise self.refuse("a repeat of something that can match nothing (like (a*)*)")
            if repeats and body.elastic and self._round_end_is_ambiguous(body):
                raise self.refuse(
                    "a repeated group whose rounds can end in more than one place (like (a+)+, "
                    "(\\d\\d?)*, (\\w+\\s?)* or (?:\\w+x)+) — end each round with a character "
                    "nothing else in the round can take"
                )
            return _Info(body.first, body.last, body.chars, lo == 0 or body.nullable, varies or body.elastic)
        if name in ("GROUPREF", "GROUPREF_EXISTS", "GROUPREF_IGNORE"):
            if self.strict:
                raise UnsafePatternError(f"Pattern '{self.pattern[:80]}': back-references (\\1) are not allowed.")
            s = self.everything  # it repeats earlier text: any length, any characters
            return _Info(s, s, s, True, True)
        raise UnsafePatternError(f"Pattern '{self.pattern[:80]}': '{name}' is not supported here.")


def judge(pattern: str, flags: int = 0, *, level: Level = "strict") -> None:
    """Raise :class:`UnsafePatternError` when ``pattern`` (already known to compile) is unsafe at ``level``."""
    parsed = _p.parse(pattern, flags)
    ic = bool(parsed.state.flags & re.IGNORECASE)
    items = list(parsed)
    j = _Judge(pattern, ic, level, _pattern_chars(items))
    j.seq(items, False)
    anchored = bool(items) and str(items[0][0]) == "AT" and str(items[0][1]) in ("AT_BEGINNING", "AT_BEGINNING_STRING")
    if j.strict and j.anything_runs >= 2 and not anchored:
        raise j.refuse(
            "two \"match anything\" runs (like .*a.*b) in a pattern that can start anywhere — anchor it "
            "with ^ or narrow one of them"
        )


def compile_safe(
    pattern: str,
    *,
    ignore_case: bool = False,
    flags: int = 0,
    level: Level = "strict",
    max_length: int | None = MAX_PATTERN_LENGTH,
) -> re.Pattern[str]:
    """Compile ``pattern`` or raise :class:`UnsafePatternError` with a sentence saying why."""
    if not isinstance(pattern, str) or not pattern:
        raise UnsafePatternError("A pattern must be a non-empty text.")
    if max_length is not None and len(pattern) > max_length:
        raise UnsafePatternError(f"Pattern '{pattern[:80]}…' is {len(pattern)} characters; at most {max_length}.")
    flags |= re.IGNORECASE if ignore_case else 0
    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        raise UnsafePatternError(f"Pattern '{pattern[:80]}' is not a valid regular expression: {e}.") from e
    judge(pattern, flags, level=level)
    return compiled


__all__ = ["MAX_PATTERN_LENGTH", "UnsafePatternError", "compile_safe", "judge"]
