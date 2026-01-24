"""Unicode word boundaries.

`UAX #29: Unicode Text Segmentation (Unicode 16.0.0)
<https://www.unicode.org/reports/tr29/tr29-45.html>`_
"""

from typing import Iterator, Optional

from uniseg.breaking import (Breakable, Breakables, Run, TailorFunction, boundaries,
                             break_units)
from uniseg.db import get_handle, get_value
from uniseg.emoji import extended_pictographic
from uniseg.unicodeproperty import EnumProperty, PropertyFunction, character_property

__all__ = [
    'WordBreak',
    'WB',
    'word_break',
    'word_breakables',
    'word_boundaries',
    'words',
]


class WordBreak(EnumProperty):
    """Word_Break property values."""

    __propname__ = 'WordBreak'

    OTHER = 'Other'
    """Word_Break property value Other"""

    CR = 'CR'
    """Word_Break property value CR"""

    LF = 'LF'
    """Word_Break property value LF"""

    NEWLINE = 'Newline'
    """Word_Break property value Newline"""

    EXTEND = 'Extend'
    """Word_Break property value Extend"""

    ZWJ = 'ZWJ'
    """Word_Break property value ZWJ"""

    REGIONAL_INDICATOR = 'Regional_Indicator'
    """Word_Break property value Regional_Indicator"""

    FORMAT = 'Format'
    """Word_Break property value Format"""

    KATAKANA = 'Katakana'
    """Word_Break property value Katakana"""

    HEBREW_LETTER = 'Hebrew_Letter'
    """Word_Break property value Hebrew_Letter"""

    ALETTER = 'ALetter'
    """Word_Break property value ALetter"""

    SINGLE_QUOTE = 'Single_Quote'
    """Word_Break property value Single_Quote"""

    DOUBLE_QUOTE = 'Double_Quote'
    """Word_Break property value Double_Quote"""

    MIDNUMLET = 'MidNumLet'
    """Word_Break property value MidNumLet"""

    MIDLETTER = 'MidLetter'
    """Word_Break property value MidLetter"""

    MIDNUM = 'MidNum'
    """Word_Break property value MidNum"""

    NUMERIC = 'Numeric'
    """Word_Break property value Numeric"""

    EXTENDNUMLET = 'ExtendNumLet'
    """Word_Break property value ExtendNumLet"""

    WSEGSPACE = 'WSegSpace'
    """Word_Break property value WSegSpace"""


# type alias for `WordBreak`
WB = WordBreak


_H_WB = get_handle('Word_Break')


@character_property
def word_break(c: str, /) -> WordBreak:
    R"""Return the Word_Break value assigned to the code point `c`.

    `c` must be a single Unicode code point string.

    >>> word_break('\r')
    WordBreak.CR
    >>> word_break('\x0b')
    WordBreak.NEWLINE
    >>> word_break('ア')
    WordBreak.KATAKANA
    """
    return WordBreak(get_value(_H_WB, ord(c)) or 'Other')


_AHLETTER = (WB.ALETTER, WB.HEBREW_LETTER)
_MIDNUMLETQ = (WB.MIDNUMLET, WB.SINGLE_QUOTE)


