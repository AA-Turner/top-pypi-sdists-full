r"""Contain some functions to permute data in arrays."""

from __future__ import annotations

__all__ = [
    "permute_along_batch",
    "permute_along_seq",
    "shuffle_along_batch",
    "shuffle_along_seq",
]


import numpy as np

from batcharray.array.indexing import take_along_batch, take_along_seq
from batcharray.constants import BATCH_AXIS, SEQ_AXIS


def permute_along_batch(array: np.ndarray, permutation: np.ndarray) -> np.ndarray:
    r"""Permute the array along the batch axis.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The array to split.
        permutation: The 1-D array containing the indices of the
            permutation. The shape should match the batch axis
            of the array.

    Returns:
        The array with permuted data along the batch axis.

    Raises:
        RuntimeError: if the shape of the permutation does not match
            the batch axis of the array.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import permute_along_batch
        >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        >>> out = permute_along_batch(array, np.array([2, 1, 3, 0, 4]))
        >>> out
        array([[4, 5],
               [2, 3],
               [6, 7],
               [0, 1],
               [8, 9]])

        ```
    """
    if permutation.shape[0] != array.shape[0]:
        msg = (
            f"permutation shape ({permutation.shape}) is not compatible with array shape "
            f"({array.shape})"
        )
        raise RuntimeError(msg)
    return take_along_batch(array, indices=permutation)


def permute_along_seq(array: np.ndarray, permutation: np.ndarray) -> np.ndarray:
    r"""Permute the array along the sequence axis.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The array to split.
        permutation: The 1-D array containing the indices of the
            permutation. The shape should match the sequence axis
            of the array.

    Returns:
        The array with permuted data along the sequence axis.

    Raises:
        RuntimeError: if the shape of the permutation does not match
            the sequence axis of the array.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import permute_along_seq
        >>> array = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        >>> out = permute_along_seq(array, np.array([2, 1, 3, 0, 4]))
        >>> out
        array([[2, 1, 3, 0, 4],
               [7, 6, 8, 5, 9]])

        ```
    """
    if permutation.shape[0] != array.shape[1]:
        msg = (
            f"permutation shape ({permutation.shape}) is not compatible with array shape "
            f"({array.shape})"
        )
        raise RuntimeError(msg)
    return take_along_seq(array, indices=permutation)


def shuffle_along_batch(array: np.ndarray, rng: np.random.Generator | None = None) -> np.ndarray:
    r"""Shuffle the array along the batch dimension.

    Note:
        This function assumes the batch axis is the first
            dimension.

    Args:
        array: The array to split.
        rng: An optional random number generator.

    Returns:
        The shuffled array.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import shuffle_along_batch
        >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        >>> out = shuffle_along_batch(array)
        >>> out
        array([[...]])

        ```
    """
    if rng is None:
        rng = np.random.default_rng()
    return permute_along_batch(
        array=array,
        permutation=rng.permutation(array.shape[BATCH_AXIS]),
    )


def shuffle_along_seq(array: np.ndarray, rng: np.random.Generator | None = None) -> np.ndarray:
    r"""Shuffle the array along the batch dimension.

    Note:
        This function assumes the sequence axis is the second
            dimension.

    Args:
        array: The array to split.
        rng: An optional random number generator.

    Returns:
        The shuffled array.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import shuffle_along_seq
        >>> array = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        >>> out = shuffle_along_seq(array)
        >>> out
        array([[...]])

        ```
    """
    if rng is None:
        rng = np.random.default_rng()
    return permute_along_seq(
        array=array,
        permutation=rng.permutation(array.shape[SEQ_AXIS]),
    )
