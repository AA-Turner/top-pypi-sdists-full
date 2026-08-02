"""Unicode derived properties.

`UAX #44: Unicode Character Database (16.0.0)
<https://www.unicode.org/reports/tr44/tr44-34.html>`_
"""

from uniseg.db import get_handle, get_value
from uniseg.unicodeproperty import EnumProperty, character_property

__all__ = [
    'IndicConjunctBreak',
    'InCB',
    'math',
    'alphabetic',
    'lowercase',
    'uppercase',
    'cased',
    'case_ignorable',
    'changes_when_lowercased',
    'changes_when_uppercased',
    'changes_when_titlecased',
    'changes_when_casefolded',
    'changes_when_casemapped',
    'id_start',
    'id_continue',
    'xid_start',
    'xid_continue',
    'default_ignorable_code_point',
    'grapheme_extend',
    'grapheme_base',
    'indic_conjunct_break',
]


_H_MATH = get_handle('Math')
_H_ALPHABETIC = get_handle('Alphabetic')
_H_LOWERCASE = get_handle('Lowercase')
_H_UPPERCASE = get_handle('Uppercase')
_H_CASED = get_handle('Cased')
_H_CASE_IGNORABLE = get_handle('Case_Ignorable')
_H_CHANGES_WHEN_LOWERCASED = get_handle('Changes_When_Lowercased')
_H_CHANGES_WHEN_UPPERCASED = get_handle('Changes_When_Uppercased')
_H_CHANGES_WHEN_TITLECASED = get_handle('Changes_When_Titlecased')
_H_CHANGES_WHEN_CASEFOLDED = get_handle('Changes_When_Casefolded')
_H_CHANGES_WHEN_CASEMAPPED = get_handle('Changes_When_Casemapped')
_H_ID_START = get_handle('ID_Start')
_H_ID_CONTINUE = get_handle('ID_Continue')
_H_XID_START = get_handle('XID_Start')
_H_XID_CONTINUE = get_handle('XID_Continue')
_H_DEFAULT_IGNORABLE_CODE_POINT = get_handle('Default_Ignorable_Code_Point')
_H_GRAPHEME_EXTEND = get_handle('Grapheme_Extend')
_H_GRAPHEME_BASE = get_handle('Grapheme_Base')
_H_INDIC_CONJUNCT_BREAK = get_handle('InCB')


class IndicConjunctBreak(EnumProperty):
    """Derived Property: Indic_Conjunct_Break."""

    __propname__ = 'Indic_Conjunct_Break'

    NONE = 'None'
    """Indic_Conjunct_Break=None"""

    LINKER = 'Linker'
    """Indic_Conjunct_Break=Linker"""

    CONSONANT = 'Consonant'
    """Indic_Conjunct_Break=Consonant"""

    EXTEND = 'Extend'
    """Indic_Conjunct_Break=Extend"""


InCB = IndicConjunctBreak


@character_property
def math(c: str, /) -> bool:
    """Return Math boolean derived Unicode property value for `c`.

    >>> math('A')
    False
    >>> math('+')
    True
    """
    return bool(get_value(_H_MATH, ord(c)))


@character_property
def alphabetic(c: str, /) -> bool:
    """Return Alphabetic boolean derived Unicode property value for `c`.

    >>> alphabetic('A')
    True
    >>> alphabetic('1')
    False
    """
    return bool(get_value(_H_ALPHABETIC, ord(c)))


@character_property
def lowercase(c: str, /) -> bool:
    """Return Lowercase boolean derived Unicode property value for `c`.

    >>> lowercase('A')
    False
    >>> lowercase('a')
    True
    """
    return bool(get_value(_H_LOWERCASE, ord(c)))


@character_property
def uppercase(c: str, /) -> bool:
    """Return Uppercase boolean derived Unicode property value for `c`.

    >>> uppercase('A')
    True
    >>> uppercase('a')
    False
    """
    return bool(get_value(_H_UPPERCASE, ord(c)))


@character_property
def cased(c: str, /) -> bool:
    """Return Cased boolean derived Unicode property value for `c`.

    >>> cased('A')
    True
    >>> cased('a')
    True
    >>> cased('*')
    False
    """
    return bool(get_value(_H_CASED, ord(c)))


@character_property
def case_ignorable(c: str, /) -> bool:
    """Return Case_Ignorable boolean derived Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> case_ignorable('A')
    False
    >>> case_ignorable('.')
    True
    """
    return bool(get_value(_H_CASE_IGNORABLE, ord(c)))


