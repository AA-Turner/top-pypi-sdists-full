import numpy as np
import pytest

from downstream._auxlib._pack_hex import pack_hex


def test_pack_hex_valid_input():
    items = np.array([0x00FF00FA, 0xBF00FF00], dtype=np.uint64)
    item_bitwidth = 32
    expected = "00ff00fabf00ff00"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_single_item():
    items = np.array([0x0000FFFFFFFFFF00], dtype=np.uint64)
    item_bitwidth = 64
    expected = "0000ffffffffff00"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_single_byte():
    items = np.array([0xAB], dtype=np.uint8)
    item_bitwidth = 8
    expected = "ab"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_single_2byte():
    items = np.array([0xAB, 0x06], dtype=np.uint16)
    item_bitwidth = 8
    expected = "ab06"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_multiple_items():
    items = np.array([0x0000456789ABCDEF, 0x0123456789000000], dtype=np.uint64)
    item_bitwidth = 64
    expected = "0000456789abcdef0123456789000000"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_short_hex_string():
    items = np.array([0xFA], dtype=np.uint8)
    item_bitwidth = 8
    expected = "fa"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_4bit_items():
    items = np.array([0xF, 0x0, 0xF, 0x0], dtype=np.uint8)
    item_bitwidth = 4
    expected = "f0f0"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_1bit_items():
    items = np.array([1, 1, 1, 1, 1, 0, 0, 0], dtype=np.uint8)
    item_bitwidth = 1
    expected = "f8"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_1bit_items_zeros():
    items = np.zeros(16, dtype=np.uint8)
    item_bitwidth = 1
    expected = "0000"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_2bit_items():
    items = np.array([3, 3, 2, 0], dtype=np.uint8)
    item_bitwidth = 2
    expected = "f8"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_2bit_items_zeros():
    items = np.zeros(8, dtype=np.uint8)
    item_bitwidth = 2
    expected = "0000"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_negative_items():
    items = np.array([-1, 0, 1], dtype=np.int8)
    item_bitwidth = 8
    # Two's-complement: -1 -> 0xFF, 0 -> 0x00, 1 -> 0x01
    expected = "ff0001"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_nonhex_aligned_error():
    # total bits not multiple of 4 should raise NotImplementedError
    items = np.array([1, 2, 3], dtype=np.uint8)
    item_bitwidth = 3  # 3*3=9 bits, not multiple of 4
    with pytest.raises(NotImplementedError):
        pack_hex(items, item_bitwidth)


def test_pack_hex_overflow_error():
    # value too large to fit in bitwidth should raise ValueError
    items = np.array([0, 1, 2, 15], dtype=np.uint8)
    item_bitwidth = 4  # max representable 0..15
    # this is fine
    pack_hex(items, item_bitwidth)
    # now overflow
    items_over = np.array([16], dtype=np.uint8)
    with pytest.raises(ValueError):
        pack_hex(items_over, 4)


def test_pack_hex_general_3bit_items():
    items = np.array([1, 2, 3, 4], dtype=np.uint8)
    item_bitwidth = 3
    # bits: 001 010 011 100 -> packed bytes 0x29,0xC0
    expected = "29c0"
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_signed_non_byte_aligned_error():
    # Negative values with non-byte-aligned bitwidth should error
    items = np.array([-1, 1], dtype=np.int8)
    item_bitwidth = 4  # non-byte-aligned
    with pytest.raises(ValueError):
        pack_hex(items, item_bitwidth)


def test_pack_hex_signed_overflow_error1():
    # Signed overflow beyond [-2^(n-1), 2^(n-1)-1] should error
    items = np.array([-129, 0], dtype=np.int16)
    item_bitwidth = 8
    with pytest.raises(ValueError):
        pack_hex(items, item_bitwidth)


def test_pack_hex_signed_overflow_error2():
    # Signed overflow beyond [-2^(n-1), 2^(n-1)-1] should error
    items = np.array([-12, 128], dtype=np.int16)
    item_bitwidth = 8
    with pytest.raises(ValueError):
        pack_hex(items, item_bitwidth)


def test_pack_hex_signed_no_overflow_error():
    items = np.array([1, 128], dtype=np.int16)
    item_bitwidth = 8
    pack_hex(items, item_bitwidth)


def test_pack_hex_bitwidth_range_error():
    # bitwidth outside [1,64] should raise ValueError
    items = np.array([0], dtype=np.uint8)
    with pytest.raises(NotImplementedError):
        pack_hex(items, 0)
    with pytest.raises(NotImplementedError):
        pack_hex(items, 65)


def test_pack_hex_uint64_extremes():
    # Unsigned 64-bit extremes: 0 and max uint64
    vals = [0, np.iinfo(np.uint64).max, 1, np.iinfo(np.uint64).max - 1]
    items = np.array(vals, dtype=np.uint64)
    item_bitwidth = 64
    expected = "".join(f"{v:016x}" for v in vals)
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_int64_extremes():
    # Signed 64-bit extremes: min int64 and max int64
    vals = [
        np.iinfo(np.int64).min,
        np.iinfo(np.int64).min + 1,
        np.iinfo(np.int64).max - 1,
        np.iinfo(np.int64).max,
    ]
    items = np.array(vals, dtype=np.int64)
    item_bitwidth = 64
    reps = [(int(v) & ((1 << item_bitwidth) - 1)) for v in vals]
    expected = "".join(f"{r:016x}" for r in reps)
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_uint32_extremes():
    # Unsigned 32-bit extremes and near-extremes
    vals = [0, np.iinfo(np.uint32).max, 1, np.iinfo(np.uint32).max - 1]
    items = np.array(vals, dtype=np.uint32)
    item_bitwidth = 32
    expected = "".join(f"{v:08x}" for v in vals)
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_int32_extremes():
    # Signed 32-bit extremes and near-extremes
    im = np.iinfo(np.int32)
    vals = [im.min, im.min + 1, im.max - 1, im.max]
    items = np.array(vals, dtype=np.int32)
    item_bitwidth = 32
    reps = [(int(v) & ((1 << item_bitwidth) - 1)) for v in vals]
    expected = "".join(f"{r:08x}" for r in reps)
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_int16_extremes():
    # Signed 16-bit extremes
    im = np.iinfo(np.int16)
    vals = [im.min, im.min + 1, im.max - 1, im.max]
    items = np.array(vals, dtype=np.int16)
    item_bitwidth = 16
    reps = [(int(v) & ((1 << item_bitwidth) - 1)) for v in vals]
    expected = "".join(f"{r:04x}" for r in reps)
    result = pack_hex(items, item_bitwidth)
    assert result == expected


def test_pack_hex_uint16_extremes():
    # Unsigned 16-bit extremes
    um = np.iinfo(np.uint16).max
    items = np.array([0, um], dtype=np.uint16)
    item_bitwidth = 16
    expected = "0000" + f"{um:04x}"
    result = pack_hex(items, item_bitwidth)
    assert result == expected
