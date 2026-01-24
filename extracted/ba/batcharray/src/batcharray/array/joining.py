r"""Contain some joining functions for arrays."""

from __future__ import annotations

__all__ = ["concatenate_along_batch", "concatenate_along_seq", "tile_along_seq"]


import numpy as np

from batcharray import computation as cmpt
from batcharray.constants import BATCH_AXIS, SEQ_AXIS


def concatenate_along_batch(arrays: list[np.ndarray] | tuple[np.ndarray, ...]) -> np.ndarray:
    r"""Concatenate the given arrays in the batch axis.

    All arrays must either have the same data type and shape (except
    in the concatenating axis) or be empty.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        arrays: The arrays to concatenate.

    Returns:
        The concatenated arrays along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import concatenate_along_batch
        >>> arrays = [
        ...     np.array([[0, 1, 2], [4, 5, 6]]),
        ...     np.array([[10, 11, 12], [13, 14, 15]]),
        ... ]
        >>> out = concatenate_along_batch(arrays)
        >>> out
        array([[ 0,  1,  2],
               [ 4,  5,  6],
               [10, 11, 12],
               [13, 14, 15]])

        ```
    """
    return cmpt.concatenate(arrays, axis=BATCH_AXIS)


def concatenate_along_seq(arrays: list[np.ndarray] | tuple[np.ndarray, ...]) -> np.ndarray:
    r"""Concatenate the given arrays in the sequence axis.

    All arrays must either have the same data type and shape (except
    in the concatenating axis) or be empty.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        arrays: The arrays to concatenate.

    Returns:
        The concatenated arrays along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import concatenate_along_seq
        >>> arrays = [
        ...     np.array([[0, 1, 2], [4, 5, 6]]),
        ...     np.array([[10, 11], [12, 13]]),
        ... ]
        >>> out = concatenate_along_seq(arrays)
        >>> out
        array([[ 0,  1,  2, 10, 11],
               [ 4,  5,  6, 12, 13]])

        ```
    """
    return cmpt.concatenate(arrays, axis=SEQ_AXIS)


def tile_along_seq(array: np.ndarray, reps: int) -> np.ndarray:
    r"""Construct an array by repeating the input array along the
    sequence axis.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The input array.
        reps: The number of repetitions data along the
            sequence axis.

    Returns:
        A new array with the data repeated along the sequence
            axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import tile_along_seq
        >>> array = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        >>> out = tile_along_seq(array, 2)
        >>> out
        array([[0, 1, 2, 3, 4, 0, 1, 2, 3, 4],
               [5, 6, 7, 8, 9, 5, 6, 7, 8, 9]])

        ```
    """
    repeats = [1] * array.ndim
    repeats[1] = reps
    return np.tile(array, repeats)
