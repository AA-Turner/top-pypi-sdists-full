"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

Copyright (C) 2023 Michael Hall <https://github.com/mikeshardmind>
"""

from __future__ import annotations

import lzma
import struct
from collections import deque
from collections.abc import Iterable
from functools import cache
from io import StringIO
from pathlib import Path

__all__ = ("decode", "encode")


@cache
def _get_data() -> tuple[tuple[int, ...], tuple[str, ...]]:

    with lzma.open(
        Path(__file__).with_name("b2048.data"),
        mode="rb",
        format=lzma.FORMAT_XZ,
    ) as fp:
        data = fp.read()

    DEC_TABLE: tuple[int, ...] = struct.unpack_from("!4340H", data, 0)
    ENC_TABLE = tuple(map(chr, struct.unpack_from("!2048H", data, 8680)))

    return DEC_TABLE, ENC_TABLE


class Peekable:
    def __init__(self, iterable: Iterable[tuple[int, str]]):
        self._it = iter(iterable)
        self._cache: deque[tuple[int, str]] = deque()

    def __iter__(self) -> Peekable:
        return self

    def has_more(self) -> bool:
        try:
            self.peek()
        except StopIteration:
            return False
        return True

    def peek(self) -> tuple[int, str]:
        if not self._cache:
            self._cache.append(next(self._it))
        return self._cache[0]

    def __next__(self) -> tuple[int, str]:
        if self._cache:
            return self._cache.popleft()
        return next(self._it)


TAIL = ("།", "༎", "༏", "༐", "༑", "༆", "༈", "༒")

ZERO_SET = {idx for idx, value in enumerate(_get_data()[0]) if value == 0xFFFF}


class DecodeError(Exception):
    pass


def encode(bys: bytes, /) -> str:
    """Encode data as base2048."""
    ret = StringIO()
    stage = 0
    remaining = 0

    enc_table = _get_data()[1]

    for byte in bys:
        need = 11 - remaining
        if need < 8:
            remaining = 8 - need
            index = (stage << need) | (byte >> remaining)
            ret.write(enc_table[index])
            stage = byte & ((1 << remaining) - 1)
        else:
            stage = (stage << 8) | byte
            remaining += 8

    if remaining > 0:
        ret.write(TAIL[stage] if remaining <= 3 else enc_table[stage])

    ret.seek(0)
    return ret.read()


def decode(string: str, /) -> bytes:
    """Decode base2048 string as raw bytes

    Raises
    ------
    DecodeError
        Not a well-formed base2048 string
    """
    dec_table = _get_data()[0]

    ret: list[int] = []
    remaining = 0
    stage = 0
    chars = Peekable(enumerate(string))
    residue = 0

    for i, c in chars:
        residue = (residue + 11) % 8
        numeric = ord(c)

        if numeric > 4339:
            msg = f"Invalid character {i}: [{numeric}]"
            raise DecodeError(msg)

        n_new_bits, new_bits = 0, 0

        if numeric in ZERO_SET:
            if chars.has_more():
                i_next, c_next = chars.peek()
                msg = f"Unexpected character {i_next}: [{c_next}] after termination sequence {i}: [{c}]"
                raise DecodeError(msg)

            try:
                index = TAIL.index(c)
            except ValueError:
                msg = f"Invalid termination character {i}: [{c}]"
                raise DecodeError(msg) from None
            else:
                need = 8 - remaining
                if index < (1 << need):
                    n_new_bits = need
                    new_bits = index
                else:
                    msg = f"Invalid tail character {i}: [{c}]"
                    raise DecodeError(msg)
        else:
            new_bits = dec_table[numeric]
            n_new_bits = 11 if chars.has_more() else 11 - residue

        remaining += n_new_bits
        stage = (stage << n_new_bits) | new_bits
        while remaining > 8:
            remaining -= 8
            ret.append(stage >> remaining)
            stage &= (1 << remaining) - 1

    if remaining > 0:
        ret.append(stage >> (8 - remaining))

    return bytes(ret)