def word_breakables(
    s: str, /, *, property: PropertyFunction[WordBreak] = word_break
) -> Breakables:
    R"""Iterate word breaking opportunities for every position of `s`

    1 for "break" and 0 for "do not break".  The length of iteration
    will be the same as ``len(s)``.

    >>> list(word_breakables('ABC'))
    [1, 0, 0]
    >>> list(word_breakables('Hello, world.'))
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1]
    >>> list(word_breakables('\x01\u0308\x01'))
    [1, 0, 1]
    """
    if not s:
        return iter([])

    run = Run(s, property)
    while run.walk():
        # WB3
        if run.prev == WB.CR and run.curr == WB.LF:
            run.do_not_break_here()
        # WB3a
        elif run.prev in (WB.NEWLINE, WB.CR, WB.LF):
            run.break_here()
        # WB3b
        elif run.curr in (WB.NEWLINE, WB.CR, WB.LF):
            run.break_here()
        # WB3c
        elif run.prev == WB.ZWJ and run.cc and extended_pictographic(run.cc):
            run.do_not_break_here()
        # WB3d
        elif run.prev == run.curr == WB.WSEGSPACE:
            run.do_not_break_here()
        # WB4
        elif run.curr in (WB.FORMAT, WB.EXTEND, WB.ZWJ):
            run.do_not_break_here()
    # WB4
    run.set_skip_table(x not in (WB.EXTEND, WB.FORMAT, WB.ZWJ)
                       for x in run.attributes())
    run.head()
    while run.walk():
        # WB5
        if run.prev in _AHLETTER and run.curr in _AHLETTER:
            run.do_not_break_here()
        # WB6
        elif (
            run.prev in _AHLETTER
            and run.curr in (WB.MIDLETTER,) + _MIDNUMLETQ
            and run.next in _AHLETTER
        ):
            run.do_not_break_here()
        # WB7
        elif (
            run.attr(-2) in _AHLETTER
            and run.prev in (WB.MIDLETTER,) + _MIDNUMLETQ
            and run.curr in _AHLETTER
        ):
            run.do_not_break_here()
        # WB7a
        elif run.prev == WB.HEBREW_LETTER and run.curr == WB.SINGLE_QUOTE:
            run.do_not_break_here()
        # WB7b
        elif (
            run.prev == WB.HEBREW_LETTER
            and run.curr == WB.DOUBLE_QUOTE
            and run.next == WB.HEBREW_LETTER
        ):
            run.do_not_break_here()
        # WB7c
        elif (
            run.attr(-2) == WB.HEBREW_LETTER
            and run.prev == WB.DOUBLE_QUOTE
            and run.curr == WB.HEBREW_LETTER
        ):
            run.do_not_break_here()
        # WB8
        elif run.prev == run.curr == WB.NUMERIC:
            run.do_not_break_here()
        # WB9
        elif run.prev in _AHLETTER and run.curr == WB.NUMERIC:
            run.do_not_break_here()
        # WB10
        elif run.prev == WB.NUMERIC and run.curr in _AHLETTER:
            run.do_not_break_here()
        # WB11
        elif (
            run.attr(-2) == WB.NUMERIC
            and run.prev in (WB.MIDNUM,) + _MIDNUMLETQ
            and run.curr == WB.NUMERIC
        ):
            run.do_not_break_here()
        # WB12
        elif (
            run.prev == WB.NUMERIC
            and run.curr in (WB.MIDNUM,) + _MIDNUMLETQ
            and run.next == WB.NUMERIC
        ):
            run.do_not_break_here()
        # WB13
        elif run.prev == run.curr == WB.KATAKANA:
            run.do_not_break_here()
        # WB13a
        elif (
            run.prev in _AHLETTER + (WB.NUMERIC, WB.KATAKANA, WB.EXTENDNUMLET)
            and run.curr == WB.EXTENDNUMLET
        ):
            run.do_not_break_here()
        # WB13b
        elif (
            run.prev == WB.EXTENDNUMLET
            and run.curr in _AHLETTER + (WB.NUMERIC, WB.KATAKANA)
        ):
            run.do_not_break_here()
    run.head()
    # WB15, WB16
    while 1:
        while run.curr != WB.REGIONAL_INDICATOR:
            if not run.walk():
                break
        if not run.walk():
            break
        while run.prev == run.curr == WB.REGIONAL_INDICATOR:
            run.do_not_break_here()
            if not run.walk():
                break
            if not run.walk():
                break
    # WB999
    run.set_default(Breakable.Break)
    return run.literal_breakables()


def word_boundaries(
    s: str,
    /,
    *,
    property: PropertyFunction[WordBreak] = word_break,
    tailor: Optional[TailorFunction] = None,
) -> Iterator[int]:
    """Iterate indices of the word boundaries of `s`

    This function yields indices from the first boundary position (> 0)
    to the end of the string (== len(s)).
    """
    breakables = word_breakables(s, property=property)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return boundaries(breakables)


def words(
    s: str,
    /,
    *,
    property: PropertyFunction[WordBreak] = word_break,
    tailor: Optional[TailorFunction] = None,
) -> Iterator[str]:
    """Iterate *user-perceived* words of `s`

    These examples bellow is from
    http://www.unicode.org/reports/tr29/tr29-15.html#Word_Boundaries

    >>> s = 'The quick (“brown”) fox can’t jump 32.3 feet, right?'
    >>> '|'.join(words(s))
    'The| |quick| |(|“|brown|”|)| |fox| |can’t| |jump| |32.3| |feet|,| |right|?'
    >>> list(words(''))
    []
    """
    breakables = word_breakables(s, property=property)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return break_units(s, breakables)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
