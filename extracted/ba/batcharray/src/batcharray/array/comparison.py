r"""Contain some comparison functions for arrays."""

from __future__ import annotations

__all__ = ["argsort_along_batch", "argsort_along_seq", "sort_along_batch", "sort_along_seq"]

from typing import TYPE_CHECKING

from batcharray.computation import argsort, sort
from batcharray.constants import BATCH_AXIS, SEQ_AXIS

if TYPE_CHECKING:
    import numpy as np

    from batcharray.types import SortKind


def argsort_along_batch(array: np.ndarray, kind: SortKind | None = None) -> np.ndarray:
    r"""Return the indices that sort an array along the batch axis in
    ascending order by value.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The input array.
        kind: Sorting algorithm. The default is `quicksort`.
            Note that both `stable` and `mergesort` use timsort
            under the covers and, in general, the actual
            implementation will vary with datatype.
            The `mergesort` option is retained for backwards
            compatibility.

    Returns:
        The indices that sort the array along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import argsort_along_batch
        >>> array = np.array([[2, 6], [0, 3], [4, 9], [8, 1], [5, 7]])
        >>> out = argsort_along_batch(array)
        >>> out
        array([[1, 3], [0, 1], [2, 0], [4, 4], [3, 2]])

        ```
    """
    return argsort(array, axis=BATCH_AXIS, kind=kind)


def argsort_along_seq(array: np.ndarray, kind: SortKind | None = None) -> np.ndarray:
    r"""Return the indices that sort an array along the sequence axis in
    ascending order by value.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The input array.
        kind: Sorting algorithm. The default is `quicksort`.
            Note that both `stable` and `mergesort` use timsort
            under the covers and, in general, the actual
            implementation will vary with datatype.
            The `mergesort` option is retained for backwards
            compatibility.

    Returns:
        The indices that sort the array along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import argsort_along_seq
        >>> array = np.array([[7, 3, 0, 8, 5], [1, 9, 6, 4, 2]])
        >>> out = argsort_along_seq(array)
        >>> out
        array([[2, 1, 4, 0, 3],
               [0, 4, 3, 2, 1]])

        ```
    """
    return argsort(array, axis=SEQ_AXIS, kind=kind)


def sort_along_batch(array: np.ndarray, kind: SortKind | None = None) -> np.ndarray:
    r"""Sort the elements of the input array along the batch axis in
    ascending order by value.

    Note:
        This function assumes the batch axis is the first
            axis.

    Args:
        array: The input array.
        kind: Sorting algorithm. The default is `quicksort`.
            Note that both `stable` and `mergesort` use timsort
            under the covers and, in general, the actual
            implementation will vary with datatype.
            The `mergesort` option is retained for backwards
            compatibility.

    Returns:
        The sorted array along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import sort_along_batch
        >>> array = np.array([[2, 6], [0, 3], [4, 9], [8, 1], [5, 7]])
        >>> out = sort_along_batch(array)
        >>> out
        array([[0, 1], [2, 3], [4, 6], [5, 7], [8, 9]])

        ```
    """
    return sort(array, axis=BATCH_AXIS, kind=kind)


def sort_along_seq(array: np.ndarray, kind: SortKind | None = None) -> np.ndarray:
    r"""Sort the elements of the input array along the sequence axis in
    ascending order by value.

    Note:
        This function assumes the sequence axis is the second
            axis.

    Args:
        array: The input array.
        kind: Sorting algorithm. The default is `quicksort`.
            Note that both `stable` and `mergesort` use timsort
            under the covers and, in general, the actual
            implementation will vary with datatype.
            The `mergesort` option is retained for backwards
            compatibility.

    Returns:
        The sorted array along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.array import sort_along_seq
        >>> array = np.array([[7, 3, 0, 8, 5], [1, 9, 6, 4, 2]])
        >>> out = sort_along_seq(array)
        >>> out
        array([[0, 3, 5, 7, 8], [1, 2, 4, 6, 9]])

        ```
    """
    return sort(array, axis=SEQ_AXIS, kind=kind)
