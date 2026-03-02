import re
from collections.abc import Mapping
from typing import Final, Optional

from ._constants import (
    CONSONANTS,
    HEPBURNTAB,
    HEPBURNTAB_H,
    KUNREITAB,
    KUNREITAB_H,
    SPECIALS_HIRA,
    SPECIALS_KATA,
    UNNCCESSARY_APOSTROPHES,
    VOWELS,
)
from ._generator import _pairs as pairs
from ._generator import romkan_from_table

__all__ = [
    "ROMKAN",
    "KANROM",
    "ROMPAT",
    "KANPAT",
    "KUNPAT",
    "HEPPAT",
    "TO_HEPBURN",
    "TO_KUNREI",
    "ROMKAN_H",
    "KANROM_H",
    "ROMPAT_H",
    "KANPAT_H",
    "KUNPAT_H",
    "HEPPAT_H",
    "TO_HEPBURN_H",
    "TO_KUNREI_H",
    "normalize_double_n",
    "to_katakana",
    "to_hiragana",
    "to_kana",
    "to_hepburn",
    "to_kunrei",
    "to_roma",
    "is_consonant",
    "is_vowel",
    "expand_consonant",
    "pairs",  # for compatibility
]

#
# Ruby/Romkan - a Romaji <-> Kana conversion library for Ruby.
#
# Copyright (C) 2001 Satoru Takabayashi <satoru@namazu.org>
#     All rights reserved.
#     This is free software with ABSOLUTELY NO WARRANTY.
#
# You can redistribute it and/or modify it under the terms of
# the Ruby's licence.
#


ROMKAN: Final[Mapping[str, str]]
KANROM: Final[Mapping[str, str]]
ROMPAT: Final[re.Pattern[str]]
KANPAT: Final[re.Pattern[str]]
KUNPAT: Final[re.Pattern[str]]
HEPPAT: Final[re.Pattern[str]]
TO_HEPBURN: Final[Mapping[str, str]]
(
    ROMKAN,
    KANROM,
    ROMPAT,
    KANPAT,
    KUNPAT,
    HEPPAT,
    TO_HEPBURN,
    TO_KUNREI,
) = romkan_from_table(
    kunrei_table=KUNREITAB,
    hepburn_table=HEPBURNTAB,
    specials=SPECIALS_KATA,
)

ROMKAN_H: Final[Mapping[str, str]]
KANROM_H: Final[Mapping[str, str]]
ROMPAT_H: Final[re.Pattern[str]]
KANPAT_H: Final[re.Pattern[str]]
KUNPAT_H: Final[re.Pattern[str]]
HEPPAT_H: Final[re.Pattern[str]]
TO_HEPBURN_H: Final[Mapping[str, str]]
TO_KUNREI_H: Final[Mapping[str, str]]
(
    ROMKAN_H,
    KANROM_H,
    ROMPAT_H,
    KANPAT_H,
    KUNPAT_H,
    HEPPAT_H,
    TO_HEPBURN_H,
    TO_KUNREI_H,
) = romkan_from_table(
    kunrei_table=KUNREITAB_H,
    hepburn_table=HEPBURNTAB_H,
    specials=SPECIALS_HIRA,
)


def normalize_double_n(text: str) -> str:
    """
    Normalize double n.
    """

    # Replace double n with n'
    text = re.sub(r"nn", "n'", text)
    # Remove unnecessary apostrophes
    text = re.sub(UNNCCESSARY_APOSTROPHES, "n", text)

    return text


def to_katakana(text: str) -> str:
    """
    Convert a Romaji (ローマ字) to a Katakana (片仮名).
    """

    text = text.lower()
    text = normalize_double_n(text)

    text = ROMPAT.sub(lambda x: ROMKAN[x.group(0)], text)
    return text


def to_hiragana(text: str) -> str:
    """
    Convert a Romaji (ローマ字) to a Hiragana (平仮名).
    """

    text = text.lower()
    text = normalize_double_n(text)

    text = ROMPAT_H.sub(lambda x: ROMKAN_H[x.group(0)], text)
    return text


def to_kana(text: str) -> str:
    """
    Convert a Romaji (ローマ字) to a Katakana (片仮名). (same as to_katakana)
    """

    return to_katakana(text)


def to_hepburn(text: str) -> str:
    """
    Convert a Kana (仮名) or a Kunrei-shiki Romaji (訓令式ローマ字) to a Hepburn Romaji (ヘボン式ローマ字).
    """

    tmp = text
    tmp = KANPAT.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H.sub(lambda x: KANROM_H[x.group(0)], tmp)

    # Remove unnecessary apostrophes
    tmp = re.sub(UNNCCESSARY_APOSTROPHES, "n", tmp)

    # If unmodified, it's a Kunrei-shiki Romaji -- convert it to a Hepburn Romaji
    if tmp == text:
        tmp = tmp.lower()
        tmp = normalize_double_n(tmp)
        tmp = KUNPAT.sub(lambda x: TO_HEPBURN[x.group(0)], tmp)

    return tmp


def to_kunrei(text: str) -> str:
    """
    Convert a Kana (仮名) or a Hepburn Romaji (ヘボン式ローマ字) to a Kunrei-shiki Romaji (訓令式ローマ字).
    """

    tmp = text
    tmp = KANPAT.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H.sub(lambda x: KANROM_H[x.group(0)], tmp)

    # Remove unnecessary apostrophes
    tmp = re.sub(UNNCCESSARY_APOSTROPHES, "n", tmp)

    # If unmodified, it's a Hepburn Romaji Romaji -- convert it to a Kunrei-shiki Romaji
    # If modified, it's also a Hepburn Romaji Romaji -- convert it to a Kunrei-shiki Romaji
    tmp = tmp.lower()
    tmp = normalize_double_n(tmp)
    tmp = HEPPAT.sub(lambda x: TO_KUNREI[x.group(0)], tmp)

    return tmp


def to_roma(text: str) -> str:
    """
    Convert a Kana (仮名) to a Hepburn Romaji (ヘボン式ローマ字).
    """

    tmp = text
    tmp = KANPAT.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H.sub(lambda x: KANROM_H[x.group(0)], tmp)

    # Remove unnecessary apostrophes
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", "n", tmp)

    return tmp


def is_consonant(text: str) -> Optional[re.Match]:
    """
    Return a MatchObject if a Latin letter is a consonant in Japanese.
    Return None otherwise.
    """

    text = text.lower()

    return re.match(CONSONANTS, text)


def is_vowel(text: str) -> Optional[re.Match]:
    """
    Return a MatchObject if a Latin letter is a vowel in Japanese.
    Return None otherwise.
    """

    text = text.lower()

    return re.match(VOWELS, text)


def expand_consonant(text: str) -> list[str]:
    """
    Expand consonant to its related moras.
    Example: 'sh' => ['sha', 'she', 'shi', 'sho', 'shu']
    """

    text = text.lower()

    return sorted([mora for mora in ROMKAN.keys() if re.match(rf"^{text}.$", mora)])