@character_property
def changes_when_lowercased(c: str, /) -> bool:
    """Return Changes_When_Lowercased boolean derived Unicode property value
    for `c`.

    `c` must be a single Unicode character (code point).

    >>> changes_when_lowercased('A')
    True
    >>> changes_when_lowercased('a')
    False
    """
    return bool(get_value(_H_CHANGES_WHEN_LOWERCASED, ord(c)))


@character_property
def changes_when_uppercased(c: str, /) -> bool:
    """Return Changes_When_Uppercased boolean derived Unicode property value
    for `c`.

    `c` must be a single Unicode character (code point).

    >>> changes_when_uppercased('A')
    False
    >>> changes_when_uppercased('a')
    True
    """
    return bool(get_value(_H_CHANGES_WHEN_UPPERCASED, ord(c)))


@character_property
def changes_when_titlecased(c: str, /) -> bool:
    """Return Changes_When_Titlecased boolean derived Unicode property value
    for `c`.

    `c` must be a single Unicode character (code point).

    >>> changes_when_titlecased('A')
    False
    >>> changes_when_titlecased('a')
    True
    """
    return bool(get_value(_H_CHANGES_WHEN_TITLECASED, ord(c)))


@character_property
def changes_when_casefolded(c: str, /) -> bool:
    """Return Changes_When_Casefolded boolean derived Unicode property value
    for `c`.

    `c` must be a single Unicode character (code point).

    >>> changes_when_casefolded('A')
    True
    >>> changes_when_casefolded('a')
    False
    """
    return bool(get_value(_H_CHANGES_WHEN_CASEFOLDED, ord(c)))


@character_property
def changes_when_casemapped(c: str, /) -> bool:
    """Return Changes_When_Casemapped boolean derived Unicode property value
    for `c`.

    `c` must be a single Unicode character (code point).

    >>> changes_when_casemapped('A')
    True
    >>> changes_when_casemapped('a')
    True
    >>> changes_when_casemapped('1')
    False
    """
    return bool(get_value(_H_CHANGES_WHEN_CASEMAPPED, ord(c)))


@character_property
def id_start(c: str, /) -> bool:
    """Return ID_Start boolean derived Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> id_start('A')
    True
    >>> id_start('a')
    True
    >>> id_start('1')
    False
    """
    return bool(get_value(_H_ID_START, ord(c)))


@character_property
def id_continue(c: str, /) -> bool:
    """Return ID_Continue boolean derived Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> id_continue('A')
    True
    >>> id_continue('a')
    True
    >>> id_continue('1')
    True
    >>> id_continue('.')
    False
    """
    return bool(get_value(_H_ID_CONTINUE, ord(c)))


@character_property
def xid_start(c: str, /) -> bool:
    """Return XID_Start boolean derived Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> xid_start('A')
    True
    >>> xid_start('a')
    True
    >>> xid_start('1')
    False
    """
    return bool(get_value(_H_XID_START, ord(c)))


@character_property
def xid_continue(c: str, /) -> bool:
    """Return XID_Continue boolean derived Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> xid_continue('A')
    True
    >>> xid_continue('a')
    True
    >>> xid_continue('1')
    True
    >>> xid_continue('.')
    False
    """
    return bool(get_value(_H_XID_CONTINUE, ord(c)))


@character_property
def default_ignorable_code_point(c: str, /) -> bool:
    """Return Default_Ignorable_Code_Point boolean derived Unicode property
    value for `c`.

    `c` must be a single Unicode character (code point).

    >>> default_ignorable_code_point('A')
    False
    >>> default_ignorable_code_point('\u00ad')
    True
    """
    return bool(get_value(_H_DEFAULT_IGNORABLE_CODE_POINT, ord(c)))


@character_property
def grapheme_extend(c: str, /) -> bool:
    """Return Grapheme_Extend boolean derived Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> grapheme_extend('A')
    False
    >>> grapheme_extend('\u0300')
    True
    """
    return bool(get_value(_H_GRAPHEME_EXTEND, ord(c)))


@character_property
def grapheme_base(c: str, /) -> bool:
    """Return Grapheme_Base boolean derived Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> grapheme_base('A')
    True
    >>> grapheme_extend('\u0300')
    True
    """
    return bool(get_value(_H_GRAPHEME_BASE, ord(c)))


@character_property
def indic_conjunct_break(c: str, /) -> IndicConjunctBreak:
    """Retrun Indic_Conjunct_Break derived property for `c`.

    `c` must be a single Unicode character (code point).

    >>> indic_conjunct_break('A')
    IndicConjunctBreak.NONE
    >>> indic_conjunct_break('\u094d')
    IndicConjunctBreak.LINKER
    """
    return IndicConjunctBreak(get_value(_H_INDIC_CONJUNCT_BREAK, ord(c)) or 'None')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
