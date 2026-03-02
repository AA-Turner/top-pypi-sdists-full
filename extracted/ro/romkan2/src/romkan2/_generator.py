import re
from collections.abc import Iterator
from functools import cache, cmp_to_key
from typing import NamedTuple

from ._constants import SPACES

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


class RomkanTable(NamedTuple):
    romkan: dict[str, str]
    kanrom: dict[str, str]
    rompat: re.Pattern[str]
    kanpat: re.Pattern[str]
    kunpat: re.Pattern[str]
    heppat: re.Pattern[str]
    to_hepburn: dict[str, str]
    to_kunrei: dict[str, str]


def _pairs(arr: list[str], size: int = 2) -> Iterator[list[str]]:
    for i in range(0, len(arr) - 1, size):
        yield arr[i : i + size]


@cache
def romkan_from_table(
    kunrei_table: str,
    hepburn_table: str,
    specials: tuple[tuple[str, str], ...],
) -> RomkanTable:
    kanrom: dict[str, str] = {}
    romkan: dict[str, str] = {}

    for pair in _pairs(re.split(SPACES, kunrei_table + hepburn_table)):
        kana, roma = pair
        kanrom[kana] = roma
        romkan[roma] = kana

    # special modification
    romkan.update(specials)

    # Sort in long order so that a longer Romaji sequence precedes.

    rompat = re.compile("|".join(sorted(romkan.keys(), key=len, reverse=True)))

    def _kanpat_cmp(x: str, y: str) -> int:
        return (len(y) > len(x)) - (len(y) < len(x)) or (len(kanrom[x]) > len(kanrom[x])) - (
            len(kanrom[x]) < len(kanrom[x])
        )

    kanpat = re.compile("|".join(sorted(kanrom.keys(), key=cmp_to_key(_kanpat_cmp))))

    kunrei = [y for (_, y) in _pairs(re.split(SPACES, kunrei_table))]
    hepburn = [y for (_, y) in _pairs(re.split(SPACES, hepburn_table))]

    kunpat = re.compile("|".join(sorted(kunrei, key=len, reverse=True)))
    heppat = re.compile("|".join(sorted(hepburn, key=len, reverse=True)))

    to_hepburn = {}
    to_kunrei = {}

    for kun, hep in zip(kunrei, hepburn):
        to_hepburn[kun] = hep
        to_kunrei[hep] = kun

    to_hepburn.update({"ti": "chi"})

    return RomkanTable(
        romkan=romkan,
        kanrom=kanrom,
        rompat=rompat,
        kanpat=kanpat,
        kunpat=kunpat,
        heppat=heppat,
        to_hepburn=to_hepburn,
        to_kunrei=to_kunrei,
    )
