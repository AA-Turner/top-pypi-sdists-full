import numpy as np


def unpack_hex_bits(hex_str: str) -> np.ndarray:
    """Convert a hex string to a numpy array of bit values (0/1)."""
    needs_pad = len(hex_str) % 2 != 0
    padded_hex = hex_str.zfill(len(hex_str) + needs_pad)
    bits = np.unpackbits(
        np.frombuffer(bytes.fromhex(padded_hex), dtype=np.uint8),
    )
    if needs_pad:
        # zfill added one hex char (4 bits) of leading zeros; strip them
        bits = bits[4:]
    return bits
