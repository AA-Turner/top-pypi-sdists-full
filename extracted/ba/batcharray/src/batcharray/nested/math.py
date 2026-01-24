r"""Contain some mathematical functions for arrays."""

from __future__ import annotations

__all__ = [
    "cumprod_along_batch",
    "cumprod_along_seq",
    "cumsum_along_batch",
    "cumsum_along_seq",
]

from functools import partial
from typing import Any

from coola.recursive import recursive_apply

from batcharray import array as ba


def cumprod_along_batch(data: Any) -> Any:
    r"""Return the cumulative product of elements of input in the batch
    dimension.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.

    Returns:
        The cumulative product of elements of input in the batch
            dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import cumprod_along_batch
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = cumprod_along_batch(data)
        >>> out
        {'a': array([[   1,    2], [   3,    8], [  15,   48], [ 105,  384], [ 945, 3840]]),
         'b': array([ 4, 12, 24, 24,  0])}

        ```
    """
    return recursive_apply(data, partial(ba.cumprod_along_batch))


def cumprod_along_seq(data: Any) -> Any:
    r"""Return the cumulative product of elements of input in the
    sequence dimension.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.

    Returns:
        The cumulative product of elements of input in the sequence
            dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import cumprod_along_seq
        >>> data = {
        ...     "a": np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = cumprod_along_seq(data)
        >>> out
        {'a': array([[    1,     2,     6,    24,   120], [    6,    42,   336,  3024, 30240]]),
         'b': array([[ 4, 12, 24, 24,  0]])}

        ```
    """
    return recursive_apply(data, partial(ba.cumprod_along_seq))


def cumsum_along_batch(data: Any) -> Any:
    r"""Return the cumulative sum of elements of input in the batch
    dimension.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.

    Returns:
        The cumulative sum of elements of input in the batch
            dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import cumsum_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = cumsum_along_batch(data)
        >>> out
        {'a': array([[ 0,  1], [ 2,  4], [ 6,  9], [12, 16], [20, 25]]),
         'b': array([ 4,  7,  9, 10, 10])}

        ```
    """
    return recursive_apply(data, partial(ba.cumsum_along_batch))


def cumsum_along_seq(data: Any) -> Any:
    r"""Return the cumulative sum of elements of input in the sequence
    dimension.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.

    Returns:
        The cumulative sum of elements of input in the sequence
            dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import cumsum_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = cumsum_along_seq(data)
        >>> out
        {'a': array([[ 0,  1,  3,  6, 10], [ 5, 11, 18, 26, 35]]),
         'b': array([[ 4,  7,  9, 10, 10]])}

        ```
    """
    return recursive_apply(data, partial(ba.cumsum_along_seq))
