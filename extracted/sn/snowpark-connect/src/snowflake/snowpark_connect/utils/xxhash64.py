#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

# Implementation based on https://github.com/apache/spark/blob/master/sql/catalyst/src/main/java/org/apache/spark/sql/catalyst/expressions/XXH64.java
#
# Apache Spark License:
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct


def _to_int64(n: int) -> int:
    n = n & MASK_64BIT

    # Adjust for the sign bit
    if n & (1 << 63):
        n -= 1 << 64

    return n


MASK_64BIT = 0xFFFFFFFFFFFFFFFF

DEFAULT_SEED = 42

PRIME64_1 = _to_int64(0x9E3779B185EBCA87)
PRIME64_2 = _to_int64(0xC2B2AE3D27D4EB4F)
PRIME64_3 = _to_int64(0x165667B19E3779F9)
PRIME64_4 = _to_int64(0x85EBCA77C2B2AE63)
PRIME64_5 = _to_int64(0x27D4EB2F165667C5)


def _float_to_int_bits(f: float) -> int:
    return struct.unpack(">I", struct.pack(">f", f))[0]


def _double_to_long_bits(d: float) -> int:
    return struct.unpack(">Q", struct.pack(">d", d))[0]


def _rotate_left(i: int, shift: int) -> int:
    result = ((i << shift) & MASK_64BIT) | ((i & MASK_64BIT) >> (64 - shift))

    return _to_int64(result)


def _unsigned_right_shift(n: int, shift: int) -> int:
    """Mimics Java's '>>>' operator."""

    return ((n & MASK_64BIT) >> shift) & MASK_64BIT


def _fmix(hash_value: int) -> int:
    hash_value ^= _unsigned_right_shift(hash_value, 33)

    hash_value = _to_int64(hash_value * PRIME64_2)

    hash_value ^= _unsigned_right_shift(hash_value, 29)

    hash_value = _to_int64(hash_value * PRIME64_3)

    hash_value ^= _unsigned_right_shift(hash_value, 32)

    return hash_value


def _get_long(base: bytes, offset: int) -> int:
    val = base[offset : offset + 8].ljust(8, b"\x00")
    return int.from_bytes(val, byteorder="little", signed=False)


def _get_int(base: bytes, offset: int) -> int:
    val = base[offset : offset + 4].ljust(4, b"\x00")
    return int.from_bytes(val, byteorder="little", signed=False)


def _hash_bytes_by_words_next_iter(
    base: bytes, offset: int, v1: int, v2: int, v3: int, v4: int
) -> tuple[int, int, int, int]:
    k1 = _get_long(base, offset)
    k2 = _get_long(base, offset + 8)
    k3 = _get_long(base, offset + 16)
    k4 = _get_long(base, offset + 24)

    v1 = _to_int64(
        _rotate_left(_to_int64(v1 + _to_int64(k1 * PRIME64_2)), 31) * PRIME64_1
    )
    v2 = _to_int64(
        _rotate_left(_to_int64(v2 + _to_int64(k2 * PRIME64_2)), 31) * PRIME64_1
    )
    v3 = _to_int64(
        _rotate_left(_to_int64(v3 + _to_int64(k3 * PRIME64_2)), 31) * PRIME64_1
    )
    v4 = _to_int64(
        _rotate_left(_to_int64(v4 + _to_int64(k4 * PRIME64_2)), 31) * PRIME64_1
    )

    return v1, v2, v3, v4


