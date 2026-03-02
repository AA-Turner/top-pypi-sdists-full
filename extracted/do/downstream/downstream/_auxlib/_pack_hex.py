import numpy as np


def pack_hex(items: np.ndarray, item_bitwidth: int) -> str:
    """Packs a numpy array into hexidecimal string.

    Values are encoded in their binary representation, evenly spaced according
    to item_bitwidth. If item_bitwidth is less than 8, only unsigned integers
    are supported.

    Parameters
    ----------
    items : str
        Numerical data to be packed.
    item_bitwidth : int
        Number of bits per item.

    Returns
    -------
    np.ndarray
        Hexadecimal string representing the packed data.

    Notes
    -----
    - Hex data is packed using big-endian byte order.
    """
    try:
        items = np.asarray(items, dtype=np.int64)
    except OverflowError:
        items = np.asarray(items, dtype=np.uint64)

    if not (1 <= item_bitwidth <= 64):
        raise NotImplementedError(f"{item_bitwidth=} not yet supported")

    if not item_bitwidth * len(items) & 3 == 0:
        raise NotImplementedError("non-hex-aligned data not yet supported")

    is_signed = np.any(items < 0)
    if item_bitwidth % 8 != 0 and is_signed:
        raise ValueError(
            f"signed data not representable with {item_bitwidth=}",
        )

    norm_items = items + is_signed * np.asarray(
        1 << (item_bitwidth - 1), dtype=np.uint64
    )
    if np.any(np.clip(norm_items, 0, (1 << item_bitwidth) - 1) != norm_items):
        raise ValueError(f"data not representable with {item_bitwidth=}")

    if item_bitwidth == 1:
        bits = items.astype(np.uint8)
        packed_bytes = np.packbits(bits, bitorder="big").tobytes()
    elif item_bitwidth == 4:
        arr = items.astype(np.uint8)
        high = arr[0::2] << 4
        low = arr[1::2]
        packed_bytes = (high | low).astype(np.uint8).tobytes()
    elif item_bitwidth & 7 == 0:
        bytewidth = item_bitwidth >> 3
        kind = "i" if is_signed else "u"
        dtype = np.dtype(f">{kind}{bytewidth}")
        packed_bytes = items.astype(dtype).tobytes()
    else:
        arr = items.astype(np.uint64)
        shifts = np.arange(item_bitwidth - 1, -1, -1).astype(np.uint8)
        bits = ((arr[:, None] >> shifts) & 1).astype(np.uint8)
        packed_bytes = np.packbits(bits.ravel(), bitorder="big").tobytes()

    return packed_bytes.hex()
