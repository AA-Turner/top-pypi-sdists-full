import numpy as np

from downstream._auxlib._bitwise_count32_batched import bitwise_count32_batched


def test_bitwise_count_batched_uint32():
    test_values = np.array(
        [
            0x00000000,  # Zero
            0xFFFFFFFF,  # All ones
            0xAAAAAAAA,  # Alternating ones and zeros starting with 1 (1010...)
            0x55555555,  # Alternating ones and zeros starting with 0 (0101...)
            0x12345678,  # Random value
            0x87654321,  # Another random value
            0x0000FFFF,  # Lower half ones
            0xFFFF0000,  # Upper half ones
            0x80000000,  # Highest bit set
            0x00000001,  # Lowest bit set
        ],
        dtype=np.uint32,
    )

    expected_counts = np.bitwise_count(test_values)
    actual_counts = bitwise_count32_batched(test_values)
    np.testing.assert_array_equal(actual_counts, expected_counts)
