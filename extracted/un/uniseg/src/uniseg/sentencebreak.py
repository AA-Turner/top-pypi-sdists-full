"""Unicode sentence boundaries.

`UAX #29: Unicode Text Segmentation (Unicode 16.0.0)
<https://www.unicode.org/reports/tr29/tr29-45.html>`_
"""

from collections.abc import Iterator
from typing import Optional

from uniseg.breaking import (Breakable, Breakables, Run, TailorFunction, boundaries,
                             break_units)
from uniseg.db import get_handle, get_value
from uniseg.unicodeproperty import EnumProperty, PropertyFunction, character_property

__all__ = [
    'SentenceBreak',
    'SB',
    'sentence_break',
    'sentence_breakables',
    'sentence_boundaries',
    'sentences',
]


_H_SB = get_handle('Sentence_Break')


class SentenceBreak(EnumProperty):
    """Sentence_Break property values."""

    __propname__ = 'SentenceBreak'

    OTHER = 'Other'
    """Sentence_Break property value Other"""

    CR = 'CR'
    """Sentence_Break property value CR"""

    LF = 'LF'
    """Sentence_Break property value LF"""

    EXTEND = 'Extend'
    """Sentence_Break property value Extend"""

    SEP = 'Sep'
    """Sentence_Break property value Sep"""

    FORMAT = 'Format'
    """Sentence_Break property value Format"""

    SP = 'Sp'
    """Sentence_Break property value Sp"""

    LOWER = 'Lower'
    """Sentence_Break property value Lower"""

    UPPER = 'Upper'
    """Sentence_Break property value Upper"""

    OLETTER = 'OLetter'
    """Sentence_Break property value OLetter"""

    NUMERIC = 'Numeric'
    """Sentence_Break property value Numeric"""

    ATERM = 'ATerm'
    """Sentence_Break property value ATerm"""

    SCONTINUE = 'SContinue'
    """Sentence_Break property value SContinue"""

    STERM = 'STerm'
    """Sentence_Break property value STerm"""

    CLOSE = 'Close'
    """Sentence_Break property value Close"""


# type alias for `SentenceBreak`
SB = SentenceBreak


@character_property
def sentence_break(c: str, /) -> SentenceBreak:
    R"""Return the Sentence_Break value assigned to the code point `c`.

    `c` must be a single Unicode code point string.

    >>> sentence_break('\r')
    SentenceBreak.CR
    >>> sentence_break(' ')
    SentenceBreak.SP
    >>> sentence_break('a')
    SentenceBreak.LOWER
    >>> sentence_break('/')
    SentenceBreak.OTHER
    """
    return SentenceBreak(get_value(_H_SB, ord(c)) or 'Other')


_PARASEP = (SB.SEP, SB.CR, SB.LF)
_SATERM = (SB.STERM, SB.ATERM)


def sentence_breakables(
    s: str, /, *, property: PropertyFunction[SentenceBreak] = sentence_break
) -> Breakables:
    R"""Iterate sentence breaking opportunities for every position of
    `s`.

    1 for "break" and 0 for "do not break".  The length of iteration
    will be the same as ``len(s)``.

    >>> from pprint import pp
    >>> s = 'He said, \u201cAre you going?\u201d John shook his head.'
    >>> pp(list(sentence_breakables(s)), width=76, compact=True)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """
    run = Run(s, property)
    # SB1
    run.break_here()
    while run.walk():
        # SB3
        if run.prev == SB.CR and run.curr == SB.LF:
            run.do_not_break_here()
        # SB4
        elif run.prev in _PARASEP:
            run.break_here()
    # SB5
    run.set_skip_table(x not in (SB.EXTEND, SB.FORMAT) for x in run.attributes())

    run.head()
    while run.walk():
        # SB6
        if run.prev == SB.ATERM and run.curr == SB.NUMERIC:
            run.do_not_break_here()
        # SB7
        elif (
            run.attr(-2) in (SB.UPPER, SB.LOWER)
            and run.prev == SB.ATERM
            and run.curr == SB.UPPER
        ):
            run.do_not_break_here()
        # SB8
        elif (
            run.is_following(SB.SP, greedy=True)
            .is_following(SB.CLOSE, greedy=True).prev == SB.ATERM
            and (
                (
                    run.curr in (SB.EXTEND, SB.FORMAT, SB.SP,
                                 SB.NUMERIC, SB.SCONTINUE, SB.CLOSE)
                    and run.is_leading((SB.EXTEND, SB.FORMAT, SB.SP, SB.NUMERIC,
                                        SB.SCONTINUE, SB.CLOSE), greedy=True)
                    .next == SB.LOWER
                )
                or run.curr == SB.LOWER
            )
        ):
            run.do_not_break_here()
        # SB8a
        elif (
            run.is_following(SB.SP, greedy=True)
            .is_following(SB.CLOSE, greedy=True).prev in _SATERM
            and run.curr in (SB.SCONTINUE,) + _SATERM
        ):
            run.do_not_break_here()
        # SB9
        elif (
            run.is_following(SB.CLOSE, greedy=True).prev in _SATERM
            and run.curr in (SB.CLOSE, SB.SP) + _PARASEP
        ):
            run.do_not_break_here()
        # SB10
        elif (
            run.is_following(SB.SP, greedy=True)
            .is_following(SB.CLOSE, greedy=True).prev in _SATERM
            and run.curr in (SB.SP,) + _PARASEP
        ):
            run.do_not_break_here()
        # SB11
        elif (
            run.is_following(SB.SP, greedy=True)
            .is_following(SB.CLOSE, greedy=True).prev in _SATERM
            or run.is_following(_PARASEP, noskip=True)
            .is_following(SB.SP, greedy=True)
            .is_following(SB.CLOSE, greedy=True).prev in _SATERM
        ):
            run.break_here()
        else:
            run.do_not_break_here()
    # SB998
    run.set_default(Breakable.DoNotBreak)
    return run.literal_breakables()


def sentence_boundaries(
    s: str,
    /,
    *,
    property: PropertyFunction[SentenceBreak] = sentence_break,
    tailor: Optional[TailorFunction] = None,
) -> Iterator[int]:
    R"""Iterate indices of the sentence boundaries of `s`.

    This function yields from 0 to the end of the string (== len(s)).

    >>> list(sentence_boundaries('ABC'))
    [0, 3]
    >>> s = 'He said, “Are you going?” John shook his head.'
    >>> list(sentence_boundaries(s))
    [0, 26, 46]
    >>> list(sentence_boundaries(''))
    []
    """
    breakables = sentence_breakables(s, property=property)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return boundaries(breakables)


def sentences(
    s: str,
    /,
    *,
    property: PropertyFunction[SentenceBreak] = sentence_break,
    tailor: Optional[TailorFunction] = None,
) -> Iterator[str]:
    R"""Iterate every sentence of `s`.

    >>> s = 'He said, “Are you going?” John shook his head.'
    >>> list(sentences(s))
    ['He said, “Are you going?” ', 'John shook his head.']
    """
    breakables = sentence_breakables(s, property=property)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return break_units(s, breakables)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
