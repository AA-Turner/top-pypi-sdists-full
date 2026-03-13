import numpy as np

from downstream._auxlib._unpack_hex_bits import unpack_hex_bits


def test_unpack_hex_bits_empty_string():
    result = unpack_hex_bits("")
    assert result.dtype == np.uint8
    assert len(result) == 0


def test_unpack_hex_bits_single_hex_char():
    result = unpack_hex_bits("f")
    np.testing.assert_array_equal(result, [1, 1, 1, 1])


def test_unpack_hex_bits_zero():
    result = unpack_hex_bits("0")
    np.testing.assert_array_equal(result, [0, 0, 0, 0])


def test_unpack_hex_bits_two_chars():
    result = unpack_hex_bits("0f")
    np.testing.assert_array_equal(
        result,
        [0, 0, 0, 0, 1, 1, 1, 1],
    )


def test_unpack_hex_bits_odd_length():
    # odd-length hex: "a" -> 1010
    result = unpack_hex_bits("a")
    np.testing.assert_array_equal(result, [1, 0, 1, 0])


def test_unpack_hex_bits_even_length():
    result = unpack_hex_bits("ff")
    np.testing.assert_array_equal(result, [1] * 8)


def test_unpack_hex_bits_longer():
    result = unpack_hex_bits("00ff")
    assert len(result) == 16
    np.testing.assert_array_equal(result[:8], [0] * 8)
    np.testing.assert_array_equal(result[8:], [1] * 8)


def test_unpack_hex_bits_deadbeef():
    result = unpack_hex_bits("deadbeef")
    assert len(result) == 32
    expected = [int(b) for b in bin(0xDEADBEEF)[2:].zfill(32)]
    np.testing.assert_array_equal(result, expected)


def test_unpack_hex_bits_accede():
    result = unpack_hex_bits("accede")
    assert len(result) == 24
    expected = [int(b) for b in bin(0xACCEDE)[2:].zfill(24)]
    np.testing.assert_array_equal(result, expected)


def test_unpack_hex_bits_coffee():
    result = unpack_hex_bits("c0ffee")
    assert len(result) == 24
    expected = [int(b) for b in bin(0xC0FFEE)[2:].zfill(24)]
    np.testing.assert_array_equal(result, expected)


def test_unpack_hex_bits_ace():
    # odd-length hex string
    result = unpack_hex_bits("ace")
    assert len(result) == 12
    expected = [int(b) for b in bin(0xACE)[2:].zfill(12)]
    np.testing.assert_array_equal(result, expected)


def test_unpack_hex_bits_101():
    # odd-length hex string
    result = unpack_hex_bits("101")
    assert len(result) == 12
    expected = [int(b) for b in bin(0x101)[2:].zfill(12)]
    np.testing.assert_array_equal(result, expected)
