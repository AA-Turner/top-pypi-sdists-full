r"""Contain some indexing functions for arrays."""

from __future__ import annotations

__all__ = [
    "chunk_along_batch",
    "chunk_along_seq",
    "select_along_batch",
    "select_along_seq",
    "slice_along_batch",
    "slice_along_seq",
    "split_along_batch",
    "split_along_seq",
]


from typing import TYPE_CHECKING

import numpy as np

from batcharray.constants import BATCH_AXIS, SEQ_AXIS

if TYPE_CHECKING:
    from collections.abc import Sequence


def chunk_along_batch(array: np.ndarray, chunks: int) -> list[np.ndarray]:
    r"""Split the array into chunks along the batch axis.

    Each chunk is a view of the input array.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The array to split.
        chunks: Number of chunks to return.

    Returns:
        The array chunks.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import chunk_along_batch
        >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        >>> outputs = chunk_along_batch(array, chunks=3)
        >>> outputs
        [array([[0, 1], [2, 3]]), array([[4, 5], [6, 7]]), array([[8, 9]])]

        ```
    """
    return np.array_split(array, indices_or_sections=chunks, axis=BATCH_AXIS)


def chunk_along_seq(array: np.ndarray, chunks: int) -> list[np.ndarray]:
    r"""Split the array into chunks along the sequence axis.

    Each chunk is a view of the input array.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The array to split.
        chunks: Number of chunks to return.

    Returns:
        The array chunks.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import chunk_along_seq
        >>> array = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        >>> outputs = chunk_along_seq(array, chunks=3)
        >>> outputs
        [array([[0, 1], [5, 6]]), array([[2, 3], [7, 8]]), array([[4], [9]])]

        ```
    """
    return np.array_split(array, indices_or_sections=chunks, axis=SEQ_AXIS)


def select_along_batch(array: np.ndarray, index: int) -> np.ndarray:
    r"""Slice the input array along the batch axis at the given index.

    This function returns a view of the original array with the batch axis removed.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The input array.
        index: The index to select with.

    Returns:
        The sliced array along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import select_along_batch
        >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        >>> out = select_along_batch(array, index=2)
        >>> out
        array([4, 5])

        ```
    """
    return array[index]


def select_along_seq(array: np.ndarray, index: int) -> np.ndarray:
    r"""Slice the input array along the sequence axis at the given index.

    This function returns a view of the original array with the sequence axis removed.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The input array.
        index: The index to select with.

    Returns:
        The sliced array along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import select_along_seq
        >>> array = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        >>> out = select_along_seq(array, index=2)
        >>> out
        array([2, 7])

        ```
    """
    return array[:, index]


def slice_along_batch(
    array: np.ndarray, start: int = 0, stop: int | None = None, step: int = 1
) -> np.ndarray:
    r"""Slice the array along the batch axis.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The input array.
        start: The index where the slicing of object starts.
        stop: The index where the slicing of object stops.
            ``None`` means last.
        step: The increment between each index for slicing.

    Returns:
        The sliced array along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import slice_along_batch
        >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        >>> out = slice_along_batch(array, start=2)
        >>> out
        array([[4, 5], [6, 7], [8, 9]])
        >>> out = slice_along_batch(array, stop=3)
        >>> out
        array([[0, 1], [2, 3], [4, 5]])
        >>> out = slice_along_batch(array, step=2)
        >>> out
        array([[0, 1], [4, 5], [8, 9]])

        ```
    """
    return array[start:stop:step]


def slice_along_seq(
    array: np.ndarray, start: int = 0, stop: int | None = None, step: int = 1
) -> np.ndarray:
    r"""Slice the array along the sequence axis.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The input array.
        start: The index where the slicing of object starts.
        stop: The index where the slicing of object stops.
            ``None`` means last.
        step: The increment between each index for slicing.

    Returns:
        The sliced array along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import slice_along_seq
        >>> array = np.array([[0, 1, 2, 3, 4], [9, 8, 7, 6, 5]])
        >>> out = slice_along_seq(array, start=2)
        >>> out
        array([[2, 3, 4], [7, 6, 5]])
        >>> out = slice_along_seq(array, stop=3)
        >>> out
        array([[0, 1, 2], [9, 8, 7]])
        >>> out = slice_along_seq(array, step=2)
        >>> out
        array([[0, 2, 4], [9, 7, 5]])

        ```
    """
    return array[:, start:stop:step]


def split_along_batch(
    array: np.ndarray, split_size_or_sections: int | Sequence[int]
) -> list[np.ndarray]:
    r"""Split the array into chunks along the batch axis.

    Each chunk is a view of the original array.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The input array.
        split_size_or_sections: Size of a single chunk or list of
            sizes for each chunk

    Returns:
        The array chunks.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import split_along_batch
        >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        >>> outputs = split_along_batch(array, split_size_or_sections=2)
        >>> outputs
        [array([[0, 1], [2, 3]]), array([[4, 5], [6, 7]]), array([[8, 9]])]

        ```
    """
    if isinstance(split_size_or_sections, int):
        split_size_or_sections = tuple(
            range(split_size_or_sections, array.shape[0], split_size_or_sections)
        )
    else:
        split_size_or_sections = np.cumsum(split_size_or_sections)[:-1]
    return np.array_split(array, split_size_or_sections, axis=BATCH_AXIS)


def split_along_seq(
    array: np.ndarray, split_size_or_sections: int | Sequence[int]
) -> list[np.ndarray]:
    r"""Split the array into chunks along the sequence axis.

    Each chunk is a view of the original array.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The input array.
        split_size_or_sections: Size of a single chunk or list of
            sizes for each chunk

    Returns:
        The array chunks.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import split_along_seq
        >>> array = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        >>> outputs = split_along_seq(array, split_size_or_sections=2)
        >>> outputs
        [array([[0, 1], [5, 6]]), array([[2, 3], [7, 8]]), array([[4], [9]])]

        ```
    """
    if isinstance(split_size_or_sections, int):
        split_size_or_sections = tuple(
            range(split_size_or_sections, array.shape[1], split_size_or_sections)
        )
    else:
        split_size_or_sections = np.cumsum(split_size_or_sections)[:-1]
    return np.array_split(array, split_size_or_sections, axis=SEQ_AXIS)
