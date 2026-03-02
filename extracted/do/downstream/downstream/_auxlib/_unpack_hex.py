import sys

import numpy as np


def unpack_hex(hex_str: str, num_items: int) -> np.ndarray:
    """Unpacks a hexadecimal string into an array of 64-bit unsigned integers.

    This function interprets the input hexadecimal string as a sequence of bits,
    reshapes it to represent `num_items` items, and returns a NumPy array of
    64-bit unsigned integers.

    Parameters
    ----------
    hex_str : str
        Hexadecimal string to be unpacked.
    num_items : int
        Number of items to unpack from the hexadecimal data.

    Returns
    -------
    np.ndarray
        Array of unsigned integers representing the unpacked data.

    Notes
    -----
    - Hex data is assumed to be packed using big-endian byte order.
    - The function requires a runtime little-endian byte order.
    """
    if sys.byteorder != "little":
        raise NotImplementedError(
            "native big-endian byte order not yet supported",
        )

    if num_items > len(hex_str) * 4:
        raise ValueError(
            "not enough data to unpack requested number of items, "
            f"cannot unpack {num_items=} from {len(hex_str)} hex chars "
            f"({len(hex_str) * 4} bits)",
        )

    if num_items == len(hex_str):
        # handle 4-bit values by processing ascii ordinals directly
        ascii_codes = np.frombuffer(
            hex_str.lower().encode("ascii"), dtype=np.uint8
        )
        digits = ascii_codes - ord("0")
        alphas = ascii_codes - (ord("a") - 10)
        return np.where(digits < 10, digits, alphas)

    # unpack hex string into numpy bytes array
    bytes_array = np.frombuffer(
        bytes.fromhex(hex_str),
        count=len(hex_str) >> 1,
        dtype=np.uint8,
    )
    if num_items == len(bytes_array):
        # for 1-byte values, we are done
        return bytes_array

    # unpack bits, creating array with one entry per bit value
    bits_array = np.unpackbits(bytes_array, bitorder="big")
    if num_items == len(bytes_array) * 8:
        # for 1-byte values, we are done
        return bits_array

    # for the general case,
    # reshape bits into subarrays `num_items` wide
    # then pack bits from each subarray into a single value
    item_bits_array = bits_array.reshape((num_items, -1))[:, ::-1]
    item_bytes_array = np.packbits(
        item_bits_array,
        axis=1,
        bitorder="little",
    )
    item_8bytes_array = np.pad(
        item_bytes_array,
        ((0, 0), (0, 8 - len(item_bytes_array[0]))),
        constant_values=0,
        mode="constant",
    )
    return np.frombuffer(item_8bytes_array.ravel(), dtype=np.uint64)
