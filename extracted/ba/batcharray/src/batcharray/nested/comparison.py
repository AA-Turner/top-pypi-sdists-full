r"""Contain some array comparison functions for nested data."""

from __future__ import annotations

__all__ = ["argsort_along_batch", "argsort_along_seq", "sort_along_batch", "sort_along_seq"]

from functools import partial
from typing import TYPE_CHECKING, Any

from coola.recursive import recursive_apply

from batcharray import array as ba

if TYPE_CHECKING:
    from batcharray.types import SortKind


def argsort_along_batch(data: Any, kind: SortKind | None = None) -> Any:
    r"""Return the indices that sort each array along the batch dimension
    in ascending order by value.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array .
        kind: Sorting algorithm. The default is `quicksort`.
            Note that both `stable` and `mergesort` use timsort
            under the covers and, in general, the actual
            implementation will vary with datatype.
            The `mergesort` option is retained for backwards
            compatibility.

    Returns:
        The indices that sort each array along the batch dimension

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import argsort_along_batch
        >>> data = {
        ...     "a": np.array([[2, 6], [0, 3], [4, 9], [8, 1], [5, 7]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = argsort_along_batch(data)
        >>> out
        {'a': array([[1, 3], [0, 1], [2, 0], [4, 4], [3, 2]]), 'b': array([4, 3, 2, 1, 0])}

        ```
    """
    return recursive_apply(data, partial(ba.argsort_along_batch, kind=kind))


def argsort_along_seq(data: Any, kind: SortKind | None = None) -> Any:
    r"""Return the indices that sort each array along the sequence
    dimension in ascending order by value.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array .
        kind: Sorting algorithm. The default is `quicksort`.
            Note that both `stable` and `mergesort` use timsort
            under the covers and, in general, the actual
            implementation will vary with datatype.
            The `mergesort` option is retained for backwards
            compatibility.

    Returns:
        The indices that sort each array along the sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import argsort_along_seq
        >>> data = {
        ...     "a": np.array([[7, 3, 0, 8, 5], [1, 9, 6, 4, 2]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = argsort_along_seq(data)
        >>> out
        {'a': array([[2, 1, 4, 0, 3], [0, 4, 3, 2, 1]]), 'b': array([[4, 3, 2, 1, 0]])}

        ```
    """
    return recursive_apply(data, partial(ba.argsort_along_seq, kind=kind))


def sort_along_batch(data: Any, kind: SortKind | None = None) -> Any:
    r"""Sort the elements of the input array along the batch dimension in
    ascending order by value.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array .
        kind: Sorting algorithm. The default is `quicksort`.
            Note that both `stable` and `mergesort` use timsort
            under the covers and, in general, the actual
            implementation will vary with datatype.
            The `mergesort` option is retained for backwards
            compatibility.

    Returns:
        A similar object where each array is replaced by a sorted
            array along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import sort_along_batch
        >>> data = {
        ...     "a": np.array([[2, 6], [0, 3], [4, 9], [8, 1], [5, 7]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = sort_along_batch(data)
        >>> out
        {'a': array([[0, 1], [2, 3], [4, 6], [5, 7], [8, 9]]), 'b': array([0, 1, 2, 3, 4])}

        ```
    """
    return recursive_apply(data, partial(ba.sort_along_batch, kind=kind))


def sort_along_seq(data: Any, kind: SortKind | None = None) -> Any:
    r"""Sort the elements of the input array along the sequence dimension
    in ascending order by value.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array .
        kind: Sorting algorithm. The default is `quicksort`.
            Note that both `stable` and `mergesort` use timsort
            under the covers and, in general, the actual
            implementation will vary with datatype.
            The `mergesort` option is retained for backwards
            compatibility.

    Returns:
        A similar object where each array is replaced by a sorted
            array along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import sort_along_seq
        >>> data = {
        ...     "a": np.array([[7, 3, 0, 8, 5], [1, 9, 6, 4, 2]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = sort_along_seq(data)
        >>> out
        {'a': array([[0, 3, 5, 7, 8], [1, 2, 4, 6, 9]]), 'b': array([[0, 1, 2, 3, 4]])}

        ```
    """
    return recursive_apply(data, partial(ba.sort_along_seq, kind=kind))
