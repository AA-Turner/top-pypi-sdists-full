import numpy as np

from downstream._auxlib._bitwise_count64_batched import bitwise_count64_batched


def test_bitwise_count_batched_uint64():
    test_values = np.array(
        [
            0x0000000000000000,  # Zero
            0xFFFFFFFFFFFFFFFF,  # All ones
            0xAAAAAAAAAAAAAAAA,  # Alternating ones and zeros starting with 1 (1010...)
            0x5555555555555555,  # Alternating ones and zeros starting with 0 (0101...)
            0x123456789ABCDEF0,  # Random value
            0x0FEDCBA987654321,  # Another random value
            0x00000000FFFFFFFF,  # Lower 32 bits ones
            0xFFFFFFFF00000000,  # Upper 32 bits ones
            0x8000000000000000,  # Highest bit set
            0x0000000000000001,  # Lowest bit set
        ],
        dtype=np.uint64,
    )

    expected_counts = np.bitwise_count(test_values)
    actual_counts = bitwise_count64_batched(test_values)
    np.testing.assert_array_equal(actual_counts, expected_counts)
