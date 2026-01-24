r"""Contain some functions to permute data in arrays."""

from __future__ import annotations

__all__ = ["permute_along_batch", "permute_along_seq", "shuffle_along_batch", "shuffle_along_seq"]


from functools import partial
from typing import Any

import numpy as np
from coola.iterator import dfs_iterate
from coola.recursive import recursive_apply

from batcharray import array
from batcharray.constants import BATCH_AXIS, SEQ_AXIS


def permute_along_batch(data: Any, permutation: np.ndarray) -> Any:
    r"""Permute all the arrays along the batch axis.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.
        permutation: The 1-D array containing the indices of the
            permutation. The shape should match the batch axis
            of the array.

    Returns:
        The data with permuted arrays along the batch axis.
            The output data has the same structure as the input data.

    Raises:
        RuntimeError: if the shape of the permutation does not match
            the batch axis of the array.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import permute_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = permute_along_batch(data, np.array([2, 1, 3, 0, 4]))
        >>> out
        {'a': array([[4, 5], [2, 3], [6, 7], [0, 1], [8, 9]]), 'b': array([2, 3, 1, 4, 0])}

        ```
    """
    return recursive_apply(data, partial(array.permute_along_batch, permutation=permutation))


def permute_along_seq(data: Any, permutation: np.ndarray) -> Any:
    r"""Permute all the arrays along the sequence axis.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.
        permutation: The 1-D array containing the indices of the
            permutation. The shape should match the sequence axis
            of the array.

    Returns:
        The data with permuted arrays along the sequence axis.
            The output data has the same structure as the input data.

    Raises:
        RuntimeError: if the shape of the permutation does not match
            the sequence axis of the array.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import permute_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = permute_along_seq(data, np.array([2, 1, 3, 0, 4]))
        >>> out
        {'a': array([[2, 1, 3, 0, 4], [7, 6, 8, 5, 9]]), 'b': array([[2, 3, 1, 4, 0]])}

        ```
    """
    return recursive_apply(data, partial(array.permute_along_seq, permutation=permutation))


def shuffle_along_batch(data: Any, rng: np.random.Generator | None = None) -> Any:
    r"""Shuffle all the arrays along the batch axis.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.
        rng: An optional random number generator.

    Returns:
        The data with shuffled arrays along the sequence axis.
            The output data has the same structure as the input data.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import shuffle_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = shuffle_along_batch(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    if rng is None:
        rng = np.random.default_rng()
    value = next(dfs_iterate(data))
    return permute_along_batch(
        data=data,
        permutation=rng.permutation(value.shape[BATCH_AXIS]),
    )


def shuffle_along_seq(data: Any, rng: np.random.Generator | None = None) -> Any:
    r"""Shuffle all the arrays along the batch axis.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.
        rng: An optional random number generator.

    Returns:
        The data with shuffled arrays along the sequence axis.
            The output data has the same structure as the input data.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import shuffle_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = shuffle_along_seq(data)
        >>> out
        {'a': array([[...]]), 'b': array([[...]])}

        ```
    """
    if rng is None:
        rng = np.random.default_rng()
    value = next(dfs_iterate(data))
    return permute_along_seq(
        data=data,
        permutation=rng.permutation(value.shape[SEQ_AXIS]),
    )
