r"""Contain some mathematical functions for arrays."""

from __future__ import annotations

__all__ = [
    "cumprod_along_batch",
    "cumprod_along_seq",
    "cumsum_along_batch",
    "cumsum_along_seq",
]

from typing import TYPE_CHECKING

from batcharray.constants import BATCH_AXIS, SEQ_AXIS

if TYPE_CHECKING:
    import numpy as np


def cumprod_along_batch(array: np.ndarray) -> np.ndarray:
    r"""Return the cumulative product of elements of input in the batch
    axis.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The input array.

    Returns:
        The cumulative product of elements of input in the batch
            axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import cumprod_along_batch
        >>> array = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
        >>> out = cumprod_along_batch(array)
        >>> out
        array([[   1,    2], [   3,    8], [  15,   48], [ 105,  384], [ 945, 3840]])

        ```
    """
    return array.cumprod(axis=BATCH_AXIS)


def cumprod_along_seq(array: np.ndarray) -> np.ndarray:
    r"""Return the cumulative product of elements of input in the
    sequence axis.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The input array.

    Returns:
        The cumulative product of elements of input in the sequence
            axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import cumprod_along_seq
        >>> array = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
        >>> out = cumprod_along_seq(array)
        >>> out
        array([[    1,     2,     6,    24,   120],
                [    6,    42,   336,  3024, 30240]])

        ```
    """
    return array.cumprod(axis=SEQ_AXIS)


def cumsum_along_batch(array: np.ndarray) -> np.ndarray:
    r"""Return the cumulative sum of elements of input in the batch axis.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The input array.

    Returns:
        The cumulative sum of elements of input in the batch
            axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import cumsum_along_batch
        >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        >>> out = cumsum_along_batch(array)
        >>> out
        array([[ 0,  1], [ 2,  4], [ 6,  9], [12, 16], [20, 25]])

        ```
    """
    return array.cumsum(axis=BATCH_AXIS)


def cumsum_along_seq(array: np.ndarray) -> np.ndarray:
    r"""Return the cumulative sum of elements of input in the sequence
    axis.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The input array.

    Returns:
        The cumulative sum of elements of input in the sequence
            axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import cumsum_along_seq
        >>> array = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        >>> out = cumsum_along_seq(array)
        >>> out
        array([[ 0,  1,  3,  6, 10],
               [ 5, 11, 18, 26, 35]])

        ```
    """
    return array.cumsum(axis=SEQ_AXIS)
