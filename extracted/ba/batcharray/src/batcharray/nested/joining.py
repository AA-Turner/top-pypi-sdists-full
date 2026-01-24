r"""Contain some array joining functions for nested data."""

from __future__ import annotations

__all__ = ["concatenate_along_batch", "concatenate_along_seq", "tile_along_seq"]

from functools import partial
from typing import TYPE_CHECKING, Any

from coola.recursive import recursive_apply

from batcharray import array as ba

if TYPE_CHECKING:
    from collections.abc import Hashable, Sequence

    import numpy as np


def concatenate_along_batch(
    data: Sequence[dict[Hashable, np.ndarray]],
) -> dict[Hashable, np.ndarray]:
    r"""Concatenate the given arrays in the batch axis.

    All arrays must either have the same data type and shape (except
    in the concatenating axis) or be empty.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data to concatenate. The dictionaries must have
            the same keys.

    Returns:
        The concatenated arrays along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import concatenate_along_batch
        >>> data = [
        ...     {
        ...         "a": np.array([[0, 1, 2], [4, 5, 6]]),
        ...         "b": np.array([[10, 11, 12], [13, 14, 15]]),
        ...     },
        ...     {"a": np.array([[7, 8, 9]]), "b": np.array([[17, 18, 19]])},
        ... ]
        >>> out = concatenate_along_batch(data)
        >>> out
        {'a': array([[0, 1, 2], [4, 5, 6], [7, 8, 9]]),
         'b': array([[10, 11, 12], [13, 14, 15], [17, 18, 19]])}

        ```
    """
    if not data:
        return {}
    item = data[0]
    return type(item)({key: ba.concatenate_along_batch([d[key] for d in data]) for key in item})


def concatenate_along_seq(data: Sequence[dict[Hashable, np.ndarray]]) -> dict[Hashable, np.ndarray]:
    r"""Concatenate the given arrays in the sequence axis.

    All arrays must either have the same data type and shape (except
    in the concatenating axis) or be empty.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data to concatenate. The dictionaries must have
            the same keys.

    Returns:
        The concatenated arrays along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import concatenate_along_seq
        >>> data = [
        ...     {
        ...         "a": np.array([[0, 1, 2], [4, 5, 6]]),
        ...         "b": np.array([[10, 11, 12], [13, 14, 15]]),
        ...     },
        ...     {"a": np.array([[7], [8]]), "b": np.array([[17], [18]])},
        ... ]
        >>> out = concatenate_along_seq(data)
        >>> out
        {'a': array([[0, 1, 2, 7], [4, 5, 6, 8]]),
         'b': array([[10, 11, 12, 17], [13, 14, 15, 18]])}

        ```
    """
    if not data:
        return {}
    item = data[0]
    return type(item)({key: ba.concatenate_along_seq([d[key] for d in data]) for key in item})


def tile_along_seq(data: Any, reps: int) -> Any:
    r"""Repeat all the arrays along the sequence axis.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.
        reps: The number of repetitions data along the
            sequence axis.

    Returns:
        The arrays repeated along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import tile_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = tile_along_seq(data, 2)
        >>> out
        {'a': array([[0, 1, 2, 3, 4, 0, 1, 2, 3, 4], [5, 6, 7, 8, 9, 5, 6, 7, 8, 9]]),
         'b': array([[4, 3, 2, 1, 0, 4, 3, 2, 1, 0]])}

        ```
    """
    return recursive_apply(data, partial(ba.tile_along_seq, reps=reps))