def _hash_bytes_by_words(base: bytes, offset: int, length: int, seed: int) -> int:
    end = offset + length
    if length >= 32:
        limit = end - 32
        v1 = _to_int64(_to_int64(seed + PRIME64_1) + PRIME64_2)
        v2 = _to_int64(seed + PRIME64_2)
        v3 = seed
        v4 = _to_int64(seed - PRIME64_1)

        v1, v2, v3, v4 = _hash_bytes_by_words_next_iter(base, offset, v1, v2, v3, v4)
        offset += 32

        while offset <= limit:
            v1, v2, v3, v4 = _hash_bytes_by_words_next_iter(
                base, offset, v1, v2, v3, v4
            )
            offset += 32

        hash_value = _to_int64(_rotate_left(v1, 1) + _rotate_left(v2, 7))
        hash_value = _to_int64(hash_value + _rotate_left(v3, 12))
        hash_value = _to_int64(hash_value + _rotate_left(v4, 18))

        for v in (v1, v2, v3, v4):
            v = _to_int64(v * PRIME64_2)
            v = _to_int64(_rotate_left(v, 31))
            v = _to_int64(v * PRIME64_1)
            hash_value = _to_int64(hash_value ^ v)
            hash_value = _to_int64(_to_int64(hash_value * PRIME64_1) + PRIME64_4)
    else:
        hash_value = _to_int64(seed + PRIME64_5)

    hash_value = _to_int64(hash_value + length)
    limit = end - 8

    while offset <= limit:
        k1 = _get_long(base, offset)

        hash_value = _to_int64(
            hash_value
            ^ (_to_int64(_rotate_left(_to_int64(k1 * PRIME64_2), 31) * PRIME64_1))
        )
        hash_value = _to_int64(
            _to_int64(_rotate_left(hash_value, 27) * PRIME64_1) + PRIME64_4
        )

        offset += 8

    return hash_value


def _hash_unsafe_bytes(base: bytes, offset: int, length: int, seed: int) -> int:
    hash_value = _hash_bytes_by_words(base, offset, length, seed)

    end = offset + length
    offset += length & (~0x7)

    if (offset + 4) <= end:
        k1 = _get_int(base, offset)
        hash_value = _to_int64(hash_value ^ ((k1 & 0xFFFFFFFF) * PRIME64_1))
        hash_value = _to_int64(
            _to_int64(_rotate_left(hash_value, 23) * PRIME64_2) + PRIME64_3
        )
        offset += 4

    while offset < end:
        hash_value = _to_int64(
            hash_value ^ _to_int64((base[offset] & 0xFF) * PRIME64_5)
        )
        hash_value = _to_int64(_rotate_left(hash_value, 11) * PRIME64_1)
        offset += 1

    return _fmix(hash_value)


def xxhash64_string(value: str, seed: int = DEFAULT_SEED) -> int:
    """hash a string using the 64-bit xxhash algorithm."""

    if value is None:
        return DEFAULT_SEED

    encoded_s = value.encode("utf-8")
    return _hash_unsafe_bytes(encoded_s, 0, len(encoded_s), seed)


def xxhash64_int(value: int, seed: int = DEFAULT_SEED) -> int:
    """hash 32-bit integer using the 64-bit xxhash algorithm."""

    if value is None:
        return DEFAULT_SEED

    hash_value = _to_int64(_to_int64(seed + PRIME64_5) + 4)
    hash_value = _to_int64(hash_value ^ _to_int64((value & 0xFFFFFFFF) * PRIME64_1))
    hash_value = _to_int64(
        _to_int64(_rotate_left(hash_value, 23) * PRIME64_2) + PRIME64_3
    )

    return _fmix(hash_value)


def xxhash64_long(value: int, seed: int = DEFAULT_SEED) -> int:
    """hash a 64-bit integer using the 64-bit xxhash algorithm."""

    if value is None:
        return DEFAULT_SEED

    hash_value = _to_int64(_to_int64(seed + PRIME64_5) + 8)
    hash_value = _to_int64(
        hash_value
        ^ _to_int64(_rotate_left(_to_int64(value * PRIME64_2), 31) * PRIME64_1)
    )
    hash_value = _to_int64(
        _to_int64(_rotate_left(hash_value, 27) * PRIME64_1) + PRIME64_4
    )

    return _fmix(hash_value)


def xxhash64_float(value: float, seed: int = DEFAULT_SEED) -> int:
    """hash a float using the 64-bit xxhash algorithm."""

    return (
        DEFAULT_SEED if value is None else xxhash64_int(_float_to_int_bits(value), seed)
    )


def xxhash64_double(value: float, seed: int = DEFAULT_SEED) -> int:
    """hash a double using the 64-bit xxhash algorithm."""

    return (
        DEFAULT_SEED
        if value is None
        else xxhash64_long(_double_to_long_bits(value), seed)
    )
