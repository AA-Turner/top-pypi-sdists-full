"""Unicodedata wrapper module."""

try:
    from unicodedata2 import bidirectional
    from unicodedata2 import category as _category
    from unicodedata2 import combining, decimal, decomposition, digit
    from unicodedata2 import east_asian_width as _east_asian_width
    from unicodedata2 import (is_normalized, lookup, mirrored, name, normalize, numeric,
                              ucd_3_2_0, unidata_version)
except ImportError:
    from unicodedata import bidirectional
    from unicodedata import category as _category
    from unicodedata import combining, decimal, decomposition, digit
    from unicodedata import east_asian_width as _east_asian_width
    from unicodedata import (is_normalized, lookup, mirrored, name, normalize, numeric,
                             ucd_3_2_0, unidata_version)

from uniseg.unicodeproperty import EnumProperty

__all__ = [
    'Category',
    'GC',
    'EastAsianWidth',
    'EA',
    'bidirectional',
    'combining',
    'category',
    'east_asian_width',
    'decimal',
    'decomposition',
    'digit',
    'is_normalized',
    'lookup',
    'mirrored',
    'name',
    'normalize',
    'numeric',
    'ucd_3_2_0',
    'unidata_version',
]


class Category(EnumProperty):
    """Unicode General_Category values."""

    LU = 'Lu'
    """General_Category=Uppercase_Letter"""

    LL = 'Ll'
    """General_Category=Lowercase_Letter"""

    LT = 'Lt'
    """General_Category=Titlecase_Letter"""

    LC = 'LC'
    """General_Category=Cased_Letter"""

    LM = 'Lm'
    """General_Category=Modifier_Letter"""

    LO = 'Lo'
    """General_Category=Other_Letter"""

    L = 'L'
    """General_Category=Letter"""

    MN = 'Mn'
    """General_Category=Nonspacing_Mark"""

    MC = 'Mc'
    """General_Category=Spacing_Mark"""

    ME = 'Me'
    """General_Category=Enclosing_Mark"""

    M = 'M'
    """General_Category=Mark"""

    ND = 'Nd'
    """General_Category=Decimal_Number"""

    NL = 'Nl'
    """General_Category=Letter_Number"""

    NO = 'No'
    """General_Category=Other_Number"""

    N = 'N'
    """General_Category=Number"""

    PC = 'Pc'
    """General_Category=Connector_Punctuation"""

    PD = 'Pd'
    """General_Category=Dash_Punctuation"""

    PS = 'Ps'
    """General_Category=Open_Punctuation"""

    PE = 'Pe'
    """General_Category=Close_Punctuation"""

    PI = 'Pi'
    """General_Category=Initial_Punctuation"""

    PF = 'Pf'
    """General_Category=Final_Punctuation"""

    PO = 'Po'
    """General_Category=Other_Punctuation"""

    P = 'P'
    """General_Category=Punctuation"""

    SM = 'Sm'
    """General_Category=Math_Symbol"""

    SC = 'Sc'
    """General_Category=Currency_Symbol"""

    SK = 'Sk'
    """General_Category=Modifier_Symbol"""

    SO = 'So'
    """General_Category=Other_Symbol"""

    S = 'S'
    """General_Category=Symbol"""

    ZS = 'Zs'
    """General_Category=Space_Separator"""

    ZL = 'Zl'
    """General_Category=Line_Separator"""

    ZP = 'Zp'
    """General_Category=Paragraph_Separator"""

    Z = 'Z'
    """General_Category=Separator"""

    CC = 'Cc'
    """General_Category=Control"""

    CF = 'Cf'
    """General_Category=Format"""

    CS = 'Cs'
    """General_Category=Surrogate"""

    CO = 'Co'
    """General_Category=Private_Use"""

    CN = 'Cn'
    """General_Category=Unassigned"""

    C = 'C'
    """General_Category=Other"""


GC = Category


class EastAsianWidth(EnumProperty):
    """Unicode East_Asian_Width values."""

    A = 'A'
    """East_Asian_Width=Ambiguous"""

    F = 'F'
    """East_Asian_Width=Fullwidth"""

    H = 'H'
    """East_Asian_Width=Halfwidth"""

    N = 'N'
    """East_Asian_Width=Neutral"""

    NA = 'Na'
    """East_Asian_Width=Narrow"""

    W = 'W'
    """East_Asian_Width=Wide"""


EA = EastAsianWidth


def category(chr: str, /) -> Category:
    """Return General_Category property value for `chr`."""
    return Category(_category(chr))


def east_asian_width(chr: str, /) -> EastAsianWidth:
    """Return East_Asian_Width property value for `chr`."""
    return EastAsianWidth(_east_asian_width(chr))
